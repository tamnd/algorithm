---
tag: 8R26VK
kind: data-structure
slug: linked-list
name: Linked list
aliases:
- Pointers and linked structures
area: data-structures/linear-structures
level: intro
summary: A sequence of nodes where each node stores a value and a pointer to the next, allowing constant time insertion and deletion at known positions.
implements: [list]
prereqs: [pointer, array]
see_also: [singly-linked-list, doubly-linked-list, circular-linked-list, sentinel-node, list-reversal, floyd-cycle-detection, unrolled-linked-list, free-list]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2 (Linked lists)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.3 (Linked allocation), and Section 2.6 (History and bibliography) for the origin in IPL
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, Linked lists
  - paper: "John McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, Communications of the ACM 3(4) (1960)"
    locator: the representation of S-expressions by list structure
---

A linked list stores a sequence as a chain of *nodes*: each node holds one item and a [pointer](/pointer/) to the next node, and the list keeps a pointer to the first node, the *head*. Given a pointer to a node, an insert or a delete just after it costs $\Theta(1)$, because only one or two pointers change and no item moves. The price is that the item at position $i$ is reached only by following $i$ pointers from the head, so access by index costs $\Theta(i)$, where an [array](/array/) needs $\Theta(1)$. Linked lists are the base of [stacks](/stack/), [queues](/queue/), hash chains, adjacency lists and the free lists of memory allocators.

## In plain words

Think of a treasure hunt. Each card holds one word of a message and says where the next card is hidden. You only know where the first card is. To read the fifth word, you must find the first four cards on the way.

To add a word in the middle, write it on a new card, hide the card anywhere, and change one note: the card before it now points to the new card, and the new card points to the card that came next. No other card moves. To take a word out, change the note of the card before it so that it skips that card. This is why a linked list changes fast but finds a position slowly.

## The abstract type

A linked list implements the [list](/list/) type: a finite sequence with search, insert and delete. It is best at the operations that act at a node the program already holds: insert at the front, insert after a node, delete at the front and delete after a node. A [doubly linked list](/doubly-linked-list/) adds a pointer back, so that a node can also delete itself.

## Representation

A node $v$ has two fields: $v.key$, the item, and $v.next$, a pointer to the next node or NIL. The list $L$ has the field $L.head$ and, for the cost of `length`, a count $L.n$.

**Invariant.** Starting from $L.head$ and following $next$ pointers visits $L.n$ distinct nodes $v_0, v_1, \ldots, v_{n-1}$ and then reaches NIL. The list that $L$ holds is $(v_0.key, \ldots, v_{n-1}.key)$. In particular the chain has no cycle, and $L.head = $ NIL exactly when $L.n = 0$.

The nodes can be anywhere in memory. They do not need to be in order or near each other.

## Operations

```pseudo id=main
PUSH-FRONT(L, x)
L1  v ← a new node with v.key = x
L2  v.next ← L.head
L3  L.head ← v, L.n ← L.n + 1
INSERT-AFTER(L, p, x)                      ▷ p is a node of L
L4  v ← a new node with v.key = x
L5  v.next ← p.next
L6  p.next ← v, L.n ← L.n + 1
DELETE-FRONT(L)                            ▷ L.head ≠ NIL
L7  v ← L.head
L8  L.head ← v.next, L.n ← L.n − 1
L9  return v.key
DELETE-AFTER(L, p)                         ▷ p is a node of L, p.next ≠ NIL
L10 v ← p.next
L11 p.next ← v.next, L.n ← L.n − 1
L12 return v.key
```

PUSH-FRONT makes the new node point to the old first node, then makes the head point to the new node. INSERT-AFTER does the same with $p.next$ in place of $L.head$. The order of the two writes matters: line L5 reads $p.next$ before line L6 overwrites it. Each of these costs $\Theta(1)$.

DELETE-FRONT and DELETE-AFTER make the pointer that leads to $v$ skip over it. The node $v$ is then unreachable. In a language with garbage collection it is freed later; in C the caller must free it. Each costs $\Theta(1)$.

A singly linked list cannot delete a node $v$ in $\Theta(1)$ when it has only $v$: it needs the node before $v$, and finding that node takes a walk from the head.

```pseudo id=search
SEARCH(L, x)                               ▷ the first node with key x, or NIL
S1  p ← L.head
S2  while p ≠ NIL and p.key ≠ x
S3      p ← p.next
S4  return p
NODE-AT(L, i)                              ▷ 0 ≤ i < L.n
S5  p ← L.head
S6  repeat i times: p ← p.next
S7  return p
```

SEARCH follows the chain until it finds $x$ or falls off the end. It makes at most $n$ key comparisons. NODE-AT follows $i$ pointers, so it costs $\Theta(i + 1)$. To insert at position $i \ge 1$, call INSERT-AFTER on NODE-AT$(L, i - 1)$; to delete at position $i \ge 1$, call DELETE-AFTER on the same node. Both then cost $\Theta(i)$.

## Example

Start with the empty list. A node is written by its key.

| operation | list after it | result | pointers written |
|---|---|---|---|
| push-front(3) | 3 | | v.next, head |
| push-front(7) | 7 → 3 | | v.next, head |
| insert-after(node 7, 5) | 7 → 5 → 3 | | v.next, 7.next |
| search(5) | 7 → 5 → 3 | node 5 | none |
| search(4) | 7 → 5 → 3 | NIL | none |
| delete-after(node 5) | 7 → 5 | 3 | 5.next |
| delete-front | 5 | 7 | head |

In insert-after(node 7, 5), line L5 sets the new node's next to node 3, and line L6 sets node 7's next to the new node. The search for 5 compares with 7 and then 5, so it makes 2 key comparisons. The search for 4 makes 3 comparisons and reaches NIL. In delete-after(node 5), line L11 sets node 5's next to NIL, the old next of node 3.

## Correctness

Each operation keeps the invariant: the chain from the head is finite, has no repeated node, has length $L.n$, and spells the right list. PUSH-FRONT puts one new node before the old chain, and INSERT-AFTER splices one new node between $p$ and its old successor. The deletes remove exactly one node from the chain and keep the order of the rest. SEARCH has the loop invariant that no node before $p$ holds $x$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Costs are in the [random-access machine](/random-access-machine/), with $O(1)$ time to allocate a node.

| operation | time | notes |
|---|---|---|
| push-front, delete-front | $\Theta(1)$ worst case | |
| insert-after, delete-after a given node | $\Theta(1)$ worst case | |
| access, insert or delete at position $i$ | $\Theta(i + 1)$ worst case | a walk of $i$ pointers |
| search | $\Theta(n)$ worst case | at most $n$ comparisons |
| delete a given node $v$ | $\Theta(n)$ worst case | needs the predecessor; $\Theta(1)$ in a doubly linked list |
| append at the end | $\Theta(n)$, or $\Theta(1)$ with a tail pointer | |
| length | $\Theta(1)$ with the count, else $\Theta(n)$ | |
| space | $n$ nodes | one item and one pointer each |

The space is $\Theta(n)$, but each item pays for one pointer, and each node allocation has its own header in most memory allocators. A scan is also slower than a scan of an array of the same length, because the nodes are not contiguous and each step can miss the cache.

## Variants

- **Singly and doubly linked.** This page uses one pointer per node, as in a [singly linked list](/singly-linked-list/). A [doubly linked list](/doubly-linked-list/) adds a pointer to the previous node, so that it can delete a given node and walk backward in $\Theta(1)$ per step.
- **Tail pointer.** A pointer to the last node gives append in $\Theta(1)$. A singly linked list with head and tail is the standard linked [queue](/queue/).
- **Circular.** In a [circular linked list](/circular-linked-list/) the last node points back to the first.
- **Sentinel.** A [sentinel node](/sentinel-node/) before the first item removes the special case of the head: PUSH-FRONT becomes INSERT-AFTER(sentinel).
- **Unrolled.** An [unrolled linked list](/unrolled-linked-list/) stores a small array of items in each node, which uses the cache better.
- **XOR links.** An [XOR linked list](/xor-linked-list/) stores the XOR of the two neighbour addresses in one field.
- **Persistent lists.** In functional languages, a list cell is never changed. PUSH-FRONT shares the old list as the tail of the new one, so many versions of a list coexist.

## When to use it

Use a linked list when the program inserts and deletes at places where it already holds a node, and seldom needs position $i$: a [stack](/stack/), a queue, the chains of a [hash table](/hash-table/), an LRU list, or the free list of an allocator. Use it when items must not move in memory, because other structures point to them. Use an [array](/array/) or a [dynamic array](/dynamic-array/) when the program reads by index, sorts, or scans a lot. For a long sequence with edits at arbitrary positions, a balanced tree or a [rope](/rope/) gives $O(\log n)$ for both access and edit.

## Pitfalls

- **Lost tail.** Writing line L6 before line L5 sets $p.next \leftarrow v$ and then $v.next \leftarrow p.next = v$. The new node points to itself, and the rest of the list is lost. Always link the new node to its successor first.
- **NIL at the ends.** DELETE-FRONT on an empty list and DELETE-AFTER on the last node dereference NIL. Test $L.head \ne$ NIL and $p.next \ne$ NIL first, or use a sentinel.
- **Forgotten head update.** Inserting or deleting at position 0 changes $L.head$, not the $next$ field of a node. Code that handles only the general case loses the first node.
- **Use after free.** In C, free $v$ only after line L11 has read $v.next$. In a loop that deletes nodes, save $p.next$ before freeing $p$.
- **Deep recursion.** A recursive walk of a list of a million nodes overflows the call stack in most languages. Walk with a loop.
- **A cycle by mistake.** A bad splice can make the chain loop back. Then SEARCH for an absent key never ends. [Cycle detection](/floyd-cycle-detection/) finds such a bug.

## Implementations

## History

Allen Newell, J. C. Shaw and Herbert A. Simon introduced linked lists around 1956 in their Information Processing Language (IPL), which they built for programs that searched for proofs and solved problems. Knuth tells this history in Section 2.6 of Volume 1, and his Section 2.2.3 calls the method *linked allocation*, in contrast to the *sequential allocation* of arrays. Lisp, which John McCarthy described in 1960, made the linked list of cons cells its central data structure.

## References
