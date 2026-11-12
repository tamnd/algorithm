---
tag: YFVXEQ
kind: problem
slug: counting-linear-extensions
name: Counting linear extensions of a poset
aliases:
- number of topological orders
- counting topological sorts
- '#LE'
area: combinatorics/counting-algorithms
level: research
summary: 'Counts total orders consistent with a partial order; #P-complete.'
prereqs: [topological-sort, total-order, bitmask-dp, dilworth-theorem]
see_also: [hook-length-formula, counting-standard-young-tableaux, catalan-numbers, fpras, approximate-counting, path-coupling, model-counting, sum-over-subsets]
sources:
  - paper: doi:10.1007/BF00383444
    title: Graham Brightwell and Peter Winkler, Counting linear extensions, Order 8(3), 225 to 242, 1991
    locator: "the main theorem (counting linear extensions is #P-complete)"
  - paper: doi:10.1016/S0012-365X(98)00333-1
    title: Russ Bubley and Martin Dyer, Faster random generation of linear extensions, Discrete Mathematics 201(1-3), 81 to 88, 1999
    locator: the path coupling analysis of a Markov chain on linear extensions, with mixing time O(n^3 log n)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 3, Partially ordered sets (linear extensions, order ideals, and the lattice of order ideals)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.2, Generating all permutations (the generation of all topological sorts)
---

Counting linear extensions asks, for a finite partially ordered set $P$ with $n$ elements, for the number $e(P)$ of [total orders](/total-order/) on its elements that agree with the partial order. Equivalently, $e(P)$ is the number of [topological sorts](/topological-sort/) of a directed acyclic graph. Brightwell and Winkler proved in 1991 that the problem is #P-complete. Exact algorithms run a dynamic program over the down-sets of $P$, which is exponential in general but polynomial for posets of bounded width. Special posets have product formulas, such as the [hook length formula](/hook-length-formula/), and a Markov chain on linear extensions gives an [FPRAS](/fpras/).

## In plain words

You have a list of tasks, and some pairs of tasks have a rule: this one must come before that one. How many different orders can you do all the tasks in while obeying every rule?

If there are no rules at all, every order works. If the rules force a single line, only one order works. In between, the count can be anything, and in general it is very hard to compute fast. A direct method keeps track of which tasks are already done. For each set of done tasks that obeys the rules, it counts the ways to reach that set, by adding up the counts of the sets one task smaller. This is fast when the tasks form a few long lines with some links between them, and slow when many tasks are free of each other.

## Definition

Notation: $P = (X, \le_P)$ is a finite partially ordered set with $|X| = n$. A *linear extension* of $P$ is a bijection $\lambda : X \to [n]$ such that $x <_P y$ implies $\lambda(x) < \lambda(y)$. A *down-set* (order ideal) is a set $D \subseteq X$ such that $y \in D$ and $x \le_P y$ imply $x \in D$. An element $x \in D$ is *maximal* in $D$ if no $y \in D$ has $x <_P y$. The *width* of $P$ is the size of its largest antichain.

**Problem.** Input: a poset $P$ on $n$ elements, given by its relations or by a directed acyclic graph whose reachability order is $P$. Output: $e(P)$, the number of linear extensions.

**Recurrence.** For every down-set $D$, let $e(D)$ be the number of linear extensions of $P$ restricted to $D$. Then $e(\emptyset) = 1$ and

$$e(D) = \sum_{x \text{ maximal in } D} e(D \setminus \{x\}).$$

*Proof.* In a linear extension of $D$, the last element is maximal in $D$, since an element above it would come later. Removing the last element leaves a linear extension of $D \setminus \{x\}$, which is again a down-set. Conversely, a linear extension of $D \setminus \{x\}$ followed by a maximal $x$ is a linear extension of $D$. The cases for different last elements are disjoint. $\square$

The answer is $e(X)$. The same recurrence is a path count: $e(P)$ is the number of maximal chains in the lattice of down-sets of $P$.

## Variants

- **Special posets with formulas.** An antichain has $n!$ extensions and a chain has 1. For a disjoint union, $e(P + Q) = \binom{|P| + |Q|}{|P|} e(P) \, e(Q)$, and for an ordinal sum (all of $P$ below all of $Q$), $e(P \oplus Q) = e(P) \, e(Q)$. So series-parallel posets are counted in polynomial time.
- **Forests.** If each element has at most one element directly below it (a rooted forest, roots at the bottom), then $e(P) = n! / \prod_{x} h_x$, where $h_x$ is the size of the subtree rooted at $x$.
- **Young diagrams.** For the poset of cells of a Young diagram, the linear extensions are the standard Young tableaux, counted by the [hook length formula](/hook-length-formula/); see [counting standard Young tableaux](/counting-standard-young-tableaux/).
- **Listing.** To list all linear extensions rather than count them, use a generator of all topological sorts in constant amortized time per extension, as in Knuth's Volume 4A.
- **Sampling.** Draw a uniform random linear extension. By self-reducibility, approximate sampling and approximate counting are equivalent; see [approximate counting](/approximate-counting/).
- **Restricted posets.** The problem stays #P-complete for posets of height 2 and for posets of dimension 2 (Dittmer and Pak).

## Examples

| poset | $e(P)$ for sizes $0, 1, 2, \ldots$ | OEIS |
|---|---|---|
| $2 \times m$ grid ($2m$ elements, $m = 0, \ldots, 8$) | 1, 1, 2, 5, 14, 42, 132, 429, 1430 | A000108, the [Catalan numbers](/catalan-numbers/) |
| fence $x_1 < x_2 > x_3 < x_4 > \cdots$ ($n = 0, \ldots, 12$) | 1, 1, 1, 2, 5, 16, 61, 272, 1385, 7936, 50521, 353792, 2702765 | A000111, the up/down numbers |
| Boolean lattice of subsets of $[k]$ ($k = 0, \ldots, 4$) | 1, 1, 2, 48, 1680384 | A046873 |

The $3 \times 3$ grid has 42 linear extensions, which is the number of standard Young tableaux of the $3 \times 3$ square.

**A worked case.** Let $X = \{a, b, c, d\}$ with $a < c$, $b < c$ and $b < d$. The down-sets and the values of $e$ are:

| down-set $D$ | maximal elements | $e(D)$ |
|---|---|---|
| $\emptyset$ | | 1 |
| $\{a\}$ | $a$ | 1 |
| $\{b\}$ | $b$ | 1 |
| $\{a, b\}$ | $a, b$ | $1 + 1 = 2$ |
| $\{b, d\}$ | $d$ | 1 |
| $\{a, b, c\}$ | $c$ | 2 |
| $\{a, b, d\}$ | $a, d$ | $e(\{b, d\}) + e(\{a, b\}) = 1 + 2 = 3$ |
| $\{a, b, c, d\}$ | $c, d$ | $e(\{a, b, d\}) + e(\{a, b, c\}) = 3 + 2 = 5$ |

The five extensions are $abcd$, $abdc$, $bacd$, $badc$ and $bdac$.

## Known algorithms

- **Dynamic programming over down-sets.** Evaluate the recurrence for all down-sets in order of size. Store the down-sets as bit masks, so the test "$x$ is maximal in $D$" or, going upward, "all predecessors of $x$ are in $D$" is one mask operation. The time is $O(n \cdot I(P))$ arithmetic operations, where $I(P)$ is the number of down-sets, and $I(P) \le 2^n$, so it is $O(2^n n)$ with a full table, as in [bitmask DP](/bitmask-dp/).
- **Bounded width.** If $P$ has width $w$, then by [Dilworth's theorem](/dilworth-theorem/) it splits into $w$ chains $C_1, \ldots, C_w$. A down-set meets each chain in a prefix, so $I(P) \le \prod_i (|C_i| + 1) \le (n / w + 1)^w$. The dynamic program then runs in $O(n (n/w + 1)^w)$ operations, which is polynomial for fixed $w$.
- **Formulas.** For forests, series-parallel posets and Young diagrams, the formulas above give $e(P)$ in polynomial time.
- **Approximate counting.** The Markov chain that picks a position at random, with suitable weights, and swaps the two adjacent elements at that position when the swap keeps the extension valid, mixes in $O(n^3 \log n)$ steps, by the [path coupling](/path-coupling/) analysis of Bubley and Dyer. Karzanov and Khachiyan first proved rapid mixing of a chain on linear extensions. Combined with the reduction from counting to sampling, this gives an FPRAS for $e(P)$.

## Bounds

$1 \le e(P) \le n!$, with $e(P) = 1$ exactly for a chain and $e(P) = n!$ exactly for an antichain. The output has $O(n \log n)$ bits, so the hardness is in the counting, not the output size.

**Hardness.** Counting linear extensions is #P-complete under polynomial-time Turing reductions (Brightwell and Winkler, 1991). So no polynomial-time exact algorithm exists unless every #P function is computable in polynomial time.

**Link to sorting.** Any comparison algorithm that sorts the elements of $X$, given that the order extends $P$, must tell apart all $e(P)$ possible outcomes, so it needs at least $\log_2 e(P)$ comparisons in the worst case. Kahn and Saks showed that $O(\log e(P))$ comparisons are always enough, by finding a comparison that splits the extensions in a balanced way.

## Reductions

- **To topological sorts.** A directed acyclic graph and its reachability order have the same topological sorts, so the input can be either.
- **To model counting.** The order constraints can be written as a propositional formula on position bits, so [model counting](/model-counting/) solvers apply, although the direct dynamic program is usually better.
- **Counting by sampling.** Fix the relative order of one incomparable pair at a time and estimate the fraction of extensions that agree with it by sampling. The product of the fractions gives $1 / e(P)$. This is the self-reducibility method of [Jerrum, Valiant and Vazirani](/jerrum-valiant-vazirani-theorem/).

## Applications

- Sorting under partial information, where $\log_2 e(P)$ is the information-theoretic number of comparisons that remain.
- Scheduling and project planning: the number of valid orders of tasks with precedence rules.
- Probability that one event comes before another in a random valid order, which is a ratio of two counts, used for example in ranking from partial preferences.
- Enumerative combinatorics: many classical numbers, such as the Catalan numbers, the up/down numbers and the counts of standard Young tableaux, are $e(P)$ for a natural poset.

## References
