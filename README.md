# Course-Allocation-using-Maximum-Bipartite-Matching
Course Allocation for Professors using **Maximum Unweighted Bipartite Matching** according to Professor Preferences.

##  Problem Statement

The research problem at hand revolves around the optimization of the University Course Assignment System. Within a department, there are "n" faculty members categorised into three distinct groups: "x1," "x2," and "x3." Faculty in each category are assigned different course loads, with "x1" handling 0.5 courses per semester, "x2" taking 1 course per semester, and "x3" managing 1 or 1.5 courses per semester.  
  
In this system, faculty members have the flexibility to take multiple courses in a given semester, and conversely, a single course can be assigned to multiple faculty members. When a course is shared between two professors, each professor's load is considered to be 0.5 courses. Moreover, each faculty member maintains a preference list of courses, ordered by their personal preferences, with the most preferred courses appearing at the top. Importantly, there is no prioritisation among faculty members within the same category.  
  
The primary objective of this research problem is to develop an assignment scheme that maximises the number of courses assigned to faculty while aligning with their preferences and the category-based constraints ("x1," "x2," "x3"). The challenge lies in ensuring that a course can only be assigned to a faculty member if it is present in their preference list.  
  
This problem is unique due to the flexibility it offers regarding the number of courses faculty members can take, distinct from typical Assignment problems. Potential modifications may include adjusting the maximum number of courses "y" for each category of professors, instead of requiring exact adherence, or extending the number of professor categories beyond the existing three to devise a more generalised solution.

## Abstract

Allocation of courses to professors is an endeavour common to all universities. Similar processes with the same underlying concept are applicable to other organizations as well. We attempt to automate this process in order to make it fast, efficient and trustworthy.

For this purpose, we use the **Enumerating Maximum Matchings Algorithm (EMMA)** and **NetworkX** library in python coding language. The technique we employ is that of **One-One Maximum Unweighted Bipartite Matchings**, by applying appropriate constraints to generate feasible allocations. We then assign **Satisfaction Scores** to these allocations based on the preference orders given by professors and display them in decreasing orders of Scores. 

Thus, we present all possible allocations of courses to professors in descending order of preference.

## Dependencies

 - Python
 - NetworkX
 - NumPy
 - Pandas

## Team

 - Param Gandhi
 - Soham Khadilkar
 - Anish Shastry
