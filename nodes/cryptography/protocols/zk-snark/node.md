---
tag: QH7EWC
kind: definition
slug: zk-snark
name: zk-SNARK
aliases:
- succinct non-interactive argument of knowledge
- succinct zero-knowledge argument
area: cryptography/protocols
level: research
summary: Non-interactive zero-knowledge argument with constant-size proofs and fast verification.
prereqs: [zero-knowledge-proof, proof-of-knowledge, schwartz-zippel-lemma, lagrange-interpolation, bilinear-pairing]
see_also: [zk-stark, fiat-shamir-heuristic, polynomial-identity-testing, pcp-theorem, circuit-sat, generic-group-model, sigma-protocol, random-oracle-model]
sources:
  - paper: doi:10.1007/978-3-662-49896-5_11
    title: Jens Groth, On the size of pairing-based non-interactive arguments, EUROCRYPT 2016, LNCS 9666, 305-326
    locator: the zk-SNARK for QAPs with proofs of three group elements, its proof in the generic group model, and the lower bound of two group elements
  - paper: "Bryan Parno, Jon Howell, Craig Gentry and Mariana Raykova, Pinocchio, nearly practical verifiable computation, IEEE Symposium on Security and Privacy 2013, 238-252"
    title: Bryan Parno, Jon Howell, Craig Gentry and Mariana Raykova, Pinocchio, nearly practical verifiable computation
    locator: the first implemented QAP-based SNARK, with a compiler from C to arithmetic circuits and constant-size proofs
  - paper: "Rosario Gennaro, Craig Gentry, Bryan Parno and Mariana Raykova, Quadratic span programs and succinct NIZKs without PCPs, EUROCRYPT 2013, LNCS 7881, 626-645"
    title: Rosario Gennaro, Craig Gentry, Bryan Parno and Mariana Raykova, Quadratic span programs and succinct NIZKs without PCPs
    locator: the definition of quadratic arithmetic and span programs, the reduction from circuits, and the divisibility check by the target polynomial
  - paper: "Ariel Gabizon, Zachary J. Williamson and Oana Ciobotaru, PLONK, permutations over Lagrange-bases for oecumenical noninteractive arguments of knowledge, IACR ePrint 2019/953"
    title: Ariel Gabizon, Zachary J. Williamson and Oana Ciobotaru, PLONK
    locator: the universal and updatable setup, the permutation argument, and the use of KZG commitments
  - paper: "Aniket Kate, Gregory M. Zaverucha and Ian Goldberg, Constant-size commitments to polynomials and their applications, ASIACRYPT 2010, LNCS 6477, 177-194"
    title: Aniket Kate, Gregory M. Zaverucha and Ian Goldberg, Constant-size commitments to polynomials and their applications
    locator: the polynomial commitment g^f(τ) with one-element openings checked by a pairing
  - url: https://medium.com/@VitalikButerin/quadratic-arithmetic-programs-from-zero-to-hero-f6d558cea649
    title: Vitalik Buterin, Quadratic Arithmetic Programs, from Zero to Hero, 2016
    locator: the example x^3 + x + 5 = 35, its flattening, R1CS, QAP polynomials and the quotient h
  - url: https://people.cs.georgetown.edu/jthaler/ProofsArgsAndZK.html
    title: Justin Thaler, Proofs, Arguments, and Zero-Knowledge, monograph, 2022
    locator: the chapters on SNARKs from linear PCPs (Groth16), polynomial commitments (KZG) and zero-knowledge
---

A zk-SNARK is a zero-knowledge succinct non-interactive argument of knowledge: a short proof, of a few hundred bytes, that the prover knows a witness for a statement, which anyone can check in milliseconds, independent of the size of the computation behind it. "Argument" means soundness holds only against efficient provers; "of knowledge" means a prover that is accepted must know a witness; "non-interactive" means the proof is one message. The best-known construction, Groth16, has proofs of three elliptic curve points and is used in Zcash and on Ethereum. The price is a structured reference string made by a trusted setup whose secret randomness must be destroyed.

## Definition

**Notation.** $\mathcal{R}$ is an NP relation given by an arithmetic circuit $C$ over a prime field $\mathbb{F}$; $x$ is the public input and $w$ the witness, with $(x, w) \in \mathcal{R}$ if $C(x, w) = 0$. $|C|$ is the number of gates. $\lambda$ is the security parameter. A function is negligible if it is smaller than each $1/\lambda^c$ for large $\lambda$.

**zk-SNARK.** A triple of efficient algorithms:

- $\mathrm{Setup}(1^\lambda, C) \to (\mathrm{pk}, \mathrm{vk})$, possibly with a secret trapdoor $\tau$ that must be erased;
- $\mathrm{Prove}(\mathrm{pk}, x, w) \to \pi$;
- $\mathrm{Verify}(\mathrm{vk}, x, \pi) \to \{0, 1\}$;

with these properties:

1. **Completeness.** If $(x, w) \in \mathcal{R}$, then $\mathrm{Verify}(\mathrm{vk}, x, \mathrm{Prove}(\mathrm{pk}, x, w)) = 1$.
2. **Knowledge soundness.** For each efficient adversary $A$ there is an efficient extractor $E_A$, which may read the code and coins of $A$, such that the probability that $A(\mathrm{pk}, \mathrm{vk})$ outputs $(x, \pi)$ with $\mathrm{Verify} = 1$ while $E_A$ fails to output a $w$ with $(x, w) \in \mathcal{R}$ is negligible.
3. **Succinctness.** $|\pi| = \mathrm{poly}(\lambda)$, independent of $|C|$ or growing only like $\mathrm{polylog}|C|$, and $\mathrm{Verify}$ runs in time $\mathrm{poly}(\lambda) \cdot (|x| + \mathrm{polylog}|C|)$.
4. **Zero knowledge.** There is a simulator that, given the trapdoor $\tau$ and $x \in L$ but no $w$, outputs proofs with the same distribution as real ones (perfect zero knowledge in Groth16).

Without property 4 the object is a SNARK; without "of knowledge" it is a SNARG. The name SNARK is from Bitansky, Canetti, Chiesa and Tromer (2012).

**Setup kinds.**

- **Circuit-specific trusted setup.** $\mathrm{pk}$ holds powers $g^{\tau^i}$ and circuit-dependent values for a secret $\tau$ (Pinocchio, Groth16). Whoever knows $\tau$, the "toxic waste", can forge proofs of false statements, because the simulator of property 4 uses $\tau$. In practice the setup is a multi-party ceremony that is safe if at least one participant erases its share.
- **Universal and updatable setup.** One reference string of powers of $\tau$ serves all circuits up to a size bound, and anyone can add fresh randomness to it (Sonic, PLONK, Marlin, with KZG commitments).
- **Transparent setup.** Only public randomness, as in [zk-STARKs](/zk-stark/), which use hash functions instead of pairings.

### Basic facts

1. **Arguments, not proofs.** Succinct proofs for NP with statistical soundness would put NP in a small complexity class, so SNARKs are arguments.
2. **Non-falsifiable assumptions.** Gentry and Wichs (2011) showed that no SNARG for all of NP can be proved sound by a black-box reduction to a falsifiable assumption. So the security of SNARKs rests on knowledge assumptions, the [generic group model](/generic-group-model/), or the [random oracle model](/random-oracle-model/).
3. **Proof size bounds.** Groth16 proofs are three group elements (two in $G_1$ and one in $G_2$); Groth proved that pairing-based arguments of this kind need at least two.
4. **Linear prover cost.** The prover of Groth16 does a number of group exponentiations linear in $|C|$ (multi-exponentiations) and a few FFTs of size about $|C|$. It is the slow part, often thousands of times slower than running $C$ itself.

## Examples and non-examples

**From program to QAP.** The first half of every QAP-based SNARK turns a computation into a polynomial divisibility claim. Buterin's 2016 example proves knowledge of $x$ with $x^3 + x + 5 = 35$.

1. *Flatten* into steps with one multiplication each: $\mathrm{sym}_1 = x \cdot x$, $y = \mathrm{sym}_1 \cdot x$, $\mathrm{sym}_2 = y + x$, $\mathrm{out} = \mathrm{sym}_2 + 5$.
2. *R1CS.* With the variable vector $s = (1, x, \mathrm{out}, \mathrm{sym}_1, y, \mathrm{sym}_2)$, each step $j$ becomes $\langle a_j, s \rangle \cdot \langle b_j, s \rangle = \langle c_j, s \rangle$. For example step 3 is $(x + y) \cdot 1 = \mathrm{sym}_2$: $a_3 = (0, 1, 0, 0, 1, 0)$, $b_3 = (1, 0, 0, 0, 0, 0)$, $c_3 = (0, 0, 0, 0, 0, 1)$. The witness is $s = (1, 3, 35, 9, 27, 30)$.
3. *QAP.* For each variable $i$, interpolate the column $(a_1[i], \ldots, a_4[i])$ at the points $1, 2, 3, 4$ to get $A_i(X)$ of degree 3, and in the same way $B_i$ and $C_i$ ([Lagrange interpolation](/lagrange-interpolation/)). For example $A_{\mathrm{one}}(X) = -5 + \tfrac{55}{6} X - 5 X^2 + \tfrac{5}{6} X^3$.
4. *Divisibility.* Let $A_s = \sum_i s_i A_i$, and so on, and $t(X) = (X-1)(X-2)(X-3)(X-4)$. At the point $j$, $A_s(j) B_s(j) - C_s(j)$ is the error of constraint $j$. So $s$ satisfies the R1CS if and only if $t$ divides $P = A_s B_s - C_s$. Here the quotient is $h(X) = -\tfrac{11}{3} + \tfrac{307}{18} X - \tfrac{31}{9} X^2$.
5. *One random point.* Two different polynomials of degree $d$ agree on at most $d$ points ([Schwartz-Zippel](/schwartz-zippel-lemma/)). So checking $A_s(\tau) B_s(\tau) - C_s(\tau) = h(\tau) t(\tau)$ at a random $\tau$ in a field of $2^{254}$ elements catches a false claim except with probability about $2^{-252}$.

A SNARK does step 5 without revealing $s$ or $\tau$: the setup publishes $g^{\tau^i}$, the prover computes $g^{A_s(\tau)}$, $g^{B_s(\tau)}$ and $g^{h(\tau)}$ from them as linear combinations, and the verifier checks the product relation with a [pairing](/bilinear-pairing/). Extra secret values ($\alpha$, $\beta$, $\gamma$, $\delta$ in Groth16) force the prover to use the same $s$ in all three polynomials, and random multiples of $t$ added to $A_s$ and $B_s$ give zero knowledge.

The code below follows these steps in the clear. The marked lines in the code match these lines.

```pseudo id=main
QAP-CHECK(R1CS rows a_j, b_j, c_j for j = 1..m, assignment s, point tau)
L1  for each variable i: A_i, B_i, C_i <- interpolate column i over the points 1..m
L2  t(X) <- (X - 1)(X - 2)...(X - m)
L3  A_s <- sum_i s_i A_i;  B_s <- sum_i s_i B_i;  C_s <- sum_i s_i C_i
L4  P <- A_s * B_s - C_s
L5  (h, rem) <- P divided by t        // rem = 0 iff s satisfies every constraint
L6  return A_s(tau) * B_s(tau) - C_s(tau) = h(tau) * t(tau)
```

**Code.** The Python file `zk_snark.py` implements steps 1 to 5 in the clear over the scalar field of the BN254 curve, $r = 21888242871839275222246405745257275088548364400416034343698204186575808495617$, which is prime with $2^{28} \mid r - 1$. It does not implement a pairing-based SNARK: there is no setup, no pairing, no hiding and no zero knowledge, so the "verifier" in the code sees the whole witness. The tests check that the interpolated polynomials equal the rational ones (computed with `Fraction`) and the values printed by Buterin, that $t$ divides $P$ for the witness and not for wrong ones, that the random point check accepts the witness and rejects a bad one, and that over $\mathbb{F}_{97}$ the bad witness passes at exactly the roots of the remainder, at most 3 points. There are no official test vectors for this step. The code is for study only. Real systems use reviewed libraries such as arkworks, libsnark, gnark or bellman.

**Non-examples.**

- *A [sigma protocol](/sigma-protocol/) made non-interactive by [Fiat-Shamir](/fiat-shamir-heuristic/).* It is a non-interactive zero-knowledge argument of knowledge, but its proof grows with the witness, and the verifier redoes the whole relation. Not succinct.
- *Bulletproofs.* Proofs of $O(\log |C|)$ group elements without trusted setup, but verification takes time linear in $|C|$. Not succinct in verification, so not a SNARK in the strict sense.
- *The QAP check in the clear.* The code on this page: sound by Schwartz-Zippel, but the verifier needs the whole witness. Neither zero knowledge nor succinct.
- *A [zk-STARK](/zk-stark/).* Succinct and transparent, with proofs of tens to hundreds of kilobytes; it is a succinct argument of knowledge, but usually not called a SNARK because of its different setup and assumptions.

## Related definitions

- **[Zero-knowledge proof](/zero-knowledge-proof/) and [proof of knowledge](/proof-of-knowledge/).** The properties that a zk-SNARK keeps while making the proof short and non-interactive.
- **[zk-STARK](/zk-stark/).** The transparent, hash-based alternative.
- **[PCP theorem](/pcp-theorem/).** Kilian and Micali built the first succinct arguments from PCPs and Merkle trees; QAP-based SNARKs avoid PCPs (the "without PCPs" of GGPR).
- **[Polynomial identity testing](/polynomial-identity-testing/).** The random point check at the core of every SNARK.
- **Polynomial commitment.** A short commitment to a polynomial with proofs of its values; KZG, the pairing-based one, is the core of PLONK.
- **[Circuit satisfiability](/circuit-sat/).** The NP-complete relation that SNARKs prove, after arithmetization.

## References
