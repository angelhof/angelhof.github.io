---
layout: post
title: Using try to make Copilot command suggestion a bit saner
overview: true
tags: [try, copilot, LLM]
---

Here is a cool usecase of our recently published tool, [try](https://github.com/binpash/try) that can help when using [Github Copilot in the CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli). Thanks to [Mayank](https://mkeoliya.github.io/) who came up with it! 

__TL;DR:__ Use `try` around commands suggested by LLMs to not accidentally destroy your system 😌

LLMs are here and developers use them increasingly often to suggest programs and commands to them by describing what they want in natural language. A particular usecase is [Github Copilot in the CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) which suggests shell commands that can then be easily copied to the clipboard or explained. Here is an example that I recently used to delete some garbage files that get generated when copying files from a location in Windows to WSL: 

```console
$ gh copilot suggest "delete all files in this directory recursively that end with :Zone.Identifier"

Welcome to GitHub Copilot in the CLI!
version 0.5.4-beta (2024-01-04)

I'm powered by AI, so surprises and mistakes are possible. Make sure to verify any generated code or suggestions, and share feedback so that we can learn and improve. For more information, see https://gh.io/gh-copilot-transparency

? What kind of command can I help you with?
> generic shell command

Suggestion:

  find . -name "*:Zone.Identifier" -delete

? Select an option
> Explain command

Explanation:

  • find is used to search for files and directories.
    • . specifies that we want to start the search from the current directory.
    • -name "*:Zone_Identifier" specifies that we want to search for files or directories with names ending in :Zone_Identifier.
    • -delete deletes the files found.


? Select an option
> Copy command to clipboard

Command copied to clipboard!

? Select an option  [Use arrows to move, type to filter]
> Copy command to clipboard
  Explain command
  Revise command
  Rate response
  Exit
```

Even though Copilot offers to explain this command, can we actually trust it??<a class="footnote" href="#fn-1"><sup>1</sup></a> <span class="footnoteText">In fact this command does not exactly capture the original intent, because it can also delete directories! One should use `-type f` to prevent that, but how could you have guessed to ask?!.</span> It is not very wise to immediately run this command on your system before first carefully looking at `find`'s manpage to determine if this usage is correct---but that beats the purpose of using an LLM in the first place. This is where `try` can be very helpful as a safeguard when running the suggested command. 

[try](https://github.com/binpash/try) is a tool that allows you to easily run a shell command in a sandbox to first inspect its effects before commiting it. We can use `try` to run the Copilot suggested command and inspect all the modifications that it would do:

```console
$ try 'find . -name "*:Zone.Identifier" -delete'

Changes detected in the following files:

/home/konstantinos/University/job-applications/univ1/research-statement.pdf:Zone.Identifier (deleted)
/home/konstantinos/University/job-applications/univ2/teaching-statement.pdf:Zone.Identifier (deleted)
/home/konstantinos/University/job-applications/univ3/cover-letter.pdf:Zone.Identifier (deleted)
/home/konstantinos/University/job-applications/univ3/teaching-statement.pdf:Zone.Identifier (deleted)
/home/konstantinos/University/job-applications/univ4/cover-letter.pdf:Zone.Identifier (deleted)
/home/konstantinos/University/job-applications/univ5/cover-letter.pdf:Zone.Identifier (deleted)
/home/konstantinos/University/job-applications/univ6/cover-letter.pdf:Zone.Identifier (deleted)

Commit these changes? [y/N]
```

If the changes look OK, we can ask `try` to commit, otherwise we can revise the command by mentioning the counterexample. `try` has more features to help with exploring the changes, like using `try explore` to spawn a shell in the sandbox and play around seeing if the changes are actually reasonable. You can find out more about it on [Github](https://github.com/binpash/try).

Links:

- try: [Github repo](https://github.com/binpash/try)
- Github Copilot: [Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)