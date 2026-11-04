---
tag: 776W85
kind: data-structure
slug: catenable-deque
name: Catenable deque
aliases:
- Kaplan-Tarjan persistent catenable deque
- catenable list
area: data-structures/persistent-structures
level: research
summary: A persistent double-ended queue supporting concatenation in O(1) worst-case time.
implements: [deque, list]
model: pointer-machine
complexity:
  vars: {n: the number of items}
  time: {worst: O(1)}
  space: {extra: Θ(n)}
history:
  year: 1995
  people: [Haim Kaplan, Robert E. Tarjan]
  note: Kaplan and Tarjan presented purely functional catenable deques with O(1) worst-case time for every operation, built by recursive slowdown, at STOC 1995; the journal version appeared in 1999.
prereqs: [deque, purely-functional-data-structure, bootstrapping]
see_also: [finger-tree, confluent-persistence, banker-queue, real-time-queue, debit-analysis, lazy-rebuilding, persistent-stack, rope]
sources:
  - paper: doi:10.1145/324133.324139
    title: Haim Kaplan and Robert E. Tarjan, Purely functional, real-time deques with catenation, Journal of the ACM 46(5), 1999
    locator: pages 577 to 603 (recursive slowdown, noncatenable deques, then catenable deques with O(1) worst-case time per operation)
  - paper: doi:10.1137/S0097539798339430
    title: Haim Kaplan, Chris Okasaki and Robert E. Tarjan, Simple confluently persistent catenable lists, SIAM Journal on Computing 30(3), 2000
    locator: pages 965 to 977 (a simpler structure with O(1) amortized time per operation, analyzed under persistent use)
  - url: "https://www.cs.cmu.edu/~rwh/students/okasaki.pdf"
    title: Chris Okasaki, Purely Functional Data Structures, PhD thesis, Carnegie Mellon University, CMU-CS-96-177, 1996
    locator: Chapter 8, Implicit Recursive Slowdown, Section 8.5, Catenable Double-Ended Queues (Figure 8.4, simple catenable deques, then the version with five segments and O(1) amortized catenation)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 11, Implicit Recursive Slowdown (catenable double-ended queues)
  - paper: doi:10.1006/jagm.1995.1020
    title: Adam L. Buchsbaum and Robert E. Tarjan, Confluently persistent deques via data-structural bootstrapping, Journal of Algorithms 18(3), 1995
    locator: pages 513 to 547 (O(1) worst-case catenation and O(log* k) deletion at the ends)
---

A catenable deque, or c-deque, is a [deque](/deque/) that also supports the concatenation of two deques, built from immutable nodes so that every version stays valid. Its operations are cons, snoc, head, last, tail, init and catenate. Since catenation takes two old versions and makes one, a catenable deque is [confluently persistent](/confluent-persistence/). Kaplan and Tarjan gave the first structure with $O(1)$ worst-case time for every operation, by *recursive slowdown*. Simpler versions by Okasaki and by Kaplan, Okasaki and Tarjan reach $O(1)$ amortized time, even under persistent use. All of them follow the same plan: a short *front* and *rear* at the top level, and a *middle* that is a catenable deque of small deques, one level down. This page proves a strict version with $O(\log n)$ deque operations and describes the faster ones.

## In plain words

Think of a line of people that can lose or gain someone at either end, and that can also be joined to another line. The few people near each end stand loose, so changes there are quick. Everyone else stands in small groups of two or three, and the groups themselves form a line of the same kind, with loose groups near its ends and bigger bundles in its middle.

To join two lines, the end of the first and the start of the second are packed into groups and handed to the middle. Nothing in either old line is changed: the new line is built from new pieces and shares the old ones. So both old lines are still there, and the joined line can be split, extended or joined again.

## The abstract type

The structure holds a sequence $\langle x_1, \ldots, x_n \rangle$. Every operation returns a new deque and leaves its arguments unchanged.

- `cons(x, q)` and `snoc(q, x)` add $x$ at the front or the back.
- `head(q)` and `last(q)` return $x_1$ and $x_n$, for $n \ge 1$.
- `tail(q)` and `init(q)` return $\langle x_2, \ldots, x_n \rangle$ and $\langle x_1, \ldots, x_{n-1} \rangle$, for $n \ge 1$.
- `cat(q1, q2)` returns the concatenation of $q_1$ and $q_2$. The two arguments may be the same version, or any two versions.

With only cons, head, tail and cat, the structure is a *catenable list*. A [finger tree](/finger-tree/) supports the same operations and split, at a logarithmic cost for catenation.

## Representation

The version here follows Okasaki's simple c-deque, with bounded sizes so that the small deques are tuples of $O(1)$ size. An *element of level 0* is an item. An *element of level* $k + 1$ is a tuple of 2 or 3 elements of level $k$. A *c-deque of level* $k$ is one of

- $\text{Shallow}(d)$, where $d$ is a tuple of 0 to 4 elements of level $k$;
- $\text{Deep}(f, m, r)$, where the front $f$ and the rear $r$ are tuples of 2 to 4 elements of level $k$, and the middle $m$ is a c-deque of level $k + 1$.

The sequence of a c-deque is read from left to right: the items of $f$, then those of $m$, then those of $r$. A c-deque for the user is one of level 0.

**Invariant.** (C1) Every element of level $k + 1$ has 2 or 3 children, all of level $k$. (C2) Every Shallow tuple has at most 4 elements, every front and rear has 2 to 4. (C3) The middle of a Deep c-deque of level $k$ is a c-deque of level $k + 1$.

An element of level $k$ holds at least $2^k$ items. If the spine has $D$ Deep levels, the deepest of them is a Deep c-deque of level $D - 1$ with at least 4 elements in its front and rear, so $n \ge 4 \cdot 2^{D-1} = 2^{D+1}$ and $D \le \lg n - 1$.

## Operations

SNOC and INIT are the mirror images of CONS and TAIL, and PUSH-BACK is the mirror image of PUSH-FRONT. HEAD returns the first element of $d$ or of $f$, and LAST is symmetric. FROM-TUPLE$(s)$, for at most 8 elements, returns Shallow$(s)$ if $|s| \le 4$, and otherwise splits $s$ into a front of $\lfloor |s|/2 \rfloor$ and a rear of $\lceil |s|/2 \rceil$ elements with an empty middle.

```pseudo id=main
CONS(x, q)
L1  if q = Shallow(d) and |d| < 4 then return Shallow(x · d)
L2  if q = Shallow(a, b, c, e) then return Deep((x, a), Shallow(), (b, c, e))
L3  let q = Deep(f, m, r)
L4  if |f| < 4 then return Deep(x · f, m, r)
L5  let f = (a, b, c, e)
L6  return Deep((x, a), CONS((b, c, e), m), r)    ▷ one element of the next level

TAIL(q)                                          ▷ q is not empty
L7  if q = Shallow(d) then return Shallow(d without its first element)
L8  let q = Deep(f, m, r)
L9  if |f| > 2 then return Deep(f without its first element, m, r)
L10 let f = (a, b)
L11 if m is not empty then return Deep(b · HEAD(m), TAIL(m), r)
L12 s ← b · r                                    ▷ 3 to 5 elements
L13 if |s| ≤ 4 then return Shallow(s)
L14 return Deep((s1, s2), Shallow(), (s3, s4, s5))

PUSH-FRONT(d, m)                                 ▷ d has 2 to 4 elements
L15 if |d| ≤ 3 then return CONS(d, m)
L16 return CONS((d1, d2), CONS((d3, d4), m))

CAT(q1, q2)
L17 if q1 = Shallow(d1) and q2 = Shallow(d2) then return FROM-TUPLE(d1 · d2)
L18 if q1 = Shallow(d) then                      ▷ q2 = Deep(f2, m2, r2)
L19     if |d| ≤ 1 then return q2 with the elements of d added by CONS
L20     return Deep(d, PUSH-FRONT(f2, m2), r2)
L21 if q2 = Shallow(d) then                      ▷ q1 = Deep(f1, m1, r1)
L22     if |d| ≤ 1 then return q1 with the elements of d added by SNOC
L23     return Deep(f1, PUSH-BACK(m1, r1), d)
L24 return Deep(f1, CAT(PUSH-BACK(m1, r1), PUSH-FRONT(f2, m2)), r2)
```

CONS adds to the front tuple, and when it is full it keeps two elements and sends the other three down as one element of the next level (line L6). TAIL removes from the front, and when only two are left it takes one element from the middle and opens it, so that the new front has 3 or 4 elements (line L11). If the middle is empty, the last front element joins the rear (lines L12 to L14). CAT keeps the outer front and the outer rear, and turns the inner rear $r_1$ and the inner front $f_2$ into elements of the middle. A tuple of 4 does not fit in one element, so PUSH-FRONT splits it into two pairs (line L16). The two middles are then catenated one level down (line L24).

## Example

Build $a = \langle 1, \ldots, 5 \rangle$ and $b = \langle 6, \ldots, 10 \rangle$ by SNOC. The fifth snoc finds the shallow tuple $(1, 2, 3, 4)$ full, so $a = \text{Deep}((1, 2, 3), \text{Shallow}(), (4, 5))$ and $b = \text{Deep}((6, 7, 8), \text{Shallow}(), (9, 10))$.

| step | operation | result |
|---|---|---|
| 1 | $c = $ CAT$(a, b)$, line L24 | PUSH-BACK of $(4, 5)$ gives Shallow$((4,5))$; PUSH-FRONT of $(6,7,8)$ gives Shallow$((6,7,8))$ |
| 2 | the inner CAT, line L17 | two Shallow c-deques of one element each: Shallow$((4,5), (6,7,8))$ |
| 3 | result | $c = \text{Deep}((1,2,3),\ \text{Shallow}((4,5), (6,7,8)),\ (9,10))$ |
| 4 | TAIL$(c)$, line L9 | $\text{Deep}((2,3),\ \text{Shallow}((4,5),(6,7,8)),\ (9,10))$ |
| 5 | TAIL again, line L11 | front $(3)$ plus the opened element $(4,5)$: $\text{Deep}((3,4,5),\ \text{Shallow}((6,7,8)),\ (9,10))$ |
| 6 | TAIL again, line L9 | $\text{Deep}((4,5),\ \text{Shallow}((6,7,8)),\ (9,10))$ |

After step 3, the old versions $a$ and $b$ are unchanged: CAT made new nodes and shared the tuples $(1, 2, 3)$ and $(9, 10)$ with them.

## Correctness

Each operation keeps (C1) to (C3) and returns the right sequence. CONS and TAIL are proved by induction on the depth of the spine: a full front sends one element of 3 elements one level down, and a front of 2 takes one element of 2 or 3 elements from the middle, which gives a front of 3 or 4. PUSH-FRONT turns a tuple of 2 to 4 elements into one or two elements of the next level with the same items in order. CAT is proved by induction on the level: lines L17 to L23 handle a Shallow argument directly, and line L24 keeps the outer parts and passes valid c-deques of the next level, whose sequences concatenate to the middle part, to the recursive call. No line changes an existing node, so every old version keeps its sequence. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | strict version of this page, worst case | Okasaki's simple c-deque, lazy | Kaplan and Okasaki and Tarjan, or Okasaki's five segments | Kaplan and Tarjan |
|---|---|---|---|---|
| cons, snoc, head, last | $O(\log n)$, head and last $O(1)$ | $O(1)$ amortized | $O(1)$ amortized | $O(1)$ worst case |
| tail, init | $O(\log n)$ | $O(1)$ amortized | $O(1)$ amortized | $O(1)$ worst case |
| cat | $O(\log \min(n_1, n_2) \cdot \log(n_1 + n_2))$ | $O(\log \min(n_1, n_2))$ amortized | $O(1)$ amortized | $O(1)$ worst case |
| space | $\Theta(n)$ | $\Theta(n)$ | $\Theta(n)$ | $\Theta(n)$ |

**Worst case of the strict version.** The spine has at most $\lg n$ levels. CONS does $O(1)$ work per level and recurses only when the front is full, so it costs $O(\log n)$. TAIL recurses at most once per level, through line L11. In CAT, the arguments of the recursive call at level $k$ hold at most $n_1$ and $n_2$ items, and both are Deep only if $n_1, n_2 \ge 2^{k+2}$. So the recursion has at most $1 + \lg \min(n_1, n_2)$ levels, and each level does up to four calls of CONS or SNOC, each $O(\log(n_1 + n_2))$.

**The amortized versions.** Okasaki makes the middle a lazy, memoized value. CONS and TAIL then cost $O(1)$ amortized by implicit recursive slowdown, proved with the [debit method](/debit-analysis/), and simple CAT costs $O(\log \min(n_1, n_2))$ because it recurses to the depth of the shallower deque. To make catenation $O(1)$, his second structure has five segments, a front, an *antemedial* part, a middle, a *postmedial* part and a rear, so that CAT at one level only calls CONS and SNOC at the next level. Kaplan, Okasaki and Tarjan give a simpler structure with the same amortized bounds under persistence. Kaplan and Tarjan reach $O(1)$ in the worst case with recursive slowdown, which keeps a regularity invariant on the levels, much like a redundant binary counter, so that each operation does $O(1)$ work at $O(1)$ levels.

## Variants

- **Buchsbaum and Tarjan's deques.** By [bootstrapping](/bootstrapping/), they decompose a catenable deque of size $n$ into catenable deques of size $O(\log n)$ that hold the spines of a balanced tree. Catenation is $O(1)$ in the worst case and deletion at the ends is $O(\log^* k)$, where $k$ is the number of operations.
- **Catenable lists by structural abstraction.** If only cons, head, tail and cat are needed, Okasaki's bootstrapped list stores a tree of elements in preorder, with the children in a queue. Every operation is $O(1)$ amortized, and the code is much shorter.
- **Driscoll, Sleator and Tarjan.** The first sublogarithmic persistent catenable lists, with catenation in $O(\log \log k)$ time and the other operations in $O(1)$.
- **Finger trees.** A [finger tree](/finger-tree/) gives up $O(1)$ catenation, which costs $O(\log \min(n_1, n_2))$, and gains split and indexing by a [monoid](/monoid/) measure.
- **Mutable catenable deques.** A doubly linked list catenates in $O(1)$ by relinking, but it is [ephemeral](/ephemeral-data-structure/): the two old lists are destroyed.

## When to use it

Use a catenable deque when sequences are joined often, old versions must survive, and access is only at the ends: functional programs that build output by catenation, and persistent work lists. If the program also splits or indexes, a [finger tree](/finger-tree/) or a [rope](/rope/) is a better fit. If old versions are never used again, a mutable doubly linked list is simpler and faster.

## Pitfalls

- **Cascades at one end.** In the strict version, a cons on a deque whose fronts are full at every level recurses through all levels, and so can a tail on a deque whose fronts all have 2 elements. Under persistence, one such old version can be reused again and again, at $O(\log n)$ each time. The lazy versions need memoized suspensions to make this rare, and the worst-case bound needs recursive slowdown.
- **Fronts that grow without bound.** In Okasaki's simple c-deque, the small deques can hold any number of elements, and it relies on an $O(1)$ deque for them. With plain tuples or arrays as small deques, their size must be bounded, as in this page, or each copy costs more than $O(1)$.
- **Losing an element in TAIL.** When the front drops to one element and the middle is empty, that element must join the rear (line L12). Returning the rear alone drops it.
- **Elements of different levels.** In a typed language, the middle holds deques of deques, a case of polymorphic recursion. A uniform type for all levels compiles but lets elements of different levels mix; the invariant (C1) must then be checked by hand.
- **Tuples of 4 in the middle.** The middle holds elements of 2 or 3, so a front or rear of 4 must be split into two pairs before it is pushed down (line L16).

## Implementations

The Python version is the strict structure of this page. `_Shallow` and `_Deep` are the two node classes, and fronts, rears and elements of the next level are tuples. The class `CatenableDeque` stores the root and the length, and has `cons`, `snoc`, `head`, `last`, `tail`, `init`, `concat` (also `+`), `depth` and `check_invariant`. The tests apply random operations, including catenations of two random old versions, to random old versions, and compare each result with a Python list.

## History

Myers in 1984 used AVL trees for applicative lists with $O(\log n)$ catenation. Driscoll, Sleator and Tarjan gave catenable lists with $O(\log \log k)$ catenation in 1994, and Buchsbaum and Tarjan used data-structural bootstrapping for catenable deques in 1995. Kaplan and Tarjan reached $O(1)$ worst-case time for every operation with recursive slowdown in 1995, with the journal version in 1999. Okasaki gave simpler amortized versions with lazy evaluation in his 1996 thesis, and Kaplan, Okasaki and Tarjan published simple confluently persistent catenable lists in 2000.

## References
