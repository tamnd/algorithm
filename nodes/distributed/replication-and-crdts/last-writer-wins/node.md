---
tag: SZ23RT
kind: concept
slug: last-writer-wins
name: Last-writer-wins (LWW)
aliases:
- LWW
- last-write-wins
area: distributed/replication-and-crdts
level: intro
summary: Keep the update with the largest timestamp and break ties by replica id; replicas converge, but concurrent writes are lost and a fast clock can beat a later write.
prereqs: [lamport-clocks, clock-skew, concurrent-events]
see_also: [lww-register, lww-element-set, multi-master-replication, leaderless-replication, hybrid-logical-clocks, version-vectors, tombstone, mv-register]
sources:
  - paper: "Paul R. Johnson and Robert H. Thomas, The maintenance of duplicate databases, RFC 677, 1975"
    locator: the timestamp on each update and the rule that a copy keeps the update with the latest timestamp
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, the subsection Last write wins (discarding concurrent writes); Chapter 8, the subsection Timestamps for ordering events
  - url: https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/tombstones.html
    title: Apache Cassandra documentation, Tombstones
    locator: the rules that the cell with the newer timestamp wins and that on equal timestamps a deletion wins over a write
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 558-565, 1978
    locator: the clock condition and the total order of events obtained by breaking ties with process ids
---

Last-writer-wins (LWW) is a rule for resolving conflicting updates to one replicated item: each update carries a timestamp, every replica keeps the update with the largest timestamp, and ties are broken by a replica id so that all replicas pick the same one. The rule is a merge that is commutative, associative and idempotent, so the replicas converge whatever order the updates arrive in. The price is that "last" means "largest timestamp", not "last in real time" or "last in causal order". Of two concurrent updates, one is silently thrown away. With physical clocks, a replica whose clock runs fast can win over a write that was made later and with full knowledge of it. This page is about the rule itself; the CRDTs that package it as a data type are the [LWW-register](/lww-register/) and the [LWW-element-set](/lww-element-set/).

## In plain words

Several people keep copies of one note. Each time someone changes the note, they write the time of the change next to it. When two copies disagree, everyone keeps the version with the latest time. If two versions show the same time, they keep the one from the person whose name comes later in a fixed list.

This always ends with everyone holding the same note. But if two people changed the note at about the same time, one of the changes is gone, and nobody is told.

The clocks are a second problem. If one person's watch runs ten minutes fast, their old change can look newer than a real later change by someone else, and the later change is thrown away.

## The idea

**The rule.** An update to the item is a pair $(\mathit{stamp}, v)$ with $\mathit{stamp} = (t, i)$, a timestamp $t$ and the id $i$ of the replica that made it. Stamps are ordered by $t$ and then by $i$. A replica holds one pair. When it makes or receives an update $u$, it sets its pair to the larger of the two:

$$\mathrm{merge}((s_1, v_1), (s_2, v_2)) = \begin{cases} (s_1, v_1) & \text{if } s_1 \ge s_2, \\ (s_2, v_2) & \text{otherwise.} \end{cases}$$

Each replica must give its own updates distinct stamps; if its clock has not moved since its last write, it uses the last timestamp plus one. Then all stamps are distinct, and merge is the maximum under a total order. The maximum is commutative, associative and idempotent, so after every replica has received every update, all of them hold the update with the largest stamp. This is convergence in the sense of [eventual consistency](/eventual-consistency/), and with a merge that is a join in a [join-semilattice](/join-semilattice/), it is the [CRDT convergence theorem](/crdt-convergence-theorem/) at work.

**What gets lost.** Two updates are [concurrent](/concurrent-events/) if neither replica had seen the other when it wrote. LWW keeps exactly one of them, so the effect of the other disappears. Even an update that came causally after another can lose: LWW orders by timestamp, and timestamps from physical clocks need not agree with [happened-before](/happened-before/).

**Clock skew.** Physical clocks differ by some [skew](/clock-skew/) and [drift](/clock-drift/), even when synchronized with [NTP](/ntp/). If replica $A$'s clock is ahead by $\Delta$, every update from $A$ beats every update made elsewhere within $\Delta$ after it in real time, including updates whose writers had read $A$'s value. There are three common repairs. A [Lamport clock](/lamport-clocks/) moves past every timestamp it has seen, so an update made after seeing another always gets a larger stamp; concurrent updates are still decided arbitrarily. A [hybrid logical clock](/hybrid-logical-clocks/) does the same while staying close to physical time. A bounded clock uncertainty, as in [TrueTime](/truetime/), lets a writer wait out the uncertainty so that later commits carry larger timestamps.

**The model.** LWW needs no coordination and no particular timing model: it works in the [asynchronous model](/asynchronous-model/) with message passing, any number of crashes, and partitions, as long as updates eventually reach every replica. Its outcome, however, depends on the clocks. With physical timestamps, which update survives depends on the skew between replicas.

**LWW and its neighbours.** A [multi-value register](/mv-register/) keeps all concurrent values and lets the reader choose, so it loses nothing but needs [version vectors](/version-vectors/). LWW keeps one value with one stamp, so it is small and simple. Deletion under LWW is an update with a special value, a [tombstone](/tombstone/), so that a delete can win over an older write.

## Examples

**A lost concurrent write.** Three replicas of a shopping cart. At real time 10, replica 1 writes "cart = {book}" with stamp (10, 1), and replica 2 writes "cart = {pen}" with stamp (10, 2). Neither has seen the other. When the updates spread, every replica compares the stamps, and (10, 2) is larger by id. All replicas end with "cart = {pen}". The book is gone, and no replica records that it ever existed.

**A fast clock wins over a later write.** Replica $A$'s clock is 100 units ahead. At real time 10, $A$ writes "a" with stamp (110, A). Replica $B$ receives it at time 15, so $B$ now holds "a". At time 20, $B$ writes "b" with stamp (20, B), as a change of "a". When $A$ receives "b", it compares (110, A) with (20, B) and keeps "a". Both replicas end with "a", although "b" was written later, by a writer who knew about "a". With Lamport clocks, $B$ would have set its clock past 110 when it received "a", stamped "b" with 111, and both replicas would end with "b".

**Order does not matter.** Updates with stamps (3, 0), (7, 2), (7, 1) and (1, 3) reach a replica in any of the 24 orders. In each order the replica ends with the update stamped (7, 2).

## Where it is used

- **Cassandra.** Every cell carries a write timestamp, and when replicas disagree the cell with the newer timestamp wins. On equal timestamps a deletion wins over a write, and between two writes the larger value wins. Timestamps come from the coordinator or the client, so clock skew between them decides conflicts.
- **Dynamo-style stores.** Some stores offer LWW as an option in place of keeping siblings with vector clocks; see [Dynamo-style replication](/dynamo-style-replication/) and [leaderless replication](/leaderless-replication/).
- **Duplicate databases.** Johnson and Thomas (1975) proposed timestamps on updates, with each copy keeping the latest, for databases kept at several sites; this is the origin of the rule.
- **CRDTs.** The [LWW-register](/lww-register/) and [LWW-element-set](/lww-element-set/) use the rule per register or per element, and many CRDT maps use it for each field.
- **Caches and configuration.** Systems where only the latest value matters and losing a concurrent write is harmless, such as presence status or settings, use LWW for its low cost.

## References
