---
tag: HYTKQP
kind: algorithm
slug: sidh
name: Supersingular isogeny Diffie-Hellman
aliases:
- SIDH
- SIKE
area: cryptography/post-quantum
level: research
summary: "Isogeny key exchange (Jao-De Feo, 2011) with p = 2^eA 3^eB - 1 and torsion images in the public keys. SIKE was its KEM form. Both are broken: Castryck-Decru, 2022."
model: word-ram
complexity:
  vars: {e: "the exponent e_A or e_B of one side; time counts operations in F_{p^2}"}
  time: {worst: Θ(e^2), average: Θ(e^2), best: Θ(e^2)}
  space: {extra: Θ(1)}
properties: {deterministic: false, randomized: true}
history:
  year: 2011
  people: [David Jao, Luca De Feo]
  note: Presented at PQCrypto 2011. SIKE, its KEM form, reached round 4 of the NIST process in July 2022 and was broken weeks later by Castryck and Decru.
prereqs: [supersingular-isogeny-problem, diffie-hellman, isogeny-based-cryptography, key-encapsulation-mechanism]
see_also: [castryck-decru-attack, csidh, nist-pqc-standardization, fujisaki-okamoto-transform, ecdh, crystals-kyber, hybrid-key-exchange, harvest-now-decrypt-later]
sources:
  - paper: "David Jao and Luca De Feo, Towards quantum-resistant cryptosystems from supersingular elliptic curve isogenies, PQCrypto 2011, LNCS 7071"
    locator: the key exchange with p = lA^eA lB^eB f -1, the torsion bases, the public keys with the images of the other basis, and the commutative diagram
  - paper: "Luca De Feo, David Jao and Jerome Plut, Towards quantum-resistant cryptosystems from supersingular elliptic curve isogenies, Journal of Mathematical Cryptology 8(3), 2014"
    locator: the journal version, with the optimal strategies that compute an isogeny of degree l^e in O(e log e) steps
  - url: "https://sike.org/files/SIDH-spec.pdf"
    title: David Jao and others, Supersingular Isogeny Key Encapsulation, specification for the NIST process, round 4 version, 2022
    locator: the parameter sets SIKEp434, SIKEp503, SIKEp610 and SIKEp751, the public key and ciphertext sizes, and the KEM built from the PKE
  - paper: "Steven D. Galbraith, Christophe Petit, Barak Shani and Yan Bo Ti, On the security of supersingular isogeny cryptosystems, ASIACRYPT 2016, LNCS 10031"
    locator: the adaptive attack that recovers a static SIDH key one bit at a time with manipulated public points
  - paper: "Craig Costello, Patrick Longa and Michael Naehrig, Efficient algorithms for supersingular isogeny Diffie-Hellman, CRYPTO 2016, LNCS 9814"
    locator: projective x-only arithmetic on Montgomery curves, the form that SIKE uses
  - paper: "Wouter Castryck and Thomas Decru, An efficient key recovery attack on SIDH, EUROCRYPT 2023, LNCS 14008"
    locator: the key recovery from the torsion images, with the run on SIKEp434
  - paper: doi:10.6028/NIST.IR.8545
    title: NIST, Status report on the fourth round of the NIST post-quantum cryptography standardization process, NIST IR 8545, 2025
    locator: the section on SIKE and the attacks that broke it
  - book: isbn:9781420071467
    title: Lawrence C. Washington, Elliptic Curves, Number Theory and Cryptography, 2nd edition, CRC Press, 2008
    locator: Theorem 12.16, Velu's formulas for the isogeny with a given finite kernel
---

Supersingular isogeny Diffie-Hellman (SIDH) is a key exchange in which two parties walk secret paths in a graph of supersingular elliptic curves and agree on the j-invariant of a common end curve. Jao and De Feo proposed it in 2011. SIKE, its key encapsulation form, reached round 4 of the [NIST process](/nist-pqc-standardization/) in July 2022. **SIDH and SIKE are broken.** In July 2022 the [Castryck-Decru attack](/castryck-decru-attack/) recovered SIKE keys on a single core in a short time, using the images of torsion points that SIDH must publish. Static SIDH keys were already broken in 2016 by the adaptive attack of Galbraith, Petit, Shani and Ti. This page describes SIDH as history and as a lesson. Do not use it.

**Notation.** $p = 2^{e_A} 3^{e_B} - 1$ is a prime, so $p \equiv 3 \pmod 4$. $E_0$ is a supersingular curve over $\mathbb{F}_{p^2}$, here $y^2 = x^3 + x$, and $E_0(\mathbb{F}_{p^2}) \cong (\mathbb{Z}/(p+1))^2$. $E[n]$ is the group of points of order dividing $n$. $(P_A, Q_A)$ is a basis of $E_0[2^{e_A}]$ and $(P_B, Q_B)$ a basis of $E_0[3^{e_B}]$. For a point $R$, $E/\langle R \rangle$ is the codomain of the isogeny with kernel $\langle R \rangle$. $[k]P$ is scalar multiplication. $j(E)$ is the j-invariant.

## In plain words

Both parties start from the same public curve. Each one picks a secret and uses it to take a long walk through a network of related curves, one step at a time. Each publishes the end of the walk and also where some agreed public points ended up.

Those extra points let the other party repeat the same secret walk from the new starting place. Both second walks end at the same curve, seen from two sides, so both parties now hold the same number that names this curve. That number is the shared secret.

The extra points were the weak spot. In 2022 researchers showed that they reveal the secret walk quickly, so the scheme is broken.

## The problem

Two parties want a shared secret over a public channel, as in [Diffie-Hellman](/diffie-hellman/), from a problem that a quantum computer cannot solve with Shor's algorithm. The hoped hard problem was the SIDH variant of the [supersingular isogeny problem](/supersingular-isogeny-problem/): given $E_A$ and the images $\varphi_A(P_B)$, $\varphi_A(Q_B)$, find $\varphi_A$. That variant turned out to be easy.

## The algorithm

Public parameters: $p$, $E_0$, $(P_A, Q_A)$ and $(P_B, Q_B)$. Alice works with $\ell = 2$, $e = e_A$; Bob with $\ell = 3$, $e = e_B$. KEYGEN for Alice pushes Bob's basis through her isogeny, and the other way round.

```pseudo id=main
KEYGEN(ℓ, e, P, Q, P', Q')                  ▷ (P, Q): own basis of E0[ℓ^e]; (P', Q'): the other side's basis
L1  s ← uniform in {0, …, ℓ^e − 1}
L2  R ← P + [s]Q                             ▷ a point of order ℓ^e
L3  (E, U, V) ← ISOGENY(E0, R, ℓ, e, [P', Q'])
L4  return secret s, public key (E, U, V)

ISOGENY(E, R, ℓ, e, points)                 ▷ E → E/⟨R⟩ as e steps of degree ℓ
L5  for i ← 0 to e − 1 do
L6      T ← [ℓ^(e − 1 − i)]R                ▷ T has order ℓ
L7      (E, φ) ← VELU(E, T)                  ▷ isogeny with kernel ⟨T⟩
L8      R ← φ(R); points ← φ(points)
L9  return (E, points)

SHARED(ℓ, e, s, (E, U, V))                 ▷ (E, U, V): the other side's public key
L10 R' ← U + [s]V
L11 (E', _) ← ISOGENY(E, R', ℓ, e, [])
L12 return j(E')
```

The shared key is $j(E_0/\langle R_A, R_B \rangle)$, reached by both paths of the commutative diagram:

$$\begin{array}{ccc} E_0 & \xrightarrow{\ \varphi_A\ } & E_A \\ {\scriptstyle \varphi_B} \downarrow & & \downarrow {\scriptstyle \varphi'_B} \\ E_B & \xrightarrow{\ \varphi'_A\ } & E_{AB} \end{array}$$

Here $\ker \varphi_A = \langle R_A \rangle$, $\ker \varphi'_A = \langle \varphi_B(R_A) \rangle$, and the same with $A$ and $B$ swapped. Alice can compute $\varphi_B(R_A) = U_B + [a] V_B$ only because Bob published the images $U_B = \varphi_B(P_A)$ and $V_B = \varphi_B(Q_A)$.

**SIKE.** SIKE turned this into a KEM. Bob's ephemeral key is the ciphertext, the shared $j$ is hashed into a mask for a random message $m$, and an FO-type transform ([Fujisaki-Okamoto](/fujisaki-okamoto-transform/)) re-encrypts on decapsulation to reject manipulated ciphertexts. The public key holds the $x$-coordinates of $\varphi(P)$, $\varphi(Q)$ and $\varphi(P - Q)$, which are three elements of $\mathbb{F}_{p^2}$. The round 4 parameter sets were:

| Set | $p$ | NIST category | Public key (bytes) | Ciphertext (bytes) |
|---|---|---|---|---|
| SIKEp434 | $2^{216} 3^{137} - 1$ | 1 | 330 | 346 |
| SIKEp503 | $2^{250} 3^{159} - 1$ | 2 | 378 | 402 |
| SIKEp610 | $2^{305} 3^{192} - 1$ | 3 | 462 | 486 |
| SIKEp751 | $2^{372} 3^{239} - 1$ | 5 | 564 | 596 |

The sizes are without compression; compressed versions were smaller still, for example 197 bytes for the SIKEp434 public key. These small keys were the main reason for the interest in SIKE.

## Example

The code with this page runs SIDH at the toy prime $p = 2^4 \cdot 3^3 - 1 = 431$. **It is a toy:** the secret spaces have 16 and 27 elements. $E_0 : y^2 = x^3 + x$ has $j = 1728 \equiv 4 \pmod{431}$. With seed 1 the bases are

- $P_A = (374 + 165i,\ 130 + 206i)$ and $Q_A = (118 + 44i,\ 48 + 426i)$ of order 16,
- $P_B = (84 + 404i,\ 176 + 68i)$ and $Q_B = (80 + 294i,\ 391 + 395i)$ of order 27.

With seed 2024 the secrets are $a = 15$ and $b = 5$.

1. Alice takes four 2-isogenies from $E_0$ to $E_A$ with $j(E_A) = 242$. She publishes $\varphi_A(P_B) = (79 + 375i,\ 81 + 212i)$ and $\varphi_A(Q_B) = (10 + 414i,\ 22 + 72i)$.
2. Bob takes three 3-isogenies to $E_B$ with $j(E_B) = 426 + 306i$. He publishes $\varphi_B(P_A) = (204 + 176i,\ 242 + 396i)$ and $\varphi_B(Q_A) = (62 + 257i,\ 425 + 377i)$.
3. Alice computes $E_B / \langle \varphi_B(P_A) + [15] \varphi_B(Q_A) \rangle$ and Bob computes $E_A / \langle \varphi_A(P_B) + [5] \varphi_A(Q_B) \rangle$. Both get $j = 141 + 42i$.

At this size the key spaces are tiny. Alice's 16 secrets give only 10 different curves $E_A$, and Bob's 27 secrets give 14, because the graph has only 37 vertices. An attacker can try all secrets at once; the [Castryck-Decru page](/castryck-decru-attack/) does that with a check on the torsion images.

The code uses short Weierstrass curves and Velu's formulas. SIKE uses $x$-only arithmetic on Montgomery curves (Costello, Longa and Naehrig, 2016). The isogenies are the same up to isomorphism, so the shared $j$ is the same, but the code is not the SIKE specification and does not reproduce its test vectors. It is for study only and is not constant time. Use ML-KEM ([CRYSTALS-Kyber](/crystals-kyber/)) from a FIPS 140 validated module for real key exchange.

## Correctness

Lines L5 to L9 compute an isogeny with kernel exactly $\langle R \rangle$: each step removes one factor $\ell$ of the order of the image of $R$. Because isogenies are group homomorphisms, $U_B + [a] V_B = \varphi_B(R_A)$, so Alice's second isogeny has kernel $\langle \varphi_B(R_A) \rangle$, and her composite $E_0 \to E_{BA}$ has kernel $\langle R_A, R_B \rangle$. Bob's composite has the same kernel. Two separable isogenies with the same kernel have isomorphic codomains, so both get the same $j$. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Line L6 costs $O(e)$ point doublings or triplings in step $i$, so the loop does $\Theta(e^2)$ curve operations. Each Velu step of degree 2 or 3 and each push costs $O(1)$ curve operations. Each curve operation costs $O(1)$ operations in $\mathbb{F}_{p^2}$, each $O(M(\log p))$ bit operations, where $M(n)$ is the cost of multiplying $n$-bit numbers. The optimal strategies of De Feo, Jao and Plut cut the count to $\Theta(e \log e)$ by storing $O(\log e)$ intermediate points. Since $e_A \approx \frac{1}{2} \log_2 p$, SIKEp434 needs a few hundred steps per isogeny. SIKE was one of the slowest round 3 KEMs, much slower than the lattice KEMs, which was the price of its small keys.

## Properties

- The shared secret is a j-invariant, an element of $\mathbb{F}_{p^2}$, not a curve, because the two parties reach isomorphic but not equal curves.
- The scheme is not symmetric: the two parties use different primes ($2$ and $3$) and different torsion bases.
- Unlike in [CSIDH](/csidh/), there is no commutative group action. The diagram commutes only because each party sends the images of the other's torsion basis.
- Randomized: each key pair uses a fresh secret.

## Variants and improvements

- **SIKE.** The KEM form, with key compression and an FO-type transform; see above.
- **Optimal strategies and compression.** De Feo, Jao and Plut (2014) for the isogeny chain; Costello, Longa and Naehrig (2016) for $x$-only Montgomery arithmetic; several papers on public key compression.
- **B-SIDH.** Costello (2019) let the two torsion groups lie in $E(\mathbb{F}_{p^2})$ and its quadratic twist, to allow a smaller $p$. It is broken by the same attacks.
- **After the attack.** M-SIDH and MD-SIDH (Fouotsa, Moriya and Petit, EUROCRYPT 2023) hide the torsion images with a scalar or a random degree, at the cost of much larger parameters. FESTA (Basso, Maino and Pope, ASIACRYPT 2023) uses the attack itself as a trapdoor. SQIsign uses isogenies without torsion images in the public key.

## When to use it

Never, for security. SIDH and SIKE give no security: the secret is recovered in polynomial time from a public key. Use them only to study isogeny arithmetic or the attacks. For a post-quantum key exchange, use ML-KEM, alone or in a [hybrid](/hybrid-key-exchange/) with X25519.

## Pitfalls

- **Static keys.** Galbraith, Petit, Shani and Ti (2016) showed that a party who reuses a key can be made to leak it one bit per session: the attacker sends $\varphi_B(P_A)$ and $\varphi_B(Q_A) + [2^{e_A - 1}] \varphi_B(P_A)$ and checks whether the shared keys still agree. This is why SIKE used the FO transform with re-encryption. Plain SIDH is safe only with ephemeral keys, and since 2022 not even then.
- **Torsion images.** The images of $P_B$ and $Q_B$ were thought to be harmless. They are exactly what the polynomial time attacks use. This is the main lesson of SIDH: extra public information can turn a hard problem into an easy one.
- **Public key checks.** Points of the wrong order, or curves that are not supersingular, lead to wrong or leaking results. SIKE decapsulation checks by re-encryption.
- **Side channels.** The secret controls the kernel point, and there are fault and zero-value attacks on implementations. The toy code takes no care with this.

## Implementations

## History

David Jao and Luca De Feo presented SIDH at PQCrypto 2011, building on the hash of Charles, Goren and Lauter (2009) and the ordinary-curve scheme of Rostovtsev and Stolbunov. The journal version with optimal strategies followed in 2014. Galbraith, Petit, Shani and Ti broke static keys with an adaptive attack in 2016. SIKE was submitted to the NIST process in 2017, stayed as an alternate in round 3, and moved to round 4 in July 2022. On 30 July 2022, Castryck and Decru posted ePrint 2022/975, which recovered SIKEp434 keys on one core in a short time; Maino, Martindale, Panny, Pope and Wesolowski, and then Robert, extended the attack to every starting curve and to polynomial time. All three papers appeared at EUROCRYPT 2023. NIST did not select SIKE.

## References
