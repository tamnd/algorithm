---
title: BBHT search returns only marked items and makes O(sqrt(N/M)) expected Grover iterations
proves: [correctness]
status: full
---

We use the pseudocode of the page, with $\lambda \in (1, 4/3)$. The search space is $\{0, 1, \ldots, N-1\}$, the set of marked items is $S$ with $|S| = t$, and $\theta \in [0, \pi/2]$ is the angle with $\sin^2\theta = t/N$. The rounds are numbered $r = 1, 2, \ldots$. In round $r$ the value of $m$ is $m_r$, with $m_1 = 1$ and $m_{r+1} = \min(\lambda m_r, \sqrt{N})$, and $c_r$ is the number of integers $j$ with $0 \le j < m_r$, so $c_r = \lceil m_r \rceil$.

**Claim 1 (no wrong answer).** BBHT-SEARCH returns $x$ only in line L6, after the classical check $f(x) = 1$. So each returned item is marked. If $t = 0$, the check never passes, and the run ends in line L8.

**Claim 2 (one round).** Fix $c \ge 1$, and let $j$ be uniform on $\{0, 1, \ldots, c-1\}$. The probability $P_c$ that line L5 gives a marked item is

$$P_c = \frac{1}{2} - \frac{\sin(4c\theta)}{4c\sin(2\theta)} \quad (0 < \theta < \pi/2),$$

and $P_c \ge 1/4$ when $c \ge 1/\sin(2\theta)$.

*Proof.* By the correctness of Grover's search, after $j$ iterations from $|s\rangle$ the measurement gives a marked item with probability $\sin^2((2j+1)\theta)$. So

$$P_c = \frac{1}{c}\sum_{j=0}^{c-1}\sin^2((2j+1)\theta) = \frac{1}{2} - \frac{1}{2c}\sum_{j=0}^{c-1}\cos((2j+1)a), \qquad a = 2\theta.$$

For $0 < a < \pi$, $\sin a > 0$, and $2\sin a\cos((2j+1)a) = \sin((2j+2)a) - \sin(2ja)$. The sum telescopes: $2\sin a\sum_{j=0}^{c-1}\cos((2j+1)a) = \sin(2ca)$. So the sum is $\sin(4c\theta)/(2\sin 2\theta)$, and the formula follows. If $c \ge 1/\sin(2\theta)$, then $|\sin(4c\theta)|/(4c\sin 2\theta) \le 1/(4c\sin 2\theta) \le 1/4$, so $P_c \ge 1/4$. $\square$

**Claim 3 (expected work).** Let $1 \le t \le 3N/4$, let the budget be infinite, and let $m_0 = 1/\sin(2\theta)$. Then the expected total number of Grover iterations is less than

$$\frac{m_0}{2}\left(\frac{\lambda}{\lambda - 1} + \frac{\lambda}{1 - 3\lambda/4}\right),$$

which is $9 m_0$ for $\lambda = 6/5$. Also $m_0 \le \sqrt{N/t}$, so the expectation is $O(\sqrt{N/t})$.

*Proof.* Since $t \le 3N/4$, $\cos^2\theta \ge 1/4$, so $\sin 2\theta = 2\sin\theta\cos\theta \ge \sin\theta = \sqrt{t/N}$, and $m_0 \le \sqrt{N/t} \le \sqrt{N}$. Also $m_0 \ge 1$.

Each round draws a fresh $j$ and prepares a fresh state. So, given that round $r$ is reached, it makes $j_r$ iterations with $\mathbb{E}[j_r] = (c_r - 1)/2 < m_r/2$, and it succeeds with probability $P_{c_r}$, no matter what happened before.

The sequence $m_r$ grows until it reaches $\sqrt{N} \ge m_0$, and then stays there. So there is a first round $s$ with $c_s \ge m_0$. For $r < s$, $m_r \le c_r < m_0 \le \sqrt{N}$, so the cap was not used and $m_r = \lambda^{r-1}$.

*Rounds before $s$.* Their iterations, in expectation, are less than

$$\frac{1}{2}\sum_{r=1}^{s-1}\lambda^{r-1} < \frac{1}{2}\cdot\frac{\lambda^{s-1}}{\lambda - 1} = \frac{1}{2}\cdot\frac{\lambda\, m_{s-1}}{\lambda - 1} < \frac{1}{2}\cdot\frac{\lambda\, m_0}{\lambda - 1}$$

(the sum is empty when $s = 1$).

*Rounds from $s$ on.* The $c_r$ do not decrease, so $c_{s+u} \ge m_0$ for each $u \ge 0$, and by Claim 2 each of these rounds succeeds with probability at least $1/4$. So round $s + u$ is reached with probability at most $(3/4)^u$. Also $m_{s+u} \le \lambda^u m_s$, and $m_s \le \lambda m_0$: if $s = 1$, $m_s = 1 \le m_0$; if $s \ge 2$, $m_s \le \lambda m_{s-1} < \lambda m_0$. So the expected iterations from round $s$ on are less than

$$\sum_{u \ge 0}\left(\frac{3}{4}\right)^u \frac{\lambda^u \lambda m_0}{2} = \frac{\lambda m_0}{2}\cdot\frac{1}{1 - 3\lambda/4},$$

and the series converges because $\lambda < 4/3$. Add the two parts. For $\lambda = 6/5$: $\lambda/(\lambda - 1) = 6$ and $\lambda/(1 - 3\lambda/4) = 12$, so the total is less than $9 m_0$. $\square$

**Claim 4 (rounds).** Under the conditions of Claim 3, the expected number of rounds, and so of classical checks, is less than $\log_\lambda m_0 + 5$.

*Proof.* There are $s - 1$ rounds before $s$, and $\lambda^{s-2} = m_{s-1} < m_0$ when $s \ge 2$, so $s - 1 < \log_\lambda m_0 + 1$. From round $s$ on, the expected number of rounds is at most $\sum_{u \ge 0}(3/4)^u = 4$. $\square$

**Claim 5 (the budget).** With a budget $B$ in line L2:

- if $t = 0$, the run returns NO SOLUTION after fewer than $B + \sqrt{N}$ iterations;
- if $1 \le t \le 3N/4$, it returns NO SOLUTION with probability less than $9\sqrt{N/t}/B$. For $B = 18\sqrt{N}$ this is less than $1/2$.

*Proof.* Line L2 lets a round start only when the iterations so far are below $B$, and one round makes $j < m \le \sqrt{N}$ iterations. If $t = 0$, no round succeeds (Claim 1), so the run stops when the count reaches $B$, after fewer than $B + \sqrt{N}$ iterations. If $t \ge 1$, the run returns NO SOLUTION only if the run without a budget would make at least $B$ iterations before its success. By Markov's inequality and Claim 3, this has probability at most $9 m_0/B \le 9\sqrt{N/t}/B$. $\square$

**The case $t > 3N/4$.** Round 1 has $m_1 = 1$, so $j = 0$: line L5 measures $|s\rangle$, which is a uniform classical sample, and it succeeds with probability $t/N > 3/4$. So the run ends in round 1 with probability above $3/4$. Every later round succeeds with probability $P_c \ge (1/c)\sin^2\theta > 0$, from the term $j = 0$ alone, with $c \le \lceil\sqrt{N}\rceil$. So the run ends with probability 1, and the expected number of rounds is at most $\lceil\sqrt{N}\rceil N/t$, a bound that the exact values are far below. $\blacksquare$
