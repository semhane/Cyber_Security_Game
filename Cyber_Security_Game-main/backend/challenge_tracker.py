from backend.supabase_client import supabase
from backend.score_manager import update_user_score

def log_challenge(challenge_id: str, points: int, user_id: int = 1) -> bool:
    """Record challenge completion and update total score."""
    try:
        # 1. Log the challenge
        supabase.table("user_challenges").insert({
            "user_id": user_id,
            "challenge_id": challenge_id,
            "points_earned": points
        }).execute()

        # 2. Update score
        return update_user_score(points, user_id)
    except Exception as e:
        print(f"[log_challenge] Error: {e}")
        return False