import os

def replace_experimental_rerun(file_path):
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace all instances of st.rerun() with st.rerun()
    updated_content = content.replace('st.rerun()', 'st.rerun()')
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    # Count the number of replacements
    count = content.count('st.rerun()')
    return count

# Path to your app.py file
file_path = 'D:\\Python\\class-project\\school\\app.py'

# Make the replacements
replacements = replace_experimental_rerun(file_path)
print(f"Replaced {replacements} instances of st.rerun() with st.rerun()")
print(f"File updated: {file_path}")