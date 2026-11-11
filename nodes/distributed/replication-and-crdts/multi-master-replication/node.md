---
tag: WPTZGD
kind: concept
slug: multi-master-replication
name: Multi-master replication
aliases:
- multi-leader replication
- active-active replication
area: distributed/replication-and-crdts
level: intro
summary: Several replicas each accept writes and forward them to the others, so concurrent writes can conflict and must be detected and resolved, for example by LWW or CRDTs.
prereqs: [eventual-consistency, concurrent-events]
see_also: [leaderless-replication, primary-backup-replication, last-writer-wins, crdt, version-vectors, operational-transformation, strong-eventual-consistency, anti-entropy]
sources:
  - paper: "Douglas B. Terry, Marvin M. Theimer, Karin Petersen, Alan J. Demers, Mike J. Spreitzer and Carl H. Hauser, Managing update conflicts in Bayou, a weakly connected replicated storage system, Proceedings of the 15th ACM Symposium on Operating Systems Principles (SOSP), 1995"
    locator: the sections on dependency checks and merge procedures, tentative and committed writes, and the primary server that commits writes
  - paper: "Paul R. Johnson and Robert H. Thomas, The maintenance of duplicate databases, RFC 677, 1975"
    locator: the use of timestamps on updates so that all copies keep the update with the latest timestamp
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, the section Multi-Leader Replication (use cases, handling write conflicts, multi-leader replication topologies)
  - paper: doi:10.1145/41840.41841
    title: Alan Demers and others, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1 (updates accepted at any site and spread to the others, with timestamps to decide between them)
---

Multi-master replication lets several replicas, the masters or leaders, accept writes at the same time. Each master applies a write locally, answers the client and forwards the write to the other masters, usually in the background. This keeps writes fast and available when masters are far apart or cut off from each other, but it gives up a single order of writes: two masters can accept conflicting writes to the same item, and the system must **detect** the conflict and **resolve** it so that all replicas end in the same state. [Primary-backup replication](/primary-backup-replication/) avoids conflicts by having one writer. [Leaderless replication](/leaderless-replication/) has no leaders at all and sends each write to several replicas in parallel. Multi-master sits between them: each write has one home master, but there are several homes.

## In plain words

A family shares a calendar, and each person keeps a copy on their own phone. Anyone can add or change an entry on their phone, even with no signal. When the phones connect, they send each other the changes.

Most of the time the changes do not touch the same entry, and the copies simply combine. Sometimes two people change the same entry while apart. One moves dinner to 6, the other to 7. Now the phones must notice that the two changes clash, and they must pick a rule. They can keep the later change, keep both and ask a person, or merge the two in some fixed way. Every phone must use the same rule, or the copies stay different.

## The idea

### Accepting and forwarding writes

Each master keeps a full copy. A write at master $i$ is applied to the copy of $i$ and gets an identity, for example a pair (master, sequence number). The master sends its writes to the others along some topology: all to all, a ring, or a star. A master that receives a write applies it, unless it has seen it before. The links can be slow or down for a long time; writes then queue up and are sent later, as in [anti-entropy](/anti-entropy/).

The model is the [asynchronous model](/asynchronous-model/) with message passing and [crash-recovery](/crash-recovery/) failures, and with partitions that can last a long time. No master waits for another before it answers, so the system is available during partitions, and the guarantee it can aim for is [eventual consistency](/eventual-consistency/).

### Detecting conflicts

Two writes conflict when they touch the same data and neither was made with knowledge of the other, that is, they are [concurrent](/concurrent-events/) in the sense of [happened-before](/happened-before/). A system detects this with [version vectors](/version-vectors/): each item carries a vector of counters, one per master, and two versions conflict exactly when neither vector is at least the other in every entry. Systems that use only one timestamp per item cannot tell a conflict from an overwrite.

### Resolving conflicts

- **Last-writer-wins.** Keep the write with the larger timestamp and drop the other ([last-writer-wins](/last-writer-wins/)). Johnson and Thomas (1975) used this rule for duplicate databases. It is simple and converges, but it loses writes and depends on clocks.
- **Keep siblings.** Keep all concurrent values and let the next reader, or the application, merge them. Dynamo returns such siblings to the client.
- **Merge by data type.** Store a [CRDT](/crdt/) such as a [PN-counter](/pn-counter/), an [OR-set](/or-set/) or an [LWW-register](/lww-register/). Its merge is commutative, associative and idempotent, so the replicas converge however the writes arrive; see [strong eventual consistency](/strong-eventual-consistency/).
- **Application merge code.** In Bayou (Terry et al. 1995), each write carries a dependency check, a query with an expected result, and a merge procedure. A server that applies the write runs the check on its copy; if the check fails, it runs the merge procedure in place of the update.
- **Transform operations.** Collaborative editors change concurrent operations so that they can be applied in any order; see [operational transformation](/operational-transformation/) and [collaborative text editing](/collaborative-text-editing/).

### Bayou's order of writes

Bayou shows how far one can go. Each server keeps its writes in an order: committed writes first, in the order chosen by one primary server, then tentative writes in timestamp order. When a server learns of new writes, it undoes the tentative writes, inserts the new ones and redoes them, so all servers that have seen the same writes reach the same state. The primary gives a final order, so a write is first tentative and later committed. This mixes multi-master writes with a single point that fixes the order.

## Examples

**Two datacenters.** Masters $M_1$ in Europe and $M_2$ in Asia replicate a user table. A user in Europe changes their name to "Ann", and at the same time an agent in Asia changes it to "Anne". Each master applies its own write and replies. When the writes cross, $M_1$ sees "Anne" and $M_2$ sees "Ann". With last-writer-wins on timestamps 1000 and 1003 both keep "Anne", and "Ann" is lost. With version vectors, $M_1$ has $[1, 0]$ for "Ann" and receives $[0, 1]$ for "Anne"; neither is at least the other, so both masters keep both values and flag the conflict.

**A meeting room in Bayou.** Two users book the same room from their laptops while offline, each for 10:00. The first write to reach the primary is committed. The second write's dependency check, "the room is free at 10:00", fails there, so its merge procedure runs and books the next free slot it lists, say 11:00.

**A shared counter.** Two masters count page views. If each stores a plain number and forwards the new number, concurrent increments are lost. If each stores a [G-counter](/g-counter/), each master increases its own entry and the merge takes the maximum per entry, so no increment is lost.

## Where it is used

- **Databases across datacenters.** Several relational and document databases offer multi-master modes so that each region writes locally; conflicts are resolved by timestamps or by custom handlers.
- **Offline-first and mobile apps.** Each device is a master while it is offline, and syncs later. Calendars, notes and the CouchDB family of stores work this way.
- **Collaborative editing.** Each editor is a master for its own edits, merged with [operational transformation](/operational-transformation/) or sequence CRDTs such as [RGA](/rga/).
- **Directory and naming services.** Older systems such as Grapevine and Clearinghouse spread updates between servers with timestamps, which is the setting of the epidemic algorithms of Demers et al. (1987).

## References
