---
tag: EQYVHD
kind: theorem
slug: online-makespan-lower-bound
name: Lower bound for deterministic online makespan
aliases:
- Rudin-Chandrasekaran lower bound
- lower bounds for online makespan
- Faigle-Kern-Turan lower bound
area: online-and-streaming/online-scheduling
level: advanced
summary: "No deterministic online algorithm on identical machines beats 3/2 for m = 2 or 5/3 for m = 3, so list scheduling is optimal there; for many machines the best known lower bound is about 1.88."
prereqs: [online-makespan-minimization, adversary-argument]
see_also: [online-makespan-minimization, list-scheduling-competitive-ratio, identical-machines, adversary-argument, request-answer-game, competitive-ratio, preemptive-scheduling, online-restricted-assignment-lower-bound]
sources:
  - paper: "Ulrich Faigle, Walter Kern and Gyorgy Turan, On the performance of on-line algorithms for partition problems, Acta Cybernetica 9(2), 1989"
    title: Faigle, Kern and Turan 1989
    locator: the lower bounds 3/2 for m = 2, 5/3 for m = 3, and 1 + 1/sqrt(2) for m at least 4
  - paper: "Yair Bartal, Howard Karloff and Yuval Rabani, A better lower bound for on-line scheduling, Information Processing Letters 50(3), 1994"
    title: Bartal, Karloff and Rabani 1994
    locator: the lower bound 1.837 for m at least 3454
  - paper: "Susanne Albers, Better bounds for online scheduling, SIAM Journal on Computing 29(2), 1999"
    title: Albers 1999
    locator: the lower bound 1.852 for m at least 80
  - paper: "Todd Gormley, Nick Reingold, Eric Torng and Jeffery Westbrook, Generating adversaries for request-answer games, SODA 2000"
    title: Gormley, Reingold, Torng and Westbrook 2000
    locator: the computer search for adversaries and the lower bound about 1.854 for m at least 80
  - paper: "John F. Rudin III, Improved bounds for the on-line scheduling problem, PhD thesis, The University of Texas at Dallas, 2001"
    title: Rudin 2001, PhD thesis
    locator: the lower bound 1.88 for large m
  - paper: "John F. Rudin III and R. Chandrasekaran, Improved bounds for the online scheduling problem, SIAM Journal on Computing 32(3), 2003"
    title: Rudin and Chandrasekaran 2003
    locator: the lower bound sqrt(3) for m = 4
---

These lower bounds say how well any deterministic online algorithm can do for [online makespan minimization](/online-makespan-minimization/), $P \mid \mathrm{online\text{-}list} \mid C_{\max}$. For $m = 2$ the bound is $\frac32$ and for $m = 3$ it is $\frac53$, so [list scheduling](/list-scheduling-competitive-ratio/), with ratio $2 - \frac1m$, is optimal on two and three machines. For many machines the best known bound is about $1.88$, against the best known algorithm at about $1.9201$. This page proves the bounds for $m = 2$ and $m = 3$ with an [adversary argument](/adversary-argument/) and cites the others.

## Statement

**Notation.** The input is a list $\sigma$ of job sizes on $m$ identical machines. $\mathrm{ALG}(\sigma)$ is the makespan of the online algorithm and $\mathrm{OPT}(\sigma)$ the optimal makespan. An algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$ and a constant $b$.

**Theorem.** Let $A$ be a deterministic online algorithm for $P \mid \mathrm{online\text{-}list} \mid C_{\max}$, and let $c$ be its competitive ratio.

1. If $m \ge 2$, then $c \ge \frac32$ (Faigle, Kern and Turán 1989).
2. If $m = 3$, then $c \ge \frac53$ (Faigle, Kern and Turán 1989).
3. (Cited.) If $m \ge 4$, then $c \ge 1 + \frac1{\sqrt2} \approx 1.7071$ (Faigle, Kern and Turán 1989). If $m = 4$, then $c \ge \sqrt3 \approx 1.7321$ (Rudin and Chandrasekaran 2003). For $m \ge 80$, $c \ge 1.852$ (Albers 1999), and for large $m$, $c \ge 1.88$ (Rudin 2001).

Parts 1 and 2 hold for every additive constant $b$, and they are proved below.

## In plain words

The adversary watches the algorithm and picks the next job to hurt it. First it sends small equal jobs. If the algorithm stacks two of them on one machine, the adversary stops, and the algorithm looks bad against a schedule that spreads them. If the algorithm spreads them evenly, the adversary sends one big job, and every machine is already busy, so the big job lands on top of some work. On three machines the adversary does this twice, with medium jobs and then one large job. At every point where it may stop, the algorithm is worse than the optimum by the claimed factor.

## Proof

The algorithm is deterministic, so the adversary can compute its choice for each job before it chooses the next job. At each step the adversary either stops or gives one more job. It suffices to show that at some stop the ratio $\frac{\mathrm{ALG}}{\mathrm{OPT}}$ of the prefix is at least the claimed value. To include an additive constant $b$, play the same adversary with all sizes multiplied by $\lambda > 0$. The case analysis does not change, $\mathrm{ALG}$ and $\mathrm{OPT}$ at each stop are $\lambda$ times the values below, and for large $\lambda$ the term $b$ does not matter.

**Part 1: $\frac32$ for every $m \ge 2$.** Give $m$ jobs of size $1$.

- If $A$ puts two of them on one machine, stop. Then $\mathrm{ALG} \ge 2$ and $\mathrm{OPT} = 1$, a ratio of $2$.
- Otherwise each machine has load $1$. Give a job of size $2$. Wherever $A$ puts it, $\mathrm{ALG} = 3$. The optimum puts the big job alone and the $m$ unit jobs on the other $m - 1$ machines with at most two per machine, which is possible since $m \le 2(m - 1)$; it cannot be below $2$, the size of the big job. So $\mathrm{OPT} = 2$ and the ratio is $\frac32$.

For $m = 2$ the list is $(1, 1, 2)$.

**Part 2: $\frac53$ for $m = 3$.** Give three jobs of size $1$. If $A$ puts two on one machine, stop: the ratio is $2$. Otherwise the loads are $(1, 1, 1)$. Now give jobs of size $3$, one at a time, at most three of them, and stop as soon as $A$ puts one on a machine that already has a job of size $3$.

| step | jobs so far | loads of $A$ if it spreads | $\mathrm{OPT}$ | if $A$ stacks, it gets | ratio at the stop |
|---|---|---|---|---|---|
| 4 | $1, 1, 1, 3$ | $(4, 1, 1)$ | $3$ | (no stacking possible) | |
| 5 | $1, 1, 1, 3, 3$ | $(4, 4, 1)$ | $3$ | $7$ | $\frac73$ |
| 6 | $1, 1, 1, 3, 3, 3$ | $(4, 4, 4)$ | $4$ | $7$ | $\frac74$ |
| 7 | $1, 1, 1, 3, 3, 3, 6$ | $(10, 4, 4)$ | $6$ | | $\frac{10}{6} = \frac53$ |

The optimal values come from these schedules. For step 5: $\{3\}, \{3\}, \{1, 1, 1\}$, and $3$ is the size of the largest job. For step 6: $\{3, 1\}, \{3, 1\}, \{3, 1\}$, and $4$ is the average load $\frac{12}{3}$. For step 7: $\{6\}, \{3, 3\}, \{3, 1, 1, 1\}$, and $6$ is the average load $\frac{18}{3}$.

At step 5 or step 6, a job of size 3 on a machine of load 4 gives $\mathrm{ALG} = 7$, and the ratios $\frac73$ and $\frac74$ are both at least $\frac53$. If $A$ spreads all three jobs of size 3, the loads are $(4, 4, 4)$, and the last job of size $6$ gives $\mathrm{ALG} = 10$ wherever it goes. In each branch the ratio is at least $\frac53$. $\square$

**The proof as a game tree.** Because the machines are identical, the state of the game is the sorted load vector. The adversary for $m = 3$ is a tree with four stop points: after the unit jobs, after the second and third jobs of size $3$, and after the job of size $6$. A deterministic algorithm chooses one path through it, and every leaf has ratio at least $\frac53$.

## Consequences

- **List scheduling is optimal for $m = 2$ and $m = 3$.** Its ratio is $2 - \frac1m$, which is $\frac32$ and $\frac53$ ([Graham's bound](/list-scheduling-competitive-ratio/)). So the optimal deterministic ratios are exactly $\frac32$ and $\frac53$.
- **For $m \ge 4$ the question is open.** The best known algorithm has ratio about $1.9201$ ([problem page](/online-makespan-minimization/)), and the lower bounds reach about $1.88$ for large $m$. For $m = 4$ the lower bound is $\sqrt3 \approx 1.732$, and the algorithm of Galambos and Woeginger is below $2 - \frac14 = 1.75$.
- **Far from the offline optimum.** Every lower bound above is at least $\frac32$, so no deterministic online algorithm gets close to the offline PTAS.
- **Randomization and preemption change the answer.** Against an oblivious adversary the randomized ratio on two machines is $\frac43$, and with preemption it is also $\frac43$; the proof for the preemptive case is on the [preemptive scheduling](/preemptive-scheduling/) page.

## Tightness

Parts 1 and 2 are tight: list scheduling reaches $\frac32$ on two machines and $\frac53$ on three. Part 1 is not tight for $m \ge 3$: on three machines the bound is $\frac53$, not $\frac32$. For large $m$ the gap between $1.88$ and $1.9201$ remains. The adversaries for large $m$ use many more rounds, and some of them were found with computer help (Gormley, Reingold, Torng and Westbrook 2000).

## History

Faigle, Kern and Turán (1989) proved the bounds for $m = 2$ and $m = 3$, and $1 + \frac1{\sqrt2}$ for $m \ge 4$. Bartal, Karloff and Rabani (1994) gave the first bound above $1.8$, namely $1.837$ for $m \ge 3454$. Albers (1999) proved $1.852$ for $m \ge 80$, Gormley, Reingold, Torng and Westbrook (2000) about $1.854$ with computer-generated adversaries, and Rudin (2001, PhD thesis) $1.88$ for large $m$. Rudin and Chandrasekaran (2003) proved $\sqrt3$ for $m = 4$. The alias of this page names that last line of work.

## References
