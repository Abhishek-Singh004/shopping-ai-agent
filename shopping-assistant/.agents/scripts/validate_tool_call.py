import json
import re
import sys


def main():
    # Read all input from stdin
    input_data = sys.stdin.read().strip()
    if not input_data:
        print("Empty input. Command allowed.", file=sys.stderr)
        sys.exit(0)

    command = ""
    # Try to parse as JSON first (common in tool hooks)
    try:
        data = json.loads(input_data)
        # Look for typical tool payload keys
        for key in ["CommandLine", "command", "args", "arguments", "cmd"]:
            if key in data:
                command = str(data[key])
                break
        else:
            # Fallback to stringified JSON if no match keys
            command = input_data
    except json.JSONDecodeError:
        # Fallback to raw string input
        command = input_data

    # Destructive command patterns (e.g. rm -rf, rm -fr)
    destructive_patterns = [
        r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\b",
        r"\brm\s+-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*\b",
        r"\brm\s+-rf\b",
        r"\brm\s+-fr\b",
    ]

    is_destructive = False
    for pattern in destructive_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            is_destructive = True
            break

    if is_destructive:
        print(
            f"Error: Blocked destructive command execution: '{command}'",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Command validated as safe.")
    sys.exit(0)


if __name__ == "__main__":
    main()
