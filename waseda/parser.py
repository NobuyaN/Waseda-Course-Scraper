from itertools import repeat


def make_schedules(match_object, segment_regex, intensive):
    schedules = []
    tail = match_object.group("tail")
    for i, segment in enumerate(segment_regex.finditer(tail), 1):
        flags = {}
        if segment.group("day_others"):
            day = "others"
            period = segment.group("period_flag") # either others or On demand
            start_time = None
            end_time = None
            flags = {"others": True, "time_unknown": True,}
            if period == "On demand":
                flags["on_demand"] = True
        else:
            day = segment.group("day_word")
            period = segment.group("period_text")
            start = segment.group("start_time")
            end = segment.group("end_time")
            start_time = int(start) if start is not None else None
            end_time = start_time if end is None else int(end)
            if start_time == None:
                flags = {"time_unknown": True}
            if period == "On demand":
                flags["on_demand"] = True
        
        if intensive:
            flags["intensive"] = True
            
        schedules.append({
            "seq": i,
            "day": day,
            "period": period,
            "start_time": start_time,
            "end_time": end_time,
            "note": segment.group("note"),
            "flags": flags
        })

    return schedules

def make_terms(terms_list, seasons, session=None):
    if seasons[0] == "full":
            terms_list = [
                {"season": "Fall", "session": "Semester", "position": 1},
                {"season": "Spring", "session": "Semester", "position": 2}
            ]
            return terms_list
    
    for i, season in enumerate(seasons , 1):
        terms_list.append({
            "season": season.capitalize(),
            "session": session.capitalize() if session else None,
            "position": i
        })

    return terms_list

def make_slots(terms, schedules, value):
    slots_key = ["day", "start_time", "end_time", "flags"]
    terms_length = len(terms)
    schedule_length = len(schedules)
    pairs = []

    if terms_length == schedule_length:
        pairs = zip(terms, schedules)
    elif terms_length == 1:
        pairs = zip(repeat(terms[0], schedule_length), schedules)
    elif schedule_length == 1:
        pairs = zip(terms, repeat(schedules[0], terms_length))
    else:
        print(f"WARNING. Unmatching iterable mappings for term_day_period: {value}")
    
    return [
        {
            "season": term["season"],
            "session": term["session"],
            **{key: sched[key] for key in slots_key}
        }
        for term, sched in pairs
    ]