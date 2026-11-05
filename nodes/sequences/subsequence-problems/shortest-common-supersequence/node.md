---
tag: TEZVCS
kind: problem
slug: shortest-common-supersequence
name: Shortest common supersequence
aliases:
- SCS
area: sequences/subsequence-problems
level: core
summary: Find a shortest sequence that contains both given sequences as subsequences; its length is n + m minus the LCS length.
prereqs: [longest-common-subsequence, lcs-dynamic-programming]
see_also: [shortest-edit-script, shortest-common-superstring, subsequence, hirschberg-lcs, traceback, myers-diff]
sources:
  - paper: "David Maier, The complexity of some problems on subsequences and supersequences, Journal of the ACM 25(2), 1978, 322-336"
    locator: the NP-completeness of the shortest common supersequence and longest common subsequence problems for an unbounded number of strings
  - paper: "Kari-Jouko Räihä and Esko Ukkonen, The shortest common supersequence problem over binary alphabet is NP-complete, Theoretical Computer Science 16(2), 1981, 187-198"
    locator: the NP-completeness for many strings over a two-letter alphabet
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A4, storage and retrieval, the entries for shortest common supersequence and longest common subsequence
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.4, the LCS table and its traceback, on which the construction of the supersequence is based
---

The shortest common supersequence problem asks for a shortest sequence $S$ that has both $X$ (length $m$) and $Y$ (length $n$) as [subsequences](/subsequence/). For two sequences it is the mirror of the [longest common subsequence](/longest-common-subsequence/): the items that $S$ uses for both inputs at once form a common subsequence, so the shortest length is $m + n - \mathrm{lcs}(X, Y)$, and an SCS is built from an LCS in linear time. For an unbounded number of sequences the problem is NP-hard, even over a two-letter alphabet. It is not the same as the [shortest common superstring](/shortest-common-superstring/), which asks for contiguous occurrences.

## In plain words

You have two lists, and you want one list that contains both, each in its own order, maybe with other items between. The easy answer is to write one list after the other, but this is long. You save one place each time one item of the new list can serve both lists at once.

The items that serve both lists are in both lists in the same order, so they form a common part of the two lists. To save the most, use a longest common part. Walk through the two lists, write the common items once, and write all other items of both lists where they belong.

## Definition

**Input.** Sequences $X = \langle x_1, \ldots, x_m \rangle$ and $Y = \langle y_1, \ldots, y_n \rangle$ over an alphabet $\Sigma$.

**Output.** A sequence $S$ of least length with $X \preceq S$ and $Y \preceq S$, or only its length $\mathrm{scs}(X, Y)$.

**Theorem.** $\mathrm{scs}(X, Y) = m + n - \mathrm{lcs}(X, Y)$.

*Proof.* ($\le$) Take an LCS $Z$ of length $L$ with its positions in $X$ and in $Y$. Between two consecutive items of $Z$ (and before the first and after the last), write the items of $X$ that lie between their positions in $X$, then the items of $Y$ that lie between their positions in $Y$, and then the next item of $Z$ once. The result contains $X$ and $Y$ as subsequences and has $m + n - L$ items.

($\ge$) Let $S$ be a common supersequence of length $s$, with an embedding of $X$ (positions $p_1 < \cdots < p_m$ in $S$) and one of $Y$ (positions $q_1 < \cdots < q_n$). Each position of $S$ is used by at most one item of $X$ and at most one of $Y$. Let $c$ be the number of positions used by both. Then $s \ge m + n - c$. The positions used by both, in increasing order, hold items that are in $X$ and in $Y$ in this order, so they spell a common subsequence of length $c$, and $c \le \mathrm{lcs}(X, Y)$. $\square$

**Direct recurrence.** With $s(i, j) = \mathrm{scs}(X_i, Y_j)$ for the prefixes, $s(i, 0) = i$, $s(0, j) = j$, and for $i, j \ge 1$

$$s(i, j) = \begin{cases} s(i - 1, j - 1) + 1 & \text{if } x_i = y_j, \\ \min(s(i - 1, j), s(i, j - 1)) + 1 & \text{otherwise}. \end{cases}$$

It is the [LCS table](/lcs-dynamic-programming/) with $s(i, j) = i + j - c[i, j]$. The [traceback](/traceback/) writes $x_i$ once on a match, $x_i$ on a move up, and $y_j$ on a move left, and writes the rest of $X$ or $Y$ when it reaches the border.

## Variants

- **Many sequences.** Given $k$ sequences, find a shortest common supersequence. For a fixed $k$, a table over $k$-tuples of prefixes takes $O(n^k)$ time for lengths $n$. When $k$ is part of the input, the decision version is NP-complete (Maier 1978), and it stays NP-complete over a binary alphabet (Räihä and Ukkonen 1981).
- **Weighted items.** Each item has a cost, and the supersequence of least total cost is wanted. For two sequences the same table works with costs in place of 1.
- **Supersequence of a set as a schedule.** For many sequences over an alphabet of size $\sigma$, the sequence $(c_1 c_2 \cdots c_\sigma)^\ell$, where $\ell$ is the largest input length and $c_1, \ldots, c_\sigma$ are the letters, is a common supersequence of length $\sigma \ell$. Since each common supersequence has length at least $\ell$, this is within a factor $\sigma$ of the optimum.
- **Superstring.** If the inputs must occur as contiguous blocks, the problem is the [shortest common superstring](/shortest-common-superstring/), NP-hard already in its basic form and used in genome assembly.

## Examples

| $X$ | $Y$ | lcs | scs | one SCS |
| --- | --- | --- | --- | --- |
| ABCBDAB | BDCABA | 4 | 9 | ABDCABDAB |
| abac | cab | 2 | 5 | cabac |
| AGGTAB | GXTXAYB | 4 | 9 | AGXGTXAYB |
| geek | eke | 2 | 5 | gekek |

For ABDCABDAB, the items of $X = $ ABCBDAB are at positions 1, 2, 4, 6, 7, 8, 9 and the items of $Y = $ BDCABA at 2, 3, 4, 5, 6, 8. The four shared positions 2, 4, 6, 8 hold BCBA, an LCS.

**Three sequences.** For abc, bca and cab, a search over all strings gives the shortest common supersequence abcab, of length 5. The pairwise values do not determine it: for $k \ge 3$ there is no formula like the theorem.

## Known algorithms

- **Through the LCS table.** Fill the [LCS table](/lcs-dynamic-programming/) and trace back as above: $\Theta(mn)$ time and space.
- **Linear space.** Find an LCS with [Hirschberg's algorithm](/hirschberg-lcs/) and merge as in the proof of the theorem: $\Theta(mn)$ time, $\Theta(m + n)$ space.
- **Similar inputs.** A [shortest edit script](/shortest-edit-script/) from [Myers' algorithm](/myers-diff/), with the deleted items, inserted items and kept items written in path order, is an SCS, in $O((m + n) D)$ time.
- **Many sequences.** Exact methods search the $k$-dimensional table, with $\prod_i (n_i + 1)$ cells, or use branch and bound; heuristics such as merging the sequences one by one give supersequences that need not be shortest.

## Bounds

- **Range.** $\max(m, n) \le \mathrm{scs}(X, Y) \le m + n$. The lower end is reached when one sequence is a subsequence of the other, the upper end when they have no common item.
- **Time.** The same as for the LCS length, since each gives the other with one subtraction: $O(mn)$ by the table, $\Omega(mn)$ equality tests in the model of Aho, Hirschberg and Ullman, and no $O(n^{2 - \varepsilon})$ algorithm under SETH (see the [conditional lower bound](/backurs-indyk-lcs-lower-bound/)).
- **Many sequences.** NP-hard, so no polynomial algorithm unless P = NP.

## Reductions

- **To and from LCS.** By the theorem, for two sequences, in $O(m + n)$ time for the objects and $O(1)$ for the lengths.
- **To the shortest edit script.** A path in the edit graph that deletes the items of $X$ not in an LCS and inserts the items of $Y$ not in it, read in order with each item written once, is a common supersequence; the [shortest edit script](/shortest-edit-script/) of length $D = m + n - 2L$ gives an SCS of length $D + L$.
- **Many LCS and many SCS.** For $k \ge 3$ sequences both are NP-hard, but the theorem no longer links their values.

## Applications

- **Merged views of versions.** A side-by-side or unified view of two versions of a file shows each common line once and each changed line once, which is a common supersequence of the two versions.
- **Scheduling on one machine.** If several jobs each need a sequence of operations in a given order, and the machine can serve all jobs that wait for the same operation at once, a shortest schedule is a shortest common supersequence of the operation lists.
- **Teaching.** It is a standard exercise on reusing the LCS table and its traceback.

## References
