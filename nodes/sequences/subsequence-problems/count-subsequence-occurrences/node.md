---
tag: CW3966
kind: problem
slug: count-subsequence-occurrences
name: Counting pattern occurrences as a subsequence
aliases:
- number of subsequence matches
area: sequences/subsequence-problems
level: intro
summary: Count the index sets in a text at which a pattern occurs as a subsequence, using an O(nm) DP.
prereqs: [subsequence, subsequence-checking, tabulation]
see_also: [distinct-subsequences, longest-common-subsequence, rolling-array-space-reduction, binomial-coefficient]
sources:
  - book: "M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997"
    locator: Chapter 6, Subwords, the binomial coefficients of words and their Pascal-type recurrence
  - paper: "Cees Elzinga, Sven Rahmann and Hui Wang, Algorithms for subsequence combinatorics, Theoretical Computer Science 409(3), 2008, 394-404"
    locator: the dynamic programs that count subsequences and embeddings
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.3, Elements of dynamic programming (optimal substructure and overlapping subproblems), and Section 14.4 for the prefix-pair table
---

This problem asks for the number of ways a pattern $P$ of length $m$ occurs as a [subsequence](/subsequence/) of a text $T$ of length $n$: the number of index lists $i_1 < \cdots < i_m$ with $t_{i_k} = p_k$. A table over pairs of prefixes, like the [LCS table](/lcs-dynamic-programming/) but with a sum in place of a maximum, solves it with $\Theta(nm)$ additions, in one row of memory. In combinatorics on words the answer is the *binomial coefficient of words* $\binom{T}{P}$, because for a one-letter alphabet it is the binomial coefficient $\binom{n}{m}$.

## In plain words

Take the text "babgbag" and the word "bag". You can pick a b, then a later a, then a later g, in five different ways. The problem asks for that number.

Look at the last letter of the text. Each way of picking either does not use that letter, or uses it for the last letter of the word. The ways that do not use it are the ways in the text without its last letter. The ways that use it exist only if the two last letters are the same, and they are the ways to pick the rest of the word from the rest of the text. So each count is a sum of two smaller counts, and a table of counts for all pairs of beginnings gives the answer.

## Definition

**Input.** A text $T = t_1 \cdots t_n$ and a pattern $P = p_1 \cdots p_m$ over an alphabet $\Sigma$.

**Output.** The number

$$\binom{T}{P} = \#\{(i_1, \ldots, i_m) : 1 \le i_1 < \cdots < i_m \le n,\ t_{i_k} = p_k \text{ for } k = 1, \ldots, m\}.$$

The empty pattern has one occurrence (the empty list), so $\binom{T}{\varepsilon} = 1$.

**The recurrence.** Let $N[i, j] = \binom{T_i}{P_j}$ for the prefixes $T_i = t_1 \cdots t_i$ and $P_j = p_1 \cdots p_j$. Then

$$N[i, 0] = 1, \qquad N[0, j] = 0 \ (j \ge 1), \qquad N[i, j] = N[i-1, j] + [t_i = p_j]\, N[i-1, j-1] \ (i, j \ge 1),$$

where $[t_i = p_j]$ is 1 if the letters are equal and 0 otherwise.

*Proof.* Split the occurrences of $P_j$ in $T_i$, for $i, j \ge 1$, by their last index $i_j$. If $i_j < i$, the list is an occurrence of $P_j$ in $T_{i-1}$, and each such occurrence is a list of this kind; there are $N[i-1, j]$ of them. If $i_j = i$, then $t_i = p_j$ is needed, and $(i_1, \ldots, i_{j-1})$ is an occurrence of $P_{j-1}$ in $T_{i-1}$; conversely, each such occurrence extended by $i$ is an occurrence of $P_j$ in $T_i$ when $t_i = p_j$. This is a bijection, so there are $[t_i = p_j] N[i-1, j-1]$ of them. The two kinds do not overlap, so the counts add. The base cases hold because the empty list is the only occurrence of $\varepsilon$, and a non-empty pattern has no occurrence in the empty text. $\square$

**One row.** Row $i$ uses only row $i - 1$. If $j$ runs from $m$ down to 1, the update $N[j] \gets N[j] + [t_i = p_j] N[j-1]$ reads $N[j-1]$ before it is changed in this row, so one array of $m + 1$ entries is enough.

```pseudo id=count
COUNT-OCCURRENCES(P[1 .. m], T[1 .. n])
L1  N[0] ← 1; N[1 .. m] ← 0
L2  for i ← 1 to n do
L3      for j ← m downto 1 do
L4          if T[i] = P[j] then N[j] ← N[j] + N[j − 1]
L5  return N[m]
```

## Variants

- **Modulo a number.** The count can have about $n$ bits, so contests ask for it modulo a prime. The same recurrence works in modular arithmetic.
- **Only matching cells.** Line L4 changes $N[j]$ only when $p_j = t_i$. If for each letter $c$ the positions $j$ with $p_j = c$ are listed in decreasing order, the loop of line L3 can visit only these. The work is then $O(n + r)$ additions, where $r$ is the number of pairs $(i, j)$ with $t_i = p_j$.
- **Distinct subsequences.** Count the different strings that are subsequences of $T$, not the index lists: [counting distinct subsequences](/distinct-subsequences/). That needs a different recurrence, because several index lists give the same string.
- **All patterns of one length.** $\sum_{|P| = m} \binom{T}{P} = \binom{n}{m}$, because each set of $m$ indices is an occurrence of exactly one pattern.
- **Common subsequences.** Count the pairs of embeddings of a common subsequence in two texts. The table then runs over pairs of prefixes of the two texts.
- **Decision version.** $\binom{T}{P} > 0$ if and only if $P \preceq T$, which [subsequence checking](/subsequence-checking/) decides in $O(n)$ time.

## Examples

**The CLRS string.** For $T = \text{ABCBDAB}$ and $P = \text{ABB}$, the array $N[0..3]$ after each letter of $T$ is:

| after | $N[0]$ | $N[1]$ (A) | $N[2]$ (AB) | $N[3]$ (ABB) |
| --- | --- | --- | --- | --- |
| start | 1 | 0 | 0 | 0 |
| A | 1 | 1 | 0 | 0 |
| B | 1 | 1 | 1 | 0 |
| C | 1 | 1 | 1 | 0 |
| B | 1 | 1 | 2 | 1 |
| D | 1 | 1 | 2 | 1 |
| A | 1 | 2 | 2 | 1 |
| B | 1 | 2 | 4 | 3 |

So ABB occurs 3 times: at $(1, 2, 4)$, $(1, 2, 7)$ and $(1, 4, 7)$.

**More values.**

| $T$ | $P$ | $\binom{T}{P}$ |
| --- | --- | --- |
| babgbag | bag | 5 |
| rabbbit | rabbit | 3 |
| aaaaaaaaaa (10 a's) | aa | 45 = $\binom{10}{2}$ |
| abab...ab (10 copies of ab) | ab | 55 |
| aaaaaaaaaabbbbbbbbbb | ab | 100 |

The last two rows show that the order of the letters matters: both texts have ten a's and ten b's, but in the second one each a is before each b.

## Known algorithms

- **Table or one row.** $\Theta(nm)$ letter tests and at most $nm$ additions, $O(m)$ words of memory with one row, by COUNT-OCCURRENCES. It is correct by the recurrence and induction on $i$.
- **Sparse version.** $O(n + r)$ additions with $r$ the number of matching pairs, after $O(m + \sigma)$ preprocessing for an alphabet of size $\sigma$.
- **Big numbers.** Since $\binom{T}{P} \le \binom{n}{m}$, each entry has at most $\lg \binom{n}{m} \le n$ bits. With exact integers, each addition costs $O(n / w)$ word operations on a $w$-bit machine, so the bit cost is $O(nm \cdot n / w)$ in the worst case.

## Bounds

- **Size of the answer.** $0 \le \binom{T}{P} \le \binom{n}{m}$, because each occurrence is a set of $m$ indices out of $n$. The bound is reached when $T$ and $P$ use one letter only.
- **Work.** The table needs $nm$ letter tests if it does them all. The sparse version shows that only the matching pairs need an addition. No better general bound for exact counting is stated on this page.
- **Recursion without a table.** A plain recursion on the recurrence makes about $\binom{T}{P}$ or more calls in the worst case, which is exponential. The table avoids this, as in all [tabulation](/tabulation/).

## Reductions

- **From subsequence checking.** $P \preceq T$ if and only if the count is positive.
- **Relation to binomial coefficients.** For $\Sigma = \{a\}$, $\binom{a^n}{a^m} = \binom{n}{m}$, and the recurrence becomes Pascal's rule $\binom{n}{m} = \binom{n-1}{m} + \binom{n-1}{m-1}$.
- **Counting by blocks.** If $T = UV$, then $\binom{UV}{P} = \sum_{P = P'P''} \binom{U}{P'}\binom{V}{P''}$, summed over the $m + 1$ ways to cut $P$ in two. Proof: let $k$ be the number of indices of an occurrence that fall in $U$. Since the indices increase, they are the first $k$, so the occurrence is an occurrence of $p_1 \cdots p_k$ in $U$ followed by an occurrence of $p_{k+1} \cdots p_m$ in $V$, shifted by $|U|$, and each such pair gives one occurrence. This lets the count of a long text be split into parts, or be kept in a segment tree for updates.

## Applications

- **Combinatorics on words.** The binomial coefficients of words are the main tool of Lothaire Chapter 6 for the study of the subword order.
- **Sequence analysis.** The number of embeddings of a motif, with gaps, in a DNA or event sequence is a measure of how often the motif appears.
- **Contest problems.** "Distinct subsequences" style questions (count the ways to delete letters of a text to get a pattern) are this problem.

## References
