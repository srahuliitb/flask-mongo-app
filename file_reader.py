
def get_all_user_credentials_from_persistent_storage():
    file_path = 'user_credentials.txt'
    user_credentials = []
    try:
        with open(file_path, 'r') as file:
            # Read each line and print it
            for line in file:
                username, password = line.strip().split(',')
                # print(line.strip())  # Use strip() to remove trailing newline characters
                user_credentials.append((username, password))
        return user_credentials
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"An error occurred: {e}"
        