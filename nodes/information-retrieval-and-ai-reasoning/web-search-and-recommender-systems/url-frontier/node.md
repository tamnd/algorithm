---
tag: 91KJAA
kind: data-structure
slug: url-frontier
name: URL frontier
aliases:
- Mercator frontier
- crawl frontier
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: The queues of URLs still to be fetched, with front queues for priority and back queues per host so each host is visited politely.
model: word-ram
complexity:
  vars: {F: the number of front queues, B: the number of back queues, U: the number of distinct URLs added, H: the number of hosts served}
  time: {add: O(F) amortized, next: O(log B) amortized}
  space: {total: O(U + B + H)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [queue, priority-queue, hash-table, web-crawling]
see_also: [binary-heap, bloom-filter, consistent-hashing, breadth-first-search, focused-crawling, crawl-revisit-policy, pagerank]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 20, Section 20.2.3 (the URL frontier with F front queues for priority, B back queues that each hold one host, the heap of back queues by earliest contact time, and the heuristics for the gap and the number of back queues)
  - paper: "Marc Najork and Allan Heydon, High-performance web crawling, SRC Research Report 173, Compaq Systems Research Center, 2001; also in J. Abello, P. Pardalos and M. Resende (eds), Handbook of Massive Data Sets, Kluwer, 2002"
    locator: the design of the Mercator URL frontier with front queues that set the priority and back queues that enforce politeness
  - paper: "Allan Heydon and Marc Najork, Mercator: a scalable, extensible web crawler, World Wide Web 2(4), 219-229, 1999"
    locator: the section on the URL frontier, with one FIFO subqueue for each worker thread and hosts assigned to subqueues by a hash
  - paper: "Christopher Olston and Marc Najork, Web crawling, Foundations and Trends in Information Retrieval 4(3), 175-246, 2010"
    locator: the chapter on crawl ordering and politeness, which surveys frontier designs
---

A URL frontier is the data structure of a [web crawler](/web-crawling/) that holds the URLs that the crawler has found but not fetched yet. It has two jobs that pull against each other. It must hand out important URLs first, and it must never contact one host again before a politeness gap has passed. The two-stage design of the Mercator crawler, described by Marc Najork and Allan Heydon, gives each job its own stage. A row of front [queues](/queue/), one for each priority level, decides which URLs enter the second stage first. A row of back queues, each holding the URLs of one host only, together with a [priority queue](/priority-queue/) of the times at which each host may be contacted again, decides when each URL leaves.

## In plain words

Think of a post office that must deliver many letters, but each house will accept a letter only once in a while. The letters first go into a few bins by how urgent they are. A clerk takes letters from the urgent bins first and sorts them into trays, one tray for each house. A board shows the earliest time each house can take its next letter. Each delivery person takes the tray whose time comes up first, delivers one letter, and writes a later time on the board for that house. So urgent letters get into trays first, and no house gets letters too often. If a house must wait, letters for other houses, even less urgent ones, go out in the meantime. The office also keeps a list of every letter it has seen, so it never handles the same one twice.

## The abstract type

A URL frontier holds a set of URLs, each with a priority in $\{1, \ldots, F\}$, where 1 is the highest. Every URL $u$ has a host $h(u)$, and every host $h$ has a gap $\delta(h) \ge 0$. The operations are:

- ADD$(u, p)$: insert $u$ with priority $p$, unless $u$ was added before. Return whether it was inserted.
- NEXT$(\mathit{now})$: remove a URL $u$ and return it with a start time $s \ge \mathit{now}$, or report that the frontier is empty.

The contract has three parts. NEXT returns each added URL exactly once, if it is called until it reports empty. If NEXT returns URLs $u$ and then $v$ of the same host $h$ with start times $s_u$ and $s_v$, then $s_v \ge s_u + \delta(h)$. URLs of the same priority leave the front stage in the order in which they came in, and with a strict selector a URL of priority $p$ leaves the front stage only when no URL of a higher priority waits there. The order of the returned URLs is not the priority order: politeness can hold back an urgent URL while URLs of other hosts go first.

## Representation

The frontier has these parts:

- Front queues $F_1, \ldots, F_F$, FIFO. ADD puts a URL of priority $p$ at the tail of $F_p$.
- Back queues $Q_1, \ldots, Q_B$, FIFO. A back queue that is not empty holds URLs of exactly one host, its owner.
- A map from hosts to their back queues, so at most one back queue holds a given host.
- A min-heap, such as a [binary heap](/binary-heap/), with one entry $(t, j)$ for each back queue $Q_j$ that is not empty, where $t$ is the earliest time at which the owner of $Q_j$ may be contacted.
- A set of free back queues, which are empty and have no heap entry.
- A map next from hosts to the earliest time of their next contact. It keeps the time after a host loses its back queue, so a host that comes back soon after still waits its full gap.
- A set Seen of all URLs ever added, in a [hash table](/hash-table/). Large crawlers keep it on disk or in a [Bloom filter](/bloom-filter/), which can drop a few new URLs by mistake but never admits a URL twice.

A selector picks the front queue at each move. The strict selector takes the first queue that is not empty. A biased random selector takes queue $i$ with a weight that falls with $i$, so that low priority URLs also move.

## Operations

```pseudo id=main
ADD(u, p)
L1  if u ∈ Seen then return false
L2  add u to Seen; append u to F_p; return true

NEXT(now)
L3  while some back queue Q_j is free and some front queue is not empty: REFILL(j, now)
L4  if the heap is empty then return EMPTY
L5  (t, j) ← EXTRACT-MIN(heap)
L6  s ← max(now, t); u ← remove the head of Q_j; h ← owner(Q_j)
L7  next(h) ← s + δ(h)
L8  if Q_j is not empty then INSERT(heap, (next(h), j))
L9  else remove h as owner of Q_j; REFILL(j, s)
L10 return (u, s)

REFILL(j, now)                         ▷ Q_j is empty, with no owner and no heap entry
L11 while some front queue is not empty:
L12     i ← SELECT a front queue that is not empty
L13     u ← remove the head of F_i; h ← host of u
L14     if h owns a back queue Q_k then append u to Q_k
L15     else make h the owner of Q_j; append u to Q_j; INSERT(heap, (max(now, next(h)), j)); return
L16 mark Q_j free
```

REFILL moves URLs until it finds a host that has no back queue, so the URLs of a host that already has a queue go to that queue. NEXT serves the back queue whose host may be contacted first. In a crawler with several threads, each thread calls NEXT, waits until the start time, fetches the page, and calls ADD on the links it finds. The priority of a new URL can come from a [PageRank](/pagerank/) estimate, the depth of the URL, or the rate at which the page changes; the frontier does not care how it is computed.

## Example

Take $F = 2$ front queues, $B = 2$ back queues, a gap of 1 time unit for every host, and the strict selector. Add a/1, a/2 and c/1 with priority 1, and b/1 and a/3 with priority 2, in the order a/1, a/2, b/1, c/1, a/3, where a, b and c are hosts. Then $F_1$ holds a/1, a/2, c/1 and $F_2$ holds b/1, a/3. One thread calls NEXT, each time with now equal to the last start time.

| call | what happens | returns |
|---|---|---|
| NEXT(0) | REFILL($Q_1$) takes a/1: host a gets $Q_1$, heap entry $(0, Q_1)$. REFILL($Q_2$) takes a/2 into $Q_1$, then c/1: host c gets $Q_2$, entry $(0, Q_2)$. The heap gives $(0, Q_1)$; next(a) = 1, and $Q_1$ still holds a/2, so $(1, Q_1)$ goes back. | a/1 at 0 |
| NEXT(0) | The heap gives $(0, Q_2)$. $Q_2$ is now empty, so REFILL($Q_2$) takes b/1 from $F_2$: host b gets $Q_2$, entry $(0, Q_2)$. | c/1 at 0 |
| NEXT(0) | The heap gives $(0, Q_2)$. REFILL($Q_2$) takes a/3 into $Q_1$, then finds the front queues empty and marks $Q_2$ free. | b/1 at 0 |
| NEXT(0) | The heap gives $(1, Q_1)$; next(a) = 2, entry $(2, Q_1)$. | a/2 at 1 |
| NEXT(1) | The heap gives $(2, Q_1)$; $Q_1$ is empty and nothing is left to refill. | a/3 at 2 |
| NEXT(2) | The heap is empty. | EMPTY |

The URL b/1 has the lower priority, but it goes before a/2, because host a must wait one time unit after a/1. Host a is contacted at times 0, 1 and 2, exactly one gap apart.

## Correctness

The file proofs/correctness.md proves the contract from four invariants. Each back queue is either free, with no owner and no heap entry, or not empty, with one owner and exactly one heap entry. Every URL in a back queue has the host of its owner, and each host owns at most one queue. Each URL of Seen is either waiting in exactly one queue or has been returned. For each owned queue, its heap time is at least next of its owner. ADD, REFILL and NEXT each keep these invariants.

Each URL is returned once, because Seen admits it once and it waits in one queue until NEXT removes it. When NEXT reports empty, no queue holds a URL. For politeness, when NEXT returns a URL of host $h$ at time $s$, it removes the only heap entry of $h$ and sets next$(h) = s + \delta(h)$. Any later entry for $h$ is created at line L8 or L15 with a time of at least next$(h)$, and line L6 never starts before the time of the entry. Line L15 reads next$(h)$ even for a host that had no queue, which is why the map next must keep old hosts. The order in each front queue is FIFO because line L2 appends at the tail and line L13 takes the head.

## Complexity

ADD costs $O(1)$ expected for the hash lookup and the append. Each URL later moves once from a front queue to a back queue, at a cost of $O(F)$ for the selector and $O(1)$ expected for the host lookup; charge this move to the ADD of the URL, which gives $O(F)$ amortized expected. Each call of NEXT does one EXTRACT-MIN and at most one INSERT on a heap of at most $B$ entries, and the REFILL calls at line L3 that do not end at line L15 empty the front stage, so they are paid by the moves. NEXT thus costs $O(\log B)$ amortized expected. A crawl with $U$ distinct URLs and $R$ calls of NEXT costs $O(U F + (U + R) \log B)$ expected time. The space is $O(U + B + H)$ for Seen, the queues, the heap and the map next over $H$ hosts. With a few priority levels, $F$ is a small constant. The bounds in the front matter are amortized and, because of the hash tables, expected.

## Variants

- **One queue per thread.** The 1999 Mercator crawler of Heydon and Najork had one FIFO subqueue for each worker thread, with hosts assigned to subqueues by a hash of the host name. One thread serves each host, so a host is never contacted by two threads at once, but there is no priority and no time gap.
- **Distributed frontier.** A crawl over many machines gives each machine a set of hosts, often by a hash of the host or by [consistent hashing](/consistent-hashing/). A machine that finds a URL of a host it does not own sends the URL to the owner.
- **Disk-based queues.** Large frontiers keep the queues on disk and only their heads and tails in memory, because the frontier can hold billions of URLs. Seen also lives on disk, often with a cache of popular URLs.
- **Gap from the fetch time.** Manning, Raghavan and Schuetze describe a common heuristic in which the gap after a fetch is about an order of magnitude larger than the time that the fetch took. A slow host then gets fewer requests.
- **Revisits.** A crawler that refetches pages puts known URLs back into the frontier with a priority from a [revisit policy](/crawl-revisit-policy/). Seen must then allow re-adds of URLs that are due.
- **Topical priority.** A [focused crawler](/focused-crawling/) sets the priority from a classifier score of the page that links to the URL.

## When to use it

Use the two-stage frontier in any crawler that fetches from many hosts at once and must respect a per-host gap. When the crawl is small or comes from one host, a single FIFO queue with a sleep between requests, which gives a [breadth-first](/breadth-first-search/) order, is enough. Manning, Raghavan and Schuetze suggest about three times as many back queues as crawler threads, so that most threads find a host that is ready.

## Pitfalls

- **Starvation.** With the strict selector, a steady flow of high priority URLs keeps low priority URLs in the front stage forever. Use a biased random selector if every URL must be fetched in the end.
- **Forgetting old hosts.** If the map next is dropped when a host loses its back queue, a URL of that host that arrives a moment later gets a fresh queue with the time now, and the host is contacted too early. The test file has this case.
- **Hosts versus servers.** Many host names can share one IP address, and one name can map to many servers. A gap per host name can still overload one server; some crawlers key the back queues by IP address.
- **Too few back queues.** With fewer active hosts than threads, threads wait idle on the heap even though URLs are waiting, because all of them belong to hosts that must wait.
- **URL normalization.** Seen catches only exact repeats. Normalize the URLs (case of the host, default ports, fragments, relative paths) before ADD, or the same page enters many times under different names.
- **robots.txt.** Politeness also means that the crawler obeys the robots exclusion file of each host. Check it before ADD or before the fetch, and cache it for each host.

## Implementations

## History

Heydon and Najork described the Mercator crawler of the Compaq Systems Research Center in 1999. Its frontier had one FIFO subqueue for each thread, so that each host was crawled by one thread only. In their 2001 report "High-performance web crawling", Najork and Heydon described the frontier with front queues for priority and back queues for politeness, with a heap of back queues ordered by the next allowed contact time. Manning, Raghavan and Schuetze made this design the standard textbook frontier in Chapter 20 of their 2008 book, and Olston and Najork survey it with other designs in their 2010 review of web crawling.

## References
