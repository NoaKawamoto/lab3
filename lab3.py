import unittest
from dataclasses import dataclass, field

@dataclass
class Stack:
    items: list = field(default_factory=list)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def top(self):
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

@dataclass
class Stacks:
    stacks_dict: dict = field(default_factory=lambda: {'+': 1, '-': 1, '*': 2, '/': 2})

    def infix_to_postfix(self, expression: str) -> str:
        stack = Stack()
        output = []
        items = expression.split()

        for item in items:
            if item.isnumeric():
                output.append(item)
            elif item in "+-*/":
                while (not stack.is_empty() and stack.top() != '(' and
                       self.stacks_dict.get(stack.top(), 0) >= self.stacks_dict.get(item, 0)):
                    output.append(stack.pop())
                stack.push(item)
            elif item == '(':
                stack.push(item)
            elif item == ')':
                while not stack.is_empty() and stack.top() != '(':
                    output.append(stack.pop())
                stack.pop()

        while not stack.is_empty():
            output.append(stack.pop())

        return ' '.join(output)

    def post(self, expression: str) -> float:
        stack = Stack()
        items = expression.split()

        for item in items:
            if item.isnumeric():
                stack.push(float(item))
            elif item in "+-*/":
                right = stack.pop()
                left = stack.pop()
                if item == '+':
                    stack.push(left + right)
                elif item == '-':
                    stack.push(left - right)
                elif item == '*':
                    stack.push(left * right)
                elif item == '/':
                    stack.push(left / right)

        return stack.pop()

    def new(self, expression: str) -> float:
        postfix: str = self.infix_to_postfix(expression)
        return self.post(postfix)

class TestStacks(unittest.TestCase):
    def setUp(self):
        self.stacks = Stacks()

    def test_infix_postfix_example(self):
        input = "2 + 3"
        expected = "2 3 +"
        result = self.stacks.infix_to_postfix(input)
        self.assertEqual(expected, result)

    def test_post_example(self):
        input = "2 3 +"
        expected = 5
        result = self.stacks.post(input)
        self.assertEqual(expected, result)

    def test_new_example(self):
        input = "2 + 3"
        expected = 5
        result = self.stacks.new(input)
        self.assertEqual(expected, result)

    def test_multi_and_add(self):
        input = "4 + 6 * 2"
        expected = 16
        result = self.stacks.new(input)
        self.assertEqual(expected, result)

    def test_parentheses(self):
        input = "( 4 + 6 ) * 2"
        expected = 20
        result = self.stacks.new(input)
        self.assertEqual(expected, result)

    def test_operations(self):
        input = "2 * 6 / 2 - 3 + 7"
        expected = 10
        result = self.stacks.new(input)
        self.assertEqual(expected, result)

    def test_infix_postfix(self):
        input = "( 2 + 3 ) * ( 4 - 1 )"
        expected = "2 3 + 4 1 - *"
        result = self.stacks.infix_to_postfix(input)
        self.assertEqual(expected, result)

    def test_new_parentheses(self):
        input = "( 2 + 3 ) * ( 4 - 1 )"
        expected = 15
        result = self.stacks.new(input)
        self.assertEqual(expected, result)

    def test_infix_postfix_x(self):
        input = "2 + 3 * 4 - 5"
        expected = "2 3 4 * + 5 -"
        result = self.stacks.infix_to_postfix(input)
        self.assertEqual(expected, result)

    def test_c(self):
        input = "2 + 3 * 4 - 5"
        expected = 9
        result = self.stacks.new(input)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()

