

# frontend/games/general_qcm_data.py

CHALLENGES = [
    {
        "level": 1,
        "score": 100,
        "scenario": "Hello, this is IT support. We noticed an issue on your machine. Can you send us your password to verify?",
        
        "responses": ["Give password", "Ignore", "Report to IT"],
        "correct_response": "Report to IT",
        "attacker_type": "Impersonation",
        "policy_reminder": "Company policy prohibits sharing passwords with anyone.",
        
    },
    {
        "level": 2,
        "score": 150,
        "scenario": "You receive an email from 'admin@secure-login.com' asking you to reset your password using a link.",
        
        "responses": ["Click the link", "Report the email", "Reply to sender"],
        "correct_response": "Report the email",
        "attacker_type": "Phishing",
        "policy_reminder": "Always verify unexpected password reset emails via official channels.",
        
    },
    {
        "level": 3,
        "score": 200,
        "scenario": "Your manager sends a message on WhatsApp asking you to urgently buy gift cards and send the codes.",
        
        "responses": ["Buy gift cards", "Ignore", "Call the manager to verify"],
        "correct_response": "Call the manager to verify",
        "attacker_type": "Executive Scam",
        "policy_reminder": "Verify financial requests through official channels.",
        
    }
]