---
tag: ECE9S6
kind: algorithm
slug: ntru-prime
name: NTRU Prime
aliases:
- Streamlined NTRU Prime
- sntrup761
- NTRU LPRime
area: cryptography/post-quantum
level: advanced
summary: "An NTRU variant in the field Z_q[x]/(x^p - x - 1) with p and q prime, made to remove ring structure that attacks could use. Its KEM sntrup761 is used in OpenSSH with X25519."
model: word-ram
complexity:
  vars: {p: the ring degree (761 for sntrup761)}
  time: {worst: Θ(p^2), average: Θ(p^2), best: Θ(p^2)}
  space: {extra: Θ(p)}
properties: {deterministic: false, randomized: true}
history:
  year: 2017
  people: [Daniel J. Bernstein, Chitchanok Chuengsatiansup, Tanja Lange, Christine van Vredendaal]
  note: Published at SAC 2017. Submitted to NIST in 2017, it was an alternate candidate in round 3 and did not go on to round 4. OpenSSH 9.0 (2022) made sntrup761x25519-sha512 its default key exchange.
prereqs: [ntru-encrypt, ntru-problem, learning-with-rounding, key-encapsulation-mechanism]
see_also: [crystals-kyber, saber, hybrid-key-exchange, x25519, lattice-based-cryptography, nist-pqc-standardization, extended-euclidean-algorithm, polynomial-multiplication]
sources:
  - paper: doi:10.1007/978-3-319-72565-9_12
    title: Daniel J. Bernstein, Chitchanok Chuengsatiansup, Tanja Lange and Christine van Vredendaal, NTRU Prime, reducing attack surface at low cost, SAC 2017, LNCS 10719
    locator: "the sections on the choice of ring (x^p - x - 1), Streamlined NTRU Prime (key generation, encryption with rounding, decryption with the no-failure condition q >= 16w + 1) and NTRU LPRime"
  - url: "https://ntruprime.cr.yp.to/"
    title: Daniel J. Bernstein and others, NTRU Prime, NIST round 3 submission and specification, 2020
    locator: "the parameter set sntrup761 (p = 761, q = 4591, w = 286), the encodings, the hashes with their prefixes and the known answer tests of the package"
  - paper: doi:10.6028/NIST.IR.8413-upd1
    title: NIST, IR 8413 (update 1), Status report on the third round of the NIST post-quantum cryptography standardization process, 2022
    locator: the section on NTRU Prime (an alternate candidate)
---

NTRU Prime is a lattice-based key encapsulation mechanism by Bernstein, Chuengsatiansup, Lange and van Vredendaal (2017). It keeps the idea of [NTRUEncrypt](/ntru-encrypt/), a public key $h = g/(3f)$ that hides two short polynomials, but changes the ring to $\mathbb{Z}_q[x]/(x^p - x - 1)$ with $p$ and $q$ prime, so that the ring is a field and has none of the extra structure of $x^n - 1$ or $x^n + 1$ (no factors, no subfields, no cyclic automorphisms). Streamlined NTRU Prime (sntrup) encrypts by rounding instead of by adding a random error, and its parameters make decryption failures impossible. The family also has NTRU LPRime, a variant in the style of ring-LWE encryption. The parameter set sntrup761, combined with [X25519](/x25519/), is the default key exchange of OpenSSH 9.0 (2022). This page is about the design of NTRU Prime and its core; the 1998 scheme and the NIST round 3 NTRU are on the NTRUEncrypt page.

**Notation.** $p$ is a prime (the degree), $q$ a prime, and $R = \mathbb{Z}[x]/(x^p - x - 1)$, with $R/q$ and $R/3$ its quotients. "Small" means coefficients in $\{-1, 0, 1\}$. "Short" means small with exactly $w$ nonzero coefficients. $\mathrm{Round}(a)$ takes each coefficient of $a \in R/q$, centered in $[-(q-1)/2, (q-1)/2]$, to the nearest multiple of 3. For sntrup761, $p = 761$, $q = 4591$ and $w = 286$.

## In plain words

The owner picks a small secret g and a short secret f, and publishes h, which is g divided by 3f, modulo q. The sender picks a short random r, which is the secret to share. The sender multiplies h by r and rounds every number to a multiple of 3; this rounding is the noise that hides r. The owner multiplies the ciphertext by 3f. The result is g times r plus a small error, with numbers so small that nothing wraps around modulo q. Modulo 3 the error vanishes, and dividing by g gives back r. A shared key is a hash of r. The ring is chosen with care: it has no special structure that an attacker could use to split the problem into smaller ones.

## The problem

NTRU Prime solves the [key encapsulation](/key-encapsulation-mechanism/) problem. The design goal is to keep NTRU's speed and small keys while removing ring structure that could help attacks. The rings $\mathbb{Z}[x]/(x^n + 1)$ with $n$ a power of two, used by Kyber and Dilithium, have many automorphisms and subfields, and $x^n - 1$ has the factor $x - 1$. Attacks on some lattice problems with such structure are known (for example on ideal lattices and on overstretched NTRU), even though none breaks the standard schemes. NTRU Prime asks for a ring where these tools do not apply, and for parameters with no decryption failures.

## The algorithm

The pseudocode is the core of Streamlined NTRU Prime, as on this page's code.

```pseudo id=main
KEYGEN(p, q, w)
L1  g ← random small element of R
L2  if g is not invertible in R/3, go to L1;  v ← g⁻¹ in R/3
L3  f ← random short element of R            ▷ weight w
L4  h ← g / (3f) in R/q                       ▷ R/q is a field, so 3f is invertible
L5  return pk = h, sk = (f, v)

ENCRYPT(h, r)                                 ▷ r short
L6  t ← h·r in R/q
L7  return c ← Round(t)

DECRYPT((f, v), c)
L8  e ← 3f·c in R/q, centered
L9  r' ← e·v in R/3, centered
L10 if r' has weight w, return r'; else return (1, …, 1, 0, …, 0) (weight w)
```

**The KEM.** The full sntrup761 wraps this core. Key generation also stores the encoded public key, a hash of it, and a random value $\rho$ for implicit rejection. Encapsulation picks a random short $r$, encodes $c$ with a compact variable-radix encoding (1039 bytes), adds a confirmation hash of $r$, and derives the session key from hashes of $r$ and of the ciphertext, each hash with its own prefix byte. Decapsulation decrypts, encrypts again, and returns a key derived from $\rho$ instead if the ciphertexts differ. **The code on this page does not implement the encodings, the hashes or the confirmation**, so it cannot reproduce the official known answer tests; see Implementations.

**NTRU LPRime.** The second member of the family uses a public random $G$ and a public key $A = \mathrm{Round}(a G)$, as in ring-LWE encryption with rounding (see [learning with rounding](/learning-with-rounding/)). It encrypts a 256-bit value in the top bits of 256 coefficients. Its key generation needs no inversion and is faster, and its security rests on a different problem than the NTRU-style one.

**Why this ring.** $x^p - x - 1$ is irreducible over $\mathbb{Q}$, and its Galois group is the full symmetric group, so the number field has no proper subfields and no nontrivial automorphisms. $q$ is chosen so that $x^p - x - 1$ stays irreducible modulo $q$, which makes $R/q$ a field: every nonzero element is invertible, and line L4 never fails. The reduction rule is $x^p = x + 1$.

**Parameter set sntrup761.** $p = 761$, $q = 4591$, $w = 286$. Public key 1158 bytes, secret key 1763 bytes, ciphertext 1039 bytes, session key 32 bytes.

## Example

**Reduction.** In $R$, $x^{p-1} \cdot x = x^p = x + 1$, which the tests check for $p = 761$. A product of degree up to $2p - 2$ folds back with two terms: $x^{2p-2} = x^{p-2} \cdot x^p = x^{p-1} + x^{p-2}$. So each coefficient of a reduced product collects at most two products per pair of input coefficients.

**Rounding.** With $q = 4591$, a centered coefficient 1000 rounds to 999, $-1000$ to $-999$, 2 to 3, and the largest value 2295 stays 2295, which is $3 \cdot 765$. The rounding error is always $-1$, 0 or 1.

**The no-failure bound.** For sntrup761, $16 w + 1 = 4577 \le 4591 = q$, so the condition of the correctness proof holds and decryption never fails.

## Correctness

Let $\varepsilon = c - h r$ (centered), which is small by the rounding. Then $3 f c \equiv 3 f h r + 3 f \varepsilon = g r + 3 f \varepsilon \pmod q$. In $R$, a product of a small element and a short element has coefficients at most $2w$ in absolute value, because the rule $x^p = x + 1$ folds each product into at most two places. So $g r + 3 f \varepsilon$ has coefficients at most $2w + 6w = 8w$, which is below $q/2$ when $q \ge 16w + 1$. Line L8 then gets $g r + 3 f \varepsilon$ exactly, modulo 3 it is $g r$, and line L9 returns $r$. The full proof is in the proof file.

## Complexity

The cost is a few products in $R/q$ and $R/3$, $\Theta(p^2)$ with schoolbook multiplication. Since $q$ is prime but $p$ is not of the form that an NTT needs, fast code uses Karatsuba and Toom-Cook, or an NTT over a larger auxiliary modulus. Key generation computes two inverses, $\Theta(p^2)$ with the extended Euclidean algorithm or with a constant-time variant such as the divstep algorithm of Bernstein and Yang (2019). The code on this page uses Kronecker substitution on Python integers.

## Properties

- **No decryption failures.** The parameters satisfy $q \ge 16w + 1$, so attacks based on failures do not apply, and the KEM proof does not need a failure term.
- **Deterministic encryption.** The randomness is only $r$, and rounding replaces the extra error; this makes the re-encryption check of the KEM simple.
- **A field.** $R/q$ is a field, so every nonzero element is invertible and there is no ring homomorphism to a smaller ring modulo $q$.
- **Security.** Key recovery is an NTRU problem in this ring; message recovery is a rounding problem like LWR. The best known attacks are lattice reduction and hybrid attacks. NIST saw the non-cyclotomic ring as a useful hedge, and also noted that it has been studied less.

## Variants and improvements

- **sntrup653, sntrup761, sntrup857, sntrup953, sntrup1013, sntrup1277** are the Streamlined NTRU Prime sets of round 3, and ntrulpr with the same sizes are the LPRime sets.
- **sntrup761x25519-sha512** is the hybrid key exchange of OpenSSH; it combines the two shared secrets with SHA-512, so it stays secure if either part is secure.
- **NTRUEncrypt and NTRU (round 3)** use the cyclic ring $x^n - 1$, see [NTRUEncrypt](/ntru-encrypt/).

## When to use it

Use sntrup761 where it is already deployed, such as SSH, always as part of a [hybrid key exchange](/hybrid-key-exchange/). For new designs, prefer the NIST standard [ML-KEM](/crystals-kyber/); OpenSSH itself added an ML-KEM hybrid later. NTRU Prime is a good choice for those who want a ring without cyclotomic structure. The code on this page is only a study of the core.

## Pitfalls

- **Weight checks and sorting.** The short sampler and the weight check of line L10 must be constant time; the reference code samples short elements by a constant-time sort.
- **Rounding at the edge.** The largest centered value $(q-1)/2$ must round to a value in range; for $q = 4591$ it is already a multiple of 3.
- **Inversion.** Inversion in $R/3$ fails for some $g$; key generation must retry, and must do so without leaking timing.
- **Not interoperable.** This page's code has no encodings; its outputs are not sntrup761 keys or ciphertexts.

## Implementations

The Python code on this page is the core of Streamlined NTRU Prime with the sntrup761 parameters: key generation with the inverses, encryption by rounding, decryption with the weight check. Its tests check the reduction rule, the no-failure bound $q \ge 16w + 1$, that $h \cdot 3f = g$ is small, round trips, the bound on the coefficients in line L8, and that a wrong key fails. **There is no official vector on this page**: the known answer tests of sntrup761 cover the full KEM with its encodings, hashes and confirmation, which this code leaves out. The code is for study only: it is not constant time and must not be used to protect real data.

## History

Bernstein, Chuengsatiansup, Lange and van Vredendaal published NTRU Prime at SAC 2017, after a 2016 preprint that argued for removing cyclotomic structure. It was submitted to NIST in 2017 and was an alternate candidate in round 3 (2020 to 2022); NIST did not move it to round 4. OpenSSH added sntrup4591761x25519 in 2019 as an experiment, then sntrup761x25519-sha512 in version 8.5 (2021), and made it the default in version 9.0 (April 2022).

## References
