---
tag: B6YRKD
kind: algorithm
slug: naccache-stern-cryptosystem
name: Naccache-Stern cryptosystem
area: cryptography/public-key
level: research
summary: "Encryption c = g^m x^σ mod N where σ is a product of small primes. Decryption takes small discrete logarithms and joins them by the CRT. Additively homomorphic, IND-CPA under higher residuosity."
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of N, k: the number of small primes in σ, s: the sum of the small primes}
  time: {worst: Θ(k·b^3), average: Θ(k·b^3), best: Θ(k·b^3)}
  space: {extra: Θ(b + s)}
properties: {deterministic: false, randomized: true}
history:
  year: 1998
  people: [David Naccache, Jacques Stern]
  note: Presented at ACM CCS 1998. It extends the dense probabilistic encryption of Benaloh (1994) from one prime to a product of many small primes.
prereqs: [public-key-encryption, modular-exponentiation, chinese-remainder-theorem, pohlig-hellman]
see_also: [paillier-cryptosystem, okamoto-uchiyama-cryptosystem, goldwasser-micali-cryptosystem, homomorphic-encryption, decisional-composite-residuosity, merkle-hellman-knapsack-cryptosystem, quadratic-residuosity-problem, baby-step-giant-step]
sources:
  - paper: "David Naccache and Jacques Stern, A new public key cryptosystem based on higher residues, Proceedings of the 5th ACM Conference on Computer and Communications Security (CCS 1998), pages 59 to 66"
    locator: the key generation with p = 2au + 1 and q = 2bv + 1, the deterministic and the probabilistic schemes, decryption by small discrete logarithms and the Chinese remainder theorem, and the security discussion
  - paper: "David Naccache and Jacques Stern, A new public-key cryptosystem, Eurocrypt 1997, LNCS 1233, pages 27 to 36"
    locator: the different multiplicative knapsack scheme with public v_i = p_i^(1/s) mod P
  - paper: "Josh Benaloh, Dense probabilistic encryption, Proceedings of the Workshop on Selected Areas of Cryptography (SAC 1994), pages 120 to 128"
    locator: the scheme y^m u^r mod N for a single prime r that divides p − 1, which Naccache-Stern extends
  - paper: "Laurent Fousse, Pascal Lafourcade and Mohamed Alnuaimi, Benaloh's dense probabilistic encryption revisited, Africacrypt 2011, LNCS 6737, pages 348 to 362"
    locator: the correction of the key generation condition in Benaloh's scheme
  - paper: "Don Coppersmith, Finding a small root of a bivariate integer equation; factoring with high bits known, Eurocrypt 1996, LNCS 1070, pages 178 to 189"
    locator: the lattice method that factors N = pq when enough information on p is known, which limits how large σ can be
---

The Naccache-Stern cryptosystem is a [public-key encryption](/public-key-encryption/) scheme that David Naccache and Jacques Stern published in 1998. The message space is $\mathbb{Z}_\sigma$, where $\sigma$ is a product of many small distinct primes, and a message is sent as $c = g^m x^\sigma \bmod N$ for an RSA modulus $N$. The receiver, who knows $\varphi(N)$, finds $m$ modulo each small prime by a discrete logarithm in a group of that small order, and joins the parts with the [Chinese remainder theorem](/chinese-remainder-theorem/). This is the [Pohlig-Hellman](/pohlig-hellman/) idea used as a trapdoor. The scheme is additively [homomorphic](/homomorphic-encryption/) and IND-CPA under a higher residuosity assumption.

**Notation.** $p_1, \ldots, p_k$ are distinct small odd primes, $u$ is the product of half of them, $v$ the product of the other half, and $\sigma = uv$. $a$ and $b$ are large distinct primes, $p = 2au + 1$ and $q = 2bv + 1$ are primes, $N = pq$ has $b$ binary digits, and $\varphi = \varphi(N) = 4abuv$. The letter $b$ for the size of $N$ and the prime $b$ are told apart by context. $s = p_1 + \cdots + p_k$ is the total size of the decryption tables.

## In plain words

The receiver builds two secret primes so that the numbers one below them contain many small known prime factors. The product of these small primes is public, and a message is a number below it. To encrypt, the sender raises a public base to the message and hides the result with a random number raised to the public product.

To decrypt, the receiver uses the secret primes to look at the ciphertext through one small prime at a time. Through each such view the random part disappears, and the message shows up as one of only a few possible values, which a small table identifies. This gives the message modulo each small prime, and the remainders join into the full message. Multiplying two ciphertexts adds their messages.

## The problem

Naccache-Stern solves [public-key encryption](/public-key-encryption/) for messages in $\mathbb{Z}_\sigma$. It was designed as a probabilistic scheme with a dense message space: [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) sends one bit per ciphertext and Benaloh's scheme sends $\log_2 r$ bits for one prime $r$, while Naccache-Stern sends $\log_2 \sigma$ bits, a large fraction of $\log_2 N$. Its semantic security rests on the higher residuosity assumption: for each $p_i$, it is hard to decide if a random element of $\mathbb{Z}_N^*$ is a $p_i$-th power. This generalizes the [quadratic residuosity problem](/quadratic-residuosity-problem/) from 2 to odd primes.

## The algorithm

```pseudo id=main
NS-KEYGEN(p_1, …, p_k)                   ▷ distinct small odd primes, k even
L1  u ← p_1 ⋯ p_(k/2); v ← p_(k/2+1) ⋯ p_k; σ ← u·v
L2  a, b ← distinct large primes; p ← 2au + 1; q ← 2bv + 1
L3  if p or q is not prime then go to L2
L4  N ← p·q; φ ← (p − 1)(q − 1)
L5  g ← a square in Z_N^* of order φ/4    ▷ check g^(φ/(4f)) ≠ 1 for every prime f of φ/4
L6  return the public key (σ, N, g) and the private key (φ, p_1, …, p_k)

NS-ENCRYPT((σ, N, g), m)                  ▷ 0 ≤ m < σ
L7  x ← a uniform element of Z_N^*
L8  return c ← g^m · x^σ mod N

NS-DECRYPT((φ, p_1, …, p_k), c)
L9  for i ← 1 to k
L10     c_i ← c^(φ/p_i) mod N
L11     m_i ← the j in {0, …, p_i − 1} with c_i = g^(j·φ/p_i) mod N   ▷ a table of p_i entries, or baby-step giant-step
L12 return the m in Z_σ with m ≡ m_i (mod p_i) for all i         ▷ Chinese remainder theorem
```

Raising to $\varphi / p_i$ in line L10 kills the random factor: $x^{\sigma \varphi / p_i} = (x^\varphi)^{\sigma / p_i} = 1$ because $p_i$ divides $\sigma$. What remains is $(g^{\varphi/p_i})^m$, and $g^{\varphi/p_i}$ has order exactly $p_i$, so it reveals $m \bmod p_i$ and nothing more. The tables of line L11 hold $s = \sum p_i$ entries in all and depend only on the key, so they are built once at key generation.

## Example

Take $p_1, \ldots, p_4 = 3, 5, 7, 11$, so $u = 15$, $v = 77$ and $\sigma = 1155$. With $a = 19$ and $b = 13$, $p = 2 \cdot 19 \cdot 15 + 1 = 571$ and $q = 2 \cdot 13 \cdot 77 + 1 = 2003$ are prime, $N = 1143713$ and $\varphi = 570 \cdot 2002 = 1141140$. The square $g = 9$ has order $\varphi / 4 = 285285$.

| step | computation | value |
|---|---|---|
| L8 | $m = 202$, $x = 17$: $g^{202} \bmod N$ | 697934 |
| L8 | $17^{1155} \bmod N$ | 170166 |
| L8 | $c = 697934 \cdot 170166 \bmod N$ | 335411 |
| L10, L11 | $p_1 = 3$: $c^{\varphi/3} \bmod N = 713069$ | index 1 in the table |
| L10, L11 | $p_2 = 5$: $c^{\varphi/5} \bmod N = 963444$ | index 2 |
| L10, L11 | $p_3 = 7$: $c^{\varphi/7} \bmod N = 1031227$ | index 6 |
| L10, L11 | $p_4 = 11$: $c^{\varphi/11} \bmod N = 1015239$ | index 4 |
| L12 | $m \equiv 1, 2, 6, 4 \pmod{3, 5, 7, 11}$ | 202 |

Each index is the remainder of 202: $202 = 67 \cdot 3 + 1 = 40 \cdot 5 + 2 = 28 \cdot 7 + 6 = 18 \cdot 11 + 4$.

## Correctness

Let $c = g^m x^\sigma \bmod N$. For each $i$, $c^{\varphi / p_i} = (g^{\varphi/p_i})^m \cdot (x^{\varphi})^{\sigma / p_i}$, and the second factor is 1 by Euler's theorem because $\sigma / p_i$ is an integer. Write $\varphi / 4 = p_i t$. The order of $g^{\varphi/p_i} = g^{4t}$ is $(\varphi/4) / \gcd(\varphi/4, 4t) = p_i t / t = p_i$, since $p_i$ is odd. So $c_i = (g^{\varphi/p_i})^{m \bmod p_i}$ and line L11 finds the unique $j = m \bmod p_i$ below $p_i$. The $p_i$ are pairwise coprime, so line L12 returns the unique $m$ in $\mathbb{Z}_\sigma$ with these remainders. The full proof, with the existence of $g$, is in the proof file.

## Complexity

Let $b$ be the number of binary digits of $N$, and let a multiplication modulo $N$ cost $\Theta(b^2)$.

- **Key generation**: the search for $a$ and $b$ such that $2au + 1$ and $2bv + 1$ are prime is a prime search of the usual kind. The tables cost $s$ multiplications.
- **Encryption**: two exponentiations modulo $N$, with exponents of fewer than $b$ binary digits, so $\Theta(b^3)$.
- **Decryption**: $k$ exponentiations with exponents of about $b$ binary digits, so $\Theta(k b^3)$, plus $k$ table lookups. With baby-step giant-step instead of tables, each $m_i$ costs $\Theta(\sqrt{p_i})$ multiplications and no table. Since each $p_i$ divides only one of $p - 1$ and $q - 1$, the exponentiation for $p_i$ can be done modulo that prime alone, with half the number of binary digits.
- **Space**: the private tables hold $s = \sum p_i$ residues. With small primes below a few thousand the tables are small.

## Properties

- **Additively homomorphic.** $c_1 c_2 = g^{m_1 + m_2} (x_1 x_2)^\sigma$ is an encryption of $m_1 + m_2 \bmod \sigma$, and $c^e$ is an encryption of $e m \bmod \sigma$. Unlike [Okamoto-Uchiyama](/okamoto-uchiyama-cryptosystem/), the message space $\mathbb{Z}_\sigma$ is public, so sums wrap modulo a known number.
- **IND-CPA under higher residuosity.** The factor $x^\sigma$ is a uniform $\sigma$-th power. If no algorithm can tell $\sigma$-th powers from random elements of $\mathbb{Z}_N^*$, then $g^m x^\sigma$ hides $m$. By the CRT this splits into one decision problem per prime $p_i$.
- **Malleable, so not IND-CCA.** Any additively homomorphic scheme is malleable: from $c$ anyone can make an encryption of $m + 1$.
- **A deterministic variant.** The paper also has the deterministic scheme $c = g^m \bmod N$. It decrypts in the same way but it is not IND-CPA, because equal messages give equal ciphertexts.

## Variants and improvements

- **Benaloh (1994).** Dense probabilistic encryption is the case of one prime: $c = y^m u^r \bmod N$ with $r \mid p - 1$. Fousse, Lafourcade and Alnuaimi (2011) showed that the key generation condition in the original paper was too weak, which made decryption ambiguous for some keys, and corrected it.
- **Okamoto-Uchiyama and Paillier.** The same year, [Okamoto-Uchiyama](/okamoto-uchiyama-cryptosystem/) found an easy logarithm in a subgroup of order $p$ of $\mathbb{Z}_{p^2}^*$, and a year later [Paillier](/paillier-cryptosystem/) used $\mathbb{Z}_{N^2}^*$. These give a message space of size $p$ or $N$ and decryption by one exponentiation instead of $k$, which is why Paillier replaced Naccache-Stern in practice.
- **The 1997 knapsack scheme (a different cryptosystem).** At Eurocrypt 1997 the same authors proposed a multiplicative knapsack. The public key is a prime $P$ and $v_i = p_i^{1/s} \bmod P$, where $p_1, \ldots, p_n$ are small primes with $\prod p_i < P$ and $s$ is a secret exponent coprime to $P - 1$. A bit string $m$ is sent as $c = \prod v_i^{m_i} \bmod P$. The receiver computes $c^s \bmod P = \prod p_i^{m_i}$, which is an integer below $P$, and factors it by trial division. For example, with $P = 2003$, $s = 3$ and the primes $2, 3, 5, 7$, the public key is $v = (268, 1326, 1282, 1152)$; the bits $1011$ give $c = 268 \cdot 1282 \cdot 1152 \bmod 2003 = 743$, and $743^3 \bmod 2003 = 70 = 2 \cdot 5 \cdot 7$. The scheme is deterministic, so it is not IND-CPA, and its security has no reduction to a standard problem. Do not mix it up with the higher residue scheme of this page, and see [Merkle-Hellman](/merkle-hellman-knapsack-cryptosystem/) for the additive knapsacks that came before it.

## When to use it

Do not use Naccache-Stern for new systems. For confidentiality, use an IND-CCA2 scheme or [hybrid encryption](/hybrid-encryption/). For additive homomorphism, [Paillier](/paillier-cryptosystem/) and exponential [ElGamal](/elgamal-encryption/) are standardized in ISO/IEC 18033-6 and decrypt faster. Naccache-Stern is a good example of a trapdoor made from Pohlig-Hellman: the discrete logarithm is easy because the receiver knows that the group order is smooth, and the sender does not.

## Pitfalls

- **σ too large.** $p \equiv 1 \pmod{2u}$, so $u$ gives $p$ modulo $2u$. A lattice method of Coppersmith (1996) factors $N$ when $p$ is known modulo a number larger than about $N^{1/4}$, and anyone can try the ways to split the public $\sigma$ into $u$ and $v$. So $\sigma$ must stay much smaller than $N$, and the ciphertext is several times larger than the message.
- **Wrong order of $g$.** If the order of $g$ misses a prime $p_i$, then $g^{\varphi/p_i} = 1$ and the remainder modulo $p_i$ is lost. Line L5 checks the order.
- **Shared small primes.** If a prime $p_i$ divided both $p - 1$ and $q - 1$, the elements of order $p_i$ would not form a cyclic group, and line L11 would fail for most ciphertexts. The $p_i$ must be distinct, and $a$ and $b$ must differ from them, so that $\varphi/4$ is a product of distinct primes and the order test of line L5 is complete.
- **Decryption oracles.** The scheme is malleable, so a server that decrypts chosen ciphertexts gives away plaintexts.
- **Toy keys.** The keys of the example and of the tests (391 binary digits) are not secure.

## Implementations

The Python code is for study only. It is not constant time, it is not protected against side channels, and it must not protect real data. Use an IND-CCA2 scheme from a vetted library, for example HPKE (RFC 9180), and for additive homomorphism a maintained Paillier library. There are no official test vectors for Naccache-Stern. The tests check the example above, all 1155 messages of the toy key, round trips, the additive homomorphism and the deterministic variant on a key with 16 small primes from a fixed seed, and the 1997 knapsack example.

## History

Goldwasser and Micali (1984) encrypted one bit with quadratic residues, and Benaloh (1994) used residues of a higher prime degree $r$ to send $\log_2 r$ bits at once. Naccache and Stern (ACM CCS 1998) let the degree be a product of many small primes and decrypted with the Pohlig-Hellman method, which made the message space dense. A year earlier they had proposed a multiplicative knapsack at Eurocrypt 1997 under a similar title. In 1998 and 1999 the schemes of Okamoto and Uchiyama and of Paillier gave larger message spaces and faster decryption, and Paillier became the standard additively homomorphic scheme.

## References
