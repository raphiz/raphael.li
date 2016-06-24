---
layout: project
title: HRS Stundenplanplaner
type: project
github: https://github.com/raphiz/stundenplanplaner
teaser: Optimised timetable planning
initiation: 2016
status: maintained
---

Every semester, all students of [HSR](https://www.hsr.ch) have to put together their timetable for the next semester. Most students create spreadsheets or use calendar apps. Obviously, this isn't fun at all. So instead of doing this crunching work manually, I spent my time creating a program that does the work for me.

The result consists of a python library to fetch raw timetable data from the HSR timetable portal, a planning algorithm as well as a calendar export mechanism.

Since the HSR timetable portal is closed source and has no public API, I had to [scrape](https://de.wikipedia.org/wiki/Screen_Scraping) the markup code of the website.

I used a constraint solver algorithm for the actual timetable planning which allowed me to define constraints such as "at least twice a week no lectures in the afternoon" or "no lectures after 4 pm".

Here is an example output:

```
[...]
Calculation took 43.428021 seconds
Found 4 solutions!
Time      Mon      Tue       Wed       Thu       Fri       Sat    Sun
--------  -------  --------  --------  --------  --------  -----  -----
08:10:00  WED2-v1  AD2-v1    BuPl-v6   PrFm-v1   PrFm-u11
09:05:00  WED2-v1  AD2-v1    BuPl-u61  PrFm-v1   PrFm-u11
10:10:00  MGE-v1   SE1-v1    CPl-v1    WED2-u13  MGE-u11
11:05:00  MGE-v1   SE1-v1    CPl-v1    WED2-u13  MGE-u11
12:10:00                     MsTe-v1
13:10:00           AD2-u14
14:05:00           AD2-u14   MsTe-v1
15:10:00           SE1-u14   CPl-u12
16:05:00           SE1-u14   CPl-u12
17:00:00           ReIng-v1  MsTe-u11
17:55:00           ReIng-v1  MsTe-u11

[...]
```

Later have I realised that having access to *all* timetable data can be used for other interesting calculations - for example, which of my fellow students visit the same lectures as I do or do we have common lunch breaks?

The project is, of course, open source and can be used by all HSR students although I have not advertised. Since it's more an API than a practical tool it's not (yet) accessible to people without programming experience.

The application could be easily adapted for students of other universities - the back end part is isolated and can be replaced ([contact  me ](/contact/) if you plan to do this - I can help you with it <i class="fa fa-smile-o" aria-hidden="true"></i>)
