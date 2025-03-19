When troubleshooting it is often useful to see the interfaces which are getting maximum input packets and input drops. If the number of interfaces is large, often it is possible to some error in manual checking.
This script takes show tech as input and prints the interfaces sorted by "1 minute input rate pps", "1 minute input rate bps", "5 minute input rate pps", "5 minute input rate bps", "1 minute drop rate pps".

