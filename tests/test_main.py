import os
import unittest

# This env var is need before importing the module
os.environ["GH_WEBHOOK_SECRET"] = "xyz"

import flask
from flask_github_signature import (
    compute_signature,
    get_github_signature,
    verify_signature,
)


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

    def test_get_github_signature_no_header(self):
        headers = {}
        with app.test_request_context(method="POST", headers=headers):
            req = flask.request
            signature = get_github_signature(req)
            self.assertIsNone(signature)


class TestViewDecorator(unittest.TestCase):
    def test_verify_signature(self):
        headers = {
            "X-Hub-Signature-256": "sha256=a60cd2167b32e1d7e906ba3829ffd9ac63f04a18a58cd0f5faa4d3f84c554ec5",
        }
        data = b'{"zen": "Responsive is better than fast.", "hook_id": 1111111}'
        with app.test_request_context(method="POST", data=data, headers=headers):
            req = flask.request

            @verify_signature
            def fn():
                return "Hello, World!"

            self.assertEqual(fn(), "Hello, World!")

    def test_verify_signature_mismatch(self):
        headers = {
            "X-Hub-Signature-256": "sha256=xxxxxxx",
        }
        data = b'{"zen": "Responsive is better than fast.", "hook_id": 1111111}'
        with app.test_request_context(method="POST", data=data, headers=headers):
            req = flask.request

            @verify_signature
            def fn():
                return "Hello, World!"

            message, status_code = fn()
            self.assertEqual(status_code, 400)


    def test_verify_signature_malformed(self):
        headers = {
            "X-Hub-Signature-256": "xxxxxxx",
        }
        data = b'{"zen": "Responsive is better than fast.", "hook_id": 1111111}'
        with app.test_request_context(method="POST", data=data, headers=headers):
            req = flask.request

            @verify_signature
            def fn():
                return "Hello, World!"

            message, status_code = fn()
            self.assertEqual(status_code, 400)


    def test_no_gh_header(self):
        headers = {}
        data = b'{"zen": "Responsive is better than fast.", "hook_id": 1111111}'
        with app.test_request_context(method="POST", data=data, headers=headers):
            req = flask.request

            @verify_signature
            def fn():
                return "Hello, World!"

            message, status_code = fn()
            self.assertEqual(status_code, 400)


    def test_no_post_method(self):
        headers = {
            "X-Hub-Signature-256": "sha256=a60cd2167b32e1d7e906ba3829ffd9ac63f04a18a58cd0f5faa4d3f84c554ec5",
        }
        data = b'{"zen": "Responsive is better than fast.", "hook_id": 1111111}'
        with app.test_request_context(method="GET", data=data, headers=headers):
            req = flask.request

            @verify_signature
            def fn():
                return "Hello, World!"

            message, status_code = fn()
            self.assertEqual(status_code, 400)


if __name__ == "__main__":
    unittest.main()
