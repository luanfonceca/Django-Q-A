"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, client as TestClient

from core.models import *

DICT_QUESTION = {
    'author': 'Bill Gates',
    'title': 'Why not working?!',
    'description': 'That shit dont work anymore ;/',
}

DICT_ANSWER = {
    'body': 'Use python, always resolve!',
    'author': 'Guido van Rossum',
}

class TestQuestion(TestCase):
    def setUp(self):
        self.dict_question = DICT_QUESTION.copy()
        self.client = TestClient.Client()
        self.client.login(username='admin', password="admin")

    def test_duplication(self):
        question = Question.objects.create(**self.dict_question)
        self.assertEqual(question.slug, 'why-not-working')
        new_question = Question.objects.create(**self.dict_question)
        self.assertEqual(new_question.slug, 'why-not-working-1')

    def test_view_basic_creation(self):
        self.assertEqual(Question.objects.count(), 0)
        response = self.client.post(
            '/question/add/',
            self.dict_question
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)

    def test_view_basic_increment_view(self):
        question = Question.objects.create(**self.dict_question)
        self.client.get(question.get_absolute_url())
        question = Question.objects.get()
        self.assertEqual(question.views, 1)

    def test_view_basic_edition(self):
        old_question = Question.objects.create(**self.dict_question)
        dict_changed_question = self.dict_question.copy()
        dict_changed_question['title'] = 'I Change the Title!'
        response = self.client.post(
            old_question.get_edit_url(),
            dict_changed_question
        )
        new_question = Question.objects.get()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_question.slug, 'i-change-the-title')

    def test_view_basic_deletion(self):
        question = Question.objects.create(**self.dict_question)
        self.assertEqual(question.slug, 'why-not-working')
        response = self.client.post(
            question.get_delete_url()
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 0)

    def test_view_question(self):
        question = Question.objects.create(**self.dict_question)
        response = self.client.get(
            question.get_absolute_url()
        )
        question = Question.objects.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(question.views, 1)

class TestAnswer(TestCase):
    def setUp(self):
        self.dict_answer = DICT_ANSWER.copy()
        self.question = Question.objects.create(**DICT_QUESTION)
        self.dict_answer.update({
            'question': self.question
        })

    def test_basic_creation(self):
        answer = Answer.objects.create(**self.dict_answer)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(self.question.answers.count(), 1)

    def test_view_basic_creation(self):
        self.assertEqual(Answer.objects.count(), 0)
        response = self.client.post(
            self.question.get_answer_add_url(),
            self.dict_answer
        )
        question = Question.objects.get()
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(self.question.answers.count(), 1)

    def test_view_basic_edition(self):
        old_answer = Answer.objects.create(**self.dict_answer)
        dict_changed_answer = self.dict_answer.copy()
        dict_changed_answer['body'] = 'I Change the Body!'
        response = self.client.post(
            old_answer.get_edit_url(),
            dict_changed_answer
        )
        new_answer = Answer.objects.get()
        self.assertEqual(new_answer.body, 'I Change the Body!')

    def test_view_set_as_correct(self):
        answer = Answer.objects.create(**self.dict_answer)

        response = self.client.post(
            answer.get_set_as_correct_url()
        )
        answer = Answer.objects.get()
        self.assertEqual(answer.is_correct, True)
        self.assertEqual(answer.aproves, 100)

    def test_view_aprove_answer(self):
        answer = Answer.objects.create(**self.dict_answer)

        response = self.client.post(
            answer.get_aprove_url()
        )
        answer = Answer.objects.get()
        self.assertEqual(answer.aproves, 1)

    def test_view_desaprove_answer(self):
        answer = Answer.objects.create(**self.dict_answer)

        response = self.client.post(
            answer.get_desaprove_url()
        )
        answer = Answer.objects.get()
        self.assertEqual(answer.desaproves, 1)
