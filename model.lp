\ENCODING=ISO-8859-1
\Problem name: 

Maximize
 obj1: h_1 + h_2 + h_3 + h_4
Subject To
 c1:  y_1 + y_2 + y_3 + y_4  = 3
 c2:  - y_1 + h_1 <= 0
 c3:  - y_2 + h_2 <= 0
 c4:  - y_3 + h_3 <= 0
 c5:  - y_4 + h_4 <= 0
 c6:  - y_2 + h_1 <= 0
 c7:  - y_3 + h_1 <= 0
 c8:  - y_4 + h_1 <= 0
 c9:  - y_1 + h_2 <= 0
 c10: - y_1 + h_3 <= 0
 c11: - y_1 + h_4 <= 0
 c12: - y_1 - y_2 - y_3 - y_4 + h_1 >= -3
 c13: - y_1 - y_2 + h_2 >= -1
 c14: - y_1 - y_3 + h_3 >= -1
 c15: - y_1 - y_4 + h_4 >= -1
Bounds
 0 <= y_1 <= 1
 0 <= y_2 <= 1
 0 <= y_3 <= 1
 0 <= y_4 <= 1
 0 <= h_1 <= 1
 0 <= h_2 <= 1
 0 <= h_3 <= 1
 0 <= h_4 <= 1
Binaries
 y_1  y_2  y_3  y_4  h_1  h_2  h_3  h_4 
End
