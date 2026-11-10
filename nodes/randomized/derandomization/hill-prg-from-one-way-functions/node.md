---
tag: 4E8GV3
kind: theorem
slug: hill-prg-from-one-way-functions
name: PRG from one-way functions (HILL theorem)
aliases:
- HILL theorem
- Hastad-Impagliazzo-Levin-Luby theorem
area: randomized/derandomization
level: research
summary: One-way functions exist if and only if pseudorandom generators exist. The easy case uses a one-way permutation and the Goldreich-Levin bit; the general case needs pseudoentropy and hashing.
prereqs: [one-way-function, pseudorandom-generator, hard-core-predicate, yao-next-bit-unpredictability]
see_also: [blum-micali, leftover-hash-lemma, pseudorandom-function, computational-indistinguishability, universal-hash-family, cryptographically-secure-prng, pseudorandom-generation, stream-cipher]
sources:
  - paper: doi:10.1137/S0097539793244708
    title: Johan Hastad, Russell Impagliazzo, Leonid A. Levin and Michael Luby, A pseudorandom generator from any one-way function, SIAM Journal on Computing 28(4), 1999
    locator: the main theorem (a pseudorandom generator from any one-way function), with false entropy, pseudoentropy and hashing
  - paper: doi:10.1145/73007.73009
    title: Russell Impagliazzo, Leonid A. Levin and Michael Luby, Pseudo-random generation from one-way functions, 21st ACM Symposium on Theory of Computing (STOC), 1989
    locator: the non-uniform version of the construction and the use of universal hashing to extract pseudoentropy
  - paper: doi:10.1145/73007.73010
    title: Oded Goldreich and Leonid A. Levin, A hard-core predicate for all one-way functions, 21st ACM Symposium on Theory of Computing (STOC), 1989
    locator: the hard-core bit <x, r> for f'(x, r) = (f(x), r)
  - paper: doi:10.1137/0213053
    title: Manuel Blum and Silvio Micali, How to generate cryptographically strong sequences of pseudo-random bits, SIAM Journal on Computing 13(4), 1984
    locator: the iterated generator from a permutation and a hard-core predicate
  - paper: doi:10.1109/SFCS.1982.45
    title: Andrew C. Yao, Theory and applications of trapdoor functions, 23rd IEEE Symposium on Foundations of Computer Science (FOCS), 1982
    locator: generators from one-way permutations, and the next-bit test
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Chapter 2 (hard-core predicates and the Goldreich-Levin theorem) and Chapter 3 (generators from one-way permutations; an outline of the general construction)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 9 (one-way functions, the Goldreich-Levin theorem and generators from one-way permutations)
---

The HILL theorem, by Håstad, Impagliazzo, Levin and Luby, says that a [pseudorandom generator](/pseudorandom-generator/) exists if a [one-way function](/one-way-function/) exists. The converse is easy, so the two assumptions are equivalent. The case of a one-way *permutation* is much older and short: the generator outputs the Goldreich-Levin [hard-core bit](/hard-core-predicate/) along the orbit of the permutation, which is the [Blum-Micali](/blum-micali/) and Yao construction. This page proves that case in full and outlines the general case, which needs pseudoentropy and the [leftover hash lemma](/leftover-hash-lemma/).

## Statement

All functions are computable in polynomial time, and all adversaries are probabilistic polynomial-time algorithms (or polynomial-size circuits, for the non-uniform version). Negligible means smaller than $1/p(n)$ for every polynomial $p$ and all large $n$.

**Theorem (HILL 1999).** If a one-way function exists, then a pseudorandom generator exists. Conversely, if a pseudorandom generator exists, then a one-way function exists.

The forward direction is the hard part. The theorem is *conditional* in the sense that nobody knows whether one-way functions exist; their existence implies P $\ne$ NP. The implication itself is proved without any assumption.

**Theorem (the permutation case: Blum and Micali 1984, Yao 1982, Goldreich and Levin 1989).** Let $f : \{0,1\}^n \to \{0,1\}^n$ be a one-way permutation. For $\ell = \ell(n)$ a polynomial, define the generator on the seed $(x, r) \in \{0,1\}^n \times \{0,1\}^n$ by

$$G_\ell(x, r) = \big(f^{\ell}(x),\ r,\ \langle x, r \rangle,\ \langle f(x), r \rangle,\ \ldots,\ \langle f^{\ell-1}(x), r \rangle\big),$$

where $\langle x, r \rangle = \sum_j x_j r_j \bmod 2$. Then $G_\ell$ is a pseudorandom generator from $2n$ to $2n + \ell$ bits.

The concrete form of the proof: if $f$ is computed by a circuit of size $s_f$ and a test of size $t$ has advantage $\varepsilon$ against $G_\ell$, then a circuit of size at most $t + \ell (s_f + O(n))$ predicts $\langle x, r \rangle$ from $(f(x), r)$ with probability at least $\frac12 + \frac{\varepsilon}{\ell}$.

## In plain words

A one-way function is easy to compute and hard to undo. A pseudorandom generator turns a short random seed into a long string that no fast program can tell from random. The theorem says that these two things come together: one exists exactly when the other does.

When the one-way function is a permutation, the generator is short. It takes a secret starting point and a random mask. At each step it outputs one bit, the parity of the current point under the mask, and then it moves the point one step along the permutation. Each bit is hard to guess from what comes after it, because guessing it would undo the permutation. For a general one-way function, the outputs can collide, and the proof needs extra steps that collect hidden randomness and then purify it by hashing.

## Proof

The proof of the permutation case has three steps: a hard-core bit, one bit of stretch, and the stretch extension. The converse is proved last.

**Step 1: a hard-core bit (cited).** The Goldreich-Levin theorem says: if a circuit $P$ of size $t$ has $\Pr_{x, r}[P(f(x), r) = \langle x, r \rangle] \ge \frac12 + \delta$, then a circuit of size $t \cdot \mathrm{poly}(n, 1/\delta)$ inverts $f$ on a fraction $\Omega(\delta)$ of the inputs. The proof is a [list-decoding](/list-decoding/) algorithm for the [Hadamard code](/hadamard-code/); see Goldreich and Levin (1989), or Goldreich, Chapter 2. So if $f$ is one-way, then $b(x, r) = \langle x, r \rangle$ is a hard-core predicate of the permutation $g(x, r) = (f(x), r)$ of $\{0,1\}^{2n}$: no polynomial-size circuit predicts it from $g(x, r)$ with an advantage that is not negligible.

**Step 2: one bit of stretch.** Let $G(x, r) = (g(x, r), b(x, r)) = (f(x), r, \langle x, r \rangle)$, from $2n$ to $2n + 1$ bits. Let $D$ be a test of size $t$ with $\Pr[D(G(U_{2n})) = 1] - \Pr[D(U_{2n+1}) = 1] = \varepsilon > 0$; if the sign is negative, negate $D$.

Since $g$ is a permutation, $g(U_{2n})$ is exactly uniform on $\{0,1\}^{2n}$. So the hybrid $H_{2n}$ of [Yao's theorem](/yao-next-bit-unpredictability/), the first $2n$ bits of $G(U_{2n})$ followed by one uniform bit, is exactly $U_{2n+1}$. In the notation of that theorem, $p_0 = p_1 = \cdots = p_{2n}$ and $p_{2n+1} - p_{2n} = \varepsilon$. The predictor for the last position therefore succeeds with probability exactly $\frac12 + \varepsilon$, and with its random bit fixed it is a circuit $P$ of size at most $t + 2$ with

$$\Pr_{x, r}\big[P(f(x), r) = \langle x, r \rangle\big] \ge \tfrac12 + \varepsilon.$$

There is no loss of a factor $2n + 1$, because only the last hybrid step can contribute. By Step 1, $\varepsilon$ is negligible, so $G$ is a generator with stretch one.

**Step 3: polynomial stretch.** Apply the stretch extension of [pseudorandom generator](/pseudorandom-generator/) to $G$, and keep the final state. The state is $(x_i, r)$ with $x_i = f^i(x)$, so the bit at step $i$ is $\langle f^{i-1}(x), r \rangle$, and the output is $G_\ell(x, r)$ as defined above. The hybrid proof given there works without change when the final state is appended: let $H_j$ be $j$ uniform bits followed by the output of $\ell - j$ steps from a uniform state; then $H_0 = G_\ell(U_{2n})$, $H_\ell = U_{2n+\ell}$, and two neighbors $H_j$, $H_{j+1}$ are the images of $G(U_{2n})$ and $U_{2n+1}$ under one map that uses $\ell - j - 1$ copies of $G$. A test of size $t$ with advantage $\varepsilon$ on $G_\ell$ gives a test of size at most $t + \ell (s_f + O(n))$ with advantage $\varepsilon/\ell$ on $G$. Step 2 converts it into the predictor of the statement. $\ell$ is a polynomial, so $\varepsilon$ is negligible.

**The converse.** Let $G : \{0,1\}^n \to \{0,1\}^{\ell(n)}$ be a generator. By the stretch extension we may assume $\ell(n) \ge 2n$. Then $G$ itself is one-way. Suppose an algorithm $A$ inverts it: $\Pr_s[G(A(G(s))) = G(s)] \ge 1/p(n)$ for a polynomial $p$ and infinitely many $n$. Define the test $D(z) = 1$ if $G(A(z)) = z$. On $G(U_n)$ it accepts with probability at least $1/p(n)$. On $U_{\ell}$ it accepts only strings in the image of $G$, which has at most $2^n$ elements out of $2^{\ell} \ge 2^{2n}$, so with probability at most $2^{-n}$. The advantage $1/p(n) - 2^{-n}$ is not negligible, which is a contradiction. $\blacksquare$

**The general case (outline, not proved here).** For a one-way function $f$ that is not a permutation, $f(U_n)$ need not be uniform, and Step 2 fails. Håstad, Impagliazzo, Levin and Luby replace it by the following chain.

1. *Pseudoentropy.* A distribution has pseudoentropy $k$ if it is computationally indistinguishable from a distribution with entropy $k$. From $f$, the Goldreich-Levin bit and pairwise independent hashing of $f(x)$ by a length that is guessed, they build a function whose output has pseudoentropy larger than its true entropy by a fraction of a bit. They call this a false entropy generator.
2. *Flattening.* Many independent copies are concatenated. By concentration, the Shannon entropy of the copies becomes close to their min-entropy, and the gap in pseudoentropy adds up over the copies.
3. *Extraction.* A [universal hash](/universal-hash-family/) function, with its key part of the seed and of the output, is applied. By the [leftover hash lemma](/leftover-hash-lemma/), the result is close to uniform in the computational sense, and it is longer than the seed.

Each step loses a polynomial factor, so the seed length of the final generator is a large polynomial in $n$. The details are in the HILL paper and in Goldreich, Chapter 3.

## Consequences

- **The equivalence.** One-way functions, pseudorandom generators, [pseudorandom functions](/pseudorandom-function/) (by the construction of Goldreich, Goldwasser and Micali) and private-key encryption with [semantic security](/semantic-security/) for many messages all exist under the same single assumption.
- **Stream ciphers.** A generator with polynomial stretch is a [stream cipher](/stream-cipher/) in the theoretical sense: the key is the seed and the output is XORed with the message.
- **Minimal assumption.** Since a generator gives a one-way function, a one-way function is the weakest assumption from which pseudorandomness in the cryptographic sense can follow.
- **A toy trace.** Take $n = 4$, the permutation $f(x) = 5x + 3 \bmod 16$, $x = 6$ and $r = 11$, with bit $j$ of a number as coordinate $j$. The orbit $x_{i-1} = f^{i-1}(x)$ and the bits $\langle x_{i-1}, r \rangle$ are:

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $x_{i-1}$ | 6 | 1 | 8 | 11 | 10 | 5 |
| $\langle x_{i-1}, r \rangle$ | 1 | 1 | 1 | 1 | 0 | 1 |

The output of $G_6$ is $f^6(6) = 12$, then $r = 11$, then the six bits $1, 1, 1, 1, 0, 1$: 14 bits from an 8-bit seed. This $f$ is easy to invert, so the toy is not secure; it shows only the shape of the output.

**Why a linear $f$ fails.** If $f(x) = Ax$ for an invertible matrix $A$ over $\mathrm{GF}(2)$, then $\langle f^{i-1}(x), r \rangle = \langle x, (A^{\mathsf T})^{i-1} r \rangle$. The vectors $(A^{\mathsf T})^{i-1} r$ for $i = 1, \ldots, n + 1$ are linearly dependent, and the test can find a dependency from $r$, which is part of the output. The same XOR of the output bits is then always 0, while on uniform bits it is 0 with probability $\frac12$. The test has advantage exactly $\frac12$.

## Tightness

- **The converse holds**, so one-way functions are both necessary and sufficient.
- **Loss in the permutation case.** The reduction loses a factor $\ell$ in the advantage and adds $\ell$ copies of $f$ to the size of the test. A seed of $2n$ bits gives $\ell$ bits for any polynomial $\ell$.
- **Seed length in the general case.** The HILL construction has a seed length that is a large polynomial in the input length of $f$. Haitner, Reingold and Vadhan (2013) and Vadhan and Zheng (2012) shortened it a great deal, using a notion called next-block pseudoentropy. No construction from a general one-way function with a seed of $O(n)$ bits is known.

## History

Blum and Micali (1982, journal version 1984) built a generator from the discrete logarithm by iterating it and outputting a hard-core bit. Yao (1982) showed that any one-way permutation with a hard-core predicate gives a generator, and proved the next-bit test universal. Goldreich and Levin (1989) showed that every one-way function has the hard-core bit $\langle x, r \rangle$, which made the permutation case work for every one-way permutation. Impagliazzo, Levin and Luby (1989) gave the construction from any one-way function for non-uniform adversaries, and Håstad (1990) gave the uniform case; the combined journal paper of Håstad, Impagliazzo, Levin and Luby appeared in 1999.

## References
