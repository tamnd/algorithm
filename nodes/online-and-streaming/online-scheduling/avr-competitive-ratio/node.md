---
tag: 8ZQHN4
kind: theorem
slug: avr-competitive-ratio
name: AVR competitive ratio for energy
aliases:
- Yao-Demers-Shenker bound
- AVR is 2^(alpha-1) alpha^alpha competitive
area: online-and-streaming/online-scheduling
level: advanced
summary: With power function s^alpha, AVR is 2^(alpha-1) alpha^alpha competitive for energy.
prereqs: [avr, online-speed-scaling, potential-function, competitive-ratio]
see_also: [optimal-available, bkp-speed-scaling, yds-algorithm, convex-function, jensens-inequality, speed-scaling, edf-optimality]
sources:
  - paper: "F. Frances Yao, Alan Demers and Scott Shenker, A scheduling model for reduced CPU energy, FOCS 1995"
    locator: pages 374 to 382 (the upper bound 2^(alpha - 1) alpha^alpha for alpha at least 2, the reduction to bitonic inputs, and the lower bound alpha^alpha)
  - paper: doi:10.1007/s00453-009-9379-z
    title: Nikhil Bansal, David P. Bunde, Ho-Leung Chan and Kirk Pruhs, Average rate speed scaling, Algorithmica 60(4), 2011 (LATIN 2008)
    locator: pages 877 to 889, Section 4, Theorem 3 (the lower bound ((2 - delta) alpha)^alpha / 2) and Section 5, Lemmas 4 to 8 and Theorem 7 (the potential function proof)
  - paper: "Nikhil Bansal, Tracy Kimbrel and Kirk Pruhs, Speed scaling to manage energy and temperature, Journal of the ACM 54(1), 2007"
    locator: the potential function for Optimal Available and the inequality used in the arrival case (Lemma 8 of Bansal, Bunde, Chan and Pruhs)
---

## Statement

Let the power at speed $s$ be $P(s) = s^{\alpha}$ with a constant $\alpha > 1$. For every sequence $\sigma$ of jobs $(r_j, w_j, d_j)$ in [online speed scaling](/online-speed-scaling/), the energy of [AVR](/avr/) satisfies

$$\text{AVR}(\sigma) \le 2^{\alpha - 1} \alpha^{\alpha} \cdot \text{OPT}(\sigma),$$

where OPT$(\sigma)$ is the minimum energy of a feasible schedule, as computed by the [YDS algorithm](/yds-algorithm/). So AVR is $c$-competitive with $c = 2^{\alpha - 1} \alpha^{\alpha}$ and additive constant $b = 0$. For $\alpha = 2$ this is 8, and for $\alpha = 3$ it is 108. Yao, Demers and Shenker proved it for $\alpha \ge 2$; the proof below, by Bansal, Bunde, Chan and Pruhs, works for each $\alpha > 1$.

## In plain words

AVR runs each job at the same speed over its whole window and adds up these speeds. The theorem says that this simple rule never uses more than a fixed multiple of the least possible energy, and that multiple depends only on the power exponent. The factor has two parts. If the best schedule always runs every job ahead of AVR, or always behind it, AVR loses at most $\alpha^{\alpha}$. A general input splits into these two kinds of jobs, and adding two speeds before raising them to the power $\alpha$ costs at most another factor $2^{\alpha - 1}$.

## Proof

The full proof is in [proofs/potential.md](proofs/potential.md). Here is its structure.

Fix any feasible schedule $S$, for example an optimal one. Think of AVR as running each job $j$ at rate $\delta_j = w_j / (d_j - r_j)$ on its window; this gives the same speed, so the same energy. Call a job *type A* if $S$ has done at least as much of it as AVR at each time in its window, and *type B* if $S$ has done at most as much.

1. **Splitting.** If $S$ and AVR have done the same work $x$ on job $j$ at a time $t$ inside its window, replace $j$ by $(r_j, x, t)$ and $(t, w_j - x, d_j)$. Both new jobs have density $\delta_j$, so AVR's speed does not change, and $S$ stays feasible with the same energy. After finitely many splits, each job is of type A or of type B.
2. **Type A jobs.** For an input of type A jobs only, a [potential function](/potential-function/) $\Phi = \alpha \sum_i s_i^{\alpha - 1} (w_{\text{AVR}, i} - \alpha \, w_{S, i})$ over the future intervals between deadlines satisfies $s_{\text{AVR}}^{\alpha} + d\Phi/dt \le \alpha^{\alpha} s_S^{\alpha}$ at each time and does not increase at arrivals. Integrating gives AVR $\le \alpha^{\alpha} \cdot E(S)$.
3. **Type B jobs.** Reversing time turns the type B jobs into type A jobs, and AVR and $S$ keep their energies. So the same bound holds for them.
4. **Combining.** With $s_A$ and $s_B$ the AVR speeds on the two kinds, [convexity](/convex-function/) gives $(s_A + s_B)^{\alpha} \le 2^{\alpha - 1} (s_A^{\alpha} + s_B^{\alpha})$. And $E(S)$ is at least the sum of the energies of $S$ on each kind, since $(x + y)^{\alpha} \ge x^{\alpha} + y^{\alpha}$. Together, AVR $\le 2^{\alpha - 1} \alpha^{\alpha} E(S)$. $\blacksquare$

## Consequences

- **A constant ratio.** AVR has a ratio that depends only on $\alpha$, not on the number of jobs or the lengths of the windows.
- **Feasibility for free.** AVR also meets every deadline, as shown on the [AVR](/avr/) page, so the bound is about energy only.
- **The type A bound is the OA bound.** Step 2 is the same potential argument as the one that shows that [Optimal Available](/optimal-available/) is $\alpha^{\alpha}$-competitive. The extra factor $2^{\alpha - 1}$ is the cost of jobs that the optimum runs late.
- **Comparison.** For $\alpha = 3$, AVR is guaranteed 108, OA is guaranteed 27, and [BKP](/bkp-speed-scaling/) is guaranteed about 135.6. For large $\alpha$, BKP is the best of the three, because its ratio grows like $e^{\alpha}$ rather than $\alpha^{\alpha}$.

## Tightness

The bound is nearly tight. These lower bounds are cited and not proved.

| $\alpha$ | upper bound $2^{\alpha - 1} \alpha^{\alpha}$ | lower bound $\alpha^{\alpha}$ (YDS 1995) | lower bound $(\alpha + (\alpha - 1)^{1 - 1/\alpha})^{\alpha} / 2$ (BBCP) |
|---|---|---|---|
| 2 | 8 | 4 | 4.5 |
| 3 | 108 | 27 | about 48.3 |
| 4 | 2048 | 256 | about 777 |

- **The $\alpha^{\alpha}$ family.** Work arrives at rate $(1 - t)^{-1/\alpha}$ on $[0, 1)$, all with deadline 1. The optimum runs at the arrival rate, and AVR runs at about $\alpha$ times it, so the ratio tends to $\alpha^{\alpha}$. A discrete version with $n$ jobs is in the tests of the AVR page; the ratio grows slowly, like $\alpha^{\alpha}$ times $1 - O(1/\log n)$.
- **The BBCP family.** A second stream of work arrives late with later deadlines, so that AVR runs too fast in the short interval where both streams are open. With $c = \alpha - 1$, the ratio tends to $((2 - \delta) \alpha)^{\alpha} / 2$ with $\delta = 1 - (\alpha - 1)^{1 - 1/\alpha} / \alpha$, which tends to 0 as $\alpha$ grows. So the factor $2^{\alpha - 1}$ is needed, up to a factor about $\alpha^{1/2}$.
- **Easy inputs.** For a single job, or for windows that do not overlap, AVR is optimal. The loss comes only from overlapping windows.

## History

Yao, Demers and Shenker defined the model in 1995 and proved this bound for $\alpha \ge 2$, by a reduction to bitonic inputs and a direct analysis of each kind. They proved that the ratio is at least $\alpha^{\alpha}$ and conjectured that $\alpha^{\alpha}$ is the exact ratio. Bansal, Bunde, Chan and Pruhs disproved the conjecture in 2008 and replaced the analysis of each kind by the potential function of Bansal, Kimbrel and Pruhs for Optimal Available.

## References
