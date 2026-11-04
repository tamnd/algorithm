---
tag: 9CMPMD
kind: model
slug: comparison-model
name: Comparison model
aliases: [comparison-based model, comparison-based computation]
area: foundations/models-of-computation
level: intro
summary: A model where an algorithm learns about its input only by comparing two items. The cost is the number of comparisons.
prereqs: [asymptotic-notation, logarithms]
see_also: [decision-tree-model, comparison-sort, comparison-cost-model, information-theoretic-bound, adversary-argument, word-ram, sorting-problem, ford-johnson-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1 (Theorem 8.1, the lower bound for comparison sorts), Section 9.1 (minimum and maximum) and Section 9.3 (selection in worst-case linear time)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (minimum-comparison sorting and merge insertion), Section 5.3.2 (minimum-comparison merging) and Section 5.3.3 (minimum-comparison selection)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Proposition I (no compare-based algorithm sorts with fewer than lg(N!) compares)
  - paper: doi:10.1080/00029890.1959.11989306
    title: Lester R. Ford Jr. and Selmer M. Johnson, A tournament problem, American Mathematical Monthly 66(5) (1959)
    locator: pp. 387 to 389
  - paper: doi:10.1145/361405.361423
    title: Ira Pohl, A sorting problem and its complexity, Communications of the ACM 15(6) (1972)
    locator: pp. 462 to 464 (the bound for the maximum and the minimum)
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973)
    locator: pp. 448 to 461
  - paper: doi:10.1137/S0895480199353895
    title: Dorit Dor and Uri Zwick, Median selection requires (2+epsilon)n comparisons, SIAM Journal on Discrete Mathematics 14(3) (2001)
    locator: pp. 312 to 325
  - paper: "Dorit Dor and Uri Zwick, Selecting the median, SIAM Journal on Computing 28(5) (1999)"
    locator: pp. 1722 to 1758 (the algorithm with at most 2.95n comparisons)
  - paper: "Marcin Peczarski, New results in minimum-comparison sorting, Algorithmica 40 (2004)"
    locator: pp. 133 to 145 (the values for 13, 14 and 22 elements)
  - paper: doi:10.1016/j.ipl.2006.09.001
    title: Marcin Peczarski, The Ford-Johnson algorithm still unbeaten for less than 47 elements, Information Processing Letters 101(3) (2007)
    locator: pp. 126 to 128
  - paper: "Florian Stober and Armin Weiss, Lower bounds for sorting 16, 17, and 18 elements, arXiv:2206.05597 (2022)"
    locator: abstract and the table of known values
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983)"
    locator: the main theorem (the bound from the number of connected components) and its application to element distinctness
---

The comparison model is a model of computation in which an algorithm learns about its input only by comparing two items. The cost of an algorithm is the number of comparisons that it makes. For each input size, an algorithm of the model is a [decision tree](/decision-tree-model/), so lower bounds come from counting the leaves of the tree or from an [adversary argument](/adversary-argument/). Examples are $\lceil \lg(n!) \rceil$ comparisons to [sort](/sorting-problem/) $n$ items, $n - 1$ to find the maximum, and $\lceil \lg(n+1) \rceil$ to [search in a sorted array](/search-in-sorted-array/).

## The machine

The input is a sequence $x_1, \dots, x_n$ of items from a set with a total order $\le$. The algorithm knows $n$ but cannot read the items. It can ask one kind of question about them:

- a two-way comparison "is $x_i < x_j$?", with the answers yes and no, or
- a three-way comparison of $x_i$ and $x_j$, with the answers less, equal and greater.

The choice of the next question can depend on all earlier answers. The algorithm can do any other work that does not look at the items. It can move, copy and swap items, follow pointers, and compute with indices and counters. It cannot add two items, use an item as an index, take a hash of an item, or read one bit of an item. The output is a function of the answers only: a permutation, an index, a yes or no, or a set of indices.

Fix $n$. The run of the algorithm on all inputs of size $n$ forms a tree. Each inner node is a comparison, each edge is an answer, and each leaf is an output. The run on one input follows one path from the root to a leaf. This is the [decision tree model](/decision-tree-model/) with comparisons as the queries. A randomized algorithm is a probability distribution over such trees.

Two inputs with the same relative order give the same answer to every comparison, so they reach the same leaf. So the model sees only the order type of the input. For sorting $n$ distinct items, an input is in effect one of the $n!$ permutations of $\{1, \dots, n\}$.

## What it counts

The cost of a run is the number of comparisons on its path. The worst-case cost of an algorithm is the height of its tree. The average cost, under a probability distribution on inputs, is the expected depth of the leaf that the input reaches. For sorting, the usual distribution makes each of the $n!$ orders equally likely. The expected cost of a randomized algorithm on an input is its average over the random choices, and its cost is the largest expected cost over all inputs.

All other work is free. This free work can be large:

- [Binary insertion sort](/insertion-sort/) uses $\sum_{k=1}^{n} \lceil \lg k \rceil$ comparisons in the worst case, which is $n \lg n + O(n)$, but it moves $\Theta(n^2)$ items in the worst case on an array.
- [Merge sort](/merge-sort/) and [heapsort](/heapsort/) do $O(n \log n)$ other work, so for them the number of comparisons is the right measure of time up to a constant factor.

The [comparison cost model](/comparison-cost-model/) counts comparisons and exchanges together.

The lower bounds of the model count comparisons only. So they are valid for every algorithm that touches the items only in comparisons, whatever other work it does. They are not bounds on the running time of an algorithm that uses other operations on the items.

## Relation to other models

The comparison model is the [decision tree model](/decision-tree-model/) in which each query compares two input items. Other decision tree models allow more general queries on numbers. A [linear decision tree](/linear-decision-tree/) tests the sign of a linear function of the inputs, an [algebraic decision tree](/algebraic-decision-tree/) tests the sign of a polynomial of bounded degree, and an [algebraic computation tree](/algebraic-computation-tree/) also does arithmetic between tests. A comparison $x_i < x_j$ is the linear test $x_i - x_j < 0$, so each lower bound in these models also holds in the comparison model.

A [random access machine](/random-access-machine/) program that touches its keys only in comparisons is an algorithm of the comparison model. Its number of comparisons is at most its [unit-cost](/unit-cost-model/) running time.

The [word RAM](/word-ram/) can do arithmetic on the items and use them as addresses. So it is not bound by the comparison model when the items are integers that fit in a word. [Radix sort](/radix-sort/) with [counting sort](/counting-sort/) as its inner step sorts $n$ integers in the range $0$ to $n^c - 1$ in $O(cn)$ time, the [fusion tree](/fusion-tree/) supports search in $o(\log n)$ time, and a [hash table](/hash-table/) answers a membership query in $O(1)$ expected time. See [integer sorting](/integer-sorting/). The comparison model is still the right model for code that must work for any type with an order, such as a library sort that takes a comparison function.

## Known results in the model

Here the items are distinct unless the statement says otherwise. Distinct items are the hard case for the bounds below, so the bounds hold for general inputs too. All bounds are for the worst case unless the statement says otherwise. Here $\lg = \log_2$.

### Sorting

**The lower bound.** Each comparison sort of $n$ items makes at least $\lceil \lg(n!) \rceil$ comparisons on some input. The proof: the tree must have a different leaf for each of the $n!$ orders, because two orders need different outputs, and a binary tree of height $h$ has at most $2^h$ leaves. With three-way comparisons the answer "equal" never occurs on distinct items, so the same bound holds. The average over the $n!$ orders is at least $\lg(n!)$, and so is the expected cost of a randomized sort on its worst input. Stirling's formula gives $\lg(n!) = n \lg n - n \lg e + O(\log n)$ with $\lg e \approx 1.443$. The proofs are on the [decision tree model](/decision-tree-model/) page and the [comparison sort lower bound](/comparison-sort-lower-bound/) page (CLRS Theorem 8.1; Sedgewick and Wayne, Proposition I).

**Upper bounds.** [Merge sort](/merge-sort/) makes at most $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ comparisons, which is $n \lg n + O(n)$. Binary insertion sort makes the same number in the worst case. The merge insertion algorithm of [Ford and Johnson](/ford-johnson-algorithm/) (1959) makes $\sum_{k=1}^{n} \lceil \lg(3k/4) \rceil$ comparisons in the worst case, which is $n \lg n - c_n n + O(\log n)$ with $c_n$ between about $1.329$ and $1.415$, depending on $n$ (Knuth, Section 5.3.1). So merge sort and merge insertion are within $O(n)$ comparisons of the lower bound. See [merge sort optimality](/merge-sort-optimality/).

**Exact values.** Let $S(n)$ be the least worst-case number of comparisons of any sort of $n$ items. The table compares it with the lower bound and with the three algorithms above.

| $n$ | $\lceil \lg(n!) \rceil$ | merge sort | binary insertion | merge insertion | $S(n)$ |
|---|---|---|---|---|---|
| 4 | 5 | 5 | 5 | 5 | 5 |
| 5 | 7 | 8 | 8 | 7 | 7 |
| 8 | 16 | 17 | 17 | 16 | 16 |
| 10 | 22 | 25 | 25 | 22 | 22 |
| 11 | 26 | 29 | 29 | 26 | 26 |
| 12 | 29 | 33 | 33 | 30 | 30 |
| 13 | 33 | 37 | 37 | 34 | 34 |
| 16 | 45 | 49 | 49 | 46 | 46 |
| 22 | 70 | 79 | 79 | 71 | 71 |

The lower bound is exact for $n \le 11$. For $n = 12$ it is not: Wells (1965) showed by a computer search that $S(12) = 30$, while $\lceil \lg(12!) \rceil = 29$ (Knuth, Section 5.3.1). Peczarski (2004) proved $S(13) = 34$, $S(14) = 38$ and $S(22) = 71$, and Stober and Weiss (2022) proved $S(16) = 46$, $S(17) = 50$ and $S(18) = 54$. In each of these cases merge insertion is optimal. Merge insertion is not optimal for every $n$. Manacher (1979, see Peczarski 2007) showed that sorting two parts by merge insertion and then merging them beats it for some large $n$, and later work showed that it is not optimal for $n = 47$. Peczarski (2007) showed by computer search that no method of this split and merge form beats it for $n < 47$.

### Search, maximum, merging and selection

- **Search in a sorted array.** Let $A[1] < \dots < A[n]$ be sorted, and let a query compare $x$ with one entry by a three-way comparison. Each algorithm that finds $x$ or reports that it is absent makes at least $\lceil \lg(n+1) \rceil$ comparisons, and [binary search](/binary-search/) makes $\lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$. See the [sorted search lower bound](/sorted-search-lower-bound/).
- **Maximum.** Finding the maximum takes exactly $n - 1$ comparisons. A linear scan makes $n - 1$. For the lower bound, call an item a loser when it was the smaller item in some comparison. Each comparison makes at most one new loser. If two items are not losers at the end, the algorithm cannot tell which of them is the maximum: raise the one that it does not output above all other items, and every answer stays the same. So $n - 1$ items must be losers. See the [maximum finding lower bound](/max-finding-lower-bound/) and [tournament method](/tournament-method/).
- **Maximum and minimum.** Finding both takes exactly $\lceil 3n/2 \rceil - 2$ comparisons for $n \ge 1$ (Pohl, 1972). The algorithm compares the items in pairs and then finds the maximum of the larger items and the minimum of the smaller items. For $n = 8$ it makes 10 comparisons, against 13 for two separate scans. See the [max-min lower bound](/max-min-lower-bound/) and CLRS Section 9.1.
- **Second largest.** Finding the largest and the second largest takes exactly $n + \lceil \lg n \rceil - 2$ comparisons for $n \ge 2$ (Kislitsyn, 1964; Knuth, Section 5.3.3). A knockout tournament finds the maximum with $n - 1$ comparisons, and the second largest lost directly to the maximum, which met at most $\lceil \lg n \rceil$ items. For $n = 8$ the value is 9. See the [second largest lower bound](/second-largest-lower-bound/).
- **Merging.** Merging two sorted lists of $n$ items each takes exactly $2n - 1$ comparisons (Knuth, Section 5.3.2). The usual merge makes at most $2n - 1$. For the lower bound, an adversary sets the order $a_1 < b_1 < a_2 < b_2 < \dots < a_n < b_n$. Each of the $2n - 1$ adjacent pairs must be compared, because if a pair is not compared, swapping the two items gives an input with the same answers and a different output. See the [merging lower bound](/merging-lower-bound/).
- **Selection.** Finding the item of rank $k$ takes $O(n)$ comparisons for every $k$ (Blum, Floyd, Pratt, Rivest and Tarjan, 1973; see [median of medians](/median-of-medians/) and [deterministic linear selection](/deterministic-linear-selection/)). So selection is cheaper than sorting, and leaf counting gives only a weak bound for it. For the median, the best known algorithm makes at most $2.95n + o(n)$ comparisons (Dor and Zwick, 1999), and every algorithm makes at least $(2 + \varepsilon) n$ comparisons for a fixed $\varepsilon > 0$ and large $n$ (Dor and Zwick, 2001, with $\varepsilon$ about $2^{-80}$). The exact constant is open. See the [selection lower bound](/selection-lower-bound/) and the [selection problem](/selection-problem/).

### Element distinctness

The problem asks if all $n$ items are different. The answer is one bit, so leaf counting gives only one comparison. A different argument gives the bound for sorting.

**Claim.** Each comparison algorithm for element distinctness makes at least $\lceil \lg(n!) \rceil$ comparisons on some input.

*Proof.* Take an input of distinct items, and let $P$ be its path. Let $x_a < x_b$ be two items that are adjacent in the sorted order. Suppose that $P$ does not compare $x_a$ with $x_b$. Change $x_b$ to the value of $x_a$. For each other item $x_c$, no item lies strictly between $x_a$ and $x_b$, so $x_c < x_b$ exactly when $x_c < x_a$, and $x_c > x_b$ exactly when $x_c > x_a$. So each comparison on $P$ has the same answer for the new input, which reaches the same leaf. That leaf says "distinct", but the new input has two equal items. This is a contradiction. So $P$ compares each of the $n - 1$ adjacent pairs, and its answers fix the full order of the input. Two inputs with different orders therefore reach different leaves. Every comparison on these paths has the answer less or greater, so these $n!$ leaves lie in a binary tree, and its height is at least $\lceil \lg(n!) \rceil$. $\square$

Sorting and then checking neighbours meets this bound up to $O(n)$. The bound $\Omega(n \log n)$ also holds in stronger models: for algebraic computation trees by Ben-Or (1983), who counts the connected components of the set of inputs with answer "yes". See the [element distinctness lower bound](/element-distinctness-lower-bound/).

### Pitfalls

- **A lower bound in this model is not a bound on all algorithms.** Integers in a small range sort in linear time on a [word RAM](/word-ram/). The claim "sorting needs $\Omega(n \log n)$ time" is true only for algorithms that use comparisons alone.
- **The counting bound is not always exact.** $\lceil \lg(n!) \rceil$ is a lower bound, but $S(12) = 30 > 29$. Do not state $\lceil \lg(n!) \rceil$ as the exact cost of sorting.
- **Comparisons are not time.** A bound on comparisons says nothing about moves or memory. Binary insertion sort has a near optimal comparison count and $\Theta(n^2)$ moves.
- **Few outputs do not mean an easy problem.** Leaf counting gives one comparison for element distinctness, and the true bound is $\lceil \lg(n!) \rceil$. A weak counting bound is not evidence of a fast algorithm.
- **Equal items change the count.** With many equal keys, a three-way comparison can sort faster than $\lg(n!)$: if all keys are equal, $n - 1$ comparisons are enough. The bound for distinct keys is the worst case, not the cost on every input.
- **A comparison must be a consistent total order.** An inconsistent comparison function (for example, one that uses `<=` on floating-point values with NaN) can make a sort fail or loop, and the bounds of the model then do not apply.

## References
