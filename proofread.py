import lmstudio as lms
import subprocess

ORIGINAL_PATH = "./working/original.txt"
OUTPUT_PATH = "./working/suggestions.txt"
SYS_PROMPT_PATH = "./llm_proofreader_system_prompt.txt"


def readTxt(path):
    with open(path) as infile:
        return infile.read()


def writeTxt(content, path):
    with open(path, "w") as outfile:
        outfile.write(content)


def llmCall(current_prompt):
    system_prompt = readTxt(SYS_PROMPT_PATH)

    model = lms.llm("qwen/qwen3-4b-2507")  # TODO: make this configurable
    chat = lms.Chat(system_prompt)
    chat.add_user_message(current_prompt)
    llm_output = model.respond(chat)
    return str(llm_output)


def triggerDiff(file1, file2):
    subprocess.run(["delta", ORIGINAL_PATH, OUTPUT_PATH])


def main():
    original_text = readTxt(ORIGINAL_PATH)
    processed_text = llmCall(original_text)
    writeTxt(processed_text, OUTPUT_PATH)
    triggerDiff(ORIGINAL_PATH, OUTPUT_PATH)


if __name__ == "__main__":
    main()
