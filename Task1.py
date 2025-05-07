from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()


def main():
    print("Type 'q' to quit.")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        user_input = input("You: ")
        if user_input.lower() == "q":
            break

        messages.append({"role": "user", "content": user_input})
        reply = get_response(messages)
        print(f"Chat: {reply}")
        messages.append({"role": "assistant", "content": reply})



if __name__ == "__main__":
    main()
