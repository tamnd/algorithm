---
tag: 6D0YW3
kind: algorithm
slug: oblivious-transfer-extension
name: Oblivious transfer extension
aliases:
- IKNP extension
- OT extension
area: cryptography/protocols
level: research
summary: Turn κ base oblivious transfers into millions of OTs with only hashing. IKNP reverses the roles in the base OTs, transposes a bit matrix, and hashes its rows.
solves: [secure-multiparty-computation]
model: word-ram
complexity:
  vars: {m: the number of transfers, k: the security parameter and number of base OTs, l: the message length}
  time: {worst: Θ(m (k + l)), average: Θ(m (k + l)), best: Θ(m (k + l))}
  space: {extra: Θ(m k)}
properties: {deterministic: false, randomized: true}
history:
  year: 2003
  people: [Yuval Ishai, Joe Kilian, Kobbi Nissim, Erez Petrank]
  note: Beaver showed in 1996 that OTs can be extended. Ishai, Kilian, Nissim and Petrank gave the practical protocol at CRYPTO 2003, and Keller, Orsini and Scholl made it secure against malicious receivers in 2015.
prereqs: [oblivious-transfer, random-oracle-model]
see_also: [gmw-protocol, yao-garbled-circuits, private-set-intersection, malicious-adversary-model, pseudorandom-generator, learning-parity-with-noise, semi-honest-model, cut-and-choose]
sources:
  - paper: doi:10.1007/978-3-540-45146-4_9
    title: "Yuval Ishai, Joe Kilian, Kobbi Nissim and Erez Petrank, Extending oblivious transfers efficiently, CRYPTO 2003, LNCS 2729, pages 145 to 161"
    locator: the protocol with reversed base OTs and the bit matrix, and its security with a random oracle or a correlation-robust hash
  - paper: doi:10.1145/237814.237996
    title: "Donald Beaver, Correlated pseudorandomness and the complexity of private computations, STOC 1996, pages 479 to 489"
    locator: the first OT extension, by a secure computation of a PRG on a few seeds
  - paper: doi:10.1007/978-3-662-47989-6_35
    title: "Marcel Keller, Emmanuela Orsini and Peter Scholl, Actively secure OT extension with optimal overhead, CRYPTO 2015, LNCS 9215, pages 724 to 741"
    locator: the consistency check on random linear combinations of rows over a field of size 2 to the κ
  - paper: "Gilad Asharov, Yehuda Lindell, Thomas Schneider and Michael Zohner, More efficient oblivious transfer and extensions for faster secure computation, CCS 2013, pages 535 to 548"
    locator: the optimized semi-honest IKNP with random and correlated OT
  - paper: "Vladimir Kolesnikov and Ranjit Kumaresan, Improved OT extension for transferring short secrets, CRYPTO 2013, LNCS 8043, pages 54 to 70"
    locator: 1-out-of-n OT extension with a code in place of the repetition code
  - paper: "Elette Boyle, Geoffroy Couteau, Niv Gilboa, Yuval Ishai, Lisa Kohl and Peter Scholl, Efficient two-round OT extension and silent non-interactive secure computation, CCS 2019"
    locator: silent OT extension from LPN, with a short seed exchange
  - paper: "Elette Boyle, Geoffroy Couteau, Niv Gilboa, Yuval Ishai, Lisa Kohl and Peter Scholl, Efficient pseudorandom correlation generators, silent OT extension and more, CRYPTO 2019"
    locator: pseudorandom correlation generators for OT and vector OLE
  - paper: doi:10.1561/3300000019
    title: "David Evans, Vladimir Kolesnikov and Mike Rosulek, A pragmatic introduction to secure multi-party computation, Foundations and Trends in Privacy and Security 2(2-3), 2018"
    locator: Section 3.7 (oblivious transfer and OT extension)
---

Oblivious transfer extension turns a small number of [oblivious transfers](/oblivious-transfer/), about $\kappa = 128$, into as many OTs as needed, with only a hash function and a pseudorandom generator. A base OT needs public-key cryptography and costs about a millisecond; an extended OT costs a few hash calls. Since [GMW](/gmw-protocol/) needs OTs for every AND gate and [Yao's garbled circuits](/yao-garbled-circuits/) need one for every input bit of the evaluator, extension is what makes these protocols practical. This page gives the protocol of Ishai, Kilian, Nissim and Petrank (2003), called IKNP, for [semi-honest](/semi-honest-model/) parties, proves it correct, and shows the attack by a cheating receiver that the malicious version of Keller, Orsini and Scholl (2015) blocks.

**Notation.** The sender has $m$ pairs $(x_j^0, x_j^1)$ of $\ell$-bit strings. The receiver has choice bits $r = (r_1, \ldots, r_m)$. $\kappa$ is the security parameter. $G$ is a pseudorandom generator from $\kappa$-bit seeds to $\{0,1\}^m$, and $H$ is a hash function modelled as a [random oracle](/random-oracle-model/). Columns of an $m \times \kappa$ bit matrix are $t^i$ (superscript) and rows are $t_j$ (subscript). For a bit $b$ and a string $v$, $b \cdot v$ is $v$ or the zero string.

## In plain words

Public-key OT is slow, so we want only a few of them. The trick is to run $\kappa$ OTs with the roles swapped: the future sender acts as receiver and picks a secret string $s$ of $\kappa$ bits as its choices.

The receiver builds a big table of random bits with $m$ rows and $\kappa$ columns. Through the swapped OTs, the sender gets a copy of the table in which each row is either the same as the receiver's row or differs from it by exactly $s$. Which of the two depends on the receiver's choice bit for that row, and the sender cannot tell which.

Now the sender hides message 0 of transfer $j$ under a hash of its row, and message 1 under a hash of its row XOR $s$. One of the two equals the receiver's row, so the receiver opens that message. The other needs $s$.

## The problem

Given a protocol for $\kappa$ instances of 1-out-of-2 OT on $\kappa$-bit strings, realize $m \gg \kappa$ instances of 1-out-of-2 OT on $\ell$-bit strings: the receiver learns $x_j^{r_j}$ for each $j$ and nothing about $x_j^{1 - r_j}$, and the sender learns nothing about $r$. The extended OTs must use only symmetric primitives. Some public-key step is unavoidable: OT cannot be built from a one-way function used as a black box (Impagliazzo and Rudich 1989), so the base OTs carry the public-key cost and the extension spreads it over many transfers.

## The algorithm

```pseudo id=main
IKNP(sender: pairs (x_j^0, x_j^1) for j = 1..m; receiver: bits r_1..r_m)
L1  S picks a random s ∈ {0,1}^κ
L2  R picks κ pairs of random seeds (k_i^0, k_i^1)
L3  for i = 1..κ: S gets k_i^{s_i} by a base OT in which R is the sender
L4  R sets t^i ← G(k_i^0) and sends u^i ← t^i ⊕ G(k_i^1) ⊕ r, for i = 1..κ
L5  S sets q^i ← G(k_i^{s_i}) ⊕ s_i · u^i, for i = 1..κ
L6  let t_j and q_j be row j of the m × κ matrices T = [t^1 … t^κ] and Q = [q^1 … q^κ]
L7  S sends y_j^0 ← x_j^0 ⊕ H(j, q_j) and y_j^1 ← x_j^1 ⊕ H(j, q_j ⊕ s), for j = 1..m
L8  R outputs z_j ← y_j^{r_j} ⊕ H(j, t_j), for j = 1..m
```

The key identity is $q^i = t^i \oplus s_i \cdot r$ for each column, and so $q_j = t_j \oplus r_j \cdot s$ for each row. When $r_j = 0$ the sender's row is $t_j$; when $r_j = 1$ it is $t_j \oplus s$. In both cases, the pad on $x_j^{r_j}$ is $H(j, t_j)$, which the receiver knows, and the pad on the other message is $H(j, t_j \oplus s)$, which needs $s$.

## Example

A toy run with $\kappa = 4$ and $m = 3$, far too small to be secure. The sender's secret is $s = 1010$ (bits $s_1 s_2 s_3 s_4$), and the receiver's choices are $r = (1, 0, 1)$. The receiver's matrix $T$ has rows $t_1 = 0110$, $t_2 = 1100$, $t_3 = 0011$, so its columns are $t^1 = (0,1,0)$, $t^2 = (1,1,0)$, $t^3 = (1,0,1)$ and $t^4 = (0,0,1)$. By line L5 the sender gets $q^i = t^i \oplus r$ for $s_i = 1$ and $q^i = t^i$ for $s_i = 0$: $q^1 = (1,1,1)$, $q^2 = (1,1,0)$, $q^3 = (0,0,0)$, $q^4 = (0,0,1)$.

| $j$ | $r_j$ | $t_j$ | $q_j$ | $q_j \oplus s$ | pad on $x_j^0$ | pad on $x_j^1$ | receiver's pad | receiver gets |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 0110 | 1100 | 0110 | $H(1, 1100)$ | $H(1, 0110)$ | $H(1, 0110)$ | $x_1^1$ |
| 2 | 0 | 1100 | 1100 | 0110 | $H(2, 1100)$ | $H(2, 0110)$ | $H(2, 1100)$ | $x_2^0$ |
| 3 | 1 | 0011 | 1001 | 0011 | $H(3, 1001)$ | $H(3, 0011)$ | $H(3, 0011)$ | $x_3^1$ |

In each row, $q_j = t_j$ when $r_j = 0$ and $q_j = t_j \oplus s$ when $r_j = 1$. The receiver's pad always matches the chosen message. The other pad is the hash of $t_j \oplus s$, and with $\kappa = 128$ the receiver would have to guess all of $s$.

**The code.** The implementation runs IKNP with $\kappa = 128$ base OTs from a local ideal OT, $G$ as SHA-256 in counter mode, and $H(j, q) = $ SHA-256 of $(j, q)$ cut to 16 bytes. The test runs $m = 10000$ transfers on random 16-byte messages and checks each output directly against the sender's pairs. It also checks $q_j = t_j \oplus r_j \cdot s$ on every row, and counts $\kappa$ base OTs, $\kappa m$ bits from the receiver and $2m$ masked messages from the sender.

**A cheating receiver.** IKNP for semi-honest parties trusts the receiver to put the same $r$ in every column. The test runs a receiver that does not. For probe transfer $j \le \kappa$ it puts the unit vector $e_j$ in row $j$, so that $q_j = t_j \oplus s_j e_j$ and the pad $H(j, q_j)$ depends on the single bit $s_j$. If the receiver can check that pad (in the test it knows $x_j^0$ for the probes; in a real protocol a selective failure can play the same role), it learns $s_j$ by trying both values. After $\kappa$ probes it knows all of $s$, and then it computes both pads $H(j, t_j)$ and $H(j, t_j \oplus s)$ of every other transfer. The test checks that it recovers $s$ and both messages of 500 further transfers. This is why the malicious version adds a consistency check.

There are no official test vectors for IKNP. SHA-256 comes from Python's `hashlib`. The code is for study only and is not constant time; it runs both parties in one process. Use a maintained library such as libOTe or EMP-toolkit for real data.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). For each column, if $s_i = 0$ then $q^i = G(k_i^0) = t^i$, and if $s_i = 1$ then $q^i = G(k_i^1) \oplus t^i \oplus G(k_i^1) \oplus r = t^i \oplus r$. So $q^i = t^i \oplus s_i \cdot r$. Reading bit $j$ of each column gives the row identity $q_j = t_j \oplus r_j \cdot s$. If $r_j = 0$ the pad on $x_j^0$ is $H(j, t_j)$, and if $r_j = 1$ the pad on $x_j^1$ is $H(j, q_j \oplus s) = H(j, t_j)$. In both cases line L8 removes the pad and returns $x_j^{r_j}$.

**Security against a semi-honest party.** The sender sees $u^i = G(k_i^0) \oplus G(k_i^1) \oplus r$. For $s_i = 0$ it knows $k_i^0$ but not $k_i^1$, and for $s_i = 1$ the opposite, so each $u^i$ is masked by the output of $G$ on an unknown seed and looks uniform: the sender learns nothing about $r$. The receiver knows $t_j$, and the other message is masked by $H(j, t_j \oplus s)$. The secret $s$ is uniform and hidden by the base OTs, and the same $s$ appears in all rows. A random oracle, or a hash that is *correlation robust* (its outputs on $t_j \oplus s$ look random even for known $t_j$ and a fixed unknown $s$), makes all these pads look uniform. IKNP prove security for semi-honest parties under either assumption.

## Complexity

| Resource | Base phase | Extension, per transfer |
|---|---|---|
| public-key operations | $\kappa$ base OTs | none |
| receiver to sender | $\kappa$ base OT messages | $\kappa$ bits (one bit of each $u^i$) |
| sender to receiver | $\kappa$ base OT messages | $2\ell$ bits |
| hash calls | none | 3 (2 by the sender, 1 by the receiver) |
| PRG output | none | $2\kappa$ bits for the receiver, $\kappa$ for the sender |

The local work is $\Theta(m(\kappa + \ell))$, with the bit matrix transpose as the main cost after hashing; real libraries transpose $128 \times 128$ blocks with SIMD instructions. The extension phase has two messages, $u$ from the receiver and $y$ from the sender, after the base OTs.

## Properties

- **Cost is symmetric-key only.** After the base OTs, each transfer costs a few hash calls and $\kappa + 2\ell$ bits of communication. Implementations reach millions of OTs per second.
- **One-time setup.** The base OTs can be run once, and the seeds expanded with $G$ for many later batches.
- **Reversed roles.** The base OTs run in the other direction: the extension sender is the base receiver.
- **Random OT for free.** If the sender does not send $y$, both parties hold random OT outputs: the sender has $H(j, q_j)$ and $H(j, q_j \oplus s)$, and the receiver has one of them. These can be derandomized later or used directly, for example for triples in GMW.
- **Correlated OT.** With $x_j^1 = x_j^0 \oplus \Delta$ for a fixed $\Delta$, the sender sends one string per transfer. This is what free-XOR garbling and GMW triples use.
- **Semi-honest only.** A receiver that puts different vectors in different columns breaks it, as shown above.

## Variants and improvements

- **Malicious receivers (KOS).** Keller, Orsini and Scholl (2015) add a check: the sender picks random field elements $\chi_j$ in $\mathbb{F}_{2^\kappa}$, and the receiver must send $\sum_j \chi_j r_j$ and $\sum_j \chi_j t_j$ such that $\sum_j \chi_j q_j = \sum_j \chi_j t_j \oplus (\sum_j \chi_j r_j) \cdot s$. A receiver with non-constant rows fails the check except with small probability, or leaks only a few bits of $s$, which extra columns absorb. The cost is close to the semi-honest protocol. Earlier malicious versions used cut-and-choose or extra checks at a higher cost.
- **1-out-of-$n$ OT.** Kolesnikov and Kumaresan (2013) replace the repetition code $r_j \cdot 1^\kappa$ hidden in IKNP by a code with larger distance, giving 1-out-of-$n$ OT for short strings at about the same cost. Batched OPRFs for [private set intersection](/private-set-intersection/) extend this idea.
- **Optimized semi-honest IKNP.** Asharov, Lindell, Schneider and Zohner (2013) tune the protocol for random and correlated OT, which need less communication from the sender, and speed up the transpose and the hashing.
- **Silent OT.** Boyle, Couteau, Gilboa, Ishai, Kohl and Scholl (CCS 2019 and CRYPTO 2019) build *pseudorandom correlation generators*: each party gets a short seed and expands it locally to millions of random OTs. The seeds come from a small amount of interaction, and security rests on [learning parity with noise](/learning-parity-with-noise/) (LPN). Communication drops from $\kappa$ bits per OT to almost nothing, at the price of more local work.
- **Beaver's extension.** Beaver (1996) first showed that a few OTs suffice: the parties securely compute, with a garbled circuit, a function that expands seeds into many OTs. It uses the one-way function inside the circuit, so it is far slower than IKNP, but it needs no random oracle.

## When to use it

Use OT extension whenever a protocol needs more than a few hundred OTs: GMW, Yao's garbled circuits (for the evaluator's inputs), OT-based PSI, and the offline phases of SPDZ-like systems. Use semi-honest IKNP when both parties are trusted to follow the protocol, KOS when the receiver may cheat, and silent OT when bandwidth is the limit. For a handful of OTs, run base OTs directly.

## Pitfalls

- **Trusting the receiver's columns.** A malicious receiver breaks semi-honest IKNP and learns the sender's whole secret $s$, and then both messages of every transfer. Use KOS against active adversaries.
- **Hash without the index.** $H$ must take $j$ as input. Without it, two transfers with equal rows get equal pads, and correlated OT variants leak.
- **Reusing $s$ across sessions.** Each set of base OTs fixes one $s$. If an attacker learns $s$ once, every transfer under it is open.
- **Too few base OTs.** $\kappa$ sets the security: with $\kappa = 80$ the brute-force search for $s$ costs $2^{80}$ hash calls.
- **A weak hash.** $H$ must be correlation robust. A linear function, or a hash with a known structure in its input, leaks $s$.
- **Not constant time.** The code on this page is for study only.

## Implementations

## History

The cost of public-key OT was the bottleneck of early secure computation. Beaver (STOC 1996) showed that OT can be *extended*: a small number of OTs and a one-way function give any number of OTs, but his construction evaluates the one-way function inside a secure computation and is not practical. Impagliazzo and Rudich's black-box separation (1989) implies that some public-key step cannot be avoided. Ishai, Kilian, Nissim and Petrank (CRYPTO 2003) gave the practical protocol, using a random oracle or a correlation-robust hash and only $\kappa$ base OTs. It became the base of fast GMW and Yao implementations from about 2010 on. Asharov, Lindell, Schneider and Zohner (2013) optimized it, and Keller, Orsini and Scholl (CRYPTO 2015) made it secure against a malicious receiver at almost no extra cost. Since 2019, pseudorandom correlation generators based on LPN have given silent OT extension with very little communication.

## References
