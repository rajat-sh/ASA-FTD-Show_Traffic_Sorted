def process_traffic_blocks(file_path):
    start_marker = "------ show traffic --------"
    end_marker = "--------------------------------"

    inside_range = False
    traffic_blocks = []  # Store unique lists for each block
    int_traffic_blocks = []  # Lists of every 13th element starting from 0th
    min_int_traffic_blocks = []  # Lists of every 13th element starting from 7th
    five_min_int_traffic_blocks = []  # Lists of every 13th element starting from 10th
    five_min_drop_traffic_blocks = []  # Lists of every 13th element starting from 12th

    # Open the file for reading
    try:
        with open(file_path, 'r') as file:
            current_block = []

            for line in file:
                # Check for the start marker
                if start_marker in line:
                    inside_range = True
                    current_block = []  # Start a new block
                    continue

                # Check for the end marker
                if end_marker in line:
                    inside_range = False
                    if current_block and current_block not in traffic_blocks:  # Check for uniqueness
                        traffic_blocks.append(current_block)
                        int_block = [current_block[i] for i in range(0, len(current_block), 13)]
                        min_int_block = [current_block[i] for i in range(7, len(current_block), 13)]
                        five_min_int_block = [current_block[i] for i in range(10, len(current_block), 13)]
                        five_min_drop_block = [current_block[i] for i in range(12, len(current_block), 13)]
                        int_traffic_blocks.append(int_block)
                        min_int_traffic_blocks.append(min_int_block)
                        five_min_int_traffic_blocks.append(five_min_int_block)
                        five_min_drop_traffic_blocks.append(five_min_drop_block)
                    continue

                # Process lines within the block
                if inside_range:
                    stripped_line = line.strip()
                    if stripped_line:  # Ignore blank lines
                        current_block.append(stripped_line)

        # Process and print each Traffic_block list
        #for i, int_block in enumerate(int_traffic_blocks, start=1):
            #print(f"Int_Traffic_block{i}:")
            #for item in int_block:
                #print(item)
            #print()

        for i, min_int_block in enumerate(min_int_traffic_blocks, start=1):
            #print(f"1_Min_Int_Traffic_block{i}:")
            processed_block = []
            for item in min_int_block:
                # Remove specified substrings
                processed_item = item.replace("1 minute input rate", "").replace("pkts/sec", "").replace("bytes/sec", "").strip()
                processed_block.append(processed_item)
                #print(processed_item)
            min_int_traffic_blocks[i-1] = processed_block
            #print()

        for i, five_min_int_block in enumerate(five_min_int_traffic_blocks, start=1):
            #print(f"5_Min_Int_Traffic_block{i}:")
            processed_block = []
            for item in five_min_int_block:
                # Remove specified substrings
                processed_item = item.replace("5 minute input rate", "").replace("pkts/sec", "").replace("bytes/sec", "").strip()
                processed_block.append(processed_item)
                #print(processed_item)
            five_min_int_traffic_blocks[i-1] = processed_block
            #print()

        for i, five_min_drop_block in enumerate(five_min_drop_traffic_blocks, start=1):
            #print(f"5_MinDrop_Int_Traffic_block{i}:")
            processed_block = []
            for item in five_min_drop_block:
                # Remove specified substrings
                processed_item = item.replace("5 minute drop rate,", "").replace("pkts/sec", "").strip()
                processed_block.append(processed_item)
                #print(processed_item)
            five_min_drop_traffic_blocks[i-1] = processed_block
            #print()

        # Print formatted columns for each block
        for i in range(len(traffic_blocks)):
            print(f"Formatted Output for Traffic_block{i+1}:\n")

            # 1 Minute Packets Per Second
            interface_names = int_traffic_blocks[i]
            pps_rates = [int(item.split(",")[0].strip()) if "," in item and item.split(",")[0].strip().isdigit() else 0 for item in min_int_traffic_blocks[i]]
            sorted_pps_data = sorted(zip(interface_names, pps_rates), key=lambda x: x[1], reverse=True)
            print(f"{'Interface Name':<30}{'1 Minute Packets Per Second':>30}")
            for interface, rate in sorted_pps_data:
                if rate > 0:
                    print(f"{interface:<30}{rate:>30}")
            print()

            # 1 Minute Bytes Per Second
            bps_rates = [int(item.split(",")[1].strip()) if "," in item and item.split(",")[1].strip().isdigit() else 0 for item in min_int_traffic_blocks[i]]
            sorted_bps_data = sorted(zip(interface_names, bps_rates), key=lambda x: x[1], reverse=True)
            print(f"{'Interface Name':<30}{'1 Minute Bytes Per Second':>30}")
            for interface, rate in sorted_bps_data:
                if rate > 0:
                    print(f"{interface:<30}{rate:>30}")
            print()

            # 5 Minute Packets Per Second
            pps_rates = [int(item.split(",")[0].strip()) if "," in item and item.split(",")[0].strip().isdigit() else 0 for item in five_min_int_traffic_blocks[i]]
            sorted_pps_data = sorted(zip(interface_names, pps_rates), key=lambda x: x[1], reverse=True)
            print(f"{'Interface Name':<30}{'5 Minute Packets Per Second':>30}")
            for interface, rate in sorted_pps_data:
                if rate > 0:
                    print(f"{interface:<30}{rate:>30}")
            print()

            # 5 Minute Bytes Per Second
            bps_rates = [int(item.split(",")[1].strip()) if "," in item and item.split(",")[1].strip().isdigit() else 0 for item in five_min_int_traffic_blocks[i]]
            sorted_bps_data = sorted(zip(interface_names, bps_rates), key=lambda x: x[1], reverse=True)
            print(f"{'Interface Name':<30}{'5 Minute Bytes Per Second':>30}")
            for interface, rate in sorted_bps_data:
                if rate > 0:
                    print(f"{interface:<30}{rate:>30}")
            print()

            # 5 Minute Drop Rate Packets Per Second
            drop_rates = [int(item.strip()) if item.strip().isdigit() else 0 for item in five_min_drop_traffic_blocks[i]]
            sorted_drop_data = sorted(zip(interface_names, drop_rates), key=lambda x: x[1], reverse=True)
            print(f"{'Interface Name':<30}{'5 Minute Drop Rate Packets Per Second':>30}")
            for interface, rate in sorted_drop_data:
                if rate > 0:
                    print(f"{interface:<30}{rate:>30}")
            print()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    file_path = input("Please enter the path to the file: ")
    process_traffic_blocks(file_path)

if __name__ == "__main__":
    main()
