---
tag: X9QTNE
kind: concept
slug: load-factor
name: Load factor
aliases:
- alpha
- fill ratio
- load
area: data-structures/hashing
level: intro
summary: Ratio of stored keys to table slots, which governs expected probe or chain length.
prereqs: [hash-table]
see_also: [separate-chaining, open-addressing, rehashing, uniform-hashing-assumption, linear-probing-analysis, lazy-deletion, balls-into-bins]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.2 (the load factor and the analysis of chaining) and Section 11.4 (the analysis of open addressing)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4, Hashing (the load factor and the costs of chaining, linear probing and uniform probing)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4, Hash Tables (array resizing in SeparateChainingHashST and LinearProbingHashST)
  - url: https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/HashMap.java
    title: OpenJDK source, java.util.HashMap
    locator: the constants DEFAULT_INITIAL_CAPACITY and DEFAULT_LOAD_FACTOR, and the method resize
  - url: https://github.com/python/cpython/blob/main/Objects/dictobject.c
    title: CPython source, Objects/dictobject.c
    locator: the macros USABLE_FRACTION and GROWTH_RATE
  - url: https://github.com/abseil/abseil-cpp/blob/master/absl/container/internal/raw_hash_set.h
    title: Abseil source, absl/container/internal/raw_hash_set.h
    locator: the function CapacityToGrowth
---

The load factor of a [hash table](/hash-table/) is the number $\alpha = n/m$, where $n$ is the number of stored keys and $m$ is the number of slots. It is the single number that controls the expected cost of a search: with [separate chaining](/separate-chaining/) the expected length of a chain is $\alpha$, and with [open addressing](/open-addressing/) the expected number of probes grows like a power of $1/(1 - \alpha)$. A table keeps its load factor between two bounds by [rehashing](/rehashing/), and the choice of the upper bound is a trade between time and memory.

## In plain words

A hash table has a fixed number of slots, and it holds some number of keys. The load factor tells you how full the table is: the number of keys divided by the number of slots. A load factor of one half means one key for every two slots.

When the table is nearly empty, a new key almost always finds its own free place, and a search looks at one place. When the table gets full, keys collide more often, and a search must look at more places before it finds the key or gives up. So each table picks a limit. When the load goes above the limit, the table moves to a bigger array. A low limit makes searches fast but wastes memory. A high limit saves memory but makes searches slower.

## The idea

**Definition.** For a table with $m \ge 1$ slots that holds $n \ge 0$ keys, the load factor is $\alpha = n/m$. With chaining, $\alpha$ can be any non-negative number. With open addressing, each slot holds at most one key, so $0 \le \alpha \le 1$. A table with buckets of $b$ entries in each slot often uses $\alpha = n/(bm)$, so that $\alpha \le 1$ again means "not over capacity".

**Why one number is enough.** Under the [uniform hashing assumption](/uniform-hashing-assumption/), the expected cost of an operation depends on $n$ and $m$ only through $\alpha$, up to terms that vanish as $m$ grows. The standard results are in the table below. Here "keys" counts the keys that a search of a chain compares with, and "probes" counts the slots that an open-addressing search looks at.

| scheme | unsuccessful search | successful search | source of the formula |
|---|---|---|---|
| chaining | $\alpha$ keys | $1 + \alpha/2 - \alpha/(2n)$ keys | [separate chaining](/separate-chaining/) |
| uniform probing | at most $1/(1-\alpha)$ probes | at most $(1/\alpha)\ln(1/(1-\alpha))$ probes | [uniform hashing assumption](/uniform-hashing-assumption/) |
| linear probing | about $\frac{1}{2}\bigl(1 + 1/(1-\alpha)^2\bigr)$ probes | about $\frac{1}{2}\bigl(1 + 1/(1-\alpha)\bigr)$ probes | [analysis of linear probing](/linear-probing-analysis/) |

For chaining the cost grows linearly in $\alpha$, so a load of 2 or 5 still works. For open addressing the cost has a pole at $\alpha = 1$, so the load must stay below a constant less than 1.

**Why the load is kept between two bounds.** If a table never grows, $\alpha = n/m$ grows with $n$, and the cost per operation is no longer constant. If it grows by a constant factor each time $\alpha$ passes an upper bound $\alpha_{\max}$, and shrinks when $\alpha$ falls below a lower bound $\alpha_{\min} < \alpha_{\max}/2$, then $\alpha$ stays in a fixed range and the cost of the rebuilds is $O(1)$ amortized per operation. The [rehashing](/rehashing/) page proves this. The space is then $\Theta(n)$, because $m \le n/\alpha_{\min}$ when the table is above its minimum size.

**Effective load with deletions.** In open addressing with [lazy deletion](/lazy-deletion/), a deleted key leaves a tombstone. An unsuccessful search must pass the tombstones as well as the keys, so its cost depends on $(n + d)/m$, where $d$ is the number of tombstones. A table must count the tombstones in its rule for a rebuild, or a sequence of inserts and deletes can fill every slot and make an unsuccessful search loop forever.

**Load and the longest chain.** The load factor controls the average, not the worst case. With chaining and $n = m$ under random hashing, the average chain has one key, but the longest chain has $\Theta(\log n / \log \log n)$ keys with high probability. This is the maximum load of [balls into bins](/balls-into-bins/).

## Examples

**Costs for some loads.** The values of the formulas of the table above:

| $\alpha$ | chaining, unsuccessful | chaining, successful | uniform, unsuccessful | uniform, successful | linear, unsuccessful | linear, successful |
|---|---|---|---|---|---|---|
| 0.25 | 0.25 | 1.125 | 1.333 | 1.151 | 1.389 | 1.167 |
| 0.5 | 0.5 | 1.25 | 2 | 1.386 | 2.5 | 1.5 |
| 0.75 | 0.75 | 1.375 | 4 | 1.848 | 8.5 | 2.5 |
| 0.9 | 0.9 | 1.45 | 10 | 2.558 | 50.5 | 5.5 |
| 0.95 | 0.95 | 1.475 | 20 | 3.153 | 200.5 | 10.5 |

The chaining column ignores the term $\alpha/(2n)$. From $\alpha = 0.5$ to $\alpha = 0.9$, an unsuccessful search of linear probing becomes about 20 times as expensive, while chaining changes little.

**Memory for some loads.** Take 8-byte keys and 8-byte pointers, and ignore the values. An open-addressing table uses $8/\alpha$ bytes per key: 16 bytes at $\alpha = 1/2$, 12 bytes at $\alpha = 2/3$ and about 9.14 bytes at $\alpha = 7/8$. A chained table uses $8/\alpha$ bytes per key for the heads, and 16 bytes per node for the key and the next pointer: 32 bytes at $\alpha = 1/2$ and 24 bytes at $\alpha = 1$, before the overhead of the memory allocator. So open addressing at a moderate load often uses less memory than chaining at a high load.

**Java `HashMap`.** The default table has 16 slots and the default maximum load is $0.75$. So it holds 12 keys at $\alpha = 0.75$, and the insertion of the 13th key, which would make $\alpha = 13/16 = 0.8125$, doubles the table to 32 slots.

**CPython `dict`.** The macro `USABLE_FRACTION(n)` is $\lfloor 2n/3 \rfloor$, so the index table of a `dict` is at most two thirds full. When it is full, the new size is computed from three times the number of keys in use.

**Sedgewick and Wayne.** Their linear-probing table doubles when $n \ge m/2$ and halves when $n \le m/8$, so $1/8 \le \alpha \le 1/2$ for a table above its minimum size. Their chaining table doubles when $n \ge 10m$ and halves when $n \le 2m$, so its chains have between 2 and 10 keys on average.

**A non-example.** The fraction of nonempty slots is not the load factor. In the chained table of the example on the [separate chaining](/separate-chaining/) page, 11 keys are in 11 slots, so $\alpha = 1$, but only 6 of the 11 slots are in use.

## Where it is used

- [Separate chaining](/separate-chaining/) and [open addressing](/open-addressing/) state their costs as functions of $\alpha$.
- [Rehashing](/rehashing/) and [linear hashing](/linear-hashing/) use a bound on $\alpha$ as the trigger for growth.
- [Linear probing](/linear-probing/), [quadratic probing](/quadratic-probing/), [double hashing](/double-hashing/) and [Robin Hood hashing](/robin-hood-hashing/) differ mainly in how fast their costs grow as $\alpha$ tends to 1.
- [Cuckoo hashing](/cuckoo-hashing/) with two tables works only below a load of one half. The [cuckoo hashing load threshold](/cuckoo-hashing-load-threshold/) page gives the limits for other variants.
- A [Swiss table](/swiss-table/) in Abseil uses a maximum load of $7/8$ for all but the smallest tables. Its probes look at a group of slots at a time, so a high load costs less than in plain linear probing.
- The [Bloom filter](/bloom-filter/) has an analogue: the ratio of stored items to bits fixes the best number of hash functions and the false positive rate.

## References
