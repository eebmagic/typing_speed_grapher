#!/usr/local/bin/python3
from matplotlib import pyplot as plt
from pathlib import Path
import numpy
import os
from datetime import datetime
from dateutil import parser
import matplotlib.dates as mdates
import pandas as pd

times = []
raw_speeds = []
moving_averages = []

# Load file
pathfile = str(Path.home()).strip() + "/.wpm.csv"
assert Path.exists(Path(pathfile)), "~/.wpm.csv file not found"

# Open file
names = ["race", "wpm", "accuracy", "rank", "racers", "text_id", "timestamp", "database", "tag"]
content = pd.read_csv(pathfile, names=names)
content["dates"] = [parser.parse(x) for x in content["timestamp"]]
content["datestrings"] = [x.strftime("%b - %d") for x in content["dates"]]
back_dist = 10
content["rolling_average"] = content.iloc[:,1].rolling(window=back_dist).mean()

minspeed = content["wpm"].min()
maxspeed = content["wpm"].max()
avgspeed = round(content["wpm"].sum() / len(content), 2)
lastavg = round(content["wpm"][-10:].sum() / 10, 2)

print(f"\nWorst Speed: {minspeed}")
print(f" Best Speed: {maxspeed} wpm")
print(f"  Avg Speed: {avgspeed} wpm")
print(f"Last 10 avg: {lastavg} wpm")

xticks = [x.strftime("%y - %b - %d") for x in content["dates"]]
# Plot and make graph
plt.plot(content["race"], content["wpm"])
plt.plot(content["race"], content["rolling_average"], color="red")
plt.yticks(numpy.arange(int(minspeed) - 2, int(maxspeed), 5))
plt.xticks(content["race"][::5], xticks[::5], rotation=45, ha='right')
plt.tight_layout()
plt.grid()
plt.ylabel("WPM")
plt.legend(["Test Results", f"Rolling Average ({back_dist} previous samples used)"])
plt.show()