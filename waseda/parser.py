def make_schedule(match_object, segment_regex):
    schedule = []
    tail = match_object.group("tail")
    for i, segment in enumerate(segment_regex.finditer(tail), 1):
        if segment.group("day_others"):
            day = "others"
            period = segment.group("period_flag")
            start_time = None
            end_time = None
        else:
            day = segment.group("day_word")
            period = segment.group("period_text")
            start = segment.group("start_time")
            end = segment.group("end_time")
            start_time = int(start) if start is not None else None
            end_time = int(end) if end is not None else None

        schedule.append({
            "seq": i,
            "day": day,
            "period": period,
            "start_time": start_time,
            "end_time": end_time,
            "note": segment.group("note")
        })
    return schedule

def make_terms(terms_list, seasons, session=None):
    for i, season in enumerate(seasons , 1):
        terms_list.append({
            "season": season.capitalize(),
            "session": session,
            "position": i
        })
    return terms_list
