---
tag: R4MGVH
kind: data-structure
slug: bw-tree
name: Bw-tree
aliases:
- latch-free B-tree with delta records
area: databases/storage-and-indexing
level: research
summary: "A latch-free B+ tree that changes pages by prepending delta records and installs them with compare-and-swap on a mapping table."
model: word-ram
complexity:
  vars: {n: the number of keys, h: the height of the tree, c: the largest length of a delta chain, B: the largest number of entries in a page}
  time: {worst: "O(h (c + log B))", average: "O(h (c + log B))", best: "O(h)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, external: false, online: true, in_place: false, recursive: false}
history:
  year: 2013
  people: [Justin J. Levandoski, David B. Lomet, Sudipta Sengupta]
  note: "Levandoski, Lomet and Sengupta of Microsoft Research presented the Bw-tree at ICDE 2013, as a B+ tree for multicore processors and flash storage that never takes a latch."
prereqs: [b-plus-tree, compare-and-swap, blink-tree]
see_also: [linearizability, lock-freedom, epoch-based-reclamation, aba-problem, log-structured-merge-tree, adaptive-radix-tree, non-blocking-algorithm, read-copy-update]
sources:
  - paper: doi:10.1109/ICDE.2013.6544834
    title: "Justin J. Levandoski, David B. Lomet and Sudipta Sengupta, The Bw-Tree: a B-tree for new hardware platforms, Proceedings of the 29th IEEE International Conference on Data Engineering (ICDE 2013)"
    locator: pp. 302 to 313, the mapping table, delta updates, consolidation, the two-step split with an index term delta, merges, epoch-based memory reclamation and the flash log
  - paper: doi:10.1145/3183713.3196895
    title: "Ziqi Wang, Andrew Pavlo, Hyeontaek Lim, Viktor Leis, Huanchen Zhang, Michael Kaminsky and David G. Andersen, Building a Bw-Tree takes more than just buzz words, Proceedings of ACM SIGMOD 2018"
    locator: pp. 473 to 488, the OpenBw-Tree, its missing details and optimizations, and the comparison with other in-memory indexes
---

The Bw-tree is a [B+ tree](/b-plus-tree/) in which no thread ever takes a latch. Pages do not refer to each other by memory addresses but by *page ids*, and a *mapping table* maps each page id to the current address of the page. A thread never changes a page in place. It makes a small *delta record* that describes the change, points it at the current page, and installs it with one [compare-and-swap](/compare-and-swap/) on the slot of the page in the mapping table. Long chains of deltas are later merged into a new page, and splits are done in two steps, each one compare-and-swap, in the style of the [B-link tree](/blink-tree/). The operations are linearizable and the structure is lock-free (a theorem, under the invariant of the proof); its speed is a measurement.

## In plain words

Think of a shared notebook in which nobody may erase anything. To change an entry, you write the change on a sticky note, stick it on top of the page, and point the table of contents at your note. If somebody else changed that entry of the table while you wrote, your change fails and you try again. A reader reads the notes first, newest first, and then the page under them.

When a page has too many notes, somebody copies it out clean and points the table at the copy. When a page gets too full, somebody moves its upper half to a new page and puts a note "the keys from 35 on are now on page 3" on the old page. Anybody who sees that note can later add the new page to the index above.

## The abstract type

A map from ordered keys to values, used by many threads at the same time:

- `lookup(k)`: the value of $k$, or nothing.
- `upsert(k, v)`: insert $k$ with $v$, or replace its value.
- `delete(k)`.
- Range scans along the leaf level.

Each operation is [linearizable](/linearizability/): it acts as if it took place at one instant between its start and its end.

## Representation

- **Mapping table.** An array $M$ from page ids (pids) to the head of a page. Every change of the tree is a compare-and-swap (CAS) on one slot of $M$. A page that is not yet reachable can be set up without a CAS.
- **Base page.** A sorted array of entries, as in a B+ tree, with a range $[low, high)$ and the pid of its right sibling. A leaf holds keys and values; an inner page holds separator keys and child pids.
- **Delta records.** A delta points to the previous head of the same page. A leaf has *insert* and *delete* deltas. A *split* delta $(sep, Q)$ says that the keys from $sep$ on are now in page $Q$, and so sets $high = sep$ and the right link to $Q$. An *index term* delta $(sep \to Q)$ on an inner page adds a child.
- **Chain.** The head of a page is a chain of zero or more deltas in front of one base page. The newest delta comes first.

Because pages refer to each other by pid, a change of one page never needs to update a pointer in another page. This is what lets one CAS install it, and it also lets the store move a page to flash and back without changing its parent.

## Operations

```pseudo id=main
UPDATE(k, kind, v)                        ▷ upsert or delete
L1  repeat (pid, parent, h) ← FIND(k, 0)
L2      (found, old) ← search the chain h for k: the newest delta on k decides, else a binary search of the base page
L3      if kind = delete and not found then return nothing
L4      d ← a new delta (kind, k, v) whose next pointer is h
L5  until CAS(M[pid], h, d)
L6  if the chain of pid is longer than max_chain then CONSOLIDATE(pid)
L7  if the page of pid holds more than max_page entries then SPLIT(pid, parent); return old
```

```pseudo id=find
FIND(k, level)
L8  pid ← root; parent ← nothing
L9  loop h ← M[pid]
L10     (low, high, right) ← the bounds of h (from the newest split delta, else the base page); if k ≥ high then
L11         if the walk came down to pid then HELP-ALONG(parent, high, right); pid ← right; continue
L12     if the level of h is level then return (pid, parent, h)
L13     parent ← pid; pid ← the child for k in h (the index term deltas first, then the base page)
```

```pseudo id=smo
CONSOLIDATE(pid)
L14 h ← M[pid]; b ← a new base page with the content of h
L15 CAS(M[pid], h, b)                     ▷ if it fails, another thread changed the page; keep the new head

SPLIT(pid, parent)
L16 h ← M[pid]; sep ← the middle key of h; Q ← a new pid with the entries ≥ sep, the range [sep, high) and the right link of h
L17 if not CAS(M[pid], h, a split delta (sep, Q) on h) then return
L18 HELP-ALONG(parent, sep, Q)

HELP-ALONG(parent, sep, q)
L19 loop g ← M[parent]; if g is not one level above q, or sep is not in its range, or g already routes sep to q, then return
L20     if CAS(M[parent], g, an index term delta (sep → q) on g) then return
```

- **Lookup** is FIND followed by the search of L2.
- **Root split.** The root has no parent, so its split makes two new pages from its content and replaces the root head by a new inner base page one level up, in one CAS.
- **Retry.** A failed CAS at L5 means that another thread changed the page; the operation starts again at L1. A failed CAS at L15 or L17 is not retried by the code on this page: the other thread's change wins, and the next update of the page checks again.
- **Help along.** A thread that reaches a page by its parent and must follow a right link has found a split whose index term is missing, and it posts the term (L11). So a thread that stops after L17 never blocks the others.
- **Merges** are also in the paper, in three steps (a remove node delta, a merge delta on the left sibling and an index term delete delta on the parent). The code on this page does not merge pages.

## Example

The tree has `max_page` = 4 and `max_chain` = 3, and starts as one empty leaf, pid 0, the root. These are the upserts of 10, 20, 30, 40, 25, 35 and 45, one thread, as the code on this page runs them.

1. **10, 20, 30.** Each one is an insert delta on pid 0. The chain is now ins 30, ins 20, ins 10, then the empty base page.
2. **40.** The fourth delta makes the chain longer than 3, so the page is consolidated: one CAS installs the base page [10, 20, 30, 40].
3. **25.** Now pid 0 has 5 entries. It is the root, so the root splits at the middle key 25: pid 1 gets [25, 30, 40] with the range [25, ∞), pid 2 gets [10, 20] with the range [-∞, 25) and the right link 1, and one CAS makes pid 0 the inner page [-∞ → 2, 25 → 1].
4. **35.** An insert delta on pid 1.
5. **45.** A second delta on pid 1, which now has the 5 keys 25, 30, 35, 40 and 45. The split takes the middle key 35, sets up pid 3 as the base page [35, 40, 45] with the range [35, ∞), and puts the split delta (35, 3) on pid 1. The chain of pid 1 is now split 35, ins 45, ins 35, then the base page [25, 30, 40], and its content is [25, 30]. The help-along step puts the index term delta (35 → 3) on the root.

| pid | chain, newest first | content | range |
|---|---|---|---|
| 0 | term (35 → 3), base [-∞ → 2, 25 → 1] | 3 children | [-∞, ∞) |
| 1 | split (35, 3), ins 45, ins 35, base [25, 30, 40] | 25, 30 | [25, 35) |
| 2 | base [10, 20] | 10, 20 | [-∞, 25) |
| 3 | base [35, 40, 45] | 35, 40, 45 | [35, ∞) |

The run made 11 successful CAS operations: 7 deltas, 1 consolidation, 1 root split, 1 split delta and 1 index term. A lookup of 40 now goes from the root to pid 3 directly. Before the index term was posted, it would have gone to pid 1, seen that 40 is at least its new high key 35, and followed the right link to pid 3.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). The main points:

- **One CAS per change.** A CAS on $M[pid]$ succeeds only if the head is still the one the thread read, so each change is computed from the page as it is at the instant it is installed.
- **Invariant.** Each level, read along the right links, splits the key space into ranges in order; each inner page routes a key to a child whose low key is at most that key; every key is in the leaf whose range holds it; and a low key never changes while a high key can only fall. Every kind of CAS (delta, consolidation, split delta, index term, root split) keeps this invariant.
- **Find.** Under the invariant, a walk that follows a right link when the key is at least the high key always reaches the page whose range holds the key, even if a split is half done.
- **Linearizability (theorem).** An update takes effect at its successful CAS at L5, and a lookup at its read of the leaf head. Splits and consolidations do not change the map.
- **Lock-freedom (theorem).** A CAS fails only because another CAS on the same slot succeeded, so some operation always makes progress. One operation can retry without bound, so the Bw-tree is not wait-free.

The tests check sequential runs against a dict, concurrent writers with disjoint keys, a split stopped half way, and, by a search over all orders, that every interleaving of three threads with four operations each on 60 seeds is linearizable.

## Complexity

- **Lookup.** At each of the $h$ levels, a scan of at most $c$ deltas and a binary search of a base page of at most $B$ entries, so $O(h (c + \log B))$ without contention. Right links add steps only while a split is half done.
- **Update.** A lookup and one CAS. Under contention a CAS can fail and the operation starts again, so there is no bound on the time of one operation, only on the progress of the system.
- **Consolidation** costs $O(B + c)$ with a merge of the deltas into the base page (the code on this page sorts, which costs a log factor more). It happens once per $c$ updates of a page, so its amortized cost per update is $O(B / c + 1)$.
- **Space.** $O(n)$: the base pages, at most $c$ deltas per page, and one mapping table slot per page. Old chains must be kept until no thread can still read them, which the paper does with epochs.

## Variants

- **LLAMA.** The authors' store under the Bw-tree. It writes pages and deltas to a log-structured store on flash and can keep a page on flash while its pid stays the same.
- **OpenBw-Tree.** The open version of Wang et al. (2018), which adds pre-allocated delta space in each page, faster consolidation, a different garbage collection and other changes to the original design.
- **[B-link tree](/blink-tree/).** The same right links and the same two-step split, but with latches on the pages instead of a CAS on a mapping table.
- **Other designs.** In-memory indexes that use optimistic locks, such as the [adaptive radix tree](/adaptive-radix-tree/) with optimistic lock coupling, are not latch-free but avoid the chain walks.

## When to use it

The Bw-tree fits an ordered index on a multicore machine where threads must never block each other, and where the pages may live on flash, since the mapping table lets a page move without changes to its parent. Microsoft used it in the Hekaton in-memory engine of SQL Server. It is a research design with many details that the paper does not fix. Wang et al. found that even their optimized version was slower than in-memory indexes with optimistic locks in their tests (a measurement). If latches are acceptable, a B-link tree or a tree with optimistic lock coupling is usually simpler and faster.

## Pitfalls

- **Memory reclamation.** A thread can still be reading a chain after another thread has replaced it. Freeing the old chain at once is a use-after-free. The paper uses [epoch-based reclamation](/epoch-based-reclamation/); the Python code relies on the garbage collector.
- **ABA.** If the memory of a freed delta is reused for a new head of the same slot, a late CAS can succeed against the wrong page. Safe reclamation also prevents this [ABA problem](/aba-problem/).
- **Help along needs checks.** A thread that posts an index term must check that the parent is one level above the new page, that the separator is still in the parent's range, and that the term is not already there (L19). Without these checks, two threads post the same term twice, or a term goes to a parent that has split.
- **Long chains.** Every lookup walks the chain. If consolidation is late, lookups slow down; if it is too early, it copies pages too often. The limit on chain length is a heuristic, tuned by measurement.
- **Lost work.** If the CAS of a split delta fails, the new page was set up for nothing and must be freed. If a consolidation CAS fails, the new base page is lost too.
- **Merges.** Removing a page needs three steps and careful rules for threads that are in the middle of the page being removed. Wang et al. report this as one of the hardest parts to get right.

## Implementations

## History

Justin Levandoski, David Lomet and Sudipta Sengupta of Microsoft Research presented the Bw-tree at ICDE 2013, together with the LLAMA store under it. It built on the B-link tree of Lehman and Yao (1981), which brought in right links and splits in two steps, and replaced its latches by delta records and a CAS on a mapping table. In 2018, Ziqi Wang, Andrew Pavlo and coauthors at Carnegie Mellon University built the OpenBw-Tree, described the details that the paper leaves open, and compared it with other in-memory indexes.

## References
