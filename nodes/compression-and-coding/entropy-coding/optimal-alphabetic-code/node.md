---
tag: GS71SB
kind: problem
slug: optimal-alphabetic-code
name: Optimal alphabetic code problem
aliases:
- optimal alphabetic binary tree
- alphabetic prefix code
- optimal alphabetic tree problem
area: compression-and-coding/entropy-coding
level: advanced
summary: Find a prefix code of least weighted length whose codewords keep a given order of the symbols. Interval DP with Knuth's speedup solves it in O(n^2); Hu-Tucker and Garsia-Wachs in O(n log n).
prereqs: [optimal-prefix-code, interval-dp]
see_also: [hu-tucker-algorithm, garsia-wachs-algorithm, gilbert-moore-code, optimal-binary-search-tree, huffman-coding, length-limited-prefix-code]
sources:
  - paper: doi:10.1002/j.1538-7305.1959.tb01583.x
    title: Edgar N. Gilbert and Edward F. Moore, Variable-length binary encodings, Bell System Technical Journal 38(4), 1959
    locator: pages 933 to 967 (alphabetic codes and the O(n^3) program)
  - paper: doi:10.1007/bf00264289
    title: Donald E. Knuth, Optimum binary search trees, Acta Informatica 1(1), 1971
    locator: pages 14 to 25 (the monotone roots and O(n^2) time)
  - paper: doi:10.1145/800141.804691
    title: F. Frances Yao, Efficient dynamic programming using quadrangle inequalities, Proceedings of the 12th ACM Symposium on Theory of Computing, 1980
    locator: pages 429 to 435
  - paper: doi:10.1137/0121057
    title: T. C. Hu and A. C. Tucker, Optimal computer search trees and variable-length alphabetical codes, SIAM Journal on Applied Mathematics 21(4), 1971
    locator: pages 514 to 532
  - paper: doi:10.1137/0206045
    title: Adriano M. Garsia and Michelle L. Wachs, A new algorithm for minimum cost binary trees, SIAM Journal on Computing 6(4), 1977
    locator: pages 622 to 642
  - paper: doi:10.1016/S0304-3975(96)00296-4
    title: Marek Karpinski, Lawrence L. Larmore and Wojciech Rytter, Correctness of constructing optimal alphabetic trees revisited, Theoretical Computer Science 180, 1997
    locator: pages 309 to 324
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2, Binary tree searching (optimum binary search trees and the Hu-Tucker and Garsia-Wachs algorithms)
---

The optimal alphabetic code problem asks for a [prefix code](/prefix-code/) of least weighted length among the codes whose codewords keep a given order of the symbols. Equivalently, it asks for a binary tree with the symbols at the leaves, in the given order from left to right, that minimizes the weighted sum of the leaf depths. Without the order this is the [optimal prefix code problem](/optimal-prefix-code/), which Huffman's algorithm solves; with the order, Huffman's greedy merge of the two lightest weights no longer works, because the two lightest symbols may be far apart. It is the [optimal binary search tree](/optimal-binary-search-tree/) problem with weights only on the leaves. An [interval dynamic program](/interval-dp/) solves it in $O(n^3)$ time, Knuth's rule cuts this to $O(n^2)$, and the [Hu-Tucker](/hu-tucker-algorithm/) and [Garsia-Wachs](/garsia-wachs-algorithm/) algorithms take $O(n \log n)$.

## In plain words

You have a list of words in alphabetical order, and you know how often each one is used. You want to give each word a string of bits, with two rules: no string starts another one, and the strings sort in the same order as the words. Among all such codes, find the one that uses the fewest bits on average.

Without the second rule, the answer is a Huffman code. The order rule makes it harder, because the two rarest words may sit at opposite ends of the list, and Huffman's trick of joining the two rarest no longer gives an ordered result.

The same question appears in searching. Put the words in the gaps of a sorted table and ask how to arrange the comparisons so that the expected number of them is least.

## Definition

**Input.** Positive weights $w_1, \ldots, w_n$ for symbols $1, \ldots, n$ in a fixed order. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area.

**Output.** A full binary tree whose leaves, read from left to right, are the symbols $1, \ldots, n$, or the equivalent alphabetic code: the codeword of a leaf is its path, 0 for left and 1 for right.

**Objective.** Minimize $\sum_i w_i d_i$, where $d_i$ is the depth of leaf $i$, that is the length of its codeword.

A code is *alphabetic* when $i < j$ implies that codeword $i$ comes before codeword $j$ in lexicographic order. An alphabetic prefix code is the same as the leaves of a binary tree in the given order. An optimal one is a full tree, since an inner node with one child can be removed. So the problem is to choose, among the full binary trees with $n$ leaves in a fixed order, the one of least weighted external path length.

## Variants

- **Optimal binary search trees.** Knuth's problem puts weights on the $n - 1$ keys as well as on the $n$ gaps between them; the cost counts a key at its depth plus one and a gap at its depth. Setting all key weights to zero gives the alphabetic problem.
- **Length-limited alphabetic codes.** Codewords of at most $L$ bits, as for [length-limited prefix codes](/length-limited-prefix-code/).
- **Other cost functions.** Hu, Kleitman and Tamaki (1979) studied a family of cost functions, besides the weighted sum, for which methods of the Hu-Tucker kind still find an optimal tree.
- **$t$-ary alphabetic trees.** Each inner node has up to $t$ children; the interval program still works.
- **Approximate codes.** The [Gilbert-Moore code](/gilbert-moore-code/) gives an alphabetic code with $L < H + 2$ in linear time, without optimality.

## Examples

**The order has a price.** For weights 1, 10, 1 in this order, any alphabetic tree puts the heavy middle symbol at depth 2, for a cost of 23. A Huffman code gives it depth 1, for a cost of 14.

**The interval program at work.** Take symbols A to E with weights 4, 1, 6, 2, 3. The table lists the least cost $c$ of each run of symbols and its best split, the last symbol of the left subtree.

| run | weight | split costs, for each split point | least cost | best split |
|---|---|---|---|---|
| A B | 5 | 0 | 5 | after A |
| B C | 7 | 0 | 7 | after B |
| C D | 8 | 0 | 8 | after C |
| D E | 5 | 0 | 5 | after D |
| A B C | 11 | 7, 5 | 16 | after B |
| B C D | 9 | 8, 7 | 16 | after C |
| C D E | 11 | 5, 8 | 16 | after C |
| A B C D | 13 | 16, 13, 16 | 26 | after B |
| B C D E | 12 | 16, 12, 16 | 24 | after C |
| A B C D E | 16 | 24, 21, 21, 26 | 37 | after B |

The split costs are $c(\text{left run}) + c(\text{right run})$, and the least cost is the run's weight plus the smallest of them. The optimal tree splits A B C D E after B, then C D E after C. The depths are 2, 2, 2, 3, 3, the codewords 00, 01, 10, 110, 111, and the cost 37. A Huffman code costs 35. A best split never moves left when a run gains a symbol at its right end, nor when it loses a symbol at its left end; this is the property behind Knuth's speedup.

## Known algorithms

| algorithm | time | space | note |
|---|---|---|---|
| Interval program (Gilbert and Moore 1959) | $O(n^3)$ | $O(n^2)$ | Try every split point of every run. |
| Knuth's speedup (1971) | $O(n^2)$ | $O(n^2)$ | Search the best split of $(i, j)$ only between those of $(i, j - 1)$ and $(i + 1, j)$. |
| [Hu-Tucker algorithm](/hu-tucker-algorithm/) (1971) | $O(n \log n)$ | $O(n)$ | Combine the lightest compatible pair, assign levels, rebuild. $O(n^2)$ in its simple form. |
| [Garsia-Wachs algorithm](/garsia-wachs-algorithm/) (1977) | $O(n \log n)$ | $O(n)$ | Combine the first pair with $w_{i-1} \le w_{i+1}$, move it left, rebuild. $O(n^2)$ in its simple form. |
| [Gilbert-Moore code](/gilbert-moore-code/) | $O(n)$ | $O(1)$ | Not optimal; $L < H + 2$. |

**Why Knuth's speedup applies.** Write $c(i, j) = W(i, j) + \min_{i \le k < j} (c(i, k) + c(k + 1, j))$, with $W(i, j) = w_i + \cdots + w_j$. Knuth (1971) proved that the best root of an optimal binary search tree is monotone, $R(i, j - 1) \le R(i, j) \le R(i + 1, j)$, for any nonnegative key and gap weights; the alphabetic problem is the case of zero key weights. Yao (1980) gave the general reason: the recurrence has this property whenever $W$ satisfies the quadrangle inequality $W(i, j) + W(i', j') \le W(i', j) + W(i, j')$ for $i \le i' \le j \le j'$ and is monotone under inclusion. Here $W$ is a sum over an interval, so the quadrangle inequality holds with equality, and $W$ grows with the interval because the weights are positive. With the range of splits limited this way, the work for all runs of one length telescopes to $O(n)$, and the total is $O(n^2)$.

## Bounds

- **Entropy.** With $p_i = w_i / \sum_j w_j$ and $H$ the [entropy](/shannon-entropy/), the mean length $L$ of an optimal alphabetic code satisfies $H \le L < H + 2$. The lower bound holds for every prefix code; the upper bound follows from the Gilbert-Moore code.
- **Against Huffman.** An optimal alphabetic code is never shorter than a Huffman code for the same weights, and is equal to it when the weights are sorted, since then a Huffman tree can be drawn with the leaves in order. The gap can be large in absolute terms, as the example 1, 10, 1 shows, but it is less than 2 bits per symbol on average because of the entropy bounds.
- **Time.** Any algorithm must read all $n$ weights, so $\Omega(n)$ time is needed. The known exact algorithms take $O(n \log n)$ time.

## Reductions

- **To optimal binary search trees.** An alphabetic tree on $n$ leaves is a search tree on $n - 1$ keys whose gaps are the leaves. With all key weights set to zero, the costs agree, so any algorithm for optimal search trees solves the alphabetic problem. The converse does not hold: Hu-Tucker and Garsia-Wachs need the key weights to be zero.
- **Optimal merging in a line.** Merging $n$ piles in a row, where only neighbouring piles can be merged and each merge costs the total size of the two piles, is the same problem: each pile is charged once for each merge it takes part in, which is its depth in the merge tree.
- **To depths.** Hu-Tucker and Garsia-Wachs both reduce the problem to finding the depths of the leaves in an optimal tree. Given depths that some alphabetic tree realizes, a stack builds that tree in $O(n)$ time.
- **From the unordered problem.** When the weights are sorted, an optimal alphabetic code is an optimal prefix code.

## Applications

- **Search in sorted tables.** When the probabilities of the gaps of a sorted table are known, an optimal alphabetic tree is a comparison tree of least expected cost for unsuccessful searches, or for searches that only need the gap.
- **Order-preserving compression.** Codes that keep the order let compressed keys in a sorted index be compared, and range queries be answered, without decoding.
- **Merging of runs in a fixed order.** Merging sorted runs that must stay in place, such as neighbouring blocks of a file, at the least total cost.

## References
