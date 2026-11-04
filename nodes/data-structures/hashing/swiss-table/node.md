---
tag: 5PH332
kind: data-structure
slug: swiss-table
name: Swiss table
aliases:
- SwissTable
- abseil flat hash map
- flat hash map
area: data-structures/hashing
level: advanced
summary: Cache-friendly open-addressing table that uses SIMD group probing and control bytes.
implements: [dictionary]
model: word-ram
complexity:
  vars: {m: the number of slots, n: the number of keys, W: the group width}
  time: {worst: Θ(m), expected: O(1), best: Θ(1)}
  space: {extra: Θ(m)}
history:
  year: 2017
  people: [Sam Benzaquen, Alkis Evlogimenos, Matt Kulukundis, Roman Perepelitsa]
  note: Google engineers built the Swiss table for the Abseil C++ library. Matt Kulukundis presented it at CppCon 2017. Rust (2019) and Go (2025) later moved their standard hash maps to the same design.
prereqs: [open-addressing, quadratic-probing, lazy-deletion]
see_also: [linear-probing, robin-hood-hashing, hash-table, load-factor, rehashing, hopscotch-hashing, cuckoo-hashing, extendible-hashing]
sources:
  - url: https://abseil.io/about/design/swisstables
    title: Abseil, Swiss Tables Design Notes
    note: control bytes, the split of the hash into H1 and H2, groups of 16 with SSE2, tombstones, the maximum load of 7/8
  - url: https://github.com/abseil/abseil-cpp/blob/master/absl/container/internal/raw_hash_set.h
    title: Abseil, raw_hash_set.h, with hashtable_control_bytes.h and raw_hash_set.cc in the same directory
    note: the values kEmpty = -128, kDeleted = -2, kSentinel = -1, the triangular probe sequence over groups, capacity 2^N − 1, the cloned control bytes, and the erase rule of WasNeverFull
  - url: https://www.youtube.com/watch?v=ncHmEUmJZf4
    title: Matt Kulukundis, Designing a Fast, Efficient, Cache-friendly Hash Table, Step by Step, CppCon 2017
  - url: https://blog.rust-lang.org/2019/07/04/Rust-1.36.0/
    title: The Rust Release Team, Announcing Rust 1.36.0 (2019)
    note: the standard HashMap moves to hashbrown, a port of the Swiss table
  - url: https://go.dev/blog/swisstable
    title: Michael Pratt, Faster Go maps with Swiss Tables, The Go Blog, 2025
    note: Go 1.24 maps use groups of 8 slots with a 64-bit control word, a maximum load of 7/8, and many small tables
---

A Swiss table is an [open-addressing](/open-addressing/) [hash table](/hash-table/) that keeps one control byte for each slot, in a separate array. The control byte says that the slot is EMPTY, DELETED, or full, and for a full slot it holds 7 bits of the key's hash. The slots are cut into groups of $W$ slots, for example $W = 16$. A search compares the 7 bits of its key with all $W$ control bytes of a group in one SIMD instruction, and it reads a key only where the bits match. The probe sequence moves from group to group in the triangular order of [quadratic probing](/quadratic-probing/), and it stops at the first group that holds an EMPTY slot. The table grows when $7/8$ of its slots are full or DELETED.

## In plain words

Picture a hotel with rooms in rows of 16. Next to each row is a small board with one light for each room. A light is off for an empty room, red for a room that was given back, and shows a short code for a room in use. The code is a small part of the guest's name.

To find a guest, the clerk goes to the row the guest's name points to and reads the whole board at once. Only rooms that show the guest's code are worth a knock. If the row has an empty room, the guest would have taken it, so the search ends. If not, the clerk goes to another row, by a fixed rule, and does the same.

Most searches read one board and knock on one door. The board is small, so it is fast to read.

## The abstract type

A Swiss table implements the [dictionary](/dictionary/) abstract type on a finite map $D$ with distinct keys: `insert(T, k, v)` sets $D(k) = v$, `find(T, k)` returns the slot of $k$ (or NIL), `erase(T, k)` removes $k$, and `size(T)` returns $n = |D|$. It needs only an equality test and a [hash function](/hash-function/) on the keys, and it does not support ordered queries.

## Representation

This page describes a simple form of the Abseil design, the form that the Python version implements. The section on variants lists what Abseil does differently.

The fields are:

- the group width $W$ and the number of groups $G$, a power of two, so the table has $m = GW$ slots, and group $g$ is the slots $gW, \ldots, gW + W - 1$;
- an array $\text{ctrl}[0 \ldots m-1]$ of control bytes. Each byte is EMPTY ($-128$, the bits $10000000$), DELETED ($-2$, the bits $11111110$), or a number $0 \le c < 128$ for a full slot. These are the values of Abseil; the sign bit marks a slot that is not full;
- arrays $\text{key}[0 \ldots m-1]$ and $\text{value}[0 \ldots m-1]$;
- the count $n$ of full slots and the count $d$ of DELETED slots.

A 64-bit hash $h$ of a key is cut into two parts: $h_2$ is its low 7 bits, and $h_1 = \lfloor h / 128 \rfloor$ is the other 57 bits. The probe sequence of a key visits the groups

$$g_i = \left(h_1 + \tfrac{i(i+1)}{2}\right) \bmod G, \qquad i = 0, 1, 2, \ldots$$

As $G$ is a power of two, $g_0, \ldots, g_{G-1}$ are all $G$ groups, each one once (Lemma 1 of [the quadratic probing proof](/quadratic-probing/)). Let $\text{MaxFill}(m) = \min(\lfloor 7m/8 \rfloor, m - 1)$.

**Invariant.**

- **(S1) Control bytes.** A slot is full exactly when its control byte is in $\{0, \ldots, 127\}$, and then the byte is $h_2$ of its key. No key occurs in two slots. $n$ and $d$ are the numbers of full and of DELETED slots.
- **(S2) No EMPTY slot before a key.** If key $k$ is in group $g_j$ of its probe sequence, where $j$ is the first index with that group, then none of the groups $g_0, \ldots, g_{j-1}$ holds an EMPTY slot.
- **(S3) Room.** $n + d \le \text{MaxFill}(m)$, so at least one slot is EMPTY.

The map is $D = \{(\text{key}[s], \text{value}[s]) : \text{slot } s \text{ is full}\}$.

## Operations

```pseudo id=main
SWISS-FIND(T, k)
L1  (h1, h2) ← the two parts of hash(k); g ← h1 mod G; i ← 0
L2  loop
L3      M ← the slots s of group g with ctrl[s] = h2          ▷ one SIMD compare
L4      if some s in M has key[s] = k then return s
L5      if group g has an EMPTY slot then return NIL
L6      i ← i + 1; g ← (g + i) mod G

SWISS-INSERT(T, k, v)
L7  s ← SWISS-FIND(T, k)
L8  if s ≠ NIL then value[s] ← v; return
L9  if n + d + 1 > MaxFill(m) then REBUILD(T)
L10 (h1, h2) ← the two parts of hash(k); g ← h1 mod G; i ← 0
L11 while group g has no EMPTY slot and no DELETED slot
L12     i ← i + 1; g ← (g + i) mod G
L13 s ← the first EMPTY or DELETED slot of group g
L14 if ctrl[s] = DELETED then d ← d − 1
L15 ctrl[s] ← h2; key[s] ← k; value[s] ← v; n ← n + 1

SWISS-ERASE(T, k)
L16 s ← SWISS-FIND(T, k)
L17 if s = NIL then return false
L18 if the group of s has an EMPTY slot then ctrl[s] ← EMPTY
L19 else ctrl[s] ← DELETED; d ← d + 1
L20 n ← n − 1; return true

REBUILD(T)
L21 G′ ← G; while 2(n + 1) > MaxFill(G′W) do G′ ← 2G′
L22 make a table of G′ groups with all slots EMPTY and d = 0; put each old pair in it by lines L10 to L15
```

**Find.** Line L3 is the step that makes the table fast. With $W = 16$ and SSE2, it is three instructions: `_mm_set1_epi8(h2)` puts $h_2$ in all 16 bytes of a register, `_mm_cmpeq_epi8` compares them with the 16 control bytes, and `_mm_movemask_epi8` turns the result into a 16-bit mask with one bit for each match. Line L4 compares keys only at the bits of this mask. EMPTY and DELETED have the sign bit set, so they never equal $h_2$. Line L5 is a second SIMD compare, with EMPTY. The search stops only at a group with an EMPTY slot. A DELETED slot acts as a full slot that never matches.

**Insert.** Lines L7 and L8 replace the value of a key that is present. Line L9 keeps (S3). Lines L10 to L12 follow the same probe sequence and stop at the first group with a free slot, EMPTY or DELETED. Line L13 takes a free slot of that group, and line L14 reuses a tombstone if it is one.

**Erase.** A probe for another key may have passed over the group of $s$ only if that group had no EMPTY slot at the time. If the group holds an EMPTY slot now, it held one at each moment since the table was built (see the correctness proof), so no probe passed over it and line L18 can make the slot EMPTY at once. Otherwise line L19 leaves a tombstone, as in [lazy deletion](/lazy-deletion/).

**Rebuild.** Lines L21 and L22 rehash all keys into a table with no tombstones. If the keys fit in half of the new MaxFill, the size stays the same, and the rebuild only removes the tombstones. Otherwise the number of groups doubles until they fit.

## Example

Take $W = 4$ and $G = 4$, so $m = 16$ and $\text{MaxFill}(16) = 14$. To keep the numbers small, let $\text{hash}(k) = k$, so $h_2 = k \bmod 128$ and $h_1 = \lfloor k / 128 \rfloor$. The probe sequence from group 0 is 0, 1, 3, 2.

Insert 3, 7, 131, 11, 15, 19, 23 and 27. All keys except 131 have $h_1 = 0$. The key 131 has $h_1 = 1$ and $h_2 = 3$.

| step | group 0 | group 1 | group 2 | group 3 |
|---|---|---|---|---|
| insert 3, 7 | 3 7 · · | · · · · | · · · · | · · · · |
| insert 131 | 3 7 · · | 131 · · · | · · · · | · · · · |
| insert 11, 15 | 3 7 11 15 | 131 · · · | · · · · | · · · · |
| insert 19, 23, 27 | 3 7 11 15 | 131 19 23 27 | · · · · | · · · · |
| erase 7 | 3 D 11 15 | 131 19 23 27 | · · · · | · · · · |
| erase 27 | 3 D 11 15 | 131 19 23 D | · · · · | · · · · |
| insert 35 | 3 35 11 15 | 131 19 23 D | · · · · | · · · · |

The cells show the keys, "·" for EMPTY and "D" for DELETED. After the first eight inserts, the control bytes of groups 0 and 1 are 3 7 11 15 and 3 19 23 27.

- **find 27.** Group 0 has no byte 27 and no EMPTY slot. Group 1 has the byte 27 at slot 7, and the key there is 27.
- **find 259.** Here $h_1 = 2$, and group 2 has no match and an EMPTY slot, so the answer is NIL after one group.
- **find 1027.** Here $h_1 = 8 \equiv 0$ and $h_2 = 3$. In group 0 the byte 3 matches at slot 0, but the key is 3, not 1027. Group 0 has no EMPTY slot. In group 1 the byte 3 matches again, at the key 131. Group 1 has no EMPTY slot. Group 3 has no match and an EMPTY slot, so the answer is NIL. Two key comparisons were wasted on matches of 7 bits.
- **erase 7.** Group 0 has no EMPTY slot, so slot 1 becomes DELETED. A later find 27 still goes past group 0 to group 1.
- **erase 27.** Group 1 has no EMPTY slot either, so slot 7 becomes DELETED.
- **insert 35.** Group 0 is the first group of its sequence with a free slot, and slot 1 is DELETED, so 35 takes it, and $d$ goes from 2 to 1.

If, in a new table, we insert 3 and 7 and then erase 3, group 0 still has two EMPTY slots, so slot 0 becomes EMPTY and no tombstone is left.

## Correctness

The invariant (S1) to (S3) holds for the empty table and is kept by each operation. A find for $k$ goes through the groups of its probe sequence in order. By (S2), every group before the group of $k$ has no EMPTY slot, so the search does not stop there, and at the group of $k$ the byte $h_2$ matches and the key compare succeeds. For a key that is not present, the search stops at a group with an EMPTY slot, which it meets within $G$ groups because (S3) gives an EMPTY slot and the probe sequence covers all groups. Insert puts the key in the first group of its sequence with a free slot, so the groups before it are full, which gives (S2) for the new key. The key fact for erase is that a group with no EMPTY slot never gets one again until a rebuild: insert never writes EMPTY, and line L18 writes EMPTY only in a group that has an EMPTY slot. So a group that holds an EMPTY slot was never a group that (S2) needs, and making a slot EMPTY there breaks nothing. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Worst case.** A find can go through all $G$ groups and compare $k$ with all $m$ keys, for example when all keys have the same $h_1$ and $h_2$. So each operation takes $\Theta(m)$ time in the worst case. A rebuild takes $\Theta(m)$ time.

**Expected cost.** No published theorem covers the Swiss table as such. If the start groups $h_1 \bmod G$ of the keys are independent and uniform, the table behaves like quadratic probing with buckets of $W$ slots, and the 7 bits of $h_2$ give a wrong match with probability $1/128$ for each full slot that the search compares. So a group costs one SIMD compare and, on average, $W\alpha/128$ wasted key compares at load $\alpha$. The table below is a simulation of the Python version with $W = 16$, $G = 1024$ ($m = 16384$) and random 64-bit hashes, with all keys found once (successful) and 20000 absent keys (unsuccessful).

| load $\alpha$ | groups, successful | key compares, successful | groups, unsuccessful | key compares, unsuccessful |
|---|---|---|---|---|
| 0.5 | 1.000 | 1.033 | 1.005 | 0.064 |
| 0.75 | 1.029 | 1.046 | 1.276 | 0.127 |
| 0.875 | 1.099 | 1.063 | 2.098 | 0.230 |

So at the maximum load of $7/8$, a successful find reads about 1.1 groups and an unsuccessful find about 2.1 groups. The expected $O(1)$ of the front matter is the observed cost at a load of at most $7/8$, not a proved bound.

**Rebuild.** After a rebuild, $n + 1 \le \text{MaxFill}(m)/2$ and $d = 0$. Each insert adds at most 1 to $n + d$, and an erase does not add to it, so at least $\text{MaxFill}(m)/2 = \Theta(m)$ inserts come before the next rebuild. The $\Theta(m)$ cost of a rebuild is therefore $O(1)$ amortized for each insert.

**Space.** The table has $m$ slots and $m$ control bytes, one byte of overhead for each slot. The load is at most $7/8$, and after a doubling at least about $7/32$, so $m = \Theta(n)$ while the table only grows.

| operation | cost |
|---|---|
| find, erase | $\Theta(m)$ worst case; about 1 to 2 groups at load $\le 7/8$ in the simulation |
| insert | as find, plus $O(1)$ amortized for rebuilds |
| rebuild | $\Theta(m)$ |
| space | $m$ slots and $m$ control bytes |

## Variants

- **Abseil's layout.** Abseil uses a capacity of the form $2^N - 1$ and does not align the groups. A probe position is a slot index, and the group is the $W$ control bytes that start there. The control array is $\text{ctrl}[0 \ldots m-1]$, then one SENTINEL byte ($-1$), then copies of the first $W - 1$ bytes, so that a group that starts near the end can be read with one load. The probe sequence is $p(i) = (h_1 + W \cdot i(i+1)/2) \bmod (m + 1)$, which visits every group once because the number of groups is a power of two.
- **Abseil's erase rule.** Abseil leaves a tombstone only when a window of $W$ slots with no EMPTY slot can cover the erased slot. It counts the slots that are not EMPTY just before and just after the erased slot, and if the two counts add up to less than $W$, no probe can have gone past the slot, and it marks it EMPTY.
- **Abseil's load.** The maximum load is $7/8$ for large tables. Small tables, of less than about four groups, allow all slots but one to be full, and a table of less than one group can be full. When tombstones fill much of the table, Abseil rehashes in place instead of growing.
- **The hash split.** Abseil's design notes describe $h_1$ as 57 bits and $h_2$ as the other 7 bits. Which bits form each part has changed between versions; any split works if both parts are well mixed.
- **Portable groups.** Without SIMD, a group of 8 control bytes fits in one 64-bit word, and bit tricks find the bytes that equal $h_2$. Go 1.24 uses such groups of 8 slots, with each map split into many small Swiss tables of at most 1024 entries, so that growth copies only one small table.
- **Rust.** The `hashbrown` crate is a port of the Swiss table, and it became the standard `HashMap` of Rust in version 1.36 (2019). Before that, the standard map used [Robin Hood hashing](/robin-hood-hashing/).

## When to use it

Use a Swiss table as the general-purpose hash map of a program when the keys are small, the hash function is good, and speed matters. The control bytes are dense, so a probe reads one cache line of metadata, and the slots hold the pairs inline, so there are no pointers to follow as in [chaining](/hash-table/). It works at a high load of $7/8$ with short probes. Do not use it when the hash is weak, because a bad hash puts many keys in the same groups and $h_2$ then also matches often. Do not use it when references to elements must stay valid across inserts: a rebuild moves every pair. For many erases in a nearly full table, [Robin Hood hashing](/robin-hood-hashing/) with backward shift avoids tombstones.

## Pitfalls

- **An EMPTY slot on every erase.** If line L18 always wrote EMPTY, a search for a key that was placed after a full group would stop early at the new EMPTY slot. In the example, making slot 1 EMPTY at erase 7 would make find 27 stop at group 0 and return NIL.
- **Not counting tombstones.** If line L9 tests only $n$, tombstones can fill all EMPTY slots, and then an unsuccessful find never stops. Count $n + d$ against MaxFill, as (S3) does.
- **Stopping on a group with no match.** A group with no byte equal to $h_2$ is not the end of the search. Only an EMPTY slot ends it.
- **Insert without a find.** If an insert puts the key in the first free slot without a find, a key that is already present after a tombstone gets a second copy. Lines L7 and L8 prevent this.
- **The same bits in $h_1$ and $h_2$.** If $h_2$ is taken from the bits that choose the group, all keys of a group have related $h_2$ values, and the 7-bit filter stops working. Take the two parts from different bits.
- **A table size that is not a power of two groups.** The triangular sequence then misses some groups, and an insert can loop although the table has free slots.

## Implementations

The Python version is a class `SwissTable` with the methods `find`, `get`, `insert`, `erase` and `check_invariant`. It scans a group with a Python loop where a real table uses one SIMD compare. It uses the aligned groups of this page, not Abseil's unaligned layout. The tests use $W = 4$ and the identity hash to reproduce the example.

## History

The Swiss table was designed at Google by Sam Benzaquen, Alkis Evlogimenos, Matt Kulukundis and Roman Perepelitsa, and it became the hash map of Google's C++ code. Matt Kulukundis presented it at CppCon 2017. It was later released in the open-source Abseil library as `absl::flat_hash_map` and related types. Amanieu d'Antras ported it to Rust as `hashbrown`, which became the standard `HashMap` in Rust 1.36 in July 2019. Go 1.24, released in February 2025, uses Swiss tables for its built-in maps, based on the `swiss` package of Peter Mattis for CockroachDB.

## References
