---
tag: V93QWB
kind: algorithm
slug: elgamal-encryption
name: ElGamal encryption
aliases:
- ElGamal cryptosystem
area: cryptography/public-key
level: core
summary: Public-key encryption that multiplies the message by a Diffie-Hellman value. IND-CPA under DDH in a prime order group, but malleable and multiplicatively homomorphic.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of p}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1985
  people: [Taher ElGamal]
  note: Published in IEEE Transactions on Information Theory in 1985, with the ElGamal signature scheme. Tsiounis and Yung proved IND-CPA security under DDH in 1998.
prereqs: [decisional-diffie-hellman, ind-cpa-security, modular-exponentiation]
see_also: [cramer-shoup-cryptosystem, diffie-hellman, homomorphic-encryption, non-malleability, ecies, safe-prime, elgamal-signature, fujisaki-okamoto-transform]
sources:
  - url: "https://doi.org/10.1109/TIT.1985.1057074"
    title: Taher ElGamal, A public key cryptosystem and a signature scheme based on discrete logarithms, IEEE Transactions on Information Theory 31(4), pages 469 to 472, 1985
    locator: Section II (the encryption scheme)
  - paper: "Yiannis Tsiounis and Moti Yung, On the security of ElGamal based encryption, PKC 1998, LNCS 1431, pages 117 to 134"
    locator: the proof that ElGamal encryption is semantically secure if and only if DDH holds
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Section 8.4.1, Algorithms 8.17 and 8.18, Example 8.19, Notes 8.21 and 8.23
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 12, the El Gamal encryption scheme and the proof of its CPA security under DDH
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 11, the section on ElGamal encryption and its security under DDH
  - paper: "Ronald Cramer, Rosario Gennaro and Berry Schoenmakers, A secure and optimally efficient multi-authority election scheme, Eurocrypt 1997, LNCS 1233, pages 103 to 118"
    locator: the use of ElGamal with the message in the exponent to add encrypted votes
  - url: "https://nvd.nist.gov/vuln/detail/CVE-2018-6829"
    title: NIST National Vulnerability Database, CVE-2018-6829, Libgcrypt ElGamal implementation without semantic security, 2018
    locator: the description of the record (plaintexts not encoded into the prime order subgroup)
---

ElGamal encryption is the [public-key encryption](/public-key-encryption/) scheme that Taher ElGamal published in 1985. The public key is $h = g^x$ in a cyclic group, and a message $m$ in the group is sent as $(g^r, m h^r)$ for a fresh random $r$: the sender multiplies the message by a [Diffie-Hellman](/diffie-hellman/) value that only the key holder can recompute. In a group of prime order it is [IND-CPA](/ind-cpa-security/) secure under the [decisional Diffie-Hellman assumption](/decisional-diffie-hellman/), with a tight reduction. It is malleable and multiplicatively homomorphic, so it is not [IND-CCA](/ind-cca-security/) secure; [Cramer-Shoup](/cramer-shoup-cryptosystem/) and [ECIES](/ecies/) are the chosen-ciphertext secure relatives.

**Notation.** $p$ is a prime and $b$ its number of binary digits. On this page $q$ is the order of the group $G = \langle g \rangle \subseteq \mathbb{Z}_p^*$, a prime in the main setting $p = 2q + 1$ (a [safe prime](/safe-prime/)). $x$ is the private key, $h = g^x$ the public key, $r$ the encryption randomness, $m \in G$ the message and $(c_1, c_2)$ the ciphertext. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary that runs in time $t$, and $\mathrm{Adv}$ an advantage. All results here are in the standard model.

## In plain words

The receiver picks a secret number and publishes a public value made from it. To send a message, the sender picks a fresh secret number of its own, publishes a value made from it, and uses both public values to compute a shared mask. Only the receiver can compute the same mask, from the sender's public value and the receiver's own secret. The sender multiplies the message by the mask and sends the product with its public value.

Because the sender picks a new secret number each time, the same message gives a different ciphertext each time. An eavesdropper sees two values that look random, provided the mask cannot be told apart from a random group element. The scheme has a weakness: anyone can multiply the second value by a known number, and the message is then multiplied by that number. So it protects secrecy but not integrity.

## The problem

ElGamal solves [public-key encryption](/public-key-encryption/) for messages that are elements of the group $G$. Its security rests on the [computational](/computational-diffie-hellman/) and the [decisional Diffie-Hellman](/decisional-diffie-hellman/) problems in $G$. Recovering $m$ from a ciphertext and the public key is exactly as hard as CDH in $G$ (Handbook of Applied Cryptography Note 8.23 (i)), and hiding every bit of $m$ is exactly DDH.

## The algorithm

The group $(p, q, g)$ is public and may be shared by all users.

```pseudo id=main
ELGAMAL-KEYGEN(p, q, g)                  ▷ g has order q in Z_p^*
L1  x ← a uniform integer in {0, …, q − 1}
L2  h ← g^x mod p
L3  return the public key h and the private key x

ELGAMAL-ENCRYPT(h, m)                    ▷ m ∈ G, that is m^q ≡ 1 (mod p)
L4  r ← a uniform integer in {0, …, q − 1}
L5  c1 ← g^r mod p
L6  c2 ← m · h^r mod p
L7  return (c1, c2)

ELGAMAL-DECRYPT(x, (c1, c2))
L8  if c1 ∉ G or c2 ∉ G then return ⊥  ▷ test a^q ≡ 1 (mod p) and 0 < a < p
L9  return c2 · c1^(q − x) mod p         ▷ c1^(q − x) = c1^(−x)
```

Line L5 and the value $h^r$ of line L6 form a Diffie-Hellman exchange between the key $h = g^x$ and the one-time key $c_1 = g^r$: both equal $g^{xr}$ after one more exponentiation. Line L9 removes that value with the exponent $q - x$, which is $-x$ modulo the order of $c_1$ and avoids a separate inversion.

**Encoding messages.** The message must lie in $G$. For a safe prime $p = 2q + 1$ with $p \equiv 3 \pmod 4$, $-1$ is not a square modulo $p$, so exactly one of $m$ and $p - m$ is a square for each $1 \le m \le q$. The map $m \mapsto m$ if $m$ is a square, $p - m$ otherwise, is a bijection from $\{1, \ldots, q\}$ onto $G$, and its inverse is $a \mapsto \min(a, p - a)$. The square test is one [Legendre symbol](/legendre-symbol/).

## Example

Take the toy group $p = 23$, $q = 11$, $g = 4$. The subgroup is $G = \{1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18\}$, the squares modulo 23.

| step | computation | value |
|---|---|---|
| L1 | private key | $x = 7$ |
| L2 | $h = 4^7 \bmod 23$ | 8 |
| | message $m = 6$, a square, so it encodes to itself | 6 |
| L4 | randomness | $r = 5$ |
| L5 | $c_1 = 4^5 \bmod 23$ | 12 |
| L6 | $h^r = 8^5 \bmod 23$, then $c_2 = 6 \cdot 16 \bmod 23$ | 16, then 4 |
| L9 | $c_1^{q-x} = 12^4 \bmod 23$, then $4 \cdot 13 \bmod 23$ | 13, then 6 |

The message 5 is not a square modulo 23, so it encodes to $23 - 5 = 18$, and 18 decodes to $\min(18, 5) = 5$.

Two properties show on the same numbers. A second ciphertext of $m' = 3$ with $r = 9$ is $(13, 4)$. The componentwise product $(12 \cdot 13, 4 \cdot 4) \bmod 23 = (18, 16)$ decrypts to $16 \cdot 18^4 \bmod 23 = 18 = 6 \cdot 3 \bmod 23$. And the changed ciphertext $(12, 2 \cdot 4) = (12, 8)$, made without the key, decrypts to $8 \cdot 13 \bmod 23 = 12 = 2 \cdot 6$.

The textbook form uses all of $\mathbb{Z}_p^*$. Handbook of Applied Cryptography Example 8.19 takes $p = 2357$, the generator $g = 2$, $x = 1751$, so $h = 1185$. The message $m = 2035$ with $r = 1520$ gives $(c_1, c_2) = (1430, 697)$, and $1430^{605} \bmod 2357 = 872$ gives $872 \cdot 697 \bmod 2357 = 2035$. The test file checks these numbers. This form leaks one bit of the message, as the pitfalls below show.

## Correctness

Decryption computes $c_2 c_1^{-x} = m g^{xr} g^{-rx} = m$, for every $m \in G$ and every $r$, and the test of line L8 accepts every honest ciphertext because $G$ is closed under multiplication. The full proof, with the membership test $a^q \equiv 1$, is below.

## Complexity

Let $b$ be the number of binary digits of $p$. With schoolbook arithmetic a multiplication modulo $p$ costs $\Theta(b^2)$, and an exponentiation with an exponent below $q < p$ costs $\Theta(b)$ multiplications by [modular exponentiation](/modular-exponentiation/), so $\Theta(b^3)$.

- **Key generation**: one exponentiation, $\Theta(b^3)$.
- **Encryption**: two exponentiations ($g^r$ and $h^r$) and one multiplication, $\Theta(b^3)$. Both bases are fixed, so precomputed tables make them faster in practice.
- **Decryption**: one exponentiation and one multiplication, plus two membership tests of one exponentiation each, $\Theta(b^3)$.
- **Space and expansion**: the ciphertext has two group elements for one message element, so it is twice as long as the message (HAC Note 8.21).

In an elliptic curve group the same scheme costs a few scalar multiplications on a curve of about $2\lambda$ binary digits; see [elliptic-curve cryptography](/elliptic-curve-cryptography/).

## Properties

### IND-CPA security under DDH

**Theorem.** Let $G = \langle g \rangle$ have prime order $q$. For every IND-CPA adversary $\mathcal{A}$ against ElGamal in $G$ there is a DDH distinguisher $\mathcal{B}$ with

$$\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_{\mathrm{EG}}(\mathcal{A}) = 2\,\mathrm{Adv}^{\mathrm{ddh}}_{G}(\mathcal{B}),$$

where $\mathrm{Adv}^{\mathrm{ind\text{-}cpa}} = |\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]|$ and $\mathrm{Adv}^{\mathrm{ddh}}$ is the difference of the output probabilities of $\mathcal{B}$ on $(g^x, g^y, g^{xy})$ and on $(g^x, g^y, g^z)$, with $x, y, z$ uniform in $\mathbb{Z}_q$. $\mathcal{B}$ runs in the time of $\mathcal{A}$ plus one group multiplication and the choice of one bit. The reduction is tight: the factor 2 comes only from the two conventions for advantage.

*Proof.* $\mathcal{B}$ gets $(X, Y, Z) = (g^x, g^y, Z)$. It gives $\mathcal{A}$ the public key $h = X$. When $\mathcal{A}$ outputs two messages $m_0, m_1 \in G$, $\mathcal{B}$ draws a uniform bit $\beta$ and gives $\mathcal{A}$ the challenge $(Y, Z \cdot m_\beta)$. When $\mathcal{A}$ outputs $\beta'$, $\mathcal{B}$ outputs 1 if $\beta' = \beta$ and 0 otherwise.

Case $Z = g^{xy}$. The key $h = g^x$ has the distribution of line L2, and $(Y, Z m_\beta) = (g^y, m_\beta h^y)$ is an encryption of $m_\beta$ with randomness $y$, uniform as in line L4. So $\mathcal{A}$ runs in the real IND-CPA game, and

$$\Pr[\mathcal{B} = 1] = \Pr[\beta' = \beta] = \tfrac{1}{2} + \tfrac{1}{2}\bigl(\Pr[\beta' = 1 \mid \beta = 1] - \Pr[\beta' = 1 \mid \beta = 0]\bigr).$$

Case $Z = g^z$ with $z$ uniform and independent of $x$, $y$ and $\beta$. Multiplication by $m_\beta$ is a bijection of $G$, so $Z m_\beta$ is uniform in $G$ and independent of $\beta$, given everything else that $\mathcal{A}$ sees. So the view of $\mathcal{A}$ does not depend on $\beta$, and $\Pr[\beta' = \beta] = \tfrac{1}{2}$ exactly.

The difference of the two cases is $\tfrac{1}{2}(\Pr[\beta' = 1 \mid \beta = 1] - \Pr[\beta' = 1 \mid \beta = 0])$. Replace $\mathcal{A}$ by the adversary that flips its output if this bracket is negative; the advantage stays the same. Then $\mathrm{Adv}^{\mathrm{ddh}}(\mathcal{B}) = \tfrac{1}{2}\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}(\mathcal{A})$. $\square$

The converse also holds: an IND-CPA attack exists if DDH is easy in $G$. Tsiounis and Yung (1998) proved both directions. So the security of ElGamal is exactly the DDH assumption, and the group must be one where DDH is believed hard: a prime order subgroup of $\mathbb{Z}_p^*$ or of an elliptic curve without an efficient pairing.

### Other properties

- **Probabilistic.** Each message has $q$ ciphertexts, one for each $r$. The [probabilistic encryption](/probabilistic-encryption/) page explains why this is necessary.
- **Multiplicatively homomorphic.** $(c_1, c_2) \cdot (d_1, d_2) = (g^{r + s}, m m' h^{r+s})$ encrypts $m m'$. Multiplication by an encryption of 1 rerandomizes a ciphertext. See [homomorphic encryption](/homomorphic-encryption/).
- **Malleable.** $(c_1, t c_2)$ encrypts $t m$ for any known $t \in G$. So ElGamal is not [non-malleable](/non-malleability/) and not IND-CCA secure: a decryption oracle on $(c_1, t c_2)$ returns $tm$, and the attacker divides by $t$. This is a [chosen-ciphertext attack](/chosen-ciphertext-attack/) with one query.
- **Exponential ElGamal.** Encrypt $g^v$ instead of $v$. Then products of ciphertexts encrypt $g^{v_1 + v_2}$, so the scheme adds plaintexts. Decryption ends with a discrete logarithm of $g^v$, which is fast only when $v$ is small, for example a vote count. Cramer, Gennaro and Schoenmakers (1997) built an election scheme on it.
- **One-way under CDH.** Recovering the whole message is CDH, which holds in groups where DDH fails. So the full group $\mathbb{Z}_p^*$ gives a scheme that is one-way but not IND-CPA.

## Variants and improvements

- **Elliptic curve ElGamal.** The same scheme in the group of points of an elliptic curve. Messages must be encoded as points, which is awkward, so curves are almost always used in the hybrid form below.
- **Hashed ElGamal and DHIES.** Encrypt $m \oplus H(g^{xr})$, or derive a symmetric key from $g^{xr}$ and use it in a symmetric cipher. This removes the encoding problem and allows long messages. With a MAC it is [DHIES and ECIES](/ecies/), which are IND-CCA secure under an oracle Diffie-Hellman assumption.
- **Cramer-Shoup.** Two generators and a hash proof make the scheme IND-CCA secure in the standard model under DDH, at about twice the cost; see [Cramer-Shoup](/cramer-shoup-cryptosystem/).
- **Fujisaki-Okamoto.** ElGamal is one-way under CDH, so the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) turns it into an IND-CCA secure KEM in the random oracle model.
- **Threshold and re-encryption.** The private key can be split with Shamir shares, and ciphertexts can be rerandomized, which is the base of [mix networks](/mix-network/) and [threshold decryption](/threshold-cryptography/).

## When to use it

Use plain ElGamal when you need its algebra: rerandomization in a mix network, exponential ElGamal for an encrypted tally, or threshold decryption. Combine it with zero-knowledge proofs of correct behaviour in those protocols. For ordinary encryption of data, do not use it directly: use [hybrid encryption](/hybrid-encryption/) with an IND-CCA secure KEM, for example ECIES, HPKE (RFC 9180) or the post-quantum [ML-KEM](/crystals-kyber/). Compared with [RSA](/rsa-cryptosystem/), ElGamal is randomized without padding, but its ciphertext is twice the group size, and it needs a group where DDH holds.

## Pitfalls

- **The full group $\mathbb{Z}_p^*$.** If $g$ generates all of $\mathbb{Z}_p^*$ (as in HAC Algorithm 8.17), DDH is false: the [Legendre symbol](/legendre-symbol/) of $g^{xy}$ follows from those of $g^x$ and $g^y$. Then $(c_2 / p) = (m / p) \cdot (h^r / p)$ shows whether $m$ is a square, which is one bit of the message. The test file wins the IND-CPA game with probability 1 against HAC Example 8.19. Use a prime order subgroup (line L1 with $q$ prime) and encode messages into it.
- **Messages outside the subgroup.** Even with a subgroup, encrypting an integer that is not in $G$ leaks its quadratic character. CVE-2018-6829 (2018) records that Libgcrypt through version 1.8.2 encrypted plaintexts without this encoding when used directly. GnuPG was not affected because it uses ElGamal only to encrypt random session keys. The code refuses such messages before line L4.
- **No membership test.** Without line L8 an attacker can send $c_1$ of small order and learn $x$ modulo small factors of $p - 1$ from the answers, as in the [small subgroup attack](/small-subgroup-attack/).
- **Reused randomness.** Two messages with the same $r$ give $c_2 / c_2' = m / m'$, so one known message reveals the other (HAC Note 8.23 (ii)). Draw $r$ from a cryptographic generator for each message.
- **Relying on secrecy against active attackers.** The malleability above means that an attacker who can see whether a changed ciphertext decrypts to something meaningful can learn the message. Never decrypt and act on ciphertexts from an untrusted source with plain ElGamal.
- **Exponential ElGamal with large values.** Decryption needs a discrete logarithm. Keep the plaintext range small, for example below $2^{40}$, and use baby-step giant-step.

## Implementations

The Python code is for study only. It is not constant time, it is not protected against side channels, and it must not protect real data. Use a FIPS 140 validated module, libsodium, or the hybrid public-key encryption of your platform's standard library. The tests check HAC Example 8.19, the safe prime toy group (the smallest safe prime above $2^{63}$), the round trip, the homomorphism, the malleability attack, the Legendre attack in the full group, and the tight reduction from DDH on that group.

## History

Diffie and Hellman (1976) gave key exchange but no encryption. ElGamal (1985) turned the exchange into encryption and also gave the ElGamal signature scheme in the same paper, in IEEE Transactions on Information Theory. Goldwasser and Micali had defined semantic security in 1984; Tsiounis and Yung (1998) proved that ElGamal is semantically secure exactly when DDH holds, the same year that Cramer and Shoup gave the chosen-ciphertext secure extension. OpenPGP (RFC 4880) uses ElGamal to encrypt session keys. Exponential ElGamal underlies many electronic voting systems since Cramer, Gennaro and Schoenmakers (1997).

## References
