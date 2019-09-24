import csv
from matplotlib import pyplot as plt
import numpy as np
from pathlib import Path

times = []
raw_speeds = []

pathfile = str(Path.home()).strip() + "/.wpm.csv"

assert Path.exists(Path(pathfile)), "~/.wpm.csv file not found"

with open(pathfile) as file:
	for row in file:
		if int(row[0]) == 14:
			pass
		row = row.split(",")

		full_date = row[-3]
		day, time = full_date.split()
		time = time[:time.index('.')]
		HOUR, MIN, SEC = time.split(":")
		short_time = ':'.join([HOUR, MIN])
		times.append(day + " " + short_time)
		raw_speeds.append(float(row[1]))

rounded_speeds = [round(x) for x in raw_speeds]
both = zip(times, rounded_speeds)
print(rounded_speeds)
print(times)

print("\n\n")

for a in both:
	print(a)

plt.plot(times, rounded_speeds)
print((min(rounded_speeds), max(rounded_speeds)))
plt.yticks(np.arange(min(rounded_speeds) - 2, max(rounded_speeds), 5))
plt.xticks(rotation=45, ha='right')
plt.grid()
plt.ylabel("WPM")
plt.show()