import unittest
import requests


class FlaskTest(unittest.TestCase):

    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<form method="GET" action="./login">' in response.text, True)
        self.assertEqual('<form method="GET" action="./register">' in response.text, True)

    def test_questions(self):
        response = requests.get("http://127.0.0.1:5000/questions")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Home' in response.text, True)

    def test_view_question(self):
        response = requests.get("http://127.0.0.1:5000/questions/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Answers' in response.text, True)

    def test_new_question(self):
        response = requests.get("http://127.0.0.1:5000/new_question")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Title' in response.text, True)
        self.assertEqual('Topic' in response.text, True)

    def test_delete(self):
        response = requests.get("http://127.0.0.1:5000/questions/delete/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)

    def test_profile(self):
        response = requests.get("http://127.0.0.1:5000/profile")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Likes' in response.text, True)

    def test_reviews(self):
        response = requests.get("http://127.0.0.1:5000/reviews")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<form action="./new_review" method="get">' in response.text, True)

    def test_delete_review(self):
        response = requests.get("http://127.0.0.1:5000/reviews/delete")
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)


if __name__ == "__main__":
    unittest.main()
