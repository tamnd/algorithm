---
tag: A1A979
kind: theorem
slug: comparison-sort-lower-bound
name: Comparison sorting lower bound
aliases:
- Omega(n log n) lower bound for sorting
- Omega(n log n) sorting bound
- sorting lower bound
area: sorting/comparison-sorts
level: core
summary: Any comparison sort needs Omega(n log n) comparisons in the worst case, since a decision tree needs n! leaves.
prereqs: [comparison-sort, decision-tree-model, logarithms, asymptotic-notation]
see_also: [information-theoretic-bound, decision-tree-method, merge-sort-optimality, ford-johnson-algorithm, element-distinctness-lower-bound, integer-sorting, stirling-approximation, comparison-model]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1, Lower bounds for sorting (Theorem 8.1 and Corollary 8.2), and Problem 8-1, Probabilistic lower bounds on comparison sorting
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1, Minimum-comparison sorting (the bound S(n) at least ceil(lg n!), the average bound by external path length, and the table of S(n))
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Mergesort (Proposition I, no compare-based algorithm can guarantee to sort N items with fewer than lg(N!) compares)
  - paper: "Marcin Peczarski, New results in minimum-comparison sorting, Algorithmica 40 (2004)"
    locator: pp. 133 to 145 (the values of S(13), S(14) and S(22))
  - paper: "Florian Stober and Armin Weiss, Lower bounds for sorting 16, 17, and 18 elements, arXiv:2206.05597 (2022)"
    locator: abstract and the table of known values
---

The comparison sorting lower bound says that each [comparison sort](/comparison-sort/) makes at least $\lceil \lg(n!) \rceil$ comparisons on some input of $n$ distinct keys, and at least $\lg(n!)$ comparisons on average over the $n!$ orders. Since $\lg(n!) = n \lg n - n \lg e + O(\log n)$, no comparison sort beats $\Omega(n \log n)$ in the worst case or on average, so [merge sort](/merge-sort/) and [heapsort](/heapsort/) are optimal up to a constant factor. The bound holds only in the [comparison model](/comparison-model/): [integer sorting](/integer-sorting/) with other operations can be faster.

## Statement

Let $n \ge 1$. Consider inputs $a_1, \dots, a_n$ of distinct keys from a totally ordered set. A comparison sort learns about the keys only by two-way comparisons $a_i < a_j$ or three-way comparisons of $a_i$ and $a_j$. Here $\lg = \log_2$.

**Theorem.**

1. **(Worst case.)** Each deterministic comparison sort makes at least $\lceil \lg(n!) \rceil$ comparisons on some input.
2. **(Average case.)** For each deterministic comparison sort, the average number of comparisons over the $n!$ orders of $n$ distinct keys, each with probability $1/n!$, is at least $\lg(n!)$.
3. **(Randomized.)** For each randomized comparison sort that is always correct, there is an input on which the expected number of comparisons is at least $\lg(n!)$.
4. **(Size.)** For $n \ge 1$,
$$n \lg n - n \lg e + \lg e \;\le\; \lg(n!) \;\le\; n \lg n,$$
so $\lg(n!) = n \lg n - O(n)$, and the three bounds above are $\Omega(n \log n)$.

## In plain words

A sorting method that only compares pairs can be drawn as a tree of questions. Each question has two answers, so each step down the tree at most doubles the number of different endings. The method must end in a different place for each of the possible orders of the items, because each order needs a different rearrangement. Ten items have more than three million orders. A tree that has that many endings must be at least 22 questions deep. So some input costs at least 22 comparisons.

The same counting works for the average. A tree with many endings cannot have most of them near the top, so the typical ending is also deep. Random choices do not help, because a random method is just a random choice of one of these trees.

## Proof

Fix $n$. A deterministic comparison sort, run on inputs of $n$ distinct keys, forms a [decision tree](/decision-tree-model/) $T$: each inner node is a comparison, each edge is an answer, and each leaf is an output. The number of comparisons on an input is the depth of the leaf that it reaches. On distinct keys a three-way comparison never answers "equal", so we delete those edges and $T$ is a tree in which each node has at most two children.

**Step 1: the inputs reach $n!$ different leaves.** Take the inputs $a^\sigma$ for the $n!$ permutations $\sigma$ of $\{1, \dots, n\}$, with $a^\sigma_i = \sigma(i)$. For each $\sigma$ there is exactly one permutation $\pi$ with $a^\sigma_{\pi(1)} < \cdots < a^\sigma_{\pi(n)}$, namely $\pi = \sigma^{-1}$. Two different $\sigma$ need two different outputs. The output depends only on the leaf, so they reach two different leaves. Let $\Lambda$ be this set of $n!$ leaves.

**Step 2: height.** A tree in which each node has at most two children has at most $2^h$ leaves at depth $h$ or less: this is true for $h = 0$, and each node at depth $h$ has at most 2 children at depth $h + 1$. So $2^{\text{height}(T)} \ge |\Lambda| = n!$, and since the height is an integer, it is at least $\lceil \lg(n!) \rceil$. The leaf of greatest depth in $\Lambda$ belongs to an input with that many comparisons. This proves part 1.

**Step 3: average depth.** Let $D(L)$ be the least possible sum of the depths of $L$ leaves of a tree with at most two children per node. We prove $D(L) \ge L \lg L$ by strong induction on $L$. For $L = 1$, $D(1) \ge 0 = 1 \lg 1$. For $L \ge 2$, take a tree and $L$ of its leaves, and cut away each part that contains none of them. If the root has one child, removing the root lowers each depth by 1, so the sum was larger than for a smaller tree, and we may assume that the root has two children whose subtrees hold $L_1 \ge 1$ and $L_2 \ge 1$ of the leaves, with $L_1 + L_2 = L$. Each depth is 1 more than the depth in its subtree, so by the induction hypothesis the sum is at least
$$L_1 \lg L_1 + L_2 \lg L_2 + L.$$
The function $x \lg x$ is convex on $x > 0$, so $L_1 \lg L_1 + L_2 \lg L_2 \ge 2 \cdot \tfrac{L}{2} \lg \tfrac{L}{2} = L \lg L - L$. So the sum is at least $L \lg L$. Apply this to the $n!$ leaves of $\Lambda$: the sum of the comparisons over all $n!$ inputs is at least $n! \lg(n!)$, and the average is at least $\lg(n!)$. This proves part 2.

**Step 4: randomness.** A randomized comparison sort that is always correct chooses its random bits $r$ and then runs a deterministic comparison sort $T_r$. Let $C(r, \sigma)$ be the number of comparisons of $T_r$ on $a^\sigma$. By Step 3, $\frac{1}{n!}\sum_\sigma C(r, \sigma) \ge \lg(n!)$ for each $r$. Take the expectation over $r$ and exchange the two averages:
$$\frac{1}{n!}\sum_\sigma \mathbb{E}_r[C(r, \sigma)] \ge \lg(n!).$$
An average of $n!$ numbers is at most their maximum, so $\mathbb{E}_r[C(r, \sigma)] \ge \lg(n!)$ for some $\sigma$. This proves part 3.

**Step 5: size.** Each factor of $n!$ is at most $n$, so $n! \le n^n$ and $\lg(n!) \le n \lg n$. For the lower bound, $\ln$ is increasing, so $\ln k \ge \int_{k-1}^{k} \ln x \, dx$ for $k \ge 2$. Summing over $k = 2, \dots, n$ gives
$$\ln(n!) \ge \int_1^n \ln x \, dx = n \ln n - n + 1.$$
Divide by $\ln 2$ and use $\lg e = 1/\ln 2$ to get $\lg(n!) \ge n \lg n - n \lg e + \lg e$. This proves part 4. $\blacksquare$

## Consequences

- **Optimal sorts.** [Merge sort](/merge-sort/) and [heapsort](/heapsort/) make $O(n \log n)$ comparisons in the worst case, so they are asymptotically optimal comparison sorts (CLRS, Corollary 8.2). Merge sort is within about $0.53 n$ comparisons of the bound. See [merge sort optimality](/merge-sort-optimality/).
- **Quicksort on average.** Randomized [quicksort](/quicksort/) makes about $2 n \ln n \approx 1.39\, n \lg n$ comparisons in expectation. By part 3, no randomized comparison sort can make fewer than $\lg(n!)$ on its worst input, so the constant of quicksort cannot go below 1 in front of $n \lg n$.
- **Data structures.** A [binary search tree](/binary-search-tree/) built by comparisons gives the sorted order by an in-order walk in $O(n)$ time. So building one from $n$ keys needs $\Omega(n \log n)$ comparisons. In the same way, a comparison-based [priority queue](/priority-queue/) that supports $n$ inserts and $n$ extract-min operations sorts, so some operation costs $\Omega(\log n)$ amortized comparisons.
- **Element distinctness.** A longer argument gives the same bound $\lceil \lg(n!) \rceil$ for deciding whether $n$ keys are distinct, although that problem has only two answers. See the [element distinctness lower bound](/element-distinctness-lower-bound/).
- **Other models.** The bound fails outside the model. On the [word RAM](/word-ram/), [radix sort](/radix-sort/) sorts $n$ integers of $O(\log n)$ bits in $O(n)$ time.

## Tightness

The bound is tight in its leading term. Merge sort, binary insertion and the [Ford-Johnson algorithm](/ford-johnson-algorithm/) all make $n \lg n - \Theta(n)$ comparisons in the worst case. The Ford-Johnson algorithm makes $\sum_{k=1}^{n} \lceil \lg(3k/4) \rceil$, which is about $n \lg n - 1.415 n$ for some $n$, against $\lg(n!) \approx n \lg n - 1.443 n$.

The bound is not always exact. Let $S(n)$ be the least worst-case number of comparisons of any comparison sort of $n$ keys.

| $n$ | 5 | 10 | 12 | 16 | 20 | 100 | 1000 |
|---|---|---|---|---|---|---|---|
| $\lceil \lg(n!) \rceil$ | 7 | 22 | 29 | 45 | 62 | 525 | 8530 |
| $n \lg n - n \lg e + \lg e$ | 5.84 | 20.24 | 27.15 | 42.36 | 59.03 | 521.56 | 8524.53 |
| Ford-Johnson | 7 | 22 | 30 | 46 | 62 | 534 | 8641 |

The bound $\lceil \lg(n!) \rceil$ equals $S(n)$ for $n \le 11$ and for $n = 20$ and $n = 21$, but $S(12) = 30$ (Knuth, Section 5.3.1), $S(13) = 34$ and $S(14) = 38$ (Peczarski, 2004), each one more than the bound. Whether $S(n) - \lg(n!)$ grows linearly in $n$ is an open question.

The average bound in part 2 is also tight up to $O(n)$: merge sort and binary insertion make $n \lg n - O(n)$ comparisons on average.

## History

The counting argument belongs to the early study of sorting with the fewest comparisons, which also produced the merge insertion method of Ford and Johnson (1959). Knuth, Section 5.3.1, presents the worst-case bound, the average bound through the external path length of the tree, and the known values of $S(n)$. The value $S(12) = 30$, the first case where the bound is not exact, was found by a computer search by Wells in 1965. Later searches found $S(13)$, $S(14)$ and $S(22)$ (Peczarski, 2004) and $S(16)$ to $S(18)$ (Stober and Weiss, 2022).

## References
