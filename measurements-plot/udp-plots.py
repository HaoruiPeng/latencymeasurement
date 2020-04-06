import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

def read_udp(file_path):
    with open(file_path, "r") as f:
        data_dict = {'send':{}, 'rec':{}}
        data = pd.read_csv(file_path, sep=",", engine='python', error_bad_lines=False)
        data.columns=['mode', 'seq', 'stamp']
        for index, row in data.iterrows():
            data_dict[row['mode']][row['seq']] = row['stamp']
        loss = 0
        rtt_array = []
        for k in data_dict['send'].keys():
            try:
                rtt = (data_dict['rec'][k] - data_dict['send'][k])*1000
                rtt_array.append(rtt)
            except KeyError:
                loss += 1

    total_send = data['seq'].iloc[-1]
    loss_prob =  loss/total_send

    return loss_prob, rtt_array

DATADIR = "../data"
cluster_name = ["bbcluster", "erdc"]
figure, axes = plt.subplots(1, 2)
figure.suptitle("UDP")

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
            if mode == "udp":
                dst = stack.split(".")[0]
                file_path =  os.path.join(cluster_dir, file_name)
                loss_prb, rtt_array = read_udp(file_path)
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
