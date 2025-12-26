def process_traffic_blocks(file_path):
    start_marker = "------ show traffic --------"
    end_marker = "--------------------------------"

    inside_range = False
    traffic_blocks = []  # Store unique lists for each block
    int_traffic_blocks = []  # Lists of every 13th element starting from 0th
    min_int_traffic_blocks = []  # Lists of every 13th element starting from 7th
    five_min_int_traffic_blocks = []  # Lists of every 13th element starting from 10th
    five_min_drop_traffic_blocks = []  # Lists of every 13th element starting from 12th

    try:
        with open(file_path, 'r') as file:
            current_block = []

            for line in file:
                if start_marker in line:
                    inside_range = True
                    current_block = []
                    continue

                if end_marker in line:
                    inside_range = False
                    if current_block and current_block not in traffic_blocks:
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

                if inside_range:
                    stripped_line = line.strip()
                    if stripped_line:
                        current_block.append(stripped_line)

        # Clean up rate lines (same logic you already had)
        for i, min_int_block in enumerate(min_int_traffic_blocks, start=1):
            processed_block = []
            for item in min_int_block:
                processed_item = item.replace("1 minute input rate", "").replace("pkts/sec", "").replace("bytes/sec", "").strip()
                processed_block.append(processed_item)
            min_int_traffic_blocks[i - 1] = processed_block

        for i, five_min_int_block in enumerate(five_min_int_traffic_blocks, start=1):
            processed_block = []
            for item in five_min_int_block:
                processed_item = item.replace("5 minute input rate", "").replace("pkts/sec", "").replace("bytes/sec", "").strip()
                processed_block.append(processed_item)
            five_min_int_traffic_blocks[i - 1] = processed_block

        for i, five_min_drop_block in enumerate(five_min_drop_traffic_blocks, start=1):
            processed_block = []
            for item in five_min_drop_block:
                processed_item = item.replace("5 minute drop rate,", "").replace("pkts/sec", "").strip()
                processed_block.append(processed_item)
            five_min_drop_traffic_blocks[i - 1] = processed_block

        def parse_pkts_bytes(rate_str):
            """
            Expects something like: '646446, 33824818'
            Returns (pkts, bytes) as ints. If invalid, returns (0, 0).
            """
            if "," not in rate_str:
                return 0, 0
            parts = [p.strip() for p in rate_str.split(",", 1)]
            if len(parts) != 2:
                return 0, 0
            pkts = int(parts[0]) if parts[0].isdigit() else 0
            byts = int(parts[1]) if parts[1].isdigit() else 0
            return pkts, byts

        # Print formatted columns for each block (your existing output)
        for i in range(len(traffic_blocks)):
            print(f"Formatted Output for Traffic_block{i+1}:\n")

            interface_names = int_traffic_blocks[i]

            # 1 Minute Packets Per Second
            pps_1 = [parse_pkts_bytes(s)[0] for s in min_int_traffic_blocks[i]]
            sorted_pps_data = sorted(zip(interface_names, pps_1), key=lambda x: x[1], reverse=True)
            print(f"{'Interface Name':<30}{'1 Minute Packets Per Second':>30}")
            for interface, rate in sorted_pps_data:
                if rate > 0:
                    print(f"{interface:<30}{rate:>30}")
            print()

            # 1 Minute Bytes Per Second
            bps_1 = [parse_pkts_bytes(s)[1] for s in min_int_traffic_blocks[i]]
            sorted_bps_data = sorted(zip(interface_names, bps_1), key=lambda x: x[1], reverse=True)
            print(f"{'Interface Name':<30}{'1 Minute Bytes Per Second':>30}")
            for interface, rate in sorted_bps_data:
                if rate > 0:
                    print(f"{interface:<30}{rate:>30}")
            print()

            # 5 Minute Packets Per Second
            pps_5 = [parse_pkts_bytes(s)[0] for s in five_min_int_traffic_blocks[i]]
            sorted_pps_data = sorted(zip(interface_names, pps_5), key=lambda x: x[1], reverse=True)
            print(f"{'Interface Name':<30}{'5 Minute Packets Per Second':>30}")
            for interface, rate in sorted_pps_data:
                if rate > 0:
                    print(f"{interface:<30}{rate:>30}")
            print()

            # 5 Minute Bytes Per Second
            bps_5 = [parse_pkts_bytes(s)[1] for s in five_min_int_traffic_blocks[i]]
            sorted_bps_data = sorted(zip(interface_names, bps_5), key=lambda x: x[1], reverse=True)
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

            # ---------------- NEW: Average Packet Size outputs ----------------
            # Avg size = bytes/sec / pkts/sec (bytes/packet)

            avg_1 = []
            for iface, p, b in zip(interface_names, pps_1, bps_1):
                if p > 0 and b > 0:
                    avg_1.append((iface, b / p))
            avg_1.sort(key=lambda x: x[1], reverse=True)

            print(f"{'Interface Name':<30}{'1 Minute Avg Packet Size (Bytes/Pkt)':>40}")
            for iface, avg in avg_1:
                print(f"{iface:<30}{avg:>40.2f}")
            print()

            avg_5 = []
            for iface, p, b in zip(interface_names, pps_5, bps_5):
                if p > 0 and b > 0:
                    avg_5.append((iface, b / p))
            avg_5.sort(key=lambda x: x[1], reverse=True)

            print(f"{'Interface Name':<30}{'5 Minute Avg Packet Size (Bytes/Pkt)':>40}")
            for iface, avg in avg_5:
                print(f"{iface:<30}{avg:>40.2f}")
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
