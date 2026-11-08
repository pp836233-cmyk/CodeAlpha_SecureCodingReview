# CodeAlpha_SecureCodingReview

Task 3 - Secure Coding Review (CodeAlpha Cyber Security Internship)

- `CodeAlpha_SecureCodingReview.pdf` - full audit report
- `app.py` - intentionally vulnerable Flask app (8 vulnerabilities)
- `app_fixed.py` - remediated version

## Run static analysis
    pip install bandit
    bandit -r app.py

> Warning: `app.py` is deliberately insecure. Run it only locally for learning.
