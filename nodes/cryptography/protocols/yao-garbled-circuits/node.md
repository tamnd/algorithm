---
tag: 7XSXVN
kind: algorithm
slug: yao-garbled-circuits
name: Yao's garbled circuits
aliases:
- garbled circuit
- Yao's protocol
area: cryptography/protocols
level: advanced
summary: Two-party secure computation in constant rounds. One party encrypts a Boolean circuit gate by gate, the other gets input keys by OT and evaluates it, learning only the output.
solves: [secure-multiparty-computation]
model: word-ram
complexity:
  vars: {n: the number of AND gates, m: the number of XOR and INV gates, k: the label length in binary digits (the security parameter)}
  time: {worst: Θ((n + m) k), average: Θ((n + m) k), best: Θ((n + m) k)}
  space: {extra: Θ((n + m) k)}
properties: {deterministic: false, randomized: true}
history:
  year: 1986
  people: [Andrew Chi-Chih Yao]
  note: The technique is credited to Yao and his FOCS 1986 paper, but that paper has no explicit garbling construction. Lindell and Pinkas gave the first full proof in 2009.
prereqs: [oblivious-transfer, boolean-circuit, semi-honest-model]
see_also: [gmw-protocol, cut-and-choose, oblivious-transfer-extension, yao-millionaires-problem, secure-multiparty-computation, private-set-intersection, random-oracle-model]
sources:
  - paper: doi:10.1109/SFCS.1986.25
    title: "Andrew Chi-Chih Yao, How to generate and exchange secrets, FOCS 1986, pages 162 to 167"
    locator: the general two-party result; the paper itself has no explicit garbled circuit construction
  - paper: doi:10.1007/s00145-008-9036-8
    title: "Yehuda Lindell and Benny Pinkas, A proof of security of Yao's protocol for two-party computation, Journal of Cryptology 22(2), 2009, pages 161 to 188"
    locator: the full description of the protocol and its proof against semi-honest adversaries
  - paper: doi:10.1145/2382196.2382279
    title: "Mihir Bellare, Viet Tung Hoang and Phillip Rogaway, Foundations of garbled circuits, CCS 2012, pages 784 to 796"
    locator: garbling schemes and the notions of privacy, obliviousness and authenticity; the remarks on the history of Yao's construction
  - paper: doi:10.1145/100216.100287
    title: "Donald Beaver, Silvio Micali and Phillip Rogaway, The round complexity of secure protocols, STOC 1990, pages 503 to 513"
    locator: the multiparty garbling (BMR) and the permute bits on wire labels
  - paper: doi:10.1145/336992.337028
    title: "Moni Naor, Benny Pinkas and Reuban Sumner, Privacy preserving auctions and mechanism design, EC 1999, pages 129 to 139"
    locator: the garbled table with one row fixed to zero (GRR3)
  - paper: doi:10.1007/978-3-540-70583-3_40
    title: "Vladimir Kolesnikov and Thomas Schneider, Improved garbled circuit: free XOR gates and applications, ICALP 2008, LNCS 5126, pages 486 to 498"
    locator: the global offset and free XOR gates
  - paper: doi:10.1007/978-3-662-46803-6_8
    title: "Samee Zahur, Mike Rosulek and David Evans, Two halves make a whole, reducing data transfer in garbled circuits using half gates, EUROCRYPT 2015, LNCS 9057, pages 220 to 250"
    locator: the half gates construction (2 ciphertexts per AND gate) and the lower bound for linear garbling
  - paper: doi:10.1007/978-3-030-84242-0_5
    title: "Mike Rosulek and Lawrence Roy, Three halves make a whole? Beating the half-gates lower bound for garbled circuits, CRYPTO 2021, LNCS 12825, pages 94 to 124"
    locator: the scheme with 1.5k + 5 bits per AND gate
  - paper: "Seung Geol Choi, Jonathan Katz, Ranjit Kumaresan and Hong-Sheng Zhou, On the security of the free-XOR technique, TCC 2012, LNCS 7194, pages 39 to 53"
    locator: the circular correlation robustness assumption needed by free XOR
  - paper: "Chun Guo, Jonathan Katz, Xiao Wang and Yu Yu, Efficient and secure multiparty computation from fixed-key block ciphers, IEEE Symposium on Security and Privacy 2020, pages 825 to 841"
    locator: the attacks on some fixed-key AES hash designs used in garbling, and the fixed constructions
  - paper: doi:10.1561/3300000019
    title: "David Evans, Vladimir Kolesnikov and Mike Rosulek, A pragmatic introduction to secure multi-party computation, Foundations and Trends in Privacy and Security 2(2-3), 2018"
    locator: Section 3.1 (Yao's garbled circuits) and Chapter 4 (point-and-permute, row reduction, free XOR, half gates)
---

Yao's garbled circuits is the classic protocol for secure two-party computation. One party, the *garbler*, turns a [Boolean circuit](/boolean-circuit/) for the function into an encrypted form: each wire gets two random keys, one for 0 and one for 1, and each gate gets a small table that turns keys for its inputs into the key for its output. The other party, the *evaluator*, gets the keys for its own input bits by [oblivious transfer](/oblivious-transfer/), runs through the tables, and learns the output and nothing else. The protocol takes a constant number of rounds, whatever the depth of the circuit, and with free XOR and half gates it sends $2k$ bits per AND gate and nothing for XOR gates. This page gives the protocol with point-and-permute, free XOR and half gates, proves it correct, and traces the history of the optimizations.

**Notation.** $C$ is the circuit with $n$ AND gates and $m$ XOR and INV gates. $k$ is the label length, the security parameter (128 in practice, written $\kappa$ in many papers). The garbler has input $x$, the evaluator input $y$. $W_w^0, W_w^1 \in \{0,1\}^k$ are the two labels of wire $w$, $\Delta$ is the global offset with $W_w^1 = W_w^0 \oplus \Delta$, and $\mathrm{lsb}$ is the last bit. $H$ is a hash function with a tweak $j$, modeled as circular correlation robust or as a [random oracle](/random-oracle-model/). $v\Delta$ means $\Delta$ if $v = 1$ and $0^k$ if $v = 0$.

## In plain words

Picture a circuit of logic gates drawn on paper. The garbler replaces the 0 and the 1 on every wire with two long random passwords. For each gate it writes a small locked table: "if you hold these two input passwords, here is the output password."

The evaluator gets one password for each input wire. The garbler sends the passwords for its own input bits. For the evaluator's bits, the two parties run oblivious transfer, so the evaluator gets the right password and the garbler does not learn which one. The evaluator then opens one row in each table, gate after gate, and ends with a password on each output wire. A last small table turns those passwords into plain 0s and 1s.

Since the passwords look random, the evaluator never knows whether a password inside the circuit means 0 or 1.

## The problem

The input is a Boolean circuit $C$ that both parties know, a private input $x$ for the garbler and $y$ for the evaluator. The output is $C(x, y)$, which the evaluator learns and passes to the garbler. Security is against a [semi-honest](/semi-honest-model/) adversary that corrupts one party: its view must be simulatable from its input and the output. This is the two-party case of [secure multiparty computation](/secure-multiparty-computation/). Against malicious parties the protocol must be changed, for example by [cut-and-choose](/cut-and-choose/).

## The algorithm

The garbler builds labels and tables (GARBLE), the evaluator walks through them (EVALUATE), and the protocol joins them with OT. Gates are $(op, a, b, c)$ with input wires $a, b$, output wire $c$, and index $j$ in topological order.

```pseudo id=main
GARBLE(C)
L1  Δ ← random k-bit string with lsb(Δ) = 1                  ▷ free XOR offset
L2  for each input wire w: W_w^0 ← random k-bit string         ▷ W_w^1 = W_w^0 ⊕ Δ
L3  for each gate (op, a, b, c) with index j, in topological order:
L4      if op = XOR then W_c^0 ← W_a^0 ⊕ W_b^0                  ▷ no table
L5      else if op = INV then W_c^0 ← W_a^0 ⊕ Δ                  ▷ no table
L6      else                                                     ▷ AND: two half gates
L7          p_a ← lsb(W_a^0), p_b ← lsb(W_b^0)
L8          T_G ← H(W_a^0, 2j) ⊕ H(W_a^1, 2j) ⊕ p_b·Δ            ▷ garbler half: a ∧ p_b
L9          W_G ← H(W_a^0, 2j) ⊕ p_a·T_G
L10         T_E ← H(W_b^0, 2j+1) ⊕ H(W_b^1, 2j+1) ⊕ W_a^0        ▷ evaluator half: a ∧ (b ⊕ p_b)
L11         W_E ← H(W_b^0, 2j+1) ⊕ p_b·(T_E ⊕ W_a^0)
L12         W_c^0 ← W_G ⊕ W_E, table_j ← (T_G, T_E)
L13 d_w ← lsb(W_w^0) for each output wire w                      ▷ output decoding bits
L14 return (tables, d) and the labels

EVALUATE(C, tables, d, X)                                        ▷ X_w: one label per input wire
L15 for each gate (op, a, b, c) with index j, in topological order:
L16     if op = XOR then X_c ← X_a ⊕ X_b
L17     else if op = INV then X_c ← X_a
L18     else s_a ← lsb(X_a), s_b ← lsb(X_b), (T_G, T_E) ← table_j
L19         X_c ← H(X_a, 2j) ⊕ s_a·T_G ⊕ H(X_b, 2j+1) ⊕ s_b·(T_E ⊕ X_a)
L20 return lsb(X_w) ⊕ d_w for each output wire w

PROTOCOL: garbler with input x, evaluator with input y
L21 garbler runs GARBLE(C), sends tables, d, and W_w^(x_w) for its input wires
L22 for each evaluator input wire w: OT with (W_w^0, W_w^1) offered, choice y_w
L23 evaluator runs EVALUATE and sends the output to the garbler
```

Why the labels work: the last bit of a label is its *permute bit*. Since $\mathrm{lsb}(\Delta) = 1$, the two labels of a wire have different last bits, so the evaluator always knows which row or which branch to use (lines L18 and L19), but the last bit $s_w = v_w \oplus p_w$ is the true value masked by a random bit, so it tells the evaluator nothing.

Each half gate computes an AND in which one party knows one of the inputs. The *garbler half* (lines L8 and L9) computes $a \wedge p_b$, where the garbler knows $p_b$. The *evaluator half* (lines L10 and L11) computes $a \wedge (b \oplus p_b)$, where the evaluator knows $b \oplus p_b = s_b$. Their XOR is $a \wedge b$. Each half needs one ciphertext, so an AND gate costs 2.

## Example

**One AND gate, followed in full.** Take a gate with $p_a = 1$ and $p_b = 0$. The evaluator computes $G = H(X_a, 2j) \oplus s_a T_G$ and $E = H(X_b, 2j+1) \oplus s_b(T_E \oplus X_a)$. By the proof, $G = W_G \oplus (a \wedge p_b)\Delta$ and $E = W_E \oplus (a \wedge (b \oplus p_b))\Delta$.

| $a$ | $b$ | $s_a = a \oplus p_a$ | $s_b = b \oplus p_b$ | $G$ | $E$ | $X_c = G \oplus E$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | $W_G$ | $W_E$ | $W_c^0$ |
| 0 | 1 | 1 | 1 | $W_G$ | $W_E$ | $W_c^0$ |
| 1 | 0 | 0 | 0 | $W_G$ | $W_E$ | $W_c^0$ |
| 1 | 1 | 0 | 1 | $W_G$ | $W_E \oplus \Delta$ | $W_c^1$ |

Only the row $a = b = 1$ gives the 1-label, as an AND gate should. The evaluator sees the pair $(s_a, s_b)$, which is uniform because $p_a$ and $p_b$ are, so the row it uses says nothing about $a$ and $b$.

**Sizes on real circuits.** The code builds a comparator for $[a > b]$ (one AND gate per bit, see the [millionaires' problem](/yao-millionaires-problem/)) and a ripple-carry adder. Counted by script:

| Circuit | AND | XOR | INV | point-and-permute (4 rows) | GRR3 (3 rows) | half gates (2 rows) |
|---|---|---|---|---|---|---|
| comparator, 3 bits | 3 | 7 | 1 | 1536 bits | 1152 bits | 768 bits |
| adder, 3 bits | 3 | 11 | 0 | 1536 bits | 1152 bits | 768 bits |
| comparator, 32 bits | 32 | 94 | 1 | 16384 bits | 12288 bits | 8192 bits |
| adder, 32 bits | 32 | 156 | 0 | 16384 bits | 12288 bits | 8192 bits |

The table sizes use $k = 128$. With free XOR, the XOR column costs nothing in any mode.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows the invariant that the evaluator holds $W_w^{v_w}$ on every wire $w$, where $v_w$ is the value of $w$ in the plain evaluation. XOR and INV gates keep it because $W^1 = W^0 \oplus \Delta$ on every wire. For an AND gate, the garbler half gives $W_G \oplus (a p_b)\Delta$ and the evaluator half gives $W_E \oplus a(b \oplus p_b)\Delta$, and these add to $W_c^0 \oplus ab\Delta$. On an output wire, $\mathrm{lsb}(W_w^{v}) = p_w \oplus v$, and line L20 removes $p_w$.

**Security.** For semi-honest parties the simulators are:

- *Corrupt evaluator.* The simulator, given $y$ and $C(x, y)$, makes a fake garbled circuit that always outputs the right value: one random label per wire, tables built so that these labels decrypt correctly, and decoding bits set to give $C(x, y)$. A distinguisher between the fake and the real garbled circuit would break the hash: in the real one, the labels the evaluator does not hold are hidden by $H$ applied to labels it does not know. For the original double-encryption garbling, [Lindell and Pinkas (2009)](https://doi.org/10.1007/s00145-008-9036-8) gave the first full proof, in the standard model, assuming a symmetric encryption scheme secure under chosen double encryption with an elusive and efficiently verifiable range, and OT secure against semi-honest parties.
- *Corrupt garbler.* The garbler sees only the OT messages and the final output, so the simulator runs the OT simulator and outputs $C(x, y)$.

Free XOR needs more than a plain PRF, because the same $\Delta$ is inside every label and $H$ is applied to $W$ and $W \oplus \Delta$. Choi, Katz, Kumaresan and Zhou (TCC 2012) showed that *circular correlation robustness* of $H$ is the right assumption. Half gates are proven secure under the same assumption, in the standard model if such an $H$ exists, and in the random oracle model for a hash.

**Garbling schemes.** [Bellare, Hoang and Rogaway (2012)](https://doi.org/10.1145/2382196.2382279) separated the garbling from the protocol. A garbling scheme is a tuple of algorithms (garble, encode, evaluate, decode) with three security notions: *privacy* (the garbled circuit and the encoded input reveal only the output), *obliviousness* (they reveal nothing, without the decoding information) and *authenticity* (the evaluator cannot produce a valid output label for a wrong output). Yao's protocol is then "a private garbling scheme plus OT", and garbling schemes are used beyond 2PC, in zero-knowledge proofs and in functional encryption.

## Complexity

Let $n$ be the number of AND gates and $m$ the number of XOR and INV gates, and $\ell_x, \ell_y$ the input lengths.

| Resource | Garbler | Evaluator |
|---|---|---|
| hash calls per AND gate (half gates) | 4 | 2 |
| hash calls per XOR or INV gate | 0 | 0 |
| total time | $\Theta((n + m) k)$ | $\Theta((n + m) k)$ |
| communication | $2nk$ bits of tables, $\ell_x k$ bits of labels, $\ell_y$ OTs | $|C(x,y)|$ bits back |
| rounds | 2 messages plus the OT rounds | |

The rounds do not depend on the depth of $C$, unlike the [GMW protocol](/gmw-protocol/). The $\ell_y$ OTs cost $\ell_y$ public-key operations, or $k$ of them plus symmetric work with [OT extension](/oblivious-transfer-extension/). The space is $\Theta((n + m)k)$ for all labels; a garbler can stream tables gate by gate and keep only live wires.

## Properties

- **Constant rounds.** The whole circuit is sent in one message.
- **Asymmetric roles.** The garbler does about twice the hashing of the evaluator, and the evaluator learns the output first.
- **Semi-honest only, as given.** A malicious garbler can garble a different circuit (for example one that leaks $y$), and nothing in the protocol detects it. A malicious evaluator, in contrast, cannot do much: with authenticity it cannot produce wrong output labels.
- **One-time.** A garbled circuit must not be evaluated twice with different inputs: two labels of the same wire reveal $\Delta$, and then all labels.

## Variants and improvements

The cost of an AND gate, in ciphertexts of $k$ bits, fell over 35 years:

| Year | Technique | AND gate | XOR gate | Source |
|---|---|---|---|---|
| 1986 | original idea: 4 double encryptions, the evaluator tries all rows | 4 | 4 | Yao (as described by later authors) |
| 1990 | point-and-permute: a permute bit tells which row to decrypt | 4 | 4 | [Beaver, Micali and Rogaway](https://doi.org/10.1145/100216.100287) |
| 1999 | row reduction GRR3: pick the output label so that one row is zero | 3 | 3 | [Naor, Pinkas and Sumner](https://doi.org/10.1145/336992.337028) |
| 2008 | free XOR: one global $\Delta$, XOR of labels | 3 | 0 | [Kolesnikov and Schneider](https://doi.org/10.1007/978-3-540-70583-3_40) |
| 2015 | half gates: two half gates per AND | 2 | 0 | [Zahur, Rosulek and Evans](https://doi.org/10.1007/978-3-662-46803-6_8) |
| 2021 | three halves: slice labels into halves | $1.5 + 5/k$ | 0 | [Rosulek and Roy](https://doi.org/10.1007/978-3-030-84242-0_5) |

- **Point-and-permute.** Without it the evaluator tries all 4 rows and needs redundancy to recognize the right one. With a permute bit on each label, the rows are sorted by the permute bits and the evaluator decrypts exactly one.
- **GRR3.** The output label is chosen as the decryption of an all-zero row, so that row is not sent. It is compatible with free XOR. (GRR2, with 2 rows by polynomial interpolation, is not compatible with free XOR.)
- **Free XOR.** All wires share one offset $\Delta$, so the XOR of two labels is a label of the XOR. It needs circular correlation robustness of $H$.
- **Half gates.** Zahur, Rosulek and Evans also proved that 2 ciphertexts per AND gate is optimal for *linear* garbling schemes, which covers all the earlier ones.
- **Three halves.** Rosulek and Roy got around that bound by splitting each label into two halves and using a random choice of linear combinations controlled by the permute bits: $1.5k + 5$ bits per AND gate, still with free XOR.
- **Garbling with fixed-key AES.** Fast implementations replace SHA-256 with AES under a fixed key, which avoids key scheduling. Guo, Katz, Wang and Yu (IEEE S&P 2020) showed that some such hash designs are weaker than claimed and gave sound ones.
- **Malicious security.** [Cut-and-choose](/cut-and-choose/) on many garbled circuits, authenticated garbling (in the TinyOT and SPDZ style), or zero-knowledge proofs of correct garbling.
- **Many parties.** The BMR protocol of Beaver, Micali and Rogaway garbles a circuit jointly among $n$ parties in a constant number of rounds.

## When to use it

Use garbled circuits for two parties when the network has high latency and the function has deep Boolean circuits: comparisons, sorting, AES evaluation, string matching, and other bit-level work. They need only one round of tables, so a deep circuit costs no extra round trips. When the function is arithmetic (sums and products of large numbers), secret-sharing protocols such as the [BGW protocol](/bgw-protocol/) or SPDZ on arithmetic circuits are cheaper. When bandwidth is the bottleneck and latency is low, [GMW](/gmw-protocol/) with OT extension can send less per AND gate.

## Pitfalls

- **Reusing a garbled circuit.** Labels for both values of a wire reveal $\Delta$ and break every gate. Garble afresh for each evaluation.
- **Weak hash.** With free XOR, $H$ must be circular correlation robust, and with a tweak $j$ per gate. Without the gate index, a wire that feeds two AND gates gives the same pad $H(W)$ in both tables, and their XOR leaks.
- **Output decoding.** If the garbler sends the decoding bits for internal wires, the evaluator learns their values. Send them only for output wires.
- **Selective failure in the OT step.** A malicious garbler can offer a bad label in one OT; if the evaluation then fails, the garbler learns the evaluator's input bit there. This is the reason for input encoding tricks in the malicious variants (see [cut-and-choose](/cut-and-choose/)).
- **Malicious garbler.** The plain protocol gives no protection; do not use it as is when the garbler may cheat.
- **Not constant time.** The code on this page branches on secret bits and is for study only.

## Implementations

## History

Yao introduced secure two-party computation in his 1982 paper on the [millionaires' problem](/yao-millionaires-problem/), and gave a general solution in his FOCS 1986 paper, "How to generate and exchange secrets". The garbled circuit construction is credited to that paper, but the written paper does not contain an explicit description of garbling; the construction is known from Yao's oral presentations and from the accounts of later authors, and [Bellare, Hoang and Rogaway (2012)](https://doi.org/10.1145/2382196.2382279) note that the usual double-encryption form is attributed to Yao by others and may not be his original approach. One of the first written garbling constructions is in the BMR paper of 1990, which also introduced the permute bits. The protocol went without a full proof until [Lindell and Pinkas (2009)](https://doi.org/10.1007/s00145-008-9036-8). Fairplay (Malkhi, Nisan, Pinkas and Sella, 2004) was the first widely used implementation, and the optimizations in the table above made garbled circuits practical for circuits with millions of gates.

The code on this page implements GARBLE, EVALUATE and the protocol with half gates, and also the classic point-and-permute (4 rows) and GRR3 (3 rows) modes, all with free XOR, with $H$ = SHA-256 from hashlib cut to 128 bits and a local ideal OT. The tests run the comparator and the adder on all 3-bit inputs against plain evaluation in each mode, run random circuits, and count 4, 3 and 2 ciphertexts per AND gate. There are no official test vectors for garbled circuits, since labels are random. The code is for study only and is not constant time; use a maintained library such as EMP-toolkit or MP-SPDZ for real data.

## References
