---
tag: VDRRCB
kind: algorithm
slug: pbft
name: PBFT
aliases:
- Practical Byzantine Fault Tolerance
- Castro-Liskov
- Castro-Liskov algorithm
area: distributed/byzantine-agreement
level: advanced
summary: Byzantine state machine replication with 3f + 1 replicas under partial synchrony; three phases order requests, checkpoints bound the log, view changes replace a bad primary.
solves: [byzantine-state-machine-replication]
model: partial-synchrony
complexity:
  vars: {n: the number of replicas, f: the largest number of Byzantine replicas, d: the largest message delay after GST, L: the size of the window between the watermarks}
  time: {best: 3d}
  messages: {best: 2n(n - 1), worst: O(n^2)}
  space: {extra: O(L n)}
properties: {deterministic: true, recursive: false}
prereqs: [state-machine-replication, byzantine-failure-model, partial-synchrony, quorum-certificate]
see_also: [view-change, byzantine-quorum-system, quorum-intersection, zyzzyva, hotstuff, tendermint, honeybadger-bft, byzantine-state-machine-replication]
sources:
  - paper: "Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance, 3rd USENIX Symposium on Operating Systems Design and Implementation (OSDI), 1999"
    locator: "Section 4 (normal case in 4.2, garbage collection and watermarks in 4.3, view changes in 4.4, safety and liveness in 4.5)"
  - paper: doi:10.1145/571637.571640
    title: Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance and proactive recovery, ACM Transactions on Computer Systems 20(4), 2002
    locator: the algorithm with signatures, the version with MACs only, proactive recovery, and the correctness arguments
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: the partially synchronous model with an unknown global stabilization time
  - paper: doi:10.1145/3293611.3331591
    title: Maofan Yin, Dahlia Malkhi, Michael K. Reiter, Guy Golan Gueta and Ittai Abraham, HotStuff, BFT consensus with linearity and responsiveness, ACM Symposium on Principles of Distributed Computing (PODC), 2019
    locator: the comparison table, with authenticator complexity O(n^2) for PBFT with a correct leader and O(n^3) for a view change
---

PBFT (Practical Byzantine Fault Tolerance) replicates a deterministic service on $n = 3f + 1$ replicas so that clients see one correct server although up to $f$ replicas are [Byzantine](/byzantine-failure-model/). One replica, the primary, gives each client request a sequence number, and the replicas agree on it in three phases: PRE-PREPARE, PREPARE and COMMIT. Checkpoints let the replicas drop old messages. When the primary seems faulty, the replicas run a [view change](/view-change/) that moves the role to the next replica and carries every request that may have committed into the new view. Safety holds in every run, and the service makes progress under [partial synchrony](/partial-synchrony/). Miguel Castro and Barbara Liskov published PBFT in 1999. It was the first Byzantine replication protocol fast enough for real services, and most later BFT protocols start from it.

## In plain words

Four computers run copies of the same program, and one of them may lie or crash. Clients send requests, and all honest copies must run the same requests in the same order.

One computer, the leader, puts a number on each request and tells the others. They do not trust the leader, so they tell each other what the leader said. When a computer has heard the same thing from three computers, it says "ready to commit". When it hears "ready to commit" from three computers, it runs the request and answers the client. The client waits for two equal answers, because one liar cannot give two.

If the leader is silent or cheats, the others time out and choose the next computer as leader. Each one tells the new leader which requests it was ready for, so no request that may have run gets a different number.

## The problem

There are $n = 3f + 1$ replicas $p_0, \ldots, p_{n-1}$ and any number of clients. At most $f$ replicas and any number of clients are Byzantine. Messages are signed, and signatures cannot be forged. The network can delay, reorder and drop messages, but a message sent again and again between honest parties arrives in the end. The model is [partially synchronous](/partial-synchrony/): after an unknown global stabilization time (GST) every message between honest replicas arrives within an unknown bound $\Delta$. The goal is [Byzantine state machine replication](/byzantine-state-machine-replication/): honest replicas execute the same requests in the same order (safety), and every request of a correct client is executed and answered (liveness). The [FLP result](/flp-impossibility/) rules out liveness in a fully asynchronous network, so PBFT needs synchrony only for liveness.

## The algorithm

A *view* $v$ has primary $p_{v \bmod n}$. Each replica keeps a message log, a low watermark $h$ (its last stable checkpoint) and the high watermark $h + L$. A *quorum* is $2f + 1$ replicas. The digest of a request stands for the request in all messages.

```pseudo id=main
PBFT(i)                                                            ▷ replica p_i, view v, primary p_(v mod n)
L1  primary, on request m: pick the next s in (h, h + L]; broadcast ⟨PRE-PREPARE, v, s, m⟩
L2  backup, on the first valid PRE-PREPARE for (v, s): log it; broadcast ⟨PREPARE, v, s, m, i⟩
L3  prepared(m, v, s) ⇔ the PRE-PREPARE and 2f matching PREPARE from different backups
L4  when prepared(m, v, s) and not in a view change: broadcast ⟨COMMIT, v, s, m, i⟩
L5  committed-local(m, v, s) ⇔ prepared(m, v, s) and 2f + 1 matching COMMIT
L6  execute committed requests in order of s; send the reply to the client
L7  every K requests: broadcast ⟨CHECKPOINT, s, digest, i⟩; on 2f + 1 matching: h ← s, drop the log up to s
L8  on timeout: stop taking part in v; broadcast ⟨VIEW-CHANGE, v + 1, h, C, P, i⟩         ▷ C: checkpoint proof, P: prepared certificates
L9  primary of v + 1, with 2f + 1 VIEW-CHANGE for v + 1: compute O; broadcast ⟨NEW-VIEW, v + 1, V, O⟩
L10 on a valid NEW-VIEW: recompute O from V; enter v + 1; handle the PRE-PREPARE messages of O as in L2
```

**The view change in detail.** At line L8 a replica includes, for each sequence number $s$ above its stable checkpoint, the prepared certificate of the highest view in which it was prepared at $s$. At line L9 the new primary takes a set $V$ of $2f + 1$ valid VIEW-CHANGE messages for $v + 1$. Let $min\text{-}s$ be the highest stable checkpoint in $V$ and $max\text{-}s$ the highest $s$ of a certificate in $V$. For each $s$ in $(min\text{-}s, max\text{-}s]$, $O$ holds a PRE-PREPARE for view $v + 1$: with the request of the certificate of the highest view for $s$ in $V$, or with a null request that does nothing if $V$ has no certificate for $s$. A backup checks $O$ at line L10 by doing the same computation, so a faulty new primary cannot choose $O$.

**The other rules.** A replica that waits for a NEW-VIEW for $v + 1$ and does not get one in time sends VIEW-CHANGE for $v + 2$ and doubles its timeout. A replica that gets VIEW-CHANGE messages for higher views from $f + 1$ other replicas joins the smallest of those views at once. Messages of a later view that come before its NEW-VIEW are kept, not dropped. A client sends its request to the primary, waits for $f + 1$ matching replies from different replicas, and sends the request to all replicas if the replies do not come in time.

## Example

Take $n = 4$, $f = 1$, primary $p_0$ in view 0, and a request $m$.

| step | messages | count |
|---|---|---|
| L1 | $p_0$ sends PRE-PREPARE $\langle 0, 1, m \rangle$ to $p_1, p_2, p_3$ | 3 |
| L2 | each of $p_1, p_2, p_3$ sends PREPARE to the 3 others | 9 |
| L3, L4 | each replica has the PRE-PREPARE and 2 PREPARE messages from backups, so it is prepared and sends COMMIT to the 3 others | 12 |
| L5, L6 | each replica has 3 COMMIT messages, executes $m$ at $s = 1$ and replies | 4 replies |

That is $3 + 9 + 12 = 24 = 2n(n - 1)$ messages between replicas and three message delays. The implementation counts the same: 4 requests and one checkpoint at $n = 4$ give $4 \cdot 24 + 12 = 108$ messages.

**A view change that keeps a request.** Now suppose $p_1$ and $p_2$ are prepared for $m$ at $s = 1$ and $p_2$ committed it, but then $p_0$ stops. The timers of $p_1, p_2, p_3$ expire and each one sends VIEW-CHANGE for view 1 to the 3 others (9 messages). $p_1$ and $p_2$ include their prepared certificates for $(m, 0, 1)$. The new primary $p_1$ gets 3 VIEW-CHANGE messages. Any 3 of them include one from $p_1$ or $p_2$, so $O$ holds PRE-PREPARE $\langle 1, 1, m \rangle$ and $m$ keeps the number 1. $p_1$ sends NEW-VIEW to the 3 others, 12 view-change messages in all; the tests check the count $(n - 1)^2 + (n - 1)$ for $n = 4, 7, 10$. If $p_0$ had been prepared alone, without any certificate, the new view could give $s = 1$ to a null request, which is safe, because no honest replica committed anything at $s = 1$.

## Correctness

The full proof is below; this is its outline.

- **Within a view.** Two prepared certificates for the same $(v, s)$ come from two quorums of $2f + 1$, which share $f + 1$ replicas and so an honest one. An honest replica endorses one request per $(v, s)$, so the requests are equal.
- **Committed implies prepared at $f + 1$ honest replicas.** A replica that is committed-local has $2f + 1$ COMMIT messages, and the $f + 1$ or more honest senders were prepared.
- **Across views.** The $2f + 1$ VIEW-CHANGE messages in a NEW-VIEW include one of those $f + 1$ honest replicas, which reports its certificate. By induction on the view, every certificate for $s$ in a later view is for the same request, and the highest-view rule puts that request into $O$.
- **Checkpoints** carry $2f + 1$ signatures on one state digest, so a copied state agrees with the committed requests.
- **Liveness.** After GST, faulty replicas cannot force view changes alone, $f + 1$ view changes pull in all honest replicas, the timeouts double until a view change finishes in time, and among $f + 1$ views in a row one primary is honest. In such a view the request commits in three message delays.

The proof also shows why a replica must stop sending COMMIT for view $v$ once it sent VIEW-CHANGE: otherwise it can report no certificate and then help to commit in the old view.

## Complexity

- **Normal case.** Each request costs $n - 1$ PRE-PREPARE, $(n - 1)^2$ PREPARE and $n(n - 1)$ COMMIT messages, $2n(n - 1) = O(n^2)$ in all, and three message delays from the primary to execution. Checkpoints add $n(n - 1)$ messages every $K$ requests. With batching the cost per request falls.
- **View change.** $O(n^2)$ messages: every replica sends VIEW-CHANGE to all, and the primary sends NEW-VIEW to all. But the messages are large. A VIEW-CHANGE carries up to $L$ prepared certificates of $2f + 1$ signatures each, and a NEW-VIEW carries $2f + 1$ VIEW-CHANGE messages. So a NEW-VIEW has $O(L n^2)$ signatures, and sending it to $n$ replicas costs $O(L n^3)$ signatures; for a constant window this is the $O(n^3)$ that the HotStuff paper gives for a PBFT view change.
- **Space.** The log holds at most $L$ sequence numbers with $O(n)$ messages each, so $O(L n)$ per replica, plus the checkpoint proofs and the state.
- **Rounds.** With a correct primary after GST, three message delays. Each failed view costs a timeout, and $f$ faulty primaries in a row cost $f$ view changes.

## Properties

- **Deterministic.** No coins. It does not contradict the FLP result, because it needs partial synchrony for liveness.
- **Optimal resilience.** $n = 3f + 1$ is the least possible for Byzantine agreement under partial synchrony.
- **Safe under asynchrony.** No timing assumption is used for safety.
- **Responsive with a correct primary.** In the normal case the speed depends on the real message delays, not on the timeout.
- **Quadratic.** All-to-all PREPARE and COMMIT messages; [HotStuff](/hotstuff/) makes each phase linear with a leader that collects votes.

## Variants and improvements

- **MACs instead of signatures.** The TOCS paper uses vectors of MACs (authenticators) in the normal case, which are much cheaper than signatures, and gives a view change that works without signatures. It also adds proactive recovery, which restarts replicas from a clean state so that $f$ can bound the faults in a window of time.
- **Optimizations in the papers.** Only one replica sends the full reply and the others send digests; tentative execution replies after the prepare phase and saves one message delay; read-only requests skip ordering; batching puts many requests under one sequence number.
- **Speculation.** [Zyzzyva](/zyzzyva/) executes before agreement and lets the client find out whether the order is final, with one phase when all $3f + 1$ replicas reply.
- **Linear and rotating leaders.** [HotStuff](/hotstuff/) uses [quorum certificates](/quorum-certificate/) built from threshold signatures, a third phase and a leader that collects votes, so that each view, including a view change, costs $O(n)$ messages. [Tendermint](/tendermint/) uses the same two voting steps as PBFT with gossip and a rotating proposer.
- **Asynchronous.** [HoneyBadgerBFT](/honeybadger-bft/) needs no timing assumption at all, at the cost of randomization.
- **Robust variants.** Aardvark (Clement, Wong, Alvisi, Dahlin and Marchetti, 2009) changes the protocol so that faulty clients and a slow faulty primary cannot cut the throughput by much.

## When to use it

Use PBFT for a permissioned group of a few to a few dozen replicas that must tolerate arbitrary faults, where the replicas know each other and links are mostly fast. It is the standard design to start from, and its normal case has the lowest latency of the classic protocols with $3f + 1$ replicas, three message delays. For large groups the $O(n^2)$ messages per request and the large view-change messages favour [HotStuff](/hotstuff/). If the network can be adversarial for long times, use an asynchronous protocol such as [HoneyBadgerBFT](/honeybadger-bft/).

## Pitfalls

- **Voting in the old view after a view change starts.** A replica that sends COMMIT for view $v$ after its VIEW-CHANGE breaks the safety proof. A first version of the implementation of this page did so, and its tests found two different requests at one sequence number.
- **Dropping messages of the next view.** PRE-PREPARE and PREPARE messages of view $v + 1$ can arrive before NEW-VIEW. If a replica drops them, the new view can stall.
- **Counting your own old VIEW-CHANGE.** The join rule needs $f + 1$ VIEW-CHANGE messages from other replicas for views above the one the replica is in or moving to. A stale message of the replica itself must not block it; this also stalled a first version of the implementation.
- **Trusting $O$ from the new primary.** Backups must recompute $O$ from $V$. Otherwise a faulty primary can give a committed sequence number to another request.
- **Fixed timeouts.** Without growth (doubling), the replicas can keep changing views before a NEW-VIEW arrives, and no view lasts long enough to commit.
- **Clients that accept one reply.** One reply can come from a faulty replica. A client needs $f + 1$ matching replies.
- **Watermarks.** Without the high watermark, a faulty primary can use up the sequence numbers with very large values.
- **Non-determinism.** The service must be deterministic, or the primary must propose the non-deterministic inputs, such as time stamps, with the request.

## Implementations

## History

Byzantine agreement goes back to Pease, Shostak and Lamport (1980), and Byzantine replication was studied in the 1980s and 1990s, but the systems were slow or assumed synchrony for safety. Castro and Liskov presented PBFT at OSDI 1999 with BFS, a replicated NFS file service that was only a few percent slower than an unreplicated one. The protocol used MACs in the normal case and signatures in the view change. Castro's thesis (MIT, 2001) and the TOCS paper of 2002 removed the signatures and added proactive recovery. Later work, such as Zyzzyva (2007), Aardvark (2009), BFT-SMaRt, Tendermint and HotStuff, kept the quorums of $2f + 1$ out of $3f + 1$ and changed the number of phases, the leader rule or the message pattern.

## References
