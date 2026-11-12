---
title: C-LOOK serves each request once, never moves more than C-SCAN, and its wait is less than three sweeps
proves: [correctness]
status: full
---

We use the pseudocode of the page with the service direction $+1$; the case $-1$ is the mirror image. Cylinders are $0, \ldots, C - 1$ with $C \ge 2$. Let $t$ be the last request in `ahead`, or $r$ if `ahead` is empty, and, when `behind` is not empty, let $lo$ and $b$ be its first and last elements.

**Claim 1 (static batch).** C-LOOK returns a permutation of $R$. If `behind` is empty its cost is $t - r$. Otherwise its cost is $(t - r) + (t - lo) + (b - lo)$ with the jump counted, and $(t - r) + (b - lo)$ without it.

*Proof.* Lines L1 and L2 put each request in exactly one list, by the test $x \ge r$, and line L3 returns both. The path is $r$, then `ahead` in increasing order up to $t$, then `behind` in increasing order from $lo$ to $b$. The part from $r$ to $t$ only goes up, so its length is $t - r$. The jump goes from $t$ to $lo$, and $lo < r \le t$, so its length is $t - lo$. The last part only goes up, from $lo$ to $b$. $\square$

On the textbook queue with the head at 53, toward 199: $t = 183$, $lo = 14$, $b = 37$, so the cost is $130 + 169 + 23 = 322$, or 153 without the jump. Toward 0, by the mirror formula, it is $39 + 169 + 118 = 326$, or 157.

**Claim 2 (no more than C-SCAN).** On the same batch, direction and convention, C-LOOK moves no more than [C-SCAN](/c-scan/).

*Proof.* If `behind` is empty, both cost $t - r$. Otherwise C-SCAN costs $(C - 1 - r) + (C - 1) + b$ with the return and $(C - 1 - r) + b$ without it. With the return, the difference is $(C - 1 - t) + (C - 1 - t + lo) + lo \ge 0$, since $t \le C - 1$ and $lo \ge 0$. Without it, the difference is $(C - 1 - t) + lo \ge 0$. $\square$

For the dynamic model we use the clock of the implementation. At each tick, the requests that have arrived join the pending set. If a request is pending at the head cylinder $p$, all pending requests there finish at this tick (service time 0). Otherwise, if some pending request lies above $p$, the head moves up one cylinder in one tick. Otherwise it picks the smallest pending cylinder $f$ and jumps there in $p - f$ ticks, serving nothing; requests that arrive during the jump join the pending set when it ends, and the target $f$ does not change. If no request is pending, the head stays.

Two facts follow. While a request $q$ at $x$ is pending, the head never stays. And if the head is at $p < x$ outside a jump, it reaches $x$ in exactly $x - p$ ticks, since $q$ lies above it at each tick before that, so no jump starts.

**Claim 3 (wait bound).** With service time 0 and a jump of one tick per cylinder, each request waits at most $3(C - 1) - 2$ ticks.

*Proof.* Let request $q$ at cylinder $x$ arrive at tick $a$.

*Case 1: the head is at $p$ at tick $a$, outside a jump.* If $p = x$, the wait is 0. If $p < x$, the wait is $x - p \le C - 1$. If $p > x$, the head goes up to some $p_1$ with $p \le p_1 \le C - 1$, jumps to the smallest pending cylinder $f \le x$, since $q$ is pending, and goes up from $f$ to $x$. The wait is $(p_1 - p) + (p_1 - f) + (x - f) \le (C - 1 - p) + (C - 1) + x$. With $p \ge x + 1$ this is at most $2(C - 1) - 1$.

*Case 2: the arrival falls inside a jump from $p_0$ to $f_0$ that starts at tick $s$,* so $s < a < s + (p_0 - f_0)$. The rest of the jump takes $s + (p_0 - f_0) - a \le p_0 - f_0 - 1$ ticks. Then the head is at $f_0$, outside a jump. If $x \ge f_0$, Case 1 with $p = f_0 \le x$ gives $x - f_0$ more ticks, and the wait is at most $(p_0 - f_0 - 1) + (x - f_0) \le 2(C - 1) - 1$. If $x < f_0$, then $f_0 \ge 1$, and Case 1 with $p = f_0 > x$ gives at most $(C - 1 - f_0) + (C - 1) + x$ more ticks. With $p_0 \le C - 1$ and $x \le f_0 - 1$, the wait is at most

$$(C - 2 - f_0) + (C - 1 - f_0) + (C - 1) + (f_0 - 1) = 3(C - 1) - 2 - f_0 \le 3(C - 1) - 3.$$

In all cases the wait is at most $3(C - 1) - 2$. $\square$

**Claim 4 (the bound of two sweeps fails).** There is a stream in which a request waits more than $2(C - 1)$ ticks.

*Proof.* Take $C = 200$, the head at 199, requests at 199 and 10 at tick 0, and requests at 5 and 198 at tick 1. At tick 0 the head serves 199. No request lies above it, so it jumps to 10, the smallest pending cylinder, during ticks 0 to 189, and serves 10 at tick 189. The requests at 5 and 198 joined at the end of the jump. The request at 198 lies above, so the head goes up and serves it at tick $189 + 188 = 377$. Then nothing lies above, so it jumps to 5 and serves it at tick $377 + 193 = 570$. The request at 5 waits $570 - 1 = 569 > 398 = 2(C - 1)$ ticks. $\square$

This is Case 2 with $x < f_0$: a request that arrives during a jump, below the landing cylinder, waits for the rest of the jump, one sweep and a second jump. The tests run this stream, and they find waits between $2(C - 1)$ and $3(C - 1)$ on random streams.
