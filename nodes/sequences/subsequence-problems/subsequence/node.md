---
tag: MB6045
kind: definition
slug: subsequence
name: Subsequence
aliases:
- subsequence versus substring
area: sequences/subsequence-problems
level: intro
summary: A sequence obtained by deleting zero or more elements without reordering the rest, unlike a contiguous substring.
prereqs: [alphabet]
see_also: [subarray, subsequence-checking, longest-common-subsequence, longest-increasing-subsequence, shortest-common-supersequence, distinct-subsequences, count-subsequence-occurrences, subsequence-automaton]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.4, Longest common subsequence (the definition of a subsequence and of a common subsequence)
  - book: "M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997"
    locator: Chapter 6, Subwords (J. Sakarovitch and I. Simon), the subword order, binomial coefficients of words and Higman's theorem
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 1 (the difference between a substring and a subsequence) and Chapter 11, Core string edits, alignments, and dynamic programming
---

A subsequence of a sequence is what is left after you delete zero or more of its elements and keep the rest in their original order. The kept elements do not have to be next to each other, and this is the difference from a substring (for arrays, a [subarray](/subarray/)), which is a contiguous block. Subsequences are the objects of the [longest common subsequence](/longest-common-subsequence/), [longest increasing subsequence](/longest-increasing-subsequence/) and [shortest common supersequence](/shortest-common-supersequence/) problems, and of the diff tools that compare files.

## Definition

Let $X = \langle x_1, x_2, \ldots, x_m \rangle$ be a finite sequence over a set $\Sigma$, for example the characters of an [alphabet](/alphabet/). A sequence $Z = \langle z_1, \ldots, z_k \rangle$ is a **subsequence** of $X$ if there are indices

$$1 \le i_1 < i_2 < \cdots < i_k \le m \quad \text{with} \quad x_{i_j} = z_j \text{ for } j = 1, \ldots, k.$$

The index list $(i_1, \ldots, i_k)$ is an **embedding** (or occurrence) of $Z$ in $X$. The case $k = 0$ is allowed: the empty sequence $\varepsilon$ is a subsequence of every sequence. We write $Z \preceq X$. The same object is called a *subword* or *scattered subword* in combinatorics on words.

A **substring** (or *factor*) of $X$ is the special case where the indices are consecutive: $i_{j+1} = i_j + 1$ for each $j$. So $Z = x_{s+1} x_{s+2} \cdots x_{s+k}$ for some offset $s$ with $0 \le s \le m - k$.

A **common subsequence** of $X$ and $Y$ is a sequence $Z$ with $Z \preceq X$ and $Z \preceq Y$. A **supersequence** of $X$ is a sequence $W$ with $X \preceq W$.

**Basic facts.** Let $|X| = m$.

1. Each set of indices $\{i_1 < \cdots < i_k\} \subseteq \{1, \ldots, m\}$ gives one subsequence, so $X$ has $2^m$ embeddings in total, and at most $2^m$ distinct subsequences, the empty one included.
2. The number of distinct subsequences is exactly $2^m$ if and only if the elements of $X$ are pairwise distinct. If $x_i = x_j$ with $i < j$, the index sets $\{i\}$ and $\{j\}$ give the same subsequence. If the elements are distinct, each element fixes its own index, so different index sets give different sequences.
3. Each substring is a subsequence, but not conversely. $X$ has at most $m(m+1)/2$ non-empty substrings, one for each pair of a start and an end position.
4. The relation $\preceq$ is a partial order on the finite sequences over $\Sigma$. It is reflexive (take all indices). It is transitive: if $Z \preceq Y$ by indices $(j_1, \ldots, j_k)$ and $Y \preceq X$ by indices $(i_1, \ldots, i_l)$, then $(i_{j_1}, \ldots, i_{j_k})$ is strictly increasing and embeds $Z$ in $X$. It is antisymmetric: $Z \preceq X$ gives $|Z| \le |X|$, so $Z \preceq X$ and $X \preceq Z$ give $|Z| = |X|$, and then the only index list is $(1, \ldots, m)$, so $Z = X$.
5. If $Z \preceq X$, then $|Z| \le |X|$, with equality only for $Z = X$.

## Examples and non-examples

Take $X = \text{ABCBDAB}$, of length 7, the running example of CLRS Section 14.4.

| $Z$ | subsequence of $X$? | substring of $X$? | number of embeddings |
| --- | --- | --- | --- |
| BCBA | yes, indices 2, 3, 4, 6 | no | 1 |
| BDA | yes | yes, positions 4 to 6 | 2 |
| CBDA | yes | yes, positions 3 to 6 | 1 |
| ABB | yes | no | 3 |
| AA | yes, indices 1, 6 | no | 1 |
| DC | no: the only D is after the only C | no | 0 |

- **Non-example by order.** DC uses letters of $X$, but not in the order of $X$. A subsequence keeps the order.
- **Non-example by multiplicity.** BBBB is not a subsequence of $X$, because $X$ has only three B's.
- **Counts.** $X$ has $2^7 = 128$ embeddings, but only 102 distinct subsequences (the empty one included), because A and B repeat. It has 25 distinct substrings, the empty one included. The page [counting distinct subsequences](/distinct-subsequences/) gives the method that finds 102 without a list of all index sets.
- **Sequences of numbers.** In $\langle 3, 1, 4, 1, 5, 9, 2, 6 \rangle$, the sequence $\langle 1, 4, 5, 9 \rangle$ is an increasing subsequence (indices 2, 3, 5, 6). The sequence $\langle 1, 1, 2 \rangle$ is a subsequence (indices 2, 4, 7). The sequence $\langle 4, 3 \rangle$ is not.

## Related definitions

- **Substring and subarray.** The contiguous case. Problems on contiguous parts, such as the [maximum subarray problem](/maximum-subarray-problem/), have different tools (prefix sums, sliding windows) from problems on subsequences (dynamic programming over two indices).
- **Subsequence test.** Deciding $Z \preceq X$ is [subsequence checking](/subsequence-checking/). A greedy scan does it in $O(|X|)$ time, and a [subsequence automaton](/subsequence-automaton/) answers many such queries on one fixed $X$.
- **Longest common subsequence.** A longest $Z$ with $Z \preceq X$ and $Z \preceq Y$: the [longest common subsequence](/longest-common-subsequence/).
- **Shortest common supersequence.** A shortest $W$ with $X \preceq W$ and $Y \preceq W$: the [shortest common supersequence](/shortest-common-supersequence/).
- **Increasing subsequence.** A subsequence of numbers with $z_1 < z_2 < \cdots < z_k$: the [longest increasing subsequence](/longest-increasing-subsequence/) problem.
- **Binomial coefficient of words.** The number of embeddings of $Z$ in $X$, written $\binom{X}{Z}$ in Lothaire's book. For a one-letter alphabet it is the usual binomial coefficient $\binom{m}{k}$. See [counting pattern occurrences as a subsequence](/count-subsequence-occurrences/).
- **Higman's theorem.** Over a finite alphabet, each infinite set of words has two words $u \ne v$ with $u \preceq v$. In other words, $\preceq$ is a well-quasi-order. Lothaire Chapter 6 gives the proof.
- **Palindromic subsequence.** A subsequence that reads the same in both directions: see the [longest palindromic subsequence](/longest-palindromic-subsequence/).

## References
