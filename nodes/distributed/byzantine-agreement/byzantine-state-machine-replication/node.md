---
tag: PV9DJN
kind: problem
slug: byzantine-state-machine-replication
name: Byzantine state machine replication
aliases:
- BFT state machine replication
- Byzantine SMR
area: distributed/byzantine-agreement
level: advanced
summary: Run one deterministic service on n replicas, up to f of them Byzantine, so that clients see one correct sequence of results. Needs n ≥ 3f + 1 and f + 1 matching replies.
prereqs: [state-machine-replication, byzantine-failure-model, partial-synchrony, quorum-intersection]
see_also: [pbft, zyzzyva, hotstuff, tendermint, honeybadger-bft, quorum-certificate, byzantine-quorum-system, byzantine-resilience-bound]
sources:
  - paper: doi:10.1145/98163.98167
    title: Fred B. Schneider, Implementing fault-tolerant services using the state machine approach, a tutorial, ACM Computing Surveys 22(4), 1990
    locator: the state machine approach, agreement and order, and the 2t + 1 replicas needed to outvote t Byzantine outputs
  - paper: doi:10.1145/571637.571640
    title: Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance and proactive recovery, ACM Transactions on Computer Systems 20(4), 2002
    locator: the service properties, the 3f + 1 replicas, the client that waits for f + 1 matching replies, and the read-only optimization with 2f + 1 replies
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: Byzantine consensus with partial synchrony needs n > 3f
  - paper: doi:10.1145/3293611.3331591
    title: Maofan Yin, Dahlia Malkhi, Michael K. Reiter, Guy Golan Gueta and Ittai Abraham, HotStuff, BFT consensus with linearity and responsiveness, PODC 2019
    locator: the table that compares the authenticator cost of PBFT, Tendermint and HotStuff in the normal case and at a leader change
  - paper: doi:10.1145/2976749.2978399
    title: Andrew Miller, Yu Xia, Kyle Croman, Elaine Shi and Dawn Song, The honey badger of BFT protocols, ACM CCS 2016
    locator: asynchronous atomic broadcast from reliable broadcast and binary agreement, and the per-transaction cost with large batches
---

Byzantine state machine replication is the problem of running one deterministic service on $n$ replicas so that the service stays correct and available while up to $f$ replicas are [Byzantine](/byzantine-failure-model/): they may crash, lie, or work together against the others. It is [state machine replication](/state-machine-replication/) with the crash failures replaced by arbitrary ones. The replicas must agree on one order of client requests and execute it, and each client must be able to tell a correct reply from a false one. With signatures and [partial synchrony](/partial-synchrony/) it needs $n \ge 3f + 1$ replicas, and a client accepts a result after $f + 1$ matching replies. [PBFT](/pbft/) made it practical in 1999, and blockchains made it common.

## In plain words

A company runs a service on several computers so that it keeps working if some of them fail. Here a failed computer may do anything: give wrong answers, tell different computers different things, or work with the other bad computers.

The computers must run the same requests in the same order, so they all reach the same state. A client asks all of them and waits until $f + 1$ give the same answer: at least one of those is honest, so the answer is right. To make this work with $f$ bad computers, the group needs at least $3f + 1$ computers.

## Definition

A *service* is a deterministic state machine: a state, and an operation $op$ that maps a state and a request to a new state and a reply. There are $n$ replicas, each with a copy of the state, and any number of clients. At most $f$ replicas are Byzantine; any client may also be faulty. Messages are signed or authenticated, so a message cannot be forged. A solution must give:

- **Safety (linearizability).** The replies that honest clients accept are the replies of a single sequential execution of the requests, in an order that respects real time: if a request completes before another starts, it comes first. Equivalently, honest replicas execute the same sequence of requests, and a client accepts a reply only if it is the result of that sequence.
- **Liveness.** Every request of an honest client eventually completes.

Safety must hold in every run. By the FLP result, no deterministic protocol gives liveness in the [asynchronous model](/asynchronous-model/), so deterministic protocols guarantee it only after GST under partial synchrony, and asynchronous protocols use randomness.

**Why $f + 1$ matching replies.** Each reply carries the result and the replica. Up to $f$ replies can come from faulty replicas and can say anything, and the faulty replicas can agree on the same false reply. So $f$ matching replies prove nothing. With $f + 1$ matching replies from different replicas, at least one comes from an honest replica, which executed the agreed sequence, so the result is the correct one. The client may need to wait for more than $f + 1$ replies to get $f + 1$ that match, but at most $2f + 1$: all $n - f \ge 2f + 1$ honest replicas send the same reply.

The count $f + 1$ is enough only when the honest replicas that reply have already committed the order. A protocol whose replicas reply before commit, as with speculation in [Zyzzyva](/zyzzyva/) or the read-only optimization of PBFT, needs more matching replies: $2f + 1$ for reads in PBFT, $3f + 1$ or a commit certificate in Zyzzyva.

## Variants

- **Timing.** Partially synchronous protocols (PBFT, Zyzzyva, HotStuff, Tendermint) are safe always and live after GST. Asynchronous protocols ([HoneyBadgerBFT](/honeybadger-bft/)) are live with probability 1 in every run and use randomness. Synchronous protocols tolerate more faults with signatures but lose safety if the bound on delay fails.
- **Permissioned and permissionless.** The classical problem has a fixed, known set of replicas. Blockchains with [proof of stake](/proof-of-stake/) count voting power instead of replicas, and the bounds become fractions of the total power.
- **Read-only requests.** Reads can skip ordering if the client waits for $2f + 1$ matching replies, and falls back to the ordered path if they disagree.
- **Proactive recovery.** Replicas are restarted from a clean state from time to time, so the bound $f$ applies within a window of time and not to the whole life of the system.
- **Separating agreement from execution.** Agreement needs $3f + 1$ replicas, but $2f + 1$ execution replicas suffice when agreement is done by others.

## Examples

**A bank account.** The state is a balance, requests are deposits and withdrawals. With $n = 4$ and $f = 1$, a faulty replica that reports a balance of one million gets no other replica to match it, so the client ignores it.

**Two orders.** If a faulty primary tells replicas 1 and 2 that "withdraw 100" is first and replica 3 that "deposit 100" is first, the replicas would end in different states. An ordering protocol must stop this: in [PBFT](/pbft/), each order needs a [quorum certificate](/quorum-certificate/) of $2f + 1$ PREPARE messages, and two such sets share an honest replica.

**Comparison of the protocols on this site.** Delays count message delays in the normal case, from the leader's proposal to the commit at the replicas. Messages are per decision, with $n$ replicas.

| protocol | timing | normal-case phases | delays to commit | messages per decision | leader change |
|---|---|---|---|---|---|
| [PBFT](/pbft/) | partial synchrony | pre-prepare, prepare, commit | 3 | $\Theta(n^2)$ | VIEW-CHANGE and NEW-VIEW with certificates, $O(n^3)$ signatures in total |
| [Zyzzyva](/zyzzyva/) | partial synchrony | order, then speculative execution; commit certificate if fewer than $3f + 1$ replies | 2 (fast path), 4 (two-phase) | $\Theta(n)$ | view change with commit certificates and histories; unsafe as published |
| [HotStuff](/hotstuff/) | partial synchrony | prepare, pre-commit, commit, decide, each with a threshold-signed QC | 7 (basic), one QC per block in the chained version | $\Theta(n)$ | part of the protocol, $\Theta(n)$ messages; optimistically responsive |
| [Tendermint](/tendermint/) | partial synchrony | propose, prevote, precommit | 3 | $\Theta(n^2)$, more with gossip | a new round with the next proposer; locks carry state; waits for timeouts |
| [HoneyBadgerBFT](/honeybadger-bft/) | asynchronous | threshold encryption, $n$ reliable broadcasts, $n$ binary agreements | $O(\log n)$ expected rounds | $O(n)$ bits per transaction for large batches | no leader |

## Known algorithms

- [PBFT](/pbft/) (Castro and Liskov, 1999): the first practical protocol, three phases with a stable primary.
- [Zyzzyva](/zyzzyva/) (Kotla and others, 2007): speculative execution with a fast path; its view change was later shown unsafe.
- [HotStuff](/hotstuff/) (Yin and others, 2019): linear messages through threshold signatures and a three-chain commit rule.
- [Tendermint](/tendermint/) (Kwon 2014, Buchman, Kwon and Milosevic 2018): rotating proposers, locks and gossip, for blockchains.
- [HoneyBadgerBFT](/honeybadger-bft/) (Miller and others, 2016): asynchronous atomic broadcast with no leader.

## Bounds

- **Replicas.** $n \ge 3f + 1$ for any solution that is safe in every run and live after GST, because Byzantine consensus under partial synchrony needs it ([the resilience bound](/byzantine-resilience-bound/)). Signatures do not help here, because the protocol must decide without hearing from $f$ replicas that may be only slow.
- **Quorums.** With $n = 3f + 1$, a quorum of $2f + 1$ is the most the protocol can wait for, since $f$ replicas may never answer, and two quorums of $2f + 1$ share $f + 1$ replicas, one of them honest. This [quorum intersection](/quorum-intersection/) argument is the core of every protocol above; see [Byzantine quorum systems](/byzantine-quorum-system/).
- **Latency.** Three message delays to commit in the normal case with $3f + 1$ replicas; two-delay fast paths need more replicas, such as $5f + 1$, or a speculative design.
- **Messages.** Deterministic protocols need $\Omega(n^2)$ messages in the worst case (the [Dolev-Reischuk bound](/dolev-reischuk-lower-bound/)); HotStuff reaches $O(n)$ per decision in the normal case and at a leader change, and $O(n^2)$ over a run with $f$ faulty leaders.

## Reductions

- **From consensus.** Run one instance of Byzantine consensus per position of the log, with the requests as proposals and a validity check that the request is signed by a client. The decided sequence is the order, and each replica executes it.
- **To consensus.** Byzantine SMR with one write request per replica solves consensus on the first request, so it inherits every lower bound of Byzantine consensus.
- **Atomic broadcast.** SMR is the same as Byzantine [total order broadcast](/total-order-broadcast/) of requests followed by deterministic execution.

## Applications

- Permissioned blockchains and [proof-of-stake](/proof-of-stake/) chains (Tendermint in Cosmos, HotStuff descendants in Diem and Aptos).
- Critical coordination services, such as certificate authorities and key stores, that must survive an intrusion into some servers.
- Research systems for BFT file systems and databases, starting with the BFS file system of PBFT.

## References
