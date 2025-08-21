## Waseda Course Scraper
This scraper, built entirely with Scrapy framework, allows the extraction of Waseda's course syllabus from their syllabus search. Although the scraper is optimized with pre-existing URL mappings built with Selenium, which is not covered in this repository, it extracts approximately 35,000 core course details with Scrapy's built-in concurrency. All course details are stored in JSON format (Unfortunately, not in pretty-JSON).

## Example Datum
```
  {"url": "https://www.wsl.waseda.jp/syllabus/JAA104.php?pKey=5301103005012025530110300553&pLng=en",
  "year": 2025,
  "school": "Graduate School of Advanced Science and Engineering",
  "course_title": "Reactor Experiments",
  "instructor": ["SATO, Isamu", "FUKAHORI, Tokio", "YAMAJI, Akifumi"],
  "term_day_period": {"terms": [{"season": "Spring", "session": null, "position": 1}, {"season": "Fall", "session": null, "position": 2}],
                      "schedule": [{"seq": 1, "day": "others", "period": "others", "start_time": null, "end_time": null, "note": null}],
                      "is_intensive": true},
  "category": "Exercise",
  "eligible_year": 1,
  "credits": 2,
  "classroom": null,
  "campus": "Nishi-Waseda",
  "main_language": "Japanese",
  "class_modality_categories": "[On-campus] Hybrid (over 50% of classes on-campus)",
  "level": "Level of Master",
  "types_of_lesson": "Work",
  "exam_contrib_prcnt": null,
  "papers_contrib_prcnt": 80,
  "class_participation_contrib_prcnt": null,
  "others_contrib_prcnt": 20},
```
