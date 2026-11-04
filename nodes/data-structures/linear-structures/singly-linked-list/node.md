---
tag: QXYA7A
kind: data-structure
slug: singly-linked-list
name: Singly linked list
aliases:
- linked list
area: data-structures/linear-structures
level: intro
summary: Nodes each holding a value and a pointer to the next node.
implements: [stack, queue]
prereqs: [pointer, stack, queue]
see_also: [doubly-linked-list, circular-linked-list, sentinel-node, reverse-linked-list, unrolled-linked-list, xor-linked-list, dynamic-array, skip-list]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2 (Linked lists), searching, inserting into and deleting from a linked list
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.2.3 (Linked allocation), and Section 2.6 (History and bibliography) for the first uses of linked memory
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3 (Bags, Queues, and Stacks), the part on linked lists, with the linked-list stack and queue
  - url: https://opendatastructures.org/
    title: Pat Morin, Open Data Structures
    locator: Section 3.1 (SLList, a singly linked list)
  - paper: John McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, Communications of the ACM 3(4) (1960)
    locator: the list structure of S-expressions in memory, built from words with an address part and a decrement part
---

A singly linked list stores a sequence as a chain of nodes, where each node holds one item and a [pointer](/pointer/) to the next node, and the last node points to NIL. The list keeps a pointer to the first node, the *head*, and often one to the last node, the *tail*. It inserts and deletes at the front, after a known node, and at the tail in $O(1)$ time, without moving any item, but it needs $\Theta(k)$ time to reach the $k$-th item. It is the simplest linked structure, and the standard way to build a [stack](/stack/) and a [queue](/queue/) with a worst-case bound on each operation.

## In plain words

Picture a treasure hunt. Each card has a prize and tells you where the next card is hidden. You only know where the first card is. To reach the fifth card, you must read cards one to four first.

The cards can lie anywhere, so adding a card is cheap: write the new card, make it point to the old next card, and change one earlier card to point to the new one. Nothing else moves. Taking a card out is just as cheap if you hold the card before it. What the hunt cannot do is jump straight to the hundredth card, and it cannot go backwards, because each card knows only the card after it.

## The abstract type

A singly linked list holds a sequence $\langle a_1, \dots, a_n \rangle$ and supports:

- `push_front(L, k)`, `pop_front(L)` and `front(L)`: the operations of a [stack](/stack/), with the top at the head;
- `push_back(L, k)` with `pop_front(L)`: the operations of a [queue](/queue/), with the back at the tail;
- `search(L, k)`: the first node with key $k$, or NIL;
- `insert_after(L, y, k)`: insert $k$ right after the node $y$;
- `delete(L, k)`: remove the first node with key $k$, and report if one was found;
- `size(L)` and iteration from the head to the tail.

## Representation

A node $x$ has two fields: $x.key$, the item, and $x.next$, a pointer to the next node or NIL. The list $L$ has three fields: $L.head$, $L.tail$ and the count $L.n$.

**Invariant (I).** There are $n = L.n$ distinct nodes $x_1, \dots, x_n$ such that $L.head = x_1$, $x_i.next = x_{i+1}$ for $1 \le i < n$, and $x_n.next = \text{NIL}$. If $n \ge 1$ then $L.tail = x_n$. If $n = 0$ then $L.head = L.tail = \text{NIL}$. The list represents the sequence $\langle x_1.key, \dots, x_n.key \rangle$.

So the walk from the head reaches NIL after exactly $n$ steps, and it never meets a node twice. The tail pointer is what makes `push_back` cheap. The count is not needed by any operation, but it makes `size` cost $O(1)$ instead of $\Theta(n)$.

## Operations

The main block holds the operations at the two ends.

```pseudo id=main
PUSH-FRONT(L, k)
L1  x ← a new node; x.key ← k
L2  x.next ← L.head
L3  L.head ← x
L4  if L.tail = NIL then L.tail ← x
L5  L.n ← L.n + 1

PUSH-BACK(L, k)
L6  x ← a new node; x.key ← k; x.next ← NIL
L7  if L.tail = NIL then L.head ← x
L8  else L.tail.next ← x
L9  L.tail ← x
L10 L.n ← L.n + 1

POP-FRONT(L)                               ▷ L.n ≥ 1
L11 x ← L.head
L12 L.head ← x.next
L13 if L.head = NIL then L.tail ← NIL
L14 L.n ← L.n − 1
L15 return x.key
```

PUSH-FRONT links the new node in front of the old head (line L2) before it moves the head (line L3). If the list was empty, the new node is also the tail (line L4). PUSH-BACK appends after the old tail (line L8), or makes the node the head when the list is empty (line L7). POP-FRONT moves the head one node on (line L12). When the list becomes empty, line L13 clears the tail too, so that it does not point to the removed node. Each of the three costs $\Theta(1)$ in the worst case.

```pseudo id=search
SEARCH(L, k)
S1  x ← L.head
S2  while x ≠ NIL and x.key ≠ k do
S3      x ← x.next
S4  return x
```

SEARCH walks from the head and stops at the first node with key $k$, or at NIL. If the first match is node $x_i$, it makes $i$ key comparisons. A miss makes $n$. So the cost is $\Theta(n)$ in the worst case.

```pseudo id=insert-after
INSERT-AFTER(L, y, k)                      ▷ y is a node of L
A1  x ← a new node; x.key ← k
A2  x.next ← y.next
A3  y.next ← x
A4  if L.tail = y then L.tail ← x
A5  L.n ← L.n + 1
```

The order of lines A2 and A3 matters: line A2 saves the rest of the list in the new node before line A3 overwrites $y.next$. The cost is $\Theta(1)$. There is no INSERT-BEFORE in $O(1)$ time, because the node before $y$ is not known.

```pseudo id=delete
DELETE(L, k)                               ▷ remove the first node with key k
D1  prev ← NIL; x ← L.head
D2  while x ≠ NIL and x.key ≠ k do
D3      prev ← x; x ← x.next
D4  if x = NIL then return false
D5  if prev = NIL then L.head ← x.next else prev.next ← x.next
D6  if L.tail = x then L.tail ← prev
D7  L.n ← L.n − 1
D8  return true
```

To unlink a node, the list must change the link that points to it, which is in the node before it. So DELETE walks with two pointers, $prev$ one node behind $x$. Line D5 has two cases: the node is the head, or it is not. A [sentinel node](/sentinel-node/) before the head, or a pointer to the link field (see [pointer](/pointer/)), removes this case. Line D6 moves the tail back when the last node goes. The search costs $\Theta(n)$ in the worst case and the unlink $\Theta(1)$.

## Example

Start with the empty list and run these operations. The head is on the left.

| step | operation | result | list after | head, tail |
|---|---|---|---|---|
| 1 | push_front 3 | | 3 | 3, 3 |
| 2 | push_back 7 | | 3 → 7 | 3, 7 |
| 3 | push_front 1 | | 1 → 3 → 7 | 1, 7 |
| 4 | push_back 9 | | 1 → 3 → 7 → 9 | 1, 9 |
| 5 | search 7 | the node of 7, after 3 comparisons | 1 → 3 → 7 → 9 | 1, 9 |
| 6 | insert_after (node of 7) 4 | | 1 → 3 → 7 → 4 → 9 | 1, 9 |
| 7 | delete 3 | true | 1 → 7 → 4 → 9 | 1, 9 |
| 8 | pop_front | 1 | 7 → 4 → 9 | 7, 9 |
| 9 | delete 9 | true | 7 → 4 | 7, 4 |
| 10 | delete 5 | false | 7 → 4 | 7, 4 |

At step 7, the loop of line D2 stops with $prev$ at the node of 1 and $x$ at the node of 3, and line D5 sets the next field of the node of 1 to the node of 7. At step 9, the deleted node is the tail, so line D6 moves the tail back to the node of 4. Without line D6, a later push_back would link the new node after the removed node of 9, and the new node would not be reachable from the head.

## Correctness

Each operation keeps the invariant (I) and changes the represented sequence as the abstract type says. PUSH-FRONT makes the new node $x_0$ the first of the chain, and the old chain follows it. PUSH-BACK sets $x_n.next$ to the new node, whose next is NIL. POP-FRONT removes $x_1$ from the chain. INSERT-AFTER on $y = x_i$ puts the new node between $x_i$ and $x_{i+1}$. SEARCH keeps the [loop invariant](/loop-invariant/) that no node before $x$ has key $k$. DELETE keeps the invariant that $prev$ is the node before $x$ (or NIL when $x$ is the head), and it bypasses $x$ by one link. In each case, the tail and the count follow the change. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst-case time | notes |
|---|---|---|
| push_front, pop_front, front | $\Theta(1)$ | at the head |
| push_back | $\Theta(1)$ | needs the tail pointer; $\Theta(n)$ without it |
| insert_after a known node | $\Theta(1)$ | |
| search, delete by key | $\Theta(n)$ | $i$ comparisons when the first match is at position $i$ |
| delete a known node, pop_back | $\Theta(n)$ | the node before it must be found |
| access the $k$-th item | $\Theta(k)$ | |
| size | $\Theta(1)$ | with the count $L.n$ |
| space | $n$ nodes | one item and one pointer each, plus three fields |

These bounds hold on the [word RAM](/word-ram/) and on the [pointer machine](/pointer-machine/), with a new node made in $O(1)$ time. Each node is a separate block of memory, so a walk over the list jumps around in memory and makes poor use of the cache, unlike a walk over an [array](/array/).

## Variants

- **Doubly linked list.** A [doubly linked list](/doubly-linked-list/) adds a pointer to the previous node, so it deletes a known node and pops at the back in $O(1)$ time, at the cost of one more pointer per node.
- **Circular list.** In a [circular linked list](/circular-linked-list/) the last node points back to the first. One pointer to the tail then gives both ends.
- **Sentinel.** A [sentinel node](/sentinel-node/) at the front makes the head an ordinary node and removes the special cases of lines L4, L7, L13 and D5.
- **Persistent list.** If nodes are never changed after they are made, push_front makes a new list that shares all the old nodes, and the old list stays valid. This is the list of Lisp and of functional languages, and the simplest [persistent data structure](/persistent-data-structure/).
- **More items per node.** An [unrolled linked list](/unrolled-linked-list/) keeps a small array in each node, which uses fewer pointers and the cache better.
- **One field for two links.** An [XOR linked list](/xor-linked-list/) stores the XOR of the previous and the next address, which gives two-way travel at the memory cost of one pointer.
- **Faster search.** A [skip list](/skip-list/) adds express links and searches a sorted list in $O(\log n)$ expected time. A [self-organizing list](/self-organizing-list/) moves the items that are asked for often toward the head.
- **Reversal.** [In-place reversal](/reverse-linked-list/) turns all the links around in $\Theta(n)$ time and $O(1)$ extra space.

## When to use it

Use a singly linked list for a stack or a queue when each operation must be fast in the worst case, not only on average: a [dynamic array](/dynamic-array/) gives $O(1)$ amortized time, but a single push can cost $\Theta(n)$ when it resizes. Use it when items are inserted and deleted in the middle at places the program already holds, when nodes must keep their addresses, or when many lists share their tails. Do not use it when the program indexes by position or scans large sequences often: an array then wins, because it reads memory in order and has no pointer per item. When you need to delete a node that you hold, or to walk backwards, use a doubly linked list.

## Pitfalls

- **The tail after deleting the last node.** Without line D6, deleting the tail leaves $L.tail$ on a removed node, and the next push_back links into nothing. The same holds for line L13 when pop_front empties the list. The test of step 9 of the example catches this.
- **Losing the rest of the list.** Doing line A3 before line A2 sets $y.next \leftarrow x$ and then $x.next \leftarrow y.next = x$: the node points to itself, and the old rest of the list is lost. Save the old link first.
- **Deleting the head.** The case $prev = \text{NIL}$ of line D5 must change $L.head$, not a field of a node. Code that writes `prev.next = x.next` without the test fails on a match at the head.
- **An $O(1)$ pop at the back.** A singly linked list cannot pop its last node in $O(1)$ time, even with a tail pointer, because the new tail is the node before it. So a queue built on it must add at the tail and remove at the head, not the reverse.
- **A node in two places.** Inserting a node that is already in the list makes a cycle, and each walk then runs forever. Make a new node for each insert, as lines L1, L6 and A1 do.
- **Recursion on long lists.** A recursive walk uses stack space proportional to the length, which overflows the call stack of most languages for a list of a million nodes. Use a loop.

## Implementations

## History

Linked memory was first used by Allen Newell, Cliff Shaw and Herbert Simon around 1955 and 1956, in the Information Processing Language (IPL) that they built for their Logic Theorist program; Knuth gives this history in Section 2.6 of Volume 1. John McCarthy's Lisp, described in 1960, made the linked list of two-field cells its main data structure. Knuth's Section 2.2.3 and CLRS Section 10.2 give the standard treatment that this page follows.

## References
