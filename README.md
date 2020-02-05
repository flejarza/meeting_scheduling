# meeting_scheduling
Mixed integer program used to schedule meetings between two groups of people. Given a groups availability (i.e., faculty) and the other groups meeting preferences (i.e., ranking of faculty to meet), how to best schedule the meetings to maximize matching staisfaction.

The matching is performed in two steps. First, two Excel csv file are reads in order to generate dictionaries containing availability 
and matching prefences. These are the used in the MIP to define constraints and the objective function. (Refer to the example files 
in this repo to see how the input data should look like) 

The second step involves formualting and solving the MIP. The user might need to change some parameters based on their needs (i.e., 
how many people can attend a meeting at the same time, how many meetings must be scheduled in the entire time horizon, and 
some matching satisfaction level, among others). CPLEX was set as the solver, but any other MIP solver should work as well. 
