---
tag: HPJEPD
kind: technique
slug: decision-tree-method
name: Decision tree lower bound method
aliases:
- comparison tree lower bound
- decision tree argument
area: foundations/lower-bounds
level: intro
summary: Bounds the worst-case cost of comparison algorithms by the depth of any decision tree that solves the problem.
prereqs: [decision-tree-model, comparison-model, information-theoretic-bound]
see_also: [information-theoretic-bound, adversary-argument, counting-argument, comparison-sort-lower-bound, merging-lower-bound, sorted-search-lower-bound, element-distinctness, yao-minimax-principle]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1, Lower bounds for sorting (the decision-tree model, Theorem 8.1 and Corollary 8.2)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (comparison trees and the bound for sorting) and Section 5.3.2 (minimum-comparison merging, the bound 2n - 1 for equal lists)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 12, Decision trees (certificate complexity and randomized decision trees)
  - paper: doi:10.1109/SFCS.1977.24
    title: Andrew Chi-Chih Yao, Probabilistic computations, toward a unified measure of complexity, 18th IEEE Symposium on Foundations of Computer Science (FOCS 1977)
    locator: pp. 222 to 227 (the minimax principle for randomized algorithms)
---

The decision tree method proves a lower bound for every algorithm of a query model at once. It turns each algorithm, for a fixed input size, into a [decision tree](/decision-tree-model/), proves that every tree that solves the problem must have some property, and derives from that property a bound on the depth. The property is most often "many leaves", which gives the [information-theoretic bound](/information-theoretic-bound/), or "each path must contain certain queries", which gives bounds that leaf counting misses. It is the standard method for [comparison](/comparison-model/) lower bounds such as $\lceil \lg(n!) \rceil$ for sorting and $2n - 1$ for merging.

## In plain words

A program that only compares items can be drawn as a tree. The first comparison is at the top. Each answer leads down to the next comparison, and the end of each route gives the result. The number of comparisons on a route is the cost on the inputs that follow it, and the worst case is the longest route.

So to show that every such program is slow, it is enough to show that every tree that solves the problem has a long route. There are two common ways. One: the tree needs many ends, because many inputs need different results, and a short tree has few ends. Two: on one chosen input, the route must make many particular comparisons, because if it skipped one of them, a slightly changed input would follow the same route and get a wrong result.

## When it applies

- The algorithms learn about the input only through queries of one kind: comparisons of two items, reads of one bit, signs of linear functions. Other work is free.
- The algorithm is deterministic. For a randomized algorithm, use the method with a distribution on inputs and the [Yao minimax principle](/yao-minimax-principle/).
- The bound is for a fixed input size $n$. The model is non-uniform: the bound holds for each tree, and so for each algorithm.

## The template

**Step 1, unfold.** Fix $n$. Let $A$ be a deterministic algorithm of the model that stops on each input of size $n$. Its next query depends only on the answers so far, since that is all it knows about the input. Build a tree: the root is the first query of $A$, and the child of a node along answer $a$ is the query that $A$ makes next after that sequence of answers, or a leaf with the output of $A$ if it stops. Keep only the answer sequences that some input produces. In the comparison model the inputs of size $n$ fall into finitely many order types, and each run is finite, so the tree is finite. The run of $A$ on input $x$ makes exactly the queries on the path of $x$, so

$$\text{worst-case number of queries of } A = \text{height of the tree}.$$

**Step 2, find a property of all correct trees.** Choose one of these forms.

- **(Leaves.)** A set $S$ of inputs must end at pairwise different leaves. Then the tree has at least $|S|$ leaves, and with $k$ answers per query, height $\ge \lceil \log_k |S| \rceil$.
- **(Path.)** On one input $x$, the path must contain each query of a set $Q_x$. Then height $\ge |Q_x|$. The usual proof: if the path of $x$ skips a query $q$ of $Q_x$, build an input $x'$ that answers every query of the path in the same way as $x$, but has a different correct output. Both reach the same leaf, and the tree is wrong on one of them.
- **(Average.)** A set $S$ of $L$ inputs must end at different leaves. Then the sum of their depths is at least $L \lg L$ in a binary tree, and the average depth is at least $\lg L$ (Lemma 4 of the [decision tree model](/decision-tree-model/)).

**Step 3, combine.** Often both forms work together: a path argument shows that the leaves must be different, and then counting gives the bound. Element distinctness below is the example.

**Step 4, randomness.** A zero-error randomized algorithm is a distribution over trees. If every tree has average depth at least $D$ under a distribution $\mu$ on inputs, then the randomized algorithm has expected cost at least $D$ on some input.

## Classic examples

**1. Sorting (leaves).** The $n!$ orders of distinct items need different outputs, and comparisons of distinct items have 2 answers. So height $\ge \lceil \lg(n!) \rceil$. See the [comparison sort lower bound](/comparison-sort-lower-bound/).

**2. Maximum (path, on every input).** On each input of distinct items, every item other than the maximum must have lost a comparison on the path. If an item $y$ other than the output never lost, raise $y$ above all other items: each comparison on the path that involves $y$ was won by $y$ and still is, the others do not change, so the run ends at the same leaf with a wrong output. Each comparison makes at most one item lose for the first time. So each path has length at least $n - 1$. See the [maximum finding lower bound](/max-finding-lower-bound/).

**3. Merging (path).** Merge $a_1 < \dots < a_n$ with $b_1 < \dots < b_n$. Take the input with $a_1 < b_1 < a_2 < b_2 < \dots < a_n < b_n$. Its path must compare each of the $2n - 1$ adjacent pairs $(a_i, b_i)$ and $(b_i, a_{i+1})$. If it skips one pair, swap the two values of that pair. Both lists stay sorted, because no other item lies between the two values. Each comparison on the path that does not compare the pair gets the same answer. So the run ends at the same leaf, but the merged order has changed. Hence $2n - 1$ comparisons are necessary, and the usual merge makes $2n - 1$. Leaf counting gives only $\lceil \lg \binom{2n}{n} \rceil$, which is 8 instead of 9 for $n = 5$. See the [merging lower bound](/merging-lower-bound/).

**4. Element distinctness (path, then leaves).** For an input of distinct items, the path must compare each pair of items that are adjacent in sorted order: else set one of them equal to the other, and the run reaches the same leaf "distinct" on an input with a repeated item. Those comparisons fix the full order, so inputs with different orders reach different leaves, and the height is at least $\lceil \lg(n!) \rceil$, although the problem has only two outputs. See [element distinctness](/element-distinctness/).

**5. Search in a sorted array (path, then leaves).** For a key $x$ that falls in a gap between $A[g]$ and $A[g+1]$, the path must compare $x$ with both neighbours, so the $n + 1$ gaps reach different leaves along "less" and "greater" answers only. Height $\ge \lceil \lg(n+1) \rceil$. See the [sorted search lower bound](/sorted-search-lower-bound/).

**6. Average case of sorting (average).** On a uniformly random order of $n$ distinct items, every comparison sort makes at least $\lg(n!)$ comparisons on average. For $n = 10$ this is $21.79$.

**7. Boolean functions (path).** In a tree that reads bits, the bits read on the path of $x$ fix $f$ on every input that agrees with $x$ on them. So the height is at least the [certificate complexity](/certificate-complexity/) $C(f)$, and at least the [sensitivity](/sensitivity/) $s(f)$. For parity of $n$ bits this gives $n$.

The values of the comparison examples, for small sizes:

| problem | size | bound from leaves alone | bound with paths | true value |
|---|---|---|---|---|
| maximum | $n = 8$ | 3 | 7 | 7 |
| merging | $n = 5$ and $5$ | 8 | 9 | 9 |
| element distinctness | $n = 8$ | 1 | 16 | 16 |
| sorted search | $n = 8$ | 3 (three answers, 17 outputs) | 4 | 4 |
| sorting | $n = 8$ | 16 | 16 | 16 |

## Variations

- **Linear and algebraic decision trees.** Queries are signs of linear functions or of polynomials of bounded degree. Leaf counting is replaced by counting the connected components of the set of inputs with each answer. See [linear decision trees](/linear-decision-tree/), [algebraic decision trees](/algebraic-decision-tree/) and the [Ben-Or theorem](/ben-or-theorem/).
- **Adversary form.** Instead of a tree, describe a strategy that answers queries one by one. It is the same argument read along one path. See the [adversary argument](/adversary-argument/).
- **Randomized trees.** Combine the average form with the [Yao minimax principle](/yao-minimax-principle/).
- **Query complexity of Boolean functions.** Sensitivity, block sensitivity, certificate complexity and degree all bound the height of a tree. See [query complexity](/query-complexity/).

### Pitfalls

- **Forgetting the model.** The tree has only the queries of the model. An algorithm that compares $x_i + x_j$ with $x_k$, or uses an item as an array index, is not a comparison tree, and the bound may fail for it.
- **A randomized algorithm is not one tree.** The bound for a deterministic tree does not hold for each tree of a randomized algorithm on the same input. Use the average form and Yao's principle.
- **Counting leaves that are not needed.** Leaves are needed only for different correct outputs, or for inputs that a path argument separates. A tree can have many more leaves than outputs.
- **The changed input must be legal.** In a path argument, the input $x'$ must satisfy the promise of the problem: for merging both lists must stay sorted, for sorted search the array must stay sorted. Check it each time.
- **One tree per size.** The method gives a bound for each $n$. It says nothing about how hard it is to build the trees, so an upper bound in the model is not an algorithm.

## Exercises

1. Write out the comparison tree of insertion sort for $n = 3$ and find its height and its average depth over the 6 orders.
2. Prove that each comparison algorithm that finds the minimum of $n$ distinct items makes at least $n - 1$ comparisons on every input, not only on the worst one.
3. Prove that each comparison algorithm that decides whether a given item $x_1$ is the median of $n$ distinct items, $n$ odd, makes at least $n - 1$ comparisons.
4. Merging a list of 1 item into a sorted list of $n$ items needs $\lceil \lg(n+1) \rceil$ comparisons. Prove it with a leaf argument.
5. Use a path argument to prove that each comparison algorithm that checks whether an array is sorted makes at least $n - 1$ comparisons.
6. Show that the average depth bound $\lg(n!)$ for sorting also bounds the expected cost of randomized quicksort on its worst input.

## References
