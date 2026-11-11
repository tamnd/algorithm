---
tag: HVCFWA
kind: concept
slug: session-guarantees
name: Session guarantees
aliases:
- client-centric consistency
- Bayou session guarantees
area: distributed/replication-and-crdts
level: intro
summary: Four per-client rules over a weakly consistent store (read your writes, monotonic reads, writes follow reads, monotonic writes), enforced with version vectors.
prereqs: [eventual-consistency, version-vectors]
see_also: [read-your-writes, monotonic-reads, causal-consistency, consistency-models, anti-entropy, dynamo-style-replication, vector-clocks]
sources:
  - paper: doi:10.1109/PDIS.1994.331722
    title: Douglas B. Terry, Alan J. Demers, Karin Petersen, Mike J. Spreitzer, Marvin M. Theimer and Brent B. Welch, Session guarantees for weakly consistent replicated data, PDIS 1994
    locator: pages 140 to 149 (the four guarantees defined with DB(S, t), RelevantWrites and WriteOrder; the implementation with read sets, write sets and version vectors, and the table of checks)
  - paper: doi:10.1145/1435417.1435432
    title: Werner Vogels, Eventually consistent, Communications of the ACM 52(1), 2009
    locator: pages 40 to 44 (read-your-writes, session, monotonic read and monotonic write consistency as variations of eventual consistency)
  - paper: doi:10.1145/2926965
    title: Paolo Viotti and Marko Vukolić, Consistency in non-transactional distributed storage systems, ACM Computing Surveys 49(1), 2016
    locator: Article 19, the section on session guarantees (the formal definitions and their relation to PRAM and causal consistency)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, Problems with replication lag (reading your own writes, monotonic reads, consistent prefix reads)
---

Session guarantees are four rules that a weakly consistent replicated store can give to each client *session*, the sequence of reads and writes that one application makes. Terry, Demers, Petersen, Spreitzer, Theimer and Welch defined them in 1994 for the Bayou system: [read your writes](/read-your-writes/), [monotonic reads](/monotonic-reads/), writes follow reads, and monotonic writes. Each rule only constrains what one session sees, so the store stays [eventually consistent](/eventual-consistency/) and highly available, and a client can enforce the rules by itself with two [version vectors](/version-vectors/) and a check at the server it contacts.

## In plain words

A store keeps copies of the data on several servers, and the copies catch up with each other in the background. A user who talks to a different server for each request can see strange things: a change they just made is missing, a message they already read disappears, a reply shows up before the message it answers, or two edits arrive in the wrong order.

The session guarantees remove these effects for each user. The user's program remembers a short summary of what it has written and read. Before a server answers, it checks that it has seen at least that much. If it has not, the program asks another server or waits. Other users may still see old data, but each user's own view makes sense.

## The idea

**Model.** There are $n$ servers, each with a database $DB(S)$, the set of writes it holds, and any number of clients. A client can send each operation to any server. A server accepts reads and writes at once, without talking to other servers, and servers exchange writes in the background by [anti-entropy](/anti-entropy/), in any pairs and at any times. The system is asynchronous; messages may be lost, delayed, duplicated and reordered, and any server may be cut off for a while. Servers may crash and recover with their logs on durable storage. Two rules on servers are assumed, as in Bayou:

- *Write order.* A server orders a new write after every write it already holds; $\mathit{WriteOrder}(W_1, W_2)$ means that $W_1$ is ordered before $W_2$. Lamport timestamps give such an order.
- *Ordered propagation.* A server sends writes in such a way that a database holding a write $W$ also holds every write that the origin server of $W$ held when it accepted $W$. Sending the whole log, or the log in order, does this.

$DB(S, t)$ is the database of $S$ at time $t$. $\mathit{RelevantWrites}(S, t, R)$ is the smallest set of writes in $DB(S, t)$ that is enough to produce the result of the read $R$.

**The four guarantees.** For operations of one session:

- **Read your writes (RYW).** If a read $R$ follows a write $W$, and $R$ is done at server $S$ at time $t$, then $W \in DB(S, t)$.
- **Monotonic reads (MR).** If a read $R_1$ at $S_1$ at time $t_1$ precedes a read $R_2$ at $S_2$ at time $t_2$, then $\mathit{RelevantWrites}(S_1, t_1, R_1) \subseteq DB(S_2, t_2)$.
- **Writes follow reads (WFR).** If a read $R_1$ at $S_1$ at time $t_1$ precedes a write $W_2$, then at every server $S$ and time $t$ with $W_2 \in DB(S, t)$, each $W_1 \in \mathit{RelevantWrites}(S_1, t_1, R_1)$ is in $DB(S, t)$ and $\mathit{WriteOrder}(W_1, W_2)$.
- **Monotonic writes (MW).** If a write $W_1$ precedes a write $W_2$, then at every server $S$ and time $t$ with $W_2 \in DB(S, t)$, also $W_1 \in DB(S, t)$ and $\mathit{WriteOrder}(W_1, W_2)$.

RYW and MR are about what the session *reads*: they constrain the server that serves a read. WFR and MW are about what *other* clients see of the session's writes: they constrain every server, for ever after the write. This is why only the second pair needs the server rules above.

All four are safety properties. None of them makes an operation return; a server that does not meet a guarantee must refuse, and the client must try another server or wait for anti-entropy. This is the availability cost: a client that is cut off from every server holding its writes cannot read under RYW. The guarantees are independent: each one can fail while the other three hold.

**Enforcement with version vectors.** Each server keeps a version vector $V_S$, where $V_S[j]$ is the number of writes from server $j$ that $S$ holds. Under ordered propagation, $DB(S)$ holds exactly the first $V_S[j]$ writes of each server $j$, so $V_S \ge V$ pointwise implies that $S$ holds every write that $V$ summarizes. Each session keeps a *read vector* $RV$, the writes that its reads depended on, and a *write vector* $WV$, its own writes.

| guarantee | on a read at $S$ | on a write at $S$ |
| --- | --- | --- |
| RYW | require $V_S \ge WV$ | then set $WV[S] \leftarrow$ the number of the new write |
| MR | require $V_S \ge RV$; then $RV \leftarrow \max(RV, V)$ | |
| WFR | then $RV \leftarrow \max(RV, V)$ | require $V_S \ge RV$ |
| MW | | require $V_S \ge WV$; then set $WV[S]$ |

Here $V$ is the vector of the relevant writes of the read; using $V_S$ in its place is simpler and safe, at the price of refusing some servers that would do. The check for WFR and MW is made when the write is accepted. After that, write order puts the new write after everything the server holds, including the writes in $RV$ or $WV$, and ordered propagation carries those writes along with it to every other server. The state of a session is $2n$ integers, and it can move with the client from server to server.

**Relation to other models.** The guarantees are weaker than [causal consistency](/causal-consistency/): a causally consistent store gives all four to every session. In a model where each process is one session, Brzezinski, Sobaniec and Wawrzyniak showed that RYW, MR and MW together are equivalent to PRAM consistency, and that adding WFR gives causal consistency, as summarized by Viotti and Vukolić (2016). The guarantees say nothing about two different clients: two sessions may see concurrent writes in different orders, and a client that switches to a new session loses them.

## Examples

Each example is a run that breaks one guarantee when the client does not check vectors. With the checks on, the step marked "stale" is refused, and the client must use another server. All four runs are in the tests of the implementation.

- **RYW.** A user changes a password at server $S_0$ ($W$: password $= 1$) and then logs in through $S_1$, which has not yet received $W$. The login is checked against the old password. With RYW, $V_{S_1}[0] = 0 < WV[0] = 1$, so $S_1$ refuses.
- **MR.** Another user writes $x = 1$ at $S_0$. Our user reads $x = 1$ at $S_0$, then reads at $S_1$ and gets nothing: the message they already saw has vanished. With MR, $RV[0] = 1$ after the first read, and $S_1$ refuses.
- **WFR.** Our user reads a posting $x = 1$ at $S_0$ and replies with $y = 2$ at $S_1$, which does not hold $x = 1$. Anti-entropy carries the reply from $S_1$ to $S_2$, and readers at $S_2$ see the reply without the posting. A second failure is in the order: if $S_1$ has a smaller Lamport counter, the reply is ordered before the posting at every server, even after both arrive everywhere.
- **MW.** Our user writes version $x = 1$ of a file at $S_0$ and then version $x = 2$ at $S_1$. $S_2$ receives the second write from $S_1$ and not the first one. If the second write was an edit that assumes the first, $S_2$ applies it to the wrong base.
- **Independence.** In the MR run, a client that checks only RYW is not stopped, because it has made no writes. In the RYW run, a client that checks only MR is not stopped, because it has made no reads.

## Where it is used

- **Bayou.** The guarantees were designed for Bayou, a store for mobile clients that work while disconnected, with anti-entropy between servers and conflict handling by the application.
- **Dynamo-style stores.** In [Dynamo-style replication](/dynamo-style-replication/), read-your-writes and monotonic reads are often obtained by *sticky sessions* (a client always talks to the same replica) or by [quorums](/quorum-replication/) with $R + W > N$, in place of version vectors held by the client. Vogels (2009) lists read-your-writes, session, monotonic read and monotonic write consistency as the useful variants of eventual consistency.
- **Leader-follower replication.** A client that reads from followers can pass the log position of its last write and wait until the follower has applied it, which is the RYW check with a single counter in place of a vector.
- **Causally consistent sessions.** Some databases offer sessions that give all four guarantees together, by passing a logical timestamp from operation to operation of the session.

## References
