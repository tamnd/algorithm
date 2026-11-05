---
tag: Q8SJ29
kind: problem
slug: longest-common-subsequence
name: Longest common subsequence
aliases:
- LCS
area: sequences/subsequence-problems
level: intro
summary: Given two sequences, find a longest sequence that is a subsequence of both.
prereqs: [subsequence]
see_also: [lcs-dynamic-programming, hirschberg-lcs, hunt-szymanski, myers-diff, shortest-edit-script, shortest-common-supersequence, edit-distance, longest-common-substring]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.4, Longest common subsequence (Theorem 14.1, the procedures LCS-LENGTH and PRINT-LCS, and the DNA example)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11 (the longest common subsequence as a special case of alignment) and Chapter 12 (linear space and sparse dynamic programming)
  - paper: "Alfred V. Aho, Daniel S. Hirschberg and Jeffrey D. Ullman, Bounds on the complexity of the longest common subsequence problem, Journal of the ACM 23(1), 1976, 1-12"
    locator: the lower bound of order mn comparisons in the model of equal and unequal tests
  - paper: "David Maier, The complexity of some problems on subsequences and supersequences, Journal of the ACM 25(2), 1978, 322-336"
    locator: the NP-completeness of the longest common subsequence of many strings
  - paper: "Vaclav Chvatal and David Sankoff, Longest common subsequences of two random sequences, Journal of Applied Probability 12(2), 1975, 306-315"
    locator: the existence of the limit constant for random sequences and the first bounds on it
  - paper: "William J. Masek and Michael S. Paterson, A faster algorithm computing string edit distances, Journal of Computer and System Sciences 20(1), 1980, 18-31"
    locator: the Four Russians method for the edit distance table, O(n^2 / log n) for a finite alphabet
---

The longest common subsequence (LCS) problem takes two sequences $X$ and $Y$ and asks for a longest sequence that is a [subsequence](/subsequence/) of both. A [dynamic program](/lcs-dynamic-programming/) over pairs of prefixes solves it in $O(nm)$ time for lengths $n$ and $m$, and no algorithm is known that is faster by a polynomial factor; under the Strong Exponential Time Hypothesis none exists. LCS is the core of the `diff` tool: the lines of an LCS are the lines that two files share, and the other lines are the [edit script](/shortest-edit-script/). For three or more input sequences in general, the problem is NP-hard.

## In plain words

You have two words, or two files. You want the longest list of items that appears in both, in the same order, where in each input the items may have other items between them. For the words ABCBDAB and BDCABA, one answer is BCBA: you can find B, C, B, A from left to right in both words.

The answer is not unique in general, but its length is. The standard method fills a table. Each cell holds the answer for a beginning of the first word and a beginning of the second word. Each cell needs only three cells next to it, so you can fill the whole table row by row.

## Definition

**Input.** Two finite sequences $X = \langle x_1, \ldots, x_n \rangle$ and $Y = \langle y_1, \ldots, y_m \rangle$ over a set $\Sigma$ with an equality test.

**Output.** A sequence $Z$ with $Z \preceq X$ and $Z \preceq Y$ (a *common subsequence*) whose length $|Z|$ is maximum. The maximum length is written $\mathrm{lcs}(X, Y)$. The length-only version outputs this number.

Equivalently, the output is a *matching*: index pairs $(i_1, j_1), \ldots, (i_k, j_k)$ with $i_1 < \cdots < i_k$, $j_1 < \cdots < j_k$ and $x_{i_t} = y_{j_t}$ for each $t$, with $k$ maximum. The pairs are non-crossing lines between equal items of the two sequences.

From the definition, $0 \le \mathrm{lcs}(X, Y) \le \min(n, m)$, $\mathrm{lcs}(X, Y) = \mathrm{lcs}(Y, X)$, and $\mathrm{lcs}(X, Y) = \min(n,m)$ if and only if the shorter sequence is a subsequence of the longer.

## Variants

- **Length only or one LCS.** The length needs only two rows of the table. One LCS needs the full table and a [traceback](/traceback/), or [Hirschberg's algorithm](/hirschberg-lcs/) in linear space.
- **All LCSs or their number.** The number of distinct LCSs can be exponential in $n$, so listing them all takes exponential time in the worst case.
- **Many sequences ($k$-LCS).** A longest common subsequence of $k$ sequences. The DP over $k$-tuples of prefixes takes $O(n^k)$ time. For an unbounded number of sequences the decision version is NP-complete (Maier 1978).
- **Weighted LCS and alignment.** Matches score by a weight table, and gaps cost. This is [global alignment](/global-alignment/) and the [Needleman-Wunsch](/needleman-wunsch/) algorithm. LCS is the case with match score 1 and no other score.
- **Longest common substring.** The common part must be contiguous in both. This is a different problem, solved in linear time with suffix trees: see [longest common substring](/longest-common-substring/).
- **Constrained and restricted LCS.** The LCS must contain, or must avoid, a given pattern as a subsequence.

## Examples

**The CLRS example.** $X = \text{ABCBDAB}$ and $Y = \text{BDCABA}$. Then $\mathrm{lcs}(X, Y) = 4$, and the distinct LCSs are BCAB, BCBA and BDAB. The full table of prefix lengths $c[i, j] = \mathrm{lcs}(X[1 \ldots i], Y[1 \ldots j])$ is

| | | B | D | C | A | B | A |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| B | 0 | 1 | 1 | 1 | 1 | 2 | 2 |
| C | 0 | 1 | 1 | 2 | 2 | 2 | 2 |
| B | 0 | 1 | 1 | 2 | 2 | 3 | 3 |
| D | 0 | 1 | 2 | 2 | 2 | 3 | 3 |
| A | 0 | 1 | 2 | 2 | 3 | 3 | 4 |
| B | 0 | 1 | 2 | 2 | 3 | 4 | 4 |

The [LCS dynamic programming](/lcs-dynamic-programming/) page traces this table back.

**DNA.** For the strands $S_1 = \text{ACCGGTCGAGTGCGCGGAAGCCGGCCGAA}$ (29 bases) and $S_2 = \text{GTCGTTCGGAATGCCGTTGCTCTGTAAA}$ (28 bases), the LCS has length 20 and is unique: GTCGTCGGAAGCCGGCCGAA.

**Edge cases.** $\mathrm{lcs}(X, \varepsilon) = 0$. If $X$ and $Y$ have no item in common, the answer is 0. If $Y$ is the reverse of $X$, an LCS is a [longest palindromic subsequence](/longest-palindromic-subsequence/) of $X$ in length.

**Random sequences.** For two independent uniform random binary sequences of length $n$, $\mathbb{E}[\mathrm{lcs}]/n$ tends to a constant $\gamma_2$ (Chvátal and Sankoff 1975). Its exact value is not known. A simulation (seed 3; 20, 20 and 3 pairs) gives

| $n$ | 100 | 1000 | 3000 |
| --- | --- | --- | --- |
| mean of $\mathrm{lcs}/n$ | 0.771 | 0.805 | 0.809 |

so $\gamma_2$ is about 0.81.

## Known algorithms

| algorithm | time | space | when it is good |
| --- | --- | --- | --- |
| [LCS dynamic programming](/lcs-dynamic-programming/) | $\Theta(nm)$ | $\Theta(nm)$, or $\Theta(\min(n,m))$ for the length | always; the base method |
| [Hirschberg's algorithm](/hirschberg-lcs/) | $\Theta(nm)$ | $\Theta(n + m)$ | one LCS with little memory |
| [Hunt-Szymanski](/hunt-szymanski/) | $O((r + n) \log n)$, $r$ matching pairs | $O(r + n)$ | few matches, as in lines of files |
| [Myers' O(ND) algorithm](/myers-diff/) | $O((n + m) D)$, $D = n + m - 2\,\mathrm{lcs}$ | $O(n + m)$ | similar inputs |
| [Bit-parallel LCS](/bit-parallel-lcs/) | $O(\lceil m/w \rceil n)$ on a $w$-bit word RAM | $O(\sigma m / w)$ | short strings, small alphabet $\sigma$ |
| [Four Russians](/four-russians-method/) (Masek and Paterson 1980) | $O(n^2 / \log n)$ for a constant alphabet | $O(n^2 / \log n)$ | theory |

The structure that all exact methods use is the [optimal substructure of LCS](/lcs-optimal-substructure/): if the last items are equal, they end an LCS; if not, an LCS drops the last item of one of the two sequences.

## Bounds

- **Upper bound.** $O(nm)$ by the DP, and $O(n^2 / \log n)$ for constant alphabets by the Four Russians method. For unbounded alphabets, slightly sub-quadratic bounds exist, by factors polylogarithmic in $n$.
- **Comparison lower bound.** Aho, Hirschberg and Ullman (1976) proved that an algorithm that only tests pairs of items for equal or not equal needs $\Omega(nm)$ tests in the worst case when the alphabet is not bounded. With a total order on the items, their bound is $\Omega(n \log n)$ comparisons.
- **Conditional lower bound.** If the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) holds, no algorithm computes $\mathrm{lcs}$ of two binary strings of length $n$ in $O(n^{2 - \varepsilon})$ time for any $\varepsilon > 0$. See the [Backurs-Indyk lower bound](/backurs-indyk-lcs-lower-bound/) and the [LCS SETH lower bound](/lcs-seth-lower-bound/).
- **Many sequences.** For $k$ sequences with $k$ part of the input, the problem is NP-hard (Maier 1978).

## Reductions

- **Shortest edit script.** With insertions and deletions only, the least number of edits from $X$ to $Y$ is $D = n + m - 2\,\mathrm{lcs}(X, Y)$. The matched items stay, the other items of $X$ are deleted and the other items of $Y$ are inserted. See [shortest edit script](/shortest-edit-script/).
- **Shortest common supersequence.** A shortest common supersequence has length $n + m - \mathrm{lcs}(X, Y)$. See [shortest common supersequence](/shortest-common-supersequence/).
- **Edit distance.** LCS is [edit distance](/edit-distance/) with insertions and deletions of cost 1 and no substitution (or substitutions of cost 2).
- **Longest increasing subsequence.** Each LIS problem is an LCS problem with the sorted sequence. In the other direction, LCS reduces to LIS on the list of matching pairs, which is Hunt-Szymanski. See [longest increasing subsequence](/longest-increasing-subsequence/).
- **Palindromes.** The [longest palindromic subsequence](/longest-palindromic-subsequence/) of $X$ has the length $\mathrm{lcs}(X, X^R)$.

## Applications

- **File comparison.** `diff` and the merge tools of version control systems show the lines outside an LCS of the two files as deletions and insertions.
- **Biology.** LCS is the simplest measure of how similar two DNA or protein sequences are. Real tools use scored [alignments](/pairwise-sequence-alignment/), which use the same table.
- **Text and data.** Detection of copied text, the comparison of records, and the merge of edits in collaborative tools.

## References
