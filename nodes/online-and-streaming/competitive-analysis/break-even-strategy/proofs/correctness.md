---
title: The break-even strategy pays less than twice the optimum, and no deterministic rule does better
proves: [correctness]
status: full
---

We use rent $r > 0$ per day, price $p > 0$, and $m = \lceil p/r \rceil$. A season has $n \ge 1$ days, and $\mathrm{OPT}(n) = \min(n r, p)$.

**Lemma 1 (the buy day).** BREAK-EVEN buys on day $m$ if the season lasts $m$ days or more, and never buys on a shorter season.

*Proof.* Line L1 sets $\mathrm{paid} = 0$. While $\mathrm{owned}$ is false, each day that line L5 runs adds $r$ to $\mathrm{paid}$, and no other line changes it. So at the start of day $d$, before any purchase, $\mathrm{paid} = (d - 1) r$. Line L4 buys on day $d$ exactly when $(d - 1) r + r \ge p$, that is $d \ge p/r$. The first such day is $d = m$. On the days after the purchase, line L3 runs, which costs nothing. $\square$

**Theorem 1 (upper bound).** For every $n \ge 1$, $\mathrm{ALG}(n) \le \left(1 + \frac{(m - 1) r}{p}\right) \mathrm{OPT}(n)$, with equality for $n = m$. The factor is less than 2, and it equals $2 - r/p$ when $p/r$ is an integer.

*Proof.* By Lemma 1 there are two cases.

- If $n < m$, the rule rents on all $n$ days and pays $n r$. Since $n \le m - 1 < p/r$, we have $n r < p$, so $\mathrm{OPT}(n) = n r = \mathrm{ALG}(n)$.
- If $n \ge m$, the rule rents on days $1, \ldots, m - 1$ and buys on day $m$, so $\mathrm{ALG}(n) = (m - 1) r + p$. Since $n r \ge m r \ge p$, $\mathrm{OPT}(n) = p$. So $\mathrm{ALG}(n)/\mathrm{OPT}(n) = 1 + (m - 1) r / p$.

In both cases the bound holds, and for $n = m$ it is an equality. Since $m - 1 < p/r$, $(m - 1) r < p$, so the factor is less than 2. If $p/r$ is an integer, $m = p/r$ and the factor is $1 + (p - r)/p = 2 - r/p$. $\square$

**Theorem 2 (lower bound).** Let $r = 1$ and $p = B$ with $B \ge 1$ an integer. For every deterministic online rule there is a season $n$ with $\mathrm{ALG}(n) \ge (2 - 1/B) \cdot \mathrm{OPT}(n)$. For $B \ge 2$, equality for the worst season holds only for the rule that buys on day $B$.

*Proof.* A deterministic rule sees only the number of days so far, so it is described by the day $j \in \{1, 2, \ldots\} \cup \{\infty\}$ on which it buys. If $j = \infty$, the season of $n$ days costs $n$ and $\mathrm{OPT}(n) = B$ for $n \ge B$, so the ratio $n/B$ is unbounded. Otherwise let the season end on day $n = j$, so the rule pays $j - 1 + B$.

- If $j \le B$, then $\mathrm{OPT}(j) = j$ and the ratio is $1 + (B - 1)/j \ge 1 + (B - 1)/B = 2 - 1/B$, with equality only for $j = B$ when $B \ge 2$.
- If $j > B$, then $\mathrm{OPT}(j) = B$ and the ratio is $(j - 1 + B)/B \ge 2B/B = 2 > 2 - 1/B$. $\square$

**Corollary.** BREAK-EVEN with $r = 1$ and $p = B$ is strictly $(2 - 1/B)$-competitive, and this is the best ratio of any deterministic online algorithm for ski rental. $\blacksquare$
