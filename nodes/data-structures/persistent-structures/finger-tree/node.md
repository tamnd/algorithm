---
tag: BJ50ZK
kind: data-structure
slug: finger-tree
name: Finger tree
aliases:
- Hinze-Paterson finger tree
area: data-structures/persistent-structures
level: advanced
summary: A persistent balanced sequence with amortized O(1) access at both ends and O(log n) split and concatenation.
implements: [deque, list]
model: pointer-machine
complexity:
  vars: {n: the number of items}
  time: {worst: O(log n), amortized: O(1)}
  space: {extra: Θ(n)}
history:
  year: 2006
  people: [Ralf Hinze, Ross Paterson]
  note: Hinze and Paterson published the 2-3 finger tree with measures in the Journal of Functional Programming in 2006, as a simpler form of earlier purely functional deques and finger search trees.
prereqs: [two-three-tree, deque, monoid, purely-functional-data-structure]
see_also: [catenable-deque, finger-search-tree, binary-random-access-list, persistent-vector, rope, banker-queue, confluent-persistence, priority-queue]
sources:
  - paper: doi:10.1017/S0956796805005769
    title: Ralf Hinze and Ross Paterson, Finger trees, a simple general-purpose data structure, Journal of Functional Programming 16(2), 2006
    locator: pages 197 to 217 (the deque operations, concatenation, measures as monoids, and splitting, with the amortized bounds)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 11, Implicit Recursive Slowdown (implicit deques, whose structure of digits and a middle deque of pairs the finger tree follows)
  - paper: doi:10.1145/324133.324139
    title: Haim Kaplan and Robert E. Tarjan, Purely functional, real-time deques with catenation, Journal of the ACM 46(5), 1999
    locator: pages 577 to 603 (catenable deques with worst-case O(1) operations by recursive slowdown)
---

A finger tree is a [purely functional](/purely-functional-data-structure/) sequence that gives fast access at both ends and fast splitting and concatenation. The version of Hinze and Paterson stores the items in a spine of levels. Each level has a short *prefix* and *suffix* of one to four elements, and a middle finger tree whose elements are [2-3 tree](/two-three-tree/) nodes of the next level. Adding or removing an item at either end takes $O(1)$ amortized time, and appending two trees or splitting a tree at a position takes logarithmic time. If each node also stores a summary of its items in a [monoid](/monoid/), such as a size or a maximum, the same tree becomes an indexed sequence, a priority queue or an ordered set. Haskell's `Data.Sequence` is a finger tree measured by size.

## In plain words

Picture a sequence held at its two ends, like a string of beads held in two hands. The few beads nearest each hand are kept loose, so taking one or adding one is quick. The beads further in are tied into small bundles of two or three. The bundles further in still are tied into bundles of bundles, and so on toward the center. So the outer layers are thin and quick to change, and the inner layers pack more and more beads into few bundles.

To join two strings, only the loose beads where they meet must be re-tied, one layer at a time. To cut a string at some position, a bundle on each layer is opened. Both jobs touch one bundle per layer, and there are only about as many layers as the number of digits of the length in binary.

## The abstract type

The structure holds a sequence $\langle x_1, \ldots, x_n \rangle$. Every operation returns new sequences and leaves its arguments unchanged.

- `cons(a, s)` and `snoc(s, a)` add $a$ at the front or the back.
- `viewl(s)` returns nothing for the empty sequence, and otherwise $x_1$ and $\langle x_2, \ldots, x_n \rangle$; `viewr` is the mirror image.
- `append(s, t)` returns the concatenation of $s$ and $t$.
- `split_at(i, s)` returns $\langle x_1, \ldots, x_i \rangle$ and $\langle x_{i+1}, \ldots, x_n \rangle$.
- `lookup(i, s)` returns $x_{i+1}$, the item at position $i$, counting from 0.

So it implements a [deque](/deque/) with catenation and a [list](/list/) with access by position.

## Representation

An *element of level 0* is an item. An *element of level* $k + 1$ is a node $\text{Node2}(y_1, y_2)$ or $\text{Node3}(y_1, y_2, y_3)$ whose children are elements of level $k$. Each node caches its *size*, the number of items below it, and an item has size 1. A *digit* of level $k$ is a sequence of 1 to 4 elements of level $k$.

A *finger tree of level* $k$ is one of

- $\text{Empty}$;
- $\text{Single}(x)$, where $x$ is an element of level $k$;
- $\text{Deep}(pr, m, sf)$, where the prefix $pr$ and the suffix $sf$ are digits of level $k$ and the middle $m$ is a finger tree of level $k + 1$. A Deep tree caches its size.

The sequence of a tree is read from left to right: the items of $pr$, then those of $m$, then those of $sf$. A finger tree for the user is a tree of level 0.

**Invariant.** (F1) Every node has 2 or 3 children, all of the level below, and every digit has 1 to 4 elements. (F2) A tree of level $k$ holds only elements of level $k$ in its digits and singles, and its middle is of level $k + 1$. (F3) Every cached size is the number of items below.

An element of level $k$ is a complete 2-3 tree of height $k$, so it holds at least $2^k$ items. A tree whose spine has $d$ Deep levels has a Deep tree at level $d - 1$, with two digits of elements of that level, so $n \ge 2^d$ and the depth is at most $\lg n$.

## Operations

SNOC, VIEWR and DEEPR are the mirror images of CONS, VIEWL and DEEPL. APPEND$(t_1, t_2)$ is APP3$(t_1, [\,], t_2)$, and SPLIT-AT$(i, t)$ for $0 < i < n$ is $(l, \text{CONS}(x, r))$ with $(l, x, r) = \text{SPLIT-TREE}(i, t)$. The size of a digit or a list of elements is the sum of their sizes.

```pseudo id=main
CONS(a, t)                                ▷ a is an element of the level of t
L1  if t = Empty then return Single(a)
L2  if t = Single(b) then return Deep([a], Empty, [b])
L3  Deep(pr, m, sf) ← t
L4  if pr = [b, c, d, e] then return Deep([a, b], CONS(Node3(c, d, e), m), sf)
L5  return Deep([a] ++ pr, m, sf)

CONS-ALL(xs, t)
L6  for x in xs, from the last to the first do t ← CONS(x, t); return t
SNOC-ALL(t, xs)
L7  for x in xs, from the first to the last do t ← SNOC(t, x); return t
TREE-OF(xs)
L8  return CONS-ALL(xs, Empty)

VIEWL(t)                                  ▷ nil, or the first element and the rest
L9  if t = Empty then return nil
L10 if t = Single(a) then return (a, Empty)
L11 Deep([a] ++ pr, m, sf) ← t
L12 return (a, DEEPL(pr, m, sf))

DEEPL(pr, m, sf)                          ▷ as Deep, but pr may be empty
L13 if pr ≠ [ ] then return Deep(pr, m, sf)
L14 if VIEWL(m) = nil then return TREE-OF(sf)
L15 (n, m′) ← VIEWL(m); return Deep(the children of n, m′, sf)

NODES(xs)                                 ▷ 2 to 12 elements; returns 1 to 4 nodes
L16 if xs = [a, b] then return [Node2(a, b)]
L17 if xs = [a, b, c] then return [Node3(a, b, c)]
L18 if xs = [a, b, c, d] then return [Node2(a, b), Node2(c, d)]
L19 [a, b, c] ++ rest ← xs; return [Node3(a, b, c)] ++ NODES(rest)

APP3(t1, ts, t2)                          ▷ t1, then the elements ts, then t2
L20 if t1 = Empty then return CONS-ALL(ts, t2)
L21 if t2 = Empty then return SNOC-ALL(t1, ts)
L22 if t1 = Single(x) then return CONS(x, CONS-ALL(ts, t2))
L23 if t2 = Single(x) then return SNOC(SNOC-ALL(t1, ts), x)
L24 Deep(pr1, m1, sf1) ← t1; Deep(pr2, m2, sf2) ← t2; return Deep(pr1, APP3(m1, NODES(sf1 ++ ts ++ pr2), m2), sf2)

LOCATE(i, xs)                             ▷ 0 ≤ i < size(xs)
L25 k ← the least k with i < size(xs[1 .. k]); return (k, i − size(xs[1 .. k − 1]))

SPLIT-TREE(i, t)                          ▷ t ≠ Empty, 0 ≤ i < size(t); returns (l, x, r)
L26 if t = Single(x) then return (Empty, x, Empty)
L27 Deep(pr, m, sf) ← t; if i < size(pr) then (l, x, r) ← pr cut at LOCATE(i, pr); return (TREE-OF(l), x, DEEPL(r, m, sf))
L28 i ← i − size(pr); if i < size(m) then (ml, n, mr) ← SPLIT-TREE(i, m); (l, x, r) ← the children of n cut at LOCATE(i − size(ml), children of n); return (DEEPR(pr, ml, l), x, DEEPL(r, mr, sf))
L29 (l, x, r) ← sf cut at LOCATE(i − size(m), sf); return (DEEPR(pr, m, l), x, TREE-OF(r))

LOOKUP(i, t)                              ▷ 0 ≤ i < size(t)
L30 while t = Deep(pr, m, sf) and size(pr) ≤ i < size(pr) + size(m) do
L31     i ← i − size(pr); t ← m
L32 if t = Single(x) then xs ← [x]
L33 else Deep(pr, m, sf) ← t; xs ← pr ++ sf; if i ≥ size(pr) then i ← i − size(m)
L34 loop: (k, i) ← LOCATE(i, xs); if xs[k] is an item then return xs[k]; xs ← the children of xs[k]
```

Line L4 is the carry of the structure: a full prefix of four elements keeps two and pushes the other three, as one node, into the middle tree. Line L15 is the borrow: an empty prefix takes the first node of the middle tree and spreads its two or three children into a new prefix. Line L24 appends two deep trees by keeping the outer digits and appending the middle trees, with the inner digits and the elements between them packed into at most four nodes of the next level. "Cut at $(k, j)$" splits a list of elements into the elements before position $k$, the element $k$, and the elements after it.

## Example

Snoc the items 1 to 9 onto the empty tree. Nodes are written in parentheses.

| after snoc | tree |
|---|---|
| 1 | $\text{Single}(1)$ |
| 2 | $\text{Deep}([1], \text{Empty}, [2])$ |
| 5 | $\text{Deep}([1], \text{Empty}, [2, 3, 4, 5])$ |
| 6 | $\text{Deep}([1], \text{Single}((2\,3\,4)), [5, 6])$ |
| 8 | $\text{Deep}([1], \text{Single}((2\,3\,4)), [5, 6, 7, 8])$ |
| 9 | $\text{Deep}([1], \text{Deep}([(2\,3\,4)], \text{Empty}, [(5\,6\,7)]), [8, 9])$ |

At the 6th and 9th snoc the suffix is full and three of its elements move down as a node. The tree now has two Deep levels, and a cons of 0 only changes the prefix to $[0, 1]$.

- **split_at(4).** SPLIT-TREE(4) skips the prefix (size 1) and looks for position 3 in the middle tree, whose prefix $(2\,3\,4)$ has size 3, so it finds the node $(5\,6\,7)$ in its suffix, with $ml = \text{Single}((2\,3\,4))$ and $mr = \text{Empty}$. Inside the node, position 0 is the item 5, with $l = [\,]$ and $r = [6, 7]$. The left part is DEEPR$([1], \text{Single}((2\,3\,4)), [\,]) = \text{Deep}([1], \text{Empty}, [2, 3, 4])$, and the right part is CONS$(5, \text{Deep}([6, 7], \text{Empty}, [8, 9])) = \text{Deep}([5, 6, 7], \text{Empty}, [8, 9])$.
- **append.** Appending the right part and the left part, in that order, packs the inner digits $[8, 9]$ and $[1]$ into NODES$([8, 9, 1]) = [(8\,9\,1)]$, which gives $\text{Deep}([5, 6, 7], \text{Single}((8\,9\,1)), [2, 3, 4])$, the sequence $5, 6, 7, 8, 9, 1, 2, 3, 4$. The trees made before are unchanged.
- **lookup(4).** In the tree of nine items, position 4 is not in the prefix, so the loop goes into the middle tree with $i = 3$. That tree's prefix has size 3, and $3 < 3 + 0$ fails, so it stops; $xs = [(2\,3\,4), (5\,6\,7)]$ and $i = 3$. LOCATE picks the node $(5\,6\,7)$ with offset 0, and then the item 5.

## Correctness

Each operation keeps (F1) to (F3) and returns the right sequence. CONS and VIEWL with DEEPL are proved by induction on the depth of the spine: a full prefix sends one node of the right level to the middle tree, and an empty prefix takes one node from it, whose two or three children form a valid digit. NODES turns 2 to 12 elements into 1 to 4 nodes with the same children in order, so APP3, by induction on the depth of $t_1$, keeps the number of elements passed down within 4. SPLIT-TREE and LOOKUP keep the position $i$ relative to the part that is searched. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | strict tree, worst case | with a lazy middle (Hinze and Paterson) |
|---|---|---|
| cons, snoc, viewl, viewr | $O(\log n)$ | $O(1)$ amortized, also under persistence |
| append | $O(\log(n_1 + n_2))$ | $O(\log \min(n_1, n_2))$ amortized |
| split at $i$ | $O(\log^2 n)$ | $O(\log \min(i, n - i))$ amortized |
| lookup $i$ | $O(\log n)$ | $O(\log \min(i, n - i))$ |
| space | $\Theta(n)$ | $\Theta(n)$ |

**Worst case.** The depth is at most $\lg n$. CONS and VIEWL do $O(1)$ work per level and recurse at most once per level. LOOKUP does $O(1)$ work per level in the loop of line L30 and per level of a node in line L34. APP3 does $O(1)$ work per level, and the recursion stops at a level where one tree is Empty or Single, where at most 4 calls of CONS or SNOC, each $O(\log n)$, finish the job. SPLIT-TREE recurses once per level, and at each level calls DEEPL and DEEPR, each $O(\log n)$.

**Amortized, single-threaded.** Call a digit *dangerous* if it has 1 or 4 elements, and let the potential be the number of dangerous digits. A cons that recurses through $j$ levels finds a full prefix at each of them and leaves the prefix $[a, b]$ there, which is safe, so it removes $j$ dangerous digits and creates at most one. Its amortized cost is $O(1)$. The same holds for snoc, viewl and viewr, since a borrow also leaves a digit of 2 or 3 elements. This argument fails under persistence, because the same version can be reused. Hinze and Paterson make the middle tree a lazy, memoized value and show with Okasaki's [debit method](/debit-analysis/) that the bound then holds for every sequence of operations on any versions.

## Variants

- **Measures.** Replace the size by any monoid measure, cached in nodes and Deep trees, and split by a predicate on the prefix measures. With the maximum of priorities the tree is a [priority queue](/priority-queue/); with the largest key it is an ordered sequence that supports merge and partition, as a [finger search tree](/finger-search-tree/) does.
- **Lazy middle.** In a lazy language the middle tree is a suspension, which gives the amortized bounds under persistence.
- **Catenable deques.** Kaplan and Tarjan's [catenable deques](/catenable-deque/) support catenation in $O(1)$ worst-case time but no efficient split.
- **Other indexed sequences.** A [binary random-access list](/binary-random-access-list/) has fast front operations and indexing but no catenation. A [persistent vector](/persistent-vector/) has fast access at the back and by index. A [rope](/rope/) is a balanced tree of strings with logarithmic catenation and split.

## When to use it

Use a finger tree when a persistent sequence needs most of these at once: both ends, concatenation, splitting, and access by position, as in an editor buffer, a functional queue with priorities, or the work list of a parallel program. When only one of these is needed, a simpler structure is faster by a constant factor: a two-list queue for a queue, a vector for indexing.

## Pitfalls

- **The order of children.** CONS pushes $\text{Node3}(c, d, e)$, the last three elements of the prefix, and SNOC pushes the first three of the suffix. Swapping them puts items out of order with no error.
- **Empty digits.** After a split or a view, a prefix can be empty. DEEPL and DEEPR repair it by borrowing from the middle tree; building a Deep tree with an empty digit directly breaks the invariant and the depth bound.
- **NODES with 4 elements.** Four elements must become two Node2, not a Node3 and a single element, since a node needs at least 2 children.
- **Strict middles.** Without laziness, a cons on a tree whose prefixes are all full costs $\Theta(\log n)$, and a program that keeps reusing that version pays it every time.
- **Recomputed sizes.** The sizes must be cached in nodes and Deep trees. Computing them on demand makes lookup and split linear.

## Implementations

The Python version is strict and has no lazy middle. Items, `_Node` objects and the tree classes `_Empty`, `_Single` and `_Deep` cache their sizes, and digits are tuples of 1 to 4 elements. The class `FingerTree` has `cons`, `snoc`, `viewl`, `viewr`, `append`, `split_at`, `lookup` and `check_invariant`. The tests run random operations on random old versions, including appends of two versions, against Python lists.

## History

Guibas, McCreight, Plass and Roberts introduced finger search trees in 1977, with fast access near designated positions. Purely functional deques with catenation followed: Kaplan and Tarjan gave worst-case $O(1)$ catenable deques by recursive slowdown, and Okasaki gave simpler implicit deques by implicit recursive slowdown, in which each level holds digits and a middle deque of pairs. Hinze and Paterson (2006) used 2-3 nodes and a measure in a monoid to get one simple structure for many sequence types.

## References
