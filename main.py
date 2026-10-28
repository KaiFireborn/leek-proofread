from utilities import (
    getSysPrompt,
    readTxt,
    writeTxt,
    llmCall,
    getOriginal,
    saveOutput,
    showDiff,
)
import sys
import pyperclip


def processProofread(model_mode, input_mode, show_diff=True):
    result = llmCall(getSysPrompt(model_mode), getOriginal(input_mode))
    saveOutput(result)
    if show_diff:
        showDiff()


def get_modes():
    def model_mode_map(arg):
        aliases = {
            "tte": ["translate_to_english", "g2e"],
            "ttg": ["translate_to_german", "e2g"],
            "pre": ["proofread_english"],
            "prg": ["proofread_german"],
        }

        mode_map = {}
        for key, values in aliases.items():
            for alias in [key] + values:
                mode_map[alias] = key
        if arg not in mode_map:
            raise KeyError(arg, "not in mode map")
        return mode_map[arg]

    def model_input_map_and_inp(args):
        # check args length or something
        input_mode = "file"
        if args[2] in ["-v", "--clipboard"]:  # TODO: extract automatically to doc
            return ("clipboard", pyperclip.paste())
        elif args[2] in ["-s", "--string"]:
            if args[3] != "":  # FIXME: potentially check length here instead
                raise Exception(
                    "No string provided despite -s argument"
                )  # print them or sth
            return ("string", args[3])

    args = sys.argv

    # usage: leek ttg ttg -s

    return {"model_mode": model_mode_map(args[1]), "input_mode": input_mode}


def execute(display_diff=True):

    processProofread(get_modes(), getOriginal("file"))


if __name__ == "__main__":
    execute()
