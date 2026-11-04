---
tag: B9V487
kind: data-structure
slug: doubly-linked-list
name: Doubly linked list
aliases:
- two-way linked list
area: data-structures/linear-structures
level: intro
summary: Nodes with pointers to both neighbours, so a node can be unlinked in O(1).
implements: [list, deque]
prereqs: [linked-list]
see_also: [sentinel-node, circular-linked-list, xor-linked-list, dancing-links, lru-cache, singly-linked-list, deque, skip-list]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2 (Linked lists), the procedures LIST-SEARCH, LIST-PREPEND, LIST-INSERT and LIST-DELETE, and the subsection Sentinels
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.5 (Doubly linked lists)
  - paper: "Donald E. Knuth, Dancing links, in Millennial Perspectives in Computer Science, Palgrave (2000), arXiv:cs/0011047"
    locator: Section 1, the removal and restoration of a node in a doubly linked list
---

A doubly linked list is a [linked list](/linked-list/) in which each node holds two pointers: `next` to the node after it and `prev` to the node before it. With the back pointer, a program that holds a node can delete it, or insert a new node before it, in $O(1)$ time, without a search for its predecessor. With a [sentinel node](/sentinel-node/) that closes the chain into a ring, the list has no special cases for the empty list or for the ends, and it gives a [deque](/deque/) with $O(1)$ worst-case time for each end operation. The cost is one more pointer per node and two more pointer writes per update.

## In plain words

Think of a train in which each carriage is coupled to the one in front and the one behind. If you stand in any carriage, you can walk forward or backward. To take one carriage out, you join its front neighbour to its back neighbour, and the rest of the train is not touched.

A plain linked list only has the forward coupling, so to take out a carriage you must first walk from the engine to find the one in front of it. The doubly linked list keeps both couplings and pays for it with one more link per carriage. An extra dummy carriage that joins the two ends into a ring means the first and last carriages need no special treatment.

## The abstract type

The structure implements the [list](/list/) type, and in particular the [deque](/deque/) type: insert and delete at the front and at the back. Its strong operations work on a *handle*, a pointer to a node that the program got from an earlier insert or search: `insert_after(p, x)`, `insert_before(p, x)` and `delete(p)`, each in $O(1)$. Access by index $i$ walks from the nearer end and costs $\Theta(\min(i, n - i) + 1)$.

## Representation

Each node $v$ has three fields: $v.key$, $v.next$ and $v.prev$. The list $L$ has one sentinel node $L.nil$, which holds no item, and a count $L.n$. Write the item nodes from the front to the back as $v_0, \ldots, v_{n-1}$ and set $v_{-1} = v_n = L.nil$.

**Invariant.** The nodes $L.nil, v_0, \ldots, v_{n-1}$ are distinct, $v_{i}.next = v_{i+1}$ for $-1 \le i \le n - 1$, and $v_{i}.prev = v_{i-1}$ for $0 \le i \le n$. So the `next` pointers form one ring through the sentinel, and the `prev` pointers form the same ring in reverse. For the empty list, $L.nil.next = L.nil.prev = L.nil$.

The front is $L.nil.next$ and the back is $L.nil.prev$, so both ends are one pointer away.

## Operations

```pseudo id=main
INSERT-AFTER(L, p, x)                      ▷ p is L.nil or a node of L
L1  v ← a new node with key x
L2  v.next ← p.next, v.prev ← p
L3  p.next.prev ← v
L4  p.next ← v, L.n ← L.n + 1
DELETE(L, v)                               ▷ v is a node of L, v ≠ L.nil
L5  v.prev.next ← v.next
L6  v.next.prev ← v.prev, L.n ← L.n − 1
L7  return v.key
```

```pseudo id=search
SEARCH(L, k)
S1  x ← L.nil.next
S2  while x ≠ L.nil and x.key ≠ k
S3      x ← x.next
S4  if x = L.nil then return NIL else return x
```

INSERT-AFTER links the new node between $p$ and its old successor. Line L2 sets the two pointers of the new node first, so line L3 can still reach the old successor as `p.next`. Line L4 then makes $p$ point to $v$. DELETE joins the two neighbours of $v$ to each other. It does not change the fields of $v$, which is what makes the [dancing links](/dancing-links/) trick possible.

The other operations are short forms:

- `push_front(x)` is INSERT-AFTER$(L, L.nil, x)$, and `push_back(x)` is INSERT-AFTER$(L, L.nil.prev, x)$.
- `insert_before(p, x)` is INSERT-AFTER$(L, p.prev, x)$.
- `pop_front` is DELETE$(L, L.nil.next)$ and `pop_back` is DELETE$(L, L.nil.prev)$, on a non-empty list.

Because the sentinel stands in for both ends, no line tests for NIL in INSERT-AFTER or DELETE.

## Example

Start from the empty list. A node is named by its key. The column "ring" lists the nodes in `next` order from the sentinel, written $\bullet$.

| operation | ring after it | result |
|---|---|---|
| push_back(1) | $\bullet$ 1 | node 1 |
| push_back(2) | $\bullet$ 1 2 | node 2 |
| push_back(3) | $\bullet$ 1 2 3 | node 3 |
| insert_after(node 1, 5) | $\bullet$ 1 5 2 3 | node 5 |
| delete(node 2) | $\bullet$ 1 5 3 | 2 |
| push_front(9) | $\bullet$ 9 1 5 3 | node 9 |
| pop_back | $\bullet$ 9 1 5 | 3 |
| search(5) | $\bullet$ 9 1 5 | node 5 |
| search(4) | $\bullet$ 9 1 5 | NIL |

In insert_after(node 1, 5), line L2 sets $5.next = 2$ and $5.prev = 1$, line L3 sets $2.prev = 5$, and line L4 sets $1.next = 5$. In delete(node 2), line L5 sets $5.next = 3$ and line L6 sets $3.prev = 5$. Node 2 still points to 5 and 3, but no node of the ring points to it. At the end, $\bullet.next = 9$ and $\bullet.prev = 5$.

## Correctness

The invariant holds for the empty list, where the ring is the sentinel alone. INSERT-AFTER with $p = v_j$ ($-1 \le j \le n - 1$) writes four fields: the two of the new node, $v_{j+1}.prev$ and $v_j.next$. After it, the ring is $v_{-1}, \ldots, v_j, v, v_{j+1}, \ldots$ in both directions. DELETE of $v_j$ writes only $v_{j-1}.next$ and $v_{j+1}.prev$, which removes $v_j$ from both rings at once. In both cases the other pointers do not change, so they still match the invariant. SEARCH visits $v_0, v_1, \ldots$ in order and stops at the first match or back at the sentinel. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | pointer writes |
|---|---|---|
| insert after or before a handle, push at either end | $O(1)$ worst case | 4 |
| delete a handle, pop at either end | $O(1)$ worst case | 2 |
| search by key | $\Theta(n)$ worst case | 0 |
| access by index $i$ | $\Theta(\min(i, n - i) + 1)$ | 0 |
| space | $n + 1$ nodes of 3 fields | |

A singly linked list uses 2 fields per node, so the doubly linked list uses 1.5 times as much space for small keys. Concatenation of two lists with sentinels costs $O(1)$: four pointer writes join the back of one ring to the front of the other, and the second sentinel is dropped.

## Variants

- **Without a sentinel.** Keep $head$ and $tail$ pointers and use NIL at the ends. Each update then needs tests for the first and last node. CLRS gives both forms.
- **[Circular linked list](/circular-linked-list/).** The ring without a sentinel: the last node points to the first. Rotation is one pointer move.
- **[XOR linked list](/xor-linked-list/).** Store $prev \oplus next$ in one field. A walk from either end recovers both neighbours, but a handle alone is not enough to delete a node, and the trick does not work with a garbage collector.
- **[Dancing links](/dancing-links/).** Since DELETE does not change $v.prev$ and $v.next$, the two writes `v.prev.next ← v` and `v.next.prev ← v` put $v$ back, provided the deletions are undone in the reverse order. Knuth's [Algorithm X](/algorithm-x/) for [exact cover](/exact-cover/) is built on this.
- **Intrusive lists.** The `prev` and `next` fields live inside the user's object, as in the Linux kernel's `list_head`. Then an object can be removed from the list given only the object, and no node is allocated.
- **[Skip list](/skip-list/).** Adds more forward pointers at random levels for $O(\log n)$ expected search.

## When to use it

Use a doubly linked list when the program holds handles to items and must delete them, or insert next to them, in constant time. The standard case is an [LRU cache](/lru-cache/): a [hash table](/hash-table/) maps each key to its node, and on each access the node moves to the front in $O(1)$. Other cases are the free lists of memory allocators, the run queues of schedulers, and the root list and child lists of a [Fibonacci heap](/fibonacci-heap/). If the program only adds and removes at the ends, an array-based [circular buffer](/circular-buffer/) is faster in practice because its items sit next to each other in memory. If it only needs one direction, a [singly linked list](/singly-linked-list/) uses less space.

## Pitfalls

- **Wrong order of the writes in INSERT-AFTER.** If line L4 runs before line L2 reads `p.next`, then $v.next$ becomes $v$ itself and the old successor is lost. Read `p.next` first, or save it in a variable.
- **Updating one direction only.** Every insert must write both a `next` and a `prev`, and every delete must fix both neighbours. A list whose `next` ring is right but whose `prev` ring is wrong passes forward tests and fails when walked backward.
- **Deleting the sentinel.** DELETE$(L, L.nil)$ on an empty list, as a pop on an empty list does, breaks the ring. Test that $L.n > 0$ first.
- **Stale handles.** After DELETE$(L, v)$, the fields of $v$ still point into the list. A second DELETE of $v$ then corrupts the neighbours. Set the fields of $v$ to NIL after deletion when handles may be kept, unless dancing links needs them.
- **Handles from another list.** INSERT-AFTER and DELETE do not check that the node belongs to $L$. A node of a different list changes that list and leaves $L.n$ wrong.

## Implementations

## History

Knuth (Volume 1, Section 2.2.5) describes doubly linked lists with a list head that links the two ends, which is the sentinel form, and discusses their use in simulation programs. The sentinel form with the names LIST-INSERT and LIST-DELETE is the one taught in CLRS Section 10.2. Knuth's paper "Dancing links" (2000) made popular the observation that a deleted node can be put back with two writes, an idea he credits to Hiroshi Hitotumatu and Kohei Noshita (1979).

## References
