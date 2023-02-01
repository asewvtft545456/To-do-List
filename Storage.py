import datetime
import sqlite3
from rich.console import Console
from rich.table import Table

class Planner:
    def __init__(self):
        self.conn = sqlite3.connect('task.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS todo(
                        date text,
                        tak text)""")
        self.console = Console()
    
    def menu(self):
        table = Table(title="Commands", box=None)
        table.add_column(justify="center", style="cyan", no_wrap=True)
        table.add_column(style="magenta", justify="center")
        table.add_row("add", "Add a task")
        table.add_row("remove (data)", "Remove a task")
        table.add_row('remove task #(starting at 1) from (date)', 'remove a specific task')
        table.add_row("view all", "view all tasks")
        table.add_row("view (date)",'view task on a certain date')
        table.add_row("close", "Close program")
        self.console.print(table, justify="center")
        
    def getDate(self):
        current = datetime.datetime.now()
        splitDateTime = str(datetime.datetime(current.year, current.month, current.day)).split()
        return splitDateTime[0]
    
    def addTask(self, day, things):
        e = self.select(day)
        if e:
            additional = ''
            for x in e:
                additional += (x[1] + things)
            self.updateTask(day, additional)
        else:
            with self.conn:
                self.c.execute("INSERT INTO todo VALUES(:date, :tak)", {'date':day, 'tak':things})
                self.conn.commit()
    
    def select(self, day):
        self.c.execute("SELECT * FROM todo WHERE date=:date", {'date':day})
        return self.c.fetchall()

    def viewTask(self):
        self.c.execute("SELECT * FROM todo")
        res = self.c.fetchall()
        for x, y in res:
            self.console.rule(x)
            tasks = y.split(',')
            for x in tasks:
                self.console.print(x, justify="center")
            
    
    def viewDate(self, day):
        self.c.execute("SELECT * FROM todo WHERE date=:date", {'date':day})
        res = self.c.fetchall()[0]
        date = res[0]
        tasks = res[1].split(',')
        self.console.rule(date)
        for x in tasks:
            self.console.print(x, justify="center")
            

    
    def removeDate(self, day):
        with self.conn:
            self.c.execute("DELETE from todo WHERE date= :date", {'date':day})
            self.conn.commit()

    def removeTask(self, day, num):
        self.c.execute("SELECT * FROM todo WHERE date=:date", {'date':day})
        tasks = self.c.fetchall()[0][1].split(',')
        del tasks[int(num)-1]
        newTasks = ','.join(tasks)
        with self.conn:
            self.c.execute("""UPDATE todo SET tak =:tak
                        WHERE date = :date""",
                    {'date':day, 'tak':newTasks})
    
    def updateTask(self, day, newT):
        with self.conn:
            self.c.execute("""UPDATE todo SET tak =:tak
                        WHERE date = :date""",
                    {'date':day, 'tak':newT})