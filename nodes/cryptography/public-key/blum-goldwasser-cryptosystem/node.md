---
tag: QJYEG7
kind: algorithm
slug: blum-goldwasser-cryptosystem
name: Blum-Goldwasser cryptosystem
aliases:
- BG cryptosystem
area: cryptography/public-key
level: advanced
summary: Probabilistic public-key encryption that XORs the message with Blum-Blum-Shub output and sends the last state. IND-CPA if factoring is hard; broken by chosen ciphertexts.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of n, l: the number of message digits}
  time: {worst: Θ(b^3 + l b^2 / log b), average: Θ(b^3 + l b^2 / log b), best: Θ(b^3 + l b^2 / log b)}
  space: {extra: Θ(l + b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1984
  people: [Manuel Blum, Shafi Goldwasser]
  note: Presented at CRYPTO 1984. It cut the expansion of Goldwasser-Micali from a factor of lg n to one element of Z_n.
prereqs: [blum-blum-shub, rabin-cryptosystem, probabilistic-encryption]
see_also: [goldwasser-micali-cryptosystem, hard-core-predicate, trapdoor-one-way-function, chinese-remainder-theorem, extended-euclidean-algorithm, integer-factorization, chosen-ciphertext-attack, stream-cipher]
sources:
  - paper: "Manuel Blum and Shafi Goldwasser, An efficient probabilistic public-key encryption scheme which hides all partial information, CRYPTO 1984, LNCS 196, pages 289 to 299"
    locator: the scheme and its security under factoring
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Section 8.7.2, Algorithms 8.55 and 8.56, Example 8.57, Notes 8.58 and 8.59
  - paper: "Lenore Blum, Manuel Blum and Michael Shub, A simple unpredictable pseudo-random number generator, SIAM Journal on Computing 15(2), pages 364 to 383, 1986"
    locator: the x^2 mod n generator and its unpredictability
  - paper: "Werner Alexi, Benny Chor, Oded Goldreich and Claus-Peter Schnorr, RSA and Rabin functions, certain parts are as hard as the whole, SIAM Journal on Computing 17(2), pages 194 to 209, 1988"
    locator: the O(log log n) lowest binary digits of the Rabin function are simultaneously hard-core under factoring
  - paper: "Umesh V. Vazirani and Vijay V. Vazirani, Efficient and secure pseudo-random number generation, FOCS 1984, pages 458 to 463"
    locator: several hard-core bits per squaring
  - paper: "Roger Fischlin and Claus-Peter Schnorr, Stronger security proofs for RSA and Rabin bits, Journal of Cryptology 13(2), pages 221 to 244, 2000"
    locator: a tighter reduction from factoring to predicting the low bits of the Rabin function
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 5, the randomized public-key encryption built from a trapdoor permutation and its hard-core bits
---

The Blum-Goldwasser cryptosystem (BG) is the [public-key encryption](/public-key-encryption/) scheme that Manuel Blum and Shafi Goldwasser presented in 1984. The sender runs the [Blum-Blum-Shub generator](/blum-blum-shub/) from a random seed, XORs its output onto the message like a [stream cipher](/stream-cipher/), and sends the final state $x_{t+1}$; the receiver, who knows the factors of $n$, takes square roots backwards to the seed and runs the generator again. It is [IND-CPA](/ind-cpa-security/) secure if factoring Blum integers is hard, and its ciphertext is only one element of $\mathbb{Z}_n$ longer than the message, against a factor of $\log_2 n$ for [Goldwasser-Micali](/goldwasser-micali-cryptosystem/). One chosen ciphertext breaks it.

**Notation.** $p$ and $q$ are distinct primes with $p \equiv q \equiv 3 \pmod 4$, and $n = pq$ is then a *Blum integer*. $b$ is the number of binary digits of $n$, $k = \lfloor \lg n \rfloor$ and $h = \lfloor \lg k \rfloor$, the number of binary digits taken from each state (HAC Algorithm 8.56). A message is $t$ blocks $m_1, \ldots, m_t$ of $h$ binary digits each, so $\ell = th$. $\mathrm{low}_h(x)$ is the number formed by the $h$ lowest binary digits of $x$. $QR_n$ is the set of squares modulo $n$. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary that runs in time $t_{\mathcal{A}}$, and $\mathrm{Adv}$ an advantage. All results here are in the standard model.

## In plain words

The receiver multiplies two secret primes of a special form and publishes the product. To send a message, the sender picks a random starting number and squares it again and again modulo the product. From each result it takes a few of the lowest binary digits, and uses this stream of digits as a one-time key: it XORs the stream onto the message. It sends the masked message and the last number of the chain.

Going forward in the chain is easy for everyone. Going backward means taking square roots, which is as hard as factoring the product, so an eavesdropper cannot get back to the start. The receiver knows the primes and can take all the square roots at once, find the starting number, rebuild the stream, and remove the mask.

## The problem

BG solves [public-key encryption](/public-key-encryption/) of long messages with a small expansion. It uses the [Rabin function](/rabin-cryptosystem/) $x \mapsto x^2 \bmod n$. For a Blum integer this function is a permutation of $QR_n$: each square has exactly one square root that is itself a square, its *principal* square root. Finding square roots modulo $n$ is as hard as [factoring](/integer-factorization/) $n$, and with $p$ and $q$ the principal root of $s$ modulo $p$ is $s^{(p+1)/4} \bmod p$. So squaring on $QR_n$ is a [trapdoor permutation](/trapdoor-one-way-function/), and its lowest $O(\log \log n)$ binary digits are [hard-core](/hard-core-predicate/): they look random to anyone who sees only the square.

## The algorithm

```pseudo id=main
BG-KEYGEN(p, q)                           ▷ distinct primes, p ≡ q ≡ 3 (mod 4)
L1  n ← p · q
L2  find a, b with a·p + b·q = 1          ▷ extended Euclidean algorithm
L3  return the public key n and the private key (p, q, a, b)

BG-ENCRYPT(n, m1 … mt)                    ▷ each mi has h binary digits
L4  x0 ← r² mod n for a uniform unit r modulo n
L5  for i ← 1 to t
L6      xi ← x(i−1)² mod n
L7      ci ← low_h(xi) ⊕ mi
L8  x(t+1) ← xt² mod n
L9  return (c1 … ct, x(t+1))

BG-DECRYPT((p, q, a, b), (c1 … ct, x(t+1)))
L10 d1 ← ((p + 1)/4)^(t+1) mod (p − 1);  d2 ← ((q + 1)/4)^(t+1) mod (q − 1)
L11 u ← x(t+1)^d1 mod p;  v ← x(t+1)^d2 mod q
L12 x0 ← v·a·p + u·b·q mod n
L13 for i ← 1 to t: xi ← x(i−1)² mod n;  mi ← low_h(xi) ⊕ ci
L14 return m1 … mt
```

Line L4 makes the seed a uniform element of $QR_n$, so every later state is in $QR_n$ too. Lines L5 to L7 are the Blum-Blum-Shub generator used as a pad. Line L8 squares once more, so that the value sent is not $x_t$ itself: the low digits of $x_t$ are part of the pad. Line L10 combines $t + 1$ principal square roots into one exponent, reduced by Fermat's little theorem. Line L12 is the [Chinese remainder theorem](/chinese-remainder-theorem/) with the coefficients of line L2 from the [extended Euclidean algorithm](/extended-euclidean-algorithm/).

## Example

This is Handbook of Applied Cryptography Example 8.57. The primes $p = 499$ and $q = 547$ are both $3 \bmod 4$, $n = 272953$, and $a = -57$, $b = 52$ satisfy $ap + bq = 1$. Then $k = 18$ and $h = 4$. The message is the 20 binary digits $1001\ 1100\ 0001\ 0000\ 1100$, so $t = 5$, and the seed is $x_0 = 399^2 \bmod n = 159201$.

| $i$ | $x_i = x_{i-1}^2 \bmod n$ | $\mathrm{low}_4(x_i)$ | $m_i$ | $c_i$ |
|---|---|---|---|---|
| 1 | 180539 | 1011 | 1001 | 0010 |
| 2 | 193932 | 1100 | 1100 | 0000 |
| 3 | 245613 | 1101 | 0001 | 1100 |
| 4 | 130286 | 1110 | 0000 | 1110 |
| 5 | 40632 | 1000 | 1100 | 0100 |

Line L8 gives $x_6 = 139680$, and the ciphertext is $(0010, 0000, 1100, 1110, 0100, 139680)$. To decrypt, line L10 computes $d_1 = 125^6 \bmod 498 = 463$ and $d_2 = 137^6 \bmod 546 = 337$. Line L11 gives $u = 139680^{463} \bmod 499 = 20$ and $v = 139680^{337} \bmod 547 = 24$, and line L12 gives $x_0 = 159201$. Line L13 then rebuilds the same column of pads and XORs it off. The test file checks every number of this example.

## Correctness

Every state $x_i$ is a square and a unit modulo $p$. For such a value Euler's criterion gives $x_{i-1}^{(p-1)/2} \equiv 1$, so $x_i^{(p+1)/4} = x_{i-1}^{(p+1)/2} \equiv x_{i-1} \pmod p$: raising to $(p+1)/4$ goes back one step. Doing this $t + 1$ times is raising to $((p+1)/4)^{t+1}$, and the exponent may be reduced modulo $p - 1$. So $u \equiv x_0 \pmod p$ and $v \equiv x_0 \pmod q$, and $ap + bq = 1$ makes $vap + ubq \equiv x_0$ modulo both primes. The receiver then regenerates the same pad. The full proof is below.

## Complexity

Let $b$ be the number of binary digits of $n$ and $\ell = th$ the number of message digits, with $h = \Theta(\log b)$. A multiplication modulo $n$ costs $\Theta(b^2)$ with schoolbook arithmetic.

- **Encryption**: $t + 2$ squarings modulo $n$, so $\Theta(b^2 + \ell b^2 / \log b)$. One squaring encrypts $h$ digits (HAC Note 8.59 (ii)).
- **Decryption**: two exponentiations with exponents below $p - 1$ and $q - 1$ (line L10), two [modular exponentiations](/modular-exponentiation/) modulo $p$ and $q$ (line L11), each $\Theta(b^3)$, and $t$ squarings modulo $n$: $\Theta(b^3 + \ell b^2 / \log b)$. This is the cost in the front matter (HAC Note 8.59 (iii)).
- **Expansion**: the ciphertext is $\ell + b$ binary digits for $\ell$ message digits (HAC Note 8.59 (i)): one element of $\mathbb{Z}_n$ in total.

For long messages BG is faster than RSA per message digit, but in practice [hybrid encryption](/hybrid-encryption/) with a symmetric cipher is faster still.

## Properties

### IND-CPA security under factoring

**Theorem (Blum and Goldwasser, 1984).** Let $h = O(\log \log n)$. If factoring Blum integers is hard, BG is IND-CPA secure (HAC Note 8.58 (i)).

*Proof sketch.* The adversary sees $(m \oplus P, x_{t+1})$, where $P = \mathrm{low}_h(x_1) \cdots \mathrm{low}_h(x_t)$. It suffices to show that $(P, x_{t+1})$ is indistinguishable from $(U, x_{t+1})$ with $U$ uniform; then the challenge looks the same for $m_0$ and $m_1$. Since $x_{t+1}$ is a uniform element of $QR_n$ and squaring permutes $QR_n$, anyone can compute $x_{i+1}, \ldots, x_{t+1}$ and the later blocks from $x_{i+1}$. A hybrid argument over the $t$ blocks therefore turns a distinguisher with advantage $\varepsilon$ into a predictor that, given $x_{i+1} = x_i^2$, tells $\mathrm{low}_h(x_i)$ from random with advantage at least $\varepsilon / t$. Alexi, Chor, Goldreich and Schnorr (1988) showed that such a predictor for $h = O(\log \log n)$ low digits of the principal root yields an algorithm that takes square roots modulo $n$, and so factors $n$. $\square$

The reduction is **not tight**. It loses the factor $t$ of the hybrid argument, and the hard-core bit reduction runs the predictor many times, a polynomial in $b$ and $1/\varepsilon$. Fischlin and Schnorr (2000) made it tighter, but for a modulus of fixed length the theorem gives no concrete guarantee by itself (HAC Note 8.58 (i)).

### Other properties

- **Probabilistic.** The seed is fresh for each message, so encrypting the same message twice gives different pads and different $x_{t+1}$.
- **Malleable, and broken by one chosen ciphertext.** XORing any $\delta$ into $c_1 \cdots c_t$ XORs $\delta$ into the decrypted message, so BG is not [non-malleable](/non-malleability/). In a [chosen-ciphertext attack](/chosen-ciphertext-attack/) the attacker flips every block and keeps $x_{t+1}$; the changed ciphertext differs from the challenge, and the oracle's answer XOR the flips is the message. HAC Note 8.58 (iii) also notes a chosen-ciphertext attack that recovers the private key, as for [Rabin](/rabin-cryptosystem/).
- **Decryption cost is nearly independent of $t$.** The four exponentiations of lines L10 and L11 replace $t + 1$ separate square roots.

## Variants and improvements

- **Any trapdoor permutation.** The same design works with any [trapdoor permutation](/trapdoor-one-way-function/) $f$ and hard-core bits $B$: apply $f$ again and again to a random seed, XOR the hard-core bits onto the message, and send the last state. With RSA in place of squaring, the receiver inverts with $d^{t+1} \bmod \varphi(n)$. Goldreich (2004) presents this general construction.
- **More digits per step.** Taking more than $O(\log \log n)$ digits per squaring speeds up encryption, but security then rests on a stronger assumption than factoring. Fischlin and Schnorr (2000) and later work studied how many digits may be taken.
- **Chosen-ciphertext security.** BG has no standard CCA secure version. Generic transforms such as the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) apply to any IND-CPA scheme, at the cost of the [random oracle model](/random-oracle-model/), and then a modern KEM is the simpler choice.
- **[Goldwasser-Micali](/goldwasser-micali-cryptosystem/).** The predecessor; it encrypts each bit with a whole element of $\mathbb{Z}_n$, under the quadratic residuosity assumption.

## When to use it

Use BG to study how a pseudorandom generator built from a trapdoor permutation gives efficient probabilistic encryption, with security from factoring. Do not use it to protect data. It is broken by one chosen ciphertext, and it has no standard parameters or test vectors. For real systems use [hybrid encryption](/hybrid-encryption/) with an IND-CCA secure KEM such as ECIES, HPKE or ML-KEM, or [RSA-OAEP](/rsa-oaep/).

## Pitfalls

- **Decrypting attacker-chosen ciphertexts.** One query recovers a message, and a chosen-ciphertext attack recovers the key (HAC Note 8.58 (iii)). Never expose a decryption oracle; add authentication of the whole ciphertext, or use a CCA secure scheme.
- **Too many digits per step.** The proof covers $h = O(\log \log n)$ digits per squaring; HAC takes $h = \lfloor \lg \lfloor \lg n \rfloor \rfloor$, 10 for a modulus of 1025 binary digits (Note 8.58 (ii)). Taking all digits of $x_i$ would hand out the states themselves.
- **Reused seed.** A repeated seed gives a repeated pad, and the XOR of two ciphertexts is the XOR of the two messages, as with a reused [one-time pad](/one-time-pad/). Draw $r$ from a cryptographic generator each time.
- **The block count is part of the key schedule.** Line L10 uses $t$. If blocks are dropped or added, the receiver computes a root of the wrong depth and gets a wrong seed; the test file shows this. Encode the message length so that $t$ is fixed by the ciphertext.
- **Wrong primes.** If $p$ or $q$ is $1 \bmod 4$, $(p+1)/4$ is not an integer and squaring is not a permutation of $QR_n$, so decryption fails. The key generator must check $p \equiv q \equiv 3 \pmod 4$.
- **Modulus size.** HAC asked for at least 1024 binary digits in 1996. Today the modulus needs the size of an RSA modulus at the same security level, at least 2048 and preferably 3072 binary digits.

## Implementations

The Python code is for study only. It is not constant time and must not protect real data. There are no official test vectors for BG; the tests check every number of HAC Example 8.57, round trips of byte strings with the primes $2^{31} - 1$ and $2^{61} - 1$, the randomization, the one-query chosen-ciphertext attack against a local oracle, the rejection of primes that are not $3 \bmod 4$, and the wrong seed that a wrong block count gives.

## History

Blum, Blum and Shub described the $x^2 \bmod n$ generator in the early 1980s (journal version 1986), and Vazirani and Vazirani (1984) and Alexi, Chor, Goldreich and Schnorr (journal version 1988) showed that several low digits per squaring are hard-core under factoring. Blum and Goldwasser presented the encryption scheme at CRYPTO 1984, as an efficient form of the [probabilistic encryption](/probabilistic-encryption/) that Goldwasser and Micali had defined in 1982. The Handbook of Applied Cryptography (1996) made it a standard textbook example, and also recorded its weakness against chosen-ciphertext attacks, which kept it out of practice.

## References
