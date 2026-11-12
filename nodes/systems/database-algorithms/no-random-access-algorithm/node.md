---
tag: 29R7VV
kind: algorithm
slug: no-random-access-algorithm
name: No-random-access algorithm
aliases:
- NRA top-k algorithm
- no random access top-k algorithm
area: systems/database-algorithms
level: advanced
summary: "Top-k over m graded lists with sorted access only: keep a lower and an upper bound on each seen score, and stop when no other object can beat the k best lower bounds."
solves: [top-k-query]
model: query-model
complexity:
  vars: {n: the number of objects, m: the number of lists, k: the number of answers}
  time: {worst: O(m n)}
  space: {extra: O(m n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [top-k-query, threshold-algorithm]
see_also: [fagin-algorithm, top-k-selection, priority-queue, k-way-merge, pareto-front-computation]
sources:
  - paper: doi:10.1016/S0022-0000(03)00026-6
    title: Ronald Fagin, Amnon Lotem and Moni Naor, Optimal aggregation algorithms for middleware, Journal of Computer and System Sciences 66(4), 614 to 656 (2003); first in PODS 2001, 102 to 113
    locator: Section 8.1 (NRA, Example 8.3, Theorem 8.4 on correctness, Theorem 8.5 and Corollary 8.6 on instance optimality, Remark 8.7 on bookkeeping) and Section 8.2 (CA)
  - paper: doi:10.1145/1391729.1391730
    title: Ihab F. Ilyas, George Beskales and Mohamed A. Soliman, A survey of top-k query processing techniques in relational database systems, ACM Computing Surveys 40(4), Article 11 (2008)
    locator: the section on top-k processing with sorted access only
---

The no-random-access algorithm (NRA) finds the $k$ objects with the highest combined score over $m$ lists, each sorted by one grade, when the sources allow only *sorted access*: you can read each list from the top, but you cannot ask for the grade of a given object. NRA keeps, for each object it has seen, a *worst-case* score $W$ (missing grades set to 0) and a *best-case* score $B$ (each missing grade set to the last grade read in its list). It stops when $k$ objects have lower bounds that no other object can beat, even in the best case. NRA may stop before it knows the exact scores of its answers, so it returns the set, not the scores. Fagin, Lotem and Naor (2001) proved it is instance optimal among algorithms without random access.

## In plain words

Two radio charts rank the same songs, but each chart only lets you read it from the top. You want the best song by the sum of its two chart scores.

Read one line from each chart at a time. For each song you have seen, write two numbers. The low number counts a missing score as 0. The high number counts a missing score as the last score you read on that chart, since the song must be lower than that line.

A song you have not seen at all can score at most the sum of the last two scores you read.

Stop when your best song's low number is at least every other song's high number, and at least that sum. You may not know its exact score, but you know it wins.

## The problem

The input is a [top-k query](/top-k-query/): $m$ lists over the same $N$ objects, list $L_i$ sorted by grade $x_i(R) \ge 0$ from high to low, a monotone aggregation $t$, and $k$. The output is a set of $k$ objects with the highest scores $t(R) = t(x_1(R), \ldots, x_m(R))$. Only sorted access is allowed, and the cost is the number of sorted accesses. NRA returns each answer with an interval that contains its score, not the score itself.

## The algorithm

After round $d$, let $\underline{x}_i$ be the last grade read in $L_i$. For a seen object $R$ with known grades on the set of lists $S(R)$:

- $W(R) = t(\ldots)$ with $x_i(R)$ for $i \in S(R)$ and 0 for the others.
- $B(R) = t(\ldots)$ with $x_i(R)$ for $i \in S(R)$ and $\underline{x}_i$ for the others.
- An unseen object has $B = t(\underline{x}_1, \ldots, \underline{x}_m)$, the same threshold as in the [threshold algorithm](/threshold-algorithm/).

```pseudo id=main
NRA(L_1 .. L_m, t, k)
L1  d ← 0; for each seen object, its known grades, empty at first
L2  while d < N do
L3      for i ← 1 to m do read L_i[d] by sorted access; record the grade; x̲_i ← that grade
L4      d ← d + 1
L5      for each seen R: compute W(R) and B(R)
L6      T ← k seen objects with the largest W, ties to the larger B; M ← min of W over T
L7      if |T| = k and B(R) ≤ M for each seen R ∉ T and (all objects are seen or t(x̲_1, ..., x̲_m) ≤ M) then stop
L8  return T, with the bounds [W(R), B(R)] of each member
```

## Example

Find the top object under $t = $ sum:

| depth | $L_1$ | $L_2$ |
|---|---|---|
| 1 | a 9 | b 5 |
| 2 | b 3 | c 4 |
| 3 | c 2 | d 3 |
| 4 | d 1 | a 0 |

| after depth | $\underline{x}$ | a: $[W, B]$ | b: $[W, B]$ | c: $[W, B]$ | unseen $B$ | $T$, $M$ | stop? |
|---|---|---|---|---|---|---|---|
| 1 | 9, 5 | [9, 14] | [5, 14] | | 14 | a, 9 | no: b may reach 14 |
| 2 | 3, 4 | [9, 13] | [8, 8] | [4, 7] | 7 | a, 9 | yes |

NRA returns a after 4 sorted accesses. It knows only that the score of a is between 9 and 13; the true score is 9, but the grade 0 of a in $L_2$ is at the bottom of the list, and no algorithm without random access can learn it early. The [threshold algorithm](/threshold-algorithm/) also stops at depth 2 here, but it needs 4 random accesses to do so (b is looked up twice, since it did not enter TA's buffer of size 1).

## Correctness

Each bound is sound: a grade that has not been read in $L_i$ is at least 0 and at most $\underline{x}_i$, because the list is sorted, and $t$ is monotone. When NRA stops, each member of $T$ has score at least $W \ge M$; each other seen object has score at most $B \le M$; and each unseen object has score at most $t(\underline{x}_1, \ldots, \underline{x}_m) \le M$. So $T$ is a top $k$ set. If NRA reads all lists to the end, every bound is exact. The full proof is in the proof file.

## Complexity

- **Accesses.** NRA stops after some depth $d \le N$ with $m d$ sorted accesses and no random accesses.
- **Instance optimality.** For every correct algorithm $A$ that makes no random accesses and every database $D$, $\mathrm{cost}(\mathrm{NRA}, D) \le m \cdot \mathrm{cost}(A, D) + O(1)$. For a strict $t$ such as min, the ratio $m$ is exact and best possible.
- **Compared with TA.** For $k < N$, the threshold algorithm, which also has random access, never stops later than NRA.
- **Bookkeeping.** The bounds of all seen objects change after each round, so a direct version does $\Theta(m \cdot \text{seen})$ work per round and $O(m d^2)$ by depth $d$. Memory holds all seen objects, up to $m d$, unlike the $k$ objects of TA.

## Properties

- **Correct for every monotone $t$**, with no random access.
- **Returns a set, not scores.** The paper's Example 8.3 shows that exact scores can cost a full scan; NRA returns intervals instead.
- **Uses both bounds.** Earlier sorted-access-only algorithms used only upper bounds and had to see an object in every list before they could output it; NRA can output an object it has seen in only one list, as in the example.
- **Tie-breaking matters.** Ties in $W$ are broken in favor of the larger $B$; the instance optimality proof uses this rule.

## Variants and improvements

- **Combined algorithm (CA).** Every $h = \lfloor c_R / c_S \rfloor$ rounds, do random access for the seen object with the largest $B$ among those with $B > M$ whose score is not known. CA interpolates between NRA and TA.
- **Faster bookkeeping.** Update $B$ lazily and keep candidates in a [priority queue](/priority-queue/) on $B$, so most rounds touch only a few objects. LARA by Mamoulis and coauthors (2007) is a well known example.
- **Specific functions.** For min or max, the bounds have simple closed forms, and the work per round drops.
- **Approximation.** Stop when $B(R) \le \theta M$ for all $R \notin T$, to get a $\theta$-approximate answer earlier.
- **Rank join.** Top-k join operators in query engines generalize NRA to joins on keys other than a shared object identity.

## When to use it

Use NRA when the sources stream ranked results but cannot score a given object: web search APIs, remote ranked services, or sorted inverted lists without a document-level index. It is also a good choice when random access is so costly that even TA's few lookups dominate. If only the set of winners is needed, NRA gives it with no lookups at all. If exact scores are needed, add random accesses for the $k$ winners at the end.

## Pitfalls

- **Missing floor.** The lower bound $W$ needs a known minimum grade. With negative grades, use the true floor; using 0 makes $W$ unsound.
- **Forgetting unseen objects.** The test must include the threshold $t(\underline{x}_1, \ldots, \underline{x}_m)$; checking only seen objects stops too early.
- **Expecting exact scores.** The returned bounds may be wide, as in the example. Do not rank the answer by $W$ and treat it as the true order.
- **Memory growth.** NRA must remember every seen object until it can rule it out; on correlated-against lists this can be most of the data.

## Implementations

## History

Fagin, Lotem and Naor introduced NRA and CA at PODS 2001, in the same paper as the threshold algorithm, with the journal version in 2003. In related work they note that Güntzer, Balke and Kießling had studied the case without random access with an algorithm called Stream-Combine, which uses only upper bounds and is not instance optimal.

## References
