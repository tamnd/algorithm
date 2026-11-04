---
tag: RA7KJS
kind: data-structure
slug: skew-binary-random-access-list
name: Skew binary random-access list
aliases:
- Okasaki skew binary list
area: data-structures/persistent-structures
level: research
summary: A persistent random-access list using skew binary numbers for O(1) cons and O(log n) index.
implements: [list]
model: pointer-machine
complexity:
  vars: {n: the number of items, i: the index used}
  time: {cons: Θ(1), head: Θ(1), tail: Θ(1), lookup: "O(min(i, log n))", update: "O(min(i, log n))", from_iterable: Θ(n)}
  space: {total: Θ(n)}
history:
  year: 1995
  people: [Chris Okasaki]
  note: Okasaki gave the structure at FPCA 1995, as a purely functional list with constant worst-case list operations and logarithmic random access, based on skew binary numbers.
prereqs: [complete-binary-tree, persistent-stack, binary-random-access-list, redundant-number-system]
see_also: [persistent-vector, structural-sharing, path-copying, purely-functional-data-structure, finger-tree, real-time-queue, positional-number-system, preorder-traversal]
sources:
  - paper: doi:10.1145/224164.224187
    title: Chris Okasaki, Purely functional random-access lists, Functional Programming Languages and Computer Architecture (FPCA), 1995
    locator: the skew binary representation, the list of complete trees, and the bounds for cons, head, tail, lookup and update
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 9, Numerical Representations, the section on skew binary numbers and skew binary random-access lists
  - paper: Eugene W. Myers, An applicative random-access stack, Information Processing Letters 17(5), 1983
    locator: an earlier persistent stack with logarithmic random access built on the same numbers
---

A skew binary random-access list is a persistent list that has the stack operations `cons`, `head` and `tail` in $\Theta(1)$ worst-case time, and access or update by index in $O(\min(i, \log n))$ time. It stores the items in a list of complete binary trees, in preorder, and the sizes of the trees are the digits of $n$ written in *skew binary*, a number system in which each digit weight is $2^k - 1$. In skew binary, adding one changes at most two digits, so `cons` joins at most two trees and does no cascade of carries; `tail` undoes it in the same way. Chris Okasaki published the structure in 1995. It is a standard example of a *numerical representation*, a data structure designed from a number system.

## In plain words

Keep the items in small piles, and each pile is a perfect tree of 1, 3, 7, 15 and so on items. The piles go from small to large, and only the two smallest piles can be the same size.

To add an item at the front: if the two smallest piles are the same size, put the new item on top of both, which makes one pile of the next size. If not, start a new pile of one. To remove the front item, do the reverse. Either way, only the front changes.

To find item $i$, skip whole piles until you reach the pile that holds it, and then go down that tree. Nothing is ever changed in place, so old lists stay valid.

## The abstract type

The structure implements a persistent [list](/list/) with these operations. `cons(x, s)` puts $x$ at the front. `head(s)` returns the first item, and `tail(s)` returns the list without it. `lookup(s, i)` returns item $i$, counting from 0. `update(s, i, y)` returns a list in which item $i$ is $y$. Each operation returns a new version and leaves the old ones valid. `head` and `tail` of the empty list, and indices outside $0 \le i < n$, are errors.

## Representation

**Skew binary numbers.** A skew binary number is a sequence of digits $d_k \in \{0, 1, 2\}$ with value $\sum_k d_k (2^{k+1} - 1)$. A number is in *canonical form* if only the lowest nonzero digit can be 2. Every $n \ge 0$ has exactly one canonical form. For example, $10 = 3 + 7$ has digits $0, 1, 1$ for the weights $1, 3, 7$, and $6 = 3 + 3$ has the digit 2 for the weight 3.

**Trees.** A list of $n$ items is a list of pairs $(w, t)$, one for each unit of a canonical digit, from the lowest weight up. Each $t$ is a complete binary tree with $w = 2^k - 1$ nodes. The items of $t$ are in preorder: the root holds the first item, the left subtree the next $(w - 1)/2$ items, and the right subtree the rest. The items of the whole list are the items of the trees, front to back.

**Invariant.** (I1) Each weight is $2^k - 1$ for some $k \ge 1$, and the tree with that weight is complete. (I2) The weights grow strictly from front to back, except that the first two may be equal. (I3) The weights sum to $n$. (I1) to (I3) say that the weights are the canonical skew binary form of $n$.

## Operations

```pseudo id=main
CONS(x, ts)
L1  if ts = (w1, t1) :: (w2, t2) :: rest and w1 = w2 then
L2      return (1 + w1 + w2, Node(x, t1, t2)) :: rest
L3  return (1, Leaf(x)) :: ts

HEAD(ts)
L4  (w, t) :: _ ← ts; return the root item of t

TAIL(ts)
L5  (w, t) :: rest ← ts
L6  if w = 1 then return rest
L7  Node(x, t1, t2) ← t; return (w div 2, t1) :: (w div 2, t2) :: rest

LOOKUP(ts, i)
L8  while i ≥ the weight of the first tree of ts do i ← i − w; ts ← rest
L9  (w, t) ← the first tree of ts
L10 while i ≠ 0 do
L11     w ← w div 2
L12     if i ≤ w then (t, i) ← (left of t, i − 1) else (t, i) ← (right of t, i − 1 − w)
L13 return the root item of t

UPDATE(ts, i, y)
L14 walk as in LOOKUP, and keep the trees skipped and the path of nodes
L15 make a copy of the node reached, with item y
L16 copy the nodes of the path, bottom up, each pointing to the new child
L17 copy the cells of the trees skipped, in front of the new tree
```

CONS is the skew binary increment: if the lowest digit is 2, it becomes 0 and the next digit goes up by one (L1, L2); otherwise the lowest digit for weight 1 goes up by one (L3). TAIL is the decrement. LOOKUP skips whole trees, then goes down a complete tree, in which the left subtree holds the items $1, \ldots, w/2$ after the root and the right subtree the items $w/2 + 1, \ldots, w - 1$ (with $w/2$ rounded down).

## Example

Cons the items $9, 8, \ldots, 0$ onto the empty list. The weights after each cons are:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| weights | 1 | 1, 1 | 3 | 1, 3 | 1, 1, 3 | 3, 3 | 7 | 1, 7 | 1, 1, 7 | 3, 7 |

Each step makes one new tree node and at most one new list cell. For $n = 10$, the first tree holds $0, 1, 2$ with root 0. The second tree has root 3, a left subtree with root 4 and leaves 5, 6, and a right subtree with root 7 and leaves 8, 9.

**Lookup of index 8.** The first tree has weight 3, and $8 \ge 3$, so skip it and set $i = 5$. In the tree of weight 7, set $w = 3$; since $5 > 3$, go right with $i = 5 - 1 - 3 = 1$. Set $w = 1$; since $1 \le 1$, go left with $i = 0$. The root there is 8.

**Update of index 8 to 80.** The walk is the same. The update copies the leaf 8, the node 7 and the root 3, and one list cell for each of the two trees. The new list shares the first tree and the subtree of 4 with the old one, and the old list still has 8 at index 8.

**Tail.** The front tree has weight 3, so tail drops its root 0 and leaves two trees of weight 1: the weights are $1, 1, 7$, which is the row for $n = 9$.

## Correctness

The invariant makes the list a canonical skew binary number. CONS: if the first two weights are equal, by (I2) they are both $w$, and $1 + 2w = 2^{k+1} - 1$ when $w = 2^k - 1$; the new tree is complete and has $x$ first in preorder, and the next weight is larger by (I2), so the invariant holds. Otherwise a weight-1 tree goes in front; the old first weight is at least 1, and if it is 1, the old second weight is larger, so only the first two can be equal. TAIL undoes either case. LOOKUP skips trees whose items come before index $i$ and then follows the preorder layout. UPDATE copies the nodes on that path only, so all old versions keep their contents. The full proof is in the proofs folder.

## Complexity

| operation | time | new space |
|---|---|---|
| cons | $\Theta(1)$ worst case | one node, at most one cell |
| head | $\Theta(1)$ | none |
| tail | $\Theta(1)$ worst case | at most two cells |
| lookup | $O(\min(i, \log n))$ | none |
| update | $O(\min(i, \log n))$ | $O(\min(i, \log n))$ |

**Lookup.** The weights grow strictly after the first two, and each is at least twice the one before it, less one. So the list has $O(\log n)$ trees, and the walk down a tree of weight $w$ takes $O(\log w)$ steps. Both parts are also $O(i)$: each tree skipped holds at least one item before index $i$, and each step down a tree moves $i$ down by at least one. The total is $O(\min(i, \log n))$. The constant is small: a lookup takes at most about $2 \log_2 n$ steps.

**Space.** A list of $n$ items has $n$ tree nodes and $O(\log n)$ cells. Versions share all trees they have in common.

## Variants

- **Binary random-access lists.** With ordinary binary numbers, trees of weight $2^k$, and items only at the leaves, `cons` and `tail` take $O(\log n)$ worst-case time, because of carries and borrows. The [binary random-access list](/binary-random-access-list/) has this simpler form.
- **Skew binomial heaps.** The same number system gives priority queues with $O(1)$ worst-case insert, and Brodal and Okasaki built on them purely functional priority queues with $O(1)$ worst-case find-min, insert and meld, a functional relative of the [Brodal queue](/brodal-queue/).
- **Myers's random-access stack.** Myers gave in 1983 an applicative stack with logarithmic access by index, built on the same skew numbers, using links that skip back along the stack instead of trees.
- **Other random-access sequences.** A [persistent vector](/persistent-vector/) gives $O(\log_{32} n)$ access with a much larger fan-out, and appends at the back. A [finger tree](/finger-tree/) adds $O(\log n)$ concatenation and split.

## When to use it

Use it in a functional language when a program uses a list mainly as a stack but needs occasional access by index, or when it must give worst-case $O(1)$ stack operations with persistence: interpreters that keep environments indexed by position, and stacks of frames in purely functional virtual machines. The constant factors are small, and access to the first items is fast. For arrays that change at random places and are read at random places, a persistent vector or a balanced tree has better constants.

## Pitfalls

- **Ordinary binary numbers.** A design with powers of two loses the $O(1)$ worst case for `cons` and `tail`; the skew form is what removes the carry chain.
- **Off-by-one in the tree walk.** In a tree of weight $w$, the left subtree holds indices $1$ to $\lfloor w/2 \rfloor$. Using $i < w/2$ in line L12 is wrong for the last item of the left subtree.
- **Indices out of range.** Line L8 runs off the end of the list for $i \ge n$. Check the bound first, or keep $n$ with each version, as the implementation does.
- **Recursion on deep structures.** The tree walk is short, but code that turns the list into a sequence must not recurse over $n$ items; use an explicit stack.
- **No concatenation.** Joining two such lists takes linear time. Use a finger tree or a rope when appends of whole lists matter.

## Implementations

## History

Eugene Myers described an applicative random-access stack in 1983 that already used the skew binary weights $2^k - 1$. Chris Okasaki presented the skew binary random-access list at FPCA in 1995, and made it a central example in his 1998 book, where numerical representations are a general method: choose a number system whose increment and decrement have the cost you want, and build a structure whose shape follows the digits. Okasaki and Brodal used the same numbers for skew binomial heaps.

## References
