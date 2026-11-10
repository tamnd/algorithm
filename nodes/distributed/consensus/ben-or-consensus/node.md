---
tag: G8VCBD
kind: algorithm
slug: ben-or-consensus
name: Ben-Or randomized consensus
aliases:
- Ben-Or algorithm
area: distributed/consensus
level: advanced
summary: Randomized asynchronous consensus that terminates with probability one.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, f: the largest number of crashes}
  time: {best: Θ(1), expected: O(2^n)}
  space: {extra: O(n)}
properties: {deterministic: false, recursive: false}
prereqs: [flp-impossibility, randomized-algorithm]
see_also: [rabin-randomized-byzantine-agreement, bracha-asynchronous-agreement, chandra-toueg-consensus, consensus-properties, las-vegas-algorithm, fair-coin-flipping, adaptive-adversary, crash-failure]
sources:
  - paper: doi:10.1145/800221.806707
    title: Michael Ben-Or, Another advantage of free choice, Completely asynchronous agreement protocols, PODC 1983
    locator: pages 27 to 30 (the protocol for crash failures with n > 2t, the protocol for Byzantine failures with n > 5t, and the expected number of rounds)
  - paper: doi:10.1007/s00446-012-0162-z
    title: Marcos K. Aguilera and Sam Toueg, The correctness proof of Ben-Or's randomized consensus algorithm, Distributed Computing 25(5), 2012
    locator: pages 371 to 381 (a full proof of safety and of termination with probability 1 against an adversary that sees the coins, and an example where a global coin prevents termination)
  - paper: doi:10.1145/3149.214121
    title: Michael J. Fischer, Nancy A. Lynch and Michael S. Paterson, Impossibility of distributed consensus with one faulty process, Journal of the ACM 32(2), 1985
    locator: pages 374 to 382 (the impossibility for deterministic protocols that randomization gets around)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 21, Section 21.3 (a randomized algorithm for agreement in an asynchronous network with stopping failures, the Ben-Or algorithm)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 14 (randomized consensus in asynchronous systems)
---

Ben-Or's algorithm (1983) is the first [randomized](/randomized-algorithm/) [consensus](/consensus-problem/) protocol for the [asynchronous model](/asynchronous-model/). It gets around the [FLP impossibility](/flp-impossibility/) with coin flips: it is always safe, and it terminates with probability 1. It solves binary consensus with $f$ [crash failures](/crash-failure/) when $n > 2f$, in rounds of two phases, and a version for Byzantine failures needs $n > 5f$. With a local coin at each process, the expected number of rounds can be exponential in $n$.

## In plain words

A group of computers must agree on 0 or 1. Messages can take any time, and some computers may stop. No fixed rule can always finish in this setting, so each computer is allowed to flip a coin.

The computers work in rounds. First, each one tells everyone its current value. If a computer sees that more than half of all computers hold the same value, it suggests that value. Then each computer listens to the suggestions. If enough of them name one value, it decides that value. If it sees at least one suggestion, it takes that value. If it sees none, it flips a coin.

Two suggestions can never differ, because two different majorities cannot exist. Once the coins all land on the same side, everyone agrees in the next round.

## The problem

There are $n$ processes on a complete network of reliable links. Process $p_i$ has an input $x_i \in \{0, 1\}$. At most $f$ processes can crash, with $n > 2f$, and a crash can stop a process in the middle of a broadcast. The model is the asynchronous model: there are no clocks, and messages take any finite time. The algorithm must give the [consensus properties](/consensus-properties/):

- **Agreement.** No two processes decide different values.
- **Validity.** If all inputs are $v$, every decision is $v$.
- **Termination.** Each correct process decides with probability 1.

Safety, which is agreement and validity, must hold in every run. Only termination is probabilistic, so the algorithm is of the [Las Vegas](/las-vegas-algorithm/) kind.

## The algorithm

The code of process $p_i$ is below. A *broadcast* sends a message to every process, $p_i$ included. Each process keeps the messages it gets, by kind and round, and the waits at lines L4 and L7 count messages from different senders.

```pseudo id=main
BEN-OR(i, x_i)                                ▷ the code of p_i; n > 2f
L1  x ← x_i; r ← 1
L2  loop
L3      broadcast (R, r, x)                     ▷ phase 1: report
L4      wait for n − f messages (R, r, ·)
L5      if more than n/2 of them carry the same v then broadcast (P, r, v)
L6      else broadcast (P, r, ?)                ▷ phase 2: propose
L7      wait for n − f messages (P, r, ·)
L8      if at least f + 1 of them carry the same v ≠ ? then decide v (once)
L9      if at least one of them carries a v ≠ ? then x ← v
L10     else x ← 0 or 1, each with probability 1/2
L11     r ← r + 1
```

Line L5 compares with $n/2$, not with $(n - f)/2$: a value must be held by a majority of *all* processes before it can be proposed. Line L8 needs $f + 1$ proposals, so that every other process sees at least one of them. A process that has decided stays in the loop, because the others need its messages to reach $n - f$ at lines L4 and L7.

## Example

Take $n = 3$, $f = 1$ and the inputs $x_1 = 0$, $x_2 = 1$, $x_3 = 1$. Each wait is for $n - f = 2$ messages, a proposal needs more than $1.5$ equal reports, so 2, and a decision needs $f + 1 = 2$ equal proposals. The adversary chooses which two messages each process uses.

| round | process | reports used | proposes | proposals used | result |
|---|---|---|---|---|---|
| 1 | $p_1$ | 0, 1 | ? | ?, 1 | $x = 1$ |
| 1 | $p_2$ | 1, 1 | 1 | 1, ? | $x = 1$ |
| 1 | $p_3$ | 0, 1 | ? | ?, ? | coin gives $x = 0$ |
| 2 | $p_1$ | 1, 1 | 1 | 1, ? | $x = 1$ |
| 2 | $p_2$ | 1, 0 | ? | ?, 1 | $x = 1$ |
| 2 | $p_3$ | 0, 1 | ? | ?, ? | coin gives $x = 1$ |
| 3 | all | 1, 1 | 1 | 1, 1 | decide 1 |

In rounds 1 and 2 only one process sees a majority, and the adversary hides its proposal from $p_3$, which flips a coin. In round 2 the coin of $p_3$ lands on 1, so all processes start round 3 with 1. Then every process sees only 1, proposes 1, gets two proposals 1 and decides 1.

## Correctness

The proof has three lemmas. The full proof is below.

- **One proposal value.** A process proposes $v$ only if more than $n/2$ processes reported $v$. Two values would need two disjoint sets of more than $n/2$ processes, so all proposals other than $?$ in a round carry one value.
- **A decision fixes the next round.** A decision on $v$ in round $r$ needs $f + 1$ proposals $v$. Every other process uses $n - f$ proposals and so misses at most $f$ senders, so it sees at least one $v$ and sets $x = v$. All processes start round $r + 1$ with $v$.
- **A common value decides.** If all processes start a round with $v$, every process gets $n - f > n/2$ reports $v$, every proposal is $v$, and $n - f \ge f + 1$ proposals $v$ make each process decide $v$.

Agreement follows: after the first decision on $v$, all start values are $v$ for ever, so every later decision is $v$. Validity follows from the third lemma in round 1. Every correct process completes every round, because at least $n - f$ processes are correct and decided processes keep sending.

For termination, at most one value $w$ can be proposed in a round. If all processes that flip a coin in round $r$ get $w$, or get the same value when nobody proposes, then all start round $r + 1$ with one value and decide in it. Against an adversary that does not see the coins, at most $n$ coins are flipped in a round and they are independent of $w$, so this happens with probability at least $2^{-n}$ in each round. So the algorithm terminates with probability 1. Aguilera and Toueg (2012) prove termination with probability 1 also against an adversary that sees the coins and the states, which needs a more careful argument, because a fast process may flip its coin before the start values of slow processes are fixed.

## Complexity

The costs are in asynchronous rounds and messages.

- **Rounds, best case.** If all inputs are equal, every correct process decides in round 1.
- **Rounds, expected.** Against an adversary that does not see the coins, the expected number of rounds until all correct processes decide is at most $2^n + 1$, from the bound $2^{-n}$ per round. With $f = \Theta(n)$, local coins give an expected number of rounds that is exponential in $n$ in the worst case. Ben-Or states that the expected number of rounds is constant when $f = O(\sqrt{n})$: the coins then give a majority that is larger than the $f$ values the adversary can hide.
- **Messages.** Each round sends two broadcasts per process, so $2n^2$ messages per round with messages to oneself, each of $O(\log r)$ bits.
- **Local space.** $O(n)$ for the messages of the current round. Messages of later rounds can arrive early and must be kept.

The table gives the mean number of rounds until the last correct process decides, over 200 seeded runs with inputs $0, 1, 0, 1, \ldots$, $f = \lfloor (n-1)/2 \rfloor$ and no crash. The random scheduler delivers a random message in transit. The split scheduler looks at the reports and tries to give each process a mix of values in phase 1, which forces coin flips. It is a simple adversary, not the worst one.

| $n$ | $f$ | random scheduler | split scheduler |
|---|---|---|---|
| 3 | 1 | 2.60 | 4.74 |
| 4 | 1 | 4.11 | 8.92 |
| 5 | 2 | 4.14 | 14.98 |
| 7 | 3 | 5.77 | 18.12 |
| 9 | 4 | 7.87 | 47.19 |

## Properties

- **Randomized, Las Vegas.** The output is always correct. Only the running time is random.
- **Optimal resilience.** $n > 2f$ is necessary for crash-tolerant consensus in the asynchronous model, also with randomization: with $n \le 2f$, two halves of the processes can each decide alone while the messages between them are slow.
- **Local coins.** Each process flips its own coin. No shared randomness, no cryptography and no failure detector is used.
- **Uniform agreement.** A process that decides and then crashes decided the common value.
- **Binary.** The algorithm decides one bit. Multi-valued consensus needs an extra reduction.

## Variants and improvements

- **Byzantine version.** Ben-Or's paper also gives a version for [Byzantine failures](/byzantine-failure-model/) with $n > 5f$, with thresholds that account for lying processes.
- **Optimal Byzantine resilience.** [Bracha's algorithm](/bracha-asynchronous-agreement/) (1987) reaches $n > 3f$ by running Ben-Or's rounds over [reliable broadcast](/bracha-reliable-broadcast/), which stops a faulty process from sending different values to different processes.
- **Common coin.** [Rabin's algorithm](/rabin-randomized-byzantine-agreement/) (1983) uses a coin that all processes see the same, dealt in advance, and terminates in a constant expected number of rounds. Later protocols build the common coin with [cryptography](/fair-coin-flipping/).
- **Early decision.** A process can stop sending after it decides if it first broadcasts a final message, so that the others can count it in later rounds.

## When to use it

Use Ben-Or's algorithm to teach how randomization gets around FLP, or when a protocol must not depend on any timing assumption at all. For a small group and a crash model it is simple and correct. For larger groups with $f$ close to $n/2$, the expected time with local coins is too long, and a common coin or a timing based protocol such as [Paxos](/paxos/) or [Chandra-Toueg](/chandra-toueg-consensus/) is better. Modern asynchronous Byzantine protocols keep its round structure and replace the local coin with a threshold signature coin.

## Pitfalls

- **Counting a majority of the received messages.** Line L5 needs more than $n/2$ of all processes, not more than half of the $n - f$ received. With the weaker test two values can be proposed in one round, and agreement breaks.
- **Halting after the decision.** A process that decides and stops sending can leave the others below $n - f$ messages for ever, because the halted process counts against $f$.
- **A shared coin used naively.** Aguilera and Toueg show that if the local coins are replaced with one global coin, the algorithm may not terminate. A common coin helps only in protocols built for it, such as Rabin's.
- **Proving termination too quickly.** The simple argument "all coins equal $w$ with probability $2^{-n}$" assumes that $w$ is fixed before the coins are flipped. Against an adversary that sees the coins this is not true, and the full proof needs more care.
- **Expecting speed.** With $f$ close to $n/2$ and an adversary that splits the reports, the expected number of rounds grows quickly with $n$, as the table shows.

## Implementations

## History

Fischer, Lynch and Paterson presented their impossibility result in 1983. In the same year Ben-Or showed at PODC that randomization gets around it, and Rabin showed that a common coin dealt in advance gives a constant expected time. Bracha (1987) raised the Byzantine resilience to the optimal $n > 3f$. Aguilera and Toueg wrote a full proof of Ben-Or's algorithm against a strong adversary in a 1998 technical report, published in 2012, which they describe as the first full proof of the algorithm. The algorithm has also become a test case for the automatic verification of randomized distributed algorithms.

## References
