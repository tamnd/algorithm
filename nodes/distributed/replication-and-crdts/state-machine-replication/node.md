---
tag: QVEPRQ
kind: problem
slug: state-machine-replication
name: State machine replication
aliases:
- replicated state machine
- RSM
area: distributed/replication-and-crdts
level: core
summary: Make a deterministic service tolerate faults by running replicas that apply the same commands in the same order, so clients see one correct copy of the service.
prereqs: [total-order-broadcast, consensus-problem, linearizability, crash-failure]
see_also: [replicated-state-machine, replicated-log, active-replication, primary-backup-replication, chain-replication, multi-paxos, raft, byzantine-state-machine-replication]
sources:
  - paper: doi:10.1145/98163.98167
    title: Fred B. Schneider, Implementing fault-tolerant services using the state machine approach, a tutorial, ACM Computing Surveys 22(4), 299-319, 1990
    locator: Section 2 (state machines, determinism) and Section 3 (fault tolerance, Agreement and Order, t + 1 and 2t + 1 replicas)
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 558-565, 1978
    locator: the section on the total ordering of events, with a state machine at each process
  - paper: doi:10.1145/78969.78972
    title: Maurice P. Herlihy and Jeannette M. Wing, Linearizability, a correctness condition for concurrent objects, ACM Transactions on Programming Languages and Systems 12(3), 463-492, 1990
    locator: the definition of linearizable histories, used here as the correctness condition
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 288-323, 1988
    locator: the resilience bounds n ≥ 2t + 1 for crash faults and n ≥ 3t + 1 for Byzantine faults under partial synchrony
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 6 (total-order broadcast, the replicated state machine, and its relation to consensus)
---

State machine replication is the problem of making a service fault tolerant by running it on $n$ servers, the replicas, so that the clients see one correct copy of the service while up to $f$ replicas fail. The standard solution, due to Lamport (1978) and set out by Schneider (1990), models the service as a deterministic state machine and has every replica apply the same commands in the same order. A replica that starts in the same state and applies the same command sequence then reaches the same state; this page proves that theorem and states how many replicas each fault model needs. The agreement on the order is a [consensus problem](/consensus-problem/), which the page [replicated state machine](/replicated-state-machine/) treats from the consensus side, and the data structure that holds the order is the [replicated log](/replicated-log/).

## In plain words

A bank keeps its accounts on one computer. If that computer stops, the bank stops. So the bank runs the same program on several computers and wants them to act as one.

The program must be predictable: the same request on the same data always gives the same result. Then it is enough to give every computer the same requests in the same order. Each computer reaches the same balances, and any working computer can answer.

Two things make this hard. The computers must agree on one order of the requests, even when messages are slow or some computers stop. And there must be enough computers left to answer. If computers can only stop, one survivor is enough to give a right answer. If computers can lie, a majority of honest ones must outvote the liars.

## Definition

**The service.** A deterministic state machine is $M = (S, s_0, C, O, \delta, \omega)$: states $S$, a start state $s_0 \in S$, commands $C$, outputs $O$, a transition function $\delta: S \times C \to S$ and an output function $\omega: S \times C \to O$. For a sequence $\sigma = c_1 \cdots c_k$ let $\delta^*(s, \sigma)$ be the state after applying $c_1, \ldots, c_k$ in order, with $\delta^*(s, \varepsilon) = s$.

**The input and the output.** Clients invoke commands $c \in C$ and wait for an output. The replicated service is a set of $n$ processes that communicate by messages. A run produces a history: the invocations and the responses, each with its time.

**The requirement.** In every run in which at most $f$ replicas fail (in the fault model of the problem: [crash](/crash-failure/) or [Byzantine](/byzantine-failure-model/)):

- **Safety.** The history is [linearizable](/linearizability/) with respect to $M$: there is a sequence $c_1, c_2, \ldots$ of the invoked commands (each at most once) that respects the real-time order of non-overlapping commands, and the response to $c_k$ is $o_k = \omega(s_{k-1}, c_k)$ with $s_k = \delta^*(s_0, c_1 \cdots c_k)$.
- **Liveness.** Each command of a correct client gets a response. In the [asynchronous model](/asynchronous-model/) this can hold only under extra assumptions, such as [partial synchrony](/partial-synchrony/) or a [failure detector](/failure-detector/).

**The approach.** Schneider splits a solution into two requirements on the replicas: **Agreement** (every correct replica receives every command) and **Order** (every correct replica processes the commands it receives in the same relative order). The theorem below shows why the two are enough for equal states.

**Theorem (same sequence, same state).** Let $M$ be deterministic, and let replicas $p$ and $q$ start in $s_0$. If $p$ has applied the sequence $\sigma$ and $q$ has applied the sequence $\tau$, and $\tau$ is a prefix of $\sigma$, then the state of $q$ is a state that $p$ passed through, and if $\sigma = \tau$, then $p$ and $q$ are in the same state and sent the same outputs.

*Proof.* Write $\sigma = c_1 \cdots c_m$ and let $p_k$ be the state of $p$ after its $k$-th command. We show $p_k = \delta^*(s_0, c_1 \cdots c_k)$ by induction on $k$. For $k = 0$, $p_0 = s_0 = \delta^*(s_0, \varepsilon)$. If $p_{k-1} = \delta^*(s_0, c_1 \cdots c_{k-1})$, then $p$ applies $c_k$ to $p_{k-1}$, and because $M$ is deterministic its new state is $\delta(p_{k-1}, c_k) = \delta^*(s_0, c_1 \cdots c_k)$ and its output is $\omega(p_{k-1}, c_k)$. The right sides depend only on $s_0$, $M$ and the first $k$ commands. The same induction for $q$ on $\tau = c_1 \cdots c_j$ with $j \le m$ gives $q_j = \delta^*(s_0, c_1 \cdots c_j) = p_j$, and equal outputs at each step. $\square$

The hypothesis of determinism is used in every step. If $\delta$ could read a clock, a random source or the scheduling of threads, two replicas could leave $p_{k-1}$ in different states.

## Variants

- **Crash faults or Byzantine faults.** With crash faults, any reply of a replica is correct. With Byzantine faults, the client must vote on the replies.
- **Who executes.** In [active replication](/active-replication/) every replica executes every command. In [primary-backup replication](/primary-backup-replication/) (passive replication) only the primary executes, and the backups receive state updates; the Order requirement then applies to the updates. [Chain replication](/chain-replication/) orders the updates along a chain of servers.
- **Reads.** A read can be a command in the order, or it can go to a replica with a lease, or to the tail of a chain. Each choice must keep linearizability.
- **Commutative commands.** If two commands commute, $\delta^*(s, ab) = \delta^*(s, ba)$, and their relative order does not matter. Generalized consensus orders only the conflicting commands.
- **Weaker goals.** If the service gives up linearizability, the replicas can accept commands in different orders and reconcile later, as in [multi-master replication](/multi-master-replication/) and with [CRDTs](/crdt/). That is not state machine replication.

## Examples

**Order matters.** The state is an integer $x$, $s_0 = 1$, and the commands are $a$: $x \leftarrow x + 1$ and $b$: $x \leftarrow 2x$. A replica that applies $ab$ ends at 4, and one that applies $ba$ ends at 3. Both received the same commands, so Agreement holds, but Order fails, and the replicas diverge.

**A prefix.** Replica $p$ has applied put$(x, 1)$, add$(x, 1)$, cas$(x, 2, 5)$, and replica $q$ has applied only the first two. Then $q$ holds $x = 2$, which is the state of $p$ after its second command. When $q$ applies the third command, it also reaches $x = 5$. A lagging replica is never wrong, only behind.

**Nondeterminism.** A command "set $x$ to a random number", run at each replica, gives different states. The fix is to draw the number once, before the command enters the order, and to put the drawn value into the command.

## Known algorithms

- [Active replication](/active-replication/): total-order broadcast, then every replica executes; $f + 1$ replicas for crash faults and $2f + 1$ for the Byzantine vote.
- [Primary-backup replication](/primary-backup-replication/): one primary executes and sends updates; needs a failure detector and a view change.
- [Chain replication](/chain-replication/): updates flow from head to tail, the tail answers; $f + 1$ servers tolerate $f$ fail-stop crashes, with a reliable configuration master.
- Consensus-based logs: [Multi-Paxos](/multi-paxos/), [Raft](/raft/), [Viewstamped Replication](/viewstamped-replication/) and [Zab](/zab/) fill a [replicated log](/replicated-log/) with $2f + 1$ replicas under partial synchrony.
- Byzantine protocols: [PBFT](/pbft/) and the others of [Byzantine state machine replication](/byzantine-state-machine-replication/), with $3f + 1$ replicas.

## Bounds

The replica counts depend on two separate tasks: agreeing on the order, and producing a correct output once the order is fixed. Schneider (1990, Section 3, who writes $t$ for $f$) gives the second: $f + 1$ replicas for crash (fail-stop) faults, because one survivor gives a correct output, and $2f + 1$ for Byzantine faults, because a client can then take the majority output, and the $f + 1$ correct replicas outvote the $f$ faulty ones. These counts are tight for that task: with $f$ replicas all can crash, and with $2f$ replicas the liars can tie.

Agreeing on the order is consensus, and it costs more in weaker timing models:

- In the [asynchronous model](/asynchronous-model/), no deterministic protocol solves consensus with even one crash (the [FLP impossibility](/flp-impossibility/) result), so no deterministic protocol solves state machine replication with both safety and liveness there. By the reduction below, this carries over.
- Under [partial synchrony](/partial-synchrony/), consensus with $f$ crash faults needs $n \ge 2f + 1$, and with $f$ Byzantine faults $n \ge 3f + 1$, with or without signatures (Dwork, Lynch and Stockmeyer 1988).
- In the [synchronous model](/synchronous-model/), crash-tolerant consensus works for any $f < n$, for example with [FloodSet](/floodset/) in $f + 1$ rounds, which is optimal by the [round lower bound](/consensus-round-lower-bound/).

These are cited bounds; the theorem above is the only result proved on this page.

## Reductions

- **Consensus reduces to state machine replication.** Take the machine with the state "undecided or $v$", where the command propose$(v)$ sets the state to $v$ if it is undecided and outputs the state. Each process submits propose(its input) and decides the output. All outputs equal the value of the first command in the order, which is some input. So agreement, validity and termination follow from the safety and liveness of the replicated service. The cost is one command per process.
- **State machine replication reduces to total-order broadcast.** Broadcast each command with [total-order broadcast](/total-order-broadcast/) and apply the delivered commands in order; the theorem gives equal states. This is [active replication](/active-replication/). Total-order broadcast in turn reduces to a sequence of consensus instances, one for each slot of a [replicated log](/replicated-log/).

## Applications

- Lock services, configuration stores and coordination services, built on Paxos, Raft or Zab.
- Replicated databases and storage systems, often with one replicated log for each shard of the data.
- Byzantine fault-tolerant services and blockchains, where the state machine is the ledger.
- A shared-memory analogue: Herlihy's [universal construction](/universal-construction/) makes any sequential object wait-free from consensus objects, by the same idea of agreeing on the next command.

## References
