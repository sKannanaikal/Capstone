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
    

def genPieChart(attributionScores):
    labels = 'Malicious', 'Benign', 'No-Correlation'
    counts = functionCount(attributionScores)
    figure, axis = plt.subplots()
    axis.pie(counts, labels=labels, autopct='%1.1f%%')
    plt.savefig("./static/images/pie_chart.png") #increase image quality with dpi

def genBarChart(topMaliciousFunctionNames, topMaliciousFunctionAttributions):
    fig, ax = plt.subplots()
    ax.barh(topMaliciousFunctionNames, topMaliciousFunctionAttributions, align='center')
    ax.invert_yaxis()
    plt.savefig("./static/images/bar_chart.png") #increase image quality with dpi

def genHistogram(sortedMaliciousFunctionAttributions):
    plt.hist(sortedMaliciousFunctionAttributions, bins=10, edgecolor='black')
    plt.savefig("./static/images/histogram.png") #increase image quality with dpi