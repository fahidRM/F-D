
__Runtime__: [3 days]: Sat, 0ct 4th, 2025 10:15am  - Tue, Oct 7th, 2025 10:15am


### SOME NOTES BEFORE YOU BEGIN

#### Assumptions Made:

- No two tasks share the same id: all tasks with the same id refer to the same task
- No two programs share the same id: all programs with the same id refer to the same program
- Post urls are unique to user and task: No two tasks can share the same post url -- it ties to a post a user has made on a platform towards one and only one task.


#### Limitation of the Data and Potential expansion:

- Programs List: A list of programs would have allowed filtering out tasks that do not belong to any known program
- Task List: A list of tasks would allow for ensuring the program-task relationships are valid
- No timestamps: Beyond `joined_at`, there is no timing information. If we had timing information, we could potentially see if performance changes based on time of the year and or time of the day which would allow for greater insights. For example, we could see how engagement changes from months to month and are affected by events


#### Approach and Thought process
- For thoughts on the exploration stage, please refer to the notebook `exploration.ipynb` in the root directory.
- [Data Processing + ETL Pipeline](processing.md): Details the steps taken to process the data are in the file `processing.md` in the root directory. Additionally comments have been added through-out the codebase to explain my thinking.
- 

- [ETL Pipeline](_docs/1_etl_pipeline.md)
- [Data Quality Checks](_docs/2_data_quality_checks.md)
- [Data Validation](_docs/3_data_validation.md)
- [Data Documentation](_docs/4_data_documentation.md)
- [Deployment & Automation](_docs/5_deployment_automation.md)


#### Constraints and Future Work
A lot more could have been done but the time was insufficient to complete them.
- For scalability, I would have created a `dispatcher` that would listen to changes in the `samples directory` and batch them. These batches will be tested for structural and schema conformance and quarantined where they do not meet such. The rest of the batch will then be passed to a MessageQueue which instances of the ETL pipeline are registred to. The idea being that if we batch the jobs we can horizontally scale the ETL pipeline as required. The batch size will also determine how soon we can start seeing data on the dashboard. For this demonstration this was left out due to time constraint. On the bringhtside, running the entire pipeline on the 10000 records took < 30secs on my dev computer which is has 8gb of RAM, it means testing the pipeline wont eat too much of your time :)
- Due to time constraint, the dispatcher and ETL service were not containerised and need to be run directly on the host machine or via a notebook.
- Due to time constraints, I have implemented a single page dashboard using AngularJS (angular 1) this is because it is far quicker to prototype in angularJS than other frameworks or at least it is for me in comparison to the latest release of angular and/or react.
- Go has been used for the backend API because I'm implementing a pet project in Go currently and thought I might as well squeeze in more practice.

#### My envisioned solution
Due to constraints, I scaled down the solution but the image below summarises the key points:



### RUNNING THIS SOLUTION