A proofreader that uses local lm-studio API and some configurable model loaded there.

To use:
- have the local lm-studio server running with a model loaded

- run `python proofread.py` or equivalently `leek` with necessary arguments (see below
- the tool saves its suggested changes as `./working/suggestions.txt` and shows the diff via `git-delta`.

AI use disclosure:
- `llm_proofreader_system_prompt.txt` is generated from a simpler human-written version by the free web version of Claude...

# Example Usage
`leek pre -s "This tekst has a mistaker," -n "this text should be formal"`

Syntax:
`leek <pr{e, g}|ttg{e, g}> -<f|v|s "input_text"> [-n note]`
The option `-f` takes the inut from `./working/original.txt` (where the other options also save the last input to). `-v` takes it from keyboard and `-s` from a following argument. `-n` optionally adds a hint for the llm layer e.g intended style of the text.
`e`, `g` stand for english and german, `tt` for *translate to*, `pr` for proofread.
