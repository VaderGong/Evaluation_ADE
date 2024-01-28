import csv
import matplotlib.pyplot as plt

def read_column(filename, column_name):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return [row[column_name] for row in reader]
    
ttc=read_column("../testData/processed_tracks2.csv", 'ttc')
ttc=[float(i) for i in ttc]
ttc=[i for i in ttc if i is not None and i > 0 and i < 100]
plt.hist(ttc, bins=100, width = (max(ttc)-min(ttc))/100)
plt.xlabel('TTC')
plt.ylabel('number')
plt.title('TTC distribution(for comparison)')
plt.show()


