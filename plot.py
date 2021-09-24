import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

file_dir = Path(__file__).parent.resolve()
data_files = [
    {
        "file": "ec2_data/redis_data.json",
        "title": "Redis EC2" 
    },
    {
        "file": "ec2_data/s3_data.json",
        "title": "S3 EC2"
    }
]

figs, axs = plt.subplots(2, 3)

axs = np.ndarray.flatten(axs)
print(axs)

i = 0
for data_file_info in data_files:
    title = data_file_info["title"]
    with open(data_file_info["file"]) as fp:
        data = json.load(fp)

    for key in data.keys():
        ax = axs[i]
        i += 1
        pts = data[key]["data"]
        labels = data[key]["labels"]
        ax.set_title(f"{title}, {key.upper()}")
        ax.boxplot(pts, labels=labels)

plt.show()
