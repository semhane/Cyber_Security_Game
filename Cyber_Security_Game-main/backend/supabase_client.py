import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_questions(game_id):
    try:
        questions = supabase.table("questions").select("*").eq("game_id", game_id).execute()
        return questions.data or []
    except Exception as e:
        print(f"An error occurred while fetching questions: {e}")
        return []

def fetch_answers(question_id):
    try:
        answers = supabase.table("answers").select("*").eq("question_id", question_id).execute()
        return answers.data or []
    except Exception as e:
        print(f"An error occurred while fetching answers: {e}")
        return []

def fetch_tools(question_id):
    try:
        tools = supabase.table("question_tools").select("tool_id").eq("question_id", question_id).execute()
        tool_ids = [tool['tool_id'] for tool in tools.data or []]

        if not tool_ids:
            return []

        tools_details = supabase.table("tools").select("*").in_("id", tool_ids).execute()
        return tools_details.data or []
    except Exception as e:
        print(f"An error occurred while fetching tools: {e}")
        return []

def fetch_red_flags(question_id):
    try:
        red_flags = supabase.table("red_flags").select("*").eq("question_id", question_id).execute()
        return red_flags.data or []
    except Exception as e:
        print(f"An error occurred while fetching red flags: {e}")
        return []

def fetch_user_stats(user_id):
    try:
        user = supabase.table("users").select("score, experience").eq("id", user_id).single().execute()
        return user.data or {'score': 0, 'experience': 0}
    except Exception as e:
        print(f"[fetch_user_stats] {e}")
        return {'score': 0, 'experience': 0}

def update_user_stats(user_id, score_increment, experience_increment):
    try:
        current = fetch_user_stats(user_id)
        new_score = current['score'] + score_increment
        new_experience = current['experience'] + experience_increment

        response = supabase.table("users").update({
            "score": new_score,
            "experience": new_experience
        }).eq("id", user_id).execute()

        return True
    except Exception as e:
        print(f"[update_user_stats] {e}")
        return False

def log_user_game_completion(user_id, game_id, score):
    try:
        response = supabase.table("user_game_logs").insert({
            "user_id": user_id,
            "game_id": game_id,
            "score": score
        }).execute()
        return True
    except Exception as e:
        print(f"[log_user_game_completion] {e}")
        return False