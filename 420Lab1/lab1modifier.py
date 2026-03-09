# python file to modify the csv file so I am only looking at classes 1 and 2

import csv

input_file = "MasterExperiment.csv"
output_file = "MasterExperiment_Class1-2.csv"

with open(input_file, newline="", encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    CLASS_COL_INDEX = 2  # zero-based index of the Class column

    kept_rows = 0

    for row in reader:
        # Skip empty or malformed rows
        if len(row) <= CLASS_COL_INDEX:
            continue

        try:
            class_value = int(row[CLASS_COL_INDEX])
        except ValueError:
            # Skip rows where class is not numeric (metadata, notes, etc.)
            continue

        if class_value == 1 or class_value == 2:
            writer.writerow(row)
            kept_rows += 1

print(f"Saved {kept_rows} Class 1&2 steps to {output_file}")

