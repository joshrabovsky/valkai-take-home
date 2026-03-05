from dataclasses import dataclass

@dataclass
class Turn:
    message: str
    expected_keywords: list[str] | None = None

SCRIPT = [
    Turn("My name is Josh and I live in San Francisco"),
    Turn("My favourite number is 9"),
    Turn("I am a software engineer who is applying to VALK AI"),
    Turn("What is the capital of France?"),
    Turn("What is the square root of 81?"),
    Turn("Who won the NBA championship in 2010?"),
    Turn("What is the boiling point of water at sea level?"),
    Turn("What is the chemical symbol for gold?"),
    Turn("What is the largest mammal on Earth?"),
    Turn("What is the currency of Japan?"),
    Turn("What is the largest planet in our solar system?"),
    Turn("What is the chemical symbol for silver?"),
    Turn("Who is the president of the United States"),
    Turn("What does the flag of Canada look like?"),
    Turn("Who invented the light bulb?"),
    Turn("What is an oreo made of?"),
    Turn("What is my name?", ["Josh"]),
    Turn("Where do I live?", ["San Francisco"]),
    Turn("What is my favourite number?", ["9"]),
    Turn("What is my job?", ["software engineer"]),
    Turn("What company am I applying to?", ["VALK AI"]),
]