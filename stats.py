import matplotlib.pyplot as plt

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
    plt.savefig("./static/images/pie_chart.png")