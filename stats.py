import matplotlib.pyplot as plt
import numpy as np

def functionCount(attributionScores):
    maliciousCount = 0
    benignCount = 0
    noCorrelationCount = 0
    for attribution in attributionScores:
        if attribution == 0.0:
            noCorrelationCount += 1
        elif attribution > 0.0:
            maliciousCount += 1
        elif attribution < 0.0:
            benignCount += 1
    return [maliciousCount, benignCount, noCorrelationCount]
    

def normalizeData(data):
    minMaxedData = (data - np.min(data)) / (np.max(data) - np.min(data))
    normalizedData = minMaxedData / np.sum(minMaxedData)
    for i in range(len(data)):
        data[i] = round(data[i] * 100, 2)

    return normalizedData

def genHistogram(sortedMaliciousFunctionAttributions):
    plt.clf()
    plt.hist(sortedMaliciousFunctionAttributions, bins=20, edgecolor='black')
    plt.savefig("./static/images/histogram.png") #increase image quality with dpi
