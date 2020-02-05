from pyomo.environ import *
import data_processing
import xlsxwriter

import numpy as np
import gc
import cplex
import pandas as pd


N_t = 9         # Number of time periods for scheduling a given day
# Calling data processing routing 
faculty_names, faculty_availability, student_names, student_ranking = data_processing.data_process()


m = ConcreteModel()

# Define group 1 
m.students = Set(initialize = student_names)
# Define group 2 
m.faculty = Set(initialize = faculty_names)
# Define the time periods for which scheduling is needed 
m.time_slots = RangeSet(1,N_t)

# Availability parameter 
def a_jt_init(m,j,t):
    return faculty_availability[j][t]

m.a_jt = Param(m.faculty,m.time_slots, initialize = a_jt_init)

# Preference parameter
def p_ij_init(m,i,j):
    return student_ranking[i][j]

m.p_ij = Param(m.students, m.faculty, initialize = p_ij_init)

# Variable x_ijt = {0,1} if student i is scheduled to meet faculty j at time slot t
m.x_ijt = Var(m.students, m.faculty, m.time_slots, within = Binary)

# Objective (maximize the matching score) 
m.obj = Objective(expr = -sum(sum(sum(m.p_ij[i,j]*m.x_ijt[i,j,t] for i in m.students) for j in m.faculty) \
                             for t in m.time_slots))

# Constraints
# Feasibility cuts to improve (allegedly) solution time
for j in m.faculty:
    for t in m.time_slots:
        if m.a_jt[j,t] == 0:
            for i in m.students:
                m.x_ijt[i,j,t] = 0
                m.x_ijt[i, j, t].fixed = True

# Students can only be in one meeting at a given time
def c1_rule(m, i, t):
    return sum(m.x_ijt[i,j,t] for j in m.faculty) <= 1

m.c_1 = Constraint(m.students, m.time_slots, rule = c1_rule)

# Meetings can have a max number of 3 students each
def c2_rule(m, j, t):
    return sum(m.x_ijt[i,j,t] for i in m.students) <= 3

m.c_2 = Constraint(m.faculty, m.time_slots, rule = c2_rule )

# All students must have four meetings scheduled
def c3_rule(m, i):
    return sum(sum(m.x_ijt[i,j,t] for j in m.faculty) for t in m.time_slots) == 4

m.c_3 = Constraint(m.students, rule = c3_rule )

# Students can only meet with faculty once
def c4_rule(m,i,j):
    return sum(m.x_ijt[i,j,t] for t in m.time_slots) <= 1

m.c_4 = Constraint(m.students, m.faculty, rule = c4_rule)

# Constraint used to establish that a certain level of "satisfaction" must be attained for every student (in this particular
# case each student must have a "mathcing score" >= 14, which implies that they are scheudled meetings with at least 2 out of
# the top 4 members in group 1 as provided in their ranking) 
def c5_rule(m,i):
    return  sum(sum(m.p_ij[i,j]*m.x_ijt[i,j,t] for j in m.faculty) for t in m.time_slots) >= 14

m.c_5 = Constraint(m.students, rule = c5_rule)

# Solving model 
solver = SolverFactory('cplex')
solver.options['mipgap'] = 0.05
solver.options['timelimit'] = 1000
results = solver.solve(m, tee=True, symbolic_solver_labels=True)

# Writing results back into Excel file 
workbook = xlsxwriter.Workbook('student_meeting_schedule.xlsx')
schedule = workbook.add_worksheet('schedule')

student_row = 1
for i in student_names:
    schedule.write(student_row, 0, i)
    for j in faculty_names:
        for t in range(1, 10):
            schedule.write(0, t, t)
            if m.x_ijt[i,j,t].value > 0:
                schedule.write(student_row, t, j)

    student_row += 1




workbook.close()












