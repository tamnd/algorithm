---
tag: W3TY6D
kind: concept
slug: ghost-lists
name: Ghost lists
aliases:
- ghost entries
area: systems/caching-policies
level: advanced
summary: Lists that keep only the keys of recently evicted objects, so a policy can tell when an eviction was a mistake and adapt or promote the returning object.
prereqs: [lru, cache-replacement-policy]
see_also: [arc, car, two-q, lirs, clock-pro, s3-fifo, mattson-stack-algorithm, tinylfu]
sources:
  - url: https://www.usenix.org/legacy/events/fast03/tech/full_papers/megiddo/megiddo.pdf
    title: "Nimrod Megiddo and Dharmendra S. Modha, ARC: A Self-Tuning, Low Overhead Replacement Cache, USENIX FAST 2003, 115-130"
    locator: Section IV and Fig. 4 (the ghost lists B1 and B2 and the update of the target p)
  - paper: "Theodore Johnson and Dennis Shasha, 2Q, a low overhead high performance buffer management replacement algorithm, Proceedings of the 20th International Conference on Very Large Data Bases (VLDB), 1994, 439-450"
    title: 2Q, a low overhead high performance buffer management replacement algorithm
    locator: the full 2Q with the queue A1out of page identifiers and the size Kout
  - paper: doi:10.1145/511334.511340
    title: "Song Jiang and Xiaodong Zhang, LIRS: An Efficient Low Inter-reference Recency Set Replacement Policy to Improve Buffer Cache Performance, ACM SIGMETRICS 2002, 31-42"
    locator: the nonresident HIR blocks kept in the stack S
  - paper: doi:10.1145/3600006.3613147
    title: "Juncheng Yang, Yazhuo Zhang, Ziyue Qiu, Yao Yue and K. V. Rashmi, FIFO Queues are All You Need for Cache Eviction, ACM SOSP 2023"
    locator: Section 4.1 and Algorithm 1 (the ghost queue G), Section 4.2 (ghost entries stored in the hash table)
---

A ghost list holds the keys of objects that a cache evicted recently, but not their data. When a miss finds its key in a ghost list, the cache learns that the object was evicted too early: a slightly different choice would have made this request a hit. Policies use this signal in two ways. They can adapt a parameter, as [ARC](/arc/) moves the split between its recency and frequency lists, or they can treat the returning object as proven useful and put it in a protected part of the cache, as [2Q](/two-q/) and [S3-FIFO](/s3-fifo/) do. A ghost entry costs a key and a few pointers, which is small next to the data of a page or an object.

## In plain words

A shop that runs out of shelf space removes some products. It writes the names of the removed products on a short list. When a customer asks for a product on that list, the shop knows it removed that product too soon. It can then give that product a better shelf, or change how it picks products to remove.

The list holds names only, so it is cheap. It is also short: old names fall off the end, because a request for a product removed long ago says little about the current choices.

## The idea

**What a ghost hit means.** A request is a *ghost hit* when it misses in the cache but its key is in a ghost list. It is still a miss, and the data must be fetched. But it is evidence: the object came back after a short time out of the cache.

**A ghost list behind LRU measures a larger cache.** Put a ghost list of $g$ keys behind an [LRU](/lru/) cache of $c$ objects, ordered by recency. A key leaves the ghost list when it is requested or when it is pushed past position $g$. Then the cache and the ghost list together hold the top $c + g$ entries of the LRU stack of [Mattson's stack algorithm](/mattson-stack-algorithm/), and the cache holds the top $c$. So a request is a ghost hit exactly when it is a miss for LRU with $c$ objects and a hit for LRU with $c + g$ objects, and its position $j$ in the ghost list says that a cache of $c + j$ objects would have hit. This is the [inclusion property](/inclusion-property/) of LRU at work, and it is the basis of the adaptive rules below.

**Two uses.**

1. *Adapting a parameter.* ARC keeps ghost lists $B_1$ and $B_2$ for the keys evicted from its list $T_1$ of objects seen once and its list $T_2$ of objects seen twice or more. A ghost hit in $B_1$ says $T_1$ was too small, so ARC raises the target $p$ for the size of $T_1$, by $\max(1, |B_2|/|B_1|)$. A ghost hit in $B_2$ lowers $p$ by $\max(1, |B_1|/|B_2|)$. [CAR](/car/) uses the same rule with clocks. [CLOCK-Pro](/clock-pro/) raises its target for cold pages when a non-resident cold page is requested during its test period.
2. *Promoting a returning object.* In 2Q, a page evicted from the FIFO queue A1in goes to the ghost queue A1out, and a later miss found in A1out puts the page in the main LRU queue Am. S3-FIFO does the same with its small queue $S$, its ghost queue $G$ and its main queue $M$. In [LIRS](/lirs/), a non-resident block in the stack S shows that its reuse distance is small, so the block comes back with LIR status.

**Bounding the size.** A ghost list must have a limit, or it grows with the number of distinct keys. The policies set the limit in terms of the cache size:

| policy | ghost list | limit | on a ghost hit |
| --- | --- | --- | --- |
| [ARC](/arc/) | $B_1$, $B_2$ | $\lvert T_1 \rvert + \lvert B_1 \rvert \le c$ and at most $2c$ keys in all | move $p$, insert into $T_2$ |
| [CAR](/car/) | $B_1$, $B_2$ | as in ARC | as in ARC |
| [2Q](/two-q/) | A1out | Kout, about 50% of the cache in the paper's tuning | insert into Am |
| [LIRS](/lirs/) | nonresident HIR blocks in S | stack pruning, and a cap on S in the later paper | the block becomes LIR |
| [CLOCK-Pro](/clock-pro/) | non-resident cold pages | at most $m$, the number of resident pages | raise the cold target, the page becomes hot |
| [S3-FIFO](/s3-fifo/) | $G$ | the size of $M$, about 90% of the cache | insert into $M$ |

**Ghosts are not the only memory of the past.** [TinyLFU](/tinylfu/) remembers keys that are not cached as approximate counts in a sketch, not as a list. [SIEVE](/sieve/) keeps no history at all, and [LHD](/lhd/) keeps histograms of ages, not keys.

## Examples

**LRU with a ghost list.** Take an LRU cache of $c = 2$ objects with a ghost list of $g = 2$ keys, both written most recent first, and the requests A B C A D B.

| $t$ | request | cache | ghost list | result |
| --- | --- | --- | --- | --- |
| 1 | A | A | | miss |
| 2 | B | B A | | miss |
| 3 | C | C B | A | miss |
| 4 | A | A C | B | ghost hit at position 1 |
| 5 | D | D A | C B | miss |
| 6 | B | B D | A C | ghost hit at position 2 |

LRU with 4 objects has hits at $t = 4$ and $t = 6$ on this trace, the same two requests. The position of each ghost hit says that 3 objects would have caught A and 4 objects would have caught B.

**A ghost hit in ARC.** On the trace 1 2 1 3 4 2 with $c = 3$, ARC evicts page 2 from $T_1$ at $t = 5$ and keeps its key in $B_1$. At $t = 6$ page 2 is found in $B_1$, so $p$ rises from 0 to 1 and page 2 enters $T_2$. The [ARC page](/arc/) gives the full trace.

## Where it is used

- *Adaptive replacement.* ARC and its ghost lists are used in the ZFS file system's cache. CAR and CLOCK-Pro keep ghosts in the same clocks as cached pages.
- *Databases.* 2Q was designed for database buffer pools, where ghosts let a page that is read twice in a short time escape a scan.
- *Key-value and web caches.* S3-FIFO stores its ghost entries in the hash table of the cache, as a 4-byte fingerprint of the key with an insertion count, so a ghost costs a few bytes.
- *Operating systems.* The Linux page cache leaves a small shadow entry in place of an evicted page, and when the page is read again it uses the entry to estimate how far the page was from staying in memory. This is a ghost entry under another name.
- *Hit ratio curves.* A ghost list behind LRU, as in the first example, estimates the hits a larger cache would get, which helps size caches online.

## References
