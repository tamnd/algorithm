---
tag: PY5NQC
kind: data-structure
slug: skew-heap
name: Skew heap
aliases:
- self-adjusting heap
area: data-structures/heaps
level: advanced
summary: Self-adjusting leftist-style heap with amortized O(log n) merge and no balance bookkeeping.
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heaps}
  time: {worst: O(n), amortized: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [leftist-heap, heap-property, binary-tree, potential-method]
see_also: [leftist-heap, pairing-heap, splay-tree, meldable-priority-queue, randomized-heap, binomial-heap, fibonacci-heap, amortized-cost]
sources:
  - paper: Daniel Dominic Sleator and Robert Endre Tarjan, Self-adjusting heaps, SIAM Journal on Computing 15(1), 1986
    locator: pages 52 to 69 (top-down skew heaps with the heavy-node potential, and bottom-up skew heaps with O(1) amortized insert and meld)
  - paper: Anne Kaldewaij and Berry Schoenmakers, The derivation of a tighter bound for top-down skew heaps, Information Processing Letters 37(5), 1991
    locator: the bound of about log_φ n amortized comparisons per operation, and its tightness
  - book: isbn:9780898711875
    title: Robert Endre Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 3 (Heaps), the leftist heaps that skew heaps simplify
---

A skew heap is a heap-ordered binary tree that is merged like a [leftist heap](/leftist-heap/), down the right paths of the two trees, but with no rank or balance field: at every node of the merge path it swaps the two children. A single merge is bounded only by $O(n)$ time, but any sequence of operations takes $O(\log n)$ amortized time per insert, delete-min and meld. Daniel Sleator and Robert Tarjan introduced it in 1986, at the same time as the [splay tree](/splay-tree/), as an example of a *self-adjusting* structure, which gets good amortized bounds from a simple local rule.

## In plain words

To join two heaps, walk down the right side of both, always taking the smaller item next, and zip the two paths into one. A leftist heap keeps a count at each item to make sure the right side stays short.

A skew heap does not keep any count. Instead, at each item it passes on the way down, it swaps the left and the right side. The side that just got longer moves to the left, out of the way of the next join. A single join can still be slow, if the right side happens to be long. But that slow join swaps all those items, so the right side becomes short for the next joins. Over many operations, the work per operation stays small.

## The abstract type

A skew heap implements the [meldable priority queue](/meldable-priority-queue/) on a multiset of keys from a total order: `insert(H, k)`, `find-min(H)`, `delete-min(H)` and `meld(H1, H2)`, which destroys its inputs. This page uses a min-heap.

## Representation

Each node holds a key and two pointers, $left$ and $right$. There is no rank, size or color field. The heap is a pointer $H.root$ and a count $n$.

**Invariant (heap order).** The key of each node is at least the key of its parent.

Any binary tree in heap order is a valid skew heap. The shape is not controlled at all; only the amortized analysis limits how bad the shape can become for the operations.

## Operations

```pseudo id=main
MERGE(a, b)                             ▷ roots of two skew heaps; either may be NIL
L1  if a = NIL then return b; if b = NIL then return a
L2  if b.key < a.key then swap a and b  ▷ a has the smaller root
L3  r ← a.right
L4  a.right ← a.left                    ▷ swap the children of a ...
L5  a.left ← MERGE(r, b)                ▷ ... and merge into the side that was on the right
L6  return a

INSERT(H, k)
L7  H.root ← MERGE(H.root, a new node with key k)

DELETE-MIN(H)                           ▷ H is not empty
L8  x ← H.root; H.root ← MERGE(x.left, x.right)
L9  return x.key
```

**Merge** (lines L1 to L6) keeps the smaller root $a$, merges the other heap with the old right subtree of $a$, and puts the result on the left, with the old left subtree moved to the right. The recursion goes down the right paths of both heaps. It stops when one of them is empty, and the other is then attached without changes. The number of calls is the length of the *merge path*.

**Insert** (line L7) is a merge with a one-node heap. **Delete-min** (lines L8 and L9) merges the two subtrees of the root. **Find-min** returns the root key.

The merge path is bounded only by $n$, so a program should not use recursion for MERGE. The loop form keeps a pointer to the last node on the merge path and writes the next smaller root into its left field.

## Example

Write a tree as key(left, right), with "-" for an empty subtree and a leaf as its key alone. Insert 5, 3, 8, 1, 7, 2 into an empty heap.

| operation | merge path | tree after |
|---|---|---|
| insert 5 | | 5 |
| insert 3 | 3: swap its empty children, merge 5 into the left | 3(5, -) |
| insert 8 | 3: right $\leftrightarrow$ left, merge(-, 8) on the left | 3(8, 5) |
| insert 1 | 1: merge 3(8, 5) into its left | 1(3(8, 5), -) |
| insert 7 | 1: old left 3(8, 5) moves right, merge(-, 7) on the left | 1(7, 3(8, 5)) |
| insert 2 | 1: old left 7 moves right; merge(3(8, 5), 2): 2 wins, gets 3(8, 5) on its left | 1(2(3(8, 5), -), 7) |

The insert of 8 shows the difference from a leftist heap: there, 3(5, 8) keeps 5 on the left; here, the swap puts the new key on the left. Delete-min then returns 1 and merges 2(3(8, 5), -) with 7. The root 2 wins, its left child 3(8, 5) moves to the right, and merge(-, 7) goes on the left: 2(7, 3(8, 5)).

**A meld.** Merge $x$ = 1(2(3(5, -), -), 7(8, -)) with $y$ = 4(6(10, -), 9).

1. 1 < 4: root 1. Its left 2(3(5, -), -) moves to the right. Merge its old right 7(8, -) with $y$, into the left of 1.
2. 4 < 7: node 4. Its left 6(10, -) moves to the right. Merge its old right 9 with 7(8, -), into the left of 4.
3. 7 < 9: node 7. Its left 8 moves to the right. Its old right is empty, so 9 goes on the left, and the merge ends.

The result is 1(4(7(9, 8), 6(10, -)), 2(3(5, -), -)). The merge path is 1, 4, 7, with 3 comparisons. All three nodes had their children swapped.

## Correctness

Each MERGE call returns a heap-ordered tree with the keys of both inputs. By induction on the number of nodes: line L2 makes the root a smallest key of both trees, the recursive call at line L5 returns a heap-ordered tree with the remaining keys, and every key in it is at least the root. Swapping two subtrees does not change heap order. Delete-min removes the root, which is a smallest key, and merges the two subtrees. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case | amortized |
|---|---|---|
| find-min | $O(1)$ | $O(1)$ |
| insert | $O(n)$ | $O(\log n)$ |
| delete-min | $O(n)$ | $O(\log n)$ |
| meld | $O(n)$ | $O(\log n)$ |
| space | $\Theta(n)$: a key and two pointers per node | |

**Worst case of one operation.** Nothing limits the length of a right path, so the only bound for one merge is the number of nodes, $O(n)$. A long merge swaps the children of every node on its path, and the heavy nodes on it become light, which is how the amortized analysis pays for it.

**The amortized bound.** Sleator and Tarjan use the [potential method](/potential-method/). Let $s(x)$ be the number of nodes in the subtree of $x$. Call $x$ *heavy* if $s(x.right) > s(x.left)$, and *light* otherwise. The potential $\Phi$ is the number of heavy nodes.

- On a right path, each light node has a right subtree with less than half of its nodes, so a right path of a tree with $m$ nodes has at most $\lfloor \lg m \rfloor + 1$ light nodes.
- A merge visits $h$ heavy and $\ell$ light nodes on the right paths of its two inputs, and swaps the children of each of them. A heavy node $x$ on the path becomes light: its old right subtree, now merged with more nodes, is on the left, and its old left subtree, the smaller one, is on the right. A light node may become heavy. Nodes off the path keep their subtrees.
- So the actual cost is $h + \ell$, and $\Phi$ changes by at most $\ell - h$. The amortized cost is at most $2\ell \le 2(\lg n_1 + \lg n_2) + 4 \le 4 \lg n + O(1)$.

Delete-min removes the root, which does not increase $\Phi$, and does one merge. The full proof is in [the complexity proof](proofs/complexity.md). Kaldewaij and Schoenmakers later found the tight constant: about $\log_\varphi n \approx 1.44 \lg n$ amortized comparisons per merge, where $\varphi$ is the golden ratio.

## Variants

- **Bottom-up skew heap.** Sleator and Tarjan also describe a version that keeps pointers to the bottom of the right paths and merges from the bottom up. It takes $O(1)$ amortized time for insert and meld and $O(\log n)$ amortized time for delete-min.
- **Purely functional skew heap.** With MERGE as a function that builds new nodes, the old versions stay valid. The amortized bound then holds only if no old version is used again, because the analysis charges future operations; a [leftist heap](/leftist-heap/) has worst-case bounds and does not have this problem.
- **Randomized heap.** The [randomized heap](/randomized-heap/) chooses at random which subtree to merge into, and gets $O(\log n)$ expected time for every single operation.

## When to use it

Use a skew heap when you need a meldable heap and want the least code: merge is six lines and the nodes hold no extra field. It is a good choice for a merge-heavy program, such as a simulation or a graph algorithm that melds sets of edges, in which the total time matters and not the time of each operation. Do not use it in a real-time system that needs a bound on each operation, or with persistence, where old versions are reused; use a [leftist heap](/leftist-heap/) there. When only insert and delete-min are needed, a [binary heap](/binary-heap/) in an array is faster.

## Pitfalls

- **Recursion.** The length of a merge path is not bounded by $O(\log n)$, only by $n$, so a recursive MERGE can need a deep stack. Use a loop.
- **Swapping at the wrong time.** The swap must put the merged subtree on the left and the old left subtree on the right, as in lines L3 to L5. Swapping before choosing which subtree to merge into merges into the old left subtree and loses the amortized bound.
- **Reusing old versions.** The amortized bound counts the potential of one current heap. If a program keeps copies of old heaps and operates on them again, the same expensive merge can be repeated many times.
- **Worst-case latency.** A single operation has no bound better than $O(n)$. Code that needs a bound per operation must not use a skew heap.

## Implementations

The Python version does MERGE with a loop that holds the last node of the merge path. It also has a `heavy_count` method, which computes the potential of the analysis, used in the tests.

## History

Sleator and Tarjan published the skew heap in 1986 in the SIAM Journal on Computing, in a paper on self-adjusting heaps, a year after their paper on splay trees. They presented it as a simpler form of Crane's leftist heap, in which the rule "swap if the right side is too heavy" becomes "always swap". The name comes from the skewed shapes the trees can take. Kaldewaij and Schoenmakers derived the tight amortized constant in 1991.

## References
