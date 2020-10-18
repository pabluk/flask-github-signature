# flask-github-signature

A Flask view decorator to verify Github's webhook signatures.

# Usage

```python
from flask import Flask
from flask_github_signature import verify_signature 

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@verify_signature
def hello_world():
    return "Hello, World!"
```
