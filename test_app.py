import unittest
import json
import os
from main import StoryManager, QuizManager, Chatbot

class TestStoryManager(unittest.TestCase):
    def setUp(self):
        self.sm = StoryManager()
        self.sm.filepath = "test_stories.json"

    def test_add_story_true(self):
        self.sm.add("Ana", "My baby smiled today!")
        stories = self.sm.load()
        self.assertEqual(stories[0]["author"], "Ana")

    def test_add_story_false(self):
        self.sm.add("Ana", "My baby smiled today!")
        stories = self.sm.load()
        self.assertNotEqual(stories[0]["author"], "WrongName")

    def tearDown(self):
        if os.path.exists("test_stories.json"):
            os.remove("test_stories.json")


class TestQuizManager(unittest.TestCase):
    def setUp(self):
        self.qm = QuizManager()

    def test_grade_correct(self):
        perfect = {"q1":"2","q2":"1","q3":"0","q4":"2","q5":"1",
                   "q6":"0","q7":"1","q8":"0","q9":"0","q10":"0"}
        self.assertEqual(self.qm.grade(perfect), 10)

    def test_grade_wrong(self):
        all_wrong = {"q1":"0","q2":"0","q3":"1","q4":"0","q5":"0",
                     "q6":"1","q7":"0","q8":"1","q9":"1","q10":"1"}
        self.assertNotEqual(self.qm.grade(all_wrong), 10)


class TestChatbot(unittest.TestCase):
    def test_ask_returns_string(self):
        bot = Chatbot()
        result = bot.ask("When should I feed my newborn?")
        self.assertIsInstance(result, str)

    def test_ask_not_empty(self):
        bot = Chatbot()
        result = bot.ask("When should I feed my newborn?")
        self.assertNotEqual(result, "")


if __name__ == "__main__":
    unittest.main()