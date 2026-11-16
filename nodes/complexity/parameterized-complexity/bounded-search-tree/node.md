---
tag: 41MVNH
kind: technique
slug: bounded-search-tree
name: Bounded search tree
aliases:
- depth-bounded search tree
- search tree method
area: complexity/parameterized-complexity
level: core
summary: "Branch on a few exhaustive choices that each lower the parameter k. The search tree then has at most c^k leaves, where c is the root of an equation set by how much each branch lowers k."
prereqs: [fixed-parameter-tractable, recurrence-relation]
see_also: [vertex-cover-branching, measure-and-conquer, kernelization, exact-exponential-algorithms, branch-and-reduce, cluster-editing, dpll, characteristic-polynomial]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 3, Bounded search trees (Section 3.1, Vertex Cover; Section 3.2, How to solve recursive relations)
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: Chapter 3, Bounded Search Trees (Section 3.1, The Basic Method; Section 3.2, Vertex Cover)
  - book: isbn:9780198566076
    title: Rolf Niedermeier, Invitation to Fixed-Parameter Algorithms, Oxford University Press, 2006
    locator: Chapter 8, Depth-bounded search trees
  - paper: doi:10.1016/j.tcs.2010.06.026
    title: "Jianer Chen, Iyad A. Kanj and Ge Xia, Improved upper bounds for vertex cover, Theoretical Computer Science 411(40-42), 3736-3756 (2010)"
    locator: the branching rules and their analysis, O(1.2738^k + kn) time
---

A bounded search tree is a recursive algorithm for a [parameterized problem](/parameterized-problem/) that, at each step, splits the instance into a few cases, solves each case with a lower parameter, and stops when the parameter reaches 0. The cases must be *exhaustive*: if the instance has a solution, one of the cases has one. Each case lowers the parameter $k$ by at least 1, so the tree has depth at most $k$. If every node has at most $t$ children, the tree has at most $t^k$ leaves, and the algorithm runs in time $O(t^k \cdot \mathrm{poly}(n))$, which is [fixed-parameter tractable](/fixed-parameter-tractable/). A finer count uses the *branching vector*: if the cases lower $k$ by $d_1, \ldots, d_t$, the number of leaves is at most $c^k$, where $c$ is the positive root of $1 = c^{-d_1} + \cdots + c^{-d_t}$. The [edge branching for vertex cover](/vertex-cover-branching/) is the first example, with $t = 2$ and $c = 2$.

## In plain words

You look for a small set of at most $k$ items that fixes a problem. You find one small spot where something is wrong. Any good set must touch that spot, and there are only a few ways to do it. You do not know which way is right, so you try each one in turn.

Each try puts at least one item into the set, so after $k$ tries in a row the set is full, and you stop. The tries form a tree. Its height is at most $k$, and each node has only a few children. So the size of the tree depends on $k$ and on the number of ways, but not on the size of the input. When some ways put more items into the set at once, the tree is even smaller.

## When it applies

- The parameter $k$ bounds the size of a solution, such as a set of vertices, elements or edits.
- There is a small *obstacle* that every solution must touch, and it can be found in polynomial time: an uncovered edge, an unhit set, an induced path on three vertices.
- The obstacle has a bounded number of ways to be fixed, and each way lowers $k$ by at least 1.
- When no obstacle is left, the instance is solved, or the rest can be solved in polynomial time.

If the number of choices grows with $n$, for example "choose any vertex of the graph", the tree has size $n^k$, and the result is only an [XP](/xp/) algorithm.

## The template

The template has three holes. BASE$(I, k)$ is a test that runs in polynomial time and must hold when $k = 0$. SOLVE-BASE$(I, k)$ answers a base instance in polynomial time. BRANCH$(I, k)$ returns a list of instances $(I_1, k - d_1), \ldots, (I_t, k - d_t)$, in polynomial time, with these properties:

- *exhaustive:* $(I, k)$ is a yes-instance if and only if some $(I_i, k - d_i)$ with $k - d_i \ge 0$ is one;
- *progress:* every $d_i \ge 1$;
- *bounded:* the vector $(d_1, \ldots, d_t)$ comes from a fixed finite set of branching vectors.

```pseudo id=main
BST(I, k)                                          ▷ k ≥ 0
L1  if BASE(I, k) then return SOLVE-BASE(I, k)
L2  (I_1, k - d_1), …, (I_t, k - d_t) ← BRANCH(I, k)
L3  for i ← 1 to t do
L4      if d_i ≤ k and BST(I_i, k - d_i) = YES then return YES
L5  return NO
```

To return a solution, each branch also records the items it adds, as in [vertex cover branching](/vertex-cover-branching/).

**Branching number.** For a branching vector $(d_1, \ldots, d_t)$ with all $d_i \ge 1$ and $t \ge 1$, the function $f(x) = \sum_i x^{-d_i}$ falls strictly from $t$ at $x = 1$ to 0 as $x$ grows. If $t \ge 2$, the equation $f(x) = 1$ has exactly one root $c > 1$; for $t = 1$ we set $c = 1$. This $c$ is the *branching number* of the vector. Multiplying $f(x) = 1$ by $x^{\max d_i}$ gives a polynomial equation; for $(1, 3)$ it is $x^3 = x^2 + 1$.

**Lemma.** Let $c^\ast \ge 1$ be the largest branching number among the vectors that BRANCH can use. Then the search tree of BST$(I, k)$ has at most $(c^\ast)^k$ leaves and at most $(k + 1)(c^\ast)^k$ nodes. If each node takes time $p(n)$, BST runs in time $O((c^\ast)^k \cdot k \cdot p(n))$.

*Proof.* Let $L(k)$ be the largest number of leaves of a tree for budget $k$. We show $L(k) \le (c^\ast)^k$ by induction on $k$. A node that stops at L1, or whose branches all have $d_i > k$, is a leaf, and $1 \le (c^\ast)^k$ because $c^\ast \ge 1$ and $k \ge 0$. Otherwise the node uses some vector $(d_1, \ldots, d_t)$ with branching number $c \le c^\ast$, and its children have budgets $k - d_i \ge 0$, which are smaller than $k$. By induction,

$$L(k) \le \sum_{i:\, d_i \le k} (c^\ast)^{k - d_i} \le (c^\ast)^k \sum_{i} (c^\ast)^{-d_i} \le (c^\ast)^k \sum_{i} c^{-d_i} = (c^\ast)^k.$$

The third step holds because $x^{-d}$ falls as $x$ grows, and the last step is the definition of $c$. For $t = 1$ it holds too, because then $c = 1$ and the sum is 1. Every node lies on a path from the root to a leaf, and each path has at most $k + 1$ nodes, because the budget falls by at least 1 at each step. So there are at most $(k + 1)(c^\ast)^k$ nodes. $\square$

Correctness follows from the exhaustive property by induction on $k$, in the same way. The usual notation is $O^\ast(c^k)$, where $O^\ast$ hides factors polynomial in $n$ and $k$. Since the bound $c^k$ is an upper bound, a running time is often written with $c$ rounded up, such as $1.4656$ for the root $1.46557\ldots$ of $x^3 = x^2 + 1$.

Branching numbers of common vectors:

| vector | equation | branching number |
|---|---|---|
| $(1, 1)$ | $x = 2$ | 2 |
| $(1, 1, 1)$ | $x = 3$ | 3 |
| $(1, 2)$ | $x^2 = x + 1$ | 1.61803 |
| $(1, 2, 2)$ | $x^2 = x + 2$ | 2 |
| $(1, 3)$ | $x^3 = x^2 + 1$ | 1.46557 |
| $(1, 4)$ | $x^4 = x^3 + 1$ | 1.38028 |
| $(2, 2)$ | $x^2 = 2$ | 1.41421 |
| $(2, 3)$ | $x^3 = x + 1$ | 1.32472 |
| $(3, 3)$ | $x^3 = 2$ | 1.25992 |

Two rules of thumb follow from the table. A larger drop in any branch gives a smaller number. For the same total drop, a balanced vector is better: $(2, 2)$ gives 1.414 and $(1, 3)$ gives 1.466.

## Classic examples

The examples go from simple to hard.

### Vertex cover: branch on an edge

The obstacle is an uncovered edge $\{u, v\}$. Every cover contains $u$ or $v$, so the branches are $(G - u, k - 1)$ and $(G - v, k - 1)$. The vector is $(1, 1)$, and the tree has at most $2^k$ leaves. The time is $O(2^k (n + m))$. See [vertex cover branching](/vertex-cover-branching/) for the algorithm, a proof and code.

### Vertex cover: branch on a vertex of high degree

Let $v$ be a vertex with $\deg(v) = d$. Every cover contains $v$ or, if not, all of $N(v)$. So the branches are $(G - v, k - 1)$ and $(G - N[v], k - d)$, where $N[v]$ is $v$ with its neighbors.

- If we branch on any vertex of degree at least 2, the vector is $(1, 2)$ or better. The leaves follow $T(k) \le T(k - 1) + T(k - 2)$, the [Fibonacci](/fibonacci-numbers/) recurrence, with the root 1.618.
- If we branch only on vertices of degree at least 3, the vector is $(1, 3)$ or better, with the root 1.4656. When every degree is at most 2, the graph is a union of paths and cycles, and a least cover is found in linear time: this is the BASE case.

The number of leaves for $k = 10$ and $k = 20$, from the recurrences with $T(k) = 1$ for small $k$:

| $k$ | $(1, 1)$: $2^k$ | $(1, 2)$ | $(1, 3)$ | $1.4656^k$ |
|---|---|---|---|---|
| 10 | 1024 | 89 | 28 | 46 |
| 20 | 1048576 | 10946 | 1278 | 2090 |

Many more rules of this kind, with a careful case analysis, lead to the $O(1.2738^k + kn)$ algorithm of Chen, Kanj and Xia.

### 3-Hitting set and cluster editing: three branches

In [d-hitting set](/parameterized-hitting-set/), each set has at most $d$ elements, and we must choose $k$ elements that hit every set. An unhit set $\{a, b, c\}$ is the obstacle, and the branches take $a$, $b$ or $c$, each with budget $k - 1$. The vector is $(1, 1, 1)$ and the tree has $3^k$ leaves; for sets of size $d$ it has $d^k$.

[Cluster editing](/cluster-editing/) asks if at most $k$ edge insertions and deletions turn a graph into a disjoint union of cliques. A graph is such a union exactly when it has no induced path $u - v - w$, that is, edges $\{u, v\}$ and $\{v, w\}$ but no edge $\{u, w\}$. Every solution must change one of these three pairs, so the branches delete $\{u, v\}$, delete $\{v, w\}$ or insert $\{u, w\}$, each with budget $k - 1$. Each changed pair must also be marked as fixed, so that a later branch does not undo the change. The tree has at most $3^k$ leaves.

### Independent set in planar graphs: a bounded choice from structure

Independent set with the solution size $k$ as the parameter is W[1]-hard in general graphs, but a bounded search tree solves it on [planar graphs](/planar-graph/). Every planar graph has a vertex $v$ of degree at most 5, by Euler's formula. Some largest independent set contains a vertex of $N[v]$: if a set $S$ contains none, then $S \cup \{v\}$ is independent and larger. So the branches choose one $w \in N[v]$, put it in the set, delete $N[w]$, and keep looking for $k - 1$ more vertices. There are at most 6 branches, the graph stays planar, and the tree has at most $6^k$ leaves. Here the parameter falls toward 0 as the solution grows, so the base case is $k = 0$, which is a yes-instance.

## Variations

- **Measure and conquer.** Instead of $k$, the analysis uses a finer measure, such as a weighted count of vertices by degree, that drops more in some branches. The algorithm stays the same, but the bound improves. See [measure and conquer](/measure-and-conquer/).
- **Kernel first.** Run a [kernelization](/kernelization/) before the search. The tree then works on an instance of size $g(k)$, and the time becomes $O(\mathrm{poly}(n) + c^k \cdot \mathrm{poly}(g(k)))$. Running the reduction rules again at every node of the tree often helps more in practice.
- **Branch and reduce.** [Branch and reduce](/branch-and-reduce/) applies reduction rules at each node and branches only when no rule applies. With the input size $n$ as the measure instead of $k$, the same analysis gives [exact exponential algorithms](/exact-exponential-algorithms/) with time $O^\ast(c^n)$ for a $c$ below the brute-force base.
- **Optimization.** To find a least solution, run BST with $k = 0, 1, 2, \ldots$ until it answers YES. The total time is at most a constant times the time of the last run, because $c^k$ grows geometrically when $c > 1$.
- **Satisfiability.** The [DPLL](/dpll/) procedure branches on the value of a variable. For 3-SAT, branching on the literals of an unsatisfied clause $(a \lor b \lor c)$ gives the cases $a$; $\lnot a, b$; $\lnot a, \lnot b, c$, with the vector $(1, 2, 3)$ in the number of fixed variables and the branching number 1.8393.

## Pitfalls

- **Branches that are not exhaustive.** For vertex cover with a vertex $v$ of degree $d$, the branches "take $v$" and "take one neighbor of $v$" are wrong: a cover without $v$ must take all of $N(v)$. The right second branch takes all $d$ neighbors.
- **A branch with no progress.** A branch with $d_i = 0$ can repeat forever. Every branch must lower the parameter or another measure that is bounded by a function of $k$.
- **Choices that grow with n.** Branching on "any vertex" gives $n$ children per node and $n^k$ leaves. The obstacle must be small, with a number of fixes bounded by a constant or a function of $k$.
- **The wrong root.** The branching number of $(1, 2)$ is 1.618, not 1.5. Solve $\sum_i c^{-d_i} = 1$; do not average the drops.
- **Undoing a decision.** In cluster editing, a later branch may delete an edge that an earlier branch inserted. Mark changed pairs as fixed, or the budget does not bound the depth.
- **A base case that is not polynomial.** The branching number of the vertex cover rule with degree at least 3 is valid only because graphs of maximum degree 2 are solved directly. A base case that needs its own search breaks the bound.

## Exercises

1. Show that the branching number of $(1, 1, \ldots, 1)$ with $t$ entries is $t$, and that the branching number of $(d, d)$ is $2^{1/d}$.
2. Prove that the branching number of $(1, 2)$ is the golden ratio $(1 + \sqrt{5})/2$, and compute the number of leaves for $k = 10$ from the recurrence.
3. Give a bounded search tree for vertex cover in graphs of maximum degree 3 that branches on a vertex of degree 3 and its neighbors, and find its branching vector.
4. Feedback vertex set in tournaments: a tournament has no directed cycle if and only if it has no directed triangle. Use this to give an $O^\ast(3^k)$ algorithm that deletes at most $k$ vertices to make a tournament acyclic.
5. A 2-SAT formula can be solved in polynomial time. Give a bounded search tree for the question whether at most $k$ variables can be fixed so that a CNF formula becomes a 2-SAT formula, where each clause has at most three literals.

## References
