import copy
import json
from timeit import default_timer as timer

import networkx as nx
import pandas as pd

import AllMaxMatching

start = timer()


def coursehas2(course, matching):
    """for constraint3, checks if a course has 2 units assigned"""
    coursename = Courses[course].split("||")[0]
    match1 = False
    match2 = False
    for edge in matching:
        if (edge[0] == (0, Courses.index(coursename + "||1"))) or (edge[1] == (0, Courses.index(coursename + "||1"))):
            match1 = True
        if (edge[0] == (0, Courses.index(coursename + "||2"))) or (edge[1] == (0, Courses.index(coursename + "||2"))):
            match2 = True
        if match1 and match2:
            break
    return match1 and match2


def profhas3(prof, matching):
    """for constraint3, checks if a professor has 3 units assigned, and if so, checks if the other 2 courses have 2
    units assigned"""
    Professor = Professors[prof].split("||")[0]
    match1 = False
    match2 = False
    match3 = False
    match1course = None
    match2course = None
    match3course = None
    for edge in matching:
        if (edge[0] == (1, Professors.index(Professor + "||1"))) or (
                edge[1] == (1, Professors.index(Professor + "||1"))):
            match1 = True
            if edge[0][0] == 0:
                match1course = edge[0][1]
            else:
                match1course = edge[1][1]
        if (edge[0] == (1, Professors.index(Professor + "||2"))) or (
                edge[1] == (1, Professors.index(Professor + "||2"))):
            match2 = True
            if edge[0][0] == 0:
                match2course = edge[0][1]
            else:
                match2course = edge[1][1]
        if (edge[0] == (1, Professors.index(Professor + "||3"))) or (
                edge[1] == (1, Professors.index(Professor + "||3"))):
            match3 = True
            if edge[0][0] == 0:
                match3course = edge[0][1]
            else:
                match3course = edge[1][1]
        if match1 and match2 and match3:
            break
    if match1 and match2 and match3:
        if (Professors[prof].split("||")[1] == "1") and coursehas2(match2course, matching) and coursehas2(match3course,
                                                                                                          matching):
            return True
        elif ((Professors[prof].split("||")[1] == "2") and coursehas2(match1course, matching) and coursehas2(
                match3course, matching)):
            return True
        elif ((Professors[prof].split("||")[1] == "3") and coursehas2(match1course, matching) and coursehas2(
                match2course, matching)):
            return True
        else:
            return False


# ---------------------------------------------------------------------------------------------------------------------#
# -------READING INPUTS FROM DIFFERENT SOURCES AND CONVERTING THEM TO THE REQUIRED FORMAT------------------------------#
# -------UNCOMMENT THE REQUIRED INPUT METHOD OF CHOICE ----------------------------------------------------------------#


# """reading input from csv file"""
# df_Courses = pd.read_csv('Courses.csv')
# df_Profs = pd.read_csv('Professors.csv')
# df_Data = pd.read_csv('Preferences.csv')


"""reading input from Excel file"""
df_Courses = pd.read_excel('Input.xlsx', sheet_name='Courses')
df_Profs = pd.read_excel('Input.xlsx', sheet_name='Professors')
df_Data = pd.read_excel('Input.xlsx', sheet_name='Preferences')

FDCDCs = df_Courses.FDCDCs.dropna().tolist()
FDElecs = df_Courses.FDElecs.dropna().tolist()
HDCDCs = df_Courses.HDCDCs.dropna().tolist()
HDElecs = df_Courses.HDElecs.dropna().tolist()

Cat1 = df_Profs.Category1.dropna().tolist()  # only 1 unit (0.5 course)
Cat2 = df_Profs.Category2.dropna().tolist()  # only 2 units (1 course)
Cat3 = df_Profs.Category3.dropna().tolist()  # only 3 units (1.5 courses)

Raw_Data = {}
for column in df_Data.columns:
    Raw_Data[column] = df_Data[column].dropna().tolist()
Raw_Data = dict(sorted(Raw_Data.items()))

# """Direct input"""
# FDCDCs = ["Course0", "Course1"]
# FDElecs = ["Course2", "Course3"]
# HDCDCs = ["Course4", "Course5"]
# HDElecs = ["Course6", "Course7"]

# Cat1 = ["Prof0"]  # only 1 unit (0.5 course)
# Cat2 = ["Prof1", "Prof2", "Prof5", ]  # only 2 units (1 course)
# Cat3 = ["Prof3", "Prof4"]  # only 3 units (1.5 courses)

# Raw_Data = {"Prof0": ["Course0", "Course1"],
#             "Prof1": ["Course0", "Course1"],
#             "Prof2": ["Course0", "Course2"],
#             "Prof3": ["Course0", "Course4"],
#             "Prof4": ["Course4", "Course6"],
#             "Prof5": ["Course2", "Course5"]}


# print(Raw_Data)

Raw_Professors = list(Raw_Data.keys())
Raw_Courses = list(set([item for sublist in Raw_Data.values() for item in sublist]))
Raw_Courses.sort()
# print(Raw_Professors)
# print(Raw_Courses)

for cdc in (FDCDCs + HDCDCs):
    if cdc not in Raw_Courses:
        print(f"{cdc} CDC not in any professor's preferences")
        exit()

"""converting each course to 2 units"""
Courses = []
for item in Raw_Courses:
    Courses.append(item + "||1")
    Courses.append(item + "||2")
# print(Courses)

"""converting each professor to 1, 2, 3 units according to their category"""
Professors = []
for item in Raw_Professors:
    if item in Cat1:
        Professors.append(item + "||1")
    elif item in Cat2:
        Professors.append(item + "||1")
        Professors.append(item + "||2")
    elif item in Cat3:
        Professors.append(item + "||1")
        Professors.append(item + "||2")
        Professors.append(item + "||3")
# print(Professors)

"""modifying the data to fit the new format"""
Data = {}
for prof in Raw_Data:
    raw_course = Raw_Data[prof]
    course = []
    for item in raw_course:
        course.append(item + "||1")
        course.append(item + "||2")
    if prof in Cat1:
        Data.update({prof + "||1": course})
    elif prof in Cat2:
        Data.update({prof + "||1": course})
        Data.update({prof + "||2": course})
    elif prof in Cat3:
        Data.update({prof + "||1": course})
        Data.update({prof + "||2": course})
        Data.update({prof + "||3": course})
# print(Data)


"""creating graph and edges according to data and generating matchings"""
g = nx.Graph()
edges = []
# for p in Raw_Professors:
#     for c in Raw_Data[p]:
#         edges.append([(1, Raw_Professors.index(p)), (0, Courses.index(c))])

for p in Professors:
    for c in Data[p]:
        edges.append([(1, Professors.index(p)), (0, Courses.index(c))])
# print(edges)
RawMaxMatchingsList = AllMaxMatching.listAllMaxMatchings(g, edges)
# print(*RawMaxMatchingsList, sep='\n')
# print(len(RawMaxMatchingsList))

MaxMatchingsList = copy.deepcopy(RawMaxMatchingsList)


"""weeding out the matchings that are not satisfying constraints"""
if len(MaxMatchingsList) > 0:
    for matching in RawMaxMatchingsList:
        removed = False

        """constraint 1: Cat 1, 2 professors must be assigned 1 and 2 units respectively,
         and Cat 3 professors can be assigned either 2 or 3 units"""
        for prof in Raw_Professors:
            if prof in Cat1:
                match = False
                for edge in matching:
                    if (edge[0] == (1, Professors.index(prof + "||1"))) or (
                            edge[1] == (1, Professors.index(prof + "||1"))):
                        match = True
                        break
                if not match:
                    MaxMatchingsList.remove(matching)
                    removed = True
                    break
            elif prof in Cat2:
                match1 = False
                match2 = False
                for edge in matching:
                    if (edge[0] == (1, Professors.index(prof + "||1"))) or (
                            edge[1] == (1, Professors.index(prof + "||1"))):
                        match1 = True
                    if (edge[0] == (1, Professors.index(prof + "||2"))) or (
                            edge[1] == (1, Professors.index(prof + "||2"))):
                        match2 = True
                    if match1 and match2:
                        break
                if not (match1 and match2):
                    MaxMatchingsList.remove(matching)
                    removed = True
                    break
            elif prof in Cat3:
                match1 = False
                match2 = False
                match3 = False
                for edge in matching:
                    if (edge[0] == (1, Professors.index(prof + "||1"))) or (
                            edge[1] == (1, Professors.index(prof + "||1"))):
                        match1 = True
                    if (edge[0] == (1, Professors.index(prof + "||2"))) or (
                            edge[1] == (1, Professors.index(prof + "||2"))):
                        match2 = True
                    if (edge[0] == (1, Professors.index(prof + "||3"))) or (
                            edge[1] == (1, Professors.index(prof + "||3"))):
                        match3 = True
                    if (match1 and match2) or (match1 and match3) or (match2 and match3):
                        break
                if not ((match1 and match2) or (match1 and match3) or (match2 and match3)):
                    MaxMatchingsList.remove(matching)
                    removed = True
                    break
        if removed:
            continue

        """constraint 2: Both units of CDCs should be satisfied"""
        for course in (FDCDCs + HDCDCs):
            match1 = False
            match2 = False
            for edge in matching:
                if (edge[0] == (0, Courses.index(course + "||1"))) or (edge[1] == (0, Courses.index(course + "||1"))):
                    match1 = True
                if (edge[0] == (0, Courses.index(course + "||2"))) or (edge[1] == (0, Courses.index(course + "||2"))):
                    match2 = True
                if match1 and match2:
                    break
            if not (match1 and match2):
                MaxMatchingsList.remove(matching)
                removed = True
                break
        if removed:
            continue

        """constraint 3: For elective courses, either both or no units should be satisfied.
        We also check for certain eligible matchings which are not maximum, but whose maximum version is eliminated due 
        to this constraint"""

        problematic_edges = []
        for course in (FDElecs + HDElecs):
            if course in Raw_Courses:
                match1 = False
                match2 = False
                problem = None
                for edge in matching:
                    if (edge[0] == (0, Courses.index(course + "||1"))) or (
                            edge[1] == (0, Courses.index(course + "||1"))):
                        match1 = True
                        problem = edge
                    if (edge[0] == (0, Courses.index(course + "||2"))) or (
                            edge[1] == (0, Courses.index(course + "||2"))):
                        match2 = True
                        problem = edge
                    if match1 and match2:
                        break
                if (match1 and not match2) or (match2 and not match1):
                    if (((problem[0][0] == 1) and (Professors[problem[0][1]].split("||")[0] in Cat3)
                         and (profhas3(problem[0][1], matching)))
                            or
                            ((problem[1][0] == 1) and (Professors[problem[1][1]].split("||")[0] in Cat3)
                             and (profhas3(problem[1][1], matching)))):
                        problematic_edges.append(problem)
                        # matching.remove(problem)
                    else:
                        MaxMatchingsList.remove(matching)
                        removed = True
                        break
        if len(problematic_edges) > 0 and not removed:
            # print("problematic edges", problematic_edges)
            # print("matching", matching)
            index = MaxMatchingsList.index(matching)
            for problem in problematic_edges:
                # print(*MaxMatchingsList , sep='\n')
                # print("problem", problem)
                # print(index)
                # print(MaxMatchingsList[index])
                MaxMatchingsList[index].remove(problem)
                # print(MaxMatchingsList[MaxMatchingsList.index(matching)])

# print(*MaxMatchingsList, sep='\n')
# print(len(MaxMatchingsList))
# print(len(RawMaxMatchingsLmist))


"""converting the output to the original format"""
Output_List = []
for matching in MaxMatchingsList:
    output = []
    unindexed_output = []

    for edge in matching:
        if edge[0][0] == 1:
            match = (Professors[edge[0][1]].split("||")[0], Courses[edge[1][1]].split("||")[0])
        else:
            match = (Professors[edge[1][1]].split("||")[0], Courses[edge[0][1]].split("||")[0])
        if match in unindexed_output:
            output = [(x, y, z + 1) if (x == match[0] and y == match[1]) else (x, y, z) for (x, y, z) in output]
        else:
            output.append((match[0], match[1], 1))
            unindexed_output.append(match)

    exists = False
    for i in Output_List:
        if set(i) == set(output):
            exists = True
            break
    if not exists:
        Output_List.append(output)

"""sort outputlist according to professors"""
for i in range(len(Output_List)):
    Output_List[i] = sorted(Output_List[i], key=lambda x: x[0])

# print(*Output_List, sep='\n')
print(f"Number of satisfactory matchings: {len(Output_List)}")
# print(len(MaxMatchingsList))
# print(len(RawMaxMatchingsList))

"""Assigning Satisfaction Scores according to the Course Priorities of the Professors"""
MaxPoints = len(Raw_Courses)
Scores = {}
for match in Output_List:
    score = 0
    for item in match:
        score += (MaxPoints - Raw_Data[item[0]].index(item[1])) * item[2]
    Scores.update({tuple(match): score})
Sorted_Scores = dict(sorted(Scores.items(), key=lambda x: x[1], reverse=True))


"""printing the output to console"""
for key, value in Sorted_Scores.items():
    print(value, " : ", key)


"""creating json file for output"""
json_obj = {
    "Number of satisfactory matchings": len(Output_List),
    "Matchings": []
}
for match in Output_List:
    json_obj["Matchings"].append({
        "Satisfaction Score": Scores[tuple(match)],
        "Matches": [],
    })
    for item in match:
        json_obj["Matchings"][-1]["Matches"].append({
            "Professor": item[0],
            "Course": item[1],
            "Units": item[2]
        })

# convert into json format
json_obj = json.dumps(json_obj, indent=4)
# create json file
with open('output.json', 'w') as f:
    f.write(json_obj)
# print(json_obj)


"""creating txt file for output"""
with open('output.txt', 'w') as f:
    f.write(f"Number of satisfactory matchings: {len(Output_List)} \n\n\n")
    for key, value in Sorted_Scores.items():
        f.write(str(value) + " : " + str(key) + "\n\n")

print("\nTime:", timer() - start)
