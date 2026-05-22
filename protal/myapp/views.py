from collections import defaultdict
import shutil
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Avg, Case, Count, IntegerField, Max, Sum, When
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import AptitudeQuestionForm, PrepTestForm, CodingQuestionForm
from .models import Activity, AptitudeQuestion, AttemptAnswer, PrepTest, Resume, TestAttempt, UserProfile, CodingQuestion, CodingSubmission
from .coding_data import CODING_PROBLEMS


DEFAULT_TESTS = [
    {
        'title': 'Quantitative Aptitude',
        'category': PrepTest.APTITUDE,
        'difficulty': PrepTest.EASY,
        'question_count': 20,
        'duration_minutes': 15,
        'topics': 'Numbers, percentages, profit and loss',
    },
    {
        'title': 'Logical Reasoning',
        'category': PrepTest.APTITUDE,
        'difficulty': PrepTest.MEDIUM,
        'question_count': 20,
        'duration_minutes': 20,
        'topics': 'Series, seating, syllogism',
    },
    {
        'title': 'Data Interpretation',
        'category': PrepTest.APTITUDE,
        'difficulty': PrepTest.HARD,
        'question_count': 20,
        'duration_minutes': 30,
        'topics': 'Charts, tables, data analysis',
    },
    {
        'title': 'DSA Challenge',
        'category': PrepTest.CODING,
        'difficulty': PrepTest.MEDIUM,
        'question_count': 12,
        'duration_minutes': 90,
        'topics': 'Arrays, strings, and recursion',
    },
    {
        'title': 'Python Programming Exam',
        'category': PrepTest.CODING,
        'difficulty': PrepTest.MEDIUM,
        'question_count': 12,
        'duration_minutes': 45,
        'topics': 'Basic math, recursion, dynamic programming in Python',
    },
    {
        'title': 'Java Programming Exam',
        'category': PrepTest.CODING,
        'difficulty': PrepTest.MEDIUM,
        'question_count': 12,
        'duration_minutes': 45,
        'topics': 'Strings, stacks, palindromes in Java',
    },
    {
        'title': 'C Programming Exam',
        'category': PrepTest.CODING,
        'difficulty': PrepTest.MEDIUM,
        'question_count': 12,
        'duration_minutes': 45,
        'topics': 'Pointers, searching, memory management in C',
    },
    {
        'title': 'C++ Programming Exam',
        'category': PrepTest.CODING,
        'difficulty': PrepTest.MEDIUM,
        'question_count': 12,
        'duration_minutes': 45,
        'topics': 'Arrays, duplicates, sorting in C++',
    },
    {
        'title': 'JavaScript Programming Exam',
        'category': PrepTest.CODING,
        'difficulty': PrepTest.MEDIUM,
        'question_count': 12,
        'duration_minutes': 45,
        'topics': 'Loops, conditions, brackets in JavaScript',
    },
    {
        'title': 'Aptitude Test',
        'category': PrepTest.MOCK,
        'difficulty': PrepTest.EASY,
        'question_count': 20,
        'duration_minutes': 15,
        'topics': 'Quantitative and reasoning',
    },
    {
        'title': 'Coding Test',
        'category': PrepTest.MOCK,
        'difficulty': PrepTest.MEDIUM,
        'question_count': 5,
        'duration_minutes': 45,
        'topics': 'DSA and problem solving',
    },
    {
        'title': 'Technical Interview',
        'category': PrepTest.MOCK,
        'difficulty': PrepTest.HARD,
        'question_count': 15,
        'duration_minutes': 30,
        'topics': 'HR and technical',
    },
]



APTITUDE_QUESTION_BANK = {
    PrepTest.EASY: [
        {'topic': 'Quantitative', 'question_text': 'What is 18 + 27?', 'option_a': '35', 'option_b': '45', 'option_c': '54', 'option_d': '37', 'correct_option': 'B', 'explanation': '18 + 27 = 45.'},
        {'topic': 'Quantitative', 'question_text': 'What is 25% of 200?', 'option_a': '25', 'option_b': '40', 'option_c': '50', 'option_d': '75', 'correct_option': 'C', 'explanation': '25% is one-fourth, and one-fourth of 200 is 50.'},
        {'topic': 'Quantitative', 'question_text': 'The ratio of boys to girls is 3:2. If there are 50 students, how many boys are there?', 'option_a': '20', 'option_b': '25', 'option_c': '30', 'option_d': '35', 'correct_option': 'C', 'explanation': '3 out of 5 parts are boys, so 3/5 of 50 is 30.'},
        {'topic': 'Quantitative', 'question_text': 'Find the average of 10, 20, and 30.', 'option_a': '15', 'option_b': '20', 'option_c': '25', 'option_d': '30', 'correct_option': 'B', 'explanation': '(10 + 20 + 30) / 3 = 20.'},
        {'topic': 'Quantitative', 'question_text': 'A pen bought for 100 is sold for 120. What is the profit percentage?', 'option_a': '10%', 'option_b': '15%', 'option_c': '20%', 'option_d': '25%', 'correct_option': 'C', 'explanation': 'Profit is 20 on cost price 100, so profit percentage is 20%.'},
        {'topic': 'Quantitative', 'question_text': 'What is 7 x 8?', 'option_a': '48', 'option_b': '54', 'option_c': '56', 'option_d': '64', 'correct_option': 'C', 'explanation': '7 multiplied by 8 is 56.'},
        {'topic': 'Reasoning', 'question_text': 'Complete the series: 2, 4, 6, 8, ?', 'option_a': '9', 'option_b': '10', 'option_c': '11', 'option_d': '12', 'correct_option': 'B', 'explanation': 'The series increases by 2 each time.'},
        {'topic': 'Reasoning', 'question_text': 'Choose the odd one out: Cat, Dog, Cow, Car.', 'option_a': 'Cat', 'option_b': 'Dog', 'option_c': 'Cow', 'option_d': 'Car', 'correct_option': 'D', 'explanation': 'Car is not an animal.'},
        {'topic': 'Reasoning', 'question_text': 'If A is greater than B, and B is greater than C, which statement is true?', 'option_a': 'C is greater than A', 'option_b': 'A is greater than C', 'option_c': 'A equals C', 'option_d': 'B is less than C', 'correct_option': 'B', 'explanation': 'If A > B and B > C, then A > C.'},
        {'topic': 'Quantitative', 'question_text': 'Three bottles contain 2 liters each. How many liters are there in total?', 'option_a': '4', 'option_b': '5', 'option_c': '6', 'option_d': '8', 'correct_option': 'C', 'explanation': '3 x 2 = 6 liters.'},
        {'topic': 'Quantitative', 'question_text': 'Find simple interest on 1000 at 10% per year for 2 years.', 'option_a': '100', 'option_b': '150', 'option_c': '200', 'option_d': '250', 'correct_option': 'C', 'explanation': 'SI = PRT/100 = 1000 x 10 x 2 / 100 = 200.'},
        {'topic': 'Quantitative', 'question_text': 'A person travels 15 km in 3 hours. What is the speed?', 'option_a': '3 km/h', 'option_b': '4 km/h', 'option_c': '5 km/h', 'option_d': '6 km/h', 'correct_option': 'C', 'explanation': 'Speed = distance / time = 15 / 3 = 5 km/h.'},
        {'topic': 'Quantitative', 'question_text': 'Evaluate 12 + 6 / 3.', 'option_a': '6', 'option_b': '14', 'option_c': '18', 'option_d': '24', 'correct_option': 'B', 'explanation': 'Divide first: 6 / 3 = 2, then 12 + 2 = 14.'},
        {'topic': 'Reasoning', 'question_text': 'What day comes immediately after Monday?', 'option_a': 'Sunday', 'option_b': 'Tuesday', 'option_c': 'Friday', 'option_d': 'Saturday', 'correct_option': 'B', 'explanation': 'Tuesday comes after Monday.'},
        {'topic': 'Quantitative', 'question_text': 'What is 40% of 150?', 'option_a': '45', 'option_b': '50', 'option_c': '60', 'option_d': '75', 'correct_option': 'C', 'explanation': '40% of 150 is 60.'},
        {'topic': 'Quantitative', 'question_text': 'What is 5 squared?', 'option_a': '10', 'option_b': '20', 'option_c': '25', 'option_d': '30', 'correct_option': 'C', 'explanation': '5 squared means 5 x 5 = 25.'},
        {'topic': 'Data Interpretation', 'question_text': 'A chart shows 12 apples sold in the morning and 8 in the evening. How many apples were sold in total?', 'option_a': '16', 'option_b': '18', 'option_c': '20', 'option_d': '22', 'correct_option': 'C', 'explanation': '12 + 8 = 20.'},
        {'topic': 'Quantitative', 'question_text': 'Find the perimeter of a square with side 5 cm.', 'option_a': '10 cm', 'option_b': '15 cm', 'option_c': '20 cm', 'option_d': '25 cm', 'correct_option': 'C', 'explanation': 'Perimeter of a square is 4 x side = 20 cm.'},
        {'topic': 'Data Interpretation', 'question_text': 'In a table, the values are 0.25, 0.5, 0.75, and 1. Which is the smallest?', 'option_a': '0.25', 'option_b': '0.5', 'option_c': '0.75', 'option_d': '1', 'correct_option': 'A', 'explanation': '0.25 is the smallest value.'},
        {'topic': 'Quantitative', 'question_text': '9 + ? = 15. Find the missing number.', 'option_a': '4', 'option_b': '5', 'option_c': '6', 'option_d': '7', 'correct_option': 'C', 'explanation': '15 - 9 = 6.'},
    ],
    PrepTest.MEDIUM: [
        {'topic': 'Quantitative', 'question_text': 'A product costs 800 and is sold at a 15% profit. Find the selling price.', 'option_a': '880', 'option_b': '900', 'option_c': '920', 'option_d': '950', 'correct_option': 'C', 'explanation': '15% of 800 is 120, so selling price is 920.'},
        {'topic': 'Quantitative', 'question_text': 'The average of 6 numbers is 15. A seventh number is added and the average becomes 16. What is the seventh number?', 'option_a': '18', 'option_b': '20', 'option_c': '22', 'option_d': '24', 'correct_option': 'C', 'explanation': 'Old total is 90. New total is 112. The added number is 22.'},
        {'topic': 'Quantitative', 'question_text': 'Two numbers are in the ratio 5:7 and their sum is 96. Find the larger number.', 'option_a': '40', 'option_b': '48', 'option_c': '56', 'option_d': '64', 'correct_option': 'C', 'explanation': '12 parts = 96, so 1 part = 8. Larger number is 7 x 8 = 56.'},
        {'topic': 'Quantitative', 'question_text': 'Find simple interest on 5000 at 8% per year for 3 years.', 'option_a': '800', 'option_b': '1000', 'option_c': '1200', 'option_d': '1400', 'correct_option': 'C', 'explanation': 'SI = 5000 x 8 x 3 / 100 = 1200.'},
        {'topic': 'Reasoning', 'question_text': 'Complete the series: 3, 6, 11, 18, 27, ?', 'option_a': '34', 'option_b': '36', 'option_c': '38', 'option_d': '40', 'correct_option': 'C', 'explanation': 'Differences are 3, 5, 7, 9, so the next difference is 11.'},
        {'topic': 'Reasoning', 'question_text': 'If ACE is coded as 135, how is BED coded?', 'option_a': '254', 'option_b': '245', 'option_c': '524', 'option_d': '452', 'correct_option': 'A', 'explanation': 'Use alphabet positions: B=2, E=5, D=4.'},
        {'topic': 'Reasoning', 'question_text': 'If North becomes East after a right turn, what direction does East become after a right turn?', 'option_a': 'North', 'option_b': 'South', 'option_c': 'West', 'option_d': 'East', 'correct_option': 'B', 'explanation': 'A right turn from East faces South.'},
        {'topic': 'Quantitative', 'question_text': 'A bag has 3 red balls and 2 blue balls. What is the probability of picking a red ball?', 'option_a': '2/5', 'option_b': '3/5', 'option_c': '1/2', 'option_d': '4/5', 'correct_option': 'B', 'explanation': 'There are 3 red balls out of 5 total balls.'},
        {'topic': 'Quantitative', 'question_text': 'A can finish work in 10 days and B in 15 days. How many days will they take together?', 'option_a': '5', 'option_b': '6', 'option_c': '8', 'option_d': '12', 'correct_option': 'B', 'explanation': 'Together rate is 1/10 + 1/15 = 1/6, so they take 6 days.'},
        {'topic': 'Quantitative', 'question_text': 'A car travels 150 km at 60 km/h. Find the time taken.', 'option_a': '2 hours', 'option_b': '2.5 hours', 'option_c': '3 hours', 'option_d': '3.5 hours', 'correct_option': 'B', 'explanation': 'Time = 150 / 60 = 2.5 hours.'},
        {'topic': 'Quantitative', 'question_text': 'A value increases from 80 to 100. What is the percentage increase?', 'option_a': '20%', 'option_b': '25%', 'option_c': '30%', 'option_d': '40%', 'correct_option': 'B', 'explanation': 'Increase is 20 on base 80, so 20/80 x 100 = 25%.'},
        {'topic': 'Data Interpretation', 'question_text': 'Sales on Monday, Tuesday, and Wednesday are 20, 30, and 40. What is the average sales value?', 'option_a': '25', 'option_b': '30', 'option_c': '35', 'option_d': '40', 'correct_option': 'B', 'explanation': '(20 + 30 + 40) / 3 = 30.'},
        {'topic': 'Data Interpretation', 'question_text': 'Store A sold 120 units and Store B sold 80 units. What is the ratio A:B?', 'option_a': '2:3', 'option_b': '3:2', 'option_c': '4:5', 'option_d': '5:4', 'correct_option': 'B', 'explanation': '120:80 simplifies to 3:2.'},
        {'topic': 'Reasoning', 'question_text': 'All roses are flowers. Some flowers are red. Which conclusion definitely follows?', 'option_a': 'All flowers are roses', 'option_b': 'All roses are flowers', 'option_c': 'All roses are red', 'option_d': 'No flower is red', 'correct_option': 'B', 'explanation': 'The first statement directly says all roses are flowers.'},
        {'topic': 'Quantitative', 'question_text': 'Find the LCM of 12 and 18.', 'option_a': '24', 'option_b': '30', 'option_c': '36', 'option_d': '48', 'correct_option': 'C', 'explanation': 'The least common multiple of 12 and 18 is 36.'},
        {'topic': 'Quantitative', 'question_text': 'Find the HCF of 24 and 36.', 'option_a': '6', 'option_b': '8', 'option_c': '12', 'option_d': '18', 'correct_option': 'C', 'explanation': 'The greatest common factor is 12.'},
        {'topic': 'Quantitative', 'question_text': 'Find the compound amount on 1000 at 10% per year for 2 years.', 'option_a': '1100', 'option_b': '1200', 'option_c': '1210', 'option_d': '1220', 'correct_option': 'C', 'explanation': 'Amount = 1000 x 1.1 x 1.1 = 1210.'},
        {'topic': 'Reasoning', 'question_text': 'What is the angle between hour and minute hands at 3:00?', 'option_a': '45 degrees', 'option_b': '60 degrees', 'option_c': '90 degrees', 'option_d': '120 degrees', 'correct_option': 'C', 'explanation': 'At 3:00, the hands are perpendicular.'},
        {'topic': 'Quantitative', 'question_text': 'How many ways can 5 people stand in a line?', 'option_a': '25', 'option_b': '60', 'option_c': '100', 'option_d': '120', 'correct_option': 'D', 'explanation': '5 people can be arranged in 5! = 120 ways.'},
        {'topic': 'Data Interpretation', 'question_text': 'Find the median of 2, 5, 8, 11, and 14.', 'option_a': '5', 'option_b': '8', 'option_c': '9', 'option_d': '11', 'correct_option': 'B', 'explanation': 'The middle value is 8.'},
    ],
    PrepTest.HARD: [
        {'topic': 'Quantitative', 'question_text': 'A train 120 m long travels at 54 km/h. How long will it take to cross a pole?', 'option_a': '6 seconds', 'option_b': '8 seconds', 'option_c': '10 seconds', 'option_d': '12 seconds', 'correct_option': 'B', 'explanation': '54 km/h = 15 m/s. Time = 120 / 15 = 8 seconds.'},
        {'topic': 'Quantitative', 'question_text': 'A can do a job in 12 days and B in 18 days. How long will they take together?', 'option_a': '6.2 days', 'option_b': '7.2 days', 'option_c': '8.2 days', 'option_d': '9.2 days', 'correct_option': 'B', 'explanation': 'Together rate is 1/12 + 1/18 = 5/36, so time is 36/5 = 7.2 days.'},
        {'topic': 'Quantitative', 'question_text': 'A 20 liter mixture has 30% acid. If 10 liters of water is added, what is the new acid percentage?', 'option_a': '15%', 'option_b': '18%', 'option_c': '20%', 'option_d': '25%', 'correct_option': 'C', 'explanation': 'Acid remains 6 liters in 30 liters total, so 20%.'},
        {'topic': 'Quantitative', 'question_text': 'An item marked 1000 is sold after 20% discount at a 25% profit. Find the cost price.', 'option_a': '600', 'option_b': '640', 'option_c': '700', 'option_d': '750', 'correct_option': 'B', 'explanation': 'Selling price is 800. If this is 125% of CP, CP is 640.'},
        {'topic': 'Reasoning', 'question_text': 'How many distinct arrangements can be made from the letters of LEVEL?', 'option_a': '20', 'option_b': '30', 'option_c': '40', 'option_d': '60', 'correct_option': 'B', 'explanation': '5 letters with L repeated twice and E repeated twice: 5!/(2!2!) = 30.'},
        {'topic': 'Quantitative', 'question_text': 'What is the probability of getting exactly two heads in three coin tosses?', 'option_a': '1/8', 'option_b': '1/4', 'option_c': '3/8', 'option_d': '1/2', 'correct_option': 'C', 'explanation': 'There are 3 favorable outcomes out of 8 total outcomes.'},
        {'topic': 'Reasoning', 'question_text': 'Complete the series: 5, 11, 23, 47, 95, ?', 'option_a': '171', 'option_b': '181', 'option_c': '191', 'option_d': '201', 'correct_option': 'C', 'explanation': 'Each term is previous x 2 + 1, so 95 x 2 + 1 = 191.'},
        {'topic': 'Reasoning', 'question_text': 'If all managers are leaders and some leaders are mentors, which conclusion is valid?', 'option_a': 'All mentors are managers', 'option_b': 'All managers are leaders', 'option_c': 'No leader is a manager', 'option_d': 'Some managers are mentors definitely', 'correct_option': 'B', 'explanation': 'The definite conclusion is exactly given by the first statement.'},
        {'topic': 'Data Interpretation', 'question_text': 'A company sold 120 units in January and 180 in March. What is the percentage growth?', 'option_a': '40%', 'option_b': '45%', 'option_c': '50%', 'option_d': '60%', 'correct_option': 'C', 'explanation': 'Growth is 60 on 120, which is 50%.'},
        {'topic': 'Data Interpretation', 'question_text': '40 students average 60 marks. Another 10 students average 80 marks. Find the combined average.', 'option_a': '62', 'option_b': '64', 'option_c': '66', 'option_d': '68', 'correct_option': 'B', 'explanation': 'Total marks are 2400 + 800 = 3200 for 50 students. Average is 64.'},
        {'topic': 'Quantitative', 'question_text': 'A invests 5000 for 12 months and B invests 8000 for 9 months. What is their profit ratio?', 'option_a': '5:6', 'option_b': '6:5', 'option_c': '4:5', 'option_d': '5:4', 'correct_option': 'A', 'explanation': 'Capital time products are 60000 and 72000, simplifying to 5:6.'},
        {'topic': 'Quantitative', 'question_text': 'A boat travels downstream at 20 km/h and upstream at 12 km/h. Find the speed of the boat in still water.', 'option_a': '14 km/h', 'option_b': '16 km/h', 'option_c': '18 km/h', 'option_d': '20 km/h', 'correct_option': 'B', 'explanation': 'Still water speed = (20 + 12) / 2 = 16 km/h.'},
        {'topic': 'Quantitative', 'question_text': 'A person travels 120 km at 40 km/h and returns at 60 km/h. Find the average speed for the whole trip.', 'option_a': '45 km/h', 'option_b': '48 km/h', 'option_c': '50 km/h', 'option_d': '52 km/h', 'correct_option': 'B', 'explanation': 'Total distance is 240 km and total time is 3 + 2 = 5 hours. Average speed is 48 km/h.'},
        {'topic': 'Reasoning', 'question_text': 'Father is three times as old as his son. After 10 years, father will be twice as old as son. What is the son age now?', 'option_a': '8', 'option_b': '10', 'option_c': '12', 'option_d': '15', 'correct_option': 'B', 'explanation': 'Let son be S. 3S + 10 = 2(S + 10), so S = 10.'},
        {'topic': 'Reasoning', 'question_text': 'In how many ways can 6 people sit around a circular table?', 'option_a': '60', 'option_b': '100', 'option_c': '120', 'option_d': '720', 'correct_option': 'C', 'explanation': 'Circular arrangements of 6 people are (6 - 1)! = 120.'},
        {'topic': 'Data Interpretation', 'question_text': 'A table lists expenses as 1200, 1500, 1800, and 2100. What is the range?', 'option_a': '600', 'option_b': '700', 'option_c': '800', 'option_d': '900', 'correct_option': 'D', 'explanation': 'Range is maximum minus minimum: 2100 - 1200 = 900.'},
        {'topic': 'Quantitative', 'question_text': 'Which number is divisible by 9?', 'option_a': '5841', 'option_b': '5842', 'option_c': '5843', 'option_d': '5845', 'correct_option': 'A', 'explanation': 'Digits of 5841 sum to 18, which is divisible by 9.'},
        {'topic': 'Quantitative', 'question_text': 'A pipe fills a tank in 12 hours and another pipe empties it in 18 hours. If both are open, when will the tank fill?', 'option_a': '24 hours', 'option_b': '30 hours', 'option_c': '36 hours', 'option_d': '42 hours', 'correct_option': 'C', 'explanation': 'Net rate is 1/12 - 1/18 = 1/36.'},
        {'topic': 'Quantitative', 'question_text': 'Find compound interest on 10000 at 10% per year for 2 years.', 'option_a': '2000', 'option_b': '2100', 'option_c': '2200', 'option_d': '2400', 'correct_option': 'B', 'explanation': 'Amount is 12100, so compound interest is 2100.'},
        {'topic': 'Data Interpretation', 'question_text': 'A data set has values 15, 20, 20, 25, and 40. What is the mode?', 'option_a': '15', 'option_b': '20', 'option_c': '25', 'option_d': '40', 'correct_option': 'B', 'explanation': '20 appears most often.'},
    ],
}

APTITUDE_TOPICS = ['Quantitative', 'Reasoning', 'Data Interpretation']


superuser_required = user_passes_test(lambda user: user.is_superuser, login_url='site_admin_login')


def ensure_default_tests():
    for test in DEFAULT_TESTS:
        PrepTest.objects.get_or_create(title=test['title'], category=test['category'], defaults=test)
    ensure_default_aptitude_questions()
    ensure_default_coding_questions()


def ensure_default_coding_questions():
    exams_map = {
        'DSA Challenge': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        'Python Programming Exam': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'Java Programming Exam': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        'C Programming Exam': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        'C++ Programming Exam': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0],
        'JavaScript Programming Exam': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1],
    }
    
    for exam_title, question_indices in exams_map.items():
        test = PrepTest.objects.filter(title=exam_title, category=PrepTest.CODING).first()
        if not test:
            continue
        
        if test.coding_questions.exists():
            if test.coding_questions.count() == len(question_indices):
                continue
            test.coding_questions.all().delete()
            
        for order, idx in enumerate(question_indices, start=1):
            prob = CODING_PROBLEMS[idx]
            CodingQuestion.objects.create(
                test=test,
                order=order,
                title=prob['title'],
                description=prob['description'],
                difficulty=prob['difficulty'],
                input_format=prob['input_format'],
                output_format=prob['output_format'],
                sample_input=prob['sample_input'],
                sample_output=prob['sample_output'],
                test_cases=prob['test_cases'],
                starter_code_python=prob['starter_code_python'],
                starter_code_java=prob['starter_code_java'],
                starter_code_cpp=prob['starter_code_cpp'],
                starter_code_c=prob['starter_code_c'],
                starter_code_js=prob['starter_code_js'],
            )
            
        test.question_count = test.coding_questions.count()
        test.save(update_fields=['question_count'])


def ensure_default_aptitude_questions():
    aptitude_tests = PrepTest.objects.filter(category=PrepTest.APTITUDE, is_active=True)

    for test in aptitude_tests:
        if test.aptitude_questions.exists():
            continue

        question_bank = APTITUDE_QUESTION_BANK.get(test.difficulty, [])
        created_any = False

        for order, question in enumerate(question_bank, start=1):
            _, created = AptitudeQuestion.objects.get_or_create(
                test=test,
                order=order,
                defaults=question,
            )
            created_any = created_any or created

        if created_any:
            test.question_count = test.aptitude_questions.count()
            test.save(update_fields=['question_count'])


def record_activity(user, title, status='Completed'):
    if user.is_authenticated:
        Activity.objects.create(user=user, title=title, status=status)


def calculate_resume_score(data):
    fields = ['full_name', 'email', 'phone', 'location', 'links', 'summary', 'skills', 'projects', 'experience', 'degree']
    filled = sum(1 for field in fields if data.get(field))
    return min(100, filled * 10)


def get_aptitude_attempts(user):
    if not user.is_authenticated:
        return TestAttempt.objects.none()

    return TestAttempt.objects.filter(
        user=user,
        test__category=PrepTest.APTITUDE,
        status=TestAttempt.COMPLETED,
    )


def get_aptitude_stats(user):
    attempts = get_aptitude_attempts(user)
    answers = AttemptAnswer.objects.filter(attempt__in=attempts)

    topic_rows = answers.values('question__topic').annotate(
        total=Count('id'),
        correct=Sum(
            Case(
                When(is_correct=True, then=1),
                default=0,
                output_field=IntegerField(),
            )
        ),
    )

    topic_progress = {
        topic: {'topic': topic, 'total': 0, 'correct': 0, 'score': 0}
        for topic in APTITUDE_TOPICS
    }

    for row in topic_rows:
        topic = row['question__topic']
        total = row['total'] or 0
        correct = row['correct'] or 0
        topic_progress[topic] = {
            'topic': topic,
            'total': total,
            'correct': correct,
            'score': round((correct / total) * 100) if total else 0,
        }

    aggregate = attempts.aggregate(
        completed=Count('id'),
        average=Avg('score'),
        best=Max('score'),
        solved=Sum('total_questions'),
    )

    return {
        'tests_completed': aggregate['completed'] or 0,
        'average_score': round(aggregate['average'] or 0),
        'best_score': aggregate['best'] or 0,
        'questions_solved': aggregate['solved'] or 0,
        'topic_progress': list(topic_progress.values()),
        'latest_attempt': attempts.first(),
    }


def option_text(question, option):
    return {
        'A': question.option_a,
        'B': question.option_b,
        'C': question.option_c,
        'D': question.option_d,
    }.get(option, 'Not answered')


def sync_test_question_count(test):
    if test:
        if test.category == PrepTest.APTITUDE:
            test.question_count = test.aptitude_questions.count()
        elif test.category == PrepTest.CODING:
            test.question_count = test.coding_questions.count()
        test.save(update_fields=['question_count'])


def safe_admin_next(request):
    next_url = request.POST.get('next') or request.GET.get('next') or reverse('site_admin_dashboard')

    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return next_url

    return reverse('site_admin_dashboard')


def site_admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('site_admin_dashboard')

    next_url = safe_admin_next(request)

    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user_record = (
            User.objects.filter(username=identifier).first()
            or User.objects.filter(email__iexact=identifier).first()
        )
        username = user_record.username if user_record else identifier
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid admin username or password.')
            return redirect(f"{reverse('site_admin_login')}?{urlencode({'next': next_url})}")

        if not user.is_superuser:
            messages.error(request, 'Only superusers can access the admin dashboard.')
            return redirect(f"{reverse('site_admin_login')}?{urlencode({'next': next_url})}")

        login(request, user)
        messages.success(request, 'Admin login successful.')
        return redirect(next_url)

    return render(request, 'site_admin/login.html', {'next_url': next_url})


@superuser_required
def site_admin_dashboard(request):
    ensure_default_tests()
    stats = {
        'users': User.objects.count(),
        'tests': PrepTest.objects.count(),
        'questions': AptitudeQuestion.objects.count() + CodingQuestion.objects.count(),
        'attempts': TestAttempt.objects.count(),
        'resumes': Resume.objects.count(),
    }
    recent_attempts = TestAttempt.objects.select_related('user', 'test')[:8]
    recent_questions = AptitudeQuestion.objects.select_related('test').order_by('-id')[:8]

    return render(request, 'site_admin/dashboard.html', {
        'stats': stats,
        'recent_attempts': recent_attempts,
        'recent_questions': recent_questions,
    })


@superuser_required
def site_admin_tests(request):
    ensure_default_tests()
    category = request.GET.get('category', '')
    tests = PrepTest.objects.all().order_by('category', 'difficulty', 'title')

    if category:
        tests = tests.filter(category=category)

    return render(request, 'site_admin/tests.html', {
        'tests': tests,
        'category': category,
        'categories': PrepTest.CATEGORY_CHOICES,
    })


@superuser_required
def site_admin_test_create(request):
    form = PrepTestForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        test = form.save()
        sync_test_question_count(test)
        messages.success(request, 'Test created successfully.')
        return redirect('site_admin_tests')

    return render(request, 'site_admin/test_form.html', {
        'form': form,
        'title': 'Create Test',
    })


@superuser_required
def site_admin_test_update(request, test_id):
    test = get_object_or_404(PrepTest, pk=test_id)
    form = PrepTestForm(request.POST or None, instance=test)

    if request.method == 'POST' and form.is_valid():
        test = form.save()
        sync_test_question_count(test)
        messages.success(request, 'Test updated successfully.')
        return redirect('site_admin_tests')

    return render(request, 'site_admin/test_form.html', {
        'form': form,
        'title': 'Edit Test',
        'test': test,
    })


@superuser_required
def site_admin_test_delete(request, test_id):
    test = get_object_or_404(PrepTest, pk=test_id)

    if request.method == 'POST':
        test.delete()
        messages.success(request, 'Test deleted successfully.')
        return redirect('site_admin_tests')

    return render(request, 'site_admin/confirm_delete.html', {
        'object_name': test.title,
        'object_type': 'test',
        'cancel_url': reverse('site_admin_tests'),
    })


@superuser_required
def site_admin_questions(request):
    ensure_default_tests()
    test_id = request.GET.get('test', '')
    questions = AptitudeQuestion.objects.select_related('test').order_by('test__difficulty', 'test__title', 'order')
    tests = PrepTest.objects.filter(category=PrepTest.APTITUDE).order_by('difficulty', 'title')

    if test_id:
        questions = questions.filter(test_id=test_id)

    return render(request, 'site_admin/questions.html', {
        'questions': questions,
        'tests': tests,
        'test_id': test_id,
    })


@superuser_required
def site_admin_question_create(request):
    initial = {}
    test_id = request.GET.get('test')

    if test_id:
        initial['test'] = test_id

    form = AptitudeQuestionForm(request.POST or None, initial=initial)

    if request.method == 'POST' and form.is_valid():
        question = form.save()
        sync_test_question_count(question.test)
        messages.success(request, 'Question created successfully.')
        return redirect('site_admin_questions')

    return render(request, 'site_admin/question_form.html', {
        'form': form,
        'title': 'Create Aptitude Question',
    })


@superuser_required
def site_admin_question_update(request, question_id):
    question = get_object_or_404(AptitudeQuestion.objects.select_related('test'), pk=question_id)
    old_test = question.test
    form = AptitudeQuestionForm(request.POST or None, instance=question)

    if request.method == 'POST' and form.is_valid():
        question = form.save()
        sync_test_question_count(old_test)
        sync_test_question_count(question.test)
        messages.success(request, 'Question updated successfully.')
        return redirect('site_admin_questions')

    return render(request, 'site_admin/question_form.html', {
        'form': form,
        'title': 'Edit Aptitude Question',
        'question': question,
    })


@superuser_required
def site_admin_question_delete(request, question_id):
    question = get_object_or_404(AptitudeQuestion.objects.select_related('test'), pk=question_id)
    test = question.test

    if request.method == 'POST':
        question.delete()
        sync_test_question_count(test)
        messages.success(request, 'Question deleted successfully.')
        return redirect('site_admin_questions')

    return render(request, 'site_admin/confirm_delete.html', {
        'object_name': f'{question.test.title} Q{question.order}',
        'object_type': 'question',
        'cancel_url': reverse('site_admin_questions'),
    })


@superuser_required
def site_admin_coding_questions(request):
    ensure_default_tests()
    test_id = request.GET.get('test', '')
    questions = CodingQuestion.objects.select_related('test').order_by('test__difficulty', 'test__title', 'order')
    tests = PrepTest.objects.filter(category=PrepTest.CODING).order_by('difficulty', 'title')

    if test_id:
        questions = questions.filter(test_id=test_id)

    return render(request, 'site_admin/coding_questions.html', {
        'questions': questions,
        'tests': tests,
        'test_id': test_id,
    })


@superuser_required
def site_admin_coding_question_create(request):
    initial = {}
    test_id = request.GET.get('test')

    if test_id:
        initial['test'] = test_id

    form = CodingQuestionForm(request.POST or None, initial=initial)

    if request.method == 'POST' and form.is_valid():
        question = form.save()
        sync_test_question_count(question.test)
        messages.success(request, 'Coding question created successfully.')
        return redirect('site_admin_coding_questions')

    return render(request, 'site_admin/coding_question_form.html', {
        'form': form,
        'title': 'Create Coding Question',
    })


@superuser_required
def site_admin_coding_question_update(request, question_id):
    question = get_object_or_404(CodingQuestion.objects.select_related('test'), pk=question_id)
    old_test = question.test
    form = CodingQuestionForm(request.POST or None, instance=question)

    if request.method == 'POST' and form.is_valid():
        question = form.save()
        sync_test_question_count(old_test)
        sync_test_question_count(question.test)
        messages.success(request, 'Coding question updated successfully.')
        return redirect('site_admin_coding_questions')

    return render(request, 'site_admin/coding_question_form.html', {
        'form': form,
        'title': 'Edit Coding Question',
        'question': question,
    })


@superuser_required
def site_admin_coding_question_delete(request, question_id):
    question = get_object_or_404(CodingQuestion.objects.select_related('test'), pk=question_id)
    test = question.test

    if request.method == 'POST':
        question.delete()
        sync_test_question_count(test)
        messages.success(request, 'Coding question deleted successfully.')
        return redirect('site_admin_coding_questions')

    return render(request, 'site_admin/confirm_delete.html', {
        'object_name': f'{question.test.title} Q{question.order} ({question.title})',
        'object_type': 'question',
        'cancel_url': reverse('site_admin_coding_questions'),
    })


def first(request):
    return render(request, 'first.html')


def getstarted(request):
    return render(request, 'getstarted.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'register':
            full_name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip().lower()
            password = request.POST.get('password', '')

            if not full_name or not email or not password:
                messages.error(request, 'Please fill all register fields.')
                return redirect('login')

            if User.objects.filter(username=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return redirect('login')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name,
            )
            UserProfile.objects.create(user=user)
            login(request, user)
            record_activity(user, 'Created account', 'Success')
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')

        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Please fill all login fields.')
            return redirect('login')

        user = authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

        login(request, user)
        messages.success(request, 'Logged in successfully.')
        return redirect('dashboard')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


def get_coding_stats(user):
    if not user or not user.is_authenticated:
        return {
            'easy_solved': 0, 'easy_total': 0, 'easy_percent': 0,
            'medium_solved': 0, 'medium_total': 0, 'medium_percent': 0,
            'hard_solved': 0, 'hard_total': 0, 'hard_percent': 0,
            'languages': [],
        }

    total_questions = CodingQuestion.objects.all()
    easy_total = total_questions.filter(difficulty=PrepTest.EASY).count()
    medium_total = total_questions.filter(difficulty=PrepTest.MEDIUM).count()
    hard_total = total_questions.filter(difficulty=PrepTest.HARD).count()

    passed_subs = CodingSubmission.objects.filter(
        attempt__user=user,
        status='Passed'
    )
    
    solved_q_ids = passed_subs.values_list('question_id', flat=True).distinct()
    solved_questions = CodingQuestion.objects.filter(id__in=solved_q_ids)

    easy_solved = solved_questions.filter(difficulty=PrepTest.EASY).count()
    medium_solved = solved_questions.filter(difficulty=PrepTest.MEDIUM).count()
    hard_solved = solved_questions.filter(difficulty=PrepTest.HARD).count()

    easy_percent = round((easy_solved / easy_total) * 100) if easy_total else 0
    medium_percent = round((medium_solved / medium_total) * 100) if medium_total else 0
    hard_percent = round((hard_solved / hard_total) * 100) if hard_total else 0

    lang_counts = passed_subs.values('language').annotate(count=Count('id'))
    languages = []
    lang_titles = {
        'python': 'Python',
        'java': 'Java',
        'cpp': 'C++',
        'c': 'C',
        'javascript': 'JavaScript'
    }
    
    total_lang_subs = sum(item['count'] for item in lang_counts)
    for item in lang_counts:
        lang_key = item['language']
        count = item['count']
        languages.append({
            'name': lang_titles.get(lang_key, lang_key.title()),
            'count': count,
            'percent': round((count / total_lang_subs) * 100) if total_lang_subs else 0
        })

    return {
        'easy_solved': easy_solved,
        'easy_total': easy_total,
        'easy_percent': easy_percent,
        'medium_solved': medium_solved,
        'medium_total': medium_total,
        'medium_percent': medium_percent,
        'hard_solved': hard_solved,
        'hard_total': hard_total,
        'hard_percent': hard_percent,
        'languages': languages,
    }


@login_required(login_url='login')
def dashboard(request):
    ensure_default_tests()
    attempts = TestAttempt.objects.filter(user=request.user)
    completed_tests = attempts.count()
    average_score = attempts.aggregate(score=Avg('score'))['score'] or 0
    coding_score = attempts.filter(test__category=PrepTest.CODING).aggregate(score=Avg('score'))['score'] or 0
    mock_score = attempts.filter(test__category=PrepTest.MOCK).aggregate(score=Avg('score'))['score'] or 0
    resume = Resume.objects.filter(user=request.user).first()
    activities = Activity.objects.filter(user=request.user)[:6]
    
    coding_stats = get_coding_stats(request.user)

    context = {
        'completed_tests': completed_tests,
        'average_score': round(average_score),
        'coding_score': round(coding_score),
        'mock_score': round(mock_score),
        'resume_score': resume.ats_score if resume else 0,
        'activities': activities,
        'coding_stats': coding_stats,
    }
    return render(request, 'dashboard.html', context)


def aptitude(request):
    ensure_default_tests()
    tests = PrepTest.objects.filter(category=PrepTest.APTITUDE, is_active=True)
    stats = get_aptitude_stats(request.user)
    return render(request, 'aptitude.html', {'tests': tests, **stats})


def coding(request):
    ensure_default_tests()
    tests = PrepTest.objects.filter(category=PrepTest.CODING, is_active=True)
    stats = get_coding_stats(request.user)
    return render(request, 'coding.html', {'tests': tests, 'daily_test': tests.first(), **stats})


@login_required(login_url='login')
def resume(request):
    resume_obj = Resume.objects.filter(user=request.user).first()

    if request.method == 'POST':
        data = {
            'full_name': request.POST.get('full_name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'location': request.POST.get('location', '').strip(),
            'links': request.POST.get('links', '').strip(),
            'summary': request.POST.get('summary', '').strip(),
            'skills': request.POST.get('skills', '').strip(),
            'projects': request.POST.get('projects', '').strip(),
            'experience': request.POST.get('experience', '').strip(),
            'degree': request.POST.get('degree', '').strip(),
            'graduation': request.POST.get('graduation', '').strip(),
        }

        if not data['full_name'] or not data['email']:
            messages.error(request, 'Full name and email are required.')
            return redirect('resume')

        data['ats_score'] = calculate_resume_score(data)
        Resume.objects.update_or_create(user=request.user, defaults=data)
        record_activity(request.user, 'Updated resume', 'Updated')
        messages.success(request, 'Resume saved successfully.')
        return redirect('resume')

    return render(request, 'resume.html', {'resume': resume_obj})


def mocktest(request):
    ensure_default_tests()
    tests = PrepTest.objects.filter(category=PrepTest.MOCK, is_active=True)
    total_attempts = TestAttempt.objects.count()
    user_attempts = TestAttempt.objects.filter(user=request.user) if request.user.is_authenticated else TestAttempt.objects.none()
    stats = {
        'tests_completed': user_attempts.count(),
        'average_score': round(user_attempts.aggregate(score=Avg('score'))['score'] or 0),
        'mock_interviews': user_attempts.filter(test__title__icontains='interview').count(),
        'questions_solved': user_attempts.aggregate(total=Count('id'))['total'] or total_attempts,
    }
    return render(request, 'mocktest.html', {'tests': tests, 'stats': stats})


@login_required(login_url='login')
def take_aptitude_test(request, attempt_id):
    ensure_default_tests()
    attempt = get_object_or_404(
        TestAttempt.objects.select_related('test'),
        pk=attempt_id,
        user=request.user,
        test__category=PrepTest.APTITUDE,
    )

    if attempt.status == TestAttempt.COMPLETED:
        return redirect('aptitude_result', attempt_id=attempt.id)

    questions = list(attempt.test.aptitude_questions.all())

    if not questions:
        messages.error(request, 'Questions are not available for this test yet.')
        return redirect('aptitude')

    if request.method == 'POST':
        AttemptAnswer.objects.filter(attempt=attempt).delete()
        topic_totals = defaultdict(lambda: {'correct': 0, 'total': 0})
        correct_answers = 0

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}', '')
            is_correct = selected_option == question.correct_option

            if is_correct:
                correct_answers += 1
                topic_totals[question.topic]['correct'] += 1

            topic_totals[question.topic]['total'] += 1

            AttemptAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct,
            )

        total_questions = len(questions)
        score = round((correct_answers / total_questions) * 100)
        topic_breakdown = {}

        for topic, totals in topic_totals.items():
            topic_total = totals['total']
            topic_correct = totals['correct']
            topic_breakdown[topic] = {
                'total': topic_total,
                'correct': topic_correct,
                'score': round((topic_correct / topic_total) * 100) if topic_total else 0,
            }

        attempt.status = TestAttempt.COMPLETED
        attempt.score = score
        attempt.correct_answers = correct_answers
        attempt.total_questions = total_questions
        attempt.topic_breakdown = topic_breakdown
        attempt.completed_at = timezone.now()
        attempt.save(update_fields=[
            'status',
            'score',
            'correct_answers',
            'total_questions',
            'topic_breakdown',
            'completed_at',
        ])

        record_activity(request.user, f'Completed {attempt.test.title}', f'{score}%')
        messages.success(request, f'Test submitted. You scored {score}%.')
        return redirect('aptitude_result', attempt_id=attempt.id)

    return render(request, 'aptitude_test.html', {
        'attempt': attempt,
        'test': attempt.test,
        'questions': questions,
    })


@login_required(login_url='login')
def aptitude_result(request, attempt_id):
    attempt = get_object_or_404(
        TestAttempt.objects.select_related('test'),
        pk=attempt_id,
        user=request.user,
        test__category=PrepTest.APTITUDE,
    )

    if attempt.status != TestAttempt.COMPLETED:
        return redirect('take_aptitude_test', attempt_id=attempt.id)

    answers = list(attempt.answers.select_related('question'))

    for answer in answers:
        answer.selected_text = option_text(answer.question, answer.selected_option)
        answer.correct_text = option_text(answer.question, answer.question.correct_option)

    topic_breakdown = [
        {'topic': topic, **data}
        for topic, data in attempt.topic_breakdown.items()
    ]
    strengths = [item for item in topic_breakdown if item['score'] >= 75]
    focus_areas = [item for item in topic_breakdown if item['score'] < 60]

    return render(request, 'aptitude_result.html', {
        'attempt': attempt,
        'answers': answers,
        'incorrect_answers': attempt.total_questions - attempt.correct_answers,
        'topic_breakdown': topic_breakdown,
        'strengths': strengths,
        'focus_areas': focus_areas,
    })


@login_required(login_url='login')
def start_test(request, test_id):
    ensure_default_tests()
    test = get_object_or_404(PrepTest, pk=test_id, is_active=True)

    if request.method != 'POST':
        if test.category == PrepTest.MOCK:
            return redirect('mocktest')
        return redirect(test.category)

    if test.category == PrepTest.APTITUDE:
        question_count = test.aptitude_questions.count()
    elif test.category == PrepTest.CODING:
        question_count = test.coding_questions.count()
    else:
        question_count = 0

    attempt = TestAttempt.objects.create(user=request.user, test=test, score=0, total_questions=question_count)
    record_activity(request.user, f'Started {test.title}', 'Started')

    if test.category == PrepTest.APTITUDE:
        return redirect('take_aptitude_test', attempt_id=attempt.id)
    if test.category == PrepTest.CODING:
        return redirect('take_coding_test', attempt_id=attempt.id)
    if test.category == PrepTest.MOCK:
        messages.success(request, f'{test.title} started.')
        return redirect('mocktest')
    messages.success(request, f'{test.title} started.')
    return redirect(test.category)


import subprocess
import tempfile
import os
import sys
import shutil

def run_user_code(language, code, input_data, question_title):
    # Normalize input line endings
    input_data = input_data.replace('\r\n', '\n')
    
    # 1. Check if compiler is available. If not, use simulator!
    use_simulator = False
    if language == 'java' and not shutil.which('javac'):
        use_simulator = True
    elif language in ['c', 'cpp'] and not shutil.which('gcc') and not shutil.which('g++') and not shutil.which('clang') and not shutil.which('clang++'):
        use_simulator = True
    elif language == 'javascript' and not shutil.which('node'):
        use_simulator = True
        
    if use_simulator:
        return run_simulated_code(question_title, input_data)

    # 2. Run actual code
    with tempfile.TemporaryDirectory() as tmpdir:
        if language == 'python':
            filepath = os.path.join(tmpdir, 'solution.py')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            cmd = [sys.executable, filepath]
            
        elif language == 'javascript':
            filepath = os.path.join(tmpdir, 'solution.js')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            cmd = ['node', filepath]
            
        elif language == 'java':
            filepath = os.path.join(tmpdir, 'Main.java')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            compile_res = subprocess.run(['javac', 'Main.java'], cwd=tmpdir, capture_output=True, text=True, timeout=10)
            if compile_res.returncode != 0:
                return {
                    'status': 'Compile Error',
                    'output': '',
                    'error': compile_res.stderr or compile_res.stdout
                }
            cmd = ['java', 'Main']
            
        elif language == 'cpp':
            filepath = os.path.join(tmpdir, 'solution.cpp')
            binary = os.path.join(tmpdir, 'solution.exe' if os.name == 'nt' else 'solution')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            compiler = 'g++' if shutil.which('g++') else ('clang++' if shutil.which('clang++') else None)
            if not compiler:
                return run_simulated_code(question_title, input_data)
                
            compile_res = subprocess.run([compiler, '-O3', 'solution.cpp', '-o', binary], cwd=tmpdir, capture_output=True, text=True, timeout=10)
            if compile_res.returncode != 0:
                return {
                    'status': 'Compile Error',
                    'output': '',
                    'error': compile_res.stderr or compile_res.stdout
                }
            cmd = [binary]
            
        elif language == 'c':
            filepath = os.path.join(tmpdir, 'solution.c')
            binary = os.path.join(tmpdir, 'solution.exe' if os.name == 'nt' else 'solution')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            compiler = 'gcc' if shutil.which('gcc') else ('clang' if shutil.which('clang') else None)
            if not compiler:
                return run_simulated_code(question_title, input_data)
                
            compile_res = subprocess.run([compiler, '-O3', 'solution.c', '-o', binary], cwd=tmpdir, capture_output=True, text=True, timeout=10)
            if compile_res.returncode != 0:
                return {
                    'status': 'Compile Error',
                    'output': '',
                    'error': compile_res.stderr or compile_res.stdout
                }
            cmd = [binary]
        else:
            return {'status': 'Error', 'output': '', 'error': f'Unsupported language: {language}'}

        try:
            run_res = subprocess.run(cmd, input=input_data, capture_output=True, text=True, timeout=5)
            if run_res.returncode != 0:
                return {
                    'status': 'Runtime Error',
                    'output': run_res.stdout,
                    'error': run_res.stderr
                }
            return {
                'status': 'Success',
                'output': run_res.stdout,
                'error': ''
            }
        except subprocess.TimeoutExpired:
            return {
                'status': 'Time Limit Exceeded',
                'output': '',
                'error': 'Execution timed out after 5 seconds.'
            }
        except Exception as e:
            return {
                'status': 'Runtime Error',
                'output': '',
                'error': str(e)
            }


def run_simulated_code(question_title, input_data):
    inputs = input_data.strip()
    try:
        if question_title == 'Sum of Two Numbers':
            output = str(sum(map(int, inputs.split())))
        elif question_title == 'Reverse a String':
            output = inputs[::-1]
        elif question_title == 'Palindrome Check':
            clean = inputs.lower()
            output = "Yes" if clean == clean[::-1] else "No"
        elif question_title == 'FizzBuzz':
            n = int(inputs)
            res = []
            for i in range(1, n + 1):
                if i % 15 == 0: res.append("FizzBuzz")
                elif i % 3 == 0: res.append("Fizz")
                elif i % 5 == 0: res.append("Buzz")
                else: res.append(str(i))
            output = " ".join(res)
        elif question_title == 'Factorial of a Number':
            import math
            output = str(math.factorial(int(inputs)))
        elif question_title == 'Fibonacci Sequence':
            n = int(inputs)
            if n == 0: output = "0"
            elif n == 1: output = "1"
            else:
                a, b = 0, 1
                for _ in range(2, n + 1):
                    a, b = b, a + b
                output = str(b)
        elif question_title == 'Balanced Parentheses':
            stack = []
            mapping = {")": "(", "}": "{", "]": "["}
            is_bal = "Balanced"
            for char in inputs:
                if char in mapping:
                    top = stack.pop() if stack else '#'
                    if mapping[char] != top:
                        is_bal = "Not Balanced"
                        break
                elif char in ['(', '{', '[']:
                    stack.append(char)
            if stack:
                is_bal = "Not Balanced"
            output = is_bal
        elif question_title == 'Binary Search':
            lines = inputs.splitlines()
            parts = lines[0].split()
            target = int(parts[1])
            arr = [int(x) for x in lines[1].split()]
            try:
                output = str(arr.index(target))
            except ValueError:
                output = "-1"
        elif question_title == 'Find Duplicates':
            lines = inputs.splitlines()
            arr = [int(x) for x in lines[1].split()]
            seen = set()
            dups = set()
            for x in arr:
                if x in seen:
                    dups.add(x)
                seen.add(x)
            if not dups:
                output = "None"
            else:
                output = " ".join(str(x) for x in sorted(list(dups)))
        elif question_title == 'Anagram Checker':
            lines = inputs.splitlines()
            s1 = sorted(list(lines[0].strip().lower()))
            s2 = sorted(list(lines[1].strip().lower()))
            output = "Yes" if s1 == s2 else "No"
        elif question_title == 'Edit Distance':
            lines = inputs.splitlines()
            s1 = lines[0].strip()
            s2 = lines[1].strip()
            m, n = len(s1), len(s2)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(m + 1):
                for j in range(n + 1):
                    if i == 0: dp[i][j] = j
                    elif j == 0: dp[i][j] = i
                    elif s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1]
                    else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
            output = str(dp[m][n])
        elif question_title == 'Longest Palindromic Substring':
            s = inputs
            if not s:
                output = ""
            else:
                start, end = 0, 0
                def expand(left, right):
                    while left >= 0 and right < len(s) and s[left] == s[right]:
                        left -= 1
                        right += 1
                    return right - left - 1
                for i in range(len(s)):
                    l1 = expand(i, i)
                    l2 = expand(i, i + 1)
                    l = max(l1, l2)
                    if l > end - start:
                        start = i - (l - 1) // 2
                        end = i + l // 2
                output = s[start:end+1]
        elif question_title == 'Trapping Rain Water':
            lines = inputs.splitlines()
            arr = [int(x) for x in lines[1].split()]
            if not arr:
                output = "0"
            else:
                l, r = 0, len(arr) - 1
                l_max, r_max = 0, 0
                ans = 0
                while l < r:
                    if arr[l] < arr[r]:
                        if arr[l] >= l_max: l_max = arr[l]
                        else: ans += l_max - arr[l]
                        l += 1
                    else:
                        if arr[r] >= r_max: r_max = arr[r]
                        else: ans += r_max - arr[r]
                        r -= 1
                output = str(ans)
        elif question_title == 'Median of Two Sorted Arrays':
            lines = inputs.splitlines()
            parts = lines[0].split()
            n, m = int(parts[0]), int(parts[1])
            a = [int(x) for x in lines[1].split()] if n > 0 else []
            b = [int(x) for x in lines[2].split()] if m > 0 else []
            merged = sorted(a + b)
            length = len(merged)
            if length % 2 == 1:
                res = float(merged[length // 2])
            else:
                res = (merged[length // 2 - 1] + merged[length // 2]) / 2.0
            output = f"{res:.1f}"
        elif question_title == 'Longest Valid Parentheses':
            st = [-1]
            ans = 0
            for i, char in enumerate(inputs):
                if char == '(':
                    st.append(i)
                else:
                    st.pop()
                    if not st:
                        st.append(i)
                    else:
                        ans = max(ans, i - st[-1])
            output = str(ans)
        else:
            return {'status': 'Error', 'output': '', 'error': 'Unknown question.'}
            
        return {
            'status': 'Success',
            'output': output + '\n',
            'error': ''
        }
    except Exception as e:
        return {
            'status': 'Runtime Error',
            'output': '',
            'error': f'Simulation error: {str(e)}'
        }


from django.http import JsonResponse

@login_required(login_url='login')
def take_coding_test(request, attempt_id):
    ensure_default_tests()
    attempt = get_object_or_404(
        TestAttempt.objects.select_related('test'),
        pk=attempt_id,
        user=request.user,
        test__category=PrepTest.CODING,
    )

    if attempt.status == TestAttempt.COMPLETED:
        return redirect('coding_result', attempt_id=attempt.id)

    questions = list(attempt.test.coding_questions.all().order_by('order'))
    if not questions:
        messages.error(request, 'No questions found for this exam.')
        return redirect('coding')

    # Calculate remaining time
    elapsed_time = timezone.now() - attempt.started_at
    total_seconds = attempt.test.duration_minutes * 60
    seconds_left = max(0, total_seconds - int(elapsed_time.total_seconds()))

    latest_subs = {}
    for q in questions:
        latest_sub = CodingSubmission.objects.filter(attempt=attempt, question=q).order_by('-submitted_at').first()
        if latest_sub:
            latest_subs[str(q.id)] = {
                'code': latest_sub.code,
                'language': latest_sub.language,
                'status': latest_sub.status
            }

    default_lang = 'python'
    title_lower = attempt.test.title.lower()
    if 'java' in title_lower:
        default_lang = 'java'
    elif 'c++' in title_lower:
        default_lang = 'cpp'
    elif 'javascript' in title_lower or 'js' in title_lower:
        default_lang = 'javascript'
    elif ' c ' in title_lower or title_lower.startswith('c '):
        default_lang = 'c'

    questions_data = {}
    for q in questions:
        questions_data[str(q.id)] = {
            'title': q.title,
            'python': q.starter_code_python,
            'java': q.starter_code_java,
            'cpp': q.starter_code_cpp,
            'c': q.starter_code_c,
            'javascript': q.starter_code_js,
        }

    return render(request, 'coding_test.html', {
        'attempt': attempt,
        'test': attempt.test,
        'questions': questions,
        'latest_subs': latest_subs,
        'default_lang': default_lang,
        'seconds_left': seconds_left,
        'questions_data': questions_data,
    })


@login_required(login_url='login')
def run_code(request, attempt_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    attempt = get_object_or_404(TestAttempt, pk=attempt_id, user=request.user)
    question_id = request.POST.get('question_id')
    language = request.POST.get('language')
    code = request.POST.get('code')
    custom_input = request.POST.get('custom_input', '').strip()

    question = get_object_or_404(CodingQuestion, pk=question_id, test=attempt.test)
    is_custom = bool(custom_input)
    input_data = custom_input if is_custom else question.sample_input
    
    result = run_user_code(language, code, input_data, question.title)
    
    compiler_map = {
        'java': 'javac',
        'cpp': 'g++',
        'c': 'gcc',
        'javascript': 'node',
        'python': 'python'
    }
    required_bin = compiler_map.get(language, '')
    is_simulated = required_bin and not shutil.which(required_bin)
    result['simulated'] = is_simulated

    if result.get('status') == 'Success':
        actual = result.get('output', '').strip()
        expected = question.sample_output.strip()
        if not is_custom:
            if actual == expected:
                result['verification'] = 'Correct'
                result['expected'] = expected
            else:
                result['verification'] = 'Wrong'
                result['expected'] = expected
        else:
            result['verification'] = 'Custom input run (no auto-verification)'

    return JsonResponse(result)


@login_required(login_url='login')
def submit_code(request, attempt_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    attempt = get_object_or_404(TestAttempt, pk=attempt_id, user=request.user)
    question_id = request.POST.get('question_id')
    language = request.POST.get('language')
    code = request.POST.get('code')

    question = get_object_or_404(CodingQuestion, pk=question_id, test=attempt.test)
    test_cases = question.test_cases
    total_cases = len(test_cases)
    passed_cases = 0
    compile_err = ''
    runtime_err = ''
    time_limit_err = False

    for tc in test_cases:
        res = run_user_code(language, code, tc['input'], question.title)
        if res['status'] == 'Success':
            expected = tc['output'].strip()
            actual = res['output'].strip()
            if actual == expected:
                passed_cases += 1
        elif res['status'] == 'Compile Error':
            compile_err = res['error']
            break
        elif res['status'] == 'Runtime Error':
            runtime_err = res['error']
        elif res['status'] == 'Time Limit Exceeded':
            time_limit_err = True

    if compile_err:
        status = 'Compile Error'
    elif time_limit_err:
        status = 'Time Limit Exceeded'
    elif passed_cases == total_cases:
        status = 'Passed'
    else:
        status = 'Failed'

    CodingSubmission.objects.create(
        attempt=attempt,
        question=question,
        language=language,
        code=code,
        status=status,
        passed_cases=passed_cases,
        total_cases=total_cases
    )

    return JsonResponse({
        'status': status,
        'passed_cases': passed_cases,
        'total_cases': total_cases,
        'compile_error': compile_err,
        'runtime_error': runtime_err,
    })


@login_required(login_url='login')
def submit_coding_exam(request, attempt_id):
    if request.method != 'POST':
        return redirect('coding')

    attempt = get_object_or_404(
        TestAttempt.objects.select_related('test'),
        pk=attempt_id,
        user=request.user,
        test__category=PrepTest.CODING,
    )

    if attempt.status == TestAttempt.COMPLETED:
        return redirect('coding_result', attempt_id=attempt.id)

    questions = attempt.test.coding_questions.all()
    total_questions = questions.count()
    passed_questions = 0

    for q in questions:
        has_passed = CodingSubmission.objects.filter(attempt=attempt, question=q, status='Passed').exists()
        if has_passed:
            passed_questions += 1

    score = round((passed_questions / total_questions) * 100) if total_questions else 0

    attempt.status = TestAttempt.COMPLETED
    attempt.score = score
    attempt.correct_answers = passed_questions
    attempt.total_questions = total_questions
    attempt.completed_at = timezone.now()
    attempt.save(update_fields=['status', 'score', 'correct_answers', 'total_questions', 'completed_at'])

    record_activity(request.user, f'Completed {attempt.test.title}', f'{score}%')
    messages.success(request, f'Exam submitted. You scored {score}%.')

    return redirect('coding_result', attempt_id=attempt.id)


@login_required(login_url='login')
def coding_result(request, attempt_id):
    attempt = get_object_or_404(
        TestAttempt.objects.select_related('test'),
        pk=attempt_id,
        user=request.user,
        test__category=PrepTest.CODING,
    )

    if attempt.status != TestAttempt.COMPLETED:
        return redirect('take_coding_test', attempt_id=attempt.id)

    questions = attempt.test.coding_questions.all().order_by('order')
    q_results = []

    for q in questions:
        latest_sub = CodingSubmission.objects.filter(attempt=attempt, question=q).order_by('-submitted_at').first()
        q_results.append({
            'question': q,
            'submission': latest_sub
        })

    return render(request, 'coding_result.html', {
        'attempt': attempt,
        'test': attempt.test,
        'q_results': q_results,
    })
