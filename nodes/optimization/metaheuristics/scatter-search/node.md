---
tag: GRJBJP
kind: algorithm
slug: scatter-search
name: Scatter search
area: optimization/metaheuristics
level: advanced
summary: Combine a small set of diverse reference solutions to generate new ones.
model: word-ram
complexity:
  vars: {n: the number of items, P: the number of solutions in the first pool, b: the size of the reference set, I: the number of rounds}
  time: {worst: O(n log n + P b n + I b^2 (n + b))}
  space: {extra: O((P + b^2) n)}
properties: {deterministic: false, recursive: false}
prereqs: [local-search, local-optimum, knapsack-problem, hamming-distance]
see_also: [path-relinking, genetic-algorithm, population-based-search, intensification-and-diversification, tabu-search, grasp, memetic-algorithm, crossover]
sources:
  - paper: "Fred Glover, Heuristics for integer programming using surrogate constraints, Decision Sciences 8(1), 1977"
    locator: pp. 156 to 166 (the first form of scatter search, combining reference points by weighted combinations)
  - paper: "Fred Glover, A template for scatter search and path relinking, in J.-K. Hao and others (editors), Artificial Evolution, Lecture Notes in Computer Science 1363, Springer, 1998"
    locator: pp. 13 to 54 (the five methods of the template)
  - paper: "Fred Glover, Manuel Laguna and Rafael Martí, Fundamentals of scatter search and path relinking, Control and Cybernetics 29(3), 2000"
    locator: pp. 653 to 684 (the reference set of quality and diverse solutions, subset generation, combination and update)
  - paper: "Rafael Martí, Manuel Laguna and Fred Glover, Principles of scatter search, European Journal of Operational Research 169(2), 2006"
    locator: pp. 359 to 372 (the basic design, static and dynamic reference set updates, rebuilding)
  - book: isbn:9780792381877
    title: Fred Glover and Manuel Laguna, Tabu Search, Kluwer Academic Publishers, 1997
    locator: the chapter on scatter search and path relinking
---

Scatter search is a population-based [metaheuristic](/metaheuristic/) that keeps a small *reference set* of good and diverse solutions and builds new solutions by combining them in pairs. Each new solution is made feasible and improved, and it enters the reference set if it is better than the worst member. The search stops when a whole round of combinations adds nothing. Glover described the first form in 1977 for integer programming, and gave the standard template of five methods in 1998. Unlike a [genetic algorithm](/genetic-algorithm/), scatter search keeps few solutions, combines them by systematic rules rather than at random, and chooses part of the reference set for diversity, not for quality. It has no guarantee of finding an optimum.

## In plain words

Keep a short list of solutions. Half of them are the best you have found. The other half are chosen to be as different as possible from the rest, even if they are not very good.

Now take every pair from the list and mix the two into a new solution. The mixed solution may break the rules, so fix it, and then make it better with a simple local step. If it beats the worst solution on the list, it takes that place. Repeat with the pairs that have a new member. When no new solution gets onto the list, stop and return the best one.

The different solutions matter. Mixing two near copies gives the same solution again, but a poor and different solution can bring in a part that the good ones lack.

## The problem

The page shows scatter search on the 0-1 [knapsack problem](/knapsack-problem/). The input is $n$ items with values $v_i > 0$ and weights $w_i > 0$, a capacity $C$, the size $P$ of the first pool, the numbers $b_1 \ge 1$ of quality members and $b_2 \ge 0$ of diverse members of the reference set, and a source of random bits. A solution $x \in \{0, 1\}^n$ is feasible if its weight is at most $C$. The output is a feasible solution of high value. The aim is a solution of the largest value, which scatter search cannot prove it has found.

## The algorithm

```pseudo id=main
SCATTER-SEARCH(v, w, C, P, b1, b2)
L1  D ← P random 0-1 vectors, each made feasible by REPAIR and then IMPROVE; drop copies
L2  R ← the b1 best of D, then b2 more of D, each time the one farthest from R
L3  repeat
L4      N ← empty
L5      for each pair x, y in R with at least one new member do
L6          u ← x OR y;  d ← x AND y          ▷ (x + y)/2 rounded up and down
L7          add IMPROVE(REPAIR(u)) and IMPROVE(REPAIR(d)) to N
L8      for each z in N, best first do
L9          if z ∉ R and v(z) > v(worst member of R) then replace the worst member of R by z
L10 until no solution entered R
L11 return the best solution in R
```

The five methods of Glover's template are all here. The *diversification generation method* is the random vectors of line L1. The *improvement method* is IMPROVE. The *reference set update method* is line L2 for the first set and line L9 later. The *subset generation method* is line L5, which takes the pairs, and skips pairs of two old members, since they were combined before. The *solution combination method* is line L6.

REPAIR removes packed items, the lowest value per unit of weight first, until the weight is at most $C$. IMPROVE then goes once through the items, the highest value per unit of weight first, and packs each item that fits. Its result is *maximal*: no unpacked item fits. In line L2, the distance is the [Hamming distance](/hamming-distance/), and the distance of a solution from $R$ is its distance to the nearest member.

The combination at line L6 is a rounding. The midpoint $(x + y)/2$ has entries 0, 1/2 and 1. Rounding the halves up gives the union $x$ OR $y$, which packs every item of either parent and is often too heavy; rounding them down gives the intersection $x$ AND $y$, which packs only the shared items and has room to fill.

## Example

Take 7 items and capacity $C = 21$.

| item | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| value $v_i$ | 8 | 16 | 16 | 12 | 18 | 9 | 18 |
| weight $w_i$ | 10 | 4 | 10 | 10 | 5 | 2 | 2 |
| $v_i / w_i$ | 0.8 | 4 | 1.6 | 1.2 | 3.6 | 4.5 | 9 |

By enumeration, the best value is 68, at 0110101 only (items 1, 2, 4 and 6, of weight exactly 21). Here a solution is written as the bits $x_0 x_1 \ldots x_6$. The greedy solution by value per weight packs items 6, 5, 1 and 4 and then nothing else fits: 0100111, of value 61.

Run with $P = 6$, $b_1 = 2$, $b_2 = 2$ and seed 0 (Python `random.Random(0)`). The six random vectors give five distinct maximal solutions: 0100111 (61), 1100101 (60), 0110011 (59), 1000111 (53) and 1010000 (24). The two best enter $R$. Of the rest, 1010000 is at distance 6 from 0100111 and 4 from 1100101, so its distance from $R$ is 4, the largest; it enters $R$ although its value is the lowest. The other two are then both at distance 2 from $R$, and the tie goes to the earlier one in the pool, 0110011. So

$$R = \{0100111\ (61),\ 1100101\ (60),\ 1010000\ (24),\ 0110011\ (59)\}.$$

Round 1 combines all 6 pairs. Most children are again 0100111 or 0110011. The pair 1100101 and 1010000 gives the union 1110101 of weight 31. REPAIR removes item 0, the item of the lowest ratio, and the weight is now 21, so it stops at 0110101 of value 68; IMPROVE finds no item that fits. This child is not in $R$ and beats the worst member 1010000 (24), so it replaces it:

$$R = \{0100111\ (61),\ 1100101\ (60),\ 0110101\ (68),\ 0110011\ (59)\}.$$

Round 2 combines the three pairs that contain 0110101. Each of their six children is already in $R$, so the search stops and returns 0110101, the optimum. The poor member 1010000 brought item 2 into the union, and item 2 is in the optimum but in neither of the two best initial solutions.

On this one instance, with these parameters and the 100 seeds 0 to 99, 36 runs ended at 68, and in 33 of them the optimum was already in the first reference set. With $b_1 = 4$ and $b_2 = 0$ the counts were 33 and 33: the combinations found nothing new without the diverse members. This is one small instance and shows only what can happen.

## Correctness

Scatter search has no optimality guarantee, so "correct" means the following. Every member of $R$ is feasible and maximal, because every solution that enters $R$ has passed through REPAIR and IMPROVE: REPAIR stops once the weight is at most $C$, which happens at the latest when the knapsack is empty, and IMPROVE packs only items that fit. The members of $R$ are distinct. Each replacement raises the total value of $R$ by at least 1 and never lowers its best value, and every round that does not stop makes a replacement, so the search stops after at most $b \sum_i v_i$ rounds. The result is the best member of the final $R$. The [full proof](proofs/correctness.md) gives all steps.

## Complexity

Sorting the items by ratio takes $O(n \log n)$ time, and then REPAIR and IMPROVE take $O(n)$ each, with a running weight. Line L1 takes $O(P n)$. Line L2 picks $b$ members; with the distance of each pool solution to $R$ kept up to date, each pick costs $O(P n)$, so $O(P b n)$ in all. A round makes at most $b^2$ children at $O(n)$ each, and the update checks each child against $R$, by hashing in $O(n)$ and finding the worst member in $O(b)$. So the time is $O(n \log n + P b n + I b^2 (n + b))$ for $I$ rounds, where $b = b_1 + b_2$. The proof bounds $I$ by $b \sum_i v_i$, which is not polynomial; in practice the search stops after few rounds. The extra space is $O((P + b^2) n)$ for the pool and the children of one round.

## Properties

- **Randomized start, deterministic rounds.** Only line L1 uses random bits here. Glover's template also allows a systematic diversification generator with no random choices.
- **Small population.** The reference set often has about 10 members, far fewer than the population of a typical genetic algorithm.
- **Quality and diversity.** Part of $R$ is chosen for distance, not value, so combinations can bring in parts that the best solutions do not have.
- **Systematic combination.** All pairs with a new member are combined, by fixed rules, not by random choice of parents.
- **Stops by itself.** The search stops when the reference set does not change. A rebuild step, as below, can restart it.

## Variants and improvements

- **Rebuilding.** When no new solution enters $R$, keep the $b_1$ best members, generate new diverse solutions and fill the other $b_2$ places, then continue. This repeats the diversification of line L2.
- **Static and dynamic update.** The code here updates $R$ as soon as a child qualifies (dynamic). A static update first makes all children of the round and then takes the best $b$ of $R \cup N$.
- **Larger subsets.** The template also combines subsets of three or four solutions, often built by adding the best remaining member to a pair.
- **Other combinations.** For continuous problems, children are points on the line through two members, $x + \lambda (y - x)$ for a few values of $\lambda$, which is the origin of the method. For bit strings, [path relinking](/path-relinking/) is the combination that walks from one member to the other, and Glover presents it as the natural generalization of scatter search combinations.
- **Stronger improvement.** IMPROVE can be any local search, such as a swap descent or a short [tabu search](/tabu-search/).

## When to use it

Use scatter search when there is a good improvement method and a sensible way to combine two solutions, and when a small, carefully chosen population is enough. It is a good fit for problems with a natural repair step, such as knapsack and other problems with capacity constraints, and for continuous problems where combinations along lines between points make sense. It needs more design than [GRASP](/grasp/) or random restarts, since all five methods must be chosen.

## Pitfalls

- **A reference set with no diversity.** If all members of $R$ are near copies, every combination gives the same solution again, and the search stops after one round.
- **Combining old pairs again.** Combining two members that were combined before gives the same children with deterministic methods. Line L5 skips these pairs.
- **No repair.** A union of two feasible packings is often too heavy. Without repair, either most children are lost or infeasible solutions enter $R$.
- **Equating maximal with good.** A maximal packing cannot take one more item, but a swap of items can still improve it. A stronger improvement method is often worth its cost.

## Implementations

## History

Glover introduced scatter search in a 1977 paper on heuristics for integer programming with surrogate constraints, where new points come from weighted combinations of reference points, followed by rounding. Glover's 1998 template described the method as five parts, and most later work follows that template. Glover, Laguna and Martí gave a joint account with path relinking in 2000, and Martí, Laguna and Glover described the basic design and its main variants in 2006.

## References
