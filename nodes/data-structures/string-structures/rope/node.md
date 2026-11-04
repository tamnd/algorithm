---
tag: K8GJQ9
kind: data-structure
slug: rope
name: Rope
aliases:
- cord
area: data-structures/string-structures
level: core
summary: Balanced binary tree of string fragments supporting fast concatenation, split and insertion in long texts.
implements: [list]
model: word-ram
complexity:
  vars: {n: the length of the text, L: the maximum length of a leaf string}
  time: {worst: O(log n + L)}
  space: {extra: Θ(n / L + n)}
properties: {persistent: true, concurrent: false, external: false}
prereqs: [avl-tree, binary-tree, order-statistic-tree]
see_also: [piece-table, gap-buffer, avl-tree, join-based-tree-algorithms, implicit-treap, finger-tree, persistent-data-structure, weight-balanced-tree]
sources:
  - paper: Hans-J. Boehm, Russ Atkinson and Michael Plass, Ropes, an alternative to strings, Software Practice and Experience 25(12), 1995, doi:10.1002/spe.4380251203
    locator: pages 1315 to 1330, the rope representation, concatenation, substring, and the balancing rule by Fibonacci numbers
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3 (Balanced trees), the representation of linear lists by balanced trees with RANK fields, and concatenation and splitting
  - paper: Guy E. Blelloch, Daniel Ferizovic and Yihan Sun, Just join for parallel ordered sets, Proceedings of the 28th ACM Symposium on Parallelism in Algorithms and Architectures (SPAA 2016), doi:10.1145/2935764.2935768
    locator: pages 253 to 264, the join of AVL trees in time proportional to the height difference, and split built on join
---

A rope represents a long string as a binary tree whose leaves hold short strings and whose inner nodes stand for the concatenation of their two subtrees. Each inner node stores the total length of its subtree, so the character at position $i$ is found by one walk from the root that goes left or right by comparing $i$ with the length of the left subtree. When the tree is kept balanced, here by the [AVL](/avl-tree/) height rule, concatenating two ropes, splitting a rope at a position, and therefore inserting or deleting a substring anywhere all take $O(\log n)$ time plus the length of one leaf, instead of the $\Theta(n)$ of copying a flat string. Ropes are usually immutable: an operation builds $O(\log n)$ new nodes and shares the rest, so old versions stay valid.

## In plain words

A very long string is awkward to edit: inserting one word in the middle shifts everything after it. A rope cuts the string into short pieces and hangs them as the leaves of a tree, in order from left to right. Each branching point remembers how many characters lie below it.

To find character number $i$, start at the top. If the left part has more than $i$ characters, go left; otherwise subtract its size and go right. To glue two ropes, make a new top with the two old ones below it, and fix the shape if one side is much taller. To cut a rope at position $i$, walk down to $i$ and glue the pieces on each side back together. Insert and delete are a cut and a glue or two.

## The abstract type

The rope implements the [list](/list/) of characters with these operations, each returning a new rope: `char_at(i)`, `concat(other)`, `split(i)` into the first $i$ characters and the rest, `insert(i, s)`, `delete(i, j)` of positions $i$ to $j - 1$, `substring(i, j)`, `length`, and `to_string`. Because the ropes are values, it is also a [persistent](/persistent-data-structure/) sequence.

## Representation

- A *leaf* holds a nonempty string $t.s$ of length at most $L$. Its length is $\lvert t.s \rvert$ and its height is 0.
- An *inner node* $t$ has children $t.left$ and $t.right$, and stores $t.len = t.left.len + t.right.len$ and $t.h = 1 + \max(t.left.h, t.right.h)$.
- The empty rope is the empty tree NIL.

The text of a tree is $text(\text{leaf}) = t.s$ and $text(t) = text(t.left) \cdot text(t.right)$.

**Invariant.**

- **(R1) Lengths and heights.** Every inner node stores the correct $len$ and $h$, and every leaf string is nonempty and has length at most $L$.
- **(R2) Balance.** At every inner node, $\lvert t.left.h - t.right.h \rvert \le 1$.

By (R2), as in an AVL tree, a rope of height $h$ has at least $F_{h+2} - 1$ nodes, where $F$ is the Fibonacci sequence, so $h < 1.4405 \lg(\text{number of leaves} + 2)$. A rope of $n$ characters has at least $n / L$ leaves and at most $n$, so its height is $O(\log n)$.

## Operations

```pseudo id=main
CHAR-AT(t, i)
L1  while t is an inner node:
L2      if i < t.left.len then t ← t.left
L3      else i ← i − t.left.len; t ← t.right
L4  return t.s[i]

CONCAT(a, b)
L5  if a = NIL then return b; if b = NIL then return a
L6  if |a.h − b.h| ≤ 1 then return NODE(a, b)
L7  if a.h > b.h then return BALANCE(NODE(a.left, CONCAT(a.right, b)))
L8  else return BALANCE(NODE(CONCAT(a, b.left), b.right))

SPLIT(t, i)                       ▷ returns (first i characters, the rest)
L9  if t is a leaf then return (LEAF(t.s[0 .. i−1]), LEAF(t.s[i ..])), dropping empty leaves
L10 if i ≤ t.left.len then (x, y) ← SPLIT(t.left, i); return (x, CONCAT(y, t.right))
L11 else (x, y) ← SPLIT(t.right, i − t.left.len); return (CONCAT(t.left, x), y)

INSERT(t, i, s)
L12 (x, y) ← SPLIT(t, i)
L13 return CONCAT(CONCAT(x, BUILD(s)), y)

DELETE(t, i, j)                   ▷ remove positions i .. j − 1
L14 (x, y) ← SPLIT(t, i); (_, z) ← SPLIT(y, j − i)
L15 return CONCAT(x, z)
```

NODE builds a new inner node with the given children. BALANCE takes a node whose children differ in height by at most 2 and restores (R2) with one single or double rotation, exactly as in AVL insertion. BUILD cuts a string into leaves of length $L$ (the last one shorter) and builds a perfectly balanced tree over them. An implementation can also merge two leaves into one in CONCAT when their total length is at most $L$, which keeps leaves from getting too short after many splits.

**Concatenation** walks down the right spine of the taller tree, or the left spine, until it meets a subtree whose height is within 1 of the other tree, joins them there with one new node, and rebalances on the way back up. Each step down lowers the height difference, so CONCAT takes $O(\lvert a.h - b.h \rvert + 1)$ time and makes that many new nodes.

**Split** walks the path to position $i$ and, on the way back up, concatenates the pieces that hang off the path to the left and to the right of it. The costs of these concatenations add up to $O(\log n)$ because the heights of the pieces on each side increase along the way, so the height differences telescope.

## Example

Build "the_quick_fox_jumps" (19 characters) with $L = 4$. BUILD cuts it into 5 leaves, the\_, quic, k\_fo, x\_ju and mps, and makes the tree

((( the\_ quic ) k\_fo ) ( x\_ju mps ))

of height 3. The root has $len = 19$ and its left child $len = 12$.

- **CHAR-AT(10).** At the root, $10 < 12$: go left. At the left child, its left subtree has 8 characters and $10 \ge 8$: go right with $i = 2$. The leaf is k\_fo, and its character 2 is "f".
- **SPLIT(10).** The path goes to the leaf k\_fo, which splits into k\_ and fo. Going back up, the left results are concatenated into (( the\_ quic ) k\_ ), the text "the_quick_", and the right ones into ( fo ( x\_ju mps )), the text "fox_jumps".
- **INSERT(10, "brown_").** BUILD("brown_") gives ( brow n\_ ). The two concatenations give (((( the\_ quic ) k\_ ) ( brow n\_ )) ( fo ( x\_ju mps ))), the text "the_quick_brown_fox_jumps", with 8 leaves and height 4. The rope "the_quick_fox_jumps" is still there, unchanged: the new rope shares its leaves and the subtree ( x\_ju mps ).
- **DELETE(4, 10)** on the new rope removes "quick_" and gives (( the\_ ( brow n\_ )) ( fo ( x\_ju mps ))), the text "the_brown_fox_jumps".

## Correctness

CONCAT returns a tree whose text is $text(a) \cdot text(b)$, because NODE keeps the order of its children and the rotations of BALANCE do not change the order of the leaves; and it returns a balanced tree whose height is $\max(a.h, b.h)$ or one more. SPLIT returns two trees whose texts are $text(t)[0 .. i-1]$ and $text(t)[i ..]$, by induction on the path, using CONCAT. CHAR-AT keeps the claim that the answer is character $i$ of $text(t)$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| CHAR-AT | $O(\log n)$ |
| CONCAT of ropes of heights $h_a, h_b$ | $O(\lvert h_a - h_b \rvert + 1)$, so $O(\log n)$ |
| SPLIT | $O(\log n + L)$ |
| INSERT of a string of length $m$ | $O(\log n + L + m)$ |
| DELETE | $O(\log n + L)$ |
| SUBSTRING of length $m$ | $O(\log n + L + m)$ |
| TO-STRING | $O(n)$ |
| space of one rope | $O(n / L)$ nodes when the leaves are full, and $n$ characters |
| space of a new version | $O(\log n)$ new nodes plus $O(L)$ characters |

The term $L$ is the cost of copying the part of one leaf at a split. For a whole sequence of edits, the leaves can become shorter than $L$, but never more than one new short leaf is created per split, so the number of leaves stays at most $n / L$ plus twice the number of splits, unless leaves are merged again.

**Compared with a flat string.** A flat string answers CHAR-AT in $O(1)$ and is faster for short texts, but insert, delete and concatenation copy $\Theta(n)$ characters. The rope wins once texts are long and edits are many, and it also makes each old version cost only $O(\log n)$ extra space.

## Variants

- **Boehm, Atkinson and Plass ropes.** Concatenation just makes a new node, in $O(1)$ time, and does not rebalance. A rope of depth $d$ counts as balanced if its length is at least $F_{d+2}$. When an operation finds a rope that is too deep, it is rebuilt by inserting its leaves, in order, into an array of slots indexed by Fibonacci lengths (Boehm, Atkinson and Plass 1995). Short concatenations copy into a flat leaf instead of making a node.
- **Other balance rules.** Any balanced tree with join and split works: red-black trees, [weight-balanced trees](/weight-balanced-tree/), or an [implicit treap](/implicit-treap/), whose split and merge are expected $O(\log n)$. See [join-based tree algorithms](/join-based-tree-algorithms/).
- **Finger trees.** A [finger tree](/finger-tree/) of string chunks gives amortized $O(1)$ access to both ends and $O(\log \min(i, n - i))$ split at position $i$.
- **Mutable ropes.** Editors that keep one current text can update the nodes in place and skip the copying of the path, at the price of losing old versions.
- **Line counts.** Storing the number of line breaks in each subtree finds line $k$ in $O(\log n)$ time, which is what text editors need.

## When to use it

Use a rope for long strings that are built by concatenation and edited in the middle, especially in functional languages or when old versions are needed, for example in an editor with undo, or a compiler that builds output from many pieces. For short strings, or for strings that are read far more often than they change, a flat string is simpler and faster. For editing near one cursor, a [gap buffer](/gap-buffer/) is simpler, and for editing a loaded file without copying it, a [piece table](/piece-table/) is the usual choice.

## Pitfalls

- **Unbalanced concatenation.** Making a new node for each concatenation without any rebalancing gives a tree of depth $n / L$ after appending leaves one at a time, and every access becomes linear. Either rebalance on every concatenation, as here, or check the depth as Boehm, Atkinson and Plass do.
- **Tiny leaves.** Many small edits leave many leaves of one or two characters, which wastes memory and slows walks. Merge neighbouring leaves when their total length is at most $L$.
- **Positions at the boundary.** In SPLIT, position $i = t.left.len$ goes entirely to the left part. Use $i \le t.left.len$ in line L10, or a split at a node boundary will descend into the right subtree with $i = 0$ and create an empty leaf.
- **Recursion depth.** CONCAT and SPLIT recurse along one path, of length $O(\log n)$ for a balanced rope; this is safe. Recursion on unbalanced ropes is not, and a walk over all leaves must use a loop with a stack.
- **Character units.** For Unicode text, decide whether positions count code points, UTF-16 units or bytes, and store lengths in that unit.

## Implementations

The Python class is immutable and uses the AVL rule. CONCAT merges two leaves when their total length is at most $L$, and BUILD builds a perfectly balanced tree over the chunks of a string. The walks over all leaves use an explicit stack; CONCAT and SPLIT recurse along a single path. The tests check the example, the balance of a rope built by 2000 concatenations, and random edits against a plain string.

## History

Ropes were part of the Cedar environment at Xerox PARC in the 1980s. Boehm, Atkinson and Plass described the data structure in 1995, with $O(1)$ concatenation and the rebalancing rule by Fibonacci numbers; a C version, called cords, comes with the Boehm garbage collector. The underlying idea, a linear list stored in a balanced tree with the size of each subtree in its nodes, so that positions can be found and lists split and joined in logarithmic time, is older and is described by Knuth (Section 6.2.3).

## References
