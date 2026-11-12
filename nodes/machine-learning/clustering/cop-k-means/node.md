---
tag: CH7828
kind: algorithm
slug: cop-k-means
name: COP-k-means
aliases:
- COP-KMeans
- constrained k-means of Wagstaff et al.
area: machine-learning/clustering
level: advanced
summary: K-means modified to respect must-link and cannot-link constraints.
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of clusters, c: the number of constraints, t: the number of passes}
  time: {worst: "O(n^2 + c + t n k (d + n))"}
  space: {extra: "O(n^2 + k d)"}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 2001
  people: [Kiri Wagstaff, Claire Cardie, Seth Rogers, Stefan Schrödl]
  note: Wagstaff, Cardie, Rogers and Schrödl gave COP-KMEANS at ICML 2001 and used it to find road lanes in GPS data, one year after Wagstaff and Cardie introduced must-link and cannot-link constraints.
prereqs: [k-means, constrained-clustering]
see_also: [k-means-problem, k-means-plus-plus, transitive-closure, disjoint-set, graph-coloring, k-coloring, hard-and-soft-clustering]
sources:
  - paper: "K. Wagstaff, C. Cardie, S. Rogers and S. Schrödl, Constrained k-means clustering with background knowledge, Proceedings of ICML 2001, pp. 577-584"
    title: Wagstaff et al. 2001
    locator: "Section 2 (the COP-KMEANS algorithm, Table 1) and Section 4 (lane finding in GPS data)"
  - paper: "K. Wagstaff and C. Cardie, Clustering with instance-level constraints, Proceedings of ICML 2000, pp. 1103-1110"
    title: Wagstaff and Cardie 2000
    locator: must-link and cannot-link constraints and their transitive closure
  - paper: "I. Davidson and S. S. Ravi, Clustering with constraints: feasibility issues and the k-means algorithm, Proceedings of the 2005 SIAM International Conference on Data Mining (SDM), pp. 138-149"
    title: Davidson and Ravi 2005
    locator: the feasibility problem and the failure of COP-KMEANS on feasible instances
  - paper: "S. Basu, A. Banerjee and R. J. Mooney, Active semi-supervision for pairwise constrained clustering, Proceedings of the 2004 SIAM International Conference on Data Mining (SDM), pp. 333-344"
    title: Basu, Banerjee and Mooney 2004
    locator: PCKMeans with soft constraints
  - book: isbn:9781584889960
    title: "Sugato Basu, Ian Davidson and Kiri L. Wagstaff (editors), Constrained Clustering: Advances in Algorithms, Theory, and Applications"
    locator: Chapter 1 (introduction, COP-KMEANS and its variants)
---

COP-k-means is the first and simplest algorithm for [constrained clustering](/constrained-clustering/) with k-means, given by Wagstaff, Cardie, Rogers and Schrödl in 2001. It is Lloyd's [k-means](/k-means/) algorithm with one change in the assignment step: each point, taken in a fixed order, goes to the nearest center whose cluster violates no must-link or cannot-link constraint with the points already assigned in this pass. If no cluster is allowed for some point, the algorithm stops and reports failure. Every clustering it returns satisfies all constraints. But the assignment is greedy, so the result depends on the order of the points, and the algorithm can fail although a feasible clustering exists.

## In plain words

K-means repeats two steps: put each point with its nearest center, then move each center to the middle of its points. COP-k-means adds rules of the form "these two points go together" and "these two points stay apart".

The points get their places one by one. A point first tries its nearest center. If a rule says no, because a partner of the point is in another group, or a point it must avoid is already in this group, it tries the next nearest center, and so on. If every center is forbidden, the algorithm gives up.

Because the points come one at a time, an early choice can block a later point. The algorithm does not go back to change earlier choices.

## The problem

The input is a list of $n$ points $x_1, \ldots, x_n$ in $\mathbb{R}^d$, a number $k$ of clusters, a set $\mathrm{ML}$ of must-link pairs and a set $\mathrm{CL}$ of cannot-link pairs. The goal is a labeling $\ell : \{1, \ldots, n\} \to \{1, \ldots, k\}$ that satisfies all constraints and has a small sum of squared distances $\sum_i \|x_i - \mu_{\ell(i)}\|^2$, where $\mu_j$ is the mean of cluster $j$. This is the constrained version of the [k-means problem](/k-means-problem/). Even the question whether a feasible labeling exists is NP-complete with cannot-link constraints, so a fast heuristic like COP-k-means cannot always find one.

## The algorithm

Before the passes, the constraints are closed under transitivity, as Wagstaff and Cardie did in 2000: all points of one ML component (a class of the [transitive closure](/transitive-closure/) of the must-link pairs) must-link each other, and if one cannot-link pair joins two components, all their points cannot-link each other. A [disjoint-set forest](/disjoint-set/) finds the components.

```pseudo id=main
COP-K-MEANS(x[1..n], k, ML, CL, order π)
L1  close ML and CL under transitivity; choose k initial centers μ_1, ..., μ_k
L2  repeat
L3      for each point i in the order π (with no point labeled at the start of the pass)
L4          give i the nearest center j such that no ML partner of i has a label other than j
            and no CL partner of i has the label j
L5          if no such j exists then return "failure"
L6      for j ← 1 to k: μ_j ← the mean of the points with label j (keep μ_j if there are none)
L7  until the labels did not change in this pass (or a cap on the passes is reached)
L8  return the labels and the centers
```

Only points that already have a label in this pass count at line L4. A point whose partners come later in the order is free, and the partners must then follow it.

## Example

Take six points on the line, $x_0, \ldots, x_5 = 0, 1, 2, 10, 11, 12$, with $k = 2$, initial centers $0$ and $12$, and one must-link pair $\{x_2, x_3\}$. Without the constraint, k-means gives $\{0, 1, 2\}$ and $\{10, 11, 12\}$ with cost $2 + 2 = 4$.

With the order $x_0, x_1, \ldots, x_5$:

| point | nearest center | allowed? | label |
|---|---|---|---|
| $x_0 = 0$ | 1 | yes | 1 |
| $x_1 = 1$ | 1 | yes | 1 |
| $x_2 = 2$ | 1 | yes ($x_3$ has no label yet) | 1 |
| $x_3 = 10$ | 2 | no, $x_2$ has label 1 | 1 (second nearest) |
| $x_4 = 11$ | 2 | yes | 2 |
| $x_5 = 12$ | 2 | yes | 2 |

The new centers are $13/4$ and $23/2$. In the second pass $x_3$ is again nearest to center 2 and again must follow $x_2$, so the labels do not change and the algorithm stops with $\{0, 1, 2, 10\}$, $\{11, 12\}$ and cost $253/4 = 63.25$.

With the reverse order $x_5, x_4, \ldots, x_0$, the point $x_3$ comes first and takes center 2, so $x_2$ must follow it. The result is $\{0, 1\}$, $\{2, 10, 11, 12\}$ with centers $1/2$ and $35/4$. The cost is again $253/4$ here, by symmetry, but the clustering is different.

Now a failure. Take $a = 0$, $b = 10$, $c = 5$, $k = 2$, centers $0$ and $10$, and $\mathrm{CL} = \{ac, bc\}$. In the order $a, b, c$, the point $a$ takes cluster 1 and $b$ takes cluster 2. Then $c$ cannot join either, and COP-k-means returns failure. The clustering $\{a, b\}, \{c\}$ is feasible, and the order $c, a, b$ finds a feasible one.

## Correctness

The full proof is in the proofs file. When the point $i$ is labeled at line L4, every closed constraint between $i$ and an earlier point of the same pass holds, and labels do not change later in the pass. Each pair of points is checked when its later point is labeled, so a labeling returned at L8 satisfies all closed constraints, and so all given constraints. With no constraints, line L4 never rejects a cluster and the algorithm is exactly Lloyd's algorithm. With must-link constraints alone it never fails: all labeled points of one component share one label, and that label is always allowed for the next point of the component. Lemma 6 of the proof is the failure example above.

## Complexity

The closure takes $O(n^2 + c)$ time for $c$ constraints, since a point can have $\Theta(n)$ closed partners. In a pass, each point sorts the $k$ centers by distance in $O(k d + k \log k)$ time and checks at most $k$ clusters against at most $n$ partners. So a pass costs $O(n k (d + n))$, and $t$ passes cost $O(t n k (d + n))$. With few constraints per point the check is cheap, and a pass costs about the same as a pass of Lloyd's algorithm. The lists of partners take $O(n^2)$ space in the worst case.

## Properties

- **Deterministic** for given initial centers and a given order. With random centers or a random order, the output is random.
- **Order dependent.** Different orders can give different clusterings, and one order can fail where another succeeds.
- **Safe.** Every returned clustering satisfies all hard constraints.
- **Not complete.** It can fail on feasible inputs that have cannot-link constraints.
- **No monotone objective.** The greedy assignment is not the best feasible assignment for the current centers, so the cost can go up from one pass to the next, and the proof of convergence of Lloyd's algorithm does not apply. A cap on the passes makes it stop.

## Variants and improvements

- **Restarts.** Run again with another order or other initial centers after a failure.
- **Seeding.** Choose the initial centers with [k-means++](/k-means-plus-plus/), or, as Basu and others did, from the ML components.
- **Soft constraints.** PCKMeans (Basu, Banerjee and Mooney 2004) adds a penalty for each violated pair to the objective, so it always returns a clustering.
- **Exact assignment.** Solve the assignment step as an integer program, or with the components as single items, to find the best feasible assignment for the current centers when one exists.
- **Distance learning.** MPCKMeans (Bilenko, Basu and Mooney 2004) also learns a distance from the constraints.

## When to use it

Use COP-k-means when the constraints are hard, there are few of them, and a fast method with the cost of k-means is enough. It works well when the constraints are mostly must-link, since then it cannot fail. With many cannot-link constraints, and especially when $k$ is close to the chromatic number of the cannot-link graph, failures are common, and a method with soft constraints or an exact feasibility test is a better choice.

## Pitfalls

- Without the transitive closure, the check at line L4 sees only the given pairs. With $\mathrm{ML} = \{ac, cb\}$ and the order $a, b, c$, the points $a$ and $b$ can take different clusters, and then $c$ fails, although must-link constraints alone are always feasible.
- A failure does not prove that no feasible clustering exists. Test feasibility separately, for example by coloring the cannot-link graph of the ML components.
- A cannot-link pair inside one ML component makes the input infeasible. Check this once before the passes.
- A cluster can become empty. Keep its old center, as here, or reseed it.

## Implementations

## History

Wagstaff and Cardie introduced must-link and cannot-link constraints at ICML 2000, with a constrained form of the COBWEB algorithm, and noted that the constraints are closed under transitivity. At ICML 2001, Wagstaff, Cardie, Rogers and Schrödl gave COP-KMEANS and applied it to GPS traces of cars, to find the lanes of a road. Later work gave soft versions, such as PCKMeans and MPCKMeans by Basu, Bilenko and Mooney, and Davidson and Ravi showed in 2005 that the feasibility question is NP-complete with cannot-link constraints, which explains why a greedy method like COP-k-means must sometimes fail.

## References
