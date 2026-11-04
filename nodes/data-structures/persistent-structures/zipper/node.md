---
tag: T3A6Y3
kind: data-structure
slug: zipper
name: Zipper
aliases:
- Huet zipper
- list zipper
- tree zipper
area: data-structures/persistent-structures
level: advanced
summary: A tree or list plus a path of context that gives O(1) local navigation and update while keeping old versions.
implements: [tree]
model: pointer-machine
complexity:
  vars: {d: the depth of the focus, s: the size of the tree}
  time: {left: Θ(1), right: Θ(1), up: Θ(1), replace: Θ(1), set_value: Θ(1), top: Θ(1 + d), from_tree: Θ(1)}
  space: {total: Θ(s + d)}
history:
  year: 1997
  people: [Gérard Huet]
  note: Huet published the zipper as a functional pearl, as a way to edit trees in a purely functional language with local moves and updates in constant time.
prereqs: [binary-tree, persistent-stack, purely-functional-data-structure]
see_also: [path-copying, structural-sharing, persistent-binary-search-tree, finger-tree, gap-buffer, rope, tree-traversal, persistent-data-structure]
sources:
  - paper: doi:10.1017/S0956796897002864
    title: Gérard Huet, Functional pearl, The zipper, Journal of Functional Programming 7(5), 1997
    locator: the definition of the path type, the location as a pair of a subtree and a path, and the navigation and update functions
  - paper: Conor McBride, The derivative of a regular type is its type of one-hole contexts, manuscript, 2001
    locator: the derivation of the type of paths of a zipper from the type of the tree
---

A zipper is a way to hold a position inside an immutable tree or list so that a program can move the position one step and change the data near it in $O(1)$ time. It stores the subtree at the position, called the *focus*, and the path from the focus back to the root, turned inside out: each step of the path keeps the parent's value and the sibling subtree that was not taken. Moving down pushes one such step, moving up pops one and rebuilds one node, and a change at the focus only replaces the focus. Nothing is ever overwritten, so each zipper is a persistent value: old zippers and old trees stay valid, and the new tree shares all subtrees off the path with the old one. Gérard Huet described the structure in 1997.

## In plain words

Think of a tree as a set of rooms joined by doors. To walk inside it, keep two things: the room you stand in, and a trail of notes back to the entrance. Each note says which door you took and what you left on the other side.

To go deeper, write a new note on top of the trail. To go back, read the top note and rebuild the room you came from with it. To change something, change only the room you stand in.

Each step is a small, fixed amount of work. Old trails and old rooms are never erased, so you can keep an earlier position and go back to it at any time, as in an undo list.

## The abstract type

A zipper over binary trees represents a pair: a whole tree $T$ and a position $\pi$ in it (a node or an empty child). The operations are:

- `from_tree(t)`: the zipper for $t$ with the position at the root.
- `left(z)`, `right(z)`: move the position to the left or right child of the node at it.
- `up(z)`: move the position to the parent.
- `replace(z, t')`: the zipper for the tree in which the subtree at the position is $t'$, with the same position.
- `top(z)`, `to_tree(z)`: move to the root, and return the whole tree.

Each operation returns a new zipper and leaves its argument as it was. `left` and `right` on an empty position, and `up` at the root, are errors.

## Representation

A tree is empty (nil) or a node $(l, x, r)$. A zipper is a pair $(t, p)$, where $t$ is the focus subtree and $p$ is the path, a [persistent stack](/persistent-stack/) of *crumbs*. A crumb is $(\text{left}, x, s)$, meaning "the focus was the left child of a node with value $x$ and right child $s$", or $(\text{right}, x, s)$, meaning "the focus was the right child of a node with value $x$ and left child $s$". The top crumb belongs to the parent of the focus, and the bottom crumb to the root.

**Invariant.** The whole tree is $\text{plug}(t, p)$, where $\text{plug}(t, \text{nil}) = t$, $\text{plug}(t, (\text{left}, x, s) :: p') = \text{plug}((t, x, s), p')$, and $\text{plug}(t, (\text{right}, x, s) :: p') = \text{plug}((s, x, t), p')$. The depth of the focus is the length of $p$.

## Operations

```pseudo id=main
LEFT(z)
L1  (t, p) ← z
L2  if t = nil then error "empty focus"
L3  (l, x, r) ← t
L4  return (l, (left, x, r) :: p)

RIGHT(z)                                     ▷ same checks as LEFT
L5  (l, x, r) ← t
L6  return (r, (right, x, l) :: p)

UP(z)
L7  if p = nil then error "at the top"
L8  ((d, x, s), p') ← (head of p, tail of p)
L9  if d = left then return ((t, x, s), p')
L10 return ((s, x, t), p')

REPLACE(z, t')
L11 return (t', p)

TOP(z)
L12 while the path of z is not nil do z ← UP(z)
L13 return z
```

LEFT and RIGHT take a node apart: the child becomes the focus, and the rest of the node goes into a new crumb. UP is the inverse: it puts the node back together from the focus and the top crumb. A change is a REPLACE at the focus, possibly built from the old focus, such as a new value for the node. No line writes to an existing node or crumb.

## Example

Take the tree with root 4, left child 2 (children 1 and 3) and right child 6 (children 5 and 7). Write $T_k$ for the subtree with root $k$.

- `from_tree` gives $(T_4, \text{nil})$.
- `left` gives $(T_2, [(\text{left}, 4, T_6)])$.
- `right` gives $(T_3, [(\text{right}, 2, T_1), (\text{left}, 4, T_6)])$. The focus is the leaf 3, at depth 2.
- `set_value(30)` gives $(T'_{30}, \text{same path})$ with one new node, the leaf 30.
- `up` uses the crumb $(\text{right}, 2, T_1)$ and builds the new node $(T_1, 2, T'_{30})$.
- `up` uses the crumb $(\text{left}, 4, T_6)$ and builds the new root $(\ldots, 4, T_6)$.

The new tree has symmetric order $1, 2, 30, 4, 5, 6, 7$. It has three new nodes (30, 2 and 4), the same as with [path copying](/path-copying/), and it shares $T_1$ and all of $T_6$ with the old tree. The old tree and every zipper made along the way are unchanged. The difference from path copying is when the copies are made: a zipper makes them one at a time as it goes up, so many changes near one place cost $O(1)$ each, and only the final trip to the root pays for the depth.

## Correctness

The invariant gives the meaning of a zipper: the pair $(t, p)$ stands for the tree $\text{plug}(t, p)$ with the position at the root of $t$. LEFT on $((l, x, r), p)$ gives $(l, (\text{left}, x, r) :: p)$, and by the definition $\text{plug}(l, (\text{left}, x, r) :: p) = \text{plug}((l, x, r), p)$, so the tree is the same and the position is one step down to the left. RIGHT is the same with the sides swapped. UP is the inverse of LEFT and RIGHT, so it also keeps the tree and moves the position to the parent. REPLACE keeps the path, so the new tree is the old one with the subtree at the position replaced. TOP ends with an empty path, where the focus is the whole tree. No operation writes to existing memory, so all earlier zippers keep their meaning. The full proof is in the proofs folder.

## Complexity

| operation | time | new space |
|---|---|---|
| from_tree | $\Theta(1)$ | one pair |
| left, right | $\Theta(1)$ | one crumb |
| up | $\Theta(1)$ | one node |
| replace, set_value | $\Theta(1)$ | one node for set_value |
| top, to_tree | $\Theta(1 + d)$ | $d$ nodes |

A zipper for a tree of $s$ nodes with the focus at depth $d$ uses $\Theta(s + d)$ space, and most of it is shared with the original tree. The path holds exactly the parts of the tree that are not in the focus, so a walk that edits at many places and then calls `to_tree` once pays $O(1)$ per step and per edit. Reaching a node at depth $d$ from the root takes $d$ steps; the zipper does not give fast random access, only fast local moves.

## Variants

- **List zipper.** For a list, the focus is one item, and the context is two stacks: the items before it in reverse order, and the items after it. Moving left or right moves one item between the stacks, and an insert or delete at the focus is $O(1)$. This is the persistent form of a [gap buffer](/gap-buffer/), and the same idea as a two-stack list.
- **Rose trees.** For trees whose nodes have a list of children, a crumb keeps the parent's value, the siblings to the left in reverse order and the siblings to the right. Moving to the next sibling is then $O(1)$. Huet's paper uses this form.
- **Zippers for any data type.** For each algebraic data type, the type of crumbs can be derived from the type itself. McBride showed that the crumb type is the formal derivative of the type, as in calculus, so zippers exist for any regular type.
- **Finger trees and fingers.** A [finger tree](/finger-tree/) keeps fast access near both ends of a sequence, and a finger in a search tree keeps a pointer to a place in it. Unlike a zipper, both also give fast access by key or index, at a cost of $O(\log n)$ rather than $O(1)$ steps.

## When to use it

Use a zipper when a program walks an immutable tree or list and makes many changes near a moving point: structure editors (Huet's motive), the window stack of a tiling window manager, editors of syntax trees and documents, and transforms of XML and JSON trees, which libraries such as `clojure.zip` give. It also makes undo simple, because each earlier zipper is a full saved state. If the changes are at random places, a tree with [path copying](/path-copying/) from the root is simpler. If the data are mutable and not shared, a plain pointer to a node with parent links is faster.

## Pitfalls

- **Forgetting to go up.** The changes are visible in the whole tree only after `to_tree`. Reading the original tree after an edit through a zipper gives the old data, as it should; this surprises people who expect mutation.
- **Many zippers into one tree are not linked.** Two zippers made from the same tree are two separate edits. A change through one is not seen by the other, and merging them is a different problem.
- **Deep paths and recursion.** A path can be as long as the tree is deep. `top` and any walk of the path must be loops, not recursion, for trees that can be linear in depth.
- **Moves from an empty focus.** `left` and `right` at an empty subtree, and `up` at the root, must fail clearly. A sentinel that hides the error leads to wrong trees.
- **Unbalanced edits.** A zipper does not keep a search tree balanced. If the edits insert keys, rebalancing must be done separately, for example on the way up.

## Implementations

## History

Gérard Huet published the zipper in 1997 as a functional pearl in the Journal of Functional Programming. He presented it as a technique for structure editors, and noted that the idea had likely been found many times by programmers but was rarely described in print. In 2001 Conor McBride showed that the type of one-hole contexts of a regular data type is its derivative, which explained the shape of the crumbs and gave zippers for all such types. The list zipper later became common in functional programs, for example in the xmonad window manager, and libraries in Haskell, Clojure and Scala give zippers for general trees.

## References
