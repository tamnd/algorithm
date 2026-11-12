---
title: LOOK started toward the nearer end is optimal on a static batch, and its wait is less than two sweeps
proves: [correctness]
status: full
---

We use the pseudocode of the page. $R$ is a nonempty multiset of requests with $lo = \min R$ and $hi = \max R$, the head is at $r$, and $M$ is the total head movement of an order. The case $R = \emptyset$ is trivial: the order is empty and costs 0.

**Claim 1 (static cost).** LOOK returns a permutation of $R$, its path changes direction at most once, and with $d = +1$ its cost is

- $hi - r$ if $lo \ge r$,
- $r - lo$ if $hi < r$,
- $(hi - r) + (hi - lo)$ if $lo < r \le hi$.

With $d = -1$, the mirror image: $r - lo$ if $hi \le r$, $hi - r$ if $lo > r$, and $(r - lo) + (hi - lo)$ if $lo \le r < hi$.

*Proof.* Lines L1 and L2 put each request in exactly one list, and line L3 returns both. With $d = +1$ the path is $r$, then `ahead` in increasing order, all at least $r$, then `behind` in decreasing order, all less than $r$. So it never goes down and then never goes up. A monotone path has length equal to the distance between its ends. If $lo \ge r$, `behind` is empty and the path rises from $r$ to $hi$. If $hi < r$, `ahead` is empty and the path falls from $r$ to $lo$. Otherwise both lists are nonempty, the path rises from $r$ to $hi$ and falls from $hi$ to $lo$. The case $d = -1$ is the mirror image. $\square$

**Claim 2 (optimality).** If $d = -1$ when $r - lo \le hi - r$, and $d = +1$ otherwise, then the LOOK order has the least total head movement over all orders of $R$:

$$M_{\mathrm{LOOK}} = M_{\min} = (hi - lo) + \min(|r - lo|, |r - hi|).$$

*Proof.* First we show $M_{\mathrm{LOOK}} = M_{\min}$, by the cases of Claim 1.

- $d = -1$, so $r - lo \le hi - r$. If $hi \le r$, then $hi - r \le 0$ forces $r - lo \le 0$, so $lo = hi = r$ and both sides are 0. If $lo > r$, LOOK costs $hi - r = (hi - lo) + (lo - r)$, and $|r - lo| = lo - r < hi - r = |r - hi|$. If $lo \le r < hi$, LOOK costs $(r - lo) + (hi - lo)$, and $r - lo \le hi - r$ means that $|r - lo|$ is the minimum.
- $d = +1$, so $r - lo > hi - r$. If $lo \ge r$, then $r - lo \le 0$ and $hi - r \ge 0$, a contradiction; this case does not occur. If $hi < r$, LOOK costs $r - lo = (hi - lo) + (r - hi)$, and $|r - hi| = r - hi < r - lo = |r - lo|$. If $lo < r \le hi$, LOOK costs $(hi - r) + (hi - lo)$, and $hi - r < r - lo$ means that $|r - hi|$ is the minimum.

The lower bound is the theorem on the [disk scheduling](/disk-scheduling/) page. In short: in any order, let $i$ be the first step at which the head reaches $lo$ and $j$ the first step at which it reaches $hi$. If $i < j$, the [triangle inequality](/triangle-inequality/) on the line gives at least $|r - lo|$ cylinders up to step $i$ and at least $hi - lo$ from step $i$ to step $j$; if $j < i$, at least $|r - hi| + (hi - lo)$; if $lo = hi$, at least $|r - lo|$. So every order costs at least $M_{\min}$. $\square$

The test code checks Claim 2 against a search over all orders on random batches of up to 7 requests.

**Claim 3 (the other direction).** Started toward the farther end, LOOK costs at most $2 M_{\min}$.

*Proof.* If $r$ lies outside $[lo, hi]$, Claim 1 shows that LOOK goes straight across the range in either direction, and its cost is $M_{\min}$. If $lo \le r \le hi$, its cost is at most $(hi - lo) + \max(r - lo, hi - r) \le 2(hi - lo) \le 2 M_{\min}$. $\square$

**Claim 4 (wait bound).** In the dynamic model with service time 0, one cylinder per tick, and $C \ge 2$ cylinders, each request waits at most $2(C - 1) - 1$ ticks.

*Proof.* The clock is that of the implementation: at each tick the arrivals join the pending set; if a request is pending at the head cylinder, all requests there finish at this tick; otherwise, if some request is pending, the head reverses when no pending request lies strictly ahead and then moves one cylinder. Let request $q$ at cylinder $x$ arrive at tick $a$, with the head at $p$ and direction $d$ after the arrivals of tick $a$. If $p = x$, the wait is 0. Otherwise the head moves one cylinder at each tick until it reaches $x$, since $q$ is pending.

If $x$ is ahead, that is $(x - p) d > 0$, then a pending request lies ahead at each tick until the head reaches $x$, so the head does not reverse, and the wait is $|x - p| \le C - 1$.

If $x$ is behind, let $d = +1$; the other case is the mirror image. Then $x < p$, so $x \le p - 1$. The head goes up to some cylinder $p' \le C - 1$, reverses there, since no request can lie above $C - 1$, and then $q$ is ahead, so the head goes down to $x$ without another reversal. The wait is $(p' - p) + (p' - x) \le (C - 1 - p) + (C - 1 - x) \le (C - 1 - (x + 1)) + (C - 1 - x) = 2(C - 1) - 1 - 2x \le 2(C - 1) - 1$. $\square$

The tests check the bound on random streams, and a lone request at cylinder 0, with the head at 100 going up, is served after exactly 100 ticks.
