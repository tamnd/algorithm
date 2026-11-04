---
tag: MJA5FE
kind: technique
slug: lazy-deletion
name: Lazy deletion
aliases:
- Tombstone deletion
- lazy deletion
- tombstones
area: data-structures/hashing
level: intro
summary: Mark deleted slots instead of emptying them, so probe sequences stay intact.
prereqs: [open-addressing, probe-sequence]
see_also: [linear-probing, rehashing, load-factor, double-hashing, quadratic-probing, robin-hood-hashing, swiss-table, dijkstra]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.4, Open addressing (deletion with the special value DELETED)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4, Hashing (the discussion of deletions, and Algorithm R for linear probing)
  - url: https://arxiv.org/abs/2107.01250
    title: Michael A. Bender, Bradley C. Kuszmaul and William Kuszmaul, Linear probing revisited, tombstones mark the death of primary clustering (2021)
    locator: abstract and introduction (tombstones and graveyard hashing)
---

Lazy deletion removes a key from an [open addressing](/open-addressing/) hash table by writing a special mark, a tombstone, into its slot, instead of making the slot empty. A search treats a tombstone as full and walks past it, so the [probe sequences](/probe-sequence/) of other keys stay unbroken; an insert may reuse it. The method works for every probe rule, but tombstones make searches longer, so the table counts them and is rebuilt by [rehashing](/rehashing/) when live keys plus tombstones pass a fixed [load factor](/load-factor/). The same idea, mark now and clean up in bulk later, also appears in priority queues and search trees.

## In plain words

A search in an open addressing table stops at the first empty slot, because the key would have been placed there. If a deletion makes a slot empty, a key that was placed after that slot, on a route that passes through it, can no longer be found.

So a deletion does not empty the slot. It puts a sign there that says "this slot was used, keep going". Searches walk past the sign. An insert can put a new key on a sign, so the space is not lost for good.

Signs pile up after many deletions, and searches must walk past all of them. So the table counts its signs, and when there are too many, it builds a new table with only the live keys and no signs.

## When it applies

- A structure finds an item by a walk that stops at a "nothing here" mark, and removing an item would turn its place into such a mark. Open addressing with any probe rule is the main case.
- Repairing the structure at the moment of deletion is complex or slow: for [double hashing](/double-hashing/) or [quadratic probing](/quadratic-probing/) there is no cheap way to find the keys whose sequences pass through a slot.
- A periodic rebuild is affordable, so the cost of cleaning up can be spread over many operations.

For [linear probing](/linear-probing/) and [Robin Hood hashing](/robin-hood-hashing/), a backward-shift deletion repairs the run at once and needs no tombstone, which is often better.

## The template

The table $T[0 \ldots m-1]$ has three kinds of slot: EMPTY, DELETED (a tombstone) and a live key. The counters $n$ and $d$ are the numbers of live keys and of tombstones. The probe rule $h(k, i)$ gives a complete probe sequence.

```pseudo id=main
SEARCH(T, k)
L1  for i ← 0 to m − 1 do
L2      j ← h(k, i)
L3      if T[j] = EMPTY then return NIL
L4      if T[j] = k then return j        ▷ a DELETED slot is passed over
L5  return NIL

DELETE(T, k)
L6  j ← SEARCH(T, k)
L7  if j = NIL then return
L8  T[j] ← DELETED, n ← n − 1, d ← d + 1

INSERT(T, k)
L9  first ← NIL
L10 for i ← 0 to m − 1 do
L11     j ← h(k, i)
L12     if T[j] = k then return j        ▷ already present
L13     if T[j] = DELETED and first = NIL then first ← j
L14     if T[j] = EMPTY then break
L15 if first ≠ NIL then T[first] ← k, d ← d − 1     ▷ reuse a tombstone
L16 else if T[j] = EMPTY then T[j] ← k
L17 else error "table full"
L18 n ← n + 1
L19 if n + d > β · m then REBUILD(T)    ▷ hole: the threshold β < 1

REBUILD(T)
L20 make a new table of size m′ with n / m′ ≤ γ, where γ < β   ▷ hole: the new size
L21 insert each live key of T into it; d ← 0
```

**The invariant.** For each live key $x$ at slot $h(x, i)$, the slots $h(x, 0), \ldots, h(x, i-1)$ are not EMPTY. A slot changes from DELETED to EMPTY only in a rebuild, and line L8 changes a live slot to DELETED, not to EMPTY, so no operation creates an EMPTY slot on the path of a live key. Line L15 puts $k$ on a tombstone that lies before the first EMPTY slot of its sequence, so the slots that $k$ passed are not EMPTY. This is why line L3 may stop the search.

**Why insert scans to EMPTY.** The loop of line L10 does not stop at the first tombstone. A copy of $k$ may already sit further on, past the tombstone. By the invariant, any copy of $k$ lies before the first EMPTY slot of its sequence, so the scan up to EMPTY settles the question, and only then does line L15 place $k$ in the first tombstone it saw.

**The cost.** A search walks over tombstones as if they were keys. So the cost of a failed search depends on the *effective* load factor $(n + d)/m$, not on $n/m$. Under the [uniform hashing assumption](/uniform-hashing-assumption/), with live keys and tombstones in random slots, it is at most $1/(1 - (n+d)/m)$ probes in expectation. Line L19 keeps $(n + d)/m \le \beta$, so every operation stays at $O(1/(1-\beta))$ expected probes.

**The cost of rebuilds.** A delete does not change $n + d$, and an insert raises it by at most 1. After a rebuild, $n + d = n \le \gamma m'$. The next rebuild needs $n + d > \beta m'$, so at least $(\beta - \gamma) m'$ inserts come between two rebuilds. A rebuild costs $O(m')$ expected time. So its amortized cost is $O(1/(\beta - \gamma))$ per insert, which is $O(1)$ for fixed constants.

### Example

Take $m = 7$, $h(k, i) = (k + i) \bmod 7$ (linear probing with $h'(k) = k \bmod 7$), and $\beta = 3/4$.

| step | probes | slots 0 to 6 after the step | $n$ | $d$ |
|---|---|---|---|---|
| insert 10, 17, 24 | 3; 3, 4; 3, 4, 5 | E E E 10 17 24 E | 3 | 0 |
| delete 17 | 3, 4 | E E E 10 D 24 E | 2 | 1 |
| search 24 | 3, 4, 5 | unchanged | 2 | 1 |
| insert 31 | 3, 4, 5, 6 | E E E 10 31 24 E | 3 | 0 |
| delete 10 | 3 | E E E D 31 24 E | 2 | 1 |
| delete 24 | 3, 4, 5 | E E E D 31 D E | 1 | 2 |
| search 38 | 3, 4, 5, 6 | unchanged | 1 | 2 |

Here "E" is EMPTY and "D" is DELETED. The search for 24 passes the tombstone at slot 4. The insert of 31 notes the tombstone at slot 4, goes on to the EMPTY slot 6 to make sure 31 is not further on, and then puts 31 at slot 4. At the end the table holds one live key, but the search for the absent key 38 (home 3) still takes 4 probes, as many as with three keys. Each count $n + d$ stays at most 3, below $\beta m = 5.25$, so there is no rebuild.

## Classic examples

- **Open addressing in general.** CLRS gives the DELETED mark as the standard deletion for open addressing, with the remark that search times then no longer depend on the load factor alone. It is the deletion of choice for [double hashing](/double-hashing/) and [quadratic probing](/quadratic-probing/).
- **[Linear probing](/linear-probing/) with tombstones.** Many production tables use tombstones even with linear probing, for simple code. Bender, Kuszmaul and Kuszmaul showed that tombstones left between rebuilds work against primary clustering, and their graveyard hashing places tombstones on purpose at each rebuild to get $O(x)$ expected cost per operation at load factor $1 - 1/x$.
- **[Swiss table](/swiss-table/).** A deleted slot gets a special control byte, so that probes over its group go on.
- **[Dijkstra's algorithm](/dijkstra/) with a plain binary heap.** Instead of a decrease-key, push a new entry with the smaller distance and leave the old one in the heap. When an entry is popped for a vertex that is already finished, skip it. The heap then has $O(m)$ entries for a graph with $m$ edges, and the time is $O(m \log m)$, which is $O(m \log n)$.

## Variations

- **Backward-shift deletion.** For linear probing, Knuth's Algorithm R moves later keys of the run back into the hole and leaves no tombstone. Robin Hood hashing has a similar backward shift. No rebuild for tombstones is needed.
- **Rebuild in place.** Instead of a new array, a rebuild can sweep the table and reinsert the keys in place, which saves memory but needs care with keys that are moved twice.
- **Separate thresholds.** Rebuild at the same size when $d$ alone gets large (many deletions), and grow when $n$ gets large. This keeps the memory in line with the live keys.
- **Turning a tombstone back into EMPTY.** If the slot after a tombstone is EMPTY and the probe rule is linear, no live key's path can pass the tombstone into that EMPTY slot, so the tombstone may become EMPTY. This shortens runs of tombstones at the end of a cluster.
- **Lazy deletion in search trees and heaps.** Mark a node as deleted, skip it in queries, and rebuild the whole structure when half of its nodes are marked. The rebuild costs are amortized as above.

## Pitfalls

- **Stopping at the first tombstone on insert.** If INSERT puts $k$ in the first DELETED slot without scanning on to EMPTY, it can make a second copy. In the example, after "delete 10", inserting 24 that way puts it at slot 3 while 24 is still at slot 5. A later delete of 24 removes only the copy at slot 3, and 24 seems to come back.
- **Treating a tombstone as EMPTY in search.** This is the bug that lazy deletion exists to avoid: line L3 must test for EMPTY only.
- **Not counting tombstones.** If the rebuild test of line L19 uses $n$ alone, a table under a steady mix of inserts and deletes fills up with tombstones. When no EMPTY slot is left, every failed search probes all $m$ slots, and an insert of a new key may fail.
- **Growing on tombstones.** If the trigger counts $n + d$ but each rebuild doubles the size, a workload with many deletions makes the table grow without more live keys. Pick the new size from $n$ in line L20.
- **Reusing a tombstone with the wrong probe rule.** Line L15 is safe only because the tombstone lies on the probe sequence of $k$ before its first EMPTY slot. Moving $k$ to some other free slot breaks the invariant.

## Exercises

1. Prove that the table in the example could not have kept the search for 24 correct if "delete 17" had written EMPTY. Which line of the template saves it?
2. With linear probing, show that a tombstone followed directly by an EMPTY slot can be changed to EMPTY without breaking any search.
3. Give a sequence of $2m$ operations on a table of size $m$ that never holds more than one live key but leaves no EMPTY slot, if the rebuild test counts only live keys.
4. Show that with $\beta = 3/4$ and $\gamma = 1/4$, at least $m'/2$ inserts happen between two rebuilds, where $m'$ is the size chosen by the first of the two.

## References
