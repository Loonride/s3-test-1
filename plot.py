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

fig, axs = plt.subplots(2, 3)

fig.suptitle("Time for PUT/GET/DELETE in seconds, Sizes in MB, 100 runs each")

axs = np.ndarray.flatten(axs)

ax_index = 0
for data_file_info in data_files:
    title = data_file_info["title"]
    with open(data_file_info["file"]) as fp:
        data = json.load(fp)

    for key in data.keys():
        ax = axs[ax_index]
        ax_index += 1
        pts = data[key]["data"]
        labels = data[key]["labels"]
        final_labels = []
        for label in labels:
            b = int(label)
            mb = b / 1000000
            final_labels.append(str(mb))

        ax.set_title(f"{title}, {key.upper()}")
        ax.boxplot(pts, labels=final_labels)

plt.show()
