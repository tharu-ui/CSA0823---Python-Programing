from pathlib import Path

def write_outputs(records, output_folder):
    output = Path(output_folder)
    output.mkdir(parents=True, exist_ok=True)

    with (output / "master_list.csv").open("w", encoding="utf-8") as file:
        file.write("Register Number,Name,Department,Email,Events\n")
        for r in records:
            file.write(f"{r['register_number']},{r['name']},{r['department']},"
                       f"{r['email']},\"{';'.join(r['events'])}\"\n")

    event_map = {}
    for record in records:
        for event in record["events"]:
            event_map.setdefault(event, []).append(record)

    for event, participants in event_map.items():
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in event)
        with (output / f"{safe_name}_participants.txt").open("w", encoding="utf-8") as file:
            file.write(f"Participants for {event}\n")
            for p in participants:
                file.write(f"{p['register_number']}, {p['name']}, {p['department']}\n")

    with (output / "summary_report.txt").open("w", encoding="utf-8") as file:
        file.write(f"Total valid unique registrations: {len(records)}\n")
        file.write(f"Total events: {len(event_map)}\n")
        for event, participants in sorted(event_map.items()):
            file.write(f"{event}: {len(participants)} participants\n")
