import csv
import json
import sys
from pathlib import Path

json_path = Path(sys.argv[1])
otus_path = Path(sys.argv[2])


with open(json_path) as f:
    data = json.load(f)


# In ref-builder references, the same sequence ID can appear multiple times with the
# same content.
written_sequence_ids = set()


for otu in data["otus"]:
    otu_id = otu["_id"]
    otu_path = otus_path / otu["_id"]
    otu_path.mkdir(exist_ok=True, parents=True)

    for isolate in otu["isolates"]:
        for sequence in isolate["sequences"]:
            sequence_id = sequence["_id"]

            if sequence_id in written_sequence_ids:
                continue

            segment_name = sequence["segment"]
            segment_path = otu_path / segment_name

            segment_path.mkdir(exist_ok=True, parents=True)

            with open(segment_path / "sequences.fa", "a") as f:
                f.write(f">{sequence['_id']}\n{sequence['sequence']}\n")

            written_sequence_ids.add(sequence_id)
