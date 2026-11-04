---
tag: N20YMP
kind: definition
slug: upper-bound
name: Upper bound
area: foundations/lower-bounds
level: intro
summary: A guarantee on the worst case cost of some algorithm for a problem, showing the problem can be solved within that cost.
prereqs: [asymptotic-notation, worst-case-analysis]
see_also: [lower-bound, optimality, asymptotic-optimality, trivial-lower-bound, comparison-model, merge-sort, find-maximum, merge-sort-optimality]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 3.1 and Section 3.2 (O-notation as an asymptotic upper bound), Section 2.3 (the analysis of merge sort) and Section 9.1 (minimum and maximum)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 2.2, Asymptotic Order of Growth (asymptotic upper bounds, lower bounds and tight bounds)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1, Minimum-comparison sorting (the upper bounds of binary insertion and merge insertion against the function S(n))
---

An upper bound for a problem is a cost that some algorithm never exceeds: it shows that the problem can be solved within that cost, in a named [model of computation](/comparison-model/) and in a named case, usually the [worst case](/worst-case-analysis/). An upper bound comes from one algorithm and a proof of its cost. It is one half of the complexity of a problem. The other half is a [lower bound](/lower-bound/), which holds for every algorithm, and the problem is closed when the two meet ([optimality](/optimality/)).

## Definition

Fix a problem $P$, a model of computation $M$, a cost measure (time, comparisons, probes, memory) and the inputs of each size $n$. For an algorithm $A$ of $M$ that solves $P$, its **worst-case cost** is

$$W_A(n) = \max \{\, \mathrm{cost}_A(x) : x \text{ an input of size } n \,\}.$$

**Upper bound of an algorithm.** A function $U : \mathbb{N} \to \mathbb{R}_{\ge 0}$ is an upper bound on the worst-case cost of $A$ when $W_A(n) \le U(n)$ for each $n \ge n_0$, for some $n_0$. In [asymptotic notation](/asymptotic-notation/) the weaker claim is $W_A(n) = O(U(n))$: there are constants $c > 0$ and $n_0$ with $W_A(n) \le c\,U(n)$ for each $n \ge n_0$.

**Upper bound of a problem.** A function $U$ is an upper bound for $P$ in $M$ when there **exists** an algorithm $A$ of $M$ that solves $P$ with $W_A(n) \le U(n)$ for each $n \ge n_0$ (exact form), or with $W_A(n) = O(U(n))$ (asymptotic form). Let $C_P(n) = \min_A W_A(n)$ be the least worst-case cost of any algorithm of $M$ for $P$. Then $U$ is an exact upper bound for $P$ exactly when $C_P(n) \le U(n)$ for each $n \ge n_0$.

The quantifier is the whole point. An upper bound needs **one** algorithm and **all** inputs of each size. A lower bound needs **all** algorithms and, for each algorithm, **one** bad input of each size.

**Other cases.** The same definition with another cost function gives other kinds of upper bound:

- average case: replace $W_A(n)$ by the mean of $\mathrm{cost}_A(x)$ over a stated distribution on the inputs of size $n$ (see [average-case analysis](/average-case-analysis/));
- expected: for a randomized algorithm, replace $\mathrm{cost}_A(x)$ by its expectation over the random choices, and keep the maximum over $x$;
- amortized: bound the total cost of each sequence of $m$ operations by $m\,U(n)$.

A bound of one case is not a bound of another case. Each claim must name its case.

## Examples and non-examples

**Examples.**

- **The maximum.** A scan that keeps the largest item seen so far makes exactly $n - 1$ comparisons on each input of $n$ items. So $U(n) = n - 1$ is an exact upper bound for [finding the maximum](/find-maximum/) in the [comparison model](/comparison-model/). It is also a lower bound ([maximum finding lower bound](/max-finding-lower-bound/)), so the bound is exact.
- **Sorting.** [Merge sort](/merge-sort/) makes at most $n\lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ comparisons. So this function is an exact upper bound for the [sorting problem](/sorting-problem/) in the comparison model, and so is the simpler $n \lg n$, since $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1 \le n \lg n$ for $n \ge 1$. The table gives the bound of merge sort and the least possible worst case $C(n)$ from Knuth, Section 5.3.1.

| $n$ | merge sort bound | $\lfloor n \lg n \rfloor$ | least worst case $C(n)$ |
|---|---|---|---|
| 4 | 5 | 8 | 5 |
| 5 | 8 | 11 | 7 |
| 8 | 17 | 24 | 16 |
| 10 | 25 | 33 | 22 |
| 12 | 33 | 43 | 30 |

Each column is an upper bound for sorting in this model. The last column is the best one, and for $n = 5$ merge sort does not reach it. The algorithm of [Ford and Johnson](/ford-johnson-algorithm/) gives the better upper bound $7$.

- **A loose bound is still a bound.** $O(n^2)$ is an upper bound for sorting, because [insertion sort](/insertion-sort/) makes at most $n(n-1)/2$ comparisons. It is true but weaker than $O(n \log n)$. "Upper bound" says nothing about how close the bound is to the truth.
- **Search in a sorted array.** [Binary search](/binary-search/) makes at most $\lfloor \lg n \rfloor + 1$ three-way comparisons. For $n = 1000$ this is 10.
- **Matrix multiplication.** [Strassen's algorithm](/strassen-algorithm/) multiplies two $n \times n$ matrices with $O(n^{\lg 7})$ arithmetic operations, and $\lg 7 \approx 2.807$. So $O(n^{2.808})$ is an upper bound for the problem in the arithmetic model.

**Non-examples.**

- **A bound on one input.** "Merge sort sorted this array of $10^6$ items with $1.8 \times 10^7$ comparisons" is a measurement on one input. It bounds nothing for other inputs.
- **An average stated as a worst case.** [Quicksort](/quicksort/) with the first item as pivot makes about $1.39\,n \lg n$ comparisons on average over random orders, but $n(n-1)/2$ on a sorted input. So $O(n \log n)$ is an average-case upper bound for this algorithm, and it is not a worst-case upper bound.
- **A bound in another model.** [Radix sort](/radix-sort/) sorts $n$ integers in the range $0$ to $n^2 - 1$ in $O(n)$ time on the [word RAM](/word-ram/). This is an upper bound for integer sorting on the word RAM. It is not an upper bound for sorting in the comparison model, because radix sort is not an algorithm of that model.
- **A lower bound of an algorithm.** "Bubble sort takes at least $n - 1$ comparisons" bounds the algorithm from below. It is not an upper bound of anything.
- **An algorithm without a proof.** A program that seems fast on tests does not give an upper bound until its cost is proved for every input of each size.

**Pitfalls.**

- **"$O$" is not "worst case".** $O$ is a statement about a function. The function can be the worst case, the average or the best case. Write "the worst-case time is $O(n^2)$", not only "the time is $O(n^2)$".
- **An upper bound on an algorithm is not a bound on its problem in reverse.** "Insertion sort is $O(n^2)$" does not mean that sorting needs $n^2$ steps. It only shows that $n^2$ steps are enough.
- **Fixed sizes.** An exact upper bound for each $n \ge n_0$ says nothing for $n < n_0$. When a page gives a table for small $n$, the values are exact, not asymptotic.

## Related definitions

- [Lower bound](/lower-bound/): a cost that every algorithm of the model reaches on some input. A lower bound and an upper bound of the same order give a $\Theta$ bound for the problem.
- [Optimality](/optimality/) and [asymptotic optimality](/asymptotic-optimality/): an algorithm whose upper bound meets a lower bound, exactly, up to lower-order terms, or up to a constant factor.
- [Asymptotic notation](/asymptotic-notation/): $O$ states an upper bound on a function, $\Omega$ a lower bound and $\Theta$ both. Kleinberg and Tardos, Section 2.2, call these the asymptotic upper, lower and tight bounds.
- [Worst-case analysis](/worst-case-analysis/): the usual cost function of an upper bound.
- [Trivial lower bound](/trivial-lower-bound/): the lower bound from the size of the input and the output, often the first one to compare an upper bound with.

## References
