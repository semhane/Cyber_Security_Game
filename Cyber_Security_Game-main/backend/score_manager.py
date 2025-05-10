from backend.supabase_client import supabase

def get_user_data(user_id: int = 1):
    """Fetch user's name and score from database"""
    try:
        res = supabase.table("users").select("username, score").eq("id", user_id).execute()
        return res.data[0] if res.data else {"username": "GUEST", "score": 0}
    except Exception as e:
        print(f"[get_user_data] Error: {e}")
        return {"username": "GUEST", "score": 0}

def update_user_score(points: int, user_id: int = 1) -> bool:
    """Atomically increment the user's score in Supabase."""
    try:
        supabase.rpc("increment_score", {"user_id": user_id, "points": points}).execute()
        return True
    except Exception as e:
        print(f"[update_user_score] Error: {e}")
        return False