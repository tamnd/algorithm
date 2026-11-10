---
tag: D37K98
kind: algorithm
slug: epaxos
name: Egalitarian Paxos (EPaxos)
aliases:
- EPaxos
area: distributed/consensus
level: research
summary: Leaderless replication that commits non-interfering commands in parallel.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of replicas}
  time: {best: Θ(1)}
  messages: {best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 2013
  people: [Iulian Moraru, David G. Andersen, Michael Kaminsky]
  note: Presented at SOSP 2013. Sutra (2020) found a bug in the recovery of the specification and the code.
prereqs: [paxos, replicated-state-machine, quorum]
see_also: [generalized-paxos, mencius, multi-paxos, fast-paxos, raft, total-order-broadcast]
sources:
  - paper: doi:10.1145/2517349.2517350
    title: Iulian Moraru, David G. Andersen and Michael Kaminsky, There is more consensus in egalitarian parliaments, SOSP 2013, 358-372
    locator: the commit protocol with PreAccept, Accept and Commit, the execution algorithm with strongly connected components, the explicit prepare recovery, and the optimized fast quorum of F + ⌊(F + 1)/2⌋ replicas
  - paper: doi:10.1016/j.ipl.2019.105901
    title: Pierre Sutra, On the correctness of Egalitarian Paxos, Information Processing Letters 156, 105901, 2020
    locator: the counterexample in TLA+ in which replicas disagree on dependencies after a change of ballot during recovery
  - url: https://arxiv.org/abs/2511.02743
    title: Fedor Ryabinin, Alexey Gotsman and Pierre Sutra, Making democracy work, fixing and simplifying Egalitarian Paxos, OPODIS 2025, arXiv 2511.02743
    locator: the fixed protocol and its correctness proof
  - paper: doi:10.1137/0201010
    title: Robert Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146-160, 1972
    locator: the algorithm for strongly connected components that the execution step uses
---

EPaxos (Egalitarian Paxos) is a protocol for a [replicated state machine](/replicated-state-machine/) with no designated leader. Each replica leads the commands that its own clients send. Instead of a slot in a log, each command gets a set of *dependencies*, the interfering commands it must follow, and a *sequence number*. When the replicas of a fast quorum report the same dependencies, the command commits after one round trip. Replicas then run commands in an order derived from the dependency graph, so that every replica runs interfering commands in the same order. The model is [asynchronous](/asynchronous-model/) with [crash failures](/crash-failure/), and $n = 2F + 1$ replicas tolerate $F$ crashes.

## In plain words

In most Paxos systems one server, the leader, puts every request in order. Far-away clients wait for the leader, and the leader does all the work.

In EPaxos, each server takes requests from its own clients. For each request, it asks the others: "which other requests that touch the same data do you know of?" If enough servers give the same answer, the request is settled in one round trip. If not, the server takes the union of the answers and confirms it with a majority, which costs a second round trip.

Each server then runs the requests so that each request comes after the ones it depends on. Two requests that depend on each other in a cycle are run in an agreed tie-break order. Requests on different data can run in any order.

## The problem

**Model.** $n = 2F + 1$ replicas, of which up to $F$ may crash, with [asynchronous](/asynchronous-model/) messages that can be delayed, duplicated and reordered. Two commands *interfere* when they do not commute, for example two writes to the same key.

**Goal.** As in [total order broadcast](/total-order-broadcast/), but weaker in one way: every replica commits the same attributes for each command, and runs each pair of interfering commands in the same order. Commands that do not interfere may run in different orders on different replicas, because the result is the same.

**Instances.** Replica $L$ owns instances $L.0, L.1, \ldots$. A command in instance $L.i$ has attributes $seq$ (an integer) and $deps$ (a set of instances).

## The algorithm

```pseudo id=main
COMMAND LEADER L, for a command γ from a client
L1  i ← the next instance of L; seq ← 1 + max seq of the instances that interfere with γ; deps ← those instances
L2  store (γ, seq, deps) as pre-accepted; send PreAccept(γ, seq, deps, L.i) to the other replicas

REPLICA R, on PreAccept(γ, seq, deps, L.i)
L3  seq ← max(seq, 1 + max seq of R's instances that interfere with γ); deps ← deps ∪ those instances
L4  store (γ, seq, deps) as pre-accepted; reply PreAcceptOK(seq, deps, L.i)

COMMAND LEADER L
L5  on PreAcceptOK from fast quorum - 1 replicas, all with the same seq and deps:  commit with them (fast path)
L6  else, with at least F replies:  seq ← max of all; deps ← union of all; send Accept(γ, seq, deps, L.i) to the others
L7  on AcceptOK from F replicas:  commit
L8  commit:  store (γ, seq, deps) as committed; send Commit(γ, seq, deps, L.i) to all

REPLICA R
L9  on Accept:  store as accepted and reply AcceptOK; on Commit:  store as committed

EXECUTE at each replica
L10 to run instance x:  wait until x and every instance reachable from x through deps is committed
L11 compute the strongly connected components of that graph, each one after the components it reaches (Tarjan)
L12 for each component in that order:  run its commands not yet run, by increasing seq, ties by instance id
```

**PreAccept** (lines L1 to L4). Each replica adds the interfering commands it knows to $deps$ and raises $seq$ above theirs. A replica that has seen another interfering command reports it, so the leader learns about every interfering command that a quorum knows.

**Fast path** (line L5). The fast quorum has $F + \lfloor (F+1)/2 \rfloor$ replicas, the leader included, in the optimized form of the protocol. If all of them agree on the attributes, they are final. With $F = 1$ ($n = 3$) the fast quorum is the leader and one other replica, so the fast path always works. With $F = 2$ ($n = 5$) it is three replicas, a majority.

**Slow path** (lines L6 and L7). When replies differ, the leader takes the union of the dependencies and the largest sequence number, and runs a Paxos accept phase with a majority, as in phase 2 of [Paxos](/paxos/).

**Execution** (lines L10 to L12). The committed dependencies form a directed graph, which can have cycles: two interfering commands sent at the same time can each see the other. The strongly connected components put the cycles together. Components run in reverse topological order, so dependencies come first, and the commands inside a component run by $seq$, with the instance id to break ties.

**Recovery.** When the leader of an instance fails, another replica takes over the instance with a higher ballot, using an *explicit prepare*: it asks a majority what they know about the instance and, from that, commits a value or a no-op. The rules for recovering a command that may have committed on the fast path are subtle. Sutra (2020) found a run in the TLA+ specification and the code of the paper in which replicas disagree on dependencies after a change of ballot, so that they can diverge. The code on this page does not include recovery.

## Example

$n = 5$, $F = 2$, fast quorum 3. Replica $R_1$ leads $a$ (write $x$) and $R_2$ leads $b$ (write $x$) at the same time. Command $c$ (write $y$) comes from $R_3$.

| step | event | attributes |
|---|---|---|
| 1 | $R_1$: $a$ in $R_1.0$, no interfering command known | $seq = 1$, $deps = \{\}$ |
| 2 | $R_2$: $b$ in $R_2.0$, no interfering command known | $seq = 1$, $deps = \{\}$ |
| 3 | $R_3$ gets PreAccept($a$) first, then PreAccept($b$) | replies $a$: (1, {}); $b$: (2, {R1.0}) |
| 4 | $R_4$ gets PreAccept($b$) first, then PreAccept($a$) | replies $b$: (1, {}); $a$: (2, {R2.0}) |
| 5 | $R_1$ has replies from $R_3$ (1, {}) and $R_4$ (2, {R2.0}): they differ | slow path: $a$ gets (2, {R2.0}) |
| 6 | $R_2$ has replies from $R_3$ (2, {R1.0}) and $R_5$ (1, {}): they differ | slow path: $b$ gets (2, {R1.0}) |
| 7 | both commit after the Accept round | $a \to b$ and $b \to a$: one component |
| 8 | $R_3$ leads $c$; no replica knows a command on $y$ | fast path: $c$ commits with (1, {}) |
| 9 | every replica runs the component $\{a, b\}$ by $(seq, id)$: $a$ ($R_1.0$) then $b$ ($R_2.0$); $c$ runs whenever it is ready | |

The two writes to $x$ formed a cycle, but every replica breaks it in the same way, because the committed attributes are the same everywhere. Command $c$ never waits for $a$ or $b$.

## Correctness

Assume that each instance keeps its first leader (no recovery).

- **Agreement on attributes.** Only the leader of $L.i$ commits it, once, and the Commit message carries the attributes.
- **Interfering commands see each other.** If $\gamma$ and $\delta$ interfere and both commit, then $\gamma \in deps(\delta)$ or $\delta \in deps(\gamma)$. Both commit after a quorum pre-accepted them: a fast quorum or a majority, and a fast quorum has at least $F + 1$ replicas. Two such quorums share a replica $R$. Whichever command reached $R$ second has the other one in the deps that $R$ reported, and the committed deps contain that report.
- **Same order.** The graph reachable from a command depends only on committed attributes, so it is the same at all replicas. If $\gamma \in deps(\delta)$, then $\gamma$'s component comes no later than $\delta$'s, and inside one component the order by $(seq, id)$ is the same everywhere.

The full proof is below.

**Liveness.** A leader needs a majority of live replicas, and with recovery, every instance of a failed leader is eventually taken over. Execution can wait for a long chain of dependencies under constant conflicts. The paper bounds this in practice; the tests do not cover it.

## Complexity

- **Fast path.** One round trip: two message delays from the leader to the commit, with $2(n - 1)$ messages, plus $n - 1$ Commit messages.
- **Slow path.** Two round trips: four message delays, with $4(n - 1)$ messages plus the commits.
- **Load.** Each replica leads its own commands, so the load is spread evenly, and a client is served by the nearest replica.
- **Dependencies.** A command lists the interfering instances a replica knows. Real systems keep only the latest interfering instance per key, which is enough because dependencies are transitive.
- **Execution.** Tarjan's algorithm is linear in the size of the graph it visits.

## Properties

- **No designated leader.** No single replica is a bottleneck, and the failure of one replica affects only its own pending instances.
- **Optimal commit latency in the common case.** One round trip to the closest fast quorum when commands do not interfere.
- **Fast quorum.** $F + \lfloor (F+1)/2 \rfloor$ replicas with the leader, smaller than the $\lceil 3n/4 \rceil$ of [Fast Paxos](/fast-paxos/) for $n \ge 7$. The basic form of the protocol uses $2F$.
- **Partial order.** Only interfering commands are ordered, as in [Generalized Paxos](/generalized-paxos/).

## Variants and improvements

- **Basic and optimized EPaxos.** The paper presents a basic protocol with fast quorums of $2F$ replicas, and an optimized one with $F + \lfloor (F+1)/2 \rfloor$, at the cost of a more complex recovery.
- **The fix of the recovery.** Ryabinin, Gotsman and Sutra (OPODIS 2025) give a corrected and simpler protocol with a proof.
- **[Mencius](/mencius/).** Also spreads leadership over all replicas, but with a fixed, rotating assignment of log slots.
- **[Multi-Paxos](/multi-paxos/).** One leader orders all commands, with two delays from the leader but a detour for remote clients.

## When to use it

Use EPaxos in a wide-area system where clients sit near different replicas and most commands do not interfere, for example key-value stores with spread-out keys. It is a poor choice when nearly all commands interfere: most commands then take the slow path, and execution waits for large components. Its recovery is subtle enough that a published version was wrong, so use a checked version.

## Pitfalls

- **Committing with the leader's attributes.** Line L5 must commit the attributes of the replies, which may add dependencies. The tests show that committing the leader's first attributes loses the dependency between interfering commands.
- **Running commands in commit order.** Line L12 must follow the dependency graph. The tests show that running each command as soon as it commits makes replicas run interfering commands in different orders.
- **Running before dependencies commit.** Line L10 must wait for every reachable instance. A replica that runs early cannot know whether a pending dependency joins the same cycle.
- **Answering a duplicate PreAccept with new attributes.** Line L4 stores the reply. A replica that computes new attributes for a duplicate can make the leader see disagreement, or, worse, agreement on attributes it did not store.
- **Recovery.** Taking over an instance must follow a checked protocol. Sutra's counterexample shows that the published rules can lead replicas to diverge.

## Implementations

## History

Moraru, Andersen and Kaminsky presented EPaxos at SOSP 2013. Sutra showed in 2020, with a TLA+ counterexample, that the specification and the code have a bug in the way replicas change ballot during recovery. Ryabinin, Gotsman and Sutra later gave a fixed and simpler protocol with a proof.

## References
