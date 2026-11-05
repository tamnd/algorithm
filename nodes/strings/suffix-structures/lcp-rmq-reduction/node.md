---
tag: WJ6WGX
kind: concept
slug: lcp-rmq-reduction
name: LCP-RMQ reduction
aliases:
- LCP as range minimum
area: strings/suffix-structures
level: advanced
summary: The LCP of two suffixes equals the minimum of the LCP array between their ranks.
prereqs: [lcp-array, suffix-array, range-minimum-query]
see_also: [longest-common-extension-query, lcp-array, range-minimum-query, lowest-common-ancestor, cartesian-tree, lcp-interval-tree, sparse-table, fischer-heun-rmq]
sources:
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948, the Lcp values of non-adjacent suffixes computed as minima of the values of adjacent suffixes
  - paper: doi:10.1007/3-540-48194-X_17
    title: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, CPM 2001, LNCS 2089
    locator: pages 181 to 192, the lemma on the minimum of the height array between two ranks
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press, 2015
    locator: Chapter 8 (Classical indexes), the LCP array with range minimum queries
  - paper: doi:10.1016/j.jda.2010.08.004
    title: Lucian Ilie, Gonzalo Navarro and Liviu Tinta, The longest common extension problem revisited and applications to approximate string searching, Journal of Discrete Algorithms 8(4), 2010
    locator: the LCE methods compared, among them the suffix array with a range minimum structure on the LCP array
---

The LCP-RMQ reduction is the fact that, for two suffixes of a text at ranks $i < j$ of the [suffix array](/suffix-array/), the length of their longest common prefix is the minimum of the [LCP array](/lcp-array/) over the ranks $i+1$ to $j$. So any LCP question about two suffixes becomes a [range minimum query](/range-minimum-query/) on one array, which a linear-space structure answers in $O(1)$ time. It is the basis of the constant-time [longest common extension query](/longest-common-extension-query/), and it is the array form of a classic fact on the [suffix tree](/suffix-tree/): the common prefix of two suffixes is the path label of the [lowest common ancestor](/lowest-common-ancestor/) of their leaves.

## In plain words

Sort all endings of a text like words in a dictionary. For each line, write how many first letters it shares with the line just above it.

Now take two lines that are far apart. How many first letters do they share? Because the list is sorted, every line between them starts with the same letters as both of them. So the shared start of the two lines is as long as the smallest count written on the lines between them, from the line after the first to the second one.

This turns a question about two strings into a question about numbers: what is the smallest number in this stretch of a list? Many fast methods answer that question in constant time.

## The idea

Let $T = T[0 \ldots n-1]$ be a text over a general ordered alphabet, with 0-based positions, suffixes $T_p = T[p \ldots n-1]$, and no sentinel. The suffix array $SA$ lists the suffixes in increasing order, with a proper prefix before the longer string, and $S_i = T_{SA[i]}$. $LCP[0] = 0$ and $LCP[i] = \mathrm{lcp}(S_{i-1}, S_i)$ for $1 \le i < n$.

**Lemma (LCP-RMQ).** For $0 \le i < j < n$,

$$\mathrm{lcp}(S_i, S_j) = \min_{i < k \le j} LCP[k].$$

The proof uses two facts about strings.

*Fact 1 (sandwich).* If $x \le z \le y$ in lexicographic order, then $\mathrm{lcp}(x, z) \ge \mathrm{lcp}(x, y)$ and $\mathrm{lcp}(z, y) \ge \mathrm{lcp}(x, y)$. Let $h = \mathrm{lcp}(x, y)$ and $u = x[0 \ldots h-1]$. Suppose $z$ does not start with $u$. If $z$ is a proper prefix of $u$, then $z < x$. Otherwise, let $t < h$ be the first index with $z[t] \ne u[t]$. If $z[t] < u[t]$, then $z < x$, and if $z[t] > u[t]$, then $z > y$. Each case contradicts $x \le z \le y$. So $z$ starts with $u$.

*Fact 2 (chain).* For any strings, $\mathrm{lcp}(a, c) \ge \min(\mathrm{lcp}(a, b), \mathrm{lcp}(b, c))$, since $a$, $b$ and $c$ all start with the same string of length $\min(\mathrm{lcp}(a, b), \mathrm{lcp}(b, c))$.

*Proof of the lemma.* Let $h = \mathrm{lcp}(S_i, S_j)$. By Fact 1, every $S_k$ with $i \le k \le j$ starts with $S_i[0 \ldots h-1]$, so each $LCP[k]$ with $i < k \le j$ is at least $h$, and the minimum is at least $h$. By Fact 2 and induction on $j - i$, $\mathrm{lcp}(S_i, S_j) \ge \min(LCP[i+1], \ldots, LCP[j])$. So the two are equal. $\square$

The second half holds for any list of strings. The first half needs the list to be sorted; it is where the order is used.

**The reduction.** To find the longest common prefix of the suffixes at text positions $p \ne q$:

1. map them to ranks with the inverse array, $i = \min(RANK[p], RANK[q])$ and $j = \max(RANK[p], RANK[q])$;
2. return $\mathrm{RMQ}_{LCP}(i + 1, j)$.

For $p = q$ the answer is $n - p$. With a [sparse table](/sparse-table/), the query takes $O(1)$ time after $O(n \log n)$ preprocessing; with the method of [Fischer and Heun](/fischer-heun-rmq/) or of [Bender and Farach-Colton](/bender-farach-colton-rmq/), the preprocessing is $O(n)$ and the extra space is $O(n)$ or less.

**The tree view.** The [Cartesian tree](/cartesian-tree/) of $LCP[1 \ldots n-1]$ is a binary tree; when each parent and child with the same value are merged into one node, it has the shape of the internal part of the suffix tree. A range minimum is a lowest common ancestor in the Cartesian tree. The lemma says that the string depth of the lowest common ancestor of two leaves of the suffix tree is the minimum of the LCP values between them in leaf order. The [LCP interval tree](/lcp-interval-tree/) makes this exact: each internal node of the suffix tree is an interval $[i, j]$ of ranks, and its string depth is $\min LCP[i+1 \ldots j]$.

**The other direction.** Range minimum on any integer array reduces to the lowest common ancestor in its Cartesian tree, and back. So LCP queries, range minimum queries and lowest common ancestor queries are one problem in three forms, all with $O(n)$ preprocessing and $O(1)$ query time in the [word RAM](/word-ram/).

## Examples

For $T = \texttt{mississippi}$, $SA = [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$ and $LCP = [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]$.

| ranks $i, j$ | $S_i$ | $S_j$ | $LCP[i+1 \ldots j]$ | minimum = lcp |
|---|---|---|---|---|
| 2, 3 | issippi | ississippi | 4 | 4 (`issi`) |
| 1, 3 | ippi | ississippi | 1, 4 | 1 (`i`) |
| 9, 10 | ssippi | ssissippi | 3 | 3 (`ssi`) |
| 7, 10 | sippi | ssissippi | 2, 1, 3 | 1 (`s`) |
| 4, 5 | mississippi | pi | 0 | 0 |
| 0, 4 | i | mississippi | 1, 1, 4, 0 | 0 |

The row for ranks 7 and 10 shows Fact 1: the suffixes `sissippi` and `ssippi` between them also start with `s`, and the step from `sissippi` to `ssippi`, with LCP 1, is the one that limits the answer.

For text positions, $\mathrm{lcp}(T_2, T_5)$ compares `ssissippi` and `ssippi`. Their ranks are 10 and 9, so the answer is $\min LCP[10 \ldots 10] = 3$.

## Where it is used

- **Longest common extension.** The [LCE query](/longest-common-extension-query/) in $O(1)$ time after $O(n)$ preprocessing, the main step of the kangaroo method for matching with $k$ mismatches and of the search for maximal palindromes and tandem repeats.
- **Suffix comparison.** Two suffixes $T_p$ and $T_q$ compare in $O(1)$ time: find $\ell = \mathrm{lcp}(T_p, T_q)$ and compare $T[p + \ell]$ with $T[q + \ell]$. Algorithms that merge two sorted lists of suffixes, or sort a sparse set of suffixes, use this.
- **Pattern search in $O(m + \log n)$.** Manber and Myers store the LCP values of the pairs that a binary search visits; the general form of these values is the range minimum.
- **Suffix tree simulation.** The [LCP interval tree](/lcp-interval-tree/) and the [enhanced suffix array](/enhanced-suffix-array/) use the lemma to find the children and the string depth of a node, and the [compressed suffix tree](/compressed-suffix-tree/) uses range minima on a compressed LCP array.
- **Counting and repeat problems.** The proofs for the [count of distinct substrings](/count-distinct-substrings/), the [longest repeated substring](/longest-repeated-substring/) and the [longest common substring](/longest-common-substring/) all use the lemma.

## References
