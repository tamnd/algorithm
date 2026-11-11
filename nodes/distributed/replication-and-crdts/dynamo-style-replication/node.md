---
tag: 4YS13H
kind: algorithm
slug: dynamo-style-replication
name: Dynamo-style replication
aliases:
- Dynamo
area: distributed/replication-and-crdts
level: advanced
summary: Amazon's Dynamo design. A hash ring with virtual nodes picks N replicas per key; puts wait for W, gets for R; sloppy quorums, hints, vector clocks and Merkle trees repair it.
model: asynchronous-model
complexity:
  vars: {n: the number of physical nodes, N: the number of replicas of a key, v: the number of virtual nodes per physical node}
  messages: {worst: Θ(N)}
  space: {extra: O(n v)}
properties: {deterministic: true, recursive: false}
history:
  year: 2007
  people: [Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, Gunavardhan Kakulapati, Avinash Lakshman, Alex Pilchin, Swaminathan Sivasubramanian, Peter Vosshall, Werner Vogels]
  note: The Dynamo paper (SOSP 2007) combined consistent hashing, sloppy quorums, hinted handoff, vector clocks and Merkle tree anti-entropy into one always-writable key-value store.
prereqs: [leaderless-replication, consistent-hashing, quorum-intersection, vector-clocks]
see_also: [sloppy-quorum, hinted-handoff, read-repair, anti-entropy, virtual-nodes, merkle-tree, last-writer-wins, quorum-replication]
sources:
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, Gunavardhan Kakulapati, Avinash Lakshman, Alex Pilchin, Swaminathan Sivasubramanian, Peter Vosshall and Werner Vogels, Dynamo, Amazon's highly available key-value store, Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP), 205-220, 2007
    locator: Section 4.2 (partitioning, virtual nodes), 4.3 (replication, preference list), 4.4 (data versioning, vector clocks), 4.5 (get and put with R and W), 4.6 (sloppy quorum, hinted handoff), 4.7 (Merkle tree anti-entropy), 4.8 (gossip membership) and Section 5 (read repair)
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, Proceedings of the 29th ACM Symposium on Theory of Computing (STOC), 654-663, 1997
    locator: the consistent hashing construction that Dynamo's ring is based on
  - paper: doi:10.1145/1773912.1773922
    title: Avinash Lakshman and Prashant Malik, Cassandra, a decentralized structured storage system, ACM SIGOPS Operating Systems Review 44(2), 35-40, 2010
    locator: the sections on partitioning and replication, a later system with the same ring and quorum design
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, the section Leaderless Replication (read repair and anti-entropy, sloppy quorums and hinted handoff, detecting concurrent writes)
---

Dynamo-style replication is the design of Amazon's Dynamo key-value store (DeCandia et al. 2007), and of the stores that copied it. Keys live on a [consistent hashing](/consistent-hashing/) ring with [virtual nodes](/virtual-nodes/). Each key has a **preference list**: the first $N$ distinct physical nodes clockwise from the key's position. A put is sent to $N$ nodes and succeeds when $W$ of them store it; a get asks $N$ nodes and returns after $R$ replies. To stay writable when nodes fail, Dynamo uses a **sloppy quorum**: the first $N$ *healthy* nodes on the ring take the request, and a stand-in node keeps a **hint** that names the home node and hands the data back later. Versions carry [vector clocks](/vector-clocks/), so concurrent writes become siblings that the client merges. [Read repair](/read-repair/) and [Merkle tree](/merkle-tree/) [anti-entropy](/anti-entropy/) bring stale replicas up to date. This page is about that complete design; the general pattern of writes and reads to several replicas with no leader is [leaderless replication](/leaderless-replication/).

## In plain words

Picture a round table with many seats, and a few people who each sit in several seats. To store a note, you find the note's place on the table, walk clockwise, and give a copy to the first three different people you meet. You count the note as saved when two of them say they have it. To read, you ask the three and wait for two answers.

If one of the three is away, you give the copy to the next person around the table, with a slip that says "this belongs to the person who is away". When that person comes back, the slip tells the stand-in to pass the note on.

Two people can change the same note at the same time. Each copy keeps a small record of who changed it, so the next reader can see that the changes clash and can combine them.

## The problem

Store values by key so that writes are always accepted, even during node failures and network partitions, and so that all replicas of a key converge once failures heal. The model is the [asynchronous model](/asynchronous-model/) with message passing, [crash-recovery](/crash-recovery/) failures of nodes, and partitions; nodes are trusted, so there are no Byzantine faults. The target is [eventual consistency](/eventual-consistency/), not [linearizability](/linearizability/): the design chooses availability during partitions, in the sense of the [CAP theorem](/cap-theorem/).

## The algorithm

Each node has $v$ tokens on a ring of hash values. The **walk** of a key is the list of distinct physical nodes met clockwise from $h(\mathit{key})$. The coordinator of a request is the first reachable node in the walk.

```pseudo id=main
PUT(key, value, context)                    ▷ at the coordinator c
L1  P ← the first N nodes in the walk of key                   ▷ preference list
L2  T ← the first N reachable nodes in the walk; a node of T outside P gets a hint naming a node of P not in T
L3  clock ← entrywise max of the clocks in context; clock[c] ← clock[c] + 1
L4  send (clock, value) and the hints to every node in T; each node keeps it unless one of its versions descends from it
L5  succeed when W nodes have stored it

GET(key)
L6  ask the nodes of T; wait for R replies
L7  V ← the versions in the replies, minus those that another version strictly descends from
L8  send V to every replier whose versions differ from V      ▷ read repair
L9  return V; the clocks of V are the context for the next PUT

HANDOFF, periodically at a node x
L10 for each hint (home, key) at x: if home is reachable, send the versions of key to home, then drop the hint, and drop key if x is not in its preference list
```

Line L1 fixes where a key lives. Virtual nodes give each physical node many small ranges, which spreads load and spreads the data of a failed node over many others; the walk skips repeated physical nodes so that the $N$ replicas are on different machines. Line L2 is the sloppy quorum: with all home nodes reachable, $T = P$; otherwise healthy nodes further along the ring stand in. With a strict quorum, $T$ would be $P$ minus the unreachable nodes, and a put with fewer than $W$ of them fails. Line L3 makes the new version descend from every version the client read, so it replaces them; versions written without knowledge of each other have clocks that do not compare, and both survive line L7 as siblings. Lines L8 and L10 are two of the three repair paths; the third is a background exchange in which replicas of each key range compare Merkle trees and copy the keys whose hashes differ (see [anti-entropy](/anti-entropy/)).

Dynamo leaves the merge of siblings to the application: the client reads all siblings, merges them (the shopping cart takes the union of items), and writes the result with the merged context, which then descends from all of them.

## Example

Five nodes A to E, $N = 3$, $R = W = 2$. The key cart:42 has the walk B, A, C, D, E, so its preference list is B, A, C. It holds "old" on all three.

1. A partition splits the cluster into {B, D, E} and {A, C}. A client on the first side writes "new" with the context of "old". Only B of the home nodes is reachable. With a strict quorum, $T = \{B\}$ and the put fails. With a sloppy quorum, $T$ is B, D, E: D stores the version with the hint "for A" and E with the hint "for C". Three nodes store it, so the put succeeds with $W = 2$.
2. A client on the second side reads. It asks A and C, gets "old" from both, and returns "old". Here $R + W = 4 > 3 = N$, but the read set {A, C} and the write set {B, D, E} do not meet, so the read misses a successful write. This is the cost of the sloppy quorum; see [sloppy quorum](/sloppy-quorum/).
3. The partition heals. In the next handoff D sends "new" to A and E sends "new" to C, each drops its hint and its copy. Now B, A and C all hold "new", and every read returns it.

**Siblings.** Two clients read the cart with clock [B:1] and value {book}. One writes {book, pen} through B, with clock [B:2]. The other, cut off from B, writes {book, cup} through A, with clock [A:1, B:1]. Neither clock is at least the other in every entry, so a get that reaches both returns two siblings. The client merges them to {book, cup, pen} and writes it through B with the merged context; its clock [A:1, B:3] descends from both, and line L7 then drops the old siblings.

## Correctness

Dynamo promises eventual consistency, and, with strict quorums, fresh reads after completed writes. Assume that a node never loses what it has stored.

**Theorem.** (a) *Convergence.* Suppose puts stop, every node recovers, every partition heals, and handoff and anti-entropy run until no more data moves. Then every home node of a key holds the same set of versions: the versions written for that key that no other written version descends from. (b) *Strict quorums.* Without sloppy quorums and with $R + W > N$, a get that starts after a put of version $u$ has succeeded returns some version that descends from $u$, provided no node lost data.

*Proof sketch.* (a) The local update of line L4 and the repairs of lines L8 and L10 all replace a node's versions $S$ by $\max(S \cup S')$, the versions of $S \cup S'$ not strictly dominated by another. On finite sets of versions ordered by clock descent, this operation is commutative, associative and idempotent, so it is the join of a [join-semilattice](/join-semilattice/); the result after any set of merges depends only on the union of the versions merged in. Handoff delivers every hinted version to its home, and anti-entropy makes every pair of home replicas exchange whatever they lack, so at the end each home has merged the same union, and holds its maximal elements. (b) A successful put stored $u$ at $W$ home nodes (with a strict quorum all of $T$ are home nodes). A later get reads $R$ home nodes, and $R + W > N$ forces one node in both. A node's versions only grow under the join, so that node still holds $u$ or a version that descends from $u$, and line L7 keeps a version that descends from it. The full proof is in the proof file.

With sloppy quorums, (b) fails: the example gives a get that misses a successful put although $R + W > N$. Even with strict quorums Dynamo is not linearizable: reads do not wait for their write-back, and siblings are by design.

## Complexity

- **Messages.** A put sends to $N$ nodes and gets up to $N$ acks; a get the same; so $\Theta(N)$ per request, independent of the cluster size $n$. Handoff sends one message per hinted key.
- **Time.** A request needs one round trip from the coordinator. Its latency is that of the $W$-th or $R$-th fastest reply, which is why small $R$ and $W$ make requests fast.
- **Space.** Each node keeps the $nv$ tokens of the ring, found by gossip, and finds a preference list by binary search in $O(\log(nv))$ time plus a walk. Vector clocks grow with the number of coordinators that wrote a key; Dynamo truncates a clock when it exceeds a size limit, by dropping the oldest entry.
- **Repair.** A Merkle tree comparison between two replicas of a range costs messages proportional to the number of differing keys times the tree depth, not to the size of the range.

## Properties

- **Always writable.** With a sloppy quorum, a put succeeds whenever any $W$ nodes are reachable, even if every home node is down.
- **Tunable.** $N$, $R$ and $W$ are set per instance. Dynamo reports $(N, R, W) = (3, 2, 2)$ as common; $R = 1$ suits read-heavy data; $W = 1$ never rejects a write.
- **Divergent versions.** Concurrent puts create siblings that clients must merge. Merges such as union can bring back deleted cart items, which the paper notes.
- **No single point of failure.** Every node runs the same code; membership and failure information spread by gossip.
- **Not linearizable.** Stale reads are possible with sloppy quorums, after partial failures, and while repairs are pending.

## Variants and improvements

- **Last-writer-wins in place of siblings.** Cassandra and others resolve conflicts by timestamp per cell, which loses one of two concurrent writes; see [last-writer-wins](/last-writer-wins/).
- **Dotted version vectors.** Riak replaced plain vector clocks with [dotted version vectors](/dotted-version-vectors/), which track siblings exactly without growing with the number of clients.
- **CRDT values.** Storing [CRDTs](/crdt/) such as an [OR-set](/or-set/) makes the merge automatic and keeps deletes.
- **Strict quorums and write back.** Using $T = P$ and making reads write back before they return gives the atomic register of [quorum replication](/quorum-replication/), at the cost of availability.
- **Partitioning strategies.** The paper moves from random tokens to fixed, equal-size partitions assigned to nodes, which simplifies bootstrapping and Merkle tree upkeep (Section 6.2).

## When to use it

Use the Dynamo design for data that must accept writes during failures and partitions, where clients can merge conflicting versions or a lost concurrent write is acceptable: shopping carts, session state, user preferences, counters built as CRDTs. Do not use it where a read must see the latest write, or for operations such as unique name claims and balance checks; use [quorum replication](/quorum-replication/) with write back, or consensus-based replication such as [Raft](/raft/), there.

## Pitfalls

- **Reading R + W > N as a guarantee.** Wrong: assume fresh reads whenever $R + W > N$. Right: this holds only with strict quorums and no data loss. Sloppy quorums, the default for availability, break it, as the example shows.
- **Clock truncation.** Wrong: drop old clock entries freely. Right: a truncated clock can make a descendant look concurrent, so truncation trades space for spurious siblings.
- **Merging that loses deletes.** Wrong: merge two cart siblings by union. Right: union brings back items removed in one sibling; record removes, as an OR-set does.
- **Hinted data with no home.** Wrong: rely on handoff alone. Right: a stand-in can fail before handoff, so anti-entropy must also run; see [hinted handoff](/hinted-handoff/).
- **Read repair as the only repair.** Wrong: rely on reads to fix replicas. Right: keys that are never read stay stale; see [read repair](/read-repair/).

## Implementations

The Python code models the ring with virtual nodes, preference lists, vector clock versions with siblings, strict and sloppy quorums, read repair and hinted handoff. Each operation runs as one atomic step, and the set of nodes that a coordinator can reach models crashes and partitions.

## History

Consistent hashing comes from Karger et al. (1997). Weighted voting with read and write quorums comes from Gifford (1979), and vector clocks from the work of Fidge and Mattern (1988). DeCandia et al. (2007) put these together for Amazon's shopping cart service and other services that had to stay writable, added sloppy quorums and hinted handoff, and reported on running the system in production. The design spread through open source systems: Cassandra (Lakshman and Malik 2010) took the ring and the quorums, Riak and Project Voldemort the full scheme with vector clocks.

## References
