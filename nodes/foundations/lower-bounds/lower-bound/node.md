---
tag: C2VB94
kind: concept
slug: lower-bound
name: Lower bound
aliases:
- complexity lower bound
- Omega bound
area: foundations/lower-bounds
level: intro
summary: A bound showing every algorithm for a problem needs at least a given cost; the counterpart of an upper bound.
prereqs: [asymptotic-notation, worst-case-analysis, upper-bound]
see_also: [optimality, trivial-lower-bound, counting-argument, information-theoretic-bound, decision-tree-method, adversary-argument, reduction-lower-bound, decision-tree-model]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 3.1 (Omega-notation), Section 8.1 (Lower bounds for sorting, Theorem 8.1) and Section 9.1 (minimum and maximum, the lower bound of n - 1)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (the information-theoretic lower bound for sorting), Section 5.3.2 (merging) and Section 5.3.3 (selection, the lower bounds for the largest and second largest)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 2.2, Asymptotic Order of Growth (asymptotic lower bounds)
  - paper: doi:10.1145/361405.361423
    title: Ira Pohl, A sorting problem and its complexity, Communications of the ACM 15(6) (1972)
    locator: pp. 462 to 464
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983)"
    locator: the main theorem and its application to element distinctness
---

A lower bound for a problem is a cost that **every** algorithm in a given [model of computation](/decision-tree-model/) must pay on some input. It is the counterpart of an [upper bound](/upper-bound/), which needs only one good algorithm. Lower bounds come from arguments about all possible algorithms at once: a [counting argument](/counting-argument/), an [adversary argument](/adversary-argument/) or a [reduction](/reduction-lower-bound/). When a lower bound meets an upper bound, the algorithm is [optimal](/optimality/) and the search for a faster one in that model is over.

## In plain words

An upper bound is a promise from one algorithm: "I never need more than this much work." A lower bound is a statement about every algorithm that anybody will ever write: "No method can do the job with less than this much work, on its worst input."

So a lower bound must reason about methods that nobody has found yet. It does this by looking at what any method must learn. To find the largest of a list of items, a method must rule out every other item, and one comparison can rule out only one. To sort, a method must tell apart every possible order of the items, and one comparison gives only one yes or no.

A lower bound always holds for a stated set of allowed steps. Allow stronger steps, and a faster method can appear.

## The idea

**The definition.** Fix a problem $P$, a model $M$, a cost measure and a case. Let $W_B(n)$ be the worst-case cost of an algorithm $B$ on inputs of size $n$. A function $L$ is a **lower bound** for $P$ in $M$ when

$$\text{for each algorithm } B \text{ of } M \text{ that solves } P, \text{ and for each } n \ge n_0: \quad W_B(n) \ge L(n).$$

Equivalently, for each such $B$ and each $n \ge n_0$ there is an input $x$ of size $n$ with $\mathrm{cost}_B(x) \ge L(n)$. The bad input may depend on $B$. In the asymptotic form, $W_B(n) = \Omega(L(n))$ for each $B$. Let $C_P(n) = \min_B W_B(n)$ be the cost of the best algorithm. Then $L$ is a lower bound exactly when $C_P(n) \ge L(n)$ for $n \ge n_0$, and $U$ is an upper bound when $C_P(n) \le U(n)$. The true complexity $C_P(n)$ lies between them.

**Lower bound of an algorithm and of a problem.** "Insertion sort takes $\Omega(n^2)$ time in the worst case" is a lower bound on one algorithm. It needs one bad input, the reversed array. "Every comparison sort takes $\Omega(n \log n)$ comparisons in the worst case" is a lower bound on the problem. It quantifies over all algorithms. Only the second kind tells you that a better algorithm does not exist. In this reference "a lower bound for a problem" always means the second kind.

**The four parts.** A lower bound names its problem, its model, its cost measure and its case.

- **Model.** The bound $\lceil \lg(n!) \rceil$ for sorting holds in the [comparison model](/comparison-model/). [Radix sort](/radix-sort/) on the [word RAM](/word-ram/) beats it for small integers, because it is not in that model.
- **Cost measure.** A bound on comparisons is not a bound on memory or on moves.
- **Case.** A worst-case lower bound says that some input is hard. An average-case lower bound says that inputs are hard on average under a stated distribution. A lower bound for randomized algorithms bounds the expected cost on the worst input, and it usually comes from the [Yao minimax principle](/yao-minimax-principle/).
- **Problem.** A lower bound for sorting is not a lower bound for [selection](/selection-problem/), which takes $O(n)$ comparisons.

**How lower bounds are proved.** An argument must cover algorithms that nobody has written. The standard methods are these.

- The [trivial lower bound](/trivial-lower-bound/): each relevant input item must be read, and each output item must be written.
- A [counting argument](/counting-argument/), and its main case the [information-theoretic bound](/information-theoretic-bound/): an algorithm with cost $h$ has at most $2^h$ different behaviours, and the problem needs more.
- The [decision tree method](/decision-tree-method/): view the algorithm as a tree of queries, and bound the depth of each tree that solves the problem.
- The [adversary argument](/adversary-argument/): answer the queries of the algorithm so that it learns as little as possible.
- A [reduction](/reduction-lower-bound/): if problem $Q$ has a lower bound and $Q$ reduces cheaply to $P$, then $P$ has nearly the same lower bound.
- A [conditional lower bound](/conditional-lower-bound/): a bound that holds if a conjecture, such as the [3SUM](/3sum/) conjecture, is true.

**Why lower bounds are rare.** For general models, such as the word RAM, very few super-linear lower bounds are known for explicit problems. Most proved bounds hold in restricted models, such as the comparison model, [decision trees](/decision-tree-model/), [algebraic decision trees](/algebraic-decision-tree/) or the [cell-probe model](/cell-probe-model/), where the steps are simple enough to reason about.

## Examples

The table lists lower bounds with their models and the best upper bound. All bounds are on the number of comparisons in the worst case, for $n$ distinct items, unless the row says otherwise.

| problem | lower bound | upper bound | gap |
|---|---|---|---|
| maximum | $n - 1$ | $n - 1$ (one scan) | none |
| maximum and minimum | $\lceil 3n/2 \rceil - 2$ | $\lceil 3n/2 \rceil - 2$ (pairs) | none |
| largest and second largest | $n + \lceil \lg n \rceil - 2$ | the same (tournament) | none |
| search in a sorted array | $\lceil \lg(n+1) \rceil$ | the same (binary search) | none |
| merge two sorted lists of $n$ each | $2n - 1$ | $2n - 1$ | none |
| sorting | $\lceil \lg(n!) \rceil$ | $n \lg n - 1.329\,n + O(\log n)$ (merge insertion) | $\Theta(n)$ |
| median | $(2 + \varepsilon)\,n$ | $2.95\,n + o(n)$ | constant factor |
| element distinctness | $\lceil \lg(n!) \rceil$ | $n \lg n + O(n)$ (sort, then scan) | $\Theta(n)$ |

For $n = 8$ the first four rows give 7, 10, 9 and 4 comparisons. For sorting 8 items the lower bound is $\lceil \lg 40320 \rceil = 16$, and the best possible worst case is also 16.

Each row has its own page: the [maximum](/max-finding-lower-bound/), the [maximum and minimum](/max-min-lower-bound/) (Pohl, 1972), the [second largest](/second-largest-lower-bound/), [sorted search](/sorted-search-lower-bound/), [merging](/merging-lower-bound/), [sorting](/comparison-sort-lower-bound/), the [selection lower bound](/selection-lower-bound/) and [element distinctness](/element-distinctness/). The bound for sorting is not exact: for $n = 12$ it gives 29, and the least worst case is 30 (Knuth, Section 5.3.1).

Outside the comparison model:

- **Matrix multiplication.** Each algorithm must write the $n^2$ entries of the product, so $\Omega(n^2)$ is a lower bound in every model. The best upper bound is near $n^{2.371}$. See the [quadratic lower bound](/matrix-multiplication-quadratic-lower-bound/).
- **Parity of $n$ bits.** A Boolean [decision tree](/decision-tree-model/) must read all $n$ bits: if one bit is unread, flipping it changes the answer and not the path.
- **Element distinctness for real numbers.** Ben-Or proved $\Omega(n \log n)$ for [algebraic computation trees](/algebraic-computation-tree/). See the [element distinctness lower bound](/element-distinctness-lower-bound/).

A non-example: "binary search makes at least one comparison" is a true lower bound, but it is far from the truth. A lower bound is useful when it is close to an upper bound.

### Pitfalls

- **Swapping the quantifiers.** "For each input, every algorithm is slow" is false and is not what a lower bound says. A lower bound says: for each algorithm, some input is slow. A sort that first checks whether the input is sorted takes $n - 1$ comparisons on sorted inputs.
- **Generalizing beyond the model.** "Sorting needs $\Omega(n \log n)$ time" is false for integers on the word RAM. Say "comparisons" and "in the comparison model".
- **Mixing up the algorithm and the problem.** A slow analysis of one algorithm is not a lower bound for the problem.
- **A reading bound without a reason.** The trivial bound for a problem with a sorted input, such as search, is not $n$: the algorithm need not read every item. A reading bound needs a proof that each item matters.

## Where it is used

- **Stopping the search for better algorithms.** A matching lower bound shows that an algorithm is [optimal](/optimality/) in its model. Merge sort and [heapsort](/heapsort/) are optimal up to a constant factor among comparison sorts.
- **Choosing a model.** A lower bound shows which steps to add to go faster. The bound for comparison sorting is the reason to use [counting sort](/counting-sort/) or [radix sort](/radix-sort/) on small integers, and [hash tables](/hash-table/) instead of balanced search trees for membership.
- **Transferring hardness.** Through reductions, one lower bound gives many: element distinctness gives $\Omega(n \log n)$ for the [closest pair](/closest-pair-lower-bound/) and the [convex hull](/convex-hull-lower-bound/) in algebraic models.
- **Data structures.** Lower bounds in the [cell-probe model](/cell-probe-model/) show limits for [predecessor search](/predecessor-lower-bound/), [union-find](/union-find-lower-bound/) and [partial sums](/dynamic-partial-sums-lower-bound/).

## References
