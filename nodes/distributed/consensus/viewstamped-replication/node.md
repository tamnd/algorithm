---
tag: FP530T
kind: algorithm
slug: viewstamped-replication
name: Viewstamped Replication
aliases:
- VR
area: distributed/consensus
level: advanced
summary: Primary-backup replication with views and view changes that tolerates crash failures.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of replicas}
  time: {best: Θ(1)}
  messages: {best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1988
  people: [Brian M. Oki, Barbara Liskov, James Cowling]
  note: Oki and Liskov presented it at PODC 1988; Liskov and Cowling published a revised, simpler protocol in 2012.
prereqs: [replicated-state-machine, quorum, crash-failure]
see_also: [view-change, multi-paxos, raft, zab, primary-backup-replication, state-machine-replication, cluster-reconfiguration, paxos]
sources:
  - paper: doi:10.1145/62546.62549
    title: Brian M. Oki and Barbara H. Liskov, Viewstamped replication, a new primary copy method to support highly-available distributed systems, PODC 1988, 8-17
    locator: viewstamps, the primary and the backups of a view, and the view change algorithm
  - url: https://pmg.csail.mit.edu/papers/vr-revisited.pdf
    title: Barbara Liskov and James Cowling, Viewstamped Replication Revisited, MIT technical report MIT-CSAIL-TR-2012-021, 2012
    locator: Section 4 (normal operation, the view change protocol with StartViewChange, DoViewChange and StartView, and recovery with a nonce), Section 5 (pragmatics such as state transfer), Section 7 (reconfiguration) and Section 8 (correctness)
  - paper: "Robbert van Renesse, Nicolas Schiper and Fred B. Schneider, Vive la différence: Paxos vs. Viewstamped Replication vs. Zab, IEEE Transactions on Dependable and Secure Computing 12(4), 472-484, 2015"
    locator: the common model and the comparison of how each protocol chooses the state of a new leader
  - paper: "Ellis Michael, Dan R. K. Ports, Naveen Kr. Sharma and Adriana Szekeres, Recovering shared objects without stable storage, DISC 2017"
    locator: the analysis of recovery protocols for replicas that lose their state
  - paper: "Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm, USENIX ATC 2014, 305-319"
    locator: the related work section, which compares Raft with Viewstamped Replication
---

Viewstamped Replication (VR) is a protocol for a [replicated state machine](/replicated-state-machine/) built on [primary-backup replication](/primary-backup-replication/). $n = 2f + 1$ replicas pass through a sequence of *views*. In each view one replica, chosen by round robin, is the *primary*: it orders client requests and sends them to the *backups*, and a request is committed once $f$ backups have it. When the primary fails, the replicas run a [view change](/view-change/) that moves to the next view and starts it with a log that contains every committed request. A replica that crashes and loses its state rejoins through a *recovery* protocol. The model is [asynchronous](/asynchronous-model/) with [crash failures](/crash-failure/). VR was published in 1988, at about the time Lamport wrote [Paxos](/paxos/), and solves the same problem.

## In plain words

One server, the primary, takes all requests, numbers them and sends them to the others. When a majority of the servers, the primary included, have a request, it is safe, and the primary runs it and answers the client.

If the primary goes silent, the others start a new "view" with the next server in line as the primary. Before the new primary starts, it collects the logs of a majority and keeps the most recent one. Every request that was safe was in a majority, so at least one log in the collection has it.

A server that crashed and forgot everything must not vote until it has caught up, so it first asks the others for the current state.

## The problem

**Model.** $n = 2f + 1$ replicas, of which at most $f$ are crashed or recovering at one time, with asynchronous messages that can be delayed, duplicated and reordered. In the 2012 version, replicas keep no state on disk; a crashed replica loses everything.

**Goal.** As in [total order broadcast](/total-order-broadcast/): all replicas run the same sequence of requests, a request that a client was told was done is never lost, and when enough replicas work and a primary is stable, every request is eventually run.

**State.** Each replica has a view number $v$, a status (normal, view-change or recovering), a log, an op-number $n$ (the length of the log), a commit-number $k$, and the last view in which its status was normal, $v'$.

## The algorithm

```pseudo id=main
NORMAL OPERATION, in view v, primary p = v mod n
L1  p, on a client request:  append it to the log; n ← n + 1; send Prepare(v, op, n, k) to the backups
L2  backup, on Prepare in view v, once it has all earlier ops:  append op; reply PrepareOK(v, n)
L3  p, on PrepareOK from f backups for n:  k ← n; run the ops up to k in order; reply to the clients; send Commit(v, k)
L4  backup, on Commit(v, k) or a Prepare with k:  run the ops up to k in order

VIEW CHANGE
L5  on a timeout, or on a message for a higher view:  v ← the new view; status ← view-change; send StartViewChange(v) to all
L6  on StartViewChange(v) from f others:  send DoViewChange(v, log, v', n, k) to the new primary v mod n
L7  new primary, on DoViewChange(v) from f + 1 replicas, itself included:  log ← the log with the largest v', ties by the largest n; k ← the largest k
L8  status ← normal; v' ← v; send StartView(v, log, k) to all; run the ops up to k
L9  backup, on StartView(v, log, k):  take the log; status ← normal; v' ← v; send PrepareOK for the uncommitted ops; run the ops up to k

RECOVERY of a replica that lost its state
L10 status ← recovering; send Recovery(i, nonce) to all
L11 replica with status normal, on Recovery:  reply RecoveryResponse(v, nonce, and if it is the primary: log, n, k)
L12 on f + 1 responses with the nonce, one from the primary of the largest view among them:  take that state; status ← normal
```

**Normal operation** (lines L1 to L4). This is two-phase commit without the abort: the primary waits for $f$ PrepareOK messages, so the request is in $f + 1$ logs. A backup processes Prepare messages in order, so PrepareOK for $n$ also covers every earlier op. The commit-number travels with the next Prepare, or in a Commit message when the primary is idle.

**View change** (lines L5 to L9). The StartViewChange step makes sure that $f + 1$ replicas have left the old view before the new primary acts. A replica in view-change status sends no PrepareOK, so after this point no more requests commit in the old view. The new primary takes the log with the largest $v'$: that replica was normal in the latest view, so its log holds every op committed in that view. Ties are broken by the longest log, because in one view the logs are prefixes of the primary's log.

**Recovery** (lines L10 to L12). A replica that lost its state may have sent PrepareOK for an op that only its vote made committed. If it voted again with an empty log, that op could be lost. So it takes no part in anything until it has the state of the current primary. The nonce makes sure that the responses are fresh.

## Example

$f = 1$, replicas $R_0, R_1, R_2$. View 0 has primary $R_0$; view 1 has primary $R_1$.

| step | event | logs |
|---|---|---|
| 1 | $R_0$ gets $a$, sends Prepare(0, $a$, 1, 0) | $R_0$: [a] |
| 2 | $R_1$ gets it, replies PrepareOK(0, 1); the Prepare to $R_2$ is slow | $R_1$: [a] |
| 3 | $R_0$ has $f = 1$ PrepareOK: commits $a$ ($k = 1$), answers the client | |
| 4 | $R_0$ crashes before it sends Commit | |
| 5 | $R_2$ times out: view 1, sends StartViewChange(1); $R_1$ joins | |
| 6 | DoViewChange to $R_1$: $R_1$ sends ([a], $v' = 0$, $k = 0$), $R_2$ sends ([], $v' = 0$, $k = 0$) | |
| 7 | $R_1$ picks the longer log of the same $v'$: [a]; sends StartView(1, [a], 0) | $R_2$: [a] |
| 8 | $R_2$ sends PrepareOK(1, 1); $R_1$ commits $a$ again in view 1 and runs it | |
| 9 | the slow Prepare(0, a) reaches $R_2$, which ignores it: its view is 1 | |
| 10 | $R_0$ restarts, sends Recovery; $R_1$ (primary) and $R_2$ answer; $R_0$ takes [a], $k = 1$ | $R_0$: [a] |

The client was told that $a$ was done in step 3, and $a$ survived the crash of the replica that committed it, because the log of $R_1$ was in the DoViewChange quorum.

## Correctness

- **Committed ops are in $f + 1$ logs.** An op commits in view $v$ only after $f$ backups in view $v$ with normal status have it (line L3), so $f + 1$ replicas hold it.
- **A view change keeps them.** The new primary hears from $f + 1$ replicas (line L7). Two sets of $f + 1$ out of $2f + 1$ meet, so some DoViewChange comes from a replica that has the op, or from one that was normal in a later view whose primary already had it. The log with the largest $v'$ then has it at the same position.
- **No commit after leaving a view.** A replica sends DoViewChange only after it stops sending PrepareOK in the old view, and the new primary waits for $f + 1$ of them, so a later commit in the old view would need a replica that left it.
- **Recovery keeps the quorum honest.** A recovering replica neither sends PrepareOK nor DoViewChange until it has a state at least as new as the latest view it sees.

The full proof below covers normal operation and the view change. For recovery without stable storage, Liskov and Cowling give an informal argument, and Michael, Ports, Sharma and Szekeres (2017) show how subtle such recovery is; the tests check it only by simulation. VR needs a majority of live replicas and a primary that is not replaced too often to make progress, as any consensus protocol must under [FLP](/flp-impossibility/).

## Complexity

- **Normal case.** One round trip from the primary to $f$ backups: four message delays from the client's request to the reply, and $2(n - 1)$ messages per request plus the reply. Batching amortizes this over many requests.
- **View change.** Three message delays (StartViewChange, DoViewChange, StartView), with $O(n^2)$ StartViewChange messages. The DoViewChange and StartView messages carry logs; the paper shortens them in practice by sending only the end of the log.
- **Recovery.** One round trip, plus the transfer of the state.
- **Storage.** No disk writes on the critical path in the 2012 version, which instead needs that at most $f$ replicas fail at one time, including those that recover.

## Properties

- **One primary per view, by round robin.** No election is needed: view $v$ has primary $v \bmod n$. A view with a crashed primary is skipped by another view change.
- **The new primary gets the log.** Any replica can become primary, and it takes the best log from the others, unlike [Raft](/raft/), which allows only an up-to-date candidate to win.
- **No stable storage needed.** The recovery protocol replaces the disk, at the price of the rule on concurrent failures.
- **Relation to Paxos.** A view is a [ballot number](/ballot-number/), the primary is the leader of [Multi-Paxos](/multi-paxos/), and the view change is phase 1 for all slots at once. The difference is in how the new leader chooses its state: Paxos looks at each slot's accepted value and ballot, VR takes the whole log of the replica with the latest normal view.

## Variants and improvements

- **The 1988 protocol.** The original VR was part of a transaction system and wrote viewstamps, pairs of a view and a timestamp, to identify events. The 2012 version removes the link to transactions and simplifies the view change.
- **Reconfiguration.** Liskov and Cowling add epochs and a reconfiguration protocol that changes the replica set; see [cluster reconfiguration](/cluster-reconfiguration/).
- **Optimizations.** Witnesses, batching, fast reads at the primary with [leases](/leader-lease/), and state transfer from a checkpoint instead of the whole log.
- **[Zab](/zab/) and [Raft](/raft/).** Later protocols of the same shape: a single primary in a numbered epoch or term, and a log copied from a quorum at the start of each term.

## When to use it

Use VR when you want a leader-based replicated log with a simple, deterministic primary order and no disk writes on the critical path, for example in-memory services with fast networks. If replicas can fail and restart all at once, for example in a power cut, use a protocol with stable storage instead, such as [Raft](/raft/) or [Multi-Paxos](/multi-paxos/), because the recovery protocol needs $f + 1$ live replicas with state.

## Pitfalls

- **Picking the wrong log.** Line L7 must use the largest $v'$ first. The tests show that a new primary that takes the first DoViewChange it receives can lose committed requests.
- **Rejoining without recovery.** Line L10 must run before a restarted replica votes. The tests show that a replica that rejoins with an empty log can be part of a quorum that does not hold a committed request, which is then lost.
- **Acknowledging out of order.** Line L2 must hold back a Prepare until all earlier ops have arrived; otherwise PrepareOK for $n$ does not cover the gap.
- **Running uncommitted ops.** Lines L3, L4 and L9 run ops only up to $k$. An op past $k$ can be replaced in a view change.
- **Accepting messages of an old view.** A replica must drop a Prepare of a lower view, as in step 9 of the example, or an old primary can overwrite the new log.

## Implementations

## History

Oki and Liskov presented Viewstamped Replication at PODC 1988, as part of a system for distributed transactions. It appeared at about the same time as Lamport's Paxos, which was written in 1989 and published in 1998, and the two solve the same problem with similar ideas. Liskov and Cowling published "Viewstamped Replication Revisited" in 2012, a simpler protocol for state machine replication with no dependence on transactions and no need for disks. Van Renesse, Schiper and Schneider compared VR, Paxos and Zab in one framework in 2015.

## References
