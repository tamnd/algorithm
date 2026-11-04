---
tag: SD1PX6
kind: data-structure
slug: fusion-tree
name: Fusion tree
aliases:
- Fredman-Willard fusion tree
area: data-structures/search-trees
level: research
summary: Integer search tree achieving O(log n / log w) time per operation on w-bit words using word-parallel tricks.
model: word-ram
complexity:
  vars: {n: the number of keys, w: the number of bits in a word}
  time: {worst: O(log n / log w)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [predecessor-problem, b-tree, word-ram, bit-parallelism]
see_also: [floor-and-ceiling-in-ordered-set, predecessor-lower-bound, integer-sorting, bitwise-operations, trie, b-tree, cell-probe-model, sorted-search-lower-bound]
sources:
  - paper: doi:10.1016/0022-0000(93)90040-4
    title: Michael L. Fredman and Dan E. Willard, Surpassing the information theoretic bound with fusion trees, Journal of Computer and System Sciences 47(3), 1993
    locator: pages 424 to 436
  - paper: doi:10.1145/1132516.1132551
    title: Mihai Pătraşcu and Mikkel Thorup, Time-space trade-offs for predecessor search, STOC 2006
    locator: the whole paper, for the optimality of the fusion tree bound in some ranges of n and w
---

A fusion tree is a [B-tree](/b-tree/) for $w$-bit integer keys on the [word RAM](/word-ram/) whose nodes hold $B = w^{\Theta(1)}$ keys each and find the rank of a query among those keys in $O(1)$ time, by compressing the keys into short *sketches* and comparing all the sketches with one word operation. A search visits $O(\log_B n) = O(\log n / \log w)$ nodes, so it answers [predecessor queries](/predecessor-problem/) in $O(\log n / \log w)$ time with $O(n)$ space. Fredman and Willard introduced it in 1993, and it was the first structure to beat the $\Theta(\log n)$ bound of comparison-based search for all word sizes. With $w \ge \lg n$, the bound is $O(\log n / \log \log n)$.

## In plain words

A search tree with two children per node needs about $\log_2 n$ steps. A tree with $B$ children per node needs only $\log_B n$ steps, but each step must find the right child among $B$ keys, which normally costs more.

A fusion tree makes that step cheap. Among a few keys, only a few bit positions matter to tell them apart. The tree keeps just those bits of each key, a short *sketch*. All the sketches of one node fit in a single machine word, and one subtraction compares the query with all of them at once. A small correction step then turns this into the exact answer.

## The abstract type

The static fusion tree on this page stores a fixed set $S$ of $n$ distinct integers in $\{0, \ldots, 2^w - 1\}$ and answers $\mathrm{pred}(q)$, the largest key $\le q$, and $\mathrm{succ}(q)$, the smallest key $\ge q$. It is a solution of the static [predecessor problem](/predecessor-problem/). Dynamic versions are discussed under Variants.

## Representation

The tree is a B-tree in which each node has $k \le B$ keys $x_0 < \cdots < x_{k-1}$ and $k + 1$ children $c_0, \ldots, c_k$, with the keys of $c_j$ between $x_{j-1}$ and $x_j$. For $B$ keys per node to fit in one word as sketches, $B^2 \le w$ here (the original uses $B = w^{1/5}$).

**Distinguishing positions.** For the keys of a node, let $D$ be the set of positions $\mathrm{msb}(x_j \oplus x_{j+1})$ for $0 \le j < k - 1$, where $\oplus$ is bitwise exclusive or and $\mathrm{msb}$ is the position of the highest set bit. These are the levels where the binary [trie](/trie/) of the keys branches. So $r = |D| \le k - 1$.

**Sketch.** For any $w$-bit $z$, $\mathrm{sketch}(z)$ is the $r$-bit number formed by the bits of $z$ at the positions of $D$, from high to low. The sketches of the keys of a node are in the same order as the keys.

**Packed word.** The node stores the word $K = \sum_j (2^r + \mathrm{sketch}(x_j)) \cdot 2^{j(r+1)}$: field $j$ has $r + 1$ bits, a *sentinel* 1 on top of the sketch of $x_j$. It also stores $M = \sum_j 2^{j(r+1)}$ and the mask $H = 2^r M$ of the sentinel bits. The fields take $k(r+1) \le B^2 \le w$ bits.

**Invariant.** (U1) The node keys are increasing, and the keys below $c_j$ lie between $x_{j-1}$ and $x_j$. (U2) $D$, $K$, $M$ and $H$ are as defined from the node keys.

## Operations

```pseudo id=main
NODE-PRED(v, q)                ▷ index of the largest key of v that is ≤ q, or −1
L1  s ← SKETCH(v, q)
L2  i ← PACKED-RANK(v, s)      ▷ the number of keys of v with sketch < s
L3  y ← the one of x_{i−1}, x_i that has the longer common prefix with q
L4  if y = q then return i
L5  p ← MSB(q ⊕ y)             ▷ q leaves the trie of the keys at bit p
L6  if bit p of q is 1 then e ← (q's bits above p) 0 1…1; return PACKED-RANK(v, SKETCH(v, e) + 1) − 1
L7  else e ← (q's bits above p) 1 0…0; return PACKED-RANK(v, SKETCH(v, e)) − 1
L8  ▷ both lines return the rank of e minus 1, which is the index of the predecessor

PACKED-RANK(v, s)              ▷ for 0 ≤ s ≤ 2^r
L9  Q ← s · M                  ▷ s copied into each field
L10 T ← (K − Q) AND H          ▷ field j keeps its sentinel exactly when sketch(x_j) ≥ s
L11 return k − POPCOUNT(T)

PRED(T, q)
L12 v ← T.root; best ← NIL
L13 while v ≠ NIL do
L14     j ← NODE-PRED(v, q)
L15     if j ≥ 0 and x_j = q then return q
L16     if j ≥ 0 then best ← x_j
L17     v ← c_{j+1}            ▷ the child between x_j and x_{j+1}
L18 return best
```

**Packed rank.** Each field of $K - Q$ is $2^r + \mathrm{sketch}(x_j) - s$, which is between 0 and $2^{r+1} - 1$, so no borrow crosses a field. Its top bit is 1 exactly when $\mathrm{sketch}(x_j) \ge s$. So $k$ minus the number of surviving sentinels is the number of keys with a smaller sketch.

**Why the correction.** The rank of $\mathrm{sketch}(q)$ is not always the rank of $q$: bits of $q$ outside $D$ are ignored. But the sketch neighbours of $q$ contain a key $y$ with the longest common prefix with $q$ (Lemma 4 of the proof). From $y$ the position $p$ where $q$ leaves the trie is known. If $q$ goes right there, $q$ is larger than each key with the same prefix, and the answer is the largest of those keys, the rank of $e = $ prefix, 0, then all ones. If $q$ goes left, $q$ is smaller than each of them, and the answer is the key just before them, from the rank of $e = $ prefix, 1, then all zeros. For these special $e$, the sketch rank is exact.

**Successor.** The same walk, with $\mathrm{succ}(q) = x_{j+1}$ at the node where $q$ is not a key, and the best such candidate on the path.

## Example

A node with the 5-bit keys 2, 9, 12 and 26:

| key | binary | bits at 4, 3, 2 | sketch |
|---|---|---|---|
| 2 | 00010 | 0 0 0 | 0 |
| 9 | 01001 | 0 1 0 | 2 |
| 12 | 01100 | 0 1 1 | 3 |
| 26 | 11010 | 1 1 0 | 6 |

The positions come from $\mathrm{msb}(2 \oplus 9) = \mathrm{msb}(01011) = 3$, $\mathrm{msb}(9 \oplus 12) = 2$ and $\mathrm{msb}(12 \oplus 26) = 4$, so $D = \{4, 3, 2\}$ and $r = 3$. The fields have 4 bits, and the field values $8 + \mathrm{sketch}$ are 8, 10, 11 and 14.

**Query $q = 13 = 01101$.** Its sketch is $011 = 3$. Packed rank: subtracting 3 from each field gives 5, 7, 8 and 11; the sentinels (value $\ge 8$) survive in two fields, so $i = 4 - 2 = 2$. The sketch rank alone would say that the predecessor is $x_1 = 9$, which is wrong. The neighbours are $x_1 = 9$ and $x_2 = 12$; $13 \oplus 9 = 00100$ and $13 \oplus 12 = 00001$, so $y = 12$ and $p = 0$. Bit 0 of 13 is 1, so $e = 01100 = 12$ with sketch 3, and the number of sketches $\le 3$ is 3. The predecessor is $x_2 = 12$, which is right.

**Query $q = 21 = 10101$.** The sketch is $101 = 5$, $i = 3$, and the neighbours are 12 and 26; $21 \oplus 26 = 01111$ has a lower top bit than $21 \oplus 12 = 11001$, so $y = 26$ and $p = 3$. Bit 3 of 21 is 0, so $e = 11000 = 24$ with sketch $110 = 6$; three sketches are $< 6$, and the predecessor is $x_2 = 12$.

## Correctness

Sketches keep the order of the node keys because two keys first differ at a position of $D$. A query $q$ and a key $x$ compare correctly by sketch whenever they first differ at a position of $D$. Each key outside the block of keys that share the longest prefix with $q$ first differs from $q$ above $p$, at a position of $D$, so the sketch order puts that block exactly at the place of $q$, which proves that a sketch neighbour is in the block. For $e$, all keys outside the block compare correctly, and the keys in the block are all on one side of $e$ in value and in sketch, which gives the exact rank. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The tree has height $O(\log_{B+1} n)$. With $B = w^{1/5}$, as in Fredman and Willard, this is $O(\log n / \log w)$.

**Per node.** PACKED-RANK costs one multiplication, one subtraction, one AND and one population count. The population count of the sentinels can itself be done by one more multiplication by $M$ and a shift, which adds the sentinel bits into one field. MSB of a word takes $O(1)$ time on the word RAM with multiplication, by another method of Fredman and Willard. The sketch is the hard part: gathering $r$ scattered bits into a contiguous field in $O(1)$ time is not a standard operation. Fredman and Willard compute an *approximate* sketch with one multiplication by a carefully chosen constant, which puts the needed bits at known positions, spread over $O(r^4)$ bits; this is why they need $B^5 \le w$. The Python code computes the exact sketch with a loop over $D$, which takes $O(B)$ time instead of $O(1)$.

| operation | this implementation | fusion tree with multiplication |
|---|---|---|
| predecessor, successor | $O(B \log_B n)$ | $O(\log n / \log w)$ |
| build from sorted keys | $O(n B)$ | $O(n)$ plus the cost of the node constants |
| space | $O(n)$ words | $O(n)$ words |

**Comparison.** For $w = 64$ and $n = 10^5$ keys with $B = 8$, the tree has 5 levels, where a balanced binary tree has 17.

## Variants

- **Dynamic fusion trees.** Fredman and Willard also support inserts and deletes, with amortized bounds, by rebuilding a node's constants after enough changes. Pătraşcu and Thorup (2014) gave a dynamic fusion tree with $O(\log n / \log w)$ time per operation, including rank and select.
- **Exponential search trees.** Andersson and Thorup combine fusion nodes of growing degree into a tree with $O(\sqrt{\log n / \log \log n})$ time per operation, for any $w$.
- **Fusion nodes in other structures.** A fusion node is a constant-time rank structure for $w^{\Theta(1)}$ keys. It is used inside integer [priority queues](/priority-queue/), [integer sorting](/integer-sorting/) algorithms, and the atomic heap of Fredman and Willard.
- **AC0 versions.** Later work replaces the multiplications by operations that are cheaper in hardware.
- **Combined with van Emde Boas.** Using a van Emde Boas tree when $\log w < \sqrt{\log n}$ and a fusion tree otherwise gives $O(\sqrt{\log n})$ for each $n$ and $w$.

## When to use it

Fusion trees are mainly a theoretical tool: they show that integer search is easier than comparison search, and they are a part of fast integer sorting and of the [predecessor bounds](/predecessor-lower-bound/). In practice the constants of the multiplication sketches are large, and $B = w^{1/5}$ is only 2 for $w = 64$. Practical structures use the same ideas in a simpler form: SIMD comparison of a query with a node of keys, as in cache-friendly B-trees, is a packed comparison of full keys.

## Pitfalls

- **Using the sketch rank as the answer.** It can be wrong, as the query 13 above shows. The correction of lines L3 to L7 is needed.
- **Borrows between fields.** Without the sentinel bit, a field with $\mathrm{sketch}(x_j) < s$ would borrow from the next field and spoil its result. The sentinel absorbs the borrow.
- **Strict and non-strict counts.** Line L6 counts sketches $\le \mathrm{sketch}(e)$ (by asking for $< \mathrm{sketch}(e) + 1$), and line L7 counts sketches $< \mathrm{sketch}(e)$. Swapping them gives off-by-one errors exactly when a key's sketch equals the sketch of $e$.
- **Choosing $y$ by sketch.** The key with the longest common prefix is found by the real keys, comparing $q \oplus x_{i-1}$ and $q \oplus x_i$ as numbers; the sketches do not tell which neighbour is closer.
- **Word size.** All fields of a node must fit in one word. With exact sketches this means $k(r + 1) \le w$; the code checks $B^2 \le w$.

## Implementations

The Python class builds a static tree from a list of keys, with parameters $w$ and $B$. Each node stores its positions, the packed word and the masks, and `node_pred` follows lines L1 to L8 with Python integers as words; the population count is `bin(t).count("1")`. The tests compare predecessor and successor with `bisect` on random sets, including clustered keys that share long prefixes, and check the example above.

## History

Fredman and Willard presented fusion trees at STOC 1990, with the journal version in 1993. They used them to sort $n$ integers in $O(n \log n / \log \log n)$ time and to answer predecessor queries in $O(\log n / \log \log n)$ time, the first results to beat the information-theoretic bound of comparison sorting and searching on the word RAM. Pătraşcu and Thorup (2006) later showed that the bound $O(\log_w n)$ is optimal for predecessor search with near-linear space when $w$ is large compared to $\log n$.

## References
