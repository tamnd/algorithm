---
tag: BSY6SQ
kind: data-structure
slug: persistent-trie
name: Persistent trie
aliases:
- persistent binary trie
- versioned trie
area: data-structures/persistent-structures
level: advanced
summary: A trie updated by path copying, used for prefix and max-xor queries over past versions.
implements: [dictionary]
model: word-ram
complexity:
  vars: {w: the number of bits of a key, u: the number of updates done}
  time: {insert: Θ(w), remove: Θ(w), count: Θ(w), max_xor: Θ(w), size: Θ(1)}
  space: {total: Θ(u w)}
history:
  year: 1989
  people: [James R. Driscoll, Neil Sarnak, Daniel D. Sleator, Robert E. Tarjan]
  note: Path copying, the general method behind the persistent trie, was studied for linked structures; tries themselves go back to de la Briandais and Fredkin around 1960.
prereqs: [trie, path-copying, persistent-data-structure]
see_also: [persistent-segment-tree, maximum-xor-subarray, radix-tree, persistent-vector, structural-sharing, version-tree, wavelet-tree, ternary-search-tree]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: the path copying method for linked data structures
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Section 10.3.1, Tries (finite maps over strings as functional tries)
  - paper: Edward Fredkin, Trie memory, Communications of the ACM 3(9), 1960
    locator: the trie as a tree indexed by the symbols of the key
  - url: https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/
    title: Erik Demaine, MIT 6.851 Advanced Data Structures, Spring 2012
    locator: Lecture 1, Persistent data structures (path copying)
---

A persistent trie is a [trie](/trie/) in which an insertion or deletion does not change any node but copies the nodes on the path of the key, from the root down, and returns a new root. Every other node is shared with the old version, so an update of a key of $w$ symbols makes $w + 1$ new nodes and takes $\Theta(w)$ time, and every old version stays valid. The usual form in algorithms is a binary trie over $w$-bit integers in which each node counts the keys below it. Two versions of such a trie, one made from the other by insertions, then describe the keys inserted between them, and a walk down both at once answers "the maximum of $x \oplus y$ over the keys of a subarray" in $\Theta(w)$ time.

## In plain words

A binary trie stores numbers by their bits. From the root, go left for a 0 bit and right for a 1 bit, from the highest bit down. Each number is a path of $w$ steps, and each node can count how many stored numbers pass through it.

To add a number without losing the old trie, copy only the nodes on its path, with each count one higher, and let each copy point to the old nodes on the side the path does not take. The old root still shows the old trie.

If you add the items of an array one by one and keep every root, then the counts in root $r$ minus the counts in root $l$ describe exactly the items from position $l$ to $r - 1$. That lets you ask questions about any part of the array.

## The abstract type

The structure keeps numbered versions of a multiset of keys in $[0, 2^w)$. Version 0 is empty. The operations are:

- `insert(v, x)` and `remove(v, x)`: make a new version from version $v$ with one more or one fewer copy of $x$, and return its number;
- `count(v, x)`: the number of copies of $x$ in version $v$; `size(v)`: the total count;
- `max_xor(u, v, y)`: for a version $v$ made from version $u$ by insertions, the maximum of $x \oplus y$ over the keys $x$ of the multiset difference $v - u$.

Any version can be updated, so the structure is fully persistent. With $w$ symbols from an alphabet of size $\sigma$ instead of bits, the same structure is a persistent [dictionary](/dictionary/) of strings.

## Representation

A node has two child pointers, $child[0]$ and $child[1]$, and a count $cnt$. The node $\varnothing$ (node 0 in the pool) stands for the empty trie: its count is 0 and both its children are $\varnothing$ itself, so a walk can pass through empty parts with no special case. The root of a version is at depth 0, and a node at depth $w$ is the leaf of one key; its count is the multiplicity of that key. A table $roots$ maps each version to its root.

**Invariant.** (I1) After an operation returns, no field of any node reachable from a root changes again. (I2) For each version, every node at depth less than $w$ has $cnt = child[0].cnt + child[1].cnt$, and the node reached from the root by the bits of $x$, from bit $w - 1$ down to bit 0, is a leaf whose count is the multiplicity of $x$. (I3) $\varnothing$ has count 0 and is its own child.

## Operations

```pseudo id=main
ADD(t, x, d)                                ▷ new root: version t with d more copies of x
L1  root ← NEW-NODE(t.child[0], t.child[1], t.cnt + d); cur ← root
L2  for i ← w − 1 down to 0 do
L3      b ← bit i of x
L4      t ← t.child[b]                       ▷ the old node on the path
L5      new ← NEW-NODE(t.child[0], t.child[1], t.cnt + d)
L6      cur.child[b] ← new                   ▷ cur is new and not yet shared
L7      cur ← new
L8  return root

REMOVE(t, x)
L9  if COUNT(t, x) = 0 then return t else return ADD(t, x, −1)

COUNT(t, x)
L10 for i ← w − 1 down to 0 do t ← t.child[bit i of x]
L11 return t.cnt

MAX-XOR(u, v, y)                            ▷ v made from u by insertions only
L12 if v.cnt − u.cnt = 0 then error "empty"
L13 r ← 0; for i ← w − 1 down to 0 do
L14     b ← bit i of y
L15     if v.child[1 − b].cnt − u.child[1 − b].cnt > 0 then r ← r + 2^i; u ← u.child[1 − b]; v ← v.child[1 − b]
L16     else u ← u.child[b]; v ← v.child[b]
L17 return r
```

`insert(v, x)` appends ADD$(roots[v], x, 1)$ to the version table. Line L6 is the only write to an existing node, and it writes into a node made by the same call (in line L1 or L5), before the new root is returned, so (I1) holds.

**Why MAX-XOR is greedy.** The answer has its highest bit set if and only if some key in the difference has bit $w - 1$ equal to $1 - b$, where $b$ is that bit of $y$; a set high bit is worth more than all lower bits together. So the walk goes to the side with the opposite bit whenever the difference has a key there, and fixes the bits of the answer from the top down.

**Range queries over an array.** Let $a[0..m)$ be an array of $w$-bit numbers. Make version $j + 1$ by inserting $a[j]$ into version $j$. Then version $r$ minus version $l$ is the multiset of $a[l..r)$, and MAX-XOR$(roots[l], roots[r], y)$ is $\max_{l \le i < r} a[i] \oplus y$. For the [maximum XOR subarray](/maximum-xor-subarray/) with bounds on the start, insert the prefix XORs $P_0, P_1, \ldots$ instead: the XOR of $a[l..r)$ is $P_r \oplus P_l$.

## Example

Let $w = 3$ and $a = [5, 1, 6, 3]$, that is, $101, 001, 110, 011$ in binary. Versions 1 to 4 insert these keys into the version before. Each insertion makes $w + 1 = 4$ nodes, so the pool has $1 + 16 = 17$ nodes, where 1 is $\varnothing$. Version 4 holds $\{1, 3, 5, 6\}$, and version 2 still holds $\{1, 5\}$.

**MAX-XOR on $a[1..3) = [1, 6]$ with $y = 4 = 100$.** Walk the roots of versions 1 and 3; the difference is $\{1, 6\}$.

- Bit 2 of $y$ is 1, so look for a key with bit 2 equal to 0. The difference of counts on side 0 is $1 - 0 = 1$ (the key 1; version 1 holds only 5, which is on side 1). Set bit 2 of $r$: $r = 4$.
- Bit 1 of $y$ is 0, so look for bit 1 equal to 1. Below the path $0$, the only key is $001$, with bit 1 equal to 0, so the difference on side 1 is 0, and the walk takes side 0.
- Bit 0 of $y$ is 0, so look for bit 0 equal to 1. The key $001$ has it: $r = 4 + 1 = 5$.

The answer is $5 = 4 \oplus 1$, and indeed $4 \oplus 6 = 2$ is smaller. Over all of $a$ with $y = 4$ the answer is $7 = 4 \oplus 3$, and over $a[2..4) = [6, 3]$ with $y = 0$ it is 6.

**A removal.** Removing 6 from version 4 makes a version with $\{1, 3, 5\}$ by 4 new nodes, and version 4 still holds 6.

## Correctness

Write $\text{ms}(t)$ for the multiset that a root $t$ stores: the multiset in which each $x$ appears as often as the count of the leaf reached by the bits of $x$. ADD copies the nodes on the path of $x$, adds $d$ to each count, and keeps the other child of each copy, which is the old node on the side the path does not take. So the leaf of $x$ has its count changed by $d$, every other leaf is reached through the same old nodes as before, and the count of each copy is the sum of its children's counts, by (I2) for the old nodes. So $\text{ms}$ of the new root is $\text{ms}(t)$ with $d$ copies of $x$ added, and (I2) holds. By (I1) the old versions do not change. For MAX-XOR, counts are additive, so the difference of counts at a pair of nodes on the same path is the number of keys of $v - u$ below it, and the greedy choice is right by the argument above. The full proof is in the proofs folder.

## Complexity

| operation | time | new nodes |
|---|---|---|
| insert, remove | $\Theta(w)$ | $w + 1$ (none for a removal of an absent key) |
| count | $\Theta(w)$ | none |
| max_xor | $\Theta(w)$ | none |
| size | $\Theta(1)$ | none |

**Time.** Each operation follows one path of $w$ steps, or two paths in step for MAX-XOR, and does $O(1)$ work per step on the [word RAM](/word-ram/). The bounds are worst case and hold for every version.

**Space.** After $u$ updates the pool has at most $1 + u(w + 1)$ nodes, which is $\Theta(u w)$. For an array of $m$ numbers of 30 bits, that is $31m$ nodes. A compressed trie, as in the [radix tree](/radix-tree/), stores only branching nodes and lowers the space of one version to $O(n)$ nodes, but an update in it still copies a path.

## Variants

- **String tries.** For keys that are strings over an alphabet of size $\sigma$, each node has $\sigma$ child pointers, or a small map from symbols to children. An update copies the nodes on the path of the key; with an array of $\sigma$ pointers per node, each copy costs $\Theta(\sigma)$, so a map is better for large alphabets.
- **Minimum XOR and rank queries.** The same two-version walk gives the minimum of $x \oplus y$ (prefer the same bit), the count of keys below a bound, and the k-th smallest key of the difference, like the [persistent segment tree](/persistent-segment-tree/) over values.
- **Hash tries.** Hash the key and use its bits as the path, with wide nodes of 32 slots and a bitmap of the slots in use. This is the hash array mapped trie of Bagwell, and its persistent form is the standard immutable hash map of Clojure and Scala. The [persistent vector](/persistent-vector/) is the same idea with the index as the path.
- **Static alternative.** For range queries on a fixed array, a [wavelet tree](/wavelet-tree/) gives the same queries in $O(m \log \sigma)$ bits instead of $\Theta(m w)$ words.

## When to use it

Use a persistent trie when keys are fixed-width integers or strings, when old versions must stay queryable, and especially when a query concerns the elements inserted between two versions: maximum or minimum XOR with a given value over a subarray, or the count of values in a range over a subarray. Updates cost $\Theta(w)$ independently of the number of keys, and there is no balancing. If only the newest version matters, a plain trie uses $w$ times less space per update. If the keys are not of bounded length, a persistent balanced search tree is safer.

## Pitfalls

- **Writing into a shared node.** Line L6 writes only into nodes made in the same call. Writing $t.child[b]$ for an old node $t$ changes every version that shares it.
- **Two versions that are not related by insertions.** MAX-XOR uses the count difference $v - u$; if $v$ was not made from $u$ by insertions alone, the difference can be negative and the walk gives a wrong answer.
- **Memory.** Each update makes $w + 1$ nodes, so $10^6$ insertions of 30-bit keys make $3.1 \times 10^7$ nodes. Store the pool as flat integer arrays, not as one object per node.
- **Fixed width.** All keys must have exactly $w$ bits, with leading zeros. A key with more bits is silently cut, or, as in the implementation, rejected.
- **Removal of an absent key.** Without the guard in line L9, a removal would make a count of $-1$ at the leaf, which breaks (I2).

## Implementations

## History

Tries were described by René de la Briandais in 1959 and named by Edward Fredkin in 1960. Path copying as a general way to make linked structures persistent was studied by Driscoll, Sarnak, Sleator and Tarjan in 1989, and Okasaki's book of 1998 gives tries as finite maps in a purely functional setting. The binary trie with counts, one version per prefix of an array, became a standard tool in programming contests for XOR queries over subarrays.

## References
