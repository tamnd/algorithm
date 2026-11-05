---
tag: 0514ZY
kind: problem
slug: permutation-pattern-matching
name: Permutation pattern matching
aliases:
- pattern containment in permutations
area: sequences/inversions-and-permutations
level: advanced
summary: Decide whether a permutation contains a subsequence order-isomorphic to a given pattern; NP-complete in general.
prereqs: [permutation-pattern-avoidance]
see_also: [stack-sortable-permutations, longest-increasing-subsequence, counting-inversions, np-complete, inversion, stack-permutation-generability, erdos-szekeres-theorem, subsequence]
sources:
  - paper: "Prosenjit Bose, Jonathan F. Buss and Anna Lubiw, Pattern matching for permutations, Information Processing Letters 65(5) (1998) 277-283"
    locator: NP-completeness of the general problem and the polynomial algorithm for separable patterns
  - paper: "Sylvain Guillemot and Dániel Marx, Finding small patterns in permutations in linear time, Proceedings of the 25th ACM-SIAM Symposium on Discrete Algorithms (2014) 82-101"
    locator: the fixed-parameter algorithm with running time linear in n for every fixed pattern length
  - paper: "Michael H. Albert, Robert E. L. Aldred, Mike D. Atkinson and Derek A. Holton, Algorithms for pattern involvement in permutations, Proceedings of the 12th International Symposium on Algorithms and Computation, Lecture Notes in Computer Science 2223 (2001) 355-366"
    locator: fast algorithms for patterns of length at most 4
---

Permutation pattern matching asks whether a text permutation $p$ of length $n$ contains a pattern $\sigma$ of length $k$: whether some $k$ entries of $p$, in their left-to-right order, have the same relative order as $\sigma$. It is the membership test for the classes of [pattern avoidance](/permutation-pattern-avoidance/). Bose, Buss and Lubiw showed in 1998 that the problem is NP-complete when $k$ is part of the input, while trying all $\binom nk$ subsequences solves it in $n^{O(k)}$ time. Guillemot and Marx showed that for every fixed $k$ it takes only linear time, with a constant that grows like $2^{O(k^2 \log k)}$, and special patterns such as $12 \cdots k$ or separable patterns are solved in polynomial time for every $k$.

## In plain words

You have a long row of distinct numbers and a short template such as "low, high, middle". The question is whether you can pick some numbers from the row, keeping their order, so that they fit the template. In 3 1 4 5 2 the numbers 1, 4, 2 fit "low, high, middle".

For a template of 2 or 3 numbers this is quick. For a long template the number of ways to pick entries explodes, and in general nobody knows a method that is fast for long templates; the problem is one of the hard ones. But if the template has a fixed length, there is a clever method whose running time grows only in proportion to the length of the row.

## Definition

**Input.** A permutation $p \in S_n$, the text, and a permutation $\sigma \in S_k$, the pattern, with $k \le n$.

**Question.** Are there positions $i_1 < i_2 < \cdots < i_k$ such that $p_{i_a} < p_{i_b} \iff \sigma_a < \sigma_b$ for all $a, b \in [k]$? Such positions are an *occurrence* of $\sigma$ in $p$, and $p$ *contains* $\sigma$. Otherwise $p$ *avoids* $\sigma$.

**Equivalently.** An occurrence is an order-preserving map $\phi : [k] \to [n]$ such that $p_{\phi(a)}$ standardizes to $\sigma$. In the plot of the points $(i, p_i)$, it is a set of $k$ points whose relative positions, left to right and bottom to top, are those of the points of $\sigma$.

## Variants

- **Counting.** Count the occurrences, not only decide whether one exists. For $\sigma = 21$ this is [counting inversions](/counting-inversions/).
- **Fixed pattern.** $\sigma$ is fixed and only $p$ is input. Then the question is membership in the class $\operatorname{Av}(\sigma)$.
- **Special patterns.** $\sigma = 12 \cdots k$, which asks whether the [longest increasing subsequence](/longest-increasing-subsequence/) has length at least $k$, and separable patterns, which avoid $2413$ and $3142$.
- **Special texts.** $p$ itself avoids some pattern, for example $321$. The problem stays NP-complete for some such text classes and becomes polynomial for others.
- **Consecutive patterns.** The entries of an occurrence must be adjacent in $p$, which makes the problem a string-matching problem with an order-isomorphism test, solvable in $O(n + k \log k)$ time by a variant of Knuth-Morris-Pratt.
- **Avoiding a set of patterns.** Test membership in $\operatorname{Av}(B)$ for a finite basis $B$, one test per pattern.

## Examples

**Patterns of length 3 in $3\,1\,4\,5\,2$.** Its $\binom53 = 10$ triples of entries give $123$ twice ($1\,4\,5$ and $3\,4\,5$), $132$ twice, $213$ twice, $231$ three times, $312$ once and $321$ never. So it contains every pattern of length 3 except $321$.

**Length 4.** $3\,1\,4\,5\,2$ contains $3142$, in the two occurrences $3\,1\,4\,2$ and $3\,1\,5\,2$, but avoids $2413$. The permutation $3\,1\,6\,2\,5\,4$ contains both: $3\,6\,2\,5$ is a $2413$ and $3\,1\,6\,2$ is a $3142$.

**A fast special case.** Whether $p$ contains $231$ is decided by one pass of greedy stack sorting in $\Theta(n)$ time: $p$ avoids $231$ exactly when the pass sorts it, see [stack-sortable permutations](/stack-sortable-permutations/).

## Known algorithms

- **Brute force.** Try all $\binom nk$ position sets and test each in $O(k \log k)$ time, for $O(\binom nk k \log k)$ total. A backtracking search that extends partial occurrences and checks the order constraints as it goes is much faster in practice.
- **Increasing patterns.** $12 \cdots k$ is contained exactly when the longest increasing subsequence has length at least $k$, decided in $O(n \log n)$ time by patience sorting, or $O(n \log \log n)$ for integer values.
- **Small patterns.** Every pattern of length 3 is detected in $O(n)$ time, and Albert, Aldred, Atkinson and Holton gave $O(n \log n)$ time for every pattern of length 4.
- **Separable patterns.** Bose, Buss and Lubiw match a separable pattern by dynamic programming over its decomposition tree in $O(kn^4)$ time, and later work lowered the exponent.
- **Fixed-parameter algorithm.** Guillemot and Marx find an occurrence in $2^{O(k^2 \log k)}\, n$ time. Their method uses the Marcus-Tardos theorem: if $p$ avoids $\sigma$, then $p$ has a structure of bounded width in terms of $k$, along which a dynamic program searches for $\sigma$; otherwise a large grid structure in $p$ contains every pattern of length $k$. Fox later improved the dependence on $k$ to $2^{O(k^2)}$.
- **Constraint satisfaction.** Berendsohn, Kozma and Marx treat an occurrence as a solution of a binary constraint satisfaction problem and decide, and also count, in $n^{k/4 + o(k)}$ time, which beats brute force when $k$ grows with $n$.

## Bounds

- **NP-completeness.** The problem is NP-complete when both $p$ and $\sigma$ are input, by a reduction from 3-satisfiability, see [NP-complete](/np-complete/). It is in NP since an occurrence is checked in $O(k \log k)$ time.
- **Fixed $k$.** Linear time for every fixed $k$, so the problem is fixed-parameter tractable in $k$. The dependence on $k$ cannot be polynomial unless P = NP.
- **Lower bound for any input.** $\Omega(n)$ time is needed to read $p$, so the Guillemot-Marx bound is optimal in $n$.
- **Counting.** No algorithm that counts occurrences in $f(k)\, n$ time is known; the best general counting methods take $n^{ck}$ time for a constant $c < 1$.

## Reductions

- **From 3-satisfiability.** Bose, Buss and Lubiw build a text and a pattern from a formula so that occurrences correspond to satisfying assignments.
- **To the longest increasing subsequence.** For $\sigma = 12 \cdots k$ or $k \cdots 21$ the problem is the LIS question for $p$ or its reverse.
- **Symmetries.** Containment is preserved by reversing, complementing or inverting both $p$ and $\sigma$, so an algorithm for one pattern solves its images under these 8 symmetries.

## Applications

- **Membership in permutation classes.** Deciding whether a permutation can be sorted by a given device, such as a stack, a deque or two parallel stacks, is a pattern test for each element of the basis.
- **Experimental combinatorics.** Computing $|\operatorname{Av}_n(B)|$ for small $n$ by generating permutations and testing them, which is how conjectures about pattern classes are found.
- **Time series and ranked data.** Searching for an order pattern, such as a local peak or a rise-fall-rise shape, in a sequence of measurements, usually in its consecutive form.

## References
