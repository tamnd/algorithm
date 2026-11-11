---
tag: X0W0EG
kind: model
slug: oral-messages-model
name: Oral messages model
aliases:
- oral messages
- unauthenticated messages
area: distributed/byzantine-agreement
level: core
summary: "Synchronous Byzantine model of Lamport, Shostak and Pease: messages arrive, the receiver knows the sender, and missing messages are seen, but nobody can prove what they received."
prereqs: [byzantine-failure-model, synchronous-model]
see_also: [signed-messages-model, oral-messages-algorithm, byzantine-resilience-bound, byzantine-round-lower-bound, phase-king-algorithm, dolev-reischuk-lower-bound, byzantine-broadcast, vertex-connectivity]
sources:
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 3 (oral messages and assumptions A1 to A3, page 387), Section 5 (missing communication paths) and Section 6 (how A1 to A3 are met in a real system)
  - paper: doi:10.1145/322186.322188
    title: Marshall Pease, Robert Shostak and Leslie Lamport, Reaching Agreement in the Presence of Faults, Journal of the ACM 27(2), 1980
    locator: pages 228 to 234 (the unauthenticated case, with the bound n >= 3m + 1)
  - paper: doi:10.1007/BF01843568
    title: Michael J. Fischer, Nancy A. Lynch and Michael Merritt, Easy impossibility proofs for distributed consensus problems, Distributed Computing 1(1), 1986
    locator: pages 26 to 39 (the axioms of a model in which a faulty process can mimic any correct behavior, and the scenario proofs in it)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6, Sections 6.3 to 6.5 (Byzantine agreement in synchronous networks without authentication)
---

The oral messages model is the synchronous model of Byzantine agreement without signatures. Lamport, Shostak and Pease (1982) defined an *oral message* as one whose contents are completely under the control of the sender, and they listed three assumptions: every message is delivered correctly, the receiver knows who sent it, and a missing message can be detected. A faulty process can say anything, but it cannot pretend to be someone else on a link. What it cannot be caught at is lying about what others told it, because an oral message carries no proof. This one weakness costs a lot: [Byzantine broadcast](/byzantine-broadcast/) needs $n > 3t$ processes in this model, while with signatures any $t < n$ is enough.

## The machine

**Network.** There are $n$ processes, and each pair is joined by a private two-way link, so the network is the complete graph $K_n$. The processes know $n$ and each other's names. The system runs in the [synchronous model](/synchronous-model/): in each round, each process sends at most one message on each link, then receives all messages sent to it in the round, then changes state.

**Assumptions of Lamport, Shostak and Pease.**

- **A1.** Every message that is sent is delivered correctly.
- **A2.** The receiver of a message knows who sent it.
- **A3.** The absence of a message can be detected.

A1 rules out lost or changed messages on links, so all faults are process faults. A2 rules out a faulty process that sends in the name of another one. A3, with synchronous rounds, lets a process replace a missing message with a default value, so a faulty process cannot block progress by silence.

**Faults.** At most $t$ processes are [Byzantine](/byzantine-failure-model/). A faulty process may send any message on any of its links in any round, including different messages to different processes and messages about what it claims to have received. The faulty processes act together.

**What is missing.** There are no signatures. When $q$ tells $p$ "$r$ told me $v$", $p$ knows that $q$ said it, by A2, but it has no way to check that $r$ said $v$. Fischer, Lynch and Merritt capture this as a *locality* and *fault* axiom: a faulty process can send to each neighbor any message that some correct process could send to that neighbor in some other system. This is all their hexagon proofs need.

**A real system.** LSP, Section 6, explain how to meet the assumptions. A1 and A2 come from fixed, direct lines between the processors, so that a faulty processor cannot inject messages on the line between two others. A3 comes from synchronized clocks and a time-out: a message not received by a known time counts as absent.

## What it counts

- **Resilience.** The largest number $t$ of faulty processes for $n$ processes. In this model the answer is $t < n/3$ for every agreement problem.
- **Rounds.** The number of synchronous rounds until all correct processes decide, in the worst case over inputs and fault patterns.
- **Messages and bits.** The number of messages sent by correct processes, and sometimes their total size in bits. Messages of faulty processes are not counted.
- **Local computation** is free, but algorithms whose local work is exponential, such as [OM(m)](/oral-messages-algorithm/), are noted as such.

## Relation to other models

- **[Signed messages model](/signed-messages-model/).** Adds assumption A4: a correct process's signature cannot be forged, and anyone can check it. A faulty process then cannot lie about what a correct one sent. Every algorithm for the oral model works in the signed model, and every lower bound for the signed model holds in the oral model.
- **"Authenticated channels" in cryptography.** In cryptographic papers, the oral model is often called the model with *authenticated channels*, since A2 is the authentication of each link. It is not "authenticated Byzantine agreement", which means the signed model.
- **Crash and omission faults.** If the faulty processes may only crash or omit messages, the oral model allows any $t < n$ for synchronous consensus, as in [FloodSet](/floodset/).
- **General graphs.** If the network is not complete, A2 holds only on the links that exist. Then the [vertex connectivity](/vertex-connectivity/) of the graph must be at least $2t + 1$, in addition to $n > 3t$ (Dolev, 1982).
- **Weaker timing.** Without synchrony, A3 fails: a missing message may be slow. In the [asynchronous model](/asynchronous-model/) with the same kind of links, [Byzantine reliable broadcast](/byzantine-reliable-broadcast/) and randomized agreement such as [Bracha's](/bracha-asynchronous-agreement/) still work for $n > 3t$.

## Known results in the model

**Processes.** Byzantine broadcast, [interactive consistency](/interactive-consistency/) and consensus with [strong validity](/strong-validity/) or [weak validity](/weak-validity/) are solvable if and only if $n > 3t$. Pease, Shostak and Lamport (1980) proved this for interactive consistency, and Fischer, Lynch and Merritt (1986) gave the short hexagon proofs. See the [Byzantine resilience bound](/byzantine-resilience-bound/). The same bound holds for approximate agreement and clock synchronization.

**Rounds.** Every deterministic algorithm needs $t + 1$ rounds in some run, for $t \le n - 2$. See the [Byzantine round lower bound](/byzantine-round-lower-bound/).

**Messages.** Without signatures, every deterministic algorithm sends $\Omega(nt)$ messages in some run (Dolev and Reischuk, 1985). See the [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/).

**Algorithms.**

| Algorithm | Problem | Processes | Rounds | Messages |
| --- | --- | --- | --- | --- |
| [OM(m)](/oral-messages-algorithm/) | broadcast | $n > 3t$ | $t + 1$ | $O(n^{t+1})$ |
| [Phase king](/phase-king-algorithm/) | binary consensus | $n > 3t$ | $3(t + 1)$ | $O(n^2 t)$ |
| [Phase queen](/phase-queen-algorithm/) | binary consensus | $n > 4t$ | $2(t + 1)$ | $O(n^2 t)$ |
| Garay and Moses 1998 | consensus | $n > 3t$ | $t + 1$ | polynomial |
| [Feldman and Micali](/feldman-micali-byzantine-agreement/), randomized | consensus | $n > 3t$ | expected $O(1)$ | polynomial |

OM(m) meets the bounds on processes and rounds, but not on messages. Garay and Moses meet all three up to polynomial factors in messages.

## References
