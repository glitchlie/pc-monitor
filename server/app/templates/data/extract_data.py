import pandas as pd
from datetime import datetime
import time


data = pd.read_csv("./OpenHardwareMonitorLog-2022-03-06.csv")
data["Time"] = pd.to_datetime(data["Time"]).astype("Int64") / 10 ** 6
gpu_data = data[["Time", "GPU Core"]]

arr_gpu_data = list()

for i in range(len(data)):
    arr_gpu_data.append([gpu_data.loc[i, "Time"], 
                         gpu_data.loc[i, "GPU Core"]])
with open("gpu_data.txt", "w") as f:
    for elem in arr_gpu_data:
        f.write(str(elem) + ',\n')
