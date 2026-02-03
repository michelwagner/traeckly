# traeckly
## Time tracking service

### Starting tasks
Starting a task terminates the previous task.
Stopping stops the previous task without starting a new one.

`traekly.py start TASK_NAME_A`  
`traekly.py start TASK_NAME_B`  
`traeckly.py stop`  


### Creating a report for a given period of time
`traeckly.py report 2023-01-01 2023-01-31`

Calculates the total time spent for each task. 


### GUI
Rename `traeckly_gui.json` to `traeckly_gui.user.json` and adapt to your needs.  
*title* is used to lable the buttons, *task* is used as the task name that accumulates time.

### Shortcuts
`trk.bat stop` to terminate the active task (e.g. system shutdown, logoff)  
`trk_gui.bat` to launch GUI (e.g. system start, logon)  
