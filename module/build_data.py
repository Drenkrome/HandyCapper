import datetime
import numpy as np
import os
import re
from collections import Counter

h2h = False

# Globals
path = os.path.dirname(os.getcwd()) + "/HandyCapper/data/output/"
path_arch = os.path.dirname(os.getcwd()) + "/HandyCapper/data/archive/"
today = datetime.date.today().strftime("%d.%m.%Y")
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
sport = ""

calendar_fon = {" января": "01", " февраля": "02", " марта": "03", " апреля": "04", " мая": "05", " июня": "06",
                " июля": "07", " августа": "08", " сентября": "09", " октября": "10", " ноября": "11", " декабря": "12"}
calendar_boom = {"Январь": "01", "Февраль": "02", "Март": "03", "Апрель": "04", "Май": "05", "Июнь": "06",
                 "Июль": "07", "Август": "08", "Сентябрь": "09", "Октябрь": "10", "Ноябрь": "11", "Декабрь": "12"}
# Third-dimensional final giga array
dimension3 = []


def makecsv(type, raw):
    if type == "fon":
        print("Saved to CSV")
        print(standard_fon(raw))

    if type == "boom":
        print("Saved to CSV")
        print(standard_boom(raw))

    if type == "win":
        print("Saved to CSV")
        print(standard_win(raw))


def standard_fon(raw):
    clean_fon = []
    for i in raw:
        # Divide itemline
        split = i.split("$@$")
        # Replace correct date
        if "Сегодня" in split[2]:
            split[2] = split[2].replace("Сегодня", today)
            clean_fon.append(split[1:-1])
        elif "Завтра" in split[2]:
            split[2] = split[2].replace("Завтра", tomorrow)
            clean_fon.append(split[1:-1])
        else:
            try:
                month = " " + split[2].split(" ")[1]
                split[2] = split[2].replace(month, "." + calendar_fon[month] + "." + today[-4:])
                clean_fon.append(split[1:-1])
            except:
                pass
    export(clean_fon, "Fonbet")
    return clean_fon


def standard_boom(raw):
    name = ""
    clean_boom = []
    date = ""
    for i in raw:
        if "$@$" in i:
            month = i.split(" ")[1][i.split(" ")[1].find(")") + 1:]
            month = month.replace(month, calendar_boom[month])
            day = i[-2:]
            year = datetime.date.today().strftime("%Y")
            date = day + "." + month + "." + year
        elif ":" in i:
            time = i[i.find(":") - 2:i.find(":") + 3]
            # Get name of event
            count = 0
            for x in range(0, 100):
                if not i[count].isdigit() and i[count] != ":":
                    letter = i.find(i[count])
                    count = 0
                    # Names, contains dot, like "S.Korea"
                    if i[letter+1] == "." and i.find(".", i.find(".") + 1) == " ":
                        name = i[letter:i.find(".", i.find(".") + 1)]
                    elif i[letter+1] == "." and i.find(".", i.find(".") + 1) != " ":
                        name = i[letter:i.find(".", i.find(".", i.find(".") + 1))]
                    else:
                        name = i[letter:i.find(".")]
                else:
                    count += 1
            # Get coefficients
            reverse = i[::-1]
            pos = reverse.find("П", reverse.find("П") + 1) + 1
            coefficients = i[-pos:]
            team1 = coefficients[2:coefficients.find("X")]
            both = coefficients[coefficients.find("X") + 1:coefficients.find("П", coefficients.find("П") + 1)]
            if "¥" in coefficients:
                team2 = coefficients[coefficients.find("П", coefficients.find("П") + 1) + 2:coefficients.find("¥")]
            else:
                team2 = coefficients[coefficients.find("П", coefficients.find("П") + 1) + 2:]
            block = [name, date + " в " + time, team1, both, team2]

            clean_boom.append(block)
    export(clean_boom, "Betboom")
    return clean_boom


def standard_win(raw):
    clean_win = []
    for i in raw:
        if "." in i[1]:
            date = i[1][:i[1].find(".", i[1].find(".") + 1) + 1] + "20" + i[1][i[1].find(".", i[1].find(".") + 1) + 1:]
            datetime = date.split(" ")
            clean_win.append([i[0], datetime[0] + " в " + datetime[1], i[2], i[3], i[4]])
        elif "Сегодня" in i[1]:
            date = i[1].replace("Сегодня", today)
            datetime = date.split(" ")
            clean_win.append([i[0], datetime[0] + " в " + datetime[1], i[2], i[3], i[4]])
        elif "Завтра" in i[1]:
            date = i[1].replace("Завтра", tomorrow)
            datetime = date.split(" ")
            clean_win.append([i[0], datetime[0] + " в " + datetime[1], i[2], i[3], i[4]])

    export(clean_win, "Winline")
    return clean_win


def export(data, room):
    # Define the file name
    time = str(datetime.datetime.now().time())[:-7]
    file_name = room + "." + sport + "." + time + ".csv"
    # Delete existing file
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f):
            if room + "." + sport in f:
                os.remove(f)
    # Writing to CSV file
    np.savetxt(path + file_name, data, delimiter=",", fmt="%s")


def make_archive(data, sport, days):
    for page in data:
        makestring(page)
    archive = open(path_arch + "archive_" + today + "_" + str(days) + "days_" + sport + ".txt", "w")
    note = str(dimension3)
    archive.write(note)
    archive.close()


def makestring(page):
    global h2h, dimension3
    h2h = False
    team1 = page[page.find("ПОСЛЕДНИЕ ИГРЫ:"):page.find("ПОСЛЕДНИЕ ИГРЫ:", page.find("ПОСЛЕДНИЕ ИГРЫ:") + 1)].replace(
        " (Ж)", "Ж").replace(" U20", "U").replace(" (Б)", "")
    team2 = page[page.find("ПОСЛЕДНИЕ ИГРЫ:", page.find("ПОСЛЕДНИЕ ИГРЫ:") + 1):page.find("ОЧНЫЕ ВСТРЕЧИ")].replace(
        " (Ж)", "Ж").replace(" U20", "U").replace(" (Б)", "")
    both = page[page.find("ОЧНЫЕ ВСТРЕЧИ"):].replace(" (Ж)", "Ж").replace(" U20", "U").replace(" (Б)", "")

    nest1 = format_team_names(nested(team1))
    nest2 = format_team_names(nested(team2))
    h2h = True
    nest3 = format_team_names(nested(both))
    dimension3.append([nest1, nest2, nest3])


def nested(string):
    # GENIUS regular expression
    pattern = r"([\w\s-]+)\n(\d+)\n(\d+)\n"
    matches = re.findall(pattern, string)
    # Make nest
    raw = [[match[0], int(match[1]), int(match[2])] for match in matches]
    return raw


def format_team_names(arr):
    global h2h
    result = []
    for i in arr:
        split = i[0].split("\n")
        if split[-1].isdigit():
            try:
                name = split[-4] + " - " + split[-3]
                res1 = split[-2]
                res2 = split[-1]
                result.append([name, res1, res2])
            except:
                try:
                    name = split[-3]
                    res1 = split[-2]
                    res2 = split[-1]
                    result.append([name, res1, res2])
                except:
                    result.append(i)
        else:
            try:
                name = split[-2] + " - " + split[-1]
                result.append([name, i[1], i[2]])
            except:
                result.append([i[0], i[1], i[2]])

    # Team name for arrays
    naming = []
    team = []

    for i in result:
        naming.append(i[0].split(" - "))
    for i in naming:
        for x in i:
            team.append(x)
    if Counter(team).most_common(1) == "list":
        name = Counter(team).most_common(1)[0][0]
    else:
        name = Counter(team).most_common(1)
    if h2h:
        result.insert(0, ["Очные встречи"])
    else:
        result.insert(0, name)
    if result != [[]]:
        return result
