---
tag: ZNZ7PD
kind: technique
slug: bakers-trick
name: Baker's trick
aliases:
- Baker's rerooting
- rerooting
- reversal of diffs
area: data-structures/persistent-structures
level: advanced
summary: Keep one version as a real array and the others as chains of diffs to it; before a version is used, reverse the diffs on the path so that it holds the real array.
prereqs: [array, full-persistence]
see_also: [fully-persistent-array, persistent-union-find, semi-persistent-array, fat-node, path-copying, version-tree, persistent-vector, union-find-with-rollback]
sources:
  - paper: doi:10.1145/359545.359566
    title: Henry G. Baker, Shallow binding in Lisp 1.5, Communications of the ACM 21(7), 1978
    locator: pages 565 to 569 (rerooting the tree of variable bindings so that the current environment is at the root)
  - paper: doi:10.1145/122598.122614
    title: Henry G. Baker, Shallow binding makes functional arrays fast, ACM SIGPLAN Notices 26(8), 1991
    locator: pages 145 to 147 (functional arrays as a real array plus a tree of diffs, rerooted on access)
  - paper: doi:10.1145/1292535.1292541
    title: Sylvain Conchon and Jean-Christophe Filliâtre, A persistent union-find data structure, Proceedings of the 2007 ACM SIGPLAN Workshop on ML
    locator: pages 37 to 46, the section on persistent arrays (the reroot function, and its use for union-find)
---

Baker's trick makes an [array](/array/) [fully persistent](/full-persistence/) with no copying when the versions are used one after another. Exactly one version holds the real array. Every other version is a *diff*: a record "this version equals the version that I point to, except that cell $i$ holds $v$". Before a version is read or written, the diffs on the path from it to the real array are reversed, one by one, so that the version in use holds the array and the others point toward it. Access to the version in use costs $O(1)$, and a switch to another version costs the length of the path between them. Henry Baker used the idea in 1978 for the shallow binding of variables in Lisp and in 1991 for functional arrays. Conchon and Filliâtre used it to build a [persistent union-find](/persistent-union-find/) structure.

## In plain words

Keep one real copy of a big table. Each other version is a small note: "same as that version over there, but row 5 says 7". To look at a version that is a note, follow the notes to the real table, and on the way back, fix the table so that it matches the version you want. Each note you pass is turned around: it now describes the table as it was before you fixed it. In the end, the version you want is the real table, and every other version is again a chain of notes that leads to it.

If you keep working on the newest version, the table is always right where you are, and every step is quick. Jumping far back and forth is what costs time.

## When it applies

- **An array or another mutable structure with cheap inverse updates.** A diff must be reversible in $O(1)$ time: the write $a[i] \leftarrow v$ is undone by writing the old value back.
- **Single-threaded or backtracking use.** The cost is low when most operations apply to the version used last, or to a version close to it in the [version tree](/version-tree/). Backtracking search, which goes forward and then returns to an ancestor, is a good case.
- **The interface must be persistent.** The trick hides mutation behind a persistent interface, so code can keep old versions safely, and only pays when it actually uses them.

## The template

A version $t$ is a mutable reference whose contents are either $\text{Arr}(a)$, the real array, or $\text{Diff}(i, v, t')$, which means "version $t'$ with cell $i$ set to $v$".

```pseudo id=main
REROOT(t)                                ▷ afterwards t holds Arr(a)
L1  if t holds Diff(i, v, t′) then
L2      REROOT(t′)                       ▷ now t′ holds Arr(a)
L3      a ← the array of t′
L4      t′ ← Diff(i, a[i], t); a[i] ← v  ▷ reverse the diff
L5      t ← Arr(a)

GET(t, i)
L6  REROOT(t)
L7  return a[i], where t holds Arr(a)

SET(t, i, v)                             ▷ returns a new version
L8  REROOT(t)
L9  a ← the array of t
L10 r ← a new reference holding Arr(a)
L11 t ← Diff(i, a[i], r); a[i] ← v
L12 return r
```

Line L4 is the heart of the trick. Before it, $t'$ is the real array and $t$ is "$t'$ with $a[i] = v$". After it, $t$ is the real array, with $a[i] = v$, and $t'$ is "$t$ with the old value of $a[i]$". Both versions still describe the same contents. Line L11 does the same for a new version $r$: the old version $t$ becomes a diff toward $r$.

**Why it is correct.** Write $\text{val}(t)$ for the array that version $t$ describes: $a$ if $t$ holds $\text{Arr}(a)$, and $\text{val}(t')$ with cell $i$ replaced by $v$ if $t$ holds $\text{Diff}(i, v, t')$. The references form a tree whose root is the one holding the array, with each diff pointing to its parent. Line L4 changes the contents of $t'$, of $t$ and of the array, but in such a way that $\text{val}(t)$ and $\text{val}(t')$ stay the same, and all other versions point to $t$ or $t'$ or to a version that does, so their values do not change either. By induction on the length of the path, REROOT$(t)$ leaves every value unchanged and makes $t$ the root. So GET returns the cell of $\text{val}(t)$. SET makes $r$ the root with $\text{val}(r) = \text{val}(t)$ with cell $i$ set to $v$, and keeps $\text{val}(t)$.

**Cost.** REROOT takes $O(1 + \ell)$ time, where $\ell$ is the number of diffs between $t$ and the root, and needs no extra space. So GET and SET take $O(1)$ time when $t$ is the version used last, and $O(1)$ time per step back for a backtracking search that returns along its path. A version that is not used again costs one diff record, $O(1)$ space. In the worst case, alternating between two versions $\ell$ apart costs $\Theta(\ell)$ per access.

## Classic examples

### A trace

Let $v_0$ hold the array $[0, 0, 0]$, with indices 0 to 2.

| step | operation | contents afterwards |
|---|---|---|
| 1 | $v_1 \leftarrow \text{SET}(v_0, 1, 5)$ | $v_1 = \text{Arr}[0, 5, 0]$, $v_0 = \text{Diff}(1, 0, v_1)$ |
| 2 | $v_2 \leftarrow \text{SET}(v_1, 2, 7)$ | $v_2 = \text{Arr}[0, 5, 7]$, $v_1 = \text{Diff}(2, 0, v_2)$, $v_0 = \text{Diff}(1, 0, v_1)$ |
| 3 | $\text{GET}(v_0, 1)$, the reroot of $v_1$ | $v_1 = \text{Arr}[0, 5, 0]$, $v_2 = \text{Diff}(2, 7, v_1)$ |
| 4 | the reroot of $v_0$, then return 0 | $v_0 = \text{Arr}[0, 0, 0]$, $v_1 = \text{Diff}(1, 5, v_0)$, $v_2 = \text{Diff}(2, 7, v_1)$ |
| 5 | $v_3 \leftarrow \text{SET}(v_0, 0, 9)$ | $v_3 = \text{Arr}[9, 0, 0]$, $v_0 = \text{Diff}(0, 0, v_3)$ |

After step 5 the version tree has the edges $v_0 \to v_1$, $v_1 \to v_2$ and $v_0 \to v_3$, and all four versions are still correct: $v_2$ reads $[0, 5, 7]$ by following $v_2 \to v_1 \to v_0 \to v_3$ and undoing the diffs. The diffs point toward the version used last, not toward the newest one.

### Other examples

- **Shallow binding in Lisp.** The environment of variable bindings is a tree. The values of the current environment sit in the value cells of the symbols, and a switch of environment reroots the tree, which is the setting of Baker's 1978 paper.
- **Persistent union-find.** Conchon and Filliâtre keep the parent and rank arrays of a [disjoint-set](/disjoint-set/) forest as persistent arrays with rerooting. Path compression writes to the array of the version in use. In a backtracking program, such as a type checker or a SAT solver, the versions are used in a stack-like order and the operations stay fast.
- **Semi-persistent arrays.** If an update may only apply to the version in use or to one of its ancestors, the diffs toward the descendants that are given up need not be kept; see [semi-persistent array](/semi-persistent-array/).
- **Trails in backtracking.** A trail of old values, which a search undoes on backtracking, is the ephemeral form of the same idea; see [union-find with rollback](/union-find-with-rollback/).

## Variations

- **Copy on far access.** A version that is far from the root can be given its own copy of the array instead of rerooting, which bounds the cost of an access by $O(n)$ and keeps other versions fast. This trades space for a bound on the worst case.
- **Other structures.** Any structure whose updates have $O(1)$ inverses can be rerooted, such as a hash table with a diff per insertion, as long as the reversal of a diff is cheap.
- **Comparison with tree-based arrays.** A persistent array by [path copying](/path-copying/), such as a [persistent vector](/persistent-vector/), pays $O(\log n)$ for each access in every version, with no bad access pattern. Baker's trick pays $O(1)$ in the good case and the path length in the bad case. The [fat node](/fat-node/) method and Dietz's [fully persistent array](/fully-persistent-array/) bound every access by $O(\log m)$ or $O(\log \log m)$.

## Pitfalls

- **Reads mutate.** GET changes the shared array, so two threads that read two versions at once corrupt the structure. Use a lock, or give each thread its own copy.
- **Deep recursion.** REROOT recurses along the whole path, and a path of a million diffs overflows the call stack. Collect the path in a list first and reverse it in a loop.
- **Thrashing.** Alternating between two distant versions costs the full distance on every access. If the access pattern is not single-threaded, use a tree-based persistent array.
- **Forgetting to reroot before a write.** SET must reroot first. Writing into the array of another version changes that version silently.
- **Memory.** An old version is a small diff, but it keeps alive the versions on its path. Old versions that are dropped can be collected, since diffs point toward the root and the root does not point back to them.

## Exercises

1. Continue the trace: compute $\text{GET}(v_2, 2)$ after step 5 and give the contents of all versions afterwards.
2. Write an iterative REROOT that uses $O(1)$ extra space besides the path itself, and prove that it does the same changes as the recursive one.
3. Show that a sequence of $m$ operations in which each one applies to the result of the previous one takes $O(m)$ time in total.
4. Give a sequence of $2m$ operations on an array of size 1 that takes $\Theta(m^2)$ time with Baker's trick.

## References
