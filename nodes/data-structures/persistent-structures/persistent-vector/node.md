---
tag: E5Q5G6
kind: data-structure
slug: persistent-vector
name: Persistent vector
aliases:
- Bagwell persistent vector
- Clojure vector
- hash array mapped trie vector
area: data-structures/persistent-structures
level: advanced
summary: A wide, shallow persistent trie giving near-constant indexing and update by copying a short path.
implements: [list]
model: word-ram
complexity:
  vars: {n: the number of items, M: the branching factor, u: the number of updates done}
  time: {get: Θ(1 + log n / log M), set: Θ(M (1 + log n / log M)), push: Θ(M (1 + log n / log M)), pop: Θ(M (1 + log n / log M)), size: Θ(1)}
  space: {total: Θ(n + u M (1 + log n / log M))}
history:
  year: 2007
  people: [Rich Hickey, Phil Bagwell]
  note: Hickey built the vector of Clojure as a 32-way persistent trie with a tail buffer, following the wide array mapped tries of Bagwell.
prereqs: [persistent-trie, path-copying, dynamic-array]
see_also: [structural-sharing, persistent-segment-tree, skew-binary-random-access-list, rope, finger-tree, radix-tree, fully-persistent-array, semi-persistent-array]
sources:
  - paper: Phil Bagwell, Ideal Hash Trees, technical report, EPFL, 2001
    locator: the array mapped trie with 32-way nodes and a bitmap of the slots in use
  - url: https://github.com/clojure/clojure/blob/master/src/jvm/clojure/lang/PersistentVector.java
    title: Rich Hickey, clojure.lang.PersistentVector, the Clojure source code
    locator: the methods nth, assocN, cons, pop, pushTail, popTail and tailoff
  - paper: Phil Bagwell and Tiark Rompf, RRB-Trees, Efficient Immutable Vectors, technical report, EPFL, 2011
    locator: the description of the 32-way vector trie and its relaxed form for concatenation
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: the path copying method for linked data structures
---

A persistent vector is an immutable sequence stored as a wide [trie](/persistent-trie/) on the digits of the index in base $M$, usually $M = 32$, with the items in leaves of $M$ items each and a separate *tail* leaf for the last items. Index $i$ is found by following its base-$M$ digits from the root, so `get` visits $1 + \lceil \log_M (n/M) \rceil$ nodes, which is at most 7 for $n < 2^{35}$. An update copies the one node on each level of that path, at most $M$ slots each, and shares the rest; push and pop at the end usually copy only the tail. It is the vector of Clojure, designed by Rich Hickey on the array mapped tries of Phil Bagwell, and the same design is the immutable vector of Scala and of several other libraries.

## In plain words

Picture a shelf of boxes, each holding 32 items. A cabinet has 32 drawers, each drawer holding one box; a room has 32 cabinets; and so on. To find item number $i$, write $i$ in base 32: its digits tell you which cabinet, which drawer and which place in the box. That takes only a few steps even for millions of items.

To change one item without losing the old vector, copy the box that holds it, the drawer list that points to that box, and so on up to the top. Everything else is shared with the old vector. That is a few copies of 32 slots each, out of millions of items.

New items go into a separate loose box at the end, the tail. Only when it is full is it put on the shelf.

## The abstract type

The structure implements an immutable [list](/list/) with the operations of a [dynamic array](/dynamic-array/): a sequence $\langle a_0, \ldots, a_{n-1} \rangle$ with value semantics. Each update returns a new vector and leaves its argument unchanged:

- `get(v, i)`: the item $a_i$;
- `set(v, i, x)`: the vector with $a_i$ replaced by $x$;
- `push(v, x)`: the vector with $x$ added at the end;
- `pop(v)`: the vector without its last item;
- `size(v)`: $n$.

Every version can be the input of any operation, so the structure is fully persistent.

## Representation

Fix $B \ge 1$ and $M = 2^B$. A vector has four fields: its size $n$, a *shift* $s$ (a multiple of $B$, at least $B$), a root node and a tail. A node is a fixed array of at most $M$ slots. A *leaf* holds $M$ items. An inner node at level $\ell$ (a multiple of $B$, at least $B$) holds pointers to nodes of level $\ell - B$, and level 0 is the leaves; the root is at level $s$.

Let $\text{tailoff}(n) = 0$ if $n < M$, and otherwise $\text{tailoff}(n) = M \lfloor (n - 1)/M \rfloor$. The first $\text{tailoff}(n)$ items are in the trie, in $\text{tailoff}(n)/M$ full leaves, and the remaining $n - \text{tailoff}(n)$ items, between 1 and $M$ when $n > 0$, are in the tail. Item $i < \text{tailoff}(n)$ is in slot $\text{digit}_0(i)$ of the leaf reached from the root by the digits $\text{digit}_{s}(i), \text{digit}_{s - B}(i), \ldots, \text{digit}_{B}(i)$, where $\text{digit}_\ell(i) = \lfloor i / 2^\ell \rfloor \bmod M$.

**Invariant.** (I1) No node changes after it is made. (I2) The leaves of the trie are full and packed from the left: every inner node except those on the rightmost path is full, and those on the rightmost path have their slots in use from slot 0. (I3) The tail holds the items from $\text{tailoff}(n)$ on. (I4) The root is as low as possible: the trie has room for its leaves, at most $2^s$ of them, and if $s > B$ it has more than $2^{s - B}$, so that the root has at least two children.

## Operations

```pseudo id=main
GET(v, i)
L1  if i ≥ TAILOFF(v) then return v.tail[i − TAILOFF(v)]
L2  node ← v.root; for ℓ ← v.shift down to B step −B do node ← node[digit_ℓ(i)]
L3  return node[i mod M]

SET(v, i, x)
L4  if i ≥ TAILOFF(v) then return v with tail ← a copy of v.tail with slot i − TAILOFF(v) set to x
L5  return v with root ← SET-PATH(v.root, v.shift, i, x)

SET-PATH(node, ℓ, i, x)
L6  c ← a copy of node
L7  if ℓ = 0 then c[i mod M] ← x else c[digit_ℓ(i)] ← SET-PATH(node[digit_ℓ(i)], ℓ − B, i, x)
L8  return c

PUSH(v, x)
L9  if v.n − TAILOFF(v) < M then return v with tail ← v.tail + ⟨x⟩ and n ← v.n + 1
L10 if v.n / M > 2^v.shift then root ← NODE(v.root, NEW-PATH(v.shift, v.tail)); shift ← v.shift + B
L11 else root ← PUSH-TAIL(v.root, v.shift, v.n − 1, v.tail); shift ← v.shift
L12 return the vector (n ← v.n + 1, shift, root, tail ← ⟨x⟩)

PUSH-TAIL(node, ℓ, i, leaf)                 ▷ i is the last index of the leaf
L13 j ← digit_ℓ(i); c ← a copy of node; set c[j] to the child chosen below and return c
L14 if ℓ = B then the child is leaf
L15 else if slot j of node is in use then the child is PUSH-TAIL(node[j], ℓ − B, i, leaf)
L16 else the child is NEW-PATH(ℓ − B, leaf)

POP(v)
L17 if v.n = 1 then return the empty vector
L18 if v.n − TAILOFF(v) > 1 then return v with the last item of the tail dropped
L19 tail ← the leaf that holds item v.n − 2, found as in L2
L20 root ← POP-TAIL(v.root, v.shift, v.n − 2), or an empty node if nil
L21 if v.shift > B and root has one child then root ← root[0]; shift ← v.shift − B
L22 return the vector (n ← v.n − 1, shift, root, tail)

POP-TAIL(node, ℓ, i)                        ▷ i is the last index that stays
L23 j ← digit_ℓ(i); if ℓ > B then c ← POP-TAIL(node[j], ℓ − B, i); if c = nil and j = 0 return nil; else return node with slots after j dropped and slot j set to c (dropped if nil)
L24 if j = 0 then return nil
L25 return node with slots after j − 1 dropped
```

NEW-PATH$(\ell, \text{leaf})$ wraps the leaf in $\ell / B$ new inner nodes of one child each. Every write in these procedures goes to a node made by the same call, so (I1) holds.

**The tail.** Pushes go to the tail until it has $M$ items (L9). The next push moves the full tail into the trie as a new leaf (L11), or, if the trie is full, makes a new root above the old one (L10). So one push in $M$ touches the trie. Pop does the reverse: it drops the last item of the tail, and when the tail would become empty, it takes the last leaf of the trie as the new tail (L19, L20) and lowers the root if it has one child left (L21).

## Example

Take $M = 4$ ($B = 2$) and push the items 0 to 9. The vector $v$ has $n = 10$, $\text{tailoff}(10) = 8$, shift $2$, a root with two leaves $\langle 0, 1, 2, 3 \rangle$ and $\langle 4, 5, 6, 7 \rangle$, and the tail $\langle 8, 9 \rangle$.

- **get$(v, 6)$.** $6 < 8$, so it is in the trie. Its digit at level 2 is $\lfloor 6/4 \rfloor = 1$, so take the second leaf, and its slot is $6 \bmod 4 = 2$: the item 6.
- **set$(v, 6, 60)$.** SET-PATH copies the root and the second leaf, which is 2 new nodes. The new vector shares the first leaf and the tail with $v$, and $v$ still holds 6.
- **Push 10 to 16.** 10 and 11 fill the tail; 12 moves $\langle 8, 9, 10, 11 \rangle$ into slot 2 of a copy of the root, and so on. With 17 items the root has 4 full leaves, items 0 to 15, and the tail is $\langle 16 \rangle$.
- **Push 17 to 20.** At the push of 20, $n = 20$, the tail $\langle 16, 17, 18, 19 \rangle$ is full, and the trie has $4 = 2^2$ leaves, which is its capacity at shift 2; the test of line L10 is $20/4 = 5 > 4$. Line L10 makes a new root at level 4 with two children: the old root, and a new path to the leaf $\langle 16, \ldots, 19 \rangle$. The shift becomes 4 and the tail is $\langle 20 \rangle$.
- **Pop.** The tail has one item, so line L19 takes the leaf $\langle 16, \ldots, 19 \rangle$ as the new tail, POP-TAIL removes it from the trie, and the root is left with one child, so line L21 makes the old root the root again, with shift 2.

## Correctness

Write $\text{items}(v)$ for the sequence read from the leaves of the trie, left to right, followed by the tail. By (I2) and (I3), GET follows the digits of $i$ to the leaf slot that holds $a_i$, or reads the tail. SET-PATH copies exactly the nodes on that path and changes only the slot of $i$, so $\text{items}$ of the result differs from $\text{items}(v)$ only at $i$. PUSH either extends the tail, or appends the full tail as the next leaf of the trie, at the position given by the digits of its last index $n - 1$, which by (I2) is the first free leaf position; when the trie is full by (I4), the new root has the old trie as its first child and the new leaf as the first leaf of its second child. POP is the reverse step. In each case (I2) to (I4) hold for the result, and by (I1) no old version changes. The full proof is in the proofs folder.

## Complexity

Let $h = s/B$ be the height of the trie, so $h \le 1 + \lceil \log_M \max(1, n/M) \rceil$, which is $1 + \log n / \log M$ up to rounding.

| operation | time | new slots |
|---|---|---|
| get | $\Theta(h)$ | none |
| set | $\Theta(M h)$ | $h + 1$ nodes of at most $M$ slots, or one tail |
| push, tail not full | $\Theta(M)$ | one tail of at most $M$ slots |
| push, tail full | $\Theta(M h)$ | $h + 1$ inner nodes and a new tail |
| pop | $\Theta(M h)$ worst case, $\Theta(M)$ if the tail has two items or more | as push |
| size | $\Theta(1)$ | none |

With $M = 32$ and $n < 2^{30}$, $h \le 5$, so get follows at most 5 pointers, and set copies at most 6 arrays of 32 slots. That is why the operations are often called "effectively constant", though they are logarithmic with a large base.

**Space.** A vector of $n$ items uses $n + O(n/M)$ slots, since the inner nodes are a fraction $1/(M-1)$ of the leaves. Each update adds $O(M h)$ slots, so after $u$ updates the space is $O(n + u M h)$. With $M = 32$ the copies are about 200 slots per set, which is why a mutable *transient* vector is used to build a large vector in one pass.

**Choosing $M$.** A larger $M$ lowers the height and the time of get, and raises the cost of each copy. $M = 32$ is the usual choice because a node of 32 pointers fits in a few cache lines, and digits are found with shifts and masks.

## Variants

- **Transients.** A transient vector is a mutable copy that writes into nodes it owns, marked by an owner field, and copies only nodes it does not own. A loop of $n$ pushes then costs $O(n)$ total, and the result is frozen into a persistent vector at the end. Clojure provides this.
- **RRB-trees.** Relaxed radix balanced trees of Bagwell and Rompf let inner nodes be slightly less than full, and store size tables in such nodes, so that two vectors can be concatenated and a vector can be split in $O(\log n)$ time while index stays fast. The Scala vector in later versions builds on related ideas.
- **Hash array mapped trie.** The same trie with the bits of a hash of the key as the path, and a bitmap in each node that records which of the 32 slots are in use, gives an immutable hash map with the same costs. It is Bagwell's design, used for maps and sets in Clojure and Scala.
- **Head buffer.** Keeping a buffer at the front as well as at the end gives fast push at both ends.
- **Other persistent arrays.** The [skew binary random-access list](/skew-binary-random-access-list/) gives $O(1)$ push and pop at the front and $O(\log n)$ index, with binary nodes. The [semi-persistent array](/semi-persistent-array/) and the [fully persistent array](/fully-persistent-array/) give $O(1)$ access to the newest version by writing to a shared array.

## When to use it

Use a persistent vector when a program needs an immutable indexed sequence with fast read, update and push at the end, and old versions must stay valid: the default sequence in a functional language, the state of an application that keeps an undo history, or data that many threads read while one thread makes new versions. If old versions are never used again, a mutable [dynamic array](/dynamic-array/) is several times faster and smaller. If concatenation and split are the main operations, use an RRB-tree, a [rope](/rope/) or a [finger tree](/finger-tree/).

## Pitfalls

- **Writing a shared node.** A node may be part of many versions. SET-PATH and PUSH-TAIL write only into fresh copies; a write into an existing node or into the shared tail changes other versions.
- **Off-by-one in tailoff.** The tail holds 1 to $M$ items when $n > 0$, never 0. With $\text{tailoff}(n) = M \lfloor n/M \rfloor$ instead of $M \lfloor (n-1)/M \rfloor$, a vector of exactly $M$ items would have an empty tail and a trie with one leaf, and GET of the last item would read the wrong place.
- **Root overflow.** The trie is full when it has $2^s$ leaves. PUSH must grow a new root in that case (L10); forgetting it makes PUSH-TAIL write slot $M$ of the root.
- **Lowering the root.** POP must remove a root with one child (L21). Otherwise the height never shrinks, which is not wrong but makes later get and set slower than they should be, and breaks (I4).
- **Cost of building.** $n$ pushes on a persistent vector copy the tail each time, $\Theta(M)$ per push. Use a transient, or build the leaves directly, for bulk loads.

## Implementations

## History

Phil Bagwell described array mapped tries and hash array mapped tries with 32-way nodes in technical reports around 2000 and 2001. Rich Hickey used the idea for the vectors and hash maps of Clojure, released in 2007, and added the tail buffer and transients. Bagwell and Rompf gave the relaxed radix balanced form for fast concatenation in 2011. The same layout is the base of the immutable vectors of Scala and of persistent collection libraries in other languages.

## References
