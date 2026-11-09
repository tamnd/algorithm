---
tag: R3V9R0
kind: algorithm
slug: zaks-tree-generation
name: Zaks' lexicographic generation of ordered trees
aliases:
- Zaks' algorithm
- Z-sequence generation
- Lexicographic generation of t-ary trees
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: Lists ordered trees with n nodes in lexicographic order of their Dyck word encodings.
solves: [binary-tree-generation, ordered-tree-generation]
model: word-ram
complexity:
  vars: {n: the number of internal nodes of the t-ary tree, t: the arity}
  time: {worst: Θ(n), best: Θ(1), amortized: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, recursive: false}
history:
  year: 1980
  people: [Shmuel Zaks]
  note: Zaks coded t-ary trees by the preorder positions of their internal nodes and gave the successor, ranking and unranking for this code.
prereqs: [dyck-word, binary-tree, lexicographic-order]
see_also: [next-balanced-bracket-sequence, binary-tree-generation, ordered-tree-generation, balanced-parentheses-generation, balanced-bracket-sequence-ranking, ranking-unranking, constant-amortized-time-generation, catalan-numbers]
sources:
  - paper: doi:10.1016/0304-3975(80)90073-0
    title: Shmuel Zaks, Lexicographic generation of ordered trees, Theoretical Computer Science 10(1) (1980), 63 to 82
    locator: the whole paper (the z-sequence code of t-ary trees, the generation in lexicographic order, ranking and unranking)
  - paper: doi:10.1137/0208006
    title: Shmuel Zaks and Dana Richards, Generating trees and other combinatorial objects lexicographically, SIAM Journal on Computing 8(1) (1979), 73 to 81
    locator: the whole paper (lexicographic generation of trees, including ordered forests with a given degree sequence)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.1, Binary Trees, Ordered Trees (tree sequences and Algorithm 4.16), and Section 4.14, Bibliographic Remarks (the references to Zaks and to Zaks and Richards)
---

Zaks' algorithm lists all $t$-ary trees with $n$ internal nodes in lexicographic order of their *z-sequences*. The z-sequence $z_1 < z_2 < \cdots < z_n$ gives the preorder positions of the internal nodes in the extended tree, and the valid sequences are exactly those with $z_i \le t(i-1) + 1$. For $t = 2$ these are the binary trees with $n$ nodes, which are the ordered trees with $n + 1$ nodes, and the order is the lexicographic order of their [Dyck words](/dyck-word/). The successor rule changes a suffix, so one step costs $\Theta(n)$ in the worst case, but over the whole list the scan reads at most $2$ entries per tree on average, which is constant amortized time.

## In plain words

Draw the tree with all its empty child places as small leaves. Walk the tree in preorder, and number the nodes in the order you meet them. Write down the numbers of the real nodes. This list of numbers is the code of the tree.

A list of numbers is a code exactly when it starts at 1, goes up, and the $i$-th number is not too large. The bound grows by $t$ at each step. To get the next tree, find the last number that can still grow, add one to it, and make every number after it as small as possible. That is the same as an odometer whose digits have different upper limits. Most steps change only the last number.

## The problem

Fix $t \ge 2$. A $t$-ary tree is empty, or it is a root with an ordered list of $t$ subtrees that are $t$-ary trees. In the *extended* tree, every empty subtree is drawn as a leaf, so a tree with $n$ internal nodes has $(t - 1)n + 1$ leaves and $tn + 1$ nodes in total. Number the nodes $1, \ldots, tn + 1$ in preorder. The *z-sequence* of the tree is the increasing list $z_1 < \cdots < z_n$ of the numbers of the internal nodes.

**Input:** $n \ge 0$ and $t \ge 2$, or one z-sequence.

**Output:** all z-sequences of length $n$ in lexicographic order, or the next one after the given sequence.

There are $\frac{1}{(t-1)n + 1}\binom{tn}{n}$ such trees. For $t = 2$ this is the [Catalan number](/catalan-numbers/) $C_n$. A binary tree with $n$ nodes is an ordered tree with $n + 1$ nodes by the first-child and next-sibling rule, and both give the same Dyck word of length $2n$: write $\texttt{(}$ for an internal node and $\texttt{)}$ for a leaf, in preorder, and drop the last leaf. So the same algorithm solves [binary tree generation](/binary-tree-generation/) and [ordered tree generation](/ordered-tree-generation/).

## The algorithm

The first sequence is $1, 2, \ldots, n$, the tree in which every internal node is the first child of the one before. The last is $z_i = t(i - 1) + 1$ for all $i$, in which every internal node is the last child of the one before.

```pseudo id=main
NEXT-Z(z[1 .. n], t)
L1  j ← n
L2  while j ≥ 1 and z[j] = t(j − 1) + 1 do j ← j − 1
L3  if j = 0 then return LAST
L4  z[j] ← z[j] + 1
L5  for i ← j + 1 to n do z[i] ← z[i − 1] + 1
L6  return NEXT
```

Line L2 skips the suffix in which every entry is at its upper bound. Line L4 increases the last entry that can still grow, and line L5 writes the smallest increasing continuation. To list all trees, start with $z = (1, \ldots, n)$, visit $z$, and call NEXT-Z until it returns LAST. The sequence is changed in place.

## Example

All $C_4 = 14$ binary trees with $4$ nodes, in the order that NEXT-Z produces. The bound on $z_i$ is $1, 3, 5, 7$. The column $r$ is the number of entries that line L2 skips, and $j$ is the entry that line L4 increases.

| z-sequence | extended preorder | Dyck word | $r$ | $j$ |
|---|---|---|---|---|
| 1 2 3 4 | 111100000 | `(((())))` | 0 | 4 |
| 1 2 3 5 | 111010000 | `((()()))` | 0 | 4 |
| 1 2 3 6 | 111001000 | `((())())` | 0 | 4 |
| 1 2 3 7 | 111000100 | `((()))()` | 1 | 3 |
| 1 2 4 5 | 110110000 | `(()(()))` | 0 | 4 |
| 1 2 4 6 | 110101000 | `(()()())` | 0 | 4 |
| 1 2 4 7 | 110100100 | `(()())()` | 1 | 3 |
| 1 2 5 6 | 110011000 | `(())(())` | 0 | 4 |
| 1 2 5 7 | 110010100 | `(())()()` | 2 | 2 |
| 1 3 4 5 | 101110000 | `()((()))` | 0 | 4 |
| 1 3 4 6 | 101101000 | `()(()())` | 0 | 4 |
| 1 3 4 7 | 101100100 | `()(())()` | 1 | 3 |
| 1 3 5 6 | 101011000 | `()()(())` | 0 | 4 |
| 1 3 5 7 | 101010100 | `()()()()` | 4 | LAST |

The Dyck words are in lexicographic order with $\texttt{(} < \texttt{)}$. The sum of the column $r$ is $9 = C_0 + C_1 + C_2 + C_3$, less than $14$. For $t = 3$ and $n = 3$ the bounds are $1, 4, 7$, and the $12$ sequences run from $1\,2\,3$ to $1\,4\,7$.

## Correctness

A word of $tn + 1$ symbols, with $n$ internal nodes and the rest leaves, is the preorder word of an extended $t$-ary tree exactly when a counter of open child places, which starts at $1$, gains $t - 1$ at each internal node and loses $1$ at each leaf, stays positive until the last symbol. The counter is smallest just before each internal node, and just before the $i$-th internal node it equals $t(i - 1) + 2 - z_i$. So the valid z-sequences are exactly the increasing sequences with $z_i \le t(i - 1) + 1$.

On this set, the entries after position $j$ in line L2 are at their bounds, so no sequence that is larger than $z$ can differ from $z$ first after position $j$. Every larger sequence is therefore at least the sequence that lines L4 and L5 write, which is valid and larger than $z$. So NEXT-Z returns the lexicographic successor, and the list starts at the smallest sequence and stops at the largest. A smaller $z_k$ puts an internal node, $\texttt{(}$, where the other word has a leaf, $\texttt{)}$, so the order of z-sequences is the order of the Dyck words. The full proof, with the amortized bound, is below.

## Complexity

- **One step.** Line L2 reads $r + 1$ entries, where $r$ is the length of the suffix at its bounds, and line L5 writes $r$ entries. So one call costs $\Theta(r + 1)$: $\Theta(1)$ in the best case and $\Theta(n)$ in the worst case, for example at the last sequence.
- **The whole list.** Let $F_m$ be the number of sequences of length $m$. The sequences with $r \ge k$ are a valid sequence of length $n - k$ followed by the bounds, so $\sum_z r = F_0 + F_1 + \cdots + F_{n-1}$. Since $F_{m+1} \ge 2F_m$ for $m \ge 1$, this sum is at most $F_n$. So the average of $r$ over all trees is at most $1$, and the listing runs in constant amortized time. For $t = 2$ and $n = 12$ the average is $0.40$.
- **Space.** The array $z$ of $n$ entries, changed in place, and $O(1)$ more. The output is visited in place; copying each tree out costs $\Theta(n)$ per tree.

## Properties

- **In place.** The algorithm keeps no state except the current sequence, so it can restart from any tree.
- **Lexicographic.** The order of z-sequences equals the lexicographic order of the preorder words with internal node before leaf, and for $t = 2$ the order of the Dyck words with $\texttt{(} < \texttt{)}$.
- **Same order as the bracket successor.** For $t = 2$, NEXT-Z lists the trees in the same order as the [next balanced bracket sequence](/next-balanced-bracket-sequence/) algorithm, but it stores $n$ numbers instead of $2n$ brackets.
- **Mixed-radix view.** The sequence $(z_i - i)$ is a non-decreasing sequence with $z_i - i \le (t - 1)(i - 1)$, so NEXT-Z is an odometer on a lower set of a staircase.
- **Not a Gray code.** One step can change $n - 1$ entries, for example from $1\,2\,5\,7$ to $1\,3\,4\,5$.

## Variants and improvements

- **Ranking and unranking.** The number of valid completions of a prefix $z_1, \ldots, z_k$ depends only on $k$ and $z_k$, and it is a ballot-type number. Summing these numbers over the smaller choices at each position ranks a tree in $O(tn)$ arithmetic operations after a table of $O(tn^2)$ numbers; reversing the sum unranks. See [ranking and unranking](/ranking-unranking/) and [balanced bracket sequence ranking](/balanced-bracket-sequence-ranking/).
- **Other codes.** The same successor rule works on any code given by an increasing sequence with a bound on each entry. Zaks and Richards used such codes for trees with given degree conditions.
- **Reverse order.** Decrease the last entry that is larger than its predecessor plus one, and set the suffix to the bounds, to list the trees from the last to the first.
- **Gray codes.** If consecutive trees must differ by one rotation, use the rotation Gray code for binary trees, which runs in constant amortized time and has a loopless version; see [binary tree generation](/binary-tree-generation/).

## When to use it

Use Zaks' algorithm when you need all binary, ordered or $t$-ary trees of one size in a fixed, well-known order, when ranks must match the order of the list, or when a compact code of $n$ integers is convenient. If you need the Dyck word itself, the [bracket successor](/next-balanced-bracket-sequence/) gives the same order without a conversion. If you need small changes between consecutive trees, use a Gray code.

## Pitfalls

- **Off-by-one in the bound.** With 1-based positions the bound is $t(i - 1) + 1$; with 0-based positions it is $t \cdot i$. Mixing the two lists sequences that are not trees.
- **Counting the root.** The extended tree has $tn + 1$ nodes, and $z_1 = 1$ is always the root. The ordered tree that matches a binary tree with $n$ nodes has $n + 1$ nodes, one more than the length of the sequence.
- **Empty tree.** For $n = 0$ the only sequence is the empty one, and NEXT-Z returns LAST at once.
- **Worst-case latency.** One step can cost $\Theta(n)$. If every step must be fast, use a loopless Gray code.

## Implementations

## History

Zaks published the z-sequence code and its lexicographic generation, ranking and unranking for $t$-ary trees in 1980. A year before, Zaks and Richards had generated trees and other objects lexicographically, including ordered forests with a given degree sequence. Ruskey's book develops the lexicographic listing of the bitstring code of binary trees and cites both papers among the many methods for generating binary trees.

## References
