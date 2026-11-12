---
title: The RM simulation runs the highest priority, and the simulation and utilization tests are exact as stated
proves: [correctness]
status: full
---

We use the notation of the page. A job is *pending* at time $t$ if it is released by $t$ and has work left.

**Lemma 1 (the loop).** In each run of line L9, in the interval $[t, t + \delta)$, the job $j$ is the pending job of highest priority (by rank, then by release).

*Proof.* Lines L6 and L10 keep this invariant at line L7: $Q$ holds exactly the jobs released by $t$ with work left. Line L7 takes the job with the least key. By line L8, $t + \delta$ is at most the next release, so no job becomes pending inside the interval, and the other jobs do not run, so their keys and their membership stay the same. Each round ends a job or reaches a release, so the loop stops after at most $2k$ rounds. $\square$

So the loop builds the preemptive fixed-priority schedule of the jobs released in $[0, W)$, and the jobs released at or after $W$ do not change it before $W$.

**Lemma 2 (one hyperperiod is enough).** Let the tasks be synchronous with integer periods and $D_i \le T_i$, and let $H = \operatorname{lcm}(T_1, \ldots, T_n)$. The fixed-priority schedule of the infinite job sequence meets all deadlines if and only if the simulation with $W = H$ has no miss.

*Proof.* A job released at or after $H$ cannot run before $H$. So on $[0, H)$ the infinite schedule and the simulated schedule run the same jobs, by Lemma 1.

If the simulation has no miss, each job released in $[0, H)$ ends by its deadline, which is at most $(H - T_i) + D_i \le H$. So in the infinite schedule, these jobs also end in $[0, H)$, and no work is pending at $H$. At time $H$ the infinite schedule is in the state of time 0: no pending work, and the same releases, shifted by $H$. The rule depends only on the ranks and the releases, so the schedule on $[H, 2H)$ is the schedule on $[0, H)$ shifted by $H$. By induction, each hyperperiod repeats the first one, and all deadlines are met.

If the simulation has a miss, let $J$ be the missing job with the earliest deadline $d \le H$. Before $d$ the two schedules are equal: no job released at or after $H \ge d$ runs before $d$. So $J$ has work left at $d$ in the infinite schedule too. $\square$

`simulation_test` runs the loop with $W = H$ and checks each recorded finish time against its deadline, so by Lemma 2 it returns true exactly when the fixed order meets all deadlines.

**Lemma 3 (the exact form of the Liu-Layland test).** For $n \ge 1$ and $U \ge 0$,

$$U \le n(2^{1/n} - 1) \iff \left(1 + \frac{U}{n}\right)^n \le 2.$$

*Proof.* The left side is the same as $1 + U/n \le 2^{1/n}$. Both sides are positive, and $x \mapsto x^n$ is increasing for $x > 0$, so this holds if and only if $(1 + U/n)^n \le 2$. $\square$

With rational $C_i$ and $T_i$, `liu_layland_test` computes $(1 + U/n)^n$ with exact fractions, and `hyperbolic_test` computes $\prod_i (1 + U_i)$ the same way, so neither test is affected by rounding. That the two tests are sufficient for RM is proved on the page on the [Liu-Layland bound](/liu-layland-utilization-bound/). $\blacksquare$
