---
tag: 2544V4
kind: algorithm
slug: fagin-algorithm
name: Fagin's algorithm
aliases:
- Fagin's algorithm for top-k
- Fagin's top-k middleware algorithm
area: systems/database-algorithms
level: advanced
summary: "Top-k over m graded lists: read all lists in parallel until k objects have been seen in every list, then fetch missing grades by random access."
solves: [top-k-query]
model: query-model
complexity:
  vars: {n: the number of objects, m: the number of lists, k: the number of answers}
  time: {worst: O(m^2 n), average: O(m^2 n^((m-1)/m) k^(1/m))}
  space: {extra: O(m n^((m-1)/m) k^(1/m))}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [top-k-query, top-k-selection, hash-table]
see_also: [threshold-algorithm, no-random-access-algorithm, k-way-merge, priority-queue, pareto-front-computation, sorted-array-intersection]
sources:
  - paper: doi:10.1006/jcss.1998.1600
    title: Ronald Fagin, Combining fuzzy information from multiple systems, Journal of Computer and System Sciences 58(1), 83 to 99 (1999); first in PODS 1996
    locator: the algorithm, its correctness for monotone queries, and the cost bound O(N^((m-1)/m) k^(1/m)) with a matching lower bound for strict queries, with high probability for independent lists
  - paper: doi:10.1016/S0022-0000(03)00026-6
    title: Ronald Fagin, Amnon Lotem and Moni Naor, Optimal aggregation algorithms for middleware, Journal of Computer and System Sciences 66(4), 614 to 656 (2003)
    locator: Section 2 (sorted and random access, middleware cost) and Section 3 (FA and its properties)
  - paper: doi:10.1145/1391729.1391730
    title: Ihab F. Ilyas, George Beskales and Mohamed A. Soliman, A survey of top-k query processing techniques in relational database systems, ACM Computing Surveys 40(4), Article 11 (2008)
    locator: the section on top-k processing over sorted lists (FA, TA and NRA)
---

Fagin's algorithm (FA) finds the $k$ objects with the highest combined score when each of $m$ sources gives a list of all objects sorted by its own grade. Ronald Fagin introduced it in 1996 for the Garlic middleware system at IBM, to combine, for example, a color score and a shape score of images. FA reads the lists from the top in parallel until at least $k$ objects have appeared in all of them, then looks up the missing grades of every object it has seen. It is correct for each monotone combining function, and on lists with independent orders it reads about $N^{(m-1)/m} k^{1/m}$ entries per list out of $N$; for two lists that is about $\sqrt{k N}$.

## In plain words

Two web sites rank the same restaurants, one by food and one by price. You want the best 3 by the sum of both scores. You do not want to read the full lists.

Read both lists from the top, one line from each at a time. Stop when 3 restaurants have shown up on both lists. Then, for each restaurant you have seen on only one list, ask the other site for its score. Add up the scores of all restaurants you have seen, and pick the best 3.

A restaurant you have not seen at all is below the 3 full matches on both lists, so its total cannot beat theirs.

## The problem

The input is a [top-k query](/top-k-query/): $m$ lists $L_1, \ldots, L_m$ over the same $N$ objects, list $L_i$ sorted by grade $x_i(R)$ from high to low, a monotone aggregation $t$ (for example sum, min or a weighted average), and $k$. The output is $k$ objects with the highest $t(R) = t(x_1(R), \ldots, x_m(R))$, with their scores. Two kinds of access are allowed: *sorted access* reads the next entry of a list, and *random access* asks for the grade of a given object in a given list. The cost is $s c_S + r c_R$ for $s$ sorted and $r$ random accesses.

## The algorithm

```pseudo id=main
FAGIN(L_1 .. L_m, t, k)
L1  d ← 0; seen ← an empty map from objects to known grades
L2  while fewer than k objects have been seen in all m lists, and d < N do
L3      for i ← 1 to m do read L_i[d] by sorted access; record its grade
L4      d ← d + 1
L5  for each seen object R and each list i where R was not seen: get x_i(R) by random access
L6  compute t(R) for each seen object R
L7  return the k seen objects with the highest t(R)
```

The sorted phase does not depend on $t$: FA reads the same entries for sum, for min and for any other function.

## Example

Find the top object under $t = \min$, then the top 2 under $t = $ sum:

| depth | $L_1$ | $L_2$ |
|---|---|---|
| 1 | a 0.9 | c 0.9 |
| 2 | b 0.8 | a 0.8 |
| 3 | c 0.7 | e 0.7 |
| 4 | d 0.6 | b 0.4 |
| 5 | e 0.1 | d 0.2 |

- **$k = 1$, min.** After depth 2, object a has appeared in both lists, so the sorted phase stops after 4 sorted accesses. The seen objects are a, b and c. Random access gives $x_2(b) = 0.4$ and $x_1(c) = 0.7$ (2 random accesses). The scores are a 0.8, b 0.4 and c 0.7, so the answer is a with 0.8.
- **$k = 2$, sum.** At depth 3, c also appears in both lists, so FA stops with 2 matches. The scores are a 1.7, c 1.6, b 1.2 and e 0.8, and the answer is a and c. Object d was not seen; its grades 0.6 and 0.2 are below those of a and c in each list, so its sum cannot be higher.

## Correctness

Let $H$ be the set of at least $k$ objects seen in all lists when the sorted phase stops. An object $z$ that was never seen lies below depth $d$ in each list, so each of its grades is at most the grade of each object of $H$ in that list. By monotonicity, $t(z) \le t(h)$ for each $h \in H$. So at least $k$ seen objects score at least $t(z)$, and the top $k$ among the seen objects is a top $k$ of all objects. Every seen object gets its exact score from random access. The full proof is in the proof file.

## Complexity

- **Accesses.** If FA stops at depth $d$, it makes $m d$ sorted accesses and at most $(m - 1) m d$ random accesses.
- **Independent lists.** If the list orders are independent and random, an object is in the top $d$ of all $m$ lists with probability $(d / N)^m$, so about $N (d/N)^m$ matches exist at depth $d$. This reaches $k$ at $d^* = N^{(m-1)/m} k^{1/m}$. Fagin proved that FA's cost is $O(N^{(m-1)/m} k^{1/m})$ with arbitrarily high probability for constant $m$, and that every correct algorithm needs this much for a strict $t$ (one that is 1 only when all grades are 1, such as min).
- **Worst case.** FA can read all of every list, $m N$ sorted accesses, for example when the lists are in opposite orders.
- **Space.** All seen objects stay in the buffer until the end: up to $m d$ objects.

## Properties

- **Correct for every monotone $t$.** Monotonicity is the only assumption.
- **Oblivious to $t$.** The stopping rule ignores the grades. This makes FA simple but wasteful: for $t = \max$ the top object is the first entry of some list, yet FA may read far down.
- **Not instance optimal.** On some databases FA reads much deeper than needed; the [threshold algorithm](/threshold-algorithm/) never reads deeper than FA, and on some databases much less.
- **Optimal in a probabilistic worst case.** For strict $t$ and independent lists, no algorithm is better by more than a constant factor with high probability.

## Variants and improvements

- **[Threshold algorithm (TA)](/threshold-algorithm/).** Does random access as soon as an object is seen, and stops when $k$ seen objects score at least $t$ applied to the last grades read in each list. It stops no later than FA and keeps only $k$ objects.
- **[No-random-access algorithm (NRA)](/no-random-access-algorithm/).** For sources that allow only sorted access, it keeps lower and upper bounds on each score.
- **Filter conditions.** Chaudhuri and Gravano simulated FA in a relational system by turning the stopping depth into a range condition on each grade.
- **Unequal rates.** The lists do not need to be read in lockstep; the results hold when the rates of sorted access are within constant factors of each other.

## When to use it

FA is mostly of historical and teaching value: it was the first algorithm with a cost sublinear in $N$ for this problem. In practice, TA dominates it whenever random access is possible, and NRA or the combined algorithm CA are used when random access is expensive or impossible. FA is still a good choice when the buffer is no concern and the sorted phase must not depend on the scoring function, for example when the same prefix is reused for several functions.

## Pitfalls

- **Non-monotone functions.** With a non-monotone $t$, an unseen object can beat all seen ones, and FA is wrong.
- **Ties.** The proof uses only that an unseen object is not above the stopping depth, so ties in grades are safe; but the answer is then one of several valid top $k$ sets.
- **Counting matches.** A match is an object seen in all $m$ lists by sorted access. Grades from random access do not count toward the stopping rule.
- **Small $N$.** If fewer than $k$ objects exist, FA reads every list to the end and returns all objects.

## Implementations

## History

Fagin presented the algorithm at PODS 1996 in "Combining fuzzy information from multiple systems", and the journal version appeared in 1999. It was implemented in IBM's Garlic middleware system, which combined sources such as the QBIC image search system. In 2001, Fagin, Lotem and Naor gave the threshold algorithm, which they showed to be instance optimal, and they compared it with FA; they found that the threshold algorithm had been discovered independently by Nepal and Ramakrishna and by Güntzer, Balke and Kießling.

## References
