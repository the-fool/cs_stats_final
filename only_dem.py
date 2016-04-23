import json
import csv

with open('primaries2.json', 'r') as data:
    data = json.load(data).get('races')


with open('dem_results.csv', 'w') as out:
    writer = csv.writer(out)
    row = ['FIPS', 'NAME', 'CLINTON', 'SANDERS',
           'OMALLEY', 'DEM_OTHER']
    # dict of candidates and their index -- why did I do it this way?
    cd = dict(zip(row[2:], range(2, len(row))))
    writer.writerow(row)

    for race in data:
        if race.get('race_type') == 'president' and\
           race.get("result") == "winner" and\
           race.get("party_id") == "democrat":
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
                        row[cd["DEM_OTHER"]] += results[key]
                    denominator = denominator + int(results[key])

                # if we have a hit
                if denominator:
                    for i, _ in enumerate(row[2:]):
                        row[i + 2] = float(
                            "{0:.3f}".format(int(row[i + 2]) / denominator)
                            )
                    writer.writerow(row)
