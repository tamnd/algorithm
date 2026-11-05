---
tag: A25WSV
kind: problem
slug: shortest-edit-script
name: Shortest edit script
aliases:
- minimal diff
- insertion-deletion edit distance
area: sequences/subsequence-problems
level: core
summary: Find the fewest insertions and deletions that turn one sequence into another, equivalent to LCS.
prereqs: [longest-common-subsequence, edit-operations]
see_also: [myers-diff, lcs-dynamic-programming, hunt-szymanski, hirschberg-lcs, edit-distance, alignment-graph, shortest-common-supersequence, backurs-indyk-lcs-lower-bound]
sources:
  - paper: doi:10.1007/BF01840446
    title: Eugene W. Myers, An O(ND) difference algorithm and its variations, Algorithmica 1, 1986, 251-266
    locator: the definitions of the edit script and the edit graph, the relation D = N + M - 2L with the LCS length, and the greedy O((N + M) D) algorithm
  - paper: "Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974, 168-173"
    locator: edit sequences with insertions, deletions and changes, and the table that finds a cheapest one
  - paper: "J. W. Hunt and M. D. McIlroy, An algorithm for differential file comparison, Computing Science Technical Report 41, Bell Laboratories, 1976"
    locator: the file comparison problem of the diff program, solved through a longest common subsequence of lines
  - paper: "Esko Ukkonen, Algorithms for approximate string matching, Information and Control 64, 1985, 100-118"
    locator: the computation of the edit distance in time proportional to the distance times the length
---

The shortest edit script problem asks for the fewest insertions and deletions of single items that turn a sequence $A$ of length $m$ into a sequence $B$ of length $n$, together with such a list of operations. The kept items of $A$ form a common subsequence of $A$ and $B$, so the least number of operations is $D = m + n - 2L$, where $L$ is the length of a [longest common subsequence](/longest-common-subsequence/). This is the problem that the diff program solves on the lines of two files, and the output of diff is an edit script. It is the [edit distance](/edit-distance/) with insertions and deletions only, and [Myers' algorithm](/myers-diff/) solves it in $O((m + n) D)$ time, which is fast when the two sequences are similar.

## In plain words

You have an old version and a new version of a text, as two lists of lines. You want to describe the change with as few steps as you can, where each step either removes one line of the old text or adds one line of the new text. This list of steps is a diff.

The lines that you never touch are in both texts, in the same order. So a short list of steps keeps as many lines as possible, and the lines that it keeps are a longest common part of the two texts. Each line of the old text that is not kept is removed, and each line of the new text that is not kept is added.

## Definition

**Input.** Two sequences $A = \langle a_1, \ldots, a_m \rangle$ and $B = \langle b_1, \ldots, b_n \rangle$ over a set with an equality test.

**Edit script.** A list of operations, each of one of two kinds: *delete* $a_i$, or *insert* $b_j$ (at the place between the items of $A$ where it belongs). Applied to $A$, the script must give $B$. The [edit operations](/edit-operations/) page lists the general kinds; here substitutions are not allowed.

**Output.** An edit script of least length $D(A, B)$, also called the insertion-deletion distance or LCS distance.

**The edit graph.** Myers states the problem as a shortest path. The vertices are the points $(i, j)$, $0 \le i \le m$, $0 \le j \le n$. There is a horizontal edge $(i - 1, j) \to (i, j)$ (delete $a_i$) and a vertical edge $(i, j - 1) \to (i, j)$ (insert $b_j$), each of cost 1, and a diagonal edge $(i - 1, j - 1) \to (i, j)$ of cost 0 when $a_i = b_j$. A path from $(0, 0)$ to $(m, n)$ is an edit script, its diagonals are the kept items, and $D(A, B)$ is the cost of a cheapest path. This is the [alignment graph](/alignment-graph/) of the two sequences with the costs of this problem.

**Theorem.** $D(A, B) = m + n - 2 \cdot \mathrm{lcs}(A, B)$.

*Proof.* A path from $(0, 0)$ to $(m, n)$ with $d$ diagonal edges has $m - d$ horizontal and $n - d$ vertical edges, so its cost is $m + n - 2d$. Its diagonal edges are matches $(i, j)$ with $i$ and $j$ both strictly increasing, so they spell a common subsequence of length $d$; hence $d \le \mathrm{lcs}(A, B)$ and each script has at least $m + n - 2\,\mathrm{lcs}(A, B)$ operations. Conversely, take an LCS with matches $(i_1, j_1), \ldots, (i_L, j_L)$. Go from $(0, 0)$ to $(i_1 - 1, j_1 - 1)$ by horizontal and vertical edges, take the diagonal to $(i_1, j_1)$, and so on, and end with horizontal and vertical edges to $(m, n)$. This path has $L$ diagonals and cost $m + n - 2L$. $\square$

## Variants

- **With substitutions.** Allow "change $a_i$ to $b_j$" at cost 1: this is the Levenshtein [edit distance](/edit-distance/), solved by the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/). A substitution costs 2 in the insertion-deletion model.
- **Weighted operations.** Give each operation a cost that depends on the item; the shortest path in the edit graph is still found by dynamic programming, as in [global alignment](/global-alignment/).
- **Granularity.** Line diffs treat each line as one item, word diffs each word, character diffs each character. The problem is the same; only the items change.
- **Length only.** Output only $D(A, B)$. By the theorem this is the LCS length problem.
- **Bounded distance.** Decide whether $D(A, B) \le k$, and if so find a script. Only the diagonals $j - i \in [-k, k]$ of the edit graph can be used, which gives $O(k \max(m, n))$ time, as in [banded alignment](/banded-alignment/).

## Examples

**Myers' example.** $A = \text{ABCABBA}$, $B = \text{CBABAC}$. Here $\mathrm{lcs}(A, B) = 4$ (for example CABA), so $D = 7 + 6 - 8 = 5$. One shortest script, with positions in $A$:

| step | operation | result |
| --- | --- | --- |
| 1 | delete $a_1$ = A | BCABBA |
| 2 | delete $a_2$ = B | CABBA |
| 3 | insert B after $a_3$ = C | CBABBA |
| 4 | delete $a_6$ = B | CBABA |
| 5 | insert C after $a_7$ = A | CBABAC |

The kept items are $a_3 a_4 a_5 a_7$ = CABA. The edit graph of this pair has 7 different cheapest paths from $(0, 0)$ to $(7, 6)$.

**More pairs.**

| $A$ | $B$ | lcs | $D$ |
| --- | --- | --- | --- |
| ABCBDAB | BDCABA | 4 | 5 |
| kitten | sitting | 4 | 5 |
| abc | abc | 3 | 0 |
| abc | xyz | 0 | 6 |

For kitten and sitting the Levenshtein distance is 3 (two substitutions and one insertion), but the insertion-deletion distance is 5, since each substitution costs one deletion and one insertion.

## Known algorithms

- **LCS table.** Fill the [LCS table](/lcs-dynamic-programming/) and trace back; each step of the traceback that is not a match is a deletion (up) or an insertion (left). $\Theta(mn)$ time and space.
- **Linear space.** [Hirschberg's algorithm](/hirschberg-lcs/) gives an LCS, and so a script, in $\Theta(mn)$ time and $\Theta(m + n)$ space.
- **Sparse matches.** The [Hunt-Szymanski algorithm](/hunt-szymanski/) takes $O((r + m + n) \log n)$ time, with $r$ the number of matching pairs; it was the method of the first Unix diff.
- **Greedy by distance.** [Myers' algorithm](/myers-diff/) explores the edit graph by increasing cost and follows runs of diagonals greedily. It takes $O((m + n) D)$ time, $O(m + n + D^2)$ space for the script, or linear space with the "middle snake" refinement. Ukkonen gave an algorithm with the same kind of bound for edit distance in 1985.
- **Bit-parallel.** The [bit-parallel LCS](/bit-parallel-lcs/) gives the length, so $D$, in $O(\lceil m / w \rceil n)$ word operations.

## Bounds

- **Upper bounds.** $O(mn)$ time by the table, and $O((m + n) D)$ by Myers. So two sequences that differ in a constant number of places are compared in linear time.
- **Comparison lower bound.** With only equality tests and an unbounded alphabet, $\Omega(mn)$ tests are needed for the LCS length (Aho, Hirschberg and Ullman), and by the theorem the same holds for $D$.
- **Conditional lower bound.** Under the strong exponential time hypothesis, the LCS length of two strings of length $n$ over a fixed alphabet has no $O(n^{2 - \varepsilon})$ algorithm; see the [conditional lower bound](/backurs-indyk-lcs-lower-bound/). By the theorem, the same holds for $D$. Myers' bound is not in conflict with this, because $D$ can be of order $n$.

## Reductions

- **To and from LCS.** By the theorem, $D(A, B)$ and $\mathrm{lcs}(A, B)$ give each other in $O(1)$ arithmetic, and a script and an LCS give each other in $O(m + n)$ time.
- **To shortest paths.** The edit graph is a DAG with edge costs 0 and 1, so a cheapest path is found by dynamic programming in topological order, or by a breadth-first search by cost, which is the idea of Myers' algorithm.
- **To the shortest common supersequence.** The items of the script with the kept items, in path order, spell a [shortest common supersequence](/shortest-common-supersequence/) of $A$ and $B$, of length $m + n - L$.

## Applications

- **File comparison.** diff and its descendants in version control systems show the change between two versions of a file as an edit script of lines. A patch tool applies such a script to a file.
- **Version storage.** Systems that store the differences between versions instead of each full version store edit scripts.
- **Spelling and text comparison.** Character-level scripts show where two words or texts differ.
- **Biology.** Alignments of sequences without substitution scores are insertion-deletion scripts; with scores they become [global alignments](/global-alignment/).

## References
