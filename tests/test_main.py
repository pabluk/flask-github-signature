import os
import unittest

# This env var is need before importing the module
os.environ["GH_WEBHOOK_SECRET"] = "xyz"

import flask
from flask_github_signature import compute_signature, get_github_signature


app = flask.Flask(__name__)


class TestSignatures(unittest.TestCase):
    def test_compute_signature(self):
        expected = "eba50596a17c2c8fbdbc5c68223422fe41d5310bea51ffdc461430bce0386c54"
        signature = compute_signature("xyz", b"{}")
        self.assertEqual(signature, expected)


class TestGithubRequest(unittest.TestCase):
    def test_get_github_signature(self):
        headers = {
            "X-Hub-Signature-256": "sha256=eba50596a17c2c8fbdbc5c68223422fe41d5310bea51ffdc461430bce0386c54"
        }
        with app.test_request_context(method="POST", headers=headers):
            req = flask.request
            expected = (
                "eba50596a17c2c8fbdbc5c68223422fe41d5310bea51ffdc461430bce0386c54"
            )
            signature = get_github_signature(req)
            self.assertEqual(signature, expected)


if __name__ == "__main__":
    unittest.main()
