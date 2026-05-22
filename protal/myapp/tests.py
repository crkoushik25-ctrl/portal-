from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import AptitudeQuestion, AttemptAnswer, PrepTest, Resume, TestAttempt
from .views import ensure_default_tests


class AuthFlowTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('login'), {
            'form_type': 'register',
            'name': 'Test Student',
            'email': 'student@example.com',
            'password': 'StrongPass123',
        })

        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(User.objects.filter(username='student@example.com').exists())

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'form_type': 'login',
            'email': 'missing@example.com',
            'password': 'wrong',
        })

        self.assertRedirects(response, reverse('login'))


class PageBackendTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='student@example.com',
            email='student@example.com',
            password='StrongPass123',
            first_name='Student',
        )

    def test_public_pages_load(self):
        for name in ['first', 'getstarted', 'aptitude', 'coding', 'mocktest']:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_start_test_creates_attempt(self):
        self.client.login(username='student@example.com', password='StrongPass123')
        ensure_default_tests()
        test = PrepTest.objects.filter(category=PrepTest.MOCK).first()

        response = self.client.post(reverse('start_test', args=[test.id]))
        attempt = TestAttempt.objects.get(user=self.user, test=test)

        self.assertRedirects(response, reverse('take_aptitude_test', args=[attempt.id]))
        self.assertTrue(TestAttempt.objects.filter(user=self.user, test=test).exists())

    def test_default_aptitude_tests_have_twenty_questions(self):
        ensure_default_tests()

        for test in PrepTest.objects.filter(category=PrepTest.APTITUDE):
            self.assertEqual(test.question_count, 20)
            self.assertEqual(AptitudeQuestion.objects.filter(test=test).count(), 20)

    def test_aptitude_submission_scores_attempt(self):
        self.client.login(username='student@example.com', password='StrongPass123')
        ensure_default_tests()
        test = PrepTest.objects.get(category=PrepTest.APTITUDE, difficulty=PrepTest.EASY)

        response = self.client.post(reverse('start_test', args=[test.id]))
        attempt = TestAttempt.objects.get(user=self.user, test=test)

        self.assertRedirects(response, reverse('take_aptitude_test', args=[attempt.id]))

        answers = {
            f'question_{question.id}': question.correct_option
            for question in AptitudeQuestion.objects.filter(test=test)
        }
        response = self.client.post(reverse('take_aptitude_test', args=[attempt.id]), answers)

        attempt.refresh_from_db()
        self.assertRedirects(response, reverse('aptitude_result', args=[attempt.id]))
        self.assertEqual(attempt.status, TestAttempt.COMPLETED)
        self.assertEqual(attempt.score, 100)
        self.assertEqual(attempt.correct_answers, 20)
        self.assertEqual(attempt.total_questions, 20)
        self.assertEqual(AttemptAnswer.objects.filter(attempt=attempt, is_correct=True).count(), 20)

    def test_resume_save_creates_resume(self):
        self.client.login(username='student@example.com', password='StrongPass123')

        response = self.client.post(reverse('resume'), {
            'full_name': 'Student One',
            'email': 'student@example.com',
            'phone': '9999999999',
            'location': 'Chennai',
            'links': 'github.com/student',
            'summary': 'Placement ready student.',
            'skills': 'Python, Django',
            'projects': 'PrepNova',
            'experience': 'Internship',
            'degree': 'B.E. CSE',
            'graduation': '2026',
        })

        self.assertRedirects(response, reverse('resume'))
        resume = Resume.objects.get(user=self.user)
        self.assertEqual(resume.full_name, 'Student One')
        self.assertGreater(resume.ats_score, 0)


class SiteAdminTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin@example.com',
            email='admin@example.com',
            password='StrongPass123',
        )
        self.staff = User.objects.create_user(
            username='staff@example.com',
            email='staff@example.com',
            password='StrongPass123',
            is_staff=True,
        )
        self.user = User.objects.create_user(
            username='student@example.com',
            email='student@example.com',
            password='StrongPass123',
        )

    def test_superuser_admin_login_redirects_to_dashboard(self):
        response = self.client.post(reverse('site_admin_login'), {
            'username': 'admin@example.com',
            'password': 'StrongPass123',
            'next': reverse('site_admin_dashboard'),
        })

        self.assertRedirects(response, reverse('site_admin_dashboard'))

    def test_superuser_admin_pages_load(self):
        self.client.login(username='admin@example.com', password='StrongPass123')
        ensure_default_tests()

        for name in ['site_admin_dashboard', 'site_admin_tests', 'site_admin_questions']:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_non_superuser_redirected_to_admin_login(self):
        self.client.login(username='student@example.com', password='StrongPass123')

        response = self.client.get(reverse('site_admin_dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('site_admin_login'), response['Location'])

    def test_staff_without_superuser_is_blocked(self):
        self.client.login(username='staff@example.com', password='StrongPass123')

        response = self.client.get(reverse('site_admin_dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('site_admin_login'), response['Location'])

    def test_superuser_can_update_test_data(self):
        self.client.login(username='admin@example.com', password='StrongPass123')
        ensure_default_tests()
        test = PrepTest.objects.filter(category=PrepTest.MOCK).first()

        response = self.client.post(reverse('site_admin_test_update', args=[test.id]), {
            'title': 'Updated Mock Test',
            'category': PrepTest.MOCK,
            'difficulty': PrepTest.HARD,
            'question_count': 25,
            'duration_minutes': 35,
            'topics': 'Updated topics',
            'is_active': 'on',
        })

        test.refresh_from_db()
        self.assertRedirects(response, reverse('site_admin_tests'))
        self.assertEqual(test.title, 'Updated Mock Test')
        self.assertEqual(test.question_count, 25)

# Create your tests here.
class MockTestRoundsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='student@example.com',
            email='student@example.com',
            password='StrongPass123',
            first_name='Student',
        )
        ensure_default_tests()
        self.aptitude_mock = PrepTest.objects.get(title='Aptitude Test', category=PrepTest.MOCK)
        self.coding_mock = PrepTest.objects.get(title='Coding Test', category=PrepTest.MOCK)
        self.interview_mock = PrepTest.objects.get(title='Technical Interview', category=PrepTest.MOCK)

    def test_mock_test_rounds_locked_by_default_in_view(self):
        self.client.login(username='student@example.com', password='StrongPass123')
        response = self.client.get(reverse('mocktest'))
        
        tests = response.context['tests']
        apt_info = next(t for t in tests if t['title'] == 'Aptitude Test')
        coding_info = next(t for t in tests if t['title'] == 'Coding Test')
        interview_info = next(t for t in tests if t['title'] == 'Technical Interview')

        self.assertFalse(apt_info['is_locked'])
        self.assertTrue(coding_info['is_locked'])
        self.assertTrue(interview_info['is_locked'])

    def test_start_locked_coding_test_fails(self):
        self.client.login(username='student@example.com', password='StrongPass123')
        response = self.client.post(reverse('start_test', args=[self.coding_mock.id]))
        self.assertRedirects(response, reverse('mocktest'))
        self.assertFalse(TestAttempt.objects.filter(user=self.user, test=self.coding_mock).exists())

    def test_passing_aptitude_unlocks_coding(self):
        self.client.login(username='student@example.com', password='StrongPass123')
        TestAttempt.objects.create(
            user=self.user,
            test=self.aptitude_mock,
            score=75,
            status=TestAttempt.COMPLETED
        )

        response = self.client.get(reverse('mocktest'))
        tests = response.context['tests']
        coding_info = next(t for t in tests if t['title'] == 'Coding Test')
        self.assertFalse(coding_info['is_locked'])

        response = self.client.post(reverse('start_test', args=[self.coding_mock.id]))
        attempt = TestAttempt.objects.get(user=self.user, test=self.coding_mock)
        self.assertRedirects(response, reverse('take_coding_test', args=[attempt.id]))
