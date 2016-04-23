import json
import csv

with open('primaries.json', 'r') as data:
    data = json.load(data).get('races')


with open('tmp_results.csv', 'w') as out:
    writer = csv.writer(out)
    row = ['FIPS', 'NAME', 'CLINTON', 'SANDERS',
           'OMALLEY', 'DEM_OTHER', 'TRUMP',
           'CRUZ', 'RUBIO', 'KASICH', 'CARSON',
           'BUSH', 'CHRISTIE', 'PAUL', 'REP_OTHER']
    # dict of candidates and their index -- why did I do it this way?
    cd = dict(zip(row[2:], range(2, len(row))))
    writer.writerow(row)

    for race in data:
        if race.get('race_type') == 'president' and\
           race.get("result") == "winner":
            counties = race.get('counties')
            if not counties:
                continue
            for county in counties:
                row[0] = county.get('fips')
                row[1] = county.get('name')

                # zero-out candidate tallies
                row[2:] = [0] * (len(row) - 2)
                # init the normalizer
                denominator = 0
                # set a basic index
                index = 0

                results = county.get('results')
                if not results:
                    continue

                for key in results.keys():
                    found = False
                    for candidate in cd.keys():
                        if candidate.lower() in key:
                            row[cd[candidate]] = results[key]
                            found = True
                            break
                    # if a non-important candidate / other    
                    if not found:
                        if race.get('party_id') == "republican":
                            row[cd["REP_OTHER"]] += results[key]
                        elif race.get('party_id') == "democrat":
                            row[cd["DEM_OTHER"]] += results[key]
                    denominator = denominator + int(results[key])

                # if we have a hit
                if denominator:
                    for i, _ in enumerate(row[2:]):
                        row[i + 2] = float(
                            "{0:.3f}".format(int(row[i + 2]) / denominator)
                            )
                    writer.writerow(row)

# squash the results, adding dem to rep results
with open('tmp_results.csv', 'r', newline='') as infile:
    reader = csv.reader(infile)
    with open('results.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerow(reader.__next__())
        fips = set()
        row_cache = {}

        for row in reader:
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
