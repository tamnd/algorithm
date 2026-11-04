---
tag: 2DQCEQ
kind: concept
slug: uniform-matroid
name: Uniform matroid
aliases:
- U(k,n)
- free matroid
area: techniques/greedy
level: advanced
summary: A matroid on a ground set in which the independent sets are exactly those with at most k elements.
prereqs: [matroid]
see_also: [matroid, partition-matroid, linear-matroid, matroid-greedy-algorithm, top-k-selection, selection-problem, secretary-problem]
sources:
  - book: isbn:9780199603398
    title: James Oxley, Matroid Theory, second edition
    locator: Chapter 1, Basic definitions and examples (uniform matroids)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 13, Matroids
---

The uniform matroid $U_{k,n}$ has a ground set of $n$ elements, and a set is independent when it has at most $k$ elements. It is the simplest [matroid](/matroid/): independence depends only on size. Its bases are the $k$-element subsets, and the [matroid greedy algorithm](/matroid-greedy-algorithm/) on it picks the $k$ heaviest elements. The extreme cases are $U_{n,n}$, the *free* matroid in which every set is independent, and $U_{0,n}$, in which only the empty set is.

## In plain words

You may take any items you like, but no more than $k$ of them. Which items they are does not matter, only how many. That rule is a uniform matroid.

It is a matroid because a small allowed group can always take one more item from a larger allowed group: the larger group has an item that the small one lacks, and the small group is still under the limit.

To get the most value, sort the items by value and take the top $k$ with a positive value. This is the greedy algorithm, and here it is obvious that it is right. Uniform matroids are the base case that many other matroids, and many problems with a size limit, build on.

## The idea

**Definition.** For integers $0 \le k \le n$ and a set $E$ with $|E| = n$, the uniform matroid $U_{k,n}$ on $E$ has the independent sets $\mathcal{I} = \{X \subseteq E : |X| \le k\}$.

**It is a matroid.** (I1) $|\emptyset| = 0 \le k$. (I2) A subset of a set with at most $k$ elements has at most $k$ elements. (I3) If $|X| < |Y| \le k$, then $Y \setminus X$ is not empty, and for any $y \in Y \setminus X$, $|X \cup \{y\}| = |X| + 1 \le |Y| \le k$. $\square$

**Rank, bases and circuits.** The rank of $X$ is $r(X) = \min(|X|, k)$. The bases are the $\binom{n}{k}$ subsets of size $k$. For $k < n$, the circuits are the subsets of size $k + 1$; $U_{n,n}$ has no circuits.

**Dual.** The complement of a $k$-subset is an $(n - k)$-subset, so the dual of $U_{k,n}$ is $U_{n-k,n}$.

**Greedy.** With weights $w$, the greedy algorithm takes elements by decreasing weight until it has $k$ of them. A maximum-weight basis is a set of $k$ heaviest elements, which [top-k selection](/top-k-selection/) finds in $O(n)$ time with a linear-time [selection](/selection-problem/) algorithm, without a full sort. A maximum-weight independent set takes the heaviest $\min(k, p)$ elements, where $p$ is the number of elements of positive weight.

**Representation.** $U_{k,n}$ is a [linear matroid](/linear-matroid/) over every field with enough elements: $n$ vectors in $\mathbb{F}^k$ in general position, for example the columns $(1, t, t^2, \ldots, t^{k-1})$ for $n$ distinct values $t$, any $k$ of which form an invertible Vandermonde matrix. Over a small field this can fail: $U_{2,4}$ is not representable over $\mathbb{F}_2$, because $\mathbb{F}_2^2$ has only three nonzero vectors and four pairwise independent vectors are needed.

## Examples

**$U_{2,4}$.** On $E = \{a, b, c, d\}$, the independent sets are $\emptyset$, the 4 singletons and the 6 pairs. The bases are the 6 pairs, and the circuits are the 4 triples. Over $\mathbb{F}_3$ it is represented by the vectors $(1, 0)$, $(0, 1)$, $(1, 1)$, $(1, 2)$.

**Greedy on $U_{3,6}$.** Weights $8, -2, 5, 5, 1, 9$ on elements $1, \ldots, 6$. Greedy takes element 6 (9), element 1 (8), and one of elements 3 and 4 (5), and stops at size 3, with weight 22. Both $\{1, 3, 6\}$ and $\{1, 4, 6\}$ are maximum-weight bases. The element of weight $-2$ is never reached.

**Free matroid.** $U_{n,n}$: every subset is independent, and the only basis is $E$. The maximum-weight independent set is the set of elements with positive weight.

**A partition matroid with one block.** A [partition matroid](/partition-matroid/) with a single block of capacity $k$ is $U_{k,n}$. Conversely, a partition matroid is a direct sum of uniform matroids, one for each block.

## Where it is used

- **Cardinality constraints.** "Choose at most $k$" is the constraint of a uniform matroid. Results proved for matroid constraints, such as approximation bounds for submodular maximization, apply to it.
- **Top-$k$ selection.** Picking the $k$ best items is the greedy algorithm on $U_{k,n}$; see [top-k selection](/top-k-selection/).
- **Online selection.** The [secretary problem](/secretary-problem/) with $k$ choices is the online version of a maximum-weight basis on $U_{k,n}$, and the starting case of the matroid secretary problem.
- **Counterexamples in matroid theory.** $U_{2,4}$ is the smallest matroid that is not binary, and many proofs about representability start from it.

## References
