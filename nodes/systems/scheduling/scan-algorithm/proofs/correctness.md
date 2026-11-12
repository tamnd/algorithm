---
title: SCAN serves each request once, and with no service time each request waits less than two sweeps
proves: [correctness]
status: full
---

We use the pseudocode of the page with the start direction $+1$; the case $-1$ is the mirror image. Cylinders are $0, \ldots, C - 1$ with $C \ge 2$.

**Claim 1 (static batch).** SCAN returns a permutation of $R$. Its head path changes direction at most once. Its cost is $\max R - r$ if no request is below $r$, and $(C - 1 - r) + (C - 1 - \min R)$ otherwise.

*Proof.* Lines L1 and L2 put each request in exactly one of the two lists, by the test $x \ge r$, and line L5 returns both lists. The path of line L4 is $r$, then `ahead` in increasing order, all at least $r$, then possibly $C - 1$, which is at least each request, then `behind` in decreasing order. So the path first never goes down and then never goes up: it changes direction at most once. A path that only goes up has length equal to its rise, and one that only goes down has length equal to its drop. If `behind` is empty, the path rises from $r$ to $\max R$, or has length 0 when $R$ is empty. Otherwise it rises from $r$ to $C - 1$ and drops from $C - 1$ to the last element of `behind`, which is $\min R$. $\square$

For the dynamic model we use the clock of the implementation. Time is an integer. At each tick, the requests that have arrived join the pending set. If a request is pending at the head cylinder, all pending requests there finish at this tick (service time 0). Otherwise, if some request is pending, the head moves one cylinder in its direction $d$ and the tick ends; before the move, $d$ flips if the head is at $C - 1$ with $d = +1$ or at 0 with $d = -1$. If no request is pending, the head stays.

**The walk.** While some request is pending, the head follows the *bouncing walk*: from state $(p, d)$ it goes to $(p + d, d)$, except at an end, where it first flips $d$. Let $T(p, d, x)$ be the number of ticks this walk needs to reach cylinder $x$ from $(p, d)$, with $p \ne x$. By the rule,

- if $d = +1$ and $x > p$, then $T = x - p$;
- if $d = +1$ and $x < p$, then $T = (C - 1 - p) + (C - 1 - x)$;

and the cases with $d = -1$ are the mirror images.

**Claim 2 (wait bound).** With service time 0, each request waits at most $2(C - 1) - 1$ ticks, and this bound is reached.

*Proof.* Let request $q$ at cylinder $x$ arrive at tick $a$, with the head at $(p, d)$ after the arrivals of tick $a$. If $p = x$, $q$ finishes at tick $a$. Otherwise $q$ is pending from tick $a$ on, so the head follows the bouncing walk one cylinder per tick until it reaches $x$, and $q$ finishes at the tick when it does. So the wait is $T(p, d, x)$. In the first case, $T \le C - 1$. In the second case, $p \ge x + 1$ gives $T \le (C - 2 - x) + (C - 1 - x) = 2(C - 1) - 1 - 2x \le 2(C - 1) - 1$. The mirror cases give the same bounds. Equality holds for $x = 0$, $p = 1$, $d = +1$: the head goes up to $C - 1$ and back down to 0. $\square$

The bound does not depend on the other requests, so no stream of new requests can starve $q$. The tests check the bound on random streams, and a request at cylinder 0 with the head at 100 going up waits $99 + 199 = 298$ ticks on a disk of 200 cylinders, for each length of a stream of requests at cylinder 100.

**Claim 3 (mean wait per cylinder in a steady sweep).** Let the head start at $(0, +1)$, and let one request arrive at each cylinder at each tick. Then, over the arrivals at cylinder $x$ in any $L = 2(C - 1)$ consecutive ticks, the mean wait is

$$\frac{x^2 + (C - 1 - x)^2}{C - 1} - \frac{1}{2}.$$

*Proof.* Requests are always pending, so the head follows the bouncing walk from $(0, +1)$, which is periodic with period $L$. In each period it is at cylinder $x$ once at the end of a stretch of $g_1 = 2x$ ticks and once at the end of a stretch of $g_2 = 2(C - 1 - x)$ ticks, with $g_1 + g_2 = L$. (At $x = 0$ and $x = C - 1$ one of the stretches has length 0: the head is there once per period.) A request that arrives at a tick of a stretch of length $g$, after the visit that opens it and up to the visit that closes it, waits $g - 1, g - 2, \ldots, 0$ ticks. So the sum of the waits over one period is $g_1(g_1 - 1)/2 + g_2(g_2 - 1)/2$, and since the walk is periodic, the same sum holds for any $L$ consecutive ticks. The mean is

$$\frac{g_1^2 + g_2^2 - L}{2L} = \frac{4x^2 + 4(C - 1 - x)^2 - 2(C - 1)}{4(C - 1)},$$

which is the claimed value. $\square$

At $x = 0$ the mean is $C - 1.5$. At the middle cylinder, $x = (C - 1)/2$ for odd $C$, it is $(C - 1)/2 - 1/2$. Since $\sum_{x=0}^{C-1} x^2 = (C - 1)C(2C - 1)/6$, the mean over all cylinders is $(2C - 1)/3 - 1/2$. The tests check the formula exactly, with fractions, for $C = 20$.

**Claim 4 (no bound with service time).** If each service takes $s \ge 1$ ticks, no bound on the wait holds.

*Proof.* Let the head be at 100 with $d = -1$ on a disk of 200 cylinders, let a request $q$ at cylinder 0 arrive at tick 0, and let one request arrive at cylinder 100 at each tick $0, 1, \ldots, k - 1$. At each tick $t < k$ the head is at 100 with a request pending there, so it serves that request, which takes $s$ ticks, and does not move. The head leaves 100 only at a tick $t \ge k$, so $q$ waits at least $k$ ticks. $\square$
