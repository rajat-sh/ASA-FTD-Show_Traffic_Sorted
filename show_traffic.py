def process_file_to_list_of_lists(file_path, start_string, end_string):
    """
    Reads a file and extracts non-empty lines between two specified strings,
    treating comma-separated values as separate elements and grouping them
    into sublists of 19 elements each.

    :param file_path: Path to the file to be read.
    :param start_string: The string indicating the start of the desired section.
    :param end_string: The string indicating the end of the desired section.
    :return: A list of lists, each containing 19 elements.
    """
    data = []
    temp_list = []

    try:
        with open(file_path, 'r') as file:
            processing = False

            for line in file:
                stripped_line = line.strip()  # Remove leading and trailing whitespace

                if start_string in stripped_line:
                    processing = True
                    continue

                if end_string in stripped_line and processing:
                    break

                if processing and stripped_line:
                    # Split the line by commas to treat each value as a separate element
                    elements = stripped_line.split(',')
                    temp_list.extend(elements)

                    # Once we have 19 elements, add them as a new sublist
                    while len(temp_list) >= 19:
                        data.append(temp_list[:19])
                        temp_list = temp_list[19:]

        return data

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def modify_elements(data_list):
    """
    Iterates through each element of the list and removes everything up to and including "rate",
    as well as the strings "pkts/sec" and "bytes/sec".

    :param data_list: The list of lists to be modified.
    :return: A modified list of lists.
    """
    modified_data = []
    for row in data_list:
        modified_row = []
        for item in row:
            # Remove everything up to and including "rate"
            if 'rate' in item:
                item = item.split('rate', 1)[-1]
            # Remove the strings "pkts/sec" and "bytes/sec"
            item = item.replace('pkts/sec', '').replace('bytes/sec', '')
            modified_row.append(item.strip())
        modified_data.append(modified_row)
    return modified_data

def print_selected_columns(data_list, heading):
    """
    Prints a list of lists as a table with each sublist representing a row.
    Excludes columns 2 to 7 and blank columns. Formats each column to start
    at the same screen location with at least 5 spaces between columns.
    Adds two-line spaces between rows. Prints specified column headings.

    :param data_list: The list of lists to be printed.
    :param heading: The heading to print before the data.
    """
    column_width = 30  # Set a fixed width for each column to ensure alignment
    headings = ["NAME", "1 min Pps", "1 min Bps", "5 min Pps", "5 min Bps", "1 min drop Pps"]

    # Print the main heading
    print(heading)
    print("\n")  # Two-line space after the main heading

    # Print the column headings
    print('     '.join(f"{heading:<{column_width}}" for heading in headings))
    #print("\n")  # Two-line space after the header

    for row in data_list:
        # Select specific columns: 1, 8, 9, 10, 11, 13 (indexes 0, 7, 8, 9, 10, 12)
        selected_row = [row[i] for i in [0, 7, 8, 13, 14, 12] if i < len(row) and row[i]]
        # Format each column to start at the same screen location
        formatted_row = '     '.join(f"{col:<{column_width}}" for col in selected_row)
        print(formatted_row)
        #print("\n")  # Two-line space between rows

def sort_by_column(data_list, column_index):
    """
    Sorts the data list by the specified column index in decreasing order.

    :param data_list: The list of lists to be sorted.
    :param column_index: The index of the column to sort by (1-based index).
    :return: A sorted list of lists in decreasing order.
    """
    # Adjust column index for zero-based indexing and ensure it is within valid range
    zero_based_index = column_index - 1
    return sorted(data_list, key=lambda x: float(x[zero_based_index]) if x[zero_based_index] else float('-inf'), reverse=True)

# Main function
def main():
    file_path = input("Enter the filename or path: ")
    start_string = 'show traffic'
    end_string = '------------'

    data = process_file_to_list_of_lists(file_path, start_string, end_string)

    # Modify each element to remove specified substrings
    modified_data = modify_elements(data)

    # Print the original list with formatted columns
    print_selected_columns(modified_data, "INPUT DATA")

    # Sort and print the list by different columns in decreasing order
    sort_columns = [8, 9, 10, 11, 13]  # Column indexes to sort by (1-based)
    sort_headings = [
        "\n*****SORTED BY 1 min Pps*****",
        "\n*****SORTED BY 1 min Bps*****",
        "\n*****SORTED BY 5 min Pps*****",
        "\n*****SORTED BY 5 min Bps*****",
        "\n*****SORTED BY 1 min DROP Pps*****"
    ]

    for col_index, heading in zip(sort_columns, sort_headings):
        sorted_data = sort_by_column(modified_data, col_index)
        print_selected_columns(sorted_data, heading)

if __name__ == "__main__":
    main()
