---
tag: CSRV45
kind: data-structure
slug: union-find-with-rollback
name: Union-find with rollback
aliases:
- persistent-by-rollback union-find
- persistent-by-undo union-find
- undoable union-find
- union-find with undo
area: data-structures/disjoint-sets
level: advanced
summary: Union-find without path compression that supports undoing the most recent unions in stack order.
implements: [disjoint-set]
model: word-ram
complexity:
  vars: {n: the number of elements, u: the number of unions on the stack}
  time: {worst: O(log n)}
  space: {extra: Θ(n + u)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [disjoint-set-forest, union-by-size]
see_also: [rollback-technique, offline-dynamic-connectivity, divide-and-conquer-on-queries, union-by-size, disjoint-set-forest, dsu-with-parity, dynamic-connectivity]
sources:
  - paper: "Heikki Mannila and Esko Ukkonen, The set union problem with backtracking, Proceedings of the 13th International Colloquium on Automata, Languages and Programming (ICALP), 1986"
    locator: the set union problem with backtracking and its solution by linking without compression
  - paper: "Jeffery Westbrook and Robert E. Tarjan, Amortized analysis of algorithms for set union with backtracking, SIAM Journal on Computing 18(1) (1989)"
    locator: the amortized bounds for compaction rules that allow backtracking
  - url: https://cp-algorithms.com/data_structures/disjoint_set_union.html
    title: cp-algorithms, Disjoint Set Union
    locator: the remarks on union by size without path compression
---

Union-find with rollback is a [disjoint-set forest](/disjoint-set-forest/) that can undo its most recent unions, in the reverse order in which they were made. It uses [union by size](/union-by-size/) and *no* [path compression](/path-compression/), so each union changes only two fields, and it pushes a record of them on a stack. An undo pops one record and restores the two fields. Every operation then takes $O(\log n)$ time in the worst case, not only amortized, because the trees keep their height bound. It is the union-find inside [offline dynamic connectivity](/offline-dynamic-connectivity/) and other methods of [divide and conquer on queries](/divide-and-conquer-on-queries/), which add edges on the way down a recursion and remove them on the way back.

## In plain words

Ordinary union-find cannot forget a join, because each walk to a leader also rewires the path, and these changes are spread everywhere. Here the walks rewire nothing. So a join is just one change: one leader takes a new boss, and that boss's group gets bigger.

Write each join on a stack of notes. To undo the last join, read the top note, give the old leader back its freedom, and make the other group smaller again. Undoes must come in the reverse order of the joins, like plates taken off a pile.

The walks to the leaders stay short because the smaller group always goes under the larger one.

## The abstract type

The structure implements the [disjoint-set](/disjoint-set/) type, `make-set`, `find`, `union` and `connected`, and adds:

- `undo()`: undo the most recent union that has not been undone yet;
- `snapshot()`: return a time stamp $t$, the number of unions done so far;
- `rollback(t)`: undo unions until only the first $t$ remain.

Each union, also a union of two elements of one set, counts as one step of the history, so that `undo` always reverses the last call of `union`.

## Representation

Each element $x$ has a parent $x.p$ and, at a root, a size $x.size$. A stack $H$ holds one record per union: the pair $(a, b)$ when the union made the root $a$ a child of the root $b$, or NONE when it found one set.

**Invariant (S).** The parent pointers form a forest, each root $r$ has $r.size = |T(r)|$, and for each non-root $x$, $|T(x)| \le |T(x.p)|/2$ in the current forest, where $T(x)$ is the set of nodes whose path to the root goes through $x$. So every node has depth at most $\lfloor \lg n \rfloor$.

**Invariant (H).** Let $F_0, F_1, \ldots, F_k$ be the forests after $0, 1, \ldots, k$ unions of the current history, where $k = |H|$. Then the current forest is $F_k$, and the $i$-th record of $H$ is NONE if $F_i = F_{i-1}$, and $(a, b)$ if $F_i$ is $F_{i-1}$ with $a.p$ changed from $a$ to $b$ and $b.size$ increased by $a.size$.

## Operations

```pseudo id=main
MAKE-SET(x)
L1  x.p ← x; x.size ← 1

FIND(x)                                   ▷ no compression
L2  while x.p ≠ x do x ← x.p
L3  return x

UNION(x, y)
L4  x ← FIND(x); y ← FIND(y)
L5  if x = y then push NONE on H; return false
L6  if x.size > y.size then swap x and y
L7  push (x, y) on H
L8  x.p ← y; y.size ← y.size + x.size
L9  return true

UNDO()
L10 e ← pop H
L11 if e = NONE then return
L12 (x, y) ← e
L13 y.size ← y.size − x.size; x.p ← x
```

**Find** (lines L2 and L3) climbs to the root and changes nothing, so it leaves no trace to undo.

**Union** (lines L4 to L9) is the union by size of the [disjoint-set forest](/disjoint-set-forest/), plus the push of line L7. A union inside one set pushes NONE, so that each call has one record.

**Undo** (lines L10 to L13) pops the last record. For $(x, y)$, $x$ was a root when the union made it a child of $y$, and every later union has been undone, so $x$ is again a child of $y$ with the same subtree, and $y$ is a root. Line L13 makes $x$ a root and gives back the old size of $y$.

**Snapshot and rollback.** `snapshot()` returns $|H|$. `rollback(t)` calls `undo` until $|H| = t$. The cost is $O(1)$ per undone union.

## Example

Make the sets $0$ to $5$. The table shows the parents of $0$ to $5$, the sizes at the roots, and the stack.

| step | parents | sizes at roots | stack $H$ |
|---|---|---|---|
| start | 0 1 2 3 4 5 | all 1 | |
| union(0, 1) | 1 1 2 3 4 5 | 1: 2 | (0, 1) |
| union(2, 3) | 1 1 3 3 4 5 | 1: 2, 3: 2 | (0, 1) (2, 3) |
| $t \leftarrow$ snapshot() $= 2$ | | | |
| union(1, 3) | 1 3 3 3 4 5 | 3: 4 | (0, 1) (2, 3) (1, 3) |
| union(4, 5) | 1 3 3 3 5 5 | 3: 4, 5: 2 | ... (1, 3) (4, 5) |
| union(0, 2) | roots 3 and 3, no change | | ... (1, 3) (4, 5) NONE |
| connected(0, 2) | true | | |
| rollback(2) | 1 1 3 3 4 5 | 1: 2, 3: 2 | (0, 1) (2, 3) |
| connected(0, 2) | false | | |

The rollback pops NONE, then $(4, 5)$, which makes 4 a root and gives 5 the size 1, then $(1, 3)$, which makes 1 a root and gives 3 the size 2. The forest is the one of the snapshot.

## Correctness

Each union keeps (S), by the [union by size](/union-by-size/) lemma, and its record describes its change exactly, which keeps (H). An undo of the record $(x, y)$ is correct because (H) says that the forest is $F_k$, which is $F_{k-1}$ with exactly the change of the record; reversing those two fields gives $F_{k-1}$, which satisfies (S) because it was a forest of the history. Finds read only. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case |
|---|---|
| make-set | $O(1)$ |
| find, connected | $O(\log n)$ |
| union | $O(\log n)$ |
| undo | $O(1)$ |
| rollback($t$) | $O(1)$ per undone union |
| space | $\Theta(n + u)$ for $u$ unions on the stack |

- **Find.** By (S), each depth is at most $\lfloor \lg n \rfloor$, so a find takes $O(\log n)$ steps. An undo cannot break this bound, because it returns to an earlier forest of the history.
- **Union.** Two finds and $O(1)$ more.
- **Undo.** $O(1)$: one pop and two writes.
- **No amortized gain.** Without path compression, the bound $O(\log n)$ is also the amortized bound: a sequence of unions that builds a tree of height $\lg n$ and then repeats a find of its deepest node and a union and undo of two singletons costs $\Theta(\log n)$ per find.

Path compression would give $O(\alpha(n))$ amortized time without undo, but an undo after a compressing find must restore all the pointers that the find changed, and an adversary can then repeat the expensive find. Westbrook and Tarjan (1989) studied which compaction rules can be combined with backtracking, with amortized bounds of $O(\log n/\log\log n)$ per operation.

## Variants

- **Union by rank.** Store a rank instead of a size, and record in the stack whether the rank of $y$ grew. The bounds are the same.
- **Extra data at the roots.** A count of the sets, a sum, or a flag can be saved in the record and restored by the undo, at $O(1)$ cost each.
- **[Union-find with parity](/dsu-with-parity/).** The bit of the new edge is set in line L8 and needs no restore, because the undone edge disappears. This gives an offline test of bipartiteness under insertions and deletions.
- **A general change log.** The [rollback technique](/rollback-technique/) records every field write as a pair (address, old value) and restores them in reverse. Union-find with rollback is the case with two writes per union.

## When to use it

Use it when the unions must be undone in stack order: in backtracking search, in [offline dynamic connectivity](/offline-dynamic-connectivity/) by a segment tree over time, and in [divide and conquer on queries](/divide-and-conquer-on-queries/). It pays $O(\log n)$ per find instead of $O(\alpha(n))$. When edges must be removed in any order and online, use a structure for [dynamic connectivity](/dynamic-connectivity/) instead.

## Pitfalls

- **Path compression with undo.** Adding compression to line L2 makes the find change pointers that no record restores. After an undo, a compressed node can point past the undone link to the old root, so the sets are wrong. Keep line L2 read-only.
- **No record for a union inside one set.** Without the NONE of line L5, a caller that undoes one step per union call undoes an older union instead. Either push NONE or let the caller count only the successful unions.
- **Restoring the wrong size.** Line L13 must subtract $x.size$, which did not change while $x$ was a child: sizes change only at roots. Recomputing the size from the current tree costs too much, and saving the new size of $y$ instead of the old one leaves $y$ too large.
- **Undo out of order.** The structure can undo only the most recent union. Undoing an older one breaks (H), because later unions may have linked to or below its root.

## Implementations

The Python class keys its maps by any hashable element. It has `make_set`, `find`, `union`, `connected`, `undo`, `snapshot` and `rollback`, and `check_invariant` tests (S) and that each record on the stack matches a current link.

## History

Mannila and Ukkonen (1986) introduced the set union problem with backtracking, in which the most recent unions can be undone, and they solved it with linking by size or rank and without compression. Westbrook and Tarjan (1989) gave amortized bounds for compaction rules that allow backtracking. The form with a stack of changes is now a standard tool of offline graph algorithms.

## References
