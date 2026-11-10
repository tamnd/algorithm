---
tag: 53MYYW
kind: algorithm
slug: vertical-paxos
name: Vertical Paxos
area: distributed/consensus
level: research
summary: Separates reconfiguration from the replication protocol using a master.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of acceptors in one configuration, c: the number of configurations a leader reads}
  time: {best: Θ(1)}
  messages: {best: Θ(n c)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 2009
  people: [Leslie Lamport, Dahlia Malkhi, Lidong Zhou]
  note: Presented at PODC 2009. The report version gives the two algorithms in PlusCal.
prereqs: [paxos, quorum, cluster-reconfiguration]
see_also: [primary-backup-replication, cheap-paxos, flexible-paxos, multi-paxos, leader-lease, view-change]
sources:
  - paper: doi:10.1145/1582716.1582783
    title: Leslie Lamport, Dahlia Malkhi and Lidong Zhou, Vertical Paxos and primary-backup replication, PODC 2009, 312-313
    locator: the configuration master, read and write quorums per ballot, and the two variants
  - url: https://lamport.azurewebsites.net/pubs/vertical-paxos.pdf
    title: Leslie Lamport, Dahlia Malkhi and Lidong Zhou, Vertical Paxos and primary-backup replication, Microsoft Research report, 9 February 2009, corrected 2009 and 2019
    locator: Section 3 (the primary-backup case), Section 4.1 (FindSafe, Figure 1, and complete ballots), Section 4.2 (Vertical Paxos I, Figures 2 and 3), Section 4.3 (Vertical Paxos II, Figures 4 and 5), Section 5 (Niobe and chain replication as instances)
  - paper: doi:10.1145/279227.279229
    title: Leslie Lamport, The part-time parliament, ACM Transactions on Computer Systems 16(2), 133-169, 1998
    locator: the ballots and the safety condition that Vertical Paxos keeps
---

Vertical Paxos is a family of [Paxos](/paxos/) algorithms in which the set of acceptors can change from one ballot to the next, inside a single consensus instance. An external, reliable *configuration master* picks the acceptors of each ballot and its read and write [quorums](/quorum/). A new leader reads the old state from read quorums of earlier configurations and writes into a write quorum of its own. With a single acceptor as a read quorum and all acceptors as the write quorum, $f + 1$ acceptors tolerate $f$ crashes, and the algorithm becomes classic [primary-backup replication](/primary-backup-replication/). The model is [asynchronous](/asynchronous-model/) with [crash failures](/crash-failure/), and the master is assumed not to fail.

## In plain words

A small team keeps a shared notebook. Each copy of the notebook is held by one team member. A manager, who rarely has to act, decides who is on the team.

When a member leaves, the manager names a new team and a new head. The new head first reads the notebook from the old team, then writes it to the new team. Only after that does the manager say "this team is now in charge".

Because the manager makes the decision about who is on the team, the team itself does not need a majority vote for that. So two copies are enough to survive one loss: the head reads from any one survivor and writes to everyone.

## The problem

**Model.** Processes fail by [crashing](/crash-failure/) and messages are [asynchronous](/asynchronous-model/). A master process, itself made reliable with a [replicated state machine](/replicated-state-machine/) such as [Multi-Paxos](/multi-paxos/), starts ballots and picks configurations. The goal is the [consensus problem](/consensus-problem/): choose one proposed value, and never two. For a state machine, run one instance per command, as in Multi-Paxos.

**Quorums per ballot.** For each ballot $b$, the master picks a set of read b-quorums and a set of write b-quorums. Every write b-quorum meets every read b-quorum and every write b-quorum. Configurations of different ballots need not meet at all. A value is *chosen in ballot* $b$ when every acceptor of a write b-quorum has voted for it in $b$.

**Safe values and complete ballots.** A value $v$ is *safe at* $b$ when no other value is chosen, or can still be chosen, in a ballot below $b$. Paxos keeps the invariant that acceptors vote only for safe values. A ballot is *complete* when a value is chosen in it or all values are safe at it. Once ballot $d$ is complete, a new leader need not look below $d$.

## The algorithm

Lamport, Malkhi and Zhou give two variants. They differ in which old configurations a new leader reads.

```pseudo id=main
MASTER (reliable)
L1  to start ballot b:  pick config(b) and its quorums; send newBallot(b, completeBal) in VP I, or newBallot(b, prevBal ← curBal) in VP II
L2  VP I, on complete(b):  completeBal ← max(completeBal, b)
L3  VP II, on complete(b, p):  if p = curBal then curBal ← b; send activated(b)

LEADER of ballot b
L4  safe ← AllSafe; c ← b - 1 in VP I, or c ← prevBal in VP II
L5  while safe = AllSafe and c ≥ completeBal (VP I), or once (VP II):  send 1a(b, c) to the acceptors of config(c)
L6      on 1b(b, c, v) with v ≠ None:  safe ← v
L7      on 1b(b, c, None) from a read c-quorum:  c ← c - 1 in VP I; stop in VP II
L8  if safe ≠ AllSafe:  send 2a(b, safe) to config(b); wait for 2b from a write b-quorum
L9  send complete(b) to the master; in VP II, wait for activated(b)
L10 if safe = AllSafe:  send 2a(b, v) for a client value v

ACCEPTOR a, with maxBallot and vote[·]
L11 on 1a(b, c):  if b ≥ maxBallot then maxBallot ← b; send 1b(b, c, vote[c])
L12 on 2a(b, v):  if b ≥ maxBallot then maxBallot ← b; vote[b] ← v; send 2b(b, v)

LEARNER
L13 v is chosen in b when a write b-quorum has voted v in b and, in VP II, b is activated
```

**Phase 1 reads old configurations** (lines L4 to L7). This is the FindSafe procedure of the paper, cut off at a complete ballot. The leader asks about ballot $c$ only the acceptors of config($c$). A vote in $c$ makes that value safe, because only the leader of $c$ proposes in $c$, and it proposed a safe value. A read c-quorum with no vote in $c$ and $maxBallot > c$ proves that nothing is chosen or choosable in $c$, because each write c-quorum meets it. Then the leader looks one ballot lower.

**Phase 2 writes the new configuration** (line L8). The 2a message carries the safe value to config($b$). This is the *state transfer*. When a write b-quorum has voted, $b$ is complete.

**Vertical Paxos I** (lines L2 and L5). The master keeps the largest complete ballot. A new configuration can accept new commands at once, while old configurations still hold data. If many leaders fail before they complete, a later leader may have to read many configurations, back to $completeBal$.

**Vertical Paxos II** (lines L3 and L5). Ballots start as inactive. A leader reads only config($prevBal$), the last activated ballot, and does phase 2 as if $b$ were next. The master activates $b$ only if no other ballot was activated since $b$ began (line L3). A ballot that is never activated does not count: its votes have no effect, and learners must ignore them (line L13). Then the leader takes new client values (line L10).

**The primary-backup case.** Let a read quorum be any one acceptor, and the write quorum be all acceptors of the configuration. Let the new leader, the *primary*, be an acceptor of the previous configuration. Then it is a read quorum by itself and does phase 1 locally. Phase 2 writes to all *backups*. This is Vertical Paxos II with $f + 1$ acceptors per configuration.

## Example

Vertical Paxos II with primary-backup quorums. Configuration 0 is $\{A, B\}$, and nothing has voted in ballot 0.

| step | event | master | votes |
|---|---|---|---|
| 1 | ballot 1, config $\{A, B\}$, $prevBal = 0$; leader $A$ reads its own empty vote in ballot 0: AllSafe | | |
| 2 | complete(1, 0) | $curBal = 1$, activated(1) | |
| 3 | client value $x$: 2a(1, $x$) to $A, B$; both vote | | $A$: 1 → $x$; $B$: 1 → $x$ |
| 4 | $x$ is chosen in ballot 1 (write quorum $\{A, B\}$) | | |
| 5 | $B$ crashes; ballot 2, config $\{A, C\}$, $prevBal = 1$ | | |
| 6 | leader $A$ sends 1a(2, 1) to $\{A, B\}$; its own 1b reports $x$ | | |
| 7 | 2a(2, $x$) to $A, C$; both vote (state transfer to $C$) | | $A$: 2 → $x$; $C$: 2 → $x$ |
| 8 | complete(2, 1) | $curBal = 2$, activated(2) | |

The crash of $B$ did not stop progress, though only two acceptors were ever in a configuration. In plain Paxos, two acceptors cannot tolerate one crash.

## Correctness

**Safety.** Lamport, Malkhi and Zhou keep the Paxos invariant: an acceptor votes in ballot $b$ only for a value safe at $b$. Then at most one value is chosen.

- One value per ballot: only the leader of $b$ sends 2a($b$, ·), and it sends one value.
- A vote found in config($c$) is safe at $b$: it was safe at $c$, and every ballot between $c$ and $b$ has been checked.
- A read c-quorum with no vote in $c$ and $maxBallot \ge b > c$ shows that nothing is choosable in $c$, since every write c-quorum contains one of these acceptors, which will never vote in $c$.
- A complete ballot $d$ makes everything below $d$ irrelevant: either a value is chosen in $d$ and is the only safe value above $d$, or all values are safe at $d$.
- In VP II, the ballots between $prevBal$ and $b$ are never activated, so they are not ballots of the algorithm at all, and the master activates ballots in increasing order.

The full proof is below.

**Liveness.** As in Paxos, progress needs one leader at a time, here started by the master, and live quorums: a read quorum of each configuration that the leader reads, and a write quorum of the new one. The paper leaves liveness out of scope. The tests start a new ballot only when the current one stalls; a master that starts ballots too often can keep VP I leaders reading old configurations forever.

## Complexity

Let $n$ be the number of acceptors in a configuration and $c$ the number of old configurations a leader reads.

- **Steady state.** As in Multi-Paxos: 2a to $n$ acceptors and $n$ replies per command, two message delays from the leader.
- **Leader change.** $2n$ messages per configuration read, then $2n$ for the state transfer, plus messages to the master. In VP II, $c = 1$. In VP I, $c$ is the number of ballots since the last complete one.
- **Machines.** With primary-backup quorums, $f + 1$ acceptors per configuration tolerate $f$ crashes, because the master, not the acceptors, decides the configuration.
- **State transfer.** For a state machine, phase 2 copies the whole state to the new acceptors. VP I lets new commands run during this copy. VP II waits for it before activation.

## Properties

- **Reconfiguration inside an instance.** The configuration changes with the ballot ("vertically"), not with the instance ("horizontally", as in the α window of [Cheap Paxos](/cheap-paxos/)).
- **Read and write quorums.** Only read and write quorums of the same ballot must meet, as in [Flexible Paxos](/flexible-paxos/).
- **Needs an external master.** The master must be reliable, so it is usually a separate Paxos group. It is used only for reconfiguration.
- **Safety does not depend on timing.**

## Variants and improvements

- **Primary-backup systems.** The paper shows Niobe and chain replication as instances of Vertical Paxos II, and explains how the Google File System could be made consistent with it.
- **Local reads with a lease.** A primary can answer reads alone while it holds a [lease](/leader-lease/), and the master does not start a new ballot before the lease ends.
- **Removing backups without a new ballot.** With a single write quorum per ballot, the master may shrink that write quorum at any time, as Niobe does.

## When to use it

Use Vertical Paxos, often in its primary-backup form, in a large storage system with many small replica groups and a shared, reliable configuration service. It saves machines, because each group needs $f + 1$ replicas instead of $2f + 1$. Use VP I when state transfer is slow and the group must serve requests at full fault tolerance during the copy. Do not use it without a reliable master: then the replicas must reconfigure themselves, as in [cluster reconfiguration](/cluster-reconfiguration/).

## Pitfalls

- **Quorums that do not meet.** Line L7 trusts a read c-quorum with no votes. If a write c-quorum can avoid it, a value chosen in $c$ is missed. The tests find two chosen values with one-acceptor read and write quorums.
- **Counting an inactive ballot.** In VP II, line L8 lets a write quorum vote before the master activates $b$. A learner that counts these votes, against line L13, can learn an old value that a competing, activated ballot has replaced. The tests find such runs.
- **Skipping configurations in VP I.** Line L5 must read every ballot down to $completeBal$, even those whose leaders failed early, since one of them may have chosen a value.
- **Starting phase 2 for client values too early.** Line L10 runs only after the ballot is complete (VP I) or activated (VP II). Before that, a client value may not be safe.
- **A master that changes its mind.** Once the master has given config($b$), it must never change it. The master's own state must be replicated.

## Implementations

## History

Lamport, Malkhi and Zhou presented Vertical Paxos at PODC 2009. The authors note that the only earlier algorithm of this family they know is an unpublished version of Cheap Paxos. They used it to explain primary-backup protocols used in practice, such as Niobe and chain replication, as Paxos algorithms.

## References
