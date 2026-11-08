---
tag: QDNJTG
kind: algorithm
slug: blum-blum-shub
name: Blum Blum Shub
aliases:
- BBS
- x^2 mod n generator
- quadratic residue generator
area: numerical/random-number-generation
level: advanced
summary: Squares the state modulo a Blum integer n = p q with p and q both 3 mod 4 and outputs the low bit of each state; predicting the output is as hard as factoring n.
model: word-ram
complexity:
  vars: {k: the number of squarings, L: the length of n in machine words}
  time: {worst: Θ(k L^2)}
  space: {extra: Θ(L)}
properties: {deterministic: true, recursive: false, cryptographic: true}
history:
  year: 1986
  people: [Lenore Blum, Manuel Blum, Michael Shub]
  note: The SIAM Journal on Computing paper proved the generator unpredictable under the quadratic residuosity assumption and analysed its period; Alexi, Chor, Goldreich and Schnorr reduced its security to factoring in 1988.
prereqs: [quadratic-residue, integer-factorization, cryptographically-secure-prng]
see_also: [blum-micali, hard-core-predicate, rabin-cryptosystem, blum-goldwasser-cryptosystem, quadratic-residuosity-problem, carmichael-function, modular-square-root, yao-next-bit-unpredictability]
sources:
  - paper: "Lenore Blum, Manuel Blum and Michael Shub, A simple unpredictable pseudo-random number generator, SIAM Journal on Computing 15(2), 1986, 364-383"
    locator: the x^2 mod N generator, the proof of unpredictability under the quadratic residuosity assumption, and the theorems on the period via lambda(lambda(N))
  - paper: "Werner Alexi, Benny Chor, Oded Goldreich and Claus P. Schnorr, RSA and Rabin functions: certain parts are as hard as the whole, SIAM Journal on Computing 17(2), 1988, 194-209"
    locator: the result that the least significant bit of the Rabin function is a hard-core predicate if factoring is hard, and its application to the x^2 mod N generator
  - paper: "Umesh V. Vazirani and Vijay V. Vazirani, Efficient and secure pseudo-random number generation, 25th IEEE Symposium on Foundations of Computer Science, 1984, 458-463"
    locator: the simultaneous security of O(log log N) low-order bits per squaring
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 5, Section 5.5, Cryptographically secure pseudorandom bit generation (Algorithm 5.40, the Blum-Blum-Shub pseudorandom bit generator, and the remarks on extracting j bits per step)
  - paper: "Andrey Sidorenko and Berry Schoenmakers, Concrete security of the Blum-Blum-Shub pseudorandom generator, Cryptography and Coding 2005, Lecture Notes in Computer Science 3796, Springer"
    locator: the concrete security reduction and the modulus sizes it requires
---

Blum Blum Shub (BBS) is a pseudorandom bit generator whose security is proved from a number-theoretic assumption. Its state is a number $x$ modulo $n = p q$, where $p$ and $q$ are secret primes both congruent to 3 modulo 4. Each step squares the state modulo $n$ and outputs its lowest bit. Anyone who can predict the next output bit better than by guessing can factor $n$. The cost is speed: one squaring of a number with thousands of binary digits per output bit, which makes BBS the textbook example of a provably secure [CSPRNG](/cryptographically-secure-prng/) and almost never the practical choice.

## In plain words

Pick two large secret primes of a special form and multiply them to get a public number $n$. Start with a secret number, and over and over replace it by its square, keeping only the remainder after dividing by $n$. Each time, write down whether the number is even or odd. That string of even and odd answers is the output.

Squaring is easy, but going backwards (taking a square root modulo $n$) is as hard as splitting $n$ into its two primes. The proof shows that even guessing whether the next number will be even or odd, with any real advantage, would give a way to split $n$.

## The problem

Given a seed of $\kappa$ uniformly random bits, produce a much longer bit string that no polynomial-time algorithm can distinguish from uniform, under a standard hardness assumption. In the notation of generators, the state space is $S = \mathrm{QR}_n$, the set of quadratic residues modulo $n$ that are coprime to $n$, the transition is $f(x) = x^2 \bmod n$, and the output is $g(x) = x \bmod 2^j$, the $j$ lowest bits, with $j = 1$ in the basic version.

A **Blum integer** is $n = p q$ with $p, q$ distinct primes, $p \equiv q \equiv 3 \pmod 4$. For such $n$, $-1$ is a quadratic non-residue modulo $p$ and modulo $q$, and squaring is a permutation of $\mathrm{QR}_n$: each residue has exactly one square root that is itself a residue. So $f$ is a [trapdoor one-way permutation](/trapdoor-one-way-function/) of $\mathrm{QR}_n$, assuming factoring is hard, with the factorization as trapdoor.

## The algorithm

```pseudo id=main
BBS(n, s, k)                       ▷ n = p q, p ≡ q ≡ 3 (mod 4); seed s with gcd(s, n) = 1
L1  x ← s² mod n                    ▷ x_0, a quadratic residue
L2  for i ← 1 to k
L3      x ← x² mod n                ▷ x_i = x_(i-1)² mod n
L4      b_i ← x mod 2               ▷ or the j lowest bits, j = O(log log n)
L5  return b_1 b_2 … b_k
```

Key generation picks random primes $p, q \equiv 3 \pmod 4$ of equal size, for example by [Miller-Rabin](/miller-rabin/) testing of random candidates whose two lowest bits are set, and discards them after computing $n$; the generator itself never needs $p$ and $q$. The seed $s$ must be uniform in $\mathbb{Z}_n^*$ (or at least have full entropy), and $n$ may be public.

## Example

Take $p = 11$, $q = 23$, $n = 253$ and the seed $s = 3$, so $x_0 = 9$.

| $i$ | $x_i = x_{i-1}^2 \bmod 253$ | $x_i$ in binary | output $b_i$ |
|---|---|---|---|
| 0 | 9 | 1001 | |
| 1 | 81 | 1010001 | 1 |
| 2 | 236 | 11101100 | 0 |
| 3 | 36 | 100100 | 0 |
| 4 | 31 | 11111 | 1 |
| 5 | 202 | 11001010 | 0 |
| 6 | 71 | 1000111 | 1 |

The state sequence has period 20: $9$ has multiplicative order $t = 55$ modulo 253, and $2$ has order 20 modulo 55. This is the largest possible, $\lambda(\lambda(253)) = \lambda(110) = 20$, where $\lambda$ is [Carmichael's function](/carmichael-function/). The seed $x_0 = 1$ is a fixed point and must be avoided.

**Direct access and reversal with the trapdoor.** Knowing $p$ and $q$, $x_i = x_0^{\,2^i \bmod \lambda(n)} \bmod n$ for any $i$, and $x_{i-1}$ is the unique residue square root of $x_i$, computed as $x_i^{(p+1)/4} \bmod p$ and $x_i^{(q+1)/4} \bmod q$ combined by the [Chinese remainder theorem](/chinese-remainder-theorem/). The tests check both on 200 steps with an 80-bit modulus. Without $p$ and $q$, neither is known to be feasible.

## Correctness

**Squaring permutes the residues.** Let $x \in \mathrm{QR}_n$. Its square roots modulo $p$ are $\pm a$, and exactly one of them is a residue because $-1$ is not (Euler's criterion with $p \equiv 3 \pmod 4$); the same holds modulo $q$, so by the CRT exactly one of the four square roots of $x$ modulo $n$ lies in $\mathrm{QR}_n$. So $f$ is a bijection of $\mathrm{QR}_n$, a group of odd order $(p-1)(q-1)/4$.

**Period.** By induction, $x_i = x_0^{2^i} \bmod n$. Let $t$ be the order of $x_0$ in $\mathrm{QR}_n$; it divides the odd group order, so $t$ is odd and 2 is invertible modulo $t$. Then $x_i = x_0$ if and only if $2^i \equiv 1 \pmod t$, so the sequence is purely periodic with period $\rho = \operatorname{ord}_t(2)$, and $\rho$ divides $\lambda(\lambda(n))$. Exhaustive checks over all residues for seven small Blum integers confirm $\rho = \operatorname{ord}_t(2)$; for $n = 1081 = 23 \cdot 47$, 220 of the 253 residues reach the maximum $\lambda(\lambda(1081)) = 110$.

**Security (cited, not proved here).** Blum, Blum and Shub (1986) proved that the output is unpredictable, hence by [Yao's theorem](/yao-next-bit-unpredictability/) pseudorandom, if deciding quadratic residuosity modulo $n$ for Jacobi symbol $+1$ is hard (the [quadratic residuosity problem](/quadratic-residuosity-problem/)). Alexi, Chor, Goldreich and Schnorr (1988) proved that the least significant bit of $x^2 \bmod n$ on $\mathrm{QR}_n$ is a [hard-core predicate](/hard-core-predicate/) if factoring Blum integers is hard; with the Blum-Micali construction this makes BBS a pseudorandom generator under the factoring assumption alone. Vazirani and Vazirani (1984) and Alexi et al. show that $j = O(\log \log n)$ low bits per step are simultaneously secure. The proof page covers the permutation and period statements.

## Complexity

Each step is one modular squaring of an $L$-word number: $\Theta(L^2)$ word operations with schoolbook multiplication and reduction, or $O(L^{1.585})$ with Karatsuba multiplication and [Montgomery](/montgomery-multiplication/) or Barrett reduction. For $k$ steps and $j$ output bits per step that is $\Theta(k L^2)$ for $k j$ output bits, with $\Theta(L)$ words of state. For a 3072-bit modulus on 64-bit words, $L = 48$, so each output bit costs on the order of $48^2 \approx 2300$ word multiplications plus reduction, against a few word operations per output byte for [ChaCha20](/chacha20/) or AES in counter mode. Key generation costs a prime search, $O(L^3)$ word operations per Miller-Rabin round times $O(L)$ candidates in expectation.

## Properties

- **Provable security from factoring**, with the caveats on concrete parameters below.
- **Forward secrecy needs care.** The state $x_i$ determines every later output; but without the factorization, computing $x_{i-1}$ from $x_i$ is as hard as factoring, so an attacker who captures the state cannot recover earlier outputs, assuming factoring is hard.
- **Random access with the trapdoor.** The holder of $p$ and $q$ can jump to any position, which the BBS paper notes, and can run the generator backwards.
- **Not a statistical generator.** It is far too slow for simulation, and its output passes statistical tests only because of its security, not by design.

## Variants and improvements

- **More bits per step.** Outputting the $j$ lowest bits with $j \le c \log_2 \log_2 n$ keeps the asymptotic proof. Implementations that output many more bits per squaring, such as half the bits of $x_i$, rely on stronger, less studied assumptions.
- **Blum-Goldwasser encryption.** Using the BBS stream as a one-time pad and appending $x_{k+1}$ gives the [Blum-Goldwasser cryptosystem](/blum-goldwasser-cryptosystem/), where the holder of the factors recovers $x_0$ by running the generator backwards.
- **Blum-Micali.** The general template, a one-way permutation iterated with a hard-core predicate as output, with modular exponentiation in place of squaring, is the [Blum-Micali generator](/blum-micali/).
- **Special primes.** The BBS paper suggests primes with $p = 2 p_1 + 1$, $p_1 = 2 p_2 + 1$ (and likewise for $q$) so that $\lambda(\lambda(n))$ is large and short cycles are rare; for random large $p$ and $q$ short cycles are already extremely unlikely, and the security proof does not need special primes.
- **RSA generator.** Iterating $x \mapsto x^e \bmod n$ with the RSA exponent and outputting low bits gives a generator secure under the [RSA problem](/rsa-problem/), with a similar cost.

## When to use it

Use it in teaching and in theory as the standard example of a generator with a proof from factoring, and in settings that require a reduction to a number-theoretic problem and can afford the cost. For practical cryptographic randomness, a [DRBG](/hmac-drbg/) or a stream cipher is many orders of magnitude faster and is trusted on the strength of extensive cryptanalysis rather than a reduction.

## Pitfalls

- **Concrete security.** The reductions lose large polynomial factors. Sidorenko and Schoenmakers (2005) computed what the proof guarantees for concrete parameters; for meaningful guarantees the modulus must be several thousand binary digits, larger than the moduli commonly used for RSA. A 1024-bit BBS gives no proved security level of practical value.
- **Too many bits per step.** Outputting most of $x_i$ breaks the proof and makes the state easy to reconstruct; outputting all of it gives the state away.
- **Known factorization.** Whoever knows $p$ and $q$ can run the generator backwards and recover the seed. The modulus generator must destroy them or be trusted.
- **Bad seeds.** $s = 1$ or $s = n - 1$ give $x_i = 1$ forever; seeds that are not coprime to $n$ reveal a factor. Seed uniformly from $\mathbb{Z}_n^*$.
- **Timing side channels.** Square-and-reduce with data-dependent branches leaks the state; use constant-time arithmetic.
- **Using a small $n$ for speed.** A modulus that can be factored, such as 512 bits today, gives no security at all.

## Implementations

## History

Lenore Blum, Manuel Blum and Michael Shub presented the $x^2 \bmod N$ generator at CRYPTO 1982 and published the full paper in 1986, proving unpredictability under the quadratic residuosity assumption and studying the period through $\lambda(\lambda(N))$; they compared it with the insecure $1/P$ generator. Vazirani and Vazirani (1984) showed that $O(\log \log N)$ bits per step can be output. Alexi, Chor, Goldreich and Schnorr (1988) proved that the least significant bit is hard-core under the factoring assumption, which made BBS secure if factoring is hard. Blum and Goldwasser (1984) built a public-key encryption scheme on it.

## References
