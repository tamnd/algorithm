---
tag: EHN65V
kind: algorithm
slug: dolev-strong-algorithm
name: Dolev-Strong algorithm
aliases:
- Dolev-Strong broadcast
- Dolev-Strong protocol
area: distributed/byzantine-agreement
level: advanced
summary: Authenticated Byzantine broadcast for any t < n faults in t + 1 rounds, with O(n^2) messages from correct processes. A value counts in round r only with r distinct signatures.
solves: [byzantine-broadcast]
model: signed-messages-model
complexity:
  vars: {n: the number of processes, t: the largest number of Byzantine processes}
  time: {worst: Θ(t), best: Θ(t)}
  messages: {worst: O(n^2), best: Θ(n^2)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [byzantine-broadcast, signed-messages-model, signature-chain]
see_also: [signed-messages-algorithm, oral-messages-algorithm, byzantine-round-lower-bound, authenticated-resilience-bound, dolev-reischuk-lower-bound, interactive-consistency, floodset, threshold-signature]
sources:
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (the t + 1 phase authenticated algorithms, the O(nt) message version, and the t + 1 round lower bound)
  - url: https://elaineshi.com/docs/blockchain-book.pdf
    title: Elaine Shi, Foundations of Distributed Consensus and Blockchains, book draft
    locator: Chapter 3, Section 3.4 (the Dolev-Strong protocol with the extracted set and r signatures in round r)
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 4 (Algorithm SM(m), the base of the algorithm)
  - paper: doi:10.1145/2455.214112
    title: Danny Dolev and Rüdiger Reischuk, Bounds on information exchange for Byzantine agreement, Journal of the ACM 32(1), 1985
    locator: pages 191 to 204 (lower bounds on messages and signatures)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 3 (Byzantine broadcasts) and Chapter 5 (Byzantine consensus)
---

The Dolev-Strong algorithm solves [Byzantine broadcast](/byzantine-broadcast/) in the [signed messages model](/signed-messages-model/) for any number $t < n$ of Byzantine processes, in $t + 1$ synchronous rounds. A value counts in round $r$ only if it arrives with a [signature chain](/signature-chain/) of $r$ distinct signatures that starts with the sender. Each correct process keeps the set of values it has *extracted*, relays only the first two of them, and at the end outputs the value if there is exactly one. Its $t + 1$ rounds match the [round lower bound](/byzantine-round-lower-bound/), and it is the standard base for authenticated broadcast and agreement.

## In plain words

One computer, the sender, must give a value to all the others. Some computers, maybe the sender too, are dishonest. Every computer can sign, and nobody can copy a signature of an honest computer.

The sender signs its value and sends it. When a computer gets a new value with enough signatures, it keeps it, signs it too and sends it to everyone. "Enough" grows by one each round, so a dishonest group cannot hold a value back and show it to one honest computer at the very end: by then it needs more signatures than there are dishonest computers, so an honest one has already signed it and sent it to all.

At the end, a computer that kept exactly one value outputs it. A computer that kept two or more outputs a fixed default.

## The problem

There are $n$ processes $0, \ldots, n - 1$ in the [synchronous model](/synchronous-model/) on a complete network of reliable authenticated links. Process 0 is the sender with an input $b$ from a value set $V$. At most $t$ processes are [Byzantine](/byzantine-failure-model/), for any $t < n$, and they may include the sender. The adversary controls all faulty processes together, it is static (the faulty set is fixed before the run) and rushing (in a round it sees the correct messages before it sends its own). It has the signing keys of the faulty processes and can sign anything in their names, but it cannot make a signature of a correct process, as in [existential unforgeability](/existential-unforgeability/).

The algorithm must give:

- **Agreement.** All correct processes output the same value.
- **Validity.** If the sender is correct, every correct process outputs $b$.
- **Termination.** Every correct process outputs a value at the end of round $t + 1$.

These are IC1 and IC2 of Lamport, Shostak and Pease, with termination at a fixed round.

## The algorithm

Write $v{:}0{:}j_1{:}\cdots{:}j_{r-1}$ for the value $v$ signed by the sender 0 and then in turn by $j_1, \ldots, j_{r-1}$, where each signature covers the value and all earlier signatures. Each process $i$ keeps the extracted set $\text{EXTR}_i$, empty at the start, and $\bot$ is a fixed default value.

```pseudo id=main
DOLEV-STRONG(i)                     ▷ the code of process i; process 0 is the sender with input b
L1  if i = 0 then EXTR ← {b}; sign b and send b:0 to all others in round 1
L2  for r ← 1 to t + 1 do                                              ▷ lock-step rounds
L3      for each message v:0:j_1:…:j_{r−1} that i receives in round r do
L4          if the r names 0, j_1, …, j_{r−1} are not distinct then ignore it
L5          if a signature is not valid, or v ∈ EXTR, then ignore it
L6          add v to EXTR
L7          if r ≤ t and |EXTR| ≤ 2 then
L8              sign it, which gives v:0:j_1:…:j_{r−1}:i
L9              send it in round r + 1 to every process not among 0, j_1, …, j_{r−1}, i
L10 if EXTR = {v} then output v else output ⊥
```

Line L4 is the key rule: a value extracted in round $r$ carries $r$ distinct signatures. Line L7 relays only the first two values. A correct process only needs to know whether its set has one value or more, and two relayed values are enough to tell every other correct process that the set has more than one. With line L7 replaced by "if $r \le t$", the algorithm is still correct, but a faulty sender that signs many values makes the correct processes send many more messages.

## Example

Take $n = 5$ and $t = 3$. The sender 0 and processes 3 and 4 are faulty, and 1 and 2 are correct. The default is $\bot = 0$.

| round | what happens | $\text{EXTR}_1$ | $\text{EXTR}_2$ |
|---|---|---|---|
| 1 | 0 sends $1{:}0$ to 1 and 2. It also signs $2{:}0$ and gives it only to 3 and 4 | {1} | {1} |
| 2 | 1 sends $1{:}0{:}1$ to 2, 3, 4, and 2 sends $1{:}0{:}2$ to 1, 3, 4 | {1} | {1} |
| 3 | 3 and 4 both sign, and send $2{:}0{:}3{:}4$, with 3 signatures, only to 1 | {1, 2} | {1} |
| 4 | 1 has $r = 3 \le t$ and a second value, so it sends $2{:}0{:}3{:}4{:}1$ to 2 | {1, 2} | {1, 2} |

Both correct processes output $\bot$, so agreement holds. The correct processes send 7 messages with 16 signatures, and the largest message has 4 signatures. If the algorithm stopped after $t = 3$ rounds, process 1 would output $\bot$ and process 2 would output 1. The faulty processes hold the second value back until round $t$, the last round in which they can still give it the $t$ signatures it needs, and then show it to only one correct process. In round $t + 1$ a value needs $t + 1$ signatures, more than the faulty processes can give, so this attack only works with $t$ rounds.

With no faulty process, $n = 5$ and $t = 3$, the sender sends 4 messages and each other process relays once to 3 others, so the run has $4 + 4 \cdot 3 = 16 = (n - 1)^2$ messages and 28 signatures.

## Correctness

The proof rests on one lemma: if a correct process $i$ extracts a value $v$ as one of its first two values, then every correct process extracts $v$ by the end of round $t + 1$.

- If $i$ extracts $v$ in round $r \le t$, it signs and sends $v$ in round $r + 1$ to every process not on the chain, with $r + 1$ distinct signatures. Each correct process off the chain extracts $v$ then. A correct process on the chain signed $v$, so it extracted $v$ before.
- If $i$ extracts $v$ in round $t + 1$, the chain has $t + 1$ distinct signers, so one of them, $k$, is correct. $k$ only signs a value it relays, so it extracted $v$ as one of its first two values in a round $r \le t$ and sent it to all processes not yet on the chain. The first case applies to $k$.

Agreement follows: if $\text{EXTR}_i = \{v\}$ for a correct $i$, every correct $j$ has $v$, and if $j$ had a second value, the lemma for $j$ would put it in $\text{EXTR}_i$. So either all correct sets are $\{v\}$, or all have at least two values. Validity: a correct sender signs only $b$, so every valid chain carries $b$. The full proof is below.

## Complexity

The costs are for the synchronous model.

- **Rounds.** Exactly $t + 1$ in every run. This matches the [round lower bound](/byzantine-round-lower-bound/), which holds also with signatures when $t \le n - 2$.
- **Messages.** The correct sender sends $n - 1$ messages. Every other correct process relays at most 2 values, each to at most $n - 2$ processes. So the correct processes send at most $(n - 1) + 2(n - 1)(n - 2) = O(n^2)$ messages, whatever the faulty ones do. With no faults the count is exactly $(n - 1)^2$. In the tests the largest count over all strategies for $n \le 6$ was 0.8 of the bound.
- **Signatures.** A message carries at most $t + 1$ signatures, so the correct processes send $O(n^2 t)$ signatures, and $O(n^2 t \kappa)$ bits for signatures of $\kappa$ bits. With [aggregate](/aggregate-signature/) or [multi-signatures](/threshold-signature/), a chain fits in one signature plus a list of signers.
- **Local space.** $\text{EXTR}$ needs at most 2 values to decide, so the extra space is $O(1)$ values besides the messages in transit.

Dolev and Strong state in their abstract that their best algorithm uses $t + 1$ phases and $O(nt)$ messages, so the $O(n^2)$ count of the simple version above is not optimal when $t$ is small. The [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/) shows that $\Omega(n + t^2)$ messages and $\Omega(nt)$ signatures are needed in the worst case by every deterministic authenticated algorithm.

## Properties

- **Deterministic.** No coins.
- **Any $t < n$.** It needs no honest majority. For $t = n - 1$ the problem is trivial, because at most one process is correct.
- **Round optimal.** $t + 1$ rounds, which no deterministic algorithm can beat in the worst case when $t \le n - 2$.
- **Not early stopping.** It runs $t + 1$ rounds even with no faults. Early stopping versions decide in $\min(f + 2, t + 1)$ rounds, where $f$ is the real number of faults.
- **Synchronous only.** A message that arrives a round late is ignored by line L4. In an [asynchronous](/asynchronous-model/) network, no deterministic broadcast is possible with even one crash, by the [FLP theorem](/flp-impossibility/).

## Variants and improvements

- **Signed messages algorithm.** The [SM(m) algorithm](/signed-messages-algorithm/) of Lamport, Shostak and Pease is the same idea for a commander and lieutenants, but each lieutenant relays every new value, so its message count depends on how many values a traitor signs.
- **Interactive consistency and consensus.** Running $n$ copies in parallel gives [interactive consistency](/interactive-consistency/) in $t + 1$ rounds for any $t < n$. Deciding the majority of the vector gives consensus with [strong validity](/strong-validity/) when $n > 2t$, which is the best possible by the [authenticated resilience bound](/authenticated-resilience-bound/). Deciding the value of a fixed process gives consensus with [weak validity](/weak-validity/) for any $t < n$.
- **Fewer messages.** Dolev and Strong give a version with $O(nt)$ messages. The Dolev-Reischuk bound shows that some quadratic term in $t$ cannot be avoided by deterministic algorithms.
- **Randomized versions.** Randomization can reduce the expected number of rounds when a majority is honest. Abraham et al. (2019) show that $\Omega(t^2)$ messages are still needed in expectation against a strongly adaptive adversary.

## When to use it

Use Dolev-Strong when the network is synchronous with a known bound on delay, signatures and a public key setup are available, and the system must tolerate any number of faulty processes, including a majority. It is a common subroutine in theory, for example to give a synchronous broadcast channel in secure multiparty computation. When the network is only partially synchronous, $t + 1$ fixed rounds are not safe, and a protocol for [partial synchrony](/partial-synchrony/) with $n \ge 3t + 1$, such as [PBFT](/pbft/) or [HotStuff](/hotstuff/), is the usual choice. Without signatures use the [oral messages algorithm](/oral-messages-algorithm/) or [phase king](/phase-king-algorithm/), with $n > 3t$.

## Pitfalls

- **Counting signatures and not signers.** A chain with $r$ signatures from fewer than $r$ processes lets the faulty processes delay a value past the point where a correct signer must exist. Line L4 counts distinct names.
- **Only $t$ rounds.** The example shows that $t$ rounds let the faulty processes reach one correct process in the last round with a value that nobody can pass on.
- **Relaying only one value.** If a process relays only its first value, another correct process can stay with one value while this one has two. Two relays are needed, because a correct process must learn that a set has more than one value.
- **Accepting short chains late.** A value that arrives in round $r$ with fewer than $r$ signatures must be ignored. Otherwise a value delivered in round $t + 1$ with one signature can reach only one correct process.
- **Signatures without context.** In a system that runs many broadcasts, a signature must cover the instance (the sender and a session id) and the round. Otherwise a chain from one instance can be replayed in another.

## Implementations

## History

Dolev and Strong published the algorithm in 1983 in "Authenticated algorithms for Byzantine agreement", building on the SM(m) algorithm of Lamport, Shostak and Pease. The same paper proves that $t + 1$ rounds are necessary for any algorithm, with or without signatures. Dolev and Reischuk (1985) proved the matching lower bounds on messages and signatures, and Abraham, Chan, Dolev, Nayak, Pass, Ren and Shi (2019) revisited them for randomized protocols. The version with the extracted set and the "relay at most two" rule is the form used in many lecture notes and in Shi's book.

## References
