---
tag: MSZ3DP
kind: problem
slug: quadratic-residuosity-problem
name: Quadratic residuosity problem
aliases:
- QR assumption
area: cryptography/public-key
level: advanced
summary: Given N = pq and x with Jacobi symbol +1, decide whether x is a square modulo N. Easy with the factors, believed hard without; Goldwasser-Micali encryption rests on it.
prereqs: [quadratic-residue, jacobi-symbol, integer-factorization]
see_also: [goldwasser-micali-cryptosystem, legendre-symbol, quadratic-reciprocity, rabin-cryptosystem, blum-blum-shub, decisional-composite-residuosity, identity-based-encryption, decisional-diffie-hellman]
sources:
  - paper: doi:10.1016/0022-0000(84)90070-9
    title: Shafi Goldwasser and Silvio Micali, Probabilistic encryption, Journal of Computer and System Sciences 28(2), pages 270 to 299, 1984
    locator: the quadratic residuosity assumption, its random self-reduction and the encryption scheme built on it
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.4, The quadratic residuosity problem; Chapter 2, Section 2.4.5 (Legendre and Jacobi symbols)
  - paper: "Shafi Goldwasser, Silvio Micali and Charles Rackoff, The knowledge complexity of interactive proof systems, SIAM Journal on Computing 18(1), pages 186 to 208, 1989"
    locator: the zero-knowledge proof for quadratic residuosity
  - paper: "Lenore Blum, Manuel Blum and Michael Shub, A simple unpredictable pseudo-random number generator, SIAM Journal on Computing 15(2), pages 364 to 383, 1986"
    locator: the proof that the generator is unpredictable under the quadratic residuosity assumption
  - paper: "Clifford Cocks, An identity based encryption scheme based on quadratic residues, Cryptography and Coding 2001, LNCS 2260, pages 360 to 363"
    locator: identity-based encryption under the quadratic residuosity assumption
  - paper: "Tibor Jager and Jörg Schwenk, On the analysis of cryptographic assumptions in the generic ring model, ASIACRYPT 2009, LNCS 5912"
    locator: computing the Jacobi symbol is equivalent to factoring for generic ring algorithms
---

The quadratic residuosity problem (QR) asks, given an integer $N = pq$ with unknown prime factors and an $x \in \mathbb{Z}_N^*$ whose [Jacobi symbol](/jacobi-symbol/) is $+1$, whether $x$ is a [square](/quadratic-residue/) modulo $N$. With $p$ and $q$ the answer is two [Legendre symbols](/legendre-symbol/) away; without them, no algorithm faster than [factoring](/integer-factorization/) $N$ is known. Goldwasser and Micali (1982) made this the basis of the first provably secure [probabilistic encryption](/probabilistic-encryption/) scheme, [Goldwasser-Micali](/goldwasser-micali-cryptosystem/), and of the definition of semantic security. QR is no harder than factoring, and it is not known to be as hard.

**Notation.** $N = pq$ for distinct odd primes $p$ and $q$, and $\lambda$ is the security parameter, so that $N$ has about the length that resists factoring at level $\lambda$. $\left(\frac{x}{p}\right)$ is the Legendre symbol and $\left(\frac{x}{N}\right)$ the Jacobi symbol. $J_N = \{x \in \mathbb{Z}_N^* : (\frac{x}{N}) = +1\}$, $\mathrm{QR}_N$ is the set of squares in $\mathbb{Z}_N^*$, and $\widetilde{\mathrm{QR}}_N = J_N \setminus \mathrm{QR}_N$ is the set of *pseudosquares*. $\mathcal{A}$ is an adversary that runs in time $t$, and $\mathrm{Adv}$ its advantage. All results are in the standard model.

## In plain words

Modulo a prime, it is easy to tell whether a number is a perfect square: one exponentiation does it. Modulo a product of two secret primes, the number is a square only if it is a square modulo each prime. Anyone who knows the two primes checks each one and is done.

Someone who does not know the primes has a partial test, the Jacobi symbol, computed by a fast rule like the Euclidean algorithm. It catches the numbers that are a square modulo one prime and not the other. But it gives the same answer for numbers that are squares modulo both primes and for numbers that are squares modulo neither. The problem asks to separate those two kinds, and nobody knows how without finding the primes.

## Definition

**Input.** An integer $N = pq$, the product of two distinct odd primes of the same size, and an element $x \in J_N$. The factors are not given.

**Output.** 1 if $x \in \mathrm{QR}_N$, 0 if $x \in \widetilde{\mathrm{QR}}_N$.

**Structure.** By the [Chinese remainder theorem](/chinese-remainder-theorem/), $x$ is a square modulo $N$ iff it is a square modulo $p$ and modulo $q$. Since $\left(\frac{x}{N}\right) = \left(\frac{x}{p}\right)\left(\frac{x}{q}\right)$, the set $J_N$ splits into $\mathrm{QR}_N$, where both Legendre symbols are $+1$, and $\widetilde{\mathrm{QR}}_N$, where both are $-1$. The two halves have the same size: $|\mathrm{QR}_N| = |\widetilde{\mathrm{QR}}_N| = \varphi(N)/4$, and $|J_N| = \varphi(N)/2$.

**Advantage and assumption.** Let $\mathrm{Gen}(1^\lambda)$ output a modulus $N$. Then

$$\mathrm{Adv}^{\mathrm{qr}}(\mathcal{A}) = \bigl|\Pr[\mathcal{A}(N, x) = 1 : x \leftarrow \mathrm{QR}_N] - \Pr[\mathcal{A}(N, x) = 1 : x \leftarrow \widetilde{\mathrm{QR}}_N]\bigr|,$$

with $x$ uniform in each set. The **quadratic residuosity assumption** for $\mathrm{Gen}$ says that this is negligible in $\lambda$ for every adversary that runs in polynomial time.

## Variants

- **Blum integers.** $p \equiv q \equiv 3 \pmod 4$. Then $-1$ is a non-square modulo both primes, so $N - 1 \in \widetilde{\mathrm{QR}}_N$ is a known pseudosquare, and each square has exactly one square root that is itself a square. [Rabin](/rabin-cryptosystem/), [Blum-Blum-Shub](/blum-blum-shub/) and [Blum-Goldwasser](/blum-goldwasser-cryptosystem/) use Blum integers.
- **QR with a public pseudosquare.** The [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) public key contains $N$ and one $y \in \widetilde{\mathrm{QR}}_N$. This does not seem to help, since for Blum integers anyone knows such a $y$.
- **More prime factors.** For $N = p_1 \cdots p_k$ the Jacobi symbol leaves $2^{k-1}$ classes to separate.
- **Higher residuosity.** Decide whether $x$ is an $r$-th power modulo $N$ for $r \mid \varphi(N)$; Benaloh and Naccache-Stern encryption use it, and Paillier uses the related [decisional composite residuosity](/decisional-composite-residuosity/) modulo $N^2$.
- **Modulo a prime.** For a prime $p$ the problem is easy by [Euler's criterion](/euler-criterion/). This is the reason the [DDH](/decisional-diffie-hellman/) problem fails in all of $\mathbb{Z}_p^*$.

## Examples

Take $N = 21 = 3 \cdot 7$, a Blum integer. $\mathbb{Z}_{21}^*$ has $\varphi(21) = 12$ elements.

| set | elements | modulo 3 and modulo 7 |
|---|---|---|
| Jacobi symbol $-1$ | 2, 8, 10, 11, 13, 19 | a square modulo exactly one prime |
| $\mathrm{QR}_{21}$ | 1, 4, 16 | a square modulo both |
| $\widetilde{\mathrm{QR}}_{21}$ | 5, 17, 20 | a square modulo neither |

Each square has four square roots: 1 has roots 1, 8, 13, 20; 4 has 2, 5, 16, 19; 16 has 4, 10, 11, 17. The pseudosquare 20 is $-1$, as for every Blum integer. For 5, the Jacobi symbol is $\left(\frac{5}{3}\right)\left(\frac{5}{7}\right) = (-1)(-1) = +1$, and anyone can compute it by [quadratic reciprocity](/quadratic-reciprocity/) without the factors. Only the factors show that each Legendre symbol is $-1$.

| task | with $p, q$ | with $N$ only |
|---|---|---|
| Jacobi symbol of $x$ | easy | easy, $O((\log N)^2)$ by reciprocity |
| is $x$ a square modulo a prime | easy (Euler's criterion) | easy |
| is $x \in J_N$ a square modulo $N$ | easy, two Legendre symbols | QR problem, believed hard |
| a square root of $x \in \mathrm{QR}_N$ | easy, [modular square roots](/modular-square-root/) and CRT | as hard as factoring (Rabin) |
| a random square | easy, $r^2 \bmod N$ | easy, $r^2 \bmod N$ |
| a pseudosquare | easy | easy for Blum integers ($N - 1$); otherwise no method known |

## Known algorithms

- **Factor and test.** Factor $N$ with the number field sieve, in time $L_N[1/3, (64/9)^{1/3}]$, and compute $\left(\frac{x}{p}\right)$ by Euler's criterion. No faster method is known.
- **Quantum.** [Shor's algorithm](/shor-algorithm/) factors $N$ in polynomial time, so QR falls with it.
- **Guessing.** Answering at random has advantage 0. The Jacobi symbol gives nothing on $J_N$, by the structure above.

## Bounds

**Random self-reducibility (Goldwasser and Micali).** For uniform $r \in \mathbb{Z}_N^*$, $x r^2 \bmod N$ is uniform in $\mathrm{QR}_N$ if $x \in \mathrm{QR}_N$ and uniform in $\widetilde{\mathrm{QR}}_N$ if $x \in \widetilde{\mathrm{QR}}_N$. So an algorithm with advantage $\varepsilon$ on random inputs decides any fixed input: run it on $O(\varepsilon^{-2} \log(1/\delta))$ randomized copies and compare the fraction of 1 answers with its known rates on squares and on pseudosquares (random squares $r^2$ and the known pseudosquare give these rates). The error is at most $\delta$. Hence QR is as hard on average as in the worst case for a given $N$.

**Generic ring algorithms.** Jager and Schwenk (2009) showed that an algorithm that uses only ring operations on $\mathbb{Z}_N$ and computes the Jacobi symbol can be turned into a factoring algorithm. This supports the belief that the factors are needed, but it does not cover algorithms that use the binary representation, such as the Euclid-like Jacobi algorithm itself.

## Reductions

- **QR $\le$ factoring.** Shown above. The converse, that deciding squares is as hard as factoring, is a long-standing open question.
- **Square roots $\equiv$ factoring.** Computing square roots modulo $N$ is equivalent to factoring $N$: two roots $s \ne \pm s'$ of the same square give $\gcd(s - s', N) \in \{p, q\}$. This is the basis of [Rabin encryption](/rabin-cryptosystem/). So computing square roots is at least as hard as deciding squareness, which is only a decision problem.
- **QR $\equiv$ IND-CPA of Goldwasser-Micali.** A distinguisher for the scheme gives a QR solver with half the advantage, and conversely; the proof is on the [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) page.
- **QR and hard-core bits of Rabin.** The least significant bit of the square root that is a square is a [hard-core predicate](/hard-core-predicate/) of squaring for Blum integers under the factoring assumption. Blum, Blum and Shub (1986) first proved their generator secure under the stronger QR assumption.

## Applications

- **[Goldwasser-Micali encryption](/goldwasser-micali-cryptosystem/).** A bit $b$ is encrypted as $y^b r^2$; IND-CPA secure exactly under QR.
- **[Blum-Blum-Shub](/blum-blum-shub/) and [Blum-Goldwasser](/blum-goldwasser-cryptosystem/).** The output bits of $x_{i+1} = x_i^2 \bmod N$ are unpredictable under QR, and in later work under factoring.
- **[Zero-knowledge proofs](/zero-knowledge-proof/).** Goldwasser, Micali and Rackoff (1985) gave the first zero-knowledge proof for the language of quadratic residues: the prover shows $x \in \mathrm{QR}_N$ without revealing a root.
- **[Identity-based encryption](/identity-based-encryption/).** Cocks (2001) built an IBE scheme under QR, without pairings.
- **XOR-homomorphic encryption.** Goldwasser-Micali ciphertexts multiply to the XOR of their bits, which is used in private information retrieval and in some voting protocols.

## References
