import csv
import os
import ast
import difflib
import itertools


path = os.path.dirname(os.getcwd()) + "/data/"
tuning = 5
completeness = 15

#                     Hint for 5d array
# data_array[0][0][0][0][0] - Team name
# data_array[0][0][0][0][0] + data_array[1][0][0][0][0] skip -> data_array[2][0][0][0][0] - Full event name
# data_array[0][0-2][0-5] - Team results [Name, score1, score2]
# data_array[0+n] - Next events


def big_line(sport):
    # Existing files
    rescent = []
    directory = path[:-5] + "HandyCapper/data/output/"
    files = os.listdir(directory)
    for file in files:
        type = file.split(".")[1]
        if type == sport:
            rescent.append(file)
    # Most fullness line
    most = []
    for line in rescent:
        with open(directory + line) as f:
            reader = csv.reader(f)
            lst = list(reader)
            most.append(len(lst))
    for line in rescent:
        with open(directory + line) as f:
            reader = csv.reader(f)
            lst = list(reader)
            if len(lst) == max(most):
                line = lst
                return line


def getname(line, sport):
    # Target archive
    directory = path[:-5] + "HandyCapper/data/archive/"
    files = os.listdir(directory)
    for file in files:
        type = file.split("_")[3]
        if type == sport + ".txt":
            with open(path[:-5] + "HandyCapper/data/archive/" + file, 'r') as file:
                content = file.read()
                data_array = ast.literal_eval(content[+1:-1])
    # Name arrays with indexes
    line_names = []
    arch_names = []
    archive_names = []
    arch_name = ""
    for name in line:
        line_names.append(name[0])
    for d5 in data_array:
        for d4 in d5:
            arch_names.append(d4)
    for i in arch_names:
        try:
            if i[0][0] != "Очные встречи":
                arch_name = arch_name + i[0][0][0] + " - "
            else:
                archive_names.append(arch_name[:-3])
                arch_name = ""
        except TypeError:
            pass
    return line_names, archive_names, data_array


def cross_find(line_names, archive_names):
    # Find similar
    similar = []
    for name in line_names:
        close_matches = difflib.get_close_matches(name, archive_names, 1, 0.7)
        if close_matches:
            similar.append(archive_names.index(close_matches[0]))
    return similar


def analysis(similars, archive):
    count = 0
    output = []
    for _ in similars:
        # add count and forloop
        team1 = archive[similars[count]][0][1:]
        team2 = archive[similars[count]][1][1:]
        both = archive[similars[count]][2][1:]

        team1name = archive[similars[count]][0][0][0][0]
        team2name = archive[similars[count]][1][0][0][0]

        res1 = []
        res2 = []
        resH = []

        for i in team1:
            if i[0].split(" - ")[0] == team1name:
                delta = int(i[1])-int(i[2])
            else:
                delta = int(i[2])-int(i[1])
            res1.append(delta)

        for i in team2:
            if i[0].split(" - ")[0] == team2name:
                delta = int(i[1])-int(i[2])
            else:
                delta = int(i[2])-int(i[1])
            res2.append(delta)

        for i in both:
            if i[0].split(" - ")[0] == team1name:
                delta = int(i[1])-int(i[2])
            else:
                delta = int(i[2])-int(i[1])
            resH.append(delta)

        # Calculate equity ->
        count += 1
        output.append([[team1name + " - " + team2name], res1, res2, resH])
    return output


def equity(calcs, sport):
    global tuning, completeness
    EQ1 = 0
    EQ2 = 0
    EQH = 0
    TOTALS1 = 0
    TOTALS2 = 0
    profitable = []
    # Match results
    if sport == "football":
        for calc in calcs:
            # Team1
            for i in calc[1]:
                TOTALS1 += i
                if i > 0:
                    EQ1 += 1
                elif i < 0:
                    EQ1 -= 1
                elif i == 0:
                    EQH += 1
            # Team2
            for i in calc[2]:
                TOTALS2 += i
                if i > 0:
                    EQ2 += 1
                elif i < 0:
                    EQ2 -= 1
                elif i == 0:
                    EQH += 1
            # H2H
            for i in calc[3]:
                if i > 0:
                    EQ1 += 1
                    EQ2 -= 1
                    TOTALS1 += i
                elif i < 0:
                    EQ2 += 1
                    EQ1 -= 1
                    TOTALS2 += i
                elif i == 0:
                    EQH += 1

            # Resultative equity
            total = len(calc[1]) + len(calc[2]) + len(calc[3])
            both = abs(round(TOTALS1/2.5) - round(TOTALS2/2.5))
            if both == 0:
                both = 2
            elif both == 1:
                both = 1
            else:
                both = 0
            cell1 = EQ1 + round(TOTALS1 / 2.5) + 1
            cell2 = EQ2 + round(TOTALS2 / 2.5) - 1
            delta = abs(cell1 - cell2)
            if delta >= tuning and total >= completeness:
                profitable.append([calc[0][0], " |" + str(EQ1+round(TOTALS1/2.5)+1) +
                                   "|" + str(EQH+both) + "|" + str(EQ2+round(TOTALS2/2.5)-1) + "|" + str(delta)])
            EQ1 = 0
            EQ2 = 0
            EQH = 0
            TOTALS1 = 0
            TOTALS2 = 0
    return profitable


def complex_run(sport, UI, tune):
    global tuning
    tuning = tune
    GREAT_OUTPUT = []
    line_names, archive_names, archive = getname(big_line(sport), sport)
    similars = cross_find(line_names, archive_names)
    calcs = analysis(similars, archive)
    profitable = equity(calcs, sport)
    line = big_line(sport)
    flattenlist = list(itertools.chain(*line))
    need = []
    for profit in profitable:
        need.append(difflib.get_close_matches(profit[0], flattenlist, 1, 0.7))
    count = 0
    for i in need:
        index = flattenlist[flattenlist.index(i[0])]
        CF1 = flattenlist[flattenlist.index(i[0])+2]
        CF2 = flattenlist[flattenlist.index(i[0]) + 3]
        CF3 = flattenlist[flattenlist.index(i[0]) + 4]
        GREAT_OUTPUT.append(index.ljust(5) + " | " + CF1 + " | " + CF2 + " | " + CF3 + " | " + profitable[count][1])
        count += 1
    # Write to file
    dir = path[:-5] + "HandyCapper/data/results/"
    with open(dir + "result_" + sport + ".txt", 'w') as fp:
        for item in GREAT_OUTPUT:
            # write each item on a new line
            fp.write("%s\n" % item)

    UI.statusbar_txt.setText("Found any valuable matches!")
    UI.total_txt.setText(str(len(line)))
    UI.found_txt.setText(str(len(GREAT_OUTPUT)))
    return GREAT_OUTPUT
