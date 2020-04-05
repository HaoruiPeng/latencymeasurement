import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

def read_ping(file_path):
    with open(file_path, "r") as f:
        data = pd.read_csv(file_path, sep="\s+|=", header=1 ,skipfooter=4, engine='python', error_bad_lines=False)
        try:
            data.columns = ["packet_size", "ps_unit", "from", "ip", "seq", "seqnum", "ttl", "ttl_val", "time", "rtt", "time_unit"]
        except ValueError:
            data.columns = ["packet_size", "ps_unit", "from", "host" , "ip", "seq", "seqnum", "ttl", "ttl_val", "time", "rtt", "time_unit"]
        seq_num = data["seqnum"].to_numpy()
        rtt = data["rtt"].to_numpy()
    return seq_num, rtt

DATADIR = "../data"
cluster_name = ["bbcluster", "erdc"]
figure, axes = plt.subplots(1, 2)
figure.suptitle("ICMP")

PING = dict.fromkeys(cluster_name, {})
for i in range(2):
    cluster = cluster_name[i]
    cluster_dir = os.path.join(DATADIR, cluster)
    axes[i].set_title(cluster)
    data = []
    labels = []
    for root, dirs, files in os.walk(cluster_dir, topdown=False):
        for file_name in files:
            mode, stack = file_name.split("_")
            if mode == "ping":
                dst = stack.split(".")[0]
                file_path =  os.path.join(cluster_dir, file_name)
                seq_arry, rtt_array = read_ping(file_path)
                # print(rtt_array)
                length = len(rtt_array)
                # rtt_outliar_removal = np.sort(rtt_array)[0: round(length*0.999)]
                # rtt_mean = np.mean(rtt_outliar_removal)
                # rtt_std = np.sqrt(np.var(rtt_outliar_removal))
                # rtt_conf = st.norm.interval(0.95, loc=rtt_mean, scale=rtt_std)
                # PING[cluster][dst] = (rtt_mean, rtt_conf)
                data.append(rtt_array)
                labels.append(dst)
    axes[i].boxplot(data, labels=labels, showfliers=False)

plt.show()
