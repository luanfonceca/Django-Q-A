"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, client as TestClient

from core.models import *

DICT_QUESTION = {
    'title': 'Why not working?!',
    'description': 'That shit dont work anymore ;/',
}

class TestQuestion(TestCase):
    def setUp(self):
        self.dict_question = DICT_QUESTION.copy()
        self.client = TestClient.Client()
        self.client.login(username='admin', password="admin")

    def test_basic_creation(self):
        question = Question.objects.create(**self.dict_question)
        self.assertEqual(question.slug, 'why-not-working')

    def test_duplication(self):
        question = Question.objects.create(**self.dict_question)
        self.assertEqual(question.slug, 'why-not-working')
        new_question = Question.objects.create(**self.dict_question)
        self.assertEqual(new_question.slug, 'why-not-working-1')

    def test_basic_increment_view(self):
        question = Question.objects.create(**self.dict_question)
        question.increment_view()
        self.assertEqual(question.slug, 'why-not-working')
        self.assertEqual(question.views, 1)

    def test_view_basic_creation(self):
        self.assertEqual(Question.objects.count(), 0)
        response = self.client.post(
            '/question/add/',
            self.dict_question
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)

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
