---
tag: 7RSZSV
kind: definition
slug: zk-stark
name: zk-STARK
aliases:
- scalable transparent argument of knowledge
- FRI
area: cryptography/protocols
level: research
summary: Transparent succinct argument built from hash functions and no trusted setup.
prereqs: [zero-knowledge-proof, merkle-tree, reed-solomon-code, low-degree-test]
see_also: [zk-snark, fiat-shamir-heuristic, random-oracle-model, pcp-theorem, fast-fourier-transform, polynomial-identity-testing, post-quantum-cryptography, cryptographic-hash-function]
sources:
  - paper: "Eli Ben-Sasson, Iddo Bentov, Yinon Horesh and Michael Riabzev, Scalable, transparent, and post-quantum secure computational integrity, IACR ePrint 2018/046"
    title: Eli Ben-Sasson, Iddo Bentov, Yinon Horesh and Michael Riabzev, Scalable, transparent, and post-quantum secure computational integrity
    locator: the definition of STARKs, the algebraic intermediate representation, and the measured proof sizes and times
  - paper: doi:10.4230/LIPIcs.ICALP.2018.14
    title: Eli Ben-Sasson, Iddo Bentov, Yinon Horesh and Michael Riabzev, Fast Reed-Solomon interactive oracle proofs of proximity, ICALP 2018, LIPIcs 107, 14:1-14:17
    locator: the FRI protocol, its folding step, its linear prover and logarithmic verifier, and its soundness analysis
  - paper: "Eli Ben-Sasson, Alessandro Chiesa and Nicholas Spooner, Interactive oracle proofs, TCC 2016-B, LNCS 9986, 31-60"
    title: Eli Ben-Sasson, Alessandro Chiesa and Nicholas Spooner, Interactive oracle proofs
    locator: the IOP model and the transform from a public-coin IOP to a non-interactive argument with Merkle trees and a random oracle
  - paper: "Joe Kilian, A note on efficient zero-knowledge proofs and arguments, STOC 1992, 723-732"
    title: Joe Kilian, A note on efficient zero-knowledge proofs and arguments
    locator: the first succinct argument, from a PCP and a Merkle tree commitment
  - url: https://people.cs.georgetown.edu/jthaler/ProofsArgsAndZK.html
    title: Justin Thaler, Proofs, Arguments, and Zero-Knowledge, monograph, 2022
    locator: the chapters on IOPs, the Merkle tree transform, and FRI
---

A zk-STARK is a zero-knowledge scalable transparent argument of knowledge: a proof that a long computation was done correctly, which the verifier checks in time polylogarithmic in the length of the computation, built from nothing but a hash function. "Transparent" means there is no trusted setup and no secret randomness to destroy: all the verifier's randomness is public. Because the only assumption is about the hash function, STARKs are believed to resist quantum computers. The cost is larger proofs, from tens to a few hundred kilobytes, against a few hundred bytes for a pairing-based [zk-SNARK](/zk-snark/). The engine inside is FRI, a test that a committed function is close to a polynomial of low degree.

## Definition

**Notation.** $\mathbb{F}$ is a finite field and $D \subset \mathbb{F}$ an evaluation domain of size $N$. $\mathrm{RS}[\mathbb{F}, D, d]$ is the [Reed-Solomon code](/reed-solomon-code/): the functions $D \to \mathbb{F}$ that are the values of a polynomial of degree less than $d$. The rate is $\rho = d / N$. A function $f$ is $\delta$-far from the code if each codeword differs from $f$ on more than $\delta N$ points. $T$ is the number of steps of the computation and $\lambda$ the security parameter.

**zk-STARK.** An argument system for statements of the form "a program runs for $T$ steps from a public input to a public output", with a witness of private inputs, such that:

1. **Transparent.** The setup is only the choice of public parameters (field, hash function); the verifier uses only public coins.
2. **Scalable.** The prover runs in time $T \cdot \mathrm{polylog}(T)$, and the verifier runs in time $\mathrm{polylog}(T)$ plus the size of the statement.
3. **Argument of knowledge.** In the [random oracle model](/random-oracle-model/), each prover that is accepted with good probability lets an extractor find a witness.
4. **Zero knowledge.** With random masking of the trace, the proof reveals nothing about the witness beyond the truth of the statement. Without this the object is a STARK, and many deployed systems use STARKs without zero knowledge, only for their succinctness.

**The pipeline.**

- *Trace.* The prover writes the computation as a table with $T$ rows (one per step) and a few columns (the registers).
- *AIR.* The algebraic intermediate representation is a set of low-degree polynomial constraints between consecutive rows, plus boundary constraints for the input and output.
- *Arithmetization.* Each column becomes a polynomial of degree below $T$, interpolated over a subgroup of order $T$, and then evaluated on a larger domain $D$, $N = T / \rho$ (the low-degree extension, computed with the [FFT](/fast-fourier-transform/)). Each constraint becomes a polynomial that must vanish on the subgroup, so it is divisible by the vanishing polynomial of the subgroup. A random combination of the quotients is the composition polynomial.
- *Low-degree test.* The trace is correct if and only if the quotients are polynomials of the right degree. The prover commits to their values on $D$ with a [Merkle tree](/merkle-tree/), and FRI proves that the committed function is close to a polynomial of low degree.
- *Non-interactive.* The Ben-Sasson, Chiesa and Spooner transform replaces the verifier's random challenges with hashes of the Merkle roots so far, as in the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/).

**FRI (Fast Reed-Solomon IOP of Proximity).** Let $D_0$ be a multiplicative subgroup of order $N = 2^n$, so $D_0 = -D_0$ and the squares $D_1 = \{x^2 : x \in D_0\}$ form a subgroup of order $N/2$. Each $f$ on $D_0$ can be written $f(x) = E(x^2) + x \cdot O(x^2)$, where
$$E(x^2) = \frac{f(x) + f(-x)}{2}, \qquad O(x^2) = \frac{f(x) - f(-x)}{2x}.$$
If $f$ has degree less than $d$, then $E$ and $O$ have degree less than $d/2$. FRI repeats a commit phase and then a query phase:

- *Commit.* For a verifier challenge $\alpha_i$, the prover commits to the fold $f_{i+1}(y) = E_i(y) + \alpha_i O_i(y)$ on $D_{i+1}$. After $\log_2 d$ folds the result must be a constant, which the prover sends in the clear.
- *Query.* The verifier picks a random $x \in D_0$ and asks for $f_i(\pm x^{2^i})$ in each layer with Merkle paths. It checks that each fold is consistent with the next layer.

### Basic facts

1. **Completeness.** If $f$ has degree less than $d$, then each fold has degree less than half, the last layer is a constant, and every query passes.
2. **Soundness.** If $f$ is $\delta$-far from the code, then for most $\alpha$ the fold is also far from the code of half the degree. So a cheating prover must break consistency somewhere, and each query detects this with probability about $\delta$. With $q$ queries the error is roughly $(1 - \delta)^q$ plus a small term from the choice of the $\alpha_i$. The proven bounds hold for $\delta$ up to about the unique decoding radius $(1 - \rho)/2$ or the Johnson bound; deployed systems often use a stronger conjecture, with about $\log_2(1/\rho)$ bits of security per query.
3. **Costs of FRI.** The prover does $O(N)$ field operations and hashes; the verifier does $O(q \log N)$ hashes and field operations; the proof has $O(q \log^2 N)$ hashes, because each opened value needs a Merkle path of length $\log N$.
4. **Assumptions.** Only a collision-resistant hash function, modeled as a random oracle. There is no group, so Shor's algorithm does not apply; Grover's search halves the bits of security of the hash. This is why STARKs are called plausibly [post-quantum](/post-quantum-cryptography/).

## Examples and non-examples

**One fold by hand.** Take $p = 3 \cdot 2^{30} + 1 = 3221225473$, whose multiplicative group is generated by $5$. Let $f(X) = 1 + 2X + 3X^2 + 4X^3$, so $d = 4$, on the subgroup of order $N = 32$ (blowup 8), generated by $\omega = 5^{(p-1)/32} = 66931328$.

- $E(Y) = 1 + 3Y$ and $O(Y) = 2 + 4Y$.
- With $\alpha_0 = 10$ the fold is $f_1(Y) = E + 10\,O = 21 + 43Y$ on the 16 squares. For example $f(\omega) = 3081801927$ and $f(-\omega) = 2414189666$, and the fold formula gives $2343846817$, which is $21 + 43\omega^2$ with $\omega^2 = 2526611335$.
- With $\alpha_1 = 7$ the second fold is the constant $21 + 43 \cdot 7 = 322$ on the 8 points of the last layer. The verifier checks that all 8 values are equal.

The full FRI procedure, as in the code:

```pseudo id=main
FRI-PROVE(values f_0 on D_0 of size N, degree bound d = 2^r, number of queries q)
L1  root_0 <- Merkle root of f_0; add root_0 to the transcript
    for i = 0 .. r - 1:
L2      alpha_i <- hash of the transcript
L3      f_{i+1}[j] <- (f_i[j] + f_i[j + N_i/2]) / 2 + alpha_i (f_i[j] - f_i[j + N_i/2]) / (2 w_i^j),  j < N_i/2
L4      if i < r - 1: root_{i+1} <- Merkle root of f_{i+1}; add it to the transcript
L5  send the last layer f_r (N / d values) and add it to the transcript
    for each of q queries:
L6      j <- hash of the transcript, mod N/2
L7      for each layer i: open f_i at j mod N_i/2 and j mod N_i/2 + N_i/2 with Merkle paths

FRI-VERIFY(proof)
L8  recompute every alpha_i and every query index j from the salt and the transcript
L9  check each Merkle path against its root
L10 check that the fold of each opened pair equals the opened value of the next layer (or of f_r)
L11 check that the last layer f_r is constant
```

**Code.** The Python file `zk_stark.py` implements only FRI, not a full STARK: there is no AIR, no execution trace, no composition polynomial and no zero-knowledge masking. It uses the field $p = 3 \cdot 2^{30} + 1$, a subgroup domain with blowup factor 8, a SHA-256 Merkle tree, and a SHA-256 Fiat-Shamir transcript that starts with a random salt. The tests check the field and its roots of unity; that the fold of $f$ is $E + \alpha O$; that functions of degree below $d$ pass; that random functions and a function of degree exactly $d$ fail; that changed openings or a changed salt fail; and an attack. The attack takes a low-degree $g$, corrupts 12 of its 128 values to get $f$, commits $f$ in layer 0 and the honest folds of $g$ in the later layers. The test checks that the verifier accepts exactly when no query hits a pair $\{x, -x\}$ with a corrupted value, so the acceptance rate is $u^q$ with $u = \Pr[\text{both } x \text{ and } -x \text{ unchanged}]$, and it checks the measured rate against $u^q$. With $d = 1024$ and 40 queries a proof is about 220 KB, because the code sends a full Merkle path for each opened value. There are no official test vectors for FRI. The code is for study only, not constant time, and not for real data. Real systems use reviewed libraries such as Winterfell, Plonky2 or StarkWare's Stone prover.

**Non-examples.**

- *Groth16 and other pairing-based [zk-SNARKs](/zk-snark/).* Succinct, with smaller proofs, but they need a trusted setup and rely on pairings, which a quantum computer breaks.
- *Kilian's argument.* Transparent and succinct from a PCP and a Merkle tree, the first of its kind, but the PCPs it needs are far too large to build in practice.
- *Bulletproofs.* Transparent, but based on the discrete logarithm problem (not post-quantum) and with a verifier that is linear in the circuit size.
- *A Merkle commitment alone.* It binds the prover to a function but says nothing about its degree; without FRI the prover could commit to any values.

## Related definitions

- **[zk-SNARK](/zk-snark/).** The pairing-based relative, with short proofs and a trusted setup.
- **[Low-degree test](/low-degree-test/).** The general problem of testing closeness to low-degree polynomials with few queries, of which FRI is a fast version for Reed-Solomon codes.
- **[PCP theorem](/pcp-theorem/).** Interactive oracle proofs generalize PCPs, and STARKs are IOPs compiled with Merkle trees.
- **[Zero-knowledge proof](/zero-knowledge-proof/).** The zero-knowledge property that a zk-STARK adds to a STARK.

## References
