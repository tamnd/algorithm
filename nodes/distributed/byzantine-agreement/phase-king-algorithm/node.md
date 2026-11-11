---
tag: VHXE8S
kind: algorithm
slug: phase-king-algorithm
name: Phase King algorithm
aliases:
- Phase King
- Berman-Garay-Perry algorithm
area: distributed/byzantine-agreement
level: advanced
summary: Deterministic synchronous binary Byzantine agreement for n > 3t in t + 1 phases of three rounds, with O(n^2 t) messages of two bits.
solves: [consensus-problem]
model: synchronous-model
complexity:
  vars: {n: the number of processes, t: the largest number of Byzantine processes}
  time: {worst: 3(t + 1)}
  messages: {worst: Θ(n^2 t)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [synchronous-model, byzantine-failure-model, consensus-problem]
see_also: [phase-queen-algorithm, oral-messages-algorithm, byzantine-resilience-bound, byzantine-round-lower-bound, strong-validity, dolev-strong-algorithm, feldman-micali-byzantine-agreement, rabin-randomized-byzantine-agreement]
sources:
  - paper: "Piotr Berman, Juan A. Garay and Kenneth J. Perry, Towards optimal distributed consensus, 30th Annual Symposium on Foundations of Computer Science (FOCS), IEEE, 1989"
    locator: "pages 410 to 415 (the protocol with n > 3t, 3t + 3 rounds and messages of two bits; also a protocol with n > 4t)"
  - url: https://disco.ethz.ch/courses/distsys/lnotes/chapter17.pdf
    title: Roger Wattenhofer, Distributed Systems lecture notes, ETH Zurich, Chapter 17, Byzantine Agreement
    locator: Algorithm 17.15 (the King algorithm for f < n/3) and Theorem 17.20; the version on this page
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Section 5.2.4 (a polynomial algorithm, the phase king algorithm with n > 4f and two rounds per phase)
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine generals problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: the problem and the bound n > 3m for oral messages
  - paper: "Juan A. Garay and Yoram Moses, Fully polynomial Byzantine agreement for n > 3t processors in t + 1 rounds, SIAM Journal on Computing 27(1), 1998"
    locator: the main theorem (polynomial messages, n > 3t, t + 1 rounds)
---

The phase king algorithm solves binary [Byzantine agreement](/consensus-problem/) in the [synchronous model](/synchronous-model/) without signatures when $n > 3t$. It runs $t + 1$ phases of three rounds, and in each phase one fixed process, the king, breaks ties. It sends $O(n^2 t)$ messages of two bits, while the [oral messages algorithm](/oral-messages-algorithm/) sends exponentially many. Berman, Garay and Perry gave it in 1989. This page gives the three-round version for $n > 3t$; the two-round version for $n > 4t$ is the [phase queen algorithm](/phase-queen-algorithm/).

## In plain words

A group of computers must agree on 0 or 1. Some of them are traitors that lie, and can tell different lies to different computers.

The work is cut into phases, and each phase has a leader, the king. In a phase, each computer first tells everyone its value. A computer that sees one value from almost everyone suggests that value. A computer that sees enough suggestions for a value takes it. Then the king tells everyone its value. A computer that saw very strong support for its own value keeps it. All others take the value of the king.

There is one phase more than the number of traitors, so at least one king is honest. In that phase all honest computers end with the same value. Once they agree, no traitor can change their minds again.

## The problem

There are $n$ processes $p_1, \ldots, p_n$ on a complete network of reliable, authenticated point-to-point links: a receiver knows the true sender of each message. Messages are oral, which means unsigned, as in the [oral messages model](/oral-messages-model/). The model is synchronous: computation is in lock-step rounds, and a message sent in a round arrives in that round. At most $t$ processes are [Byzantine](/byzantine-failure-model/): they can send any messages, different ones to different receivers, or none. The adversary is static (it chooses the faulty set before the run) and rushing (in each round it sees the honest messages before it chooses its own). Each process $p_i$ has an input bit $x_i$. The algorithm must give:

- **Agreement.** All honest processes decide the same bit.
- **Strong validity.** If all honest processes have the same input $v$, they all decide $v$. This is the form of [strong validity](/strong-validity/) for binary values.
- **Termination.** Every honest process decides.

Agreement and validity are safety properties, and termination is a liveness property. All three hold in every run, because the model is synchronous.

## The algorithm

The code of process $p_i$ is below. A *broadcast* sends one message to each of the $n$ processes, $p_i$ included. The king of phase $\varphi$ is $p_\varphi$. Counts are over different senders.

```pseudo id=main
PHASE-KING(i, x_i)                                   ▷ the code of p_i; n > 3t
L1  x ← x_i
L2  for φ ← 1 to t + 1 do
L3      round 1: broadcast value(x); receive value messages
L4      round 2: if value(y) came from at least n − t senders then broadcast propose(y)
L5               receive propose messages
L6               if propose(z) came from more than t senders then x ← z
L7      round 3: if i = φ then broadcast king(x)          ▷ p_φ is the king
L8               if propose(x) came from fewer than n − t senders then
L9                   x ← the bit w of king(w) from p_φ, or 0 if none came
L10 decide x
```

A message carries one bit, plus the round, so the value and king messages need one bit and the propose message needs two (0, 1, or none). Line L4 can hold for at most one $y$, because $2(n - t) > n$. Line L6 can hold for at most one $z$, by Lemma 2 of the proof. At line L8 the test uses the value $x$ that the process holds after line L6, and the count of round 2.

## Example

Take $n = 4$, $t = 1$, with $p_1$ Byzantine, so the king of phase 1 lies. The honest inputs are $x_2 = 0$, $x_3 = 1$, $x_4 = 1$. In every round, $p_1$ sends 0 to $p_1$ and $p_3$ and sends 1 to $p_2$ and $p_4$. A proposal needs $n - t = 3$ equal values, a change at line L6 needs more than $t = 1$ equal proposals, and a process keeps its value at line L8 with at least 3 proposals for it.

| phase | process | values got (0s, 1s) | proposes | proposals got (0s, 1s) | x after L6 | king says | x at end |
|---|---|---|---|---|---|---|---|
| 1 | $p_2$ | 1, 3 | 1 | 0, 3 | 1 | 1 (ignored) | 1 |
| 1 | $p_3$ | 2, 2 | none | 1, 2 | 1 | 0 | 0 |
| 1 | $p_4$ | 1, 3 | 1 | 0, 3 | 1 | 1 (ignored) | 1 |
| 2 | $p_2$ | 1, 3 | 1 | 0, 3 | 1 | 1 | 1 |
| 2 | $p_3$ | 2, 2 | none | 1, 2 | 1 | 1 | 1 |
| 2 | $p_4$ | 1, 3 | 1 | 0, 3 | 1 | 1 | 1 |

In phase 1 the faulty king pulls $p_3$ back to 0, because $p_3$ saw only two proposals for 1. In phase 2 the king $p_2$ is honest, and it sends 1, the only value that an honest process proposed. All honest processes decide 1 after 6 rounds. The honest processes send 44 messages: 12 values and 8 proposals in each phase, and 4 king messages in phase 2.

## Correctness

The proof has four lemmas, and the full proof is below.

- **One honest proposal.** An honest process proposes $y$ only if at least $n - 2t$ honest processes hold $y$. Two values would need $2(n - 2t)$ honest processes out of at most $n$, and this is too many when $n > 3t$.
- **Only that value can win round 2.** More than $t$ proposals for $z$ include an honest one.
- **Persistence.** If all honest processes hold $v$, each of them sees $n - t$ values $v$, proposes $v$, sees $n - t$ proposals $v$ and keeps $v$. The king cannot change it.
- **An honest king unifies.** An honest process keeps its value at line L8 only if at least $n - 2t > t$ honest processes proposed it. The honest king then also got more than $t$ such proposals, so it holds the same value and sends it to everyone else.

There are $t + 1$ kings and at most $t$ traitors, so some phase has an honest king. After it, all honest processes agree, and persistence keeps the agreement to the end. Validity is persistence from the first phase.

## Complexity

The costs are in the synchronous model, for the worst case.

- **Rounds.** Exactly $3(t + 1)$. This is within a factor of 3 of the lower bound of $t + 1$ rounds, the [Byzantine round lower bound](/byzantine-round-lower-bound/).
- **Messages.** In each phase each honest process sends at most $2n$ messages in rounds 1 and 2, and the king sends $n$ more. So the honest processes send at most $(t + 1)(2n^2 + n) = O(n^2 t)$ messages, and $\Theta(n^2 t)$ when all processes are honest.
- **Bits.** Each message holds at most two bits besides the round number, so $O(n^2 t)$ bits in total. The oral messages algorithm sends $\Theta(n^{t+1})$ messages, and messages that grow with the round.
- **Local work and space.** A process keeps a few counters per round, so $O(1)$ counters and $O(n)$ time per round.

The [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/) gives $\Omega(n t)$ messages for any deterministic algorithm, so the phase king is within a factor of $n$ of it.

## Properties

- **Deterministic.** No coins and no signatures. The only assumption beyond synchrony is that a receiver knows the sender.
- **Optimal resilience.** $n > 3t$ matches the [Byzantine resilience bound](/byzantine-resilience-bound/) for oral messages.
- **Constant message size.** Two bits per message, against messages of growing size in the oral messages algorithm.
- **Binary.** It decides one bit. A multivalued version needs a reduction from many values to one bit.
- **Not early stopping.** It always runs $t + 1$ phases, also when no process is faulty.

## Variants and improvements

- **Phase queen.** With $n > 4t$, two rounds per phase are enough: one round of values and one round in which the queen sends its majority value. See the [phase queen algorithm](/phase-queen-algorithm/). Attiya and Welch (Section 5.2.4) give this two-round algorithm with $n > 4f$ under the name "phase king", so a source that says "phase king" may mean either version. Check the number of rounds per phase and the threshold.
- **Fewer rounds.** Garay and Moses (1998) give an algorithm for $n > 3t$ with polynomial messages that runs in exactly $t + 1$ rounds, which is optimal.
- **Randomized algorithms.** With a common coin, [Rabin's algorithm](/rabin-randomized-byzantine-agreement/) and the [Feldman-Micali algorithm](/feldman-micali-byzantine-agreement/) decide in a constant expected number of rounds. Their round structure is the same as rounds 1 and 2 here, with the king replaced by a coin.
- **Signatures.** With signatures any $t < n$ is possible for [Byzantine broadcast](/byzantine-broadcast/), by the [Dolev-Strong algorithm](/dolev-strong-algorithm/).

## When to use it

Use the phase king algorithm when the network is synchronous, there is no public key infrastructure, and the group is small enough that $O(n^2)$ messages per round are cheap, for example in hardware or in fault-tolerant clock and sensor systems. It is the standard teaching example of a polynomial Byzantine agreement algorithm. If rounds are expensive and there are few faults, an early stopping algorithm is better. If the network is not synchronous, use a protocol for [partial synchrony](/partial-synchrony/) such as [PBFT](/pbft/), or a randomized asynchronous one such as [Bracha's](/bracha-asynchronous-agreement/).

## Pitfalls

- **Mixing up the versions.** The three-round version needs $n > 3t$. The two-round version needs $n > 4t$. Running the two-round version with $3t < n \le 4t$ breaks it.
- **Counting received messages instead of senders.** All thresholds count different senders. A Byzantine process that sends the same proposal twice must count once.
- **Testing line L8 with the old value.** The test must use the value after line L6. With the start value, an honest process can keep a value that no honest process proposed.
- **Running fewer than $t + 1$ phases.** The proof needs a phase with an honest king. With $t$ phases the faulty processes can be all the kings.
- **A default for a missing king message.** A silent king must give the receivers some value, here 0. Any fixed value works, but every process must use the same rule.

## Implementations

## History

Lamport, Shostak and Pease (1982) solved Byzantine agreement for $n > 3t$ in $t + 1$ rounds, with messages whose number grows exponentially. In 1989 Berman and Garay gave a protocol for $n > 4t$ with one-bit messages and $2t + 2$ rounds, and Berman, Garay and Perry gave at FOCS 1989 the phase king protocol for $n > 3t$, with $3t + 3$ rounds and two-bit messages. The name comes from the king that breaks ties in each phase. Garay and Moses (1998) later reached $t + 1$ rounds with polynomial messages and $n > 3t$.

## References
