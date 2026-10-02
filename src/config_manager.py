import json
import os
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / "FixBug-core"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "provider": "gemini",       
    "api_key": "",                      
    "model": "gemini-3.6-flash",       
    "ollama_host": "http://localhost:11434",
    "ollama_model": "qwen2.5-coder", 
    "max_agent_loops": 5,
    "output_max_lines": 6,
    "truncate_dot_line_length": 3,
    "theme_command_color": "\x1b[38;2;253;247;161m",
    "theme_output_color": "\x1b[38;2;224;119;123m",
    "theme_exp_color": "\x1b[38;2;253;247;161m",
    "theme_fix_color": "\x1b[38;2;253;247;161m"
}

def load_config() -> dict:
    """Load user configuration from disk."""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            return {**DEFAULT_CONFIG, **user_config}
    except Exception:
        return DEFAULT_CONFIG

def save_config(config_data: dict):
    """Write configuration data to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)

def clear_screen():
    """Clears the terminal screen cleanly across OS environments."""
    if os.name == 'nt':
        os.system('cls')
    else:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

def open_settings_menu(display):
    """Render and handle interactive settings interface."""
    from ai_client import get_installed_ollama_models

    config = load_config()
    display._get_width()
    safe_width = display.printable_width + 4

    while True:
        clear_screen()
        print()
        display.display_title()
        print(f"\n {display.command_color}{' FIXBUG SETTINGS MENU ': ^{safe_width}}\033[0m")
        print(f" {' Use Up/Down Arrows and Enter to Select ': ^{safe_width}}\n")
        print("╭" + "─" * (safe_width - 2) + "╮")

        provider = config.get("provider", "gemini").upper()
        api_key = config.get('api_key', '')
        masked_key = f"{api_key[:6]}...{api_key[-4:]}" if len(api_key) > 10 else "Not Set"

        options = [
            f"1. AI Provider             : {provider}",
            f"2. Gemini API Key          : {masked_key}",
            f"3. Gemini Model            : {config['model']}",
            f"4. Ollama Host             : {config['ollama_host']}",
            f"5. Ollama Model            : {config['ollama_model']}",
            f"6. Max Agent Loops         : {config['max_agent_loops']}",
            f"7. Output Max Lines        : {config['output_max_lines']}",
            "8. Save and Exit",
            "9. Exit Without Saving"
        ]

        selected = display.display_options(options, safe_width)

        if selected.startswith("8"):
            save_config(config)
            print("\n  \033[92mSettings saved successfully.\033[0m\n")
            break
        elif selected.startswith("9"):
            print("\n  \033[91mSettings discarded.\033[0m\n")
            break
        elif selected.startswith("1"):
            clear_screen()
            print()
            display.display_title()
            providers = ["gemini", "ollama", "Cancel"]
            print(f"\n  {display.exp_color}{' SELECT AI PROVIDER ': ^{safe_width}}\033[0m")
            print("╭" + "─" * (safe_width - 2) + "╮")
            p_sel = display.display_options(providers, safe_width)
            if p_sel != "Cancel":
                config['provider'] = p_sel

        elif selected.startswith("2"):
            clear_screen()
            print()
            display.display_title()
            print(f"\n  Current Gemini API Key: {api_key}\n")
            new_key = input("  Enter new API Key (leave blank to cancel): ").strip()
            if new_key: 
                config['api_key'] = new_key

        elif selected.startswith("3"):
            clear_screen()
            print()
            display.display_title()
            models = [
                "gemini-3.6-flash", 
                "gemini-3.6-pro", 
                "gemini-2.5-flash", 
                "Custom Model Name...", 
                "Cancel"
            ]
            print(f"\n  {display.exp_color}{' SELECT GEMINI MODEL ': ^{safe_width}}\033[0m")
            print("╭" + "─" * (safe_width - 2) + "╮")
            mod_sel = display.display_options(models, safe_width)
            
            if mod_sel == "Custom Model Name...":
                print(f"\n  Current Gemini Model: {config['model']}")
                custom_m = input("  Enter custom Gemini model string (e.g. gemini-1.5-pro): ").strip()
                if custom_m:
                    config['model'] = custom_m
            elif mod_sel != "Cancel": 
                config['model'] = mod_sel

        elif selected.startswith("4"):
            clear_screen()
            print()
            display.display_title()
            print(f"\n  Current Ollama Host: {config['ollama_host']}\n")
            new_host = input("  Enter Ollama Host (e.g. http://localhost:11434): ").strip()
            if new_host: 
                config['ollama_host'] = new_host

        elif selected.startswith("5"):
            clear_screen()
            print()
            display.display_title()
            installed_models = get_installed_ollama_models(config['ollama_host'])
            
            ollama_menu_options = list(installed_models) if installed_models else []
            ollama_menu_options.append("Custom Model Name...")
            ollama_menu_options.append("Cancel")

            if installed_models:
                print(f"\n  {display.exp_color}{' INSTALLED OLLAMA MODELS (DETECTED) ': ^{safe_width}}\033[0m")
            else:
                print(f"\n  \033[93m[!] Could not query Ollama models at {config['ollama_host']}\033[0m")
                print(f"  {display.exp_color}{' SELECT OR ENTER OLLAMA MODEL ': ^{safe_width}}\033[0m")
            print("╭" + "─" * (safe_width - 2) + "╮")

            mod_sel = display.display_options(ollama_menu_options, safe_width)

            if mod_sel == "Custom Model Name...":
                print(f"\n  Current Ollama Model: {config['ollama_model']}")
                custom_om = input("  Enter custom Ollama model name (e.g. gemma4, llama3.2): ").strip()
                if custom_om:
                    config['ollama_model'] = custom_om
            elif mod_sel != "Cancel":
                config['ollama_model'] = mod_sel

        elif selected.startswith("6"):
            clear_screen()
            print()
            display.display_title()
            print(f"\n  Current Max Agent Loops: {config['max_agent_loops']}\n")
            new_val = input("  Enter max loops (e.g., 5): ").strip()
            if new_val.isdigit(): 
                config['max_agent_loops'] = int(new_val)

        elif selected.startswith("7"):
            clear_screen()
            print()
            display.display_title()
            print(f"\n  Current Output Max Lines: {config['output_max_lines']}\n")
            new_val = input("  Enter output max lines (e.g., 6): ").strip()
            if new_val.isdigit(): 
                config['output_max_lines'] = int(new_val)