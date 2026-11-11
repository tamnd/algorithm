---
tag: 9FZTP1
kind: algorithm
slug: active-replication
name: Active replication
aliases:
- active replication
area: distributed/replication-and-crdts
level: core
summary: Every replica executes every command in the order fixed by total-order broadcast, so a crash or a lie of a minority is masked with no failover step.
solves: [state-machine-replication]
model: asynchronous-model
complexity:
  vars: {n: the number of replicas}
  messages: {worst: Θ(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1978
  people: [Leslie Lamport, Fred B. Schneider]
  note: Lamport (1978) ran one state machine at each process on commands in a total order. Schneider (1990) named the approach and gave the f + 1 and 2f + 1 replica counts.
prereqs: [state-machine-replication, total-order-broadcast, crash-failure]
see_also: [primary-backup-replication, replicated-state-machine, replicated-log, chain-replication, byzantine-state-machine-replication, multi-paxos, raft]
sources:
  - paper: doi:10.1145/98163.98167
    title: Fred B. Schneider, Implementing fault-tolerant services using the state machine approach, a tutorial, ACM Computing Surveys 22(4), 299-319, 1990
    locator: Section 3 (fault tolerance, the requirements Agreement and Order, t + 1 replicas for fail-stop and 2t + 1 for Byzantine faults)
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 558-565, 1978
    locator: the section on the total ordering of events and the mutual exclusion example, where every process runs the same state machine
  - paper: doi:10.1145/1041680.1041682
    title: Xavier Défago, André Schiper and Péter Urbán, Total order broadcast and multicast algorithms, taxonomy and survey, ACM Computing Surveys 36(4), 372-421, 2004
    locator: the fixed sequencer class of algorithms, used by the simulator on this page
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 6 (total-order broadcast and the replicated state machine)
---

Active replication runs a deterministic service on $n$ replicas and has every replica execute every client command, in one order that a [total-order broadcast](/total-order-broadcast/) fixes. It is the direct form of [state machine replication](/state-machine-replication/) that Schneider (1990) describes: because all replicas compute, a client can take the first reply when replicas only [crash](/crash-failure/), or the reply of a majority when up to $f$ of $2f + 1$ replicas are Byzantine. A failure is masked inside one request, with no failure detector and no failover step, which is the main difference from [primary-backup replication](/primary-backup-replication/). The cost is that every replica does all the work, and that the service must be deterministic.

## In plain words

Several computers each run a copy of the same program. A client does not send its request to one of them. It hands the request to an ordering service, and that service gives every request a number and passes it to all copies. Each copy runs the requests strictly in number order. If request 3 arrives before request 2, the copy waits for request 2.

Every copy then computes the same answers, and every copy sends its answer to the client. If copies can only stop, the first answer is right, and the client does not care which copies have stopped. If some copies can lie, the client waits until enough copies agree on one answer.

Nothing special happens when a copy fails. There is no leader to replace and no state to move.

## The problem

The problem is [state machine replication](/state-machine-replication/). A service is a deterministic state machine with a start state $s_0$, a transition function $\delta$ and an output function $\omega$. Clients send commands. The replicated service must answer each command as one copy of the machine would, when it runs the commands in some single order, while up to $f$ of the $n$ replicas fail.

Active replication assumes a total-order broadcast primitive with the usual properties: validity, agreement, integrity (each command is delivered at most once, and only if it was broadcast) and total order. In the [asynchronous model](/asynchronous-model/) with crash failures this primitive is as hard as [consensus](/consensus-problem/), so a real system builds it with [Multi-Paxos](/multi-paxos/), [Raft](/raft/) or a similar protocol under [partial synchrony](/partial-synchrony/). This page assumes it and studies what the replicas and the clients do on top of it.

## The algorithm

The total order is shown as a sequence number $k$ on each delivered command, as a fixed sequencer gives it. Links can reorder messages, so a replica keeps a hold-back buffer. Each replica $i$ has the state $s$, starting at $s_0$, and a counter $next = 1$.

```pseudo id=main
ON-DELIVER(k, c, client)                 ▷ at replica i: command c has number k
L1  buffer[k] ← (c, client)
L2  while buffer holds the number next do
L3      (c, client) ← remove buffer[next]
L4      (s, o) ← (δ(s, c), ω(s, c))
L5      send REPLY(next, o) to client
L6      next ← next + 1

CLIENT-INVOKE(c)
L7  TO-BROADCAST(c)
L8  on REPLY(k, o): add one vote for o at number k
L9  return o when it has 1 vote (crash faults) or f + 1 votes (Byzantine faults)
```

Lines L1 to L3 turn numbered deliveries into in-order execution: a command runs only after every command with a smaller number has run. Line L4 is the only place where the state changes, and it uses only the state and the command. Line L5 sends one reply from each replica. The client in lines L8 and L9 decides how many equal replies it needs. With crash faults, every reply comes from a correct computation, so one is enough. With Byzantine faults, $f$ liars can agree on a wrong output, so the client needs $f + 1$ equal votes, and at least one of them comes from a correct replica.

## Example

Three replicas $R_0, R_1, R_2$ run a key-value store. A client sends four commands at times 0, 3, 6 and 9. The sequencer numbers them in the order it receives them:

| number | command | output in the sequential run |
|---|---|---|
| 1 | put$(x, 1)$ | ok |
| 2 | add$(x, 1)$ | 2 |
| 3 | cas$(x, 2, 5)$ | true |
| 4 | get$(x)$ | 5 |

$R_1$ crashes at time 4, before any command reaches it. Link delays are between 1 and 10 time units. The events at the two other replicas are these:

| time | event | state after it |
|---|---|---|
| 5 | $R_0$ and $R_2$ get number 1 and apply it | $x = 1$ at both |
| 13 | the client gets "ok" for number 1 from $R_0$ | |
| 15 | $R_0$ gets number 3; $next = 2$, so it holds number 3 back | $x = 1$ at $R_0$ |
| 17 | $R_0$ gets number 2, applies 2, then the held number 3 | $x = 5$ at $R_0$ |
| 21 | $R_2$ gets number 2, applies it, then gets number 3 and applies it | $x = 5$ at $R_2$ |
| 21 | the client gets "true" for number 3 from $R_0$ | |
| 22 | the client gets 2 for number 2 from $R_0$ | |
| 24 and 26 | $R_2$, then $R_0$, apply number 4 | $x = 5$ at both |
| 27 | the client gets 5 for number 4 from $R_0$ | |

The client never waits for the crash of $R_1$ to be noticed. The replies for numbers 2 and 3 arrive out of order, but each one is the output of the sequential run at that number. Both live replicas end in the state $x = 5$ after four commands.

## Correctness

**Theorem.** Assume a total-order broadcast with validity, agreement, integrity and total order, and a deterministic state machine. Let $c_1, c_2, \ldots$ be the delivery order and $s_k = \delta^*(s_0, c_1 \cdots c_k)$. Then (a) each replica that has run line L4 for $k$ commands is in state $s_k$, and the output it sent for number $k$ is $o_k = \omega(s_{k-1}, c_k)$; (b) with crash faults and at most $n - 1$ crashes, the client returns $o_k$ for each of its commands; (c) with at most $f$ Byzantine replicas among $n \ge 2f + 1$, the client returns $o_k$, and only $o_k$.

The key invariant is that line L4 runs on the commands $c_1, c_2, \ldots$ in number order with no gap and no repeat, by lines L2 and L3. Part (a) then follows by induction on $k$, as in the theorem of [state machine replication](/state-machine-replication/). For (b), a correct replica exists and replies, and every reply is $o_k$ by (a). For (c), the $n - f \ge f + 1$ correct replicas all send $o_k$, so $o_k$ reaches $f + 1$ votes, and a wrong value gets at most $f$ votes, from the liars only. The full proof is in the proof file.

## Complexity

Cost is per command, on top of one total-order broadcast.

- **Messages.** Each of the $n$ replicas sends one reply, so a command costs $\Theta(n)$ messages beyond the broadcast. The broadcast itself costs $\Theta(n)$ messages with a fixed sequencer and more with a consensus protocol; see [total-order broadcast](/total-order-broadcast/).
- **Time.** After a command is delivered at a correct replica, its reply takes one message delay. With the sequencer of the example and delays of at most $\Delta_c$, a client gets its first reply within $3\Delta_c$ of sending: one delay to the sequencer, one to the replicas (a held command waits only for commands that the sequencer sent earlier, which also arrive within $\Delta_c$), and one back. Crashes of up to $n - 1$ replicas do not change this bound.
- **Space.** Besides the state $s$, the hold-back buffer of a replica holds the commands that arrived early. With FIFO links from the sequencer it stays empty. With reordering links it holds the commands sent during one message delay, which is $O(n)$ when $n$ clients each have one outstanding command.
- **Replicas.** Crash faults need $n \ge f + 1$; Byzantine faults need $n \ge 2f + 1$ for the vote (Schneider 1990, Section 3). These counts are for the execution and the vote only. Agreeing on the order costs more: $n \ge 2f + 1$ for crash-tolerant consensus under [partial synchrony](/partial-synchrony/), and $n \ge 3f + 1$ for Byzantine agreement, see [Byzantine state machine replication](/byzantine-state-machine-replication/).

## Properties

- **Failure masking.** A crash or a lie by a minority does not change any reply and does not delay it. There is no failover step.
- **Determinism required.** Every replica must compute the same $\delta$ and $\omega$. Threads, local clocks, random numbers and the order of messages from the network must not affect the state.
- **All replicas busy.** Each replica executes each command, so the computing cost is $n$ times that of one server. Reads also go through the order, unless the system adds a separate read path.
- **Same states, not only same outputs.** By part (a), a replica that lags is in a state that the others passed through, so it can catch up by applying the missing commands.

## Variants and improvements

- **Semi-active replication.** One replica, the leader, decides the outcome of each nondeterministic choice and sends it to the followers, which then replay it. This keeps the replicas equal when the service is not fully deterministic.
- **Read optimizations.** A read can skip the total order if it goes to a replica that holds a [leader lease](/leader-lease/), at the cost of a timing assumption.
- **Commutative commands.** Commands that commute need no relative order. [Generalized Paxos](/generalized-paxos/) and [EPaxos](/epaxos/) order only the commands that conflict.
- **Byzantine replicas.** [PBFT](/pbft/) and its successors give the order among $3f + 1$ replicas, and clients wait for $f + 1$ equal replies.

## When to use it

Use active replication when a failure must not cause a pause, and when the service is deterministic and cheap enough to run $n$ times. It is the usual choice for Byzantine fault tolerance, where a client cannot trust any single replica. Use [primary-backup replication](/primary-backup-replication/) when the operations are expensive or not deterministic: there only the primary computes, and the backups receive the resulting state. Use [chain replication](/chain-replication/) for a storage service with high write throughput.

## Pitfalls

- **Hidden nondeterminism.** A command that reads the local clock, a random number or the iteration order of a hash set gives different states. Wrong: `s[k] ← now()` inside $\delta$. Right: read the clock once before TO-BROADCAST and put the value into the command.
- **Applying on arrival.** Wrong: run line L4 when a command arrives. Right: run it only when $k = next$, as lines L2 and L3 do. The example shows the case: number 3 reaches $R_0$ before number 2.
- **Trusting one reply under Byzantine faults.** Wrong: return the first reply. Right: wait for $f + 1$ equal replies, from $n \ge 2f + 1$ replicas. With $n = 2f$ the liars can tie with the correct replicas, and the client cannot decide.
- **Counting replicas for the vote only.** The $2f + 1$ bound is for the vote. The ordering protocol under it needs its own bound.

## Implementations

The Python code runs replicas, a sequencer and a client in a discrete event simulator with seeded delays and crash times. The sequencer stands in for a total-order broadcast service and does not fail.

## History

Lamport (1978) used logical clocks to order commands and had each process run the same state machine on them; he gave mutual exclusion as the example. Schneider's tutorial (1990) made the state machine approach a general method, stated the requirements Agreement and Order, and gave the replica counts $t + 1$ for fail-stop and $2t + 1$ for Byzantine faults. Défago, Schiper and Urbán (2004) survey the total-order broadcast algorithms on which active replication rests.

## References
