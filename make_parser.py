import argparse
import re
from pathlib import Path


def get_value(contents: dict, command: str):
    if not command:
        output = []
        output.append("Variables:")
        for var_name, var_value in contents.get('variables', {}).items():
            output.append(f"{var_name} = {var_value}")
        output.append("\nRules:")
        for rule_name, rule_data in contents.get('rules', {}).items():
            output.append(f"{rule_name}:")
            for cmd in rule_data.get('commands', []):
                output.append(f"\t{cmd}")
        return '\n'.join(output)
    elif command in contents.get('rules', {}):
        commands = contents['rules'][command]['commands']
        return '\n'.join(commands)
    else:
        return f"The command \"{command}\" does not exist, please re-check the target command"


def make_load(file_path: Path):
    makefile_data = {
        "variables": {},
        "rules": {}
    }

    def substitute_variables(text, variables):
        # Regular expression to find variables in the format $(VAR_NAME) or ${VAR_NAME}
        pattern = re.compile(r'\$\((\w+)\)|\$\{(\w+)\}')

        def replace_var(match):
            var_name = match.group(1) or match.group(2)
            return variables.get(var_name, match.group(0))  # If variable not found, leave it as is

        # Keep substituting until all variables are resolved
        previous_text = None
        while previous_text != text:
            previous_text = text
            text = pattern.sub(replace_var, text)
        return text

    def get_root():
        script_directory = Path(__file__).parent
        return str(script_directory)


    makefile_data["variables"]["ROOT_DIR"] = get_root()

    with open(file_path, "r") as file:
        current_target = None
        current_commands = []
        current_command = ""
        in_multiline_command = False

        for line in file:
            line = line.rstrip()
            if not line.strip() or line.strip().startswith("#"):
                continue

            var_match = re.match(r"^(\w+)\s*[:]?=\s*(.*)$", line)
            if var_match and not line.startswith("\t"):
                var_name, var_value = var_match.groups()
                if var_name == 'ROOT_DIR':
                    pass
                else:
                    var_value = substitute_variables(var_value, makefile_data["variables"])
                    makefile_data["variables"][var_name] = var_value
                continue

            target_match = re.match(r"^(\w+):", line)
            target_match2 = re.match(r"^(\w+):=", line)
            if target_match or target_match2 and not in_multiline_command:
                if current_target:
                    for idx, cmd in enumerate(current_commands):
                        current_commands[idx] = substitute_variables(cmd, makefile_data["variables"])
                    makefile_data["rules"][current_target] = {
                        "commands": current_commands
                    }
                current_target = target_match.group(1)
                current_commands = []
                continue

            if line.startswith("\t") or in_multiline_command:
                if line.startswith("\t"):
                    line_content = line[1:]
                else:
                    line_content = line

                # Check if the line ends with a backslash indicating continuation
                if line_content.endswith("\\"):
                    in_multiline_command = True
                    line_content = line_content.rstrip("\\").strip()
                    current_command += line_content + " "
                else:
                    in_multiline_command = False
                    current_command += line_content.strip()
                    # Add the complete command to the list
                    current_commands.append(current_command)
                    current_command = ""
                continue

            if current_target:
                current_commands.append(line)
                continue
        # Save the last target's data if it exists
        if current_target:
            makefile_data["rules"][current_target] = {
                "commands": current_commands
            }

        # After parsing, perform variable substitution in variable values
        for var_name in makefile_data["variables"]:
            var_value = makefile_data["variables"][var_name]
            makefile_data["variables"][var_name] = substitute_variables(var_value, makefile_data["variables"])

        # Then perform variable substitution in commands
        for target in makefile_data["rules"]:
            commands = makefile_data["rules"][target]["commands"]
            for idx, cmd in enumerate(commands):
                commands[idx] = substitute_variables(cmd, makefile_data["variables"])

    return makefile_data


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_path', type=Path, required=True, help='path to the make file')
    parser.add_argument('-c', '--commands', type=str, required=False,
                        help='provide the command key to provide the value')
    return parser.parse_args()


def main():
    args = args_parser()
    make_file_path = args.file_path
    command = args.commands
    contents = make_load(make_file_path)

    print(get_value(contents, command))


if __name__ == '__main__':
    main()
