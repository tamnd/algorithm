---
tag: YWD1E5
kind: data-structure
slug: unrolled-linked-list
name: Unrolled linked list
aliases:
- unrolled list
area: data-structures/linear-structures
level: advanced
summary: Linked list whose nodes each hold a small array of elements for cache locality.
implements: [list]
prereqs: [singly-linked-list, array, asymptotic-notation]
see_also: [singly-linked-list, linked-list, dynamic-array, locality-of-reference, external-memory-model, b-tree, rope, skip-list]
sources:
  - url: https://opendatastructures.org/
    title: Pat Morin, Open Data Structures
    locator: Chapter 3 (Linked Lists), Section 3.3 (SEList, a space-efficient linked list with blocks of b - 1 to b + 1 items)
  - paper: doi:10.1145/182409.182453
    title: Zhong Shao, John H. Reppy and Andrew W. Appel, Unrolling lists, Proceedings of the 1994 ACM Conference on LISP and Functional Programming
    locator: pp. 185 to 195
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2 (Linked lists) and Chapter 18 (B-trees, the same idea of many keys in one node)
---

An unrolled linked list is a [singly linked list](/singly-linked-list/) in which each node holds a small [array](/array/) of up to $b$ items instead of one item. It stores a sequence and supports the operations of the [list](/list/) type (get, set, insert and delete at a position) with a walk over at most about $2n/b$ nodes plus the shift of one array of size $b$, so each operation costs $O(n/b + b)$ time, and $O(\sqrt n)$ when $b = \Theta(\sqrt n)$. Because neighbouring items sit next to each other in memory, a scan reads each cache block about once, which gives much better [locality of reference](/locality-of-reference/) than a list with one item per node, and the space for links drops from $n$ pointers to about $2n/b$.

## In plain words

A normal linked list is like a chain of small boxes, each with one item and a note saying where the next box is. Walking the chain means jumping all over memory, one item per jump.

An unrolled list uses bigger boxes. Each box has room for a fixed number of items, say sixteen, kept in order, and one note to the next box. To find the item at some position, you skip whole boxes by their item counts, then look inside one box. To insert into a full box, you split it into two half-full boxes. When a box becomes less than half full after a deletion, you move one item over from a neighbour, or you join the two boxes into one. So boxes stay at least half full, the chain stays short, and most of the work happens inside one compact box.

## The abstract type

The structure implements the [list](/list/) type, a sequence $s = (s_0, \dots, s_{n-1})$ with these operations:

- `get(L, i)` returns $s_i$, and `set(L, i, x)` replaces it, for $0 \le i < n$;
- `insert(L, i, x)` makes $x$ the item at position $i$ and moves $s_i, \dots, s_{n-1}$ one position up, for $0 \le i \le n$;
- `delete(L, i)` removes and returns $s_i$, for $0 \le i < n$;
- `size(L)` and a traversal in order.

## Representation

Fix the capacity $b \ge 2$ and let $h = \lfloor b/2 \rfloor$. Each node $v$ has an array $v.a$ of $b$ slots, a count $v.count$, and a pointer $v.next$. The list has a pointer $L.head$ (nil when the list is empty) and the size $n$.

**Invariant.** Let the nodes in order be $v_1, \dots, v_k$.

- (U1) The sequence $v_1.a[0 \ldots v_1.count - 1]$, then $v_2.a[0 \ldots v_2.count - 1]$, and so on up to $v_k$, is $s$.
- (U2) $1 \le v_t.count \le b$ for each node.
- (U3) If $k \ge 2$, then $v_t.count \ge h$ for each node.

So an empty list has no node, and only a list with one node may have a node that is less than half full. By (U3), if $k \ge 2$ then $n \ge k h$, so $k \le n / \lfloor b/2 \rfloor$, which is $2n/b$ for even $b$. In all cases $k \le \max(1, n/h)$.

## Operations

All positions are 0-based. FIND walks the nodes and returns the node $v$ that holds position $i$, its offset $j$, and its predecessor $p$.

```pseudo id=main
FIND(L, i)                                ▷ L.head ≠ nil, 0 ≤ i ≤ n
L1  p ← nil; v ← L.head
L2  while v.next ≠ nil and i ≥ v.count do
L3      i ← i − v.count; p ← v; v ← v.next
L4  return (p, v, i)
GET(L, i)                                 ▷ 0 ≤ i < n
L5  (p, v, j) ← FIND(L, i); return v.a[j]
INSERT(L, i, x)                           ▷ 0 ≤ i ≤ n
L6  if L.head = nil then L.head ← a new node holding only x; return
L7  (p, v, j) ← FIND(L, i)
L8  if v.count = b then                    ▷ full: split v
L9      w ← new node; move v.a[b − h .. b − 1] to w; w.next ← v.next; v.next ← w
L10     if j > b − h then v ← w; j ← j − (b − h)
L11 shift v.a[j .. v.count − 1] up one slot; v.a[j] ← x; v.count ← v.count + 1
DELETE(L, i)                              ▷ 0 ≤ i < n
L12 (p, v, j) ← FIND(L, i)
L13 x ← v.a[j]; shift v.a[j + 1 .. v.count − 1] down one slot; v.count ← v.count − 1
L14 if v.count ≥ h or (p = nil and v.next = nil) then
        if v.count = 0 then L.head ← nil
        return x
L15 if v.next ≠ nil then (u, r) ← (v, v.next) else (u, r) ← (p, v)
L16 if u.count + r.count ≤ b then append r's items to u; u.next ← r.next; free r
L17 else if u = v then move the first item of r to the end of u
        else move the last item of u to the front of r
L18 return x
```

**FIND.** The loop skips a node when position $i$ is past it. For $i < n$ it stops at the node that holds $s_i$; for $i = n$ it stops at the last node with $j = v.count$, the slot after its last item. It visits at most $k$ nodes, so it costs $O(k) = O(1 + n/b)$. GET and SET cost the same.

**INSERT.** If $v$ has a free slot, line L11 shifts at most $b - 1$ items, in $O(b)$ time. If $v$ is full, line L9 splits it: $v$ keeps its first $b - h = \lceil b/2 \rceil$ items and the new node $w$ gets the last $h$. Line L10 picks the node where position $j$ now is, and line L11 inserts there. The cost is $O(n/b + b)$.

**DELETE.** Line L13 removes the item in $O(b)$ time. If $v$ still has at least $h$ items, or it is the only node, the invariant holds (an empty only node is removed). Else $v$ has $h - 1$ items, and lines L15 to L17 fix it with an adjacent node: the pair $(u, r)$ is $v$ and its successor, or the predecessor and $v$ when $v$ is the last node. If the two fit in one node, line L16 merges them; else line L17 moves one item into $v$ from the neighbour. The cost is $O(n/b + b)$.

## Example

Take $b = 4$, so $h = 2$. The column "nodes" shows the arrays of the nodes in order.

| operation | result | nodes |
|---|---|---|
| append 10, 20, 30, 40 | | [10 20 30 40] |
| insert(1, 15) | | [10 15 20] [30 40] |
| insert(5, 50) | | [10 15 20] [30 40 50] |
| insert(6, 60) | | [10 15 20] [30 40 50 60] |
| get(3), get(5) | 30, 50 | |
| delete(0) | 10 | [15 20] [30 40 50 60] |
| delete(0) | 15 | [20 30] [40 50 60] |
| delete(3) | 50 | [20 30] [40 60] |
| delete(2) | 40 | [20 30 60] |

The insert of 15 goes to a full node, so line L9 splits [10 20 30 40] into [10 20] and [30 40], and line L11 puts 15 at offset 1 of the first part. The insert at position 5 is at the end: FIND skips the first node (5 ≥ 3), stops at the last node with $j = 2$, and appends. For get(5), FIND skips 3 items and returns offset 2 of the second node. The second delete(0) leaves [20], one item below $h$; the two nodes hold $1 + 4 = 5 > 4$ items, so line L17 moves 30 over. The last delete leaves [60] in the last node; with its predecessor [20 30] it fits in one node, so line L16 merges them.

## Correctness

Each operation keeps (U1), (U2) and (U3) and returns the item at the right position. FIND keeps the loop invariant "position $i$ of the original call is offset $i$ in the part of the sequence that starts at $v$", so GET reads the right item. INSERT puts $x$ at the right place in the order of (U1); a split makes two nodes of $\lceil b/2 \rceil \ge h$ and $h$ items, one of which then grows by 1 to at most $b$. In DELETE, a node that falls to $h - 1$ items has a neighbour with at least $h$ items; if their total is at most $b$ they merge into one node of at least $2h - 1 \ge h$ items, and if not, the neighbour has at least $b - h + 2 \ge h + 1$ items and can give one away. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $k \le \max(1, n/\lfloor b/2 \rfloor)$ be the number of nodes.

| operation | time (worst case) | notes |
|---|---|---|
| get, set | $O(k) = O(1 + n/b)$ | FIND, then one array access |
| insert | $O(n/b + b)$ | FIND, then a shift or a split of one array |
| delete | $O(n/b + b)$ | FIND, then a shift and a merge or a move |
| traverse | $O(n + k)$ | one pass over the arrays |
| space | $k$ arrays of $b$ slots and $k$ pointers | at most $2n + b$ slots for even $b$ |

The time bounds are on the [word RAM](/word-ram/). With $b = \Theta(\sqrt n)$, each operation costs $O(\sqrt n)$; the program must then rebuild with a new $b$ when $n$ changes by a constant factor, or pick $b$ from the expected size. With a constant $b$, the cost is $\Theta(n/b)$, a constant factor faster than a plain linked list, and the gain comes mostly from the memory system. In the [external-memory model](/external-memory-model/) with blocks of $B$ items, a node with $b = \Theta(B)$ fills $O(1)$ blocks, so a traversal costs $O(n/B + 1)$ block transfers in place of up to $n$ for one item per node, and FIND costs $O(n/B + 1)$ transfers.

## Variants

- **Doubly linked blocks with a slack rule.** Morin's SEList keeps a doubly linked list of blocks, each with $b - 1$ to $b + 1$ items except the last, and uses each block as a small deque. It reaches position $i$ from the nearer end, so get and set take $O(1 + \min(i, n - i)/b)$ time and insertion and deletion take $O(b + \min(i, n - i)/b)$ amortized time, with $n + O(b + n/b)$ space.
- **Unrolled lists in functional languages.** Shao, Reppy and Appel store several consecutive cons cells of an immutable list in one record, to reduce the space and the time of list programs.
- **Tree of blocks.** A [B-tree](/b-tree/) or a [rope](/rope/) indexes the blocks by their item counts, which lets FIND take $O(\log(n/b))$ steps instead of $O(n/b)$.
- **Other structures with chunks.** A [skip list](/skip-list/) adds express lanes over a linked list instead, and a [gap buffer](/gap-buffer/) keeps one array with a hole at the edit point.

## When to use it

Use an unrolled list when a sequence has many insertions and deletions in the middle and is also read by scans, and when a [dynamic array](/dynamic-array/) would shift too much data and a plain linked list would waste memory and cache. Text editors, the lists of an interpreter, and queues of small records are typical uses. If the program needs fast access by position for large $n$, a balanced tree of blocks such as a rope is better. If inserts happen only at the ends, a dynamic array or a deque is simpler and faster.

## Pitfalls

- **Splitting without inserting into the right half.** After line L9, an insert with $j > b - h$ must go to $w$ at offset $j - (b - h)$. Inserting into $v$ instead (at its end, since $v$ now has only $b - h$ items) puts $x$ before all the items that moved to $w$, though it belongs after some of them, so the order of (U1) breaks. Line L10 fixes the target. The example insert into a full node near its end catches this.
- **No lower bound on the node size.** A version that only splits and never merges keeps every insert correct, but a run of deletions can leave $n$ nodes of one item each, and then every operation costs $\Theta(n)$ like a plain list. Keep (U3) with lines L14 to L17.
- **Merging into an overfull node.** Merging without the test of line L16 can give a node of up to $b + h - 1$ items, which breaks (U2). Merge only when the two counts add up to at most $b$; else move one item.
- **Off by one at the end.** FIND must allow $i = n$ for INSERT and stop at the last node; a loop that also tests $i < v.count$ for the last node runs past the end. The test `v.next ≠ nil` in line L2 stops at the last node.
- **Empty nodes.** A node with zero items left in a list of two or more nodes breaks (U2) and makes FIND return an offset into an empty array. Line L14 only keeps an empty node when it is the only one, and then removes it.

## Implementations

## History

Putting several items of a list in one node is the same idea as the many keys per node of a B-tree. Shao, Reppy and Appel studied unrolled lists for the compilation of functional languages in a paper of 1994. Morin's Open Data Structures presents the imperative form as the SEList.

## References
