---
tag: CQ32KC
kind: data-structure
slug: harris-linked-list
name: Harris lock-free linked list
aliases:
- Harris list
- Harris-Michael list
- Michael list
- lock-free linked list
area: concurrency/lock-free-structures
level: core
summary: Sorted lock-free linked list using logical deletion marks followed by physical unlinking.
implements: [ordered-set]
complexity:
  vars: {n: "the number of nodes in the list, including marked nodes"}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [linked-list, compare-and-swap, linearizability, lock-freedom]
see_also: [logical-deletion, michael-hash-table, split-ordered-list, lock-free-skip-list, hazard-pointers, epoch-based-reclamation, lock-coupling, treiber-stack]
sources:
  - paper: doi:10.1007/3-540-45414-4_21
    title: Timothy L. Harris, A pragmatic implementation of non-blocking linked-lists, DISC 2001, LNCS 2180, pages 300 to 314
    locator: the search with its three phases, insert, delete with the mark bit in the next field, and the argument for linearizability
  - paper: doi:10.1145/564870.564881
    title: Maged M. Michael, High performance dynamic lock-free hash tables and list-based sets, SPAA 2002, pages 73 to 82
    locator: the list-based set that removes one marked node at a time, so that it works with hazard pointers and other memory reclamation methods
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, 2020
    locator: the chapter on linked lists (the role of locking), the section on the lock-free list with AtomicMarkableReference
---

The Harris list is a sorted [linked list](/linked-list/) that many processes can change at the same time with no locks. Timothy Harris published it in 2001. It implements a set of keys with insert, delete and find. Its main idea is [logical deletion](/logical-deletion/): to delete a node, a process first sets a *mark bit* in the node's own `next` pointer, with one [compare-and-swap](/compare-and-swap/), and only then unlinks the node from its predecessor with a second CAS. A marked node can never get a new successor, so no insert can be lost behind it. Any process that walks past a marked node may unlink it. The list is [lock-free](/lock-freedom/) and [linearizable](/linearizability/), and it is the building block of lock-free hash tables and skip lists.

## In plain words

Think of a line of people, each holding the shoulder of the next one, sorted by height. To join, a person finds the right gap and the one in front grabs their shoulder.

To leave, a person first puts on a red hat. A person with a red hat must not let anyone new hold on behind them. Then the one in front lets go of the red hat and grabs the next person. If that fails because the line changed, whoever walks by later does the job. Without the hat, someone could join right behind a person who is leaving at that moment, and leave with them by mistake.

## The abstract type

The list implements a set of keys (an [ordered set](/ordered-set/) without range queries): insert$(k)$ adds $k$ and returns true, or returns false if $k$ is already there; delete$(k)$ removes $k$ and returns true, or returns false; find$(k)$ returns whether $k$ is in the set. Any number of processes may call any operation. The safety condition is [linearizability](/linearizability/) with respect to this sequential set.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $k$ | a key; keys are integers and lie strictly between $-\infty$ and $+\infty$ |
| $n$ | the number of nodes in the list, marked or not |
| `head`, `tail` | sentinel nodes with keys $-\infty$ and $+\infty$ |
| `x.next` | a *marked pointer*: a pointer and a mark bit in one word |
| marked$(x)$ | the mark bit of `x.next` is set: $x$ is logically deleted |

The processes are asynchronous and may crash between any two steps. They use atomic read, write and single-word [compare-and-swap](/compare-and-swap/); a CAS on `x.next` compares and swaps the pointer and the mark together. The proofs assume sequential consistency. Nodes are never freed or reused; the paper assumes a garbage collector, and the section on memory reclamation says what changes without one.

### Fields

- Each node has a key, which never changes, and `next`, a marked pointer.
- `head.next` starts as `tail`. `head` and `tail` are never marked or removed.

**Invariant.** (1) The nodes reachable from `head` have strictly increasing keys, from $-\infty$ to $+\infty$. (2) Once a node is marked, its `next` field never changes again. (3) Every node that was linked and is not marked is reachable from `head`. The set is the keys of the reachable unmarked nodes.

## Operations

```pseudo id=main
SEARCH(k)                                   ▷ returns adjacent left, right with left.key < k ≤ right.key
L1  t ← head; tNext ← head.next
L2  repeat                                  ▷ phase 1: walk to the first unmarked node with key ≥ k
L3      if not marked(tNext) then left ← t; leftNext ← tNext
        t ← ptr(tNext)
        if t = tail then exit the loop
L4      tNext ← t.next
L5  until not marked(tNext) and t.key ≥ k
    right ← t
L6  if leftNext = right then                ▷ phase 2: already adjacent
L7      if right ≠ tail and marked(right.next) then go to L1
        return (left, right)
L8  if CAS(left.next, leftNext, right) then ▷ phase 3: unlink the chain of marked nodes
L9      if right ≠ tail and marked(right.next) then go to L1
        return (left, right)
    go to L1

INSERT(k)
L10 (left, right) ← SEARCH(k)
L11 if right.key = k then return false
L12 make node n with key k and n.next ← right (on a retry, only set n.next)
L13 if CAS(left.next, right, n) then return true else go to L10

DELETE(k)
L14 (left, right) ← SEARCH(k)
L15 if right.key ≠ k then return false
L16 rNext ← right.next; if marked(rNext) then go to L14
L17 if not CAS(right.next, rNext, marked rNext) then go to L14   ▷ logical delete
L18 if not CAS(left.next, right, rNext) then SEARCH(k)            ▷ physical delete, or let SEARCH do it
L19 return true

FIND(k)
L20 (left, right) ← SEARCH(k)
L21 return right.key = k
```

In a CAS on a `next` field, an expected value written as a plain pointer means the pointer with the mark bit clear. So the CAS at L8, L13 and L18 fails if `left` was marked in the meantime.

**Why the mark is needed.** In a naive list, delete would unlink $x$ with one CAS on its predecessor. Suppose the list is `head` → 1 → 3, a process deletes 1, and another inserts 2. The deleter swings `head.next` from 1 to 3; the inserter swings `1.next` from 3 to 2. Both CAS operations succeed, because each one touches a different word, and 2 hangs off a node that is no longer in the list: the insert is lost. In the Harris list, the deleter first marks `1.next`. Then the inserter's CAS on `1.next`, which expects an unmarked pointer, fails, and the inserter searches again.

**Snipping.** The search remembers the last unmarked node `left` before a run of marked nodes, and unlinks the whole run with one CAS at L8. The search ends only when `left` and `right` were adjacent and `right` was unmarked, so insert and delete always work on a clean pair.

**Linearization points.** A successful insert at its CAS at L13. A successful delete at its mark at L17; the key leaves the set then, even if the node is unlinked later. An insert that returns false, and a find that returns true, at the last read of `right.next` in the search that saw it unmarked (L7 or L9, or L4 when `right` is the node just read). A delete that returns false, and a find that returns false, at the time when `left.next` was `right`, unmarked: the read that gave `leftNext` in phase 2, or the CAS at L8 in phase 3.

### Memory reclamation

Harris assumes a garbage collector. In C or C++, a node that has been unlinked cannot be freed at once: other searches may still stand on it or be about to read its `next`. If it is freed and its memory reused, a search reads garbage, and a CAS on `left.next` may succeed against a new node at the same address, the [ABA problem](/aba-problem/). [Epoch-based reclamation](/epoch-based-reclamation/) works with the Harris list as it is. [Hazard pointers](/hazard-pointers/) do not work directly with the snipping search, because the search walks along chains of marked nodes that may already be unlinked, and a hazard pointer on such a node cannot be checked against its predecessor. Michael's list (2002) fixes this: its search unlinks each marked node as soon as it meets it, one CAS per node, and starts again from `head` when that CAS fails. Every node it visits was reachable when it protected it, so hazard pointers work. That version is called the Harris-Michael list, and it is the one inside the [Michael hash table](/michael-hash-table/).

### Weak memory

The read of a `next` field must be an acquire load, and the CAS that links a new node at L13 must be a release (or stronger), so that a process that sees the new node also sees its key and its `next`. The marks need nothing extra, because they live in the same word as the pointer and change with it. In C++ the usual choice is sequentially consistent CAS steps and acquire loads.

## Example

The list holds 1, 2, 3. Process $p$ calls delete(2), and process $q$ calls insert(4) and then find(2).

| step | process | action | list |
|---|---|---|---|
| 1 | $p$ | search(2): left = 1, right = 2 | 1, 2, 3 |
| 2 | $p$ | L17: marks `2.next` | 1, 2 (marked), 3 |
| 3 | $p$ | stops before L18 | |
| 4 | $q$ | search(4): passes 2 (marked) and 3; left = 3, right = `tail`; adjacent | |
| 5 | $q$ | L13: CAS `3.next` from `tail` to 4 | 1, 2 (marked), 3, 4 |
| 6 | $q$ | search(2): left = 1, `leftNext` = 2, right = 3; not adjacent | |
| 7 | $q$ | L8: CAS `1.next` from 2 to 3 unlinks 2 | 1, 3, 4 |
| 8 | $q$ | find returns false | |

$q$ finishes although $p$ stopped in the middle of its delete: $q$'s search did $p$'s unlink. When $p$ runs again, its CAS at L18 fails (`1.next` is no longer 2), it calls search, and it returns true. The test `test_others_finish_when_a_deleter_stops_after_marking` runs this kind of schedule, and `test_naive_list_loses_an_insert` runs the lost insert of the naive list.

## Correctness

**Safety.** The three parts of the invariant carry the proof. A CAS that links a node (L13) or unlinks nodes (L8, L18) expects an unmarked `left.next`, so it never changes the `next` field of a marked node; that is part (2). An unlink removes only marked nodes: at L8 the run between `left` and `right` was marked when it was read, and by part (2) it is still the same run; at L18 `right` is marked by this process. So no unmarked node leaves the list, which is part (3). An insert links $n$ between `left` and `right` only if `left.next` is still `right`, unmarked, so the order is kept; that is part (1). With these, the set is the keys of the unmarked nodes, an insert adds its key at L13, a delete removes it at L17, and the reads at the other points see a state in which the result is right. The proof file has the details. The tests check linearizability on all interleavings of six small cases, and on 100 seeded runs.

**Progress.** The list is lock-free: a search or an update starts again only when a CAS fails or a mark appears, and each of these means that another process made a successful CAS that changed the list, and each change either links a node or marks or unlinks a marked node, which can happen only a bounded number of times per completed operation. It is not wait-free: one insert can lose its CAS for ever while others keep inserting at the same place.

## Complexity

| case | steps of one operation |
|---|---|
| alone, find or insert | at most $n + 4$ |
| alone, delete | at most $n + 6$ |
| with contention | unbounded (lock-free, not wait-free) |

The solo bounds are measured on lists of up to 16 unmarked nodes; the search reads the `next` field of each node on its way once. Marked nodes count in $n$ until someone unlinks them. Under contention, the cost of an operation includes restarts from `head`, each up to $n$ steps. Fomitchev and Ruppert (2004) added back links to the list, so that a process can step back instead of starting again, and proved amortized bounds; the Harris list has no such bound. The space is one node per key plus marked nodes that have not been reclaimed.

## Variants

- **The Michael list (2002).** Unlinks each marked node it meets, one by one, and restarts on a failed CAS. Slightly more CAS steps, but it works with [hazard pointers](/hazard-pointers/). The aliases "Harris-Michael list" and "Michael list" name this version; the logic of the mark and of the two-step delete is the same.
- **[Logical deletion](/logical-deletion/) with locks: the lazy list** (Heller et al. 2005). Uses the same mark, but locks two nodes to change them; finds take no locks and never write.
- **Wait-free find.** A find can walk the list without unlinking anything, and decide by the mark of the node it stops at. This is the find of the lazy list and of later lock-free lists.
- **Ordered structures built on it.** The [Michael hash table](/michael-hash-table/) uses one list per bucket; the [split-ordered list](/split-ordered-list/) uses one list for the whole table; the [lock-free skip list](/lock-free-skip-list/) uses one list per level.

## When to use it

Use it as a concurrent sorted set when the set is small, or as a part of a bigger structure (hash buckets, skip list levels). It is simple and fast when operations spread over the list. For large sets alone it is slow, because every operation walks $\Theta(n)$ nodes; use a hash table or a skip list built on it. Without a garbage collector, pick a reclamation scheme first, since it decides between the Harris version and the Michael version.

## Pitfalls

- **Keeping the mark in a separate field.** The mark must be in the same word as the pointer, so that one CAS checks both. If it lives in a field of its own, an insert can read "unmarked", the delete then marks and unlinks, and the insert's CAS on `next` still succeeds: the lost insert again.
- **Freeing an unlinked node at once** with no reclamation scheme: a concurrent search may still use it.
- **Hazard pointers with the snipping search.** They need the Michael version.
- **Forgetting that delete takes effect at the mark.** A find that sees a marked node with the key must return false, even though the node is still in the list.
- **Restarting from the last good node instead of `head`.** That node may be marked and unlinked by now; Harris and Michael restart from `head`.

## Implementations

## History

Valois (1995) gave an earlier lock-free list, with auxiliary nodes between the real ones and reference counts, which was complex and slow. Harris (2001) found the simpler scheme with the mark in the `next` pointer, while an intern at Sun Labs. Michael (2002) changed the search so that the list works with hazard pointers and used it for a lock-free hash table. Heller, Herlihy, Luchangco, Moir, Scherer and Shavit (2005) used the same mark in the lazy list with locks. Fomitchev and Ruppert (2004) added back links and proved amortized bounds. The mark-then-unlink pattern is now the standard way to delete from a lock-free linked structure.

## References
