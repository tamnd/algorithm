---
tag: MN6FJG
kind: technique
slug: pareto-ranking
name: Pareto ranking
aliases:
- Goldberg ranking
- rank-based fitness
- dominance ranking
- dominance count ranking
area: optimization/multi-objective
level: core
summary: Give each member of a population a scalar rank from Pareto dominance alone, so that all non-dominated members get the best rank and a dominating member always ranks better.
prereqs: [pareto-dominance, non-dominated-sorting]
see_also: [moga, nsga-ii, spea2, npga, crowding-distance, multi-objective-evolutionary-algorithm, fitness-function]
sources:
  - book: isbn:9780201157673
    title: David E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning, Addison-Wesley, 1989
    locator: Chapter 5, the proposal to rank a population by successive non-dominated sets
  - paper: "Carlos M. Fonseca and Peter J. Fleming, Genetic algorithms for multiobjective optimization: formulation, discussion and generalization, Proceedings of the Fifth International Conference on Genetic Algorithms, Morgan Kaufmann, 1993, 416-423"
    locator: the rank as one plus the number of dominating individuals, and the fitness interpolation by rank
  - paper: "Eckart Zitzler, Marco Laumanns and Lothar Thiele, SPEA2: Improving the strength Pareto evolutionary algorithm, TIK-Report 103, ETH Zurich, 2001"
    locator: Section 3.1, the strength S(i) and the raw fitness R(i)
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 5, non-elitist multi-objective evolutionary algorithms (MOGA, NSGA and NPGA)
  - paper: "Jon L. Bentley, H. T. Kung, Mario Schkolnick and Clark D. Thompson, On the average number of maxima in a set of vectors and applications, Journal of the ACM 25(4), 1978, 536-543"
    locator: the expected number of maxima of N random vectors
---

Pareto ranking turns the objective vectors of a population into one scalar rank per member, using only [Pareto dominance](/pareto-dominance/). The rank replaces the [fitness](/fitness-function/) of a single-objective [genetic algorithm](/genetic-algorithm/), so that selection favors the non-dominated members without any weights on the objectives. The three common rules are the front number of [non-dominated sorting](/non-dominated-sorting/) (Goldberg), one plus the number of dominators (Fonseca and Fleming, used in [MOGA](/moga/)), and the sum of the strengths of the dominators (used in [SPEA2](/spea2/)). Each takes $O(p N^2)$ time for $N$ members with $p$ objectives.

## In plain words

A genetic algorithm needs one number per member to pick parents. With several costs there is no single number, and adding the costs with weights forces a choice that the user may not want to make. Pareto ranking avoids weights. A member that no other member beats gets the best grade. A member that is beaten gets a worse grade.

There are a few ways to grade the beaten members. You can peel the population in layers and use the layer number. You can count how many members beat it. You can add up how strong its attackers are. All of these agree on two points: the unbeaten members get the best grade, and if one member beats another, it gets a better grade.

## When it applies

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$. We write $a \prec b$ when $a$ dominates $b$.

Use Pareto ranking when:

- the problem has $p \ge 2$ objectives and the goal is a set of trade-offs, not one point (see [multi-objective optimization](/multi-objective-optimization/));
- the method needs a scalar fitness, such as [tournament selection](/tournament-selection/) or [roulette wheel selection](/roulette-wheel-selection/);
- the user cannot give weights in advance, or the [Pareto front](/pareto-front/) may be non-convex, where a [weighted sum](/weighted-sum-method/) misses points.

It works best for $p = 2$ or $3$. For larger $p$, most members of a population are mutually non-dominated, and the rank no longer separates them (see the pitfalls).

## The template

```pseudo id=main
PARETO-RANK-FITNESS(x[1 .. N])
L1  for i ← 1 to N do y[i] ← f(x[i])
L2  for each pair i ≠ j do record whether y[i] ≺ y[j]          ▷ O(p N^2) tests
L3  for i ← 1 to N do r[i] ← RANK(i)                           ▷ hole: the rank rule
L4  for i ← 1 to N do d[i] ← DENSITY(i)                        ▷ hole: crowding, sharing, kNN
L5  sort the members by (r[i], −d[i])                          ▷ smaller rank first, then less crowded
L6  give fitness by position in this order, or select from it  ▷ hole: the selection scheme
```

The holes are the rank rule, the density estimate and the selection scheme. The rank rules are:

| rule | RANK(i) | used in |
|---|---|---|
| Goldberg (front number) | the $k$ with $i \in F_k$, the $k$-th non-dominated front | NSGA, [NSGA-II](/nsga-ii/), [NSGA-III](/nsga-iii/) |
| Fonseca and Fleming (dominance count) | $1 + \lvert\{ j : y^j \prec y^i \}\rvert$ | [MOGA](/moga/) |
| SPEA2 raw fitness (dominance strength) | $\sum_{j : y^j \prec y^i} S(j)$, with $S(j) = \lvert\{ k : y^j \prec y^k \}\rvert$ | [SPEA2](/spea2/) |

**Proposition.** Let $r$ be any of the three rules, and let $r^* = 1$ for the first two rules and $r^* = 0$ for the third.
1. $r(i) = r^*$ if and only if no member dominates $y^i$.
2. If $y^i \prec y^j$, then $r(i) < r(j)$.
3. The Goldberg rank is at most the Fonseca-Fleming rank.

*Proof.* (1) For the dominance count and the strength sum, the value is $r^*$ exactly when the set of dominators is empty; each strength $S(j)$ of a dominator $j$ is at least 1, because $j$ dominates $i$. The first front is the set of members with no dominator.
(2) Let $D(i)$ be the set of dominators of $i$. By transitivity, $D(i) \subseteq D(j)$, and $i \in D(j) \setminus D(i)$, because the order is irreflexive. So the dominance count of $j$ is larger by at least one, and the strength sum of $j$ is larger by at least $S(i) \ge 1$. For the front number, $j$ is not in the first front that contains $i$ or an earlier one, because $i$ is still present when those fronts are formed; the proof is Lemma 1(b) in the [non-dominated sorting](/non-dominated-sorting/) proof.
(3) A member of front $k \ge 2$ has a dominator in front $k - 1$ (Lemma 1(c) of the same proof). Repeating this gives a chain $y^{j_1} \prec \cdots \prec y^{j_{k-1}} \prec y^i$ of $k - 1$ distinct members, and all of them dominate $y^i$ by transitivity. So the count is at least $k - 1$, and the Fonseca-Fleming rank is at least $k$. $\square$

Part 2 is the reason to rank by dominance: selection by any of these ranks can never prefer a dominated member to the member that dominates it. Part 1 shows the limit: all non-dominated members tie, so a density term (line L4) is needed to spread them along the front.

### A worked example

Take the eight points $A = (1, 8)$, $B = (2, 5)$, $C = (3, 6)$, $D = (4, 2)$, $E = (5, 4)$, $F = (6, 7)$, $G = (7, 1)$, $H = (8, 3)$ from the [non-dominated sorting](/non-dominated-sorting/) page.

| point | dominated by | strength $S$ | front number | Fonseca-Fleming rank | SPEA2 raw fitness |
|---|---|---|---|---|---|
| A (1, 8) | none | 0 | 1 | 1 | 0 |
| B (2, 5) | none | 2 | 1 | 1 | 0 |
| C (3, 6) | B | 1 | 2 | 2 | 2 |
| D (4, 2) | none | 3 | 1 | 1 | 0 |
| E (5, 4) | D | 1 | 2 | 2 | 3 |
| F (6, 7) | B, C, D, E | 0 | 3 | 5 | 7 |
| G (7, 1) | none | 1 | 1 | 1 | 0 |
| H (8, 3) | D, G | 0 | 2 | 3 | 4 |

The rules disagree on the order of the dominated points. By front number, $C$, $E$ and $H$ tie. By dominance count, $C$ and $E$ come before $H$. By strength, $C$ comes before $E$, and $E$ before $H$, because $D$ dominates three points and so counts more than $B$.

## Classic examples

- **[MOGA](/moga/)** (Fonseca and Fleming, 1993) ranks by dominance count, maps ranks to fitness by interpolation, averages the fitness inside each rank, and adds fitness sharing.
- **NSGA and [NSGA-II](/nsga-ii/)** rank by front number. NSGA-II computes the fronts with the fast [non-dominated sort](/non-dominated-sorting/) and breaks ties by [crowding distance](/crowding-distance/).
- **[NPGA](/npga/)** (Horn, Nafpliotis and Goldberg, 1994) does not rank the whole population. It ranks two candidates against a random comparison set inside a tournament.
- **[SPEA](/spea/) and [SPEA2](/spea2/)** rank by strength, with an external archive. SPEA2 adds a $k$-th nearest neighbor density to the raw fitness.
- **[NSGA-III](/nsga-iii/)** keeps the front number and replaces the crowding distance by niching around reference directions, for many objectives.

## Variations

- **Dominance depth, rank and count.** The front number is also called the dominance depth, the Fonseca-Fleming value the dominance rank, and the strength sum the dominance count of SPEA2. Some authors use these names in other ways, so check the formula.
- **Constrained dominance.** Deb et al. rank a feasible point before an infeasible one, and two infeasible points by their total violation. The rank rules above apply to this relation unchanged, because it is still a strict partial order.
- **Relaxed dominance.** [Epsilon-dominance](/epsilon-dominance/) and other relaxations make more pairs comparable when $p$ is large.
- **Indicator-based ranking.** Methods such as SMS-EMOA rank the members of the last front by their contribution to the [hypervolume](/hypervolume-indicator/), which is also consistent with dominance.

## Pitfalls

- **Many objectives.** Let the $N$ points have independent coordinates with a continuous distribution. For $p = 2$, sort by the first coordinate; the $i$-th point is non-dominated exactly when its second coordinate is the smallest of the first $i$, which has probability $1/i$. So the expected size of the first front is $H_N = \sum_{i=1}^N 1/i$, about $5.19$ for $N = 100$. Bentley, Kung, Schkolnick and Thompson (1978) showed that for fixed $p$ the expected number is $\Theta(\ln^{p-1} N)$, which grows fast with $p$ for the population sizes in use. With many objectives, nearly all members get rank 1 and selection depends only on the density term.
- **Ties inside a front.** Ranking alone makes the population drift along the front, by genetic drift, to a few regions. Always pair the rank with a density estimate.
- **Comparing ranks across rules.** A dominance count of 3 and a front number of 3 mean different things. Do not mix them in one population.
- **Cost.** Each rule needs the full dominance relation, $O(p N^2)$ time. Do not recompute it for each tournament; compute it once per generation.

## Exercises

1. Give a set of $N$ points in which the Fonseca-Fleming rank of some point is $N$ but its front number is $2$. *Answer:* take $N - 1$ mutually non-dominated points that all dominate one last point, for example $(t, N - 1 - t)$ for $t = 0, \ldots, N - 2$ and the point $(N, N)$.
2. Show that the strength sum of SPEA2 can rank a point of front 2 after a point of front 3. *Answer:* take $a = (0, 10)$, $b = (1, 11)$, $c_i = (2, 11 + i)$ for $i = 1, \ldots, m$ with $m \ge 3$, and $d = (5, 5)$, $e = (6, 6)$, $g = (7, 7)$. Only $a$ dominates $b$, and $a$ dominates $b$ and all $c_i$, so $b$ is in front 2 with raw fitness $S(a) = m + 1 \ge 4$. The point $g$ is in front 3, and only $d$ and $e$ dominate it, so its raw fitness is $S(d) + S(e) = 2 + 1 = 3$.
3. Prove that the three rules give the same order on a population that is a chain $y^1 \prec y^2 \prec \cdots \prec y^N$.

## References
