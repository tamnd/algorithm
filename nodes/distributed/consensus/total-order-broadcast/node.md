---
tag: 1XEK7N
kind: problem
slug: total-order-broadcast
name: Total-order broadcast
aliases:
- atomic broadcast
area: distributed/consensus
level: core
summary: Every correct process delivers the same messages in the same order. In the asynchronous model with crash failures, this problem is equivalent to consensus.
prereqs: [consensus-problem, asynchronous-model, crash-failure, total-order]
see_also: [replicated-state-machine, replicated-log, causal-broadcast, fifo-broadcast, flp-impossibility, chandra-toueg-consensus, raft, zab]
sources:
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: the section on atomic broadcast, with the reduction of atomic broadcast to consensus and of consensus to atomic broadcast
  - paper: "Vassos Hadzilacos and Sam Toueg, A modular approach to fault-tolerant broadcasts and related problems, Technical Report TR 94-1425, Cornell University, 1994"
    locator: the definitions of reliable, FIFO, causal and atomic broadcast, in uniform and non-uniform forms
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 6 (total-order broadcast, the consensus-based algorithm and its uniform form)
  - paper: "Xavier Défago, André Schiper and Péter Urbán, Total order broadcast and multicast algorithms: taxonomy and survey, ACM Computing Surveys 36(4), 2004"
    locator: the five classes of algorithms (fixed sequencer, moving sequencer, privilege-based, communication history, destination agreement)
---

Total-order broadcast, also called atomic broadcast, is the problem of sending messages to a group of $n$ processes so that every correct process delivers the same messages, each at most once, in the same order. It is the core of the [replicated state machine](/replicated-state-machine/): if every replica applies the delivered messages as commands, every replica goes through the same states. In the [asynchronous model](/asynchronous-model/) with [crash failures](/crash-failure/), total-order broadcast and the [consensus problem](/consensus-problem/) can each be built from the other (Chandra and Toueg, 1996). So total-order broadcast has no deterministic solution there with even one crash, by the [FLP impossibility](/flp-impossibility/) result.

## In plain words

A group of computers send messages to the whole group. Each computer passes the messages it gets, one at a time, to its program. The goal is that every computer that keeps working hands over the same messages in the same order, with no message twice and no made-up message.

Plain sending is not enough. Messages travel at different speeds, so one computer can get "pay Alice" first while another gets "close the account" first. A sender can also stop after it has reached only half of the group.

One fix runs a vote again and again. In each vote, the computers agree on the next batch of messages. Every computer then hands over that batch in the same fixed order. The opposite also works: with a total-order service, a group can agree on one value by taking the first message that arrives.

## Definition

There are $n$ processes $p_1, \ldots, p_n$. Each pair is joined by a reliable channel: a message sent between two correct processes arrives once, after a finite but unbounded delay, and channels do not invent messages. Up to $f$ processes can crash. A process that does not crash is **correct**. A process calls TO-BROADCAST$(m)$ to send $m$, and the service calls TO-DELIVER$(m)$ to hand $m$ to the process. Each message is unique, for example by the sender's id and a counter.

A protocol solves total-order broadcast if every run has these four properties:

- **Validity.** If a correct process broadcasts $m$, it eventually delivers $m$.
- **Agreement.** If a correct process delivers $m$, every correct process eventually delivers $m$.
- **Integrity.** Each process delivers each message at most once, and only if some process broadcast it.
- **Total order.** If processes $p$ and $q$ both deliver $m$ and $m'$, then $p$ delivers $m$ before $m'$ if and only if $q$ delivers $m$ before $m'$.

The first three properties define reliable broadcast. Validity and agreement are liveness properties, and integrity and total order are safety properties.

The **uniform** form replaces "a correct process" in agreement with "any process": a process that delivers $m$ and then crashes still forces every correct process to deliver $m$. A replicated database needs the uniform form, because a replica can answer a client and then crash. A still stronger form is the **prefix property**: the sequence that each process delivers is a prefix of the sequence that each correct process delivers. The four properties do not imply it: a correct process can deliver $x$ then $m$, while a faulty process delivers only $m$ and crashes.

## Variants

- **Uniform and non-uniform.** As above. The non-uniform form allows a faulty process to deliver a message that the correct processes never deliver.
- **FIFO total order.** Total order plus [FIFO order](/fifo-broadcast/): the messages of one sender are delivered in the order it sent them. The algorithm below does not give this by itself, because two messages of one sender can be decided in different batches.
- **Causal total order.** Total order plus [causal order](/causal-broadcast/). [Zab](/zab/) gives a form tied to one leader at a time, called primary order.
- **Total-order multicast.** Each message goes to a subset of the processes, and the order must agree on the messages that two processes have in common.
- **Byzantine total-order broadcast.** Some processes can lie. This is [Byzantine state machine replication](/byzantine-state-machine-replication/), solved by protocols such as [PBFT](/pbft/) when $n \ge 3f + 1$.

## Examples

Three processes $p_0$, $p_1$, $p_2$ each broadcast one message, $m_0$, $m_1$ and $m_2$, with the algorithm of the next section. Process $p_2$ crashes after three sends, so its broadcast of $m_2$ reaches all three processes, but it crashes while it relays the other messages.

| instance | decided batch | delivered by $p_0$ and $p_1$ | delivered by $p_2$ |
|---|---|---|---|
| 1 | $\{m_2\}$ | $m_2$ | $m_2$, then it crashes |
| 2 | $\{m_0, m_1\}$ | $m_0$, then $m_1$ | none |

Both correct processes deliver $m_2, m_0, m_1$. The sequence of the faulty $p_2$ is $m_2$, which is a prefix. The message $m_2$ is delivered although its sender crashed, because it reached the others before the crash. In another run, $p_2$ crashes before its first send reaches anyone, and no process delivers $m_2$: validity asks nothing for a faulty sender. The batch of instance 2 is delivered in sorted order, which every process computes the same way.

A non-example is reliable broadcast that delivers each message as it arrives. With the same three messages, $p_0$ can receive $m_0$ first and $p_1$ can receive $m_1$ first. Both runs satisfy validity, agreement and integrity, but not total order.

## Known algorithms

**From consensus (Chandra and Toueg).** Each process passes messages to an eager reliable broadcast, R-BROADCAST and R-DELIVER, in which each process relays a message to all before it delivers it. This makes the reliable broadcast uniform. The processes then runs consensus instances $1, 2, 3, \ldots$ in turn. Here PROPOSE$(k, \cdot)$ and DECIDE$(k, \cdot)$ belong to instance $k$ of any consensus algorithm.

```pseudo id=main
TOTAL-ORDER BROADCAST FROM CONSENSUS, at process p          ▷ pending, delivered ← ∅; k ← 0
L1  upon TO-BROADCAST(m): R-BROADCAST(m)
L2  upon R-DELIVER(m): if m ∉ delivered then pending ← pending ∪ {m}
L3  upon pending ≠ ∅ and not waiting:
L4      k ← k + 1; waiting ← true
L5      PROPOSE(k, pending)
L6  upon DECIDE(k, M):
L7      for each m ∈ M \ delivered, in a fixed order (for example sorted by id): TO-DELIVER(m)
L8      delivered ← delivered ∪ M; pending ← pending \ M; waiting ← false

CONSENSUS FROM TOTAL-ORDER BROADCAST, at process p
L9  upon PROPOSE(v): TO-BROADCAST((p, v))
L10 upon TO-DELIVER((q, v)): if p has not decided then DECIDE(v)
```

With a consensus algorithm such as [Chandra and Toueg's](/chandra-toueg-consensus/), which uses an eventually strong failure detector and $f < n/2$, the first part gives total-order broadcast in an asynchronous system.

**Other classes.** The survey of Défago, Schiper and Urbán sorts the algorithms into five classes.

- *Fixed sequencer.* One process gives each message a number. [Raft](/raft/), [Multi-Paxos](/multi-paxos/), [Zab](/zab/) and [Viewstamped Replication](/viewstamped-replication/) are of this kind, with a new sequencer elected after a crash.
- *Moving sequencer.* The role passes around the processes.
- *Privilege-based.* A token moves around a ring, and only its holder broadcasts.
- *Communication history.* Each message carries a [Lamport timestamp](/lamport-clocks/), and a process delivers a message once it knows that no message with a smaller timestamp can still arrive. This needs every process to keep sending, and it does not tolerate crashes by itself.
- *Destination agreement.* The receivers agree on the order, as in the consensus-based algorithm above.

## Bounds

- **Impossibility.** In the asynchronous model, no deterministic algorithm solves total-order broadcast if one process can crash. Consensus reduces to it (next section), and consensus has no such algorithm (Fischer, Lynch and Paterson). This is cited, not proved here.
- **Failure detectors.** With a failure detector of class $\Diamond\mathcal{S}$ (equivalently [Ω](/omega-failure-detector/)) and $f < n/2$, total-order broadcast is solvable, through consensus. Ω is the [weakest failure detector](/weakest-failure-detector-consensus/) for consensus with a majority of correct processes, and by the reductions it is also the weakest for total-order broadcast.
- **Synchrony.** With [partial synchrony](/partial-synchrony/) and $f < n/2$ crash failures, the leader-based protocols above work.
- **Consensus number.** An object that gives total-order broadcast solves consensus for any number of processes, so its [consensus number](/consensus-number/) is infinite.

## Reductions

Both reductions are for the asynchronous model with crash failures and reliable channels, with any number $f < n$ of crashes. The consensus used has these properties: termination (if every correct process proposes, every correct process decides), validity (a decided value was proposed), integrity (each process decides at most once) and uniform agreement (no two processes decide differently).

### Total-order broadcast from consensus

**Theorem.** Lines L1 to L8 solve uniform total-order broadcast with the prefix property, given uniform reliable broadcast and a sequence of consensus instances.

*Proof.* Write $M_k$ for the decision of instance $k$. By uniform agreement, it is the same at each process that decides in instance $k$.

1. *Each process delivers $D_1, D_2, \ldots$ in this order, where $D_k$ is the list of $M_k \setminus (M_1 \cup \cdots \cup M_{k-1})$ in the fixed order.* A process runs the instances one after the other: line L3 starts instance $k+1$ only after line L8 ends instance $k$. By induction on $k$, after instance $k$ the set delivered equals $M_1 \cup \cdots \cup M_k$, so line L7 in instance $k+1$ delivers exactly $D_{k+1}$, in the fixed order.
2. *Total order and integrity.* By 1, the delivered sequence of each process is a prefix of the one sequence $D_1 D_2 \cdots$, which has no repeated message. So two processes deliver common messages in the same order, and no process delivers a message twice. Each message in $M_k$ was in a proposal (consensus validity), each proposal holds only R-delivered messages (line L2), and reliable broadcast delivers only broadcast messages.
3. *Agreement.* Let some process deliver $m$, in instance $k$. Then $m$ was in a proposal, so some process R-delivered $m$, and by uniform reliable broadcast every correct process R-delivers $m$. Assume that a correct process $q$ never delivers $m$. Then $m$ stays in pending at $q$ from some time on, so $q$ proposes in each instance, and by termination it decides in each instance it proposes in. So $q$ completes instance $k$ and delivers $D_k$, which holds $m$ or comes after a $D_j$ with $j < k$ that holds $m$. This contradicts the assumption.
4. *Validity.* Let a correct process $p$ broadcast $m$, and assume that no process ever delivers $m$. Every correct process R-delivers $m$, and from then on $m$ is in its pending set at each instance it starts. So every correct process proposes in every instance, and by termination they all go through all instances. Each faulty process crashes, so it proposes in only finitely many instances. For $k$ larger than all of these, all proposals of instance $k$ come from correct processes and hold $m$, and by validity $M_k$ holds $m$. Then $p$ delivers $m$, a contradiction. If some process delivers $m$, step 3 makes $p$ deliver it.
5. *Prefix property.* Each $D_k$ is nonempty: a proposal in instance $k$ is a nonempty pending set, which line L8 keeps disjoint from $M_1 \cup \cdots \cup M_{k-1}$, and $M_k$ is one of these proposals. If a process completes instance $k$, it delivers the messages of $D_k$, and by step 3 each correct process delivers them too, which it does only in instance $k$. So each correct process completes every instance that any process completes, and by step 1 the sequence of each process is a prefix of the sequence of each correct process. $\square$

### Consensus from total-order broadcast

**Theorem.** Lines L9 and L10 solve consensus, given total-order broadcast: termination, validity, integrity, and agreement among the correct processes. If the broadcast has the prefix property, agreement is uniform.

*Proof.* *Termination.* A correct process $p$ proposes, so it broadcasts $(p, v)$, and by validity it delivers this message. So it delivers at least one message, and line L10 decides on the first. *Validity.* The first message $(q, v)$ that a process delivers was broadcast (integrity), so $q$ proposed $v$. *Integrity.* Line L10 decides once. *Agreement.* Let the correct processes $p$ and $q$ decide on their first messages $m$ and $m'$, and assume $m \ne m'$. By agreement of the broadcast, $p$ also delivers $m'$, after $m$, and $q$ also delivers $m$, after $m'$. This breaks total order. *Uniform agreement with the prefix property.* Take a correct process $c$; at least one exists, since $f < n$. The first message that any process delivers is the first message of the sequence of $c$, so all deciders decide the same value. $\square$

The algorithm of lines L1 to L8 has the prefix property, so consensus built on it has uniform agreement.

The two theorems together show that, in this model, consensus and total-order broadcast are equivalent: any algorithm for one gives an algorithm for the other, and an impossibility for one is an impossibility for the other.

## Applications

- **State machine replication.** Every replica applies the delivered messages as commands. See [replicated state machine](/replicated-state-machine/) and [replicated log](/replicated-log/).
- **Coordination services.** ZooKeeper orders all writes with [Zab](/zab/), and etcd with [Raft](/raft/).
- **Distributed databases.** A log of transactions in one total order gives one serial order of the writes on all replicas.
- **Message queues and event logs.** A totally ordered log lets each consumer rebuild the same state from the same events.
- **Blockchains.** A blockchain is a total order of transactions. [Nakamoto consensus](/nakamoto-consensus/) gives it only with high probability and with a delay, and [PBFT](/pbft/), [Tendermint](/tendermint/) and [HotStuff](/hotstuff/) give it among Byzantine replicas.

## References
