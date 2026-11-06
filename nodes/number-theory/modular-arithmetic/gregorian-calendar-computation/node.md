---
tag: 3NM0VD
kind: algorithm
slug: gregorian-calendar-computation
name: Gregorian calendar computation
aliases:
- Gregorian calendar
area: number-theory/modular-arithmetic
level: intro
summary: Converts between Gregorian calendar dates and day numbers using the rules for months and leap years.
solves: [calendrical-calculations]
model: word-ram
complexity:
  vars: {n: the number of decimal digits of the year or of the day number}
  time: {worst: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
  bit_operations: {worst: O(n)}
properties: {deterministic: true, recursive: false}
history:
  note: Pope Gregory XIII introduced the calendar in 1582 with the bull Inter gravissimas; Dershowitz and Reingold published the fixed-date algorithms in 1990 and in their book Calendrical Calculations.
prereqs: [floor-division, division-with-remainder]
see_also: [julian-day-number, calendrical-calculations, congruence, radix, integer-division, chinese-remainder-theorem]
sources:
  - book: isbn:9781107057623
    title: Edward M. Reingold and Nachum Dershowitz, Calendrical Calculations, the Ultimate Edition, Cambridge University Press, 2018
    locator: Chapter 2, The Gregorian Calendar (the leap year rule, fixed-from-gregorian, gregorian-year-from-fixed with the 400-, 100-, 4- and 1-year cycles, gregorian-from-fixed), and Chapter 1, Calendar Basics (fixed day numbers, R.D. 1 as 1 January of year 1, and the day of the week)
  - paper: doi:10.1002/spe.4380200905
    title: Nachum Dershowitz and Edward M. Reingold, Calendrical calculations, Software, Practice and Experience 20(9), 1990
    locator: pages 899 to 928 (the absolute day count and the Gregorian conversions)
  - url: https://howardhinnant.github.io/date_algorithms.html
    title: Howard Hinnant, chrono-Compatible Low-Level Date Algorithms
    locator: sections days_from_civil and civil_from_days (the conversion with eras of 400 years and years that start in March, with a proof of each step)
  - url: https://en.wikipedia.org/wiki/Gregorian_calendar
    title: Gregorian calendar, Wikipedia
    locator: the leap year rule and the mean year of 365.2425 days, and section History (the bull Inter gravissimas of 1582 and the change from 4 October to 15 October 1582)
---

**Gregorian calendar computation** converts a date of the Gregorian calendar, the civil calendar of most of the world, to a single day number and back. The method of Reingold and Dershowitz counts *fixed* day numbers (R.D.), with R.D. 1 on 1 January of year 1. To go from a date to its number it adds the days of the full years before it, with the leap days counted by three [floor divisions](/floor-division/), the days of the full months, and the day in the month. To go back, it splits the number into cycles of 400, 100, 4 and 1 years by [division with remainder](/division-with-remainder/), and then finds the month with one division. Both directions take a fixed number of integer operations. With day numbers, the difference of two dates is a subtraction and the day of the week is the number modulo $7$. The [Julian day number](/julian-day-number/) is the same count with another starting point.

## In plain words

The Gregorian calendar adds a leap day, 29 February, in every year that is a multiple of four. It skips the leap day in years that are multiples of one hundred, but keeps it in years that are multiples of four hundred. So 2000 was a leap year, and 1900 and 2100 are not.

To turn a date into a day number, count the days in the full years before it, then in the full months of its year, then add the day. The leap days before a year are counted with three divisions, one for each rule.

To go back from a day number to a date, find how many full four-hundred-year cycles fit in it, then centuries, then four-year groups, then single years. What is left gives the month and the day.

## The problem

**Input.** A date $(y, m, d)$ of the proleptic Gregorian calendar, with $1 \le m \le 12$ and $1 \le d$ at most the length of month $m$ in year $y$. Or, for the inverse, an integer day number $r$.

**Output.** The fixed day number $r$ of the date, or the date of the fixed day number $r$, and the day of the week.

**Representation and range.** Years use astronomical numbering, with year $0$ for 1 BC. The calendar is extended backward before 1582 (the *proleptic* calendar). A year $y$ is a leap year if $4 \mid y$ and either $100 \nmid y$ or $400 \mid y$. The month lengths are $31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31$, with $29$ days in February of a leap year. Fixed day numbers start with R.D. 1 on Monday 1 January of year 1 and are defined for all integers, so R.D. 0 is 31 December of year 0. For the years 1 to 9999 they agree with Python's `date.toordinal`. The divisions $\lfloor \cdot \rfloor$ and $\bmod$ are floor division and the non-negative remainder, which makes the formulas valid for negative values.

**Cost model.** On the [word RAM](/word-ram/), each formula makes a fixed number of additions, multiplications by small constants and divisions by small constants, so it takes $\Theta(1)$ time. The largest intermediate values are about $365|y|$ or $|r|$, so 64-bit signed words suffice for years of absolute value up to about $10^{16}$. For a year of $n$ decimal digits in [arbitrary precision](/arbitrary-precision-arithmetic/), each operation with a constant costs $O(n)$, so a conversion takes $O(n)$ bit operations.

## The algorithm

```pseudo id=main
LEAP(y)
L1  return y mod 4 = 0 and (y mod 100 ≠ 0 or y mod 400 = 0)

FIXED-FROM-GREGORIAN(y, m, d)                ▷ R.D. 1 is 1 January of year 1
L2  c ← 0 if m ≤ 2;  −1 if LEAP(y);  −2 otherwise
L3  return 365(y − 1) + ⌊(y − 1)/4⌋ − ⌊(y − 1)/100⌋ + ⌊(y − 1)/400⌋ + ⌊(367m − 362)/12⌋ + c + d

GREGORIAN-FROM-FIXED(r)
L4  d0 ← r − 1                               ▷ days since 1 January of year 1
L5  n400 ← ⌊d0 / 146097⌋;  d1 ← d0 mod 146097
L6  n100 ← ⌊d1 / 36524⌋;   d2 ← d1 mod 36524
L7  n4 ← ⌊d2 / 1461⌋;      d3 ← d2 mod 1461
L8  n1 ← ⌊d3 / 365⌋
L9  y ← 400 n400 + 100 n100 + 4 n4 + n1      ▷ full years before r
L10 if n100 ≠ 4 and n1 ≠ 4 then y ← y + 1    ▷ else r is 31 December of a leap year y
L11 p ← r − FIXED-FROM-GREGORIAN(y, 1, 1)    ▷ day of the year, from 0
L12 c ← 0 if r < FIXED-FROM-GREGORIAN(y, 3, 1);  1 if LEAP(y);  2 otherwise
L13 m ← ⌊(12(p + c) + 373) / 367⌋
L14 return (y, m, r − FIXED-FROM-GREGORIAN(y, m, 1) + 1)

DAY-OF-WEEK(r)
L15 return r mod 7                           ▷ 0 is Sunday, 1 is Monday, …, 6 is Saturday
```

**Line L3.** The first four terms count the days of the years $1$ to $y - 1$: $365$ each, plus one leap day for each multiple of $4$, minus one for each multiple of $100$, plus one for each multiple of $400$. The term $\lfloor (367m - 362)/12 \rfloor$ is the number of days before month $m$ if February had $30$ days: for $m = 1, \ldots, 12$ it gives $0, 31, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336$. The correction $c$ removes the two missing days of February, or one in a leap year, for the months after February.

**Lines L5 to L10.** A cycle of $400$ years has $400 \cdot 365 + 97 = 146097$ days, a century inside it has $36524$ days except the last, which has $36525$, a group of $4$ years inside a century has $1461$ days except possibly the last, and a year has $365$ days except a leap year. Dividing by the short lengths can give a quotient of $4$ only on the very last day of a long block, which is 31 December of a leap year. Line L10 handles this case: it does not add one, because that day belongs to the year that just ended.

**Lines L11 to L13.** The correction $c$ in line L12 adds the missing days of February back, so that $p + c$ is the day of the year in a calendar where February has $30$ days. Line L13 inverts the month formula of line L3 on that scale.

## Example

The table follows GREGORIAN-FROM-FIXED for two days: R.D. 739926, and R.D. 730485, which takes the special case of line L10.

| line | quantity | R.D. 739926 | R.D. 730485 |
|---|---|---|---|
| L4 | $d0$ | 739925 | 730484 |
| L5 | $n400$, $d1$ | 5, 9440 | 4, 146096 |
| L6 | $n100$, $d2$ | 0, 9440 | 4, 0 |
| L7 | $n4$, $d3$ | 6, 674 | 0, 0 |
| L8 | $n1$ | 1 | 0 |
| L9 | $y$ | 2025 | 2000 |
| L10 | $y$ | 2026 | 2000 (since $n100 = 4$) |
| L11 | $p$ | $739926 - 739617 = 309$ | 365 |
| L12 | $c$ | 2 (2026 is not a leap year) | 1 (2000 is a leap year) |
| L13 | $m$ | $\lfloor (12 \cdot 311 + 373)/367 \rfloor = \lfloor 4105/367 \rfloor = 11$ | $\lfloor (12 \cdot 366 + 373)/367 \rfloor = \lfloor 4765/367 \rfloor = 12$ |
| L14 | date | 6 November 2026 | 31 December 2000 |

In the second case $d1 = 146096$ is the last day of a 400-year cycle, the four centuries are full, and the year 2000 must not be advanced.

Forward, for 6 November 2026: $y - 1 = 2025$, so the years before give $365 \cdot 2025 + 506 - 20 + 5 = 739616$; the months before November give $\lfloor (367 \cdot 11 - 362)/12 \rfloor = 306$; the correction is $-2$; so $r = 739616 + 306 - 2 + 6 = 739926$. The day of the week is $739926 \bmod 7 = 5$, a Friday.

## Correctness

**Forward.** By [division with remainder](/division-with-remainder/), the number of multiples of $q$ in $1$ to $y - 1$ is $\lfloor (y - 1)/q \rfloor$ for $y \ge 1$, so the first four terms of line L3 count the days of the years $1$ to $y - 1$. For $y \le 0$ the same terms give minus the number of days in the years $y$ to $0$, because $\lfloor x/q \rfloor$ changes by one exactly when $x$ crosses a multiple of $q$. The month term and $c$ add the days of the months before $m$, by the table above, and $d$ adds the days of month $m$ up to the date. So line L3 counts the days from 31 December of year $0$ to the date, which is the R.D. number.

**Backward.** Write $d0 = r - 1$, the number of days from 1 January of year 1 to the date. The 400-year cycles that start on 1 January of years $\equiv 1 \pmod{400}$ have exactly $146097$ days, so line L5 gives the number of full cycles before the date and the day $d1$ in its cycle. Inside a cycle, the first three centuries have $36524$ days, and the fourth has $36525$. So $\lfloor d1/36524 \rfloor$ is the number of full centuries before the date, except on the last day of the cycle, $d1 = 146096$, where it is $4$ while only $3$ centuries and $36524$ days of the fourth are complete. The same holds for the four-year groups of $1461$ days: the last group of a short century has only $1460$ days, but there $d2 \le 36523 < 25 \cdot 1461$, so $n4 \le 24$. And it holds for the years of $365$ days, where the fourth year of a full group has $366$ days and gives the quotient $4$ only on its last day. In all cases except the quotient $4$, $y$ in line L9 is the number of full years before the date, so the year is $y + 1$; when $n100 = 4$ or $n1 = 4$, the date is 31 December of year $y$. Lines L11 to L14 then invert line L3 inside the year, since its month term is strictly increasing in $m$ and $p + c$ lies between the values for $m$ and $m + 1$. The proof in `proofs/correctness.md` gives the details.

**Day of the week.** R.D. 1 is a Monday, so R.D. $r$ falls on weekday $r \bmod 7$, with $0$ for Sunday. This holds for negative $r$ too, because $\bmod$ is the non-negative remainder.

## Complexity

FIXED-FROM-GREGORIAN makes at most $6$ divisions and $3$ multiplications by constants. GREGORIAN-FROM-FIXED makes $4$ divisions with remainder, one more division, and three calls of FIXED-FROM-GREGORIAN. So both take $\Theta(1)$ time on the word RAM, in the best and the worst case, with $\Theta(1)$ extra space. In arbitrary precision each operation with a constant costs $O(n)$ for an $n$-digit year, so a conversion costs $O(n)$ bit operations.

| measure | bound |
|---|---|
| time on the word RAM | $\Theta(1)$ per conversion |
| bit operations, $n$-digit year | $O(n)$ |
| extra space | $\Theta(1)$ words |

## Properties

- **Exact.** Only integer operations, no floating point, and no loop over years.
- **Valid for all integers.** With floor division the formulas hold for negative years and negative day numbers.
- **Periodic.** The calendar repeats every $400$ years, which hold $146097 = 7 \cdot 20871$ days, a whole number of weeks. So each date falls on the same weekday every 400 years.
- **Deterministic and iterative.** No random choices and no recursion.

## Variants and improvements

- **Years that start in March.** Moving January and February to the end of the previous year puts the leap day last, and then a single formula $\lfloor (153m + 2)/5 \rfloor$ gives the month offsets with no correction term. The [Julian day number](/julian-day-number/) page uses this form, and Hinnant's `days_from_civil` and `civil_from_days` use it with eras of 400 years and a count from 1 January 1970.
- **A loop over the years.** A naive conversion adds $365$ or $366$ per year. It is simple, but it takes time proportional to the distance from the epoch.
- **Weekday formulas.** Zeller's congruence and the "doomsday" rule give the day of the week directly from the date. They are the same computation as DAY-OF-WEEK$($FIXED-FROM-GREGORIAN$(y, m, d))$, with the constants folded together.
- **Other calendars.** Reingold and Dershowitz convert every calendar to and from fixed day numbers, so that a conversion between two calendars is a composition of two such functions.

## When to use it

Use these conversions whenever a program adds days to a date, subtracts two dates or finds a weekday in the civil calendar: convert to day numbers, compute with integers, and convert back. Library date types such as Python's `datetime.date` and C++'s `std::chrono` do this internally. For astronomy and for conversions between the Julian and the Gregorian calendars, the [Julian day number](/julian-day-number/) is the usual common count.

## Pitfalls

- **The century rule.** Testing only $y \bmod 4 = 0$ makes 1900 and 2100 leap years. Testing $y \bmod 100 \ne 0$ without the $400$ rule makes 2000 a common year.
- **Truncating division.** In C, Java and Go, `/` and `%` truncate toward zero, so the formulas fail for years before 1 or negative day numbers. Use floor division or shift the year into the positive range by a multiple of $400$ years.
- **The last day of a leap cycle.** Omitting the test in line L10 maps 31 December 2000 to 1 January 2001. The test with $n100 = 4$ or $n1 = 4$ catches it.
- **Historical dates.** The Gregorian calendar started on Friday 15 October 1582 in Catholic countries, and later elsewhere. Earlier dates in historical sources are usually in the Julian calendar, which needs the Julian conversion.
- **Year 0.** In historical numbering there is no year 0, so 1 BC must be entered as year $0$, and $k$ BC as $1 - k$.

## Implementations

The Python version follows the main block with the year computation in a separate function. Its `//`, `%` and `divmod` are floor division and the non-negative remainder, so it accepts any integer year. The tests compare it with a day-by-day count, with `datetime.date.toordinal` and `fromordinal`, and with the 400-year period for years of several hundred digits.

## History

Pope Gregory XIII introduced the calendar with the bull *Inter gravissimas* of 1582. It changed the leap year rule of the Julian calendar, so that the mean year is $365.2425$ days instead of $365.25$, and it dropped ten days: Thursday 4 October 1582 was followed by Friday 15 October 1582 (Wikipedia). Dershowitz and Reingold published the fixed-day algorithms for the Gregorian and other calendars in 1990, and expanded them in the book *Calendrical Calculations* (Chapter 2 for the Gregorian calendar).

## References
