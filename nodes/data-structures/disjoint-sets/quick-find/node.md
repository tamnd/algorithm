---
tag: E7GCG2
kind: algorithm
slug: quick-find
name: Quick-find
aliases:
- eager union-find
area: data-structures/disjoint-sets
level: intro
summary: Union-find where every element stores its set id, so find is constant time and union relabels a set.
solves: [dynamic-equivalence-problem]
model: word-ram
complexity:
  vars: {n: the number of elements, m: the number of operations}
  time: {init: Θ(n), find: Θ(1), union: Θ(n), total: O(n + m·n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: true, recursive: false}
prereqs: [disjoint-set, equivalence-relation]
see_also: [quick-union, linked-list-disjoint-sets, disjoint-set-forest, union-by-size, dynamic-equivalence-problem, connected-components]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, Case study, union-find (the quick-find implementation, its trace on tinyUF.txt, and its analysis)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.2, Linked-list representation of disjoint sets (find in O(1) time, union that rewrites the set object of each member)
---

Quick-find is the simplest solution of the [dynamic equivalence problem](/dynamic-equivalence-problem/). It keeps an array `id`, where `id[x]` is the name of the set of $x$. A find reads one entry, so it takes $\Theta(1)$ time. A union of two different sets scans the whole array and renames each member of the first set to the name of the second, so it takes $\Theta(n)$ time. Building one set of $n$ elements costs $\Theta(n^2)$, which is too slow for large inputs. [Quick-union](/quick-union/) makes the opposite trade, and the [disjoint-set forest](/disjoint-set-forest/) makes both operations almost constant.

## In plain words

Each item wears a badge with the name of its group. To ask whether two items are in one group, you compare their badges. That is one look each.

To join two groups, you pick one of the two names. Then you go past every item, and each item that wears the other name gets a new badge with the chosen name. You must go past all items, because the badges do not tell you where the members of a group are. Joining is slow, and asking is fast.

## The problem

Keep $n$ elements $0$ to $n - 1$, each first in a set of its own. Support `find(p)`, which returns a name of the set of $p$, `union(p, q)`, which merges the sets of $p$ and $q$, and `connected(p, q)`, which tells whether $p$ and $q$ are in one set. This is the [disjoint-set](/disjoint-set/) type on a fixed range of elements. The structure also keeps `count`, the number of sets.

## The algorithm

```pseudo id=main
INIT(n)
L1  for i ← 0 to n − 1 do id[i] ← i
L2  count ← n

FIND(p)
L3  return id[p]

UNION(p, q)
L4  a ← id[p]; b ← id[q]
L5  if a = b then return                  ▷ already in one set
L6  for i ← 0 to n − 1 do
L7      if id[i] = a then id[i] ← b       ▷ rename the set a to b
L8  count ← count − 1
```

**Init** (lines L1 and L2) gives each element its own name, so there are $n$ sets of one element.

**Find** (line L3) returns the name of the set of $p$. The name of a set is one of its members, but any value would do; only the equality of names matters. `connected(p, q)` is `id[p] = id[q]`.

**Union** (lines L4 to L8) reads the two names. If they are equal, $p$ and $q$ are already in one set. Otherwise the loop renames every element of the set $a$ to $b$, which merges the two sets, and the number of sets falls by one. The loop must compare with the saved name $a$, not with `id[p]`, because the loop changes `id[p]` when it reaches $p$.

## Example

Take $n = 10$ and the eleven pairs of the file tinyUF.txt of Sedgewick and Wayne. Each row shows the array `id[0..9]` after the union, and the number of entries that the loop of line L7 changes.

| union | id after the union | renamed | sets |
|---|---|---|---|
| start | 0 1 2 3 4 5 6 7 8 9 | | 10 |
| (4, 3) | 0 1 2 3 3 5 6 7 8 9 | 1 | 9 |
| (3, 8) | 0 1 2 8 8 5 6 7 8 9 | 2 | 8 |
| (6, 5) | 0 1 2 8 8 5 5 7 8 9 | 1 | 7 |
| (9, 4) | 0 1 2 8 8 5 5 7 8 8 | 1 | 6 |
| (2, 1) | 0 1 1 8 8 5 5 7 8 8 | 1 | 5 |
| (8, 9) | no change, both have id 8 | 0 | 5 |
| (5, 0) | 0 1 1 8 8 0 0 7 8 8 | 2 | 4 |
| (7, 2) | 0 1 1 8 8 0 0 1 8 8 | 1 | 3 |
| (6, 1) | 1 1 1 8 8 1 1 1 8 8 | 3 | 2 |
| (1, 0) | no change, both have id 1 | 0 | 2 |
| (6, 7) | no change, both have id 1 | 0 | 2 |

At the end there are two sets, $\{0, 1, 2, 5, 6, 7\}$ with name 1 and $\{3, 4, 8, 9\}$ with name 8. Each of the eight unions that merge sets scans all ten entries, even when it renames only one.

## Correctness

The invariant is: *two elements are in one set exactly when they have the same entry in `id`*. Init makes all entries different, which is $n$ sets of one element. A find returns the entry, and by the invariant equal entries mean one set. A union with $a \ne b$ gives each member of the set $a$ the entry $b$ and changes no other entry. So afterwards the elements with entry $b$ are the union of the two old sets, and every other set keeps its own entry. The counter falls by one exactly when two sets merge. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/), where reading or writing one array entry costs $O(1)$.

- **Init.** The loop of line L1 runs $n$ times: $\Theta(n)$.
- **Find and connected.** One or two array reads: $\Theta(1)$ in the worst case.
- **Union.** Line L4 reads two entries. When the names differ, the loop reads all $n$ entries and writes the $s$ members of the set $a$, with $1 \le s \le n - 1$. Sedgewick and Wayne count this as between $n + 3$ and $2n + 1$ array accesses. So a union that merges costs $\Theta(n)$ in each case, not only in the worst case.
- **A sequence.** At most $n - 1$ unions merge. A sequence of $m$ operations costs $O(n + mn)$, and the $n - 1$ unions that build one set cost $\Theta(n^2)$.
- **Space.** The array of $n$ entries and the counter.

## Properties

- **Online and deterministic.** Each answer is ready before the next operation.
- **Worst case per operation.** The bounds are worst case, not amortized: a find never costs more than $O(1)$.
- **Canonical names.** The name of a set is stored at each member, so a program can group the elements by name in one pass, for example to list the [connected components](/connected-components/).
- **No pointer chasing.** Each operation is a fixed scan or a single read, which suits small arrays and vector hardware.

## Variants and improvements

- **Rename the smaller set.** If each set also keeps a list of its members and its size, a union can rename only the members of the smaller set. Each element then changes its name at most $\lg n$ times, because each change at least doubles the size of its set, so $n - 1$ unions cost $O(n \log n)$ in all. This is [linked-list disjoint sets](/linked-list-disjoint-sets/) with weighted union, the idea of [union by size](/union-by-size/).
- **Quick-union.** Store a parent instead of a name, so that a union changes one entry. [Quick-union](/quick-union/) and then the [disjoint-set forest](/disjoint-set-forest/) follow this way.
- **Keyed elements.** For elements that are not $0$ to $n - 1$, map them to indices with a hash table first.

## When to use it

Use quick-find when $n$ is small, for example a few hundred, and finds are far more frequent than unions. For a large $n$ and many unions, its $\Theta(n)$ union is too slow, and the [disjoint-set forest](/disjoint-set-forest/) is better in every case. Use [linked lists](/linked-list-disjoint-sets/) with weighted union when $O(1)$ finds and the list of members of each set are both needed.

## Pitfalls

- **Comparing with `id[p]` inside the loop.** Line L7 must compare with the name $a$ that line L4 saved. A loop that tests `id[i] = id[p]` stops renaming after it passes $p$, because `id[p]` has become $b$, so the members of the set after $p$ keep the old name.
- **Merging one set with itself.** Without line L5, a union of two elements of one set renames the set to its own name, which is harmless, but it still costs $\Theta(n)$ and line L8 makes the counter wrong.
- **Renaming the wrong set.** Line L7 must rename every element whose entry is $a$. Setting only `id[p] ← b` moves $p$ alone and leaves the rest of its old set behind.

## Implementations

The Python class takes $n$ in its constructor. It has `find`, `union`, `connected` and a `count` attribute, and `check_invariant` tests that each name is a member of its set and that the counter matches the names.

## History

Representing each class by a name stored at each member is the direct method for equivalences, and the [linked-list representation](/linked-list-disjoint-sets/) with weighted union was analyzed early. Sedgewick and Wayne name the method quick-find, and present it as the first of their union-find implementations, before quick-union and weighted quick-union.

## References
