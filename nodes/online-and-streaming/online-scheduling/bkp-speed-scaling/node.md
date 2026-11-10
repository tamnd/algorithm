---
tag: Z0T4F5
kind: algorithm
slug: bkp-speed-scaling
name: Bansal-Kimbrel-Pruhs speed scaling
aliases:
- BKP algorithm
- BKP
area: online-and-streaming/online-scheduling
level: research
summary: Speed set from the maximum work density over recent windows, improving the competitive ratio for energy.
solves: [online-speed-scaling]
model: real-ram
complexity:
  vars: {n: the number of jobs, m: the number of time steps of the simulation}
  time: {worst: O(m n^2)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2004
  people: [Nikhil Bansal, Tracy Kimbrel, Kirk Pruhs]
  note: Bansal, Kimbrel and Pruhs gave the algorithm at FOCS 2004 (journal version 2007) and proved that it is 2 (alpha / (alpha - 1))^alpha e^alpha competitive for energy and e competitive for the maximum speed.
prereqs: [online-speed-scaling, earliest-deadline-first, competitive-ratio, yds-algorithm]
see_also: [optimal-available, avr, avr-competitive-ratio, speed-scaling, potential-function, edf-optimality, convex-function]
sources:
  - paper: "Nikhil Bansal, Tracy Kimbrel and Kirk Pruhs, Speed scaling to manage energy and temperature, Journal of the ACM 54(1), 2007 (FOCS 2004)"
    locator: the definition of the BKP algorithm, the energy bound 2 (alpha / (alpha - 1))^alpha e^alpha, and the bound e for the maximum speed
  - paper: doi:10.4230/LIPIcs.STACS.2011.1
    title: Susanne Albers, Algorithms for dynamic speed scaling, STACS 2011
    locator: Section 2.1 (the definition of BKP with w(t, t1, t2), and its competitive ratio)
  - paper: "Nikhil Bansal, Ho-Leung Chan, Kirk Pruhs and Dmitriy Katz, Improved bounds for speed scaling in devices obeying the cube-root rule, ICALP 2009"
    locator: pages 144 to 155 (the lower bound e^(alpha - 1) / alpha for every deterministic algorithm, and qOA)
---

The Bansal-Kimbrel-Pruhs algorithm (BKP) is an [online algorithm](/online-algorithm/) for [online speed scaling](/online-speed-scaling/). At each time $t$, it looks at windows $[t_1, t_2]$ around $t$ whose part in the past is $e - 1$ times shorter than their part in the future, and runs at the largest density of known work in such a window, scaled by $e$. It runs the jobs by [earliest deadline first](/earliest-deadline-first/). It meets every deadline, uses at most $2 (\alpha / (\alpha - 1))^{\alpha} e^{\alpha}$ times the minimum energy with power $s^{\alpha}$, and its largest speed is at most $e$ times the largest speed of the optimum. For large $\alpha$, its energy ratio grows like $e^{\alpha}$, much more slowly than the $\alpha^{\alpha}$ of [Optimal Available](/optimal-available/).

## In plain words

A processor can run fast or slow, and power grows like the speed to a power $\alpha > 1$. Jobs arrive with deadlines. Optimal Available plans only for the work it knows, so it runs too slowly when more work keeps coming. BKP guards against this. It assumes that the recent past is a guide to the near future: if a lot of work arrived recently, more may come, so it runs faster now.

To do this, BKP looks at each window that starts a little in the past and ends at some time in the future, and asks how much known work must be done in it. It takes the busiest such window and runs at its rate, scaled up. This extra speed costs energy on calm inputs, but it keeps the worst case under control.

## The problem

The input is a sequence $\sigma$ of $n$ jobs, revealed online. Job $j$ has a release time $r_j$, a work $w_j > 0$ and a deadline $d_j > r_j$, all known at time $r_j$. One processor runs at any speed $s \ge 0$ with power $s^{\alpha}$, $\alpha > 1$, and jobs may be preempted. A schedule is feasible if each job gets $w_j$ units of work inside $[r_j, d_j]$, and the objective is the energy $\int s(t)^{\alpha} \, dt$.

| symbol | meaning |
|---|---|
| $\sigma$ | the sequence of jobs, revealed at the release times |
| ALG$(\sigma)$, OPT$(\sigma)$ | the energy of the online schedule and of the optimal offline schedule, from the [YDS algorithm](/yds-algorithm/) |
| $c$ | the [competitive ratio](/competitive-ratio/): ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$, here with additive constant $b = 0$ |
| $w(t, t_1, t_2)$ | the original work of the jobs with $t_1 \le r_j \le t$ and $d_j \le t_2$, which is the known work that lies in $[t_1, t_2]$ |

## The algorithm

At time $t$, BKP runs at speed

$$s(t) = \max_{t_2 > t} \frac{w(t, \, e t - (e - 1) t_2, \, t_2)}{t_2 - t}.$$

With $t_1 = e t - (e - 1) t_2$, the window $[t_1, t_2]$ has $t - t_1 = (e - 1)(t_2 - t)$ and length $t_2 - t_1 = e (t_2 - t)$. So $s(t)$ is $e$ times the density of the known work in the window. The work in the formula is the original work $w_j$, not the remaining work. If no released job is unfinished, the processor idles.

As a function of $t_2$, the work in the window grows only in steps, at a deadline $d_j$ or when $t_1$ passes a release time $r_j$, which is at $t_2 = (e t - r_j)/(e - 1)$. Between the steps the ratio falls. So the maximum is at one of these $O(n)$ points. The speed changes continuously with $t$, so the code below simulates BKP in time steps of length $h$, with the speed of each step taken at its midpoint.

```pseudo id=main
BKP(jobs (r_j, w_j, d_j), step h)
L1  while some job is unfinished, for each step [a, a + h) in order do
L2      t ← a + h/2;  K ← the jobs with r_j ≤ t
L3      T ← {d_j : j ∈ K, d_j > t} ∪ {(e t − r_j)/(e − 1) : j ∈ K, r_j < t}
L4      s ← 0;  for each t_2 in T do
L5          t_1 ← e t − (e − 1) t_2;  W ← the sum of w_j over j ∈ K with t_1 ≤ r_j and d_j ≤ t_2
L6          s ← max(s, W / (t_2 − t))
L7      if a released job is unfinished then run EDF at speed s on [a, a + h)
L8  return the energy and the completion times
```

## Example

Take three jobs, written as (release, work, deadline): $A = (0, 4, 4)$, $B = (1, 3, 3)$ and $C = (2, 2, 6)$. Some speeds of BKP:

| $t$ | best $t_2$ | window $[t_1, t_2]$ | work | speed |
|---|---|---|---|---|
| 0.5 | 4 | $[-6.87, 4]$ | $A$: 4 | $4 / 3.5 = 8/7$ |
| 1.5 | 4 | $[-2.80, 4]$ | $A$, $B$: 7 | $7 / 2.5 = 14/5$ |
| 2.5 | 4 | $[-0.08, 4]$ | $A$, $B$: 7 | $7 / 1.5 = 14/3$ |
| 3.5 | 6 | $[-0.80, 6]$ | $A$, $B$, $C$: 9 | $9 / 2.5 = 18/5$ |

The simulation with $h = 0.001$ finishes $B$ at about 2.05, $A$ at about 2.72 and $C$ at about 3.21, well before the deadlines.

| $\alpha$ | BKP energy | optimal energy | ratio | guarantee |
|---|---|---|---|---|
| 2 | about 30.4 | $57/4$ | about 2.13 | about 59.1 |
| 3 | about 113.3 | $375/16$ | about 4.83 | about 135.6 |

On this input BKP is worse than OA (ratios $20/19$ and $432/375$), because it runs fast to guard against work that never comes. The largest speed is $7e/4 \approx 4.757$, at $t = 4(1 - 1/e) \approx 2.53$, where the window is exactly $[0, 4]$. This is $e$ times the largest optimal speed $7/4$, so the bound $e$ for the maximum speed is tight here.

## Correctness

**The maximum in line L6 is the BKP speed.** The work $W$ is a step function of $t_2$ that only grows, and at each step point the new jobs are already counted. Between two step points the ratio $W / (t_2 - t)$ falls. So the supremum over $t_2 > t$ is reached at a step point, and these are the points of line L3.

**Every job meets its deadline.** Suppose a job $j$ misses its deadline $d$. Let $t_0$ be the earliest time such that on $[t_0, d)$ the processor always runs jobs with deadline at most $d$. Just before $t_0$, no job with deadline at most $d$ is pending, so the work done on $[t_0, d)$ is at most the total work $w(X)$ of the set $X$ of jobs with $r_k \ge t_0$ and $d_k \le d$, minus what is left of $j$. Now take $t_2 = d$ in the formula. Job $k \in X$ is in the window at time $t$ when $r_k \le t \le r_k + (1 - 1/e)(d - r_k)$, so

$$\int_{t_0}^{d} s(t) \, dt \ge \sum_{k \in X} w_k \int_{r_k}^{r_k + (1 - 1/e)(d - r_k)} \frac{dt}{d - t} = \sum_{k \in X} w_k \ln e = w(X).$$

So the processor does at least $w(X)$ units of work on $[t_0, d)$, which is a contradiction. The full proof is in [proofs/correctness.md](proofs/correctness.md).

**One job.** For one job $(0, w, d)$ the speed is $w / (d - t)$ until $t = (1 - 1/e) d$, and the work done by then is $w \ln e = w$. So the job finishes exactly at $(1 - 1/e) d$, and BKP uses $(e^{\alpha - 1} - 1)/(\alpha - 1)$ times the optimal energy: about 1.72 for $\alpha = 2$ and 3.19 for $\alpha = 3$. The tests check both facts.

## Complexity

- **One speed.** Line L3 gives at most $2n$ candidates, and line L5 sums over $n$ jobs, so one speed costs $O(n^2)$. Sorting the jobs by release time and by deadline and sweeping over the candidates in order of $t_2$ reduces this to $O(n \log n)$.
- **The simulation.** With $m$ steps, the time is $O(m n^2)$ in the worst case and the extra space is $O(n)$. A real processor would update its speed at a fixed rate in the same way.
- **The error.** The midpoint rule gives a speed profile that is close to the true one, and the error in the energy and in the completion times is $O(h)$, mostly from the last step of each job.

## Properties

- **Online and feasible.** The speed depends only on the known jobs, and each job meets its deadline, as shown above.
- **Energy ratio.** At most $2 (\alpha / (\alpha - 1))^{\alpha} e^{\alpha}$, about 59.1 for $\alpha = 2$, 135.6 for $\alpha = 3$ and 345.1 for $\alpha = 4$. This bound is proved by Bansal, Kimbrel and Pruhs and is cited here, not proved.
- **Maximum speed.** At each time $t$, the jobs counted in $w(t, t_1, t_2)$ all have windows inside $[t_1, t_2]$, so the optimum must run at average speed at least $w(t, t_1, t_2) / (t_2 - t_1)$ there. Since $t_2 - t_1 = e (t_2 - t)$, $s(t)$ is at most $e$ times the largest speed of the optimum. The tests check this bound.
- **Compared with OA.** The guarantee of OA is $\alpha^{\alpha}$. BKP has the better guarantee when $\alpha$ is above about 4.2. For $\alpha = 2$ or 3, OA has the better guarantee.
- **Lower bound.** Every deterministic online algorithm has an energy ratio of at least $e^{\alpha - 1} / \alpha$ (Bansal, Chan, Katz and Pruhs 2009). So a growth like $e^{\alpha}$ is necessary, up to a factor polynomial in $\alpha$. This bound is cited.

## Variants and improvements

- **qOA.** Running at $q$ times the speed of Optimal Available, with $q = 2 - 1/\alpha$, gives the ratio $4^{\alpha} / (2 \sqrt{e \alpha})$, which is better than BKP for $\alpha$ up to about 11 (11.2 against 135.6 for $\alpha = 3$). For larger $\alpha$, BKP is better, since $4^{\alpha}$ grows faster than $e^{\alpha}$. This result is cited. See [Optimal Available](/optimal-available/).
- **Temperature.** The same paper studies the maximum temperature of the processor in a cooling model, and gives online bounds for it with a constant ratio. This is cited and not covered here.
- **A bounded maximum speed.** If the processor has a maximum speed, deadlines may be impossible to meet, and the problem changes to throughput with energy. See [online throughput maximization](/online-throughput-maximization/) for the version without energy.

## When to use it

Use BKP when the power exponent is large, or when a bound on the maximum speed matters as much as the energy, since its maximum speed is at most $e$ times the optimal one. For the usual exponent $\alpha = 3$, OA and qOA have better energy guarantees, and BKP pays for its caution on inputs where little work arrives after the first jobs.

## Pitfalls

- **Original work, not remaining work.** The window uses $w_j$ even for jobs that are partly done. Using the remaining work breaks the feasibility proof.
- **The shape of the window.** The past part of the window is $e - 1$ times its future part. If the window has length $\beta$ times its future part, the integral in the feasibility proof is $\ln \beta$, so the proof needs $\beta \ge e$. The choice $\beta = e$ is the smallest value for which it works.
- **Missed candidates.** The maximum over $t_2$ is not always at a deadline. The points $(e t - r_j)/(e - 1)$ are needed too; for one job after time $(1 - 1/e) d$ they give the only positive term.
- **Idling.** The formula can give a positive speed after all known work is done. The processor should idle then, which only saves energy.
- **Floating point.** The candidates involve $e$, so exact arithmetic is not possible. The comparisons $t_1 \le r_j$ and $d_j \le t_2$ need a small tolerance, since at a candidate point one of them holds with equality.

## Implementations

## History

Bansal, Kimbrel and Pruhs gave BKP at FOCS 2004, in a paper that also proved that Optimal Available is exactly $\alpha^{\alpha}$-competitive and that started the study of temperature in speed scaling. The journal version appeared in 2007. Bansal, Chan, Katz and Pruhs proved the general lower bound $e^{\alpha - 1} / \alpha$ in 2009 and gave qOA, which has a better ratio for small $\alpha$.

## References
