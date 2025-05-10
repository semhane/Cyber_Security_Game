import bcrypt
from backend.supabase_client import supabase

def signup_user(username, email, password, department_name, score=0, experience=0):
    try:
        # 1. Check for empty fields
        if not all([username, email, password, department_name]):
            r_eturn {"success": False, "message": "All fields are required."}

        # 2. Check if user already exists
        existing_user = supabase.table("users").select("*").eq("email", email).execute()
        if existing_user.data:
            return {"success": False, "message": "Email already registered."}

        existing_username = supabase.table("users").select("*").eq("username", username).execute()
        if existing_username.data:
            return {"success": False, "message": "Username already taken."}

        # 3. Lookup department ID
        dept_response = supabase.table("departments").select("id").eq("name", department_name).single().execute()
        if dept_response.error or not dept_response.data:
            return {"success": False, "message": "Department not found."}
        department_id = dept_response.data["id"]

        # 4. Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 5. Insert into users table
        insert_result = supabase.table("users").insert({
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "department_id": department_id,
            "score": score,
            "experience": experience
        }).execute()

        if insert_result.error:
            return {"success": False, "message": f"Signup failed: {insert_result.error.message}"}

        return {"success": True, "message": "User registered successfully!"}

    except Exception as e:
        return {"success": False, "message": f"An unexpected error occurred: {str(e)}"}

