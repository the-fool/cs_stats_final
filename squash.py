import csv

with open('tmp_results.csv', 'r', newline='') as infile:
    reader = csv.reader(infile)
    with open('results.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerow(reader.__next__())
        fips = set()
        row_cache = {}
        
        for row in reader:
            print("l")
            f = row[0]
            if f not in fips:
                fips.add(f)
                row_cache[f] = row
                continue
            else:
                row1 = row_cache[f]
                row2 = row
                for i in range(2, len(row)):
                    row1[i] = float(row1[i]) + float(row2[i])
                writer.writerow(row1)
