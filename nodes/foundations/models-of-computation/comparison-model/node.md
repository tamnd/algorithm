---
tag: 9CMPMD
kind: model
slug: comparison-model
name: Comparison model
aliases: [decision tree model, comparison-based model]
area: foundations/models-of-computation
level: intro
summary: A model where an algorithm learns about its input only by comparing two items. The cost is the number of comparisons.
prereqs: [asymptotic-notation, logarithms]
see_also: [decision-tree-model, comparison-sort, comparison-cost-model, information-theoretic-bound, word-ram, random-access-machine, sorting-problem]
sources:
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, STOC 1983"
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Proposition I
---

The comparison model is a model of computation where an algorithm learns about its input only by comparing two items. The cost of an algorithm is the number of comparisons. The model gives lower bounds that hold for each algorithm of the model, such as $\lceil \lg(n!) \rceil$ comparisons for [sorting](/sorting-problem/) $n$ items and $\lceil \lg(n+1) \rceil$ comparisons for [search in a sorted array](/search-in-sorted-array/). For each input size, an algorithm of the model is a [decision tree](/decision-tree-model/). Many bounds come from counting the leaves of the tree, and others come from adversary arguments.

## The machine

The input is a sequence $x_1, \dots, x_n$ of items from a set with a total order. The algorithm cannot read the items. It can ask "is $x_i < x_j$?" with two answers, or a three-way comparison of $x_i$ and $x_j$ with the answers less, equal and greater. The queries can depend on the earlier answers.

The algorithm can do anything else that does not look at the items. It can move, copy and swap items, follow pointers, and compute with indices and counters. It cannot add two keys, use a key as an index, take a hash of a key, or ask for a bit of a key.

An algorithm for inputs of size $n$ is a [decision tree](/decision-tree-model/). Each inner node is a comparison. Each branch is an answer. Each leaf is an output. The run on an input follows one path from the root to a leaf. For sorting, the output is the permutation of the positions that puts the keys in order. In a comparison of distinct keys, the answer "equal" does not occur, and the tree is binary.

## What it counts

The cost is the number of comparisons. The worst-case cost is the height of the tree. The average cost is the expected depth of the leaf that the input reaches, where each leaf is weighted by the probability of the inputs that reach it. Everything else that the algorithm does is free in the model.

The free work can be large. [Binary insertion sort](/insertion-sort/) on an array uses about $n \lg n$ comparisons, but it moves $\Theta(n^2)$ items. For [merge sort](/merge-sort/), the other work is $O(n \log n)$, so the number of comparisons is the right measure of its time. The page on the [comparison cost model](/comparison-cost-model/) gives the way to count comparisons and exchanges together.

## Relation to other models

The [word RAM](/word-ram/) can do arithmetic on the items and use them as addresses. So it can beat the bounds of the comparison model when the keys are integers of bounded size. [Counting sort](/counting-sort/) and [radix sort](/radix-sort/) do this, and so do hash tables, which answer a membership query in $O(1)$ expected time. The comparison model is still the right model for code that must work for any type with an order, such as the library sort of most languages, which takes a comparison function.

The comparison model is the [decision tree model](/decision-tree-model/) with comparisons as the queries. Other decision tree models allow more queries: the [linear decision tree](/linear-decision-tree/) tests the sign of a linear function of the inputs, and the [algebraic decision tree](/algebraic-decision-tree/) tests the sign of a polynomial of bounded degree. These models are for problems on numbers.

A [random access machine](/random-access-machine/) program that touches its keys only in comparisons is an algorithm of the comparison model, and the number of comparisons is at most its [unit-cost](/unit-cost-model/) time.

## Known results in the model

Bounds below are for keys that are distinct, which is the hardest case for the lower bounds that count outcomes. Each bound is for the worst case unless it says otherwise.

- **Sorting** needs at least $\lceil \lg(n!) \rceil = n \lg n - \Theta(n)$ comparisons in the worst case, and at least $\lg(n!)$ on average over the $n!$ orders. This is the proof by counting leaves in the [decision tree model](/decision-tree-model/), with the table of values for small $n$. It follows that [merge sort](/merge-sort/) and [heapsort](/heapsort/) are optimal up to a constant factor, and that merge sort is optimal up to a term of order $n$. The exact value is not always $\lceil \lg(n!) \rceil$: for $n = 12$ the least worst case is 30 (Wells, 1965; see Knuth, Section 5.3.1), while $\lceil \lg(12!) \rceil = 29$. See [the comparison sort lower bound](/comparison-sort-lower-bound/) and [merge sort optimality](/merge-sort-optimality/).
- **Randomized sorting** needs at least $\lg(n!)$ comparisons in expectation on some input. A randomized algorithm is a distribution over decision trees. Each tree has average depth at least $\lg(n!)$ over the $n!$ orders, so by the [Yao minimax principle](/yao-minimax-principle/) some input has expected cost at least $\lg(n!)$.
- **Search in a sorted array** needs $\lceil \lg(n+1) \rceil$ three-way comparisons. [Binary search](/binary-search/) meets this bound. See the [sorted search lower bound](/sorted-search-lower-bound/).
- **The maximum** of $n$ items needs $n - 1$ comparisons. Each comparison has one loser, and each item except the maximum must lose at least one comparison, or the algorithm could not rule it out as the maximum. See the [maximum finding lower bound](/max-finding-lower-bound/).
- **The maximum and the minimum** together need $\lceil 3n/2 \rceil - 2$ comparisons. See the [max-min lower bound](/max-min-lower-bound/).
- **Merging** two sorted lists of $n$ items each needs $2n - 1$ comparisons in the worst case. See the [merging lower bound](/merging-lower-bound/).
- **Element distinctness** (are all $n$ keys different?) needs $\Omega(n \log n)$ comparisons, although the answer is only yes or no, so leaf counting alone does not give it. Ben-Or (1983) extends the bound to algebraic decision trees. See the [element distinctness lower bound](/element-distinctness-lower-bound/).
- **Selection** of the median is not a case where the counting bound is the answer. The best lower bound is linear in $n$, and an algorithm with $O(n)$ comparisons exists: [median of medians](/median-of-medians/). So selection is cheaper than sorting in this model. See the [selection problem](/selection-problem/).

## References
