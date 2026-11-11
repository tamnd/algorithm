---
tag: XCTCZ1
kind: data-structure
slug: split-ordered-list
name: Split-ordered lists lock-free hash table
aliases:
- Shalev-Shavit hash table
- Split-ordered list
- lock-free extensible hash table
- split-ordered lists
- recursive split ordering
area: concurrency/lock-free-structures
level: research
summary: Lock-free resizable hash table that keeps all items in one list ordered by bit-reversed hash, so buckets split without moving items.
implements: [dictionary]
complexity:
  vars: {n: "the number of keys", s: "the number of buckets, a power of two", L: "the load bound: the table doubles when n > L s"}
  space: {extra: Θ(n + s)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [hash-table, harris-linked-list, compare-and-swap, linearizability, lock-freedom]
see_also: [michael-hash-table, logical-deletion, concurrent-hash-table, hazard-pointers, lock-free-skip-list, fetch-and-add]
sources:
  - paper: doi:10.1145/1147954.1147958
    title: "Ori Shalev and Nir Shavit, Split-ordered lists: lock-free extensible hash tables, Journal of the ACM 53(3), 2006, pages 379 to 405"
    locator: recursive split ordering, the dummy nodes, initialize_bucket with the parent bucket, the insert that doubles the size with one CAS, the two-level segment table, and the proofs of correctness and of constant expected cost
  - paper: doi:10.1145/872035.872049
    title: Ori Shalev and Nir Shavit, Split-ordered lists, lock-free extensible hash tables, PODC 2003, pages 102 to 111
    locator: the conference version of the same algorithm
  - paper: doi:10.1145/564870.564881
    title: Maged M. Michael, High performance dynamic lock-free hash tables and list-based sets, SPAA 2002, pages 73 to 82
    locator: the lock-free list-based set that the split-ordered list uses for its single list
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: the chapter on concurrent hashing, the section on a lock-free hash set with recursive split ordering
---

The split-ordered list of Shalev and Shavit is a lock-free [hash table](/hash-table/) that can grow. All keys live in one lock-free sorted list, the list of [Michael](/michael-hash-table/). The list is not sorted by key but by the *bit-reversed* hash of the key. In that order, the keys of each bucket form one contiguous run, and when the number of buckets doubles, each run splits into two runs that are already in place. So a resize never moves a key. A bucket is only a shortcut: a pointer to a *dummy node* in the list where the run of that bucket starts. Buckets are made lazily, on first use, by inserting one dummy node. The table is [linearizable](/linearizability/) and [lock-free](/lock-freedom/); a resize is a single CAS on the size.

## In plain words

Picture all the cards of a card file on one long string, in a special order. Each drawer of the file is just a bookmark on the string: the cards of a drawer sit together, right after its bookmark.

When the file gets too full, you want twice as many drawers. Usually that means taking every card out and sorting it again. Here, the special order makes every group of cards split into two groups that already sit one after the other. To make a new drawer, you only clip a new bookmark into the string, at the place where the second group starts. No card moves.

The string is a lock-free list, so many people can add and remove cards at once. New bookmarks are clipped in only when somebody first needs that drawer.

## The abstract type

The table implements a [dictionary](/dictionary/); the code keeps only the keys.

- insert(k): add $k$; return true if $k$ was not present, false otherwise.
- delete(k): remove $k$; return true if $k$ was present, false otherwise.
- contains(k): return whether $k$ is present.

## Representation

### Model and notation

We use the asynchronous shared memory model with processes that may crash, atomic read, write, CAS and [fetch-and-add](/fetch-and-add/), and [sequential consistency](/sequential-consistency/). Nodes are not freed in the code (the model has a garbage collector); see the section on memory reclamation.

| Symbol | Meaning |
|---|---|
| $W$ | the number of bits of a hash value |
| $h(k)$ | the hash of key $k$, an integer below $2^{W-1}$ (the identity in the code) |
| $\mathrm{rev}(x)$ | $x$ written in $W$ bits with the bits in reverse order |
| $\mathrm{so}(k)$ | the split-order key of a regular key: $\mathrm{rev}(h(k) \mid 2^{W-1})$, always odd |
| $\mathrm{sd}(b)$ | the split-order key of the dummy node of bucket $b$: $\mathrm{rev}(b)$, always even |
| $s$ | the shared word `size`: the number of buckets, a power of two; it only grows |
| `T[b]` | a pointer to the dummy node of bucket $b$, or null if the bucket is not initialized yet |
| $\mathrm{parent}(b)$ | $b$ with its highest 1 bit cleared |
| $L$ | the load bound: the table doubles when `count` $> L \cdot s$ |

### Fields

- One Michael list of nodes, sorted by split-order key. A node has `key` (its split-order key) and `next` (a marked pointer). Dummy nodes are never deleted.
- `T[0..MAX-1]`: the bucket array. `T[0]` points to the dummy of bucket 0, with key 0, which is the first node of the list.
- `size`: the number of buckets $s$.
- `count`: the number of keys, kept with fetch-and-add.

**Invariant.** (1) The list is sorted by split-order key, with no two nodes of the same key. (2) If `T[b]` is not null, it points to the dummy node of bucket $b$, which is in the list. (3) For every power of two $t \le s$ and every $b < t$, the regular keys with $h(k) \bmod t = b$ form one contiguous run of the list, and if `T[b]` is set, that run comes after the dummy of $b$ with no other dummy of a bucket below $t$ in between.

The trick in one line: $h(k) \bmod 2^i$ is the low $i$ bits of $h(k)$, which after the reversal are the high $i$ bits of $\mathrm{so}(k)$. Sorting by $\mathrm{so}$ sorts first by those $i$ bits, for every $i$ at once.

## Operations

```pseudo id=main
INSERT(k)
L1  node ← new node with key so(k)
L2  b ← h(k) mod size
L3  if T[b] = null then INITIALIZE_BUCKET(b)
L4  if not LIST_INSERT(T[b], node) then return false   ▷ k is already there
L5  csize ← size
L6  if FAA(count, 1) + 1 > L · csize then CAS(size, csize, 2 · csize)
L7  return true

CONTAINS(k)
L8  b ← h(k) mod size
L9  if T[b] = null then INITIALIZE_BUCKET(b)
L10 return LIST_FIND(T[b], so(k))

DELETE(k)
L11 b ← h(k) mod size
L12 if T[b] = null then INITIALIZE_BUCKET(b)
L13 if not LIST_DELETE(T[b], so(k)) then return false
L14 FAA(count, −1); return true

INITIALIZE_BUCKET(b)
L15 p ← parent(b)
L16 if T[p] = null then INITIALIZE_BUCKET(p)
L17 dummy ← new node with key sd(b)
L18 if not LIST_INSERT(T[p], dummy) then dummy ← the node with key sd(b) that is already there
L19 CAS(T[b], null, dummy)
```

LIST_INSERT, LIST_FIND and LIST_DELETE are the operations of Michael's list (see the [Michael hash table](/michael-hash-table/)), started at the given dummy node in place of a list head. A search that starts at the dummy of bucket $b$ walks only the run of bucket $b$, because the run ends at the next dummy or at a key outside the bucket, which has a larger split-order key.

**Why the dummy goes in before T[b] is set.** The CAS at L19 publishes the bucket only after its dummy is in the list (L18). If the bucket were published first, another process could insert a key after the new dummy while the dummy is not yet linked; the dummy's `next` is then set again when it is linked, and the key is lost. The test `test_publishing_a_bucket_early_loses_an_insert` finds this run with the explorer and replays it.

**Why two dummies of one bucket cannot both be linked.** Both would have key $\mathrm{sd}(b)$, and LIST_INSERT refuses a second node with a key that is in the list. The loser takes the winner's dummy (L18), so every process that sets `T[b]` sets it to the same node, and the CAS at L19 just makes the write happen once.

**Resizing.** L6 doubles `size` with one CAS. Nothing else happens: the new buckets $b + s$ for $b < s$ are null, and each is initialized by the first operation that needs it. If two processes try to double at once, the CAS lets only one of them succeed for each value of `size`.

**Linearization points.** Those of the list operations inside: a successful insert at its linking CAS; a successful delete at its mark; the others at the point of the list search. The bucket array and `size` are hints that only choose the starting point of the search, so they have no linearization point of their own.

### Memory reclamation

The list is Michael's list, so its regular nodes can be freed with [hazard pointers](/hazard-pointers/) exactly as in the [Michael hash table](/michael-hash-table/), and the paper does so. Dummy nodes are never removed, which is what makes them safe starting points: a process that reads `T[b]` needs no hazard pointer on the dummy. Without a scheme, a regular node freed at its unlink can be read by a slow search and, if its address is reused, a CAS that expects `(cur, 0)` can succeed on the new node (the [ABA problem](/aba-problem/)); the effect is the same as in any list built on [logical deletion](/logical-deletion/).

### Weak memory

The CAS at L19 must be a release and the read of `T[b]` an acquire load, so that a process that sees the dummy pointer also sees the dummy node and its link. The same holds for the linking CAS steps inside the list. The read of `size` can be relaxed: a stale size only picks a coarser bucket, whose run contains the run of the finer one, and the search still finds the key.

## Example

Take $W = 8$ bits. Write split-order keys in binary.

| key or dummy | bits before the reversal | split-order key |
|---|---|---|
| dummy 0 | 00000000 | 00000000 |
| key 4 | 10000100 | 00100001 |
| dummy 2 | 00000010 | 01000000 |
| key 2 | 10000010 | 01000001 |
| dummy 1 | 00000001 | 10000000 |
| key 1 | 10000001 | 10000001 |
| key 5 | 10000101 | 10100001 |
| key 3 | 10000011 | 11000001 |

With $s = 2$, the list is: dummy 0, 4, 2, dummy 1, 1, 5, 3. Bucket 0 is the run 4, 2 and bucket 1 is the run 1, 5, 3. Now `size` becomes 4. Bucket 2 (parent 0) and bucket 3 (parent 1) are null. A contains(2) computes $b = 2$, finds `T[2]` null, and initializes it: it inserts dummy 2 from dummy 0, between 4 and 2, and sets `T[2]`. The list is now dummy 0, 4, dummy 2, 2, dummy 1, 1, 5, 3. Bucket 0 is the run 4 (keys $\equiv 0 \bmod 4$) and bucket 2 is the run 2. No node moved; one node was added. A later insert(7) in bucket 3 would add dummy 3 (key 11000000) right before 3.

## Correctness

The structure is one Michael list plus hints, so its linearizability is that of the list (see the [Harris list](/harris-linked-list/) for the argument), provided that every operation starts its search at a node that comes before every node with key $\mathrm{so}(k)$ and that no node with key $\mathrm{so}(k)$ can lie before it. The start is the dummy of $b = h(k) \bmod t$ for the value $t$ of `size` the operation read. The keys with $h(k) \bmod t = b$ all have split-order keys whose high bits equal $\mathrm{rev}$ of the low bits of $b$, and $\mathrm{sd}(b)$ is the smallest number with those high bits, so the dummy comes before them. This is the contiguity lemma; [proofs/correctness.md](proofs/correctness.md) proves it in full, with the facts that `T[b]` is set only to a linked dummy, that dummies are never removed, and that a resize leaves every run in place.

Progress is lock-free. The list operations are lock-free. INITIALIZE_BUCKET recurses at most $\log_2 s$ times, since each parent has one fewer 1 bit, and each level does one list insert and one CAS. The CAS at L6 is tried once.

The tests check all interleavings of four small cases, including two processes that initialize the same bucket and operations that run while the table doubles; 60 seeded runs with three processes that grow the table from 1 bucket; and, after every operation of a run that grows the table to 32 buckets, that the list is sorted, that each bucket's keys are contiguous for every size up to the current one, and that each initialized bucket's keys follow its dummy.

## Complexity

| quantity | bound | status |
|---|---|---|
| steps alone, bucket initialized, $j$ keys in the run | $j + 3$ reads for contains (4 when $j = 1$, measured) | proved by counting |
| bucket initialization, worst case | at most $\log_2 s$ nested initializations | proved |
| expected steps of an operation, uniform hashing | $O(1)$ | cited (Shalev and Shavit, the JACM paper) |
| resize | one CAS, no key moves | proved |
| with contention | unbounded (lock-free, not wait-free) | |

With $n \le L s$ and a hash that spreads keys evenly, the run of a bucket has $O(L)$ expected length, so a search takes $O(1)$ expected steps. The paper also shows that the expected cost of the lazy initializations is constant; this page does not prove that. Space: one node per key, one dummy per initialized bucket, and the bucket array, $\Theta(n + s)$.

## Variants

- **Segment table.** A flat array must be sized for the largest table at the start. The paper also gives a two-level table of segments, each allocated on first use, so the bucket array grows too. The code here uses a flat array of 64 entries.
- **Hazard pointers.** The paper's list frees nodes with hazard pointers; the code here does not free nodes.
- **Fixed-size table.** The [Michael hash table](/michael-hash-table/) is the same idea without resizing: one list per bucket. It is simpler but slows down when $n$ grows far beyond the number of buckets.
- **Shrinking.** The table as given only grows. Shrinking would mean removing dummy nodes that other processes may be using as starting points, which needs more care.
- **Other resizable tables.** Lock-free tables that copy to a new array as they grow (for example Click's table for Java, and later designs) keep keys in an array and help to move them; they avoid the pointer chase of a list but need a migration protocol.

## When to use it

Use it when you need a lock-free hash table whose size you cannot fix in advance. It is the standard example of a lock-free resizable table, and the version in *The Art of Multiprocessor Programming* is often used in teaching. In practice, the long single list costs cache misses, since a search follows pointers; an open-addressing table with a migration protocol can be faster for small keys. If lock-freedom is not needed, a table with lock striping that rehashes under all locks is simpler.

## Pitfalls

- **Publishing a bucket before its dummy is linked.** Shown above: it loses inserts.
- **Forgetting the top bit of regular keys.** Regular keys must be odd and dummies even after the reversal, or a regular key can equal a dummy key.
- **Reading `size` twice.** An operation must compute its bucket from one read of `size`. Mixing two reads can pick a bucket that does not match the key.
- **Deep recursion in initialization.** In the worst case, a new bucket has a chain of $\log_2 s$ parents that are not initialized; the recursion is short, but it is not constant.
- **Comparing keys with the original order.** The list order is the split order, not the key order, so the table cannot answer range queries.

## Implementations

## History

Shalev and Shavit presented split-ordered lists at PODC 2003, and the journal version appeared in the Journal of the ACM in 2006. Before it, lock-free hash tables either had a fixed number of buckets, like Michael's 2002 table, or needed to move keys during a resize, which is hard to do without locks. The idea of recursive split ordering, which the paper describes as moving the buckets among the items instead of the items among the buckets, gave the first practical lock-free extensible hash table. Herlihy and Shavit made it a chapter of their textbook.

## References
