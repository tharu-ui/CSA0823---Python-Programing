from .validator import validate_record
from .reader import log_error

def clean_records(records, error_log):
    seen = set()
    clean = []
    for record in records:
        reg = record["register_number"]
        valid, reason = validate_record(record)
        if not valid:
            log_error(error_log, record["department"], 0, reason)
            continue
        if reg in seen:
            log_error(error_log, record["department"], 0,
                      f"duplicate registration {reg}")
            continue
        seen.add(reg)
        clean.append(record)
    return clean
