import pandas as pd
import numpy as np


def data_process():
    raw_availability = pd.read_csv('fac_availability.csv')
    raw_availability.replace(to_replace="Yes", value=1, inplace=True)
    raw_availability.replace(to_replace="yes", value=1, inplace=True)
    raw_availability.replace(to_replace=np.nan, value=0, inplace=True)
    faculty_names = raw_availability.iloc[:, 0].tolist()
    raw_availability.index = faculty_names
    raw_availability = raw_availability.iloc[:, 1:]

    faculty_availability = {}
    for j in faculty_names:
        faculty_availability[j] = {}
        for t in range(1, 10):
            faculty_availability[j][t] = raw_availability[str(t)][j]

    student_pref_raw = pd.read_csv('student_preference.csv')
    student_names = student_pref_raw.iloc[:, 0].tolist()

    student_ranking = {}
    for i in student_names:
        student_ranking[i] = {}
        pref_i = student_pref_raw[student_pref_raw.iloc[:, 0] == i].iloc[0]
        pref_i_list = pref_i.tolist()
        pref_i_list = pref_i_list[2:]
        score = 7
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
