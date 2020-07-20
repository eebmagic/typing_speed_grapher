#!/usr/local/bin/python3
from matplotlib import pyplot as plt
from pathlib import Path
import numpy


times = []
raw_speeds = []
moving_averages = []


# Load file
pathfile = str(Path.home()).strip() + "/.wpm.csv"
assert Path.exists(Path(pathfile)), "~/.wpm.csv file not found"

# Open file
with open(pathfile) as file:
	content = file.read().strip()

# Loop over file contents
for ind, row in enumerate(content.split("\n")):
	# Parse for speed and time
	row = row.split(",")
	full_date = row[-3]
	day, time = full_date.split()
	time = time[:time.index('.')]
	HOUR, MIN, SEC = time.split(':')
	short_time = ':'.join([HOUR, MIN])
	times.append(day + " " + short_time)
	raw_speeds.append(float(row[1]))

	# Make moving averages data
	# moving_averages.append(sum(raw_speeds) / len(raw_speeds))
	back_dist = 10
	if ind > back_dist:
		moving_averages.append(sum(raw_speeds[ind-back_dist:]) / back_dist)
	else:
		moving_averages.append(raw_speeds[0])

# Round final speeds
rounded_speeds = [round(x) for x in raw_speeds]


# Print out information
for a in zip(times, rounded_speeds):
	print(a)

print(f"\nMin Speed: {min(rounded_speeds)} wpm")
print(f"Max Speed: {max(rounded_speeds)} wpm")
print(f"Avg Speed: {round(sum(rounded_speeds) / len(rounded_speeds), 2)} wpm")


# Plot and make graph
plt.plot(times, rounded_speeds)
plt.plot(times, moving_averages, color="red")
plt.yticks(numpy.arange(min(rounded_speeds) - 2, max(rounded_speeds), 5))
plt.xticks(rotation=45, ha='right')
plt.grid()
plt.ylabel("WPM")
plt.legend(["Test Results", f"Rolling Average ({back_dist} previous samples used)"])
plt.show()
