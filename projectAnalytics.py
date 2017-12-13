#! usr/bin/env python 3.4
import sys
import os
from pprint import pprint as pp

from Pyro4.utils.httpgateway import return_homepage


def getComponentCountByProject(projectID):
    circuits = []
    projectIDs = []
    with open('projects.txt', 'r') as myFile:
        lines = myFile.readlines()
    # Build list of circuits that match given projectID
    for line in lines[2:]:
        line = line.split()
        projectIDs.append(line[1])
        if line[1] == projectID:
            circuits.append(line[0])
    # Return None for nonexistent projectID value
    if projectID not in projectIDs:
        return None
    # Build a set of components used
    components = []
    for circuit in circuits:
        path = 'Circuits/circuit_' + circuit + '.txt'
        with open(path, 'r') as myFile:
            lines = myFile.readlines()
        els = lines[4].split(',')
        for component in els:
            components.append(component.strip())
    componentSet = set(components)
    # Count the different types of components
    resistors = 0; inductors = 0; capacitors = 0; transistors = 0
    for component in componentSet:
        if 'R' in component:
            resistors += 1
        elif 'I' in component:
            inductors += 1
        elif 'C' in component:
            capacitors += 1
        elif 'T' in component:
            transistors += 1
    # Return a tuple of the counts
    return (resistors, inductors, capacitors, transistors)

def getComponentCountByStudent(studentName):
    with open('students.txt', 'r') as mf:
        lines = mf.readlines()
    # Get the corresponding SID (Student ID)
    exists = False
    for line in lines[2:]:
        if studentName in line:
            exists = True
            line = line.split()
            SID = line[3]
            break
    if not exists:
        return None
    # Get a list of circuits
    circuits = []
    with open('projects.txt', 'r') as mf:
        lines = mf.readlines()
    for line in lines[2:]:
        circuits.append(line.split()[0])
    circuits = set(circuits)
    # Create a set of components the student has participated with
    components = []
    participation = False
    for circuit in circuits:
        path = 'Circuits/circuit_' + circuit + '.txt'
        with open(path, 'r') as mf:
            lines = mf.readlines()
        if SID in lines[1]:
            participation = True
            for component in lines[4].split():
                components.append(component)
    if not participation:
        return ()
    compSet = set(components)
    # Count the number of components and return as a tuple
    R = 0; I = 0; C = 0; T = 0
    for component in compSet:
        if 'R' in component:
            R += 1
        elif 'I' in component:
            I += 1
        elif 'C' in component:
            C += 1
        elif 'T' in component:
            T += 1
    return (R, I, C, T)

def getParticipationByStudent(studentName):
    with open('students.txt', 'r') as mf:
        content = mf.read()
        if studentName not in content:
            return None
    with open('students.txt', 'r') as mf:
        lines = mf.readlines()
    # Get the corresponding SID (Student ID)
    for line in lines[2:]:
        if studentName in line:
            SID = line.split()[3]
            break
    # Create a set of circuits
    circuits = []
    with open('projects.txt', 'r') as mf:
        lines = mf.readlines()
    for line in lines[2:]:
        circuits.append(line.split()[0])
    circuits = set(circuits)
    # Get only the circuits the student has worked on
    worked = []
    for circuit in circuits:
        path = 'Circuits/circuit_' + circuit + '.txt'
        with open(path, 'r') as mf:
            lines = mf.readlines()
        if SID in lines[1]:
            worked.append(circuit)
    worked = set(worked)
    # Get all the project ID's of the circuits the student has worked on
    projectIDs = []
    with open('projects.txt', 'r') as mf:
        lines = mf.readlines()
    for line in lines[2:]:
        if line.split()[0] in worked:
            projectIDs.append(line.split()[1])

    # Return a set of the project ID's
    return set(projectIDs)

def getParticipationByProject(projectID):
    with open('projects.txt', 'r') as mf:
        content = mf.read()
    if projectID not in content:
        return None
    with open('projects.txt', 'r') as mf:
        lines = mf.readlines()
    # Get a list of circuits in the project
    circuits = []
    for line in lines[2:]:
        if projectID in line:
            circuits.append(line.split()[0])
    circuits = set(circuits)
    # Get a list of SIDs that worked on the circuits
    SIDs = []
    for circuit in circuits:
        path = 'Circuits/circuit_' + circuit + '.txt'
        with open(path, 'r') as mf:
            lines = mf.readlines()
        for SID in lines[1].split(','):
            SIDs.append(SID.strip())
    SIDs = set(SIDs)
    # Create a list of students that worked on the circuits
    students = []
    with open('students.txt','r') as mf:
        lines = mf.readlines()
    for line in lines[2:]:
        if line.split('|')[1].strip() in SIDs:
            students.append(line.split('|')[0].strip())
    # Return the set of students that worked on the project
    return set(students)

def getProjectByComponent(components):
    projectsByComponent = {}
    # Get set of circuits
    circuits = []
    with open('projects.txt', 'r') as mf:
        lines = mf.readlines()
    for line in lines[2:]:
        circuits.append(line.split()[0].strip())
    circuits = set(circuits)
    # For each component...
    for component in components:
        # Get list of all circuits that used the component
        circuitsWithComponent = []
        for circuit in circuits:
            path = 'Circuits/circuit_' + circuit + '.txt'
            with open(path, 'r') as mf:
                content = mf.read()
            if component in content:
                circuitsWithComponent.append(circuit)
        circuitsWithComponent = set(circuitsWithComponent)
        # Get list of all project IDs corresponding to those circuits
        projectIDsWithComponent = []
        with open('projects.txt','r') as mf:
            lines = mf.readlines()
        for line in lines[2:]:
            if line.split()[0] in circuitsWithComponent:
                projectIDsWithComponent.append(line.split()[1])
        projectsByComponent[component] = set(projectIDsWithComponent)
    return projectsByComponent

def getStudentByComponent(components):
    ComponentStudentsDict = {}
    # Get set of circuits
    circuits = set(getListOfCircuits())
    # For each component...
    for component in components:
        # Get list of all SIDs that used the component
        SIDs = []
        for circuit in circuits:
            path = 'Circuits/circuit_' + circuit + '.txt'
            with open(path, 'r') as mf:
                lines = mf.readlines()
            if component in lines[4]:
                els = lines[1].split(",")
                for el in els:
                    SIDs.append(el.strip())
        SIDs = set(SIDs)
        # Match SIDs to student names
        SIDStudentDict = getSIDStudentDict()
        students = []
        for SID in SIDs:
            students.append(SIDStudentDict[SID])
        ComponentStudentsDict[component] = set(students)
    return ComponentStudentsDict

def getComponentByStudent(studentNames):
    studentComponentDict = {}
    for student in studentNames:
        # Get the SID
        with open('students.txt', 'r') as mf:
            lines = mf.readlines()
        for line in lines[2:]:
            if student in line:
                SID = line.split('|')[1].strip()
        # Get all the components that the student has used
        circuits = set(getListOfCircuits())
        components = []
        for circuit in circuits:
            path = "Circuits/circuit_" + circuit + ".txt"
            with open(path, 'r') as mf:
                lines = mf.readlines()
            if SID in lines[1]:
                els = lines[4].split(',')
                for el in els:
                    components.append(el.strip())
        studentComponentDict[student] = set(components)
    return studentComponentDict

def getCommonByProject(projectID1, projectID2):
    # Get set of project IDs. Also get circuits used in each project
    projIDs = []
    with open('projects.txt', 'r') as mf:
        lines = mf.readlines()
    circuits1 = []
    circuits2 = []
    for line in lines[2:]:
        projIDs.append(line.split()[1].strip())
        if projectID1 in line:
            circuits1.append(line.split()[0].strip())
        elif projectID2 in line:
            circuits2.append(line.split()[0].strip())
    projIDs = set(projIDs); circuits1 = set(circuits1); circuits2 = set(circuits2)
    if projectID1 not in projIDs or projectID2 not in projIDs:
        return None
    # Get set of components used in project 1
    components1 = []
    for circuit in circuits1:
        path = "Circuits/circuit_" + circuit + ".txt"
        with open(path, 'r') as mf:
            lines = mf.readlines()
        for el in lines[4].split(','):
            components1.append(el.strip())
    components1 = set(components1)
    # Get set of components used in project 2
    components2 = []
    for circuit in circuits2:
        path = "Circuits/circuit_" + circuit + ".txt"
        with open(path, 'r') as mf:
            lines = mf.readlines()
        for el in lines[4].split(','):
            components2.append(el.strip())
    components2 = set(components2)
    # Get mutually used components
    mutuallyUsed = []
    for component1 in components1:
        if component1 in components2:
            mutuallyUsed.append(component1)
    # Return sorted list of mutually used components
    mutuallyUsed.sort()
    return mutuallyUsed

def getCommonByStudent(studentName1, studentName2):
    # Get SIDs
    with open('students.txt','r') as mf:
        content = mf.read()
    if studentName1 not in content or studentName2 not in content:
        return None
    with open('students.txt', 'r') as mf:
        lines = mf.readlines()
    for line in lines[2:]:
        if studentName1 in line:
            SID1 = line.split('|')[1].strip()
        elif studentName2 in line:
            SID2 = line.split('|')[1].strip()
    # Get set of components used by each SID
    circuits = set(getListOfCircuits())
    components1 = []
    components2 = []
    for circuit in circuits:
        path = "Circuits/circuit_" + circuit + ".txt"
        with open(path, 'r') as mf:
            lines = mf.readlines()
        els = []
        for el in lines[4].split(','):
            els.append(el.strip())
        if SID1 in lines[1]:
            components1.extend(els)
        if SID2 in lines[1]:
            components2.extend(els)
    components1 = set(components1)
    components2 = set(components2)
    # Get mutually used components
    mutuallyUsed = []
    for component in components1:
        if component in components2:
            mutuallyUsed.append(component)
    # Sort mutually used components and return
    mutuallyUsed.sort()
    return mutuallyUsed

def getProjectByCircuit():
    circuitProjectsDict = {}
    circuits = set(getListOfCircuits())
    # For every circuit
    for circuit in circuits:
        # Get a list of the project IDs the circuit is a part of
        projectIDs = []
        with open('projects.txt','r') as mf:
            lines = mf.readlines()
        for line in lines[2:]:
            if circuit in line:
                projectIDs.append(line.split()[1].strip())
        # Get the set from the list of project IDs
        projectIDs = list(set(projectIDs))
        # Sort the set (it's really a list)
        projectIDs.sort()
        # Insert the unique, sorted list of projectIDs into dictionary
        circuitProjectsDict[circuit] = projectIDs
    return circuitProjectsDict

def getCircuitByStudent():
    studentCircuitsDict = {}
    # Get a list of tuples(student name, SID)
    studentTuples = []
    with open('students.txt', 'r') as mf:
        lines = mf.readlines()
    for line in lines[2:]:
        els = line.split()
        name = els[0] + ' ' + els[1]
        studentTuples.append((name, els[3]))
    # For each student, find the circuits he/she has worked on
    circuits = set(getListOfCircuits())
    for student, SID in studentTuples:
        circuitsWorkedOn = []
        for circuit in circuits:
            path = 'Circuits/circuit_' + circuit + '.txt'
            with open(path, 'r') as mf:
                lines = mf.readlines()
            if SID in lines[1]:
                circuitsWorkedOn.append(circuit)
        circuitsWorkedOn = list(set(circuitsWorkedOn))
        circuitsWorkedOn.sort()
        studentCircuitsDict[student] = circuitsWorkedOn
    return studentCircuitsDict

def getCircuitByStudentPartial(studentName):
    studentCircuitsDict = {}
    # Make a list of tuples(student with matching names, SID)
    studentTuples = []
    with open('students.txt', 'r') as mf:
        lines = mf.readlines()
    exists = False
    for line in lines[2:]:
        full = line.split('|')[0].strip()
        last = full.split(',')[0].strip()
        first = full.split(',')[1].strip()
        if studentName == last or studentName == first:
            exists = True
            studentTuples.append((full, line.split('|')[1].strip()))
    if not exists:
        return None
    # For each student, find the circuits he/she has worked on
    circuits = set(getListOfCircuits())
    for student, SID in studentTuples:
        circuitsWorkedOn = []
        for circuit in circuits:
            path = 'Circuits/circuit_' + circuit + '.txt'
            with open(path, 'r') as mf:
                lines = mf.readlines()
            if SID in lines[1]:
                circuitsWorkedOn.append(circuit)
        # Get the unique circuit values
        circuitsWorkedOn = list(set(circuitsWorkedOn))
        # Sort the unique circuit values
        circuitsWorkedOn.sort()
        # Insert sorted, unique circuits worked with key as student's name
        studentCircuitsDict[student] = circuitsWorkedOn
    return studentCircuitsDict

def getSIDStudentDict():
    SIDStudentDict = {}
    with open('students.txt','r') as mf:
        lines = mf.readlines()
    for line in lines[2:]:
        line = line.split("|")
        SIDStudentDict[line[1].strip()] = line[0].strip()
    return SIDStudentDict

def getListOfCircuits():
    with open('projects.txt', 'r') as mf:
        lines = mf.readlines()
    circuits = []
    for line in lines[2:]:
        circuits.append(line.split()[0])
    return circuits

if __name__ == "__main__":
    # answer1 = getComponentCountByProject("082D6241-40EE-432E-A635-65EA8AA374B6")
    # answer2 = getComponentCountByStudent('S, Joe')
    # answer3 = getParticipationByStudent('Adams, Keith')
    # answer4 = getParticipationByProject('90BE0D09-1438-414A-A38B-8309A49C02EF')
    # answer5 = getProjectByComponent({'T71.386', 'C407.660', 'L103.001'})
    # answer6 = getStudentByComponent({'T71.386', 'C407.660', 'L103.001'})
    # answer7 = getComponentByStudent({'Gray, Tammy', 'Allen, Amanda', 'Baker, Craig'})
    # answer8 = getCommonByProject('90BE0D09-1438-414A-A38B-8309A49C02EF', '96CC6F98-B44B-4FEB-A06B-390432C1F6EA')
    # answer9 = getCommonByStudent('Allen, Amanda', 'Adams, Keith')
    # answer10 = getProjectByCircuit()
    # answer11 = getCircuitByStudent()
    answer12 = getCircuitByStudentPartial('Martin')
    pp(answer12)
