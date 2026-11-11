---
tag: 4VE7MR
kind: algorithm
slug: okamoto-uchiyama-cryptosystem
name: Okamoto-Uchiyama cryptosystem
aliases:
- OU cryptosystem
area: cryptography/public-key
level: research
summary: "Public-key encryption c = g^m h^r mod N with N = p^2 q, decrypted in the subgroup of order p. One-way iff factoring is hard, additively homomorphic, and broken by a chosen ciphertext attack."
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of N}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1998
  people: [Tatsuaki Okamoto, Shigenori Uchiyama]
  note: Presented at Eurocrypt 1998 as a cryptosystem as secure as factoring. The EPOC schemes submitted to IEEE P1363a add the Fujisaki-Okamoto conversion to it.
prereqs: [public-key-encryption, modular-exponentiation, integer-factorization]
see_also: [paillier-cryptosystem, decisional-composite-residuosity, naccache-stern-cryptosystem, homomorphic-encryption, chosen-ciphertext-attack, fujisaki-okamoto-transform, rabin-cryptosystem, ind-cca-security]
sources:
  - paper: "Tatsuaki Okamoto and Shigenori Uchiyama, A new public-key cryptosystem as secure as factoring, Eurocrypt 1998, LNCS 1403, pages 308 to 318"
    locator: the p-Sylow subgroup of Z_(p^2)^* and the logarithm L, the scheme, the proof that one-wayness is equivalent to factoring N = p^2 q, and semantic security under the p-subgroup assumption
  - paper: "Marc Joye, Jean-Jacques Quisquater and Moti Yung, On the power of misbehaving adversaries and security analysis of the original EPOC, CT-RSA 2001, LNCS 2020"
    locator: chosen ciphertext attacks that recover the factorization of N against the original EPOC, which is built on Okamoto-Uchiyama
  - paper: "Pascal Paillier, Public-key cryptosystems based on composite degree residuosity classes, Eurocrypt 1999, LNCS 1592, pages 223 to 238"
    locator: the comparison with the Okamoto-Uchiyama scheme in the introduction
  - paper: "Eiichiro Fujisaki and Tatsuaki Okamoto, Secure integration of asymmetric and symmetric encryption schemes, Crypto 1999, LNCS 1666, pages 537 to 554"
    locator: the conversion used by EPOC to reach chosen ciphertext security in the random oracle model
  - paper: "Dan Boneh, Glenn Durfee and Nick Howgrave-Graham, Factoring N = p^r q for large r, Crypto 1999, LNCS 1666, pages 326 to 337"
    locator: the lattice method that factors p^r q faster when r is large
---

The Okamoto-Uchiyama cryptosystem is a [public-key encryption](/public-key-encryption/) scheme that Tatsuaki Okamoto and Shigenori Uchiyama published in 1998. The modulus is $N = p^2 q$, a message $m < 2^{k-1}$ is sent as $c = g^m h^r \bmod N$ with $h = g^N$, and the receiver reads $m$ from a discrete logarithm in the subgroup of order $p$ of $\mathbb{Z}_{p^2}^*$, where logarithms are easy. Recovering $m$ is as hard as factoring $N$, the scheme is additively [homomorphic](/homomorphic-encryption/), and it is IND-CPA under the $p$-subgroup assumption. A single decryption query on a crafted ciphertext factors $N$, so the plain scheme must never decrypt for untrusted parties.

**Notation.** $p$ and $q$ are distinct primes of $k$ binary digits each; on this page $q$ is a prime. $N = p^2 q$ has about $b = 3k$ binary digits. $\Gamma = \{x \in \mathbb{Z}_{p^2}^* : x \equiv 1 \pmod p\}$ and $L(x) = (x - 1)/p$ for $x \in \Gamma$. $\mathcal{A}$ is an adversary and $\mathrm{Adv}$ its advantage. The security results are in the standard model.

## In plain words

The receiver multiplies three secret primes, one of them twice, and publishes the product. A message is hidden in the exponent of a public base, and a random factor is added in the exponent too. Inside the hidden part that belongs to the square of the repeated prime, there is a small group where taking logarithms is just a subtraction and a division. The receiver, who knows the primes, moves the ciphertext into that small group, where the random factor disappears, and reads the message off.

Multiplying two ciphertexts adds their messages, as in Paillier. The receiver only ever learns the message modulo the secret prime. If someone sends a number larger than that prime and gets the decryption back, the difference between the two numbers is a multiple of the prime, and the secret falls out with one greatest common divisor.

## The problem

Okamoto-Uchiyama solves [public-key encryption](/public-key-encryption/) for messages of fewer than $k - 1$ binary digits. Its one-wayness is equivalent to [factoring](/integer-factorization/) $N = p^2 q$, which was the selling point in 1998: [RSA](/rsa-cryptosystem/) is not known to be equivalent to factoring, and [Rabin](/rabin-cryptosystem/) encryption is, but Rabin is deterministic. Its semantic security rests on the $p$-subgroup assumption: an element $g^m h^r$ with $m < 2^{k-1}$ is hard to tell from an element $h^r$.

## The algorithm

```pseudo id=main
OU-KEYGEN(k)
L1  p, q ← distinct random primes of k binary digits
L2  N ← p²·q
L3  g ← a uniform element of {2, …, N − 1}
L4  if gcd(g, N) ≠ 1 or g^(p − 1) mod p² = 1 then go to L3   ▷ g_p = g^(p−1) mod p² must have order p
L5  h ← g^N mod N
L6  return the public key (N, g, h, k) and the private key (p, q, g_p, L(g_p)^(−1) mod p)

OU-ENCRYPT((N, g, h, k), m)              ▷ 0 ≤ m < 2^(k−1)
L7  r ← a uniform element of {1, …, N − 1}
L8  return c ← g^m · h^r mod N

OU-DECRYPT((p, q, g_p, ℓ), c)            ▷ ℓ = L(g_p)^(−1) mod p
L9  c_p ← c^(p − 1) mod p²
L10 return L(c_p) · ℓ mod p
```

The group $\mathbb{Z}_{p^2}^*$ is cyclic of order $p(p-1)$, and $\Gamma$ is its unique subgroup of order $p$ (its $p$-Sylow subgroup). Raising to $p - 1$ in line L9 maps every element into $\Gamma$, and the factor $h^r = g^{Nr}$ goes to 1 because $p(p-1)$ divides $N(p-1)$. On $\Gamma$, $L$ is a logarithm: $L(x y \bmod p^2) \equiv L(x) + L(y) \pmod p$. So line L10 divides two logarithms and gets $m \bmod p$, which is $m$ because $m < 2^{k-1} < p$.

## Example

Take the toy primes $p = 11$ and $q = 13$, so $k = 4$, $N = 121 \cdot 13 = 1573$, and messages are below $2^3 = 8$. With $g = 2$:

| step | computation | value |
|---|---|---|
| L4 | $g_p = 2^{10} \bmod 121$ | $56 = 1 + 5 \cdot 11$, so $L(g_p) = 5$ |
| L5 | $h = 2^{1573} \bmod 1573$ | 1328 |
| L6 | $\ell = 5^{-1} \bmod 11$ | 9 |
| L7, L8 | $m = 7$, $r = 5$: $2^7 = 128$, $h^5 \bmod 1573 = 604$, $c = 128 \cdot 604 \bmod 1573$ | 235 |
| L9 | $c_p = 235^{10} \bmod 121$ | $23 = 1 + 2 \cdot 11$, so $L(c_p) = 2$ |
| L10 | $2 \cdot 9 \bmod 11$ | 7 |

**The attack on the same key.** The attacker computes $C = g^{100} h^3 \bmod 1573 = 1337$ for the message $100 > p$ and gets the decryption $100 \bmod 11 = 1$. Then $\gcd(100 - 1, 1573) = 11 = p$.

## Correctness

Write $c = g^m h^r = g^{m + Nr}$. In $\mathbb{Z}_{p^2}^*$, $c^{p-1} = g_p^{m} \cdot g^{N r (p-1)}$, and $N(p-1) = p q \cdot p(p-1)$ is a multiple of the group order $p(p-1)$, so the second factor is 1. Every $x \in \Gamma$ is $1 + ap$ with $0 \le a < p$, and $(1 + ap)^m \equiv 1 + map \pmod{p^2}$ by the binomial theorem, so $L(g_p^m \bmod p^2) \equiv m L(g_p) \pmod p$. The condition of line L4 says $g_p \ne 1$, so $L(g_p) \not\equiv 0$ and $\ell$ exists. Line L10 returns $m L(g_p) \ell \bmod p = m \bmod p = m$. The full proof is in the proof file.

## Complexity

Let $b \approx 3k$ be the number of binary digits of $N$. A multiplication modulo $N$ costs $\Theta(b^2)$ with schoolbook arithmetic.

- **Encryption**: two exponentiations modulo $N$, one with an exponent of fewer than $k$ binary digits and one with about $b$, so $\Theta(b^3)$. As in Paillier, $h^r$ can be computed ahead of time.
- **Decryption**: one exponentiation modulo $p^2$ (numbers of $2k$ binary digits) with an exponent of $k$ binary digits, $\Theta(k^3)$. This is $\Theta(b^3)$, but with schoolbook arithmetic it costs about $k (2k)^2 = 4k^3$ bit operations against $3k (3k)^2 = 27k^3$ for an exponentiation modulo $N$ with an exponent of $b$ digits, so about 7 times less.
- **Size**: a ciphertext has $b \approx 3k$ binary digits for a message of $k - 1$ binary digits, an expansion factor of about 3.

## Properties

- **One-way if and only if factoring is hard.** If $N$ can be factored, decryption is easy. Conversely, Okamoto and Uchiyama show that an algorithm that inverts the encryption on a noticeable fraction of ciphertexts factors $N$. The idea of the proof is the attack below: feed the inverter $g^M \bmod N$ for a random $M$ much larger than $p$; this value is distributed almost like an honest ciphertext, so the inverter cannot tell how large $M$ was, and the answer is a different representative $m \equiv M \pmod p$, and $\gcd(M - m, N)$ gives $p$.
- **IND-CPA under the $p$-subgroup assumption.** The assumption says that $g^m h^r$ for a fixed $m$ cannot be told apart from $h^r$; the IND-CPA proof is a hybrid between the two challenge messages. It is a decisional assumption, like [DCR](/decisional-composite-residuosity/) for Paillier, and it is not known to follow from factoring.
- **Additively homomorphic.** $c_1 c_2 = g^{m_1 + m_2} h^{r_1 + r_2}$ decrypts to $m_1 + m_2 \bmod p$. Since $p$ is secret, users must keep sums below $p$; a sum that wraps returns a value that tells nothing useful to the sender.
- **Not IND-CCA, and worse.** The chosen ciphertext attack below gives the attacker the private key, not only one message. The proof of one-wayness and the attack are the same argument, which is a known tension for schemes that are as hard as factoring (the [Rabin cryptosystem](/rabin-cryptosystem/) has the same problem).

### The chosen ciphertext attack

1. Pick an integer $M$ with $M > p$, for example uniform in $[N/2, N)$, and an $r$.
2. Send $C = g^M h^r \bmod N$ to the decryption oracle and get $m' = M \bmod p$.
3. Output $p = \gcd(M - m', N)$, then $q = N / p^2$.

Step 2 returns $M \bmod p$ by the correctness argument, which works for every exponent. So $p \mid M - m'$. The gcd is $p$ unless $p^2$ or $q$ also divides $M - m'$; for a uniform $M$ this has probability about $1/p + 1/q$. A decryption device that checks nothing about the plaintext cannot stop this, since every $C$ is a valid ciphertext of some message. Joye, Quisquater and Yung (2001) showed related attacks that factor $N$ against the original EPOC, the Okamoto-Uchiyama scheme with a chosen ciphertext conversion, when the device leaks which check failed.

## Variants and improvements

- **EPOC.** Okamoto, Uchiyama and Fujisaki submitted EPOC-1, EPOC-2 and EPOC-3 to IEEE P1363a. They apply the [Fujisaki-Okamoto](/fujisaki-okamoto-transform/) conversions (Crypto 1999) to reach IND-CCA2 in the random oracle model. The conversion must reject all invalid ciphertexts in the same way; a different error for each check brings the attack back (Joye, Quisquater and Yung 2001).
- **Paillier.** Paillier (1999) uses $N^2$ for an RSA modulus $N$ instead of $p^2 q$, and gets a message space of the full size $N$ with decryption by the same function $L$. See [Paillier](/paillier-cryptosystem/).
- **Naccache-Stern.** Another additively homomorphic scheme, from the same year, with a message space that is a product of small primes; see [Naccache-Stern](/naccache-stern-cryptosystem/).

## When to use it

Do not use plain Okamoto-Uchiyama to encrypt data. For confidentiality use an IND-CCA2 scheme or [hybrid encryption](/hybrid-encryption/). For additive homomorphism use [Paillier](/paillier-cryptosystem/) or exponential ElGamal, which have larger standard support (ISO/IEC 18033-6). The scheme remains a good example of three ideas: a logarithm that is easy in the $p$-Sylow subgroup of $\mathbb{Z}_{p^2}^*$, a one-wayness proof that is a reduction from factoring, and why such a proof leads straight to a chosen ciphertext attack.

## Pitfalls

- **Any decryption oracle.** A server that returns decryptions of ciphertexts chosen by others gives away $p$ after one query, as in the attack above.
- **Messages too long.** A message of $k$ or more binary digits does not decrypt correctly, because only $m \bmod p$ comes back. The encryption code rejects $m \ge 2^{k-1}$.
- **Bad base.** If $g^{p-1} \equiv 1 \pmod{p^2}$, every ciphertext decrypts to 0. Line L4 rejects such $g$.
- **Moduli of the form $p^2 q$.** Factoring methods for $p^r q$ exist that are faster for large $r$ (Boneh, Durfee and Howgrave-Graham 1999), and the elliptic curve method finds $p$ in time that depends on the size of $p$. For $r = 2$ these do not beat the number field sieve at standard sizes, but the modulus must be sized for $p$ of at least a third of $N$, and a toy key such as the 576-binary-digit key of the tests is not secure.

## Implementations

The Python code is for study only. It is not constant time, it is not protected against side channels, and it must not protect real data. Use an IND-CCA2 scheme from a vetted library, for example RSA-OAEP from a FIPS 140 validated module or HPKE (RFC 9180). There are no official test vectors for Okamoto-Uchiyama. The tests check the example above, all messages of the toy key, round trips and the additive homomorphism on a key with primes of 192 binary digits from a fixed seed, and the chosen ciphertext attack against a local simulated decryption oracle, which recovers $p$ and $q$ and then decrypts a fresh ciphertext with the stolen key.

## History

Okamoto and Uchiyama (Eurocrypt 1998) wanted a probabilistic scheme that was provably as hard to invert as factoring and also fast to decrypt, and found the easy logarithm in the $p$-Sylow subgroup of $\mathbb{Z}_{p^2}^*$. The same year Naccache and Stern (ACM CCS 1998) published a scheme on higher residues, and a year later Paillier (Eurocrypt 1999) moved the idea to $\mathbb{Z}_{N^2}^*$ with an RSA modulus $N$. The authors, with Fujisaki, built EPOC on the scheme, and Joye, Quisquater and Yung (CT-RSA 2001) showed how careless rejection of invalid ciphertexts in the original EPOC leaked the factorization.

## References
