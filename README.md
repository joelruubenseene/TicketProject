# TicketProject

A quicker, CLI-based interface to check Elron trains timetable and prices between 2 stops

## Usage

```
$ python3 traintimes.py
```

## Output

```
$ python3 traintimes.py

Input starting stop: Tartu
Input destination: Tallinn
Input date as YYYY-MM-DD (leave empty for today): 
Show all trips today? (Y/N) Y

Tartu --> Tallinn
+---------------+--------+
| 06:18 - 08:47 | 9.95€  |
+---------------+--------+
| 07:57 - 10:02 | 12.67€ |
+---------------+--------+
| 08:54 - 10:58 | 11.56€ |
+---------------+--------+
| 10:45 - 12:52 | 11.56€ |
+---------------+--------+
| 11:33 - 14:00 | 9.95€  |
+---------------+--------+
| 13:08 - 15:15 | 12.67€ |
+---------------+--------+
| 15:05 - 17:12 | 11.56€ |
+---------------+--------+
| 16:30 - 18:36 | 12.67€ |
+---------------+--------+
| 17:57 - 20:24 | 9.95€  |
+---------------+--------+
| 19:07 - 21:13 | 11.56€ |
+---------------+--------+
| 20:25 - 22:54 | 9.95€  |
+---------------+--------+

```
