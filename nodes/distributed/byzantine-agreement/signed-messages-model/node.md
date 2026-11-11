---
tag: E8RB2Y
kind: model
slug: signed-messages-model
name: Signed messages model
aliases:
- authenticated messages
- signed messages
- authenticated Byzantine model
area: distributed/byzantine-agreement
level: core
summary: "The oral messages model plus unforgeable signatures (A4): a faulty process cannot forge or alter what a correct process signed, and anyone can check a signature."
prereqs: [oral-messages-model, digital-signature]
see_also: [signature-chain, signed-messages-algorithm, dolev-strong-algorithm, authenticated-resilience-bound, dolev-reischuk-lower-bound, threshold-signature, quorum-certificate, byzantine-round-lower-bound]
sources:
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 4 (assumption A4 and signed messages, page 390) and Section 6 (signatures in a real system with a small probability of forgery)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (the authenticated model, polynomial algorithms and the t + 1 round lower bound)
  - paper: doi:10.1145/2455.214112
    title: Danny Dolev and Rüdiger Reischuk, Bounds on information exchange for Byzantine agreement, Journal of the ACM 32(1), 1985
    locator: pages 191 to 204 (lower bounds on signatures and messages in the authenticated model)
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: Section 1, Table 1 (authenticated Byzantine faults as a fault class, and the bounds for it)
---

The signed messages model is the oral messages model with digital signatures. Lamport, Shostak and Pease (1982) added one assumption, A4: a correct process's signature cannot be forged, any change to a signed message can be detected, and anyone can check a signature. A faulty process can still sign anything with its own key and say different things to different processes. But it can no longer lie about what a correct process said, because a claim "$r$ told me $v$" must carry $r$'s signature on $v$. This makes [Byzantine broadcast](/byzantine-broadcast/) solvable for any number of faults $t < n$, while the [oral messages model](/oral-messages-model/) needs $n > 3t$.

## The machine

**Network and timing.** As in the oral messages model: $n$ processes on a complete network of reliable links, synchronous rounds, and assumptions A1 to A3. At most $t$ processes are [Byzantine](/byzantine-failure-model/), and they act together.

**Assumption A4 of Lamport, Shostak and Pease.**

- **A4 (a).** A loyal general's signature cannot be forged, and any alteration of the contents of his signed messages can be detected.
- **A4 (b).** Anyone can verify the authenticity of a general's signature.

**Signatures as tokens.** For proofs, a signature is an abstract token $\langle m \rangle_p$, meaning "$p$ signed $m$". A correct process $p$ creates $\langle m \rangle_p$ only when its algorithm says so. A faulty process can create $\langle m \rangle_q$ for any $m$ and any faulty $q$, since the faulty processes share their keys. Any process can copy a token it has received and send it on. No process can create $\langle m \rangle_p$ for a correct $p$ that did not sign $m$. The implementations on the algorithm pages keep a set of issued pairs $(p, m)$: only the code of a correct process, or the adversary for a faulty one, can add to it, and checking a signature is a lookup.

**Relayed messages.** A process that passes on a signed value adds its own signature, which gives a [signature chain](/signature-chain/): "$v$ signed by $s$, then by $q$, then by $r$". LSP write it as $v{:}s{:}q{:}r$.

**Keys.** Every process has a key pair, and every process knows the public keys of all others before the run starts. This setup is itself a form of agreement, and the model takes it as given, as a *public key infrastructure*.

**A real system.** LSP, Section 6, note that real signatures can be forged with some small probability. With [digital signatures](/digital-signature/) the model holds against an adversary with bounded computing power, except with negligible probability. The proofs in the model then give results that hold with high probability.

## What it counts

- **Resilience.** The largest number $t$ of faulty processes. In this model it depends on the problem: any $t < n$ for broadcast, and $t < n/2$ for consensus with strong validity.
- **Rounds.** As in the oral model.
- **Messages and signatures.** Messages sent by correct processes, and the number of signatures that correct processes create or send. Signing and checking cost much more than other local work, so Dolev and Reischuk count signatures as a separate measure.
- **Message size.** A chain of $k$ signatures has size $O(k)$ signatures. [Threshold signatures](/threshold-signature/) and multisignatures shrink a set of signatures on one message to the size of one.

## Relation to other models

- **Oral messages model.** The signed model gives faulty processes less power. So every algorithm for the oral model works here, and every lower bound proved here holds in the oral model.
- **Fault classes.** Dwork, Lynch and Stockmeyer call this class of faults *authenticated Byzantine*. It lies between omission faults and Byzantine faults: an omission fault never forges, and an authenticated Byzantine fault forges nothing of a correct process.
- **Weaker timing.** In [partial synchrony](/partial-synchrony/) and in the asynchronous model, signatures do not lower the bound $n > 3t$ for consensus. They are still used there for efficiency: a [quorum certificate](/quorum-certificate/), a set of $n - t$ signatures on one message, lets one process prove to others what a quorum said. [PBFT](/pbft/) can use message authentication codes instead, but [HotStuff](/hotstuff/) uses signatures to get linear messages per view.
- **General graphs.** LSP, Theorem 4: if the correct processes form a connected subgraph of diameter $d$, then SM($t + d - 1$) solves broadcast. So the connectivity bound $2t + 1$ of the oral model is replaced by the condition that the correct processes stay connected, which holds for every set of $t$ faults when the vertex connectivity is at least $t + 1$.

## Known results in the model

**Processes.**

- Byzantine broadcast and [interactive consistency](/interactive-consistency/) are solvable for any $t < n$ (Pease, Shostak and Lamport, 1980).
- Consensus with [weak validity](/weak-validity/) is solvable for any $t < n$.
- Consensus with [strong validity](/strong-validity/) is solvable if and only if $n > 2t$. See the [authenticated resilience bound](/authenticated-resilience-bound/).

**Rounds.** Every deterministic algorithm needs $t + 1$ rounds in some run, for $t \le n - 2$, no matter what message types are allowed (Dolev and Strong, 1983). See the [Byzantine round lower bound](/byzantine-round-lower-bound/).

**Messages and signatures.** Every deterministic algorithm sends $\Omega(n + t^2)$ messages and $\Omega(nt)$ signatures in some run. See the [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/).

**Algorithms.**

| Algorithm | Problem | Faults | Rounds | Messages |
| --- | --- | --- | --- | --- |
| [SM(m)](/signed-messages-algorithm/) | broadcast | any $t < n$ | $t + 1$ | $O(n^2 d)$ for $d$ signed values |
| [Dolev-Strong](/dolev-strong-algorithm/) | broadcast | any $t < n$ | $t + 1$ | $O(n^2)$ |
| $n$ parallel Dolev-Strong and majority | consensus | $n > 2t$ | $t + 1$ | $O(n^3)$ |
| Katz and Koo 2006, randomized | consensus | $n > 2t$ | expected $O(1)$ | polynomial |

## References
