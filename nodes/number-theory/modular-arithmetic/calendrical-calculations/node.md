---
tag: CH49VZ
kind: problem
slug: calendrical-calculations
name: Calendrical calculations
area: number-theory/modular-arithmetic
level: intro
summary: Converting between calendar dates and day counts and computing weekdays or date differences under calendar rules.
prereqs: [congruence, floor-division, division-with-remainder]
see_also: [julian-day-number, gregorian-calendar-computation, chinese-remainder-theorem, radix, integer-division]
sources:
  - book: isbn:9781107057623
    title: Edward M. Reingold and Nachum Dershowitz, Calendrical Calculations, the Ultimate Edition, Cambridge University Press, 2018
    locator: Chapter 1, Calendar Basics (fixed day numbers as the common base of all calendars, the day of the week, the k-th weekday on or before a date, cyclic leap-year rules of the form (a y + b) mod c < a), and Chapter 2, The Gregorian Calendar
  - paper: doi:10.1002/spe.4380200905
    title: Nachum Dershowitz and Edward M. Reingold, Calendrical calculations, Software, Practice and Experience 20(9), 1990
    locator: pages 899 to 928 (conversion of each calendar to and from an absolute day count)
  - book: isbn:9780943396613
    title: Jean Meeus, Astronomical Algorithms, second edition, Willmann-Bell, 1998
    locator: Chapter 7, Julian Day, and Chapter 8, Date of Easter
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.3.2, exercise 14 (Algorithm E, the date of Easter in the Gregorian calendar)
  - url: https://en.wikipedia.org/wiki/Julian_day
    title: Julian day, Wikipedia
    locator: section Julian day number calculation, subsection Julian period from indiction, Metonic and solar cycles
---

**Calendrical calculations** are the computations that a program makes with calendar dates: the number of days between two dates, the date $k$ days after a given one, the day of the week, the conversion of a date from one calendar to another, and the dates of holidays defined by rules such as "the fourth Thursday of November". Calendars mix units of different lengths: months of $28$ to $31$ days and years with or without a leap day. So these questions are awkward on dates and easy on a single count of days. The standard method, due to Reingold and Dershowitz, converts each date to a *fixed day number*, computes with integers, and converts back. For the arithmetic calendars, such as the [Gregorian](/gregorian-calendar-computation/) and the Julian calendar, each conversion takes a fixed number of [floor divisions](/floor-division/) and remainders, so the whole problem is a small exercise in [congruences](/congruence/).

## In plain words

People write dates as a day, a month and a year. That is good for reading, but bad for arithmetic, because months have different lengths and some years have an extra day.

So a program turns each date into one whole number: the count of days since a fixed starting day. With these numbers, the distance between two dates is a subtraction, and the date some days later is an addition. The day of the week is the remainder after division by seven.

The hard part is the conversion between a date and its count, which must follow the rules of the calendar. Good formulas need only a few divisions, with no loop over the years.

## Definition

A **calendar** $C$ is a set of names of days, the dates, together with a bijection $\operatorname{fixed}_C$ from these dates to the integers that respects the order of days: the next day of a date maps to the next integer. Reingold and Dershowitz fix $\operatorname{fixed}(1 \text{ January } 1) = 1$ in the proleptic Gregorian calendar, the *R.D.* (Rata Die) count; the [Julian day number](/julian-day-number/) is the same count shifted by $1721425$.

**Input.** One or more dates, each in a named calendar, and possibly integers (a number of days, a weekday $k \in \{0, \ldots, 6\}$, an index $n$).

**Output.** One of:

- **conversion:** $\operatorname{fixed}_C(x)$ for a date $x$, or the date $\operatorname{fixed}_C^{-1}(r)$ for an integer $r$;
- **difference:** $\operatorname{fixed}_C(x) - \operatorname{fixed}_{C'}(x')$, the number of days from $x'$ to $x$;
- **shift:** the date $\operatorname{fixed}_C^{-1}(\operatorname{fixed}_C(x) + k)$;
- **day of the week:** $\operatorname{fixed}(x) \bmod 7$, with $0$ for Sunday in the R.D. count;
- **change of calendar:** $\operatorname{fixed}_{C'}^{-1}(\operatorname{fixed}_C(x))$;
- **holiday rules:** for example the $n$-th weekday $k$ of a month, or the date of Easter in a given year.

**Representation.** A date of an arithmetic calendar is a tuple of integers such as $(y, m, d)$. Years use astronomical numbering, with year $0$ for 1 BC. Day numbers are integers of any sign.

**Cost model.** On the [word RAM](/word-ram/), with years and day numbers that fit in a word, arithmetic and floor division by constants cost $O(1)$. For years of $n$ decimal digits in arbitrary precision, an operation with a constant costs $O(n)$.

## Variants

- **Arithmetic calendars.** The rules use only integer arithmetic: the Gregorian, Julian, ISO week, arithmetic Islamic, Hebrew and Coptic calendars. All conversions take $O(1)$ operations.
- **Astronomical calendars.** The rules depend on the true positions of the sun and the moon, as in the Chinese calendar, the Persian astronomical calendar and the modern Hindu calendars. Conversion needs the time of new moons or of solar longitudes, computed from astronomical series, and a search for the right day.
- **Times within a day.** Adding a time of day turns the day count into a real or a rational number, as in the Julian date JD, Unix time in seconds, or Modified Julian Date. Time zones and daylight saving time add tables of political rules, and leap seconds make some UTC days one second longer.
- **Day count conventions.** Finance uses rules such as "30/360", where each month counts as $30$ days, and "actual/365", to compute interest between two dates. They are functions of the two dates, computed from the same day numbers or from the date fields.

## Examples

- **Difference.** 1 January 2000 is R.D. $730120$ and 6 November 2026 is R.D. $739926$, so they are $9806$ days apart.
- **Day of the week.** $739926 \bmod 7 = 5$, so 6 November 2026 is a Friday. In the ISO 8601 week calendar it is day $5$ of week $45$ of 2026.
- **The $n$-th weekday.** The last day with weekday $k$ on or before R.D. $r$ is $r - ((r - k) \bmod 7)$. The $n$-th weekday $k$ of a month that starts on R.D. $f$ is $7n + (f - 1) - ((f - 1 - k) \bmod 7)$. For Thanksgiving in the United States, the fourth Thursday ($k = 4$) of November 2026, this gives 26 November 2026.
- **Easter.** In the Gregorian calendar, Easter Sunday is defined from a tabular full moon and an epact. Gauss gave a formula for it, and Knuth (exercise 14 of Section 1.3.2) and Meeus (Chapter 8) give integer algorithms. In 2026 Easter falls on 5 April, and in 2000 it fell on 23 April.
- **Cyclic leap rules.** Many calendars spread $a$ leap years evenly over a cycle of $c$ years: year $y$ is a leap year when $(a y + b) \bmod c < a$. The arithmetic Islamic calendar uses $11$ leap years in $30$, with $(14 + 11y) \bmod 30 < 11$, which marks the years $2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29$ of each cycle. The Hebrew calendar uses $7$ leap years in $19$, with $(7y + 1) \bmod 19 < 7$, which marks the years $3, 6, 8, 11, 14, 17, 19$.
- **The Julian period.** Scaliger's Julian period of $7980 = 28 \cdot 19 \cdot 15$ years combines the solar cycle of $28$ years, the Metonic cycle of $19$ years and the indiction cycle of $15$ years. The year $Y$ AD is year $Y + 4713$ of the period, and its positions in the three cycles are its remainders modulo $28$, $19$ and $15$. For 2026 these are $19$, $13$ and $4$; since the moduli are pairwise coprime, the [Chinese remainder theorem](/chinese-remainder-theorem/) recovers the year $6739$ of the period from them.

## Known algorithms

| task | method | cost on the word RAM |
|---|---|---|
| Gregorian date to day number and back | [Gregorian calendar computation](/gregorian-calendar-computation/), cycles of 400, 100, 4 and 1 years | $\Theta(1)$ |
| Gregorian or Julian date to Julian day number and back | [Julian day number](/julian-day-number/), years that start in March | $\Theta(1)$ |
| day of the week | day number modulo $7$ | $\Theta(1)$ |
| $n$-th weekday of a month | the formula above | $\Theta(1)$ |
| date of Easter | Gauss's formula, Knuth's Algorithm E, Meeus's method | $\Theta(1)$ |
| cyclic leap rule | $(a y + b) \bmod c < a$, with day counts $\lfloor (c' y + b')/c \rfloor$ | $\Theta(1)$ |
| naive conversion | add the length of each year and month | $\Theta(\lvert y \rvert)$ |
| astronomical calendars | astronomical series and a bounded search for the day | depends on the precision of the series |

## Bounds

**Upper bounds.** For the arithmetic calendars, each conversion is a fixed formula with $O(1)$ additions, multiplications by constants and floor divisions by constants. So every task above takes $\Theta(1)$ time on the word RAM, and $O(n)$ bit operations for years of $n$ decimal digits, because multiplication and division of an $n$-digit number by a constant take $O(n)$.

**Lower bounds.** Every algorithm must read the year, so $\Omega(n)$ bit operations are needed for $n$-digit years. The formulas match this bound up to a constant factor.

**Periodicity.** The Gregorian calendar repeats every $400$ years, which hold $146097 = 7 \cdot 20871$ days, a whole number of weeks. So a table of $146097$ entries could also answer every query in $O(1)$; the formulas make such a table unnecessary.

## Reductions

- **Every conversion goes through day numbers.** With $k$ calendars, $2k$ functions to and from the fixed count give all $k^2$ conversions between pairs. This is the design of Reingold and Dershowitz.
- **Weekdays reduce to residues.** The day of the week is the day number modulo $7$, and "the last weekday $k$ on or before" is a correction by a residue modulo $7$.
- **Leap-year rules reduce to floors of linear functions.** For a cyclic rule with $a$ leap years in $c$, the number of leap years among the first $y$ is $\lfloor (a y + b')/c \rfloor$ for a suitable $b'$, so the day count is a linear function plus a floor, and its inverse is again a floor division.
- **Cycle positions reduce to the Chinese remainder theorem.** A calendar that names a year by its positions in several cycles with pairwise coprime lengths, such as the Julian period or the 60-year cycle of the Chinese calendar formed from cycles of $10$ and $12$ (with $\gcd(10, 12) = 2$, so only $60$ of the $120$ pairs occur), is decoded by the [Chinese remainder theorem](/chinese-remainder-theorem/) in its general form.

## Applications

- **Date libraries.** Python's `datetime`, C++'s `std::chrono`, Java's `java.time` and database engines store dates as day counts or second counts and convert at the input and output.
- **Scheduling.** Recurring events such as "every second Tuesday" and business-day arithmetic need weekdays and shifts.
- **Astronomy.** The Julian date is the common time scale of astronomical tables and observations.
- **Religious and civil holidays.** Easter, Passover, Ramadan and the Chinese New Year need conversions between calendars.
- **Finance.** Interest and bond accrual use day count conventions between two dates.

## References
