---
tag: P73KVS
kind: concept
slug: cache-admission-policy
name: Cache admission policy
area: systems/caching-policies
level: advanced
summary: The rule that decides whether an object fetched on a miss is stored in the cache at all, as opposed to the eviction rule that decides which cached object leaves.
prereqs: [cache-replacement-policy, cache-hit-ratio]
see_also: [tinylfu, w-tinylfu, s3-fifo, two-q, slru, bloom-filter, ghost-lists, lru]
sources:
  - paper: doi:10.1145/2805789.2805800
    title: "Bruce M. Maggs and Ramesh K. Sitaraman, Algorithmic Nuggets in Content Delivery, ACM SIGCOMM Computer Communication Review 45(3), 2015"
    locator: Section 4 (cache filtering with Bloom filters, the cache-on-second-hit rule and the share of one-hit wonders)
  - paper: doi:10.1145/3149371
    title: "Gil Einziger, Roy Friedman and Ben Manes, TinyLFU: A Highly Efficient Cache Admission Policy, ACM Transactions on Storage 13(4), 2017"
    locator: Section 3.1 (admission as a separate step beside eviction), Section 4 (W-TinyLFU)
  - paper: doi:10.1145/3600006.3613147
    title: "Juncheng Yang, Yazhuo Zhang, Ziyue Qiu, Yao Yue and K. V. Rashmi, FIFO Queues are All You Need for Cache Eviction, ACM SOSP 2023"
    locator: Section 3 (one-hit wonders) and Section 4.1 (the small queue S as a filter)
---

A cache admission policy decides, on a miss, whether the object just fetched is stored in the cache. An eviction policy, or [cache replacement policy](/cache-replacement-policy/), decides which cached object leaves when space is needed. The two are separate questions. A cache without an admission policy stores every object it fetches, and so a flood of objects that are requested only once can push out objects that are requested often. An admission policy can turn such objects away, so that the request is served but the cache does not change.

## In plain words

A library with a small shelf of popular books has two choices to make. When it gets a new book, should it put the book on the shelf at all? And if it does and the shelf is full, which book should come off? The first choice is admission and the second is eviction.

Most new books are borrowed once and never again. If every new book goes on the shelf, the popular books keep getting pushed off. A simple admission rule helps: put a book on the shelf only the second time someone asks for it.

## The idea

**Admission and eviction differ.** They act on different objects and have different options.

| | eviction | admission |
| --- | --- | --- |
| acts on | objects already in the cache | the object that just missed |
| when | the cache needs space | every miss |
| may do nothing | no: it must free space once the new object is stored | yes: the object is served and not stored |
| typical signal | recency, frequency or age of cached objects | history of keys that are not cached |

In the classic [paging problem](/paging-problem/), every requested page must be brought into memory, so there is no admission: only eviction. Web caches, content delivery networks, key-value stores and flash caches can bypass the cache and serve the object directly, so admission is allowed there. Allowing bypass can only help the best offline policy, because a policy that always admits is still allowed.

An admission policy needs to remember something about keys that are not cached, since its whole job is to judge objects that are not yet in the cache. This history can be a set of keys, a [Bloom filter](/bloom-filter/), a frequency sketch, or a list of recently evicted keys.

**Kinds of admission.**

1. *Admit on the second request.* Store an object only if its key was seen before. Maggs and Sitaraman describe this cache-on-second-hit rule in Section 4 of their 2015 paper: in the trace of a content delivery network that they report, 74% of the objects were requested only once, and a Bloom filter of keys seen once keeps these one-hit wonders out of the cache. This saves cache space and disk writes. The cost is one extra miss for every object that is requested twice or more.
2. *Admit by comparison with the victim.* [TinyLFU](/tinylfu/) asks the eviction policy for its victim and admits the new object only if a frequency sketch estimates it more frequent than the victim. [W-TinyLFU](/w-tinylfu/) puts a small LRU window in front, so that new objects get a short stay before the test.
3. *Admit to probation.* The object is stored, but in a small area where it is evicted soon unless it is requested again. [2Q](/two-q/) uses the FIFO queue A1in, [SLRU](/slru/) uses a probation segment, and [S3-FIFO](/s3-fifo/) uses a small FIFO queue $S$ of 10% of the cache, with its [ghost list](/ghost-lists/) $G$ to let returning objects skip $S$. This is admission done by eviction: the main cache admits only objects that prove themselves in the small area.
4. *Admit by size or cost.* Caches with objects of very different sizes can favor small objects, which give more hits per byte, for example by admitting large objects with a lower probability.

**What can go wrong.** A strict admission rule delays new popular objects, since they miss until they pass the test. A filter must also forget: a Bloom filter that is never cleared fills up and admits every key, and counts that never decay keep old favorites. TinyLFU halves its counters after a fixed number of requests and clears its Bloom filter at the same time.

## Examples

**Second-request admission on a small trace.** Take an [LRU](/lru/) cache of 2 objects and the requests A B A X B Y A B Z A, where A and B are popular and X, Y and Z are requested once. The history here is an exact set of seen keys.

| $t$ | request | LRU, always admit | hit | LRU, admit on second request | hit |
| --- | --- | --- | --- | --- | --- |
| 1 | A | A | | (A seen) | |
| 2 | B | B A | | (B seen) | |
| 3 | A | A B | yes | A | |
| 4 | X | X A | | A (X seen) | |
| 5 | B | B X | | B A | |
| 6 | Y | Y B | | B A (Y seen) | |
| 7 | A | A Y | | A B | yes |
| 8 | B | B A | | B A | yes |
| 9 | Z | Z B | | B A (Z seen) | |
| 10 | A | A Z | | A B | yes |

Plain LRU gets 1 hit, because X, Y and Z keep pushing A and B out. With admission on the second request, X, Y and Z never enter, and the cache gets 3 hits, at the price of misses on the first two requests of A and B.

**Admission by comparison.** The [TinyLFU page](/tinylfu/) traces the requests A A B B C C C A D A C with a cache of 2 objects. C is turned away twice, while its estimate is not above that of the victim A, and D, seen once, is never stored.

## Where it is used

- *Content delivery networks.* Akamai filters one-hit wonders with Bloom filters before they reach disk caches, as Maggs and Sitaraman describe.
- *In-memory caches.* The Caffeine Java cache uses W-TinyLFU, and libraries in other languages copy its design.
- *Flash caches.* Writes wear out flash, so flash caches often admit only objects that are likely to be read again, which also saves write bandwidth.
- *Buffer pools.* 2Q and SLRU keep pages that are read once by a scan from pushing out the working set of a database.

## References
