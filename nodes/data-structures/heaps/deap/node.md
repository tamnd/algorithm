---
tag: 5CWRB5
kind: data-structure
slug: deap
name: Deap
aliases:
- double-ended heap (deap)
area: data-structures/heaps
level: advanced
summary: Double-ended heap with a min side and a max side, both stored in one complete tree.
implements: [double-ended-priority-queue]
model: comparison-model
prereqs: [double-ended-priority-queue, binary-heap, heap-property, sift-up]
see_also: [double-ended-priority-queue, interval-heap, min-max-heap, binary-heap, heap-property, complete-binary-tree, priority-queue, heap-delete]
sources:
  - paper: "Svante Carlsson, The deap, a double-ended heap to implement double-ended priority queues, Information Processing Letters 26(1), 1987"
    locator: the definition of the deap, the correspondence between the two heaps, and the insert and delete algorithms
  - book: isbn:9781584884354
    title: Dinesh P. Mehta and Sartaj Sahni (editors), Handbook of Data Structures and Applications
    locator: the chapter Double-ended priority queues, by Sartaj Sahni, the section on deaps
---

A deap is an array structure for the [double-ended priority queue](/double-ended-priority-queue/), due to Carlsson (1987). It is a [complete binary tree](/complete-binary-tree/) stored level by level in an array, whose root is empty. The left subtree of the root is a min-heap and the right subtree is a max-heap. Each node $i$ of the min-heap has a partner $j$ in the max-heap at the same place in the right subtree, or the parent of that place if it does not exist, and the deap asks that $A[i] \le A[j]$. Then the minimum is the left child of the root and the maximum is the right child, so the finds take $O(1)$ time, and insert, extract-min and extract-max take $O(\log n)$ time with one pass up or one pass down and up.

## In plain words

Take a tree in the shape of a heap, and leave its top cell empty. Under the top there are two halves. In the left half the smallest key is on top, as in a min-heap. In the right half the largest key is on top, as in a max-heap.

Each cell on the left has a twin on the right, at the same spot in the mirror half. The rule is that a key on the left is never larger than its twin on the right. So every key on the left is at most the largest key, and every key on the right is at least the smallest key. A new key goes in at the end; if it breaks the rule with its twin, the two swap sides, and then the key moves up in its own half.

## The abstract type

A deap implements the [double-ended priority queue](/double-ended-priority-queue/): INSERT, FIND-MIN, FIND-MAX, EXTRACT-MIN and EXTRACT-MAX on a multiset of keys from a [total order](/total-order/).

## Representation

The keys are in $A[2 \ldots n]$, a 1-based array whose cell 1, the root, holds no key; so the deap holds $n - 1$ keys. The parent of $i$ is $\lfloor i/2 \rfloor$, as in a binary heap. Let $k = \lfloor \lg i \rfloor$ be the level of $i \ge 2$. The node $i$ is in the *min side*, the subtree of 2, if $2^k \le i < 2^k + 2^{k-1}$, and in the *max side*, the subtree of 3, else.

- For a max node $j$, its partner is $\mathrm{MIN\text{-}PARTNER}(j) = j - 2^{k-1}$, which always exists.
- For a min node $i$, let $j = i + 2^{k-1}$; its partner is $\mathrm{MAX\text{-}PARTNER}(i) = j$ if $j \le n$, and $\lfloor j/2 \rfloor$ else.

The invariants:

- **(L)** the min side is a min-heap: $A[\lfloor i/2 \rfloor] \le A[i]$ for each min node $i \ge 4$;
- **(R)** the max side is a max-heap: $A[\lfloor j/2 \rfloor] \ge A[j]$ for each max node $j \ge 6$;
- **(C)** $A[i] \le A[\mathrm{MAX\text{-}PARTNER}(i)]$ for each min node $i$, when $n \ge 3$.

For $n = 13$, the levels are 2 and 3; 4, 5 on the min side and 6, 7 on the max side; and 8 to 11 on the min side and 12, 13 on the max side. The node 9 has the partner 13, the node 10 has the place 14, which does not exist, so its partner is 7.

## Operations

```pseudo id=main
INSERT(x)
L1  n ← n + 1; A[n] ← x; if n = 2 then return
L2  if n is a max node then i ← MIN-PARTNER(n)
L3      if x < A[i] then A[n] ← A[i]; MIN-SIFT-UP(i, x) else MAX-SIFT-UP(n, x)
L4  else j ← MAX-PARTNER(n)
L5      if A[j] < x then A[n] ← A[j]; MAX-SIFT-UP(j, x) else MIN-SIFT-UP(n, x)

MIN-SIFT-UP(i, x)                          ▷ the cell i is a hole for x
L6  while i > 3 and x < A[⌊i/2⌋] do A[i] ← A[⌊i/2⌋]; i ← ⌊i/2⌋
L7  A[i] ← x

MAX-SIFT-UP(j, x)
L8  while j > 3 and A[⌊j/2⌋] < x do A[j] ← A[⌊j/2⌋]; j ← ⌊j/2⌋
L9  A[j] ← x

EXTRACT-MIN()
L10 if n < 2 then error "underflow"; r ← A[2]; x ← A[n]; n ← n − 1
L11 if n < 2 then return r; if n = 2 then A[2] ← x; return r
L12 i ← 2; while 2i ≤ n do: c ← the smaller child of i; A[i] ← A[c]; i ← c
L13 j ← MAX-PARTNER(i)
L14 if A[j] < x then A[i] ← A[j]; MAX-SIFT-UP(j, x) else MIN-SIFT-UP(i, x)
    return r

EXTRACT-MAX()
L15 if n < 2 then error "underflow"; if n = 2 then n ← 1; return A[2]
L16 r ← A[3]; x ← A[n]; n ← n − 1
L17 if n = 2 then return r
L18 j ← 3; while 2j ≤ n do: c ← the larger child of j; A[j] ← A[c]; j ← c
L19 i ← MIN-PARTNER(j); if 2i ≤ n then i ← the larger child of i
L20 if x < A[i] then A[j] ← A[i]; MIN-SIFT-UP(i, x) else MAX-SIFT-UP(j, x)
    return r
```

**Insert.** The new cell $n$ is a leaf. If it is a max node, its partner $i$ is a min node; if $x$ is smaller, then $x$ belongs to the min side, so the key $A[i]$ moves across to the cell $n$, and $x$ goes up the min side from $i$. Else $x$ goes up the max side from $n$. The case of a min node is the mirror image.

**Extract-min.** The minimum is $A[2]$. The hole at 2 goes down the min side, always to the smaller child, until it reaches a leaf $i$, as in the bottom-up heap delete. The last key $x$ is then placed: if it is larger than the partner $j$ of $i$, then $A[j]$ moves into the hole and $x$ goes up the max side from $j$; else $x$ goes up the min side from $i$.

**Extract-max.** The mirror image, with one more step in line L19: a max leaf $j$ can have a min partner $i$ that still has children, because the last level fills from the left. Those children have $j$ as their partner, so $x$ must be compared with the larger of them.

## Example

Start with the deap $A[2 \ldots 12] = [5, 45, 10, 8, 25, 40, 15, 19, 9, 30, 20]$: the min side holds 5; 10, 8; 15, 19, 9, 30, and the max side holds 45; 25, 40; 20.

| step | $A[2 \ldots n]$ | what happens |
|---|---|---|
| INSERT(4) | [4, 45, 5, 8, 25, 40, 15, 10, 9, 30, 20, 19] | cell 13 is a max node; its partner 9 holds 19 > 4, so 19 moves to 13, and 4 goes up the min side from 9 past 10 and 5 |
| INSERT(50) | [4, 50, 5, 8, 25, 45, 15, 10, 9, 30, 20, 19, 40] | cell 14 has the partner 10 with 9 ≤ 50, so 50 goes up the max side past 40 and 45 |
| EXTRACT-MIN | [5, 50, 10, 8, 40, 45, 15, 19, 9, 30, 20, 25] | returns 4; $x = 40$; the hole goes down 2, 4, 9; the partner 13 holds 19 < 40, so 19 moves to 9 and 40 goes up from 13 past 25 |
| EXTRACT-MAX | [5, 45, 10, 8, 40, 30, 15, 19, 9, 25, 20] | returns 50; $x = 25$; the hole goes down 3, 7; the partner 5 has the children 9 and 30, so $x$ is compared with 30; 30 moves to 7 and 25 takes its cell 11 |

In the last step, a comparison with the partner 5 alone, which holds 8, would put 25 at the leaf 7, and the min node 11 with 30 would then break (C), since its partner is 7.

## Correctness

The three invariants imply that $A[2]$ is the minimum and $A[3]$ the maximum: each max key is at least the key of its min partner, which is at least $A[2]$ by (L), and each min key is at most the key of its max partner, which is at most $A[3]$ by (R). INSERT places the new key on the side where (C) allows it, and a sift-up on that side keeps (L) or (R); a key that moves up only becomes more extreme for its side, so (C) still holds along the path. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| FIND-MIN, FIND-MAX | $O(1)$ |
| INSERT | $O(\log n)$, at most $\lfloor \lg n \rfloor$ comparisons |
| EXTRACT-MIN, EXTRACT-MAX | $O(\log n)$, at most about $2 \lg n$ comparisons |

The tree has height $\lfloor \lg n \rfloor$, so each side has height less by one. INSERT does one comparison with the partner and at most one per level in the sift-up. The extracts do one comparison per level on the way down, two or three at the bottom, and one per level on the way up. The space is the array; the empty root wastes one cell. The partner of a node is computed with a shift and a subtraction.

## Variants

- **Interval heap.** The [interval heap](/interval-heap/) pairs the keys inside a node instead of across two subtrees, and is simpler to code.
- **Min-max heap.** The [min-max heap](/min-max-heap/) alternates min and max levels in one tree.
- **Twin heaps and correspondences.** A min-heap and a max-heap can also be kept as two separate arrays with a correspondence between their leaves, which is the general method of which the deap is one case.

## When to use it

Use a deap for a DEPQ in an array with $O(1)$ finds and $O(\log n)$ updates, for example a bounded buffer of candidates where the worst is dropped and the best is used. In new code the interval heap does the same with simpler index arithmetic, so the deap is mostly of interest as a teaching example of a correspondence between two heaps.

## Pitfalls

- **The partner past the end.** For a min node near the end of the last level, $i + 2^{k-1}$ can exceed $n$; the partner is then the parent of that place.
- **The partner with children.** In EXTRACT-MAX, a max leaf can have a min partner that is not a leaf. Comparing only with the partner breaks (C) for its children, as the example shows.
- **The empty root.** The loop tests $i > 3$ and $j > 3$, so that no key ever moves into the cell 1.
- **Small sizes.** With one key, the max side is empty and $A[2]$ is both the minimum and the maximum; the code must not read $A[3]$.

## Implementations

The Python class `Deap` keeps a list `a` with `a[0]` and `a[1]` unused, so that positions match the 1-based pseudocode. `is_max_node`, `min_partner` and `max_partner` compute the sides and partners with bit operations; `insert`, `extract_min` and `extract_max` follow the pseudocode, and `check_invariant` checks (L), (R) and (C). Keys need only the operation "<".

## History

Carlsson introduced the deap in 1987 in Information Processing Letters, one year after the min-max heap of Atkinson, Sack, Santoro and Strothotte. The interval heap of van Leeuwen and Wood (1993) later gave the same bounds with simpler code. The deap is a standard example in the data structures textbooks of Horowitz, Sahni and their coauthors.

## References
