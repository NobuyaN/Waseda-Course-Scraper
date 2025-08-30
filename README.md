## Waseda Course Scraper
This scraper, built entirely with Scrapy framework, allows the extraction of Waseda's course syllabus from their syllabus search. Although the scraper is optimized with pre-existing URL mappings built with Selenium, which is not covered in this repository (consider looking at waseda-pkeys-scraper), it extracts approximately 35,000 core course details with Scrapy's built-in concurrency. All course details are stored in JSONL format. 

## Example Datum
```
  {
    "pKey_id": "9800002016012025980000201698",
    "url": "https://www.wsl.waseda.jp/syllabus/JAA104.php?pKey=9800002016012025980000201698&pLng=en",
    "year": 2025,
    "school": "Center for International Education",
    "course_title": "VIU Summer Session I 01",
    "instructor": [
                    "RHEE, Maji Christine",
                    "SHIMODA, Hiraku",
                    "SUGIMORI, Eriko"
                  ],
    "term_day_period": {
                          "terms": [
                                     {
                                       "season": "Summer",
                                       "session": "Semester",
                                       "position": 1
                                     },
                                     {
                                       "season": "Fall",
                                       "session": "Semester",
                                       "position": 2
                                     }
                                   ],
                          "schedules": [
                                         {
                                           "seq": 1,
                                           "day": "others",
                                           "period": "others",
                                           "start_time": null,
                                           "end_time": null,
                                           "note": null,
                                           "flags": {"others": true, "time_unknown": true}
                                         }
                                       ]
                       },

    "category": "Short Study Abroad Courses",
    "eligible_year": 1,
    "credits": 1,
    "classroom": null,
    "campus": "Other",
    "main_language": "N/A",
    "class_modality_categories": "[On-campus]",
    "level": "Beginner",
    "types_of_lesson": "Practice",
    "exam_contrib_prcnt": null,
    "papers_contrib_prcnt": null,
    "class_participation_contrib_prcnt": null,
    "others_contrib_prcnt": null,
    "slots": [
               {
                 "season": "Summer",
                 "session": "Semester",
                 "day": "others",
                 "start_time": null,
                 "end_time": null,
                 "flags": {"others": true, "time_unknown": true}
               },
               {
                 "season": "Fall",
                 "session": "Semester",
                 "day": "others",
                 "start_time": null,
                 "end_time": null,
                 "flags": {"others": true, "time_unknown": true}}
             ]
  }
```
