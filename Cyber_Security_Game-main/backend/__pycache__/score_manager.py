from supabase_client import supabase

def get_user_score(user_id: int = 1) -> int:
    """Fetch current score from Supabase."""
    try:
        res = supabase.table("users").select("score").eq("id", user_id).execute()
        return res.data[0]["score"] if res.data else 0
    except Exception as e:
        print(f"[get_user_score] Error: {e}")
        return 0

def update_user_score(points: int, user_id: int = 1) -> bool:
    """Atomically increment the user's score in Supabase."""
    try:
        supabase.rpc("increment_score", {"user_id": user_id, "points": points}).execute()
        return True
    except Exception as e:
        print(f"[update_user_score] Error: {e}")
        return False