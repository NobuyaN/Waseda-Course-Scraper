from itertools import repeat
from unicodedata import normalize
from typing import List, Dict, Any, Optional
from re import Match, Pattern
import logging


def make_schedules(match_object: Match[str], segment_regex: Pattern[str], intensive: bool) -> List[Dict[str, Any]]:
    """
    Creates a list of schedule dictionaries from a regex match object and a segment regex.
    Each schedule dictionary will contain details about each course's day, period, start_time, end_time, note, and flags.

    Args:
        match_object (Match[str]) The regex match object that contains the tail string to be parsed.
        segment_regex (Pattern[str]): The regex pattern used to parse the tail string into segments.
        intensive (bool): A flag indicating whether the course is intensive.

    Returns:
        List[Dict[str, Any]] A list of dictionaries, each detailing the schedule of a course.
    """
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

def make_terms(terms_list: List[Dict[str, Any]], seasons: List[str], session: Optional[str] = None) -> List[Dict[str, Any]]:
    """
        Creates a list of term dictionaries using the provided seasons and session information.
        Each term dictionary will contain details about the season, session, and position.

        Args:
            terms_list (List[Dict[str, Any]]): An empty list to be appended with each term dictionary.
            seasons (List[str]): A list of season strings of a course.
            session (Optional[str]): The session string of a course, if available.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each with details about a course's term.
    """
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

def make_slots(terms: List[Dict[str, Any]], schedules: List[Dict[str, Any]], value: str) -> List[Dict[str, Any]]:
    """
        Creates a list of slot dictionaries by combining term and schedule information, providing necessary details about each course's timing and occurrence.

        Args:
            terms (List[Dict[str, Any]]): A list of term dictionaries, each containing details about a course's term.
            schedules (List[Dict[str, Any]]): A list of schedule dictionaries, each containing details about a course's schedule.
            value (str): The original string value representing the term_day_period, used for logging warnings if necessary.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each detailing the timing and occurrence of a course.
    """
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
        logging.warning(f"Unmatching iterable mappings for term_day_period: {value}")

    return [
        {
            "season": term["season"],
            "session": term["session"],
            **{key: sched[key] for key in slots_key}
        }
        for term, sched in pairs
    ]

def shorten_mapped_string(adapter: Any, key: str, mapping: Dict[str, Any]) -> None:
    """
        Shortens a string value from an adapter based on a provided mapping dictionary.
        If the value matches a key in the mapping, it is replaced with the corresponding value from the mapping.
        If the value is an empty string, it is set to None.

        Args:
            adapter (Any): An object that provides access to item fields, an instance of ItemAdapter.
            key (str): The key in the adapter whose value is to be shortened.
            mapping (Dict[str, Any]): A dictionary mapping original string values to their shortened forms or None.

        Returns:
            None: The function modifies the adapter in place and does not return a value.
    """
    value = (adapter.get(key) or "").strip()
    value = normalize("NFKC", value).lower()

    if value in mapping:
        adapter[key] = mapping[value]
    if value == "":
        adapter[key] = None