---
tag: 8MFRY7
kind: algorithm
slug: generalized-paxos
name: Generalized Paxos
aliases:
- generalized consensus
area: distributed/consensus
level: research
summary: Agrees on partial orders of commuting commands rather than a total order.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of acceptors, l: the number of learners}
  time: {best: Θ(1)}
  messages: {best: Θ(n l)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 2005
  people: [Leslie Lamport]
  note: Published as a Microsoft Research technical report in 2005.
prereqs: [paxos, fast-paxos, quorum]
see_also: [multi-paxos, epaxos, total-order-broadcast, replicated-state-machine, quorum-intersection, ballot-number]
sources:
  - paper: "Leslie Lamport, Generalized consensus and Paxos, Microsoft Research Technical Report MSR-TR-2005-33, March 2005"
    locator: the definition of c-structs and their axioms, the generalized consensus problem, the command structures of histories, and the Generalized Paxos algorithm with the operator ProvedSafe
  - paper: doi:10.1007/s00446-006-0005-x
    title: Leslie Lamport, Fast Paxos, Distributed Computing 19(2), 79-103, 2006
    locator: the quorum requirement for fast rounds and collision recovery, which Generalized Paxos reuses
  - paper: "Fernando Pedone and André Schiper, Handling message semantics with Generic Broadcast protocols, Distributed Computing 15(2), 97-107, 2002"
    locator: generic broadcast, which orders only messages that conflict
---

Generalized Paxos is a form of [Fast Paxos](/fast-paxos/) that agrees on a *c-struct* instead of a single value. For a [replicated state machine](/replicated-state-machine/) the c-struct is a command history: a set of commands in which only the commands that do not commute need an order. Proposers send commands straight to the acceptors, and two commands that commute can arrive in different orders at different acceptors without a conflict. A collision, and so a slow recovery, happens only when two commands that interfere arrive in different orders. The model is [asynchronous](/asynchronous-model/) with [crash failures](/crash-failure/).

## In plain words

A bank keeps copies of its accounts on several servers. A deposit to Alice and a deposit to Bob can run in either order: the result is the same. Two withdrawals from Alice cannot, because the second one may fail if the first one empties the account.

Fast Paxos lets clients send commands straight to the servers and saves a step, but it fails over to a slow step each time two servers see two commands in different orders. Generalized Paxos asks the servers to agree only on the order of the commands that matter. Alice's deposit and Bob's deposit can arrive in any order, and the servers still agree at once. Only two commands on the same account, in different orders on different servers, make the system slow down and choose an order.

## The problem

**C-structs.** Lamport defines generalized consensus over a set of c-structs with:

- a bottom element $\bot$ and an append operation $v \bullet C$ that adds a command $C$,
- a prefix order: $v \sqsubseteq w$ when $w = v \bullet C_1 \bullet \cdots \bullet C_k$ for some commands,
- the greatest lower bound $v \sqcap w$ (the largest common prefix) and, when it exists, the least upper bound $v \sqcup w$,
- *compatible* c-structs: those with a common upper bound.

Ordinary consensus is the case where the c-structs are $\bot$ and single values. A sequence of commands with the usual prefix order gives consensus on a log, as in [Multi-Paxos](/multi-paxos/).

**Command histories.** For a state machine, fix an *interference* relation: two commands interfere when they do not commute. A history is a set of commands together with an order for each pair of commands in it that interfere. Two sequences that differ only by swaps of adjacent commands that do not interfere give the same history. Two histories are compatible when they order every common pair of interfering commands in the same way and neither holds a command that interferes with a command that only the other one holds.

**Generalized consensus.** Proposers propose commands and each learner $\ell$ learns a c-struct $\text{learned}_\ell$ that only grows. The requirements are:

- **Nontriviality.** Each learned c-struct holds only proposed commands.
- **Stability.** A learner's value only grows in the prefix order.
- **Consistency.** All learned values, at all learners and all times, are compatible.
- **Liveness.** With a stable leader and enough live acceptors, each proposed command is eventually in every learned value.

**Model.** $n$ acceptors with stable storage, [asynchronous](/asynchronous-model/) messages that can be lost, duplicated and reordered, and [crash failures](/crash-failure/). Ballots are fast or classic, as in Fast Paxos, with quorum sizes $q_f$ and $q_c$. Any two quorums must meet, and any quorum must meet any two fast quorums. With counting quorums this is $2q_c > n$ and $q_c + 2q_f > 2n$, for example $q_c = \lfloor n/2 \rfloor + 1$ and $q_f = \lceil 3n/4 \rceil$.

## The algorithm

```pseudo id=main
LEADER of ballot m (m is fast when its round is even)
L1  to start, or after a timeout:  m ← a fresh ballot; send 1a(m) to all acceptors
L2  on 1b(m, a, vrnd, vval) from an m-quorum Q:  w ← ProvedSafe(Q) • (the commands it knows); send 2a(m, w)
L3  ProvedSafe(Q):  k ← the largest vrnd in Q; RS ← the k-quorums R such that each a ∈ Q ∩ R reports vrnd = k
L4      if RS = ∅ then return the vval of some a ∈ Q with vrnd = k, else return ⊔ { ⊓{vval_a : a ∈ Q ∩ R} : R ∈ RS }
L5  on a proposal C in a classic ballot m:  w ← w • C; send 2a(m, w)
L6  on a timeout with a command not learned:  go to L1 with a classic ballot

ACCEPTOR a, with bal, vrnd and vval
L7  on 1a(m):  if m > bal then bal ← m; send 1b(m, a, vrnd, vval)
L8  on 2a(m, v):  if m ≥ bal and (vrnd < m or vval ⊑ v) then bal, vrnd, vval ← m, m, v; send 2b(m, a, vval)
L9  on a proposal C:  if bal = vrnd, vrnd is fast and C ∉ vval then vval ← vval • C; send 2b(vrnd, a, vval)

LEARNER
L10 on 2b(m, a, v):  keep v as the vote of a in m if it extends the vote kept
L11 for each m-quorum Q of acceptors with a vote in m:  learned ← learned ⊔ ⊓{v_a : a ∈ Q}
```

**Phase 1** (lines L1, L2 and L7) is the phase 1 of Paxos. The reply carries the last ballot $vrnd$ in which the acceptor voted, and its vote $vval$ in that ballot.

**ProvedSafe** (lines L3 and L4) finds a c-struct that extends every c-struct that could have been chosen in a ballot below $m$. Only ballot $k$ matters: in a lower ballot nothing new can be chosen, by the usual Paxos argument. A k-quorum $R$ could have chosen at most the common prefix of the votes of $R$. The leader sees only the members of $R$ in $Q$, so it takes the common prefix $\gamma(R)$ of their votes. It returns the least upper bound of these, which extends each value that could have been chosen. The quorum requirement makes them compatible.

**Phase 2.** In a classic ballot the leader appends each new command and sends the longer c-struct again (line L5). Each acceptor's vote in the ballot only grows (line L8). In a fast ballot the leader sends one 2a message, and then each acceptor appends the proposals it receives in the order it receives them (lines L8 and L9). Commands that commute give the same history in any order.

**Learning** (lines L10 and L11). A c-struct is chosen in ballot $m$ when every acceptor of an m-quorum has voted in $m$ for an extension of it. The largest such c-struct for a quorum $Q$ is the common prefix of the votes of $Q$. A learner learns the least upper bound of all c-structs that it sees chosen.

**Collisions.** If interfering commands arrive in different orders, the votes in a fast ballot may have no fast quorum with a long common prefix, and the commands stay unlearned. The leader times out and starts a classic ballot (line L6), which picks an order with ProvedSafe and then appends the rest.

## Example

$n = 5$, $q_c = 3$, $q_f = 4$. Commands $a$, $b$ and $d$ write key $x$ and interfere with each other; $c$ writes key $y$. Fast ballot $0$ has started with $w = \bot$.

| step | event | votes in ballot 0 | learned |
|---|---|---|---|
| 1 | $a$ and $c$ arrive: $A_0, A_1, A_4$ get $a$ then $c$; $A_2, A_3$ get $c$ then $a$ | all five: $\{a, c\}$ | $\{a, c\}$ after two message delays |
| 2 | $b$ and $d$ arrive: $A_0, A_1, A_4$ get $b$ then $d$; $A_2, A_3$ get $d$ then $b$ | $A_0, A_1, A_4$: $a < b < d$; $A_2, A_3$: $a < d < b$ | unchanged: no 4 votes agree on $b$ and $d$ |
| 3 | timeout; the leader starts classic ballot $1$ and gets 1b from $Q = \{A_0, A_1, A_2\}$, all with $vrnd = 0$ | | |
| 4 | ProvedSafe: for $R = \{A_0, A_1, A_3, A_4\}$, $Q \cap R = \{A_0, A_1\}$ gives $\gamma(R) = a < b < d$ with $c$; each other fast quorum holds $A_2$ and gives $\{a, c\}$ | | |
| 5 | the lub is $a < b < d$ with $c$; 2a(1, that) is accepted by three acceptors | | $\{a, b, c, d\}$ with $a < b < d$ |

In step 4 the leader must keep $b < d$. It heard $A_0$ and $A_1$ vote for it, and it did not hear $A_3$ and $A_4$. For all it knows, $A_0, A_1, A_3, A_4$ is a fast quorum that chose $a < b < d$.

## Correctness

**Consistency.** The proof follows Fast Paxos with c-structs in place of values. The key facts are:

- An acceptor's votes in one ballot only grow (lines L8 and L9).
- In a classic ballot all votes are prefixes of the leader's last c-struct, so they are compatible.
- In a fast ballot $k$, two k-quorums and any quorum $Q$ share an acceptor, so the values $\gamma(R)$ of line L4 are all prefixes of the vote of one acceptor, pairwise, and so compatible.
- If $v$ is chosen in ballot $j < m$, the value of ProvedSafe in ballot $m$ extends $v$, so every vote in ballot $m$ extends $v$.

So any two chosen c-structs are compatible, and the learned values, which are least upper bounds of chosen c-structs, are too. The full proof is below.

**Liveness.** As in Paxos, progress needs a single leader and a live quorum. A classic ballot with a single leader learns each command it receives. A fast ballot can stall on a collision, which line L6 turns into a classic ballot.

## Complexity

Let $l$ be the number of learners.

- **Fast ballot, no interference.** A command takes two message delays from the proposer to the learners: proposal to the acceptors, then 2b to the learners. That is $n + nl$ messages.
- **Classic ballot.** Three message delays (proposer, leader, acceptors, learners) and $1 + n + nl$ messages per command.
- **Collision.** A timeout, phase 1 with $2n$ messages, then a classic phase 2.
- **ProvedSafe.** The leader looks at every k-quorum, which is $\binom{n}{q}$ sets with counting quorums. For small $n$ this is cheap, and it needs no extra messages.
- **Size of messages.** A c-struct holds all commands so far. Real systems send only the new suffix and garbage collect the stable prefix.

## Properties

- **Generalizes Paxos and Fast Paxos.** With single values as c-structs it is Fast Paxos. With all commands interfering it is Fast Paxos on a log.
- **No total order where none is needed.** Learners may see commands that commute in different orders. A state machine that runs a learned history gets the same state in every case.
- **Safety does not depend on timing.**
- **Fast quorums are large.** About $3n/4$ acceptors, against $n/2$ for Paxos.

## Variants and improvements

- **[EPaxos](/epaxos/).** Uses the same idea of ordering only interfering commands, but with no leader: each command has dependencies, and each replica leads its own commands.
- **Generic broadcast.** Pedone and Schiper order only conflicting messages in a broadcast protocol, an earlier form of the same idea.
- **[Multi-Paxos](/multi-paxos/).** A total order, with the leader on the path of every command, and two delays from the leader.

## When to use it

Use the ideas of Generalized Paxos when clients are far from the leader, most commands commute (for example, writes to different keys), and saving one message delay matters. When most commands interfere, collisions are frequent and each one costs more than the delay saved. In practice EPaxos and similar protocols are more common, because they avoid the large c-structs and the single leader.

## Pitfalls

- **Learning a single vote.** Line L11 must take the common prefix over a whole quorum. A learner that learns the vote of one acceptor learns an order that was never chosen.
- **Taking a lub of all reports.** Line L4 must take the common prefix inside each $Q \cap R$ first. A lub of all votes in ballot $k$ may not exist, and if it does, it can contain an order that a later quorum overrides.
- **Appending after a promise.** Line L9 must check $bal = vrnd$. An acceptor that has promised a higher ballot and still appends proposals to its old vote breaks the promise.
- **Small fast quorums.** The quorums of lines L2, L4 and L11 must satisfy $q_c + 2q_f > 2n$. With $n = 4$ and quorums of two, the tests find runs in which two learners learn different orders of the same two commands.
- **A wrong interference relation.** If two commands that do not commute are marked as commuting, replicas run them in different orders and diverge, though the protocol is "consistent".

## Implementations

## History

Lamport described generalized consensus and Generalized Paxos in a Microsoft Research technical report in 2005, at about the same time as Fast Paxos. Generic broadcast by Pedone and Schiper had already ordered only the messages that conflict. The idea of agreeing on a partial order of commands led later to protocols such as EPaxos.

## References
