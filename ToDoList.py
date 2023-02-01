from Storage import Planner
from rich.console import Console
import re

planner = Planner()
console = Console()
planner.menu()

while True:
    todayTasks = ''
    command = console.input("[red]Enter command: ")
    if command.lower() == 'add':
        enterDate = console.input("[yellow]Set the date for the tasks(yyyy-mm-dd). Press enter if it is the current day: ") 
        date = ''
        if enterDate == '':
            date += planner.getDate()
        else:
            date += enterDate.strip()
        if re.findall("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]", date):
            while True:
                adTask = console.input("[blue]Enter task for {}. Type 'done' when finished: ".format(date))
                if adTask.lower() == 'done':
                    break
                todayTasks += (adTask + ',')
            planner.addTask(date, todayTasks)
        else:
            console.print("[bold red]Please enter a proper date", justify="center")

    elif command.lower() == 'view all':
        planner.viewTask()

    elif re.findall("remove [1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]", command.lower()):
        itemRemove = re.findall("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]", command.lower())
        planner.removeDate(itemRemove[0])
        console.print("[green]Done", justify="center")

    elif re.findall("remove task", command.lower()):
        specDate = re.findall("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]", command.lower())[0]
        taskNum = re.findall("[0-9]|[0-9][0-9]", command.lower())[0]
        planner.removeTask(specDate, taskNum)
        console.print("[bold red]Task removed", justify="center")

    elif re.findall("view", command.lower()):
        viewDay = re.findall("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]", command.lower())
        planner.viewDate(viewDay[0])

    elif command.lower() == 'close':
        break
    
    else:
        continue