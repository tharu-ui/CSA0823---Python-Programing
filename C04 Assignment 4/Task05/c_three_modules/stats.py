def percentage(records):
    return {reg: sum(s == "P" for _, s in rows) / len(rows) * 100
            for reg, rows in records.items() if rows}
def absent_three_consecutive(records):
    result = []
    for reg, rows in records.items():
        statuses = [s for _, s in sorted(rows)]
        if any(statuses[i:i+3] == ["A","A","A"] for i in range(len(statuses)-2)):
            result.append(reg)
    return result
