---
tag: S70T95
kind: concept
slug: leaderless-replication
name: Leaderless replication
aliases:
- masterless replication
area: distributed/replication-and-crdts
level: intro
summary: Any replica accepts reads and writes; a client or coordinator sends each request to N replicas and waits for W or R replies, with no leader to order writes.
prereqs: [quorum-intersection, eventual-consistency]
see_also: [quorum-replication, dynamo-style-replication, multi-master-replication, read-repair, anti-entropy, sloppy-quorum, last-writer-wins, version-vectors]
sources:
  - paper: doi:10.1145/800215.806583
    title: David K. Gifford, Weighted voting for replicated data, Proceedings of the 7th ACM Symposium on Operating Systems Principles (SOSP), 150-162, 1979
    locator: reads and writes that collect votes from several copies, with no copy in charge, and version numbers to find the current copy
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia and others, Dynamo, Amazon's highly available key-value store, Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP), 205-220, 2007
    locator: Section 4.5 (execution of get and put operations with N, R and W) and Section 4.4 (data versioning)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, the section Leaderless Replication (writing when a node is down, quorums for reading and writing, limitations of quorum consistency)
  - paper: doi:10.1145/1773912.1773922
    title: Avinash Lakshman and Prashant Malik, Cassandra, a decentralized structured storage system, ACM SIGOPS Operating Systems Review 44(2), 35-40, 2010
    locator: the sections on replication and on reads and writes at a chosen consistency level
---

Leaderless replication is a family of replication schemes in which no replica is in charge. A client, or a node acting for the client, sends each write to all $N$ replicas of a key and treats the write as done when $W$ of them acknowledge; it sends each read to the replicas and waits for $R$ replies, keeping the newest version among them. The idea goes back to Gifford's weighted voting (1979), and Amazon's Dynamo (2007) made it common in key-value stores. Compared with [multi-master replication](/multi-master-replication/), where several leaders each order their own writes and forward them, a leaderless system has no leaders at all: the writes go to the replicas in parallel. Compared with [Dynamo-style replication](/dynamo-style-replication/), which is one complete design with a hash ring, sloppy quorums, hinted handoff and vector clocks, leaderless replication is the general pattern that design belongs to.

## In plain words

Imagine three shops that each keep a price list. There is no head shop. When the price of an item changes, the owner phones all three shops, and is happy as soon as two of them confirm. When a customer wants a price, they phone the shops and wait for two answers. Each price has a date, and the customer takes the price with the latest date.

Because any two pairs of shops share a shop, the customer always reaches at least one shop that heard about the last change.

One shop may still have an old price. Someone has to fix that. A customer who sees the old price can tell that shop the new one. The shops can also compare their lists now and then.

## The idea

**Writes.** A key has $N$ replicas. The writer sends the new value with a version to all $N$ and waits for $W$ acknowledgements. A replica that is down or slow simply misses the write. No failover is needed, because no replica is special.

**Reads.** The reader sends the request to the replicas, waits for $R$ replies and returns the value with the newest version. If $R + W > N$, every read set meets every write set (see [quorum intersection](/quorum-intersection/)), so a read that starts after a write has completed sees it. Typical settings are $N = 3$ with $R = W = 2$; $W = N$ and $R = 1$ for fast reads; or $R = W = 1$ for speed with no overlap.

**Versions and conflicts.** Without a leader, two clients can write the same key at the same time through different replicas, and the replicas can receive the two writes in different orders. The system must decide what to keep. One choice is [last-writer-wins](/last-writer-wins/), which keeps the write with the larger timestamp and drops the other. Another is to track causality with [version vectors](/version-vectors/), keep concurrent values as siblings and let the application merge them, or store a [CRDT](/crdt/) that merges by itself.

**Catching up.** A replica that missed a write stays stale until something repairs it. Leaderless systems use two mechanisms: [read repair](/read-repair/), where a read that sees an old version writes the new one back, and [anti-entropy](/anti-entropy/), a background process that compares replicas and copies missing data. Read repair fixes only keys that are read, so anti-entropy is needed for the rest.

**What quorums do not give.** Even with $R + W > N$, a leaderless store is usually not [linearizable](/linearizability/). A read that overlaps a write in progress can see the new value while a later read sees the old one, unless reads write back before they return, as the ABD register does (see [quorum replication](/quorum-replication/)). Writes that fail at some replicas are not rolled back at the others. Clock-based conflict resolution can drop writes. A [sloppy quorum](/sloppy-quorum/), which accepts writes at any healthy nodes when home replicas are down, gives up the overlap altogether. The usual guarantee is [eventual consistency](/eventual-consistency/).

**The model.** The scheme runs in the [asynchronous model](/asynchronous-model/) with message passing and [crash failures](/crash-failure/) of replicas; with $N$ replicas a write survives $N - W$ crashes and a read survives $N - R$. Network partitions are allowed, and the system stays available on each side for any request that can still gather its quorum.

## Examples

**Three replicas, $R = W = 2$.** Replicas $A$, $B$, $C$ hold $x = 1$ at version 1. Replica $C$ is down. A client writes $x = 2$ at version 2; $A$ and $B$ acknowledge, which meets $W = 2$. $C$ comes back still holding version 1. Another client reads from $B$ and $C$, gets versions 2 and 1, and returns 2. With read repair it also sends version 2 to $C$.

**$R = W = 1$.** The same write is acknowledged by $A$ alone. A read that asks only $C$ returns $x = 1$ after the write completed. This is a stale read; the settings allow it.

**Concurrent writes.** Two clients write $x = 5$ and $x = 7$ at the same time. $A$ receives 5 then 7; $B$ receives 7 then 5. If each replica keeps the last value it received, they now disagree for good. With last-writer-wins on timestamps they agree on the write with the larger timestamp, and the other write is lost. With version vectors each replica sees that the two writes are concurrent and keeps both.

## Where it is used

- **Dynamo and its descendants.** Amazon's Dynamo, Apache Cassandra, Riak and Project Voldemort all replicate without a leader, with $N$, $R$ and $W$ set per table or per request; see [Dynamo-style replication](/dynamo-style-replication/).
- **Weighted voting in databases.** Gifford's scheme assigns votes to copies and reads and writes through vote quorums; see [quorum replication](/quorum-replication/).
- **Multi-datacenter stores.** A request can be satisfied by replicas in the local datacenter while the remote ones catch up in the background, which keeps latency low across wide-area links.
- **Systems that must stay writable.** Shopping carts and session stores, where a lost write costs more than a stale read, use leaderless writes with conflict merging.

## References
