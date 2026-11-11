---
tag: E86180
kind: algorithm
slug: adaptive-huffman-coding
name: Adaptive Huffman coding
aliases:
- FGK algorithm
- Vitter algorithm
- dynamic Huffman coding
- one-pass Huffman coding
area: compression-and-coding/entropy-coding
level: advanced
summary: Encoder and decoder update the same Huffman tree after each symbol, so the code follows the counts so far and no table is sent. The update costs O(1) time per output bit.
solves: [optimal-prefix-code]
model: word-ram
complexity:
  vars: {n: the number of distinct symbols, t: the number of symbols in the message, b: the number of output bits}
  time: {worst: O(t + b), average: O(t + b)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1973
  people: [Newton Faller, Robert G. Gallager, Donald E. Knuth, Jeffrey Scott Vitter]
  note: Faller (1973) and Gallager (1978) found the method on their own, Knuth (1985) made it efficient, and Vitter (1987) gave an improved update with a better bound.
prereqs: [huffman-coding]
see_also: [canonical-huffman-code, adaptive-modeling, arithmetic-coding, optimal-prefix-code, context-modeling, prefix-code]
sources:
  - paper: "Newton Faller, An adaptive system for data compression, Record of the 7th Asilomar Conference on Circuits, Systems and Computers, 1973"
    locator: pages 593 to 597
  - paper: doi:10.1109/tit.1978.1055959
    title: Robert G. Gallager, Variations on a theme by Huffman, IEEE Transactions on Information Theory 24(6), 1978
    locator: pages 668 to 674 (the sibling property and the adaptive code)
  - paper: doi:10.1016/0196-6774(85)90036-7
    title: Donald E. Knuth, Dynamic Huffman coding, Journal of Algorithms 6(2), 1985
    locator: pages 163 to 180
  - paper: doi:10.1145/31846.42227
    title: Jeffrey Scott Vitter, Design and analysis of dynamic Huffman codes, Journal of the ACM 34(4), 1987
    locator: pages 825 to 845 (algorithm Lambda, the bound of fewer than t extra bits, and the analysis of FGK)
  - paper: "Jeffrey Scott Vitter, Algorithm 673: Dynamic Huffman coding, ACM Transactions on Mathematical Software 15(2), 1989"
    locator: pages 158 to 167
  - paper: doi:10.1145/3342555
    title: Alistair Moffat, Huffman coding, ACM Computing Surveys 52(4), 2019
    locator: Section 4.2, Dynamic Huffman coding
---

Adaptive Huffman coding codes a message in one pass. Encoder and decoder start with the same small tree and, after each symbol, both update it to a [Huffman tree](/huffman-coding/) for the counts seen so far. So the code follows the statistics of the message, and no code table is sent. The update rests on the sibling property of Gallager (1978): a code tree is a Huffman tree exactly when its nodes can be listed by weight with each node next to its sibling. Algorithm FGK (Faller 1973, Gallager 1978, Knuth 1985) restores this property in time proportional to the codeword length. Vitter's algorithm (1987) also keeps the tree as flat as possible and sends fewer than $S + t$ bits for a message of $t$ symbols, where $S$ is the cost of the two-pass Huffman code.

## In plain words

A normal Huffman coder reads the message twice, to count and then to code, and it must send the code. An adaptive coder reads it once. It keeps a Huffman tree for the counts it has seen so far. To send a symbol, it sends the path to the symbol's leaf with the current tree, and then it adds one to the count and repairs the tree. The decoder reads the path, finds the symbol, and makes the same repair, so both trees stay the same.

A symbol that has not been seen before has no leaf. A special leaf with count zero stands for all such symbols. The coder sends the path to this leaf and then the symbol in plain bits. The repair walks from the leaf up to the root and, at each node, swaps the node with the last node of the same count.

## The problem

The input is a message of $t$ symbols from an alphabet of size $n$, written $\sigma$ in the notation of this area, which is not known in advance in detail. The model is adaptive: the code for the next symbol depends only on the symbols before it, through their counts. The goal is to code the message in one pass, with no table, and with about as many bits as a two-pass static Huffman code for the counts of the whole message. This is the [optimal prefix code problem](/optimal-prefix-code/) solved again after each symbol, but with an update instead of a rebuild.

**The sibling property.** Number the nodes of a code tree with $2m + 1$ nodes from $0$ to $2m$, so that the root has the largest number and the nodes with numbers $2j$ and $2j + 1$ are siblings. The tree has the *sibling property* if the weights do not decrease as the number increases. Gallager (1978) showed that a tree is a Huffman tree for its leaf weights exactly when it has the sibling property. The update keeps this property, so the tree stays optimal for the counts so far.

**The NYT node.** The tree has one leaf of weight 0, the NYT node (not yet transmitted). It stands for all symbols not seen so far. At the start the tree is this one node.

## The algorithm

The main listing is algorithm FGK, as an encoder. The decoder runs the same loop: it walks down the tree with the input bits, reads 8 raw bits if it reaches the NYT node, and then makes the same update.

```pseudo id=main
FGK-ENCODE(message)                        ▷ the symbols are bytes
L1  T ← a tree with one node, NYT, of weight 0; the node numbers follow the sibling property
L2  for each symbol s of message do
L3      if s has a leaf in T then output the path from the root to leaf(s)
L4      else output the path to NYT, then the 8 bits of s; give NYT two children, a new NYT and a leaf for s, both of weight 0
L5      q ← leaf(s)
L6      while q ≠ NIL do
L7          b ← the node with the highest number among the nodes of weight w(q), other than parent(q)
L8          if b ≠ q then swap q and b in the tree, with their subtrees and their numbers
L9          w(q) ← w(q) + 1
L10         q ← parent(q)
```

Line L7 finds the *leader* of the block of nodes of weight $w(q)$. After the swap of line L8, all nodes with a higher number than $q$ have weight at least $w(q) + 1$, so line L9 keeps the weights in order. The swap itself keeps the order, since $q$ and $b$ have the same weight, and it keeps the sibling pairs, since only two places in the tree change their contents. The new leaf and the new NYT node of line L4 get the two smallest numbers.

**Vitter's algorithm.** Vitter (1987) numbers the nodes in level order, from the bottom level up and from left to right in each level, and keeps a stronger invariant: for each weight $w$, the leaves of weight $w$ come before the inner nodes of weight $w$. The update moves a node with a *slide* instead of a swap.

```pseudo id=vitter
VITTER-UPDATE(s)
V1  if s is new then split NYT as in line L4; q ← the old NYT node; inc ← leaf(s)
V2  else q ← leaf(s); swap q with the leader of its block, the leaf of weight w(q) with the highest number
V3      if q is the sibling of NYT then inc ← q; q ← parent(q) else inc ← NIL
V4  while q ≠ NIL do q ← SLIDE-AND-INCREMENT(q)
V5  if inc ≠ NIL then SLIDE-AND-INCREMENT(inc)

SLIDE-AND-INCREMENT(p)
S1  B ← the run of nodes just above p in number order that are inner nodes of weight w(p) if p is a leaf, or leaves of weight w(p) + 1 if p is an inner node
S2  a ← parent(p)
S3  move p to the place of the highest node of B; each node of B moves one place down
S4  w(p) ← w(p) + 1
S5  if p is a leaf then return the new parent(p) else return a
```

The special case of line V3 exists because the sibling of the NYT node has the same weight as its parent. A slide of the leaf over the inner nodes of its weight could then pass its own parent, so the parent goes first.

## Example

Encode the message abracadabra with FGK. The column "sent" shows the path bits; "+x" stands for the 8 raw bits of letter x after the NYT path. In the trees, a pair in parentheses is an inner node, written with its weight after it, and the left child gets the bit 0.

| step | symbol | sent | tree after the update |
|---|---|---|---|
| 1 | a | (empty) +a | (NYT0 a1)1 |
| 2 | b | 0 +b | ((NYT0 b1)1 a1)2 |
| 3 | r | 00 +r | (a1 ((NYT0 r1)1 b1)2)3 |
| 4 | a | 0 | (a2 ((NYT0 r1)1 b1)2)4 |
| 5 | c | 100 +c | (a2 (b1 ((NYT0 c1)1 r1)2)3)5 |
| 6 | a | 0 | (a3 (b1 ((NYT0 c1)1 r1)2)3)6 |
| 7 | d | 1100 +d | (a3 (((NYT0 d1)1 c1)2 (b1 r1)2)4)7 |
| 8 | a | 0 | (a4 (((NYT0 d1)1 c1)2 (b1 r1)2)4)8 |
| 9 | b | 110 | (a4 (((NYT0 d1)1 c1)2 (r1 b2)3)5)9 |
| 10 | r | 110 | (a4 (((NYT0 d1)1 c1)2 (r2 b2)4)6)10 |
| 11 | a | 0 | (a5 (((NYT0 d1)1 c1)2 (r2 b2)4)6)11 |

In step 3 the leaf a, of weight 1, moves from the right of the root to the left: the update reaches the inner node that holds b and the new leaf r, still of weight 1, and swaps it with a, the leader of the block of weight 1. Then this node grows to weight 2 on the right. FGK sends 20 path bits plus $5 \times 8 = 40$ raw bits. Vitter's algorithm sends 22 path bits on this short message, with the paths (empty), 0, 10, 11, 110, 11, 100, 0, 110, 101, 11. A static Huffman code for the final counts a 5, b 2, r 2, c 1, d 1 costs 23 bits, plus a description of the code that is longer than the 40 raw bits.

## Correctness

The proof has three steps. First, a tree is a Huffman tree for its leaf weights exactly when it has the sibling property (Gallager 1978). Second, the FGK update keeps the sibling property: each swap is between two nodes of the same weight, and after it the node to be incremented is the last of its block, so the increment keeps the weights in order. Third, encoder and decoder run the same deterministic update after the same symbol, so their trees stay equal and each path decodes to the right symbol. For Vitter's algorithm the slide keeps the order rule "leaves before inner nodes of the same weight", and Vitter shows that this makes the tree the flattest Huffman tree. The full argument for FGK, and the idea for Vitter's algorithm, are in proofs/correctness.md.

## Complexity

Let $l$ be the length of the codeword of the current symbol. Both updates visit the $l + 1$ nodes on the path from the leaf to the root. With the nodes kept in an array by number and a pointer from each node to the leader of its block, each step of the loop takes $O(1)$ time (Knuth 1985; Vitter 1987). So one symbol costs $O(l + 1)$ time, the same order as writing its codeword, and the message costs $O(t + b)$ time for $b$ output bits. A codeword has at most $n$ bits, so this is also $O(t n)$. The tree has $2n + 1$ nodes, so the space is $\Theta(n)$. The implementation below finds the leaders with a linear scan, which is shorter but costs $O(n)$ per step in the worst case.

## Properties

- **One pass, no table.** Only the alphabet of the raw letters must be agreed in advance.
- **Optimal at each step.** After each symbol, the tree is a Huffman tree for the counts so far.
- **Bounds against two-pass Huffman.** Let $S$ be the bits of a static Huffman code for the counts of the whole message, without its table, and $t$ the number of symbols. Vitter (1987) proved that his algorithm uses fewer than $S + t$ bits, not counting the raw letters, and that no one-pass Huffman method can do better in the worst case. For FGK his bound is about $2S + t$.
- **Flattest tree.** Vitter's invariant makes the tree minimize both the sum of the depths and the largest depth among all Huffman trees for the counts.
- **Not always fewer bits.** On a given message FGK can use fewer bits than Vitter's algorithm, as in the example. The bounds are for the worst case.
- **Adaptive model.** The code at step $i$ depends only on the counts of the first $i - 1$ symbols, which is the adaptive model of [adaptive modeling](/adaptive-modeling/) with Huffman codes instead of exact probabilities.

## Variants and improvements

- **Algorithm FGK.** Faller (1973) and Gallager (1978) found the swap update on their own. Knuth (1985) gave an efficient implementation with blocks of equal weights, in time proportional to the number of bits.
- **Vitter's algorithm.** Vitter (1987) called it algorithm Λ. It uses the slide instead of the swap and the implicit level-order numbering, and Vitter (1989) published it as Algorithm 673 of ACM TOMS.
- **Aging.** Halving all counts from time to time lets the code follow a source whose statistics change. After the halving, the tree must be rebuilt, because rounding can break the sibling property.
- **Larger alphabets.** The raw letters after the NYT path can be any fixed code of the alphabet, or an index into the unused symbols.
- **Adaptive arithmetic coding.** [Arithmetic coding](/arithmetic-coding/) with adaptive counts does the same job with a cost close to the entropy of the adaptive model, and its update is a counter increment. It replaced adaptive Huffman coding in most uses.

## When to use it

Use adaptive Huffman coding when the encoder must work in one pass, for example on a stream, and the decoder must stay simple: it needs only a tree walk and the update. Use it when a code table would cost too much for short messages. Do not use it when speed of decoding matters most: a [canonical Huffman code](/canonical-huffman-code/) decodes with table lookups, while the adaptive decoder walks the tree one bit at a time and changes it after each symbol. Moffat (2019) notes that no general-purpose compression system in current use is based on it. Adaptive arithmetic coding or [context modeling](/context-modeling/) gives better compression for an adaptive model.

## Pitfalls

- **Swap with the parent.** In FGK, the leader of the block of $q$ can be the parent of $q$, when the sibling of $q$ has weight 0. Swapping them would put a node inside its own subtree. Line L7 excludes the parent.
- **Numbers are places.** A swap exchanges the two places in the tree with their whole subtrees, and the two numbers. Swapping only the weights or only the symbols breaks the tree.
- **Different updates at the two ends.** Encoder and decoder must use the same tie rule, the same child order for the split, and the same update. A small difference makes the decoder go wrong at once.
- **The first symbol.** At the start the tree is only the NYT node, so the path to it is empty, and the first symbol costs only its raw bits.
- **Counts that grow without limit.** Weights must fit in a machine word. Halve the counts and rebuild the tree before they overflow.
- **Slow in practice.** The update touches each node on the path, with pointer changes. For large data a semi-static or block-adaptive canonical code is faster.

## Implementations

## History

Faller (1973) described an adaptive Huffman coder at the Asilomar Conference. Gallager (1978) found the same method on his own, as part of his paper on the sibling property and the redundancy of Huffman codes. Knuth (1985) gave an efficient implementation of the update in time proportional to the output, and the method became known as algorithm FGK, after the three authors. Vitter (1987) analyzed FGK, introduced algorithm Λ with the bound of fewer than $t$ extra bits over two-pass Huffman coding, showed that the bound is best possible for one-pass Huffman coding, and published an implementation in 1989. The Unix program compact used adaptive Huffman coding.

## References
