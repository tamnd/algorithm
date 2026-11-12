---
title: C-SCAN serves each request once, bounds the wait by one cycle, and gives each cylinder the same mean wait
proves: [correctness]
status: full
---

We use the pseudocode of the page with the service direction $+1$; the case $-1$ is the mirror image. Cylinders are $0, \ldots, C - 1$ with $C \ge 2$.

**Claim 1 (static batch).** C-SCAN returns a permutation of $R$, and the order goes down at most once, at the wrap from `ahead` to `behind`. If no request is below $r$, the cost is $\max R - r$. Otherwise, with $b$ the largest request below $r$, the cost is $(C - 1 - r) + (C - 1) + b$ with the return counted, and $(C - 1 - r) + b$ without it.

*Proof.* Lines L1 and L2 put each request in exactly one list, by the test $x \ge r$, and line L5 returns both. Each list is in increasing order, so the order can go down only from the last element of `ahead` to the first element of `behind`. If `behind` is empty, the path rises from $r$ to $\max R$, with length $\max R - r$. Otherwise the path of line L4 rises from $r$ through `ahead` to $C - 1$, which is at least each request, so this part has length $C - 1 - r$. The return from $C - 1$ to 0 has length $C - 1$. The last part rises from 0 through `behind`, which ends at $b$, so it has length $b$. Without the return, the two rising parts remain. $\square$

On the textbook queue with the head at 53 and $C = 200$, this gives $146 + 199 + 37 = 382$, or 183, serving toward 199; and, by the mirror formula, $53 + 199 + 134 = 386$, or 187, serving toward 0.

For the dynamic model we use the clock of the implementation. At each tick, the requests that have arrived join the pending set. If a request is pending at the head cylinder, all pending requests there finish at this tick (service time 0). Otherwise, if some request is pending, the head moves up one cylinder in one tick, or, at cylinder $C - 1$, jumps to cylinder 0 in $J$ ticks. During the jump nothing is served; requests that arrive during it join the pending set when it ends. If no request is pending, the head stays. Let $L = (C - 1) + J$, the length of one cycle.

**Claim 2 (wait bound).** Let $J \ge 1$. With service time 0, each request waits at most $L - 1 = (C - 1) + J - 1$ ticks. For $J = 0$ the bound is $C - 1$.

*Proof.* Let request $q$ at cylinder $x$ arrive at tick $a$. While $q$ is pending, the head never stays, so from tick $a$ on it moves up one cylinder per tick and jumps from $C - 1$ to 0, until it reaches $x$, where $q$ finishes. There are three cases.

- The arrival falls inside a jump that starts at tick $t_0$, so $t_0 < a < t_0 + J$. The head is at 0 at tick $t_0 + J$ and reaches $x$ after $x$ more ticks. The wait is $(t_0 + J - a) + x \le (J - 1) + (C - 1)$.
- The head is at $p \le x$ at tick $a$. The wait is $x - p \le C - 1 \le (C - 1) + J - 1$.
- The head is at $p > x$ at tick $a$. It needs $C - 1 - p$ ticks up to $C - 1$, then $J$ ticks for the jump, then $x$ ticks up to $x$. Since $p \ge x + 1$, the wait is at most $(C - 2 - x) + J + x = (C - 1) + J - 1$.

For $J = 0$, the first case does not occur, the second gives at most $C - 1$, and the third at most $C - 2$. $\square$

The bound does not depend on the other requests, so no stream of requests can starve $q$. With $J = C - 1$ it is $2(C - 1) - 1$, the bound of SCAN. The tests check the weaker bound $(C - 1) + J$ on random streams for $J = C - 1$, $J = 10$ and $J = 0$.

**Claim 3 (the same mean wait on each cylinder).** Let $J \ge 1$, let the head start at cylinder 0 at tick 0, and let one request arrive at each cylinder at each tick. Then for each cylinder $x$, the waits of the requests at $x$ that arrive in any $L$ consecutive ticks are exactly $0, 1, \ldots, L - 1$, and their mean is $(L - 1)/2$.

*Proof.* Requests are always pending, so the head never stays. It is at cylinder $x$ at tick $x$, reaches $C - 1$ at tick $C - 1$, and is back at 0 at tick $(C - 1) + J = L$. So the motion is periodic with period $L$, and the head is at $x$ exactly at the ticks $x + kL$ for $k = 0, 1, 2, \ldots$; since $J \ge 1$, it is at no cylinder twice in one cycle. A request at $x$ that arrives at tick $a$ finishes at the first visit at or after $a$. The arrivals at ticks $x + (k - 1)L + 1, \ldots, x + kL$ therefore wait $L - 1, L - 2, \ldots, 0$. Any $L$ consecutive ticks contain one tick of each residue modulo $L$, so their waits are $0, 1, \ldots, L - 1$ in some order, with sum $L(L - 1)/2$. $\square$

The value does not depend on $x$. Under SCAN, by contrast, the mean at cylinder $x$ is $(x^2 + (C - 1 - x)^2)/(C - 1) - 1/2$, which is $C - 1.5$ at the edges and about $(C - 1)/2$ in the middle. With $J = C - 1$ the C-SCAN mean is $C - 1.5$ on every cylinder. With a small $J$ it is about $C/2$. The tests check Claim 3 exactly for $C = 20$, with $J = C - 1$ and with $J = 3$.
