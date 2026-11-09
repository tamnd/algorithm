---
tag: QNS07K
kind: definition
slug: output-sensitive-generation
name: Output-sensitive generation
aliases:
- Output-sensitive enumeration
- Output-sensitive listing
area: combinatorics/generating-partitions-and-trees
level: core
summary: Generation whose running time is bounded by a function of the number of objects produced, not of the size of the search space.
prereqs: [combinatorial-generation, amortized-cost]
see_also: [output-sensitive-enumeration, constant-amortized-time-generation, loopless-generation, enumeration-problem, reverse-search, next-balanced-bracket-sequence, orderly-generation, beyer-hedetniemi]
sources:
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 1.7, Analyzing the Algorithms (CAT and BEST algorithms, and the Don't Count the Output Principle), and Section 1.3, Four Basic Questions (the Next routine and loopless algorithms)
  - paper: doi:10.1016/0020-0190(88)90065-8
    title: David S. Johnson, Mihalis Yannakakis and Christos H. Papadimitriou, On generating all maximal independent sets, Information Processing Letters 27(3), 1988, 119 to 123
    locator: the definitions of polynomial total time, incremental polynomial time and polynomial delay
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1, Generating basic combinatorial patterns (loopless algorithms and the cost per visited object)
---

A generation algorithm is *output-sensitive* when its running time is bounded by a function of the number $N$ of objects it lists, and of their size $n$, and not by the size of a larger space that it searches. The strongest common forms are *constant amortized time* (CAT), total time $O(N)$, and *loopless* generation, time $O(1)$ between two objects; weaker forms are polynomial delay and polynomial total time. For trees and graphs these bounds separate good methods from methods that list a large superset and throw most of it away. The bounds count the change to one current object, not the cost of writing each object out.

## Definition

Let $S_n$ be a finite set of objects with size parameter $n$, and let $N = |S_n|$. A *generator* for $S_n$ lists each element of $S_n$ exactly once. It keeps one current object in a data structure, and it calls a procedure VISIT on it each time it is complete; the user reads the object in place. Time is measured in the [word RAM](/word-ram/) model, after a preprocessing step whose time is polynomial in $n$. Let $T(n)$ be the total time, and let the *delay* be the largest time before the first visit, between two consecutive visits, or after the last visit.

The generator is:

- **Output polynomial** (polynomial total time) if $T(n) \le p(n) \cdot N$ for a polynomial $p$.
- **Polynomial delay** if the delay is at most $p(n)$ for a polynomial $p$. This implies polynomial total time.
- **CAT**, constant amortized time, if $T(n) = O(N)$, so that the average time per object is $O(1)$, independent of $n$.
- **Loopless** if the delay is $O(1)$. This implies CAT. The name comes from the successor routine, which has no loop.

*Output-sensitive generation* is the general goal of a bound of one of these forms. A generator that is not output-sensitive does work that the size of $S_n$ does not pay for, usually by visiting the elements of a larger set $U_n \supset S_n$ with $|U_n| / |S_n| \to \infty$ faster than any polynomial.

**The cost of the output.** The time to write each object, $\Theta(n)$ per object if it is copied, is not counted. This is Ruskey's *Don't Count the Output Principle*: the measure is the amount of change to the data structure. If each object is copied, every generator costs $\Omega(nN)$, and the bounds above cannot tell a CAT method from one that rebuilds each object from scratch. Each page in this folder says which model it uses: visited in place, or copied.

**BEST algorithms.** A [backtracking](/generic-backtracking-algorithm/) generator is *BEST*, "backtracking ensuring success at terminals", if every leaf of its search tree is an object of $S_n$. If, in addition, every internal node of the search tree has at least two children, the tree has at most $N - 1$ internal nodes, because a tree with $N$ leaves and $I$ internal nodes of degree at least 2 has at least $2I$ edges and exactly $N + I - 1$. With $O(1)$ work per node, such a generator is CAT. Chains of nodes with one child are the usual obstacle, and a CAT proof must bound their total length by $O(N)$.

## Examples and non-examples

- **Successor rule for bracket words.** The [next balanced bracket sequence](/next-balanced-bracket-sequence/) rule changes the current word in place. One step can rewrite $2n - 1$ cells, so it is not loopless, but its total cost over all $C_n$ words is less than $8 C_n + 2n$. It is CAT, and its delay is $O(n)$.
- **Generate and test for bracket words.** List all $4^n$ words of length $2n$ and keep the balanced ones. The ratio $4^n / C_n$ grows like $\sqrt{\pi}\, n^{3/2}$; it is about 62 for $n = 10$ and 168 for $n = 20$. So this method is output polynomial, but not CAT.
- **Unlabeled graphs by filtering.** List all $2^{\binom{n}{2}}$ labeled graphs on $[n]$ and keep one per isomorphism class. For $n = 10$ there are $2^{45} \approx 3.5 \cdot 10^{13}$ labeled graphs and $12\,005\,168$ classes, a ratio of about $2.9 \cdot 10^6$. The ratio tends to $n!$, so this method is not output polynomial. [Orderly generation](/orderly-generation/) and [canonical augmentation](/canonical-augmentation/) visit only a small number of graphs per class.
- **Rooted and free trees.** The [Beyer-Hedetniemi](/beyer-hedetniemi/) successor of [level sequences](/level-sequence/) and the [Wright-Richmond-Odlyzko-McKay](/wright-richmond-odlyzko-mckay/) algorithm list unlabeled rooted and free trees in constant amortized time, in place.
- **Labeled trees by Prüfer decoding.** Listing all $n^{n-2}$ sequences in $[n]^{n-2}$ and [decoding](/pruefer-decoding/) each into a new tree costs $O(n)$ per tree. This has polynomial delay, but it rebuilds each tree, so it is not CAT in the in-place model.
- **Permutations.** [Heap's algorithm](/heaps-algorithm/) does one swap per permutation and is CAT, and the [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) order of adjacent swaps has loopless implementations.

## Related definitions

- [Output-sensitive enumeration](/output-sensitive-enumeration/): the same idea for enumeration problems with an input, such as all maximal independent sets of a graph, with the extra class of incremental polynomial time.
- [Constant amortized time generation](/constant-amortized-time-generation/) and [loopless generation](/loopless-generation/): the two strongest bounds, with their own pages.
- [Enumeration problem](/enumeration-problem/): the task of listing all solutions of an instance.
- [Amortized cost](/amortized-cost/): the average cost per operation over a sequence, the measure behind CAT.
- [Gray code](/gray-code/): a list in which consecutive objects differ by a small change, a frequent route to loopless generation.
- [Reverse search](/reverse-search/): a design that lists the objects as a tree of parents and children, often with polynomial delay and small space.

## References
