---
tag: 00WGSN
kind: data-structure
slug: binary-random-access-list
name: Binary random-access list
aliases:
- Okasaki binary random-access list
area: data-structures/persistent-structures
level: advanced
summary: A persistent list of complete binary trees sized by binary digits, giving O(log n) index and update.
implements: [list]
model: pointer-machine
complexity:
  vars: {n: the number of items}
  time: {worst: O(log n)}
  space: {extra: Θ(n)}
history:
  year: 1996
  people: [Chris Okasaki]
  note: Okasaki presents the binary random-access list as the first example of a numerical representation, in Section 6.2.1 of his 1996 thesis and Section 9.2.1 of his 1998 book.
prereqs: [complete-binary-tree, binary-counter-increment, path-copying, list]
see_also: [skew-binary-random-access-list, persistent-vector, finger-tree, persistent-stack, positional-number-system, redundant-number-system, binomial-heap, purely-functional-data-structure]
sources:
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 9, Numerical Representations, Section 9.1 (positional number systems) and Section 9.2.1, Binary Random-Access Lists (Figure 9.6, the code)
  - url: https://www.cs.cmu.edu/~rwh/students/okasaki.pdf
    title: Chris Okasaki, Purely Functional Data Structures, PhD thesis, Carnegie Mellon University, CMU-CS-96-177, 1996
    locator: Chapter 6, Numerical Representations, Section 6.2.1, Binary Random-Access Lists
  - paper: doi:10.1145/224164.224187
    title: Chris Okasaki, Purely functional random-access lists, Proceedings of the 7th International Conference on Functional Programming Languages and Computer Architecture (FPCA 1995)
    locator: pages 86 to 95 (the skew binary random-access list, with O(1) list operations and O(log n) lookup and update)
  - paper: doi:10.1016/0020-0190(83)90106-0
    title: Eugene W. Myers, An applicative random-access stack, Information Processing Letters 17(5), 1983
    locator: pages 241 to 248
---

A binary random-access list is a [persistent](/persistent-data-structure/) sequence that supports the [list](/list/) operations cons, head and tail together with lookup and update by index, all in $O(\log n)$ time in the worst case. It stores $n$ items in [complete binary trees](/complete-binary-tree/) whose sizes are the powers of two in the binary representation of $n$, one tree for each 1 digit. Cons and tail behave like the increment and decrement of a [binary counter](/binary-counter-increment/), and lookup and update walk one tree with [path copying](/path-copying/). It is the simplest of Okasaki's *numerical representations*, data structures designed by analogy with a number system.

## In plain words

Write the number of items in binary, for example 6 as 110. Each 1 stands for a group of items, of size 2 or 4 here, and each group is a balanced tree with the items in its leaves. The groups are kept in order, from the smallest to the largest, so the first items of the list are in the smallest group.

To add an item at the front, add one to the binary number. A carry joins two trees of the same size into one tree of twice the size. Removing the first item is the opposite: a borrow splits a tree into its two halves. To find the item at some position, skip whole groups by their sizes, then go down one tree, left or right at each level. A tree with many items is still short, so each operation is fast.

## The abstract type

The structure holds a sequence $\langle x_0, \ldots, x_{n-1} \rangle$ and supports, each returning a new list and leaving its argument unchanged:

- `cons(x, L)` gives $\langle x, x_0, \ldots, x_{n-1} \rangle$; `head(L)` gives $x_0$; `tail(L)` gives $\langle x_1, \ldots, x_{n-1} \rangle$;
- `lookup(i, L)` gives $x_i$ for $0 \le i < n$;
- `update(i, y, L)` gives the sequence with $x_i$ replaced by $y$.

These are the operations of a [list](/list/) with random access, in the persistent style of a [purely functional data structure](/purely-functional-data-structure/).

## Representation

A *leaf tree* is a leaf holding one item, or a node $\text{node}(w, t_1, t_2)$ whose two children are leaf trees of the same size and whose field $w$ is its number of leaves. A *complete* leaf tree of rank $k$ has $2^k$ leaves and depth $k$. Its items, read left to right, are its *sequence*. LINK$(t_1, t_2) = \text{node}(2^{k+1}, t_1, t_2)$ joins two complete trees of rank $k$, with the items of $t_1$ first.

A list is a linked list of *digits* $d_0, d_1, \ldots, d_{\ell-1}$, least significant first. Each digit is Zero or One $t$.

**Invariant.**

- **(B1)** If $d_k = \text{One } t$, then $t$ is a complete leaf tree of rank $k$.
- **(B2)** If $\ell \ge 1$, the last digit $d_{\ell - 1}$ is a One.
- **(B3)** The list represents the concatenation of the sequences of its trees, in digit order: first the tree of the lowest One digit, then the next, and so on.

By (B1) and (B3), $n = \sum_{k : d_k = \text{One}} 2^k$. So the digits are exactly the binary representation of $n$, and by (B2) there are $\ell = \lfloor \lg n \rfloor + 1$ digits for $n \ge 1$.

## Operations

```pseudo id=main
CONS(x, L)
L1  return CONS-TREE(leaf(x), L)

CONS-TREE(t, L)                        ▷ t has the rank of the first digit of L
L2  if L is empty then return ⟨One t⟩
L3  if first(L) = Zero then return One t :: rest(L)
L4  One u ← first(L)
L5  return Zero :: CONS-TREE(LINK(t, u), rest(L))           ▷ a carry

UNCONS-TREE(L)                         ▷ returns the first tree and the rest
L6  if L is empty then error "empty list"
L7  if L = ⟨One t⟩ then return (t, ⟨⟩)                      ▷ no trailing Zero
L8  if first(L) = One t then return (t, Zero :: rest(L))
L9  (node(w, t1, t2), L′) ← UNCONS-TREE(rest(L))            ▷ first(L) = Zero: a borrow
L10 return (t1, One t2 :: L′)

HEAD(L)
L11 (leaf(x), L′) ← UNCONS-TREE(L); return x
TAIL(L)
L12 (leaf(x), L′) ← UNCONS-TREE(L); return L′

LOOKUP(i, L)
L13 for each digit d of L, in order do
L14     if d = One t then
L15         if i < size(t) then
L16             while t = node(w, t1, t2) do
L17                 if i < w / 2 then t ← t1 else i ← i − w / 2, t ← t2
L18             return the item of the leaf t
L19         i ← i − size(t)
L20 error "index out of range"

UPDATE(i, y, L)
L21 if first(L) = Zero then return Zero :: UPDATE(i, y, rest(L))
L22 One t ← first(L)
L23 if i < size(t) then return One UPDATE-TREE(i, y, t) :: rest(L)
L24 return One t :: UPDATE(i − size(t), y, rest(L))

UPDATE-TREE(i, y, t)
L25 if t is a leaf then return leaf(y)                      ▷ then i = 0
L26 node(w, t1, t2) ← t
L27 if i < w / 2 then return node(w, UPDATE-TREE(i, y, t1), t2)
L28 return node(w, t1, UPDATE-TREE(i − w / 2, y, t2))
```

**Cons.** The new leaf is a tree of rank 0. Lines L2 to L5 are binary increment: a Zero becomes a One, and a One becomes a Zero and sends the linked tree, of rank one higher, to the next digit. LINK puts the new tree first, so the new item is the first leaf.

**Head and tail.** UNCONS-TREE is binary decrement. If the first digit is a One, its tree is the first tree (line L8), and a single One digit becomes the empty list (line L7) so that (B2) holds. If the first digit is a Zero, line L9 borrows the first tree of rank $k + 1$ from the rest and splits it: its left half is returned and its right half stays as a One of rank $k$. Repeating this down to rank 0 gives a leaf, which holds the first item.

**Lookup.** Lines L13 to L15, L19 and L20 skip the trees that end before position $i$, subtracting their sizes. Lines L16 to L18 go down the tree that holds position $i$: at a node of $w$ leaves, the left half holds positions $0$ to $w/2 - 1$.

**Update.** The same walk, but it builds new copies of the digit cells and tree nodes on the path and shares all other subtrees, as in [path copying](/path-copying/). A call with an index past the end reaches the empty list, which is an error.

## Example

Cons 10, 20, 30, 40, 50 and 60 onto the empty list. The digits are written least significant first, and $T_k[\ldots]$ is a tree of rank $k$ with the given leaves.

| after cons | digits | trees |
|---|---|---|
| 10 | 1 | $T_0[10]$ |
| 20 | 0 1 | $T_1[20, 10]$ |
| 30 | 1 1 | $T_0[30]$, $T_1[20, 10]$ |
| 40 | 0 0 1 | $T_2[40, 30, 20, 10]$ |
| 50 | 1 0 1 | $T_0[50]$, $T_2[40, 30, 20, 10]$ |
| 60 | 0 1 1 | $T_1[60, 50]$, $T_2[40, 30, 20, 10]$ |

The cons of 40 carries twice: $T_0[40]$ links with $T_0[30]$ into $T_1[40, 30]$, which links with $T_1[20, 10]$ into $T_2$. The final list is $\langle 60, 50, 40, 30, 20, 10 \rangle$, and $6 = 110_2$.

- **lookup(3).** Digit 0 is Zero. Digit 1 holds 2 items, and $3 \ge 2$, so $i$ becomes 1. Digit 2 holds 4 items and $1 < 4$. At its root $w = 4$ and $1 < 2$, so go left to $T_1[40, 30]$; there $w = 2$ and $1 \ge 1$, so go right with $i = 0$ to the leaf 30.
- **update(3, 99).** It copies the digit cells of digits 0, 1 and 2, the root of $T_2$, the node $[40, 30]$ and the leaf, and shares $T_1[60, 50]$, the leaf 40 and the subtree $[20, 10]$. The new list is $\langle 60, 50, 40, 99, 20, 10 \rangle$, and the old one is unchanged.
- **tail.** The first digit is Zero, so UNCONS-TREE borrows $T_1[60, 50]$ from digit 1, returns the leaf 60, and leaves One $T_0[50]$ at digit 0 and Zero at digit 1. The digits become 1 0 1, for $5 = 101_2$. A second tail gives 0 0 1, for $4$.

## Correctness

Each operation keeps (B1) to (B3). CONS-TREE and UNCONS-TREE follow binary increment and decrement digit by digit: a tree of rank $k$ enters at digit $k$, and LINK and the split of a node change ranks by exactly one, so (B1) holds. Line L7 and the case of line L2 keep (B2). LINK and the split keep the order of the leaves, and the new or removed item is the first leaf of the first tree, so (B3) gives the right sequence. LOOKUP and UPDATE use the invariant that, at each step, $i$ is the position of the wanted item inside the remaining trees or the current subtree. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case | notes |
|---|---|---|
| cons | $O(\log n)$ | $O(1)$ amortized in single-threaded use |
| head, tail | $O(\log n)$ | |
| lookup $i$ | $O(\log n)$ | at most $\ell$ digits, then a descent of at most $\lfloor \lg n \rfloor$ levels |
| update $i$ | $O(\log n)$ time and new nodes | |
| space | $\Theta(n)$ for one version | $2n - 1$ tree nodes at most, plus $\ell$ digit cells |

There are $\ell = \lfloor \lg n \rfloor + 1$ digits and each tree has depth at most $\ell - 1$. CONS-TREE and UNCONS-TREE make one recursive call for each digit, so they take $O(\ell)$ time. In LOOKUP, the loop of line L13 runs at most $\ell$ times and the loop of line L16 at most $\ell - 1$ times. UPDATE visits at most $\ell$ digits and one path of a tree.

A cons that carries through $k$ Ones costs $k + 1$, as a binary increment does, so $m$ cons operations from the empty list cost $O(m)$ in total. This amortized bound does not survive persistence: a list of $2^k - 1$ items has $k$ One digits, and a cons onto that same version, repeated, costs $k + 1$ each time. The same is true for tail on a list of $2^k$ items. Mixed cons and tail can also cost $\Theta(\log n)$ each, for example alternating at $n = 2^k - 1$ and $2^k$.

## Variants

- **Skew binary random-access list.** The [skew binary random-access list](/skew-binary-random-access-list/) uses the skew binary number system, in which an increment changes at most two digits. Cons, head and tail become $O(1)$ in the worst case, and lookup and update stay $O(\log n)$ (Okasaki, FPCA 1995). It is the usual choice in practice.
- **Zeroless representations.** Using the digits 1 and 2 instead of 0 and 1 makes head $O(1)$ and lookup at index $i$ cost $O(\log i)$, since the first tree is never missing (Okasaki, Section 9.2.2).
- **Lazy and segmented versions.** A lazy digit list makes cons and tail $O(1)$ amortized under persistence; a segmented representation makes them $O(1)$ in the worst case (Okasaki, Sections 9.2.3 and 9.2.4).
- **Binomial heaps.** The same digit scheme with heap-ordered binomial trees instead of leaf trees is the [binomial heap](/binomial-heap/).
- **Persistent vector.** A wide trie such as the [persistent vector](/persistent-vector/) gives $O(\log_{32} n)$ access, with fast operations at the end instead of the front. A [finger tree](/finger-tree/) adds $O(1)$ amortized access at both ends and splitting.

## When to use it

Use a binary random-access list in a purely functional program that needs a stack, or a list built by cons, with occasional access by index. It is short to write and has clean worst-case bounds. Prefer the skew binary version when cons and tail dominate, and a [persistent vector](/persistent-vector/) when indexing dominates or when items are added at the end. An ordinary array is faster when persistence is not needed.

## Pitfalls

- **A trailing Zero.** Without line L7, a tail of a list with digits $\langle \text{One } t \rangle$ gives $\langle \text{Zero} \rangle$ instead of the empty list. Then the empty test fails and the number of digits is no longer $\lfloor \lg n \rfloor + 1$.
- **The order inside LINK.** LINK$(t, u)$ must put the new tree $t$ on the left. With the order swapped, cons still builds a list of the right length, but the items come out in the wrong order.
- **Counting lookup as a list walk.** The digit loop of line L13 skips whole trees, so it is $O(\log n)$, not $O(i)$. Code that walks the leaves one by one loses the point of the structure.
- **Amortized cons under persistence.** The $O(1)$ amortized cost of cons holds only when each version is used once. Reusing a version with many trailing One digits makes each cons cost $\Theta(\log n)$.
- **Recursion in update.** UPDATE recurses once per digit and once per tree level, so the depth is $O(\log n)$, which is safe. A variant that recurses once per item would not be.

## Implementations

The Python version keeps the digits as an immutable linked list of pairs, with None for Zero, and the trees as `Leaf` and `Node` objects. The class `BinaryRandomAccessList` has `cons`, `head`, `tail`, `lookup`, `update` and `check_invariant`. The tests replay the example and run random operations on random old versions against Python lists.

## History

Myers (1983) gave an applicative random-access stack with logarithmic access. Okasaki (1995) gave random-access lists based on skew binary numbers, and then made the analogy with number systems a general design method. The binary random-access list is the simpler structure on ordinary binary numbers that his 1996 thesis and his 1998 book use to introduce numerical representations.

## References
