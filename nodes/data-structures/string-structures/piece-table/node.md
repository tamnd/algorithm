---
tag: A8HMV8
kind: data-structure
slug: piece-table
name: Piece table
area: data-structures/string-structures
level: core
summary: Text-editing structure that stores edits as a list of pieces referencing an original and an add buffer.
implements: [list]
model: word-ram
complexity:
  vars: {P: the number of pieces, n: the length of the text}
  time: {worst: O(P)}
  space: {extra: Θ(P)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [array, dynamic-array, list]
see_also: [gap-buffer, rope, dynamic-array, persistent-data-structure, red-black-tree, order-statistic-tree, list, linked-list]
sources:
  - paper: "Charles Crowley, Data structures for text sequences, Computer Science Department, University of New Mexico (1998)"
    locator: the section on the piece table method, its operations and its comparison with the gap method and with linked lines
  - url: https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation
    title: Peng Lyu, Text Buffer Reimplementation, Visual Studio Code blog (March 2018)
    locator: the sections on the piece table and on the piece tree, a piece table kept in a red-black tree with line break counts
---

A piece table stores a text that is being edited as a sequence of *pieces*, each one a reference (buffer, start, length) into one of two buffers: the *original buffer*, which holds the text as it was loaded and is never changed, and the *add buffer*, to which every inserted character is appended. The text is the concatenation of the pieces in order. An insert appends the new characters to the add buffer and splits at most one piece to make room for a piece that refers to them. A delete only shrinks, splits or removes pieces. No character is ever moved or overwritten, so the cost of an edit depends on the number of pieces, not on the length of the text, and the old states of the text stay cheap to keep for undo.

## In plain words

Think of the file as a printed book that you are not allowed to write in, plus a notebook where you write everything you add. To describe the current text, you keep a short list of instructions: "read page 1 of the book up to line 4, then read the first six words of the notebook, then go back to the book at line 4". To type, you write the new words at the end of the notebook and add one instruction. To delete, you change the instructions so that they skip the deleted part.

The book and the notebook are never erased. So an edit never copies the text, and an old list of instructions still describes the old text exactly, which makes undo simple.

## The abstract type

The piece table implements the [list](/list/) of characters: read the character at position $i$, read a range, insert a string at position $i$, delete $d$ characters starting at position $i$, and report the length. Editors add operations on lines, which a piece table supports by keeping the number of line breaks in each piece.

## Representation

- $T.orig$ is the original buffer, a string of length $n_0$, never changed.
- $T.add$ is the add buffer, an append-only array of characters.
- $T.pieces$ is a list $p_0, p_1, \ldots, p_{P-1}$ of triples $(b, s, \ell)$ with $b \in \{orig, add\}$. The piece names the string $buf_b[s .. s + \ell - 1]$.
- $T.n$ is the length of the text.

**Invariant.**

- **(P1) Pieces are in range.** Each piece has $\ell \ge 1$ and $0 \le s$ and $s + \ell \le \lvert buf_b \rvert$.
- **(P2) The text.** The text is $text(T) = str(p_0) \cdot str(p_1) \cdots str(p_{P-1})$, and $T.n = \sum \ell$.
- **(P3) Buffers.** $T.orig$ never changes, and $T.add$ only grows at its end, so the string named by a piece never changes after the piece is made.

## Operations

```pseudo id=main
FIND(T, i)                        ▷ the piece and offset of position i
L1  off ← i
L2  for k ← 0 to P − 1:
L3      if off < ℓ(p_k) then return (k, off)
L4      off ← off − ℓ(p_k)
L5  return (P, 0)                 ▷ i = n: just after the last piece

INSERT(T, i, x)
L6  if x = ε then return
L7  a ← |T.add|; append x to T.add
L8  (k, off) ← FIND(T, i)
L9  if off = 0 and k > 0 and p_{k−1} = (add, s, ℓ) with s + ℓ = a then p_{k−1} ← (add, s, ℓ + |x|); T.n ← T.n + |x|; return
L10 if off = 0 then put the piece (add, a, |x|) before p_k
L11 else replace p_k = (b, s, ℓ) by (b, s, off), (add, a, |x|), (b, s + off, ℓ − off)
    T.n ← T.n + |x|

DELETE(T, i, d)                   ▷ remove positions i .. i + d − 1
L12 T.n ← T.n − d
L13 (k, off) ← FIND(T, i)
L14 while d > 0:
L15     (b, s, ℓ) ← p_k; t ← min(d, ℓ − off)
L16     if off = 0 and t = ℓ then remove p_k
L17     else if off = 0 then p_k ← (b, s + t, ℓ − t); k ← k + 1
L18     else if off + t = ℓ then p_k ← (b, s, off); k ← k + 1
L19     else replace p_k by (b, s, off), (b, s + off + t, ℓ − off − t); k ← k + 1
L20     d ← d − t; off ← 0

CHAR-AT(T, i)
L21 (k, off) ← FIND(T, i)
L22 (b, s, ℓ) ← p_k; return buf_b[s + off]
```

**Insert.** The new characters are always appended to the add buffer (line L7). If the insert point falls inside a piece, that piece is split in two around the new piece (line L11); if it falls between pieces, the new piece is put between them (line L10). Line L9 handles typing: when the insert point is just after the piece that ends at the end of the add buffer, the characters typed next follow it in the add buffer, so that piece grows and no new piece is made.

**Delete.** The deleted range covers a run of pieces. The first may lose a tail (line L18), the last may lose a head (line L17), the middle ones are removed (line L16), and a range inside one piece splits it (line L19). The characters stay in the buffers.

**Reading.** CHAR-AT finds the piece of position $i$ and reads one character. A range read walks the pieces from there and copies the slices.

## Example

Load "the fox jumps". The original buffer is "the fox jumps", the add buffer is empty, and there is one piece (orig, 0, 13).

| step | text | add buffer | pieces |
|---|---|---|---|
| load | the fox jumps | (empty) | (orig, 0, 13) |
| insert "quick " at 4 | the quick fox jumps | quick | (orig, 0, 4), (add, 0, 6), (orig, 4, 9) |
| insert "brown " at 10 | the quick brown fox jumps | quick brown | (orig, 0, 4), (add, 0, 12), (orig, 4, 9) |
| delete 6 at 4 | the brown fox jumps | quick brown | (orig, 0, 4), (add, 6, 6), (orig, 4, 9) |
| delete 4 at 10 | the brown jumps | quick brown | (orig, 0, 4), (add, 6, 6), (orig, 8, 5) |

The first insert falls inside the only piece, at offset 4, so it splits it (line L11). The second insert is at position 10, the end of the piece (add, 0, 6), which also ends at the end of the add buffer, so line L9 extends it to (add, 0, 12). Deleting "quick " removes the head of that piece (line L17), and deleting "fox " removes the head of the last piece. The add buffer still holds "quick brown ", and the original buffer is unchanged.

## Correctness

Each operation keeps (P1) to (P3), and INSERT and DELETE change $text(T)$ as the [list](/list/) operations require. FIND returns the piece that contains position $i$ by the prefix sums of the piece lengths, using (P2). INSERT appends to the add buffer and then replaces the piece sequence so that the new string sits between the characters before and after position $i$; DELETE removes from the pieces exactly the characters at positions $i$ to $i + d - 1$, one piece at a time. The full argument is in [the correctness proof](proofs/correctness.md).

## Complexity

In the list form of this page, with $P$ pieces:

| operation | time |
|---|---|
| CHAR-AT, FIND | $O(P)$ |
| INSERT of $m$ characters | $O(P + m)$ |
| DELETE spanning $r$ pieces | $O(P + r)$ |
| read a range of length $m$ | $O(P + m)$ |
| space | the original text, all inserted characters, and $3$ words per piece |

Each insert adds at most 2 pieces and each delete at most 1, so $P \le 1 + 2 \cdot (\text{number of edits})$. In an editing session, $P$ grows with the number of separate edit places, not with the length of the file or the number of keystrokes, because of line L9.

**Balanced tree form.** Store the pieces in a balanced binary search tree, such as a [red-black tree](/red-black-tree/), keyed implicitly by position: each node stores the total length of its subtree, as in an [order-statistic tree](/order-statistic-tree/). Then FIND takes $O(\log P)$ time, and so do insert and delete, plus the length of the strings read or inserted. Storing also the number of line breaks of each subtree finds the start of a line in $O(\log P)$ time.

**Space.** The add buffer keeps every inserted character, including the ones deleted later. For a long session this is the price of never moving data; editors that save the file write the text fresh and start a new piece table.

## Variants

- **Piece tree.** The pieces kept in a red-black tree with lengths and line counts in the nodes, as in the text buffer of Visual Studio Code (Lyu 2018).
- **Several add buffers.** Instead of one append-only buffer, a list of fixed-size chunks avoids copying when the add buffer grows.
- **Undo and redo.** Since buffers never change, each state of the text is just a piece list. Keep the old lists, or with a [persistent](/persistent-data-structure/) tree of pieces keep all versions with $O(\log P)$ extra space per edit.
- **Linked list of pieces.** A [linked list](/linked-list/) gives $O(1)$ splice once the piece is found, and is the form Crowley describes. Caching the last piece found makes edits near the previous one fast.
- **Gap buffer and rope.** A [gap buffer](/gap-buffer/) stores the text in one array with a gap at the cursor; a [rope](/rope/) stores it as a balanced tree of short strings that the tree owns. The piece table is the one of the three that never copies text on an edit.

## When to use it

Use a piece table for an editor of large files, where loading must not copy the whole file, edits should be cheap anywhere, and undo should be simple. The original buffer can be the file mapped into memory. Use a [gap buffer](/gap-buffer/) for simple editors whose edits stay near the cursor. Use a [rope](/rope/) when texts are also split and joined as values, for example in functional programs.

## Pitfalls

- **Off by one at piece boundaries.** A position at the boundary of two pieces belongs to the start of the second piece. FIND must use $off < \ell$, not $off \le \ell$, or inserts at boundaries split a piece into a piece of length zero.
- **Empty pieces.** A split at offset 0 or at offset $\ell$ makes an empty piece. Empty pieces break the invariant (P1) and make the list grow; do not create them.
- **The typing case.** Without line L9, typing $m$ characters one by one makes $m$ pieces, and FIND becomes slow. The check must test that the piece ends exactly at the end of the add buffer, or a later insert will be merged with an unrelated piece.
- **Mutating the original.** If the original buffer is a memory map of the file and the file is changed by another program, every piece into it becomes wrong. Copy or lock the file while it is open.
- **Line positions.** An editor needs the position of line $k$. In the list form this costs $O(P)$ plus a scan of the pieces for line breaks; keep line break counts per piece and per subtree.

## Implementations

The Python class keeps the original buffer as a string, the add buffer as a list of characters, and the pieces as a list of triples, with FIND as a linear scan. It merges consecutive typing as in line L9. The tests replay the example of this page and compare random sequences of edits against a plain string.

## History

The piece table is usually attributed to the Bravo editor, built at Xerox PARC in the 1970s, and was later used in Microsoft Word. Crowley (1998) described it among the data structures for text sequences, compared it with the gap buffer and with linked lists of lines, and argued for it as the best general method. Visual Studio Code moved to a piece table stored in a red-black tree in 2018, which it calls a piece tree.

## References
