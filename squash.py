import csv


with open('tmp_results.csv') as input:
    reader = csv.reader(input)
    with open('results.csv', 'w') as output:
        writer = csv.writer(output)
        fips = set()
        for row in reader:
            print(row)
            f = row[0]
            if f in fips:
                continue

            fips.add(f)
            tmp = csv.reader(input)
            for r2 in tmp:
                if r2[0] == f:
                    for i in range(2, len(row)):
                        if row[i] == 0:
                            row[i] = r2[i]
            writer.writerow(row)
