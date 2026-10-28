import lmstudio as lms
import subprocess

MODEL = "qwen/qwen3-4b-2507"  # TODO: make this configurable

ORIGINAL_PATH = "working/original.txt"
OUTPUT_PATH = "working/suggestions.txt"
SYS_PROMPTS_PATH = "./llm_system_prompts/"


def readTxt(path):
    with open(path) as infile:
        return infile.read()


def writeTxt(content, path):
    with open(path, "w") as outfile:
        outfile.write(content)


def llmCall(system_prompt, current_prompt):
    model = lms.llm()
    chat = lms.Chat(system_prompt)
    chat.add_user_message(current_prompt)
    llm_output = model.respond(chat)
    return str(llm_output)


def getOriginal(input_mode):
    original_text = "ERROR"  # TODO: proper error handling here
    if input_mode == "file":
        original_text = readTxt(ORIGINAL_PATH)
    return original_text


def saveOutput(processed_text):
    writeTxt(processed_text, OUTPUT_PATH)


def showDiff():
    subprocess.run(["delta", ORIGINAL_PATH, OUTPUT_PATH])


def getSysPrompt(model_mode):
    mode_to_filename_map = {
        "tte": "translate_to_english",
        "ttg": "translate_to_german",
        "pre": "proofread_english",
        "prg": "proofread_german",
    }
    # TODO: add aliases (but elsewhere)
    return readTxt(SYS_PROMPTS_PATH + mode_to_filename_map[model_mode] + ".txt")
