---
tag: SRQFRM
kind: algorithm
slug: wander-join
name: Wander join
aliases:
- random walk join sampling
area: databases/query-planning
level: research
summary: "Estimate SUM or COUNT over a join by random walks through the indexes. Each walk is divided by its probability, so it is an unbiased estimate, and a failed walk counts as 0."
solves: [join-size-estimation-problem]
model: real-ram
complexity:
  vars: {k: the number of relations in the join, W: the number of walks}
  time: {expected: "O(k W)"}
  space: {extra: "O(k)"}
properties: {deterministic: false, randomized: true, exact: false, greedy: false, recursive: false}
history:
  year: 2016
  people: [Feifei Li, Bin Wu, Ke Yi, Zhuoyue Zhao]
  note: Given at SIGMOD 2016 as an online aggregation method for joins that uses the indexes of the database.
prereqs: [online-aggregation, horvitz-thompson-estimator, index-nested-loop-join]
see_also: [ripple-join, cardinality-estimation, join-size-estimation-problem, importance-sampling, central-limit-theorem, confidence-interval, acyclic-join-evaluation, guaranteed-error-estimator]
sources:
  - paper: "Feifei Li, Bin Wu, Ke Yi and Zhuoyue Zhao, Wander join: online aggregation via random walks, Proceedings of ACM SIGMOD 2016, 615 to 629"
    title: "Wander join: online aggregation via random walks"
    locator: "Section 3.1 (chain joins, the join data graph and the estimate v/p), Section 3.2 (acyclic queries and walk orders), Section 3.3 (confidence intervals), Section 3.4 (selections and GROUP BY), Section 3.5 (cyclic queries), Section 4 (the walk plan optimizer and trial walks)"
  - paper: "D. G. Horvitz and D. J. Thompson, A generalization of sampling without replacement from a finite universe, Journal of the American Statistical Association 47 (1952), 663 to 685"
    title: A generalization of sampling without replacement from a finite universe
    locator: the estimator that divides each sampled value by its probability of selection
  - paper: doi:10.1145/304182.304208
    title: Peter J. Haas and Joseph M. Hellerstein, Ripple joins for online aggregation, Proceedings of ACM SIGMOD 1999, 287 to 298
    locator: the earlier online aggregation method for joins that wander join is compared with
---

Wander join estimates an aggregate such as SUM or COUNT over a join without computing the join. Feifei Li, Bin Wu, Ke Yi and Zhuoyue Zhao gave it in 2016 for [online aggregation](/online-aggregation/), where the system shows an estimate and a confidence interval that improve while the query runs. One walk picks a random row of the first table, then follows the index of each next table to a random matching row. The walk keeps the probability $p$ of its choices and returns $v/p$, where $v$ is the value of the expression on the joined row. If the walk reaches a row with no match, it returns 0. Each walk is an unbiased estimate of the answer, by the [Horvitz-Thompson](/horvitz-thompson-estimator/) argument. Unlike [ripple join](/ripple-join/), which joins independent samples of each table and finds few results when the join is selective, every successful walk is a join result.

## In plain words

Suppose you want the total of a column over all rows of a join of three tables. Start at a random row of the first table. Use the index of the second table to list the rows that match it, and pick one at random. Do the same for the third table. If you reach a dead end, the walk counts as zero.

At the end, you know the chance of your path. A rare path stands for many paths you did not walk, so you multiply its value by one over its chance. On average, this gives the true total. Many walks give a good estimate, and their spread gives an error bar. The order in which you visit the tables does not change the average, but it changes the spread and the number of dead ends, so a good order makes the estimate converge faster.

## The problem

The input is a join of relations $R_1, \ldots, R_k$ with optional selections, and an expression $v$ over the joined rows. The answer is $Q = \sum_{\gamma \in J} v(\gamma)$ over the join result $J$; COUNT is $v = 1$, the join size, and AVG is a ratio of two such sums. The model is that each relation after the first has an index on the attributes it shares with an earlier relation of the walk order, and that the index can return a uniform random row among the rows with a given key, together with their number. The output is an estimate $\hat Q$ and a confidence interval that shrinks as more walks are done.

## The algorithm

A walk order $\lambda$ lists the relations so that each relation $R_{\lambda(i)}$ after the first shares attributes with an earlier one, its parent $R_{\eta(i)}$. The edges from each relation to its parent form a spanning tree of the query graph. In a cyclic query, the edges outside the tree are checked at the end of the walk.

```pseudo id=main
WANDER-JOIN(walk order R_λ(1), ..., R_λ(k), indexes, expression v, number of walks W)
L1  for w ← 1 to W do
L2      pick t_1 uniformly from R_λ(1); p ← 1/|R_λ(1)|
L3      for i ← 2 to k do
L4          M ← the rows of R_λ(i) that join with t_η(i), found with the index
L5          if M is empty, or a selection fails, then X_w ← 0 and go to the next walk
L6          pick t_i uniformly from M; p ← p/|M|
L7      if the path fails a join condition outside the walk tree, or a selection, then X_w ← 0 else X_w ← v(path)/p
L8  return the mean of X_1, ..., X_W and the interval mean ± 1.96 · s/√W, where s is their standard deviation
```

The code checks selections and the conditions outside the tree as soon as the row of that step is chosen, which gives the same result as line L7 and stops failed walks earlier. In practice the walks run until the user stops the query or the interval is small enough, so $W$ is not fixed in advance.

## Example

This is a small chain join $R_1(A, B) \bowtie R_2(B, C) \bowtie R_3(C, D)$ with COUNT, like the example of Section 3.1 of the paper.

| relation | rows |
|---|---|
| $R_1(A, B)$ | $(a_1, b_1)$, $(a_2, b_1)$, $(a_3, b_2)$ |
| $R_2(B, C)$ | $(b_1, c_1)$, $(b_1, c_2)$, $(b_2, c_3)$ |
| $R_3(C, D)$ | $(c_1, 5)$, $(c_2, 1)$, $(c_2, 3)$ |

The join has 6 rows: $a_1$ or $a_2$, then $b_1$, then one of the three rows of $R_3$ through $c_1$ or $c_2$.

In the order $R_1, R_2, R_3$, the walk starts at one of 3 rows. From $a_3$ it goes to $(b_2, c_3)$, and $R_3$ has no row with $c_3$, so the walk fails and returns 0. From $a_1$ or $a_2$ it has 2 choices in $R_2$. Through $c_1$ there is 1 row in $R_3$, so $1/p = 3 \cdot 2 \cdot 1 = 6$. Through $c_2$ there are 2 rows, so $1/p = 3 \cdot 2 \cdot 2 = 12$. The three values 0, 6 and 12 each have probability $1/3$, so the mean is 6, the true count, and the variance is 24.

In the order $R_3, R_2, R_1$, every row of $R_3$ has exactly one match in $R_2$, and $b_1$ has two matches in $R_1$. Every walk succeeds with $1/p = 3 \cdot 1 \cdot 2 = 6$, so every walk returns exactly 6 and the variance is 0. For SUM(D), the walks in this order return $6 \cdot 5$, $6 \cdot 1$ or $6 \cdot 3$, with mean 18, the true sum.

## Correctness

The proof file gives the full argument. A successful walk satisfies every join condition: the conditions with the parent hold because the index returns only matching rows, and the other conditions are checked in line L7. Conversely, every row $\gamma$ of the join can be reached by exactly one sequence of choices, with probability $p(\gamma) > 0$. So the successful walks and the join rows are in one-to-one correspondence, and

$$E[X] = \sum_{\gamma \in J} p(\gamma) \cdot \frac{v(\gamma)}{p(\gamma)} = Q.$$

Failed walks add 0. This is why a failed walk must count as 0 and not be thrown away: rejecting it would divide by the unknown chance of success. The mean of $W$ independent walks is unbiased with variance $\mathrm{Var}[X]/W$, and the interval of line L8 comes from the [central limit theorem](/central-limit-theorem/), so its coverage of 95 percent holds only as $W$ grows.

## Complexity

A walk does at most $k - 1$ index lookups and $k$ random choices. With hash indexes that keep each group of rows in an array, a walk costs $O(k)$ expected time, and $W$ walks cost $O(kW)$. With B-trees, each lookup costs $O(\log N)$, and a uniform choice in a range needs counts in the tree. The extra space is the current path and three running sums. The error falls as $\sigma/\sqrt W$, where $\sigma^2$ is the variance of one walk, so halving the interval takes four times as many walks.

## Properties

- **Unbiased, proved.** Each walk, and the mean of any number of walks, has expectation equal to the answer, for every walk order, for acyclic and cyclic queries and with selections.
- **Asymptotic intervals.** The confidence interval is based on the central limit theorem, so it is valid in the limit, not for a fixed number of walks.
- **Index based.** It needs an index for each step of the walk order. Without indexes, it cannot run.
- **Variance depends on the order.** The walk order changes the variance and the rate of failed walks, as the example shows, but not the mean.
- **No blocking.** Walks are independent, so the estimate can be shown and improved at any time, and walks can run in parallel.

## Variants and improvements

- **Walk plan optimizer.** Section 4 of the paper runs trial walks for each valid order in turn, until one order has $\tau$ successful walks ($\tau = 100$ by default), and then picks the order with the smallest estimate of $\mathrm{Var}[X] \cdot E[T]$, the variance after a fixed time. This is a heuristic, and the paper measures it.
- **Cyclic queries.** Walk a spanning tree of the query graph and check the other edges at the end (Section 3.5 of the paper).
- **Selections and GROUP BY.** A walk that hits a row that fails a selection returns 0. For GROUP BY, each walk adds its value to the estimate of its group, and the walks of one group are used for its interval.
- **Cardinality estimation.** With COUNT, the walks estimate the size of a join, which an optimizer can use in place of an estimate built on independence. Later work on sampling for [cardinality estimation](/cardinality-estimation/) uses the same idea.
- **Other estimators.** The same walks can be weighted with other designs, for example to lower variance by [importance sampling](/importance-sampling/) on the choices. This page proves only the uniform version.

## When to use it

Use it for interactive queries over large joins, when an approximate answer with an error bar is good enough and the join attributes have indexes, as foreign keys in a star schema usually do. It does well when the join is selective, where ripple join finds few results. It is a poor choice when indexes are missing, when the aggregate depends on very rare rows (the variance is then large), or when an exact answer is needed.

## Pitfalls

- **Throwing away failed walks.** A failed walk must add 0 to the sum. Rejecting it and walking again gives a biased estimate.
- **Wrong probability.** At each step, the probability must use the size of the set the row was picked from. If the walk picks from all matching rows and then checks the selection, it must divide by the number of matching rows, not by the number that pass the selection.
- **Missing a cycle edge.** In a cyclic query, a walk that is not checked against the edges outside the walk tree counts rows that are not in the join.
- **Trusting early intervals.** With few successful walks, the sample variance can be far from the true variance, and the interval can be much too narrow, for example when no rare heavy row has been seen yet.
- **Correlated walks.** The interval assumes independent walks. Walks that share a random seed or that sample without replacement need a different variance formula.

## Implementations

## History

Online aggregation was proposed by Hellerstein, Haas and Wang in 1997, and Haas and Hellerstein gave ripple join for joins in 1999. Ripple join samples each table on its own, so it needs many samples before two of them join when the join is selective. Feifei Li, Bin Wu, Ke Yi and Zhuoyue Zhao noted in 2016 that the indexes a database already has let a sampler follow the join, and called the result wander join. Its estimate is the estimator of Horvitz and Thompson from 1952. Later work used the same kind of walks to estimate join sizes for query optimizers.

## References
