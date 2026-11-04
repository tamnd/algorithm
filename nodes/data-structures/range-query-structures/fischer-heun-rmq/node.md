---
tag: 6H7AGY
kind: algorithm
slug: fischer-heun-rmq
name: Fischer-Heun RMQ
aliases:
- succinct RMQ
- 2n+o(n) bit RMQ
area: data-structures/range-query-structures
level: research
summary: Succinct range minimum structure using 2n+o(n) bits with O(1) queries.
solves: [range-minimum-query]
model: word-ram
complexity:
  vars: {n: the length of the array; the time is per query after O(n) preprocessing, and the space is in bits, without the array}
  time: {worst: O(1)}
  space: {extra: "2n + o(n)"}
properties: {deterministic: true, online: true, recursive: false}
prereqs: [bender-farach-colton-rmq, dfuds, rank-select-dictionary, succinct-data-structures]
see_also: [cartesian-tree, range-min-max-tree, balanced-parentheses-representation, catalan-numbers, lcp-array, suffix-array, ordinal-tree, sparse-table]
sources:
  - paper: doi:10.1137/090779759
    title: "Johannes Fischer and Volker Heun, Space-Efficient Preprocessing Schemes for Range Minimum Queries on Static Arrays, SIAM Journal on Computing 40(2) (2011), 465-492"
    locator: the 2d-Min-heap, its DFUDS representation in 2n + o(n) bits, the query formula with select, a ±1 range minimum and findopen, and the lower bound of 2n - O(log n) bits
  - url: https://users.dcc.uchile.cl/~gnavarro/ps/dcc16.pdf
    title: "Hector Ferrada and Gonzalo Navarro, Improved Range Minimum Queries, Data Compression Conference (DCC 2016)"
    locator: the section on the Fischer-Heun solution (the map from the binary Cartesian tree to a general tree with an extra root, Eq. (2) on DFUDS, the Grossi-Ottaviano Eq. (3)) and A Simplified Implementation (Eq. (4) on BP, with Lemma 1)
  - paper: doi:10.1007/s00453-004-1146-6
    title: "David Benoit, Erik D. Demaine, J. Ian Munro, Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Representing Trees of Higher Degree, Algorithmica 43(4) (2005), 275-292"
    locator: the depth-first unary degree sequence (DFUDS) and its navigation by rank, select and parenthesis matching
---

The Fischer-Heun structure answers [range minimum queries](/range-minimum-query/) on a static array of $n$ items in $O(1)$ time using only $2n + o(n)$ bits, and it never reads the array during a query. It stores the shape of the *2d-Min-heap* of the array, a tree in which the parent of each position is the nearest earlier position with a smaller or equal item, as a sequence of $2n + 2$ parentheses in the [DFUDS](/dfuds/) order, and it adds $o(n)$ bits of directories for rank, select, range minima on the excess, and parenthesis matching. A query is two select operations, one ±1 range minimum as in the [Bender-Farach-Colton algorithm](/bender-farach-colton-rmq/), one matching parenthesis and one or two ranks. Since the answers to all queries determine the shape of the [Cartesian tree](/cartesian-tree/), and there are $C_n \approx 4^n$ shapes, $2n - O(\log n)$ bits are needed, so the space is optimal up to the lower-order term.

## In plain words

Many programs ask "where is the smallest item between positions $l$ and $r$?" on a huge array, such as the arrays of a text index. The answers depend only on the pattern of which item is smaller than which, not on the items themselves. This pattern can be drawn as a tree, and a tree with $n$ nodes can be written down as a string of $2n$ brackets.

Fischer and Heun choose a tree in which each position hangs under the last earlier position that is not bigger, and write it as brackets. With a few small helper tables on top, each question is answered by counting and finding brackets: a handful of steps, no matter how big the array is. The array itself can be thrown away, and about two bits per item remain.

## The problem

**Input.** A static array $A[1 \ldots n]$ over a totally ordered set.

**Queries.** $\textsc{rmq}(i, j)$ for $1 \le i \le j \le n$: the position of the leftmost minimum of $A[i \ldots j]$.

**Goal.** An *encoding*: a structure that answers every query without access to $A$, in $O(1)$ time on a word RAM with $\Theta(\log n)$-bit words, with $2n + o(n)$ bits, built in $O(n)$ time.

## The algorithm

**The 2d-Min-heap.** Add a virtual position 0 with $A[0] = -\infty$. The parent of $i \ge 1$ is the largest $j < i$ with $A[j] \le A[i]$; children are ordered by position. A stack builds the tree in $O(n)$ time. The preorder of this ordered tree is $0, 1, \ldots, n$, so node $i$ is the $i$-th node after the root in preorder. It is the tree obtained from the Cartesian tree by the standard map from binary trees with $n$ nodes to ordinal trees with $n + 1$ nodes.

**DFUDS.** Write one "(" and then, for each node $v$ in preorder, $\deg(v)$ copies of "(" followed by one ")". The result $E[1 \ldots 2n + 2]$ is balanced, and the ")" that ends the description of node $v$ is the $(v + 1)$-st ")" of $E$. Let $D[p]$ be the excess, the number of "(" minus the number of ")" in $E[1 \ldots p]$.

**Directories.** On top of $E$, $o(n)$-bit structures give in $O(1)$ time: $\mathrm{rank}_0(p)$, the number of ")" in $E[1 \ldots p]$; $\mathrm{select}_0(t)$, the position of the $t$-th ")"; $\pm 1\mathrm{RMQ}(x, y)$, the position of the leftmost minimum of $D[x \ldots y]$, with the block method of Bender and Farach-Colton made succinct; and $\mathrm{open}(w)$, the position of the "(" that matches the ")" at $w$.

```pseudo id=main
BUILD(A)
L1  compute the 2d-Min-heap of A with a stack: parent(i) = the last j < i with A[j] ≤ A[i], or 0
L2  E ← "(" followed by "("^deg(v) ")" for v = 0, 1, …, n
L3  build rank, select, ±1 RMQ and open directories on E; discard A

QUERY(i, j)                                ▷ 1 ≤ i ≤ j ≤ n
L4  if i = j then return i
L5  x ← select_0(i + 1), y ← select_0(j)
L6  w ← ±1RMQ(x, y)                        ▷ the leftmost minimum of the excess D[x..y]
L7  if rank_0(open(w)) = i then return i
L8  return rank_0(w)
```

Line L5 finds the end of the description of node $i$ and of node $j - 1$. The ")" at $w$ closes the matching of a "(" in the description of some node: line L7 tests whether that node is $i$, which happens when $i$ is the parent of the answer, so $i$ itself is the minimum; otherwise line L8 returns the node whose description ends at $w$.

## Example

Take $A = [4, 2, 5, 1, 6, 3]$ with positions 1 to 6. The parents are $0, 0, 2, 0, 4, 4$, so the root 0 has the children 1, 2 and 4, node 2 has the child 3, and node 4 has the children 5 and 6. Then

$E = \texttt{(} \; \texttt{((()} \; \texttt{)} \; \texttt{()} \; \texttt{)} \; \texttt{(()} \; \texttt{)} \; \texttt{)}$ $= \texttt{(((())())(()))}$, with 14 bits.

| $p$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $E[p]$ | ( | ( | ( | ( | ) | ) | ( | ) | ) | ( | ( | ) | ) | ) |
| $D[p]$ | 1 | 2 | 3 | 4 | 3 | 2 | 3 | 2 | 1 | 2 | 3 | 2 | 1 | 0 |

The ")" are at 5, 6, 8, 9, 12, 13 and 14, which end the descriptions of nodes 0 to 6.

- $\textsc{rmq}(3, 6)$: $x = \mathrm{select}_0(4) = 9$, $y = \mathrm{select}_0(6) = 13$, and $D[9 \ldots 13] = 1, 2, 3, 2, 1$ has its leftmost minimum at $w = 9$. The match of the ")" at 9 is the "(" at 2, and $\mathrm{rank}_0(2) = 0 \ne 3$, so the answer is $\mathrm{rank}_0(9) = 4$: the minimum of $5, 1, 6, 3$ is at position 4.
- $\textsc{rmq}(1, 3)$: $x = 6$, $y = 8$, $D = 2, 3, 2$, so $w = 6$; its match is at 3, with $\mathrm{rank}_0(3) = 0 \ne 1$, so the answer is $\mathrm{rank}_0(6) = 2$.
- $\textsc{rmq}(2, 3)$: $x = y = 8$, so $w = 8$, whose match is at 7, and $\mathrm{rank}_0(7) = 2 = i$, so the answer is $i = 2$: node 2 is the parent of node 3, and $A[2] = 2 < A[3] = 5$.

## Correctness

Write $\mathrm{end}(v)$ for the position of the ")" that ends the description of node $v$. Three facts give the result. First, $D[\mathrm{end}(v)] = P(v)$, the number of nodes $u > v$ with $\mathrm{parent}(u) \le v$, and these are the strict prefix minima of $A[v + 1 \ldots n]$. Second, inside the description of a node $v$ the excess stays above $D[\mathrm{end}(v - 1)]$, so a leftmost minimum of $D[x \ldots y]$ is always at some $\mathrm{end}(v)$ with $i \le v \le j - 1$. Third, by the DFUDS layout, the ")" at $\mathrm{end}(u - 1)$ matches a "(" in the description of $\mathrm{parent}(u)$.

Now let $c'$ be the leftmost minimum of $A[i + 1 \ldots j]$. For $v < c' - 1$, the suffix $A[v + 1 \ldots n]$ has all the prefix minima of $A[c' \ldots n]$ and also $A[v + 1]$, so $P(v) > P(c' - 1)$. For $c' \le v \le j - 1$, the suffix still has every prefix minimum of $A[c' \ldots n]$ beyond $j$ and also $A[v + 1]$, so $P(v) \ge P(c' - 1)$. So line L6 returns $w = \mathrm{end}(c' - 1)$, and $\mathrm{rank}_0(w) = c'$. The items $A[i + 1 \ldots c' - 1]$ are all greater than $A[c']$, so $\mathrm{parent}(c') \le i$. If $\mathrm{parent}(c') = i$, then $A[i] \le A[c']$ and $i$ is the leftmost minimum of $A[i \ldots j]$, which line L7 detects through the third fact. Otherwise $A[i] > A[c']$, and line L8 returns $c'$. The [proof](proofs/correctness.md) writes this out, and the tests compare the implementation with a brute force on random arrays with many ties.

## Complexity

**Space.** $E$ has $2n + 2$ bits. Rank and select on a bit vector need $o(n)$ extra bits for $O(1)$ time, by the classic directories of Jacobson, Clark and Munro. The ±1 RMQ on $D$ uses the block method on blocks of $\Theta(\log n)$ bits, with a sparse table over $O(n / \log^2 n)$ superblocks and small tables of block shapes, in $o(n)$ bits, and open uses a similar directory. So the structure has $2n + o(n)$ bits, and $A$ can be discarded.

**Time.** The build is $O(n)$: the stack, one pass to write $E$, and linear-time directories. A query is a constant number of rank, select, open and ±1 RMQ operations, each $O(1)$.

**Lower bound.** Two arrays whose Cartesian trees differ in shape differ in the answer to some query, so an encoding must distinguish all $C_n = \frac{1}{n+1} \binom{2n}{n}$ shapes, the [Catalan numbers](/catalan-numbers/), which needs $\lg C_n = 2n - O(\log n)$ bits. The structure is optimal up to the $o(n)$ term.

The Python code builds the same $2n + 2$ bits and the same query, but uses simpler directories: rank samples per 64-bit word, a binary search for select, a sparse table over word minima, and a jump over this table for open. Its queries cost $O(\log n)$, and its directories take $O(n / 64 \cdot \log n)$ words.

## Properties

- **Encoding, not index.** The answers come without access to $A$; the minimum *value* needs $A$ or another structure.
- **Leftmost minima.** The tie rule $A[j] \le A[i]$ in the parent and a leftmost ±1 RMQ give the leftmost minimum.
- **Static.** A change of one item can change many parents.
- **Optimal space.** $2n + o(n)$ bits against a lower bound of $2n - O(\log n)$.

## Variants and improvements

- **Without open.** Grossi and Ottaviano replaced the test of line L7 by a comparison of two excess values, which avoids the slow parenthesis matching.
- **Balanced parentheses.** Ferrada and Navarro (2016) build the tree on the rightmost path and use the [balanced parentheses representation](/balanced-parentheses-representation/), where the query is $\mathrm{rank}_0(\pm 1\mathrm{RMQ}(\mathrm{select}_0(i), \mathrm{select}_0(j)))$ with no special case; with a [range min-max tree](/range-min-max-tree/) it uses a little more than $2n$ bits and is faster in practice.
- **Minimum and maximum.** Storing the 2d-Min-heap and the 2d-Max-heap answers both kinds of queries in $4n + o(n)$ bits.
- **Systematic structures.** If $A$ is kept, an index with $O(n / c)$ bits and query time $O(c)$ is possible, which trades space for array reads.
- **Not succinct but simple.** The plain Bender-Farach-Colton method uses $O(n)$ words, and a [sparse table](/sparse-table/) uses $n \lg n$ words.

## When to use it

Use it inside compressed text indexes, such as compressed [suffix arrays](/suffix-array/) and suffix trees, where range minima over the [LCP array](/lcp-array/) give longest common prefixes and tree navigation, and where $n$ is in the billions so that $O(n)$ words do not fit. Libraries such as SDSL provide it. For arrays that fit comfortably in memory, a sparse table over blocks is simpler and faster.

## Pitfalls

- **Ties.** With the parent rule $A[j] < A[i]$, equal items become siblings and the formula returns another minimum than the leftmost; the code here uses $A[j] \le A[i]$, which the random tests with many ties confirm.
- **The special case $i = j$.** Then $\mathrm{select}_0(i + 1) > \mathrm{select}_0(j)$, and the range of line L6 is empty.
- **Off by one in the preorder.** The ")" that ends node $v$ is the $(v + 1)$-st, because of the virtual root; the leading "(" makes the sequence balanced.
- **The leftmost ±1 RMQ.** The formula needs the leftmost minimum of $D$; a rightmost minimum gives wrong answers when the excess has ties.
- **The cost of open.** Parenthesis matching is the slowest operation in practice, which is why later variants avoid it.

## Implementations

## History

The reduction of range minima to lowest common ancestors through the Cartesian tree goes back to Gabow, Bentley and Tarjan (1984), and the constant-time solution with $O(n)$ words to Harel and Tarjan, with the simple version of Bender and Farach-Colton (2000). Sadakane gave a succinct structure for the special case of suffix trees, with one leaf per array entry. Fischer and Heun first presented the method at a conference in 2007 and published the journal version in 2011, giving the first $2n + o(n)$-bit encoding with $O(1)$ queries for any array; the DFUDS representation it uses is due to Benoit, Demaine, Munro, Raman, Raman and Rao (2005). Ferrada and Navarro (2016) simplified the query with balanced parentheses.

## References
