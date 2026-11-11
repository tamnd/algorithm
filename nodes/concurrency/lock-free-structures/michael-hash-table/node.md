---
tag: Z81DZW
kind: data-structure
slug: michael-hash-table
name: Michael lock-free hash table
aliases:
- Michael hash table
- lock-free chained hash table
area: concurrency/lock-free-structures
level: advanced
summary: Lock-free hash table in which each bucket is a Harris-Michael lock-free list with a fixed bucket count.
implements: [dictionary]
complexity:
  vars: {n: "the number of keys", m: "the number of buckets, fixed", p: "the number of processes", b: "the number of nodes in the bucket of the key"}
  space: {extra: Θ(m + n + p²)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [hash-table, harris-linked-list, hazard-pointers, linearizability, lock-freedom]
see_also: [split-ordered-list, logical-deletion, concurrent-hash-table, lock-striping, epoch-based-reclamation, aba-problem]
sources:
  - paper: doi:10.1145/564870.564881
    title: Maged M. Michael, High performance dynamic lock-free hash tables and list-based sets, SPAA 2002, pages 73 to 82
    locator: the list-based set with the Find, Insert and Delete functions and their hazard pointers, the hash table made of an array of such lists, and the proof sketch of correctness
  - paper: doi:10.1109/TPDS.2004.8
    title: "Maged M. Michael, Hazard pointers: safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491 to 504"
    locator: the hazard pointer method, the scan with a threshold R, and the bound on the number of retired nodes that are not yet freed
  - paper: doi:10.1007/3-540-45414-4_21
    title: Timothy L. Harris, A pragmatic implementation of non-blocking linked-lists, DISC 2001, LNCS 2180, pages 300 to 314
    locator: the marked next pointer and the two-step delete on which Michael's list is built
  - paper: doi:10.1145/1147954.1147958
    title: "Ori Shalev and Nir Shavit, Split-ordered lists: lock-free extensible hash tables, Journal of the ACM 53(3), 2006, pages 379 to 405"
    locator: the introduction, which takes Michael's table as the fastest lock-free table with a fixed size and adds resizing
---

The Michael hash table is a lock-free [hash table](/hash-table/) with separate chaining. It has a fixed array of $m$ buckets, and each bucket is a sorted lock-free list: the list of Michael (2002), which is the [Harris list](/harris-linked-list/) changed so that it works with [hazard pointers](/hazard-pointers/). An operation hashes its key, picks one bucket, and runs the list operation there. Operations on different buckets touch no common word, so they never slow each other down. The table is [linearizable](/linearizability/) and [lock-free](/lock-freedom/), and it frees memory safely with hazard pointers. It does not resize: if the number of keys grows far beyond $m$, the lists get long. The [split-ordered list](/split-ordered-list/) adds resizing to the same idea.

## In plain words

Think of a row of hooks. Each hook holds a short chain of tags, kept in order. To find a key, you work out from the key which hook it must be on, and then walk only that chain. Two people who work on different hooks never meet.

Each chain is a lock-free list. To remove a tag, you first mark it as removed and then cut it out. People who walk past a marked tag cut it out for you.

Removed tags cannot be thrown away at once, because somebody may still be reading them. So each person writes on a small public board the tags they are reading right now. A tag goes to the bin only when no board names it.

The number of hooks never changes. If many more keys come than hooks, the chains get long and the table gets slow.

## The abstract type

The table implements a [dictionary](/dictionary/) of keys (the values are left out here, as in the paper's set version):

- insert(k): add $k$; return true if $k$ was not present, false otherwise.
- delete(k): remove $k$; return true if $k$ was present, false otherwise.
- contains(k): return whether $k$ is present.

Each operation is linearizable: it seems to take effect at one moment between its call and its return.

## Representation

### Model and notation

We use the asynchronous shared memory model with $p$ processes that may crash, atomic read, write and single-word CAS, and [sequential consistency](/sequential-consistency/). Memory is reused: a freed node may come back as a new node at the same address with another key. Each process $q$ has three hazard pointer words that any process can read.

| Symbol | Meaning |
|---|---|
| $m$ | the number of buckets; it never changes |
| $h(k)$ | the bucket of key $k$; the code uses $k \bmod m$ |
| `bucket[i]` | the word that points to the first node of bucket $i$ |
| `n.key`, `n.next` | the key of node `n`, and its successor with a mark bit |
| `(x, b)` | a marked pointer: pointer `x` with mark bit `b` |
| `prev` | the word that points to `cur`: a `bucket[i]` word or the `next` field of the node before `cur` |
| `hp0`, `hp1`, `hp2` | the hazard pointers of the running process; they protect `next`, `cur` and the node that holds `prev` |
| $R$ | the scan threshold: a process scans when it has $R$ retired nodes |

### Fields

- `bucket[0..m-1]`: marked pointers to the first node of each list; the mark of a bucket word is always clear.
- A node: `key`, and `next`, a marked pointer.
- `hp[q][0..2]` for each process $q$: shared words, written only by $q$.
- `retired[q]`: a private list of nodes that $q$ has unlinked but not yet freed.

**Invariants.** (1) In each bucket, the reachable nodes have strictly increasing keys, and every key $k$ in bucket $i$ has $h(k) = i$. (2) A marked `next` field never changes again. (3) A node is unlinked only after it is marked. (4) A node is freed only when it is unlinked, retired, and was not in any hazard pointer at the time of the scan. The abstract set is the set of keys of the unmarked nodes that are reachable from some bucket.

## Operations

```pseudo id=main
FIND(k)                                       ▷ sets prev, cur, next and returns whether cur.key = k
L1  prev ← &bucket[h(k)]; cur ← ptr(*prev)
L2  hp1 ← cur
L3  if *prev ≠ (cur, 0) then go to L1                    ▷ cur was still in the list when protected
    loop
L4      if cur = null then return false
L5      (next, cmark) ← cur.next
L6      hp0 ← next
L7      if cur.next ≠ (next, cmark) then go to L1
L8      ckey ← cur.key
L9      if *prev ≠ (cur, 0) then go to L1
L10     if not cmark then
L11         if ckey ≥ k then return ckey = k
L12         prev ← &cur.next; hp2 ← cur
        else                                    ▷ cur is marked: unlink it, one node at a time
L13         if CAS(prev, (cur, 0), (next, 0)) then RETIRE(cur) else go to L1
L14     cur ← next; hp1 ← next

INSERT(k)
L15 repeat: if FIND(k) then
L16     return false (and free the new node if one was made)
L17 make node n with key k (or reuse it); n.next ← (cur, 0)
L18 if CAS(prev, (cur, 0), (n, 0)) then return true else go to L15

DELETE(k)
L19 repeat: if not FIND(k) then
L20     return false
L21 if not CAS(cur.next, (next, 0), (next, 1)) then go to L19     ▷ logical deletion
L22 if CAS(prev, (cur, 0), (next, 0)) then RETIRE(cur) else FIND(k)  ▷ physical deletion
L23 return true

CONTAINS(k)
L24 return FIND(k)
```

```pseudo id=retire
RETIRE(node)                                  ▷ by process q
R1  append node to retired[q]
R2  if |retired[q]| ≥ R then
R3      H ← the values of all hazard pointers of all processes
R4      for each node x in retired[q] not in H:
R5          remove x from retired[q] and free x
```

**Why FIND reads each word twice.** A hazard pointer protects a node only if the node was still in the list when the hazard pointer was set; otherwise a scan may already have missed it. So after `hp1 ← cur` the search reads `prev` again (L3, L9), and after `hp0 ← next` it reads `cur.next` again (L7). If either word changed, it starts over from the bucket head. If `prev` still holds `(cur, 0)` after `hp1` was set, then `cur` was reachable at that time, and no process can free it until `hp1` changes.

**One node at a time.** Unlike Harris's search, FIND unlinks only the marked node `cur` that it stands on (L13), and starts over from the bucket head if that CAS fails. It never walks along a chain of marked nodes that may already be unlinked, so it never needs a hazard pointer on a node that was not reachable when it was protected. This is the change that lets the list work with hazard pointers.

**Linearization points.** As in the Harris list: a successful insert at its CAS at L18; a successful delete at its mark at L21; an operation that finds the key at the read L5 that returned `cur.next` unmarked, confirmed by L9; an operation that does not find it at the read L9 (or L3) that confirmed `prev` = `(cur, 0)` with `cur.key` > $k$ or `cur` = null.

### Memory reclamation

This page is built around the reclamation scheme. A node is retired after it is unlinked (L13, L22) and freed only by a scan that finds no hazard pointer on it (R3 to R5). With $p$ processes and three hazard pointers each, a scan keeps at most $3p$ nodes, so each process holds at most $3p + R - 1$ retired nodes; with $R = \Theta(p)$, a scan frees $\Omega(R)$ nodes and costs $O(1)$ amortized steps per retired node (Michael 2004, cited). Without hazard pointers, a node freed at L13 or L22 can still be in use by a slow FIND, which then reads freed memory; and if the address is reused, a CAS at L13 or L18 that expects `(cur, 0)` can succeed against the new node, the [ABA problem](/aba-problem/). The test `test_without_hazard_pointers_a_reader_uses_a_freed_node` shows the first case. [Epoch-based reclamation](/epoch-based-reclamation/) also works, and with it the search does not need the second reads.

### Weak memory

The write of a hazard pointer must be ordered before the second read of `prev` or `cur.next` (a store followed by a load, so it needs a full fence, or a sequentially consistent store, on x86 and on ARM). Without the fence, the second read can happen before the hazard pointer is visible, and a scan can miss it. The scan must read the hazard pointers after the node was unlinked, which a full fence before R3 ensures. The CAS that links a new node must be a release, and reads of `next` must be acquire loads, as in the Harris list.

## Example

Take $m = 2$ and the keys 1, 2, 3, 6. Bucket 0 is 2 → 6 and bucket 1 is 1 → 3.

1. contains(6) by $p_0$ looks only at bucket 0. It protects 2, checks `bucket[0]`, reads `2.next` = 6, protects 6, and so on, and returns true.
2. delete(1) by $p_1$ runs at the same time in bucket 1. FIND stops at node 1 with `prev` = `&bucket[1]`. The CAS at L21 marks `1.next`, and the CAS at L22 sets `bucket[1]` to `(3, 0)`. Node 1 is retired. With $R = 1$, $p_1$ scans: if $p_2$ is in a FIND that has `hp1` = node 1, node 1 stays in `retired[1]`; otherwise it is freed.
3. A slow insert(5) by $p_2$ that had `prev` = `&1.next` and `cur` = 3 now does its CAS at L18 on `1.next`. The word is `(3, 1)`, marked, so the CAS fails and $p_2$ starts over at `bucket[1]`. It links 5 after 3.

No step of $p_0$ touched a word of bucket 1, and no step of $p_1$ or $p_2$ touched a word of bucket 0.

## Correctness

Each bucket is an independent instance of Michael's list, and the abstract set is the disjoint union of the sets of the buckets, because $h$ sends each key to one bucket. A history of the table, restricted to one bucket, is a history of that list; linearizability is local (a property of Herlihy and Wing), so the table is linearizable if each list is. The list is linearizable by the argument of the [Harris list](/harris-linked-list/), with one more fact for memory reuse: no node is freed while a process holds it in a hazard pointer, and a process uses a node only after it has set a hazard pointer on it and checked that the node was still reachable. So a process never reads a freed node, and a CAS never compares against a reused address that the process did not protect. The proof sketch is in [proofs/correctness.md](proofs/correctness.md).

Progress is lock-free. A FIND restarts only when a word it read again has changed, or when its CAS fails, and each such change is a successful CAS or a write of a `next` field by another process, which happens a bounded number of times per completed operation. The scan does a bounded number of steps. The tests check linearizability and the absence of any use after free on all interleavings of six small cases, with memory reused at once and a scan on every retire; and on 80 seeded runs with three processes.

## Complexity

| case | steps of one operation |
|---|---|
| alone, contains, bucket of $b$ nodes | $7b + 3$ (measured) |
| alone, insert | $7b + 5$ (measured) |
| alone, delete, key in the last node | $7b + 3 + 3p$ plus at most $R$ frees (measured for $p = 1$) |
| with contention | unbounded (lock-free, not wait-free) |
| expected $b$, uniform hashing | $n / m$ |

The solo counts are proved by counting the steps of the pseudocode: three to start, seven for each node passed (the read of `next`, `hp0`, the second read of `next`, the key, the second read of `prev`, `hp2` and `hp1`), five at the node where the search stops, and for delete two CAS steps and a scan of the $3p$ hazard pointers. A delete alone does not free the node it just unlinked, because its own `hp1` still holds it. The tests check them for buckets of up to 10 nodes. With a hash function that spreads keys evenly, the expected bucket length is $n/m$ (a property of chaining, cited from the [hash table](/hash-table/) page), so an operation takes $O(1 + n/m)$ expected steps alone. Since $m$ is fixed, this is $O(1)$ only while $n = O(m)$.

Space: $m$ bucket words, one node per key, plus marked nodes not yet unlinked, plus at most $3p + R - 1$ retired nodes per process, and $3p$ hazard pointers. With $R = \Theta(p)$ that is $\Theta(m + n + p^2)$ in the worst case.

## Variants

- **Values.** The paper's table maps keys to values; a node also holds a value, and the operations return it. The structure of the search is the same.
- **Other reclamation.** With [epoch-based reclamation](/epoch-based-reclamation/) or a garbage collector, the second reads in FIND can go, and the Harris search that unlinks chains of marked nodes can be used.
- **Resizable tables.** The [split-ordered list](/split-ordered-list/) keeps all keys in one Michael list in bit-reversed order, so that new buckets are only new entry points into the list and no key ever moves. Other resizable designs copy the table to a new array, which needs care to stay lock-free.
- **Lock-based tables.** A table with a lock for each bucket, or with [lock striping](/lock-striping/), is simpler and often as fast under low contention; see [concurrent hash table](/concurrent-hash-table/).
- **Open addressing.** Lock-free tables with open addressing (Purcell and Harris; Click's table in Java) avoid the pointer chase but make deletion harder; they are a different family.

## When to use it

Use it when you know the number of keys in advance, so that you can fix $m$ at about that number, and when you need lock-free progress and safe memory reuse in a language with no garbage collector. Its operations are short and touch only one bucket, so it scales well. If the number of keys is not known, use a resizable table such as the split-ordered list. If lock-freedom is not needed, a table with fine-grained locks is simpler.

## Pitfalls

- **Skipping the second read.** Setting a hazard pointer and then using the node without checking that it was still reachable lets a scan miss it. Both second reads are needed.
- **Missing the fence after the hazard pointer write.** On real hardware, the store to the hazard pointer and the following load can be reordered, which has the same effect as skipping the second read.
- **Harris's search with hazard pointers.** The chain of marked nodes may be already unlinked, and a hazard pointer set on one of them cannot be validated. Use Michael's one-node search, as here.
- **Freeing at the unlink.** The cheapest bug: it works in light tests and fails under load.
- **A bad hash.** Every key goes to its bucket by $h$; a hash that sends many keys to one bucket makes the table a single long list. The table cannot fix this by resizing.
- **Expecting resizing.** The paper's table has a fixed size. Growing it means building a new table.

## Implementations

## History

Michael presented the table at SPAA 2002, together with the list it uses. Harris (2001) had given a lock-free list with marked pointers, but its search was not compatible with the memory reclamation methods of the time; Valois (1995) had earlier given a lock-free list with auxiliary nodes and reference counts. Michael's list changed the search to unlink one marked node at a time, which made it work with his hazard pointers (PODC 2002 and IEEE TPDS 2004) and with other schemes, and made the table, he reported, faster than earlier lock-free and lock-based tables in his experiments. Shalev and Shavit (PODC 2003, JACM 2006) used Michael's list as the base of the split-ordered list, which adds lock-free resizing.

## References
