#!/usr/bin/env python3
import sys
import glob
import os
import re

# ANSI color codes
BLUE          = "\033[34m"
GREEN         = "\033[32m"
RED           = "\033[31m"
YELLOW        = "\033[33m"
CYAN          = "\033[36m"
MAGENTA       = "\033[35m"
BRIGHT_CYAN   = "\033[96m"
BOLD_MAGENTA  = "\033[1;35m"
BOLD_WHITE    = "\033[1;37m"
BRIGHT_GREEN  = "\033[92m"
RESET         = "\033[0m"

# Additional highlight for search matches (reverse video style)
HIGHLIGHT_MATCH = "\033[7m"

def highlight_modsec(text):
    """
    Apply ModSec syntax highlighting and additional colorization:
      - "SecRule" in cyan.
      - "id:<5-8digits>" in blue.
      - "pass" in green.
      - "block" or "deny" in red.
      - "severity:<digit(s)>" in yellow.
      - "chain" in bright cyan.
      - "setvar:" in magenta.
      - "tag:" in bold magenta.
      - "tx:" (case-insensitive) in bold magenta.
      - Transformation tokens starting with "t:" in yellow, excluding "t:none".
      - "||" operator in bold white.
      - All modsec variable tokens matching %{...} in bright green.
    """
    # Base highlighting
    text = re.sub(r'\bSecRule\b', CYAN + 'SecRule' + RESET, text)
    text = re.sub(r'\bid:(\d{5,8})\b', BLUE + r'id:\1' + RESET, text)
    text = re.sub(r'\bpass\b', GREEN + 'pass' + RESET, text)
    text = re.sub(r'\b(block|deny)\b', RED + r'\1' + RESET, text)
    text = re.sub(r'\bseverity:(\d+)\b', YELLOW + r'severity:\1' + RESET, text)
    
    # Additional highlighting
    text = re.sub(r'\bchain\b', BRIGHT_CYAN + 'chain' + RESET, text)
    text = re.sub(r'\b(setvar:)', MAGENTA + r'\1' + RESET, text)
    text = re.sub(r'\b(tag:)', BOLD_MAGENTA + r'\1' + RESET, text)
    
    # Highlight tx: in a case-insensitive manner
    text = re.sub(r'\b(tx:)', lambda m: BOLD_MAGENTA + m.group(1) + RESET, text, flags=re.IGNORECASE)
    
    # Highlight transformation tokens that start with t: EXCEPT "t:none"
    text = re.sub(r'\bt:(?!none\b)[^,"\s]+\b', YELLOW + r'\g<0>' + RESET, text)
    
    # Highlight the operator "||"
    text = re.sub(r'\|\|', BRIGHT_GREEN + "||" + RESET, text)

    # Highlight the single quote
    text = re.sub(r'\'', RED + "'" + RESET, text)

    # Highlight the double quote
    text = re.sub(r'\"', BRIGHT_GREEN + '"' + RESET, text)

    # Highlight ModSec variables like %{...}
    text = re.sub(r'%\{[^}]+\}', BRIGHT_GREEN + r'\g<0>' + RESET, text)
    
    return text

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <regex_search_term>")
    sys.exit(1)

# Compile the regex search term passed as first argument.
search_regex = sys.argv[1]
pattern = re.compile(search_regex)

# Adjust the file path pattern as needed
path_pattern = "/home/mdre/cl-gerrit/imunify360-modsec/raw_rules/*.conf"

for filepath in glob.glob(path_pattern):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        block = []
        for line in f:
            # A new block starts when encountering a line beginning with "# tags:"
            if line.startswith("# tags:"):
                if block:
                    block_text = "".join(block)
                    if pattern.search(block_text):
                        # Apply modsec syntax highlighting
                        highlighted = highlight_modsec(block_text)
                        # Additionally, highlight the search matches using reverse video
                        highlighted = pattern.sub(lambda m: HIGHLIGHT_MATCH + m.group(0) + RESET, highlighted)
                        print(f"== {os.path.basename(filepath)} ==")
                        print(highlighted)
                        print()
                    block = []
            block.append(line)
        # Process any remaining block at the end of the file
        if block:
            block_text = "".join(block)
            if pattern.search(block_text):
                highlighted = highlight_modsec(block_text)
                highlighted = pattern.sub(lambda m: HIGHLIGHT_MATCH + m.group(0) + RESET, highlighted)
                print(f"== {os.path.basename(filepath)} ==")
                print(highlighted)
                print()
