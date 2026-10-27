A proofreader that uses local lm-studio API and some configurable model loaded there.

To use:
- have the local lm-studio server running with the same model loaded as configured here
- paste text to be corrected in `./working/original.txt`
- run `python proofread.py`
- the tool saves its suggested changes as `./working/suggestions.txt` and shows the diff via `git-delta`.

AI use disclosure:
- `llm_proofreader_system_prompt.txt` is generated from a simpler human-written version by the free web version of Claude...
