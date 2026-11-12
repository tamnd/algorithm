---
title: Capped exponential backoff bounds the retry rate, and jitter is needed to separate clients
proves: [correctness]
status: full
---

**Setting.** After failure $n = 0, 1, 2, \ldots$ the client computes $v_n = \min(\mathit{cap}, \mathit{base} \cdot 2^n)$ (line L4) and waits $d_n$: $d_n = v_n$ without jitter (line L5), $d_n$ uniform in $[0, v_n]$ with full jitter (line L6), and $d_n = v_n/2 + $ uniform in $[0, v_n/2]$ with equal jitter (line L7). With $0 < \mathit{base} \le \mathit{cap}$, let $c$ be the first $n$ with $\mathit{base} \cdot 2^n \ge \mathit{cap}$.

**Claim 1 (the total wait without jitter).** For $n \le c$, the wait before attempt $n$ (counting from 0) is $\sum_{i=0}^{n-1} \mathit{base} \cdot 2^i = \mathit{base}(2^n - 1)$. After that, each wait is $\mathit{cap}$.

*Proof.* For $i < c$, $v_i = \mathit{base} \cdot 2^i$, and the sum is a [geometric series](/geometric-series/). For $i \ge c$, $v_i = \mathit{cap}$. $\square$

**Claim 2 (few attempts in a time span).** Without jitter, the number of attempts in the first $T$ time units, for $T \le \mathit{base}(2^c - 1)$, is at most $\lfloor \log_2 (T/\mathit{base} + 1) \rfloor + 1$. With a cap, at most $c + 1 + T/\mathit{cap}$ attempts happen in time $T$. With full jitter the expected wait after failure $n$ is $v_n/2$, and with equal jitter it is $3v_n/4$, so the same bounds hold in expectation up to a constant factor.

*Proof.* Attempt $n$ happens at time $\mathit{base}(2^n - 1)$ by Claim 1. It is at most $T$ if and only if $2^n \le T/\mathit{base} + 1$. After the cap, the attempts are $\mathit{cap}$ apart. The expected values of the uniform distributions are the middles of their ranges. $\square$

So a client that fails over and over loads the server with a rate that falls exponentially, until the cap, and then with a rate of one attempt per $\mathit{cap}$.

**Claim 3 (without jitter, synchronized clients stay synchronized).** Let $k \ge 2$ clients run the policy without jitter, start at the same time, and fail together whenever two or more of them try at the same time. Then they collide at every attempt.

*Proof.* Induction on the attempt number. All clients make attempt 0 at time 0, so they collide. If they all made attempt $n$ at the same time and collided, each of them waits the same $d_n = v_n$, which depends only on $n$, $\mathit{base}$ and $\mathit{cap}$. So they all make attempt $n + 1$ at the same time and collide again. $\square$

In the slotted test, 20 clients without jitter make $20 \times 30 = 600$ attempts and none succeeds.

**Claim 4 (with full jitter, two clients separate quickly).** In the slotted model, a client that waits $d$ tries again in slot $\lfloor \mathit{now} + d \rfloor + 1$. Let two clients collide in slot $t$ after their $n$-th failures, and draw independent full-jitter delays $X, Y$ uniform in $[0, v]$ with $v = v_n$. The probability that they try in the same slot again is at most $1/v$.

*Proof.* The slots cut $[0, v]$ into intervals $I_1, I_2, \ldots$ of lengths $\ell_j \le 1$ with $\sum_j \ell_j = v$. The clients meet again if and only if $X$ and $Y$ fall in the same interval, which has probability $\sum_j (\ell_j/v)^2 \le \frac{1}{v} \sum_j \ell_j / v = 1/v$. $\square$

So the probability that two clients collide $n$ times in a row after their first collision is at most $\prod_{i=1}^{n} 1/v_i$, which falls faster than any exponential while $v_i$ doubles. With equal jitter, the same argument over $[v/2, v]$ gives at most $2/v$. $\blacksquare$
