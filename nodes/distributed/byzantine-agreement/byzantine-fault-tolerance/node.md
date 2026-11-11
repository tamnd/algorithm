---
tag: 3HEGC7
kind: concept
slug: byzantine-fault-tolerance
name: Byzantine fault tolerance
aliases:
- BFT
- Byzantine-fault-tolerant replication
area: distributed/byzantine-agreement
level: intro
summary: "The property of a replicated system that gives correct results while some replicas act arbitrarily. It usually needs 3f + 1 replicas to agree on order with f faults."
prereqs: [byzantine-failure-model, state-machine-replication]
see_also: [pbft, hotstuff, tendermint, honeybadger-bft, byzantine-quorum-system, quorum-certificate, byzantine-state-machine-replication, byzantine-resilience-bound]
sources:
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 1 (the problem of reliable systems with components that send conflicting information) and Section 6 (reliable systems from redundant processors that vote)
  - paper: doi:10.1145/98163.98167
    title: Fred B. Schneider, Implementing fault-tolerant services using the state machine approach, a tutorial, ACM Computing Surveys 22(4), 1990
    locator: Section 3 (with Byzantine failures, a t fault-tolerant ensemble needs 2t + 1 replicas and its output is the majority output)
  - paper: doi:10.1145/571637.571640
    title: Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance and proactive recovery, ACM Transactions on Computer Systems 20(4), 2002
    locator: Sections 2 and 3 (the service model with 3f + 1 replicas, quorums of 2f + 1, and f + 1 matching replies to the client)
  - paper: doi:10.1145/945445.945470
    title: Jian Yin, Jean-Philippe Martin, Arun Venkataramani, Lorenzo Alvisi and Mike Dahlin, Separating agreement from execution for Byzantine fault tolerant services, SOSP 2003
    locator: Sections 1 to 3 (3f + 1 agreement replicas and 2f + 1 execution replicas)
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: Section 1, Table 1 (n >= 3t + 1 for Byzantine faults under partial synchrony, with or without signatures)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapters 2, 3 and 5 (Byzantine process abstractions, Byzantine broadcast and Byzantine consensus)
---

Byzantine fault tolerance (BFT) is the property of a distributed system that keeps giving correct results while up to $f$ of its components fail in [arbitrary ways](/byzantine-failure-model/): they may crash, send wrong data, send different data to different parties, or act together against the others. In practice, BFT means a service that runs on many replicas so that clients get correct answers even if $f$ replicas are buggy or under the control of an attacker. Two numbers mark the area. With deterministic replicas that already receive the same requests in the same order, $2f + 1$ replicas and a majority vote on the outputs are enough (Schneider, 1990). To make the replicas *agree on that order* without synchronized clocks, $3f + 1$ replicas are needed, as in [PBFT](/pbft/) and its successors. This page is the map of the area. The protocols and bounds have their own pages.

## In plain words

Some computers in a group may lie, and nobody knows which ones. The group must still act as one honest computer. So each request goes to all of them, each one runs it, and the answer that most of them give wins.

This works only if all honest computers run the same requests in the same order. Agreeing on that order is the hard part, because a liar can tell different things to different computers. Without exact clocks, the group needs more than three times as many computers as liars. With one liar, that means four computers.

## The idea

**Replicate and vote.** Model the service as a deterministic state machine. Run copies of it on $n$ replicas. If every correct replica starts in the same state and runs the same requests in the same order, every correct replica gives the same outputs. This is [state machine replication](/state-machine-replication/). Two parts are needed:

1. *Agreement.* All correct replicas receive the same sequence of requests. This is a sequence of [Byzantine agreement](/byzantine-broadcast/) instances.
2. *Output voting.* A client accepts an output when enough replicas give it.

**Why $2f + 1$ for voting.** With $n = 2f + 1$ replicas and at most $f$ faulty, at least $f + 1$ correct replicas give the same output, and the faulty ones give at most $f$ copies of any wrong output. So the majority output is correct. Schneider states this for Byzantine failures: a $t$ fault-tolerant ensemble needs $2t + 1$ replicas, and its output is the output of the majority. This is the same idea as triple modular redundancy in hardware, where three units and a voter mask one fault.

**Why $3f + 1$ for agreement.** The $2f + 1$ count assumes that agreement is already solved. How many replicas agreement needs depends on the model:

- In the synchronous model with signatures, Byzantine broadcast works for any $f < n$, so $2f + 1$ replicas can also agree on the order. See the [authenticated resilience bound](/authenticated-resilience-bound/).
- In the synchronous model without signatures, agreement needs $n > 3f$. See the [Byzantine resilience bound](/byzantine-resilience-bound/).
- Under [partial synchrony](/partial-synchrony/) and in the asynchronous model, agreement needs $n > 3f$ even with signatures (Dwork, Lynch and Stockmeyer; Bracha and Toueg).

Real networks have no bound on delay that holds all the time, so practical BFT protocols assume partial synchrony and use $n = 3f + 1$.

**Quorums.** With $n = 3f + 1$, a protocol waits for $n - f = 2f + 1$ replies, since $f$ replicas may never answer. Two sets of $2f + 1$ replicas share at least $2(2f + 1) - (3f + 1) = f + 1$ replicas, so they share at least one correct replica. That correct replica does not vote for two conflicting values, so two conflicting values cannot both get a quorum. This intersection argument is the core of the safety proofs of PBFT, [HotStuff](/hotstuff/) and [Tendermint](/tendermint/). It is studied in general as a [Byzantine quorum system](/byzantine-quorum-system/), and a [quorum certificate](/quorum-certificate/) is the signed proof that a quorum voted.

**Separating agreement from execution.** Yin et al. (2003) split the replicas into two groups: $3f + 1$ replicas agree on the order of requests, and only $2f + 1$ replicas execute them and vote on the outputs. Execution is often the expensive part, so this saves work and shows that the two bounds belong to two different tasks.

**Safety and liveness.** Under partial synchrony, BFT protocols keep safety (correct replicas never commit conflicting requests) at all times, and keep liveness (requests are eventually committed) only after the network becomes timely. The [FLP impossibility](/flp-impossibility/) shows that a deterministic protocol cannot have both in a fully asynchronous network. Randomized protocols, such as [HoneyBadgerBFT](/honeybadger-bft/), keep both with probability 1 in an asynchronous network.

**Map of the protocols.**

| Setting | Bound | Protocols |
| --- | --- | --- |
| Synchronous, no signatures | $n > 3f$ | [OM(m)](/oral-messages-algorithm/), [phase king](/phase-king-algorithm/), [phase queen](/phase-queen-algorithm/) ($n > 4f$) |
| Synchronous, signatures | broadcast for $f < n$, consensus for $n > 2f$ | [SM(m)](/signed-messages-algorithm/), [Dolev-Strong](/dolev-strong-algorithm/) |
| Synchronous, randomized | $n > 3f$ | [Feldman and Micali](/feldman-micali-byzantine-agreement/) |
| Asynchronous broadcast | $n > 3f$ | [Bracha reliable broadcast](/bracha-reliable-broadcast/), [Byzantine reliable broadcast](/byzantine-reliable-broadcast/) |
| Asynchronous, randomized agreement | $n > 3f$ | [Bracha agreement](/bracha-asynchronous-agreement/), [Rabin](/rabin-randomized-byzantine-agreement/), [HoneyBadgerBFT](/honeybadger-bft/) |
| Partially synchronous replication | $n > 3f$ | [PBFT](/pbft/), [Zyzzyva](/zyzzyva/), [HotStuff](/hotstuff/), [Tendermint](/tendermint/) |
| Open membership | majority of computing power or stake | [Nakamoto consensus](/nakamoto-consensus/), [proof of stake](/proof-of-stake/) |

The page [Byzantine state machine replication](/byzantine-state-machine-replication/) gives the replication protocols in more detail. The [round](/byzantine-round-lower-bound/) and [message](/dolev-reischuk-lower-bound/) lower bounds limit all deterministic protocols in the first two rows.

## Examples

**Four replicas, one fault.** Let $n = 4$ and $f = 1$. A quorum is 3 replicas. Two quorums, for example $\{1, 2, 3\}$ and $\{2, 3, 4\}$, share 2 replicas, and at most one of them is faulty. So if replica 4 is faulty and votes for $x$ in one quorum and for $y$ in the other, the shared correct replicas 2 and 3 still vote for only one of $x$ and $y$, and only one value can be committed. A client waits for $f + 1 = 2$ equal replies, since at least one of them then comes from a correct replica.

**Three replicas are not enough without synchrony.** Let $n = 3$ and $f = 1$. A protocol can wait for only $n - f = 2$ replies. The quorums $\{1, 3\}$ and $\{2, 3\}$ share only replica 3, and if replica 3 is faulty it can vote for $x$ with replica 1 and for $y$ with replica 2. Replicas 1 and 2 cannot tell this run from a run in which the other one is faulty and slow. This is the idea of the [resilience bound](/byzantine-resilience-bound/).

**Output voting.** Three deterministic replicas run the same ordered requests, and one is faulty. For a request with correct output 42, the client gets 42, 42 and 17. The majority output is 42. If the client waits for only one reply, it may get 17. If it waits for two equal replies, it gets 42.

## Where it is used

- **Aircraft and space systems.** The Byzantine generals problem came from the SIFT flight control computer project, where redundant processors had to agree on sensor values. Flight control systems still use redundant computers with voting.
- **Replicated services.** PBFT showed in 1999 that a BFT file system could run with a small overhead over an unreplicated one. Later protocols such as Zyzzyva and HotStuff reduce the cost in the common case or when the leader changes.
- **Blockchains with known validators.** Tendermint and protocols based on HotStuff order transactions among a fixed set of validators, with $3f + 1$ validators, or with weights such that faulty validators hold less than one third of the stake.
- **Open blockchains.** Bitcoin uses [proof of work](/proof-of-work/) instead of a known set of replicas. It tolerates an adversary with less than half of the computing power, but it gives only probabilistic finality and assumes a bound on message delay.
- **Clock synchronization and sensor fusion.** The same $n > 3f$ bound holds for synchronizing clocks and for [approximate agreement](/approximate-agreement/) on real values.

## References
