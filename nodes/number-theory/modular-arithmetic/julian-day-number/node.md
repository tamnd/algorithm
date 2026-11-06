---
tag: EDDN3S
kind: algorithm
slug: julian-day-number
name: Julian day number
aliases:
- Julian day numbers
area: number-theory/modular-arithmetic
level: intro
summary: Numbers days by a continuous count from a fixed epoch, which turns date arithmetic into simple integer arithmetic.
solves: [calendrical-calculations]
model: word-ram
complexity:
  vars: {n: the number of decimal digits of the year or of the day number}
  time: {worst: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
  bit_operations: {worst: O(n)}
properties: {deterministic: true, recursive: false}
history:
  note: Scaliger proposed the 7980-year Julian period in 1583; Herschel made the day count a tool of astronomy in 1849; Fliegel and Van Flandern published integer formulas for the conversion in 1968.
prereqs: [floor-division, division-with-remainder]
see_also: [gregorian-calendar-computation, calendrical-calculations, congruence, chinese-remainder-theorem, integer-division, radix]
sources:
  - paper: doi:10.1145/364096.364097
    title: Henry F. Fliegel and Thomas C. Van Flandern, A machine algorithm for processing calendar dates, Communications of the ACM 11(10), 1968
    locator: page 657 (the one-line integer formulas from a Gregorian date to the Julian day number and back)
  - book: isbn:9780943396613
    title: Jean Meeus, Astronomical Algorithms, second edition, Willmann-Bell, 1998
    locator: Chapter 7, Julian Day (the definition, the conversion from a calendar date with the Gregorian correction, the inverse, and the day of the week)
  - book: isbn:9781107057623
    title: Edward M. Reingold and Nachum Dershowitz, Calendrical Calculations, the Ultimate Edition, Cambridge University Press, 2018
    locator: Chapter 1, Calendar Basics (fixed day numbers, the Julian day number as an alternative epoch, and the use of floor and mod for negative values)
  - url: https://en.wikipedia.org/wiki/Julian_day
    title: Julian day, Wikipedia
    locator: sections History (Julian period, Julian day numbers) and Julian day number calculation (Gregorian and Julian calendar conversions, the inverse attributed to Richards, the day of the week)
---

The **Julian day number** (JDN) of a day is its position in a single continuous count of days. Day $0$ is 1 January 4713 BC in the proleptic Julian calendar, which is 24 November 4714 BC in the proleptic Gregorian calendar, and the count goes up by one each day: 1 January 2000 is day $2451545$. With such a count, the number of days between two dates is a subtraction, the date $k$ days later is an addition, and the day of the week is a [remainder](/division-with-remainder/) modulo $7$. The conversion from a calendar date to the JDN and back uses only a few integer multiplications and [floor divisions](/floor-division/), with no tables and no loops. It is the standard bridge between calendars in astronomy, and the same method gives the day counts of Unix time and of most date libraries. It solves the core of [calendrical calculations](/calendrical-calculations/).

## In plain words

Calendars are awkward for arithmetic. Months have different lengths, and some years have an extra day. So the question "how many days from one date to another" needs care.

The fix is to number all days in one long row, like the pages of a book. Each date gets one whole number, and the next day gets the next number. Then the distance between two dates is one subtraction.

The trick in the conversion is to start the year in March. Then the extra leap day comes at the very end of the year, and the month lengths repeat in a regular pattern that a single short formula can follow. The leap days before a year are counted with three divisions, one for each leap year rule.

## The problem

**Input.** A date of the proleptic Gregorian calendar: a year $Y$, a month $M$ with $1 \le M \le 12$, and a day $D$ with $1 \le D \le$ the length of month $M$ in year $Y$. Or, for the inverse, an integer $J$.

**Output.** The Julian day number $J$ of the date, or the date $(Y, M, D)$ of the day number $J$.

**Representation and range.** Years use astronomical numbering: the year before 1 AD is year $0$ (1 BC), and the year before that is $-1$ (2 BC). The Gregorian calendar is extended backward before its introduction in 1582 (the *proleptic* calendar). A Gregorian year $Y$ is a leap year if $4 \mid Y$ and either $100 \nmid Y$ or $400 \mid Y$. The JDN counts whole days; the astronomical *Julian date* JD adds the fraction of the day from noon, so that the day with number $J$ runs from JD $J - 0.5$ to JD $J + 0.5$ at Greenwich midnight to midnight. The formulas hold for every integer year and every integer $J$, positive or negative, provided that $\lfloor \cdot \rfloor$ is floor division.

**Cost model.** On the [word RAM](/word-ram/), each formula makes a fixed number of additions, multiplications by small constants and floor divisions by small constants, so it takes $\Theta(1)$ time. The largest intermediate values are about $4|J|$, so with 64-bit signed words the formulas are exact for $|J| < 2^{61}$, which covers years of absolute value up to about $6 \cdot 10^{15}$. For a year of $n$ decimal digits in [arbitrary precision](/arbitrary-precision-arithmetic/), multiplication and division by a constant cost $O(n)$, so a conversion takes $O(n)$ bit operations.

## The algorithm

Two shifts make the formulas short. The year is taken to start on 1 March, so that the leap day is the last day of a year. And the count starts at 1 March of year $-4800$, a date before day $0$ that begins a 400-year cycle, so that the count of years $y$ is non-negative for all dates of interest.

```pseudo id=main
JDN-FROM-DATE(Y, M, D)                       ▷ proleptic Gregorian date
L1  a ← ⌊(14 − M) / 12⌋                      ▷ 1 for January and February, else 0
L2  y ← Y + 4800 − a                         ▷ years since 1 March −4800, years start in March
L3  m ← M + 12a − 3                          ▷ 0 for March, …, 9 for December, 10 and 11 for January and February
L4  return D + ⌊(153m + 2) / 5⌋ + 365y + ⌊y/4⌋ − ⌊y/100⌋ + ⌊y/400⌋ − 32045

DATE-FROM-JDN(J)
L5  a ← J + 32044                            ▷ days since 1 March −4800
L6  b ← ⌊(4a + 3) / 146097⌋                  ▷ whole centuries
L7  c ← a − ⌊146097b / 4⌋                    ▷ day within the century
L8  d ← ⌊(4c + 3) / 1461⌋                    ▷ whole years within the century
L9  e ← c − ⌊1461d / 4⌋                      ▷ day within the year, 0 is 1 March
L10 m ← ⌊(5e + 2) / 153⌋                     ▷ month, 0 is March
L11 D ← e − ⌊(153m + 2) / 5⌋ + 1
L12 M ← m + 3 − 12⌊m/10⌋
L13 Y ← 100b + d − 4800 + ⌊m/10⌋
L14 return (Y, M, D)
```

The term $\lfloor (153m + 2)/5 \rfloor$ in line L4 is the number of days from 1 March to the first day of month $m$. For $m = 0, 1, \ldots, 11$ it gives $0, 31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337$: the month lengths from March to January are $31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31$, a pattern of period five that this formula follows exactly. The terms $\lfloor y/4 \rfloor - \lfloor y/100 \rfloor + \lfloor y/400 \rfloor$ count the leap days before year $y$. The constant $-32045$ fixes the count so that 1 March $-4800$ gets the number $-32044$ and 24 November $-4713$ gets $0$.

Lines L5 to L13 run the same count backward. Line L6 finds the number of whole centuries from 1 March $-4800$; a century has $36524.25$ days on average, which is $146097/4$. Line L8 does the same with years of $1461/4 = 365.25$ days inside a century, and line L10 finds the month inside the year. Lines L12 and L13 move January and February back into the civil year that starts in January.

**The Julian calendar.** For dates of the proleptic Julian calendar, every fourth year is a leap year, and the count drops the century terms:

```pseudo id=julian-calendar
JDN-FROM-JULIAN-DATE(Y, M, D)
L1  a ← ⌊(14 − M) / 12⌋;  y ← Y + 4800 − a;  m ← M + 12a − 3
L2  return D + ⌊(153m + 2) / 5⌋ + 365y + ⌊y/4⌋ − 32083

JULIAN-DATE-FROM-JDN(J)
L3  c ← J + 32082
L4  d ← ⌊(4c + 3) / 1461⌋;  e ← c − ⌊1461d / 4⌋;  m ← ⌊(5e + 2) / 153⌋
L5  return (d − 4800 + ⌊m/10⌋,  m + 3 − 12⌊m/10⌋,  e − ⌊(153m + 2) / 5⌋ + 1)
```

**Day of the week.** Day $0$ was a Monday, so $(J + 1) \bmod 7$ gives the weekday with $0$ for Sunday, $1$ for Monday, up to $6$ for Saturday.

## Example

Forward, for 1 January 2000: $a = \lfloor 13/12 \rfloor = 1$, $y = 2000 + 4800 - 1 = 6799$ and $m = 1 + 12 - 3 = 10$. Then

$$J = 1 + 306 + 365 \cdot 6799 + 1699 - 67 + 16 - 32045 = 2451545.$$

Backward, for $J = 2451545$, the lines of DATE-FROM-JDN give:

| line | variable | value | meaning |
|---|---|---|---|
| L5 | $a$ | 2483589 | days since 1 March −4800 |
| L6 | $b$ | 67 | 67 whole centuries |
| L7 | $c$ | 36465 | day 36465 of the century that starts on 1 March 1900 |
| L8 | $d$ | 99 | 99 whole years into it, so the year that starts on 1 March 1999 |
| L9 | $e$ | 306 | day 306 of that year |
| L10 | $m$ | 10 | month 10 from March, which is January |
| L11 | $D$ | 1 | $306 - 306 + 1$ |
| L12 | $M$ | 1 | $10 + 3 - 12$ |
| L13 | $Y$ | 2000 | $6700 + 99 - 4800 + 1$ |

The weekday is $(2451545 + 1) \bmod 7 = 6$, a Saturday.

**Two calendars.** In the Julian calendar, Thursday 4 October 1582 has $J = 2299160$. The next day was proclaimed Friday 15 October 1582 in the Gregorian calendar, and JDN-FROM-DATE gives $2299161$. The weekdays $(J + 1) \bmod 7$ are $4$ and $5$: Thursday and Friday, with no break in the week. Other epochs are fixed offsets: Unix time starts on 1 January 1970, $J = 2440588$, and the Modified Julian Date $\mathrm{MJD} = \mathrm{JD} - 2400000.5$ starts at midnight at the start of 17 November 1858, $J = 2400001$.

## Correctness

Let $L(y) = \lfloor y/4 \rfloor - \lfloor y/100 \rfloor + \lfloor y/400 \rfloor$. For each integer $y$, $L(y) - L(y - 1)$ is $1$ if $y$ satisfies the Gregorian leap rule and $0$ otherwise, since each term grows by one exactly when $y$ is a multiple of its divisor. The March-based year $y$ runs from 1 March of civil year $y - 4800$ to the end of February of civil year $y - 4799$. It has a leap day if and only if civil year $y - 4799$ is a leap year, and since $4800$ is a multiple of $400$, this holds if and only if $y + 1$ satisfies the leap rule. So the number of days from 1 March of year $0$ to 1 March of year $y$ is $365y + L(y)$, also for negative $y$. Adding the month offset and $D - 1$ gives the day count from 1 March $-4800$, and line L4 adds the constant $-32044$. One date with a known number, such as 24 November $-4713$ with $J = 0$, fixes the constant.

The inverse finds the largest $b$ with $\lfloor 146097b/4 \rfloor \le a$, which is the day count at the start of century $b$. The identity $\lfloor x/q \rfloor \le a \iff x \le qa + q - 1$ for integers turns this into line L6, and lines L8 and L10 are the same step for years and months. The proof in `proofs/correctness.md` checks each step and shows that the remainders $c$ and $e$ stay in the right ranges, including the short centuries and the leap days.

## Complexity

Each conversion makes a fixed number of operations: lines L1 to L4 have $3$ multiplications by constants and $5$ floor divisions by constants, and lines L5 to L13 have $8$ multiplications and $8$ divisions. So the time is $\Theta(1)$ on the word RAM, in the best and the worst case, and the extra space is $\Theta(1)$ words. In arbitrary precision, each operation on an $n$-digit value with a constant of fixed size costs $O(n)$, so a conversion costs $O(n)$ bit operations.

| measure | bound |
|---|---|
| operations per conversion | at most 16 multiplications or divisions by constants |
| time on the word RAM, $\lvert J \rvert < 2^{61}$ | $\Theta(1)$ |
| bit operations, $n$-digit year | $O(n)$ |
| extra space | $\Theta(1)$ words |

## Properties

- **Exact and table-free.** Only integer operations; no floating point and no month table.
- **Valid for all integers.** With floor division the formulas hold for every year and every $J$, including dates before day $0$ and before the year $-4800$.
- **Periodic.** A Gregorian date moved by $400$ years moves its JDN by $146097$ days, and a Julian calendar date moved by $4$ years moves by $1461$ days. These cycles hold a whole number of weeks in the Gregorian case, $146097 = 7 \cdot 20871$, so the weekdays repeat every 400 years.
- **Deterministic and iterative.** No random choices and no recursion.

## Variants and improvements

- **Fliegel and Van Flandern (1968).** The original one-line form, written for Fortran integer division that truncates toward zero, is $J = D - 32075 + \lfloor 1461(Y + 4800 + \lfloor (M - 14)/12 \rfloor)/4 \rfloor + \lfloor 367(M - 2 - 12\lfloor (M - 14)/12 \rfloor)/12 \rfloor - \lfloor 3\lfloor (Y + 4900 + \lfloor (M - 14)/12 \rfloor)/100 \rfloor/4 \rfloor$, with each division truncated. It agrees with JDN-FROM-DATE for all dates from 1 March $-4800$ on, so for all non-negative day numbers, and fails before that because truncation and floor differ for negative values.
- **Meeus's method.** Meeus (Chapter 7) computes the Julian date with a correction $B = 2 - A + \lfloor A/4 \rfloor$, $A = \lfloor Y/100 \rfloor$, applied to the Julian calendar count, and handles fractions of a day. It works with real numbers and integer parts, and it is meant for non-negative Julian dates.
- **Other epochs.** Days since 1 January 1970 (Unix time), since 1 January of year 1 (the fixed day numbers, R.D., of Reingold and Dershowitz) or the Modified Julian Date differ from the JDN by a constant. See [Gregorian calendar computation](/gregorian-calendar-computation/) for the conversion built on the 400-year, 100-year and 4-year cycles directly.
- **Fractional days.** For a time of day $h$ hours after midnight in UT, $\mathrm{JD} = J - 0.5 + h/24$.

## When to use it

Use the JDN, or any fixed day count, whenever a program compares, subtracts or shifts dates, or converts between calendars: convert once at the input, compute with integers, and convert back at the output. The JDN in particular is the common reference of astronomy and of calendar conversions. For a date library inside one era, days since 1970 or since year 1 are often more convenient; they need the same formulas with another constant.

## Pitfalls

- **Truncating division.** In C, Java and Go, `/` truncates toward zero, so the formulas give wrong results for negative intermediate values. Use floor division, or keep the shifted year $y$ non-negative, which the shift by 4800 does for dates after 1 March $-4800$.
- **Historical years.** The year 1 BC is year $0$ in this numbering, and 45 BC is $-44$. A historical BC year $k$ must be entered as $1 - k$.
- **Which calendar.** Dates before 15 October 1582 are usually written in the Julian calendar, and many countries switched later: Britain and its colonies went from Wednesday 2 September 1752 to Thursday 14 September 1752. Applying the Gregorian formula to a Julian calendar date shifts it by $10$ to $13$ days in recent centuries.
- **Noon versus midnight.** The astronomical day starts at noon. A civil date with a time before noon UT belongs to Julian date $J - 0.5 + h/24$, not to $J + h/24$.
- **The other "Julian date".** In some industries a "Julian date" means the day of the year, such as 2026-310. It is not related to the JDN.

## Implementations

The Python version follows both blocks and the weekday rule. Python's `//` is floor division, so it accepts any integer year and any integer day number. The tests compare it with a day-by-day count, with the standard `datetime` module for the years 1 to 9999, and with the 400-year period for years of several hundred digits.

## History

Joseph Scaliger proposed the Julian period of $7980 = 28 \cdot 19 \cdot 15$ years in 1583, the product of the solar cycle, the Metonic lunar cycle and the indiction cycle. All three cycles were last in their first year together in 4713 BC, which became the epoch. John Herschel, in his *Outlines of Astronomy* of 1849, made the count of days in this period a tool for astronomers (Wikipedia, section History). Fliegel and Van Flandern published integer formulas for the conversion in 1968 for computer use, and Reingold and Dershowitz built their treatment of all calendars on fixed day numbers.

## References
