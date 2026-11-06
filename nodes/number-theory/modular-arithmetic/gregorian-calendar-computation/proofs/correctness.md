---
title: The fixed-date conversions of the Gregorian calendar are inverse bijections
proves: [correctness]
status: full
---

**Claim.** Let $\mathcal{G}$ be the set of valid proleptic Gregorian dates $(y, m, d)$ with $y \in \mathbb{Z}$. FIXED-FROM-GREGORIAN numbers the days of $\mathcal{G}$ consecutively with $1$ on 1 January of year $1$, so it is a bijection from $\mathcal{G}$ to $\mathbb{Z}$. GREGORIAN-FROM-FIXED is its inverse, and DAY-OF-WEEK$(r)$ is $0$ for Sunday through $6$ for Saturday.

Throughout, $\lfloor \cdot \rfloor$ is floor division and $x \bmod q = x - q\lfloor x/q \rfloor \in \{0, \ldots, q - 1\}$, defined for all integers $x$.

**Notation.** Let $\chi(z) = 1$ if $4 \mid z$ and ($100 \nmid z$ or $400 \mid z$), and $\chi(z) = 0$ otherwise; this is LEAP (line L1). Year $z$ has $365 + \chi(z)$ days. Let $L(x) = \lfloor x/4 \rfloor - \lfloor x/100 \rfloor + \lfloor x/400 \rfloor$ and $F(x) = 365x + L(x)$. For $q \ge 1$, $\lfloor z/q \rfloor - \lfloor (z - 1)/q \rfloor = [q \mid z]$, so $L(z) - L(z - 1) = [4 \mid z] - [100 \mid z] + [400 \mid z] = \chi(z)$ by cases, and

$$F(z) - F(z - 1) = 365 + \chi(z).$$

With $F(0) = 0$, $F(x)$ is the number of days in the years $1$ to $x$ for $x \ge 0$, and minus the number of days in the years $x + 1$ to $0$ for $x < 0$. In both cases, the days before 1 January of year $y$, counted from 1 January of year $1$, number $F(y - 1)$.

**Month offsets.** Let $g(m) = \lfloor (367m - 362)/12 \rfloor$. Direct evaluation gives $g(1), \ldots, g(13) = 0, 31, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336, 367$. The differences $g(m + 1) - g(m)$ for $m = 1, \ldots, 12$ are $31, 30, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31$: the true month lengths, except $30$ for February. For year $y$, let $c_y(m) = 0$ for $m \le 2$ and $c_y(m) = -2 + \chi(y)$ for $m \ge 3$ (line L2). Then $h_y(m) = g(m) + c_y(m)$ is the number of days in year $y$ before month $m$, because February has $28 + \chi(y)$ days, which is $30 - (2 - \chi(y))$.

**Forward (lines L2 and L3).** Line L3 returns $F(y - 1) + h_y(m) + d$, which is the number of days from 1 January of year $1$ to the date, plus $1$. So two consecutive days get consecutive numbers, and 1 January of year $1$ gets $F(0) + 0 + 1 = 1$. Every date is reached from 1 January of year $1$ by finitely many steps forward or backward, so the map is a bijection from $\mathcal{G}$ to $\mathbb{Z}$.

**Mixed-radix form of $F$.** Every integer $x$ has a unique form $x = 400a + 100b + 4c + e$ with $a \in \mathbb{Z}$, $0 \le b \le 3$, $0 \le c \le 24$ and $0 \le e \le 3$. Then $\lfloor x/4 \rfloor = 100a + 25b + c$, $\lfloor x/100 \rfloor = 4a + b$ and $\lfloor x/400 \rfloor = a$, because $e \le 3$, $4c + e \le 99$ and $100b + 4c + e \le 399$. So $L(x) = 97a + 24b + c$ and

$$F(x) = 146097a + 36524b + 1461c + 365e.$$

Also $x + 1$ is a leap year exactly when $e = 3$ and ($c \ne 24$ or $b = 3$), since $x + 1 = 400a + 100b + 4(c + 1)$ is then a multiple of $4$, of $100$ exactly when $c = 24$, and of $400$ exactly when $c = 24$ and $b = 3$.

**Backward, the year (lines L4 to L10).** Let $r$ be an integer with date $(y^*, m^*, d^*)$. By the forward part, $r = F(y^* - 1) + h_{y^*}(m^*) + d^*$. Let $x^* = y^* - 1 = 400a + 100b + 4c + e$ in the form above, and $t = h_{y^*}(m^*) + d^* - 1$, the day of the year counted from $0$, so $0 \le t \le 364 + \chi(y^*)$. Line L4 gives $d0 = r - 1 = F(x^*) + t = 146097a + 36524b + 1461c + 365e + t$.

- *Line L5.* The part after $146097a$ is at most $36524 \cdot 3 + 1461 \cdot 24 + 365 \cdot 3 + 365 = 146096$, so $n400 = a$ and $d1 = 36524b + 1461c + 365e + t$.
- *Line L6.* The part $1461c + 365e + t$ is at most $35064 + 1095 + 365 = 36524$, with equality only if $c = 24$, $e = 3$ and $t = 365$. Then $y^*$ is a leap year, so $b = 3$. *Case A:* not all of these hold. Then $n100 = b$ and $d2 = 1461c + 365e + t$. *Case B:* $b = 3$, $c = 24$, $e = 3$, $t = 365$. Then $d1 = 146096$, $n100 = 4$ and $d2 = 0$, so lines L7 and L8 give $n4 = n1 = 0$, line L9 gives $y = 400a + 400 = x^* + 1 = y^*$, and line L10 keeps it.
- *Line L7, Case A.* The part $365e + t$ is at most $1095 + 365 = 1460 < 1461$, so $n4 = c$ and $d3 = 365e + t$.
- *Line L8, Case A.* If $t \le 364$, then $n1 = e \le 3$, line L9 gives $y = x^*$, and line L10 adds one: $y = y^*$. If $t = 365$, then $y^*$ is a leap year, $e = 3$, $d3 = 1460$ and $n1 = 4$, so line L9 gives $y = x^* + 1 = y^*$ and line L10 keeps it.

In every case the year after line L10 is $y^*$.

**Backward, the month and the day (lines L11 to L14).** Line L11 gives $p = r - (F(y^* - 1) + 1) = t$. The test of line L12 holds exactly when $m^* \le 2$, so $c = -c_{y^*}(m^*)$ and $p + c = g(m^*) + d^* - 1$. Since $0 \le d^* - 1$ and $d^*$ is at most the true length of month $m^*$, which is at most $g(m^* + 1) - g(m^*)$, we get $g(m^*) \le p + c < g(m^* + 1)$. The function $g$ is strictly increasing, so $m^*$ is the largest $m$ with $g(m) \le p + c$. For integers, $g(m) \le T \iff 367m - 362 \le 12T + 11 \iff m \le (12T + 373)/367$, so this largest $m$ is $\lfloor (12(p + c) + 373)/367 \rfloor$, which is line L13. Line L14 returns $r - (F(y^* - 1) + h_{y^*}(m^*) + 1) + 1 = d^*$.

**Day of the week (line L15).** R.D. $1$ is a Monday, and consecutive days have consecutive numbers, so R.D. $r$ is $r - 1$ days after a Monday and its weekday is $(1 + (r - 1)) \bmod 7 = r \bmod 7$ with $0$ for Sunday, for every integer $r$. $\blacksquare$
