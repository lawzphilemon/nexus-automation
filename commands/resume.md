---
name: resume
description: Reopen an existing NEXUS article by its project code (NXS-YYMMDD-XXXX), show which stages are done, and continue from the next one
argument-hint: "[project code, slug or keyword]"
allowed-tools: Read, Write, Glob
---

# NEX-0 — Resume a project

**Mission:** Come back to any article later, by its code, without touching other articles' files.

Argument: $ARGUMENTS

## Step 1 — Find the project

- A code was given (any case, e.g. `nxs-261014-7qf3`): open `nexus-output/<CODE>_*/`.
- A slug or keyword was given: search `nexus-output/PROJECTS.md`; if several match, list them and ask which one.
- Nothing was given: show `nexus-output/PROJECTS.md` and ask which project.

If `PROJECTS.md` is missing a project folder that exists, add its row back from the folder name and its files.

## Step 2 — Show where it stands

Read the project's files and report:

```text
Project <CODE> · <slug> · <keyword> · <market>
| Stage | File | Status |
| research / improve / geo / outline / firstdraft / finaldraft / critique / convert | 01-research.md … latest.md, 06-critique.md | done · confirmed · not started |
```

The outline counts as confirmed only when its first line is `Status: confirmed`. `/convert` is done when `latest.md` contains CTA blocks.

## Step 3 — Continue

Keep using this code for every later stage in this conversation. End: tell the user the code, the current status, and the next command to run (for example "Run /firstdraft to continue."). Re-running an earlier stage overwrites only that stage's file in this project; tell the user the later stages should be re-run.
