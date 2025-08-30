import unittest
from waseda.pipelines import WasedaPipeline

class TestWasedaPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = WasedaPipeline()

    def test_process_item(self):
        """
            Test the process_item method of WasedaPipeline with various input cases.
        """
        item = {
            "instructor": "MINOO, Arihiroothers／MORI, Masashi",
            "eligible_year": "1st year and above",
            "exam_contrib_prcnt": "80",
            "papers_contrib_prcnt": "10",
            "class_participation_contrib_prcnt": "5",
            "others_contrib_prcnt": "5",
            "credits": "3",
            "year": "2025",
            "campus": "Nishi-Waseda（Former: Okubo)",
            "level": "Beginner, initial or introductory",
            "term_day_period": "winter quarter 01:Mon.5／02:Thur.3 ",
        }

        processed_item_main = self.pipeline.process_item(item, None)

        self.assertEqual(processed_item_main["instructor"], ["MINOO, Arihiroothers", "MORI, Masashi"])
        self.assertEqual(processed_item_main["eligible_year"], 1)
        self.assertEqual(processed_item_main["exam_contrib_prcnt"], 80)
        self.assertEqual(processed_item_main["papers_contrib_prcnt"], 10)
        self.assertEqual(processed_item_main["class_participation_contrib_prcnt"], 5)
        self.assertEqual(processed_item_main["others_contrib_prcnt"], 5)
        self.assertEqual(processed_item_main["credits"], 3)
        self.assertEqual(processed_item_main["year"], 2025)
        self.assertEqual(processed_item_main["campus"], "Nishi-Waseda")
        self.assertEqual(processed_item_main["level"], "Beginner")
        self.assertEqual(
            processed_item_main["term_day_period"], 
            {
                "terms": [
                    {
                        "season": "Winter", 
                        "session": "Quarter", 
                        "position": 1
                    }
                ],
                "schedules": [
                    {
                        "seq": 1, 
                        "day": "Mon", 
                        "period": "5", 
                        "start_time": 5, 
                        "end_time": 5, 
                        "note": None, 
                        "flags": {}
                    },
                    {
                        "seq": 2, 
                        "day": "Thur", 
                        "period": "3", 
                        "start_time": 3, 
                        "end_time": 3, 
                        "note": None, 
                        "flags": {}
                    },
                ],
            }
        )
        self.assertEqual(
            processed_item_main["slots"], 
            [
                {
                    "season": "Winter", 
                    "session": "Quarter", 
                    "day": "Mon", 
                    "start_time": 5, 
                    "end_time": 5, 
                    "flags": {}
                },
                {
                    "season": "Winter", 
                    "session": "Quarter", 
                    "day": "Thur", 
                    "start_time": 3, 
                    "end_time": 3, 
                    "flags": {}
                },
            ],
        )


    def test_term_day_period_only(self):
        """
            Test multiple term_day_period formats to ensure correct parsing using wasedaPipeline process_item method.
        """
        test_cases = [
            {
                "input": "summer quarter Mon.1-2",
                "expected_terms": [
                    {"season": "Summer", "session": "Quarter", "position": 1},
                ],
                "expected_schedules": [
                    {"seq": 1, "day": "Mon", "period": "1-2", "start_time": 1, "end_time": 2, "note": None, "flags": {}}
                ]
            },
            {
                "input": "fall semester 01:othersOn demand／02:othersOn demand",
                "expected_terms": [
                    {"season": "Fall", "session": "Semester", "position": 1},
                ],
                "expected_schedules": [
                    {"seq": 1, "day": "others", "period": "On demand", "start_time": None, "end_time": None, "note": None, "flags": {"others": True, "on_demand": True, "time_unknown": True}},
                    {"seq": 2, "day": "others", "period": "On demand", "start_time": None, "end_time": None, "note": None, "flags": {"others": True, "on_demand": True, "time_unknown": True}}
                ]
            },
            {
                "input": "an intensive course(fall) Tues.others",
                "expected_terms": [
                    {"season": "Fall", "session": None, "position": 1}
                ],
                "expected_schedules": [
                    {"seq": 1, "day": "Tues", "period": "others", "start_time": None, "end_time": None, "note": None, "flags": {"intensive": True, "time_unknown": True}}
                ]
            },
            {
                "input": "an intensive course(spring and fall) 01:Wed.5-6／02:Sat.3-4",
                "expected_terms": [
                    {"season": "Spring", "session": None, "position": 1},
                    {"season": "Fall", "session": None, "position": 2}
                ],
                "expected_schedules": [
                    {"seq": 1, "day": "Wed", "period": "5-6", "start_time": 5, "end_time": 6, "note": None, "flags": {"intensive": True}},
                    {"seq": 2, "day": "Sat", "period": "3-4", "start_time": 3, "end_time": 4, "note": None, "flags": {"intensive": True}},
                ]
            },
            {
                # BE CAREFUL: For full year, in the terms list, we add both Fall and Spring with positions 1 and 2 respectively. Orders are important.
                "input": "full year Wed.6",
                "expected_terms": [
                    {"season": "Fall", "session": "Semester", "position": 1},
                    {"season": "Spring", "session": "Semester", "position": 2}
                ],
                "expected_schedules": [
                    {"seq": 1, "day": "Wed", "period": "6", "start_time": 6, "end_time": 6, "note": None, "flags": {}}
                ]
            },
            {
                "input": "fall term／winter term 01:Fri.4／02:othersothers",
                "expected_terms": [
                    {"season": "Fall", "session": "Term", "position": 1},
                    {"season": "Winter", "session": "Term", "position": 2},
                ],
                "expected_schedules": [
                    {"seq": 1, "day": "Fri", "period": "4", "start_time": 4, "end_time": 4, "note": None, "flags": {}},
                    {"seq": 2, "day": "others", "period": "others", "start_time": None, "end_time": None, "note": None, "flags": {"others": True, "time_unknown": True}}
                ]
            },
        ]

        for case in test_cases:
            item = {
                "term_day_period": case["input"]
            }
            processed_item = self.pipeline.process_item(item, None)
            self.assertEqual(processed_item["term_day_period"]["terms"], 
                             case["expected_terms"],
                             msg=f"Failed for terms input: {case['input']}")
            self.assertEqual(processed_item["term_day_period"]["schedules"], 
                             case["expected_schedules"],
                             msg=f"Failed for schedules input: {case['input']}")

if __name__ == "__main__":
    unittest.main()