---
tag: 6C5RSP
kind: algorithm
slug: hu-tucker-algorithm
name: Hu-Tucker algorithm
aliases:
- Hu-Tucker coding
- T-C algorithm
area: compression-and-coding/entropy-coding
level: advanced
summary: Builds an optimal alphabetic prefix code by combining the lightest compatible pair, reading off the leaf levels, and rebuilding an ordered tree with those levels. O(n log n) time.
solves: [optimal-alphabetic-code]
model: word-ram
complexity:
  vars: {n: the number of symbols}
  time: {worst: O(n log n), average: O(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, comparison: true}
history:
  year: 1971
  people: [T. C. Hu, Alan C. Tucker]
  note: Hu and Tucker published the algorithm in the SIAM Journal on Applied Mathematics in 1971. Its proof is hard and was reworked in 1973, 1979 and 1997.
prereqs: [optimal-alphabetic-code, huffman-coding]
see_also: [garsia-wachs-algorithm, gilbert-moore-code, optimal-binary-search-tree, interval-dp, priority-queue, optimal-prefix-code]
sources:
  - paper: doi:10.1137/0121057
    title: T. C. Hu and A. C. Tucker, Optimal computer search trees and variable-length alphabetical codes, SIAM Journal on Applied Mathematics 21(4), 1971
    locator: pages 514 to 532
  - paper: doi:10.1137/0125012
    title: T. C. Hu, A new proof of the T-C algorithm, SIAM Journal on Applied Mathematics 25(1), 1973
    locator: pages 83 to 94
  - paper: doi:10.1137/0137015
    title: T. C. Hu, D. J. Kleitman and J. K. Tamaki, Binary trees optimum under various criteria, SIAM Journal on Applied Mathematics 37(2), 1979
    locator: pages 246 to 256
  - paper: doi:10.1016/S0304-3975(96)00296-4
    title: Marek Karpinski, Lawrence L. Larmore and Wojciech Rytter, Correctness of constructing optimal alphabetic trees revisited, Theoretical Computer Science 180, 1997
    locator: pages 309 to 324
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2, Binary tree searching (the Hu-Tucker algorithm)
---

The Hu-Tucker algorithm finds an [optimal alphabetic code](/optimal-alphabetic-code/): a binary tree with the symbols at the leaves in a given order, of least weighted path length. It looks like [Huffman's algorithm](/huffman-coding/) with one extra rule. It repeatedly combines the two lightest nodes, but only nodes that are *compatible*, meaning that no original leaf still waiting to be combined lies between them. The tree that this builds is usually not in order, but the depths of its leaves are right. A last pass builds the ordered tree with those depths. Hu and Tucker (1971) gave the algorithm; its proof is famously hard. The simple form runs in $O(n^2)$ time and a version with priority queues in $O(n \log n)$.

## In plain words

Start with the symbols in their order, each one a box with its weight. At each step, join two items into a circle whose weight is their sum, and put the circle where the left one was. Choose the pair with the smallest sum, but you may only join two items if no box stands between them. Circles do not block: you may join across them.

When one item is left, you have a tree, but its leaves may be out of order. Throw the tree away, except for one number per symbol: how deep it was. Then build a new tree that has the symbols in order at exactly those depths. Hu and Tucker proved that such a tree always exists and that it is the best one.

## The algorithm

The input is the weights $w_1, \ldots, w_n > 0$ of the symbols in their order. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area. A *square* node is an original leaf not yet combined; a *circle* node is a node made by combining two nodes. Two nodes of the list are *compatible* when no square node lies strictly between them.

```pseudo id=main
HU-TUCKER(w[1 .. n])
L1  A ← the list of n square nodes with the weights w[1], …, w[n]
L2  while A has more than one node do
L3      (x, y) ← the compatible pair of A with the least weight sum; on a tie the leftmost x, then the leftmost y
L4      replace x by a circle node of weight w(x) + w(y) with the children x and y; remove y from A
L5  d[i] ← the depth of leaf i in the tree whose root is the node left in A, for each i
L6  return BUILD(d)
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

Lines L1 to L4 are the *combination* phase. A square node blocks the pairs that would jump over it; once it is combined it becomes a circle and stops blocking. So a pair can join nodes that are not neighbours, which is why the tree of this phase can have its leaves out of order. Line L5 is the *level* phase: only the depths are kept. Line L6 is the *recombination* phase. BUILD reads the depths from left to right and joins two neighbours as soon as they are at the same depth; for depths that come from an alphabetic tree it rebuilds that tree.

**The simple form.** The list splits into *blocks*: the nodes from one square node to the next, both included, with the nodes before the first square and after the last square added to the end blocks. Two nodes are compatible exactly when they are in a common block, and the best pair in a block is its two lightest nodes. So line L3 is one scan of the list, $O(n)$ time, and the whole algorithm takes $O(n^2)$ time.

## Example

Six symbols A to F with weights 10, 8, 3, 6, 2, 1. Circles are written in parentheses.

| step | list (squares plain, circles in parentheses) | least compatible pair | sum |
|---|---|---|---|
| 1 | A10 B8 C3 D6 E2 F1 | E, F | 3 |
| 2 | A10 B8 C3 D6 (EF)3 | C, D (ties with D and EF; C is further left) | 9 |
| 3 | A10 B8 (CD)9 (EF)3 | B, (EF) | 11 |
| 4 | A10 (B·EF)11 (CD)9 | A, (CD) | 19 |
| 5 | (A·CD)19 (B·EF)11 | the last two | 30 |

At step 3 the only squares are A and B, so B, (CD) and (EF) are all compatible: B and (EF) are joined across the circle (CD). At step 4 the only square is A, and A is joined with (CD) across (B·EF). The tree of this phase has the leaves in the order A, C, D, B, E, F, which is not alphabetic. Its depths are A 2, B 2, C 3, D 3, E 3, F 3.

BUILD then pushes A and B, both at depth 2, and joins them at depth 1; pushes C and D at depth 3 and joins them at depth 2; does the same for E and F; joins (CD) and (EF) at depth 1; and joins the two halves at the root. The result is ((A, B), ((C, D), (E, F))), with the codewords 00, 01, 100, 101, 110, 111. The cost is $20 + 16 + 9 + 18 + 6 + 3 = 72$, the same as the sum of the circle weights $3 + 9 + 11 + 19 + 30$, and the interval dynamic program confirms that 72 is optimal. Huffman's algorithm, free to change the order, gets 69.

## Correctness

The recombination phase is easy to prove. If the depths come from an alphabetic tree, the leftmost pair of sibling leaves are the first two neighbours with equal depth, and BUILD joins them first; replacing them by their parent gives a smaller tree, and induction finishes the proof. The cost of the depths from phase 1 is the sum of the circle weights, as in Huffman's algorithm.

The hard part is to prove that the depths of phase 1 belong to some alphabetic tree, and that their cost is optimal. The combination phase is optimal over a wider class of trees, those that combine only compatible pairs, by an exchange argument, and the least compatible pair has a local minimality that keeps the depths feasible for an ordered tree. The details are long: Hu and Tucker's paper, Hu's new proof (1973), the general treatment of Hu, Kleitman and Tamaki (1979), and the proof of Karpinski, Larmore and Rytter (1997). The proof of BUILD and the structure of the main proof are in proofs/correctness.md.

## Complexity

- **Simple form.** $n - 1$ combinations, each found by one $O(n)$ scan: $O(n^2)$ time, $O(n)$ space. This is the form in the implementation below.
- **With priority queues.** Keep a mergeable [priority queue](/priority-queue/) for each block and a global queue of the best pair of each block. A combination removes at most two square nodes and so merges at most three blocks into one. With leftist trees or another mergeable heap, each step costs $O(\log n)$, for $O(n \log n)$ in total.
- **Phases 2 and 3.** $O(n)$ time each.

## Properties

- **Exact.** It finds an optimal alphabetic tree for any positive weights.
- **Not alphabetic in phase 1.** The combination tree is generally out of order; only its depths are used.
- **Same cost as phase 1.** The final tree has the same depths, so the same cost, as the combination tree.
- **Huffman as a special case.** If no square node blocked, the rule would be Huffman's. For sorted weights the result has the cost of a Huffman code.
- **Ties matter.** The tie rule (least sum, then the leftmost left node, then the leftmost right node) is part of the algorithm. Its mirror image, rightmost first, also works. But in our tests, taking the leftmost left node with the rightmost right node, or a random pair among the ties, sometimes gave depths that no ordered tree has, for example for the weights 1, 2, 3, 4, 1, 3, 4, 4.
- **Leaves only.** It needs all the weight on the leaves. It does not solve the [optimal binary search tree](/optimal-binary-search-tree/) problem with weights on the keys.

## Variants and improvements

- **[Garsia-Wachs algorithm](/garsia-wachs-algorithm/).** A simpler combination rule, followed by the same level and recombination phases, with the same optimal cost and the same $O(n \log n)$ bound; its proof is also simpler.
- **Other cost functions.** Hu, Kleitman and Tamaki (1979) show that the same scheme is optimal for a family of cost functions besides the weighted path length.
- **Interval dynamic program.** The $O(n^2)$ program with Knuth's speedup is simpler to get right and good enough for small alphabets.

## When to use it

Use Hu-Tucker, or Garsia-Wachs, to build an order-preserving code for a large alphabet, as in order-preserving compression of keys in sorted indexes, or to build a comparison tree for searching a sorted table with known gap frequencies. For a few hundred symbols, the $O(n^2)$ dynamic program is simpler and easier to check. When the order does not matter, use [Huffman coding](/huffman-coding/).

## Pitfalls

- **Using the phase 1 tree.** It is not alphabetic. Output codewords only after the recombination phase.
- **Wrong tie rule.** Mixing the directions of the tie rule, or breaking ties at random, can give depths that no alphabetic tree has, and BUILD then fails. Use exactly the rule of line L3, or its full mirror image.
- **Circles block.** Treating circle nodes as blocking gives the plain adjacent merge, which is not optimal. Only square nodes block.
- **Placement of the new node.** The new circle takes the place of the left node of the pair. Putting it elsewhere changes later compatibility.
- **Trusting a short proof.** The algorithm looks like Huffman's, but the Huffman exchange argument does not carry over directly; test any variant against the dynamic program.

## Implementations

## History

Gilbert and Moore (1959) solved the alphabetic problem by an $O(n^3)$ dynamic program, and Knuth (1971) reduced it to $O(n^2)$. Hu and Tucker (1971) found the first $O(n \log n)$ method, as part of work on optimal search trees, with a long proof. Hu (1973) gave a new proof, and Hu, Kleitman and Tamaki (1979) placed the algorithm in a general theory of cost functions. Garsia and Wachs (1977) gave a different algorithm that yields the same depths. Karpinski, Larmore and Rytter (1997) revisited the correctness proof. The algorithm is sometimes called the T-C algorithm, after the title of Hu's 1973 paper.

## References
