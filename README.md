# FixBug - Core (Windows)
FixBug is a AI debugging, CLI application, which is specifically designed for windows users.

<img width="720" height="405" alt="Demo Video" src="https://github.com/user-attachments/assets/bcef7981-6700-4561-9ce8-8960c6255ffb" />


## Table of Content

## About
FixBug automatically scrapes the console screen buffer to read your last executed command and its exact output, isolating code defects and accelerating your debugging workflow.  When issues are found, FixBug relies on AI to analyze the context and renders syntax-highlighted visual diff comparisons directly in your terminal. Context-aware CLI tool for terminal error capture, AST parsing, and AI-powered automated code remediation.
### Features 
- Automated Context Scraping: Captures the specific command typed along with its exact terminal output directly from the Windows console buffer.
- AI-Powered Remediation: Integrates with your local AI orchestration setup to diagnose errors and generate code fixes.
- AI Action Executor: Performs file editing, creation, appending, deletions, and reading a file's content.

## Download 
[Download Latest Release for windows x64](https://github.com/r-bharathikannan-2006/FixBug-core/releases/latest/download/FixBug_core_Installer.exe
)

## How it works
1. **Context Capture**: Upon triggering, FixBug accesses the console buffer to scrape the exact command you just executed (previous Command), alongside its corresponding output or error stack trace.
2. **Codebase Mapping**: To understand the environment it is operating in, FixBug generates a directory tree and skeleton map of your code files, strictly preserving the original string casing of all your folders and files.
3. **Deep Syntax Analysis**: Using Tree-sitter parsers, FixBug reads your source code and generates an Abstract Syntax Tree (AST). During this process, local variable names are explicitly extracted and formatted as individual nodes, ensuring the AI has precise, granular context for debugging.
4. **AI-Driven Execution**: The AI digests the error output, codebase map, and AST to formulate a solution. The AI Action Executor then autonomously reads necessary files and performs precise edits, insertions, or deletions to resolve the issue.
5. **User Confirmation**: Before performing any of these automated actions, FixBug pauses to get your explicit confirmation. Every detail of the proposed modifications will be clearly shown to you for review.
6. **Visual Remediation**: The final changes are rendered back to you in the terminal as a syntax-highlighted visual difference layout, ready for your review.

## Getting Started
### Building fixbug
To compile the Python source code into a standalone executable and generate the installer:
1. Refer to command_to_build.txt for the specific PyInstaller build commands. <details>
<summary>Click to view command_to_build.txt (Command to run) file contents</summary>

```txt
pyinstaller --name FixBug --icon=fixbug.ico --collect-data cfonts --hidden-import tree_sitter_python --hidden-import tree_sitter_javascript --hidden-import tree_sitter_typescript --hidden-import tree_sitter_java --hidden-import tree_sitter_kotlin --hidden-import tree_sitter_c_sharp --hidden-import tree_sitter_c --hidden-import tree_sitter_cpp --hidden-import tree_sitter_go --hidden-import tree_sitter_rust --hidden-import tree_sitter_php --hidden-import tree_sitter_swift --hidden-import tree_sitter_ruby --hidden-import tree_sitter_bash --hidden-import tree_sitter_powershell --hidden-import tree_sitter_sql --hidden-import tree_sitter_dart main.py
```

</details>
3. Use Inno Setup with the provided installer.iss file to package the compiled executable into a distributable Windows installer.




