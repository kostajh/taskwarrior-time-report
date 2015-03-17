#!/usr/bin/env python
import datetime
import calendar
from cement.core import foundation
from taskw import TaskWarrior
import subprocess
import json
from tabulate import tabulate
from blessings import Terminal
import sys

TIME_FORMAT = '%Y%m%dT%H%M%SZ'

w = TaskWarrior()
t = Terminal()

date_today = datetime.date.today().strftime('%Y-%m-%d')
date_tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime(
    '%Y-%m-%d')


def main():
    app = foundation.CementApp('taskwarrior-time-report')
    try:
        app.setup()
        app.args.add_argument('-s', '--start', action='store', dest='start',
                              help='Start date')
        app.args.add_argument('-e', '--end', action='store', dest='end',
                              help='End date')
        # Default reports
        app.args.add_argument('-t', '--today', action='store_true',
                              dest='today', help='Timesheet for today')
        app.args.add_argument('-w', '--week', action='store_true',
                              dest='week', help='Timesheet for current week')
        app.args.add_argument('-m', '--month', action='store_true',
                              dest='month', help='Timesheet for current month')

        app.run()

        if app.pargs.today:
            date_range_start = date_today
            date_range_end = date_tomorrow
        elif app.pargs.week:
            # Weekly report
            print('todo')
            sys.exit(1)
        elif app.pargs.month:
            # Monthly report
            today = datetime.date.today()
            date_range_start = today.replace(day=1)
            date_range_end = today.replace(
                day=calendar.monthrange(today.year, today.month)[1])
        elif not app.pargs.today and not app.pargs.start:
            # Assume today as default report
            date_range_start = date_today
            date_range_end = date_tomorrow
        else:
            date_range_start = app.pargs.start
            if app.pargs.end:
                date_range_end = app.pargs.end
            else:
                date_range_end = date_tomorrow

        p = subprocess.Popen([
            'task',
            'status:completed',
            'logged:true',
            'status.not:deleted',
            'actual.not:empty',
            'end.after:%s' % date_range_start,
            'end.before:%s' % date_range_end,
            'rc.verbose=off',
            'export'
            ],
            stdout=subprocess.PIPE)
        out, err = p.communicate()

        if err:
            print t.red(err)
            sys.exit(1)

        if not out:
            print t.red("No results returned")
            sys.exit(1)

        logged_tasks = json.loads(out)

        if len(logged_tasks) == 0:
            print t.red('No data available')
            sys.exit(1)

        formatted_tasks = list()
        total_time = 0

        for task in logged_tasks:
            row = list()
            actual_time = ''
            if ('m' in task['actual']):
                # Convert to hours
                actual_time = float(int(task['actual'][:task['actual'].index('m')])) / 60
            elif ('h' in task['actual']):
                actual_time = task['actual'][:task['actual'].index('h')]
            elif ('s' in task['actual']):
                actual_time = float(int(task['actual'][:task['actual'].index('sec')]) / 60) / 60
            else:
                actual_time = float(int(task['actual']) / 60) / 60

            total_time = total_time + float(actual_time)

            # Create a row
            row.append(
                t.magenta(
                    str(datetime.datetime.strptime(task['end'], TIME_FORMAT))))
            row.append(t.green(task['project'] if 'project' in task else 'None'))
            row.append(t.green(task['description'][:40]))
            row.append(t.yellow(str(actual_time)))
            row.append(t.blue(task['uuid']))
            # Add the row
            formatted_tasks.append(row)

        print t.bold_black_on_green(
            'Timesheet for range: %s:%s' % (date_range_start, date_range_end))
        print tabulate(formatted_tasks)
        print t.bold_black_on_green('Total time: %s' % str(total_time))
    finally:
        app.close()


def cmdline():
    main()

if __name__ == '__main__':
    cmdline()
