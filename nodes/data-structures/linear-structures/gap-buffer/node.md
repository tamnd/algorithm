---
tag: DCWD8D
kind: data-structure
slug: gap-buffer
name: Gap buffer
aliases:
- gap array
area: data-structures/linear-structures
level: advanced
summary: Array with an empty gap at the edit point, making local insertions and deletions cheap.
implements: [list]
prereqs: [array, dynamic-array]
see_also: [piece-table, rope, zipper, dynamic-array, circular-buffer, doubly-linked-list, dynamic-array-resizing, list]
sources:
  - url: https://www.gnu.org/software/emacs/manual/html_node/elisp/Buffer-Gap.html
    title: GNU Emacs Lisp Reference Manual, The Buffer Gap
    locator: the whole node, on how Emacs keeps the text of a buffer as two runs of characters around a gap
  - paper: "Craig A. Finseth, The Craft of Text Editing: Emacs for the Modern World, Springer-Verlag (1991)"
    locator: Chapter 6 (The Internal Sub-Editor), the section on the buffer gap method and its comparison with linked lines
  - paper: "Charles Crowley, Data structures for text sequences, Computer Science Department, University of New Mexico (1998)"
    locator: the section on the gap method and the comparison with the piece table and with linked lists of lines
---

A gap buffer stores a sequence, usually the text of an editor, in one [array](/array/) with a run of free cells, the *gap*, at the cursor. The items before the cursor sit at the start of the array and the items after it sit at the end, so an insert at the cursor writes into the gap and a delete at the cursor widens it, both in $O(1)$ time. Moving the cursor by $d$ positions moves $d$ items across the gap, in $O(d)$ time, and reading position $i$ costs $O(1)$. When the gap is used up, the array doubles as a [dynamic array](/dynamic-array/) does, so each insert costs $O(1)$ amortized. Because editing tends to happen near the last edit, the total cost is close to the number of keystrokes, and the structure is how GNU Emacs stores its buffers.

## In plain words

Picture a line of text written on cards in a long box, with some empty cards in the middle where your cursor is. To type a letter, you write it on the first empty card. To delete the letter before the cursor, you wipe that card, and it joins the empty ones. Neither needs any other card to move.

To edit somewhere else, you move the empty cards there: you carry the cards between the old and the new place across the gap, one by one. That is slow for a long jump, but most edits happen close to the last one. When you run out of empty cards, you get a box twice as big and copy everything once.

## The abstract type

The structure implements the [list](/list/) type with a *cursor*: a position $c$ with $0 \le c \le n$, between two items or at an end. Its fast operations work at the cursor: `insert(x)` puts $x$ before the cursor and moves the cursor past it, `delete_before` (backspace) and `delete_after` (the delete key) remove one item next to the cursor, and `move_to(p)` sets the cursor. `get(i)` reads any position. A general `insert(i, x)` is `move_to(i)` followed by `insert(x)`.

## Representation

An array $A[0..cap-1]$ and two indices $g \le e$. The gap is the run of cells $A[g..e-1]$, whose contents do not matter.

**Invariant.** $0 \le g \le e \le cap$, $cap \ge 1$, and the sequence held is

$$\langle A[0], \ldots, A[g-1], A[e], \ldots, A[cap-1] \rangle,$$

of length $n = cap - (e - g)$. The cursor is at position $g$.

So item $i$ is at cell $i$ when $i < g$, and at cell $i + (e - g)$ when $i \ge g$. The gap is empty when $g = e$, which means the array is full.

## Operations

```pseudo id=main
MOVE-TO(B, p)                              ▷ 0 ≤ p ≤ n
L1  while g > p: e ← e − 1, g ← g − 1, A[e] ← A[g]
L2  while g < p: A[g] ← A[e], g ← g + 1, e ← e + 1
INSERT(B, x)                               ▷ before the cursor
L3  if g = e then GROW(B)
L4  A[g] ← x, g ← g + 1
DELETE-BEFORE(B)                           ▷ g > 0
L5  g ← g − 1, return A[g]
DELETE-AFTER(B)                            ▷ e < cap
L6  e ← e + 1, return A[e − 1]
GET(B, i)                                  ▷ 0 ≤ i < n
L7  if i < g then return A[i] else return A[i + (e − g)]
GROW(B)
L8  C ← an array of size 2·cap; copy A[0..g−1] to the start of C and A[e..cap−1] to its end; e ← e + cap, A ← C, cap ← 2·cap
```

Line L1 moves the gap left: the item just before the gap goes to the cell just before the gap's end. Line L2 moves it right. In both, each pass moves one item and keeps the gap the same width. INSERT writes into the first gap cell. The two deletes only move an end of the gap. GROW keeps both runs and the cursor, and makes the gap $cap$ cells wider.

## Example

Start with $cap = 4$. The column $A$ shows the cells, with $\_$ for a gap cell.

| operation | $A$ | $g$ | $e$ | text | result |
|---|---|---|---|---|---|
| insert(c) | c \_ \_ \_ | 1 | 4 | c | |
| insert(a) | c a \_ \_ | 2 | 4 | ca | |
| insert(t) | c a t \_ | 3 | 4 | cat | |
| move_to(1) | c \_ a t | 1 | 2 | cat | 2 moves |
| insert(h) | c h a t | 2 | 2 | chat | |
| move_to(4) | c h a t | 4 | 4 | chat | 2 moves |
| insert(s) | c h a t s \_ \_ \_ | 5 | 8 | chats | grow to 8 |
| insert(!) | c h a t s ! \_ \_ | 6 | 8 | chats! | |
| move_to(0) | \_ \_ c h a t s ! | 0 | 2 | chats! | 6 moves |
| delete_after | \_ \_ \_ h a t s ! | 0 | 3 | hats! | c |

After insert(h) the gap is empty, so the next move_to only shifts the indices: with $g = e$, the two loops move items onto themselves. The insert(s) finds $g = e = 4$ and grows: the run before the gap, "chat", stays at the start, the empty run after it stays at the end, and the new gap is cells 4 to 7. Then get(0) reads $A[0 + 3] = $ h.

## Correctness

Each pass of line L1 takes the last item before the gap, $A[g-1]$, and copies it to $A[e-1]$, the last gap cell; then both indices drop by one. The item stays in the same place in the sequence, now as the first item after the gap. Line L2 is the mirror case. INSERT writes into a gap cell, so no item is lost, and the new item becomes the last item before the gap. DELETE-BEFORE and DELETE-AFTER turn one item cell into a gap cell. GROW copies both runs to the ends of the new array. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| insert at the cursor | $O(1)$ amortized, $\Theta(n)$ worst case for a grow |
| delete before or after the cursor | $O(1)$ worst case |
| move_to$(p)$ | $\Theta(\lvert p - g \rvert + 1)$ |
| get$(i)$ | $O(1)$ |
| insert or delete at position $i$ | $\Theta(\lvert i - g \rvert + 1)$ amortized |
| space | $cap$ cells; $cap \le \max(cap_0, 2 n_{\max})$ |

**A run of edits.** A sequence of $m$ operations that moves the cursor a total distance $D$ costs $O(m + D)$ time. The grows cost $O(m)$ in total by the [potential method](/potential-method/) argument for doubling: a grow at capacity $cap$ copies $cap$ items, and at least $cap/2$ inserts happened since the last grow. So when an editor works locally, the cost is close to the number of keystrokes. A jump across the whole text costs $\Theta(n)$, which for a text of a few megabytes is a copy of a few megabytes, fast on a modern machine.

## Variants

- **Shrinking.** Halve the array when the gap is more than three quarters of it, as in [dynamic array resizing](/dynamic-array-resizing/). Editors rarely do this.
- **Lazy gap moves.** Move the gap only when an edit happens, not when the cursor moves. Reads use line L7 wherever the gap is. This is what Emacs does: the point and the gap are separate.
- **Two stacks.** The run before the gap is a stack with its top at $g - 1$, and the run after the gap is a stack with its top at $e$. Moving the cursor pops from one and pushes on the other. In a functional language, the same idea with two lists is the list [zipper](/zipper/).
- **Gap per line, or per block.** Split the text into blocks, each with its own gap, so that a jump costs at most the size of a block.
- **[Piece table](/piece-table/).** Keep the original text read-only and record edits as pieces of an append-only buffer. It makes undo and very large files cheap, at the cost of slower reads.
- **[Rope](/rope/).** A balanced tree of strings, with $O(\log n)$ for every edit anywhere, used when edits are not local or the text is very large.

## When to use it

Use a gap buffer for a sequence that is edited mostly near one moving point: the text of an editor, a line being typed in a terminal, a command line with history. It has the speed of an array for reads and for local edits, needs no pointers, and keeps the text in at most two runs, so searching and saving the text are fast. For many cursors far apart, as in an editor with multiple cursors, for undo of long histories, or for files of gigabytes, a [piece table](/piece-table/) or a [rope](/rope/) is better.

## Pitfalls

- **Order of the writes in line L1.** The indices must drop before the copy, so that $A[e-1] \leftarrow A[g-1]$ is the copy made. Copying first with the old indices writes into the cell just past the gap, which holds an item.
- **Overlap when moving by a block copy.** Fast implementations move the gap with one block copy instead of a loop. The source and the target can overlap, so use a copy that allows overlap, such as `memmove` and not `memcpy`.
- **Growing by a raw copy.** Copying $A$ to the start of the larger array puts the run after the gap in the middle, with the new free cells after it. The second run must go to the end of the new array, and $e$ must move with it.
- **Positions after the gap.** Code that reads $A[i]$ directly is wrong for $i \ge g$. Every read by position must go through line L7.
- **Variable-width characters.** In UTF-8, one character may take several bytes. Positions in characters and offsets in bytes differ, and a move must not split a character.

## Implementations

## History

The gap buffer is old in text editors; Finseth's 1991 book describes the method, which he calls the buffer gap, and compares it with keeping the text as a linked list of lines. GNU Emacs keeps the text of each buffer as two runs of characters around a gap, as its Lisp manual describes. Crowley's 1998 survey of data structures for text sequences compares the gap method with the piece table and with linked lines.

## References
