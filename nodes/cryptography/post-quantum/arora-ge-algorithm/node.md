---
tag: SGHADM
kind: algorithm
slug: arora-ge-algorithm
name: Arora-Ge algorithm
aliases:
- Arora-Ge attack
area: cryptography/post-quantum
level: research
summary: Algebraic attack on LWE when every error lies in a small known set E. Each sample gives a polynomial equation of degree |E|; linearize and solve. Needs about n^|E| samples.
solves: [learning-with-errors]
model: word-ram
complexity:
  vars: {n: the LWE dimension, D: the size of the error set E, N: "the number of unknowns, C(n + D, D) - 1", q: the prime modulus}
  time: {worst: "O(N^3)"}
  space: {extra: "O(N^2)"}
properties: {deterministic: true, exact: true}
history:
  year: 2011
  people: [Sanjeev Arora, Rong Ge]
  note: Published at ICALP 2011 as a subexponential algorithm for LWE with small Gaussian noise and a polynomial-time one for errors from a set of constant size.
prereqs: [learning-with-errors, gaussian-elimination-modular]
see_also: [xl-algorithm, groebner-basis, macaulay-matrix, bkw-algorithm, learning-with-rounding, learning-parity-with-noise, core-svp-hardness, regev-lwe-hardness]
sources:
  - paper: "Sanjeev Arora and Rong Ge, New algorithms for learning in presence of errors, ICALP 2011, LNCS 6755, pages 403 to 415"
    locator: the linearization of the equations P(b - <a, s>) = 0, the number of samples of order n^D, and the bound 2^(O~(n^(2 epsilon))) for Gaussian noise of width n^epsilon
  - paper: "Martin R. Albrecht, Carlos Cid, Jean-Charles Faugere, Robert Fitzpatrick and Ludovic Perret, Algebraic algorithms for LWE problems, ACM Communications in Computer Algebra 49(2), 2015 (IACR ePrint 2014/1018)"
    locator: the Groebner basis version of the attack, which trades fewer samples for more time under a regularity assumption
  - paper: "Matthias Johann Steiner, The complexity of algebraic algorithms for LWE, EUROCRYPT 2024"
    locator: proven bounds on the degree reached by Groebner basis algorithms on Arora-Ge systems
  - paper: "Daniele Micciancio and Chris Peikert, Hardness of SIS and LWE with small parameters, CRYPTO 2013, LNCS 8042"
    locator: the hardness of LWE with binary errors when the number of samples is only slightly above n, which shows why the attack needs many samples
---

The Arora-Ge algorithm solves [learning with errors](/learning-with-errors/) when every error lies in a small known set $E$. Each sample $(a, b)$ then satisfies the polynomial equation $P(b - \langle a, s \rangle) = 0$ with $P(t) = \prod_{e \in E}(t - e)$. Arora and Ge (2011) treat each monomial in $s$ as a new unknown, so the equations become linear, and solve them by [Gaussian elimination](/gaussian-elimination-modular/) once there are about $n^{|E|}$ samples. For Gaussian errors of width $n^\varepsilon$ with $\varepsilon < 1/2$ this gives time $2^{\tilde O(n^{2\varepsilon})}$, which is why reductions such as Regev's need width at least $\sqrt{n}$.

**Notation.** $n$ is the dimension of the secret $s \in \mathbb{Z}_q^n$, $q$ a prime modulus (not a number of queries), $E \subset \mathbb{Z}_q$ the set of possible errors and $D = |E|$. $P(t) = \prod_{e \in E}(t - e) = \sum_{j=0}^{D} p_j t^j$. A monomial is $s^\alpha = \prod_i s_i^{\alpha_i}$ with exponent vector $\alpha \in \mathbb{N}^n$ and degree $|\alpha| = \sum_i \alpha_i$; $M$ is the set of $\alpha$ with $1 \le |\alpha| \le D$, and $N = |M| = \binom{n+D}{D} - 1$. $N'$ is the number of samples used. $\tilde O$ hides factors polylogarithmic in $n$.

## In plain words

Each noisy equation hides its true value behind a small error. If the error can only be one of a few known values, then the equation must be true for one of those few values. We can write "one of these few cases is true" as a single larger equation, where the few cases are multiplied together.

The larger equation is no longer simple: it contains products of the unknowns. The trick is to give each product its own new name and to pretend it is a separate unknown. Then each sample gives one simple equation in many unknowns. With enough samples, there are as many good equations as unknowns, and ordinary elimination solves them. The answers for the simple unknowns are the secret.

## The problem

The input is $N'$ samples $(a_k, b_k) \in \mathbb{Z}_q^n \times \mathbb{Z}_q$ with $b_k = \langle a_k, s \rangle + e_k$, where the $a_k$ are uniform and every $e_k$ lies in the known set $E$. The output is $s$. This is search LWE with a bounded error and many samples. For a Gaussian error, $E$ is an interval $\{-T, \ldots, T\}$ with $T$ large enough that all $N'$ errors fall in it with high probability.

## The algorithm

```pseudo id=main
ARORA-GE((a_1, b_1), ..., (a_N', b_N'), E, q)
L1  P(t) ← ∏_{e ∈ E} (t − e)
L2  M ← all exponent vectors α with 1 ≤ |α| ≤ |E|
L3  for k ← 1 to N' do
L4      expand P(b_k − ⟨a_k, s⟩) as c_{k,0} + Σ_{α ∈ M} c_{k,α} s^α
L5      add the linear equation Σ_{α ∈ M} c_{k,α} y_α = −c_{k,0}
L6  solve the system in the unknowns y_α mod q by Gaussian elimination
L7  if the solution is not unique then return FAIL
L8  return s = (y_{e_1}, ..., y_{e_n})              ▷ e_i is the i-th unit vector
```

Line L4 uses two expansions. With $L = \langle a, s \rangle$, the binomial theorem gives $P(b - L) = \sum_{t=0}^{D} c_t L^t$ with $c_t = (-1)^t \sum_{j \ge t} p_j \binom{j}{t} b^{j-t}$. The multinomial theorem gives the coefficient of $s^\alpha$ in $L^t$ as $\frac{t!}{\prod_i \alpha_i!} \prod_i a_i^{\alpha_i}$. So $c_{k,\alpha} = c_{|\alpha|} \cdot \frac{|\alpha|!}{\prod_i \alpha_i!} \prod_i a_{k,i}^{\alpha_i}$. Line L6 treats the $y_\alpha$ as independent unknowns, which is the linearization step. The true values $y_\alpha = s^\alpha$ solve every equation, so a unique solution must be these values.

## Example

Take $q = 31$, $n = 2$, $E = \{-1, 0, 1\}$, so $P(t) = t^3 - t$ and $D = 3$. The unknowns are the $N = 9$ monomials $s_1, s_2, s_1^2, s_1 s_2, s_2^2, s_1^3, s_1^2 s_2, s_1 s_2^2, s_2^3$. The secret is $s = (5, 12)$.

**One equation.** The sample $a = (3, 7)$ with error $1$ has $b = 15 + 84 + 1 = 100 \equiv 7$. With $L = 3s_1 + 7s_2$,

$$P(7 - L) = (7^3 - 7) - (3 \cdot 7^2 - 1) L + 3 \cdot 7 \cdot L^2 - L^3.$$

Mod 31, $c_0 = 336 \equiv 26$, $c_1 = -146 \equiv 9$, $c_2 = 21$ and $c_3 = -1$. Expanding the powers of $L$ gives the linear equation

$$27 y_{s_1} + y_{s_2} + 3 y_{s_1^2} + 14 y_{s_1 s_2} + 6 y_{s_2^2} + 4 y_{s_1^3} + 28 y_{s_1^2 s_2} + 24 y_{s_1 s_2^2} + 29 y_{s_2^3} \equiv 5.$$

For instance, the coefficient of $s_1 s_2$ is $c_2 \cdot 2 \cdot 3 \cdot 7 = 882 \equiv 14$, and the right side is $-c_0 \equiv 5$.

**The system.** The code with this page draws 12 samples with errors in $E$; the first nine are $(7,18; 4)$, $(4,11; 29)$, $(15,20; 6)$, $(2,19; 20)$, $(29,26; 23)$, $(8,17; 26)$, $(6,22; 15)$, $(17,26; 26)$ and $(15,12; 3)$, written as $(a_1, a_2; b)$. With the first eight samples there are fewer equations than unknowns, and line L7 returns FAIL. With the first nine, the matrix has rank 9 and Gaussian elimination gives

$$y = (5, 12, 25, 29, 20, 1, 21, 7, 23).$$

These are exactly $s_1, s_2, s_1^2, s_1 s_2, s_2^2, s_1^3, s_1^2 s_2, s_1 s_2^2, s_2^3$ mod 31 for $s = (5, 12)$; for example $s_2^3 = 1728 = 55 \cdot 31 + 23$. Line L8 returns $(5, 12)$.

## Correctness

If every error lies in $E$, then $P(b_k - \langle a_k, s \rangle) = P(e_k) = 0$, so the vector of true monomial values $y^\star = (s^\alpha)$ solves every equation of line L5. If the system has rank $N$, its solution is unique and equals $y^\star$, and its degree-1 entries are $s$. If the rank is lower, line L7 returns FAIL. So the algorithm never returns a wrong secret when the promise on the errors holds. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Unknowns.** $N = \binom{n+D}{D} - 1$, which is about $n^D / D!$ for $n$ much larger than $D$. For $n = 4$ and $D = 3$, $N = 34$.
- **Samples.** At least $N$ samples, since each gives one equation; a few more make full rank likely. Arora and Ge show that a number of order $n^D$ suffices.
- **Time.** Building the rows costs $O(N' N D)$ operations mod $q$. Gaussian elimination on an $N' \times N$ system costs $O(N' N^2)$, so $O(N^3)$ for $N' = O(N)$, or $O(N^\omega)$ with fast matrix multiplication. Space is $O(N' N)$.
- **Gaussian errors.** For errors of width $\sigma$, an interval of half-width $T = O(\sigma \sqrt{\log N'})$ catches all $N'$ errors with high probability, so $D = 2T + 1$. Since $N' \approx n^D$, this needs $D = \tilde O(\sigma^2)$, and the cost $n^{O(D)}$ becomes $2^{\tilde O(\sigma^2)}$. For $\sigma = n^\varepsilon$ this is $2^{\tilde O(n^{2\varepsilon})}$: subexponential when $\varepsilon < 1/2$.
- **At the size of real schemes.** For an LWE dimension of 512 with errors in $\{-3, \ldots, 3\}$, the case of the Kyber512 public key, $N \approx 2^{50.8}$; the attack needs about that many samples and some $2^{150}$ operations, while the scheme gives an attacker only a few hundred samples per key.

## Properties

- **Exact.** Under the promise on the errors, the output is $s$ or FAIL, never a wrong secret.
- **Deterministic.** Given the samples, the algorithm makes no random choices.
- **Sample-hungry.** It needs about $n^D$ samples. With only $O(n)$ samples it does not apply.
- **No lattice reduction.** It uses only linear algebra over $\mathbb{Z}_q$, and its cost does not depend on $q$ beyond the cost of arithmetic.

## Variants and improvements

- **Binary errors.** For $E = \{0, 1\}$, $D = 2$ and $N \approx n^2/2$, so the attack runs in polynomial time with about $n^2$ samples. Micciancio and Peikert (2013) proved that binary-error LWE stays hard when the number of samples is only slightly above $n$, so the sample count is the dividing line.
- **Gröbner bases.** Albrecht, Cid, Faugère, Fitzpatrick and Perret (2015) replace linearization by [Gröbner basis](/groebner-basis/) algorithms such as F4 and F5, which work with a [Macaulay matrix](/macaulay-matrix/) of a chosen degree. They can use fewer samples at a higher cost, under an assumption that the system behaves like a semi-regular one. Steiner (2024) proved bounds on the degree these algorithms reach on Arora-Ge systems.
- **XL.** Multiplying the equations by monomials before linearizing, as in the [XL algorithm](/xl-algorithm/), is another way to use fewer samples.
- **Learning with rounding and LPN.** The same idea applies when the hidden error takes few values, as in [LWR](/learning-with-rounding/) with a small ratio $q/p$ and in [LPN](/learning-parity-with-noise/) over $\mathbb{F}_2$, where the field equations $s_i^2 = s_i$ must be added.

## When to use it

Use it when the error set is very small and the attacker has many samples, for example when a scheme publishes far more LWE samples than its analysis assumes, or uses binary errors with a quadratic number of samples. For schemes such as ML-KEM, with a limited number of samples and errors in $\{-3, \ldots, 3\}$ or $\{-2, \ldots, 2\}$, it is far more expensive than the lattice attacks counted in the [core-SVP](/core-svp-hardness/) model.

## Pitfalls

- **An error outside $E$.** One sample with an error outside $E$ breaks Lemma 2 of the proof. The system then becomes inconsistent, or worse, has a wrong unique solution. With Gaussian errors, choose $T$ so that the chance of any outlier among all $N'$ samples is small.
- **Small $q$.** If $q \le D$, then $s_i^q = s_i$ in $\mathbb{Z}_q$, so some monomials coincide as functions and the system cannot have full rank. Reduce the exponents with the field equations $s_i^q = s_i$ first, as for LPN.
- **Too few samples.** With $N' < N$ the solution is never unique. A random system of $N$ equations may also miss full rank by chance; a few extra samples fix this.
- **Repeated values in $E$.** Count each error value once; a repeated root raises the degree for no gain.

The Python code with this page implements the attack for any small $E$ and checks it on 500 random toy instances with $n = 3$ or $4$, $E = \{-1, 0, 1\}$ and $q \in \{31, 101\}$. It is for study only, is not constant time, and runs only on toy parameters. To protect data use ML-KEM from a FIPS 140 validated module or a maintained library.

## Implementations

## History

Arora and Ge presented the algorithm at ICALP 2011 under the title "New algorithms for learning in presence of errors". They studied it as a learning-theory result: LWE and the related problem of learning parities with structured noise become easier when the noise has a known structure. The result also explained why the error width in hardness reductions for LWE must be at least about $\sqrt{n}$. Albrecht, Cid, Faugère, Fitzpatrick and Perret gave the Gröbner basis version in 2014 and 2015, and the attack is part of the lattice estimator of Albrecht, Player and Scott.

## References
