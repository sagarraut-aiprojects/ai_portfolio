from memory import load_memory, save_memory
from llm import getresponse

def run_chatbot():
    messages = load_memory()


    print("CLI memory ChatBot")
    print("Type 'exit' to quit. \n")


    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("Please enter a message.")
            continue

        if user_input.lower() == "exit":
            print("GoodBye! Nice talking to you!")
            break

        messages.append({"role": "user", "content": user_input})


        assistant_response = getresponse(messages)

        if assistant_response is None:
            messages.pop()
            continue

        print("Assistant", assistant_response)
        print()

        messages.append({
            "role":"assistant",
            "content": assistant_response
        })

        save_memory(messages)