---
tag: YZ2GMJ
kind: algorithm
slug: fast-paxos
name: Fast Paxos
area: distributed/consensus
level: research
summary: Reaches consensus in two message delays when clients propose directly to acceptors.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of acceptors, l: the number of learners}
  time: {best: Θ(1)}
  messages: {best: Θ(n l)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 2006
  people: [Leslie Lamport]
  note: Published in Distributed Computing in 2006, after a Microsoft Research technical report in 2005.
prereqs: [paxos, quorum, ballot-number]
see_also: [multi-paxos, generalized-paxos, epaxos, flexible-paxos, quorum-intersection]
sources:
  - paper: doi:10.1007/s00446-006-0005-x
    title: Leslie Lamport, Fast Paxos, Distributed Computing 19(2), 79-103, 2006
    locator: Section 3.1 (the Quorum Requirement), Section 3.2 (collision recovery and the rule with O4(v)), Section 3.4 (quorum sizes and cost)
  - paper: "Leslie Lamport, Fast Paxos, Microsoft Research technical report MSR-TR-2005-112, 2005"
    locator: the same sections as the journal version
  - paper: "Leslie Lamport, Generalized consensus and Paxos, Microsoft Research technical report MSR-TR-2005-33, 2005"
    locator: Section 5.1 (the same quorum assumption for fast and classic ballots)
---

Fast Paxos is a variant of [Paxos](/paxos/) in which clients send their values straight to the acceptors, so that a value can be learned two message delays after a client sends it, not three. It works in rounds of two kinds: classic rounds, which run like Paxos, and fast rounds, in which each acceptor votes for the first client value that reaches it. The price is larger [quorums](/quorum/): when classic quorums are majorities, a fast quorum must hold at least $\lceil 3n/4 \rceil$ of the $n$ acceptors, and two clients that send at the same time can cause a collision that costs extra rounds.

## In plain words

In ordinary Paxos a client gives its value to a leader, and the leader asks the voters. That is one extra hop. In Fast Paxos the leader first tells the voters: "for this round, vote for whatever value reaches you first". After that, clients send their values to the voters themselves, and a value wins as soon as a large enough group votes for it.

If two clients send at the same time, some voters may get one value first and some the other. Then no value may win, which is a collision. The leader looks at the votes and starts a normal round to settle it.

The group that must agree in a fast round is bigger than a majority. It must be so big that a later leader, who sees only part of the votes, can still tell which value may have won.

## The problem

**Model.** There are $n$ acceptors, one or more coordinators, clients that propose values, and learners. The model is the [asynchronous model](/asynchronous-model/) with [crash failures](/crash-failure/), as for Paxos. Messages can be lost, duplicated and reordered. Each round $i$ has one coordinator, and each round is either classic or fast. Lamport writes $N$ for the number of acceptors, $F$ for the number of failures that classic rounds tolerate and $E$ for the number that fast rounds tolerate.

**Quorums.** For each round there is a set of $i$-quorums. A classic quorum is a set of at least $q_c$ acceptors, and a fast quorum a set of at least $q_f \ge q_c$ acceptors. A value $v$ is *chosen in round* $i$ when every acceptor of some $i$-quorum has voted for $v$ in round $i$.

**The Quorum Requirement.** For any rounds $i$ and $j$:

- (a) any $i$-quorum and any $j$-quorum have an acceptor in common;
- (b) if $j$ is fast, any $i$-quorum and any two $j$-quorums have an acceptor in common.

With sizes $q_c \le q_f$ this is the same as

$$2 q_c > n \quad\text{and}\quad q_c + 2 q_f > 2n.$$

In the terms of Lamport, $q_c = N - F$ and $q_f = N - E$, and the conditions are $N > 2F$ and $N > 2E + F$. Three sets of sizes $s_1, s_2, s_3$ of $n$ acceptors always share an acceptor if and only if $s_1 + s_2 + s_3 > 2n$, which gives the second condition. The guarantees are the same as for Paxos: agreement and validity always, and termination only when one coordinator runs alone long enough.

## The algorithm

Each acceptor keeps rnd (the largest round it has joined), vrnd and vval (the round and value of its last vote, or $\bot$). A coordinator uses the rule of lines L3 to L7 to choose a value for its round from the reports of a classic quorum $Q$. In that rule, O4($w$) means: there is a $k$-quorum $R$ such that every acceptor in $R \cap Q$ voted for $w$ in round $k$.

```pseudo id=main
COORDINATOR of round i
L1  start round i:  send 1a(i) to all acceptors
L2  on 1b(i, vrnd, vval) from each acceptor of a classic quorum Q:
L3      k ← the largest vrnd reported in Q
L4      if no acceptor of Q has voted then v ← Any if i is fast, else a proposed value
L5      else if all votes of Q in round k are for one value w then v ← w
L6      else if O4(w) holds for some value w then v ← w
L7      else v ← any proposed value
L8      send 2a(i, v) to all acceptors

ACCEPTOR
L9  on 1a(i):  if i > rnd then rnd ← i; send 1b(i, vrnd, vval) to the coordinator
L10 on 2a(i, v):  if i ≥ rnd and no vote in round i yet: if v = Any, wait for a proposal (or vote for one already here), else vote(i, v)
L11 on a proposal v from a client:  if round rnd has Any and no vote in round rnd yet then vote(rnd, v)
L12 vote(i, v):  rnd ← i; vrnd ← i; vval ← v; send 2b(i, v) to the learners and the coordinator

LEARNER
L13 on 2b(i, v) from every acceptor of an i-quorum, all for v:  learn v
```

**Fast rounds.** A coordinator with no constraint sends the special value Any in a fast round (line L4). This lets each acceptor vote for the first client value it gets (line L11). Phase 1 of a fast round can run long before any client sends, so in the steady state only the proposal and the 2b messages lie on the path.

**Collisions.** If different acceptors vote for different values in one fast round, perhaps no value gets a fast quorum. The coordinator must then choose a value for a new round, and this is where lines L5 and L6 differ from Paxos. In a fast round $k$ the quorum $Q$ can report several values for round $k$. Only a value $w$ with O4($w$) may have been chosen in round $k$, and condition (b) makes that value unique.

**Coordinated recovery.** When the coordinator of fast round $i$ also coordinates round $i + 1$, its 2b messages of round $i$ serve as the 1b messages of round $i + 1$. It runs lines L3 to L8 on them at once and sends 2a($i+1$, $v$). An acceptor that voted in round $i$ cannot vote in a round below $i + 1$ again, so its 2b message says all that a 1b message would.

**Uncoordinated recovery.** The acceptors can also send their 2b messages to each other, and each one runs the same rule and votes in round $i + 1$, which must be fast. This saves one more delay but needs all acceptors to see the same quorum's votes, or else it produces a second collision.

## Example

Five acceptors, so $q_c = 3$ and $q_f = 4$. Round 0 is fast, its coordinator has sent 2a(0, Any), and two clients send $x$ and $y$ at the same time.

| step | event | $A_0$ | $A_1$ | $A_2$ | $A_3$ | $A_4$ |
|---|---|---|---|---|---|---|
| 1 | each acceptor votes for the first value it gets | $x$ | $x$ | $x$ | $y$ | $y$ |
| 2 | no value has 4 votes: a collision | | | | | |
| 3 | the coordinator has 2b from $Q = \{A_0, A_1, A_2, A_3\}$; $k = 0$; values $\{x, y\}$ | | | | | |
| 4 | O4($x$): $R = \{A_0, A_1, A_2, A_4\}$ gives $R \cap Q = \{A_0, A_1, A_2\}$, all $x$ | | | | | |
| 5 | O4($y$) fails: each set of 4 meets $Q$ in at least 3 acceptors, and only $A_3$ voted $y$ | | | | | |
| 6 | 2a(1, $x$) in classic round 1; all acceptors vote $x$; $x$ is chosen | $x$ | $x$ | $x$ | $x$ | $x$ |

The value is learned four message delays after the clients sent: proposal, 2b, 2a, 2b.

Now take $q_c = q_f = 3$, which breaks $q_c + 2q_f > 2n$ since $9 \le 10$. In step 1 the acceptors $A_0, A_1, A_2$ vote $y$ and $A_3, A_4$ vote $x$, so $y$ is chosen in round 0 by a fast quorum of 3. A coordinator that hears from $Q = \{A_2, A_3, A_4\}$ finds that O4 holds for both values. For $x$, the fast quorum $R = \{A_0, A_3, A_4\}$ meets $Q$ in $\{A_3, A_4\}$, and both voted $x$. For $y$, the fast quorum $R = \{A_0, A_1, A_2\}$ meets $Q$ in $\{A_2\}$, which voted $y$. If it picks $x$, then $A_2, A_3, A_4$ vote $x$ in round 1, and both $x$ and $y$ are chosen.

## Correctness

Call a value $w$ *safe at round* $i$ if no value other than $w$ is ever chosen in any round $j < i$. The key lemma: lines L3 to L7 return a value that is safe at $i$, and Any only if all values are safe at $i$. The proof splits on $k$. Rounds strictly between $k$ and $i$ choose nothing, because each of their quorums meets $Q$ by (a), and no acceptor of $Q$ votes there. Rounds below $k$ choose nothing other than the values voted in round $k$, by induction. In round $k$ itself, a value can be chosen only if it satisfies O4, and by (b) at most one value does. Agreement follows: a vote in round $i$ is always for a value safe at $i$, and two quorums of the same round meet. The full proof is below.

**Liveness.** As in Paxos, a single coordinator that runs alone after [partial synchrony](/partial-synchrony/) sets in makes progress. A fast round needs $q_f$ live acceptors to choose a value, while a classic round needs only $q_c$. Clients that keep sending different values at the same time can cause collision after collision in fast rounds, so a coordinator should switch to classic rounds when collisions are frequent.

## Complexity

All delays are counted from the moment a client sends its value, with phase 1 already done.

| case | message delays | path |
|---|---|---|
| classic round | 3 | client → coordinator → acceptors → learners |
| fast round, no collision | 2 | client → acceptors → learners |
| collision, coordinated recovery | 4 | client → acceptors → coordinator → acceptors → learners |
| collision, uncoordinated recovery | 3 | client → acceptors → acceptors → learners |

In a fast round each client sends $n$ messages and each acceptor sends $l$ 2b messages, so $n + nl = \Theta(nl)$ messages per value.

Quorum sizes, with $q_c$ the smallest majority:

| $n$ | 3 | 4 | 5 | 7 | 9 |
|---|---|---|---|---|---|
| $q_c$ | 2 | 3 | 3 | 4 | 5 |
| smallest $q_f$ | 3 | 3 | 4 | 6 | 7 |

The smallest fast quorum with majority classic quorums is $\lceil 3n/4 \rceil$ ($F = \lceil n/2 \rceil - 1$ and $E = \lfloor n/4 \rfloor$). If both kinds of quorum have the same size $n - e$, the largest $e$ is $\lceil n/3 \rceil - 1$, so $q_c = q_f = \lfloor 2n/3 \rfloor + 1$.

## Properties

- **Safe under asynchrony.** Agreement and validity hold in every run, with any number of crashes.
- **Rounds of two kinds.** Classic and fast rounds can be mixed in one run. A system can use fast rounds when contention is low and classic rounds when it is high.
- **Fewer failures tolerated in fast rounds.** With $n = 5$ a fast round needs 4 acceptors, so it stops after 2 crashes while classic rounds still work.
- **Collisions cost more than they save.** One collision costs more delays than a classic round.

## Variants and improvements

- **[Generalized Paxos](/generalized-paxos/).** Commands that commute do not collide, so fast rounds succeed more often.
- **[EPaxos](/epaxos/).** A leaderless protocol with a fast path whose quorum is smaller than $\lceil 3n/4 \rceil$, because the command leader is counted and only the order of interfering commands matters.
- **[Multi-Paxos](/multi-paxos/) with fast rounds.** One phase 1 can open fast rounds for all future slots.
- **[Flexible Paxos](/flexible-paxos/).** Relaxes the intersection condition of classic Paxos in another direction: only phase 1 and phase 2 quorums must meet.

## When to use it

Use Fast Paxos when clients are many hops from a leader, conflicting proposals are rare, and enough acceptors are up to form a fast quorum. A system with heavy contention, or one that must keep working with nearly half of its acceptors down, does better with classic Paxos or [Multi-Paxos](/multi-paxos/).

## Pitfalls

- **Fast quorums that are too small.** Line L13 with $q_f$ below the bound lets two values be chosen, as the example shows. Check $q_c + 2q_f > 2n$, not only $q_f > n/2$.
- **The Paxos rule in a fast round.** After a fast round, line L5 alone is wrong: the quorum can report several values for round $k$. Taking any one of them, as Paxos would, can drop a chosen value. Line L6 must test O4.
- **Two votes in one round.** Lines L10 and L11 must allow only one vote per acceptor per round. An acceptor that votes for a second proposal in the same fast round breaks the uniqueness of O4.
- **Recovery with the wrong reports.** Coordinated recovery may use 2b messages as 1b messages only for the next round of the same coordinator. Using them for a round of another coordinator skips its promise.
- **Uncoordinated recovery with different quorums.** If acceptors apply line L6 to different sets of votes, they may vote for different values in round $i + 1$, and the collision repeats.

## Implementations

## History

Lamport wrote Fast Paxos as a Microsoft Research technical report in 2005, and it appeared in Distributed Computing in 2006. The report on Generalized Consensus and Paxos (2005) uses the same quorum assumption with commands that may commute.

## References
