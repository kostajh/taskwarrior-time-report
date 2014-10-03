Taskwarrior Time Report
=======================

This utility allows you to generate time reports of your tasks in Taskwarrior.
This assuming that you store the total active time in a UDA called `actual` of
the `duration` type.

Usage::

    taskwarrior_time_report --start:2014-09-01 --end:2014-09-30

    taskwarrior_time_report --today

Clone this repo, then install using pip::

    pip install -e /path/to/taskwarrior-time-report
