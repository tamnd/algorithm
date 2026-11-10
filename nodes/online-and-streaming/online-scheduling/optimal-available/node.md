---
tag: 4DSS0A
kind: algorithm
slug: optimal-available
name: Optimal Available speed scaling
aliases:
- OA
- Optimal Available
area: online-and-streaming/online-scheduling
level: advanced
summary: At each arrival, recompute the offline optimal speeds for the remaining work.
solves: [online-speed-scaling]
model: real-ram
complexity:
  vars: {n: the number of jobs}
  time: {worst: O(n^2 log n)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1995
  people: [Frances Yao, Alan Demers, Scott Shenker, Nikhil Bansal, Tracy Kimbrel, Kirk Pruhs]
  note: Yao, Demers and Shenker proposed Optimal Available in 1995, and Bansal, Kimbrel and Pruhs proved in 2004 that it is exactly alpha^alpha competitive for energy.
prereqs: [online-speed-scaling, yds-algorithm, earliest-deadline-first, competitive-ratio]
see_also: [avr, avr-competitive-ratio, bkp-speed-scaling, speed-scaling, potential-function, edf-optimality, convex-function]
sources:
  - paper: "F. Frances Yao, Alan Demers and Scott Shenker, A scheduling model for reduced CPU energy, FOCS 1995"
    locator: pages 374 to 382 (the definition of Optimal Available and the lower bound alpha^alpha)
  - paper: "Nikhil Bansal, Tracy Kimbrel and Kirk Pruhs, Speed scaling to manage energy and temperature, Journal of the ACM 54(1), 2007 (FOCS 2004)"
    locator: the potential function proof that Optimal Available is alpha^alpha competitive for energy, and the matching lower bound
  - paper: doi:10.4230/LIPIcs.STACS.2011.1
    title: Susanne Albers, Algorithms for dynamic speed scaling, STACS 2011
    locator: Section 2.1, Theorem 2.4 (the competitive ratio of Optimal Available is exactly alpha^alpha)
---

Optimal Available (OA) is an [online algorithm](/online-algorithm/) for [online speed scaling](/online-speed-scaling/): at each moment it runs at the speed of the minimum energy schedule for the work that is known and not yet done, as if no more jobs would arrive, and it runs the jobs by [earliest deadline first](/earliest-deadline-first/). It recomputes this plan only when a job arrives. With power $s^{\alpha}$, it uses at most $\alpha^{\alpha}$ times the minimum energy, and this ratio is exact (Bansal, Kimbrel and Pruhs 2004). It meets every deadline.

## In plain words

A processor can run fast or slow, and power grows like the speed to a power $\alpha > 1$. Jobs arrive over time with deadlines. OA always acts as if the jobs it knows are the last ones. It plans the cheapest way to finish them, which is to run as slowly and as evenly as the deadlines allow, and follows that plan. When a new job arrives, the plan is out of date, so OA makes a new one.

This is optimal if no more jobs come. When jobs keep arriving, OA runs too slowly at first and must speed up later, which costs energy because power grows fast with the speed. The theory shows that this mistake costs at most a factor $\alpha^{\alpha}$, which is 27 for $\alpha = 3$.

## The problem

The input is a sequence $\sigma$ of $n$ jobs, revealed online. Job $j$ has a release time $r_j$, a work $w_j > 0$ and a deadline $d_j > r_j$, all known at time $r_j$. One processor runs at any speed $s \ge 0$ with power $s^{\alpha}$, $\alpha > 1$, and jobs may be preempted. A schedule is feasible if each job gets $w_j$ units of work inside $[r_j, d_j]$, and the objective is the energy $\int s(t)^{\alpha} \, dt$.

| symbol | meaning |
|---|---|
| $\sigma$ | the sequence of jobs, revealed at the release times |
| ALG$(\sigma)$, OPT$(\sigma)$ | the energy of the online schedule and of the optimal offline schedule, from the [YDS algorithm](/yds-algorithm/) |
| $c$ | the [competitive ratio](/competitive-ratio/): ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$, here with additive constant $b = 0$ |
| $\rho_j(t)$ | the work of job $j$ that is not done at time $t$ |

## The algorithm

When all known jobs are available now, the YDS plan is simple. Sort the unfinished jobs by deadline, $d_1 \le d_2 \le \dots$, and let $P_k = \rho_1 + \dots + \rho_k$. The densest interval starts now and ends at the deadline $d_k$ that maximizes $P_k / (d_k - t)$. So the speed of OA at time $t$ is

$$s_{\text{OA}}(t) = \max_{k} \frac{P_k(t)}{d_k - t},$$

and it stays the same until the next release or until the deadline $d_k$, where the next part of the plan starts.

```pseudo id=main
OPTIMAL-AVAILABLE(jobs (r_j, w_j, d_j))
L1  for each release time t, in increasing order do
L2      add the jobs released at t to the set R of unfinished jobs, with ρ_j ← w_j
L3      t' ← the next release time, or ∞ if there is none
L4      while R is not empty and t < t' do
L5          sort R by deadline;  let k be the largest index that maximizes P_k / (d_k − t)
L6          s ← P_k / (d_k − t);  e ← min(d_k, t')
L7          run the jobs of R in deadline order at speed s on [t, e);  output the piece;  t ← e
L8  return the pieces and the completion times
```

Line L5 is the first step of the YDS algorithm for jobs with a common release time. The full YDS algorithm is not needed, since all known jobs are already released.

## Example

Take three jobs, written as (release, work, deadline): $A = (0, 4, 4)$, $B = (1, 3, 3)$ and $C = (2, 2, 6)$.

| time | known unfinished work | prefix densities $P_k / (d_k - t)$ | speed | until |
|---|---|---|---|---|
| 0 | $A$: 4 | $4/4 = 1$ | 1 | 1 (release of $B$) |
| 1 | $B$: 3, $A$: 3 | $3/2$, $6/3 = 2$ | 2 | 2 (release of $C$) |
| 2 | $B$: 1, $A$: 3, $C$: 2 | $1/1$, $4/2 = 2$, $6/4$ | 2 | 4 (deadline of $A$) |
| 4 | $C$: 2 | $2/2 = 1$ | 1 | 6 |

The jobs complete at $C_B = 5/2$, $C_A = 4$ and $C_C = 6$. The optimal schedule runs at $7/4$ on $[0, 4)$ and at 1 on $[4, 6)$.

| $\alpha$ | OA energy | AVR energy | optimal energy | OA ratio |
|---|---|---|---|---|
| 2 | 15 | 19 | $57/4$ | $20/19 \approx 1.05$ |
| 3 | 27 | $189/4$ | $375/16$ | $432/375 \approx 1.15$ |

At time 0 OA does not know that $B$ will come, so it runs at speed 1, slower than the optimal $7/4$, and then it must run at speed 2 later.

## Correctness

Two facts show that OA is well defined and meets every deadline.

**The plan of line L5 is feasible.** Let $g = P_k / (d_k - t)$ be the maximum, with $k$ the largest index that attains it. For each $i \le k$, $P_i \le g (d_i - t)$, so EDF at speed $g$ finishes job $i$ by $t + P_i / g \le d_i$. In particular the first $k$ jobs finish exactly by $d_k$.

**The speed is constant until $e$, and no deadline is missed.** After running EDF at speed $g$ for a time $\varepsilon$, the remaining prefix sums are $P_i - g \varepsilon$ for the jobs not yet done, with deadlines $d_i - t - \varepsilon$ ahead. For $i \le k$ the ratio is at most $g$, it equals $g$ at $i = k$, and for $i > k$ it stays below $g$. So the plan computed at any time in $[t, e)$ has the same speed, and OA is the same as the rule "run at the speed of the optimal plan for the known work" at each moment. If $e = d_k$, the first $k$ jobs are done by their deadlines. If $e = t'$, every job that is unfinished at $t'$ has $d_i > t'$, because its planned completion time is later than $t'$ and at most $d_i$. So at each step all unfinished jobs have deadlines in the future, the maximum in line L5 is well defined, and each job completes by its deadline.

**Termination.** Each pass of line L4 ends either at a deadline $d_k$, where at least one job completes, or at the next release. So there are at most $2n$ passes.

## Complexity

- **Time.** There are at most $2n$ passes of line L4. Each pass sorts at most $n$ jobs and scans them, in $O(n \log n)$. The total is $O(n^2 \log n)$ in the worst case. Keeping the jobs in a balanced search tree by deadline and the prefix sums in an augmented tree reduces each pass, but the simple version is enough here.
- **Space.** The unfinished jobs and the output take $O(n)$.
- **Online cost.** At each release, OA does $O(n \log n)$ work to make the new plan.

## Properties

- **Online and feasible.** The speed depends only on the known work, and every job meets its deadline, as shown above.
- **Competitive ratio $\alpha^{\alpha}$.** Bansal, Kimbrel and Pruhs proved that OA uses at most $\alpha^{\alpha}$ times the optimal energy. Their proof uses the [potential function](/potential-function/) $\Phi = \alpha \sum_i s_i^{\alpha - 1} (w_{\text{OA}, i} - \alpha \, w_{\text{OPT}, i})$, where $s_i$ is the planned speed of OA on its $i$-th interval, $w_{\text{OA}, i}$ is the planned work there, and $w_{\text{OPT}, i}$ is the work of OPT that is not done and has its deadline there. This upper bound is cited here and not proved; the same argument for AVR is written out on [AVR competitive ratio](/avr-competitive-ratio/).
- **The ratio is exact.** Let work arrive at rate $a(t) = (1 - t)^{-1/\alpha}$ on $[0, 1 - \varepsilon]$, all with deadline 1, as the limit of many small jobs. Running at speed $a(t)$ is feasible and uses energy $\int_0^{1 - \varepsilon} (1 - t)^{-1} dt = \ln(1/\varepsilon)$, so OPT $\le \ln(1/\varepsilon)$. OA runs at $v(t) = W(t)/(1 - t)$, where $W$ is the remaining work, and $v'(t) = a(t)/(1 - t)$, so $v(t) = \alpha ((1 - t)^{-1/\alpha} - 1)$. Its energy on $[0, 1 - \varepsilon]$ is $\alpha^{\alpha} \int_{\varepsilon}^{1} u^{-1} (1 - u^{1/\alpha})^{\alpha} du = \alpha^{\alpha} (\ln(1/\varepsilon) - O(1))$. So the ratio tends to $\alpha^{\alpha}$ as $\varepsilon \to 0$. The tests check a discrete version, where the ratio grows slowly toward $\alpha^{\alpha}$.
- **Optimal for one release.** If all jobs are released at the same time, OA is the YDS schedule.
- **Same as AVR for a common deadline.** With one deadline for all jobs, OA and [AVR](/avr/) have the same speed at every time.

## Variants and improvements

- **AVR.** A simpler rule with ratio $2^{\alpha - 1} \alpha^{\alpha}$. See [AVR](/avr/).
- **BKP.** A rule with ratio $2 (\alpha / (\alpha - 1))^{\alpha} e^{\alpha}$, which is better than $\alpha^{\alpha}$ for $\alpha$ above about 4.2. See [BKP speed scaling](/bkp-speed-scaling/).
- **qOA.** Run at $q$ times the OA speed for a constant $q > 1$. With $q = 2 - 1/\alpha$, Bansal, Chan, Katz and Pruhs showed the ratio $4^{\alpha} / (2 \sqrt{e \alpha})$, which is better than OA for $\alpha = 3$ (about 11.2 against 27). This result is cited here and not proved.
- **Other objectives.** The same idea of planning for the known work and replanning at each arrival is used for flow time plus energy and for speed-bounded processors.

## When to use it

Use OA when a new plan at each arrival is affordable and the power exponent is small to moderate, such as $\alpha$ between 2 and 3. Its ratio of 27 for $\alpha = 3$ is much better than the 108 of AVR. For large $\alpha$, BKP has the better guarantee. If jobs arrive in bursts that are then quiet, OA is close to optimal, since it is optimal when no more jobs come.

## Pitfalls

- **Recomputing from the original work.** The plan uses the remaining work $\rho_j$, not $w_j$. Using $w_j$ runs too fast.
- **Ties in line L5.** Taking the largest index $k$ that attains the maximum makes the segment as long as possible. Taking a smaller one is also correct but splits the plan into more pieces.
- **Missing the next release.** The plan must stop at the next release time, even when the densest interval ends later.
- **Floating point.** The prefix densities are compared for equality in the tie rule. With floating point, a small error can change $k$ and split segments. Exact fractions avoid this.
- **No look ahead.** OA is not optimal when work keeps arriving with the same deadline. The lower bound family shows a loss close to $\alpha^{\alpha}$.

## Implementations

## History

Yao, Demers and Shenker proposed Optimal Available in 1995, together with AVR and the offline YDS algorithm, and they showed that its ratio is at least $\alpha^{\alpha}$. Bansal, Kimbrel and Pruhs proved the matching upper bound in 2004 (journal version 2007) with a potential function argument, the first analysis of its kind for speed scaling. They also gave the BKP algorithm. Bansal, Chan, Katz and Pruhs gave qOA in 2009.

## References
