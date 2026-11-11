---
tag: P9R1W2
kind: algorithm
slug: phase-queen-algorithm
name: Phase Queen algorithm
aliases:
- Phase Queen
- Berman-Garay algorithm
area: distributed/byzantine-agreement
level: advanced
summary: Deterministic synchronous binary Byzantine agreement for n > 4t in t + 1 phases of two rounds, with O(n^2 t) one-bit messages.
solves: [consensus-problem]
model: synchronous-model
complexity:
  vars: {n: the number of processes, t: the largest number of Byzantine processes}
  time: {worst: 2(t + 1)}
  messages: {worst: Θ(n^2 t)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [synchronous-model, byzantine-failure-model, consensus-problem]
see_also: [phase-king-algorithm, oral-messages-algorithm, byzantine-resilience-bound, byzantine-round-lower-bound, strong-validity, rabin-randomized-byzantine-agreement]
sources:
  - paper: doi:10.1007/BFb0035753
    title: Piotr Berman and Juan A. Garay, Asymptotically optimal distributed consensus, ICALP 1989, Lecture Notes in Computer Science 372, Springer
    locator: "pages 80 to 94 (a protocol for n > 4t with 2t + 2 rounds and one-bit messages)"
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Section 5.2.4 (the two-round algorithm with n > 4f, which the book calls the phase king algorithm; the version on this page)
  - paper: "Piotr Berman, Juan A. Garay and Kenneth J. Perry, Towards optimal distributed consensus, 30th Annual Symposium on Foundations of Computer Science (FOCS), IEEE, 1989"
    locator: "pages 410 to 415 (protocols for n > 4t and for n > 3t)"
  - paper: doi:10.1007/BF01187072
    title: "Piotr Berman and Juan A. Garay, Cloture votes: n/4-resilient distributed consensus in t + 1 rounds, Mathematical Systems Theory 26(1), 1993"
    locator: the main theorem (n > 4t, t + 1 rounds, polynomial messages)
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine generals problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: the problem and the bound n > 3m for oral messages
---

The phase queen algorithm solves binary [Byzantine agreement](/consensus-problem/) in the [synchronous model](/synchronous-model/) without signatures when $n > 4t$. It runs $t + 1$ phases of only two rounds, and each message is one bit. In each phase one fixed process, the queen, sends its majority value, and a process that did not see a very strong majority takes the value of the queen. Berman and Garay gave it in 1989. It trades resilience for speed: the [phase king algorithm](/phase-king-algorithm/) needs one more round per phase but works for $n > 3t$.

## In plain words

A group of computers must agree on 0 or 1. Some of them are traitors that lie, and can tell different lies to different computers.

The work is cut into phases, and each phase has a leader, the queen. In a phase, each computer first tells everyone its value and finds the value that most computers sent. Then the queen tells everyone the value that she saw most. A computer that saw its majority value very many times keeps it. All others take the value of the queen.

There is one phase more than the number of traitors, so at least one queen is honest. In that phase all honest computers end with the same value. When the honest computers are more than four times the traitors, no traitor can change an agreed value again.

## The problem

There are $n$ processes $p_1, \ldots, p_n$ on a complete network of reliable, authenticated point-to-point links, so a receiver knows the true sender of each message. Messages are oral, as in the [oral messages model](/oral-messages-model/). The model is synchronous, with lock-step rounds. At most $t$ processes are [Byzantine](/byzantine-failure-model/), and the adversary is static and rushing. Each process $p_i$ has an input bit $x_i$. The algorithm must give agreement (all honest processes decide the same bit), [strong validity](/strong-validity/) (if all honest processes start with $v$, they decide $v$) and termination (every honest process decides). The problem is the same as on the [phase king](/phase-king-algorithm/) page; only the bound on $t$ is different.

## The algorithm

The code of process $p_i$ is below. A *broadcast* sends one message to each of the $n$ processes, $p_i$ included. The queen of phase $\varphi$ is $p_\varphi$. Counts are over different senders, and a missing message counts for no value.

```pseudo id=main
PHASE-QUEEN(i, x_i)                                  ▷ the code of p_i; n > 4t
L1  x ← x_i
L2  for φ ← 1 to t + 1 do
L3      round 1: broadcast x; receive one bit from each sender
L4               maj ← the bit received most often (0 on a tie); mult ← its count
L5      round 2: if i = φ then broadcast maj               ▷ p_φ is the queen
L6               if mult > n/2 + t then x ← maj
L7               else x ← the bit from p_φ, or 0 if none came
L8  decide x
```

The test of line L6 is strict. A process that passes it has seen its value from more than $n/2$ honest processes, so all such processes, and an honest queen, hold the same majority. The queen sends the value of line L4, not its value $x$ from the start of the phase.

## Example

Take $n = 5$, $t = 1$, with $p_1$ Byzantine, so the queen of phase 1 lies. The honest inputs are $x_2 = 0$, $x_3 = 0$, $x_4 = 1$, $x_5 = 1$. In every round, $p_1$ sends 1 to $p_2$ and $p_4$ and sends 0 to $p_3$ and $p_5$. A process keeps its majority at line L6 only if $mult > 5/2 + 1 = 3.5$, that is with 4 or 5 equal bits.

| phase | queen | process | bits got (0s, 1s) | maj | mult | queen says | x at end |
|---|---|---|---|---|---|---|---|
| 1 | $p_1$ (faulty) | $p_2$ | 2, 3 | 1 | 3 | 1 | 1 |
| 1 | $p_1$ (faulty) | $p_3$ | 3, 2 | 0 | 3 | 0 | 0 |
| 1 | $p_1$ (faulty) | $p_4$ | 2, 3 | 1 | 3 | 1 | 1 |
| 1 | $p_1$ (faulty) | $p_5$ | 3, 2 | 0 | 3 | 0 | 0 |
| 2 | $p_2$ | $p_2$ | 2, 3 | 1 | 3 | 1 | 1 |
| 2 | $p_2$ | $p_3$ | 3, 2 | 0 | 3 | 1 | 1 |
| 2 | $p_2$ | $p_4$ | 2, 3 | 1 | 3 | 1 | 1 |
| 2 | $p_2$ | $p_5$ | 3, 2 | 0 | 3 | 1 | 1 |

In phase 1 no count passes the test, and the faulty queen keeps the honest processes split. In phase 2 the queen $p_2$ is honest. It sends its majority 1, and every honest process takes it. All honest processes decide 1 after 4 rounds. The honest processes send 45 messages: 20 values in each phase and 5 queen messages in phase 2.

The bound matters. With $n = 4$, $t = 1$, all honest inputs 1 and $p_2$ faulty, $p_2$ sends 0 in round 1 of each phase. Each honest count is $3 = n/2 + t$, which does not pass the test, so every honest process follows the queen. The honest queen $p_1$ of phase 1 sends 1, but in phase 2 the faulty queen $p_2$ sends 0 to $p_1$ and $p_3$ and 1 to $p_4$. The honest processes decide 0, 0 and 1, so agreement and validity both fail.

## Correctness

The proof has four lemmas, and the full proof is below.

- **A strong count is an honest majority.** If an honest process passes the test of line L6 for $b$, more than $n/2 + t - t = n/2$ honest processes sent $b$.
- **Strong counts agree.** Two honest majorities cannot be for different bits.
- **An honest queen unifies.** The queen also sees more than $n/2$ copies of $b$, so its majority is $b$. Processes that pass the test keep $b$, and the others take $b$ from the queen.
- **Persistence.** If all honest processes hold $v$, each count of $v$ is at least $n - t$, and $n - t > n/2 + t$ exactly when $n > 4t$. So every honest process keeps $v$, whatever the queen says.

There are $t + 1$ queens and at most $t$ traitors, so some phase has an honest queen. After it all honest processes agree, and persistence keeps the agreement. Validity is persistence from the first phase. Only persistence uses $n > 4t$, and the second example shows that it fails at $n = 4t$.

## Complexity

The costs are in the synchronous model, for the worst case.

- **Rounds.** Exactly $2(t + 1)$, against $3(t + 1)$ for the phase king. The lower bound is $t + 1$ rounds, the [Byzantine round lower bound](/byzantine-round-lower-bound/).
- **Messages.** In each phase each honest process sends $n$ values and the queen sends $n$ more. So the honest processes send at most $(t + 1)(n^2 + n) = O(n^2 t)$ messages, and $\Theta(n^2 t)$ when all processes are honest.
- **Bits.** One bit per message besides the round number, so $O(n^2 t)$ bits in total.
- **Local work and space.** Two counters per round, so $O(1)$ space and $O(n)$ time per round.

## Properties

- **Deterministic.** No coins and no signatures.
- **Not optimally resilient.** It needs $n > 4t$, while the [Byzantine resilience bound](/byzantine-resilience-bound/) allows $n > 3t$. The phase king reaches $n > 3t$ with a third round.
- **One-bit messages.** The smallest possible message size.
- **Binary.** It decides one bit.
- **Not early stopping.** It always runs $t + 1$ phases.

## Variants and improvements

- **Phase king.** A round of proposals before the leader round lowers the bound to $n > 3t$, at the cost of $3(t + 1)$ rounds. See the [phase king algorithm](/phase-king-algorithm/). Attiya and Welch (Section 5.2.4) give the algorithm of this page under the name "phase king", so check the number of rounds per phase and the threshold in each source.
- **Optimal rounds with $n > 4t$.** Berman and Garay (1993, "Cloture votes") reach $t + 1$ rounds with $n > 4t$ and polynomial messages.
- **Randomized algorithms.** [Rabin's algorithm](/rabin-randomized-byzantine-agreement/) has the same shape: a round of values and a majority threshold, with the queen replaced by a common coin, and it decides in a constant expected number of rounds.

## When to use it

Use the phase queen algorithm when the network is synchronous, there are no signatures, and $n > 4t$ holds, so that the fewer rounds and one-bit messages are worth the lower resilience. It is also the simplest polynomial Byzantine agreement algorithm to teach, because each phase has one round of values and one round of a tie breaker. If only $n > 3t$ holds, use the [phase king algorithm](/phase-king-algorithm/).

## Pitfalls

- **Using it with $3t < n \le 4t$.** The test $mult > n/2 + t$ then fails also when all honest processes agree, and a faulty last queen splits them. The tests of the implementation show this for $n = 4t$ and for $n = 7$, $t = 2$.
- **A test that is not strict.** With $mult \ge n/2 + t$, two honest processes can pass the test for different bits.
- **The queen sends its old value.** The queen must send the majority of line L4. Its value from the start of the phase can differ from the bit that the other honest processes keep.
- **Counting messages instead of senders.** A sender counts once per round.

## Implementations

## History

Lamport, Shostak and Pease (1982) solved Byzantine agreement for $n > 3t$ in $t + 1$ rounds, with exponentially many messages. In 1989 Berman and Garay gave at ICALP a protocol for $n > 4t$ with $2t + 2$ rounds and one-bit messages, and in the same year Berman, Garay and Perry gave at FOCS protocols for $n > 4t$ and for $n > 3t$, the second one being the phase king. The names "phase king" and "phase queen" come from the process that breaks ties in each phase; textbooks and lecture notes do not use the names in the same way. In 1993 Berman and Garay reached $t + 1$ rounds with $n > 4t$.

## References
