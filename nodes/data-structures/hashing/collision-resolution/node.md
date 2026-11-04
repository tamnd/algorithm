---
tag: ZK26AP
kind: concept
slug: collision-resolution
name: Collision resolution
aliases:
- collision handling
area: data-structures/hashing
level: intro
summary: The general problem of storing keys that share a slot, with chaining or probing.
prereqs: [hash-collision, hash-function]
see_also: [separate-chaining, open-addressing, probe-sequence, linear-probing, double-hashing, cuckoo-hashing, load-factor, lazy-deletion]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.2 (collision resolution by chaining) and Section 11.4 (Open addressing)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the parts on collision resolution by chaining and by open addressing, and the analysis of the algorithms
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4 (Hash tables), hashing with separate chaining and hashing with linear probing
  - paper: doi:10.1147/rd.12.0130
    title: W. W. Peterson, Addressing for random-access storage, IBM Journal of Research and Development 1(2), 1957
    locator: pages 130 to 146 (open addressing and its measured and computed search lengths)
---

Collision resolution is the part of a [hash table](/hash-table/) that decides where to store a key when its slot, given by the [hash function](/hash-function/), already holds another key. Such [hash collisions](/hash-collision/) cannot be avoided when the universe of keys is larger than the table, so each hash table needs a rule for them. The two main families are chaining, which keeps a list of keys at each slot, and open addressing, which stores each key in the array itself and tries other slots in a fixed order. The choice of the rule, and the [load factor](/load-factor/), set the expected number of probes of each operation.

## In plain words

A hash function gives each key a home slot in a table. Sometimes two keys get the same home. Collision resolution is the rule that says what to do then.

One rule is to let a slot hold a short list. Each key goes on the list of its home slot, and a search reads that one list. The other rule is to keep one key per slot. If the home slot is taken, the key tries a second slot, then a third one, in an order that the rule fixes, until it finds a free slot. A search follows the same order and stops at the key, or at a free slot.

Both rules work well while the table has room to spare. They differ in memory use, in speed on real machines, and in how they handle removal of a key.

## The idea

Let the table have $m$ slots and hold $n$ keys, with load factor $\alpha = n/m$, and let $h(k)$ be the home slot of key $k$. A collision resolution method must meet one condition, so that a search can find each key:

> From $k$ and the contents of the table, a search can find the place of $k$ by looking at the slots in some sequence that starts at $h(k)$, and it can decide that $k$ is absent when the sequence reaches a place where $k$ would have to be.

**Chaining** (also called closed addressing, or "open hashing" in older texts). Slot $i$ holds a list of all the keys $k$ with $h(k) = i$. The search for $k$ scans the list of slot $h(k)$. The table can hold more keys than slots, so $\alpha$ can be larger than 1. See [separate chaining](/separate-chaining/).

**Open addressing** (also called "closed hashing"). Each slot holds at most one key, so $\alpha \le 1$. Each key $k$ has a [probe sequence](/probe-sequence/) $h(k, 0), h(k, 1), \ldots, h(k, m-1)$, a permutation of the slots that starts at $h(k, 0) = h(k)$. Insert puts $k$ in the first empty slot of its sequence. Search follows the same sequence and stops at $k$, or at an empty slot, which proves that $k$ is absent. See [open addressing](/open-addressing/). The common probe sequences are:

- [linear probing](/linear-probing/): $h(k, i) = (h(k) + i) \bmod m$;
- [quadratic probing](/quadratic-probing/): $h(k, i) = (h(k) + c_1 i + c_2 i^2) \bmod m$;
- [double hashing](/double-hashing/): $h(k, i) = (h_1(k) + i \cdot h_2(k)) \bmod m$, with $h_2(k)$ coprime to $m$.

**Other methods** relax "first empty slot". [Coalesced hashing](/coalesced-hashing/) stores the chains inside the array. [Robin Hood hashing](/robin-hood-hashing/) lets a key that is far from its home take the slot of a key that is closer to its home. [Hopscotch hashing](/hopscotch-hashing/) keeps each key within a fixed distance of its home. [Cuckoo hashing](/cuckoo-hashing/) gives each key two possible slots and moves keys between them, so that a search looks at only two slots.

**Expected cost.** The standard results, in the models of the pages linked, count the expected number of probes (slots or list entries examined) when $\alpha$ is a constant:

| method | unsuccessful search | successful search |
|---|---|---|
| chaining, [simple uniform hashing](/simple-uniform-hashing/) | $1 + \alpha$ (list entries, plus the slot) | $1 + \alpha/2 - \alpha/(2n)$ |
| open addressing, [uniform hashing](/uniform-hashing-assumption/) | at most $1/(1 - \alpha)$ | at most $(1/\alpha) \ln(1/(1 - \alpha))$ |
| linear probing, random hash values | about $\frac{1}{2}(1 + 1/(1 - \alpha)^2)$ | about $\frac{1}{2}(1 + 1/(1 - \alpha))$ |

The chaining results are in the [analysis of separate chaining](/chaining-analysis/). The bounds for uniform hashing are in CLRS Section 11.4, and the approximations for linear probing are from Knuth, Section 6.4. At $\alpha = 0.5$ the three unsuccessful costs are 1.5, 2 and 2.5. At $\alpha = 0.9$ they are 1.9, 10 and 50.5. So open addressing needs a load factor well below 1, and linear probing is the most sensitive to it, because full slots form long runs, called primary clusters.

**Deletion.** Under chaining, a delete removes the key from its list. Under open addressing, emptying a slot can cut the probe sequence of another key, and a later search would stop too early. The fixes are a tombstone mark that search skips and insert can reuse ([lazy deletion](/lazy-deletion/)), or, for linear probing, moving later keys of the run back into the gap.

## Examples

Take $m = 11$ slots, $h(k) = k \bmod 11$, and insert the keys 10, 22, 31, 4, 15, 28, 17 and 26, in this order, so $\alpha = 8/11$. The home slots are 10, 0, 9, 4, 4, 6, 6 and 4.

**Chaining.** The lists are: slot 0: [22]; slot 4: [4 15 26]; slot 6: [28 17]; slot 9: [31]; slot 10: [10]; the other slots are empty. A search for an absent key with home slot 4, such as 37, scans 3 list entries.

**Linear probing.** Key 15 finds slot 4 full and goes to 5. Key 28 goes to 6, its home. Key 17 finds 6 full and goes to 7. Key 26 finds 4, 5, 6 and 7 full and goes to 8, after 5 probes. The table is:

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| key | 22 | | | | 4 | 15 | 28 | 17 | 26 | 31 | 10 |

Slots 4 to 10 and slot 0 form one run of 8 full slots, since the probe sequence wraps around from 10 to 0. A search for 37 probes slots 4, 5, 6, 7, 8, 9, 10, 0 and then the empty slot 1: 9 probes.

**Double hashing** with $h_2(k) = 1 + (k \bmod 10)$, which is coprime to 11. Key 15 has step 6 and probes 4, 10 and 5, so it lands in slot 5 after 3 probes. Key 17 has step 8 and probes 6 and then 3. Key 26 has step 7 and probes 4, 0 and 7. The table is:

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| key | 22 | | | 17 | 4 | 15 | 28 | 26 | | 31 | 10 |

The keys with the same home slot 4 now follow different sequences, so they do not pile up in one run. A search for 37 has step 8 and probes slots 4, 1: 2 probes.

**A deletion bug.** In the linear-probing table, delete 15 by emptying slot 5. A search for 26 then probes slot 4 (key 4), finds slot 5 empty and reports 26 as absent, though 26 is in slot 8. A tombstone in slot 5 avoids this.

## Where it is used

- [Separate chaining](/separate-chaining/) is the method of Java's `HashMap` (which turns a long bucket into a balanced tree) and of the C++ `std::unordered_map`.
- [Open addressing](/open-addressing/) is the method of Python's `dict` (with a probe sequence that mixes in the high bits of the hash) and of the [Swiss table](/swiss-table/) of Abseil, which probes groups of slots.
- [Cuckoo hashing](/cuckoo-hashing/) and its [cuckoo filter](/cuckoo-filter/) form are used where a bound on the number of probes per search matters.
- [Linear hashing](/linear-hashing/) and [extendible hashing](/extendible-hashing/) resolve overflow of disk buckets in database indexes.
- [Perfect hashing](/perfect-hashing/) removes collisions on a fixed set of keys, so no resolution is needed at search time.

## References
