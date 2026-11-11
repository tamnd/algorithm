---
tag: JV96EK
kind: concept
slug: read-your-writes
name: Read your writes
aliases:
- read-your-own-writes
area: distributed/replication-and-crdts
level: intro
summary: A session guarantee. Each read in a session sees every write that the same session made before it, at whatever replica the read is served.
prereqs: [session-guarantees]
see_also: [monotonic-reads, session-guarantees, eventual-consistency, causal-consistency, linearizability, quorum-replication, version-vectors]
sources:
  - paper: doi:10.1109/PDIS.1994.331722
    title: Douglas B. Terry, Alan J. Demers, Karin Petersen, Mike J. Spreitzer, Marvin M. Theimer and Brent B. Welch, Session guarantees for weakly consistent replicated data, PDIS 1994
    locator: pages 140 to 149 (the definition of Read Your Writes and its check against the write set of the session)
  - paper: doi:10.1145/1435417.1435432
    title: Werner Vogels, Eventually consistent, Communications of the ACM 52(1), 2009
    locator: pages 40 to 44 (read-your-writes consistency and session consistency as variations of eventual consistency)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, Problems with replication lag, Reading your own writes (techniques, and the cross-device case)
---

Read your writes is the [session guarantee](/session-guarantees/) that a read sees every earlier write of the same session. If a client writes $W$ and later reads, the replica that serves the read must already hold $W$. The guarantee is about one client's own writes only: other clients may still read old data, and the same client may still see other clients' writes come and go, which is what [monotonic reads](/monotonic-reads/) forbids.

## In plain words

You change your profile picture and reload the page. The page comes from a different copy of the database, one that has not yet heard about the change, and shows the old picture. To you it looks as if the change was lost.

Read your writes forbids this for your own changes. Your program remembers which changes it has made. A copy that has not seen all of them must not answer your reads: it must wait, or your program must ask another copy. Other people may see the old picture for a short time, and that is allowed.

## The idea

**Model.** A store has $n$ replicas that accept writes locally and exchange them in the background by [anti-entropy](/anti-entropy/) or log shipping. The system is asynchronous, and messages may be lost or delayed, so at any time different replicas hold different sets of writes. A *session* is the sequence of operations of one client, and the client may send each operation to a different replica. $DB(S, t)$ is the set of writes held by replica $S$ at time $t$.

**Definition (Terry et al. 1994).** If a read $R$ follows a write $W$ in a session, and $R$ is served by replica $S$ at time $t$, then $W \in DB(S, t)$.

This is a safety property: it limits which replicas may answer, and it does not make any read return. A client that can reach only replicas without its last write has to wait, so the guarantee costs availability during partitions.

**How it differs from its neighbors.**

- *Monotonic reads* says that a read sees every write that an earlier read of the session saw. Read your writes says it for the session's own writes. Neither implies the other: a client that never writes has read your writes for free and can still see a value disappear, and a client that never reads anything new has monotonic reads for free and can still miss its own write.
- *[Linearizability](/linearizability/)* gives every client every write that finished before its read began. Read your writes gives one client its own writes only. A store with read your writes can show a write to its author and hide it from everyone else for a long time.
- *Read-after-write consistency*, as some cloud stores use the term, means that after a write returns, *any* client that reads sees it. That is a property of the store for all clients, much stronger than the session guarantee.
- *[Causal consistency](/causal-consistency/)* implies read your writes, because program order is part of the causal order.

**Enforcement.**

- *Write vector.* The session keeps a [version vector](/version-vectors/) $WV$ of its writes. A replica $S$ with version vector $V_S$ may serve a read only if $V_S \ge WV$ pointwise. This needs replicas to send writes in order, so that the vector describes the set exactly.
- *Read from the writer.* Send the session's reads to the replica that took its writes (a sticky session), or to the leader in leader-follower replication, at least for a short time after a write.
- *Log position.* In leader-follower replication, the client keeps the log position of its last write, and a follower serves the read only after it has applied the log up to that position.
- *Quorums.* With $N$ replicas, writes acknowledged by $W$ of them and reads that ask $R$ of them, $R + W > N$ makes every read quorum meet the write quorum of each completed write, so a read sees the session's writes and those of everyone else. [Sloppy quorums](/sloppy-quorum/) give up this overlap.

## Examples

- **Lagging follower.** A client writes $x = 1$ at the leader, which replies at once and ships the log to the followers later. The next read goes to a follower that has not yet applied the write and returns $x = 0$. This breaks read your writes. With the log position check, the follower waits until it has applied the write, or the client reads from the leader.
- **The scenario in the tests.** A session writes $x = 1$ at replica $S_0$ and reads at $S_1$. $S_1$ has version vector $(0, 0)$ and the session has $WV = (1, 0)$, so the check refuses $S_1$. Without the check the read misses the write.
- **Read your writes holds, monotonic reads fails.** Another client writes $x = 1$ at $S_0$. Our session reads $x = 1$ at $S_0$ and then reads at $S_1$, which has nothing. The session made no writes, so read your writes holds, but it has seen $x = 1$ disappear.
- **Across devices.** A user writes from a phone and reads from a laptop. The two devices are different sessions, so the guarantee says nothing unless they share the session state, for example through the user's account on a central service.

## Where it is used

- Web applications that let a user edit their own data, such as a profile or a comment, while reads go to replicas.
- [Dynamo-style](/dynamo-style-replication/) stores, where the client can choose $R$ and $W$ so that $R + W > N$, or route reads to the replica that took the write.
- Leader-follower databases, where "read from the leader after a write" is a common setting.
- Bayou, for which Terry and others defined the guarantee, and stores with causally consistent sessions, which give it together with the other three session guarantees.

## References
