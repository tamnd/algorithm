---
tag: G3Q00A
kind: algorithm
slug: avr
name: Average rate speed scaling
aliases:
- AVR
- average rate heuristic
- Average Rate
area: online-and-streaming/online-scheduling
level: advanced
summary: Run each job at its density over its feasibility window, summing the rates at each time.
solves: [online-speed-scaling]
model: real-ram
complexity:
  vars: {n: the number of jobs}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1995
  people: [Frances Yao, Alan Demers, Scott Shenker]
  note: Yao, Demers and Shenker defined the speed scaling model and the AVR rule in 1995, and showed that AVR is 2^(alpha - 1) alpha^alpha competitive for energy.
prereqs: [online-speed-scaling, earliest-deadline-first, deadline, competitive-ratio]
see_also: [avr-competitive-ratio, optimal-available, bkp-speed-scaling, yds-algorithm, speed-scaling, edf-optimality, convex-function, round-robin]
sources:
  - paper: "F. Frances Yao, Alan Demers and Scott Shenker, A scheduling model for reduced CPU energy, FOCS 1995"
    locator: pages 374 to 382 (the model, the offline algorithm, AVR with the upper bound 2^(alpha - 1) alpha^alpha and the lower bound alpha^alpha, and OA)
  - paper: doi:10.1007/s00453-009-9379-z
    title: Nikhil Bansal, David P. Bunde, Ho-Leung Chan and Kirk Pruhs, Average rate speed scaling, Algorithmica 60(4), 2011 (LATIN 2008)
    locator: pages 877 to 889, Sections 3 to 5 (the definition of AVR with EDF, the lower bound ((2 - delta) alpha)^alpha / 2, and a potential function proof of the upper bound)
  - paper: doi:10.4230/LIPIcs.STACS.2011.1
    title: Susanne Albers, Algorithms for dynamic speed scaling, STACS 2011
    locator: Section 2.1 (Average Rate, Optimal Available and BKP, and their competitive ratios)
---

Average rate (AVR) is an [online algorithm](/online-algorithm/) for [online speed scaling](/online-speed-scaling/): when a job arrives with work $w_j$ and a [deadline](/deadline/) $d_j$, it adds the job's density $w_j / (d_j - r_j)$ to the processor speed until the deadline, and it runs the jobs by [earliest deadline first](/earliest-deadline-first/). Each job then finishes in time. With power $s^{\alpha}$, AVR uses at most $2^{\alpha - 1} \alpha^{\alpha}$ times the minimum energy (Yao, Demers and Shenker 1995), and this bound is nearly tight. It is simple and fair, but [Optimal Available](/optimal-available/) and [BKP](/bkp-speed-scaling/) have better ratios.

## In plain words

A processor can run fast or slow. Running fast uses much more power, because power grows like the speed to a power $\alpha > 1$, often near 3. Jobs arrive over time, and each must be done by its deadline. To save energy, the processor should run as slowly and as evenly as it can.

AVR treats each job alone. If a job needs 6 units of work in a window of 3 time units, it needs speed 2 on average, so AVR adds 2 to the speed for that window. At each moment, the speed is the sum of these averages over the jobs whose windows are open. This is always enough to finish every job, and it is never far from the best, but it can run too fast when windows overlap.

## The problem

The input is a sequence $\sigma$ of $n$ jobs, revealed online. Job $j$ has a release time $r_j$, a work $w_j > 0$ and a deadline $d_j > r_j$, all known at time $r_j$. One processor can run at any speed $s \ge 0$, and at speed $s$ it uses power $P(s) = s^{\alpha}$ with a constant $\alpha > 1$. A job may be preempted. A schedule chooses the speed $s(t)$ and the job to run at each time, and it is feasible if each job gets $w_j$ units of work inside $[r_j, d_j]$. The objective is the energy $\int s(t)^{\alpha} \, dt$.

| symbol | meaning |
|---|---|
| $\sigma$ | the sequence of jobs, revealed at the release times |
| ALG$(\sigma)$, OPT$(\sigma)$ | the energy of the online schedule and of the optimal offline schedule, which the [YDS algorithm](/yds-algorithm/) computes |
| $c$ | the [competitive ratio](/competitive-ratio/): ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$, here with additive constant $b = 0$ |
| $\delta_j$ | the density $w_j / (d_j - r_j)$ of job $j$ |

## The algorithm

The speed of AVR at time $t$ is

$$s_{\text{AVR}}(t) = \sum_{j \,:\, r_j \le t < d_j} \delta_j.$$

Online, the algorithm adds $\delta_j$ to the speed at time $r_j$ and removes it at time $d_j$. The code below computes the whole speed profile by a sweep over these events, and then runs EDF at these speeds.

```pseudo id=main
AVR(jobs (r_j, w_j, d_j))
L1  for each job j do
L2      δ_j ← w_j / (d_j − r_j);  add the events (r_j, +δ_j) and (d_j, −δ_j)
L3  sort the events by time
L4  s ← 0;  for each event (t, Δ) in time order do
L5      if t > the previous event time and s > 0 then output the piece [previous, t) with speed s
L6      s ← s + Δ
L7  return the pieces;  at each time, run the released, unfinished job with the earliest deadline
```

The speed does not depend on which job runs. Running each job at its own density on its window would also be feasible; EDF is the usual choice, and it finishes jobs earlier.

## Example

Take three jobs, written as (release, work, deadline): $A = (0, 4, 4)$, $B = (1, 3, 3)$ and $C = (2, 2, 6)$. The densities are $\delta_A = 1$, $\delta_B = 3/2$ and $\delta_C = 1/2$.

| interval | open windows | AVR speed | EDF runs |
|---|---|---|---|
| $[0, 1)$ | $A$ | 1 | $A$ |
| $[1, 2)$ | $A$, $B$ | $5/2$ | $B$ |
| $[2, 3)$ | $A$, $B$, $C$ | 3 | $B$ until $13/6$, then $A$ |
| $[3, 4)$ | $A$, $C$ | $3/2$ | $A$ until $10/3$, then $C$ |
| $[4, 6)$ | $C$ | $1/2$ | $C$ |

The jobs complete at $C_A = 10/3$, $C_B = 13/6$ and $C_C = 6$, all by their deadlines. The optimal schedule runs $A$ and $B$ at speed $7/4$ on $[0, 4)$ and $C$ at speed 1 on $[4, 6)$.

| $\alpha$ | AVR energy | optimal energy | ratio |
|---|---|---|---|
| 2 | 19 | $57/4$ | $4/3$ |
| 3 | $189/4$ | $375/16$ | about 2.02 |

AVR wastes energy because its speed jumps to 3 on $[2, 3)$ and falls to $1/2$ later. The optimum keeps the speed flat on $[0, 4)$.

## Correctness

The sweep keeps an invariant: after the events with time less than $t$ are processed, $s$ is the sum of $\delta_j$ over the jobs with $r_j < t \le d_j$, which is the AVR speed on the open interval up to $t$. So each output piece has the AVR speed. Every job is finished in time, because the speed profile is enough for the schedule that runs each job $j$ at rate $\delta_j$ on $[r_j, d_j)$, which does exactly $w_j$ units of work in the window. EDF meets all deadlines whenever some schedule with the same speeds does ([EDF optimality](/edf-optimality/), applied after a change of the time scale to the work done). The full proof is in [proofs/correctness.md](proofs/correctness.md).

The energy bound $2^{\alpha - 1} \alpha^{\alpha}$ is a separate theorem, proved on [AVR competitive ratio](/avr-competitive-ratio/).

## Complexity

- **Time.** There are $2n$ events. Sorting them takes $O(n \log n)$, and the sweep takes $O(n)$. EDF with a [binary heap](/binary-heap/) of deadlines takes $O(\log n)$ per job release, completion or piece end, so $O(n \log n)$ in total. Online, each release and each deadline costs $O(\log n)$.
- **Space.** The events, the pieces and the heap take $O(n)$.
- **Pieces.** The profile has at most $2n - 1$ pieces, since the speed changes only at releases and deadlines.

## Properties

- **Online.** The speed at time $t$ depends only on the jobs released by $t$.
- **Always feasible.** Each job meets its deadline, for every input, since the speed is never below the sum of the active densities.
- **Competitive ratio.** At most $2^{\alpha - 1} \alpha^{\alpha}$, which is 8 for $\alpha = 2$ and 108 for $\alpha = 3$. It is at least $\alpha^{\alpha}$ (Yao, Demers and Shenker) and at least $(\alpha + (\alpha - 1)^{1 - 1/\alpha})^{\alpha} / 2$, which is 4.5 for $\alpha = 2$ and about 48.3 for $\alpha = 3$ (Bansal, Bunde, Chan and Pruhs). The lower bounds are cited and not proved.
- **Optimal on simple inputs.** With one job, or with windows that do not overlap, AVR runs each job at a constant speed over its window, which is optimal by the convexity of $s^{\alpha}$ ([Jensen's inequality](/jensens-inequality/)).
- **Same as OA for a common deadline.** If all jobs have the same deadline, the speed of AVR equals the speed of Optimal Available at each time. To see this, let $R(t)$ be the remaining work at time $t$ under the common deadline $d$. OA runs at $R(t)/(d - t)$. If this equals the AVR speed $s$ just before a release of work $w$, then just after it OA runs at $(R(t) + w)/(d - t) = s + w/(d - t)$, which is the new AVR speed. Between releases both stay constant, so by induction they are equal.

## Variants and improvements

- **Optimal Available.** Recompute the optimal schedule of the remaining work at each release. It is exactly $\alpha^{\alpha}$-competitive. See [Optimal Available](/optimal-available/).
- **BKP.** A speed based on the densest recent intervals, which is $2 (\alpha / (\alpha - 1))^{\alpha} e^{\alpha}$-competitive, better than both AVR and OA for large $\alpha$. See [BKP speed scaling](/bkp-speed-scaling/).
- **Offline optimum.** The [YDS algorithm](/yds-algorithm/) finds the minimum energy schedule when all jobs are known.
- **Discrete speeds.** If the processor has only a few speed levels, a desired speed is replaced by the two nearest levels in the right proportion, which keeps the work the same.

## When to use it

Use AVR when a simple rule with a guaranteed ratio is enough, when the power exponent is small, or when each job should get a share of the speed that depends only on its own work and window. Prefer Optimal Available when a better ratio is worth the cost of a recomputation at each release. Do not use AVR when many windows overlap in a nested way, because then its speed has high peaks.

## Pitfalls

- **Closed windows.** A job adds its density on $[r_j, d_j)$. Counting it also at $d_j$ makes the speed wrong at each deadline, though this does not change the energy.
- **Floating point.** The speed is a sum of densities that are added and removed later. In floating point, the speed may not return to exactly 0, which leaves tiny pieces. Exact fractions avoid this.
- **The speed is not the job rate.** With EDF, a job may run faster or slower than its density. Only the total speed is fixed by the rule.
- **The exponent.** The model needs $\alpha > 1$. With $\alpha \le 1$, power is not strictly [convex](/convex-function/) and running fast costs nothing extra, so the problem changes.
- **The ratio grows fast in $\alpha$.** For $\alpha = 3$, the guarantee is 108, and the worst inputs reach about 48.

## Implementations

## History

Yao, Demers and Shenker introduced speed scaling for deadlines in 1995. They gave the optimal offline algorithm now called YDS, and two online rules, Average Rate and Optimal Available. They proved that AVR is $2^{\alpha - 1} \alpha^{\alpha}$-competitive for $\alpha \ge 2$ and that its ratio is at least $\alpha^{\alpha}$, and they conjectured that $\alpha^{\alpha}$ is exact. In 2008, Bansal, Bunde, Chan and Pruhs disproved this by a lower bound of $((2 - \delta) \alpha)^{\alpha} / 2$, and they gave a simpler potential function proof of the upper bound.

## References
