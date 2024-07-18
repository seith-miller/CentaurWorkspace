import os
from dotenv import load_dotenv
from centaur_workspace.crew import MyProjectCrew

def main():
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    crew = MyProjectCrew()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response = crew.chat(user_input)
        print(f"AI: {response}")

if __name__ == "__main__":
    main()
