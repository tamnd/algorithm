---
tag: Y88NT5
kind: algorithm
slug: garsia-wachs-algorithm
name: Garsia-Wachs algorithm
aliases:
- Garsia-Wachs
area: compression-and-coding/entropy-coding
level: advanced
summary: Builds an optimal alphabetic tree by combining the leftmost pair x, y with w(x) <= w(z), moving the sum left past lighter items, then rebuilding by depths. O(n log n) time.
solves: [optimal-alphabetic-code]
model: word-ram
complexity:
  vars: {n: the number of symbols}
  time: {worst: O(n log n), average: O(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, comparison: true}
history:
  year: 1977
  people: [Adriano M. Garsia, Michelle L. Wachs]
  note: Garsia and Wachs published the algorithm in the SIAM Journal on Computing in 1977. Kingston gave a shorter proof in 1988.
prereqs: [optimal-alphabetic-code]
see_also: [hu-tucker-algorithm, gilbert-moore-code, optimal-binary-search-tree, huffman-coding, interval-dp, optimal-prefix-code]
sources:
  - paper: doi:10.1137/0206045
    title: Adriano M. Garsia and Michelle L. Wachs, A new algorithm for minimum cost binary trees, SIAM Journal on Computing 6(4), 1977
    locator: pages 622 to 642
  - paper: doi:10.1016/0196-6774(88)90009-0
    title: Jeffrey H. Kingston, A new proof of the Garsia-Wachs algorithm, Journal of Algorithms 9(1), 1988
    locator: pages 129 to 136
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2, Binary tree searching (the Garsia-Wachs algorithm)
  - paper: doi:10.1137/0121057
    title: T. C. Hu and A. C. Tucker, Optimal computer search trees and variable-length alphabetical codes, SIAM Journal on Applied Mathematics 21(4), 1971
    locator: pages 514 to 532
---

The Garsia-Wachs algorithm finds an [optimal alphabetic code](/optimal-alphabetic-code/): a binary tree with the symbols at the leaves in a given order, of least weighted path length. Like the [Hu-Tucker algorithm](/hu-tucker-algorithm/), it first builds a tree whose leaves may be out of order, keeps only the depths of the leaves, and then builds an ordered tree with those depths. Its combination rule is simpler. Find the leftmost three neighbours $x, y, z$ with $w(x) \le w(z)$, join $x$ and $y$, and move the new item to the left past all lighter items. Garsia and Wachs (1977) gave it with an $O(n \log n)$ bound; the simple form runs in $O(n^2)$ time.

## In plain words

Write the weights in a row, with a huge weight at each end. Walk from the left and look at each item together with the items two places apart from it. Stop at the first spot where an item is not heavier than the item two places to its right. Join that item with its right neighbour into one item whose weight is their sum.

Now slide the new item to the left past every item that is lighter than it, and stop in front of the first item that is at least as heavy. Repeat until one item is left.

The tree you get may have its leaves out of order, but it tells you how deep each symbol should be. Build an ordered tree with those depths, and it is the best one.

## The algorithm

The input is the weights $w_1, \ldots, w_n > 0$ of the symbols in their order. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area. The list $A$ holds items: leaves, made items, and two sentinels of weight $\infty$.

```pseudo id=main
GARSIA-WACHS(w[1 .. n])
L1  A ← ∞, leaf 1, …, leaf n, ∞            ▷ the weight of leaf i is w[i]
L2  while A has more than one item besides the two sentinels do
L3      (x, y, z) ← the leftmost three neighbours of A with w(x) ≤ w(z)
L4      remove x and y from A; t ← a new item of weight w(x) + w(y) with the children x and y
L5      insert t just after the nearest item to the left of the old place of x whose weight is at least w(t)
L6  d[i] ← the depth of leaf i in the tree whose root is the real item left in A, for each i
L7  return BUILD(d)
```

```pseudo id=build
BUILD(d[1 .. n])                           ▷ the depths of an alphabetic tree, left to right
B1  S ← an empty stack
B2  for i ← 1 to n do
B3      push (d[i], leaf i) on S
B4      while the two top items of S have the same depth δ do
B5          pop them and push (δ − 1, a node with them as left and right child)
B6  return the single node on S
```

Line L3 finds the pair to join. Since the right sentinel has weight $\infty$, some triple always qualifies, and since the left sentinel is never $x$ while two real items remain, $x$ and $y$ are real. Every triple to the left of the chosen one has $w(x) > w(z)$, so the items before $y$ are, in steps of two, decreasing. Line L5 is the *move*: $t$ passes every lighter item on its left and stops behind the first one at least as heavy, at the latest behind the left sentinel. The move can put $t$ before items that were to the left of $x$, which is why the tree of lines L1 to L5 can be out of order. Line L6 keeps only the depths, and line L7 rebuilds an ordered tree with them, as in the Hu-Tucker algorithm.

**The simple form.** Each step scans for the first triple in $O(n)$ time and moves $t$ in $O(n)$ time, so the whole algorithm takes $O(n^2)$ time. This is the form in the implementation below.

## Example

Six symbols A to F with weights 10, 8, 3, 6, 2, 1. The sentinels are written ∞, and made items in parentheses.

| step | list before the step | first triple with $w(x) \le w(z)$ | new item | moved to |
|---|---|---|---|---|
| 1 | ∞ A10 B8 C3 D6 E2 F1 ∞ | E2 F1 ∞ | (EF)3 | stays after D6 |
| 2 | ∞ A10 B8 C3 D6 (EF)3 ∞ | C3 D6 (EF)3 | (CD)9 | passes B8, stops after A10 |
| 3 | ∞ A10 (CD)9 B8 (EF)3 ∞ | B8 (EF)3 ∞ | (B·EF)11 | passes (CD)9 and A10, to the front |
| 4 | ∞ (B·EF)11 A10 (CD)9 ∞ | A10 (CD)9 ∞ | (A·CD)19 | passes (B·EF)11, to the front |
| 5 | ∞ (A·CD)19 (B·EF)11 ∞ | the last two | 30 | |

At step 2 the triples ∞ A B, A B C and B C D fail, because $\infty > 8$, $10 > 3$ and $8 > 6$; the triple C D (EF) passes, because $3 \le 3$. After step 2 the list is A, (CD), B, out of order. The final tree has the depths A 2, B 2, C 3, D 3, E 3, F 3. BUILD turns them into ((A, B), ((C, D), (E, F))), with cost $20 + 16 + 9 + 18 + 6 + 3 = 72$, which is also $3 + 9 + 11 + 19 + 30$, the sum of the new items. The interval dynamic program and the Hu-Tucker algorithm give the same cost.

**Why the move matters.** For the weights 2, 2, 1, 2 the first triple is 2, 1, 2, so the second and third items join into 3. The move takes 3 past the first 2 to the front: 3, 2, 2. The two 2s then join, and the tree has all four leaves at depth 2, cost 14. Without the move, 3 would stay in the middle, join with the last 2, and the cost would be 15.

## Correctness

The combination phase is well defined: the right sentinel makes some triple qualify, and the left sentinel stops every move. The cost of the leaf depths of the combination tree is the sum of the weights of the new items, since each leaf adds its weight to each of its ancestors. BUILD rebuilds an alphabetic tree from its depths, by the same proof as for the Hu-Tucker algorithm.

The main theorem is that one step does not lose: the optimal cost for the list before the step is $w(x) + w(y)$ plus the optimal cost for the list after it, with $t$ at its new place, and the final depths belong to an alphabetic tree. The proof shifts the depths of the items that $t$ passes by one place, which costs nothing because all of them are lighter than $t$ and the triples to the left of $x$ are decreasing. Kingston (1988) gave a shorter proof than the original one. The easy parts and the structure of the main proof are in proofs/correctness.md.

## Complexity

- **Simple form.** $n - 1$ steps, each with an $O(n)$ scan and an $O(n)$ move: $O(n^2)$ time, $O(n)$ space.
- **Faster forms.** With suitable data structures for the scan and the move, the combination phase runs in $O(n \log n)$ time (Garsia and Wachs 1977; Knuth, Section 6.2.2).
- **Phases 2 and 3.** $O(n)$ time each.

## Properties

- **Exact.** It finds an optimal alphabetic tree for any positive weights.
- **Same cost as Hu-Tucker.** Both algorithms give optimal trees, so their costs are equal. When several trees are optimal, the two methods need not pick the same one.
- **Not alphabetic in phase 1.** The move reorders items; only the depths are kept.
- **Local rule.** Each step looks only at three neighbours and at the items that $t$ passes, with no notion of compatible pairs or square nodes.
- **Leaves only.** All weight must be on the leaves; it does not solve the [optimal binary search tree](/optimal-binary-search-tree/) problem with weights on the keys.

## Variants and improvements

- **[Hu-Tucker algorithm](/hu-tucker-algorithm/).** The older method with the same three phases, combining the lightest compatible pair. It is harder to state and to prove.
- **Interval dynamic program.** The $O(n^2)$ program with Knuth's speedup, simpler to check and enough for small alphabets.
- **[Huffman coding](/huffman-coding/).** For sorted weights the order does not cost anything, and Huffman's algorithm gives the same cost more simply.

## When to use it

Use Garsia-Wachs to build an optimal order-preserving code or a comparison tree for gaps of known frequency when the alphabet is large. It is shorter to code than Hu-Tucker and easier to check. For a few hundred symbols, the $O(n^2)$ dynamic program is a simple alternative. If the order does not matter, use a Huffman code.

## Pitfalls

- **Forgetting the move.** Joining $x$ and $y$ in place gives a non-optimal tree, as the weights 2, 2, 1, 2 show.
- **Strict or not.** The triple test is $w(x) \le w(z)$, and the move stops at the first item with weight $\ge w(t)$. Keep both comparisons as stated, and test any change against the dynamic program on inputs with many equal weights.
- **Using the phase 1 tree.** It is not alphabetic. Output codewords only after BUILD.
- **Missing sentinels.** Without the sentinel of weight $\infty$ on the right, the scan can run off the end; without the one on the left, the move can.

## Implementations

## History

Garsia and Wachs (1977) gave the algorithm in the SIAM Journal on Computing as a new method for minimum cost binary trees, six years after Hu and Tucker's. Kingston (1988) gave a new proof in the Journal of Algorithms. Knuth presents the algorithm in Section 6.2.2 of The Art of Computer Programming, Volume 3.

## References
