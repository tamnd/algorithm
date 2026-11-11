---
tag: AQ9S0K
kind: concept
slug: monotonic-reads
name: Monotonic reads
aliases:
- monotonic read consistency
area: distributed/replication-and-crdts
level: intro
summary: A session guarantee. Once a session has read data that depends on some writes, its later reads are served only by replicas that hold those writes.
prereqs: [session-guarantees]
see_also: [read-your-writes, session-guarantees, eventual-consistency, causal-consistency, consistency-models, version-vectors]
sources:
  - paper: doi:10.1109/PDIS.1994.331722
    title: Douglas B. Terry, Alan J. Demers, Karin Petersen, Mike J. Spreitzer, Marvin M. Theimer and Brent B. Welch, Session guarantees for weakly consistent replicated data, PDIS 1994
    locator: pages 140 to 149 (the definition of Monotonic Reads with RelevantWrites, and its check against the read set of the session)
  - paper: doi:10.1145/1435417.1435432
    title: Werner Vogels, Eventually consistent, Communications of the ACM 52(1), 2009
    locator: pages 40 to 44 (monotonic read consistency as a variation of eventual consistency)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, Problems with replication lag, Monotonic reads (the moving-backward-in-time example and replica choice by user id)
---

Monotonic reads is the [session guarantee](/session-guarantees/) that a session never sees the store go back in time. If a read has returned data that depends on a set of writes, every later read of the same session is served by a replica that holds those writes. The guarantee is about what the session has *read*, not about what it has written, which is the subject of [read your writes](/read-your-writes/).

## In plain words

You open a page and see a new comment. You reload, the request goes to a different copy of the database that is further behind, and the comment is gone. Reload again and it may come back.

Monotonic reads forbids this. Your program remembers how much it has already seen. Every later answer must come from a copy that has seen at least as much. The data you see may still be old, and other people may see older data, but your view never moves backwards.

## The idea

**Model.** A store has $n$ replicas that accept writes and exchange them in the background. The system is asynchronous and messages may be lost or delayed, so replicas hold different sets of writes at the same time. A session is the sequence of operations of one client, which may go to a different replica each time. $DB(S, t)$ is the set of writes held by replica $S$ at time $t$, and $\mathit{RelevantWrites}(S, t, R)$ is the smallest set of writes in $DB(S, t)$ that is enough to produce the result of the read $R$.

**Definition (Terry et al. 1994).** If a read $R_1$, served by $S_1$ at time $t_1$, precedes a read $R_2$ in a session, and $R_2$ is served by $S_2$ at time $t_2$, then $\mathit{RelevantWrites}(S_1, t_1, R_1) \subseteq DB(S_2, t_2)$.

The second read must hold the writes that the first read depended on, also when $R_2$ reads a different item. This is a safety property; during a partition a session may have to wait until some reachable replica has caught up.

**How it differs from its neighbors.**

- *[Read your writes](/read-your-writes/)* protects the session's own writes. Monotonic reads protects what the session has already seen, which may include other clients' writes. Neither implies the other: a session that has made a write but has not read it back can miss it under monotonic reads, and a session that never writes can see data vanish under read your writes.
- *Monotonic writes* is about the order in which other replicas receive the session's writes; it constrains every replica, not only the one that serves the session.
- *Consistent prefix reads* (Kleppmann's name) asks that a reader sees writes in an order that respects their causal order, for example a question before its answer. Monotonic reads does not order two writes that the session has not yet seen.
- *[Causal consistency](/causal-consistency/)* implies monotonic reads: a write that a read returned is in the causal past of every later operation of the session.
- *[Eventual consistency](/eventual-consistency/)* alone allows a session to see a value and then an older one, as long as all replicas agree in the end.

**Enforcement.**

- *Read vector.* The session keeps a [version vector](/version-vectors/) $RV$. After a read at replica $S$ it sets $RV \leftarrow \max(RV, V)$, where $V$ is the vector of the relevant writes, or the whole vector $V_S$ of the replica, which is simpler and safe. A replica may serve a later read only if $V_S \ge RV$. This needs replicas to send writes in order, so that a vector describes a set of writes exactly.
- *Sticky replica.* Send all reads of a user to the same replica, for example chosen by a hash of the user id. A single replica only moves forward, so its reads are monotonic, until it fails and the user moves to another replica.
- *Log position.* In leader-follower replication, keep the highest log position that the session has read, and read only from followers that have applied the log up to it.

## Examples

- **The vanishing comment.** Another client writes a comment $x = 1$ at replica $S_0$. Our session reads $x = 1$ at $S_0$. Its next read goes to $S_1$, which has not received the write, and returns no comment. With the read vector, $RV = (1, 0)$ after the first read and $V_{S_1} = (0, 0)$, so $S_1$ refuses and the client reads elsewhere. This is the scenario in the tests of the [session guarantees](/session-guarantees/).
- **Monotonic reads holds, read your writes fails.** A session writes $x = 1$ at $S_0$ and then reads at $S_1$, which lacks the write. The session has read nothing before, so monotonic reads holds, but the session misses its own write.
- **A counter.** A page view counter shows 120, then 118 on reload. The two values came from replicas at different points of the same history. Monotonic reads would only allow 120 or more on the second read.

## Where it is used

- Feeds, inboxes and comment threads served from read replicas, where data that disappears and reappears confuses users.
- Leader-follower databases and [Dynamo-style](/dynamo-style-replication/) stores, often with a sticky choice of replica per user.
- Bayou and stores with causally consistent sessions, which give monotonic reads together with the other three session guarantees.
- Clients of a [CRDT](/crdt/) store that move between replicas: the states of a [state-based CRDT](/state-based-crdt/) only grow, so a client that carries the last state it has seen and merges it into the replica it reads from never sees an older state.

## References
