from django.urls import reverse
from django.test import TestCase
import datetime
from django.utils import timezone

from .models import Question


# Create your tests here.


def create_question(question_text, days):
    """
    Create question with given question text and published days in the future.
    :param question_text:
    :param days:
    :return:
    """
    when = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=when)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    latest_key = 'latest_question_list'
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context[self.latest_key], [])

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context[self.latest_key],
                                 ([repr(question)]))

    def test_future_question(self):
        expected = create_question("Future question.", 5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 [])

    def test_future_and_past_question(self):
        future = create_question("Future question.", 5)
        past = create_question("Past question.", -5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context[self.latest_key],
                                 [repr(past)])

    def test_two_past_questions(self):
        past1 = create_question("Past Question 1", -1)
        past2 = create_question("Past Question 2", -355)
        response = self.client.get(reverse('polls:index'))
        actual = response.context[self.latest_key]
        self.assertQuerysetEqual(actual, [repr(past1),repr(past2)])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question("Future question.", 3)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question("Past question.", -4)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)