import os
import json
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from nvento.models import *
import json


json_file_path = 'data/category.json'
data = json.load(open(json_file_path))

for entry in data:
    category = entry['category']
    thumbnail_url = entry['thumbnailUrl']
    background = entry['background']

    quiz, created = Quiz.objects.get_or_create(title=category, defaults={'thumbnailUrl': thumbnail_url})

    for question_data in entry['questions']:
        question_text = question_data['question']
        options = question_data['options']
        correct_answer = question_data['answer']

        question, created = Question.objects.get_or_create(quiz=quiz, text=question_text)

        for option_text in options:
            answer, created = Answer.objects.get_or_create(question=question, text=option_text, is_correct=(option_text == correct_answer))

print("Data import completed.")
