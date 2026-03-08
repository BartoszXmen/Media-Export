def format_duration(sec):

    if not sec:
        return "-"

    m = sec // 60
    s = sec % 60

    return f"{m:02}:{s:02}"


def format_date(d):

    if not d:
        return "-"

    return f"{d[6:8]}.{d[4:6]}.{d[0:4]}"