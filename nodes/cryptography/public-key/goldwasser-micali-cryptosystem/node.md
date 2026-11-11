---
tag: 5FBQTT
kind: algorithm
slug: goldwasser-micali-cryptosystem
name: Goldwasser-Micali cryptosystem
aliases:
- GM cryptosystem
area: cryptography/public-key
level: advanced
summary: The first provably secure probabilistic public-key encryption. Each bit is sent as a random square or a random pseudosquare modulo N = pq. IND-CPA under quadratic residuosity.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of N, l: the number of message digits}
  time: {worst: Θ(l b^3), average: Θ(l b^3), best: Θ(l b^3)}
  space: {extra: Θ(l b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1982
  people: [Shafi Goldwasser, Silvio Micali]
  note: Presented at STOC 1982 with the first definitions of semantic security; journal version in JCSS 1984. Part of the work cited for the 2012 Turing Award.
prereqs: [quadratic-residuosity-problem, probabilistic-encryption]
see_also: [blum-goldwasser-cryptosystem, paillier-cryptosystem, homomorphic-encryption, jacobi-symbol, legendre-symbol, rsa-cryptosystem, elgamal-encryption, private-information-retrieval]
sources:
  - paper: doi:10.1016/0022-0000(84)90070-9
    title: Shafi Goldwasser and Silvio Micali, Probabilistic encryption, Journal of Computer and System Sciences 28(2), pages 270 to 299, 1984
    locator: the quadratic residuosity scheme, the definitions of semantic security and polynomial security, and the security proof
  - paper: "Shafi Goldwasser and Silvio Micali, Probabilistic encryption and how to play mental poker keeping secret all partial information, STOC 1982, pages 365 to 377"
    locator: the conference version
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Section 8.7.1, Algorithms 8.50 and 8.51, Notes 8.52 and 8.53, Remark 8.54
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the section on the Goldwasser-Micali encryption scheme and the quadratic residuosity assumption
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 5, the bit encryption schemes built from trapdoor permutations and hard-core predicates
  - paper: "Eyal Kushilevitz and Rafail Ostrovsky, Replication is not needed: single database, computationally-private information retrieval, FOCS 1997, pages 364 to 373"
    locator: private information retrieval from the quadratic residuosity assumption
  - paper: "Marc Joye and Benoit Libert, Efficient cryptosystems from 2^k-th power residue symbols, Eurocrypt 2013, LNCS 7881, pages 76 to 92"
    locator: the generalization that sends k message digits in one element of Z_N
  - paper: "Clifford Cocks, An identity based encryption scheme based on quadratic residues, Cryptography and Coding 2001, LNCS 2260, pages 360 to 363"
    locator: identity-based encryption of one bit at a time from quadratic residuosity
  - paper: "Josh Benaloh, Dense probabilistic encryption, Workshop on Selected Areas of Cryptography, 1994"
    locator: the generalization from squares to r-th residues
---

The Goldwasser-Micali cryptosystem (GM) is the [public-key encryption](/public-key-encryption/) scheme that Shafi Goldwasser and Silvio Micali presented in 1982, together with the first definition of what it means for encryption to hide all partial information. The public key is a product $N = pq$ of two primes and a pseudosquare $y$, a number with [Jacobi symbol](/jacobi-symbol/) $+1$ that is not a square modulo $N$; each bit of the message is sent as a random square (bit 0) or a random pseudosquare (bit 1). It is [IND-CPA](/ind-cpa-security/) secure under the [quadratic residuosity assumption](/quadratic-residuosity-problem/), with a tight reduction. Each message bit becomes a whole element of $\mathbb{Z}_N$, so the scheme is used today mainly where its XOR homomorphism helps.

**Notation.** $p$ and $q$ are distinct odd primes (on this page $q$ is the second prime factor, not a group order), $N = pq$, and $b$ is the number of binary digits of $N$. $\mathbb{Z}_N^*$ is the set of units modulo $N$ and $J_N$ the subset with Jacobi symbol $+1$. $QR_N \subset J_N$ is the set of squares, and $\widetilde{QR}_N = J_N \setminus QR_N$ the set of pseudosquares. A message is a list of $\ell$ bits $m_1, \ldots, m_\ell$. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary that runs in time $t$, and $\mathrm{Adv}$ an advantage. All results here are in the standard model.

## In plain words

The receiver multiplies two secret primes and publishes the product, together with one special number. Modulo the product, some numbers are perfect squares and some are not, and a public test sorts out only some of the non-squares. The special number passes that public test but is not a square.

To send a 0, the sender squares a fresh random number. To send a 1, it squares a fresh random number and multiplies by the special number. Every value sent passes the public test, and nobody is known to be able to tell squares from the special non-squares without the primes. The receiver knows one prime, and modulo a prime a single power shows at once whether a number is a square. The cost is size: each bit of the message becomes a number as long as the public product.

## The problem

GM solves [public-key encryption](/public-key-encryption/) of bit strings. Its security rests on the [quadratic residuosity problem](/quadratic-residuosity-problem/): given $N$ and $z \in J_N$, decide whether $z \in QR_N$. With the factors this is easy, since $z$ is a square modulo $N$ exactly when it is a square modulo $p$ and modulo $q$ ([Chinese remainder theorem](/chinese-remainder-theorem/)), and each test is one [Legendre symbol](/legendre-symbol/). Without the factors no algorithm faster than factoring $N$ is known. The Jacobi symbol is public and easy to compute, so it splits $\mathbb{Z}_N^*$ only into $J_N$ and the rest; inside $J_N$ the two halves $QR_N$ and $\widetilde{QR}_N$ look alike.

## The algorithm

```pseudo id=main
GM-KEYGEN(p, q)                          ▷ distinct odd primes of b/2 binary digits
L1  N ← p · q
L2  y ← a uniform unit modulo N; repeat until y^((p−1)/2) ≢ 1 (mod p) and y^((q−1)/2) ≢ 1 (mod q)
L3  return the public key (N, y) and the private key (p, q)

GM-ENCRYPT((N, y), m1 … mℓ)              ▷ each mi ∈ {0, 1}
L4  for i ← 1 to ℓ
L5      r ← a uniform unit modulo N
L6      ci ← y^mi · r² mod N
L7  return c1 … cℓ

GM-DECRYPT((p, q), c1 … cℓ)
L8  for i ← 1 to ℓ
L9      mi ← 0 if ci^((p−1)/2) ≡ 1 (mod p), else 1
L10 return m1 … mℓ
```

Line L2 draws $y$ uniformly from $\widetilde{QR}_N$: a uniform unit is a non-square modulo $p$ and modulo $q$ with probability $1/4$, so the loop runs 4 times on average. The Handbook of Applied Cryptography (Remark 8.54) builds $y$ instead from a non-square $a$ modulo $p$ and a non-square $b$ modulo $q$ with the Chinese remainder theorem. Line L6 multiplies by $y$ only for a 1 bit. Line L9 is Euler's criterion: for a unit $a$ modulo $p$, $a^{(p-1)/2} \bmod p$ is $1$ if $a$ is a square and $p - 1$ if not. The factor $q$ is not needed for decryption.

## Example

Take $p = 7$, $q = 11$, $N = 77$. The squares modulo 7 are $\{1, 2, 4\}$ and modulo 11 are $\{1, 3, 4, 5, 9\}$. The value $y = 76$ is $6$ modulo 7 and $10$ modulo 11, a non-square for both, so it is a pseudosquare and $\left(\frac{76}{77}\right) = 1$. Encrypt the bits $1, 0, 1$.

| step | bit | $r$ | $c = y^{m} r^2 \bmod 77$ | $c \bmod 7$ | $c^3 \bmod 7$ (L9) | decrypted bit |
|---|---|---|---|---|---|---|
| L5 to L6, L9 | 1 | 2 | $76 \cdot 4 \bmod 77 = 73$ | 3 | 6 | 1 |
| L5 to L6, L9 | 0 | 3 | $9$ | 2 | 1 | 0 |
| L5 to L6, L9 | 1 | 5 | $76 \cdot 25 \bmod 77 = 52$ | 3 | 6 | 1 |

Here $(p-1)/2 = 3$, and $6 = p - 1$ means "not a square". All three ciphertexts have Jacobi symbol $+1$ modulo 77, so the public test does not tell them apart.

The same numbers show the homomorphism. The product $73 \cdot 9 \bmod 77 = 41$ gives $41 \bmod 7 = 6$ and $6^3 \bmod 7 = 6$, so it decrypts to $1 = 1 \oplus 0$. The product $73 \cdot 52 \bmod 77 = 23$ gives $2^3 \bmod 7 = 1$, so it decrypts to $0 = 1 \oplus 1$. Multiplying the ciphertext $9$ of a 0 by $y$ gives $9 \cdot 76 \bmod 77 = 68$, an encryption of 1 made without the key.

## Correctness

For a ciphertext $c = y^m r^2$ the Legendre symbol modulo $p$ is multiplicative, so $\left(\frac{c}{p}\right) = \left(\frac{y}{p}\right)^m \left(\frac{r}{p}\right)^2 = (-1)^m$, because line L2 makes $y$ a non-square modulo $p$ and $r$ is a unit. Euler's criterion turns this into the test of line L9, which therefore returns $m$. The full proof, with a proof of Euler's criterion and of $\left(\frac{y}{N}\right) = 1$, is below.

## Complexity

Let $b$ be the number of binary digits of $N$ and $\ell$ the number of message bits. With schoolbook arithmetic a multiplication modulo $N$ costs $\Theta(b^2)$.

- **Encryption**: per bit, a random unit (a gcd test, $O(b^2)$, which fails with negligible probability), one squaring and at most one more multiplication, so $\Theta(\ell b^2)$ in total.
- **Decryption**: per bit, one [modular exponentiation](/modular-exponentiation/) modulo $p$ with an exponent of about $b/2$ binary digits, $\Theta(b^3)$, so $\Theta(\ell b^3)$ in total. This is the cost in the front matter.
- **Key generation**: generating the primes dominates, as in [RSA](/rsa-cryptosystem/); the search for $y$ takes 4 expected iterations of two exponentiations each.
- **Expansion**: the ciphertext has $\ell b$ binary digits for $\ell$ message bits, a factor of $b = \log_2 N$ (HAC Note 8.53). For $b = 3072$, a 16-byte message becomes 48 kilobytes.

## Properties

### IND-CPA security under quadratic residuosity

The QR assumption here is that, for $N$ from the key generator and $z$ uniform in $QR_N$ or uniform in $\widetilde{QR}_N$, no efficient $\mathcal{B}$ has a non-negligible advantage $\mathrm{Adv}^{\mathrm{qr}}(\mathcal{B}) = |\Pr[\mathcal{B}(N, z) = 1 \mid z \in \widetilde{QR}_N] - \Pr[\mathcal{B}(N, z) = 1 \mid z \in QR_N]|$.

**Theorem.** For every IND-CPA adversary $\mathcal{A}$ against GM on $\ell$-bit messages there is a QR distinguisher $\mathcal{B}$ with

$$\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_{\mathrm{GM}}(\mathcal{A}) = 2\,\mathrm{Adv}^{\mathrm{qr}}(\mathcal{B}),$$

where $\mathrm{Adv}^{\mathrm{ind\text{-}cpa}} = |\Pr[\beta' = 1 \mid \beta = 1] - \Pr[\beta' = 1 \mid \beta = 0]|$. $\mathcal{B}$ runs in time $t + O(\ell b^2)$. The reduction is tight: the factor 2 comes only from the two conventions for advantage.

*Proof.* $\mathcal{B}$ gets $(N, z)$ and gives $\mathcal{A}$ the public key $(N, z)$. When $\mathcal{A}$ outputs $m^0, m^1$, $\mathcal{B}$ draws a uniform bit $\beta$, encrypts $m^\beta$ with lines L4 to L7 under $(N, z)$, and outputs 1 if $\mathcal{A}$ returns $\beta' = \beta$, else 0.

Case $z \in \widetilde{QR}_N$. Then $z$ has the distribution of line L2, and $\mathcal{A}$ runs in the real IND-CPA game. So $\Pr[\mathcal{B} = 1] = \tfrac12 + \tfrac12 (\Pr[\beta' = 1 \mid \beta = 1] - \Pr[\beta' = 1 \mid \beta = 0])$.

Case $z \in QR_N$. For a uniform unit $r$, $r^2$ is uniform in $QR_N$, because squaring maps $\mathbb{Z}_N^*$ onto $QR_N$ four to one. Multiplication by $z \in QR_N$ is a bijection of $QR_N$, so $z r^2$ is uniform in $QR_N$ too. So every component of the challenge is uniform in $QR_N$, independent of the other components and of $\beta$, and $\Pr[\beta' = \beta] = \tfrac12$ exactly.

The difference of the two cases is $\tfrac12 (\Pr[\beta' = 1 \mid \beta = 1] - \Pr[\beta' = 1 \mid \beta = 0])$. Replace $\mathcal{A}$ by the adversary that flips its output if this is negative, which keeps the advantage. $\square$

The test file runs this reduction with an adversary that cheats by using $p$, to stand in for a perfect one, and finds $\Pr[\mathcal{B} = 1]$ equal to 1 on pseudosquares and near $\tfrac12$ on squares. Goldwasser and Micali proved more: GM is semantically secure (HAC Note 8.52), and semantic security is equivalent to indistinguishability; see [semantic security](/semantic-security/).

### Other properties

- **Probabilistic.** Each bit has $|QR_N| = \varphi(N)/4$ ciphertexts. The [probabilistic encryption](/probabilistic-encryption/) page explains why this is necessary.
- **XOR homomorphic.** $c_1 c_2 = y^{m_1 + m_2} (r_1 r_2)^2$, and $y^2$ is a square, so the product encrypts $m_1 \oplus m_2$. Multiplying by a fresh $r^2$ rerandomizes a ciphertext. See [homomorphic encryption](/homomorphic-encryption/).
- **Malleable, so not IND-CCA.** $c \cdot y$ encrypts the flipped bit, so GM is not [non-malleable](/non-malleability/). Under a [chosen-ciphertext attack](/chosen-ciphertext-attack/) the attacker rerandomizes each challenge component $c_i$ to $c_i r^2$, which differs from $c_i$, and asks the decryption oracle; $\ell$ queries reveal the whole message.
- **Decryption needs only $p$.** The second factor is used only to make $y$.

## Variants and improvements

- **[Blum-Goldwasser](/blum-goldwasser-cryptosystem/)** (1984) uses the Blum-Blum-Shub generator as a pad and expands the message by one element of $\mathbb{Z}_N$ in total, instead of one element per bit.
- **Higher residues.** Benaloh's dense probabilistic encryption (1994) uses $r$-th residues instead of squares to send a value modulo $r$ in one element. Naccache-Stern, Okamoto-Uchiyama and [Paillier](/paillier-cryptosystem/) follow the same line with larger message spaces and an additive homomorphism.
- **Joye-Libert** (2013) uses $2^k$-th power residue symbols with $p \equiv 1 \pmod{2^k}$ and sends $k$ bits in one element of $\mathbb{Z}_N$, with decryption still fast.
- **Bit encryption from any trapdoor permutation.** Send $(f(r), m \oplus B(r))$ for a [trapdoor permutation](/trapdoor-one-way-function/) $f$ and a [hard-core predicate](/hard-core-predicate/) $B$. GM is the case where the hard-core bit is the quadratic character.
- **Cocks identity-based encryption** (2001) also encrypts one bit at a time with Jacobi symbols modulo a composite $N$.

## When to use it

Do not use GM to encrypt data: its expansion is a factor of $b$, and like any IND-CPA scheme it is not safe against active attackers. For data, use [hybrid encryption](/hybrid-encryption/) with an IND-CCA secure KEM. GM is useful as a teaching example of a security proof from a number-theoretic assumption, and in protocols that need to XOR encrypted bits or to rerandomize them, such as the private information retrieval scheme of Kushilevitz and Ostrovsky (1997). For an additive homomorphism over larger numbers, Paillier is usually the better choice.

## Pitfalls

- **A wrong $y$.** If $y$ is a non-square with Jacobi symbol $-1$, then every encryption of a 1 has Jacobi symbol $-1$ and every encryption of a 0 has $+1$, so anyone can read the message with the public Jacobi test. If $y$ is a square, every ciphertext is a square and decryption returns all zeros. Line L2 must check $y$ against both primes.
- **Reused or predictable randomness.** If two ciphertexts use the same $r$, then $c_1 / c_2 \bmod N$ is $1$ or $y^{\pm 1}$, which shows whether the two bits are equal. If $r$ is predictable, the attacker recomputes $r^2$ and checks whether $c = r^2$. Draw each $r$ from a cryptographic generator.
- **Active attackers.** Multiplying a ciphertext by $y$ flips its bit, and a decryption oracle reveals any bit after rerandomization, as above. Authenticate the ciphertext or use an IND-CCA scheme.
- **Short or special moduli.** Anyone who factors $N$ decrypts everything, so $N$ needs the same size as an RSA modulus, at least 2048 binary digits and 3072 for a 128-binary-digit security level. Do not reuse the modulus of another scheme whose security gives out other information about $p$ and $q$.
- **Side channels.** Line L6 multiplies by $y$ only for a 1 bit, and line L9 compares with 1. A timing difference reveals the bit. Real code must multiply in both cases (by $y^m$ computed without a branch) and run in constant time.

## Implementations

The Python code is for study only. It is not constant time, it branches on the message bits, and it must not protect real data. There are no official test vectors for GM; the tests check the worked example above, a round trip of a byte string with the primes $2^{31} - 1$ and $2^{61} - 1$, the Jacobi symbol against products of Legendre symbols, the XOR homomorphism, the bit flip by $y$, and the tight reduction from quadratic residuosity.

## History

Goldwasser and Micali presented the scheme at STOC 1982 in "Probabilistic encryption and how to play mental poker keeping secret all partial information", and the journal version "Probabilistic encryption" appeared in JCSS in 1984. The paper defined semantic security and polynomial security (indistinguishability), proved them equivalent, and proved GM secure under the quadratic residuosity assumption. It was the first public-key scheme with a proof that it hides all partial information. Blum and Goldwasser reduced the expansion in 1984, and Kushilevitz and Ostrovsky used the XOR homomorphism for private information retrieval in 1997. Goldwasser and Micali received the 2012 Turing Award, in part for this work.

## References
