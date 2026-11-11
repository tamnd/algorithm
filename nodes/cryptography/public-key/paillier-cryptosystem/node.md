---
tag: 97TJVN
kind: algorithm
slug: paillier-cryptosystem
name: Paillier cryptosystem
aliases:
- Paillier encryption
area: cryptography/public-key
level: advanced
summary: "Public-key encryption c = g^m r^N mod N^2. It is additively homomorphic, IND-CPA under the decisional composite residuosity assumption, and malleable (Paillier 1999)."
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of N}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1999
  people: [Pascal Paillier]
  note: Paillier presented the scheme at Eurocrypt 1999. Damgard and Jurik generalized it to the modulus N^(s+1) and gave threshold decryption at PKC 2001.
prereqs: [decisional-composite-residuosity, ind-cpa-security, modular-exponentiation, carmichael-function]
see_also: [homomorphic-encryption, okamoto-uchiyama-cryptosystem, naccache-stern-cryptosystem, goldwasser-micali-cryptosystem, elgamal-encryption, threshold-cryptography, private-set-intersection, non-malleability]
sources:
  - paper: "Pascal Paillier, Public-key cryptosystems based on composite degree residuosity classes, Eurocrypt 1999, LNCS 1592, pages 223 to 238"
    locator: Section 2 (the classes and the function L), Section 3 (the problems Class and D-Class), Section 4 (Scheme 1 and its semantic security under the decisional composite residuosity assumption), Section 7 (decryption with the Chinese remainder theorem)
  - paper: "Ivan Damgard and Mads Jurik, A generalisation, a simplification and some applications of Paillier's probabilistic public-key system, PKC 2001, LNCS 1992, pages 119 to 136"
    locator: the scheme modulo N^(s+1), the choice g = N + 1, threshold decryption, and the election scheme
  - paper: "Michael J. Freedman, Kobbi Nissim and Benny Pinkas, Efficient private matching and set intersection, Eurocrypt 2004, LNCS 3027, pages 1 to 19"
    locator: the protocol that evaluates an encrypted polynomial with an additively homomorphic scheme such as Paillier
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the section on the Paillier encryption scheme (the isomorphism of Z_N x Z_N^* with Z_(N^2)^*, the scheme with g = N + 1, and its CPA security under DCR)
  - url: "https://www.iso.org/standard/67740.html"
    title: ISO/IEC 18033-6:2019, IT Security techniques, Encryption algorithms, Part 6, Homomorphic encryption
    locator: the clause that specifies Paillier encryption (not checked against the full text)
---

The Paillier cryptosystem is a [public-key encryption](/public-key-encryption/) scheme that Pascal Paillier published in 1999. The public key is an RSA modulus $N = pq$, and a message $m \in \mathbb{Z}_N$ is sent as $c = g^m r^N \bmod N^2$ with a fresh random $r$ and, in the usual choice, $g = N + 1$. The product of two ciphertexts encrypts the sum of the messages, so the scheme is additively [homomorphic](/homomorphic-encryption/). It is [IND-CPA](/ind-cpa-security/) secure under the [decisional composite residuosity assumption](/decisional-composite-residuosity/) (DCR), with a tight reduction, and it is malleable, so it is not IND-CCA secure.

**Notation.** $N = pq$ is the modulus, with $p$ and $q$ distinct primes of the same length; on this page $q$ is a prime. $b$ is the number of binary digits of $N$. As in Paillier's paper, $\lambda = \lambda(N) = \operatorname{lcm}(p-1, q-1)$ is the [Carmichael function](/carmichael-function/) of $N$, not the security parameter. $L(x) = (x - 1)/N$ for $x \equiv 1 \pmod N$. $\mathcal{A}$ is an adversary that runs in time $t$, and $\mathrm{Adv}$ is an advantage. The security result is in the standard model.

## In plain words

The receiver publishes a large number that is the product of two secret primes. The sender encodes the message as a power of a fixed public value and multiplies it by a random mask. Only someone who knows the two primes can raise the ciphertext to a secret power that removes the mask. What is left reveals the message with one division.

The useful property is that anyone can add encrypted numbers. The product of two ciphertexts is a ciphertext of the sum of the two messages. A ciphertext raised to a known number is a ciphertext of the message times that number. An election server can add encrypted votes without seeing any of them. The same property lets an attacker change a ciphertext in a known way, so the scheme alone does not protect integrity.

## The problem

Paillier solves [public-key encryption](/public-key-encryption/) for messages in $\mathbb{Z}_N$, with the extra requirement that sums can be computed on ciphertexts. Its security rests on two problems from Paillier's paper. The composite residuosity class problem asks for $m$ given $c = g^m r^N \bmod N^2$; it is the one-wayness of the scheme. The decisional composite residuosity problem asks to tell an $N$-th residue modulo $N^2$ from a uniform element of $\mathbb{Z}_{N^2}^*$; it is the semantic security of the scheme. Both are no harder than factoring $N$.

## The algorithm

```pseudo id=main
PAILLIER-KEYGEN(b)
L1  repeat p, q ← random primes of b/2 binary digits until p ≠ q and gcd(pq, (p − 1)(q − 1)) = 1
L2  N ← p·q, λ ← lcm(p − 1, q − 1)
L3  μ ← λ^(−1) mod N                       ▷ for g = N + 1, L(g^λ mod N²) = λ mod N
L4  return the public key N and the private key (N, λ, μ)

PAILLIER-ENCRYPT(N, m)                     ▷ m ∈ Z_N
L5  r ← a uniform element of Z_N^*
L6  c ← (1 + m·N) · r^N mod N²             ▷ (1 + N)^m = 1 + mN (mod N²)
L7  return c

PAILLIER-DECRYPT((N, λ, μ), c)
L8  if not (0 < c < N² and gcd(c, N) = 1) then return ⊥
L9  u ← c^λ mod N²                         ▷ u = 1 + mλN (mod N²)
L10 return ((u − 1) / N) · μ mod N         ▷ the division is exact

EVAL: ADD(c1, c2) = c1·c2 mod N²,  ADD-PLAIN(c, k) = c·(1 + kN) mod N²,  MUL-PLAIN(c, k) = c^k mod N²
```

Line L6 uses the binomial theorem: $(1 + N)^m = 1 + mN + \binom{m}{2}N^2 + \cdots \equiv 1 + mN \pmod{N^2}$, so the base $g = N + 1$ costs one multiplication instead of an exponentiation. Line L9 removes the random factor because $r^{N\lambda} \equiv 1 \pmod{N^2}$. When both primes have the same length, the condition of line L1 holds by itself, since then $p \nmid q - 1$ and $q \nmid p - 1$.

Paillier's paper allows any $g \in \mathbb{Z}_{N^2}^*$ whose order is a nonzero multiple of $N$; decryption is then $m = L(c^\lambda \bmod N^2) / L(g^\lambda \bmod N^2) \bmod N$. The choice $g = N + 1$ is from Damgard and Jurik (2001) and from the textbook of Katz and Lindell, and it loses nothing: Paillier shows that the class problem is random self-reducible over $g$, so its hardness does not depend on the choice of a valid $g$.

## Example

Take the toy key $p = 7$, $q = 11$. Then $N = 77$, $N^2 = 5929$, $\lambda = \operatorname{lcm}(6, 10) = 30$ and $\mu = 30^{-1} \bmod 77 = 18$, since $30 \cdot 18 = 540 = 7 \cdot 77 + 1$.

| step | computation | value |
|---|---|---|
| L5 | message and randomness | $m = 42$, $r = 23$ |
| L6 | $g^m = 1 + 42 \cdot 77$ | 3235 |
| L6 | $r^N = 23^{77} \bmod 5929$ | 606 |
| L6 | $c = 3235 \cdot 606 \bmod 5929$ | 3840 |
| L9 | $u = 3840^{30} \bmod 5929$ | $2157 = 1 + 28 \cdot 77$ |
| L10 | $L(u) \cdot \mu = 28 \cdot 18 \bmod 77$ | 42 |

A second ciphertext of $15$ with $r = 10$ is $3442$. The product $3840 \cdot 3442 \bmod 5929 = 1539$ decrypts to $57 = 42 + 15$. The power $3840^3 \bmod 5929 = 3774$ decrypts to $49 = 3 \cdot 42 \bmod 77$.

## Correctness

Decryption returns $m$ for every $m \in \mathbb{Z}_N$ and every $r \in \mathbb{Z}_N^*$. The reason is that every element of $\mathbb{Z}_{N^2}^*$ raised to $N\lambda$ is 1, so $c^\lambda = (1 + N)^{m\lambda} r^{N\lambda} \equiv 1 + m\lambda N \pmod{N^2}$, and $\lambda$ is invertible modulo $N$. The full proof is in the proof file.

## Complexity

Let $b$ be the number of binary digits of $N$. With schoolbook arithmetic, a multiplication modulo $N^2$ (numbers of $2b$ binary digits) costs $\Theta(b^2)$, and an exponentiation with an exponent of $b$ binary digits costs $\Theta(b)$ such multiplications by [modular exponentiation](/modular-exponentiation/).

- **Key generation**: two random primes of $b/2$ digits, as for [RSA](/rsa-cryptosystem/), and one inversion modulo $N$.
- **Encryption**: one exponentiation $r^N \bmod N^2$, so $\Theta(b^3)$. The value $r^N$ does not depend on the message, so it can be computed ahead of time; then encryption is two multiplications.
- **Decryption**: one exponentiation $c^\lambda \bmod N^2$, $\Theta(b^3)$. Paillier's Section 7 computes it modulo $p^2$ and $q^2$ and joins the results with the [Chinese remainder theorem](/chinese-remainder-theorem/), which uses half-length moduli and half-length exponents.
- **Homomorphic operations**: ADD is one multiplication modulo $N^2$; MUL-PLAIN by $k$ is an exponentiation with exponent $k$.
- **Size**: a ciphertext has $2b$ binary digits for a message of $b$ binary digits, an expansion factor of 2.

## Properties

### IND-CPA security under DCR

The DCR advantage of a distinguisher $\mathcal{B}$ is

$$\mathrm{Adv}^{\mathrm{dcr}}(\mathcal{B}) = \bigl|\Pr[\mathcal{B}(N, y^N \bmod N^2) = 1] - \Pr[\mathcal{B}(N, z) = 1]\bigr|,$$

with $N$ from PAILLIER-KEYGEN, $y$ uniform in $\mathbb{Z}_{N^2}^*$ and $z$ uniform in $\mathbb{Z}_{N^2}^*$.

**Theorem.** For every IND-CPA adversary $\mathcal{A}$ against Paillier there is a DCR distinguisher $\mathcal{B}$ with $\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}(\mathcal{A}) = 2\,\mathrm{Adv}^{\mathrm{dcr}}(\mathcal{B})$, where $\mathrm{Adv}^{\mathrm{ind\text{-}cpa}} = |\Pr[\beta' = 1 \mid \beta = 1] - \Pr[\beta' = 1 \mid \beta = 0]|$. $\mathcal{B}$ runs in the time of $\mathcal{A}$ plus one multiplication modulo $N^2$. The reduction is tight.

*Proof.* $\mathcal{B}$ gets $(N, z)$. It gives $N$ to $\mathcal{A}$ as the public key. When $\mathcal{A}$ outputs $m_0, m_1 \in \mathbb{Z}_N$, $\mathcal{B}$ draws a uniform bit $\beta$ and gives $\mathcal{A}$ the challenge $c^* = (1 + m_\beta N) \cdot z \bmod N^2$. It outputs 1 if $\mathcal{A}$ outputs $\beta' = \beta$, else 0.

Case $z = y^N$. For each integer $k$, $(y + kN)^N \equiv y^N \pmod{N^2}$ by the binomial theorem, because every term after the first has a factor $N \cdot N$. So $y^N$ depends only on $y \bmod N$. The reduction modulo $N$ maps $\mathbb{Z}_{N^2}^*$ onto $\mathbb{Z}_N^*$, and each unit modulo $N$ has exactly $N$ preimages, all of them units. So $y \bmod N$ is uniform in $\mathbb{Z}_N^*$, and $z$ has the distribution of $r^N$ in line L6. Then $c^*$ is a real encryption of $m_\beta$, and $\Pr[\mathcal{B} = 1] = \tfrac12 + \tfrac12 (\Pr[\beta' = 1 \mid \beta = 1] - \Pr[\beta' = 1 \mid \beta = 0])$.

Case $z$ uniform in $\mathbb{Z}_{N^2}^*$. The factor $1 + m_\beta N$ is a unit modulo $N^2$, and multiplication by a unit is a bijection of $\mathbb{Z}_{N^2}^*$. So $c^*$ is uniform and independent of $\beta$, the view of $\mathcal{A}$ does not depend on $\beta$, and $\Pr[\mathcal{B} = 1] = \tfrac12$.

The difference of the two cases is half the bracket. If the bracket is negative, flip the output of $\mathcal{A}$; this does not change its advantage. So $\mathrm{Adv}^{\mathrm{dcr}}(\mathcal{B}) = \tfrac12 \mathrm{Adv}^{\mathrm{ind\text{-}cpa}}(\mathcal{A})$. $\square$

The one-wayness of the scheme is the composite residuosity class problem, which Paillier shows is no harder than the RSA problem with exponent $N$, and so no harder than factoring. The [DCR page](/decisional-composite-residuosity/) gives these relations.

### Homomorphic properties and malleability

- **Addition.** $c_1 c_2 = (1+N)^{m_1 + m_2} (r_1 r_2)^N$ encrypts $m_1 + m_2 \bmod N$.
- **Multiplication by a known constant.** $c^k = (1+N)^{km} (r^k)^N$ encrypts $km \bmod N$. With $k = -1$ this negates, so subtraction also works. Multiplying two encrypted values is not possible with Paillier alone.
- **Rerandomization.** $c \cdot s^N$ for a fresh $s$ encrypts the same message and cannot be linked to $c$ under DCR.
- **Malleable, so not IND-CCA2.** Given the challenge $c^*$, the ciphertext $c^* (1 + N)$ is different and encrypts $m_\beta + 1$. One decryption query wins the IND-CCA2 game. This is a [chosen-ciphertext attack](/chosen-ciphertext-attack/); see [non-malleability](/non-malleability/) and [IND-CCA security](/ind-cca-security/). Every scheme with a public homomorphism has this problem.

## Variants and improvements

- **Damgard-Jurik.** Work modulo $N^{s+1}$: $c = (1 + N)^m r^{N^s} \bmod N^{s+1}$ with $m \in \mathbb{Z}_{N^s}$. The expansion falls to $(s+1)/s$, and the security still rests on DCR. Damgard and Jurik (2001) also gave threshold decryption, in which $\lambda$ is shared among servers so that no single server can decrypt.
- **Paillier's Schemes 2 and 3.** The same paper gives a trapdoor permutation (Scheme 2) and a faster variant where $g$ has small order and the randomness lives in a subgroup (Scheme 3), with security under a related assumption.
- **Okamoto-Uchiyama and Naccache-Stern.** Two earlier additively homomorphic schemes. [Okamoto-Uchiyama](/okamoto-uchiyama-cryptosystem/) (1998) uses $N = p^2 q$ and is one-way if factoring is hard. [Naccache-Stern](/naccache-stern-cryptosystem/) (1998) uses a message space that is a product of small primes. Paillier's scheme has a larger message space than both.
- **Chosen-ciphertext security.** Wrap the scheme in the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) or add zero-knowledge proofs of plaintext knowledge, at the cost of the homomorphism for the parts that are checked.

## When to use it

Use Paillier when a protocol needs to add encrypted numbers held by different parties: tallies in electronic voting (Damgard and Jurik 2001), sums in secure aggregation, the polynomial evaluation in the [private set intersection](/private-set-intersection/) protocol of Freedman, Nissim and Pinkas (2004), and many steps in [secure multiparty computation](/secure-multiparty-computation/) and threshold signing. Always combine it with zero-knowledge proofs that the inputs are well formed, for example that a vote is 0 or 1. Exponential [ElGamal](/elgamal-encryption/) also adds, and has smaller ciphertexts on an elliptic curve, but decryption needs a small discrete logarithm; Paillier decrypts any value in $\mathbb{Z}_N$. For plain confidentiality of data, use [hybrid encryption](/hybrid-encryption/) with an IND-CCA2 KEM, not Paillier. For many multiplications on encrypted data, use a lattice scheme from [homomorphic encryption](/homomorphic-encryption/).

## Pitfalls

- **Reused randomness.** If two messages use the same $r$, then $c_1 c_2^{-1} = (1+N)^{m_1 - m_2}$, and anyone can read $m_1 - m_2 = L(c_1 c_2^{-1} \bmod N^2)$ without the key. Draw $r$ fresh from a cryptographic generator each time.
- **Overflow.** Sums wrap modulo $N$. A tally of $n$ values below $v$ is exact only if $n v < N$. Negative numbers need an encoding, for example values above $N/2$ count as negative.
- **Decryption oracles.** The malleability above means that a server that decrypts ciphertexts from others, and shows anything about the result, can leak the plaintext of a challenge ciphertext.
- **Unchecked inputs in protocols.** A dishonest voter can encrypt 100 instead of 1, and the homomorphic sum hides it. Each input needs a proof of validity.
- **Small keys.** The scheme falls if $N$ is factored, so $N$ needs the same size as an RSA modulus: 3072 binary digits for about 128-bit security by NIST SP 800-57 Part 1. The 512-digit keys of the tests are not secure.
- **Not checking the ciphertext.** Line L8 rejects values outside $\mathbb{Z}_{N^2}^*$, which no honest sender produces. Code that skips the check gives an attacker more freedom to probe the decryption.

## Implementations

The Python code is for study only. It is not constant time, it is not protected against side channels, and it must not protect real data. Use a maintained library with keys of at least 3072 binary digits, for example the Paillier code of a vetted MPC framework. There are no official test vectors in an open standard: ISO/IEC 18033-6 has numerical examples in Annex B, but its text is not free, so the tests do not use them. The tests check the example above, all messages and all $r$ of the toy key $N = 77$, round trips, the additive homomorphism, multiplication by constants, an encrypted tally, rerandomization, the one-query chosen-ciphertext attack, and the $N$-th residue test with $\lambda$, on a 512-binary-digit key with a fixed seed.

## History

Goldwasser and Micali (1984) gave the first probabilistic encryption scheme, based on quadratic residues, and it already had an XOR homomorphism on single bits. Benaloh (1994), Naccache and Stern (1998) and Okamoto and Uchiyama (1998) built schemes with larger message spaces. Paillier (1999) found the classes of $N$-th residues modulo $N^2$ and obtained a message space of the full size of $N$, with a simple decryption function. Damgard and Jurik (2001) generalized it to $N^{s+1}$ and built threshold decryption and voting on it. ISO/IEC 18033-6 (2019) standardizes Paillier encryption together with exponential ElGamal.

## References
