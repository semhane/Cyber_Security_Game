from supabase_client import supabase
from datetime import datetime

def submit_qcm_result(user_id, game_id, score_earned):
    experience_earned = score_earned // 2  # Customize this logic if needed

    # 1. Log game result
    result = supabase.table("user_game_logs").insert({
        "user_id": user_id,
        "game_id": game_id,
        "score": score_earned,
        "completed_at": datetime.now().isoformat()
    }).execute()
    if result.error:
        raise Exception(f"Error inserting game log: {result.error}")

    # 2. Fetch current user score and experience
    user = supabase.table("users").select("score, experience").eq("id", user_id).single().execute()
    if user.error:
        raise Exception(f"Error fetching user data: {user.error}")
    user_data = user.data or {}
    current_score = user_data.get('score', 0)
    current_experience = user_data.get('experience', 0)

    new_score = current_score + score_earned
    new_experience = current_experience + experience_earned

    # 3. Update user score and experience
    update = supabase.table("users").update({
        "score": new_score,
        "experience": new_experience
    }).eq("id", user_id).execute()
    if update.error:
        raise Exception(f"Error updating user score and experience: {update.error}")

    # 4. Unlock new games based on new score
    games = supabase.table("games").select("*").lte("min_score", new_score).execute()
    if games.error:
        raise Exception(f"Error fetching unlockable games: {games.error}")
    
    for game in games.data or []:
        unlock = supabase.table("user_unlocked_games").upsert({
            "user_id": user_id,
            "game_id": game['id'],
            "unlocked_at": datetime.now().isoformat()
        }, on_conflict=["user_id", "game_id"]).execute()
        if unlock.error:
            raise Exception(f"Error unlocking game: {unlock.error}")

def update_user_score(user_id, score):
    # Update the user's score in the database
    response = supabase.table('users').update({"score": score}).eq('id', user_id).execute()
    if response.error is None:
        return True
    return False
