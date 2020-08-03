import json

timetables = []


# This is a private function! Well, at least I believe so.
def findAndInsert(target, r):
    for i in range(len(target)):
        if target[i][0] > r[0]:
            target.insert(i, r)
            return
    target.insert(len(target), r)


# Load a calendar from given file
def NewCalendar(filename):
    calendar = []
    f = open(filename, encoding="utf-8")
    raw = f.read()
    objects = json.loads(raw)
    for course in objects:
        l1 = course['name']
        for meeting in course['meetings']:
            row1 = [None, None, None, None, None, None, None, None]
            row2 = [None, None, None, None, None, None, None, None]
            days = meeting['days']

            time = meeting['time']
            tTime = time.split('-')

            sTime = tTime[0]
            eTime = tTime[1]

            row1[0] = sTime[0:2] + ':' + sTime[2:]
            row2[0] = eTime[0:2] + ':' + eTime[2:]
            for d in days:
                row1[int(d)] = l1
                row2[int(d)] = meeting['location']

            findAndInsert(calendar, row1)
            findAndInsert(calendar, row2)

    l = 0
    while l < len(calendar)-1:
        if calendar[l][0] == calendar[l+1][0]:
            for it in range(len(calendar[l])):
                # print(calendar[l+1], it)
                if calendar[l+1][it] is not None:
                    calendar[l][it] = calendar[l+1][it]
            calendar.remove(calendar[l+1])
        else:
            l += 1

    return calendar


# Save the target calendar to a specific file
def ExportCSV(target, filename):
    f = open(filename, "w")
    f.write(',M,T,W,R,F,Sat,Sun\n')
    for r in target:
        for e in r:
            if e is not None:
                f.write(e)
            f.write(',')
        f.write('\n')
    f.close()


# Shift a calendar's timezone
# Takes the target calendar and the time offset (integer only)
def ShiftTimezone(target, hrs):
    tHrs = []
    tMinu = []
    for i in target:
        tHrs.append(int(i[0].split(':')[0]))
        tMinu.append(int(i[0].split(':')[1]))
        tHrs[-1] += hrs

    for i in range(len(target)):
        if tHrs[i] >= 24:
            tHrs[i] %= 24
            t = target[i][-1]
            for j in range(7, 1, -1):
                target[i][j] = target[i][j-1]
            target[i][1] = t
        elif tHrs[i] < 0:
            tHrs[i] += 24
            t = target[i][1]
            for j in range(1, 7):
                target[i][j] = target[i][j+1]
            target[i][-1] = t

        hrstr = ""
        if tHrs[i] < 10:
            hrstr = "0"
        target[i][0] = hrstr + str(tHrs[i]) + target[i][0][2:]

    target.sort(key=lambda x: x[0])


# Merge Calendar will merge the first two calendars in the "timetables" list.
# Returns a merged calendar
def MergeCalendar():
    newcal = []
    i1 = 0
    i2 = 0
    while (i1 < len(timetables[0])) or (i2 < len(timetables[1])):
        if i1 >= len(timetables[0]):
            newcal.append(timetables[1][i2])
            i2 += 1
            continue
        if i2 >= len(timetables[1]):
            newcal.append(timetables[0][i1])
            i1 += 1
            continue

        if timetables[0][i1][0] == timetables[1][i2][0]:
            newcal.append(timetables[0][i1])
            flg = False
            for it in range(len(timetables[0][i1])):
                if timetables[0][i1][it] is not None and timetables[1][i2][it] is not None:
                    flg = True
                    break
            if flg == False:
                for it in range(len(timetables[0][i1])):
                    newcal[i1][it] = timetables[1][i2][it]
                i2 += 1
            else:
                newcal.append(timetables[1][i2])
                i2 += 1

            i1 += 1
        else:
            if timetables[0][i1][0] < timetables[1][i2][0]:
                newcal.append(timetables[0][i1])
                i1 += 1
            else:
                newcal.append(timetables[1][i2])
                i2 += 1
    return newcal


# To change the behavior of the program, just call different functions below this line
timetables.append(NewCalendar("config"))
timetables.append(NewCalendar("config2"))
ShiftTimezone(timetables[0], 15)
res = MergeCalendar()
ExportCSV(res, "UTC+8.csv")
