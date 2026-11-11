---
tag: 3E3WQE
kind: problem
slug: yao-millionaires-problem
name: Yao's millionaires' problem
aliases:
- millionaires' problem
area: cryptography/protocols
level: intro
summary: Two parties with private numbers a and b learn whether a > b and nothing else. Yao posed it in 1982 as the first example of secure two-party computation.
history:
  year: 1982
  people: [Andrew Chi-Chih Yao]
  note: Yao stated the problem and gave a protocol based on a public-key trapdoor in his FOCS 1982 paper, which started the study of secure computation.
prereqs: [rsa-cryptosystem, trapdoor-one-way-function]
see_also: [secure-multiparty-computation, yao-garbled-circuits, oblivious-transfer, semi-honest-model, homomorphic-encryption, goldwasser-micali-cryptosystem, communication-complexity]
sources:
  - paper: doi:10.1109/SFCS.1982.38
    title: "Andrew C. Yao, Protocols for secure computations, FOCS 1982, pages 160 to 164"
    locator: the statement of the millionaires' problem and its solution with a one-way trapdoor function on a range of 10 values
  - paper: doi:10.1109/SFCS.1986.25
    title: "Andrew Chi-Chih Yao, How to generate and exchange secrets, FOCS 1986, pages 162 to 167"
    locator: secure computation of any two-party function, the basis of the garbled circuit approach
  - paper: doi:10.1137/0405022
    title: "Eyal Kushilevitz, Privacy and communication complexity, SIAM Journal on Discrete Mathematics 5(2), 1992, pages 273 to 284"
    locator: the characterization of two-party functions with an information-theoretically private protocol
  - paper: doi:10.1007/978-3-642-10433-6_1
    title: "Vladimir Kolesnikov, Ahmad-Reza Sadeghi and Thomas Schneider, Improved garbled circuit building blocks and applications to auctions and computing minima, CANS 2009, LNCS 5888, pages 1 to 20"
    locator: the comparison circuit with one non-XOR gate per input bit
  - paper: "Marc Fischlin, A cost-effective pay-per-multiplication comparison method for millionaires, CT-RSA 2001, LNCS 2020, pages 457 to 471"
    locator: a comparison protocol from Goldwasser-Micali encryption
  - paper: "Ivan Damgard, Martin Geisler and Mikkel Kroigaard, Efficient and secure comparison for on-line auctions, ACISP 2007, LNCS 4586, pages 416 to 430"
    locator: the DGK comparison protocol with additively homomorphic encryption
  - paper: doi:10.1016/S0166-218X(00)00342-5
    title: "Fabrice Boudot, Berry Schoenmakers and Jacques Traore, A fair and efficient solution to the socialist millionaires' problem, Discrete Applied Mathematics 111(1-2), 2001, pages 23 to 36"
    locator: the equality version of the problem and its protocol
---

Yao's millionaires' problem asks two parties, Alice with a private number $a$ and Bob with a private number $b$, to find out whether $a > b$ without revealing anything else about $a$ or $b$. [Yao (1982)](https://doi.org/10.1109/SFCS.1982.38) posed it as the first example of what is now called [secure two-party computation](/secure-multiparty-computation/), and solved it with a protocol built on a public-key trapdoor. That protocol costs time and communication linear in the *size of the range* of the inputs. A [garbled circuit](/yao-garbled-circuits/) for a comparator solves the same problem with cost linear in the *bit length* of the inputs, which is exponentially smaller. This page states the problem, works through Yao's 1982 protocol, and compares it with the modern solutions.

**Notation.** Alice holds $i$ and Bob holds $j$, both in $\{1, \ldots, n\}$, in the form of Yao's paper; the question "$a > b$" for $a, b \in \{0, \ldots, n-1\}$ is the same as "$i \ge j$" for $i = a + 1$ and $j = b + 2$ on the range $\{1, \ldots, n + 1\}$. $\ell = \lceil \log_2 n \rceil$ is the bit length of an input. $E_A$ and $D_A$ are Alice's public and private RSA maps with modulus $N$. $\kappa$ is the symmetric security parameter, for example 128.

## In plain words

Two rich people want to know who is richer, but neither wants to say how much money they have. A trusted friend could hear both numbers in secret and announce only the winner. Yao asked whether the two can get the same result alone, by sending messages to each other, so that each learns who is richer and nothing more.

The answer is yes. Yao's first solution makes Alice prepare one locked answer for every possible amount of money. Bob can open only the one for his own amount, and it tells him whether Alice has at least that much. This works, but it needs one answer for every possible amount, which is far too many for real numbers. Later methods compare the numbers one binary digit at a time, so the work grows only with the number of digits.

## Definition

**Input.** Alice has $i \in \{1, \ldots, n\}$; Bob has $j \in \{1, \ldots, n\}$.

**Output.** Both parties learn $\mathrm{GE}(i, j) = [i \ge j]$. (The strict version $[a > b]$ is equivalent, as in the notation.)

**Security.** A protocol is secure if it computes $\mathrm{GE}$ in the sense of [secure computation](/secure-multiparty-computation/): a simulator that gets one party's input and the output bit can produce that party's view. In Yao's 1982 setting the parties are [semi-honest](/semi-honest-model/): they follow the protocol and only try to learn more from what they see. A malicious version needs the tools of the [malicious adversary model](/malicious-adversary-model/), for example [cut-and-choose](/cut-and-choose/) on a garbled comparator.

The output bit itself leaks something, and that is allowed. If Alice has $i = 1$ and the answer is $i \ge j$, she learns $j = 1$; the trusted friend would have told her the same.

## Variants

- **Strict or non-strict comparison**, $[a > b]$ or $[a \ge b]$; they are the same problem with a shifted range.
- **One-sided output.** Only Bob learns the bit. In Yao's protocol Bob learns it first and then tells Alice, which a malicious Bob can lie about.
- **Socialist millionaires' problem.** Learn only whether $a = b$. It has cheaper protocols, for example the one of [Boudot, Schoenmakers and Traore (2001)](https://doi.org/10.1016/S0166-218X(00)00342-5), and is used to check a shared secret in the Off-the-Record messaging protocol.
- **Comparison on shared values.** Inside larger MPC protocols the numbers are often secret-shared, and comparison is a subprotocol that outputs a shared bit; it is one of the costly steps of secure statistics and machine learning.
- **Many parties.** Find the maximum, or the rank of each input, among $m$ parties: the sealed-bid auction problem.

## Examples

**Yao's protocol, worked.** Take the toy RSA key $N = 61 \cdot 53 = 3233$, $e = 17$, $d = 413$, a range $n = 4$, Alice with $i = 3$ and Bob with $j = 2$.

| Step | Who | Action | Value |
|---|---|---|---|
| 1 | Bob | pick $x$, compute $k = E_A(x)$ | $x = 1234$, $k = 2183$ |
| 1 | Bob | send $k - j + 1$ | $2182$ |
| 2 | Alice | $y_u = D_A(k - j + u)$ for $u = 1..4$ | $1965, 1234, 1387, 111$ |
| 3 | Alice | pick prime $p$, $z_u = y_u \bmod p$ | $p = 31$, $z = 12, 25, 23, 18$ |
| 4 | Alice | send $p$ and $z_1, z_2, z_3, z_4 + 1$ | $31$; $12, 25, 23, 19$ |
| 5 | Bob | is the $j$-th value equal to $x \bmod p$? | $25 = 1234 \bmod 31$: yes, so $i \ge j$ |

Why it works: $y_j = D_A(k) = x$, so $z_j = x \bmod p$. Alice adds 1 to exactly the positions after $i$, so position $j$ is unchanged if and only if $j \le i$. Alice also checks that all $z_u$ differ pairwise by at least 2 modulo $p$ and lie in $\{1, \ldots, p - 2\}$; the prime $p = 37$ was not allowed here because $y_4 \bmod 37 = 0$.

Why it is private for semi-honest parties: Alice sees only $k - j + 1$, and $k = E_A(x)$ is uniform in $\mathbb{Z}_N$ because $x$ is and $E_A$ is a permutation, so the message is uniform for every $j$. Bob sees $p$ and the values $z_u$ or $z_u + 1$; for $u \ne j$ he cannot compute $y_u = D_A(k - j + u)$ without Alice's private key, so he cannot tell which of them got the extra 1. Yao's paper argues this from the one-way property of $E_A$; a full proof needs more care than the 1982 text gives (see the Bounds section).

**The cost.** Alice does $n$ private-key RSA operations and sends $n + 1$ numbers of about $\log_2 N / 2$ bits. With the page's toy key of 62 bits and $n = 16$, a run sends $62 + 31 \cdot 17 = 589$ bits. For incomes up to $2^{32}$, $n = 2^{32}$, and the protocol is not usable.

**A garbled comparator.** For $\ell$-bit numbers, the circuit $c_0 = 0$, $c_{t+1} = a_t \oplus \big((a_t \oplus c_t) \wedge (b_t \oplus c_t)\big)$ for $t = 0, \ldots, \ell - 1$ (least significant bit first) outputs $c_\ell = [a > b]$ and has one AND gate per bit, the form used by [Kolesnikov, Sadeghi and Schneider (2009)](https://doi.org/10.1007/978-3-642-10433-6_1). Garbled with free XOR and half gates (see [Yao's garbled circuits](/yao-garbled-circuits/)), it costs $2\kappa\ell$ bits of garbled tables, $\ell$ input labels from Alice and $\ell$ [oblivious transfers](/oblivious-transfer/) for Bob. For $\ell = 32$ and $\kappa = 128$ the tables are 8192 bits.

**The code.** The page's Python file implements Yao's 1982 protocol with a toy RSA key of about 62 bits and a local Miller-Rabin test. The test runs all $16 \times 16$ pairs on the range $\{1, \ldots, 16\}$ against plain comparison, checks the strict form on $\{0, \ldots, 9\}$, checks that the cost is $n$ decryptions and $n + 1$ numbers, and checks that Bob's message has the same distribution for different $j$. There are no official test vectors for this protocol. The code is for study only and is not constant time.

## Known algorithms

| Solution | Main tool | Cost |
|---|---|---|
| Yao (1982) | trapdoor permutation (RSA) | $n$ private-key operations, $O(n \log N)$ bits |
| Garbled comparator (Yao 1986, KSS 2009) | garbled circuit and OT | $\ell$ AND gates, $\ell$ OTs, $O(\kappa \ell)$ bits |
| Fischlin (2001) | Goldwasser-Micali encryption | $O(\ell)$ ciphertexts, with the XOR homomorphism |
| DGK (2007) | additively homomorphic encryption | $O(\ell)$ ciphertexts |
| GMW on a comparator circuit | XOR shares and OT | $\ell$ AND gates, rounds grow with the AND depth |

- **Yao (1982).** The protocol in the example. It needs only a trapdoor permutation, and it is linear in $n = 2^\ell$.
- **Garbled circuits.** The general method of [Yao's garbled circuits](/yao-garbled-circuits/), applied to the comparator above. It is the standard answer today: constant rounds, and cost linear in $\ell$.
- **Homomorphic encryption.** Fischlin (2001) uses the [Goldwasser-Micali cryptosystem](/goldwasser-micali-cryptosystem/) to evaluate a comparison formula bit by bit; Damgard, Geisler and Kroigaard (2007) use an additively [homomorphic](/homomorphic-encryption/) scheme. These fit well when the inputs are already encrypted.
- **The [GMW protocol](/gmw-protocol/)** on the same circuit, with OT for each AND gate. A depth-optimized comparator has AND depth $O(\log \ell)$.

## Bounds

- **No information-theoretic solution.** Restrict the inputs to $i, j \in \{1, 2\}$. Then $[i \ge j] = [i = 2] \vee [j = 1]$, an OR of one bit from each side. [Kushilevitz (1992)](https://doi.org/10.1137/0405022) characterized the two-party functions that have a protocol private against unbounded semi-honest parties, and OR is not among them. So any solution needs a computational assumption, as in Yao's use of a trapdoor.
- **Yao's protocol is exponential in $\ell$.** Both the work of Alice and the length of her message are $\Theta(n) = \Theta(2^\ell)$.
- **Circuit-based cost.** A comparator for $\ell$-bit numbers has $\ell$ AND gates, so a garbled comparator costs $O(\kappa \ell)$ bits and $\ell$ OTs; with [OT extension](/oblivious-transfer-extension/) those OTs cost only symmetric-key work.
- **Rigor.** Yao's 1982 argument is informal by today's standards. The simulation-based definition of security came later, and the garbled circuit route has a full proof (Lindell and Pinkas 2009, see [Yao's garbled circuits](/yao-garbled-circuits/)).

## Reductions

- **To general secure computation.** $\mathrm{GE}$ is a two-party function, so any general [2PC](/secure-multiparty-computation/) protocol solves it; with [OT](/oblivious-transfer/) being complete, OT is enough.
- **From comparison to many tasks.** Secure maximum, sorting and ranking reduce to many comparisons; sealed-bid auctions reduce to a maximum.

## Applications

Sealed-bid auctions (who bid more, without revealing losing bids); private matching and profile comparison; secure statistics and machine learning on secret-shared data, where comparison is needed for sign tests, ReLU and maximum; and as a teaching example, because it is the smallest function whose secure computation is not trivial.

## References
