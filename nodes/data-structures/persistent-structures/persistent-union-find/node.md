---
tag: ZTTVD6
kind: data-structure
slug: persistent-union-find
name: Persistent union-find
aliases:
- Conchon-Filliatre persistent union-find
- persistent disjoint sets
area: data-structures/persistent-structures
level: research
summary: A disjoint-set structure with versioned unions and finds, built with rerooting and path compression.
implements: [disjoint-set]
model: word-ram
complexity:
  vars: {n: the number of elements, d: the number of array writes between the version used and the version that owns the shared arrays, w: the number of array writes done}
  time: {make: Θ(n), find: O(log n + d), same: O(log n + d), union: O(log n + d)}
  space: {total: Θ(n + w)}
history:
  year: 2007
  people: [Sylvain Conchon, Jean-Christophe Filliâtre]
  note: Conchon and Filliâtre built a persistent union-find from Baker's persistent arrays, with union by rank and a path compression that is a hidden side effect, for use in the Coq and Ergo provers.
prereqs: [disjoint-set, union-by-rank, path-compression, bakers-trick]
see_also: [union-find-with-rollback, semi-persistent-array, fully-persistent-array, persistent-segment-tree, persistent-data-structure, inverse-ackermann-function, undo-log, version-tree]
sources:
  - paper: doi:10.1145/1292535.1292541
    title: Sylvain Conchon and Jean-Christophe Filliâtre, A persistent union-find data structure, ACM SIGPLAN Workshop on ML, 2007
    locator: the persistent arrays with rerooting, the find with path compression that updates the handle, and the union by rank
  - paper: Giuseppe F. Italiano and Neil Sarnak, Fully persistent data structures for disjoint set union problems, Workshop on Algorithms and Data Structures (WADS), LNCS 519, 1991
    locator: fully persistent disjoint set union with logarithmic worst-case cost per operation
  - paper: Henry G. Baker, Shallow binding makes functional arrays fast, ACM SIGPLAN Notices 26(8), 1991
    locator: functional arrays as one real array plus diffs, with rerooting on access
---

A persistent union-find keeps a partition of the elements $0, \ldots, n-1$ in which `union` returns a new version and leaves the old one as it was, and `find` works on any version. The design of Conchon and Filliâtre keeps the usual disjoint-set forest, with union by rank and path compression, but stores the parent and rank maps in persistent arrays with *rerooting*: one real array holds one version, and the other versions are chains of diffs that are reversed when they are used. When the program works on the newest version, as most programs do most of the time, each array access is $O(1)$ and the structure is about as fast as an imperative union-find. Path compression writes a new parent array into the handle; this is a side effect, but it does not change the partition, so no caller can see it.

## In plain words

A union-find answers "are these two in the same group?" and merges groups. Here, each merge gives a new copy of the grouping, and the old copies keep working, so a program can try a merge and go back to an earlier grouping when it fails.

The copies are not real copies. There is one real table, and each other version is a short note: "like the table, except this entry". When you use an old version, the notes are turned around so the real table becomes that version. If you mostly use the newest version, there is almost nothing to turn around, and each step is fast.

## The abstract type

The structure represents versions of a partition of $\{0, \ldots, n-1\}$. The operations are `make(n)`, which gives the partition into singletons, `find(h, x)`, which gives a fixed member of the set of $x$ in version $h$, `same(h, x, y)`, and `union(h, x, y)`, which gives a new version in which the sets of $x$ and $y$ are merged. Every version stays valid forever: this is full persistence. The representative that `find` returns may depend on the version, but it is the same for all members of one set in one version.

## Representation

A version is a handle with two fields, `rank` and `parent`, each a persistent array of $n$ integers. The parent array encodes a forest: $x$ is a root if $\text{parent}[x] = x$, and the set of $x$ is the tree that contains it. Ranks are as in [union by rank](/union-by-rank/).

The persistent arrays are those of [Baker's trick](/bakers-trick/). There is one shared array per family of versions. A version is either *Arr*, which means that it owns the shared array, or $\text{Diff}(i, v, t)$, which means "equal to version $t$, except that slot $i$ holds $v$". Before any access, a version is *rerooted*: the diffs on the path from it to the Arr version are reversed, and it becomes the Arr version.

**Invariant.** (I1) In every version, the parent array is a forest whose roots are its fixed points, and $\text{rank}[\text{parent}[x]] > \text{rank}[x]$ for each non-root $x$. (I2) The sets of the version are the trees of its forest. (I3) The diffs and the shared array of each family together give each version its contents, as in Baker's trick.

## Operations

```pseudo id=main
FIND(h, x)
L1  f ← h.parent
L2  r ← x; while GET(f, r) ≠ r do r ← GET(f, r)
L3  y ← x
L4  while y ≠ r do (y, f) ← (GET(f, y), SET(f, y, r))
L5  h.parent ← f                              ▷ same partition: invisible to callers
L6  return r

UNION(h, x, y)
L7  rx ← FIND(h, x); ry ← FIND(h, y)
L8  if rx = ry then return h
L9  a ← GET(h.rank, rx); b ← GET(h.rank, ry)
L10 if a > b then return (h.rank, SET(h.parent, ry, rx))
L11 if a < b then return (h.rank, SET(h.parent, rx, ry))
L12 return (SET(h.rank, rx, a + 1), SET(h.parent, ry, rx))
```

The persistent array, with rerooting done by loops:

```pseudo id=array
REROOT(t)
A1  collect the path t = t_0, t_1, ..., t_m, where t_m is Arr and each t_j is Diff(i_j, v_j, t_{j+1})
A2  for j ← m − 1 down to 0 do
A3      i ← i_j
A4      t_{j+1} ← Diff(i, A[i], t_j)          ▷ the old owner remembers its value
A5      A[i] ← v_j
A6      t_j ← Arr
GET(t, i)
A7  REROOT(t); return A[i]
SET(t, i, v)
A8  REROOT(t)
A9  t' ← a new Arr version
A10 t ← Diff(i, A[i], t'); A[i] ← v; return t'
```

FIND first walks to the root $r$, then sets the parent of every node on the walk to $r$. Each SET on the newest array version is $O(1)$, and the new parent array has the same trees in the sense of (I2), so line L5 can store it in the handle. UNION links the root of smaller rank below the root of larger rank, and raises the rank only on a tie.

## Example

Take $n = 4$. Write parent arrays as $[p_0, p_1, p_2, p_3]$.

- $h_0 = \text{make}(4)$: parent $[0, 1, 2, 3]$, rank $[0, 0, 0, 0]$.
- $h_1 = \text{union}(h_0, 0, 1)$: equal ranks, so $1$ goes below $0$ and rank$[0] = 1$. Parent $[0, 0, 2, 3]$.
- $h_2 = \text{union}(h_1, 2, 3)$: parent $[0, 0, 2, 2]$, rank$[2] = 1$.
- $h_3 = \text{union}(h_2, 1, 3)$: FIND gives roots 0 and 2, both of rank 1, so $2$ goes below $0$ and rank$[0] = 2$. Parent $[0, 0, 0, 2]$.

Now $\text{find}(h_3, 3)$ walks $3 \to 2 \to 0$ and compresses: the handle $h_3$ gets parent $[0, 0, 0, 0]$, with the same single set.

Then $\text{find}(h_2, 3)$ reroots the parent array to $h_2$. The diffs for the writes made by $h_3$ and by the compression are reversed, and the shared array becomes $[0, 0, 2, 2]$, so the answer is 2. Branching works too: $h_4 = \text{union}(h_1, 1, 2)$ links $2$ below $0$ (rank 1 against rank 0) and gives the sets $\{0, 1, 2\}, \{3\}$, while $h_2$ still has $\{0, 1\}, \{2, 3\}$ and $h_3$ has one set.

## Correctness

The persistent arrays give each version its own contents, by (I3) and the argument of Baker's trick: rerooting reverses each diff in turn, and each step keeps the meaning of every version. So it is enough to check each operation on one version, as if its arrays were plain arrays. FIND on a forest that satisfies (I1) ends, because rank grows strictly along a parent walk, and it returns the root of the tree of $x$. Setting the parent of a node on the walk to the root keeps it in the same tree and keeps (I1), since the root has the largest rank on the walk; so the new parent array represents the same sets, and storing it in the handle changes no answer that any later call can give. UNION with $r_x \ne r_y$ makes one root a child of the other, which merges exactly the two trees, and the rank rule keeps (I1). The full proof is in the proofs folder.

## Complexity

| operation | time on the newest version | time on another version |
|---|---|---|
| make | $\Theta(n)$ | not applicable |
| find, same | $O(\log n)$ | $O(\log n + d)$ |
| union | $O(\log n)$ | $O(\log n + d)$ |
| one array access | $O(1)$ | $O(1 + d)$ |

**Finds.** Union by rank alone keeps every rank at most $\log_2 n$, so a find walk has $O(\log n)$ steps. After the first access in an operation, the arrays are rerooted to the version in use, and every later access and write in that operation costs $O(1)$. So the cost is the walk plus one reroot of length $d$.

**Path compression.** If the versions are used one after another, in the way of an ephemeral union-find, the classic analysis applies, and the amortized cost per operation is $O(\alpha(n))$, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). If the program jumps between old versions, that amortized argument does not hold, because the work saved by compressing one version is not shared with its siblings; the $O(\log n)$ bound from the ranks still holds.

**Space.** The shared arrays take $2n$ slots, and each array write leaves one diff, so the total is $\Theta(n + w)$ for $w$ writes. Compression adds writes; a version that is no longer referenced lets the garbage collector free its diffs.

## Variants

- **Path copying.** Store the parent and rank arrays in a fully persistent array with [path copying](/path-copying/), such as a [persistent segment tree](/persistent-segment-tree/), and use union by rank without compression. Each array access costs $O(\log n)$, so each operation costs $O(\log^2 n)$ in the worst case on every version, with no hidden side effects. This form is common in programming contests.
- **Rollback only.** If the program only goes back, never sideways, a [union-find with rollback](/union-find-with-rollback/) keeps one plain forest and an [undo log](/undo-log/) of the links. Union by rank without compression keeps finds at $O(\log n)$ and undo at $O(1)$. A [semi-persistent array](/semi-persistent-array/) gives the same pattern with version values.
- **Worst-case fully persistent bounds.** Italiano and Sarnak gave fully persistent disjoint set union structures with $O(\log n)$ worst-case time per operation, using methods in the style of DSST.
- **No compression.** Dropping path compression removes the side effect in FIND, which matters when several threads share a version. The cost becomes $O(\log n + d)$ per operation by the ranks alone.

## When to use it

Use this structure when a program needs union-find on many versions but works mostly on the most recent one: backtracking searches, decision procedures for equality in SMT solvers and proof assistants, and type inference with backtracking. This is the setting for which Conchon and Filliâtre designed it. If old versions are used at random and worst-case time matters, the path-copying variant gives a firm $O(\log^2 n)$. If the program only undoes recent unions, union-find with rollback is simpler and faster.

## Pitfalls

- **Hidden mutation and threads.** FIND writes to the handle and to the shared arrays. Two threads that use versions of one family at once corrupt the shared array. Use a lock, or drop compression and rerooting.
- **Jumping between far versions.** Each switch reroots across all writes between the two versions. A loop that alternates between two old versions pays this cost every time.
- **Compression on an old version.** Compression on an old version adds diffs off the newest branch, which later accesses to the newest version must reroot across. In a backtracking search this is usually small, but it is not free.
- **Recursive rerooting.** The diff chain can be as long as the number of writes. A recursive reroot overflows the stack; use a loop, as in lines A1 to A6.
- **Rank on the right root.** The rank update in line L12 must go to the root that stays a root, here $r_x$.

## Implementations

## History

Henry Baker described functional arrays with rerooting in 1991. In the same year Giuseppe Italiano and Neil Sarnak studied fully persistent disjoint set union with worst-case bounds. Sylvain Conchon and Jean-Christophe Filliâtre presented the structure on this page at the ACM Workshop on ML in 2007. They used Baker's arrays for the parent and rank maps, kept path compression as a side effect hidden in the handle, verified the design with the Coq proof assistant, and found it as fast as an imperative union-find in their tests with backtracking, which came from their work on the Ergo prover.

## References
