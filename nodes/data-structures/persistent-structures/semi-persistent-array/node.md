---
tag: 07TV6Q
kind: data-structure
slug: semi-persistent-array
name: Semi-persistent array
aliases:
- Baker's array
- rerooting array
- Conchon-Filliatre persistent array
area: data-structures/persistent-structures
level: advanced
summary: A persistent array with O(1) access to the newest version, where older versions are reconstructed by diffs.
implements: [static-sequence]
model: word-ram
complexity:
  vars: {n: the number of slots, d: the number of versions between the version used and the newest valid version, k: the number of valid versions}
  time: {get: Θ(1 + d), set: Θ(1 + d), to_list: Θ(n + d), is_valid: Θ(1)}
  space: {total: Θ(n + k)}
history:
  year: 2008
  people: [Sylvain Conchon, Jean-Christophe Filliâtre]
  note: Conchon and Filliâtre defined semi-persistence, where only ancestors of the newest version may be used, and showed that arrays built on Baker's diffs become simpler and faster under it.
prereqs: [array, persistent-data-structure, version-tree]
see_also: [bakers-trick, fully-persistent-array, persistent-union-find, undo-log, union-find-with-rollback, partial-persistence, persistent-vector, fat-node]
sources:
  - paper: Sylvain Conchon and Jean-Christophe Filliâtre, Semi-persistent data structures, European Symposium on Programming (ESOP), 2008
    locator: the definition of semi-persistence and the semi-persistent arrays built from diffs
  - paper: doi:10.1145/1292535.1292541
    title: Sylvain Conchon and Jean-Christophe Filliâtre, A persistent union-find data structure, ACM SIGPLAN Workshop on ML, 2007
    locator: the persistent arrays with diffs and rerooting (the Arr and Diff representation)
  - paper: Henry G. Baker, Shallow binding makes functional arrays fast, ACM SIGPLAN Notices 26(8), 1991
    locator: functional arrays as a real array plus chains of diffs, with rerooting on access
---

A semi-persistent array keeps one real array for the newest version, and stores each older version as a *diff*: "this version equals the next one, except that slot $i$ holds $x$". A read of the newest version and an update of it take $O(1)$ time. A read of an older version follows its chain of diffs to the newest, so it costs $O(1 + d)$ for a version $d$ steps back. Semi-persistence, as defined by Conchon and Filliâtre, means that only the versions on the path from the first version to the newest one may be used. An update of an older version first rolls the array back to it, which makes all later versions invalid, and then becomes the newest version. This fits backtracking, where a search goes back to an earlier state and never returns to the abandoned branch, and it costs far less than a [fully persistent array](/fully-persistent-array/).

## In plain words

Keep one real array on the table, for the latest state. Each time you change a cell, write a note on the old state: "I am the new state, except that cell $i$ was $x$". The old state is now just that note and a pointer to the new state.

To read an old state, follow its notes toward the table; the first note about your cell has the answer, and if there is none, read the table. To change an old state, go back to it: undo the notes from the newest one back to it, so the table holds that old state again. The states after it are thrown away, which is fine when you only ever go back, as in a search that tries a choice and then undoes it.

## The abstract type

The structure keeps versions of an array of $n$ slots. The operations on a version $v$ are `get(v, i)`, `set(v, i, x)` (which returns a new version), `to_list(v)` and `is_valid(v)`. The valid versions always form a path $v_0 \to v_1 \to \cdots \to v_k$ in the [version tree](/version-tree/), from the first version to the newest. `set` on $v_j$ makes $v_{j+1}, \ldots, v_k$ invalid and adds a new newest version after $v_j$. `get` does not change which versions are valid. Using an invalid version is an error, detected in $O(1)$.

So the structure gives the reads of [partial persistence](/partial-persistence/) to all valid versions, and lets the program go back and branch, as long as it never returns to a branch it has left.

## Representation

There is one shared array $A$ of $n$ slots. A version is a small record with a *kind* field:

- $\text{arr}$: this is the newest version, and its contents are $A$;
- $\text{diff}(i, x, w)$: this version equals version $w$ except that slot $i$ holds $x$;
- $\text{dead}$: this version is no longer valid.

**Invariant.** (I1) The valid versions are $v_0, \ldots, v_k$; $v_k$ has kind arr, and each $v_j$ with $j < k$ has kind $\text{diff}(i_j, x_j, v_{j+1})$. (I2) The contents of $v_k$ are $A$, and the contents of $v_j$ are those of $v_{j+1}$ with slot $i_j$ set to $x_j$. (I3) Every other version that the program holds has kind dead.

## Operations

```pseudo id=main
GET(v, i)
L1  if v.kind = dead then error "invalid version"
L2  t ← v
L3  while t.kind = diff do
L4      if t.i = i then return t.x
L5      t ← t.next
L6  return A[i]

SET(v, i, x)                                 ▷ new newest version: v with slot i set to x
L7  REROOT(v)
L8  w ← a new version of kind arr
L9  v.kind ← diff(i, A[i], w)                ▷ v remembers the old value of slot i
L10 A[i] ← x; return w

REROOT(v)                                    ▷ make v the newest version
L11 if v.kind = dead then error "invalid version"
L12 collect the path v = t_0, t_1, ..., t_m, where t_m has kind arr
L13 for j ← m − 1 down to 0 do A[t_j.i] ← t_j.x
L14 for j ← 1 to m do t_j.kind ← dead
L15 v.kind ← arr
```

GET returns the value in the first diff on the path that names slot $i$; the diffs between $v$ and that point do not touch slot $i$. REROOT undoes the diffs from the newest end back to $v$, in that order, so the array goes through the contents of $t_{m-1}, t_{m-2}, \ldots, t_0$. The versions after $v$ are marked dead, and their diff records can be freed. All loops are iterative, so chains of any length are safe.

## Example

Start with $v_0 = [0, 0, 0, 0]$.

- $v_1 = \text{set}(v_0, 1, 5)$: $v_0$ becomes $\text{diff}(1, 0, v_1)$, $A = [0, 5, 0, 0]$.
- $v_2 = \text{set}(v_1, 3, 7)$: $v_1$ becomes $\text{diff}(3, 0, v_2)$, $A = [0, 5, 0, 7]$.
- $v_3 = \text{set}(v_2, 1, 9)$: $v_2$ becomes $\text{diff}(1, 5, v_3)$, $A = [0, 9, 0, 7]$.

Now $\text{get}(v_3, 1) = 9$ in one step. $\text{get}(v_1, 1)$ looks at $v_1$ (slot 3, no), then $v_2$ (slot 1, yes) and returns 5. $\text{get}(v_0, 1)$ stops at once at its own diff and returns 0. $\text{get}(v_2, 3)$ walks to $v_3$ and reads $A[3] = 7$.

**Going back.** $v_4 = \text{set}(v_1, 2, 4)$ first reroots to $v_1$: the path is $v_1, v_2, v_3$; line L13 undoes the diff of $v_2$ ($A[1] \gets 5$) and then that of $v_1$ ($A[3] \gets 0$), so $A = [0, 5, 0, 0]$, which is $v_1$. Line L14 marks $v_2$ and $v_3$ dead. Then $v_1$ becomes $\text{diff}(2, 0, v_4)$ and $A = [0, 5, 4, 0]$. The valid versions are now $v_0, v_1, v_4$, and a call on $v_3$ is an error.

## Correctness

Assume (I1) to (I3). GET walks $v_j, v_{j+1}, \ldots$; by (I2), slot $i$ of $v_j$ equals slot $i$ of $v_{j+1}$ unless $i_j = i$, in which case it is $x_j$. So the first diff with slot $i$ gives the answer, and if there is none, slot $i$ of $v_j$ equals slot $i$ of $v_k$, which is $A[i]$. For REROOT$(v_j)$, after the step for $t_{m-1}, \ldots, t_l$ the array holds the contents of $t_l$ by (I2), so at the end it holds those of $v_j$; marking the later versions dead restores (I1) to (I3) with $k = j$. SET then records the old value of slot $i$ in $v_j$ and writes the new one, which is (I2) for the new pair. Valid versions keep their contents throughout. The full proof is in the proofs folder.

## Complexity

| operation | time | new space |
|---|---|---|
| get on a version $d$ steps before the newest | $\Theta(1 + d)$ | none |
| set on a version $d$ steps before the newest | $\Theta(1 + d)$ | one record |
| set or get on the newest version | $\Theta(1)$ | one record or none |
| to_list | $\Theta(n + d)$ | $n$ |
| is_valid | $\Theta(1)$ | none |

**Space.** The array takes $n$ slots and each valid version one record, so $\Theta(n + k)$ for $k$ valid versions. Dead records are not reachable from valid versions and can be freed.

**Backtracking cost.** In a depth-first search that makes one set per step down and goes back up by using the version it saved, each set is on the newest version or on a version $d$ steps back, and the reroot costs $d$, which is the number of sets being undone. Each set is undone at most once, so the total time is linear in the number of sets, as with an [undo log](/undo-log/), but with the convenience of version values.

## Variants

- **Baker's fully persistent form.** Instead of marking the versions after $v$ dead, REROOT can reverse the diffs on the path: each $t_{j+1}$ becomes $\text{diff}$ to $t_j$ with the value that $t_j$ wrote. Then every version stays valid and the shape of the diff graph is the version tree; each access reroots to its version and costs the distance in the tree. This is [Baker's trick](/bakers-trick/), and it is the persistent array that Conchon and Filliâtre use for the [persistent union-find](/persistent-union-find/).
- **Reads without rerooting.** The reads above walk the diffs and leave the array as it is. Rerooting on each read instead makes repeated reads of one old version cost $O(1)$ after the first.
- **Cost-bounded variants.** A fully persistent array with $O(\log \log n)$ access to every version exists, by Dietz's method on the [fully persistent array](/fully-persistent-array/) page; a balanced tree with [path copying](/path-copying/) gives $O(\log n)$ to every version with no special access pattern.
- **Other semi-persistent structures.** Conchon and Filliâtre gave semi-persistent versions of lists and other structures, where the same restriction removes work that full persistence would need.

## When to use it

Use a semi-persistent array when a program goes back to earlier states but never returns to a state it abandoned, and most work is on the newest state: backtracking search, SAT and constraint solvers, and type inference with undo. Each step costs $O(1)$ like a plain array, and going back costs the work that is undone. If old states must stay usable after going back, use Baker's form with reversal, or a [persistent vector](/persistent-vector/). If many threads read old versions at once, avoid this structure: reads and updates of one shared array need locking.

## Pitfalls

- **Using an abandoned version.** After a set on an older version, the versions after it are gone. The implementation must check for this (L1, L11); without the check, a dead version reads wrong values silently.
- **Old reads are slow.** A read of a version far back costs its distance. A loop that reads an old version many times should reroot to it first, or copy it.
- **Recursion on long chains.** Diff chains can be as long as the number of updates. Recursive GET or REROOT overflows the stack; use loops.
- **Not thread safe.** Updates and rerooting write to the shared array and to version records, so concurrent use needs a lock, unlike a purely functional array.
- **Order in REROOT.** The diffs must be undone from the newest end back to $v$. Undoing them in the other order is wrong when two diffs name the same slot.

## Implementations

## History

Henry Baker described functional arrays as one real array plus chains of diffs in 1991, building on his shallow binding technique for Lisp environments; with rerooting on access, every version stays usable. Sylvain Conchon and Jean-Christophe Filliâtre used such arrays in 2007 to build a persistent union-find for the Coq and Ergo provers, and in 2008 they defined semi-persistence, the case in which only ancestors of the newest version are used, and showed that the restriction makes the structures simpler and faster.

## References
