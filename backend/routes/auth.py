from backend.supabase_client import supabase
import bcrypt

def signup_user(username, email, password, department_name, score=0):
    try:
        # 1. Check for empty fields
        if not all([username, email, password, department_name]):
            return {"success": False, "message": "All fields are required."}
        
        # 2. Check if user already exists
        existing_user = supabase.table("users").select("*").eq("email", email).execute()
        if existing_user.data:
            return {"success": False, "message": "Email already registered."}
        
        existing_username = supabase.table("users").select("*").eq("username", username).execute()
        if existing_username.data:
            return {"success": False, "message": "Username already taken."}
        
        # 3. Lookup department ID
        try:
            # Ensure department_name is clean (no extra whitespace)
            clean_department_name = department_name.strip()
            
            # Query the database for all departments to find a match
            all_departments = supabase.table("departments").select("department_id, department_name").execute()
            
            # Debug info
            print(f"Looking for department: '{clean_department_name}'")
            
            # Search for a match by stripping whitespace and newlines from database values
            department_id = None
            for dept in all_departments.data:
                db_dept_name = dept["department_name"].strip()  # Strip whitespace and newlines
                print(f"Comparing with: '{db_dept_name}'")
                
                if db_dept_name == clean_department_name:
                    department_id = dept["department_id"]
                    print(f"Found department ID: {department_id} for {clean_department_name}")
                    break
            
            if not department_id:
                print(f"No department found with name: {clean_department_name}")
                return {"success": False, "message": "Department not found."}
                
        except Exception as e:
            print(f"Error looking up department: {str(e)}")
            return {"success": False, "message": f"Error with department: {str(e)}"}
        
        # 4. Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # 5. Insert into users table with default beginner experience level (0)
        result = supabase.table("users").insert({
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "department_id": department_id,
            "score": score,
            "experience": 0  # Always set to BEGINNER (0)
        }).execute()
        
        if hasattr(result, 'error') and result.error:
            return {"success": False, "message": f"Error inserting user: {result.error}"}
        
        return {"success": True, "message": "Registration successful."}
    
    except Exception as e:
        return {"success": False, "message": f"Exception occurred: {str(e)}"}