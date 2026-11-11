---
tag: XGV05H
kind: algorithm
slug: hotstuff
name: HotStuff
aliases:
- HotStuff BFT
- Basic HotStuff
- Chained HotStuff
area: distributed/byzantine-agreement
level: advanced
summary: Leader-based BFT replication with 3f + 1 replicas, three voting phases and threshold-signature QCs, so each view costs O(n) messages and a correct leader moves at network speed.
solves: [byzantine-state-machine-replication]
model: partial-synchrony
complexity:
  vars: {n: the number of replicas, f: the largest number of Byzantine replicas, d: the largest message delay after GST}
  time: {best: 7d}
  messages: {best: 8(n - 1), worst: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [pbft, quorum-certificate, threshold-signature, partial-synchrony]
see_also: [pbft, tendermint, quorum-certificate, threshold-signature, view-change, byzantine-state-machine-replication, zyzzyva, honeybadger-bft]
sources:
  - paper: doi:10.1145/3293611.3331591
    title: Maofan Yin, Dahlia Malkhi, Michael K. Reiter, Guy Golan Gueta and Ittai Abraham, HotStuff, BFT consensus with linearity and responsiveness, ACM Symposium on Principles of Distributed Computing (PODC), 2019
    locator: Basic HotStuff with its safeNode rule, the safety and liveness arguments, Chained HotStuff with the three-chain commit rule, the pacemaker, and the comparison table
  - url: https://arxiv.org/abs/1803.05069
    title: Maofan Yin, Dahlia Malkhi, Michael K. Reiter, Guy Golan Gueta and Ittai Abraham, HotStuff, BFT consensus in the lens of blockchain, arXiv 1803.05069 (2018)
    locator: the long version with full proofs
  - paper: doi:10.1145/571637.571640
    title: Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance and proactive recovery, ACM Transactions on Computer Systems 20(4), 2002
    locator: the two-phase protocol and the view change that HotStuff makes linear
---

HotStuff is a leader-based protocol for [Byzantine state machine replication](/byzantine-state-machine-replication/) with $n = 3f + 1$ replicas under [partial synchrony](/partial-synchrony/). In each view a leader proposes a node that extends a tree of commands, and the replicas vote in three phases: prepare, pre-commit and commit. The leader combines $n - f$ votes into one [quorum certificate](/quorum-certificate/) (QC), a [threshold signature](/threshold-signature/) of constant size, and sends it to all. So every phase, and also the change of leader, costs $O(n)$ messages. The third phase makes the protocol *optimistically responsive*: after GST a correct leader needs to wait only for $n - f$ messages, never for a fixed delay. Yin, Malkhi, Reiter, Golan Gueta and Abraham published it at PODC 2019. Its chained form, in which each new proposal carries the QC of the one before, was the basis of LibraBFT and of many later blockchain protocols.

## In plain words

A group of $3f + 1$ computers keeps one list of commands, and up to $f$ of them may cheat. In each round one computer leads, and the leader changes every round.

The leader proposes a new command that comes after the newest command that the group has seen approved. The others vote, the leader collects $2f + 1$ votes, packs them into one short certificate and sends it to all. This happens three times for the same proposal. After the second certificate a computer "locks" on the proposal and will only vote for proposals that build on it, unless it sees newer proof. After the third certificate the command is final.

Because the leader talks to all and all talk only to the leader, each round costs a number of messages that grows only linearly with the group.

## The problem

The setting is the one of [PBFT](/pbft/): $n = 3f + 1$ replicas, at most $f$ of them [Byzantine](/byzantine-failure-model/), authenticated channels, and a partially synchronous network in which every message between honest replicas arrives within an unknown bound $\Delta$ after an unknown time GST. Replicas share a $(n - f, n)$ threshold signature scheme: $n - f$ partial signatures on one message combine into one signature. The goal is that honest replicas execute the same commands in the same order (safety in every run) and that commands keep being executed after GST (liveness).

## The algorithm

A node $b$ is a command and a pointer to its parent node, so the nodes form a tree from a root. A QC of type $\tau$ is the combined signature of $n - f$ votes on $(\tau, v, b)$; write $qc.view$ and $qc.node$. Each replica keeps $prepareQC$, the highest prepareQC it saw, and $lockedQC$, both at the root at the start. The leader of view $v$ is replica $v \bmod n$.

```pseudo id=main
BASIC-HOTSTUFF(i)                                                   ▷ replica i in view v, n = 3f + 1
L1  on entering view v: send ⟨NEW-VIEW, v, prepareQC⟩ to leader(v)
L2  leader: with n - f NEW-VIEW: highQC ← the one of highest view; b ← (cmd, highQC.node); broadcast ⟨PREPARE, v, b, highQC⟩
L3  on ⟨PREPARE, v, b, qc⟩ from leader(v): if qc.view < v, b.parent = qc.node and safeNode(b, qc): vote (prepare, v, b)
L4  safeNode(b, qc) ⇔ b extends lockedQC.node or qc.view > lockedQC.view
L5  leader: with n - f prepare votes on (v, b): combine a prepareQC; broadcast ⟨PRE-COMMIT, v, prepareQC⟩
L6  on PRE-COMMIT: prepareQC ← qc; vote (pre-commit, v, b)
L7  leader: with n - f pre-commit votes: combine a precommitQC; broadcast ⟨COMMIT, v, precommitQC⟩
L8  on COMMIT: lockedQC ← qc; vote (commit, v, b)
L9  leader: with n - f commit votes: combine a commitQC; broadcast ⟨DECIDE, v, commitQC⟩
L10 on DECIDE: execute the commands on the branch from the root to qc.node; go to view v + 1
L11 on timeout in view v: send ⟨TIMEOUT, v⟩ to all; go to view v + 1 with 2f + 1 of them   ▷ the pacemaker
```

A replica votes at most once per type and view, and only in its current view. Votes go only to the leader.

**The pacemaker.** The paper keeps safety apart from liveness and leaves the view synchronization to a *pacemaker*. The implementation of this page uses a simple one: a replica that times out in view $v$ sends TIMEOUT for $v$ to all and doubles its timeout; it sends its own TIMEOUT when $f + 1$ others did; and it moves to $v + 1$ with $2f + 1$ TIMEOUT messages, or at once when the leader of a higher view sends it a valid message. This pacemaker costs $O(n^2)$ messages in a view that fails, but nothing in a view that succeeds.

**Chained HotStuff.** All four phases have the same shape: the leader sends a QC, the replicas vote. Chained HotStuff runs one *generic* phase per view, and the QC formed in view $v$ goes inside the proposal of view $v + 1$. So the prepare phase of one node is the pre-commit phase of its parent and the commit phase of its grandparent. A replica that receives node $b^*$ looks at the chain $b^* \to b'' \to b' \to b$, where each arrow follows the QC inside a node:

- **One-chain.** $prepareQC \leftarrow$ the QC for $b''$ inside $b^*$.
- **Two-chain.** If $b''.parent = b'$, then $lockedQC \leftarrow$ the QC for $b'$.
- **Three-chain.** If also $b'.parent = b$, then $b$ and its ancestors are committed.

The commit needs direct parents, which means three QCs in three views in a row. If a leader fails, the chain has a gap and the commit waits for a new three-chain.

## Example

Take $n = 4$, $f = 1$ and unit message delays. In view 1, with leader $p_1$, each of the three others sends NEW-VIEW to $p_1$ (3 messages). $p_1$ proposes $b_1 = (r_0, root)$ to the 3 others, gets 3 prepare votes (its own and 2 others), sends PRE-COMMIT, and so on.

| delay | messages | count |
|---|---|---|
| 1 | NEW-VIEW to the leader | 3 |
| 2 | PREPARE from the leader | 3 |
| 3 | prepare votes | 3 |
| 4 | PRE-COMMIT with the prepareQC | 3 |
| 5 | pre-commit votes | 3 |
| 6 | COMMIT with the precommitQC, replicas lock | 3 |
| 7 | commit votes | 3 |
| 8 | DECIDE with the commitQC, replicas execute $r_0$ | 3 |

That is $8(n - 1) = 24$ messages and 8 delays, 7 of them after the proposal. The implementation decides at time 8 in this case and sends $8(n - 1)$ messages per view for $n = 4, 7, 10$. PBFT sends $2n(n - 1)$ messages for the same request, which is also 24 at $n = 4$ but grows as $n^2$.

**Chained HotStuff on the same run.** The QC for each node rides on the next proposal.

| a replica receives | QC inside | prepareQC | lockedQC | committed |
|---|---|---|---|---|
| $b_2$ | for $b_1$ | $b_1$ | root | nothing |
| $b_3$ | for $b_2$ | $b_2$ | $b_1$ | root |
| $b_4$ | for $b_3$ | $b_3$ | $b_2$ | $b_1$ |

Each view adds one node and commits one, so the throughput is one node per view, and a node is final three views after it is proposed.

**A fork attack.** Let $p_1$ be faulty, and let it propose in a later view a node whose parent is the root, with the root QC as justify, and show its prepareQC to one honest replica only. Honest replicas that locked on a newer node refuse the fork, because the fork does not extend their lock and the root QC is not newer than their lock. If the test of line L4 is removed, the tests of the implementation show that honest replicas then execute two conflicting branches.

## Correctness

The full proof is below.

- **One QC per view and type.** Two QCs come from two quorums of $2f + 1$, which share an honest replica, and an honest replica votes once per view and type.
- **Safety.** Suppose a commitQC exists for $w$ in view $v_1$. Take the lowest-view prepareQC above $v_1$ whose node does not extend $w$. An honest replica signed both the commitQC for $w$ and that prepareQC, so it was locked on $w$ or a descendant. By $safeNode$, its vote needs the node to extend its lock, which fails, or a justify QC newer than the lock, which would be an even lower prepareQC that does not extend $w$. Both are impossible, so every later certified node extends $w$.
- **Liveness and the third phase.** A lock is on a precommitQC, so $f + 1$ honest replicas know the matching prepareQC, and one of them is in every set of $n - f$ NEW-VIEW messages. So an honest leader's $highQC$ is at least as new as every honest lock, every honest replica accepts its proposal, and the view decides in $7\Delta$ after GST. The pacemaker doubles timeouts until views last long enough, and one leader in any $f + 1$ in a row is honest.

## Complexity

- **Messages.** Per view, $n - 1$ NEW-VIEW, four leader broadcasts and three rounds of votes to the leader: $8(n - 1) = O(n)$ messages. This holds also when the leader changes, which is the main gain over PBFT, whose view change costs $O(n^2)$ messages carrying $O(n^3)$ signatures. With $f$ faulty leaders in a row the cost is $O(f n)$ for the protocol itself.
- **Authenticators.** Each QC is one threshold signature, so each message has $O(1)$ signatures.
- **Latency.** Seven message delays from the proposal to the decision in Basic HotStuff, against three in PBFT. Chained HotStuff decides a node three views after it is proposed but finishes one node per view.
- **View synchronization.** The pacemaker is not counted in the $O(n)$ bound. Simple pacemakers, like the one in the implementation, cost $O(n^2)$ messages in a failed view.
- **Space.** The leader keeps $O(n)$ partial signatures per phase; replicas keep two QCs and the tree of uncommitted nodes.

## Properties

- **Deterministic and partially synchronous.** Safety holds in every run, liveness after GST.
- **Linear.** $O(n)$ messages per view with a correct leader and also on a leader change.
- **Optimistically responsive.** After GST a correct leader proceeds as soon as it has $n - f$ messages.
- **Rotating leader.** The leader changes every view at no extra cost, which spreads the load and limits what one faulty leader can do.
- **Optimal resilience.** $n = 3f + 1$.

## Variants and improvements

- **Two-phase HotStuff.** Locking on the prepareQC saves a phase but loses responsiveness: the leader must wait for the maximal delay $\Delta$ to be sure that it sees the highest lock, as in [Tendermint](/tendermint/).
- **Event-driven and pipelined forms.** Chained HotStuff and its event-driven description put one generic phase in each view, so three proposals are in flight at a time.
- **LibraBFT and DiemBFT.** These protocols use chained HotStuff with a pacemaker that forms timeout certificates, as the implementation of this page does.
- **Fewer phases.** Later work, such as Fast-HotStuff and HotStuff-2, keeps linearity with two phases in the common case by adding information to the view change.
- **Signatures.** With [aggregate](/aggregate-signature/) [BLS signatures](/bls-signature/) a QC is one signature plus a bit vector of signers, which needs no trusted setup for a threshold key.

## When to use it

Use HotStuff, or one of its descendants, for Byzantine replication with many replicas, tens to hundreds, where the $O(n^2)$ messages of [PBFT](/pbft/) per request and its large view change are too costly, and where leaders should rotate often. It is a common choice for permissioned and proof-of-stake blockchains. For a small group on a fast network, PBFT has lower latency. For networks without timing guarantees, use an asynchronous protocol such as [HoneyBadgerBFT](/honeybadger-bft/).

## Pitfalls

- **Accepting a justify QC from the current view or a later one.** The safety proof needs $justify.view < v$. Without the check a faulty leader can use a QC of a higher view to break a lock.
- **Locking on the prepareQC.** That is two-phase HotStuff. It is safe, but a correct leader can then stall unless it waits $\Delta$.
- **Moving the lock backwards.** The lock must only move to QCs of higher views.
- **The three-chain without direct parents.** In Chained HotStuff, a commit needs $b''.parent = b'$ and $b'.parent = b$. Three QCs that skip a view do not commit $b$.
- **Ignoring the pacemaker.** With no view synchronization, honest replicas can sit in different views forever, each waiting for a leader that the others do not follow. A first version of the implementation moved to the next view on its own timeout alone, and a replica could run ahead of the others and stall the group.
- **Threshold keys.** A $(n - f, n)$ threshold key needs a trusted dealer or a distributed key generation protocol. Aggregate signatures avoid this but make each QC grow by $n$ bits.

## Implementations

## History

PBFT (1999) made Byzantine replication practical but kept all-to-all phases and a costly view change. Tendermint (described by Buchman, Kwon and Milosevic in 2018) used rotating proposers, gossip and two voting steps with a wait of $\Delta$. Yin, Malkhi, Reiter, Golan Gueta and Abraham put HotStuff on arXiv in 2018 and presented it at PODC 2019, with the third phase that gives linearity and responsiveness together. Facebook's Libra project (later Diem) built LibraBFT on chained HotStuff in 2019, and many later systems took it over.

## References
