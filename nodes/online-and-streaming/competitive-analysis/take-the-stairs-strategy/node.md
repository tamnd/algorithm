---
tag: F0PJDM
kind: algorithm
slug: take-the-stairs-strategy
name: Take-the-stairs strategy
area: online-and-streaming/competitive-analysis
level: intro
summary: Online strategy for deciding between stairs and elevator without knowing the wait, used to illustrate competitive analysis.
solves: [ski-rental-problem]
model: word-ram
complexity:
  vars: {e: the elevator ride time, s: the stair time}
  time: {worst: O(1)}
  space: {extra: O(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [ski-rental-problem, break-even-strategy]
see_also: [competitive-ratio, online-algorithm, offline-optimum, randomized-online-algorithm, linear-search-problem]
sources:
  - url: "https://www.cs.cmu.edu/~avrim/451f13/lectures/lect1107.pdf"
    title: Avrim Blum, 15-451 Algorithms lecture notes, Lecture 22, Online algorithms, Carnegie Mellon University, Fall 2013
    locator: Section 22.2, the elevator problem, and the rent-or-buy problem in the same lecture
  - paper: doi:10.1007/BF01189993
    title: "Anna R. Karlin, Mark S. Manasse, Lyle A. McGeoch and Susan Owicki, Competitive randomized algorithms for nonuniform problems, Algorithmica 11(6) (1994), 542-571"
    locator: the continuous rent-or-buy decision (spin or block), where waiting is paid by the unit of time
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: the rent-or-buy examples of competitive analysis
---

The take-the-stairs strategy is an online rule for a person who waits for an elevator and does not know when it will come: wait for $S - E$ time units, where $E$ is the time of the elevator ride and $S$ is the time to walk up the stairs, and then take the stairs. It reaches the top at most $2 - E/S$ times later than a person who knew the arrival time of the elevator, and no deterministic rule does better. It is a teaching version of the [ski rental problem](/ski-rental-problem/) in continuous time, used in lecture notes on [competitive analysis](/competitive-ratio/) (for example Blum, CMU 15-451); the name is not a standard term in the research literature.

## In plain words

You want to go up to an office on a high floor. You press the button for the elevator, but you do not know when it will come. The elevator is fast once it is here. The stairs are slow, but you can start at once.

If you wait too short a time, you climb the stairs, and the elevator comes a moment later. If you wait too long, you waste time for an elevator that never comes. The rule says: wait for as long as the stairs are slower than the elevator ride, and then walk. If the elevator comes during this wait, you take it and you are never late. If it does not come, you lose the waiting time, but you lose it only once. So you are never more than twice as slow as a person who knew when the elevator would come.

## The problem

**Notation.** $\sigma$ is the input (here, the arrival time $t$ of the elevator), $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the times of the online rule and of the optimal offline rule, and $c$ is the competitive ratio.

The elevator arrives at an unknown time $t \in [0, \infty]$, where $t = \infty$ means that it never comes. A ride takes $E \ge 0$ after the elevator arrives, and the stairs take $S > 0$ from the moment the person starts to walk. While waiting, the person sees only that the elevator has not come yet. A deterministic online rule is a wait limit $w \ge 0$: take the elevator if $t \le w$, and take the stairs at time $w$ otherwise. Its time is

$$\mathrm{ALG}_w(t) = \begin{cases} t + E & \text{if } t \le w, \\ w + S & \text{if } t > w. \end{cases}$$

The offline optimum knows $t$ and chooses the faster way: $\mathrm{OPT}(t) = \min(t + E, S)$.

The relation with ski rental: waiting is renting (each unit of time costs 1), walking is buying (it costs $S$ and ends the problem), and the arrival of the elevator is the end of the season, except that it adds the ride time $E$. Because of $E$, the break-even point is $S - E$, not $S$.

## The algorithm

```pseudo id=main
TAKE-THE-STAIRS(E, S)                 ▷ elevator ride E, stairs S
L1  if E ≥ S then take the stairs now
L2  w ← S − E
L3  wait for the elevator, for at most time w
L4  if the elevator came at a time t ≤ w then ride it: arrive at t + E
L5  else take the stairs at time w: arrive at w + S
```

If $E \ge S$, the stairs are never slower than the elevator, and line L1 walks at once with time $S = \mathrm{OPT}$.

## Example

Take $E = 15$ seconds and $S = 45$ seconds, as in the lecture notes of Blum. The rule waits $w = 30$ seconds.

| elevator arrives at $t$ | rule | $\mathrm{ALG}$ | $\mathrm{OPT}$ | ratio |
|---|---|---|---|---|
| 10 | elevator | 25 | 25 | 1 |
| 30 | elevator | 45 | 45 | 1 |
| 31 | stairs at 30 | 75 | 45 | $5/3$ |
| never | stairs at 30 | 75 | 45 | $5/3$ |

So the worst ratio is $5/3 = 2 - 15/45$. Other wait limits are worse. The exact worst ratios, over all arrival times, are:

| wait limit $w$ | 0 | 10 | 20 | 30 | 40 | 60 |
|---|---|---|---|---|---|---|
| worst ratio | $3$ | $11/5$ | $13/7$ | $5/3$ | $17/9$ | $7/3$ |

For $w < 30$ the worst ratio is a supremum that is not reached: it is the limit as the elevator arrives just after the person leaves. For $w = 0$ it is $S/E = 3$.

## Correctness

For $E < S$ and $w = S - E$:

- If $t \le w$, then $t + E \le S$, so the rule takes the elevator and $\mathrm{ALG} = t + E = \mathrm{OPT}$.
- If $t > w$, then $t + E > S$, so $\mathrm{OPT} = S$, and $\mathrm{ALG} = (S - E) + S = 2S - E$. The ratio is $2 - E/S$.

So $\mathrm{ALG}(t) \le (2 - E/S) \cdot \mathrm{OPT}(t)$ for every $t$, with equality for every $t > S - E$. Every other wait limit has a larger worst ratio: if the elevator comes just after $w$, the ratio tends to $(w + S)/\min(w + E, S)$, which is larger than $2 - E/S$ for $w \ne S - E$. The full proof is below.

## Complexity

The rule computes one number, $S - E$, and makes one decision when the wait ends or the elevator comes. Time and extra space are $O(1)$.

## Properties

- **Online and deterministic.** The decision at each moment depends only on whether the elevator has come.
- **Strictly competitive.** The ratio $2 - E/S$ holds with no additive term. It is less than 2, and it tends to 2 as $E/S$ tends to 0.
- **Optimal among deterministic rules.** The wait limit $S - E$ is the unique best one.
- **Worst case reached.** The bound is reached whenever the elevator comes after the person has left, or never.

## Variants and improvements

- **Ski rental in continuous time.** With $E = 0$, the problem is continuous ski rental with buy price $S$: wait until the waiting time equals $S$, then walk, for ratio 2. See the [break-even strategy](/break-even-strategy/).
- **Randomized waiting.** As in ski rental, a random wait limit gives a better expected ratio against an [oblivious adversary](/oblivious-adversary/). See [randomized online algorithm](/randomized-online-algorithm/) for the method.
- **Known distribution.** If the arrival time of the elevator has a known distribution, the wait limit that minimizes the expected time can be computed from it. This is an average-case problem, not a competitive one.
- **Searching instead of waiting.** In the [linear search problem](/linear-search-problem/), the walker does not wait but moves, and the unknown is a position instead of a time. The doubling strategy there plays the role of the break-even rule here.

## When to use it

Use the rule as the first example of competitive analysis, because the numbers are small and the proof is two lines. In practice, the same structure appears in any choice between waiting for a fast resource that may come and switching to a slow resource that is always there: wait for a lock or do other work, wait for a network reply or use a cached value, wait for a bus or walk.

## Pitfalls

- **Waiting $S$ instead of $S - E$.** The break-even point of ski rental is the buy price. Here the person also pays the ride after the elevator comes, so the break-even point is $S - E$. Waiting $S$ gives ratio $(2S)/S = 2$, which is worse than $2 - E/S$.
- **Taking the stairs at once.** Waiting 0 looks safe, but the elevator may come right after the person leaves; the ratio tends to $S/E$, which is large when the ride is short.
- **Waiting forever.** If the elevator never comes, the ratio is unbounded.
- **Reading the name as a literature term.** "Take the stairs" is a name for this teaching example. Research papers call the general problem ski rental or rent or buy.

## Implementations

## History

The elevator version of rent or buy is a common classroom example of competitive analysis. Avrim Blum's lecture notes for the course 15-451 at Carnegie Mellon present it with $E = 15$ and $S = 45$ next to the rent-or-buy problem. The continuous rent-or-buy decision itself, where waiting is paid by the unit of time, was analysed by Karlin, Manasse, McGeoch and Owicki (1994) for spin or block.

## References
