import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


experiment = {"Experiment":["Experiment1", "Experiment1", "Experiment1",
"Experiment2", "Experiment2", "Experiment2", "Experiment2",
"Experiment3", "Experiment3", "Experiment3","Experiment4", 
"Experiment4", "Experiment4", "Experiment4"],
"Name" : [],
"WER" : [],
}

df = pd.DataFrame(experiment)
df["lower_bound"] = df["WER"] - 1.96*1e-2*np.sqrt(df["WER"]*(100-df["WER"])/df["n_samples"])
df["upper_bound"] = df["WER"] + 1.96*1e-2*np.sqrt(df["WER"]*(100-df["WER"])/df["n_samples"])
df["error"] = 1.96*1e-2*np.sqrt(df["WER"]*(100-df["WER"])/df["n_samples"])

print(df)
#plt.bar(data=df[df["Experiment"]=="Experiment4"], x="Name", height="WER", yerr= "error", capsize=7)
#plt.plot(df[df["Experiment"]=="Experiment4"]["Name"].apply(lambda z : int(z[:-2])),
#                                              df[df["Experiment"]=="Experiment4"]["WER"])
plt.bar(data=df[df["Experiment"]=="Experiment3"], x="Name", height="WER", yerr= "error", capsize=7)
#plt.bar(data=df, x="Name", height="WER", yerr= "error", capsize=7)
plt.grid(True)
plt.show()