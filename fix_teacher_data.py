# Fix for teacher data generation issue

def fix_teacher_data_issue():
    # 1. First, check if the data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # 2. Create empty teachers.csv file with headers if it doesn't exist
    if not os.path.exists("data/teachers.csv") or os.path.getsize("data/teachers.csv") == 0:
        headers = ["id", "name", "username", "password", "role", "subject", 
                  "qualification", "contact", "address", "join_date", "salary", "salary_history"]
        df = pd.DataFrame(columns=headers)
        df.to_csv("data/teachers.csv", index=False)
        print("Created empty teachers.csv file with headers")
    
    # 3. Fix the save_data method for teachers
    def fixed_save_teachers(teachers):
        try:
            teachers_data = []
            for teacher in teachers.values():
                teacher_dict = teacher.to_dict()
                # Ensure salary_history is properly formatted for CSV storage
                if hasattr(teacher, 'salary_history') and teacher.salary_history:
                    teacher_dict['salary_history'] = str(teacher.salary_history)
                teachers_data.append(teacher_dict)
            
            # Save with proper encoding
            pd.DataFrame(teachers_data).to_csv("data/teachers.csv", index=False, encoding='utf-8')
            print(f"Successfully saved {len(teachers_data)} teachers to CSV")
            return True
        except Exception as e:
            print(f"Error saving teacher data: {e}")
            return False
    
    # 4. Fix the load_data method for teachers
    def fixed_load_teachers():
        teachers = {}
        try:
            if os.path.exists("data/teachers.csv") and os.path.getsize("data/teachers.csv") > 0:
                teachers_df = pd.read_csv("data/teachers.csv")
                print(f"Loaded teacher data with columns: {teachers_df.columns.tolist()}")
                
                for _, row in teachers_df.iterrows():
                    try:
                        # Check if all required columns exist
                        required_cols = ["id", "name", "username", "password", "subject", 
                                        "qualification", "contact", "address", "join_date", "salary"]
                        
                        if all(col in row for col in required_cols):
                            teacher = Teacher(
                                row['id'], row['name'], row['username'], row['password'],
                                row['subject'], row['qualification'], row['contact'], row['address'],
                                row['join_date'], row['salary']
                            )
                            
                            # Handle salary_history
                            if 'salary_history' in row and row['salary_history'] and row['salary_history'] != 'nan':
                                try:
                                    # Try to evaluate the string representation of the list
                                    teacher.salary_history = eval(row['salary_history'])
                                except:
                                    teacher.salary_history = []
                            
                            teachers[teacher.id] = teacher
                            print(f"Successfully loaded teacher: {teacher.id} - {teacher.name}")
                        else:
                            missing = [col for col in required_cols if col not in row]
                            print(f"Skipping teacher record due to missing columns: {missing}")
                    except Exception as e:
                        print(f"Error loading individual teacher: {e}")
        except Exception as e:
            print(f"Error loading teacher data: {e}")
        
        return teachers
    
    # 5. Test adding a sample teacher
    def test_add_teacher():
        try:
            teacher_id = f"T{str(uuid.uuid4())[:8]}"
            teacher = Teacher(
                teacher_id, "Test Teacher", "teacher1", "password123",
                "Mathematics", "PhD", "123-456-7890", "123 Teacher St",
                "2023-01-01", 2500
            )
            
            # Load existing teachers
            teachers = fixed_load_teachers()
            
            # Add new teacher
            teachers[teacher_id] = teacher
            
            # Save teachers
            if fixed_save_teachers(teachers):
                print(f"Successfully added test teacher with ID: {teacher_id}")
                return True
            else:
                print("Failed to save test teacher")
                return False
        except Exception as e:
            print(f"Error in test_add_teacher: {e}")
            return False
    
    # Run the fixes
    test_add_teacher()
    
    print("Teacher data fix completed. Please restart your application.")

# Run the fix function
if __name__ == "__main__":
    fix_teacher_data_issue()