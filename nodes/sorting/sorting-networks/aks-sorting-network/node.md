---
tag: 9EWBX0
kind: algorithm
slug: aks-sorting-network
name: AKS sorting network
aliases:
- Ajtai-Komlós-Szemerédi network
- AKS network
area: sorting/sorting-networks
level: research
summary: A sorting network of depth O(log n) built from expander-based halvers, with a very large constant.
solves: [sorting-problem]
model: sorting-network
complexity:
  vars: {n: "the number of items, a power of 2 in the construction"}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n log n)}
  depth: {worst: Θ(log n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1983
  people: [Miklós Ajtai, János Komlós, Endre Szemerédi]
  note: Ajtai, Komlós and Szemerédi gave the first sorting network of depth O(log n) at STOC 1983; Paterson (1990) and Seiferas (2009) simplified the construction and its proof.
prereqs: [sorting-network, halver, zero-one-principle]
see_also: [odd-even-merge-sort, bitonic-sort, sorting-network-depth-lower-bound, depth-size-tradeoff, network-depth, quicksort, cole-merge-sort, probabilistic-method]
sources:
  - paper: doi:10.1007/BF02579338
    title: M. Ajtai, J. Komlós and E. Szemerédi, Sorting in c log n parallel steps, Combinatorica 3(1) (1983)
    locator: pp. 1 to 19
  - paper: doi:10.1145/800061.808726
    title: M. Ajtai, J. Komlós and E. Szemerédi, An O(n log n) sorting network, Proceedings of the 15th ACM Symposium on Theory of Computing (1983)
    locator: pp. 1 to 9
  - paper: doi:10.1007/BF01840378
    title: M. S. Paterson, Improved sorting networks with O(log N) depth, Algorithmica 5 (1990)
    locator: pp. 75 to 92
  - paper: doi:10.1007/s00453-007-9025-6
    title: Joel Seiferas, Sorting networks of logarithmic depth, further simplified, Algorithmica 53 (2009)
    locator: Sections 2 to 5 (the bags, the schedule, the invariant and its proof), Section 6 (the approximate separators) and Section 7 (the constants)
  - paper: "Natalia Dobrokhotova-Maikova, Alexander Kozachinskiy and Vladimir Podolskii, Towards simpler sorting networks and monotone circuits for majority, arXiv:2310.12270 (2023)"
    locator: the abstract and Section 1 (the explicit networks of depth O(log n) and their constants)
---

The AKS sorting network, found by Ajtai, Komlós and Szemerédi in 1983, is a [sorting network](/sorting-network/) on $n$ wires of [depth](/network-depth/) $O(\log n)$ and [size](/network-size/) $O(n \log n)$. Both bounds are optimal up to a constant factor, because a network of depth $D$ makes at most $D n / 2$ comparisons and every comparison sort needs $\lg(n!)$ of them. The network works like an ideal [quicksort](/quicksort/) on a binary tree of bags: it splits the items roughly in half with constant-depth [halvers](/halver/) built from expander graphs, and it sends the items that the halvers put on the wrong side back up the tree to be fixed later. The constant factor is in the thousands, so for every practical $n$ Batcher's networks of depth $O(\log^2 n)$ are shallower.

## In plain words

Quicksort splits the items into a small half and a large half, then splits each half again. A network can not split exactly in a few steps, but a halver can split roughly: nearly all small items go left and nearly all large items go right.

AKS repeats rough splits on a tree of bags. The root bag starts with all items. In each round, each bag splits its items, sends the two halves down to its two children, and sends a few items from both ends back up to its parent. The items at the ends are the most likely to be in the wrong bag, so they go up and come down again on the correct side.

After a number of rounds proportional to the height of the tree, each item sits in a small subtree where it belongs. A small sorter on each subtree finishes the job.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, where $n = 2^L \ge 2$. The output is the same array in non-decreasing order, and the method must be a fixed sequence of compare-exchange steps that depends only on $n$. This is the [sorting problem](/sorting-problem/) in the sorting network model. The goal is a network whose depth is $O(\log n)$, the smallest possible order, since each output depends on all $n$ inputs and a layer at most doubles the number of inputs that one wire depends on (see [sorting network depth lower bound](/sorting-network-depth-lower-bound/)).

## The algorithm

This is Seiferas's version of the construction. It has four constants: $A > 1$, $\nu < 1$, and two small fractions $\lambda$ and $\varepsilon$. The values $A = 10$, $\lambda = \varepsilon = 1/100$ and $\nu = 13/20$ work.

**The tree of bags.** Take a complete binary tree whose nodes are the binary intervals of $\{0, \ldots, n-1\}$ of length at least 2: the root is the whole range, its children are the two halves, and so on down to the $n/2$ pairs at depth $L - 1$. Each node holds a *bag*, which is a set of registers (wires). An item of rank $r$ is *native* to each node whose interval contains $r$, so it is native to one node on each level. An item in a bag is a *$j$-stranger* when it is not native to the ancestor of that bag $j - 1$ levels up. So the 1-strangers are the items that are not native to their own bag.

**Capacities.** After $t$ stages, a bag at depth $d$ has the *capacity* $b = n \nu^t A^d$. This is only an upper bound on the number of items in the bag. It grows with the depth and shrinks with the time.

**One stage.** Each nonempty bag applies an approximate separator to its registers. Then it sends $\lfloor \lambda b \rfloor$ items from each end of the result to its parent (all of them, if it has fewer than $2 \lfloor \lambda b \rfloor$), and one more item if the number left is odd. It sends the first half of the rest to its left child and the second half to its right child. The root has no parent, so it sends all its items down. Sending an item to another bag moves no data: it only changes which bag a register belongs to.

```pseudo id=main
AKS-NETWORK(n)                                   ▷ n = 2^L registers
L1  put all n registers in the root bag; t ← 0
L2  while the leaf capacity n ν^t A^(L−1) ≥ 1/λ do
L3      for each nonempty bag X, at depth d, in parallel do
L4          b ← n ν^t A^d                         ▷ the capacity of X
L5          SEPARATE(the registers of X)
L6          if d > 0 then send the first and last ⌊λb⌋ registers of X to the parent (all, if fewer)
L7          if d > 0 and an odd number of registers remain then send the middle one to the parent
L8          send the first half of the rest to the left child and the second half to the right child
L9      t ← t + 1
L10 for each subtree whose root has depth max(L − 1 − k, 0) do SORT the registers of the subtree, and output them in tree order

COMPARE(A, i, j)                                 ▷ the minimum goes to register i
L11 if A[j] < A[i] then exchange A[i] and A[j]
```

In line L10, $k$ is the smallest integer with $(1/\lambda)(1/A)^{k+1} < 1$, which is $k = 2$ for the values above. Each SEPARATE and SORT is a fixed network of COMPARE steps, so the whole construction is a list of comparators. Line L5 must be an *approximate separator* of constant depth: it puts all but a fraction $\varepsilon$ of the smallest $\lambda' m$ items among the first $\lfloor \lambda m \rfloor$ positions, for each $\lambda' \le \lambda$, and the same at the other end, and it is also an $\varepsilon$-halver. Seiferas builds it from $\varepsilon_0$-halvers on nested prefixes and suffixes, and each halver from a $d$-regular bipartite expander graph whose edges split into $d$ [perfect matchings](/perfect-matching/), one layer each. The size of each bag depends only on $n$ and $t$, never on the data, so the registers of each bag are known in advance.

The Python code below follows this schedule exactly, but its SEPARATE is an exact sorter (Batcher's [odd-even merge sort](/odd-even-merge-sort/) on the bag). An exact sorter is an approximate separator with $\varepsilon = 0$, so the code sorts every input, but its depth is not $O(\log n)$. It also has functions that build halvers from random matchings and compute their exact $\varepsilon$ by trying all inputs of zeros and ones.

## Example

Take $n = 16$, so $L = 4$, the leaves are at depth 3, and the input is $[11, 3, 14, 0, 9, 6, 15, 1, 12, 5, 8, 2, 13, 7, 10, 4]$. The items are the ranks $0, \ldots, 15$. The table shows the items of each nonempty bag after each stage. The leaf capacity is $16 \cdot (13/20)^t \cdot 10^3$.

| after stage $t$ | leaf capacity | nonempty bags, with their items |
|---|---|---|
| 0 | 16000 | root: all 16 |
| 1 | 10400 | depth 1: $\{0..7\}$, $\{8..15\}$ |
| 2 | 6760 | root: $\{0, 7, 8, 15\}$; depth 2: $\{1, 2, 3\}$, $\{4, 5, 6\}$, $\{9, 10, 11\}$, $\{12, 13, 14\}$ |
| 3 | 4394 | depth 1: $\{0..7\}$, $\{8..15\}$ |
| 4 | 2856.1 | depth 2: $\{0..3\}$, $\{4..7\}$, $\{8..11\}$, $\{12..15\}$ |
| 5, 6 | 1856.5, 1206.7 | as after stages 3 and 4 |
| 7 | 784.4 | depth 1: $\{0, 3, 4, 7\}$, $\{8, 11, 12, 15\}$; depth 3: one item each, $1, 2, 5, 6, 9, 10, 13, 14$ |
| 8 | 509.8 | depth 2: $\{0..3\}$, $\{4..7\}$, $\{8..11\}$, $\{12..15\}$ |
| 9 | 331.4 | depth 3: the pairs $\{0, 1\}, \{2, 3\}, \ldots, \{14, 15\}$ |
| 10, 11, 12 | 215.4, 140.0, 91.0 | depth 2, depth 3, depth 2, as after stages 8 and 9 |

In stage 2 a depth-1 bag has capacity $16 \cdot \tfrac{13}{20} \cdot 10 = 104$, so it sends $\lfloor 104/100 \rfloor = 1$ item from each end to the root: 0 and 7 from the left bag, 8 and 15 from the right bag. In stage 3 a depth-2 bag has capacity 676, so $\lfloor \lambda b \rfloor = 6$ is more than half of its 3 items, and all of them go back up. In stage 7 the depth-1 bags have capacity about 12.1, so $\lfloor \lambda b \rfloor = 0$ and they send all items down, while the depth-2 bags, with capacity about 120.7, send one item from each end up. After stage 12 the leaf capacity is $91 < 100$ and the loop stops. Here $k = 2$, so line L10 sorts the two subtrees of depth-1 roots. They hold exactly the items $\{0..7\}$ and $\{8..15\}$, so the output is sorted. On this small input the separators already sort, so no item is ever a stranger. With real halvers the strangers are the reason for the kick back.

The network for $n = 16$ has 338 comparators and depth 53, while odd-even merge sort uses 63 comparators and depth 10.

## Correctness

By the [zero-one principle](/zero-one-principle/), it is enough to show that the network sorts each permutation of the ranks $0, \ldots, n-1$, because each input of zeros and ones is the image of such a permutation under a non-decreasing map. Seiferas proves that each stage keeps a four-part invariant: (1) alternate levels of the tree are empty; (2) all bags on one level hold the same number of items; (3) each bag holds at most its capacity; (4) each bag holds at most $\lambda \varepsilon^{j-1} b$ items that are $j$-strangers. Parts 1 and 2 hold because the schedule is the same for each bag of a level. Part 3 follows from the bound $4 \lambda A b + 2 + b/(2A)$ on the items that arrive in a bag, if $\nu \ge 4 \lambda A + 5/(2A)$. Part 4 compares the actual distribution with a benchmark in which each subtree holds only native items, and needs one more inequality between the constants. When the leaf capacity falls below $1/\lambda$, the bags above the final subtrees have capacity below 1, so they are empty, and each final subtree holds no strangers. Part 2 then says that each final subtree holds exactly the items of its interval, so line L10 sorts. The loop of line L2 never asks a leaf to send items down, because a leaf holds at most 2 items and sends $2 \lfloor \lambda b \rfloor \ge 2$ of them up. The proof below gives the case $\varepsilon = 0$ of the code in full.

## Complexity

Let $T$ be the number of stages. The loop stops after the first $t$ with $n \nu^t A^{L-1} < 1/\lambda$, so

$$T = \left\lfloor \frac{(1 + \lg A) \lg n - \lg(A/\lambda)}{\lg(1/\nu)} \right\rfloor + 1 \approx 6.95 \lg n - 15$$

for the constants above, which gives $T = 12$ for $n = 16$ and $T = 54$ for $n = 1024$. In each stage the bags are disjoint, so their separators run in parallel. If a separator has constant depth $c$, which depends only on $\lambda$ and $\varepsilon$, the network has depth at most $cT$ plus the depth of the final sorters, which is a constant. That is $O(\log n)$. A layer has at most $n/2$ comparators, so the size is $O(n \log n)$. The extra space is that of the list of comparators, which the code builds once for each $n$.

- **The constants.** For $A = 10$ and $\lambda = \varepsilon = 1/100$, Seiferas estimates about $6.95 \lg n$ stages, each as deep as seven $1/700$-halvers. Paterson's direct bound on the depth of an $\varepsilon$-halver, $\lceil 2 \log \varepsilon / \log(1 - \varepsilon) + 2/\varepsilon - 1 \rceil$, gives 10564 for $\varepsilon = 1/700$. Paterson's own tuning gives depth below $6100 \lg n$, and Chvátal's below $1830 \lg n$. Batcher's depth $\tfrac12 \lg n (\lg n + 1)$ is smaller than $1830 \lg n$ for each $n < 2^{3659}$.
- **The code.** Its exact separators have depth $O(\log^2 m)$ on a bag of $m$ items, so its depth is $O(\log^3 n)$, not $O(\log n)$. The table shows its size and depth next to odd-even merge sort.

| $n$ | stages $T$ | size (code) | depth (code) | size (odd-even merge) | depth (odd-even merge) |
|---|---|---|---|---|---|
| 16 | 12 | 338 | 53 | 63 | 10 |
| 64 | 26 | 4977 | 203 | 543 | 21 |
| 256 | 40 | 51146 | 528 | 3839 | 36 |
| 1024 | 54 | 423328 | 1074 | 24063 | 55 |

## Properties

- **Data oblivious.** Which registers each bag holds depends only on $n$ and $t$, so the comparators are fixed in advance.
- **Optimal order.** Depth $\Theta(\log n)$ and size $\Theta(n \log n)$ are the best possible up to constant factors.
- **In place and not stable.** It moves items only by exchanges, and the separators compare items far apart.
- **Not adaptive.** A sorted input costs the same comparisons as any other.
- **Not explicit in the simple form.** The halvers need expander graphs. Random regular bipartite graphs are expanders with high probability (the [probabilistic method](/probabilistic-method/)), and explicit families exist, but the explicit ones make the constants larger still.

## Variants and improvements

- **Ajtai, Komlós and Szemerédi (1983).** The original network uses $\varepsilon$-nearsorters and a more complex schedule.
- **Paterson (1990).** He reorganized the construction around the tree of bags with capacities and separators, and proved depth below $6100 \lg n$. Most later versions start from his.
- **Seiferas (2009).** He tuned the invariant so that each stage follows the same rule, removed the bags of single items, and reduced the constraints to a few inequalities between $A$, $\nu$, $\lambda$ and $\varepsilon$. This is the version on this page.
- **Multiway comparators.** Ajtai, Komlós and Szemerédi (1992) and Chvátal use $M$-sorters as building blocks of the halvers, which makes the halvers much shallower; Chvátal's bound is below $1830 \lg n$.
- **Monotone circuits.** Replacing each comparator by an AND gate and an OR gate turns the network into a monotone circuit of depth $O(\log n)$ for the majority function. No simple explicit construction of this depth is known.

## When to use it

Use the AKS network in proofs, not in programs. It shows that sorting networks, and so oblivious sorting and monotone circuits for sorting and majority, exist with depth $O(\log n)$ and size $O(n \log n)$. Other results that need an oblivious sort of optimal order use it as a black box. To sort on real parallel hardware, use [bitonic sort](/bitonic-sort/) or odd-even merge sort. On a parallel machine that may choose its steps from the data, [Cole's merge sort](/cole-merge-sort/) also reaches $O(\log n)$ time with a much smaller constant.

## Pitfalls

- **An exact separator does not give the bound.** With a sorter in line L5, each stage has depth $\Theta(\log^2 m)$ and the network is deeper than Batcher's. The depth $O(\log n)$ needs separators of constant depth.
- **A halver with the wrong $\varepsilon$.** The proof needs $\varepsilon$ small enough for all inequalities to hold together. A random union of a few matchings has a large $\varepsilon$: for 16 wires, 4 random matchings give about $1/3$ and 8 give $1/4$, far from $1/100$.
- **Capacity is not the number of items.** The kick-back count $\lfloor \lambda b \rfloor$ uses the capacity, which may be much larger than the number of items in the bag. Then all items go up, as in stage 3 of the example.
- **The odd item.** If the items left after the kick back are odd in number, the middle one must go to the parent, or the two children get different numbers and part 2 of the invariant fails.
- **The final step.** Stopping the loop too early leaves strangers outside their final subtrees. Line L10 needs the leaf capacity below $1/\lambda$ and subtrees of height $k$ with $(1/\lambda)(1/A)^{k+1} < 1$.
- **$n$ not a power of 2.** Pad with items larger than all others, or drop the comparators on the extra wires, as for Batcher's networks.

## Implementations

## History

Ajtai, Komlós and Szemerédi presented an $O(n \log n)$ sorting network at STOC 1983, and the journal paper "Sorting in $c \log n$ parallel steps" appeared in Combinatorica the same year. It answered the old question whether depth $O(\log n)$ is possible. Paterson's 1990 version made the construction simpler and the constant smaller. Seiferas gave a further simplified version in 2009, with a short proof of the invariant.

## References
