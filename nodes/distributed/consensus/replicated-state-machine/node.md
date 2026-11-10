---
tag: 691JBS
kind: concept
slug: replicated-state-machine
name: Replicated state machine
aliases:
- state machine replication
- SMR
area: distributed/consensus
level: core
summary: Deterministic replicas that start in the same state and apply the same agreed sequence of commands stay in the same state. A consensus protocol decides the sequence.
prereqs: [consensus-problem, total-order-broadcast, induction]
see_also: [state-machine-replication, replicated-log, paxos, multi-paxos, raft, zab, log-compaction, byzantine-state-machine-replication]
sources:
  - paper: doi:10.1145/98163.98167
    title: Fred B. Schneider, Implementing fault-tolerant services using the state machine approach, a tutorial, ACM Computing Surveys 22(4), 1990
    locator: Section 2 (state machines and determinism) and Section 3 (fault tolerance, the requirements Agreement and Order, t + 1 and 2t + 1 replicas)
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: the section on the total ordering of events, where each process runs the same state machine on commands ordered by logical clocks
  - url: https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro
    title: Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm, USENIX ATC 2014
    locator: Section 2 (replicated state machines and the replicated log)
---

A replicated state machine is a service that runs as $n$ copies of one deterministic state machine, each fed the same sequence of commands. If the copies start in the same state and apply the same commands in the same order, they pass through the same states and give the same outputs, so the service keeps working while some copies fail. The hard part is the agreement on the sequence, and this is a [consensus problem](/consensus-problem/) for each position, or one instance of [total-order broadcast](/total-order-broadcast/). This page takes the consensus view of Schneider (1990) and the [Paxos](/paxos/) and [Raft](/raft/) papers, in which a log of decided commands drives the replicas, and the page [state machine replication](/state-machine-replication/) takes the replication view, with clients, reads and the cost of the replicas.

## In plain words

Think of a program that only changes when it gets a command, and that always does the same thing for the same command. A counter is one: "add 5" always adds 5. Run a copy of this program on several computers. Give every copy the same list of commands, in the same order. Then every copy holds the same value after each step, so any copy can answer a question, and the service keeps working when one computer stops.

Two rules matter. Every copy must get the same commands, and every copy must run them in the same order. "Add 1, then double" and "double, then add 1" give different results. Making many computers agree on one order is the hard part, and a consensus protocol does it.

## The idea

### State machines

A **state machine** is a tuple $M = (S, s_0, C, O, \delta, \omega)$: a set of states $S$, a start state $s_0 \in S$, a set of commands $C$, a set of outputs $O$, a transition function $\delta : S \times C \to S$ and an output function $\omega : S \times C \to O$. The machine is **deterministic**: its next state and its output depend only on the current state and the command. For a sequence $\sigma = c_1 c_2 \cdots c_m$ write $\delta^*(s, \sigma)$ for the state after applying $c_1$, then $c_2$, and so on, with $\delta^*(s, \varepsilon) = s$ for the empty sequence.

A **replicated state machine** has $n$ replicas of $M$. Each replica starts in $s_0$ and applies commands one at a time, in the order of a shared sequence, the [replicated log](/replicated-log/) $c_1, c_2, \ldots$. Schneider splits the coordination into two requirements:

- **Agreement:** every correct replica receives every command.
- **Order:** every correct replica applies the commands in the same order.

A consensus protocol run once for each log index gives both: the decision at index $i$ is $c_i$, and every replica applies index $i$ only after index $i-1$.

### Same commands, same states

**Proposition.** Let $\sigma = c_1 c_2 \cdots$ be the agreed sequence. If replica $r$ has applied the first $i$ commands, then its state is $s_i = \delta^*(s_0, c_1 \cdots c_i)$ and the outputs it has sent are $o_k = \omega(s_{k-1}, c_k)$ for $k = 1, \ldots, i$. So any two replicas that have applied the same number of commands are in the same state, and a replica that has applied fewer commands is in a state that the other one passed through.

*Proof.* By [induction](/induction/) on $i$. For $i = 0$, the replica has applied nothing and is in the start state $s_0 = \delta^*(s_0, \varepsilon)$. Assume the claim for $i$, so the replica is in state $s_i$. The next command it applies is $c_{i+1}$, by the Order requirement. Since $M$ is deterministic, the new state is $\delta(s_i, c_{i+1}) = \delta^*(s_0, c_1 \cdots c_{i+1}) = s_{i+1}$, and the output is $\omega(s_i, c_{i+1}) = o_{i+1}$. The right-hand sides depend only on $s_0$, $M$ and $\sigma$, not on the replica. $\square$

The proof uses determinism in each step. If $\delta$ could read a clock, a random number or the order of two threads, the step from $s_i$ to $s_{i+1}$ could differ between replicas, and the induction would fail.

### How many replicas

The number of replicas depends on the failure model and on what the replicas must do themselves.

- With crash failures, the output of any replica is correct, so $t + 1$ replicas tolerate $t$ crashes once the sequence is agreed (Schneider). To agree on the sequence in the [asynchronous model](/asynchronous-model/), Paxos and Raft need $n \ge 2t + 1$, so that two majorities share a replica.
- With Byzantine failures, a client takes the output that a majority of replicas send, so $2t + 1$ replicas are enough to vote once the sequence is agreed (Schneider). Agreeing on the sequence among Byzantine replicas needs more: protocols such as [PBFT](/pbft/) use $n \ge 3t + 1$. See [Byzantine state machine replication](/byzantine-state-machine-replication/).

## Examples

**One register, two orders.** The state is an integer $x$ with $s_0 = 1$. The commands are $a$: $x \leftarrow x + 1$ and $b$: $x \leftarrow 2x$. A replica that applies $a$ then $b$ ends with $(1 + 1) \cdot 2 = 4$. A replica that applies $b$ then $a$ ends with $1 \cdot 2 + 1 = 3$. Both replicas got the same commands (Agreement holds), but not in the same order, and they diverge. This is a non-example: without Order, determinism alone does not help.

**Commuting commands.** If the commands are $a$: $x \leftarrow x + 1$ and $d$: $y \leftarrow y + 1$, on two different variables, both orders give the same state. Only commands that do not commute must be ordered. [Generalized Paxos](/generalized-paxos/) and [EPaxos](/epaxos/) use this to skip the ordering of commuting commands.

**A key-value store.** The state is a map from keys to values. The commands are put$(k, v)$, get$(k)$ and compare-and-set$(k, v_{\mathrm{old}}, v_{\mathrm{new}})$. Every replica applies log entry 1, then 2, and so on. A client sends a command to the leader of a [Raft](/raft/) or [Multi-Paxos](/multi-paxos/) group. The leader puts it in the next log index, and once that index is decided and applied, the leader returns the output. All replicas hold the same map after each index.

**Nondeterminism moved into the log.** A command "set $k$ to the current time" is not deterministic. The fix is to read the clock once, at the leader, before the command enters the log, and to log "set $k$ to 1700000000". Each replica then applies the same value.

## Where it is used

- **Consensus protocols.** [Multi-Paxos](/multi-paxos/), [Raft](/raft/), [Viewstamped Replication](/viewstamped-replication/) and [Zab](/zab/) all keep a replicated log for a state machine. The protocol decides the log, and the state machine is the application.
- **Coordination services.** Lock and configuration services such as Chubby, ZooKeeper and etcd are replicated state machines over Paxos, Zab and Raft.
- **Databases.** Replicated databases apply the same log of writes on each replica, often one Raft or Paxos group for each shard of the data.
- **Byzantine fault tolerance.** [PBFT](/pbft/), [Tendermint](/tendermint/) and [HotStuff](/hotstuff/) order commands among replicas that may lie, and the replicas then run the same state machine.
- **Bounded logs.** A real log cannot grow forever. A replica saves a snapshot of the state $s_i$ and drops the log up to $i$, which is safe by the proposition above. See [log compaction](/log-compaction/).
- **Linearizable objects.** A replicated state machine in which each command takes effect when its log index is applied gives a [linearizable](/linearizability/) object. Herlihy's [universal construction](/universal-construction/) is the shared-memory form of the same idea.

## References
