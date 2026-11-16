---
tag: 76M15A
kind: concept
slug: set-cover-conjecture
name: Set cover conjecture
aliases:
- set cover hypothesis
area: complexity/fine-grained-complexity
level: research
summary: "For every e > 0 there is a k such that Set Cover with sets of size at most k on n elements has no O*(2^((1-e)n)) algorithm. It is open whether SETH implies it."
prereqs: [set-cover, strong-exponential-time-hypothesis]
see_also: [set-cover, hitting-set, steiner-tree-problem, parameterized-steiner-tree, subset-sum-problem, inclusion-exclusion-principle, bitmask-dp, set-cover-inapproximability]
sources:
  - paper: doi:10.1145/2925416
    title: "Marek Cygan, Holger Dell, Daniel Lokshtanov, Dániel Marx, Jesper Nederlof, Yoshio Okamoto, Ramamohan Paturi, Saket Saurabh and Magnus Wahlström, On problems as hard as CNF-SAT, ACM Transactions on Algorithms 12(3), 2016, article 41 (conference version in CCC 2012)"
    locator: "in the arXiv version 1112.2275v3: Theorem 1.1 (SETH is equivalent to lower bounds for Hitting Set, Set Splitting and NAE-SAT), Theorem 1.2 (consequences of the set cover assumption for Steiner Tree, Connected Vertex Cover, Set Partitioning and Subset Sum) and Theorem 1.3 (parity of the number of set covers)"
  - paper: doi:10.1006/jcss.2000.1727
    title: "Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 2001, 367-375"
    locator: the exponential time hypotheses for k-SAT
  - paper: doi:10.1007/978-3-642-11269-0_6
    title: "Chris Calabro, Russell Impagliazzo and Ramamohan Paturi, The complexity of satisfiability of small depth circuits, Parameterized and Exact Computation (IWPEC 2009), LNCS 5917, 75-85"
    locator: the strong exponential time hypothesis in its usual form
  - paper: doi:10.1006/jcss.2001.1774
    title: "Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 2001, 512-530"
    locator: the sparsification lemma, used to apply SETH for each fixed clause width
  - paper: "Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 2009, 546-563"
    locator: counting covers and partitions of an n-element set by members of a family in time 2^n times a polynomial, by inclusion-exclusion
---

The set cover conjecture says that [Set Cover](/set-cover/) on a universe of $n$ elements cannot be solved much faster than $2^n$, even when every set has a bounded size: for every $\varepsilon > 0$ there is a $k$ such that Set Cover with sets of size at most $k$ has no $O^*(2^{(1-\varepsilon) n})$ algorithm. Cygan, Dell, Lokshtanov, Marx, Nederlof, Okamoto, Paturi, Saurabh and Wahlström stated it in 2012. Under it, the best known exponential algorithms for Steiner Tree, Connected Vertex Cover, Set Partitioning and the pseudo-polynomial algorithm for Subset Sum cannot be improved by a fixed factor in the base. It is open whether the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) implies it.

Here $O^*(\cdot)$ hides factors polynomial in the input size, which includes the number $m$ of sets. The page is about the hypothesis and its consequences; the problem itself, its approximation and its greedy algorithm are on [set cover](/set-cover/).

## In plain words

You have a list of items and a collection of groups of items. You want the fewest groups that together contain every item.

There is a simple method whose time doubles with each extra item: it records, for every set of items, how few groups suffice to cover it. Nobody knows a method whose time grows by a smaller factor than two with each new item, even when every group is small.

The conjecture says that no such method exists. It is like SETH, which says the same for satisfying a logic formula, but nobody has shown that one follows from the other. If you accept it, several other well-known methods are also the best possible in this sense.

## The idea

### Hypothesis

**Set Cover with sets of size at most $k$.** Instance: a universe $U$ of $n$ elements, a family $\mathcal{F}$ of $m$ subsets of $U$, each of size at most $k$, and an integer $t$. Question: are there $t$ sets in $\mathcal{F}$ whose union is $U$?

**Set cover conjecture (Cygan et al.).** For every $\varepsilon > 0$ there is an integer $k$ such that Set Cover with sets of size at most $k$ cannot be solved in time $2^{(1-\varepsilon) n} \mathrm{poly}(m)$.

- **Range.** The base is measured in $n$, the number of elements, not in $m$. Trying all subfamilies takes $2^m \mathrm{poly}(m)$ time, and $m$ can be as large as $n^k$.
- **Model.** As for SETH, the statement is robust: the factor $\mathrm{poly}(m)$ absorbs the polynomial differences between reasonable models such as the [word RAM](/word-ram/).
- **Randomness.** Cygan et al. state SETH for bounded-error randomized algorithms. Their assumption on Set Cover, in Theorem 1.2, does not mention randomness. The consequences below then exclude the same kind of algorithm that the assumption excludes.
- **The quantifiers.** As with SETH, $k$ depends on $\varepsilon$. For each fixed $k$ the conjecture claims nothing; it says that the saving must shrink to 0 as $k$ grows.

All results below are **conditional on** the named hypothesis, except the algorithms, which are unconditional.

### The algorithms it says are optimal

Set Cover on $n$ elements is solved in $2^n \mathrm{poly}(m)$ time in two ways.

- **Dynamic programming over subsets.** For every subset $X \subseteq U$, compute the fewest sets whose union contains $X$, by adding one set at a time; see [bitmask DP](/bitmask-dp/). This is $O(2^n m n)$ time.
- **Inclusion-exclusion.** For a subset $X$, let $a(X)$ be the number of sets of $\mathcal{F}$ contained in $X$. The number of ordered $t$-tuples of sets whose union is $U$ is
$$c_t = \sum_{X \subseteq U} (-1)^{|U \setminus X|}\, a(X)^t,$$
and a cover with $t$ sets exists if and only if $c_t > 0$. Björklund, Husfeldt and Koivisto used this form of the [inclusion-exclusion principle](/inclusion-exclusion-principle/) to count covers and partitions in $2^n$ times a polynomial.

### Consequences

Cygan et al. prove (Theorem 1.2 in the arXiv version): if the set cover conjecture holds, then for every $\varepsilon < 1$,

| Problem | Parameter | Not solvable in | Known algorithm |
|---|---|---|---|
| [Steiner Tree](/steiner-tree-problem/) | $t$ terminals | $2^{\varepsilon t} \mathrm{poly}(n)$ | $2^t \mathrm{poly}(n)$ |
| Connected Vertex Cover | solution size $t$ | $2^{\varepsilon t} \mathrm{poly}(n)$ | $2^t \mathrm{poly}(n)$ |
| Set Partitioning | $n$ elements | $2^{\varepsilon n} \mathrm{poly}(m)$ | $2^n \mathrm{poly}(m)$ |
| [Subset Sum](/subset-sum-problem/) | target $t$ | $t^{\varepsilon} \mathrm{poly}(n)$ | $t\, \mathrm{poly}(n)$, pseudo-polynomial |

The known algorithms are the ones the paper cites, with $\varepsilon = 1$. The theorem goes one way only: it does not reduce these problems back to Set Cover. For the parameterized view of Steiner Tree, see [parameterized Steiner tree](/parameterized-steiner-tree/).

### Relation to SETH

SETH says: for every $\varepsilon < 1$ there is a $k$ such that $k$-CNF-SAT on $n$ variables has no $O(2^{\varepsilon n})$ algorithm. Cygan et al. prove (Theorem 1.1) that SETH is **equivalent** to each of these statements, for every $\varepsilon < 1$ and some $k$:

- [Hitting Set](/hitting-set/) with sets of size at most $k$ over $n$ elements has no $O(2^{\varepsilon n})$ algorithm;
- Set Splitting with sets of size at most $k$ has no $O(2^{\varepsilon n})$ algorithm;
- NAE-SAT on $k$-CNF formulas with $n$ variables has no $O(2^{\varepsilon n})$ algorithm.

Hitting Set is Set Cover with the roles of elements and sets swapped, so the two look alike. But the measure differs: Hitting Set is hard in the number of elements to choose from, and Set Cover is conjectured hard in the number of elements to cover. No reduction from SAT to Set Cover is known that keeps $n$ small enough, so whether SETH implies the set cover conjecture is open.

As evidence, Cygan et al. prove (Theorem 1.3) that computing the **parity** of the number of set covers, with sets of size at most $k$, has no $O(2^{\varepsilon n})$ algorithm for any $\varepsilon < 1$ unless $\oplus$-SETH fails, the hypothesis that the parity of the number of satisfying assignments of a $k$-CNF formula is hard in the same sense. By earlier results that they cite, SETH implies $\oplus$-SETH. So counting set covers modulo 2 is hard under SETH, while deciding whether a cover exists is not known to be.

## Examples

**The two algorithms on a small instance.** Take $U = \{1, 2, 3, 4, 5\}$ and the six sets $S_1 = \{1,2\}$, $S_2 = \{2,3,4\}$, $S_3 = \{4,5\}$, $S_4 = \{1,5\}$, $S_5 = \{3\}$ and $S_6 = \{1,3,5\}$, so $n = 5$, $m = 6$ and $k = 3$.

- The dynamic program over the $2^5 = 32$ subsets of $U$, with one update for each reachable subset and each set, makes 102 updates (the bound $2^n m$ is 192). It finds that the fewest sets that cover $U$ is 2.
- The two smallest covers are $\{S_2, S_4\}$ and $\{S_2, S_6\}$.
- The inclusion-exclusion sum gives $c_1 = 0$, $c_2 = 4$ and $c_3 = 72$. A brute-force count of ordered tuples gives the same numbers. Since $c_1 = 0 < c_2$, the smallest cover has 2 sets, and $c_2 = 4$ counts each of the two covers in both orders.
- Of the $2^6 = 64$ subfamilies, 32 cover $U$, so the parity of the number of set covers is 0. Theorem 1.3 is about computing this bit.

**What a refutation would give.** Suppose that, for some $\varepsilon > 0$, Set Cover with sets of any bounded size had a $2^{(1-\varepsilon) n} \mathrm{poly}(m)$ algorithm. Then the conjecture fails, but no known result shows that SETH fails too. By contrast, a $2^{(1-\varepsilon) n}$ algorithm for Hitting Set with sets of every bounded size would refute SETH, by Theorem 1.1.

## Where it is used

- **Exact exponential algorithms.** It is the standard assumption for showing that dynamic programs over subsets with time $2^n$ are optimal in the base, when SETH does not apply directly.
- **Parameterized complexity.** It gives tight bounds for problems parameterized by the number of terminals or the solution size, as for Steiner Tree and Connected Vertex Cover.
- **Pseudo-polynomial algorithms.** It gives the bound $t^{1-o(1)}$ for Subset Sum in the target $t$, which says that the classic table indexed by the target cannot be shrunk by a power of $t$.
- **Comparing hypotheses.** It is one of several exponential-time hypotheses (ETH, SETH, the set cover conjecture) that are not known to imply each other in all directions; see [conditional lower bound](/conditional-lower-bound/).

## References
