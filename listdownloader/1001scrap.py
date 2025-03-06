def filter_lines_with_dash_no_presave(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Filter lines that contain '-' but do not contain 'Pre-Save'
    filtered_lines = [line for line in lines if '-' in line and 'Pre-Save' not in line]

    with open(output_file, 'w') as file:
        file.writelines(filtered_lines)

# Example usage:
# Replace 'input.txt' with your input filename and 'output.txt' with your desired output filename.
filter_lines_with_dash_no_presave('scrap.txt', 'output.txt')
