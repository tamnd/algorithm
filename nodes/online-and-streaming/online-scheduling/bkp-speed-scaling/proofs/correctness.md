---
title: BKP computes its speed from finitely many candidates and meets every deadline
proves: [correctness, termination]
status: full
---

We use the pseudocode and the notation of the page. The jobs are $(r_j, w_j, d_j)$ with $w_j > 0$ and $r_j < d_j$. For $t_2 > t$ let $t_1(t_2) = e t - (e - 1) t_2$ and

$$f(t_2) = \frac{W(t_2)}{t_2 - t}, \qquad W(t_2) = w(t, t_1(t_2), t_2) = \sum_{j \,:\, t_1(t_2) \le r_j \le t, \; d_j \le t_2} w_j.$$

The BKP speed is $s(t) = \sup_{t_2 > t} f(t_2)$. Part 1 and Part 2 are about the exact speed, as a function of continuous time. Part 3 is about the simulation.

## Part 1. The maximum is at a candidate

Fix $t$ and a job $j$ with $r_j \le t$. The condition $d_j \le t_2$ holds exactly for $t_2 \ge d_j$. Since $t_1(t_2)$ decreases as $t_2$ grows, the condition $t_1(t_2) \le r_j$ holds exactly for $t_2 \ge (e t - r_j)/(e - 1)$; if $r_j = t$ this bound is $t$, so the condition holds for all $t_2 > t$. So job $j$ is counted in $W(t_2)$ exactly for $t_2 \ge c_j$, where $c_j$ is the larger of $d_j$ and $(e t - r_j)/(e - 1)$, and $c_j > t$.

So $W$ is a step function that does not decrease, with steps only at the points $c_j$, and at each step point it already has its new value. Let $c$ be the largest step point with $c \le t_2$. On $[c, t_2]$ the value of $W$ is constant, so $f(t_2) \le f(c)$, since the denominator is larger. For $t_2$ less than every step point, $W(t_2) = 0$. So the supremum is a maximum and it is reached at some $c_j$. Each $c_j$ is either a deadline $d_j > t$ or a point $(e t - r_j)/(e - 1)$ with $r_j < t$, so it is in the set $T$ of line L3. Lines L4 to L6 take the maximum of $f$ over $T$, so they compute $s(t)$ exactly. $\square$

## Part 2. Every job meets its deadline

We run EDF at speed $s(t)$ whenever a released job is unfinished, and idle otherwise. Suppose that some job $j$ is not finished by its deadline $d = d_j$.

**The busy interval.** Let $t_0$ be the infimum of the times $\tau \le d$ such that at every time in $[\tau, d)$ the processor runs a job with deadline at most $d$. This set of times contains a short interval just before $d$, because $j$ is pending there and EDF runs a job with deadline at most $d$. If $t_0$ is larger than the first release time, there are times $\tau < t_0$ arbitrarily close to $t_0$ at which the processor idles or runs a job with deadline larger than $d$. At such a time, by the EDF rule, every released job with deadline at most $d$ is finished. Taking $\tau$ so close to $t_0$ that no job is released in $(\tau, t_0)$, we get: every job with $r_k < t_0$ and $d_k \le d$ is finished by $t_0$. This also holds if $t_0$ is the first release time, since then no job has $r_k < t_0$.

**Counting the work.** Let $X$ be the set of jobs with $t_0 \le r_k$ and $d_k \le d$, and let $w(X)$ be their total work. On $[t_0, d)$ the processor only works on jobs with deadline at most $d$, and by the last paragraph these are jobs of $X$. Job $j$ is in $X$: if $r_j < t_0$, it would be finished by $t_0$, but it is not finished even at $d$. Since $j$ is not finished at $d$, the work done on $[t_0, d)$ is

$$\int_{t_0}^{d} s(t) \, dt < w(X).$$

**A lower bound on the speed.** For $t \in [t_0, d)$, take $t_2 = d$ in the definition of $s(t)$. Then $t_1 = e t - (e - 1) d$, and a job $k \in X$ is counted in $W(d)$ if $r_k \le t$ and $e t - (e - 1) d \le r_k$. The second condition is $t \le r_k + (1 - 1/e)(d - r_k)$. Let $I_k = [r_k, \, r_k + (1 - 1/e)(d - r_k)]$, which lies inside $[t_0, d)$. So

$$s(t) \ge \frac{W(d)}{d - t} \ge \sum_{k \in X \,:\, t \in I_k} \frac{w_k}{d - t}.$$

Integrate over $[t_0, d)$ and swap the sum and the integral:

$$\int_{t_0}^{d} s(t) \, dt \ge \sum_{k \in X} w_k \int_{I_k} \frac{dt}{d - t} = \sum_{k \in X} w_k \ln \frac{d - r_k}{(d - r_k)/e} = \sum_{k \in X} w_k = w(X).$$

This contradicts the strict inequality above. So every job finishes by its deadline. $\square$

## Part 3. The simulation terminates

In each step of line L1 with a released, unfinished job $j$, the speed is positive: job $j$ is counted in $W(c_j)$, so $s \ge w_j / (c_j - t) > 0$. Moreover, while $j$ is unfinished at times $t \ge d_j$, we have $c_j = (e t - r_j)/(e - 1)$ and $c_j - t = (t - r_j)/(e - 1)$, so the speed is at least $(e - 1) w_j / (t - r_j)$. Let $r_0$ be the first release time, $w_0$ the smallest work and $D$ the largest deadline. At each step with midpoint $t > D$ in which some job is unfinished, the speed is at least $(e - 1) w_0 / (t - r_0)$. If the loop ran for ever, the work done in these steps would be at least the sum of $(e - 1) w_0 h / (t - r_0)$ over their midpoints $t$, which grows without bound like a harmonic series, while the total work is finite. So the remaining work reaches 0 after finitely many steps of length $h$, and the loop of line L1 ends. $\blacksquare$
