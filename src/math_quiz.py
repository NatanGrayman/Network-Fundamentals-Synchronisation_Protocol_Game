import random

class MathQuiz:
    def __init__(self):
        self.operators = ['+', '*']
        self.min_number = 1
        self.max_number = 10

    def create_question(self):
        operator = random.choice(self.operators)
        num1 = random.randint(self.min_number, self.max_number)
        num2 = random.randint(self.min_number, self.max_number)
        question = f"What is {num1} {operator} {num2} ? "
        return question
    
    def evaluate_answer(self, question, answer):
       try:
        # Split the question string into parts
        parts = question.split(' ')
        
        # Extract the operator, first number, and second number
        operator = parts[3]
        num1 = int(parts[2])
        num2 = int(parts[4])
        
        # Evaluate the expression
        if operator == '+':
            result = num1 + num2
        elif operator == '*':
            result = num1 * num2
        else:
            result = None
        
        is_correct = (result == int(answer))
        return result, is_correct
       except:
           return None, False