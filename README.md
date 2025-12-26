# README — `show_traffic.py`

## Overview
`show_traffic.py` parses a text file containing repeated **Cisco “show traffic”** sections and produces a per-block report that includes:

- 1-minute input rate (packets/sec and bytes/sec) per interface
- 5-minute input rate (packets/sec and bytes/sec) per interface
- 5-minute drop rate (packets/sec) per interface
- **Average packet size** (bytes/packet) per interface for:
  - 1-minute window (bytes/sec ÷ pkts/sec)
  - 5-minute window (bytes/sec ÷ pkts/sec)

For each “Traffic_block”, the script sorts each table **in descending order** by the metric being printed.

## Input File Format Expectations
The script looks for “show traffic” blocks delimited by these marker lines:

- Start marker: `------ show traffic --------`
- End marker: `--------------------------------`

All non-empty lines between these markers are collected into a block.

### Important structural assumption
Within each block, the script assumes the data repeats in **groups of 13 lines per interface**, and it extracts specific lines by index:

- Interface name: every 13th line starting at index `0`
- **1-minute input rate**: every 13th line starting at index `7`
- **5-minute input rate**: every 13th line starting at index `10`
- **5-minute drop rate**: every 13th line starting at index `12`

For correct results, your captured output should match this structure.

## What the Script Prints
For each traffic block found, the script prints:

1. **1 Minute Packets Per Second** (sorted desc)
2. **1 Minute Bytes Per Second** (sorted desc)
3. **5 Minute Packets Per Second** (sorted desc)
4. **5 Minute Bytes Per Second** (sorted desc)
5. **5 Minute Drop Rate Packets Per Second** (sorted desc)
6. **1 Minute Avg Packet Size (Bytes/Pkt)** (sorted desc)
7. **5 Minute Avg Packet Size (Bytes/Pkt)** (sorted desc)

Rows with a computed metric of `0` are generally skipped for rate/drop tables.  
For average packet size tables, interfaces are included only when both packets/sec and bytes/sec are > 0.

## Average Packet Size Calculation
Average packet size is computed as:

- **1-minute avg bytes/pkt** = `(1-minute bytes/sec) / (1-minute pkts/sec)`
- **5-minute avg bytes/pkt** = `(5-minute bytes/sec) / (5-minute pkts/sec)`

The output is printed with two decimal places.

## Requirements
- Python 3.x
- No external libraries required

## Usage
Run the script and provide the path to the file containing “show traffic” output when prompted:

```bash
python3 show_traffic.py
```

Example prompt interaction:

```text
Please enter the path to the file: /path/to/show_traffic_output.txt
```

## Example Output (abridged)
```text
Formatted Output for Traffic_block1:

Interface Name                   1 Minute Packets Per Second
inside_VR_MNG:                                        646446
INET:                                                   2754

...

Interface Name        1 Minute Avg Packet Size (Bytes/Pkt)
INET:                                     299.42
inside_VR_MNG:                              52.33
...
```

## Notes / Troubleshooting
- **No output / missing interfaces:** Ensure your input file contains the exact start/end marker lines and that blocks contain the expected 13-line repeating structure.
- **Rates show as 0:** The parser uses basic numeric checks (`str.isdigit()`), so unexpected formatting (extra text, commas in numbers, etc.) can cause values to be treated as invalid.
- **Duplicate blocks:** The script attempts to keep only unique blocks (exact line-for-line match) before processing.

## Customization Ideas
If you want enhancements, common next steps include:
- Printing a **combined table** per interface with both 1-min and 5-min avg packet size in one row
- Supporting numbers with commas (e.g., `33,824,818`)
- Making the “13 lines per interface” assumption configurable or auto-detected
