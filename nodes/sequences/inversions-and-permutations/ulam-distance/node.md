---
tag: A7K8JC
kind: definition
slug: ulam-distance
name: Ulam distance
aliases:
- Ulam metric
area: sequences/inversions-and-permutations
level: advanced
summary: Minimum number of delete-and-insert moves turning one permutation into another; equals n minus their longest common subsequence.
prereqs: [permutation, longest-increasing-subsequence]
see_also: [kendall-tau-distance, cayley-distance, spearman-footrule, longest-common-subsequence, patience-sorting, edit-distance, hamming-distance, presortedness]
sources:
  - paper: "Persi Diaconis, Group Representations in Probability and Statistics, Institute of Mathematical Statistics Lecture Notes, Monograph Series, Volume 11, 1988"
    locator: Chapter 6 (metrics on permutations, including Ulam's metric and its relation to the longest increasing subsequence)
  - paper: "David Aldous and Persi Diaconis, Longest increasing subsequences: from patience sorting to the Baik-Deift-Johansson theorem, Bulletin of the American Mathematical Society 36(4) (1999) 413-432"
    locator: patience sorting, the 2 sqrt(n) law and the Tracy-Widom fluctuations of the longest increasing subsequence
  - paper: "Jinho Baik, Percy Deift and Kurt Johansson, On the distribution of the length of the longest increasing subsequence of random permutations, Journal of the American Mathematical Society 12(4) (1999) 1119-1178"
    locator: the limit law of the longest increasing subsequence of a uniform random permutation
---

The Ulam distance between two rankings of the same $n$ items is the least number of moves that turn one into the other, where a move takes out one item and puts it back at any other place. The items that are never moved keep their relative order, so they form a common subsequence, and the distance is $n$ minus the length of the [longest common subsequence](/longest-common-subsequence/) of the two rankings. After relabeling, that is $n$ minus the [longest increasing subsequence](/longest-increasing-subsequence/) of one permutation, which [patience sorting](/patience-sorting/) finds in $O(n \log n)$ time. The metric is named after Stanislaw Ulam, who proposed it for comparing sequences in biology, and its distribution for a random permutation is concentrated near $n - 2\sqrt n$.

## Definition

**Moves.** For a sequence $a = (a_1, \ldots, a_n)$, a *move* deletes some $a_i$ and inserts it at another position. Moving an item one place left or right is an exchange of neighbors; moving it far shifts every item in between by one place.

**Ulam distance.** For two rankings $a, b$ of a set $X$ of $n$ items, $U(a, b)$ is the least number of moves that turn $a$ into $b$.

**Formula.** With $w = \operatorname{pos}_b \circ a$, the positions in $b$ of the items of $a$ in the order of $a$,
$$U(a, b) = n - \operatorname{LCS}(a, b) = n - \operatorname{LIS}(w),$$
where LCS is the length of a longest common subsequence and LIS the length of a longest increasing subsequence.

*Proof.* The items that a sequence of moves never touches appear in the same relative order in $a$ and in $b$, so they form a common subsequence, and at least $n - \operatorname{LCS}(a, b)$ items must move. Conversely, keep a longest common subsequence fixed and move each other item once, directly to its place relative to the items already placed, in the order of $b$. A common subsequence of $a$ and $b$ is a set of items whose positions in $b$ increase along $a$, an increasing subsequence of $w$. $\square$

**Properties.**

- **A metric.** It is a shortest-path distance in the graph of moves, which is symmetric, so it is a metric, invariant under renaming the items.
- **Range.** $0 \le U \le n - 1$, with $U = n - 1$ exactly when $w$ is decreasing, so when $b$ is $a$ reversed.
- **One move.** Exactly $(n-1)^2$ rankings are at distance 1 from a given one: an item can go to $n - 1$ new places, and the $n - 1$ exchanges of neighbors are each counted twice.
- **Comparison with other metrics.** $U \le K$, the [Kendall tau distance](/kendall-tau-distance/), since an exchange of neighbors is a move. $U \le H$, the [Hamming distance](/hamming-distance/) of $w$ to the identity, since the fixed points of $w$ form an increasing subsequence. $U \le 2T$, where $T$ is the [Cayley distance](/cayley-distance/), since an exchange of two items is two moves.
- **Edit distance.** With insertions and deletions only, the [edit distance](/edit-distance/) of two permutations is $2U$, since each move is one deletion and one insertion and both operations must be used equally often.
- **Computing it.** $\Theta(n \log n)$ comparisons with patience sorting, and $O(n \log \log n)$ time on a word RAM for integer positions.

## Examples and non-examples

**Two rankings.** $a = (A, B, C, D, E)$ and $b = (B, E, A, C, D)$ give $w = 3\,1\,4\,5\,2$, as on the Kendall tau page. Its longest increasing subsequences are $1\,4\,5$ and $3\,4\,5$ of length 3, so $U = 5 - 3 = 2$. In $a$ the common subsequence $A, C, D$ stays, and moving $B$ to the front and then $E$ after $B$ gives $b$. The Kendall distance is 4, the Cayley distance 4 and the footrule 8.

**One item moved far.** Moving one item from the top of a ranking of $n$ items to the bottom gives Ulam distance 1, while the Kendall distance is $n - 1$. This is the situation in which Ulam's metric differs most from Kendall's.

**Distribution.** For $n = 4$, the numbers of permutations at Ulam distance $0, 1, 2, 3$ from the identity are $1, 9, 13, 1$, and for $n = 6$ they are $1, 25, 181, 381, 131, 1$. These are the numbers of permutations whose longest increasing subsequence has length $n, n-1, \ldots, 1$, which the Robinson-Schensted correspondence expresses as sums of squares of numbers of standard Young tableaux.

**Random permutations.** For a uniform random $w \in S_n$, $\mathbb{E}[\operatorname{LIS}(w)] / \sqrt n \to 2$, by Vershik and Kerov and by Logan and Shepp, and Baik, Deift and Johansson showed that $(\operatorname{LIS}(w) - 2\sqrt n)/n^{1/6}$ converges to the Tracy-Widom distribution. So the Ulam distance between two random rankings is about $n - 2\sqrt n$.

**Non-example: substitutions.** If a single operation may also overwrite an item with another, the result is no longer a ranking of the same set. The Ulam distance applies to permutations of one set; the [edit distance](/edit-distance/) is the general notion for strings.

## Related definitions

- **[Kendall tau distance](/kendall-tau-distance/).** Moves restricted to exchanges of neighbors. It can be $n - 1$ times larger than $U$.
- **[Cayley distance](/cayley-distance/).** Exchanges of any two items. $U \le 2T$, and $T$ can be much larger than $U$: a single move of an item across $n - 1$ others is an $n$-cycle, with $T = n - 1$.
- **[Spearman's footrule](/spearman-footrule/).** The total displacement. One far move can create a footrule of $2(n-1)$.
- **[Longest common subsequence](/longest-common-subsequence/).** For two permutations it reduces to an LIS problem in $O(n \log n)$ time. This is the case of the [Hunt-Szymanski](/hunt-szymanski/) method in which every symbol has exactly one match.
- **[Presortedness](/presortedness/).** $U(w, \mathrm{id}) = n - \operatorname{LIS}(w)$ is the measure Rem, the least number of items whose removal leaves a sorted sequence.

## References
