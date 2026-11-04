---
tag: AECYGY
kind: technique
slug: bootstrapping
name: Bootstrapping
aliases:
- bootstrapped data structures
- structural bootstrapping
area: data-structures/persistent-structures
level: research
summary: Build a more efficient data structure from a simpler instance of itself to remove a logarithmic factor.
prereqs: [purely-functional-data-structure, queue, meldable-priority-queue]
see_also: [catenable-deque, banker-queue, binary-random-access-list, brodal-queue, binomial-heap, finger-tree, debit-analysis, lazy-rebuilding]
sources:
  - url: "https://www.cs.cmu.edu/~rwh/students/okasaki.pdf"
    title: Chris Okasaki, Purely Functional Data Structures, PhD thesis, Carnegie Mellon University, CMU-CS-96-177, 1996
    locator: Chapter 7, Data-Structural Bootstrapping (Section 7.1, Structural Decomposition, with 7.1.2, Queues Revisited; Section 7.2, Structural Abstraction, with 7.2.1, Lists With Efficient Catenation, and 7.2.2, Heaps With Efficient Merging; Section 7.3, Related Work)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 10, Data-Structural Bootstrapping (structural decomposition, structural abstraction, and bootstrapping to aggregate types)
  - paper: doi:10.1006/jagm.1995.1020
    title: Adam L. Buchsbaum and Robert E. Tarjan, Confluently persistent deques via data-structural bootstrapping, Journal of Algorithms 18(3), 1995
    locator: pages 513 to 547 (catenable deques of size n built from catenable deques of size O(log n))
  - paper: doi:10.1137/s0097539792242144
    title: Adam L. Buchsbaum, Rajamani Sundar and Robert E. Tarjan, Data-structural bootstrapping, linear path compression, and catenable heap-ordered double-ended queues, SIAM Journal on Computing 24(6), 1995
    locator: pages 1190 to 1206 (the name of the technique and its use for heap-ordered deques)
  - paper: doi:10.1017/S095679680000201X
    title: Gerth Stølting Brodal and Chris Okasaki, Optimal purely functional priority queues, Journal of Functional Programming 6(6), 1996
    locator: pages 839 to 857 (skew binomial queues, then two bootstrapping steps that give O(1) findMin and O(1) meld)
---

Bootstrapping, or data-structural bootstrapping, builds an efficient data structure out of a simpler or less efficient structure of the same kind, by letting the structure hold instances of itself or of the simpler structure as elements. The name and the systematic study are due to Buchsbaum, Sundar and Tarjan. Okasaki split the idea into two forms. *Structural decomposition* turns a structure that works only for bounded sizes, or one level of a recursion, into one for all sizes by storing a smaller instance in the middle. *Structural abstraction* adds a cheap join to a collection that has only a cheap insert: a bootstrapped collection is an element together with a primitive collection of bootstrapped collections, and joining two of them inserts one into the other. The second form turns heaps with $O(\log n)$ merge into heaps with $O(1)$ merge, and turns queues into [catenable lists](/catenable-deque/) with $O(1)$ catenation. Both forms work with immutable nodes, so the results are [purely functional](/purely-functional-data-structure/) and persistent.

## In plain words

Suppose you have a box that holds items and lets you add one item quickly, but pouring one full box into another is slow. Bootstrapping says: allow a box to hold other boxes. To pour box two into box one, just drop box two, unopened, into box one as a single item. That is as fast as adding one item.

The price comes later. When you take the top item out of a box, the boxes inside it must be opened and their contents put back in order. The trick is to arrange this so that the unpacking work stays small.

The other form of the idea is a structure whose middle part is a smaller copy of the same structure, which holds larger items such as pairs or whole lists. Each level is much smaller than the one above it, so there are few levels.

## When it applies

- **A primitive structure with a cheap insert and a costly join.** Structural abstraction needs a primitive collection $C$ whose insert is fast. The goal is a fast join for a new collection $B$. Typical cases: heaps with $O(1)$ insert and $O(\log n)$ merge, and queues with $O(1)$ snoc and no catenation.
- **The join may be lazy in its effect.** The joined collection is stored as one element and is opened only when the operation that removes the first element reaches it. Queries that look at the first element must be answered from the root alone.
- **A structure that is good at small sizes, or one level at a time.** Structural decomposition needs a way to split a structure into a few small top-level parts and a middle part that is a structure of the same kind over bigger elements, such as pairs or suspended lists, with far fewer of them.
- **Recursion in the types.** The element type of the inner structure differs from that of the outer one, so a typed implementation needs *polymorphic recursion* or a uniform tagged element type. Dynamic languages need no change.

## The template

The template is structural abstraction. A bootstrapped collection is either EMPTY or ROOT$(x, p)$, where $x$ is an element and $p$ is a primitive collection whose items are non-empty bootstrapped collections. The holes are the primitive operations C.INSERT and C.EXTRACT, the test FIRST-WINS that decides which root stays on top, and REATTACH, which puts the rest of a removed child back.

```pseudo id=main
UNIT(x)
L1  return ROOT(x, C.EMPTY)

JOIN(b1, b2)
L2  if b1 = EMPTY then return b2
L3  if b2 = EMPTY then return b1
L4  if FIRST-WINS(b1, b2) then           ▷ hole: lists always say yes; heaps compare the roots
L5      return ROOT(root(b1), C.INSERT(b2, items(b1)))
L6  return ROOT(root(b2), C.INSERT(b1, items(b2)))

INSERT(x, b)
L7  return JOIN(UNIT(x), b)              ▷ or JOIN(b, UNIT(x)) to add at the end of a list

REMOVE-FIRST(b)                          ▷ b = ROOT(x, p) is not empty
L8  if C.IS-EMPTY(p) then return EMPTY
L9  (c, p′) ← C.EXTRACT(p)               ▷ hole: the next child, by queue order or by smallest root
L10 let c = ROOT(y, p1)
L11 return ROOT(y, REATTACH(p1, p′))     ▷ hole: C.MERGE for heaps, a lazy join of p′ for lists
```

Line L5 is the whole point: the join of two bootstrapped collections is one primitive insert, and it never looks inside $b_2$. Line L9 picks the child that holds the next first element. For a list, that is the first child in the queue, because the elements are kept in preorder. For a heap, it is the child with the smallest root, and the primitive heap of children is ordered by roots. Line L11 puts the rest back: the grandchildren $p_1$ of the removed root and the other children $p'$ must end up below the new root $y$.

**Why it is correct.** By induction on the structure, the root of a non-empty bootstrapped collection is its first element: the first element of a list in preorder, or the minimum of a heap. Lines L4 to L6 keep this, because the root that stays on top is the first element of the joined collection: the root of $b_1$ for a list, and the smaller root for a heap. After REMOVE-FIRST, the next first element is the root of one child, the one that line L9 picks, so the new root is again the first element, and every element except $x$ appears exactly once below it.

**Cost.** UNIT and JOIN cost one primitive insert, plus $O(1)$. REMOVE-FIRST costs one primitive extract plus REATTACH. So the bootstrapped structure has the insert cost of the primitive structure for join, which is the gain, and pays at REMOVE-FIRST, which is the price. When the primitive operations are $O(1)$, the bound on REMOVE-FIRST still needs an argument about REATTACH, which is where laziness and [debit analysis](/debit-analysis/) come in for lists.

## Classic examples

### A trace of bootstrapped heaps

Here the primitive collection is a heap of bootstrapped heaps ordered by their roots, FIRST-WINS compares the roots, C.EXTRACT removes the child with the smallest root, and REATTACH is the primitive merge. Write $(x; c_1, c_2, \ldots)$ for ROOT$(x, p)$ where $p$ holds $c_1, c_2, \ldots$ in any order, and $(x)$ when $p$ is empty.

| step | operation | result |
|---|---|---|
| 1 | UNIT of 5, 3, 8, 1 | $(5)$, $(3)$, $(8)$, $(1)$ |
| 2 | $J_1 = $ JOIN$((5), (3))$ | $3 < 5$, so $(3)$ stays on top: $J_1 = (3; (5))$ |
| 3 | $J_2 = $ JOIN$((8), (1))$ | $J_2 = (1; (8))$ |
| 4 | $J = $ JOIN$(J_1, J_2)$ | $1 < 3$: $J = (1; (8), (3; (5)))$ |
| 5 | REMOVE-FIRST$(J)$ | children $(8)$ and $(3; (5))$; the smaller root is 3, so $c = (3; (5))$, $p_1 = \{(5)\}$, $p' = \{(8)\}$; result $(3; (5), (8))$ |
| 6 | REMOVE-FIRST | children $(5)$ and $(8)$; $c = (5)$, $p_1 = \{\}$, $p' = \{(8)\}$; result $(5; (8))$ |
| 7 | REMOVE-FIRST | $c = (8)$; result $(8)$ |

Every JOIN did one primitive insert and no merge of the primitive heaps. Each REMOVE-FIRST did one find-min, one delete-min and one merge on the primitive heap. With skew binomial heaps as the primitive structure, whose insert is $O(1)$ worst case and the other operations $O(\log n)$, the result has find-min, insert and merge in $O(1)$ worst-case time and delete-min in $O(\log n)$. This is the purely functional priority queue of Brodal and Okasaki, which is optimal among comparison-based heaps.

### Other examples, simple to hard

- **Catenable lists (Okasaki, Section 7.2.1).** The primitive collection is a [queue](/queue/), FIRST-WINS always says yes, and the elements are kept in preorder of the tree. Catenation is one snoc onto the queue of children of the first tree. REMOVE-FIRST links the children from right to left, and each link except the outermost one is suspended. With a [banker's queue](/banker-queue/) or a [real-time queue](/real-time-queue/) inside, a debit argument with the *left-linear debit invariant* gives $O(1)$ amortized time for every operation, even under persistent use (Theorem 7.1 of the thesis).
- **Bootstrapped queues (Okasaki, Section 7.1.2).** This one is structural decomposition. In a [banker's queue](/banker-queue/), the front is a nest of appends $(\ldots((f \mathbin{+\!\!+} \text{rev}\, r_1) \mathbin{+\!\!+} \text{rev}\, r_2) \ldots)$. The bootstrapped queue stores $f$ and the rear $r$ as plain lists and the suspended reversals in a middle queue of lists, which is itself a bootstrapped queue. Each suspended list is at least twice as long as the one before it, so the middle holds $O(\log n)$ lists and the recursion has few levels. Snoc and tail take $O(\log n)$ amortized time, and Okasaki remarks that a depth above five would need at least $2^{65536}$ elements.
- **Nested sequences.** The type $\text{Seq}\,\alpha = \text{Nil} \mid \text{Zero}(\text{Seq}(\alpha \times \alpha)) \mid \text{One}(\alpha, \text{Seq}(\alpha \times \alpha))$ is structural decomposition in its simplest form: a sequence is zero or one loose element followed by a sequence of pairs. The constructors spell the size in binary, the spine has length $O(\log n)$, and it is a typed version of the [binary random-access list](/binary-random-access-list/).
- **Finger trees.** A [finger tree](/finger-tree/) keeps short digits at both ends and a middle finger tree of 2-3 nodes, a structural decomposition with elements that grow by a factor of 2 or 3 per level.
- **Catenable deques (Buchsbaum and Tarjan).** They decompose a catenable deque of size $n$ into catenable deques of size $O(\log n)$ that hold the spines of a balanced tree. The result catenates in $O(1)$ worst-case time and deletes at the ends in $O(\log^* k)$ worst-case time, where $k$ is the number of operations so far. Kaplan and Tarjan later reached $O(1)$ for all operations with recursive slowdown; see [catenable deque](/catenable-deque/).

## Variations

- **Structural decomposition and structural abstraction.** The first stores a smaller instance over bigger elements in the middle; the second stores instances of the new structure as elements of the primitive one. Okasaki credits earlier uses of the two forms to Dietz and to Driscoll, Sleator and Tarjan.
- **A lazy middle.** Wrapping the middle queue of a bootstrapped queue in a suspension, so that operations on it run lazily, brings snoc and tail down to $O(1)$ amortized (Okasaki, Section 7.1.2). The same idea gives the lazy middle of the [finger tree](/finger-tree/).
- **Bootstrapping to add find-min.** Before the merge step, Brodal and Okasaki add a separate root that holds the minimum to a skew binomial heap, which turns $O(\log n)$ find-min into $O(1)$. This is a smaller bootstrapping step with the same shape.
- **Bootstrapping to aggregate types.** The bootstrapped structure can hold collections of a different kind, such as a trie whose children are kept in a finite map of tries (Okasaki's book, Chapter 10).
- **Recursive slowdown.** Kaplan and Tarjan combine structural decomposition with a counter-like invariant on the levels, so that an operation does $O(1)$ work at only a constant number of levels. It removes the extra $\log$ or $\log^*$ factor of plain decomposition and gives worst-case bounds.

## Pitfalls

- **Empty collections as elements.** A primitive collection of bootstrapped collections must never hold EMPTY, because the order on children compares roots. Lines L2 and L3 return before the insert for this reason.
- **Ephemeral amortization under persistence.** The simple catenable list, with an eager link of all children in REMOVE-FIRST, has $O(1)$ amortized cost only when used ephemerally. One old version with many children can be used again and again, and each use pays $\Theta(n)$. The persistent bound needs the suspended links and [debit analysis](/debit-analysis/).
- **Linking the children in the wrong order.** For catenable lists, linking the children of the removed root from left to right makes later removals redo work. Okasaki links them from right to left, which leaves the least duplicated work for later calls.
- **Types that recurse on a different type.** In a typed language, Seq of pairs inside Seq is polymorphic recursion. Without it, a uniform type with tags for elements and pairs works, but it loses the type-level guarantee that each level has the right shape.
- **Depth hidden in the constant.** Plain structural decomposition pays $O(1)$ at each level, so the bound is the number of levels times the cost per level. Count the levels: $O(\log n)$ for halving sizes, much less when each level shrinks the count by a logarithm.
- **The comparison of bootstrapped heaps.** The order on children is the order on their roots. With a primitive heap that is fixed to one element type, the element type of the primitive heap must be the bootstrapped heap itself, a recursive definition that some module systems cannot express directly.

## Exercises

1. Continue the trace of bootstrapped heaps: from $J = (1; (8), (3; (5)))$, JOIN with $(2; (4))$, then do REMOVE-FIRST twice. Write each intermediate tree.
2. Prove that with skew binomial heaps as the primitive structure, the bootstrapped heap has find-min, insert and merge in $O(1)$ worst-case time and delete-min in $O(\log n)$ worst-case time.
3. Show that the simple catenable list with an eager link of all children has $O(1)$ amortized cost per operation when used ephemerally, and give a sequence of persistent operations that costs $\Theta(n)$ per operation.
4. In the bootstrapped queue, show that the $i$-th list of the middle queue has length at least $2^{i-1}$ times the length of the first one, and conclude that the middle queue holds $O(\log n)$ lists.
5. Write the type $\text{Seq}\,\alpha$ of nested sequences above in a language without polymorphic recursion, and give a lookup by index in $O(\log n)$ time.

## References
