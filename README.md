# traeckly

## Time tracking service

### GUI
Rename `traeckly_gui.json` to `traeckly_gui.user.json` and adapt to your needs.  
*title* is used to lable the buttons, *task* is used as the task name that accumulates time.


### Starting tasks
Starting a task terminates the previous task.
Stopping stops the previous task without starting a new one.

`traekly.py start TASK_A` starts Task A.  
`traekly.py start TASK_B` stops Task A and starts Task B.  
`traeckly.py stop` stops Task B.


### Creating a report for a given period of time
`traeckly.py report 2023-01-01 2023-01-31`

Calculates the total time spent for each task. 


### Shortcuts
`trk.bat stop` to terminate the active task (e.g. system shutdown, logoff)  
`trk_gui.bat` to launch GUI (e.g. system start, logon)  


### Storage
By default the task durations are stored in a SQLite database file.  
To view the data a database viewer such as [DB Browser for SQLite](https://sqlitebrowser.org/) can be used.  