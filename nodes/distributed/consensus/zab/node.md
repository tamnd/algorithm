---
tag: M3MBBQ
kind: algorithm
slug: zab
name: ZooKeeper Atomic Broadcast (Zab)
aliases:
- Zab
area: distributed/consensus
level: advanced
summary: The broadcast protocol of ZooKeeper. A primary sends state changes in order over FIFO channels, and a new primary first syncs the latest history, so no primary's changes are reordered.
solves: [total-order-broadcast]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, L: the length of the history}
  time: {best: Θ(1)}
  messages: {best: Θ(n)}
  space: {extra: Θ(L)}
properties: {deterministic: true, recursive: false}
history:
  year: 2011
  people: [Flavio P. Junqueira, Benjamin C. Reed, Marco Serafini]
  note: Zab was built for Apache ZooKeeper at Yahoo, described by Reed and Junqueira in 2008, and specified with its properties and proofs by Junqueira, Reed and Serafini at DSN 2011.
prereqs: [total-order-broadcast, primary-backup-replication, quorum, crash-failure]
see_also: [paxos, multi-paxos, raft, viewstamped-replication, replicated-state-machine, total-order-broadcast, log-compaction, split-brain]
sources:
  - paper: doi:10.1109/DSN.2011.5958223
    title: Flavio P. Junqueira, Benjamin C. Reed and Marco Serafini, Zab, high-performance broadcast for primary-backup systems, Proceedings of the 41st IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2011, pages 245 to 256
    locator: the properties (integrity, total order, agreement, local and global primary order, primary integrity), Figure 1 (the Paxos run that breaks primary order), the three phases with CEPOCH, NEWEPOCH, ACK-E, NEWLEADER, ACK-LD and COMMIT-LD, and zxids as epoch and counter
  - paper: "Benjamin Reed and Flavio P. Junqueira, A simple totally ordered broadcast protocol, Proceedings of the 2nd Workshop on Large-Scale Distributed Systems and Middleware (LADIS), 2008"
    locator: the first description of the protocol and of why ZooKeeper needs primary order
  - url: https://www.usenix.org/legacy/event/atc10/tech/full_papers/Hunt.pdf
    title: Patrick Hunt, Mahadev Konar, Flavio P. Junqueira and Benjamin Reed, ZooKeeper, wait-free coordination for Internet-scale systems, USENIX Annual Technical Conference, 2010
    locator: the use of Zab in ZooKeeper, with idempotent transactions made by the leader
---

Zab is the atomic broadcast protocol of Apache ZooKeeper. One process, the primary, turns client requests into state changes, gives each one a zxid made of an epoch number and a counter, and sends them to the other processes over FIFO channels; a change is committed once a [quorum](/quorum/) has logged it. When the primary fails, a new one runs a discovery phase that picks the most recent history among a quorum, and a synchronization phase that installs it, before it sends anything new. This gives [total-order broadcast](/total-order-broadcast/) plus primary order: the changes of one primary are delivered in the order it sent them, and never mixed with the changes of a later primary out of order, which Multi-Paxos does not guarantee (Junqueira, Reed and Serafini, 2011).

## In plain words

A team keeps a shared notebook. One person, the leader, writes the new lines. Each line says "change the balance from 100 to 150", so a line makes sense only after the line before it.

The leader sends each line to everyone in order. When more than half have written it down, the leader tells them all to make it official.

When the leader disappears, someone new takes over. Before writing anything, the new leader asks a majority for their notebooks, takes the most up-to-date one, and makes everyone copy it. Lines that only a few people had, and that were never made official, may be dropped. Only then does the new leader start writing new lines, with a new number for its turn as leader.

## The problem

A set of $n$ processes, up to a minority of which can crash and recover, must deliver state changes in one order, as in [total-order broadcast](/total-order-broadcast/). The system is [primary-backup](/primary-backup-replication/): the primary runs each client request against its current state and broadcasts the resulting change, which is idempotent but depends on the changes before it. So beyond integrity, total order and agreement, Zab must give three primary order properties:

- **Local primary order.** If a primary broadcasts $a$ before $b$, a process that delivers $b$ has delivered $a$ before $b$.
- **Global primary order.** If $a$ is broadcast by the primary of epoch $e$ and $b$ by the primary of a later epoch $e' > e$, a process that delivers both delivers $a$ first.
- **Primary integrity.** If the primary of epoch $e$ broadcasts $b$, and some process delivers $a$ broadcast in an earlier epoch, then that primary delivered $a$ before it broadcast $b$.

The model is asynchronous with crash and recovery. Channels between processes are FIFO and reliable while a connection lasts, as TCP gives; a lost message breaks the connection. Each process keeps on stable storage its accepted epoch $f.p$ (the last NEWEPOCH it acknowledged), its current epoch $f.a$ (the last NEWLEADER it accepted) and its history $h_f$, a sequence of transactions. For liveness, a leader election oracle eventually picks one live process that a quorum follows.

## The algorithm

A transaction is $\langle v, z \rangle$ with a zxid $z = (e, c)$: $e$ is the epoch of the primary that made it and $c$ counts its transactions in that epoch, from 1. Zxids are compared first by epoch, then by counter. In the phases below, Q is the quorum of followers that a prospective leader gathers in discovery; the leader is also a follower of itself.

```pseudo id=main
PHASE 1, DISCOVERY
L1  FOLLOWER f, on connecting to prospective leader ℓ: send CEPOCH(f.p) to ℓ
L2  LEADER ℓ, on CEPOCH from a quorum Q: e′ ← 1 + max of their f.p; send NEWEPOCH(e′) to Q
L3  FOLLOWER, on NEWEPOCH(e′): if e′ > f.p then f.p ← e′, send ACK-E(f.a, h_f); else go back to election
L4  LEADER, on ACK-E from all of Q: I ← the history h_f with the largest (f.a, last zxid of h_f)
PHASE 2, SYNCHRONIZATION
L5  LEADER: send NEWLEADER(e′, I) to Q
L6  FOLLOWER, on NEWLEADER(e′, I): if f.p = e′ then f.a ← e′, h_f ← I, send ACK-LD; else go back to election
L7  LEADER, on ACK-LD from a quorum: send COMMIT-LD to Q
L8  FOLLOWER, on COMMIT-LD: deliver the transactions of I, in order
PHASE 3, BROADCAST
L9  LEADER, to broadcast v: c ← c + 1; send PROPOSE(⟨v, (e′, c)⟩) to Q
L10 FOLLOWER, on PROPOSE(t): append t to h_f; send ACK
L11 LEADER, on ACK for (e′, c) from a quorum, once (e′, c − 1) is committed: send COMMIT((e′, c)) to Q
L12 FOLLOWER, on COMMIT(z): deliver every transaction of h_f up to z that it has not delivered
```

**Epochs (lines L1 to L3).** A follower acknowledges NEWEPOCH only for an epoch larger than any it has acknowledged, and records it on disk first. Two quorums share a follower, so two prospective leaders cannot both collect a quorum of ACK-E for the same epoch: each epoch has at most one primary, and every zxid is unique.

**Choosing the history (line L4).** The follower with the largest current epoch $f.a$ accepted the most recent NEWLEADER, so its history holds every history installed before; among followers with the same $f.a$, the one with the largest last zxid has the longest run of the latest primary's proposals. A committed transaction was logged by a quorum, which shares a follower with Q, so it is in the chosen history. This is the step that a broken version, which picks a random history, gets wrong in the tests.

**Synchronization (lines L5 to L8).** Each follower in Q replaces its history by I and sets $f.a$. The leader waits for a quorum, then commits all of I at once. Transactions of an old primary that were logged by only a few processes and are not in I are removed. The new primary sends no proposal before COMMIT-LD, and channels are FIFO, so every follower installs I before it sees the first new proposal.

**Broadcast (lines L9 to L12).** This is two-phase commit without aborts: propose, acknowledge, commit. Commits go out in zxid order, so a follower that delivers up to $z$ has the whole prefix. A follower that connects to an established leader late gets NEWEPOCH, NEWLEADER with the leader's current history and the committed prefix, and COMMIT-LD in one go, and then joins Q.

## Example

Three processes $P_0$, $P_1$, $P_2$. $P_0$ leads epoch 1 and is synchronized with both. The run is the one in the test that checks that an old primary's uncommitted suffix is dropped and that the order is kept.

| step | event | $h$ of $P_0$ | $h$ of $P_1$ | $h$ of $P_2$ | delivered |
|---|---|---|---|---|---|
| 1 | $P_0$ proposes A = (1,1) and B = (1,2) | A, B | | | none |
| 2 | $P_1$ logs A only; then $P_0$ crashes | A, B | A | | none |
| 3 | $P_2$ leads with $\{P_1, P_2\}$: CEPOCH, NEWEPOCH(2), ACK-E | A, B | A | | none |
| 4 | L4 picks the history of $P_1$ (same $f.a = 1$, larger last zxid): I = A | A, B | A | A | A at $P_1$, $P_2$ |
| 5 | $P_2$ proposes C = (2,1); quorum ack; commit | A, B | A, C | A, C | A, C at $P_1$, $P_2$ |
| 6 | $P_0$ recovers; $P_1$ leads epoch 3; L4 picks $f.a = 2$ over $f.a = 1$: I = A, C | A, C | A, C | A, C | A, C everywhere |

B was never committed, and it disappears. No process delivers B, and none delivers C before A. Paxos can do worse: in Figure 1 of the DSN paper, the old leader proposes A in slot 27 and B in slot 28 with ballot 1, a new leader proposes C in slot 27 with ballot 2, and the chosen sequence can be C, B, D. Then B is delivered without A, which it depends on, and after C, which a later primary made. The test encodes this sequence and the checker reports both broken primary order properties.

## Correctness

Each epoch has at most one primary, because followers acknowledge strictly increasing epochs and quorums intersect. Every history is a chain: the initial history of some epoch followed by a prefix of that epoch's proposals, so histories are sorted by zxid and hold each primary's proposals without gaps. The key lemma is that a transaction committed in epoch $e'$ is in the initial history of every later established epoch, by induction on the epoch, using the shared follower of the commit quorum and the discovery quorum, and the choice of the largest $(f.a, \text{zxid})$. A process delivers only committed transactions, and only a prefix of its history, so all delivered sequences are prefixes of one sequence; primary order follows from the shape of the histories. The full proof is below.

## Complexity

In the broadcast phase, each transaction costs one PROPOSE, one ACK and one COMMIT per follower, so $3(n-1)$ messages, $\Theta(n)$, and the leader learns it is committed after two message delays (propose and acknowledge); followers deliver after three. Many transactions can be in flight at once, which is where Zab gets its throughput. Recovery costs a constant number of message rounds, but ACK-E and NEWLEADER carry histories of length up to $L$; with snapshots (see [log compaction](/log-compaction/)) only the part after the last snapshot is sent. Each process stores its history, $\Theta(L)$.

## Properties

- Safe in the asynchronous model with crash and recovery failures and any number of crashes; live while a quorum is up and connected to one leader.
- Integrity, total order and agreement, as in [total-order broadcast](/total-order-broadcast/), plus local primary order, global primary order and primary integrity.
- Needs FIFO channels; a lost message must break the connection, not just vanish.
- Each epoch has one primary, and the zxid identifies both the primary and the position in its stream.
- A recovering primary transfers a whole history, not one value per log slot.

## Variants and improvements

- **ZooKeeper's implementation.** The leader election of ZooKeeper picks a process with the most recent history, so the leader can use its own history and the discovery phase only fixes the epoch. Followers that are behind receive the missing part, a truncation order, or a snapshot, depending on how far behind they are.
- **Observers.** Processes that receive commits but do not vote, which add read capacity without enlarging the quorum.
- **Comparison with Raft.** [Raft](/raft/) also has one leader per term, appends in order and elects only up-to-date candidates, so it also keeps primary order; its leader brings followers up to date one entry at a time instead of in a separate synchronization phase.
- **Comparison with Paxos.** [Multi-Paxos](/multi-paxos/) chooses a value for each slot on its own, so a new leader can fill a slot with its own value while a later slot keeps an old leader's value. That is fine when commands are independent, as in [state machine replication](/replicated-state-machine/), but not for primary-backup changes that depend on each other.

## When to use it

Use Zab when a primary computes state changes and sends them to backups, so each change depends on the ones before it, and when the system can rely on FIFO connections. It fits coordination services such as ZooKeeper, with small data and many reads. If commands are deterministic and independent, [Multi-Paxos](/multi-paxos/) or [Raft](/raft/) works too, and Raft is often simpler to build from scratch.

## Pitfalls

- **Choosing the history by length or at random.** It must be the largest $(f.a, \text{zxid})$. The longest history can belong to an old primary that was replaced; a random one can miss committed transactions. The broken version in the tests breaks agreement or primary order in 99 of 100 seeded runs.
- **Proposing before COMMIT-LD.** A new primary that proposes before the quorum has the initial history lets a follower deliver a new transaction before the old ones it depends on.
- **Not persisting $f.p$ before ACK-E.** A process that forgets its accepted epoch after a crash can acknowledge an epoch twice, and two primaries could share an epoch and its zxids.
- **Treating a dropped message as harmless.** A follower that misses one PROPOSE and accepts the next has a gap in its history. The connection must be dropped and the follower resynchronized.
- **Counting the leader's epoch from its own state only.** The new epoch must exceed every $f.p$ in the quorum, not only the leader's.

## Implementations

## History

Benjamin Reed and Flavio Junqueira designed Zab for ZooKeeper at Yahoo Research and described it in a 2008 workshop paper; ZooKeeper itself was described at USENIX ATC in 2010. They had found that Paxos as usually stated did not keep the order of a primary's dependent changes when the primary changed, and that many outstanding proposals were needed for throughput. In 2011, Junqueira, Reed and Serafini gave the properties of primary order, the three-phase protocol with epochs and zxids, and proofs, and compared the protocol with Paxos.

## References
