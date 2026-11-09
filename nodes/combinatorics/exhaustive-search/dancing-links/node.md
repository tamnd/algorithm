---
tag: 48VR35
kind: data-structure
slug: dancing-links
name: Dancing links
aliases:
- DLX
- toroidal doubly linked list
area: combinatorics/exhaustive-search
level: advanced
summary: Doubly linked lists whose node removal and restoration make Algorithm X fast.
model: word-ram
complexity:
  vars: {n: the number of items, s: the total size of all options}
  time: {worst: O(n + s)}
  space: {extra: O(n + s)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2000
  people: [Donald E. Knuth, Hiroshi Hitotsumatsu, Kohei Noshita]
  note: Hitotsumatsu and Noshita used the undo of a list deletion in a backtrack program for the n-queens problem in 1979. Knuth named the method dancing links and built Algorithm X on it in 2000.
prereqs: [doubly-linked-list, exact-cover, generic-backtracking-algorithm]
see_also: [algorithm-x, exact-cover, doubly-linked-list, generic-backtracking-algorithm, n-queens-problem, sudoku, polyomino-tiling-problem, linked-list]
sources:
  - paper: "Donald E. Knuth, Dancing links, in Millennial Perspectives in Computer Science, Palgrave, 2000, 187 to 214, arXiv:cs/0011047"
    locator: Section 1 (the undo of a deletion from a doubly linked list) and Section 2 (the column and row lists of an exact cover matrix, cover and uncover)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2.1, Dancing links (the node layout with spacers, and the operations hide, cover, unhide and uncover)
  - paper: "Hiroshi Hitotsumatsu and Kohei Noshita, A technique for implementing backtrack algorithms and its application, Information Processing Letters 8(4), 1979, 174 to 175"
    locator: the restore of a deleted node in a backtrack program for the n-queens problem
---

Dancing links is Knuth's name for a set of circular [doubly linked lists](/doubly-linked-list/) that hold an [exact cover](/exact-cover/) problem as a sparse 0/1 matrix, with one list for each item and one node for each one of the matrix. Its trick is that a node removed from a doubly linked list still holds the links to its old neighbors, so it can be put back in $O(1)$ time, as long as the removals are undone in the reverse order. A [backtracking](/generic-backtracking-algorithm/) search such as [Algorithm X](/algorithm-x/) removes and restores nodes all the time, so this makes each step cheap and needs no copy of the state. The structure supports two operations, COVER and UNCOVER, each in time proportional to the number of nodes it moves.

## In plain words

Think of a line of people, where each person holds the hand of the one on the left and the one on the right. To take a person out, the two neighbors let go of that person and hold each other's hands. The person who left still remembers who the neighbors were.

To put the person back, tell the two old neighbors to hold that person's hands again. This works if nothing else has changed in between, or if every later change was undone first.

A search that tries a choice, explores it and then undoes it takes people out and puts them back in exactly reverse order. So each change and each undo is a few quick steps, and the search never has to copy the whole table.

## The abstract type

The structure stores an exact cover problem: a list of primary items, a list of secondary items, and a list of options, each a set of items. At each moment some items are *active* and some options are *active*. The operations are:

- COVER$(i)$, for an active item $i$: make $i$ inactive and make each active option that contains $i$ inactive. The list of options of $i$ itself keeps its contents, so that a search can still walk it.
- UNCOVER$(i)$: undo the last COVER$(i)$. The calls must be in last-in first-out order: UNCOVER$(i)$ is called only when the last COVER that is not yet undone is COVER$(i)$.
- Queries: the active primary items, in order; for an item $i$, the active options that contain it, and their number $\mathrm{LEN}[i]$.

## Representation

Number the items $1, \ldots, n$, primary items first. The structure has the following nodes, in this order in arrays:

- Node $0$ is the root. The headers of the primary items form a circular list through the root with links LLINK and RLINK. Each secondary header links to itself, so it is never in the root list.
- Nodes $1$ to $n$ are the item headers. The header of item $i$ is also the head of a circular *column* list with links ULINK and DLINK, which holds one node for each active option that contains $i$. LEN$[i]$ is the length of this list.
- Then come the options, one node for each item of each option, in order. Each such node $x$ has TOP$[x]$, the item of its column, and ULINK and DLINK in that column.
- A *spacer* node comes before the first option, between two options, and after the last one. Its TOP is zero or negative. Its ULINK points to the first node of the option before it, and its DLINK to the last node of the option after it. So the nodes of an option are consecutive, and a walk along them can wrap around through a spacer.

With the six options of Knuth's example (see [Algorithm X](/algorithm-x/)), the headers are nodes $1$ to $7$ for $A$ to $G$, node $8$ is a spacer, the option C E F is nodes $9$ to $11$, node $12$ is a spacer, A D G is nodes $13$ to $15$, and so on up to the last spacer, node $30$. The space is $n + 1$ headers, $s$ option nodes and $m + 1$ spacers, where $m \le s$ is the number of options, so it is $O(n + s)$.

## Operations

```pseudo id=main
HIDE(p)                                   ▷ remove the other nodes of the option of p from their columns
L1  q ← p + 1
L2  while q ≠ p do
L3      x ← TOP[q], u ← ULINK[q], d ← DLINK[q]
L4      if x ≤ 0 then q ← u                ▷ a spacer: go to the first node of the option
L5      else DLINK[u] ← d, ULINK[d] ← u, LEN[x] ← LEN[x] − 1
L6           q ← q + 1
COVER(i)
L7  p ← DLINK[i]
L8  while p ≠ i do
L9      HIDE(p)
L10     p ← DLINK[p]
L11 l ← LLINK[i], r ← RLINK[i]
L12 RLINK[l] ← r, LLINK[r] ← l
UNHIDE(p)                                 ▷ undo HIDE(p), walking the option backward
L13 q ← p − 1
L14 while q ≠ p do
L15     x ← TOP[q], u ← ULINK[q], d ← DLINK[q]
L16     if x ≤ 0 then q ← d                ▷ a spacer: go to the last node of the option
L17     else DLINK[u] ← q, ULINK[d] ← q, LEN[x] ← LEN[x] + 1
L18          q ← q − 1
UNCOVER(i)                                ▷ undo COVER(i), walking the column upward
L19 l ← LLINK[i], r ← RLINK[i]
L20 RLINK[l] ← i, LLINK[r] ← i
L21 p ← ULINK[i]
L22 while p ≠ i do
L23     UNHIDE(p)
L24     p ← ULINK[p]
```

Line L5 is the deletion of node $q$ from its column, and line L17 is its undo. They are the "dancing" steps: line L5 does not change ULINK$[q]$ and DLINK$[q]$, so line L17 finds the old neighbors there. Line L12 deletes the header $i$ from the root list in the same way, and line L20 puts it back. HIDE$(p)$ leaves node $p$ in its own column, so the walk of lines L7 to L10 down the column of $i$ is not disturbed. Every undo walks in the opposite direction of the matching removal: UNCOVER goes up the column, and UNHIDE goes backward along the option.

## Example

Cover item $A$ in Knuth's example. Column $A$ holds nodes $13$ (option A D G) and $21$ (option A D).

1. HIDE$(13)$: node $14$ leaves column $D$ and node $15$ leaves column $G$. Then $q = 16$ is a spacer with ULINK $13$, so the walk returns to $p$ and stops.
2. HIDE$(21)$: node $22$ leaves column $D$. Node $23$ is a spacer with ULINK $21$, so the walk stops.
3. Lines L11 and L12 delete header $1$ from the root list: RLINK$[0] = 2$ and LLINK$[2] = 0$.

| | before | after COVER$(A)$ |
|---|---|---|
| active primary items | A B C D E F G | B C D E F G |
| column D | 14, 22, 27 | 27 |
| column G | 15, 25, 29 | 25, 29 |
| LEN of A to G | 2 2 2 3 2 2 3 | 2 2 2 1 2 2 2 |

Column $A$ still holds $13$ and $21$, so Algorithm X can walk it to try both options. UNCOVER$(A)$ puts header $1$ back first, then walks column $A$ upward: UNHIDE$(21)$ puts back node $22$, and UNHIDE$(13)$ puts back node $15$ and then node $14$. The links and lengths are then exactly as before.

## Correctness

The basic fact is about one list. Delete $x$ from a circular doubly linked list by RLINK$[\mathrm{LLINK}[x]] \gets \mathrm{RLINK}[x]$ and LLINK$[\mathrm{RLINK}[x]] \gets \mathrm{LLINK}[x]$. This does not change the links of $x$. If the links are exactly as right after the deletion, then RLINK$[\mathrm{LLINK}[x]] \gets x$ and LLINK$[\mathrm{RLINK}[x]] \gets x$ give back exactly the links before it. By induction, deletions $x_1, \ldots, x_k$ followed by the undos of $x_k, \ldots, x_1$ give back the start state.

COVER$(i)$ is a sequence of such deletions, and UNCOVER$(i)$ performs their undos in the reverse order: it walks column $i$ upward instead of downward, and UNHIDE walks each option backward instead of forward. Column $i$ and the spacers do not change during the two calls, so both walks see the same nodes. With last-in first-out calls, the whole structure returns to its state before each COVER. An invariant on the active options shows that COVER$(i)$ has the effect of the abstract type. The full proof is below.

## Complexity

HIDE$(p)$ takes time proportional to the size of the option of $p$, plus one step for a spacer. So COVER$(i)$ and UNCOVER$(i)$ take $O(1 + t)$ time, where $t$ is the total size of the active options that contain $i$; this is at most $O(s)$. The build takes $O(n + s)$ time, and an item lookup by its node number is $O(1)$. A scan of the active primary items for the one with the least LEN takes time linear in their number, which is at most $n$. The space is $O(n + s)$ words, with no other memory during the search: the undo information is in the removed nodes themselves.

## Variants

- **Colors.** In Section 7.2.2.1 of *The Art of Computer Programming*, an option node of a secondary item can carry a color. An option that sets the color *purifies* the column: it hides only the options with another color.
- **Multiplicities.** An item may be covered between $u$ and $v$ times; the list operations are the same, with a counter per item.
- **Other searches.** The same undo of a deletion helps any backtracking program that keeps a set of candidates in a doubly linked list, for example the free columns of the [n-queens problem](/n-queens-problem/) in the program of Hitotsumatsu and Noshita.
- **Arrays of sets.** A simpler but slower representation stores, for each item, a set of options, and removes and adds options with set operations. It has the same behavior but costs hashing at each step.

## When to use it

Use dancing links when a depth-first search over a sparse matrix removes many rows and columns at each step and restores them when it backs up, as in exact cover, [Sudoku](/sudoku/) and [polyomino tilings](/polyomino-tiling-problem/). If the matrix is dense and small, bit vectors per item can be faster. If the search needs to jump between unrelated states, as in best-first search, the last-in first-out rule fails, and a copy of the state or a persistent structure is needed instead.

## Pitfalls

- **Undo in the wrong order.** If UNCOVER$(i)$ and UNCOVER$(j)$ are swapped, the links of a node can point to a node that is still out of the list, and the structure is broken without any error.
- **Forward and backward walks.** UNHIDE must walk the option backward and UNCOVER must walk the column upward. Walking in the same direction as the removal restores the nodes in the wrong order.
- **Removing the node that the loop stands on.** HIDE$(p)$ skips $p$, so the loop of COVER can still use DLINK$[p]$. A version that also removes $p$ from its column would break the walk.
- **Secondary items in the root list.** Secondary headers must not be in the root list, or the search would try to cover them.
- **Repeated items in an option.** An option that names an item twice gives two nodes in one column, and HIDE would remove a node of the column that COVER is walking. Reject such input.

## Implementations

## History

Hitotsumatsu and Noshita (1979) used the undo of a deletion from a doubly linked list in a fast backtrack program for the n-queens problem. Knuth gave the method the name *dancing links* in his paper of 2000 (arXiv cs/0011047). The same paper introduced the column and row lists for exact cover, the operations cover and uncover, and the program DLX for [Algorithm X](/algorithm-x/). Section 7.2.2.1 of Volume 4B of *The Art of Computer Programming* (2022) uses the array layout with spacer nodes that this page follows.

## References
