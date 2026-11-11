---
tag: PHGT6X
kind: algorithm
slug: unbalanced-oil-and-vinegar
name: Unbalanced oil and vinegar
aliases:
- UOV
- oil and vinegar
area: cryptography/post-quantum
level: advanced
summary: Multivariate signature with quadratic forms that vanish on a secret oil space. Fixing the vinegar variables makes signing linear. Unbroken since 1999, in round 3 of NIST's signature process.
model: word-ram
complexity:
  vars: {n: the number of variables v + o, m: "the number of equations, equal to the number o of oil variables"}
  time: {worst: O(m n^2), average: O(m n^2), best: O(m n^2)}
  space: {extra: O(m n^2)}
properties: {deterministic: false, randomized: true}
history:
  year: 1999
  people: [Aviad Kipnis, Jacques Patarin, Louis Goubin]
  note: Patarin proposed balanced oil and vinegar in 1997, Kipnis and Shamir broke it in 1998, and Kipnis, Patarin and Goubin repaired it in 1999 with more vinegar than oil variables.
prereqs: [multivariate-quadratic-problem, digital-signature]
see_also: [rainbow-signature, multivariate-cryptography, hidden-field-equations, existential-unforgeability, hash-and-sign-paradigm, crystals-dilithium, shake, xl-algorithm]
sources:
  - paper: "Aviad Kipnis, Jacques Patarin and Louis Goubin, Unbalanced oil and vinegar signature schemes, Eurocrypt 1999, LNCS 1592, pages 206 to 222"
    locator: the whole paper (the scheme with v > o, the extended Kipnis-Shamir attack of cost about q^(v - o - 1) o^4, and the advice v at least 2o)
  - paper: "Aviad Kipnis and Adi Shamir, Cryptanalysis of the oil and vinegar signature scheme, Crypto 1998, LNCS 1462, pages 257 to 266"
    locator: the whole paper (the invariant subspace attack on balanced oil and vinegar)
  - paper: "Jacques Patarin, The oil and vinegar signature scheme, Dagstuhl Workshop on Cryptography, September 1997"
    locator: the talk (balanced oil and vinegar, with as many vinegar as oil variables)
  - paper: "Ward Beullens, Improved cryptanalysis of UOV and Rainbow, Eurocrypt 2021, LNCS 12696, pages 348 to 373"
    locator: the intersection attack on UOV and the rectangular MinRank attack on Rainbow
  - paper: "Ward Beullens, MAYO: practical post-quantum signatures from oil-and-vinegar maps, SAC 2021, LNCS 13203, pages 355 to 376"
    locator: the whole paper (a small oil space whipped up to a larger map, for small public keys)
  - paper: "Koichi Sakumoto, Taizo Shirai and Harunaga Hiwatari, On provable security of UOV and HFE signature schemes against chosen-message attack, PQCrypto 2011, LNCS 7071"
    locator: the whole paper (EUF-CMA security of UOV with a random salt in the random oracle model)
  - url: "https://csrc.nist.gov/Projects/pqc-dig-sig/round-2-additional-signatures"
    title: "Ward Beullens, Ming-Shing Chen, Jintai Ding and others, UOV: Unbalanced Oil and Vinegar, algorithm specifications and supporting documentation, version 2.0, 2025"
    locator: the specification (the oil space view, the parameter sets uov-Is, uov-Ip, uov-III and uov-V, and key compression)
  - url: "https://doi.org/10.6028/NIST.IR.8610"
    title: NIST IR 8610, Status Report on the Second Round of the Additional Digital Signature Schemes for the NIST Post-Quantum Cryptography Standardization Process, May 2026
    locator: Section 3.11 (UOV advanced to round 3, the wedge attack and the small field attack, 96 byte signatures and expanded public keys over 200 kilobytes)
  - url: "https://eprint.iacr.org/2025/1143"
    title: Lars Ran, Wedges, oil, and vinegar, an analysis of UOV in characteristic 2, IACR ePrint 2025/1143
    locator: the whole paper (the wedge attack, which lowered the security of UOV parameter sets over fields of characteristic 2)
---

Unbalanced oil and vinegar (UOV) is a [multivariate](/multivariate-cryptography/) [signature](/digital-signature/) scheme by Kipnis, Patarin and Goubin (1999). The public key is $m$ quadratic forms in $n = v + o$ variables over a small field $\mathbb{F}_q$. The secret is a hidden subspace $O$ of dimension $o = m$, the oil space, on which all the forms vanish. Equivalently, in secret coordinates, no polynomial has a product of two oil variables. A signer fixes the $v$ vinegar variables at random, which leaves $m$ linear equations in the $m$ oil variables, and solves them. A verifier evaluates the public polynomials. Patarin's balanced version with $v = o$ (1997) fell to Kipnis and Shamir in 1998; with $v \ge 2o$ the scheme has resisted attack since 1999. UOV and three variants of it are in round 3 of the NIST process for additional post-quantum signatures.

**Notation.** $q$ is the field size, $v$ the number of vinegar variables, $o = m$ the number of oil variables and equations, and $n = v + o$. $F_k$ is the symmetric matrix of the central form $f_k(x) = x^T F_k x$, $S$ an invertible $n \times n$ matrix, and $P_k = S^T F_k S$ the public matrix, so $p_k(s) = s^T P_k s$. $O = S^{-1}\{(0, x_o)\}$ is the oil space. $H$ hashes a message and a salt to $\mathbb{F}_q^m$. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. **Security model.** The goal is existential unforgeability under chosen message attack ([EUF-CMA](/existential-unforgeability/)): $\mathrm{Adv}$ is the probability that $\mathcal{A}$, with the public key and a signing oracle, outputs a valid signature on a new message. With a random salt, Sakumoto, Shirai and Hiwatari (2011) proved EUF-CMA security in the random oracle model, assuming that the public map is hard to invert. In practice that rests on two assumptions: the [MQ problem](/multivariate-quadratic-problem/) for the public system, and the hardness of finding $O$ from the public key.

## In plain words

Take quadratic equations in two kinds of unknowns, vinegar and oil. Allow products of vinegar with vinegar and vinegar with oil, but never oil with oil. Now guess random values for all the vinegar unknowns. What remains has only oil unknowns, each appearing alone, so you have plain linear equations, which are easy.

To hide this shape, the signer mixes all unknowns with a secret linear change before publishing the equations. The published system looks like a random quadratic system, which is very hard to solve. A signature is a solution for the hash of the message. The scheme needs many more vinegar than oil unknowns, because an equal number lets an attacker find the hidden shape.

## The problem

Build a [hash-and-sign](/hash-and-sign-paradigm/) signature from a quadratic map $\mathcal{P} : \mathbb{F}_q^n \to \mathbb{F}_q^m$ that anyone can evaluate, but only the key owner can invert: for a target $t = H(M \,\|\, \mathrm{salt})$, find $s$ with $\mathcal{P}(s) = t$.

## The algorithm

```pseudo id=main
KEYGEN(q, v, o)                              ▷ n = v + o, m = o
L1  for k = 1..m: F_k ← a random symmetric n × n matrix over F_q with a zero oil × oil block
L2  S ← a random invertible n × n matrix over F_q
L3  for k = 1..m: P_k ← Sᵀ F_k S
L4  return pk = (P_1, ..., P_m) and sk = (F_1, ..., F_m, S)

SIGN(sk, M)
L5  salt ← 16 random bytes; t ← H(M ‖ salt) ∈ F_q^m
L6  x_v ← a random vector of F_q^v
L7  build the m × m linear system in x_o: x_vᵀ A_k x_v + 2 x_vᵀ B_k x_o = t_k for k = 1..m
L8  if the system is singular, go back to L6
L9  x_o ← its solution; x ← (x_v, x_o)
L10 return σ = (S⁻¹x, salt)

VERIFY(pk, M, σ = (s, salt))
L11 return true if sᵀ P_k s = H(M ‖ salt)_k for every k, else false
```

Here $A_k$ is the vinegar $\times$ vinegar block of $F_k$ and $B_k$ the vinegar $\times$ oil block. In odd characteristic a symmetric matrix holds a quadratic form; in characteristic 2 the specification uses upper triangular matrices instead.

**The oil space view.** All $P_k$ vanish on $O$: for $s, s' \in O$, $s^T P_k s' = 0$. Conversely, anyone who knows a basis of $O$ can sign without $F_k$ and $S$: pick a random $y$, and solve $\mathcal{P}(y + u) = t$ for $u \in O$, which is linear in $u$ because $\mathcal{P}(y + u) = \mathcal{P}(y) + 2 y^T P_k u$. The UOV specification uses this view, and so does every key recovery attack: the goal is $O$.

**The Kipnis-Shamir attack on balanced oil and vinegar.** When $v = o$, each central matrix maps the oil coordinates onto the vinegar coordinates. So for public combinations $W_1, W_2$ of the $P_k$, the matrix $W_1^{-1} W_2$ maps $O$ into $O$. Its characteristic polynomial is a square $g^2$, and an eigenvector with a one-dimensional eigenspace lies in $O$.

```pseudo id=attack
KIPNIS-SHAMIR(P_1, ..., P_m)                 ▷ v = o, so n = 2m
A1  repeat
A2      W_1, W_2 ← random linear combinations of the P_k, with W_1 invertible
A3      M ← W_1⁻¹ W_2
A4      for each eigenvalue λ of M in F_q with a one-dimensional eigenspace ⟨u⟩:
A5          if all P_k vanish on span(found ∪ {u}), add u to found
A6  until found has m independent vectors
A7  return found                             ▷ a basis of O: now sign with the oil space view
```

When $v > o$, the matrices $W_1^{-1} W_2$ no longer keep $O$ invariant. Kipnis, Patarin and Goubin showed that the attack still works with probability about $q^{-(v - o)}$ per try, so its cost grows like $q^{v - o - 1} o^4$, and they advised $v \ge 2o$.

## Example

**One central polynomial over $\mathbb{F}_{31}$.** Take vinegar $x_1, x_2$, oil $x_3$, and $f = x_1^2 + 2 x_1 x_3 + 3 x_2 x_3 + x_1 x_2$, with no $x_3^2$ term. Fix $x_1 = 1$ and $x_2 = 2$: $f = 1 + 2x_3 + 6x_3 + 2 = 3 + 8x_3$. To sign the target 5, solve $8 x_3 = 2$. Since $8 \cdot 4 = 32 \equiv 1$, $x_3 = 2 \cdot 4 = 8$, and indeed $f(1, 2, 8) = 1 + 16 + 48 + 2 = 67 \equiv 5 \pmod{31}$. As a symmetric matrix with entries in the order $x_1, x_2, x_3$, $f$ has rows $(1, 1/2, 1)$, $(1/2, 0, 3/2)$, $(1, 3/2, 0)$, where $1/2 = 16$ in $\mathbb{F}_{31}$.

**Toy keys.** The tests use $q = 31$ with $(v, o) = (8, 4)$ and $(12, 6)$. For $(12, 6)$ the public key has $6 \cdot \binom{19}{2} = 1026$ field elements, and a signature is 18 field elements and a 16 byte salt. The Kipnis-Shamir attack recovers $O$ for balanced keys with $v = o = 4$ and $v = o = 6$ from the public key alone, and the forged signatures verify. For $(v, o) = (8, 4)$ it finds nothing.

**Real sizes.** UOV has signatures as small as 96 bytes at NIST security category 1, and verification takes tens of thousands of cycles, but its expanded public keys are over 200 kilobytes (NIST IR 8610).

## Correctness

By the shape of $F_k$, $f_k(x_v, x_o) = x_v^T A_k x_v + 2 x_v^T B_k x_o$, so line L7 builds exactly the equations $f_k(x) = t_k$, and line L9 returns a solution $x$. Then $s = S^{-1} x$ satisfies $s^T P_k s = (Ss)^T F_k (Ss) = f_k(x) = t_k$, which is what line L11 checks. The proof file also proves the oil space view and the invariant subspace lemma behind the Kipnis-Shamir attack.

## Complexity

- **Signing.** Computing $x_v^T A_k x_v$ and the rows $2 x_v^T B_k$ costs $O(m v^2)$, solving the system $O(m^3)$, and $S^{-1}x$ costs $O(n^2)$, so $O(m n^2)$ field operations per try. A try fails only when the $m \times m$ system is singular, which for a random matrix happens with probability less than $1/(q - 1)$, so the expected number of tries is $O(1)$.
- **Verification.** $m$ quadratic forms in $n$ variables: $O(m n^2)$ field operations, and only additions and multiplications in a small field, which is why it is fast.
- **Key generation.** $m$ products $S^T F_k S$: $O(m n^3)$.
- **Space.** The public key has $m \binom{n+1}{2}$ field elements. Key compression in the specification stores part of it as a seed.

## Properties

- **Randomized signing** with a salt. The salt makes the signature distribution independent of the secret key, which the security proof needs.
- **Short signatures and fast verification**, but large public keys.
- **No known quantum speed-up** beyond Grover-type search inside the classical attacks.
- **Many signatures for one target**: the map has about $q^{n - m}$ preimages per value, and the signer returns one at random.

## Variants and improvements

- **Rainbow** (Ding and Schmidt, 2005) stacks UOV layers to shrink keys. It was broken in 2022; see [Rainbow](/rainbow-signature/).
- **MAYO** (Beullens, 2021) uses a small oil space that is too small for signing and a whipping map that combines several copies, which gives much smaller public keys.
- **QR-UOV** uses quotient rings to shrink the public key, and **SNOVA** uses a noncommutative matrix ring. With UOV and MAYO, they are the multivariate candidates of round 3 of the NIST process.
- **Attacks.** Beullens (2021) found the intersection attack, which uses several pairs of polar forms to find vectors in $O$ and lowered UOV security a little. In round 2 the wedge attack (Ran, 2025) and a key recovery attack over small fields (Furue and Ikematsu, 2026) put the parameter sets uov-Ip, uov-III and uov-V below their targets; NIST asked for new parameters, perhaps in odd characteristic.

## When to use it

UOV fits where very short signatures and very fast verification matter and a large public key is acceptable, for example a key that is stored once and checks many signatures. It is not yet a NIST standard, and its parameters are still being revised after the attacks of round 2. For general use pick a standard scheme from a vetted library, such as [ML-DSA](/crystals-dilithium/) in a FIPS 140 validated module.

## Pitfalls

- **Balanced parameters.** $v = o$ is broken by the attack above in polynomial time. $v$ must be clearly larger than $o$.
- **Too many vinegar variables.** In characteristic 2, systems with $n \ge m(m + 1)$ are solvable in polynomial time (Kipnis, Patarin and Goubin), so $v$ cannot be very large either.
- **Reused vinegar values.** Two signatures made with the same $x_v$ differ by a vector of $O$, which leaks the secret. Draw $x_v$ fresh from a good random source each time.
- **No salt.** Without the salt, signatures of the same message are linked to the secret and the proof does not apply.
- **Timing.** The retry loop in lines L6 to L8 and the field arithmetic must not leak secret data through timing. The code of this page does not try to avoid that.

## Implementations

The Python code is for study only. It is not constant time, it uses the random module, and the toy sizes give no security. It works over $\mathbb{F}_{31}$ with symmetric matrices, hashes with SHAKE256, and is not the UOV of the NIST submission: there is no $\mathbb{F}_{16}$ or $\mathbb{F}_{256}$, no key compression and no official encoding, so the official known answer tests do not apply, and there are no official vectors for these toy keys. The tests check the hand example above, the linear algebra against brute force over $\mathbb{F}_5$, the public key against the secret composition, sign and verify round trips, and the Kipnis-Shamir attack, all with fixed seeds.

## History

Patarin presented balanced oil and vinegar at a Dagstuhl workshop in 1997, inspired by his linearization attack on C*. Kipnis and Shamir broke it at Crypto 1998 with the invariant subspace attack. At Eurocrypt 1999 Kipnis, Patarin and Goubin proposed the unbalanced version and analyzed the attack for $v > o$. Ding and Schmidt built Rainbow on it in 2005. Sakumoto, Shirai and Hiwatari proved EUF-CMA security with a salt in 2011. After Rainbow fell in 2022, UOV itself, MAYO, QR-UOV and SNOVA entered the NIST process for additional signatures in 2023, moved to round 2 in October 2024, and to round 3 in May 2026.

## References
