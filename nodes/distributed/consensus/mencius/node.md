---
tag: H2QGRY
kind: algorithm
slug: mencius
name: Mencius
area: distributed/consensus
level: research
summary: Rotates the leader per log slot so all replicas propose in parallel.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of servers}
  time: {best: Θ(1)}
  messages: {best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 2008
  people: [Yanhua Mao, Flavio P. Junqueira, Keith Marzullo]
  note: Presented at OSDI 2008 as a replicated state machine for wide-area networks.
prereqs: [multi-paxos, paxos, replicated-state-machine]
see_also: [multi-paxos, epaxos, generalized-paxos, cheap-paxos, failure-detector, total-order-broadcast]
sources:
  - paper: "Yanhua Mao, Flavio P. Junqueira and Keith Marzullo, Mencius: building efficient replicated state machines for WANs, 8th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2008), 369-384"
    locator: Coordinated Paxos and the skip, the four rules of Mencius, the optimizations that piggyback skips on other messages, and the wide-area evaluation
  - paper: "Leslie Lamport, Paxos made simple, ACM SIGACT News 32(4), 51-58, December 2001"
    locator: Section 3 (a sequence of Paxos instances for a state machine, and filling gaps with no-op)
---

Mencius is a form of [Multi-Paxos](/multi-paxos/) in which the role of leader rotates over the slots of the log. With $n$ servers, server $p$ is the default leader, the *coordinator*, of the instances $p, p + n, p + 2n, \ldots$. Each server puts its own clients' commands in its own instances, so all servers propose in parallel and the load is spread evenly. A server with nothing to propose fills its instances with no-op by a cheap *skip*. A server that has crashed is *revoked*: the others run a full [Paxos](/paxos/) round to fill its instances with no-op. The model is [asynchronous](/asynchronous-model/) with [crash failures](/crash-failure/), $n = 2F + 1$ servers, and a [failure detector](/failure-detector/) for liveness.

## In plain words

Picture a shared notebook with numbered lines. Three servers take turns: server 0 owns lines 0, 3, 6, server 1 owns lines 1, 4, 7, and server 2 owns lines 2, 5, 8. A server writes its clients' requests on its own lines, and a majority confirms each entry.

Every server reads the notebook from the top, line by line, so a blank line stops everyone. A server that has nothing to write must say "skip" for its lines, so the others can go past them. When a server sees that someone else wrote on a later line, it skips all its own earlier lines at once.

If a server crashes, the others agree by a vote to put "nothing" on its lines.

## The problem

**Model.** $n = 2F + 1$ servers, at most $F$ of which crash, with asynchronous messages that may be delayed, reordered and duplicated. A failure detector tells each server which servers it suspects; it can be wrong for a while.

**Goal.** As in [total order broadcast](/total-order-broadcast/): every server runs the same sequence of commands, each command at most once, and every command sent to a server that does not crash runs at every live server.

**Instances.** Instance $i$ is a [Paxos](/paxos/) instance whose coordinator is server $i \bmod n$. The coordinator owns ballot 0 and can propose any command or no-op in it. Every other server can only propose no-op, and must do it with a full Paxos run at a higher ballot.

## The algorithm

```pseudo id=main
SERVER p, with I_p ← p, the next instance p coordinates
L1  Rule 1. on a client command v:  send SUGGEST(I_p, v) to all; I_p ← I_p + n
L2  on SUGGEST(i, v) from q:  if p promised no ballot above 0 in i, accept (0, v) and reply ACK(i)
L3  Rule 2. also, if i > I_p:  send SKIP(j) for each own instance j with I_p ≤ j < i; I_p ← the first own instance > i
L4  on ACK(i) from a majority, for a suggestion of p:  learn v in i; send LEARN(i, v) to all
L5  on SKIP(i):  learn no-op in i

L6  Rule 3. on suspecting q:  for each instance j of q with j < I_p and not learned:  revoke j
L7    revoke j:  pick a ballot b > 0; send PREPARE(j, b); an acceptor promises b and reports its accepted (ballot, value)
L8    on promises from a majority:  v ← the value with the highest ballot, or no-op if none
L9    send ACCEPT(j, b, v); an acceptor accepts if it promised no higher ballot, and replies
L10   on accepts from a majority:  learn v in j; send LEARN(j, v) to all

L11 Rule 4. on learning no-op in i where p suggested v ≠ no-op:  suggest v again (L1)
L12 run the learned instances in order 0, 1, 2, ...; skip no-ops; wait at the first instance not learned
```

**Coordinated Paxos** (lines L1, L2, L4 and L5). In its own instance the coordinator starts at ballot 0, so it needs no first phase: it goes straight to the accept phase, as a stable leader in [Multi-Paxos](/multi-paxos/) does. A skip is learned *at once*, with one message: since the coordinator never proposes a command in that instance, and the other servers can propose only no-op, no-op is the only value that can be chosen.

**Rule 2** (line L3). When server $p$ sees a suggestion for a later instance, it skips all its own instances before it. So an idle server never blocks the log, and a busy one does not wait for the idle ones. The paper sends skips on other messages to save messages.

**Revocation** (lines L6 to L10). A crashed coordinator never skips, so its instances would block the log forever. A server that suspects it runs both Paxos phases with a higher ballot and proposes no-op, unless phase 1 shows that the coordinator's command was accepted; then it must propose that command.

**Rule 4** (line L11). A server that is only slow can be suspected and revoked. If its command loses its instance to no-op, it suggests the command again in a later instance.

## Example

$n = 3$, $F = 1$. Server 0 coordinates instances 0, 3, 6, server 1 coordinates 1, 4, 7, server 2 coordinates 2, 5, 8.

| step | event | learned log |
|---|---|---|
| 1 | server 0 gets $a$: SUGGEST(0, $a$) | |
| 2 | server 2 gets $b$: SUGGEST(2, $b$) | |
| 3 | server 1 gets SUGGEST(2, $b$); $2 > I_1 = 1$, so it sends SKIP(1) and sets $I_1 = 4$ | 1: no-op |
| 4 | server 2 gets SUGGEST(0, $a$); $0 < I_2 = 5$, so no skip | |
| 5 | ACKs reach servers 0 and 2; LEARN(0, $a$) and LEARN(2, $b$) | 0: $a$, 1: no-op, 2: $b$ |
| 6 | all servers run $a$ then $b$ | |
| 7 | server 1 crashes; server 0 suggests $c$ in instance 3, server 2 suggests $d$ in 5 | |
| 8 | instance 4 belongs to server 1 and stays empty: instance 5 waits | 3: $c$, 5: $d$ |
| 9 | server 0 suspects server 1, sends PREPARE(4, $b = (1, 0)$); servers 0 and 2 promise, nothing accepted | |
| 10 | ACCEPT(4, $b$, no-op) is accepted by servers 0 and 2 | 4: no-op |
| 11 | all live servers run $c$ then $d$ | |

## Correctness

- **Agreement per instance.** Each instance is one run of [Paxos](/paxos/) in which ballot 0 belongs to the coordinator. A skip is safe to learn at once, because the coordinator proposes either one command or no-op, never both, and revokers can propose only no-op or a value found in phase 1.
- **Same sequence.** Line L12 runs the instances in index order, and every server learns the same value per instance, so every server runs the same sequence.
- **No duplicates.** A coordinator suggests a command again only when no-op was chosen for its earlier instance (line L11), so the command was not chosen there.
- **Liveness.** A live server's command commits after one round trip to a majority. To run it, every earlier instance must be learned: earlier instances of live servers get a command or a skip by Rule 2, and those of crashed servers are revoked once the failure detector suspects them.

The full proof is below.

## Complexity

- **Commit.** One round trip from the coordinator to a majority, as in Multi-Paxos with a stable leader: two message delays, and $3(n - 1)$ messages per command with SUGGEST, ACK and LEARN.
- **Execution delay.** A command can wait for the skips of earlier instances. The SKIP from a far server needs only one message delay, but it must come from every server, not from a majority, so the slowest server sets the pace.
- **Skips.** With all servers busy, almost no skips are needed. With one busy server, each command makes $n - 1$ skips, which the paper sends on other messages.
- **Revocation.** Four message delays per revoked instance, and many instances can be revoked in one run.
- **Load.** Each server coordinates $1/n$ of the instances, so no single leader limits throughput.

## Properties

- **Rotating leadership.** The bottleneck of a single leader in Multi-Paxos is gone: CPU and network load are spread over all servers.
- **Low latency in a wide area.** Each client talks to its nearest server, which coordinates its command at once.
- **Sensitive to slow servers.** Execution waits for every server's skips or suggestions, and a crashed server blocks the log until it is revoked.
- **Total order.** All commands are ordered, interfering or not, unlike [EPaxos](/epaxos/) and [Generalized Paxos](/generalized-paxos/).

## Variants and improvements

- **Piggybacked skips.** The paper sends skips with ACK messages and later suggestions, so that a busy system needs almost no extra messages.
- **Commutative commands.** The paper also lets commands that commute run before the earlier instances are learned, which hides some of the delay from slow servers.
- **[EPaxos](/epaxos/).** Also has no single leader, but orders only interfering commands and has no fixed slots, so it never waits for skips.
- **[Multi-Paxos](/multi-paxos/).** One leader for all slots: simpler, but the leader is a bottleneck and far from some clients.

## When to use it

Use Mencius when clients are spread over sites, every site has load, and links are reliable, for example a wide-area system with steady traffic at each data center. It is a poor choice when one server is often slow or unreachable, because the whole log waits for its skips, or when the load is very uneven and the skips cost more than they save.

## Pitfalls

- **Learning a skip in two phases.** Line L5 learns a skip at once. That is safe only because a coordinator never proposes a command in an instance it skips; a server that skips its own instance after suggesting in it (for example, a bug in line L3 that skips $j \ge I_p$) can lose that command.
- **Forgetting Rule 2.** Without line L3, an idle server never fills its instances, and line L12 waits forever. The tests show that execution stalls when only one server has clients.
- **Revoking without phase 1.** Line L8 must take an accepted value if there is one. The tests show that a revoker that proposes no-op without reading phase 1 can make a server learn no-op where the coordinator has learned a command.
- **Dropping a revoked command.** Line L11 must suggest it again. The tests show that without Rule 4, commands of a falsely suspected server are lost.
- **Reusing a revoked instance.** A revoker can fill an instance that the coordinator has not used yet. The coordinator must not suggest in an instance it already learned as no-op, or the command is silently lost.

## Implementations

## History

Mao, Junqueira and Marzullo presented Mencius at OSDI 2008. Their starting point was the observation that, in a wide-area network, a single Multi-Paxos leader is both a bottleneck and far from most clients. They gave each server a fixed share of the log and made the cost of an unused share small, with skips. Later leaderless protocols such as [EPaxos](/epaxos/) (2013) compare their wide-area latency with Mencius.

## References
