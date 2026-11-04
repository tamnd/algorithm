---
tag: BAW0K0
kind: problem
slug: external-searching
name: External searching
area: data-structures/external-memory-structures
level: core
summary: Problem of searching data too large for main memory, where cost is measured in page accesses to external storage.
model: external-memory-model
prereqs: [external-memory-model, search-in-sorted-array, dictionary-problem]
see_also: [b-tree, b-plus-tree, extendible-hashing, linear-hashing, van-emde-boas-layout, cache-oblivious-b-tree, b-epsilon-tree, predecessor-problem]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.4 (multiway trees for external searching) and Section 6.4 (hashing, including external searching with buckets)
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Chapter 3 (the bound Search(N)), Chapter 10 (external hashing) and Chapter 11 (multiway trees, Section 11.1 on B-trees)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 18 (B-trees, the counting of disk accesses)
  - paper: "Gerth Stølting Brodal and Rolf Fagerberg, Lower bounds for external memory dictionaries, Proceedings of the 14th ACM-SIAM Symposium on Discrete Algorithms (SODA 2003)"
    locator: the main theorem (the trade-off between update and query cost)
---

External searching is the problem of answering search queries on a set of keys that is stored on a disk, or another slow storage, because it does not fit in main memory, with the cost measured in block transfers instead of comparisons. In the [external memory model](/external-memory-model/) with blocks of $B$ keys, a comparison-based search for one key among $N$ needs $\Theta(\log_B N)$ block reads in the worst case, and the [B-tree](/b-tree/) achieves this. Hashing does better for exact matches, with $O(1)$ expected reads, but it cannot answer order queries. The problem is the reason that database and file system indexes are multiway trees and not binary ones.

## In plain words

Your data is on a disk. The disk does not hand you one key at a time: each read brings a whole block of hundreds or thousands of keys, and each read is slow compared with any work you do in memory. So the question is not how many keys you compare, but how many blocks you read.

A search in a sorted list cuts the list in half with each look. On a disk this wastes most of each block, because you use only one key of the block you read. A better plan uses every key of each block to choose among hundreds of ways at once. Then a billion keys need only three or four reads per search.

## Definition

**Model.** The [external memory model](/external-memory-model/) with an internal memory of $M$ keys and blocks of $B$ keys, $2 \le B \le M/2$. Keys come from a total order. In the comparison version, keys are indivisible and the algorithm learns about them only by comparing two keys in memory.

**Input.** A set $S$ of $N$ keys. A *structure* for $S$ is a placement of the keys, and of any extra data such as pointers, in disk blocks. Its space is the number of blocks it uses. The aim is $O(N/B)$ blocks.

**Queries.** For a query key $q$:

- *membership*: decide whether $q \in S$;
- *predecessor*: return $\max\{s \in S : s \le q\}$, or none (the [predecessor problem](/predecessor-problem/));
- *range reporting*: for a second key $q' \ge q$, return all $s \in S$ with $q \le s \le q'$. We write $Z$ for the number of keys in the answer.

**Cost.** The number of block reads that one query makes, in the worst case over $S$ and $q$, with the structure built in advance. A structure may keep $O(1)$ blocks in memory between queries, such as the root of a tree.

**Dynamic version.** The structure must also support `insert(S, k)` and `delete(S, k)`, and the cost of an update is the number of block reads and writes, in the worst case or amortized over a sequence.

## Variants

- **Static and dynamic.** A static structure is built once. A dynamic one changes with insertions and deletions, as a [dictionary](/dictionary-problem/) does.
- **Exact match only.** Only membership, with the record that goes with the key. This allows hashing, which does not use the order.
- **Order queries.** Predecessor, successor and range reporting need the order of the keys, so they rule out plain hashing.
- **Batched or offline searching.** $Q$ queries are known together and the answers may come in any order. Sorting the queries and merging them with the sorted keys answers all of them in $O(\mathrm{Sort}(Q) + (N + Q)/B)$ I/Os, which for large $Q$ is far below $Q \log_B N$.
- **Cache-oblivious searching.** The structure must not depend on $B$ or $M$; see the [cache-oblivious model](/cache-oblivious-model/).
- **Several disks.** With $D$ disks read in parallel, the bound becomes $\Theta(\log_{DB} N)$ ([external memory model](/external-memory-model/), relation to other models).

## Examples

Take $N = 10^9$ keys and blocks of $B = 512$ keys, so the sorted file has $N/B = 1953125$ blocks.

- **Binary search on the sorted file.** Each probe reads one block and halves the range of blocks, so a search reads about $\lg(N/B) \approx 20.9$, that is 21, blocks. Only the last read uses more than two keys of its block.
- **A B-tree.** A [B-tree](/b-tree/) or [B+ tree](/b-plus-tree/) with about 512 keys per node has at most 4 levels for $10^9$ keys. With the root in memory, a search reads at most 3 blocks.
- **The lower bound.** Every comparison-based method needs at least $\log_{B+1}(N+1) = \log_{513}(10^9 + 1) \approx 3.32$ reads in the worst case, so at least 4 reads with nothing kept in memory between queries.
- **Hashing.** With [extendible hashing](/extendible-hashing/) and the directory in memory, a lookup reads one bucket block. A predecessor query, for example "the largest key at most 700", gets no help from the hash function.
- **Range reporting.** Reporting $Z = 10^6$ consecutive keys from a B+ tree costs the search plus about $Z/B \approx 1954$ leaf reads, while $10^6$ separate searches would cost about $3 \times 10^6$ reads.

## Known algorithms

| structure | query (block reads) | update | notes |
|---|---|---|---|
| sorted file and [binary search](/binary-search/) | $\Theta(\log_2 (N/B))$ | $\Theta(N/B)$ | static |
| [B-tree](/b-tree/), [B+ tree](/b-plus-tree/), [B\*-tree](/b-star-tree/) | $O(\log_B N)$, range $O(\log_B N + Z/B)$ | $O(\log_B N)$ worst case | the standard index |
| [B^ε-tree](/b-epsilon-tree/), $0 < \varepsilon \le 1$ | $O(\frac{1}{\varepsilon}\log_B N)$ | $O(\frac{1}{\varepsilon B^{1-\varepsilon}}\log_B N)$ amortized | write-optimized |
| [log-structured merge tree](/log-structured-merge-tree/) | $O(\log_B N)$ per level, over $O(\log N)$ levels | $O(\frac{1}{B}\log N)$ amortized for the basic form | write-optimized |
| [van Emde Boas layout](/van-emde-boas-layout/) | $O(\log_B N)$ for every $B$ | static | cache-oblivious |
| [cache-oblivious B-tree](/cache-oblivious-b-tree/) | $O(\log_B N)$ for every $B$ | $O(\log_B N + \frac{\log^2 N}{B})$ amortized | cache-oblivious |
| [extendible hashing](/extendible-hashing/), [linear hashing](/linear-hashing/) | $O(1)$ expected | $O(1)$ expected amortized | membership only |

The [buffer tree](/buffer-tree/) answers batched queries: $N$ operations cost $O(\mathrm{Sort}(N))$ in total, but each answer comes late.

## Bounds

- **Comparison-based searching.** Every comparison-based algorithm, for every fixed placement of the keys, needs at least $\log_{B+1}(N+1)$ block reads in the worst case to find the rank of $q$. One block of at most $B$ keys tells the algorithm only in which of $B + 1$ gaps $q$ falls, and there are $N + 1$ possible answers. The proof is on the [external memory model](/external-memory-model/) page, under "Searching". The B-tree meets the bound up to a constant factor, so the comparison complexity is $\Theta(\log_B N)$. Vitter calls this bound $\mathrm{Search}(N)$ (Chapter 3).
- **Range reporting.** A query with $Z$ answers needs at least $Z/B$ more reads, to hold the answers, and a B+ tree gives $O(\log_B N + Z/B)$, which is optimal.
- **Binary search loses a factor of about $\lg B$.** $\log_2(N/B) / \log_B N$ is about $\lg B$ for large $N$, which is 9 for $B = 512$.
- **Updates.** A B-tree update costs $\Theta(\log_B N)$ I/Os. Amortized updates can be much cheaper: the [B^ε-tree](/b-epsilon-tree/) gives the query cost and update cost of the table, and Brodal and Fagerberg (2003) proved that this trade-off between the two costs is optimal for comparison-based dictionaries. In particular, for each constant $\varepsilon$ with $0 < \varepsilon < 1$, a query cost of $O(\log_B N)$ allows an amortized insertion cost of $O(\frac{1}{B^{1-\varepsilon}}\log_B N)$, far below one I/O.
- **Cache-oblivious searching.** A structure that does not know $B$ still achieves $O(\log_B N)$, but needs at least about $\lg e \cdot \log_B N \approx 1.443 \log_B N$ reads in the worst case on some level of the memory hierarchy (Bender and others, 2003, on the [cache-oblivious model](/cache-oblivious-model/) page).
- **Hashing.** Without comparisons, membership takes $O(1)$ expected reads, so the $\Omega(\log_B N)$ bound is a bound for comparison-based algorithms only.

## Reductions

- **Membership reduces to predecessor.** Find the predecessor $p$ of $q$ and test $p = q$. So a lower bound for membership in the comparison model is also one for predecessor.
- **Predecessor reduces to range reporting.** A predecessor query is a range query on $(-\infty, q]$ that stops after the last answer. In a B+ tree this costs $O(\log_B N)$.
- **Batched searching reduces to sorting.** As in the variants above, $Q$ offline queries cost $O(\mathrm{Sort}(Q) + (N + Q)/B)$, by a sort of the queries and one merge with the sorted keys.

## Applications

- The indexes of relational databases, which are B+ trees in most systems.
- Directories and extent maps of file systems. The Btrfs file system takes its name from the B-tree.
- Key-value stores, many of which use [log-structured merge trees](/log-structured-merge-tree/) or [B^ε-trees](/b-epsilon-tree/) to make writes cheap.
- The term dictionary of an inverted index in a search engine.
- In main memory, the same reasoning applies with cache lines in place of disk blocks: B-trees with small nodes and the [Eytzinger layout](/eytzinger-layout/) make fewer cache misses than a plain binary search.

## References
