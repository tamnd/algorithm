---
tag: Y5F2MS
kind: concept
slug: eventual-consistency
name: Eventual consistency
aliases:
- eventual consistency model
area: distributed/replication-and-crdts
level: intro
summary: If updates stop, all replicas eventually return the same value; no bound on how long convergence takes.
prereqs: [consistency-models]
see_also: [strong-eventual-consistency, crdt, session-guarantees, causal-consistency, anti-entropy, dynamo-style-replication, cap-theorem, last-writer-wins]
sources:
  - paper: doi:10.1145/1435417.1435432
    title: Werner Vogels, Eventually consistent, Communications of the ACM 52(1), 2009
    locator: pages 40 to 44 (the definition "if no new updates are made to the object, eventually all accesses will return the last updated value", the inconsistency window, and the client-side variations)
  - paper: doi:10.1145/224056.224070
    title: Douglas B. Terry, Marvin M. Theimer, Karin Petersen, Alan J. Demers, Mike J. Spreitzer and Carl H. Hauser, Managing update conflicts in Bayou, a weakly connected replicated storage system, SOSP 1995
    locator: the write log, tentative and committed writes, dependency checks and merge procedures, and anti-entropy between pairs of servers
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia et al., Dynamo, Amazon's highly available key-value store, SOSP 2007
    locator: Section 4 (versioning with vector clocks, sloppy quorums, hinted handoff, and anti-entropy with Merkle trees), Section 6 (the measured share of reads that see divergent versions)
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, Lecture Notes in Computer Science 6976, Springer
    locator: Section 2.2 (Definition 2, eventual consistency with eventual delivery, convergence and termination; Definition 3, strong eventual consistency)
  - paper: "Peter Bailis and Ali Ghodsi, Eventual consistency today, limitations, extensions, and beyond, ACM Queue 11(3), 2013, also in Communications of the ACM 56(5), 2013"
    title: Peter Bailis and Ali Ghodsi, Eventual consistency today, limitations, extensions, and beyond, 2013
    locator: eventual consistency as a liveness property without safety, probabilistically bounded staleness, and the measured windows of inconsistency
---

Eventual consistency is the weakest common guarantee of replicated data. In the words of Vogels (2009): if no new updates are made to an object, eventually all accesses will return the last updated value. Each replica accepts reads and writes at once, from its own copy, and replicas exchange updates in the background, so the system stays available when the network breaks. The guarantee says nothing about what a read returns while updates continue, and gives no bound on how long the replicas take to agree.

## In plain words

Picture several copies of a phone book kept in different cities. Each office changes its own copy whenever it likes, and the offices mail their changes to each other.

At any moment, two offices may give different answers for the same name, because news has not yet arrived. Eventual consistency promises only this: if people stop making changes, the mail catches up and all offices give the same answer in the end.

It does not say how long that takes. It does not say what to do when two offices changed the same entry in different ways. The system must pick a rule for that, such as "keep the later change", or keep both and ask a person.

## The idea

**Model.** There are $n$ replicas of a data store. A client sends each request to one replica, which answers from its local state at once, without waiting for any other replica. Replicas propagate updates to each other asynchronously, by [anti-entropy](/anti-entropy/), gossip or hints. Messages may be delayed, lost and repeated, and the network may partition.

**Definitions.** Several precise forms exist.

- **Vogels (2009).** If updates stop, all reads eventually return the last updated value. This is a *quiescent* form: it promises nothing in an execution where updates never stop.
- **Shapiro et al. (2011), Definition 2.** *Eventual delivery*: an update delivered at one correct replica is eventually delivered at all of them. *Convergence*: replicas that have delivered the same updates eventually reach equivalent states. *Termination*: every operation terminates. This form needs no quiescence. [Strong eventual consistency](/strong-eventual-consistency/) strengthens convergence so that it holds at once, not eventually.
- **Burckhardt et al. (2014).** In terms of visibility: an update cannot stay invisible to infinitely many later operations, and values do not appear out of thin air.

All of these are *liveness* properties, except the "no thin air" axiom. A store that returns any value at all, as long as it later returns the right one, meets the quiescent form; Bailis and Ghodsi (2013) point out that eventual consistency by itself has no safety part.

**Three things an implementation must choose.**

1. *Propagation.* How updates reach every replica: push on write, periodic pairwise anti-entropy with Merkle trees or version vectors, read repair, or hinted handoff. Eventual delivery requires only that every update keeps spreading until all correct replicas have it.
2. *Ordering and conflict resolution.* Two replicas may accept concurrent writes to the same item. Options: [last writer wins](/last-writer-wins/) by timestamp, which loses one of the writes; keep all concurrent versions as siblings for the application to merge, detected with version vectors; or use a [CRDT](/crdt/), whose merge combines them by a fixed rule.
3. *Rollback or not.* Bayou applied writes *tentatively* in timestamp order, and later rolled them back and redid them in a commit order chosen by a primary server. Such a system is eventually consistent, but a replica's state can change even when no new update reaches it. CRDTs avoid rollback, which is what strong eventual consistency demands.

**Inconsistency window.** The time from a write until every replica reflects it. It depends on network delay, load and the number of replicas, and in practice it is often below a second. Bailis et al. model it as *probabilistically bounded staleness*: given the delays of a store with $N$ replicas and read and write quorums $R$ and $W$, compute the chance that a read returns the last write after time $t$.

**Where it sits.** Eventual consistency is below every model in the [consistency hierarchy](/consistency-models/) that constrains order. Adding [session guarantees](/session-guarantees/) gives a sensible view to each client, adding [causal consistency](/causal-consistency/) orders updates that depend on each other, and both still allow availability under partitions. Linearizability and sequential consistency do not; see the [CAP theorem](/cap-theorem/) and [PACELC](/pacelc/).

## Examples

- **A key-value store with last-writer-wins.** Two clients write `x = 1` and `x = 2` at different replicas at the same time. Each replica reads its own value at first. Anti-entropy brings both writes to both replicas, and both keep the write with the larger timestamp. Both now return the same value; the other write is lost.
- **A shopping cart with siblings.** In Dynamo, concurrent writes to a cart produce two versions with incomparable vector clocks. A later read returns both, the application merges them by union, and writes the result back. A deleted item can come back, because union does not know about the deletion.
- **A counter.** A replicated counter whose increments are sent by gossip converges if each increment is counted once at each replica, for example as a [g-counter](/g-counter/). Without such a design, retries and duplicates make replicas count different totals.
- **A stale read.** A user posts a comment through replica A and reloads through replica B, which has not yet received it. The comment is missing. This is allowed by eventual consistency and forbidden by [read your writes](/read-your-writes/).
- **Never quiescent.** In a store with a steady stream of writes to one key, the quiescent definition promises nothing; the definitions of Shapiro et al. and Burckhardt et al. still require each write to reach every replica.

## Where it is used

- **Dynamo-style key-value stores.** Amazon's Dynamo, and the stores it inspired such as Cassandra and Riak, replicate each key on $N$ nodes with tunable read and write quorums, and use hinted handoff, read repair and Merkle-tree anti-entropy for propagation. See [Dynamo-style replication](/dynamo-style-replication/).
- **DNS.** Changes to a zone spread to secondary servers and caches over time, bounded by time-to-live values.
- **Mobile and offline-first applications.** Devices work offline and sync later, from Bayou and Coda to current apps built on CRDT libraries.
- **Caches and read replicas.** Asynchronous replicas of a primary database, and caches in front of it, are eventually consistent views of the primary.
- **Collaborative editing.** Text editors built on CRDTs or operational transformation let each user type at once and converge later.

## References
