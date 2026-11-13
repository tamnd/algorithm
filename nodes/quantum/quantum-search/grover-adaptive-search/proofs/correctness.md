---
title: Grover adaptive search keeps the best point, finds a minimum with the budget rule, and needs a patience that grows with N
proves: [correctness]
status: full
---

We use the pseudocode of the page with $\lambda = 6/5$. The cost function $f$ is defined on $N = 2^n$ points. Let $v_1 < v_2 < \cdots < v_K$ be its distinct values, let $n_k$ be the number of points with $f(x) = v_k$, and let $R_k = n_1 + \cdots + n_k$, so $R_K = N$. While the threshold is $y = v_k$, the marked points are the $x$ with $f(x) < y$, and there are $t = R_{k-1}$ of them. A *phase* is the time between two changes of $y$. Let $P_c(t)$ be the probability that a round with $c$ choices of $r$ measures a marked point, and let $c_1, c_2, \ldots$ be the numbers of choices in rounds $1, 2, \ldots$ of a phase: $c_i = \lceil\min(\lambda^{i-1}, \sqrt N)\rceil$.

**Theorem.**

1. Every run stops after at most $KP$ rounds if $P$ is finite, and after fewer than $B + \sqrt N + 2$ queries if $B$ is finite. It returns a point $x$ with $f(x) = y$, and $y$ is the smallest value of $f$ at the first point and at all measured points.
2. With $P = \infty$ and $B \ge 2Q(N)$, where $Q(N) = 1 + 18\sqrt N + \ln N(\log_{6/5}\sqrt N + 5)$, the run returns a minimum point with probability at least $1/2$.
3. With $B = \infty$ and a finite $P$, the run returns a minimum point with probability exactly $\sum_{k=1}^{K}\frac{n_k}{N}S_k$, where $S_1 = 1$ and
$$S_k = g_k\sum_{i=1}^{k-1}\frac{n_i}{R_{k-1}}S_i, \qquad g_k = 1 - \prod_{i=1}^{P}\bigl(1 - P_{c_i}(R_{k-1})\bigr) \quad (k \ge 2).$$
This probability is at most $\frac{n_1}{N}\bigl(1 + P(2c_P - 1)^2\ln N\bigr)$, so for a fixed $P$ it tends to 0 as $N$ grows with $n_1$ fixed.

**Claim 1 (one round).** Let the threshold be $y$ with $t$ marked points, $0 \le t < N$. Line L5 with $r$ iterations measures a marked point with probability $\sin^2((2r+1)\theta)$, where $\sin^2\theta = t/N$, and given that, the point is uniform among the $t$ marked points. A round of line L4 with $c$ choices succeeds with probability $P_c(t) = \frac1c\sum_{r=0}^{c-1}\sin^2((2r+1)\theta)$.

*Proof.* $A = H^{\otimes n}$ gives the uniform state $|s\rangle$. The oracle $O_y$ flips the sign of the marked points, and $A(2|0\rangle\langle 0| - I)A^\dagger = 2|s\rangle\langle s| - I$. So $G_y$ is the Grover iteration for the marking $[f(x) < y]$, and the analysis of [Grover's search](/grover-search/) gives $\sin^2((2r+1)\theta)$. The uniform state, $O_y$ and $2|s\rangle\langle s| - I$ do not change when two marked points are swapped, so all marked points have the same amplitude. Line L4 chooses $r$ uniformly from $c$ values, which gives $P_c(t)$. Since $t < N$ (the threshold point is not marked), $P_c(t) < 1$ for $c = 1$; if $t = 0$, then $P_c(0) = 0$. $\square$

**Claim 2 (the best point).** $y$ never increases, $f(x) = y$ always holds, and $y$ is the least value seen.

*Proof.* Line L1 sets $y = f(x)$. Line L7 changes $x$ and $y$ only to a measured point $x'$ and its value, and only if $f(x') < y$. So both statements hold after each line, by induction on the rounds. Line L9 returns them. $\square$

**Claim 3 (termination).** In a phase, the counter `fails` equals the number of rounds of the phase that have ended. So a phase has at most $P$ rounds, and a run has at most $KP$ rounds, because each phase except the last strictly lowers $y$ to one of the $K$ values.

*Proof.* Line L7 sets `fails` to 0 when a phase starts, and line L8 adds 1 at each failed round of the phase. When `fails` reaches $P$, line L3 stops the loop. A round with the budget rule starts only when used $< B$, and it adds $r + 1 \le \lceil\sqrt N\rceil$ because $r < \sqrt N$; so a run makes fewer than $B + \sqrt N + 2$ queries. $\square$

Claims 2 and 3 prove part 1.

**Claim 4 (the link to Dürr-Høyer minimum finding).** Let $T[x] = f(x)$. With $P = \infty$, lines L1 to L9 are the lines L1 to L9 of [Dürr-Høyer minimum finding](/durr-hoyer-minimum-finding/) for the table $T$, with the threshold value $y = T[y_{\mathrm{index}}]$ in place of the threshold index.

*Proof.* Both start from a uniform point and read its value with one query. Both choose $r$ (there $j$) uniformly from $\lceil m\rceil$ values with $m \le \sqrt N$, grow it by $6/5$ with the cap $\sqrt N$ and reset it to 1 at an improvement. Both apply the Grover iteration for the marking $T[x] < $ the current threshold value, count $r + 1$ queries, and accept a measured point only if its value is smaller. So the two runs have the same distribution of the sequence of thresholds and counts, step by step. $\square$

By Claim 4, the theorem of the Dürr-Høyer proof applies: the expected number of queries until $y = v_1$ is at most $Q(N)$, and a budget $B \ge 2Q(N)$ gives a minimum with probability at least $1/2$, by [Markov's inequality](/markov-inequality/). This proves part 2.

**Claim 5 (one phase with patience).** Let the threshold become $v_k$, $k \ge 2$, at some moment. Given the past, the phase that starts ends with an improvement with probability $g_k$, and then the new threshold point is uniform on the $R_{k-1}$ marked points.

*Proof.* At the start of the phase, the variable that line L8 grows has been reset to 1 by line L7 (or set to 1 by line L2), and `fails` is 0. The phase runs rounds $1, 2, \ldots$ with $c_1, c_2, \ldots$ choices, with fresh random choices and fresh measurements. By Claim 3 it ends without an improvement exactly when its first $P$ rounds all fail, which by Claim 1 has probability $\prod_{i=1}^{P}(1 - P_{c_i}(R_{k-1}))$. When a round succeeds, Claim 1 says the measured point is uniform on the marked points. $\square$

**Proof of part 3.** Let $S_k$ be the probability that the run returns a minimum point, given that the threshold has just become $v_k$. If $k = 1$, the threshold never changes again and the run returns a point of value $v_1$, so $S_1 = 1$. If $k \ge 2$, by Claim 5 the phase improves with probability $g_k$, and then the new threshold has the value $v_i$, $i < k$, with probability $n_i/R_{k-1}$; from there, the run behaves as a run that has just reached $v_i$, because the next phase starts fresh. Otherwise the run stops with $y = v_k > v_1$. This gives the recursion for $S_k$. Line L1 gives the value $v_k$ with probability $n_k/N$, which gives the sum.

For the upper bound, let $\rho_k$ be the probability that $v_k$ is ever the threshold. The run succeeds only if line L1 gives a point of value $v_1$, with probability $n_1/N$, or some phase with a threshold $v_k$, $k \ge 2$, improves to a point of value $v_1$. By Claim 5 that phase does so with probability $g_k n_1/R_{k-1}$. In round $i$ of the phase, $r \le c_i - 1 \le c_P - 1$, and $|\sin(m\theta)| \le m|\sin\theta|$ for integers $m \ge 1$, so $\sin^2((2r+1)\theta) \le (2c_P - 1)^2 R_{k-1}/N$. By the union bound over the $P$ rounds, $g_k \le P(2c_P - 1)^2R_{k-1}/N$. As in Claim 4 of the Dürr-Høyer proof, the first threshold with value at most $v_k$ is uniform on the $R_k$ points with value at most $v_k$, so $\rho_k \le n_k/R_k$, and $\sum_{k \ge 2} n_k/R_k \le \ln N$ by Claim 5 of that proof. Together,

$$\Pr[\text{success}] \le \frac{n_1}{N} + \sum_{k=2}^{K}\rho_k\,\frac{P(2c_P - 1)^2 R_{k-1}}{N}\cdot\frac{n_1}{R_{k-1}} \le \frac{n_1}{N}\bigl(1 + P(2c_P - 1)^2\ln N\bigr).$$

For a fixed $P$, $c_P$ is fixed, so the bound is $O(\log N/N)$ when $n_1$ is fixed. $\blacksquare$
