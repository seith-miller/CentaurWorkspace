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
        "'Alex' to talk to the new Anthropic agent, "
        "'exit' to quit, or anything else to chat with our general AI."
    )

    agent_choice = (
        input("Who would you like to talk to? (Greeter, Responder, Dave, Alex): ")
        .strip()
        .lower()
    )
    talking_to_dave = agent_choice == "dave"
    talking_to_alex = agent_choice == "alex"
    general_agent = 0 if agent_choice == "greeter" else 1

    while True:
        if not talking_to_dave and not talking_to_alex:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            elif user_input.lower() == "dave":
                talking_to_dave = True
                print(
                    "You're now talking to Dave Product. What would you like "
                    "to discuss about the product? (Type 'stop' to end the "
                    "conversation with Dave)"
                )
                continue
            elif user_input.lower() == "alex":
                talking_to_alex = True
                print(
                    "You're now talking to Alex. What would you like "
                    "to discuss? (Type 'stop' to end the conversation with Alex)"
                )
                continue
            else:
                response = crew.agents[general_agent].generate_text(user_input)
        elif talking_to_dave:
            user_input = input("You (to Dave): ")
            if user_input.lower() == "stop":
                talking_to_dave = False
                print(
                    "You've ended your conversation with Dave. You can type "
                    "'Dave' again to talk to him later."
                )
                continue
            response = crew.interact_with_product_manager(user_input)
        elif talking_to_alex:
            user_input = input("You (to Alex): ")
            if user_input.lower() == "stop":
                talking_to_alex = False
                print(
                    "You've ended your conversation with Alex. You can type "
                    "'Alex' again to talk to him later."
                )
                continue
            response = crew.interact_with_alex(user_input)

        print(f"AI: {response}")


if __name__ == "__main__":
    main()
