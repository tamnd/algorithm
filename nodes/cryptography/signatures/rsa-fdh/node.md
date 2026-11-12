---
tag: 0866Z3
kind: algorithm
slug: rsa-fdh
name: Full-domain hash RSA
aliases:
- RSA-FDH
- full domain hash
- FDH signature
area: cryptography/signatures
level: advanced
summary: "Sign M as H(M)^d mod N, where H hashes onto all of Z_N. EUF-CMA in the random oracle model under RSA, with loss q_s + q_h + 1 (Bellare and Rogaway 1996), improved to about e q_s (Coron 2000)."
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus N}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: true, randomized: false}
history:
  year: 1993
  people: [Mihir Bellare, Phillip Rogaway]
  note: Proposed in the random oracle paper of 1993 and given an exact security analysis in 1996. Coron improved the bound in 2000 and showed in 2002 that it is optimal for unique signatures.
prereqs: [rsa-signature, random-oracle-model, existential-unforgeability]
see_also: [rsa-pss, rsa-problem, hash-and-sign-paradigm, rabin-signature, bls-signature, strong-unforgeability, trapdoor-one-way-function, chosen-message-attack]
sources:
  - paper: "Mihir Bellare and Phillip Rogaway, Random oracles are practical: a paradigm for designing efficient protocols, ACM CCS 1993, pages 62 to 73"
    locator: the random oracle model and the full-domain hash signature from a trapdoor permutation
  - paper: "Mihir Bellare and Phillip Rogaway, The exact security of digital signatures: how to sign with RSA and Rabin, EUROCRYPT 1996, LNCS 1070"
    locator: Section 3, Theorem 3.1, the exact security of FDH with t = t' minus (q_hash + q_sig + 1) Θ(k^3) and ε = (q_sig + q_hash + 1) ε'
  - paper: "Jean-Sébastien Coron, On the exact security of full domain hash, CRYPTO 2000, LNCS 1880, pages 229 to 235"
    locator: the improved reduction with ε = (1 + 1/q_sig)^(q_sig + 1) q_sig ε', about e q_sig ε'
  - paper: "Jean-Sébastien Coron, Optimal security proofs for PSS and other signature schemes, EUROCRYPT 2002, LNCS 2332, pages 272 to 287"
    locator: the loss of a factor q_sig is optimal for schemes with unique signatures such as FDH, and probabilistic FDH
  - paper: "Saqib A. Kakvi and Eike Kiltz, Optimal security proofs for full domain hash, revisited, EUROCRYPT 2012, LNCS 7237"
    locator: the optimality result needs certified permutations, and RSA-FDH has a tight proof under the Phi-hiding assumption for small public exponents
  - paper: "Jonathan Katz and Nan Wang, Efficiency improvements for signature schemes with tight security reductions, ACM CCS 2003"
    locator: a tight variant of FDH that adds one secret bit to the hashed message
  - paper: "Yvo Desmedt and Andrew M. Odlyzko, A chosen text attack on the RSA cryptosystem and some discrete logarithm schemes, CRYPTO 1985, LNCS 218"
    locator: forging RSA signatures on small values from signatures on smooth values
  - paper: "Craig Gentry, Chris Peikert and Vinod Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, STOC 2008"
    locator: hash-and-sign signatures with preimage sampleable trapdoor functions on lattices
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: "Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1, RSA Cryptography Specifications Version 2.2, November 2016"
    locator: Appendix B.2.1 (MGF1), Section 4 (I2OSP and OS2IP), Section 5.2.1 (RSASP1)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, RSA-FDH and its proof in the random oracle model
---

Full-domain hash RSA (RSA-FDH) signs a message $M$ as $s = H(M)^d \bmod N$, where $H$ is a hash function whose output is spread over all of $\mathbb{Z}_N$, and it accepts $s$ when $s^e \bmod N = H(M)$. Bellare and Rogaway proposed it in 1993 as the first example of the [random oracle](/random-oracle-model/) paradigm. In that model it is [existentially unforgeable](/existential-unforgeability/) under chosen-message attack if the [RSA problem](/rsa-problem/) is hard. The reduction is not tight: Bellare and Rogaway (1996) lose a factor $q_s + q_h + 1$, Coron (2000) reduces it to about $\mathrm{e} \cdot q_s$, and Coron (2002) shows that no proof can do much better for schemes with unique signatures.

**Notation.** $N = pq$ is the RSA modulus, $k$ its length in bytes and $b$ in binary digits, $e$ and $d$ the public and private exponents. $H$ or $H_{\mathrm{FDH}}$ is the full-domain hash into $\mathbb{Z}_N$. $A$ or $F$ is a forger that runs in time $t$, makes $q_h$ hash queries and $q_s$ signing queries, and succeeds with probability $\varepsilon$; $t'$ and $\varepsilon'$ are the time and success of the derived RSA inverter. The proofs are in the random oracle model (ROM). $\mathrm{e} = 2.718\ldots$ is Euler's number, written upright to keep it apart from the exponent $e$.

## In plain words

Plain RSA signatures can be forged because the math of RSA lets an attacker combine signatures or invent them backwards. The full-domain hash idea is to first turn the message into a number that looks completely random and can be any number below the modulus. The signer then applies the secret RSA operation to that number.

An attacker who wants a signature for a new message must now apply the secret operation to a random-looking number that nobody controls. That is exactly the hard problem RSA is built on. Combining old signatures does not help, because the hash values of different messages have no useful relation. The proof of this treats the hash as a perfect random function. The name "full domain" says that the hash must cover the whole range of RSA, not only a small part of it.

## The problem

Build an EUF-CMA [signature scheme](/signature-scheme/) for arbitrary messages from the RSA [trapdoor permutation](/trapdoor-one-way-function/) $f(x) = x^e \bmod N$, with a proof that a forger gives an RSA inverter. The model is the random oracle model, and the assumption is that RSA is $(t', \varepsilon')$-hard: no algorithm with time $t'$ finds $y^d \bmod N$ for a uniform $y$ with probability more than $\varepsilon'$.

## The algorithm

```pseudo id=main
FDH-SIGN(sk, M)                        ▷ sk = (N, d), or its CRT form
L1  k ← length of N in bytes
L2  y ← OS2IP(MGF1-SHA-256(M, k + 16)) mod N     ▷ the full-domain hash H(M)
L3  s ← y^d mod N                       ▷ RSASP1, with the CRT
L4  return I2OSP(s, k)

FDH-VERIFY((N, e), M, S)
L5  if |S| ≠ k or OS2IP(S) ≥ N then return invalid
L6  return valid if OS2IP(S)^e mod N = H(M), else invalid
```

**The full-domain hash.** The scheme needs $H : \{0,1\}^* \to \mathbb{Z}_N$, and no standard fixes one. The code and line L2 use MGF1 of RFC 8017, Appendix B.2.1, with SHA-256 and the message as the seed, stretched to $k + 16$ bytes and reduced modulo $N$. The 128 extra binary digits make the result at most $2^{-128}$ away from uniform on $\mathbb{Z}_N$ in statistical distance (Lemma 2 of the correctness proof). Other choices are equally valid: any extendable-output function such as [SHAKE](/shake/) can replace MGF1. A hash of 256 binary digits followed by fixed padding is not a full-domain hash, and the proofs below do not apply to it.

**About the code.** The Python code is for study only. It is not constant time, its key generator uses a seeded non-cryptographic random source, and it must not protect real data. For RSA signatures in practice, use RSA-PSS from the pyca/cryptography library or from a FIPS 140 validated module. The code takes SHA-256 from `hashlib`, because the page is about the signature and not the hash.

## Example

A toy key: $p = 61$, $q = 53$, $N = 3233$, $e = 17$, $d = 2753$, so $k = 2$ and line L2 stretches to 18 bytes.

| message | first 8 bytes of MGF1-SHA-256 | $y = H(M)$ | $s = y^{2753} \bmod 3233$ | $s^{17} \bmod 3233$ |
|---|---|---|---|---|
| `hi` | `a3875a5322e4c359` | 212 | 265 | 212 |
| `ho` | `a7ff1849b14d101e` | 2764 | 1693 | 2764 |

The product of the two signatures, $265 \cdot 1693 \bmod 3233$, is a signature on the value $212 \cdot 2764 \bmod 3233$. A forger can use it only if it finds a message whose hash is that value, which for a random oracle takes about $N$ tries.

**What the bounds say.** Bellare and Rogaway (1996) give an example with $q_s = 2^{30}$ signatures and $q_h = 2^{60}$ hash computations. If RSA inversion succeeds with probability at most $\varepsilon' = 2^{-61}$, their bound only says that forgery succeeds with probability at most $(2^{30} + 2^{60} + 1) \cdot 2^{-61} \approx 1/2$. Coron's bound, $\varepsilon \le (1 + 1/q_s)^{q_s + 1} q_s \varepsilon'$, gives about $\mathrm{e} \cdot 2^{30} \cdot 2^{-61} \approx 2^{-29.6}$ for the same numbers.

## Correctness

The proof that each honest signature verifies, and that the hash of line L2 is $2^{-128}$-close to uniform on $\mathbb{Z}_N$, is in [proofs/correctness.md](proofs/correctness.md).

**Security.** The full proof of Coron's theorem is in [proofs/security.md](proofs/security.md). The statements, with $k$ the length of $N$ in binary digits as in the papers:

- **Bellare and Rogaway 1996, Theorem 3.1.** If RSA is $(t', \varepsilon')$-secure, then FDH is $(t, q_s, q_h, \varepsilon)$-secure with $t = t' - (q_h + q_s + 1) \cdot \Theta(k^3)$ and $\varepsilon = (q_s + q_h + 1) \cdot \varepsilon'$. The inverter guesses which hash query will be the forged message.
- **Coron 2000.** The same with $\varepsilon = (1 + 1/q_s)^{q_s + 1} \cdot q_s \cdot \varepsilon'$, which tends to $\mathrm{e} \cdot q_s \cdot \varepsilon'$. The inverter plants the RSA challenge in each hash answer with probability $1/(q_s + 1)$ and can sign the other messages.
- **Coron 2002, optimality.** For schemes with unique signatures, such as FDH, a reduction from inverting RSA must lose about a factor $q_s$: from a reduction with a smaller loss, Coron builds an efficient RSA inverter that needs no forger. Kakvi and Kiltz (2012) showed that this argument needs the permutation to be certified, that is, publicly checkable as a permutation. RSA with a small $e$ is not certified, and they proved RSA-FDH tight under the Phi-hiding assumption for small $e$.

FDH has unique signatures, so EUF-CMA implies [strong unforgeability](/strong-unforgeability/) for it.

## Complexity

Signing is one RSA private operation, two exponentiations of half size with the CRT, plus the hash: $\Theta(b^3)$ with schoolbook arithmetic for messages of bounded length. Line L2 makes $\lceil (k + 16)/32 \rceil$ SHA-256 calls, and each of them hashes the whole message, because MGF1 uses the message as its seed; for long messages, a variant that hashes the message once and uses the digest as the seed costs one pass over the message. Verification with $e = 65537$ is 17 modular multiplications, $\Theta(b^2)$. The signature has $k$ bytes.

| operation | cost |
|---|---|
| sign | 1 private RSA exponentiation (2 half-size with the CRT) and $\lceil (k + 16)/32 \rceil$ SHA-256 calls on the message |
| verify | 1 exponentiation by $e$ and the same hash |

## Properties

- **Deterministic and unique.** Each message has exactly one valid signature for a key.
- **Generic in the trapdoor.** The same design works for any trapdoor permutation; with Rabin's squaring it gives [Rabin-Williams](/rabin-signature/) signatures, and in pairing groups the same pattern gives [BLS](/bls-signature/).
- **Proof only in the ROM.** There is no proof of FDH from the RSA assumption in the standard model.
- **Not standardized as such.** PKCS #1 and FIPS 186-5 specify PSS and PKCS #1 v1.5, not FDH.

## Variants and improvements

- **[RSA-PSS](/rsa-pss/).** Adds a random salt and gets a tight reduction; with a fixed salt it falls back to FDH-like security.
- **Probabilistic FDH (PFDH).** Signs $H(M \| r)$ with a random $r$ that is sent with the signature; Coron (2002) shows that $\log_2 q_s$ random binary digits are enough for a tight proof.
- **Katz and Wang (2003).** Signs $H(\beta \| M)$ where $\beta$ is one bit derived from the message with a secret key. The proof is tight, and the scheme stays deterministic.
- **Lattice FDH.** Gentry, Peikert and Vaikuntanathan (2008) built a hash-and-sign scheme with trapdoor sampling on lattices; Falcon follows that approach.

## When to use it

RSA-FDH is the textbook scheme for proofs in the random oracle model and the base of several advanced constructions (blind signatures, threshold RSA). For deployed RSA signatures, use RSA-PSS as RFC 8017 requires for new applications, because it is standardized and has a tight proof.

## Pitfalls

- **A short hash is not full domain.** Signing $H(M)$ of 256 binary digits with a fixed padding, as in PKCS #1 v1.5, is a different scheme with a different analysis. Desmedt and Odlyzko (1985) showed chosen-message attacks when signed values are small enough to be smooth.
- **Bias.** Reducing a value of exactly $k$ bytes modulo $N$ gives a biased hash. Add enough extra output, as line L2 does.
- **Large $q_s$.** The bound degrades linearly in the number of signatures. Pick the modulus with this loss in mind, or use a scheme with a tight proof.
- **Hash and key from one source.** Line L2 depends on $N$ only through $k$. A multi-user setting should include the public key or a domain separation tag in the hash input.

## Implementations

The Python code gives `mgf1`, `fdh_hash` (line L2), `sign` (lines L1 to L4), `verify` (lines L5 and L6), a seeded toy key generator, and `CoronReduction`, the inverter of the security proof. No standard defines RSA-FDH or its hash, so there are no official test vectors: the tests check round trips, rejections, the definition of MGF1, the spread of the hash over $\mathbb{Z}_N$, and the failure of the multiplicative forgery. They also run Coron's reduction against a forger that cheats by holding $d$: with $q_s = 3$ and $p_0 = 3/4$ the inverter must solve the RSA instance with probability about $27/256$, and every success is checked.

## History

Bellare and Rogaway introduced the random oracle model and full-domain hash signatures at ACM CCS 1993. In 1996 they gave exact security bounds for FDH and introduced PSS, whose tight reduction was the reason to prefer it. Coron (2000) improved the FDH bound from $q_h$ to $q_s$, and Coron (2002) proved that this was optimal for schemes with unique signatures and showed that PSS needs only a short salt. Kakvi and Kiltz (2012) found a gap in the optimality argument and gave a tight proof of FDH under Phi-hiding.

## References
