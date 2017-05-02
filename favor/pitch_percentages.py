""" Determine the percentage of 10 ms chunks within a given segment that were
above the speaker's average pitch, ignoring all chunks where pitch was not
recorded. Also record the final pitch of the segment.

Output: percentage_above_average.csv -- percent above average for each segment
        final_pitch.csv -- the final pitch of each segment
"""

import csv
import os
import sys

def writePercentage(writer, uniqueID, nonBlankCount, highCount, blankCount):
    """ Write down the percent above the average pitch. """
    writer.writerow({"Subject": uniqueID[0], "Sentence": uniqueID[1],
        "Type": uniqueID[2], "Reading": uniqueID[3], "Blank": blankCount,
        "NonBlank": nonBlankCount, "NumAboveAverage": highCount,
        "PercentAboveAverage": highCount / nonBlankCount})

def writeFinalPitch(writer, lines, uniqueID):
    """ Write the final pitch for the given segment. """
    # read list of lines in reverse; record the first one with a pF0
    for line in lines[::-1]:
        if line['pF0']:
            writer.writerow({"Subject": uniqueID[0], "Sentence": uniqueID[1],
                "Type": uniqueID[2], "Reading": uniqueID[3], "Final": line['pF0']})
            return
    writer.writerow({"Subject": uniqueID[0], "Sentence": uniqueID[1],
        "Type": uniqueID[2], "Reading": uniqueID[3], "Final": lines[-1]['pF0']})

def extractUniqueID(line):
    """ Get the ID of a row. This uses a DictReader, so lines are indexed by
    column name. """
    return (line['Subject'], line['sentence'], line['type'], line['Reading'])

def getDiffAndAvg(line):
    """ Return the values of the pitch average and difference columns. """
    global line_num
    line_num += 1
    try:
        print(line['diff'], line['Avg(Subj-file)'], line_num)
        return float(line['diff']), float(line['Avg(Subj-file)'])
    except:
        global count
        count += 1
        #print(line, count, line_num)
        return (0,0)

def storeLine(line, currentLines):
    """ Add a line to the list, keeping the last 80 lines.
    Most only require going back 5-10 lines before finding a final pitch
    track, but it's necessary to store 80 lines to get a final pitch
    for all segments. """
    currentLines = currentLines[-79:]
    currentLines.append(line)
    return currentLines

def setUpWriters(percentFile, finalPitchFile):
    """ Set up the CSV writers. """
    # DictWriters/Readers keep track of fields by name, not index
    percentFieldNames = ["Subject", "Sentence", "Type", "Reading", "Blank",
        "NonBlank", "NumAboveAverage", "PercentAboveAverage"]
    percentWriter = csv.DictWriter(percentFile, fieldnames=percentFieldNames)
    percentWriter.writeheader()
    finalPitchFieldNames = ["Subject", "Sentence", "Type", "Reading",
        "Final"]
    finalPitchWriter = csv.DictWriter(finalPitchFile,
        fieldnames=finalPitchFieldNames)
    finalPitchWriter.writeheader()
    return percentWriter, finalPitchWriter

def main():

    global count
    count = 0
    global line_num
    line_num = 0

    with open("SPLIT_1.csv", "r") as results:
        percentFile = open("percent_above_average.csv", "w", newline='')
        finalPitchFile = open("final_pitch.csv", "w", newline='')
        #percentFile = open("percent_above_average.csv", "w")
        #finalPitchFile = open("final_pitch.csv", "w")
        percentWriter, finalPitchWriter = setUpWriters(percentFile, finalPitchFile)

        # Read the first row
        resultsReader = csv.DictReader(results)
        firstRow = next(resultsReader)
        currentID = extractUniqueID(firstRow)
        currentLines = [firstRow]
        diff, avg = getDiffAndAvg(firstRow)
        if diff == (avg * -1):
            blankCount, nonBlankCount = 1, 0
        else:
            blankCount, nonBlankCount = 0, 1
        highCount = 0

        for line in resultsReader:
            if extractUniqueID(line) == currentID:
                diff, avg = getDiffAndAvg(line)
                # Skip missing chunks
                if diff == (avg * -1):
                    blankCount += 1
                else:
                    nonBlankCount += 1
                    currentLines = storeLine(line, currentLines)
                    if diff > 0:
                        highCount += 1
            else:
                writePercentage(percentWriter, currentID, nonBlankCount, highCount,
                    blankCount)
                writeFinalPitch(finalPitchWriter, currentLines, currentID)
                currentID = extractUniqueID(line)
                currentLines = [line]
                diff, avg = getDiffAndAvg(line)
                if diff == (avg * -1):
                    blankCount = 1
                    highCount = 0
                    nonBlankCount = 0
                elif diff > 0:
                    highCount = 1
                    blankCount = 0
                    nonBlankCount = 1
                else:
                    highCount = 0
                    blankCount = 0
                    nonBlankCount = 1

        percentFile.close()
        finalPitchFile.close()

main()
