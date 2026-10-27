import lmstudio as lms


def llmCall(current_prompt):
    model = lms.llm("qwen/qwen3-4b-2507")
    chat = lms.Chat("speak like a space pirate")
    chat.add_user_message(current_prompt)
    return model.respond(chat)


def main():
    print(
        llmCall("""
Hello lol                  
""")
    )


if __name__ == "__main__":
    main()
