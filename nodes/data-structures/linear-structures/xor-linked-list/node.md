---
tag: GE847R
kind: data-structure
slug: xor-linked-list
name: XOR linked list
aliases:
- XOR list
- memory-efficient doubly linked list
area: data-structures/linear-structures
level: advanced
summary: Doubly linked list storing the XOR of the two neighbour addresses in one field.
implements: [deque]
prereqs: [doubly-linked-list, pointer]
see_also: [doubly-linked-list, singly-linked-list, deque, xor-swap, bitwise-operations, reverse-linked-list, tracing-garbage-collection, unrolled-linked-list]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 10.2, Exercise 10.2-8 (one value x.np per item, the XOR of x.next and x.prev, with SEARCH, INSERT, DELETE and an O(1) reversal)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.4 (Circular lists) and Section 2.2.5 (Doubly linked lists), with their exercises
  - url: https://www.linuxjournal.com/article/6828
    title: Prokash Sinha, A memory-efficient doubly linked list, Linux Journal, issue 129 (2005), posted online in 2004
    locator: the whole article (the XOR form of the links, insertion, traversal and deletion in C)
---

An XOR linked list is a [doubly linked list](/doubly-linked-list/) in which each node keeps one link field instead of two: the bitwise exclusive or of the addresses of its predecessor and its successor. A walk that knows the addresses of two neighbouring nodes can recover the next address with one XOR, so the list can be read in both directions and supports the operations of a [deque](/deque/) in $O(1)$ time, with $n$ link words in place of the $2n$ of a doubly linked list. Reversal is free: swapping the head and the tail reverses the list. The price is that a node address alone is not enough to move or to delete, and that the links are no longer [pointers](/pointer/) that a garbage collector or a debugger can follow.

## In plain words

In a normal two-way list, each item stores two addresses: the one before it and the one after it. An XOR list writes down one number that mixes the two addresses together. The mix is the exclusive or of their bits, and it has a useful property: if you know one of the two addresses, you can take it out of the mix and get the other one.

So when you walk along the list, you always carry the address of the item you just left. At the next item you take that address out of its number, and what is left is the address of the item after it. You can walk from either end, because the first and the last item each have only one real neighbour. You save one address per item, but you cannot start a walk in the middle without also knowing a neighbour.

## The abstract type

The XOR linked list implements the [deque](/deque/): `push_front(L, k)`, `push_back(L, k)`, `pop_front(L)`, `pop_back(L)`, `is_empty(L)`, and traversal from the front or from the back. It also supports `reverse(L)` in $O(1)$ time, and `insert_between(L, p, q, k)` for two adjacent nodes $p$ and $q$ whose addresses are known. It does not support "delete the node at address $x$" in $O(1)$ time, which a doubly linked list does, because the node does not give the addresses of its neighbours on its own.

## Representation

Addresses are $w$-bit words, and the address 0 is nil; no node has address 0. Write $\oplus$ for the bitwise exclusive or of two words. Each node $x$ has a key $x.key$ and a link $x.np$. The list has two fields, $L.head$ and $L.tail$.

**Invariant.** Let the nodes in list order be $x_1, \dots, x_n$, and set $x_0 = x_{n+1} = 0$. Then

$$x_i.np = x_{i-1} \oplus x_{i+1} \quad \text{for } 1 \le i \le n,$$

$L.head = x_1$ and $L.tail = x_n$, with $L.head = L.tail = 0$ when $n = 0$.

The proofs use four facts about $\oplus$ on words: it is associative and commutative, $a \oplus 0 = a$, and $a \oplus a = 0$. From these, $(a \oplus b) \oplus a = b$: knowing either neighbour gives the other one. For the end nodes the invariant says $x_1.np = x_2$ and $x_n.np = x_{n-1}$, so a walk can start at either end with the known neighbour 0.

## Operations

The main block holds the front operations and the walk.

```pseudo id=main
PUSH-FRONT(L, k)
L1  x ← ALLOCATE-NODE(); x.key ← k
L2  x.np ← L.head                         ▷ 0 ⊕ L.head
L3  if L.head ≠ 0 then L.head.np ← L.head.np ⊕ x
L4  else L.tail ← x
L5  L.head ← x
POP-FRONT(L)                              ▷ L is not empty
L6  x ← L.head; nxt ← x.np                ▷ x.np = 0 ⊕ second node
L7  if nxt ≠ 0 then nxt.np ← nxt.np ⊕ x
L8  else L.tail ← 0
L9  L.head ← nxt
L10 k ← x.key; FREE(x); return k
TRAVERSE(L)
L11 prev ← 0; cur ← L.head
L12 while cur ≠ 0 do
L13     visit cur.key
L14     nxt ← cur.np ⊕ prev
L15     prev ← cur; cur ← nxt
```

PUSH-FRONT makes the new node $x$ the first node. Its predecessor is 0 and its successor is the old head, so line L2 sets $x.np = 0 \oplus L.head$. The old head had predecessor 0; line L3 replaces that 0 by $x$ inside its link by XOR-ing $x$ in. POP-FRONT reads the second node from the link of the first (line L6) and removes $x$ from the link of the second node (line L7), which leaves 0 there, since the second node becomes the first. TRAVERSE carries the address $prev$ of the node it just left, and line L14 recovers the next address. Each of PUSH-FRONT and POP-FRONT costs $O(1)$; TRAVERSE costs $\Theta(n)$.

The back operations follow from one more operation.

```pseudo id=reverse
REVERSE(L)
R1  swap L.head and L.tail
PUSH-BACK(L, k)
R2  REVERSE(L); PUSH-FRONT(L, k); REVERSE(L)
POP-BACK(L)
R3  REVERSE(L); k ← POP-FRONT(L); REVERSE(L); return k
```

The invariant is symmetric: if $x_1, \dots, x_n$ satisfies it, so does $x_n, \dots, x_1$, because $x_{i-1} \oplus x_{i+1} = x_{i+1} \oplus x_{i-1}$. So swapping the two ends reverses the list without touching a node, in $O(1)$ time. PUSH-BACK and POP-BACK are then the front operations on the reversed list, and each costs $O(1)$.

Insertion in the middle needs the addresses of both neighbours.

```pseudo id=between
INSERT-BETWEEN(L, p, q, k)                ▷ p and q are adjacent, p before q
B1  x ← ALLOCATE-NODE(); x.key ← k
B2  x.np ← p ⊕ q
B3  p.np ← p.np ⊕ q ⊕ x                   ▷ replace the neighbour q of p by x
B4  q.np ← q.np ⊕ p ⊕ x                   ▷ replace the neighbour p of q by x
```

A walk delivers such a pair $(p, q)$ at each step, as $(prev, cur)$. The cost is $O(1)$ once the pair is known. Deletion of $cur$ during a walk is the same idea in reverse: with $nxt = cur.np \oplus prev$, set $prev.np \leftarrow prev.np \oplus cur \oplus nxt$ and $nxt.np \leftarrow nxt.np \oplus cur \oplus prev$, and when $prev$ or $nxt$ is 0, skip that update and set $L.head$ or $L.tail$ instead.

## Example

Nodes get the addresses 1, 2, 3, 4 in the order of allocation, and a freed address is reused first. The column "nodes" lists (address, key, np) from the front.

| operation | head | tail | nodes | result |
|---|---|---|---|---|
| push_front 10 | 1 | 1 | (1, 10, 0) | |
| push_back 20 | 1 | 2 | (1, 10, 2) (2, 20, 1) | |
| push_back 30 | 1 | 3 | (1, 10, 2) (2, 20, 2) (3, 30, 2) | |
| push_front 5 | 4 | 3 | (4, 5, 1) (1, 10, 6) (2, 20, 2) (3, 30, 2) | |
| traverse | | | | 5, 10, 20, 30 |
| pop_front | 1 | 3 | (1, 10, 2) (2, 20, 2) (3, 30, 2) | 5 |
| reverse | 3 | 1 | (3, 30, 2) (2, 20, 2) (1, 10, 2) | |
| pop_front | 2 | 1 | (2, 20, 1) (1, 10, 2) | 30 |
| push_front 7 | 3 | 1 | (3, 7, 2) (2, 20, 2) (1, 10, 2) | |

After push_front 5, node 1 has neighbours 4 and 2, and $4 \oplus 2 = 6$ ($100 \oplus 010 = 110$ in binary). The traversal starts with $prev = 0$ at node 4 and computes $1 \oplus 0 = 1$, then $6 \oplus 4 = 2$, then $2 \oplus 1 = 3$, then $2 \oplus 2 = 0$, and stops. The reverse step changes only the two end fields: the links $(3, 30, 2)$ and $(1, 10, 2)$ already say "my one neighbour is 2". The last push_front reuses the address 3 that the second pop freed.

## Correctness

Each operation keeps the invariant and returns the right key. PUSH-FRONT turns the list $x_1, \dots, x_n$ into $x, x_1, \dots, x_n$: the new node needs $0 \oplus x_1$ (line L2), the old head needs $x \oplus x_2$ instead of $0 \oplus x_2$ (line L3, since $x_2 \oplus x = (0 \oplus x_2) \oplus x$), and no other node has a new neighbour. POP-FRONT is the inverse step. TRAVERSE keeps $prev = x_{i-1}$ and $cur = x_i$ at the test of line L12, because $x_i.np \oplus x_{i-1} = x_{i+1}$; so it visits $x_1, \dots, x_n$ in order and stops after $n$ steps. REVERSE is correct by the symmetry of the invariant, and INSERT-BETWEEN changes exactly the two nodes that get a new neighbour. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time (worst case) | notes |
|---|---|---|
| push_front, push_back | $O(1)$ | plus the cost of the allocator |
| pop_front, pop_back | $O(1)$ | |
| reverse | $O(1)$ | swap two fields |
| insert_between, delete during a walk | $O(1)$ | needs the addresses of two adjacent nodes |
| traverse from either end | $\Theta(n)$ | |
| delete the node at address $x$, given only $x$ | $\Theta(n)$ | walk from an end to find a neighbour |
| space | $n$ keys and $n$ link words, plus 2 words | a doubly linked list needs $2n$ link words |

These bounds are on the [word RAM](/word-ram/) with XOR of two words as one step. The saving is one word per node: for 8-byte keys and 8-byte addresses, a node shrinks from 24 to 16 bytes. Each step of a walk does one XOR more than a doubly linked list, which costs little next to the memory access to the node.

## Variants

- **Sum and difference links.** Store $x_{i-1} + x_{i+1}$ (modulo $2^w$) instead of the XOR. A forward step computes $x_{i+1} = np - x_{i-1}$ and a backward step $x_{i-1} = np - x_{i+1}$; the rest is the same.
- **Index links.** In an array pool, the links can be XORs of indices instead of addresses, which also works in languages without pointer arithmetic. The Python implementation of this page does that.
- **Other memory savings.** An [unrolled linked list](/unrolled-linked-list/) saves link space in another way, by storing many keys per node, and it also improves cache use. A [singly linked list](/singly-linked-list/) uses the same $n$ link words but can only be read in one direction.

## When to use it

Use an XOR list only when memory per node is the main cost, the list is read by walks from its ends, and the program never needs to delete a node given only its address. This happens in small embedded systems and in some low-level code. In most programs a plain doubly linked list is better: it supports deletion of a known node in $O(1)$ time, works with debuggers and garbage collectors, and needs no casts between pointers and integers. When the extra word matters because nodes are small, an unrolled list or an [array](/array/)-based [deque](/deque/) often saves more memory and runs faster.

## Pitfalls

- **Losing the previous address.** A walk that writes line L15 as $cur \leftarrow nxt$ and then $prev \leftarrow cur$ stores the new node in $prev$, and the next XOR gives a wrong address. Update both at once, or save $cur$ in $prev$ first.
- **Forgetting the neighbour at the end.** If line L3 is left out, the old head keeps the link $0 \oplus x_2$, which now reads as "predecessor 0", so a backward walk stops at the old head and never reaches the new node. Each insertion must change the link of each node that gets a new neighbour.
- **Starting in the middle.** Given only the address of a node, its link $x_{i-1} \oplus x_{i+1}$ tells you nothing about either neighbour. An API that returns node handles must return a pair of adjacent addresses, or the caller must walk from an end.
- **Garbage collection.** A [tracing garbage collector](/tracing-garbage-collection/) cannot see a node that is reached only through an XOR value, so it frees nodes that are still in use. XOR lists need manual memory management or an array pool.
- **Pointer to integer conversion.** In C, the XOR must be done on `uintptr_t` values, and the conversions between pointers and integers are implementation-defined. Some tools and checked environments (sanitizers, debuggers, pointer authentication) do not accept pointers rebuilt this way.

## Implementations

## History

The idea of storing a combination of the two neighbour addresses in one field is older than its common name. It appears as Exercise 10.2-8 of the third edition of CLRS, which asks for SEARCH, INSERT, DELETE and an $O(1)$ reversal with one value $x.np$ per item. Prokash Sinha described a C implementation in the Linux Journal in 2004, which made the name "memory-efficient doubly linked list" common.

## References
