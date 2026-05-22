# coding_data.py
# Standardized definitions for 15 coding questions.

CODING_PROBLEMS = [
    # EASY PROBLEMS
    {
        'title': 'Sum of Two Numbers',
        'difficulty': 'easy',
        'description': 'Write a program that takes two integers as input and prints their sum.',
        'input_format': 'A single line containing two space-separated integers, A and B.',
        'output_format': 'Print the sum of A and B.',
        'sample_input': '10 20',
        'sample_output': '30',
        'test_cases': [
            {'input': '10 20\n', 'output': '30\n'},
            {'input': '5 7\n', 'output': '12\n'},
            {'input': '-3 8\n', 'output': '5\n'},
            {'input': '0 0\n', 'output': '0\n'},
            {'input': '100 200\n', 'output': '300\n'},
        ],
        'starter_code_python': """import sys

def solve(a, b):
    # Write your code here
    return a + b

if __name__ == '__main__':
    lines = sys.stdin.read().split()
    if len(lines) >= 2:
        a = int(lines[0])
        b = int(lines[1])
        print(solve(a, b))
""",
        'starter_code_java': """import java.util.Scanner;

public class Main {
    public static int solve(int a, int b) {
        // Write your code here
        return a + b;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int a = sc.nextInt();
            int b = sc.nextInt();
            System.out.println(solve(a, b));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>

using namespace std;

int solve(int a, int b) {
    // Write your code here
    return a + b;
}

int main() {
    int a, b;
    if (cin >> a >> b) {
        cout << solve(a, b) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>

int solve(int a, int b) {
    // Write your code here
    return a + b;
}

int main() {
    int a, b;
    if (scanf("%d %d", &a, &b) == 2) {
        printf("%d\\n", solve(a, b));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(a, b) {
    // Write your code here
    return a + b;
}

const input = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/);
if (input.length >= 2) {
    const a = parseInt(input[0], 10);
    const b = parseInt(input[1], 10);
    console.log(solve(a, b));
}
"""
    },
    {
        'title': 'Reverse a String',
        'difficulty': 'easy',
        'description': 'Given a string, print its reversed version.',
        'input_format': 'A single line containing the string S.',
        'output_format': 'Print the reversed string.',
        'sample_input': 'hello',
        'sample_output': 'olleh',
        'test_cases': [
            {'input': 'hello\n', 'output': 'olleh\n'},
            {'input': 'world\n', 'output': 'dlrow\n'},
            {'input': 'a\n', 'output': 'a\n'},
            {'input': 'PrepNova\n', 'output': 'avoNperP\n'},
            {'input': '12345\n', 'output': '54321\n'},
        ],
        'starter_code_python': """import sys

def solve(s):
    # Write your code here
    return s[::-1]

if __name__ == '__main__':
    s = sys.stdin.read().strip()
    print(solve(s))
""",
        'starter_code_java': """import java.util.Scanner;

public class Main {
    public static String solve(String s) {
        // Write your code here
        return new StringBuilder(s).reverse().toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextLine()) {
            String s = sc.nextLine().trim();
            System.out.println(solve(s));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

string solve(string s) {
    // Write your code here
    reverse(s.begin(), s.end());
    return s;
}

int main() {
    string s;
    if (getline(cin, s)) {
        // Remove potential trailing carriage returns in Windows
        if (!s.empty() && s.back() == '\\r') {
            s.pop_back();
        }
        cout << solve(s) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>
#include <string.h>

void solve(char* s) {
    // Write your code here
    int n = strlen(s);
    for (int i = 0; i < n / 2; i++) {
        char temp = s[i];
        s[i] = s[n - 1 - i];
        s[n - 1 - i] = temp;
    }
}

int main() {
    char s[1000];
    if (fgets(s, sizeof(s), stdin)) {
        s[strcspn(s, "\\r\\n")] = 0; // Strip newline
        solve(s);
        printf("%s\\n", s);
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(s) {
    // Write your code here
    return s.split('').reverse().join('');
}

const input = fs.readFileSync(0, 'utf-8').trim();
console.log(solve(input));
"""
    },
    {
        'title': 'Palindrome Check',
        'difficulty': 'easy',
        'description': 'Determine if a given string is a palindrome. Ignore case differences.',
        'input_format': 'A single line containing the string S.',
        'output_format': 'Print "Yes" if the string is a palindrome, otherwise print "No".',
        'sample_input': 'radar',
        'sample_output': 'Yes',
        'test_cases': [
            {'input': 'radar\n', 'output': 'Yes\n'},
            {'input': 'hello\n', 'output': 'No\n'},
            {'input': 'RaceCar\n', 'output': 'Yes\n'},
            {'input': 'a\n', 'output': 'Yes\n'},
            {'input': 'abccba\n', 'output': 'Yes\n'},
        ],
        'starter_code_python': """import sys

def solve(s):
    # Write your code here
    s = s.lower()
    return "Yes" if s == s[::-1] else "No"

if __name__ == '__main__':
    s = sys.stdin.read().strip()
    print(solve(s))
""",
        'starter_code_java': """import java.util.Scanner;

public class Main {
    public static String solve(String s) {
        // Write your code here
        String clean = s.toLowerCase();
        String rev = new StringBuilder(clean).reverse().toString();
        return clean.equals(rev) ? "Yes" : "No";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextLine()) {
            String s = sc.nextLine().trim();
            System.out.println(solve(s));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

using namespace std;

string solve(string s) {
    // Write your code here
    string clean = s;
    for (char &c : clean) c = tolower(c);
    string rev = clean;
    reverse(rev.begin(), rev.end());
    return (clean == rev) ? "Yes" : "No";
}

int main() {
    string s;
    if (getline(cin, s)) {
        if (!s.empty() && s.back() == '\\r') s.pop_back();
        cout << solve(s) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>
#include <string.h>
#include <ctype.h>

const char* solve(char* s) {
    // Write your code here
    int n = strlen(s);
    int i = 0, j = n - 1;
    while (i < j) {
        if (tolower(s[i]) != tolower(s[j])) {
            return "No";
        }
        i++;
        j--;
    }
    return "Yes";
}

int main() {
    char s[1000];
    if (fgets(s, sizeof(s), stdin)) {
        s[strcspn(s, "\\r\\n")] = 0;
        printf("%s\\n", solve(s));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(s) {
    // Write your code here
    const clean = s.toLowerCase();
    const rev = clean.split('').reverse().join('');
    return clean === rev ? "Yes" : "No";
}

const input = fs.readFileSync(0, 'utf-8').trim();
console.log(solve(input));
"""
    },
    {
        'title': 'FizzBuzz',
        'difficulty': 'easy',
        'description': 'For a given integer N, print space-separated outputs from 1 to N. For multiples of 3, print "Fizz", for multiples of 5, print "Buzz", and for multiples of both, print "FizzBuzz". For other numbers, print the number itself.',
        'input_format': 'An integer N.',
        'output_format': 'Space-separated outputs from 1 to N.',
        'sample_input': '15',
        'sample_output': '1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz',
        'test_cases': [
            {'input': '3\n', 'output': '1 2 Fizz\n'},
            {'input': '5\n', 'output': '1 2 Fizz 4 Buzz\n'},
            {'input': '15\n', 'output': '1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz\n'},
            {'input': '1\n', 'output': '1\n'},
            {'input': '10\n', 'output': '1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz\n'},
        ],
        'starter_code_python': """import sys

def solve(n):
    # Write your code here
    res = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            res.append("FizzBuzz")
        elif i % 3 == 0:
            res.append("Fizz")
        elif i % 5 == 0:
            res.append("Buzz")
        else:
            res.append(str(i))
    return " ".join(res)

if __name__ == '__main__':
    line = sys.stdin.read().strip()
    if line:
        n = int(line)
        print(solve(n))
""",
        'starter_code_java': """import java.util.Scanner;
import java.util.ArrayList;

public class Main {
    public static String solve(int n) {
        // Write your code here
        ArrayList<String> list = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            if (i % 15 == 0) list.add("FizzBuzz");
            else if (i % 3 == 0) list.add("Fizz");
            else if (i % 5 == 0) list.add("Buzz");
            else list.add(String.valueOf(i));
        }
        return String.join(" ", list);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            System.out.println(solve(n));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <string>
#include <vector>

using namespace std;

string solve(int n) {
    // Write your code here
    string res = "";
    for (int i = 1; i <= n; i++) {
        if (i > 1) res += " ";
        if (i % 3 == 0 && i % 5 == 0) res += "FizzBuzz";
        else if (i % 3 == 0) res += "Fizz";
        else if (i % 5 == 0) res += "Buzz";
        else res += to_string(i);
    }
    return res;
}

int main() {
    int n;
    if (cin >> n) {
        cout << solve(n) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>

void solve(int n) {
    // Write your code here
    for (int i = 1; i <= n; i++) {
        if (i > 1) printf(" ");
        if (i % 3 == 0 && i % 5 == 0) printf("FizzBuzz");
        else if (i % 3 == 0) printf("Fizz");
        else if (i % 5 == 0) printf("Buzz");
        else printf("%d", i);
    }
    printf("\\n");
}

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        solve(n);
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(n) {
    // Write your code here
    let res = [];
    for (let i = 1; i <= n; i++) {
        if (i % 3 === 0 && i % 5 === 0) res.push("FizzBuzz");
        else if (i % 3 === 0) res.push("Fizz");
        else if (i % 5 === 0) res.push("Buzz");
        else res.push(i.toString());
    }
    return res.join(' ');
}

const input = fs.readFileSync(0, 'utf-8').trim();
if (input) {
    const n = parseInt(input, 10);
    console.log(solve(n));
}
"""
    },
    {
        'title': 'Factorial of a Number',
        'difficulty': 'easy',
        'description': 'Given a non-negative integer N, compute and print its factorial (N!). For N = 0, the factorial is 1.',
        'input_format': 'An integer N (0 <= N <= 12).',
        'output_format': 'Print the value of N!.',
        'sample_input': '5',
        'sample_output': '120',
        'test_cases': [
            {'input': '5\n', 'output': '120\n'},
            {'input': '0\n', 'output': '1\n'},
            {'input': '1\n', 'output': '1\n'},
            {'input': '10\n', 'output': '3628800\n'},
            {'input': '12\n', 'output': '479001600\n'},
        ],
        'starter_code_python': """import sys

def solve(n):
    # Write your code here
    ans = 1
    for i in range(1, n + 1):
        ans *= i
    return ans

if __name__ == '__main__':
    line = sys.stdin.read().strip()
    if line:
        n = int(line)
        print(solve(n))
""",
        'starter_code_java': """import java.util.Scanner;

public class Main {
    public static int solve(int n) {
        // Write your code here
        int ans = 1;
        for (int i = 1; i <= n; i++) {
            ans *= i;
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            System.out.println(solve(n));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>

using namespace std;

long long solve(int n) {
    // Write your code here
    long long ans = 1;
    for (int i = 1; i <= n; i++) {
        ans *= i;
    }
    return ans;
}

int main() {
    int n;
    if (cin >> n) {
        cout << solve(n) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>

long long solve(int n) {
    // Write your code here
    long long ans = 1;
    for (int i = 1; i <= n; i++) {
        ans *= i;
    }
    return ans;
}

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        printf("%lld\\n", solve(n));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(n) {
    // Write your code here
    let ans = 1;
    for (let i = 1; i <= n; i++) {
        ans *= i;
    }
    return ans;
}

const input = fs.readFileSync(0, 'utf-8').trim();
if (input) {
    const n = parseInt(input, 10);
    console.log(solve(n));
}
"""
    },

    # MEDIUM PROBLEMS
    {
        'title': 'Fibonacci Sequence',
        'difficulty': 'medium',
        'description': 'Compute the N-th Fibonacci number. The Fibonacci sequence is defined as F(0) = 0, F(1) = 1, and F(N) = F(N-1) + F(N-2) for N >= 2.',
        'input_format': 'An integer N (0 <= N <= 30).',
        'output_format': 'Print the N-th Fibonacci number.',
        'sample_input': '10',
        'sample_output': '55',
        'test_cases': [
            {'input': '0\n', 'output': '0\n'},
            {'input': '1\n', 'output': '1\n'},
            {'input': '10\n', 'output': '55\n'},
            {'input': '20\n', 'output': '6765\n'},
            {'input': '30\n', 'output': '832040\n'},
        ],
        'starter_code_python': """import sys

def solve(n):
    # Write your code here
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

if __name__ == '__main__':
    line = sys.stdin.read().strip()
    if line:
        n = int(line)
        print(solve(n))
""",
        'starter_code_java': """import java.util.Scanner;

public class Main {
    public static int solve(int n) {
        // Write your code here
        if (n == 0) return 0;
        if (n == 1) return 1;
        int a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            int temp = a + b;
            a = b;
            b = temp;
        }
        return b;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            System.out.println(solve(n));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>

using namespace std;

int solve(int n) {
    // Write your code here
    if (n == 0) return 0;
    if (n == 1) return 1;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

int main() {
    int n;
    if (cin >> n) {
        cout << solve(n) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>

int solve(int n) {
    // Write your code here
    if (n == 0) return 0;
    if (n == 1) return 1;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        printf("%d\\n", solve(n));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(n) {
    // Write your code here
    if (n === 0) return 0;
    if (n === 1) return 1;
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        let temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

const input = fs.readFileSync(0, 'utf-8').trim();
if (input) {
    const n = parseInt(input, 10);
    console.log(solve(n));
}
"""
    },
    {
        'title': 'Balanced Parentheses',
        'difficulty': 'medium',
        'description': 'Given a string containing only standard brackets (), [], and {}, check if the input string is balanced (each opening bracket must have a matching closing bracket of the same type in correct nested order).',
        'input_format': 'A single line containing the string S.',
        'output_format': 'Print "Balanced" if balanced, otherwise print "Not Balanced".',
        'sample_input': '{[()]}',
        'sample_output': 'Balanced',
        'test_cases': [
            {'input': '{[()]}\n', 'output': 'Balanced\n'},
            {'input': '{[(])}\n', 'output': 'Not Balanced\n'},
            {'input': '()\n', 'output': 'Balanced\n'},
            {'input': '((((((()))))))\n', 'output': 'Balanced\n'},
            {'input': '{\n', 'output': 'Not Balanced\n'},
        ],
        'starter_code_python': """import sys

def solve(s):
    # Write your code here
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return "Not Balanced"
        elif char in ['(', '{', '[']:
            stack.append(char)
    return "Balanced" if not stack else "Not Balanced"

if __name__ == '__main__':
    s = sys.stdin.read().strip()
    print(solve(s))
""",
        'starter_code_java': """import java.util.Scanner;
import java.util.Stack;

public class Main {
    public static String solve(String s) {
        // Write your code here
        Stack<Character> stack = new Stack<>();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            } else if (c == ')' || c == '}' || c == ']') {
                if (stack.isEmpty()) return "Not Balanced";
                char top = stack.pop();
                if (c == ')' && top != '(') return "Not Balanced";
                if (c == '}' && top != '{') return "Not Balanced";
                if (c == ']' && top != '[') return "Not Balanced";
            }
        }
        return stack.isEmpty() ? "Balanced" : "Not Balanced";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextLine()) {
            String s = sc.nextLine().trim();
            System.out.println(solve(s));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <string>
#include <stack>

using namespace std;

string solve(string s) {
    // Write your code here
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '{' || c == '[') {
            st.push(c);
        } else if (c == ')' || c == '}' || c == ']') {
            if (st.empty()) return "Not Balanced";
            char top = st.top();
            st.pop();
            if (c == ')' && top != '(') return "Not Balanced";
            if (c == '}' && top != '{') return "Not Balanced";
            if (c == ']' && top != '[') return "Not Balanced";
        }
    }
    return st.empty() ? "Balanced" : "Not Balanced";
}

int main() {
    string s;
    if (getline(cin, s)) {
        if (!s.empty() && s.back() == '\\r') s.pop_back();
        cout << solve(s) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>
#include <string.h>

const char* solve(char* s) {
    // Write your code here
    char stack[1000];
    int top = -1;
    int n = strlen(s);
    for (int i = 0; i < n; i++) {
        char c = s[i];
        if (c == '(' || c == '{' || c == '[') {
            stack[++top] = c;
        } else if (c == ')' || c == '}' || c == ']') {
            if (top == -1) return "Not Balanced";
            char t = stack[top--];
            if (c == ')' && t != '(') return "Not Balanced";
            if (c == '}' && t != '{') return "Not Balanced";
            if (c == ']' && t != '[') return "Not Balanced";
        }
    }
    return (top == -1) ? "Balanced" : "Not Balanced";
}

int main() {
    char s[1000];
    if (fgets(s, sizeof(s), stdin)) {
        s[strcspn(s, "\\r\\n")] = 0;
        printf("%s\\n", solve(s));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(s) {
    // Write your code here
    let stack = [];
    for (let i = 0; i < s.length; i++) {
        let c = s[i];
        if (c === '(' || c === '{' || c === '[') {
            stack.push(c);
        } else if (c === ')' || c === '}' || c === ']') {
            if (stack.length === 0) return "Not Balanced";
            let top = stack.pop();
            if (c === ')' && top !== '(') return "Not Balanced";
            if (c === '}' && top !== '{') return "Not Balanced";
            if (c === ']' && top !== '[') return "Not Balanced";
        }
    }
    return stack.length === 0 ? "Balanced" : "Not Balanced";
}

const input = fs.readFileSync(0, 'utf-8').trim();
console.log(solve(input));
"""
    },
    {
        'title': 'Binary Search',
        'difficulty': 'medium',
        'description': 'Search for a target value in a sorted array of N integers. Return the 0-based index of the target. If the target is not present, return -1.',
        'input_format': 'First line contains two space-separated integers, N and Target. Second line contains N sorted space-separated integers representing the array.',
        'output_format': 'Print the 0-based index of the Target, or -1.',
        'sample_input': '5 30\n10 20 30 40 50',
        'sample_output': '2',
        'test_cases': [
            {'input': '5 30\n10 20 30 40 50\n', 'output': '2\n'},
            {'input': '5 35\n10 20 30 40 50\n', 'output': '-1\n'},
            {'input': '1 10\n10\n', 'output': '0\n'},
            {'input': '6 5\n1 2 3 4 5 6\n', 'output': '4\n'},
            {'input': '4 -1\n-5 -3 -1 2\n', 'output': '2\n'},
        ],
        'starter_code_python': """import sys

def solve(arr, target):
    # Write your code here
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

if __name__ == '__main__':
    lines = sys.stdin.read().splitlines()
    if len(lines) >= 2:
        parts = lines[0].split()
        if len(parts) >= 2:
            n = int(parts[0])
            target = int(parts[1])
            arr = [int(x) for x in lines[1].split()]
            print(solve(arr, target))
""",
        'starter_code_java': """import java.util.Scanner;

public class Main {
    public static int solve(int[] arr, int target) {
        // Write your code here
        int low = 0;
        int high = arr.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) return mid;
            else if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            int target = sc.nextInt();
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = sc.nextInt();
            }
            System.out.println(solve(arr, target));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <vector>

using namespace std;

int solve(const vector<int>& arr, int target) {
    // Write your code here
    int low = 0;
    int high = arr.size() - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int main() {
    int n, target;
    if (cin >> n >> target) {
        vector<int> arr(n);
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
        }
        cout << solve(arr, target) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>

int solve(int arr[], int n, int target) {
    // Write your code here
    int low = 0;
    int high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int main() {
    int n, target;
    if (scanf("%d %d", &n, &target) == 2) {
        int arr[1000];
        for (int i = 0; i < n; i++) {
            scanf("%d", &arr[i]);
        }
        printf("%d\\n", solve(arr, n, target));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(arr, target) {
    // Write your code here
    let low = 0;
    let high = arr.length - 1;
    while (low <= high) {
        let mid = Math.floor((low + high) / 2);
        if (arr[mid] === target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

const input = fs.readFileSync(0, 'utf-8').trim().split(/\\n+/);
if (input.length >= 2) {
    const parts = input[0].trim().split(/\\s+/);
    const n = parseInt(parts[0], 10);
    const target = parseInt(parts[1], 10);
    const arr = input[1].trim().split(/\\s+/).map(x => parseInt(x, 10));
    console.log(solve(arr, target));
}
"""
    },
    {
        'title': 'Find Duplicates',
        'difficulty': 'medium',
        'description': 'Given an array of integers, find all elements that appear more than once. Print them in sorted order. If no duplicates are found, print "None".',
        'input_format': 'First line contains N, the size of the array. Second line contains N space-separated integers.',
        'output_format': 'Print space-separated duplicate elements in ascending order, or "None".',
        'sample_input': '6\n4 3 2 7 8 2',
        'sample_output': '2',
        'test_cases': [
            {'input': '6\n4 3 2 7 8 2\n', 'output': '2\n'},
            {'input': '7\n1 2 3 1 2 3 4\n', 'output': '1 2 3\n'},
            {'input': '5\n1 2 3 4 5\n', 'output': 'None\n'},
            {'input': '3\n5 5 5\n', 'output': '5\n'},
            {'input': '8\n8 3 1 2 8 3 1 2\n', 'output': '1 2 3 8\n'},
        ],
        'starter_code_python': """import sys

def solve(arr):
    # Write your code here
    seen = set()
    dups = set()
    for x in arr:
        if x in seen:
            dups.add(x)
        seen.add(x)
    if not dups:
        return "None"
    return " ".join(str(x) for x in sorted(list(dups)))

if __name__ == '__main__':
    lines = sys.stdin.read().splitlines()
    if len(lines) >= 2:
        arr = [int(x) for x in lines[1].split()]
        print(solve(arr))
""",
        'starter_code_java': """import java.util.*;

public class Main {
    public static String solve(int[] arr) {
        // Write your code here
        HashSet<Integer> seen = new HashSet<>();
        TreeSet<Integer> dups = new TreeSet<>();
        for (int x : arr) {
            if (seen.contains(x)) {
                dups.add(x);
            }
            seen.add(x);
        }
        if (dups.isEmpty()) return "None";
        ArrayList<String> list = new ArrayList<>();
        for (int val : dups) {
            list.add(String.valueOf(val));
        }
        return String.join(" ", list);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = sc.nextInt();
            }
            System.out.println(solve(arr));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <vector>
#include <unordered_set>
#include <set>
#include <string>

using namespace std;

string solve(const vector<int>& arr) {
    // Write your code here
    unordered_set<int> seen;
    set<int> dups;
    for (int x : arr) {
        if (seen.count(x)) {
            dups.insert(x);
        }
        seen.insert(x);
    }
    if (dups.empty()) return "None";
    string res = "";
    for (int x : dups) {
        if (!res.empty()) res += " ";
        res += to_string(x);
    }
    return res;
}

int main() {
    int n;
    if (cin >> n) {
        vector<int> arr(n);
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
        }
        cout << solve(arr) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>
#include <stdlib.h>

int cmp(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

void solve(int arr[], int n) {
    // Write your code here
    qsort(arr, n, sizeof(int), cmp);
    int printed = 0;
    for (int i = 0; i < n - 1; i++) {
        if (arr[i] == arr[i+1]) {
            if (i > 0 && arr[i] == arr[i-1]) continue; // Skip duplicates already printed
            if (printed) printf(" ");
            printf("%d", arr[i]);
            printed = 1;
        }
    }
    if (!printed) printf("None");
    printf("\\n");
}

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        int arr[1000];
        for (int i = 0; i < n; i++) {
            scanf("%d", &arr[i]);
        }
        solve(arr, n);
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(arr) {
    // Write your code here
    let seen = new Set();
    let dups = new Set();
    for (let x of arr) {
        if (seen.has(x)) {
            dups.add(x);
        }
        seen.add(x);
    }
    if (dups.size === 0) return "None";
    return Array.from(dups).sort((a, b) => a - b).join(' ');
}

const input = fs.readFileSync(0, 'utf-8').trim().split(/\\n+/);
if (input.length >= 2) {
    const arr = input[1].trim().split(/\\s+/).map(x => parseInt(x, 10));
    console.log(solve(arr));
}
"""
    },
    {
        'title': 'Anagram Checker',
        'difficulty': 'medium',
        'description': 'Determine if two strings are anagrams of each other (contain the same characters in any order, ignoring case).',
        'input_format': 'Two lines, each containing a string.',
        'output_format': 'Print "Yes" if they are anagrams, otherwise print "No".',
        'sample_input': 'listen\nsilent',
        'sample_output': 'Yes',
        'test_cases': [
            {'input': 'listen\nsilent\n', 'output': 'Yes\n'},
            {'input': 'hello\nbello\n', 'output': 'No\n'},
            {'input': 'Astronomer\nMoonStarrer\n', 'output': 'Yes\n'},
            {'input': 'a\na\n', 'output': 'Yes\n'},
            {'input': 'ab\nba\n', 'output': 'Yes\n'},
        ],
        'starter_code_python': """import sys

def solve(s1, s2):
    # Write your code here
    c1 = sorted(list(s1.lower()))
    c2 = sorted(list(s2.lower()))
    return "Yes" if c1 == c2 else "No"

if __name__ == '__main__':
    lines = sys.stdin.read().splitlines()
    if len(lines) >= 2:
        print(solve(lines[0].strip(), lines[1].strip()))
""",
        'starter_code_java': """import java.util.Scanner;
import java.util.Arrays;

public class Main {
    public static String solve(String s1, String s2) {
        // Write your code here
        char[] c1 = s1.toLowerCase().toCharArray();
        char[] c2 = s2.toLowerCase().toCharArray();
        Arrays.sort(c1);
        Arrays.sort(c2);
        return Arrays.equals(c1, c2) ? "Yes" : "No";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextLine()) {
            String s1 = sc.nextLine().trim();
            if (sc.hasNextLine()) {
                String s2 = sc.nextLine().trim();
                System.out.println(solve(s1, s2));
            }
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

using namespace std;

string solve(string s1, string s2) {
    // Write your code here
    for (char &c : s1) c = tolower(c);
    for (char &c : s2) c = tolower(c);
    sort(s1.begin(), s1.end());
    sort(s2.begin(), s2.end());
    return (s1 == s2) ? "Yes" : "No";
}

int main() {
    string s1, s2;
    if (getline(cin, s1) && getline(cin, s2)) {
        if (!s1.empty() && s1.back() == '\\r') s1.pop_back();
        if (!s2.empty() && s2.back() == '\\r') s2.pop_back();
        cout << solve(s1, s2) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>
#include <string.h>
#include <ctype.h>

void sort_str(char* s) {
    int n = strlen(s);
    for (int i = 0; i < n; i++) {
        s[i] = tolower(s[i]);
    }
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (s[i] > s[j]) {
                char temp = s[i];
                s[i] = s[j];
                s[j] = temp;
            }
        }
    }
}

const char* solve(char* s1, char* s2) {
    // Write your code here
    sort_str(s1);
    sort_str(s2);
    return (strcmp(s1, s2) == 0) ? "Yes" : "No";
}

int main() {
    char s1[1000], s2[1000];
    if (fgets(s1, sizeof(s1), stdin) && fgets(s2, sizeof(s2), stdin)) {
        s1[strcspn(s1, "\\r\\n")] = 0;
        s2[strcspn(s2, "\\r\\n")] = 0;
        printf("%s\\n", solve(s1, s2));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(s1, s2) {
    // Write your code here
    const c1 = s1.toLowerCase().split('').sort().join('');
    const c2 = s2.toLowerCase().split('').sort().join('');
    return c1 === c2 ? "Yes" : "No";
}

const input = fs.readFileSync(0, 'utf-8').trim().split(/\\n+/);
if (input.length >= 2) {
    console.log(solve(input[0].trim(), input[1].trim()));
}
"""
    },

    # HARD PROBLEMS
    {
        'title': 'Edit Distance',
        'difficulty': 'hard',
        'description': 'Given two strings S1 and S2, find the minimum number of operations required to convert S1 to S2. The allowed operations are: Insert a character, Delete a character, or Replace a character.',
        'input_format': 'Two lines, each containing a string.',
        'output_format': 'Print the minimum edit distance.',
        'sample_input': 'horse\nros',
        'sample_output': '3',
        'test_cases': [
            {'input': 'horse\nros\n', 'output': '3\n'},
            {'input': 'intention\nexecution\n', 'output': '5\n'},
            {'input': 'a\n\n', 'output': '1\n'},
            {'input': 'abc\nabc\n', 'output': '0\n'},
            {'input': 'kitten\nsitting\n', 'output': '3\n'},
        ],
        'starter_code_python': """import sys

def solve(s1, s2):
    # Write your code here
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

if __name__ == '__main__':
    lines = sys.stdin.read().splitlines()
    s1 = lines[0].strip() if len(lines) > 0 else ""
    s2 = lines[1].strip() if len(lines) > 1 else ""
    print(solve(s1, s2))
""",
        'starter_code_java': """import java.util.Scanner;

public class Main {
    public static int solve(String s1, String s2) {
        // Write your code here
        int m = s1.length();
        int n = s2.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                if (i == 0) dp[i][j] = j;
                else if (j == 0) dp[i][j] = i;
                else if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(dp[i - 1][j], Math.min(dp[i][j - 1], dp[i - 1][j - 1]));
                }
            }
        }
        return dp[m][n];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s1 = sc.hasNextLine() ? sc.nextLine().trim() : "";
        String s2 = sc.hasNextLine() ? sc.nextLine().trim() : "";
        System.out.println(solve(s1, s2));
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int solve(string s1, string s2) {
    // Write your code here
    int m = s1.length();
    int n = s2.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0) dp[i][j] = j;
            else if (j == 0) dp[i][j] = i;
            else if (s1[i - 1] == s2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
        }
    }
    return dp[m][n];
}

int main() {
    string s1, s2;
    getline(cin, s1);
    getline(cin, s2);
    if (!s1.empty() && s1.back() == '\\r') s1.pop_back();
    if (!s2.empty() && s2.back() == '\\r') s2.pop_back();
    cout << solve(s1, s2) << endl;
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>
#include <string.h>

int min(int a, int b, int c) {
    int m = a < b ? a : b;
    return m < c ? m : c;
}

int solve(char* s1, char* s2) {
    // Write your code here
    int m = strlen(s1);
    int n = strlen(s2);
    int dp[200][200];
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0) dp[i][j] = j;
            else if (j == 0) dp[i][j] = i;
            else if (s1[i - 1] == s2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
        }
    }
    return dp[m][n];
}

int main() {
    char s1[200] = {0}, s2[200] = {0};
    if (fgets(s1, sizeof(s1), stdin)) {
        s1[strcspn(s1, "\\r\\n")] = 0;
    }
    if (fgets(s2, sizeof(s2), stdin)) {
        s2[strcspn(s2, "\\r\\n")] = 0;
    }
    printf("%d\\n", solve(s1, s2));
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(s1, s2) {
    // Write your code here
    const m = s1.length;
    const n = s2.length;
    const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
    for (let i = 0; i <= m; i++) {
        for (let j = 0; j <= n; j++) {
            if (i === 0) dp[i][j] = j;
            else if (j === 0) dp[i][j] = i;
            else if (s1[i - 1] === s2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
        }
    }
    return dp[m][n];
}

const input = fs.readFileSync(0, 'utf-8').split(/\\n+/);
const s1 = input[0] ? input[0].trim() : "";
const s2 = input[1] ? input[1].trim() : "";
console.log(solve(s1, s2));
"""
    },
    {
        'title': 'Longest Palindromic Substring',
        'difficulty': 'hard',
        'description': 'Given a string S, find and print the longest palindromic substring in S. If there are multiple, print the one that starts first.',
        'input_format': 'A single line containing the string S.',
        'output_format': 'Print the longest palindromic substring.',
        'sample_input': 'babad',
        'sample_output': 'bab',
        'test_cases': [
            {'input': 'babad\n', 'output': 'bab\n'},
            {'input': 'cbbd\n', 'output': 'bb\n'},
            {'input': 'a\n', 'output': 'a\n'},
            {'input': 'ac\n', 'output': 'a\n'},
            {'input': 'racecar\n', 'output': 'racecar\n'},
        ],
        'starter_code_python': """import sys

def solve(s):
    # Write your code here
    if not s: return ""
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
    return s[start:end+1]

if __name__ == '__main__':
    s = sys.stdin.read().strip()
    print(solve(s))
""",
        'starter_code_java': """import java.util.Scanner;

public class Main {
    private static int start = 0, maxLen = 0;

    public static String solve(String s) {
        // Write your code here
        int n = s.length();
        if (n < 2) return s;
        start = 0;
        maxLen = 0;
        for (int i = 0; i < n; i++) {
            expand(s, i, i);
            expand(s, i, i + 1);
        }
        return s.substring(start, start + maxLen);
    }

    private static void expand(String s, int left, int right) {
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        if (maxLen < right - left - 1) {
            start = left + 1;
            maxLen = right - left - 1;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextLine()) {
            String s = sc.nextLine().trim();
            System.out.println(solve(s));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

string solve(string s) {
    // Write your code here
    int n = s.length();
    if (n < 2) return s;
    int start = 0, maxLen = 1;
    auto expand = [&](int left, int right) {
        while (left >= 0 && right < n && s[left] == s[right]) {
            left--;
            right++;
        }
        int l = right - left - 1;
        if (l > maxLen) {
            start = left + 1;
            maxLen = l;
        }
    };
    for (int i = 0; i < n; i++) {
        expand(i, i);
        expand(i, i + 1);
    }
    return s.substr(start, maxLen);
}

int main() {
    string s;
    if (getline(cin, s)) {
        if (!s.empty() && s.back() == '\\r') s.pop_back();
        cout << solve(s) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>
#include <string.h>

void solve(char* s, char* res) {
    // Write your code here
    int n = strlen(s);
    if (n == 0) {
        res[0] = 0;
        return;
    }
    int start = 0, maxLen = 1;
    for (int i = 0; i < n; i++) {
        // Odd palindrome
        int l = i, r = i;
        while (l >= 0 && r < n && s[l] == s[r]) {
            if (r - l + 1 > maxLen) {
                start = l;
                maxLen = r - l + 1;
            }
            l--; r++;
        }
        // Even palindrome
        l = i; r = i + 1;
        while (l >= 0 && r < n && s[l] == s[r]) {
            if (r - l + 1 > maxLen) {
                start = l;
                maxLen = r - l + 1;
            }
            l--; r++;
        }
    }
    strncpy(res, s + start, maxLen);
    res[maxLen] = 0;
}

int main() {
    char s[1000], res[1000] = {0};
    if (fgets(s, sizeof(s), stdin)) {
        s[strcspn(s, "\\r\\n")] = 0;
        solve(s, res);
        printf("%s\\n", res);
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(s) {
    // Write your code here
    const n = s.length;
    if (n < 2) return s;
    let start = 0, maxLen = 1;
    function expand(left, right) {
        while (left >= 0 && right < n && s[left] === s[right]) {
            left--;
            right++;
        }
        let l = right - left - 1;
        if (l > maxLen) {
            start = left + 1;
            maxLen = l;
        }
    }
    for (let i = 0; i < n; i++) {
        expand(i, i);
        expand(i, i + 1);
    }
    return s.substring(start, start + maxLen);
}

const input = fs.readFileSync(0, 'utf-8').trim();
console.log(solve(input));
"""
    },
    {
        'title': 'Trapping Rain Water',
        'difficulty': 'hard',
        'description': 'Given N non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.',
        'input_format': 'First line contains N. Second line contains N space-separated integers representing the elevation map.',
        'output_format': 'Print the total units of trapped rain water.',
        'sample_input': '12\n0 1 0 2 1 0 1 3 2 1 2 1',
        'sample_output': '6',
        'test_cases': [
            {'input': '12\n0 1 0 2 1 0 1 3 2 1 2 1\n', 'output': '6\n'},
            {'input': '6\n4 2 0 3 2 5\n', 'output': '9\n'},
            {'input': '3\n3 0 3\n', 'output': '3\n'},
            {'input': '5\n1 2 3 4 5\n', 'output': '0\n'},
            {'input': '1\n10\n', 'output': '0\n'},
        ],
        'starter_code_python': """import sys

def solve(arr):
    # Write your code here
    if not arr: return 0
    l, r = 0, len(arr) - 1
    l_max, r_max = 0, 0
    ans = 0
    while l < r:
        if arr[l] < arr[r]:
            if arr[l] >= l_max:
                l_max = arr[l]
            else:
                ans += l_max - arr[l]
            l += 1
        else:
            if arr[r] >= r_max:
                r_max = arr[r]
            else:
                ans += r_max - arr[r]
            r -= 1
    return ans

if __name__ == '__main__':
    lines = sys.stdin.read().splitlines()
    if len(lines) >= 2:
        arr = [int(x) for x in lines[1].split()]
        print(solve(arr))
""",
        'starter_code_java': """import java.util.Scanner;

public class Main {
    public static int solve(int[] arr) {
        // Write your code here
        int l = 0, r = arr.length - 1;
        int l_max = 0, r_max = 0;
        int ans = 0;
        while (l < r) {
            if (arr[l] < arr[r]) {
                if (arr[l] >= l_max) l_max = arr[l];
                else ans += l_max - arr[l];
                l++;
            } else {
                if (arr[r] >= r_max) r_max = arr[r];
                else ans += r_max - arr[r];
                r--;
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = sc.nextInt();
            }
            System.out.println(solve(arr));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int solve(const vector<int>& arr) {
    // Write your code here
    int l = 0, r = arr.size() - 1;
    int l_max = 0, r_max = 0;
    int ans = 0;
    while (l < r) {
        if (arr[l] < arr[r]) {
            if (arr[l] >= l_max) l_max = arr[l];
            else ans += l_max - arr[l];
            l++;
        } else {
            if (arr[r] >= r_max) r_max = arr[r];
            else ans += r_max - arr[r];
            r--;
        }
    }
    return ans;
}

int main() {
    int n;
    if (cin >> n) {
        vector<int> arr(n);
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
        }
        cout << solve(arr) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>

int solve(int arr[], int n) {
    // Write your code here
    int l = 0, r = n - 1;
    int l_max = 0, r_max = 0;
    int ans = 0;
    while (l < r) {
        if (arr[l] < arr[r]) {
            if (arr[l] >= l_max) l_max = arr[l];
            else ans += l_max - arr[l];
            l++;
        } else {
            if (arr[r] >= r_max) r_max = arr[r];
            else ans += r_max - arr[r];
            r--;
        }
    }
    return ans;
}

int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        int arr[1000];
        for (int i = 0; i < n; i++) {
            scanf("%d", &arr[i]);
        }
        printf("%d\\n", solve(arr, n));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(arr) {
    // Write your code here
    let l = 0, r = arr.length - 1;
    let l_max = 0, r_max = 0;
    let ans = 0;
    while (l < r) {
        if (arr[l] < arr[r]) {
            if (arr[l] >= l_max) l_max = arr[l];
            else ans += l_max - arr[l];
            l++;
        } else {
            if (arr[r] >= r_max) r_max = arr[r];
            else ans += r_max - arr[r];
            r--;
        }
    }
    return ans;
}

const input = fs.readFileSync(0, 'utf-8').trim().split(/\\n+/);
if (input.length >= 2) {
    const arr = input[1].trim().split(/\\s+/).map(x => parseInt(x, 10));
    console.log(solve(arr));
}
"""
    },
    {
        'title': 'Median of Two Sorted Arrays',
        'difficulty': 'hard',
        'description': 'Given two sorted arrays of size N and M respectively, find the median of the combined sorted array. Output the median with one decimal place.',
        'input_format': 'First line contains two space-separated integers, N and M. Second line contains N sorted integers. Third line contains M sorted integers.',
        'output_format': 'Print the median as a float formatted to 1 decimal place (e.g. 2.0 or 2.5).',
        'sample_input': '2 1\n1 3\n2',
        'sample_output': '2.0',
        'test_cases': [
            {'input': '2 1\n1 3\n2\n', 'output': '2.0\n'},
            {'input': '2 2\n1 2\n3 4\n', 'output': '2.5\n'},
            {'input': '0 1\n\n1\n', 'output': '1.0\n'},
            {'input': '4 4\n1 3 5 7\n2 4 6 8\n', 'output': '4.5\n'},
            {'input': '3 2\n1 5 9\n2 6\n', 'output': '5.0\n'},
        ],
        'starter_code_python': """import sys

def solve(a, b):
    # Write your code here
    merged = sorted(a + b)
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n//2])
    else:
        return (merged[n//2 - 1] + merged[n//2]) / 2.0

if __name__ == '__main__':
    lines = sys.stdin.read().splitlines()
    if len(lines) >= 3:
        parts = lines[0].split()
        n, m = int(parts[0]), int(parts[1])
        a = [int(x) for x in lines[1].split()] if n > 0 else []
        b = [int(x) for x in lines[2].split()] if m > 0 else []
        print(f"{solve(a, b):.1f}")
""",
        'starter_code_java': """import java.util.Scanner;
import java.util.Arrays;

public class Main {
    public static double solve(int[] a, int[] b) {
        // Write your code here
        int[] merged = new int[a.length + b.length];
        System.arraycopy(a, 0, merged, 0, a.length);
        System.arraycopy(b, 0, merged, a.length, b.length);
        Arrays.sort(merged);
        int n = merged.length;
        if (n % 2 == 1) {
            return merged[n / 2];
        } else {
            return (merged[n / 2 - 1] + merged[n / 2]) / 2.0;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            int m = sc.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = sc.nextInt();
            int[] b = new int[m];
            for (int i = 0; i < m; i++) b[i] = sc.nextInt();
            System.out.printf("%.1f\\n", solve(a, b));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

double solve(vector<int>& a, vector<int>& b) {
    // Write your code here
    vector<int> merged;
    merged.reserve(a.size() + b.size());
    merged.insert(merged.end(), a.begin(), a.end());
    merged.insert(merged.end(), b.begin(), b.end());
    sort(merged.begin(), merged.end());
    int n = merged.size();
    if (n % 2 == 1) {
        return merged[n / 2];
    } else {
        return (merged[n / 2 - 1] + merged[n / 2]) / 2.0;
    }
}

int main() {
    int n, m;
    if (cin >> n >> m) {
        vector<int> a(n), b(m);
        for (int i = 0; i < n; i++) cin >> a[i];
        for (int i = 0; i < m; i++) cin >> b[i];
        cout << fixed << setprecision(1) << solve(a, b) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>
#include <stdlib.h>

int cmp(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

double solve(int a[], int n, int b[], int m) {
    // Write your code here
    int total = n + m;
    int* merged = (int*)malloc(total * sizeof(int));
    for (int i = 0; i < n; i++) merged[i] = a[i];
    for (int i = 0; i < m; i++) merged[n + i] = b[i];
    qsort(merged, total, sizeof(int), cmp);
    double res;
    if (total % 2 == 1) {
        res = merged[total / 2];
    } else {
        res = (merged[total / 2 - 1] + merged[total / 2]) / 2.0;
    }
    free(merged);
    return res;
}

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) == 2) {
        int a[100], b[100];
        for (int i = 0; i < n; i++) scanf("%d", &a[i]);
        for (int i = 0; i < m; i++) scanf("%d", &b[i]);
        printf("%.1f\\n", solve(a, n, b, m));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(a, b) {
    // Write your code here
    const merged = a.concat(b).sort((x, y) => x - y);
    const n = merged.length;
    if (n % 2 === 1) {
        return merged[Math.floor(n / 2)].toFixed(1);
    } else {
        return ((merged[n / 2 - 1] + merged[n / 2]) / 2.0).toFixed(1);
    }
}

const input = fs.readFileSync(0, 'utf-8').trim().split(/\\n+/);
if (input.length >= 3) {
    const parts = input[0].trim().split(/\\s+/);
    const n = parseInt(parts[0], 10);
    const m = parseInt(parts[1], 10);
    const a = n > 0 ? input[1].trim().split(/\\s+/).map(x => parseInt(x, 10)) : [];
    const b = m > 0 ? input[2].trim().split(/\\s+/).map(x => parseInt(x, 10)) : [];
    console.log(solve(a, b));
}
"""
    },
    {
        'title': 'Longest Valid Parentheses',
        'difficulty': 'hard',
        'description': 'Given a string containing just the characters "(" and ")", find the length of the longest valid (well-formed) parentheses substring.',
        'input_format': 'A single line containing the string S.',
        'output_format': 'Print the length of the longest valid parentheses substring.',
        'sample_input': '(()',
        'sample_output': '2',
        'test_cases': [
            {'input': '(()\n', 'output': '2\n'},
            {'input': ')()())\n', 'output': '4\n'},
            {'input': '\n', 'output': '0\n'},
            {'input': '()(())\n', 'output': '6\n'},
            {'input': '(((())))\n', 'output': '8\n'},
        ],
        'starter_code_python': """import sys

def solve(s):
    # Write your code here
    st = [-1]
    ans = 0
    for i, char in enumerate(s):
        if char == '(':
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)
            else:
                ans = max(ans, i - st[-1])
    return ans

if __name__ == '__main__':
    s = sys.stdin.read().strip()
    print(solve(s))
""",
        'starter_code_java': """import java.util.Scanner;
import java.util.Stack;

public class Main {
    public static int solve(String s) {
        // Write your code here
        Stack<Integer> st = new Stack<>();
        st.push(-1);
        int ans = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(') {
                st.push(i);
            } else {
                st.pop();
                if (st.isEmpty()) {
                    st.push(i);
                } else {
                    ans = Math.max(ans, i - st.peek());
                }
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextLine()) {
            String s = sc.nextLine().trim();
            System.out.println(solve(s));
        }
    }
}
""",
        'starter_code_cpp': """#include <iostream>
#include <string>
#include <stack>
#include <algorithm>

using namespace std;

int solve(string s) {
    // Write your code here
    stack<int> st;
    st.push(-1);
    int ans = 0;
    for (int i = 0; i < s.length(); i++) {
        if (s[i] == '(') {
            st.push(i);
        } else {
            st.pop();
            if (st.empty()) {
                st.push(i);
            } else {
                ans = max(ans, i - st.top());
            }
        }
    }
    return ans;
}

int main() {
    string s;
    if (getline(cin, s)) {
        if (!s.empty() && s.back() == '\\r') s.pop_back();
        cout << solve(s) << endl;
    }
    return 0;
}
""",
        'starter_code_c': """#include <stdio.h>
#include <string.h>

int solve(char* s) {
    // Write your code here
    int stack[1000];
    int top = -1;
    stack[++top] = -1;
    int ans = 0;
    int n = strlen(s);
    for (int i = 0; i < n; i++) {
        if (s[i] == '(') {
            stack[++top] = i;
        } else {
            top--;
            if (top == -1) {
                stack[++top] = i;
            } else {
                int len = i - stack[top];
                if (len > ans) ans = len;
            }
        }
    }
    return ans;
}

int main() {
    char s[1000];
    if (fgets(s, sizeof(s), stdin)) {
        s[strcspn(s, "\\r\\n")] = 0;
        printf("%d\\n", solve(s));
    }
    return 0;
}
""",
        'starter_code_js': """const fs = require('fs');

function solve(s) {
    // Write your code here
    let st = [-1];
    let ans = 0;
    for (let i = 0; i < s.length; i++) {
        if (s[i] === '(') {
            st.push(i);
        } else {
            st.pop();
            if (st.length === 0) {
                st.push(i);
            } else {
                ans = Math.max(ans, i - st[st.length - 1]);
            }
        }
    }
    return ans;
}

const input = fs.readFileSync(0, 'utf-8').trim();
console.log(solve(input));
"""
    }
]
