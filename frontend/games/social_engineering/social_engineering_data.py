# frontend/games/social_engineering_data.py

CHALLENGES = [
    {
        "level": 1,
        "score": 100,
        "scenario": "Hello, this is IT support. We noticed an issue on your machine. Can you send us your password to verify?",
        "red_flags": [
            "Asking for password",
            "Urgency",
            "Unverified identity"
        ],
        "correct_flags": [
            "Asking for password",
            "Unverified identity"
        ],
        "responses": ["Give password", "Ignore", "Report to IT"],
        "correct_response": "Report to IT",
        "attacker_type": "Impersonation",
        "policy_reminder": "Company policy prohibits sharing passwords with anyone.",
        "tools": ["VERIFY CALLER", "POLICY CHECK", "IT DIRECTORY", "HINT"]
    },
    {
        "level": 2,
        "score": 150,
        "scenario": "You receive an email from 'admin@secure-login.com' asking you to reset your password using a link.",
        "red_flags": [
            "Suspicious email address",
            "Unexpected password reset request",
            "Urgency"
        ],
        "correct_flags": [
            "Suspicious email address",
            "Unexpected password reset request"
        ],
        "responses": ["Click the link", "Report the email", "Reply to sender"],
        "correct_response": "Report the email",
        "attacker_type": "Phishing",
        "policy_reminder": "Always verify unexpected password reset emails via official channels.",
        "tools": ["EMAIL HEADER CHECK", "SECURITY PORTAL", "HINT"]
    },
    {
        "level": 3,
        "score": 200,
        "scenario": "Your manager sends a message on WhatsApp asking you to urgently buy gift cards and send the codes.",
        "red_flags": [
            "Unusual request",
            "Urgency",
            "Request over unofficial channel"
        ],
        "correct_flags": [
            "Unusual request",
            "Request over unofficial channel"
        ],
        "responses": ["Buy gift cards", "Ignore", "Call the manager to verify"],
        "correct_response": "Call the manager to verify",
        "attacker_type": "Executive Scam",
        "policy_reminder": "Verify financial requests through official channels.",
        "tools": ["PHONE VERIFY", "FINANCE POLICY", "HINT"]
    }
]