from utilities import (
    getSysPrompt,
    llmCall,
    getOriginalFromFile,
    saveOutput,
    saveOriginal,
    showDiff,
    getConfig,
)
import sys
import pyperclip

config = getConfig()


def get_modes():
    def model_mode_map(relevant_args):
        if len(relevant_args) < 1:
            raise Exception("no first argument")

        aliases = {
            "tte": ["translate_to_english", "g2e"],
            "ttg": ["translate_to_german", "e2g", "ttd"],
            "pre": ["proofread_english"],
            "prg": ["proofread_german", "prd"],
        }

        mode_map = {}
        for key, values in aliases.items():
            for alias in [key] + values:
                mode_map[alias] = key

        if relevant_args[0] not in mode_map:
            raise Exception(f"{relevant_args[0]} not in mode map")

        return mode_map[relevant_args[0]]

    def model_input_map_and_inp(args):
        print(args)

        def get_note(relevant_args):
            print(relevant_args)
            if len(relevant_args) < 1:
                return ""
            else:
                print("Found note:", relevant_args[0])
                return f"@hint: {relevant_args[0]}\n"

        if len(args) < 1:
            return ("file", getOriginalFromFile())

        elif args[0] in ["-f", "--file"]:
            return ("file", get_note(args[1:]) + getOriginalFromFile())

        elif args[0] in ["-v", "--clipboard"]:  # TODO: extract automatically to doc
            return ("clipboard", get_note(args[1:]) + pyperclip.paste())

        elif args[0] in ["-s", "--string"]:
            if len(args) < 2:
                raise Exception("No string provided despite -s argument")
            return ("string", get_note(args[2:]) + args[1])

        else:
            print(args[0])
            raise Exception("No such mode")

    # usage: leek ttg ttg -s

    return {
        "model_mode": model_mode_map(sys.argv[1:]),
        "input_mode": model_input_map_and_inp(sys.argv[2:]),
    }


def process(model_mode, original, show_diff=True):
    saveOriginal(original)
    result = llmCall(getSysPrompt(model_mode), original)
    saveOutput(result)
    if show_diff:
        showDiff()


def execute(show_diff=True):
    modes = get_modes()
    process(modes["model_mode"], modes["input_mode"][1], show_diff)


if __name__ == "__main__":
    execute()
