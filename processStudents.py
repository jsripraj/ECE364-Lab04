from glob import glob
from pprint import pprint as pp
import os

def getRegistration():
    studentCoursesDict = {}
    # Get the set of students
    students = []
    for course in os.listdir("./Classes"):
        with open('Classes/' + course, 'r') as mf:
            content = mf.read()
        students.extend(content.split('\n'))
    students = set(students)
    # Get a sorted list of the courses each student is enrolled in
    for student in students:
        courses = []
        for course in os.listdir("./Classes"):
            with open('Classes/' + course, 'r') as mf:
                if student in mf.read():
                    courses.append(course.replace('.txt', ''))
        courses.sort()
        studentCoursesDict[student] = courses
    return studentCoursesDict

def getCommonClasses(studentName1, studentName2):
    courses1 = []
    courses2 = []
    exists1 = False; exists2 = False;
    # Get the respective courses for each student
    for course in os.listdir("./Classes"):
        with open('Classes/' + course, 'r') as mf:
            content = mf.read()
        if studentName1 in content:
            exists1 = True
            courses1.append(course.replace('.txt', ''))
        if studentName2 in content:
            exists2 = True
            courses2.append(course.replace('.txt', ''))
    # If either student does not exist, return None
    if not exists1 or not exists2:
        return None
    # Find the mutual courses between the two students
    mutual = []
    for course in courses1:
        if course in courses2:
            mutual.append(course)
    # Return a set of the mutual courses
    return set(mutual)

if __name__ == "__main__":
    answer1 = getRegistration()
    # answer2a = getCommonClasses('Tamatha Granderson', 'Tasha Shell')
    # answer2b = getCommonClasses('Zenaida Blaisdell', 'Neomi Flournoy')
    # answer2c = getCommonClasses('Merideth Kind', 'Melba Gist')
    # answer2d = getCommonClasses('Joe Sriprajittichai', 'Dylan Lurk')
    pp(answer1)