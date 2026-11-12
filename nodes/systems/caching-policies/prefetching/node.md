---
tag: P6H46Y
kind: concept
slug: prefetching
name: Prefetching
aliases:
- Cache prefetching
- read-ahead
- one block lookahead prefetching
- stride prefetching
- integrated prefetching and caching
area: systems/caching-policies
level: intro
summary: "Loading blocks into a cache before they are requested, from a guess of the next accesses: the next block, a learned stride, or a known sequence of future requests."
prereqs: [cache, locality-of-reference, belady-optimal]
see_also: [multilevel-caching, three-cs-model, set-associative-cache, lru, paging-problem, memory-hierarchy, cache-hit-ratio, reuse-distance]
sources:
  - paper: doi:10.1145/356887.356892
    title: "Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3) (1982), 473-530"
    locator: the section on the fetch algorithm (demand fetch and prefetch; always prefetch, prefetch on misses and tagged prefetch, all with one block lookahead)
  - paper: "Alan Jay Smith, Sequential program prefetching in memory hierarchies, IEEE Computer 11(12), 1978"
    title: "Alan Jay Smith, Sequential program prefetching in memory hierarchies, IEEE Computer, 1978"
    locator: one block lookahead prefetching of the next page or block, and its effect on misses and memory traffic
  - paper: doi:10.1109/12.381947
    title: "Tien-Fu Chen and Jean-Loup Baer, Effective hardware-based data prefetching for high-performance processors, IEEE Transactions on Computers 44(5) (1995), 609-623"
    locator: the reference prediction table (instruction address, previous address, stride and a state of initial, transient, steady or no prediction) and the basic, lookahead and correlated schemes
  - paper: "Pei Cao, Edward W. Felten, Anna R. Karlin and Kai Li, A study of integrated prefetching and caching strategies, ACM SIGMETRICS 1995, 188-197"
    title: "Cao, Felten, Karlin and Li, A study of integrated prefetching and caching strategies, SIGMETRICS 1995"
    locator: "Section 2 (the model, the example ABCA, the four rules, the conservative and aggressive strategies) and Section 3 (conservative within 2 of optimal, aggressive within min(1 + F/k, 2))"
  - paper: "Norman P. Jouppi, Improving direct-mapped cache performance by the addition of a small fully-associative cache and prefetch buffers, 17th Annual International Symposium on Computer Architecture (ISCA), 1990"
    title: "Jouppi, Improving direct-mapped cache performance by the addition of a small fully-associative cache and prefetch buffers, ISCA 1990"
    locator: stream buffers, which prefetch the blocks after a miss into a small queue beside the cache
---

Prefetching loads a block into a [cache](/cache/) before the program asks for it, so that the time of the fetch overlaps with useful work. It works only as well as its guess of the future: the next block in memory, a stride learned from the past addresses of one instruction, or a list of future requests given by the program. A good prefetch turns a miss into a hit, while a bad one costs bandwidth and can evict a block that was still needed. Hardware caches, operating system read-ahead and database buffer pools all use it.

## In plain words

A waiter who sees that a table has nearly finished the main course starts to make the coffee before anyone asks for it. When the guests ask, the coffee is ready. If the guests do not want coffee, the work was wasted, and if the tray was full, something else had to go to make room.

Prefetching is that habit in a computer. Memory and disks are slow, so the system tries to load data before the program needs it. The simplest guess is "the next piece": a program that reads part 7 of a file will likely read part 8 next. A better guess learns a pattern, such as "this loop reads every third piece". The hard part is to know when a guess is good enough to be worth the space it takes.

## The idea

A demand cache loads a block only on a miss, so each miss costs the full time of a fetch. Prefetching adds a second decision: what to load, and when, before it is asked for. Three numbers judge a prefetcher. *Coverage* is the share of the misses it removes. *Accuracy* is the share of its prefetches that are used before they are evicted. *Timeliness* asks if the block arrives before it is needed, but not so early that it is evicted first. A wrong prefetch costs memory bandwidth and can cause *pollution*: it evicts a useful block. Prefetching removes mostly compulsory and capacity misses in the sense of the [three Cs model](/three-cs-model/), and only by [locality](/locality-of-reference/) in space or in a pattern of addresses.

**Sequential prefetching.** Alan Jay Smith studied one block lookahead (OBL) in 1978 and in his 1982 survey: when block $i$ is referenced, consider fetching block $i + 1$. The three classic forms differ in when they act.

- *Always prefetch*: after every reference to block $i$, fetch $i + 1$ if it is not in the cache. It needs a cache lookup for $i + 1$ on each reference.
- *Prefetch on miss*: only a miss on block $i$ fetches $i + 1$. On a long scan this misses on every other block, since a hit on a prefetched block does not prefetch the next one.
- *Tagged prefetch*: a prefetched block carries a tag bit. A miss on $i$, or the first use of a tagged block $i$, fetches $i + 1$. On a scan only the first block misses, and unlike always prefetch it makes no lookup on the repeated hits to a block.

Jouppi's stream buffers (1990) take the same idea further. After a miss, a small queue beside the cache fetches the next several blocks, so a stream is served from the queue and does not pollute the cache. Operating systems do the same for files with read-ahead, and grow the read-ahead window while the accesses stay sequential.

**Stride prefetching.** Loops over arrays touch addresses $a, a + s, a + 2s, \ldots$ with a stride $s$ that need not be one block. Chen and Baer (1995) keep a *reference prediction table*, indexed by the address of the load instruction. Each entry holds the previous address, a stride and a state.

- The state is one of *initial*, *transient*, *steady* or *no prediction*. A guess is correct when the new address equals the previous address plus the stride.
- A correct guess moves the state toward steady, and a wrong one moves it toward no prediction. A wrong guess also learns the new stride, except in the steady state, so one odd access does not break a long stream.
- Unless the state is no prediction, the table prefetches the address plus the stride. The lookahead form of the scheme runs ahead of the program counter to prefetch further in time.

Indexing by instruction keeps several streams apart, even when their accesses alternate.

**Integrated prefetching and caching.** When the future requests are known, as for a program that tells the file system what it will read, the question becomes exact. Cao, Felten, Karlin and Li (1995) studied a model with a known sequence of $n$ references, one reference per time unit, a cache of $k$ blocks, and fetches that take $F$ time units, one at a time. When a fetch starts, it evicts a block at once, and the new block arrives $F$ units later. The cursor stalls while the next reference is not in the cache, and the cost is the elapsed time. They gave four rules that some optimal schedule obeys:

1. **Optimal prefetching.** Each prefetch fetches the next block in the sequence that is not in the cache.
2. **Optimal replacement.** Each prefetch evicts the block whose next reference is furthest in the future, as [Belady's MIN](/belady-optimal/) does.
3. **Do no harm.** Never evict block $A$ to fetch block $B$ when $A$ is referenced before $B$.
4. **First opportunity.** Never start a fetch and eviction that could have been started earlier.

Rules 1 and 2 fix what to fetch and what to evict; only the time is left to choose. The *conservative* strategy makes exactly the fetches and evictions of MIN, each as early as the rules allow; its elapsed time is at most twice the optimum. The *aggressive* strategy fetches the next missing block whenever the disk is free and rule 3 allows. Its elapsed time is at most $\min(1 + F/k, 2)$ times the optimum, and it makes no more fetches than LRU demand paging. Later work by Albers, Garg and Leonardi (1998) computed the optimal schedule for one disk in polynomial time.

## Examples

**A scan and short runs.** An [LRU](/lru/) cache of 64 blocks reads blocks 0 to 999 once. With no prefetch all 1000 references miss, prefetch on miss leaves 500 misses, and always and tagged prefetch leave 1. Next, a trace of about 20,000 references is made of runs of 1 to 16 consecutive blocks from random places, with a cache of 256 blocks.

| policy | misses | prefetches |
|---|---|---|
| none | 20,001 | 0 |
| prefetch on miss | 10,585 | 10,585 |
| tagged | 2,314 | 20,001 |

Tagged prefetch removes almost 9 misses in 10, at the cost of one prefetch per reference; about 2,300 of its prefetches go past the end of a run and are wasted.

**Strides.** Three load instructions take turns: A reads blocks $1000 + 3i$, B reads blocks $10^6 + 7i$, and C reads random blocks, 5,000 times each. With 256 blocks of cache, no prefetch and tagged prefetch both miss all 15,000 references, since no block is ever used twice and the next block is never the one needed. The reference prediction table learns the strides 3 and 7 after the first loads of A and B, and only the 5,000 random loads of C and a few loads at the start still miss.

**When prefetching hurts.** This is the example of Cao and others. The cache holds $k = 2$ blocks, starting with A and B, a fetch takes $F = 4$ units, and the sequence is A B C A.

| schedule | what it does | elapsed time |
|---|---|---|
| no prefetch, MIN replacement | hits A and B, stalls 4 units for C (evicting B), hits A | 8 |
| aggressive | after A, fetches C and evicts A; stalls 3 units for C; then fetches A and evicts B; stalls 3 units for A | 10 |

Aggressive hides latency but makes two fetches where one was enough. On A B C B the same early fetch of C, evicting A, is never undone, and aggressive takes 7 units against 8. A search over all schedules of small inputs confirms that 8 and 7 are optimal, and that keeping only schedules that obey rules 1 to 3 does not change the optimum.

## Where it is used

- **Processor caches.** Next-line and stride prefetchers in L1 and L2, and stream prefetchers that follow several streams at once. Compilers and programmers can also insert software prefetch instructions ahead of a loop's loads.
- **Operating systems.** File read-ahead in the page cache, and prefetching of the pages around a page fault.
- **Databases and storage.** Read-ahead for sequential scans, prefetching of index pages, and disk arrays that detect sequential streams.
- **Informed prefetching.** Applications that pass hints of their future reads, so that the system can use a strategy such as aggressive or conservative.
- **The web.** Browsers that prefetch the pages behind links and resources named in a page.

In a [multilevel](/multilevel-caching/) hierarchy each level may prefetch for the level above, and a prefetcher at a lower level sees only the misses of the higher one.

## References
