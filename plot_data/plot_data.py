import numpy as np
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Input the datra file')
parser.add_argument('-f', action="store", dest="f")

args = parser.parse_args()

file_name = args.f
data = []
with open(file_name, 'r') as file:
	lines = file.readlines()
	for l in lines:
		data.append(float(l))

data_array = np.array(data)
print(np.mean(data_array))
print(np.std(data_array))
print(np.std(data_array)/np.mean(data_array))

fig, ax = plt.subplots(1,1, figsize=(8, 6))
counts, bin_edges = np.histogram(data, bins=100)
norm_dom = np.sum(counts)
x = [(bin_edges[i+1] + bin_edges[i])/2 for i in range(len(bin_edges)-1)]
ax.plot(x, counts/norm_dom)
plt.show()
