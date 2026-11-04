---
tag: AQJK5W
kind: data-structure
slug: hollow-heap
name: Hollow heap
aliases:
- hollow heaps
area: data-structures/heaps
level: research
summary: Simple heap with O(1) worst-case insert and decrease-key and O(log n) amortized delete.
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
prereqs: [fibonacci-heap, heap-property, decrease-key, potential-method, directed-acyclic-graph]
see_also: [fibonacci-heap, pairing-heap, rank-pairing-heap, strict-fibonacci-heap, brodal-queue, decrease-key, dijkstra, lazy-deletion]
sources:
  - paper: "Thomas Dueholm Hansen, Haim Kaplan, Robert E. Tarjan and Uri Zwick, Hollow heaps, ACM Transactions on Algorithms 13(3), 2017"
    locator: the multi-root and one-root hollow heaps, the operations with ranked and unranked links, and the amortized analysis
  - paper: "Thomas Dueholm Hansen, Haim Kaplan, Robert E. Tarjan and Uri Zwick, Hollow heaps, ICALP 2015, Lecture Notes in Computer Science 9134"
    locator: the conference version, with the definitions and the bounds
---

A hollow heap is a [priority queue](/priority-queue/) of Hansen, Kaplan, Tarjan and Zwick (2015) with the same bounds as the [Fibonacci heap](/fibonacci-heap/): find-min, insert, meld and [decrease-key](/decrease-key/) in $O(1)$ time, each in the worst case, and delete and delete-min in $O(\log N)$ amortized time. It gets them with less machinery. Its two ideas are *lazy deletion*, in which an item is removed by marking its node *hollow*, and *moving* an item on decrease-key: the item goes to a new node, the old node becomes hollow and stays where it is, and the new node takes the old one as a child. So no subtree is ever cut out, and the structure is a [directed acyclic graph](/directed-acyclic-graph/) in which a node can have two parents. Hollow nodes are destroyed only when they become roots, during a delete, and the full nodes found below them are linked by rank, as in a Fibonacci heap.

## In plain words

Think of a tournament tree in which each winner sits above the players it beat. To make a player stronger, you do not tear its part of the tree apart. You leave an empty chair where it was, and the player plays again from the top, with its old chair below it.

To remove a player, you also just leave its chair empty. The empty chairs stay until one of them is at the very top. Then the queue clears the empty chairs at the top and below them, and the players it finds there play short matches in pairs of equal size, until one winner is left on top. Each step of a change takes a fixed number of moves; the clearing does the work later, and that work is shared out over all the earlier steps.

## The abstract type

A hollow heap implements the meldable, addressable min-[priority queue](/priority-queue/): INSERT$(e, k)$ returns a handle to the item $e$, and FIND-MIN, MELD, DECREASE-KEY$(e, k)$ for a key $k$ not larger than the current key, DELETE$(e)$ and DELETE-MIN work on items through their handles. Keys come from a [total order](/total-order/) and are only compared.

## Representation

The heap is a DAG of nodes with one root. Each node $u$ has a key, a rank $r(u) \ge 0$, an item pointer, which is empty when $u$ is *hollow* and points to the item when $u$ is *full*, a first child, a next sibling, and an *extra parent* $\mathit{ep}(u)$. Each item points to the full node that holds it, so each item is in exactly one full node.

- Each node except the root has one or two parents. A node with two parents is a hollow node $u$ left by decrease-key; its second parent is $\mathit{ep}(u)$, the node made for the item, and $u$ is the last child of $\mathit{ep}(u)$. Its sibling pointer belongs to the child list of its first parent.
- **(O)** The heap order: the key of each child is at least the key of each of its parents.
- **(R)** The root is full, unless the heap is empty.

By (O) and (R), the root holds an item of minimum key, since every full node is below the root. A *link* of two roots makes the root with the larger key the first child of the other; a *ranked link* is a link of two roots of the same rank $r$, after which the winner has the rank $r + 1$. Links that do not change ranks are *unranked*.

## Operations

```pseudo id=main
LINK(v, w)                                       ▷ v and w are roots
L1  if key(v) ≥ key(w) then
L2      make v the first child of w; return w
L3  make w the first child of v; return v

INSERT(e, k)
L4  u ← a new full node for e with key k and rank 0
L5  h ← u if the heap is empty, else LINK(u, h)

MELD(h, h′)
L6  h ← LINK(h, h′), if both are not empty

DECREASE-KEY(e, k)
L7  u ← node(e); if u = h then key(u) ← k; return
L8  v ← a new full node for e with key k
L9  make u hollow
L10 r(v) ← max(0, r(u) − 2)
L11 child(v) ← u; ep(u) ← v                       ▷ u now has two parents
L12 h ← LINK(v, h)

DELETE(e)
L13 make node(e) hollow
L14 if h is full then return                     ▷ lazy: nothing more to do
L15 H ← the list [h]; A ← an empty map from ranks to full roots
L16 while H is not empty: x ← remove the first node of H
L17     for each child u of x, in order:
L18         if u is hollow then
L19             if ep(u) = nil then add u to H           ▷ u has no parent left
L20             else ep(u) ← nil; if ep(u) was x then stop the scan of x
L21         else while A has a root t of rank r(u) do
L22             remove t from A; u ← LINK(u, t); r(u) ← r(u) + 1
L23             A[r(u)] ← u
L24     destroy x
L25 h ← nil; for each root t in A, in order of rank:
L26     h ← t if h = nil, else LINK(t, h)
```

**Decrease-key.** The item moves to a new node $v$ with the smaller key, and $v$ is linked with the root. The old node $u$ keeps its place and its children; they still satisfy (O) under $u$, whose key did not change, and under $v$, whose key is smaller. The rank rule of line L10 is the key to the analysis: $u$ has, in effect, ranked children of ranks $0, \ldots, r(u) - 1$, and $v$ gets credit for all of them but the two largest.

**Delete.** A delete makes the node hollow, and if it was not the root, it stops. If the root is now hollow, the loop destroys every hollow node that has no parent left. A child $u$ of such a node $x$ either is full, and becomes a root that joins the ranked links, or is hollow with one parent, and is destroyed in turn, or is hollow with two parents, and loses the parent $x$. In the last case, if $x$ was the extra parent, $u$ is the last child of $x$, so the scan of $x$ stops there; else $u$ stays the only child of its extra parent, which becomes its one parent. At the end, the roots in $A$, at most one per rank, are linked into one tree by unranked links.

## Example

Insert $a$ with key 5, $b$ with 3, $c$ with 8, $d$ with 6 and $e$ with 7. A tree is written as root[children], a full node as its item and key, a hollow node as H and its key, and all ranks are 0 unless shown.

| step | heap | what happens |
|---|---|---|
| the five inserts | b3[e7 d6 c8 a5] | each new node loses its link with b |
| DECREASE-KEY($c$, 1) | c1[b3[e7 d6 H8 a5] H8] | the new node c1 takes the hollow H8 as its child and wins the link with b3; H8 has the parents b3 and c1 |
| DECREASE-KEY($e$, 2) | c1[e2[H7] b3[H7 d6 H8 a5] H8] | e2 takes H7 and loses the link with c1 |
| DELETE-MIN | e2 (rank 1)[b3[H7 d6 H8 a5] H7] | returns $c$; c1 becomes hollow and is destroyed; its children are e2 and b3, which are full, and H8, which loses its extra parent; the ranked link of e2 and b3 gives rank 1 |
| DELETE-MIN | b3[H7 d6 H8 a5] | returns $e$; H7 loses its extra parent e2 |
| DELETE-MIN | a5 (rank 1)[d6] | returns $b$; H7 and H8 now have no parent and are destroyed; d6 and a5 are linked by rank |

## Correctness

The operations keep (O) and (R), and they keep the item pointers right: each item is in exactly one full node, and the full nodes are exactly the nodes of the items in the heap. LINK keeps (O), since the loser's key is at least the winner's. DECREASE-KEY gives $v$ a key no larger than that of $u$, and moves no edge. DELETE destroys only hollow nodes with no parent left, so every full node is still below the root when the loop ends; a full child that loses its parent becomes a root in $A$, and the final links put all roots under one. The loop ends, since each node enters $H$ at most once, each scan visits each child once, and each ranked link removes one root from $A$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| FIND-MIN, INSERT, MELD, DECREASE-KEY | $O(1)$ in the worst case |
| DELETE, DELETE-MIN | $O(\log N)$ amortized, for $N$ the number of nodes made so far |
| space | $O(N)$ |

INSERT, MELD and DECREASE-KEY make at most one node and do at most one link, so they take $O(1)$ time in the worst case, unlike in a Fibonacci heap, whose decrease-key does cascading cuts and is only amortized $O(1)$. A DELETE that leaves a full root takes $O(1)$ time.

**The amortized bound.** Hansen, Kaplan, Tarjan and Zwick prove the bound for DELETE with a [potential argument](/potential-method/). The main facts are these. A node of rank $r$ has a number of descendants that is exponential in $r$, as in a Fibonacci heap, so every rank is $O(\log N)$, and the final loop of DELETE does $O(\log N)$ links. Each ranked link reduces the number of roots by one, so it is paid by the root it removes. Each node is made hollow at most once and destroyed at most once. The rule $r(v) = \max(0, r(u) - 2)$ makes the children of a hollow node that are not accounted for by the rank of the new node $O(1)$ per decrease-key, as the two children of largest rank and the unranked ones.

$N$ is at most the number of inserts plus the number of decrease-keys. The paper also shows how to rebuild the heap from time to time so that the bound becomes $O(\log n)$ for the number $n$ of items in the heap.

**Dijkstra.** With this heap, [Dijkstra's algorithm](/dijkstra/) on $V$ vertices and $E$ edges takes $O(E + V \log V)$ time, as with a Fibonacci heap.

## Variants

- **Multi-root hollow heaps.** The paper first gives a version that keeps a list of roots and links only during delete, as in a lazy Fibonacci heap. The one-root version here links at once on insert, meld and decrease-key.
- **Other heaps with the same bounds.** The [Fibonacci heap](/fibonacci-heap/) and the [rank-pairing heap](/rank-pairing-heap/) have amortized decrease-key; the [strict Fibonacci heap](/strict-fibonacci-heap/) and the [Brodal queue](/brodal-queue/) have all the bounds in the worst case, with much more complex code.

## When to use it

Use a hollow heap when an algorithm does many decrease-keys and a heap with Fibonacci bounds is wanted, such as [Dijkstra's](/dijkstra/) or [Prim's algorithm](/prim/) on dense graphs. It is shorter to code than a Fibonacci heap: there are no cuts, no marks and no parent pointers to fix. A binary heap with lazy deletion, or a [pairing heap](/pairing-heap/), has smaller constant factors and is the usual choice when the bounds are not needed.

## Pitfalls

- **The scan of a node with an extra-parent child.** The sibling pointer of a node with two parents belongs to the list of its first parent. The scan of the extra parent must stop at that node, else it walks into the list of another node.
- **Destroying too soon.** A hollow node may be destroyed only when it has no parent left. A hollow node with two parents loses one parent per destroyed parent.
- **The handle after a decrease-key.** The item moves to a new node, so a caller that keeps node pointers in place of item handles points to a hollow node afterwards. Keep handles to items, and let each item point to its node.
- **Decrease-key of the root.** If the node is the root, change its key in place; making a new node and linking it with itself would break the heap.
- **Rank of the new node.** Taking $r(v) = r(u)$, or $r(u) - 1$, breaks the bound on ranks and the amortized analysis.

## Implementations

The Python class `HollowHeap` keeps a single `root` and `Node` objects with `item`, `key`, `rank`, `child`, `next` and `ep`; an `Item` handle points to its full node. `insert`, `meld`, `find_min`, `decrease_key`, `delete` and `delete_min` follow the pseudocode, with a dict from ranks to roots as the map $A$. `check_invariant` walks the DAG and checks (O), (R), the parent counts and the item pointers. Keys need only the operation "<".

## History

Hansen, Kaplan, Tarjan and Zwick presented hollow heaps at ICALP 2015, and the full version appeared in the ACM Transactions on Algorithms in 2017. They followed a line of work that looked for a simpler structure with the bounds of Fredman and Tarjan's Fibonacci heap (1987), among them the rank-pairing heaps of Haeupler, Sen and Tarjan (2011). The idea of moving an item to a new node in place of cutting a subtree is the new element.

## References
