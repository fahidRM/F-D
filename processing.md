#### Processing the data





Handling missing values: The method of handling missing values depended on the column that was missing and is summarised below:

- User Identifiers (`user_id`, `name`, `email`, `instagram_handle`, `tiktok_handle`): These were restored from other records where possible. The idea being that if a user has multiple records then chances are one of those records are complete and could be used to patch the missing values. Otherwise, the record isn't entirely useful (it may be useful to get a better picture of program and activity efforts, beyond which it has limited utility) and was dropped.
- Campaign Identifiers (`program_id`, `brand`, `task_id`): Similar to user identifiers, the assumption is that there ought to be multiple records for a program, brand and task which we can then use to fill in missing data. To fill in a missing value we make use of one or both of the other identifiers in this category. Similar to user identifiers, where this is incomplete it has limited utility.
- `platform` and `post_url`: My understanding is that the `post_url` ideally will be the link to the post on the specified platform. If that were the case then we could reconstruct missing `platform` details supposing link shortening was not used but that was not the case, as such no attempt was made to restore these fields where they were missing. A missing `post_url` has limited impact on the metrics measured but missing `platform` information weakens the completeness on the statistics gathered.
- Metrics (`likes`, `comments`, `shares`, `reaach`, `sales_attributed`): These were set to zero where missing. The assumption here is that if a metric was not recorded then it is likely that the metric was zero. This may not always be the case, but it is a reasonable assumption in the absence of other information. My assumption is that `sales_attributed` is obtained by combining the other listed metrics fields and using some ML techniques we could reconstruct it and fill in the missing data. Due to time I did not attempt this and where these were missing a value of 0 was used to replace them.
- `joined_at`: No possible way to restore or approximate this. If we had other information like when programs and activities were run we could approximate it as the later of those dates. The date also had no bearing on the data or analysis that could be ascertained from the data hence we did not attempt to reconstruct it and we did not excluse data with missing dates.


Incorrect Typing: Handles by observing the data and choosing what was most suitable for it. e.g: lowercase for email and title case for names.

Formatting Issues: No formatting issues were observed in the data.

Normalisation Strategy:
- The arrays `advocacy_programs` and `tasks_completed` were exploded and flattened. For each task completed a new row was added and for each advocacy program rows were added to match the numner of tasks they had. In this datasset the JSON payload only had one advocacy program and one task, though this implementation has been build to support cases with multiple and to also tackle deduplication in those cases.
- More comments added to code...


Standardisation Strategy:
- Same as incorrect typing above.
- Special consideration given for `joined_at`. A library was used to convert the provided timestamp into a uniform representation irrespective of its source format. To the best of my knowledge in this dataset all timestamps were identical and the only issue was some data not being actual timestamps.