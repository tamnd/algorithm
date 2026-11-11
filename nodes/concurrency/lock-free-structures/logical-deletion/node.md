---
tag: 5CC8PY
kind: technique
slug: logical-deletion
name: Logical deletion (marked pointers)
aliases:
- mark bit
- marked pointers
area: concurrency/lock-free-structures
level: core
summary: Mark a node as deleted with a bit in its next pointer before physically unlinking it.
prereqs: [linked-list, compare-and-swap, linearizability]
see_also: [harris-linked-list, michael-hash-table, split-ordered-list, lock-free-skip-list, non-blocking-bst, tagged-pointers, hazard-pointers, lock-coupling]
sources:
  - paper: doi:10.1007/3-540-45414-4_21
    title: Timothy L. Harris, A pragmatic implementation of non-blocking linked-lists, DISC 2001, LNCS 2180, pages 300 to 314
    locator: the two-step delete (mark the next field of the node, then unlink it) and the runs that lose an insert or a delete without the mark
  - paper: doi:10.1145/564870.564881
    title: Maged M. Michael, High performance dynamic lock-free hash tables and list-based sets, SPAA 2002, pages 73 to 82
    locator: the list-based set in which a traversal unlinks each marked node it meets, one at a time, so that hazard pointers can free them
  - paper: doi:10.1007/11795490_3
    title: Steve Heller, Maurice Herlihy, Victor Luchangco, Mark Moir, William N. Scherer III and Nir Shavit, A lazy concurrent list-based set algorithm, OPODIS 2005, LNCS 3974, pages 3 to 16
    locator: the lazy list, with a marked field, locks on two nodes for each change, and a membership test with no locks
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: the chapter on linked lists (the role of locking), the sections on lazy synchronization and on the nonblocking list with AtomicMarkableReference
---

Logical deletion removes a node from a concurrent linked structure in two steps. First a process *marks* the node: it sets a bit that says "this node is deleted". From that step on, the node is not in the abstract set, although it is still linked. Then a process (the deleter or any other one) *unlinks* it with a [compare-and-swap](/compare-and-swap/) on the pointer that leads to it. The mark is usually kept in the low bit of the node's own `next` pointer, so that one CAS reads and changes the pointer and the mark together. This page explains the template, why the mark must share a word with the pointer, and the lazy list, which uses the same idea with locks.

## In plain words

To take a box out of a chain of boxes, you must change the box before it so that it points past the one you remove. If two people change the chain near the same place at the same time, one change can undo the other: a new box hung on a box that is being taken out falls out with it.

Logical deletion first puts a sticker on the box that leaves. The sticker means "this box is gone". Nobody may hang a new box on a box with a sticker, and the box that leaves keeps its own link fixed. After the sticker is on, anybody who walks past can cut the box out of the chain. The sticker must be part of the link itself, so that "is the box still good?" and "change its link" happen in one atomic step.

## When it applies

Use logical deletion when all of these hold.

- The structure is made of nodes linked by pointers, such as a [linked list](/linked-list/), a [skip list](/skip-list/), a hash table built on lists, or a [binary search tree](/binary-search-tree/).
- A delete must change a pointer in a node that is not the one it removes (the predecessor), while other processes may at the same time insert after the removed node or delete its neighbours.
- The changes are made with single-word CAS (or with locks, for the lazy list), and there is no atomic operation on two words such as [double compare-and-swap](/double-compare-and-swap/).

It is the base of most lock-free sets and maps: the [Harris list](/harris-linked-list/), the [Michael hash table](/michael-hash-table/), the [split-ordered list](/split-ordered-list/), the [lock-free skip list](/lock-free-skip-list/) and the [non-blocking BST](/non-blocking-bst/).

## The template

### Model and notation

We use the model of the other pages in this area: asynchronous processes that may stop at any time, atomic read, write and single-word CAS, [sequential consistency](/sequential-consistency/), and nodes that are not freed while a process can still reach them. The proof of the claims below is a sketch; the full invariants for one structure are in the proof of the [Harris list](/harris-linked-list/).

| Symbol | Meaning |
|---|---|
| `n.next` | the word that holds the successor of node `n` and its mark bit |
| `ptr(w)`, `marked(w)` | the pointer and the mark bit of a word `w` |
| `(p, b)` | the word with pointer `p` and mark bit `b` |
| `pred`, `curr`, `succ` | three nodes next to each other on a traversal |
| $S$ | the abstract set: the keys of the linked nodes that are not marked |

The rules of the template are these.

1. **Mark.** A delete of `curr` sets the mark bit of `curr.next` with one CAS from `(succ, false)` to `(succ, true)`. This CAS is the linearization point of a successful delete.
2. **Freeze.** A marked `next` field never changes again. Every CAS that writes a `next` field expects an unmarked value, so it fails on a marked one.
3. **Unlink.** A CAS on `pred.next` from `(curr, false)` to `(succ, false)` takes `curr` out. The deleter tries once; if it fails, a later traversal does it.
4. **Help.** A traversal that finds a marked `curr` unlinks it before it goes on, or restarts when its CAS fails. This is a small case of [helping](/helping/).
5. **Read.** A lookup walks with plain reads and answers from the mark of the node it stops at. It does not need to unlink anything.

The pseudocode is a sorted list set in the form of Michael's list (each traversal unlinks marked nodes one at a time). The Python file implements it with these line labels.

```pseudo id=main
DELETE(k)
L1  repeat
L2      (pred, curr) ← FIND(k)
L3      if curr.key ≠ k then return false
L4      (succ, m) ← curr.next; if m then continue
L5      if CAS(curr.next, (succ, false), (succ, true)) then exit the loop   ▷ logical deletion
L6  CAS(pred.next, (curr, false), (succ, false))                          ▷ physical deletion, one try
L7  return true

INSERT(k)
L8  repeat
L9      (pred, curr) ← FIND(k)
L10     if curr.key = k then return false
L11     make node n with key k and n.next ← (curr, false) (on a retry, only set n.next)
L12     if CAS(pred.next, (curr, false), (n, false)) then return true    ▷ fails if pred is marked

FIND(k)                                      ▷ returns pred, curr with pred.key < k ≤ curr.key, both seen unmarked
L13 pred ← head; curr ← ptr(head.next)
L14 loop
L15     (succ, m) ← curr.next
L16     if m then                            ▷ curr is logically deleted: help unlink it
L17         if not CAS(pred.next, (curr, false), (succ, false)) then go to L13
L18         curr ← succ
L19     else if curr.key ≥ k then return (pred, curr)
L20     else pred ← curr; curr ← succ

CONTAINS(k)                                  ▷ only reads; never helps
L21 curr ← head; while curr.key < k do curr ← ptr(curr.next)
L22 return curr.key = k and not marked(curr.next)
```

The CAS at L12 is where the shared word matters. It expects `pred.next` to be `(curr, false)`. If a delete marked `pred` after FIND returned, the word is now `(curr, true)`, the CAS fails, and the insert tries again. The new node is never hung on a node that has left the set.

### Why the mark must share a word with the pointer

Suppose the mark is a separate field `pred.marked`. An insert must then check two words: it reads `pred.marked` and then does its CAS on `pred.next`. These are two steps, and a delete can run between them. The list is `head` → 1 → 3, and insert(2) and delete(1) run at the same time.

1. insert(2) finds `pred` = 1 and `curr` = 3, and reads `1.marked` = false.
2. delete(1) sets `1.marked` and swings `head.next` from 1 to 3. It returns true.
3. insert(2) does its CAS on `1.next` from 3 to the new node. The CAS succeeds, because `1.next` did not change. It returns true.

Node 2 hangs from node 1, which no traversal from `head` reaches, so a later contains(2) returns false. No order of the operations explains that, so the run is not [linearizable](/linearizability/). The test `test_separate_mark_field_loses_an_insert` finds this run by search and replays it; with the mark in the word, the same schedule makes the CAS at step 3 fail.

The same race breaks the delete side. If the mark is separate, a process can insert after `curr` once `curr` is marked, and the unlink at L6 then uses a stale `succ` and drops the new node. With the mark in `curr.next`, the mark freezes `curr.next`, so the `succ` that the unlink installs is the true successor.

There are three ways to check the mark and change the pointer in one atomic step.

- Put the mark in the low bit of the pointer. Nodes are aligned to at least two bytes, so the low bit of a real address is always zero. This is the usual method in C and C++; see [tagged pointers](/tagged-pointers/).
- Put the pair in an object and swap the object, as Java's `AtomicMarkableReference` does. This costs an allocation for each change of the pair.
- Change both words at once with [double compare-and-swap](/double-compare-and-swap/) or [multi-word CAS](/multi-word-cas/), or hold locks on both nodes, as the lazy list does.

### Why it is correct (sketch)

Three facts carry the proof. A marked `next` field never changes (rule 2). A node is unlinked only after it is marked, because the CAS at L6 and L17 removes only a node whose `next` it read as marked, and that mark is final. So every linked node that is not marked is reachable from `head`, and $S$ can be read off the list. A successful insert links its node at L12 between `pred` and `curr` while `pred` is unmarked and points to `curr`, so the node goes into the reachable list. A successful delete changes $S$ at its mark (L5), and nothing else changes $S$. The full argument, with the linearization points of failed operations, is on the [Harris list](/harris-linked-list/) page.

Progress is lock-free: a CAS fails only because another CAS on the same word succeeded, and each successful CAS is a link, a mark or an unlink, of which there are only finitely many per completed operation. CONTAINS never retries. Along any walk the keys strictly increase, even through marked nodes, so with a finite key space CONTAINS takes a bounded number of steps and is wait-free.

### The lazy list

The lazy list of Heller, Herlihy, Luchangco, Moir, Scherer and Shavit uses the same two steps with locks in place of CAS. Each node has a lock and a separate `marked` field.

- Add and remove walk the list with no locks, lock `pred` and `curr`, and then *validate*: both are unmarked and `pred.next = curr`. If the check fails, they unlock and start again.
- Remove sets `curr.marked` (the logical deletion) and then sets `pred.next` to `curr.next` (the physical deletion), both while it holds the two locks.
- Contains takes no lock. It walks the list and returns true only if it finds the key in an unmarked node.

Here a separate `marked` field is safe, because each writer changes `pred.next` only while it holds the lock of `pred` and has seen `pred` unmarked under that lock; a remover of `pred` needs the same lock. Updates are blocking, but contains is wait-free. One subtle point is the linearization point of a contains that returns false: it may be a time before the contains read the mark, for example just before a concurrent add of the same key. The class `LazyList` in the Python file implements the lazy list with spin locks, and the tests check it for linearizability.

### Memory reclamation

A node that has been unlinked may still be in use: a traversal can stand on it and read its `next`. The marked `next` of an unlinked node still leads back into the list, which is why such a traversal stays correct. So the node cannot be freed at the unlink. It needs [hazard pointers](/hazard-pointers/), [epoch-based reclamation](/epoch-based-reclamation/) or another safe scheme. If the node is freed and reused at once, a slow traversal follows a pointer into the new node, and a CAS that expects `(curr, false)` can succeed on the reused address (the [ABA problem](/aba-problem/)). Michael's form of the list unlinks one marked node at a time and restarts on a failed CAS, which is what hazard pointers need; Harris's original form unlinks a whole chain of marked nodes with one CAS, which works with epochs but not with plain hazard pointers.

## Classic examples

- **The Harris list.** Harris (2001) introduced the mark in the low bit of `next` for a lock-free sorted list. His search unlinks a chain of marked nodes with one CAS. See [Harris lock-free linked list](/harris-linked-list/).
- **Michael's list and hash table.** Michael (2002) changed the search to unlink one node at a time, so that the list works with hazard pointers, and used one such list for each bucket of a [hash table](/michael-hash-table/).
- **The split-ordered list.** Shalev and Shavit build a resizable hash table on one marked-pointer list in bit-reversed key order. See [split-ordered list](/split-ordered-list/).
- **Lock-free skip lists.** Fraser, and later Herlihy, Lev, Luchangco and Shavit, mark the `next` pointer at every level of a tower, from the top down, and take the mark at the bottom level as the linearization point. See [lock-free skip list](/lock-free-skip-list/).
- **The non-blocking BST.** Ellen, Fatourou, Ruppert and van Breugel mark a node in a status field that holds a pointer to an operation record, and flag its parent before they unlink it. See [non-blocking BST](/non-blocking-bst/).
- **The lazy list.** The lock-based use described above. It is a common base for lock-based concurrent sets, and the membership test with no locks is its main gain over [lock coupling](/lock-coupling/).

## Variations

- **Marker nodes.** Java has no spare bit in a reference. Doug Lea's `ConcurrentSkipListMap` in `java.util.concurrent` deletes a node by first setting its value to null and then appending a special marker node after it with a CAS. The marker plays the role of the mark bit: no insert can go between the node and the marker.
- **Flag the predecessor.** Fomitchev and Ruppert (2004) also *flag* the predecessor before they mark the node, and add a back link from the marked node to its predecessor. A process that fails a CAS follows back links in place of a restart from `head`, which gives a better amortized bound.
- **Mark edges, not nodes.** Natarajan and Mittal (2014) put a flag bit and a tag bit on the child pointers of an external BST, so that a delete marks edges and needs no operation records.
- **Mark only.** Some structures never unlink at once: they leave marked nodes in place and remove them in a batch, for example when a bucket of a hash table is rebuilt. Lookups must then skip marked nodes, and their cost grows with the number of marked nodes.
- **Logical deletion in a value.** In a map, a delete can set the value field to a special "deleted" value with one CAS. This is the same idea when the key never moves; the node is unlinked later or never.

## Pitfalls

- **A separate mark field with CAS.** As shown above, a read of the mark and a CAS on the pointer are two steps, and an insert is lost between them. The mark must be in the word that the CAS changes, or both words must be changed under a lock or with a multi-word operation.
- **A CAS that ignores the mark.** Every CAS on a `next` field must expect the unmarked form of the old value. A CAS that compares only the pointer part (after masking off the bit) can write into a marked node and lose the write.
- **Reading a marked pointer as an address.** In C, a process must clear the low bit before it follows a pointer. A missing mask follows an odd address.
- **Freeing at the unlink.** An unlinked node is still reachable from processes that stand on it. Free it only through a reclamation scheme.
- **A delete that returns before its mark is visible.** On hardware with weak memory order, the mark CAS must be at least a release operation, and the read of `next` in a traversal must be an acquire load, so that a process that sees the mark also sees the state before it. A sequentially consistent CAS, as in the C++ default, is enough.
- **A contains that helps.** Making contains unlink marked nodes turns a read-only, wait-free operation into one that writes and can retry. Michael's lookup does unlink, for the sake of hazard pointers; the AMP list's contains does not.

## Exercises

1. In the list `head` → 1 → 2 → 3, delete(1) and delete(2) run at the same time on a list that unlinks with one CAS and never marks. Give a schedule in which both return true and 2 stays in the list. Show that the mark at L5 prevents it.
2. Prove that once `curr.next` is marked, the `succ` that L6 installs is the successor of `curr` at the time of the unlink.
3. In the lazy list, why must the validation check that `pred` is unmarked, and not only that `pred.next = curr`? Give a run that goes wrong without it.
4. Give the linearization point of a contains(k) of the lazy list that returns false, when an add(k) runs at the same time and its new node is linked after the contains passed the place where it goes.
5. Explain why Harris's search, which unlinks a chain of marked nodes with one CAS, cannot protect the nodes of the chain with a fixed number of hazard pointers.

## References
