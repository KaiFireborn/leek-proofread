import lmstudio as lms
import subprocess
import json

ORIGINAL_PATH = "working/original.txt"
OUTPUT_PATH = "working/suggestions.txt"
SYS_PROMPTS_PATH = "./llm_system_prompts/"


def getConfig():
    with open("config.json", "r") as infile:
        return json.load(infile)


config = getConfig()


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


def getOriginalFromFile():
    original_text = readTxt(ORIGINAL_PATH)
    return original_text


# maybe those two better in main?
def saveOriginal(original):
    writeTxt(original + "\n", ORIGINAL_PATH)


def saveOutput(processed_text):
    writeTxt(processed_text.replace("  ", "") + "\n", OUTPUT_PATH)


def showDiff():
    subprocess.run(["delta", ORIGINAL_PATH, OUTPUT_PATH])
    # remove lines like ""\ No newline at end of file"


def getSysPrompt(model_mode):
    mode_to_filename_map = {
        "tte": "translate_to_english",
        "ttg": "translate_to_german",
        "pre": "proofread_english",
        "prg": "proofread_german",
    }
    # TODO: add aliases (but elsewhere)
    return readTxt(SYS_PROMPTS_PATH + mode_to_filename_map[model_mode] + ".txt")


def getHelpText():
    return readTxt("README.txt")
