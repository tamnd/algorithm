---
tag: E1PH4P
kind: data-structure
slug: randomized-heap
name: Randomized heap
aliases:
- Randomized Heap
area: data-structures/heaps
level: advanced
summary: A mergeable heap that merges by randomly choosing which child to descend into, giving expected logarithmic insert, merge and extract-min.
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heaps}
  time: {worst: O(n), expected: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [heap-property, binary-tree, randomized-algorithm, expected-running-time]
see_also: [skew-heap, leftist-heap, meldable-priority-queue, pairing-heap, randomized-algorithm, linearity-of-expectation, binomial-heap, treap]
sources:
  - paper: Anna Gambin and Adam Malinowski, Randomized meldable priority queues, SOFSEM'98, Theory and Practice of Informatics, Lecture Notes in Computer Science 1521, Springer, 1998
    locator: the randomized meld that descends into a random child, and the expected O(log n) bound for meld, insert, delete-min, decrease-key and delete
  - paper: Daniel Dominic Sleator and Robert Endre Tarjan, Self-adjusting heaps, SIAM Journal on Computing 15(1), 1986
    locator: the skew heap, the deterministic structure of the same shape that this heap randomizes
---

A randomized heap, or randomized meldable heap, is a heap-ordered binary tree whose meld walks down from the two roots and, at each node, flips a fair coin to choose the child that the rest is melded into. There is no balance field, and the tree can have any shape. Yet for every tree, a random walk from the root reaches an empty subtree after at most $\lg(n + 1)$ steps on average, so each meld, insert and delete-min takes $O(\log n)$ expected time, for every single operation and every input. Anna Gambin and Adam Malinowski described it in 1998.

## In plain words

To join two heaps, start at the two tops and keep the smaller item. Then the larger top must go somewhere below the smaller one. A [skew heap](/skew-heap/) or a [leftist heap](/leftist-heap/) always sends it down the right side, and has to manage the shape so that this side stays short.

A randomized heap tosses a coin instead: heads, go left; tails, go right. It does not look at the shape at all. Even if the tree is very lopsided, a walk that picks a random side at each step tends to fall off the tree quickly, because the side that is big is also the side that is less likely to be chosen again and again. So joins are fast on average, for every shape.

## The abstract type

A randomized heap implements the [meldable priority queue](/meldable-priority-queue/) on a multiset of keys from a total order: `insert(H, k)`, `find-min(H)`, `delete-min(H)` and `meld(H1, H2)`, which destroys its inputs. With parent pointers it also supports `decrease-key` and `delete` of an item given by a handle. This page uses a min-heap.

## Representation

Each node holds a key and two pointers, $left$ and $right$. The heap is a pointer $H.root$ and a count $n$. The heap also has a source of random bits, which must not depend on the keys.

**Invariant (heap order).** The key of each node is at least the key of its parent.

Any heap-ordered binary tree is a valid randomized heap. The analysis does not need any property of the shape.

## Operations

```pseudo id=main
MELD(a, b)                              ▷ roots of two heaps; either may be NIL
L1  if a = NIL then return b; if b = NIL then return a
L2  if b.key < a.key then swap a and b  ▷ a has the smaller root
L3  c ← left or right, each with probability 1/2, independent of all else
L4  a.c ← MELD(a.c, b)
L5  return a

INSERT(H, k)
L6  H.root ← MELD(H.root, a new node with key k)

DELETE-MIN(H)                           ▷ H is not empty
L7  x ← H.root; H.root ← MELD(x.left, x.right)
L8  return x.key
```

**Meld** (lines L1 to L5) keeps the smaller root, picks one of its children at random, and melds the other heap into that child. The calls form a *meld path* that goes down through both trees. It ends when the chosen child is empty, and the remaining heap is attached there.

**Insert** (line L6) melds with a one-node heap. **Delete-min** (lines L7 and L8) melds the two subtrees of the root. **Find-min** returns the root key.

**Decrease-key and delete.** With a parent pointer in each node, decrease-key lowers the key, cuts the subtree of the node from its parent, and melds it with the root. Delete cuts the node out, melds its two subtrees, and melds the result with the root. Each is $O(1)$ work plus one or two melds.

## Example

Write a tree as key(left, right), with "-" for an empty subtree and a leaf as its key alone. Meld $x$ = 2(6, 4(9, -)) with $y$ = 3(5, -), and let the coin give right, left, right.

| call | roots | smaller | coin | next call |
|---|---|---|---|---|
| 1 | 2, 3 | 2 | right | MELD(4(9, -), 3(5, -)) into the right of 2 |
| 2 | 4, 3 | 3 | left | MELD(5, 4(9, -)) into the left of 3 |
| 3 | 5, 4 | 4 | right | MELD(-, 5) into the right of 4, which returns 5 |

The result is 2(6, 3(4(9, 5), -)), after 3 comparisons. With the coins left, right instead, the first call melds 3(5, -) into the left child 6, so 3 becomes the left child of 2, and then 6 goes into the empty right child of 3: the result is 2(3(5, 6), 4(9, -)), after 2 comparisons. Both are valid heaps with the same keys; the coins change only the shape.

## Correctness

MELD returns a heap-ordered tree with the keys of both inputs, for every result of the coins. The proof is the same induction as for the skew heap: line L2 puts a smallest key at the root, the recursive call returns a heap-ordered tree of the other keys, and all of them are at least the root. Delete-min removes the root, which holds a smallest key. Randomness affects only the shape and the time, not the result. The full proof, with the bound on the expected time, is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | expected | worst case |
|---|---|---|
| find-min | $O(1)$ | $O(1)$ |
| meld | at most $\lg(n_1 + 1) + \lg(n_2 + 1) + 1$ calls | $O(n_1 + n_2)$ |
| insert | at most $\lg(n + 1) + 2$ calls | $O(n)$ |
| delete-min | at most $2 \lg n + 1$ calls | $O(n)$ |
| decrease-key, delete | $O(\log n)$ | $O(n)$ |
| space | $\Theta(n)$: a key and two pointers per node | |

**The random walk lemma.** In a binary tree $T$ with $m$ nodes, let a walk start at the root and go to a random child, left or right with probability $1/2$ each, until it reaches an empty subtree. Let $E(T)$ be the expected number of nodes it visits. Then $E(T) \le \lg(m + 1)$. The proof is by induction: for a root with subtrees of $\ell$ and $r$ nodes,
$$E(T) = 1 + \tfrac12 E(L) + \tfrac12 E(R) \le 1 + \tfrac12 \lg(\ell + 1) + \tfrac12 \lg(r + 1) \le 1 + \lg\frac{\ell + r + 2}{2} = \lg(m + 1),$$
where the second step uses that $\lg$ is concave. The bound is exact for a complete tree with $m = 2^h - 1$, and it holds for every shape, also for a path.

**Meld.** The nodes of the meld path that come from $x$ are a prefix of a random walk in $x$: from each such node, the coin of line L3 decides which child of it the path meets next. The same holds for $y$, with other coins. So the expected number of calls is at most $1 + E(x) + E(y) \le \lg(n_1 + 1) + \lg(n_2 + 1) + 1$, by [linearity of expectation](/linearity-of-expectation/). The bound holds for every shape, so it holds for every operation of every sequence, as long as the sequence does not depend on the coins.

## Variants

- **Skew heap.** The [skew heap](/skew-heap/) is the deterministic relative: it always melds into one side and swaps the children, which gives $O(\log n)$ amortized time instead of expected time per operation.
- **Leftist heap.** The [leftist heap](/leftist-heap/) stores a rank at each node and gets $O(\log n)$ worst-case time.
- **Treap-like heaps.** A [treap](/treap/) also combines heap order with random choices, but there the priorities are random and the keys are in search-tree order, so it answers searches, not delete-min of the keys.

## When to use it

Use a randomized heap when you want a meldable heap with very short code, no balance field and no amortization: each operation is fast in expectation on its own, so it is fine with persistence or with old versions in a functional program, where a [skew heap](/skew-heap/) loses its bound. It also supports decrease-key and delete with only parent pointers. If you need guarantees per operation that do not depend on luck, use a [leftist heap](/leftist-heap/) or a [binomial heap](/binomial-heap/). If only insert and delete-min are needed, a [binary heap](/binary-heap/) in an array is faster.

## Pitfalls

- **Coins that depend on the data.** The analysis needs fresh coins, independent of the keys and of the shape. A coin that is a function of the key, for example its lowest bit, lets an adversary build inputs with long meld paths.
- **An adaptive adversary.** If the sequence of operations can depend on the shape that the coins produced, for example by a user who can see the tree, the expected bound no longer holds.
- **Recursion.** The expected meld path is short, but the worst case is linear. A recursive MELD can, with small probability, use a deep stack. Use a loop.
- **Reproducible tests.** A heap seeded from the clock gives different shapes on each run. Tests should inject a seeded source or a scripted coin, as the Python tests do.

## Implementations

The Python version takes the coin as an object with a `random()` method, so the tests can give it a fixed script of left and right moves. MELD is a loop that keeps the last node of the meld path.

## History

Anna Gambin and Adam Malinowski presented randomized meldable priority queues at SOFSEM in 1998. The structure is the randomized form of the skew heap of Sleator and Tarjan of 1986, and it replaces the amortized analysis of the potential function by the expected length of a random walk. Pat Morin uses it as the meldable heap of his textbook Open Data Structures.

## References
