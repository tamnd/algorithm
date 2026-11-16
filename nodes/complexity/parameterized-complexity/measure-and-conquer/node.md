---
tag: 67X6DJ
kind: technique
slug: measure-and-conquer
name: Measure and conquer
aliases:
- measure-and-conquer analysis
area: complexity/parameterized-complexity
level: research
summary: "Analyze a branching algorithm with a weighted measure of the instance instead of its size. Good weights prove a smaller base for the same algorithm, such as 1.2201^n for independent set."
prereqs: [branch-and-reduce, recurrence-relation]
see_also: [branch-and-reduce, bounded-search-tree, exact-exponential-algorithms, maximum-independent-set, dominating-set, set-cover, parameterized-feedback-vertex-set, iterative-compression]
sources:
  - paper: doi:10.1145/1552285.1552286
    title: "Fedor V. Fomin, Fabrizio Grandoni and Dieter Kratsch, A measure and conquer approach for the analysis of exact algorithms, Journal of the ACM 56(5), article 25 (2009)"
    locator: the method, independent set in time O*(1.2201^n), and dominating set through set cover in time O(1.5260^n) with polynomial space and O(1.5137^n) with exponential space
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 6, Measure & Conquer
---

Measure and conquer is a way to analyze branching algorithms more sharply. A branching algorithm splits an instance into smaller ones and recurses. The usual analysis measures each instance by a simple size, such as the number $n$ of vertices or the parameter $k$, and solves a recurrence for the number of leaves of the search tree. Measure and conquer replaces the simple size by a *measure* $\mu$ that gives different weights to different parts of the instance, for example a weight to each vertex that depends on its degree. A vertex of degree 2 is easier to handle than one of degree 5, so it gets a smaller weight. Each branching rule then drops the measure by more in its worst case, and the bound in terms of $\mu$, and so in terms of $n$, gets better. The algorithm does not change; only the proof does. Fomin, Grandoni and Kratsch introduced the method in 2005 and proved with it that a simple algorithm for [maximum independent set](/maximum-independent-set/) runs in time $O^*(1.2201^n)$ and one for [dominating set](/dominating-set/) in time $O(1.5260^n)$, where $O^*$ hides factors polynomial in $n$. It is a tool of [exact exponential algorithms](/exact-exponential-algorithms/), and it applies the same way to parameterized ones, where the measure combines $k$ with other quantities.

## In plain words

A search that splits a problem into smaller ones is often judged by counting how many pieces are left after each split. But not all pieces are equally hard. A point with few links is nearly solved; a point with many links is the real work.

So give each part of the problem a weight that says how much work it still holds. Then measure the progress of each split by the drop in total weight, not by the drop in count.

With good weights, the bad cases of the old count turn out to make good progress. The same search then gets a better time bound. You find the best weights by trying many and keeping the ones that give the smallest bound.

## When it applies

- The algorithm is a [branch and reduce](/branch-and-reduce/) algorithm: reduction rules that make the instance simpler, and branching rules that split it.
- The plain analysis has worst cases that are rare or weak in some sense, for example when the branching vertex has neighbors of small degree, which the reduction rules then remove for free.
- The parts of the instance have a natural type, such as the degree of a vertex or the size of a set, and parts of different types differ in how hard they are.
- The parameter of the bound is the size $n$ of the instance, or the parameter $k$ of a parameterized problem. The measure is at most $n$ (or bounded by a function of $k$), so a bound $c^{\mu}$ gives a bound in the parameter.

## The template

The algorithm is a plain branching algorithm. The template has three holes: the measure $\mu$, the reduction rules REDUCE, and the branching rules BRANCH.

```pseudo id=main
SOLVE(I)                              ▷ an optimal solution of the instance I
L1  apply the rules of REDUCE to I while one applies
L2  if I is simple then solve I directly and return the result
L3  choose a rule of BRANCH that applies to I
L4  let I_1, …, I_t be the instances it makes
L5  for j ← 1 to t do r_j ← SOLVE(I_j)
L6  return the best r_j, mapped back to a solution of I
```

The analysis has three steps.

1. *Choose the measure.* For a graph, $\mu(G) = \sum_{v} w(\deg v)$ with a weight function $w$ that grows with the degree and has $w(d) \le 1$, so $\mu(G) \le n$.
2. *List the cases.* For each branching rule and each case of the neighborhood, compute a lower bound $\Delta_j$ on the drop of $\mu$ in branch $j$. The *branching number* of the case is the unique $x > 1$ with $\sum_j x^{-\Delta_j} = 1$.
3. *Optimize.* Let $c$ be the largest branching number over all cases. Choose the weights that make $c$ as small as possible.

**Lemma.** Suppose the reduction rules never increase $\mu$, every $\Delta_j$ is at least some constant $\delta > 0$, instances with $\mu \le 0$ are simple, and the work per node of the search tree is polynomial. Then the search tree has at most $c^{\mu(I)}$ leaves, and SOLVE runs in time $O^*(c^{\mu(I)})$.

*Proof.* By induction on the number of branch steps that remain, which is at most $\mu(I)/\delta$. A simple instance is one leaf, and $c^{\mu} \ge 1$ for $\mu \ge 0$. Otherwise the leaves are at most $\sum_j c^{\mu - \Delta_j} = c^{\mu} \sum_j c^{-\Delta_j} \le c^{\mu}$, since $c$ is at least the branching number of the case, and $x \mapsto \sum_j x^{-\Delta_j}$ falls as $x$ grows. $\square$

Since $\mu(I) \le n$, the time is $O^*(c^n)$.

## Classic examples

### A simple independent set algorithm

The algorithm takes a vertex of degree 0 or 1 into the solution and deletes its closed neighborhood, solves a graph of maximum degree 2 directly (it is a union of paths and cycles), and otherwise branches on a vertex $v$ of maximum degree $d \ge 3$: discard $v$, or take $v$ and delete its closed neighborhood.

The plain analysis uses $\mu = n$. The worst case is $d = 3$: the branches remove 1 and 4 vertices, so $T(n) \le T(n - 1) + T(n - 4)$, with the branching number $1.3803$.

Now give each vertex the weight $w(\deg v)$, with $w(0) = w(1) = 0$, $w(2) = \alpha$, $w(3) = \beta$ and $w(d) = 1$ for $d \ge 4$. When the algorithm branches, every vertex has degree at least 2 and at most $d$. In the discard branch, $\mu$ drops by $w(d)$ for $v$ and by $w(d_u) - w(d_u - 1)$ for each neighbor $u$ of degree $d_u$. In the take branch, it drops by $w(d)$ and by $w(d_u)$ for each neighbor; the drops of vertices further away only help, and the bound ignores them. The worst case over all degrees $d$ and all neighbor degrees gives:

| weights $(\alpha, \beta)$ | worst case | drops | bound |
|---|---|---|---|
| $(1, 1)$, as with $\mu = n$ | $d = 3$, neighbors of degree 3 | 1 and 4 | $1.3803^n$ |
| $(0.5, 1)$ | $d = 4$, neighbors of degree 4 | 1 and 5 | $1.3247^n$ |
| $(0.6, 0.94)$ | $d = 4$, neighbors of degree 4 | 1.24 and 5 | $1.2952^n$ |

The first row is the plain analysis. With $\alpha = 0.5$, the case $d = 3$ with three neighbors of degree 2 drops $\mu$ by $2.5$ in both branches, which is much better than it looks with $\mu = n$, and the worst case moves to $d = 4$. With a weight for degree 3 as well, the two cases balance further. The algorithm is the same in all three rows.

### Independent set, the full result

Fomin, Grandoni and Kratsch analyzed an algorithm with a few more rules (folding of vertices of degree 2, and branching on *mirrors*) and weights that depend on the degree. Measure and conquer proves the bound $O^*(1.2201^n)$ for it, while an analysis with $\mu = n$ gives a weaker bound for the same algorithm. Kneis, Langer and Rossmanith later lowered the base to $1.2132$ with a finer analysis.

### Dominating set through set cover

Dominating set on $G$ is [set cover](/set-cover/) with the universe $V$ and the sets $N[v]$. A branching algorithm for set cover picks a largest set $S$ and either takes it or discards it. Fomin, Grandoni and Kratsch weight each set by a function of its size and each element by a function of its frequency, the number of sets that contain it. The result is $O(1.5260^n)$ time with polynomial space, and $O(1.5137^n)$ with exponential space for memoization. Van Rooij and Bodlaender (2008) designed new rules with the help of the same analysis and reached $O(1.5063^n)$.

## Variations

- *Design by measure and conquer.* Look at the worst cases of the optimized analysis, add a rule that handles them, and analyze again. Van Rooij and Bodlaender used this loop for dominating set.
- *Parameterized measures.* In a parameterized algorithm the measure can mix $k$ with other values, for example $k$ minus a lower bound on the solution size, or $k$ plus weights on vertices of small degree. The bound $c^{\mu}$ then gives $c^{f(k)}$ when $\mu \le f(k)$. Sharper analyses of branching for [feedback vertex set](/parameterized-feedback-vertex-set/) use such measures.
- *Finding the weights.* The largest branching number is a quasiconvex function of the weights, so a local search or a convex program finds the best weights.
- *Lower bounds for an algorithm.* A family of instances on which the algorithm takes long shows how far the analysis is from the truth. For most measure and conquer results a gap remains.

## Pitfalls

- A reduction rule that increases the measure. Folding or merging can raise a degree; the analysis must check that $\mu$ does not grow, or count the increase.
- Weights that go below zero in a case. A drop $\Delta_j \le 0$ breaks the lemma; every branch must drop $\mu$ by a positive constant.
- Forgetting a case. The analysis is only as strong as the list of cases; a computer enumeration of the cases is safer than a hand list.
- Reading the bound as the true running time. Measure and conquer gives an upper bound; the real worst case of the algorithm can be much lower, and it is usually unknown.
- A measure larger than $n$. If some weight exceeds 1, the bound $c^{\mu}$ is not $c^n$; it is $c^{w_{\max} n}$.

## Exercises

1. For the simple independent set algorithm, show that the reduction rules never increase $\mu$ when $w$ is nondecreasing.
2. Compute the branching number of the case $d = 3$ with three neighbors of degree 2 for $\alpha = 0.5$ and $\beta = 1$. (Answer: $2^{1/2.5} \approx 1.3195$.)
3. Show that for $\alpha = 0.25$ and $\beta = 1$ the same case gives a branching number of about $1.486$, worse than the plain analysis. What does this say about small weights?
4. Add a rule that solves all graphs of maximum degree 3 directly, and redo the analysis with weights only for degrees 2 and 3 of the neighbors. What changes in the worst case?
5. For set cover, explain why an element of frequency 1 forces its set into the solution, and why such elements can get weight 0.

## References
