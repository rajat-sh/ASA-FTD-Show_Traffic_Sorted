When troubleshooting it is often useful to see the interfaces which are getting maximum input packets and input drops. If the number of interfaces is large, often it is possible to some error in manual checking.
This script takes show tech as input and prints the interfaces sorted by "1 minute input rate pps", "1 minute input rate bps", "5 minute input rate pps", "5 minute input rate bps", "1 minute drop rate pps".

example

(base) RAJATSH-M-V7QW:LIST_PYTHON rajatsh$ python3 show_traffic.py 
Enter the filename or path: asa_tech
INPUT DATA


NAME                               1 min Pps                          1 min Bps                          5 min Pps                          5 min Bps                          1 min drop Pps                
dmz:                               0                                  44                                 0                                  8                                  0                             
outside:                           58                                 9877                               99                                 7687                               1                             
inside:                            7                                  1092                               2                                  108                                1                             
nlp_int_tap:                       0                                  0                                  0                                  0                                  0                             

*****SORTED BY 1 min Pps*****


NAME                               1 min Pps                          1 min Bps                          5 min Pps                          5 min Bps                          1 min drop Pps                
outside:                           58                                 9877                               99                                 7687                               1                             
inside:                            7                                  1092                               2                                  108                                1                             
dmz:                               0                                  44                                 0                                  8                                  0                             
nlp_int_tap:                       0                                  0                                  0                                  0                                  0                             

*****SORTED BY 1 min Bps*****


NAME                               1 min Pps                          1 min Bps                          5 min Pps                          5 min Bps                          1 min drop Pps                
outside:                           58                                 9877                               99                                 7687                               1                             
inside:                            7                                  1092                               2                                  108                                1                             
dmz:                               0                                  44                                 0                                  8                                  0                             
nlp_int_tap:                       0                                  0                                  0                                  0                                  0                             

*****SORTED BY 5 min Pps*****


NAME                               1 min Pps                          1 min Bps                          5 min Pps                          5 min Bps                          1 min drop Pps                
outside:                           58                                 9877                               99                                 7687                               1                             
inside:                            7                                  1092                               2                                  108                                1                             
dmz:                               0                                  44                                 0                                  8                                  0                             
nlp_int_tap:                       0                                  0                                  0                                  0                                  0                             

*****SORTED BY 5 min Bps*****


NAME                               1 min Pps                          1 min Bps                          5 min Pps                          5 min Bps                          1 min drop Pps                
outside:                           58                                 9877                               99                                 7687                               1                             
inside:                            7                                  1092                               2                                  108                                1                             
dmz:                               0                                  44                                 0                                  8                                  0                             
nlp_int_tap:                       0                                  0                                  0                                  0                                  0                             

*****SORTED BY 1 min DROP Pps*****


NAME                               1 min Pps                          1 min Bps                          5 min Pps                          5 min Bps                          1 min drop Pps                
outside:                           58                                 9877                               99                                 7687                               1                             
inside:                            7                                  1092                               2                                  108                                1                             
dmz:                               0                                  44                                 0                                  8                                  0                             
nlp_int_tap:                       0                                  0                                  0                                  0                                  0                             
