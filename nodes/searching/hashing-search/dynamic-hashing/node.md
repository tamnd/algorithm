---
tag: BQBB2X
kind: concept
slug: dynamic-hashing
name: Dynamic hashing
aliases:
- expandable hashing
area: searching/hashing-search
level: advanced
summary: Family of schemes that grow or shrink the table gradually without full rebuilds.
prereqs: [hash-table, load-factor, rehashing]
see_also: [extendible-hashing, linear-hashing, rehashing, trie, b-tree, external-memory-model, dynamic-perfect-hashing, array-doubling]
sources:
  - paper: doi:10.1007/BF01931695
    title: Per-Ake Larson, Dynamic hashing, BIT 18(2) (1978)
    locator: pages 184 to 201 (buckets addressed through a binary trie on the bits of a pseudorandom sequence, splitting and merging one bucket at a time)
  - paper: doi:10.1145/320083.320092
    title: Ronald Fagin, Jurg Nievergelt, Nicholas Pippenger and H. Raymond Strong, Extendible hashing, a fast access method for dynamic files, ACM Transactions on Database Systems 4(3) (1979)
    locator: pages 315 to 344 (the directory of 2^d pointers, global and local depths)
  - paper: "Witold Litwin, Linear Hashing: A New Tool for File and Table Addressing, Proceedings of the Sixth International Conference on Very Large Data Bases (VLDB), Montreal, 1980, pages 212 to 223"
    title: Witold Litwin, Linear Hashing, A New Tool for File and Table Addressing, VLDB 1980
    locator: the split pointer and the splits of buckets in linear order, without a directory
  - url: https://wrap.warwick.ac.uk/46327/
    title: G. N. N. Martin, Spiral storage, incrementally augmentable hash addressed storage, Theory of Computation Report 27, Department of Computer Science, University of Warwick, March 1979
    locator: the whole report (the exponential address function and the expansion of the address space one bucket at a time)
  - paper: doi:10.1145/46157.330532
    title: R. J. Enbody and H. C. Du, Dynamic hashing schemes, ACM Computing Surveys 20(2) (1988)
    locator: pages 85 to 113 (survey and classification of the schemes with and without a directory)
  - paper: doi:10.1145/42404.42410
    title: Per-Ake Larson, Dynamic hash tables, Communications of the ACM 31(4) (1988)
    locator: pages 446 to 457 (linear hashing and spiral storage adapted to tables in main memory)
---

Dynamic hashing is the family of hashing schemes in which the address space grows or shrinks one bucket at a time as keys are inserted and deleted, so that no operation has to move all the stored keys. A plain [hash table](/hash-table/) with a fixed number of slots must be rebuilt for a new size by [rehashing](/rehashing/) all $n$ keys, while a dynamic scheme splits one bucket into two, or merges two into one, and moves only the keys of those buckets. The family began with files on disk, where a full rebuild would read and write the whole file: Larson's dynamic hashing (1978), [extendible hashing](/extendible-hashing/) (1979), spiral storage (1979) and [linear hashing](/linear-hashing/) (1980).

## In plain words

Think of a filing cabinet in which each drawer holds the folders whose labels end in certain letters. When one drawer gets too full, you do not empty the whole cabinet and sort everything again. You buy one new drawer and move half of the folders of the full drawer into it, by looking at one more letter of each label.

Every scheme in this family works this way. They differ in two choices: which drawer is split next, and how you find the right drawer for a folder. Some keep an index that points to the drawers. Others number the drawers so that the right one can be computed directly, and split them in a fixed order.

## The idea

**Hash values as bit strings.** Each key $x$ is hashed to a long string of bits, $h(x)$, which acts as an infinite sequence of fair coin flips. A bucket is named by a short string of bits $s$, and it holds the keys whose hash starts with $s$ (some schemes use the low-order bits instead, which is the same idea read from the other end). The buckets of a table form the leaves of a binary [trie](/trie/) on the hash bits, and the set of their names is prefix-free and covers all strings.

**Splitting and merging.** A split replaces a bucket $s$ with the two buckets $s0$ and $s1$ and moves each of its keys by the next bit of the hash. A merge does the reverse. Only the keys of one bucket move, so the cost of a split is proportional to the size of the bucket, not to $n$. A full rebuild by [rehashing](/rehashing/) corresponds to splitting every bucket at once.

**Locating a bucket.** The schemes differ in how a search finds the bucket of $h(x)$.

- With a directory. Larson's dynamic hashing keeps the trie itself in memory and walks down it by the bits of $h(x)$. [Extendible hashing](/extendible-hashing/) flattens the trie into an array of $2^d$ pointers indexed by the first $d$ bits, where $d$ is the depth of the deepest bucket, so that a search is one array access followed by one bucket read. The price is that the array doubles when one bucket at the greatest depth splits, and its size grows faster than linearly in $n$ for a fixed bucket capacity.
- Without a directory. [Linear hashing](/linear-hashing/) splits buckets in a fixed order, $0, 1, 2, \ldots$, given by a split pointer $p$, whatever bucket overflowed. With $m_0 2^i$ buckets at the start of a round, the address is $j = h(x) \bmod m_0 2^i$, and if $j < p$ the bucket has already split and the address is $h(x) \bmod m_0 2^{i+1}$. Overflowing buckets keep overflow chains until their turn comes. Spiral storage maps keys to addresses by an exponential function, so that the load is uneven on purpose: on the active range of buckets $[N, 2N)$ a key falls in bucket $i$ with probability $\log_2(1 + 1/i)$, which sums to 1 over that range. The fullest bucket is always the first one, and an expansion splits it into two new buckets at the end of the range.

**When to split.** An uncontrolled scheme splits whenever a bucket overflows. A controlled scheme splits whenever the [load factor](/load-factor/) $n/(\text{number of buckets} \cdot b)$, for buckets of capacity $b$, passes a threshold, and merges when it falls below a lower threshold. The control of the load factor is natural for linear hashing and spiral storage, which do not split the overflowing bucket anyway.

**What the family buys.** Each insertion or deletion moves $O(b)$ keys in expectation at a split or merge, and the time and the number of disk reads of a search stay bounded as $n$ changes by any factor. No operation pauses to move the whole table, which [rehashing](/rehashing/) only achieves by keeping two tables and moving keys between them a few at a time. The cost is a more complex addressing rule, overflow chains in the directoryless schemes, and, for extendible hashing, a directory that can grow out of proportion when the hash bits are not uniform.

## Examples

**Splitting by one more bit.** Take buckets of capacity 2, addressed by the low-order bits of a 3-bit hash, and the keys $A, B, C, D, E$ with hash values $000, 101, 010, 111, 100$, inserted in this order.

| Step | Event | Buckets (name: keys) | Keys moved |
| --- | --- | --- | --- |
| 1 | insert A, B | (empty name): A, B | 0 |
| 2 | insert C, overflow, split by bit 0 | 0: A, C; 1: B | 2 (A, B) |
| 3 | insert D | 0: A, C; 1: B, D | 0 |
| 4 | insert E, overflow of bucket 0, split by bit 1 | 00: A, E; 10: C; 1: B, D | 2 (A, C) |

At step 4 the keys B and D are not touched, while a rebuild of the whole table would have moved all four. Extendible hashing would store this table with a directory of 4 entries, indexed by 2 bits, in which the entries $01$ and $11$ both point to bucket 1. Linear hashing would not split bucket 0 at step 4 if its split pointer were elsewhere; it would add an overflow block to bucket 0 and split the bucket at the pointer.

**A growing file.** A file of records on disk that grows from a thousand to a million records keeps a search cost of about one or two block reads under any of these schemes, with each insertion that causes a split reading and writing a constant number of blocks. A static hash file of fixed size would instead see its overflow chains grow longer, or would need a full reorganization pass.

## Where it is used

- Hash indexes of database systems and hash files of storage libraries, where the table lives on disk and a full rebuild would stop the system; linear hashing and extendible hashing are the common choices, and they compete with [B-trees](/b-tree/) in the [external memory model](/external-memory-model/) when range queries are not needed.
- Hash tables in main memory that must keep the latency of each operation small, as in Larson's 1988 adaptation of linear hashing with a directory of fixed-size segments, so that the table grows without the copy of a doubling [array](/array-doubling/).
- Distributed and parallel tables, where the buckets live on different machines and splitting one bucket moves data to one new machine instead of reshuffling all of them.
- The worst-case search of [dynamic perfect hashing](/dynamic-perfect-hashing/) is a different goal: it keeps a constant number of probes in every search, while the schemes here keep the number of probes small in expectation and focus on cheap growth.

## References
