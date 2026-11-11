---
tag: 6M8M74
kind: algorithm
slug: gmw-protocol
name: GMW protocol
aliases:
- Goldreich-Micali-Wigderson protocol
area: cryptography/protocols
level: research
summary: Secure computation of a Boolean circuit on XOR-shared wires. XOR gates are local, each AND gate uses an OT or a Beaver triple, and the rounds grow with the AND depth.
solves: [secure-multiparty-computation]
model: word-ram
complexity:
  vars: {n: the number of AND gates, m: the number of XOR and INV gates, d: the AND depth of the circuit}
  time: {worst: Θ(n + m), average: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1987
  people: [Oded Goldreich, Silvio Micali, Avi Wigderson]
  note: Goldreich, Micali and Wigderson gave the protocol at STOC 1987, with security for semi-honest parties and a compiler to malicious security. Beaver added multiplication triples in 1991.
prereqs: [oblivious-transfer, semi-honest-model, boolean-circuit]
see_also: [yao-garbled-circuits, bgw-protocol, secure-multiparty-computation, oblivious-transfer-extension, malicious-adversary-model, secret-sharing]
sources:
  - paper: doi:10.1145/28395.28420
    title: "Oded Goldreich, Silvio Micali and Avi Wigderson, How to play any mental game, or a completeness theorem for protocols with honest majority, STOC 1987, pages 218 to 229"
    locator: the protocol on shared bits with OT for the AND gates, and the compiler to malicious security
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Section 7.3 (privately computing any functionality in the semi-honest model, with 1-out-of-4 OT for multiplication gates)
  - paper: doi:10.1007/3-540-46766-8_34
    title: "Donald Beaver, Efficient multiparty protocols using circuit randomization, CRYPTO 1991, LNCS 576, pages 420 to 432"
    locator: multiplication triples computed in advance and the online multiplication with two openings
  - paper: "Thomas Schneider and Michael Zohner, GMW vs. Yao? Efficient secure two-party computation with low depth circuits, Financial Cryptography 2013, LNCS 7859, pages 275 to 292"
    locator: the implementation of GMW with OT extension and multiplication triples, and the comparison with Yao
  - paper: "Gilad Asharov, Yehuda Lindell, Thomas Schneider and Michael Zohner, More efficient oblivious transfer and extensions for faster secure computation, CCS 2013, pages 535 to 548"
    locator: multiplication triples from two random 1-out-of-2 OTs
  - paper: "Jesper Buus Nielsen, Peter Sebastian Nordholt, Claudio Orlandi and Sai Sheshank Burra, A new approach to practical active-secure two-party computation, CRYPTO 2012, LNCS 7417, pages 681 to 700"
    locator: TinyOT, GMW style computation with MACs on bits for malicious security
  - paper: "Toshinori Araki, Jun Furukawa, Yehuda Lindell, Ariel Nof and Kazuma Ohara, High-throughput semi-honest secure three-party computation with an honest majority, CCS 2016"
    locator: the three-party protocol on replicated shares with one bit per party per AND gate
  - paper: doi:10.1561/3300000019
    title: "David Evans, Vladimir Kolesnikov and Mike Rosulek, A pragmatic introduction to secure multi-party computation, Foundations and Trends in Privacy and Security 2(2-3), 2018"
    locator: Section 3.2 (the GMW protocol)
---

The GMW protocol, by Goldreich, Micali and Wigderson (1987), computes a [Boolean circuit](/boolean-circuit/) on secret inputs by keeping the value of every wire split into random XOR shares, one per party. XOR and NOT gates are computed by each party alone on its shares. Each AND gate needs one interaction: in the original protocol a 1-out-of-4 [oblivious transfer](/oblivious-transfer/), and in the version of Beaver (1991) a multiplication triple prepared in advance. All AND gates at the same depth run in parallel, so the number of rounds equals the AND depth of the circuit. This is the main difference from [Yao's garbled circuits](/yao-garbled-circuits/), which use a constant number of rounds whatever the depth. This page gives the two-party protocol for [semi-honest](/semi-honest-model/) parties, proves it correct, and describes the multiparty and malicious versions.

**Notation.** $P_1$ and $P_2$ are the parties, with inputs $x$ and $y$. $[w]_i \in \{0,1\}$ is the share of party $P_i$ on wire $w$, with $v_w = [w]_1 \oplus [w]_2$. The circuit $C$ has $n$ AND gates, $m$ XOR and INV gates, and AND depth $d$: the largest number of AND gates on any path from an input to an output. $\binom{4}{1}$-OT is a 1-out-of-4 OT. $\lambda$ is the security parameter.

## In plain words

Every bit in the computation is split into two random-looking halves, one for each party, and the true bit is the XOR of the two halves. Neither half alone says anything.

Adding bits (XOR) is easy: each party XORs its own halves and gets a half of the result, with no talking. Multiplying bits (AND) is the hard part, because the halves get mixed. Here the first party prepares the four possible answers, one for each possible half the second party might hold, each hidden with a fresh random bit. The second party picks the one answer that fits its halves by oblivious transfer, so neither side learns the other's half.

The parties go gate by gate. AND gates at the same level of the circuit run at the same time, so the rounds of talking grow with the number of levels.

## The problem

The input is a Boolean circuit $C$ that both parties know, $x$ for $P_1$ and $y$ for $P_2$. Both parties must learn $C(x, y)$, and a [semi-honest](/semi-honest-model/) party must learn nothing else: its view must be simulatable from its input and the output. This is the two-party case of [secure multiparty computation](/secure-multiparty-computation/). The protocol is given for an ideal OT (or an ideal dealer of triples); with a secure OT protocol in its place, the composition theorem gives a real protocol.

## The algorithm

Gates are $(op, a, b, c)$ in topological order, with $op \in \{\mathrm{AND}, \mathrm{XOR}, \mathrm{INV}\}$. The protocol processes the gates by AND depth $\delta(c)$ of their output wire (inputs have depth 0, an AND gate adds 1).

```pseudo id=main
GMW(C, x, y)
L1  for each input wire w with value v of party P_i: P_i picks a random bit r, keeps v ⊕ r and gives r to the other party
L2  for δ = 0, 1, ..., d:
L3      for each AND gate (a, b, c) with depth δ, all in one round:
L4          P_1 picks a random bit r and sets [c]_1 ← r
L5          P_1 makes T[i][j] ← r ⊕ (([a]_1 ⊕ i) ∧ ([b]_1 ⊕ j)) for i, j ∈ {0, 1}
L6          P_2 gets [c]_2 ← T[[a]_2][[b]_2] by a 1-out-of-4 OT
L7      for each XOR or INV gate (a, b, c) with depth δ, in topological order:
L8          XOR: [c]_1 ← [a]_1 ⊕ [b]_1 and [c]_2 ← [a]_2 ⊕ [b]_2
L9          INV: [c]_1 ← [a]_1 ⊕ 1 and [c]_2 ← [a]_2
L10 the parties swap their shares of the output wires; each outputs [w]_1 ⊕ [w]_2
```

**Beaver triples instead of OT.** Lines L4 to L6 can be replaced by a precomputed triple: shares of random bits $x', y', z'$ with $z' = x' \wedge y'$. The parties open $e_a = v_a \oplus x'$ and $e_b = v_b \oplus y'$ (each sends its two shares of them) and set

$$[c]_1 = [z']_1 \oplus e_a [y']_1 \oplus e_b [x']_1 \oplus e_a e_b, \qquad [c]_2 = [z']_2 \oplus e_a [y']_2 \oplus e_b [x']_2.$$

The opened bits are one-time pads of $v_a$ and $v_b$, so they reveal nothing. Triples do not depend on the inputs, so they can all be made in an offline phase, with OT extension in practice, and the online phase then costs 4 bits and no cryptography per AND gate.

## Example

**One AND gate, both methods.** $P_1$ holds $a = 1$ and $P_2$ holds $b = 1$. With input coins 0 for $P_1$ and 1 for $P_2$, the shares are $[a]_1 = 1$, $[a]_2 = 0$, $[b]_1 = 1$, $[b]_2 = 0$.

| Method | $P_1$'s step | $P_2$'s step | $[c]_1$ | $[c]_2$ | $c$ |
|---|---|---|---|---|---|
| OT | $r = 1$; $T = (T_{00}, T_{01}, T_{10}, T_{11}) = (0, 1, 1, 1)$ | chooses $T[0][0] = 0$ | 1 | 0 | 1 |
| Triple | triple shares $(x', y', z')_1 = (1, 0, 0)$; $e_a = 0$, $e_b = 0$ | triple shares $(x', y', z')_2 = (0, 1, 1)$ | 0 | 1 | 1 |

In the OT row, $T[i][j] = 1 \oplus ((1 \oplus i) \wedge (1 \oplus j))$: only $T_{00}$ has the AND term 1. In the triple row, $x' = 1$ and $y' = 1$, so $z' = 1$, $e_a = 1 \oplus 1 = 0$ and $e_b = 1 \oplus 1 = 0$, and the shares of $c$ are just the shares of $z'$.

**Rounds on an adder.** A $w$-bit ripple-carry adder has $w$ AND gates in a chain, so AND depth $w$. The test runs it for $w = 1, 4, 8, 16$ and counts $w$ rounds and $w$ OTs. It also checks that the round counter equals the AND depth on 100 random circuits in both modes.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The invariant is $[w]_1 \oplus [w]_2 = v_w$ on each processed wire. Input sharing (line L1) sets it, XOR and INV keep it by linearity (lines L8 and L9), and the OT table of line L5 gives $[c]_1 \oplus [c]_2 = r \oplus r \oplus v_a v_b$. For the triple method, expanding $z' \oplus e_a y' \oplus e_b x' \oplus e_a e_b$ gives $v_a v_b$. The proof also shows that processing by depth respects the topological order, and that there is an AND gate at every depth from 1 to $d$, so the AND gates take exactly $d$ rounds.

**Security against a semi-honest party.** Every message a party gets during the gates is a uniform bit independent of everything else: the share $r$ of the other party's input, and the OT output $T[[a]_2][[b]_2] = r \oplus \ldots$ masked by the fresh $r$ of line L4 (or, with triples, the openings $e_a$ and $e_b$, masked by the triple). The simulator for $P_2$ outputs uniform bits for all of these, and for the final output shares it outputs $C(x, y) \oplus [w]_2$, which makes the view consistent with the output. In the OT version $P_1$ receives nothing during the gates (it is the OT sender), so its simulator is even simpler. With an ideal OT the security is perfect; with a real OT it is as strong as the OT. The proof is in Goldreich's book, Volume 2, Section 7.3.

## Complexity

| Resource | OT version | Triple version, online |
|---|---|---|
| local work | $\Theta(n + m)$ bit operations | $\Theta(n + m)$ bit operations |
| AND gates | $n$ $\binom{4}{1}$-OTs on bits | 4 bits sent per AND gate |
| XOR and INV gates | free | free |
| rounds | $d$ for the gates, plus input and output rounds | $d$, plus input and output rounds |

A $\binom{4}{1}$-OT on bits costs two 1-out-of-2 OTs of keys plus four short encryptions; with [OT extension](/oblivious-transfer-extension/), each 1-out-of-2 OT costs $O(\lambda)$ bits and a few hash calls. The triple version moves all OTs to an offline phase: Asharov, Lindell, Schneider and Zohner (2013) make one triple from two random 1-out-of-2 OTs.

## Properties

- **Rounds grow with depth.** The cost in rounds is $d + O(1)$. Yao's garbled circuits use $O(1)$ rounds. On a network with high latency, a deep circuit is slow in GMW.
- **Symmetric roles.** Both parties do the same kind of work, unlike Yao's garbler and evaluator.
- **Cheap online phase.** With triples, the online phase has no cryptography at all: XORs and 4 bits per AND gate.
- **Any number of parties.** With $n$ parties, $v = [w]_1 \oplus \cdots \oplus [w]_n$, XOR is local, and an AND gate needs the cross terms $[a]_i [b]_j$ for all pairs $i \neq j$, by one OT per ordered pair. It is secure against up to $n - 1$ semi-honest parties.
- **Perfect security given ideal OT.** All the computational assumptions sit in the OT.

## Variants and improvements

- **Malicious security, by compilation.** The GMW paper gave a compiler: each party commits to its input and random tape, and proves in [zero knowledge](/zero-knowledge-proof/) that each message follows the protocol. It shows feasibility but is slow; see the [malicious adversary model](/malicious-adversary-model/).
- **TinyOT** (Nielsen, Nordholt, Orlandi and Burra 2012). Bits carry information-theoretic MACs, and authenticated triples come from OT extension; a cheater is caught at the end with high probability.
- **Arithmetic GMW.** The same idea over $\mathbb{Z}_{2^k}$ or a prime field, with additive shares and multiplication triples. This is the online phase of SPDZ.
- **Depth-optimized circuits.** Because rounds follow the AND depth, GMW wants circuits of low AND depth: a parallel-prefix adder (depth $O(\log w)$) in place of the ripple-carry adder (depth $w$), as in Schneider and Zohner (2013).
- **Honest majority.** With three parties and one corrupt, replicated secret sharing gives AND gates with one bit sent per party, as in the protocol of Araki, Furukawa, Lindell, Nof and Ohara (CCS 2016).

## When to use it

GMW suits low-latency networks (a data center or a LAN), circuits of small AND depth, and settings where the preprocessing can be done in advance: then the online phase is only XORs and a few bits per AND gate. It also suits more than two parties. On a high-latency network, or for deep circuits such as AES with many rounds, [Yao's garbled circuits](/yao-garbled-circuits/) usually win. For arithmetic over large numbers, arithmetic sharing (as in [BGW](/bgw-protocol/) or SPDZ) is cheaper than bit circuits.

## Pitfalls

- **Reusing the random bit $r$.** Line L4 needs a fresh $r$ for each AND gate; with a fixed $r$, $P_2$ learns relations between AND outputs.
- **Reusing a triple.** Opening $e_a = v_a \oplus x'$ twice with the same $x'$ reveals $v_a \oplus v_a'$.
- **Revealing internal shares.** Only output shares may be swapped at the end. A share of an internal wire, together with the other party's share, reveals that wire.
- **Malicious parties.** The plain protocol gives no protection: $P_1$ can put a wrong table in the OT and flip any AND output, and nothing detects it.
- **Not constant time.** The code on this page branches on shares and is for study only.

## Implementations

## History

Goldreich, Micali and Wigderson presented the protocol at STOC 1987 in "How to play any mental game", together with the compiler that makes it secure against malicious parties with an honest majority (or with abort when there is no honest majority). With Yao's work it established that every function has a secure protocol. Beaver (1991) introduced multiplication triples ("circuit randomization"), which split the protocol into an input-independent offline phase and a fast online phase; this split is the basis of most modern MPC systems. Choi, Hwang, Katz, Malkin and Rubenstein (CT-RSA 2012) and Schneider and Zohner (2013) gave efficient implementations with OT extension, which showed GMW to be competitive with Yao on fast networks.

The code on this page implements two-party GMW with a local ideal $\binom{4}{1}$-OT and, as the second mode, with Beaver triples from a local dealer. The tests compare both modes with plain evaluation on 200 random circuits and on a 4-bit adder on all inputs, check that the round counter equals the AND depth, and check that $P_2$'s view has the same distribution for both values of $P_1$'s input bit. There are no official test vectors for GMW. The code is for study only and is not constant time; use a maintained framework such as MP-SPDZ or ABY for real data.

## References
