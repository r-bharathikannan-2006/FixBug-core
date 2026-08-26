# FixBug - Core (for Windows 10, 11)
FixBug-Core is a AI debugging, CLI application, which is specifically designed for windows users.

<img width="720" height="405" alt="Demo Video" src="https://github.com/user-attachments/assets/bcef7981-6700-4561-9ce8-8960c6255ffb" />


## Table of Content
   1. [About](#about)
   2. [Features](#features)
   3. [Download](#download)
   4. [How it works](#how-it-works)
   5. [How to use](#how-to-use)
   6. [Building FixBug-core](#building-fixbug-core)

## About
FixBug-Core automatically scrapes the console screen buffer to read your last executed command and its exact output, isolating code defects and accelerating your debugging workflow.  When issues are found, FixBug-Core relies on AI to analyze the context and renders syntax-highlighted visual diff comparisons directly in your terminal. Fixbug acts as a context-aware CLI tool for terminal error capture, AST parsing, and AI-powered automated code remediation.
### Features 
- Automated Context Scraping: Captures the specific command typed along with its exact terminal output directly from the Windows console buffer.
- AI-Powered Remediation: Integrates with your local AI orchestration setup to diagnose errors and generate code fixes.
- AI Action Executor: Performs file editing, creation, appending, deletions, and reading a file's content.

## Download 
   [Download Latest Release for windows x64](https://github.com/r-bharathikannan-2006/FixBug-core/releases/latest/download/FixBug_core_Installer.exe)
   
   Or else, you can build the FixBug-Core using instruction provided [here](#building-fixbug).

## How it works
1. **Context Capture**: Upon triggering, FixBug-Core accesses the console buffer to scrape the exact command you just executed (previous Command), alongside its corresponding output or error stack trace.
2. **Codebase Mapping**: To understand the environment it is operating in, FixBug-Core generates a directory tree and skeleton map of your code files, strictly preserving the original string casing of all your folders and files.
3. **Deep Syntax Analysis**: Using Tree-sitter parsers, FixBug-Core reads your source code and generates an Abstract Syntax Tree (AST). During this process, local variable names are explicitly extracted and formatted as individual nodes, ensuring the AI has precise, granular context for debugging.
4. **AI-Driven Execution**: The AI digests the error output, codebase map, and AST to formulate a solution. The AI Action Executor then autonomously reads necessary files and performs precise edits, insertions, or deletions to resolve the issue.
5. **User Confirmation**: Before performing any of these automated actions, FixBug-Core pauses to get your explicit confirmation. Every detail of the proposed modifications will be clearly shown to you for review.
6. **Visual Remediation**: The final changes are rendered back to you in the terminal as a syntax-highlighted visual difference layout, ready for your review.

## How to use
   > After an error, just call fbcore in your terminal.
FixBug-Core operates retroactively. You do not need to wrap your commands or pass your scripts as arguments. Simply run your code normally, and if it crashes, run fixbug-core immediately afterward.
1. #### Configuration
   Before your first run, you need to configure your Gemini API key and preferences.
   Open the interactive settings menu by running any of the following commands:
   ```bash 
   fbcore --settings
   # or
   fbcore -s
   # or
   fbcore config
   ```
   > Note: FixBug-Core will not run without a valid Gemini API key.

2. #### Standard Workflow
   When you encounter an error in your terminal, simply type fbcore. The agent will automatically capture the last executed command, analyze the error output, scan your local codebase, and apply the necessary fixes.
   Example:
   ```bash 
   # 1. You run your script and get an error
   $ python my_app.py
   Traceback (most recent call last):
     File "my_app.py", line 42, in <module>
       process_data(data)
   NameError: name 'data' is not defined
   
   # 2. Call FixBug-Core
   $ fbcore
   ```
   

## Building FixBug-Core
To compile the Python source code into a standalone executable and generate the installer:
1. **Install required packages using pip:**
   Run these commands in Terminal to install required packages:
   1. ``` cd FixBug-Core ```
   2. ``` pip install -r requirements.txt ```
2. **Build executable using pyinstaller:**
   Run this command in the terminal :
   ```txt
   pyinstaller --name FixBug --icon=fixbug.ico --collect-data cfonts --hidden-import tree_sitter_python --hidden-import tree_sitter_javascript --hidden-import
   tree_sitter_typescript --hidden-import tree_sitter_java --hidden-import tree_sitter_kotlin --hidden-import tree_sitter_c_sharp --hidden-import tree_sitter_c --hidden
   import tree_sitter_cpp --hidden-import tree_sitter_go --hidden-import tree_sitter_rust --hidden-import tree_sitter_php --hidden-import tree_sitter_swift --hidden-import
   tree_sitter_ruby --hidden-import tree_sitter_bash --hidden-import tree_sitter_powershell --hidden-import tree_sitter_sql --hidden-import tree_sitter_dart main.py
   ```
3. **Build installer using Inno Setup**:
   Use Inno Setup with the provided installer.iss file to package the compiled executable into a distributable Windows installer.
   1. Download and install Inno setup on your machine.
   2. Open installer.iss file in your machine, press compile inside run tab and wait for it to complete.
   4. Click on the FixBug_core_Installer file inside Output directory and install it.
