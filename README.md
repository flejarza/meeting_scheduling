# meeting_scheduling
Mixed integer program (MIP) used to schedule meetings between two groups of people. Given a group's availability (i.e., faculty) and the other group's meeting preferences (i.e., ranking of faculty to meet), this program determines how to best schedule such meetings to maximize matching staisfaction.

The matching is performed in two steps. First, two Excel .csv files are read in order to generate dictionaries containing availabilities
and matching prefences. These two are then used in the MIP mdoel to define constraints and the objective function. (Refer to the example files 
in this repo to see what the input data should look like) 

The second step involves formualting and solving the MIP. The user might need to change some parameters based on their needs (i.e., 
how many people are allowed to be at one meeting, how many meetings must be scheduled for the entire time horizon, 
some matching satisfaction level, among others). CPLEX was set as the solver, but any other MIP solver should work as well. 

(This program was build to schedulen faculty and student meetings during a unviersity recruitment event, in order to maximize the prospective students' matching rate given a ranking of faculty they wanted to meet, as well as the faculty availability for a given time period. The names of variables used in this program reflect the problem just described) 

(All data and parameters provided are ficticious and for illustrative purposes only) 
