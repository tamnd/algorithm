---
tag: N4ZP5Y
kind: data-structure
slug: circular-linked-list
name: Circular linked list
aliases:
- ring list
area: data-structures/linear-structures
level: intro
summary: List whose last node points back to the first, suited to round-robin iteration.
implements: [queue, stack]
prereqs: [linked-list]
see_also: [doubly-linked-list, round-robin, josephus-problem, sentinel-node, circular-buffer, floyd-cycle-detection, fibonacci-heap, singly-linked-list]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.4 (Circular lists), with the pointer PTR to the rear node and the operations of insertion at the front and the rear and deletion at the front
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, exercise 1.3.29 (a queue on a circular linked list with one pointer to the last node) and exercise 1.3.37 (Josephus problem)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2, the circular, doubly linked list with a sentinel
---

A circular linked list is a [linked list](/linked-list/) in which the last node points back to the first instead of to NIL, so the nodes form a ring. The usual form keeps one pointer, to the last node: its successor is the first node, so both ends are reached in $O(1)$ time. With that one pointer the list gives push at the front, push at the back, pop at the front and rotation by one place, each in $O(1)$ worst-case time. Rotation, the move of the front item to the back, is a single pointer move, which makes the ring the natural structure for [round-robin](/round-robin/) scheduling and for the [Josephus problem](/josephus-problem/).

## In plain words

Picture children sitting in a circle, each holding the hand of the child on their left. There is no first or last child in the circle itself. You only keep a finger on one child, and you call the child after it the first.

To let the next child have a turn and then go to the back, you move your finger one place. Nobody stands up. To add a child, you open one pair of hands and put the new child in between. To remove the first child, the child under your finger takes the hand of the child after the one leaving. A plain line of children would need a finger on both ends to do all of this.

## The abstract type

The structure implements the [queue](/queue/) type (push at the back, pop at the front) and the [stack](/stack/) type (push and pop at the front) at once, and adds `rotate`, which moves the front item to the back. It does not give $O(1)$ pop at the back: the node before the last one is a full turn away. For that, use the doubly linked form of [doubly linked list](/doubly-linked-list/).

## Representation

Each node $v$ has fields $v.key$ and $v.next$. The list $L$ has a pointer $L.last$ and a count $L.n$.

**Invariant.** If $n = 0$, then $L.last = $ NIL. If $n \ge 1$, the items are in distinct nodes $v_0, \ldots, v_{n-1}$ with $v_i.next = v_{i+1}$ for $i < n - 1$, $v_{n-1}.next = v_0$, and $L.last = v_{n-1}$. The list held is $(v_0.key, \ldots, v_{n-1}.key)$, so the front is $L.last.next$.

A list of one node is a node that points to itself.

## Operations

```pseudo id=main
PUSH-FRONT(L, x)
L1  v ← a new node with key x
L2  if L.last = NIL then v.next ← v, L.last ← v
L3  else v.next ← L.last.next, L.last.next ← v
PUSH-BACK(L, x)
L4  PUSH-FRONT(L, x)
L5  L.last ← L.last.next
POP-FRONT(L)                               ▷ L is not empty
L6  v ← L.last.next
L7  if v = L.last then L.last ← NIL else L.last.next ← v.next
L8  return v.key
ROTATE(L)                                  ▷ L is not empty
L9  L.last ← L.last.next
```

The counts are updated with the pushes and the pop and are left out of the lines. PUSH-FRONT links the new node between the last node and the old first node. PUSH-BACK makes the same link and then moves $L.last$ onto the new node, which makes it last instead of first: in a ring, "after the last node" and "before the first node" are the same place. POP-FRONT unlinks the node after the last one. ROTATE moves $L.last$ forward by one, so the old front becomes the back.

## Example

Start from the empty list. The column "ring" lists the items from the front, and "last" is the key of $L.last$.

| operation | ring after it | last | result |
|---|---|---|---|
| push_back(1) | 1 | 1 | |
| push_back(2) | 1 2 | 2 | |
| push_back(3) | 1 2 3 | 3 | |
| push_front(0) | 0 1 2 3 | 3 | |
| rotate | 1 2 3 0 | 0 | |
| pop_front | 2 3 0 | 0 | 1 |
| rotate | 3 0 2 | 2 | |
| pop_front | 0 2 | 2 | 3 |

In push_back(1) on the empty list, line L2 makes a node that points to itself, and line L5 leaves $L.last$ on it. In push_back(2), line L3 puts 2 after 1, and line L5 moves $L.last$ to 2. Each rotate writes one pointer and moves no node.

**Josephus.** Seven people 1 to 7 stand in a ring, and every third one leaves. With the ring built by push_back, repeat: rotate twice, then pop_front. The pops return 3, 6, 2, 7, 5, 1, and the last one left is 4. Each step costs $O(k)$ for a step size $k$, so the whole order costs $O(nk)$.

## Correctness

PUSH-FRONT on the empty list makes a ring of one node. On a non-empty list, it reads the old first node $v_0 = L.last.next$ into $v.next$ before line L3 writes $L.last.next = v$, so the new ring is $v, v_0, \ldots, v_{n-1}$ and $L.last$ is still $v_{n-1}$. PUSH-BACK then moves $L.last$ to $v$, so the same ring is read from $v_0$: the list is $(v_0, \ldots, v_{n-1}, v)$. POP-FRONT removes $v_0$ by linking $v_{n-1}$ to $v_1$, or empties the list when $n = 1$. ROTATE changes no link, only the starting point. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | pointer writes |
|---|---|---|
| push_front, push_back | $O(1)$ worst case | 2 or 3 |
| pop_front | $O(1)$ worst case | 1 |
| rotate | $O(1)$ worst case | 1 |
| pop_back, access by index $i$ | $\Theta(n)$, $\Theta(i + 1)$ | |
| space | $n$ nodes of 2 fields, one pointer | |

Two rings $A$ and $B$ are joined in $O(1)$ time by swapping $A.last.next$ and $B.last.next$ and keeping $B.last$ as the new last: the result is $A$ followed by $B$. Knuth uses this for the concatenation of circular lists.

## Variants

- **Circular doubly linked list.** Add `prev` pointers. With a [sentinel node](/sentinel-node/) in the ring, this is the form of CLRS Section 10.2 and of the [doubly linked list](/doubly-linked-list/) page, and it adds pop at the back in $O(1)$.
- **Head pointer only.** Keeping a pointer to the first node instead of the last makes push at the back cost $\Theta(n)$, since the last node must be found first. The pointer to the last node gives both ends.
- **Fibonacci heap root list.** The roots and the children of each node of a [Fibonacci heap](/fibonacci-heap/) are kept in circular doubly linked lists, so that two root lists are joined in $O(1)$.
- **[Circular buffer](/circular-buffer/).** The same ring idea on an array, with the indices taken modulo the capacity.

## When to use it

Use a circular linked list when the program cycles through a set of items in turn and the set changes: a [round-robin](/round-robin/) scheduler gives each task a time slice, rotates, and removes a task when it ends. The ring is also the natural model for the [Josephus problem](/josephus-problem/) and for games where turns go around a table. As a plain queue it saves one pointer compared with a list with $head$ and $tail$. When the number of items has a known bound, a [circular buffer](/circular-buffer/) does the same job without allocating nodes.

## Pitfalls

- **A loop that never ends.** A walk that waits for `x = NIL` never stops, because no node points to NIL. Stop when the walk comes back to its first node, or count $n$ steps. A list that is a ring by mistake is the subject of [cycle detection](/floyd-cycle-detection/).
- **Order of the writes in line L3.** Writing $L.last.next \leftarrow v$ before reading $L.last.next$ into $v.next$ makes $v$ point to itself and loses the ring.
- **The one-node case in POP-FRONT.** With one node, $v = L.last$, and linking $L.last.next \leftarrow v.next$ leaves $L.last$ on the deleted node. Line L7 must set $L.last$ to NIL.
- **Forgetting to move last in PUSH-BACK.** Without line L5, the new node becomes the front, not the back.

## Implementations

## History

Knuth (Volume 1, Section 2.2.4) describes circular lists with a pointer to the rear node, shows that one pointer gives insertion at both ends and deletion at the front, and uses them for the arithmetic of polynomials. Sedgewick and Wayne pose the queue on a circular list with one pointer to the last node as an exercise. The Josephus problem, which the ring models, is much older; Knuth (Volume 1, Section 1.3.2, exercise 22) gives a history of it.

## References
