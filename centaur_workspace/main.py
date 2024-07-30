import os
from dotenv import load_dotenv
from centaur_workspace.crew import MyProjectCrew


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    crew = MyProjectCrew()

    print(
        "Welcome! You can chat with our AI assistants or interact with Dave "
        "Product, our Product Manager."
    )
    print(
        "Type 'Dave' to talk to Dave Product, "
        "'Alex' to talk to Alex the Entrepreneur, "
        "'Bob' to talk to Bob the Engineer, "
        "'exit' to quit."
    )

    agent_choice = (
        input("Who would you like to talk to? (Dave, Alex, Bob): ").strip().lower()
    )
    talking_to_dave = agent_choice == "dave"
    talking_to_alex = agent_choice == "alex"
    talking_to_bob = agent_choice == "bob"

    while True:
        if not talking_to_dave and not talking_to_alex and not talking_to_bob:
            print("Please choose a valid option: 'Dave', 'Alex', or 'Bob'.")
            agent_choice = (
                input("Who would you like to talk to? (Dave, Alex, Bob): ")
                .strip()
                .lower()
            )
            talking_to_dave = agent_choice == "dave"
            talking_to_alex = agent_choice == "alex"
            talking_to_bob = agent_choice == "bob"
            continue

        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "stop":
            talking_to_dave = False
            talking_to_alex = False
            talking_to_bob = False
            print(
                "You've ended your conversation. You can type 'Dave', 'Alex', or 'Bob' "
                "again to continue the conversation."
            )
            continue
        else:
            if talking_to_dave:
                response = crew.interact_with_dave_product_manager(user_input)
            elif talking_to_alex:
                response = crew.interact_with_alex_entrepreneur(user_input)
            elif talking_to_bob:
                response = crew.interact_with_bob(user_input)

        print(f"AI: {response}")


if __name__ == "__main__":
    main()
