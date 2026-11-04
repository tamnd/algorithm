---
tag: 1DC4F6
kind: algorithm
slug: gabow-tarjan-union-find
name: Gabow-Tarjan linear-time static union-find
aliases:
- Gabow-Tarjan algorithm
area: data-structures/disjoint-sets
level: research
summary: Linear-time algorithm for static tree set union using word-level parallelism.
solves: [static-tree-set-union]
model: word-ram
complexity:
  vars: {n: the number of nodes of the tree, m: the number of operations}
  time: {total: O(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: true, recursive: false}
prereqs: [static-tree-set-union, disjoint-set-forest, bit-parallelism, word-ram]
see_also: [static-tree-set-union, union-find-lower-bound, offline-minimum, offline-subarray-painting, arpa-offline-rmq, tarjan-offline-lca, floor-log2, bit-parallelism]
sources:
  - paper: doi:10.1016/0022-0000(85)90014-5
    title: "Harold N. Gabow and Robert Endre Tarjan, A linear-time algorithm for a special case of disjoint set union, Journal of Computer and System Sciences 30(2) (1985), 209-221"
    locator: the partition into microsets, the micro and macro finds, the analysis, and the applications
  - paper: doi:10.1145/321879.321884
    title: "Robert Endre Tarjan, Efficiency of a Good But Not Linear Set Union Algorithm, Journal of the ACM 22(2) (1975), 215-225"
    locator: the bound O(m alpha(m, n)) used for the macro forest
  - paper: doi:10.1016/0022-0000(79)90042-4
    title: "Robert Endre Tarjan, A class of algorithms which require nonlinear time to maintain disjoint sets, Journal of Computer and System Sciences 18(2) (1979), 110-127"
    locator: the separable pointer machine lower bound, which a RAM algorithm can avoid
---

The Gabow-Tarjan algorithm solves [static tree set union](/static-tree-set-union/) in $O(n + m)$ time on a [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits. The tree of the unions is known in advance, so it can be cut into small connected groups of $O(\log n)$ nodes, the *microsets*. Inside a microset, the marks of the linked nodes and the ancestors of each node fit in one word, and a find inside it is an AND and a most significant bit. A general union-find forest, the *macro forest*, joins the microsets, and it has only $O(n/\log n)$ elements, which makes its inverse Ackermann cost disappear. Gabow and Tarjan published it in 1985. It shows that union-find in this special case is linear on a RAM, while every separable pointer algorithm needs $\Omega(m\,\alpha(m, n))$ time.

## In plain words

The family tree is known before any question. So cut it into small bunches of a few dozen people each. A bunch is small enough that a single number in the computer can say, with one bit per person, who in the bunch has joined their parent. A second number, stored for each person, says who in the bunch is above that person.

To answer "who is the top of my group?", combine the two numbers. If someone above you in your bunch has not joined, the lowest such person is the answer, found with one bit trick.

If everyone above you in your bunch has joined, the answer lies above the bunch. A normal union-find, over the bunches only, takes you there. It has so few members that its slow growth costs nothing extra.

## The problem

**Input.** A rooted tree $T$ on $n$ nodes, given by a parent array, and then online operations $\mathrm{link}(v)$ for a non-root $v$ linked at most once, and $\mathrm{find}(v)$. **Output.** For each find, the nearest ancestor of $v$, with $v$ included, that is not linked. See [static tree set union](/static-tree-set-union/).

## The algorithm

**Microsets.** Fix $b = \Theta(\log n)$, at most the word size. Cut $T$ into disjoint *microsets* of at most $b$ nodes. Each microset $S$ has a *root* $r(S)$, a node outside $S$ or NONE, such that for each $x \in S$, the parent of $x$ is in $S$ or equal to $r(S)$. So $S$ is a union of *pieces*, connected parts of $T$ whose top nodes are children of $r(S)$. Number the nodes of $S$ from $0$ so that each node has a larger number than its parent in $S$. For $x \in S$, let $\mathrm{anc}(x)$ be the mask of the ancestors of $x$ inside its piece, $x$ included, and let $M(S)$ be the mask of the linked nodes of $S$.

**Cutting.** Go up the tree from the leaves. Each node $v$ collects the open lists of its children, one child at a time, into a group $G$. As soon as $|G| \ge \lceil b/2 \rceil$, $G$ is closed as a microset with root $v$, and a new group starts. At the end, the open list of $v$ is $v$ followed by what is left of $G$, which has fewer than $\lceil b/2 \rceil$ nodes. The open list of the root of $T$ is closed with root NONE. A closed group has between $\lceil b/2 \rceil$ and $2\lceil b/2 \rceil - 1 \le b$ nodes, so there are at most $2n/b + 1$ microsets. The lists, kept as linked lists in this order, are in preorder, which gives the numbering.

**The macro forest.** The set $R$ of the roots $r(S)$ that are not NONE has at most $2n/b + 1$ nodes. A disjoint-set forest on $R$, with union by size, [path compression](/path-compression/) and a name at each root, records the nodes of $R$ that are *exhausted*: all their ancestors inside their own piece are linked.

```pseudo id=main
INIT(T)
L1  b ← ⌈lg(n + 1)⌉
L2  cut T into microsets S, each with a root r(S)
L3  for each S: number its nodes in preorder; M(S) ← 0; anc(x) ← anc(x.p) or bit(x), or bit(x) if x.p ∉ S
L4  MAKE-SET(y) in the macro forest for each y in R, with name y

LINK(v)
L5  M(S(v)) ← M(S(v)) or bit(v)

MICRO-FIND(x)
L6  u ← anc(x) and not M(S(x))
L7  if u = 0 then return NONE
L8  return the node of S(x) with number ⌊lg u⌋

FIND(v)
L9  w ← MICRO-FIND(v); if w ≠ NONE then return w
L10 z ← MACRO-NAME(r(S(v)))
L11 while (w ← MICRO-FIND(z)) = NONE do
L12     MACRO-UNION(z, r(S(z)))          ▷ z is exhausted, for good
L13     z ← MACRO-NAME(z)
L14 return w
```

MICRO-FIND (lines L6 to L8) keeps the unlinked ancestors of $x$ inside its piece and takes the deepest of them, the one with the largest number, by a [floor of the base 2 logarithm](/floor-log2/). FIND first looks inside the microset of $v$. If all ancestors of $v$ inside its piece are linked, the walk leaves the microset at $r(S(v))$, and the macro forest gives the first node $z$ above it that is not exhausted. Line L12 merges an exhausted name with the set of its microset root, and MACRO-UNION gives the merged set the name of the set of $r(S(z))$.

Gabow and Tarjan do the work inside a microset by table lookup on the encoding of its shape and its marks. With a most significant bit in $O(1)$, as on this page, the masks are enough.

## Example

Take the tree of the [static tree set union](/static-tree-set-union/) page: root 0, $\mathrm{parent}(1) = \mathrm{parent}(2) = 0$, $\mathrm{parent}(3) = \mathrm{parent}(4) = 1$, $\mathrm{parent}(5) = 2$, $\mathrm{parent}(6) = \mathrm{parent}(7) = 5$, and $b = 4$, so groups close at 2 nodes. The cutting gives the microsets $A = \{3, 4\}$ with root 1, $B = \{6, 7\}$ with root 5, $C = \{1, 2, 5\}$ with root 0, numbered 1, 2, 5 as bits 0, 1, 2, and $D = \{0\}$ with root NONE. In $C$, $\mathrm{anc}(5) = \{2, 5\}$, the mask `110`. The macro forest is on $R = \{0, 1, 5\}$.

| operation | what happens | answer |
|---|---|---|
| find(6) | in $B$, 6 is not linked | 6 |
| link(6), link(5) | $M(B) = \{6\}$, $M(C) = \{5\}$ | |
| find(7) | in $B$, 7 is not linked | 7 |
| find(6) | $B$ gives NONE; name of 5 is 5; in $C$, $\{2, 5\} \setminus \{5\} = \{2\}$ | 2 |
| link(3), link(1) | $M(A) = \{3\}$, $M(C) = \{1, 5\}$ | |
| find(3) | $A$ gives NONE; name of 1 is 1; in $C$, $\mathrm{anc}(1) = \{1\}$ is all linked, so 1 is exhausted: union of 1 with $r(C) = 0$; the name is 0, and MICRO-FIND(0) = 0 | 0 |
| find(4) | in $A$, 4 is not linked | 4 |
| link(2) | $M(C) = \{1, 2, 5\}$ | |
| find(6) | $B$ gives NONE; name of 5 is 5; in $C$, $\{2, 5\}$ is all linked, so union of 5 with 0; name 0 | 0 |

The answers are the ones of the direct walk over the marks.

## Correctness

The proof rests on three facts, proved in [the correctness proof](proofs/correctness.md).

1. **The cutting.** Each node is in one microset, each piece is a connected part of $T$ whose top is a child of $r(S)$, and the preorder numbers give each ancestor a smaller number. So MICRO-FIND$(x)$ returns the nearest unlinked ancestor of $x$ inside its piece, or NONE if all are linked.
2. **Leaving a microset.** If MICRO-FIND$(x)$ is NONE, the walk from $x$ to the answer passes the whole piece and reaches $r(S(x))$, so $\mathrm{find}(x) = \mathrm{find}(r(S(x)))$. Links never get undone, so a node that is exhausted stays exhausted.
3. **The macro forest.** For each macro set, every member other than its name is exhausted and has its microset root in the same set. So the name is an ancestor of all members, and all members have the same answer as the name. Line L12 keeps this, by fact 2. Since $r(S(z))$ is a proper ancestor of the name $z$, it is in another macro set, so each union of line L12 merges two sets, and the loop stops.

## Complexity

| part | cost |
|---|---|
| cutting, numbering, masks | $O(n)$ |
| link | $O(1)$ |
| find, without the macro work | $O(1)$ |
| macro forest | at most $\lvert R \rvert - 1$ unions and $O(m + n/b)$ finds on $\lvert R \rvert \le 2n/b + 1$ nodes |
| total | $O(n + m)$ |

Each operation on masks takes $O(1)$ on a word RAM with $b \le w$; the most significant bit is $O(1)$ by an instruction, a table, or the methods of the [floor of log 2](/floor-log2/) page. Each FIND does one MACRO-NAME on line L10, plus two macro operations for each union of line L12. There are at most $\lvert R \rvert - 1$ unions in all, so the macro forest gets $m' = O(m + n/b)$ operations on $n' = O(n/\log n)$ elements, which by Tarjan's bound cost $O(n' + m'\,\alpha(m', n'))$. If $m' \ge n' \lg n'$, then $m'/n' \ge \lg n'$ and $\alpha(m', n') = O(1)$, so the cost is $O(m')$. Otherwise $m' < n' \lg n' = O(n)$, and $\alpha(m', n') \le \alpha(n') = O(\log n')$ gives $O(n' \log n') = O(n)$. In both cases the macro part costs $O(n + m)$.

## Properties

- **Online.** The links and finds may come in any order; only the tree must be known first.
- **Deterministic.** No hashing or randomness.
- **Needs a RAM.** It uses masks and table lookup or a bit scan. On a pointer machine, the separable lower bound of Tarjan applies.
- **Linear space.** Three words per node and the macro forest.

## Variants and improvements

- **Table lookup.** Gabow and Tarjan encode the shape of each microset and its marks as a small integer, and answer the micro finds from a table built in $o(n)$ time, so no bit scan is needed.
- **A growing tree.** The tree can also grow by leaves between the operations, at linear total cost, with microsets that are filled as the tree grows. This is the form that matching algorithms use.
- **Interval union-find.** When $T$ is a path, the microsets are blocks of $b$ consecutive positions, and the method becomes a simple two-level structure for [offline minimum](/offline-minimum/) and [painting subarrays](/offline-subarray-painting/).
- **Arpa's trick.** [Offline RMQ](/arpa-offline-rmq/) links along the tree of next smaller elements, so this algorithm makes it linear.

## When to use it

Use it when the bound $O(n + m)$ matters in a proof, for example to show that [offline LCA](/tarjan-offline-lca/) or offline minimum takes linear time. In code, a [disjoint-set forest](/disjoint-set-forest/) with path compression is shorter and as fast for every real input size, because $\alpha$ is at most 4.

## Pitfalls

- **Numbering.** MICRO-FIND takes the largest number among the unlinked ancestors. This is the deepest one only if each node has a larger number than its parent in the microset, as the preorder of the cutting gives.
- **Pieces, not subtrees.** A microset can hold several pieces, and a node of a piece can have children in other microsets. The mask $\mathrm{anc}(x)$ must stop at the top of the piece of $x$.
- **Wrong name after a union.** The merged macro set takes the name of the set of $r(S(z))$, not $z$, and the name must be read before the union.
- **Groups that are too small.** If groups close at any size, the number of microsets need not be $O(n/\log n)$, and the macro part is no longer linear.

## Implementations

The Python class `GabowTarjanUnionFind(parent, b=None)` builds the microsets with linked lists, keeps the masks as integers, and uses `int.bit_length` for the bit scan. The macro forest uses dictionaries with union by size and path compression. A parameter `b` sets the microset size for tests, and `check_invariant` checks the cutting, the masks and the macro names.

## History

Gabow and Tarjan (1985) gave the algorithm and many applications, among them the offline LCA problem and several graph problems. It was one of the first data structures to use the word size of a RAM to beat a pointer machine bound: Tarjan's 1979 bound for separable pointer algorithms holds for this special case, so a RAM is strictly stronger here. The question whether a RAM could also beat $\alpha$ for general unions was settled in the negative by Fredman and Saks (1989); see the [union-find lower bound](/union-find-lower-bound/).

## References
