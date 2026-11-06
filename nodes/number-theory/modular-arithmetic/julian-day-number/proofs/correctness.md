---
title: The Julian day number conversions are inverse bijections
proves: [correctness]
status: full
---

**Claim.** Let $\mathcal{G}$ be the set of valid dates $(Y, M, D)$ of the proleptic Gregorian calendar, with $Y \in \mathbb{Z}$, $1 \le M \le 12$ and $1 \le D \le \ell(Y, M)$, the length of month $M$ in year $Y$. Let $\operatorname{succ}$ be the map that sends each date to the next day. Then:

1. JDN-FROM-DATE (lines L1 to L4) satisfies $J(\operatorname{succ}(Y, M, D)) = J(Y, M, D) + 1$ for each date, and $J(-4713, 11, 24) = 0$. So it numbers the days consecutively, with day $0$ on 24 November $-4713$, and it is a bijection from $\mathcal{G}$ to $\mathbb{Z}$.
2. DATE-FROM-JDN (lines L5 to L14) returns, for each integer $J$, the date in $\mathcal{G}$ whose number is $J$.

Throughout, $\lfloor \cdot \rfloor$ is floor division, defined for all integers.

**A floor lemma.** For integers $x$, $a$ and $q \ge 1$: $\lfloor x/q \rfloor \le a \iff x \le qa + q - 1$. Indeed $\lfloor x/q \rfloor \le a \iff x/q < a + 1 \iff x < q(a + 1) \iff x \le qa + q - 1$. Consequently, for an integer $p \ge 1$ and an integer $t$, the largest integer $b$ with $\lfloor pb/q \rfloor \le t$ is $\lfloor (qt + q - 1)/p \rfloor$, because $\lfloor pb/q \rfloor \le t \iff pb \le qt + q - 1 \iff b \le (qt + q - 1)/p$.

**March-based coordinates.** For a date $(Y, M, D)$, lines L1 to L3 compute $a = \lfloor (14 - M)/12 \rfloor$, which is $1$ for $M \in \{1, 2\}$ and $0$ for $3 \le M \le 12$; then $y = Y + 4800 - a$ and $m = M + 12a - 3$, so $m = M - 3 \in \{0, \ldots, 9\}$ for March to December and $m = M + 9 \in \{10, 11\}$ for January and February. The map $(Y, M) \mapsto (y, m)$ is a bijection from $\mathbb{Z} \times \{1, \ldots, 12\}$ to $\mathbb{Z} \times \{0, \ldots, 11\}$, with inverse $M = m + 3 - 12\lfloor m/10 \rfloor$ and $Y = y - 4800 + \lfloor m/10 \rfloor$, since $\lfloor m/10 \rfloor = a$. Call the twelve months with the same $y$ the *March-year* $y$; it runs from 1 March of civil year $y - 4800$ to the last day of February of civil year $y - 4799$.

**Month offsets.** Let $f(m) = \lfloor (153m + 2)/5 \rfloor$. Direct evaluation gives $f(0), \ldots, f(11) = 0, 31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337$, and $f(12) = 367$. The differences $f(m + 1) - f(m)$ for $m = 0, \ldots, 10$ are $31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31$, the lengths of March to January. So $f(m)$ is the number of days from 1 March to the first day of month $m$ of the same March-year, for $0 \le m \le 11$.

**Year lengths.** The March-year $y$ ends with February of civil year $y - 4799$, so it has $366$ days if that year is a leap year and $365$ otherwise. Since $4800 = 12 \cdot 400$, the civil year $y - 4799$ satisfies the leap rule (divisible by $4$, and not by $100$ unless by $400$) if and only if $y + 1$ does. Let $\chi(z) = 1$ if $z$ satisfies the leap rule and $0$ otherwise. Let $L(y) = \lfloor y/4 \rfloor - \lfloor y/100 \rfloor + \lfloor y/400 \rfloor$. For each $q \ge 1$, $\lfloor z/q \rfloor - \lfloor (z-1)/q \rfloor$ is $1$ if $q \mid z$ and $0$ otherwise. So $L(z) - L(z - 1) = [4 \mid z] - [100 \mid z] + [400 \mid z] = \chi(z)$, by cases on the divisibility of $z$. Let $N(y) = 365y + L(y)$. Then for every integer $y$,

$$N(y + 1) - N(y) = 365 + \chi(y + 1) = \text{the length of March-year } y.$$

So $N(y)$ is the number of days from 1 March of March-year $0$ to 1 March of March-year $y$ (negative for $y < 0$), with $N(0) = 0$.

**Part 1.** Line L4 returns $J = D - 1 + f(m) + N(y) - 32044$. By the last two paragraphs, $D - 1 + f(m) + N(y)$ is the number of days from 1 March of March-year $0$ (1 March $-4800$) to the given date. Each step to the next day raises this count by one: within a month $D$ grows by one; from the last day of month $m < 11$ to the first of month $m + 1$, the term $D - 1 + f(m)$ goes from $f(m + 1) - f(m) - 1 + f(m)$ to $f(m + 1)$; from the last day of month $11$ (which has $N(y + 1) - N(y) - f(11)$ days) to 1 March of year $y + 1$ the count goes from $N(y + 1) - 1$ to $N(y + 1)$. So $J(\operatorname{succ}(x)) = J(x) + 1$. For 24 November $-4713$: $a = 0$, $y = 87$, $m = 8$, and $J = 24 + 245 + 31755 + 21 - 0 + 0 - 32045 = 0$. A map from $\mathcal{G}$ to $\mathbb{Z}$ that sends one date to $0$ and each successor to the next integer is a bijection, since $\operatorname{succ}$ is a bijection of $\mathcal{G}$ and every date is reached from 24 November $-4713$ by a finite number of steps forward or backward.

**Part 2.** Let $J$ be an integer and let $(Y^*, M^*, D^*)$ be its date from Part 1, with March-based coordinates $(y^*, m^*)$ and $e^* = D^* - 1 + f(m^*)$, so that $a = J + 32044 = N(y^*) + e^*$ by Part 1 and line L5, with $0 \le e^* < N(y^* + 1) - N(y^*)$.

*Centuries (lines L6 and L7).* For an integer $b$, $N(100b) = 36500b + 25b - b + \lfloor b/4 \rfloor = 36524b + \lfloor b/4 \rfloor = \lfloor 146097b/4 \rfloor$. The function $N$ is strictly increasing, so the largest $b$ with $N(100b) \le a$ is the one with $100b \le y^* < 100(b + 1)$, that is, $b = \lfloor y^*/100 \rfloor$. By the floor lemma with $p = 146097$ and $q = 4$, this $b$ is $\lfloor (4a + 3)/146097 \rfloor$, which is line L6. Line L7 sets $c = a - N(100b)$, the number of days from the start of March-year $100b$ to the date, so $c \ge 0$.

*Years (lines L8 and L9).* Let $d^* = y^* - 100b$, so $0 \le d^* \le 99$. For $0 \le d \le 99$, the March-years $100b, \ldots, 100b + d - 1$ have leap days exactly when $\chi(z) = 1$ for $z = 100b + 1, \ldots, 100b + d$. None of these $z$ is a multiple of $100$, so $\chi(z) = [4 \mid z]$, and their number is $\lfloor d/4 \rfloor$ because $100b$ is a multiple of $4$. Hence $N(100b + d) - N(100b) = 365d + \lfloor d/4 \rfloor = \lfloor 1461d/4 \rfloor$ for $0 \le d \le 99$. Let $g(d) = \lfloor 1461d/4 \rfloor$; it is strictly increasing in $d$. We have $g(d^*) \le c$, and we claim $c < g(d^* + 1)$. If $d^* \le 98$, then $g(d^* + 1) = N(y^* + 1) - N(100b) > c$. If $d^* = 99$, then $c < N(100b + 100) - N(100b) \le 36525 = g(100)$. So $d^*$ is the largest $d$ with $g(d) \le c$, and by the floor lemma with $p = 1461$ and $q = 4$, it equals $\lfloor (4c + 3)/1461 \rfloor$, which is line L8. Line L9 gives $e = c - g(d^*) = a - N(y^*) = e^*$.

*Months (lines L10 and L11).* Here $0 \le e^* \le 365$, and $f(m^*) \le e^* < f(m^* + 1)$ for $m^* \le 10$, while for $m^* = 11$, $f(11) = 337 \le e^* \le 365 < 367 = f(12)$. Since $f$ is strictly increasing, $m^*$ is the largest $m$ with $f(m) \le e^*$. By the floor lemma with $p = 153$, $q = 5$ and the offset $+2$ (that is, $f(m) \le e \iff 153m + 2 \le 5e + 4 \iff m \le (5e + 2)/153$), it is $\lfloor (5e^* + 2)/153 \rfloor$, which is line L10. Line L11 gives $D = e^* - f(m^*) + 1 = D^*$.

*Back to the civil year (lines L12 and L13).* With $y^* = 100b + d^*$, lines L12 and L13 apply the inverse of the March-based coordinates, so they return $M^*$ and $Y^* = y^* - 4800 + \lfloor m^*/10 \rfloor$.

So DATE-FROM-JDN$(J) = (Y^*, M^*, D^*)$ for every integer $J$, and the two procedures are inverse bijections between $\mathcal{G}$ and $\mathbb{Z}$.

**The Julian calendar block.** The same argument holds with $\chi(z) = [4 \mid z]$, $L(y) = \lfloor y/4 \rfloor$ and $N(y) = 365y + \lfloor y/4 \rfloor = \lfloor 1461y/4 \rfloor$, without the century step. The constant $-32083$ makes 1 January $-4712$ day $0$: $a = 1$, $y = 87$, $m = 10$ and $1 + 306 + 31755 + 21 - 32083 = 0$. In the inverse, $c = J + 32082$ is the count from 1 March $-4800$ of the Julian calendar, and $d = \lfloor (4c + 3)/1461 \rfloor$ is the March-year, by the floor lemma. $\blacksquare$
