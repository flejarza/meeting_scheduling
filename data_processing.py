import pandas as pd
import numpy as np


def data_process(N_t):
    
    # INPUT N_t: number of time periods for which scheduling will be performed
   
    # Read availability file and convert strings indicating availability into binary represenattion 
    raw_availability = pd.read_csv('fac_availability.csv')
    raw_availability.replace(to_replace="Yes", value=1, inplace=True)
    raw_availability.replace(to_replace="yes", value=1, inplace=True)
    raw_availability.replace(to_replace=np.nan, value=0, inplace=True)
    
    # Create list of people within group 1 
    faculty_names = raw_availability.iloc[:, 0].tolist()
    raw_availability.index = faculty_names
    raw_availability = raw_availability.iloc[:, 1:]
    
    # Create dictionary of group 1's availability needed in the MIP scheudling problem 
    faculty_availability = {}
    for j in faculty_names:
        faculty_availability[j] = {}
        for t in range(1, N_t+1):
            faculty_availability[j][t] = raw_availability[str(t)][j]

    # Reading group 2's meeting preferences (i.e., ranking of people in group 1 with whom they would like to meet)            
    student_pref_raw = pd.read_csv('student_preference.csv')
    student_names = student_pref_raw.iloc[:, 0].tolist()

    # Create dictionary of group 2's preferences needed in MIP 
    student_ranking = {}
    for i in student_names:
        student_ranking[i] = {}
        pref_i = student_pref_raw[student_pref_raw.iloc[:, 0] == i].iloc[0]
        pref_i_list = pref_i.tolist()
        pref_i_list = pref_i_list[2:]
        score = 7
        # The 6 in the range represents that 6 preferences must be indicated (rank 6 people from group 1)
        for rank in range(0, 6):
            score += -1
            student_ranking[i][pref_i_list[rank]] = score
            for j in faculty_names:
                if j in pref_i_list:
                    continue
                else:
                    student_ranking[i][j] = 0


    for index, row in student_pref_raw.iterrows():
        faculty_list = student_pref_raw.iloc[index,2:].tolist()
        for i in faculty_list:
            if i not in faculty_names:
                print(i,": needs replacement")



    return faculty_names, faculty_availability, student_names, student_ranking
