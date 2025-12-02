import json
import sys
import csv
from pathlib import Path

sample_labels_path = sys.argv[1]
reference_json_path = sys.argv[2]
output_path = sys.argv[3]

sequence_ids_by_virus_id = {}

with open(reference_json_path) as f:
    reference = json.load(f)

    for otu in reference["otus"]:
        sequence_ids = []

        for isolate in otu["isolates"]:
            for sequence in isolate["sequences"]:
                sequence_ids.append(sequence["_id"])

        sequence_ids_by_virus_id[otu["_id"]] = sequence_ids


with (
    open(sample_labels_path, "r") as sample_labels_f,
    open(output_path, "w") as output_f,
):
    sample_labels = csv.reader(sample_labels_f)
    next(sample_labels)

    sample_viruses = {}

    for row in sample_labels:
        sample_name = Path(row[0]).stem.split(".")[0]
        virus_id = row[10]
        sample_viruses.setdefault(sample_name, []).extend(sequence_ids_by_virus_id[virus_id])

    json.dump(sample_viruses, output_f)
