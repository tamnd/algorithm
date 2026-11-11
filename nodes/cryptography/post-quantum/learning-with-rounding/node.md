---
tag: DNQHCE
kind: problem
slug: learning-with-rounding
name: Learning with rounding
aliases:
- LWR
area: cryptography/post-quantum
level: advanced
summary: LWE with deterministic rounding instead of random noise. Given a and round((p/q) <a, s>) mod p, find s or tell from uniform. Banerjee, Peikert and Rosen 2012. Saber uses its module form.
prereqs: [learning-with-errors]
see_also: [module-learning-with-errors, ring-learning-with-errors, saber, pseudorandom-function, core-svp-hardness, arora-ge-algorithm, crystals-kyber, regev-lwe-hardness]
sources:
  - paper: "Abhishek Banerjee, Chris Peikert and Alon Rosen, Pseudorandom functions and lattices, EUROCRYPT 2012, LNCS 7237"
    locator: the definition of LWR, the reduction from LWE for a superpolynomial ratio q/p, and the PRF constructions (the direct construction and the synthesizer-based one)
  - paper: "Joel Alwen, Stephan Krenn, Krzysztof Pietrzak and Daniel Wichs, Learning with rounding, revisited, new reduction, properties and applications, CRYPTO 2013, LNCS 8042"
    locator: the reduction from LWE to LWR with a polynomial modulus for a number of samples fixed in advance
  - paper: "Andrej Bogdanov, Siyao Guo, Daniel Masny, Silas Richelson and Alon Rosen, On the hardness of learning with rounding over small modulus, TCC 2016-A, LNCS 9562"
    locator: the reductions with a smaller modulus based on the Renyi divergence, for a bounded number of samples
  - url: "https://www.esat.kuleuven.be/cosic/pqcrypto/saber/"
    title: Jan-Pieter D'Anvers, Angshuman Karmakar, Sujoy Sinha Roy, Frederik Vercauteren and others, SABER, Mod-LWR based KEM, NIST round 3 submission, 2020
    locator: the Module-LWR problem and the parameter sets (q = 2^13, p = 2^10, ranks 2, 3 and 4)
---

Learning with rounding (LWR) is the problem of finding a secret $s \in \mathbb{Z}_q^n$, or of telling samples from uniform, given random $a \in \mathbb{Z}_q^n$ and the rounded value $\lfloor (p/q) \langle a, s \rangle \rceil \bmod p$ for a smaller modulus $p < q$. Banerjee, Peikert and Rosen (BPR, 2012) introduced it as a deterministic version of [learning with errors](/learning-with-errors/): the rounding plays the role of the random error. It gives [pseudorandom functions](/pseudorandom-function/) and schemes that need no noise sampling, such as [Saber](/saber/), which uses its module form.

**Notation.** $n$ is the dimension, $q > p \ge 2$ are the two moduli (not numbers of queries), $m$ the number of samples, and $B$ a bound on the LWE error. $\lfloor x \rceil$ is the nearest integer to $x$ (halves round up), and $\lfloor x \rceil_p = \lfloor (p/q) x \rceil \bmod p$ for $x \in \mathbb{Z}_q$. $\lambda$ is the security parameter and $\mathcal{A}$ an adversary. Security statements are in the standard model.

## In plain words

Learning with errors hides a secret by adding a small random error to each equation. Learning with rounding hides it in a different way: it computes the exact answer and then throws away its lowest digits. Only the leading digits are published.

The lost digits act like an error, but no random numbers are needed: the same equation always gives the same published value. This makes the problem useful for functions that must give the same output each time, and it saves the cost of drawing random errors. The price is that the hiding error is not random, and the proofs that the problem is hard are weaker than for the version with random errors.

## Definition

Fix $n$, $q > p \ge 2$. For $s \in \mathbb{Z}_q^n$, the LWR distribution draws $a \in \mathbb{Z}_q^n$ uniformly and outputs

$$\bigl(a,\; b = \lfloor \tfrac{p}{q} \langle a, s \rangle \rceil \bmod p\bigr) \in \mathbb{Z}_q^n \times \mathbb{Z}_p.$$

**Search LWR$_{n,q,p}$:** given $m$ samples, find $s$. **Decision LWR$_{n,q,p}$:** tell $m$ samples for a uniform $s$ from $m$ pairs $(a, u)$ with $u$ uniform in $\mathbb{Z}_p$. The advantage of $\mathcal{A}$ is the difference of its acceptance probabilities in the two cases; the LWR assumption says it is negligible for every adversary that runs in time polynomial in $\lambda$.

**The hidden error.** Write $\langle a, s \rangle = (q/p)\, b + e$ over the reals. Then $e$ lies in $(-q/(2p), q/(2p)]$, so $(q/p) b$ is an LWE-like value with an error of size at most $q/(2p)$. Unlike in LWE, $e$ is a function of $a$ and $s$.

**Condition on $p$.** When $p$ divides $q$, rounding maps the uniform distribution on $\mathbb{Z}_q$ to the uniform distribution on $\mathbb{Z}_p$. When it does not, some values of $\mathbb{Z}_p$ are hit $\lceil q/p \rceil$ times and others $\lfloor q/p \rfloor$ times, so even rounded uniform values are biased; schemes therefore take $q$ and $p$ as powers of 2.

## Variants

- **Ring-LWR and Module-LWR.** The secret and the samples live in a polynomial ring or a module over it, with rounding coefficient by coefficient; [Saber](/saber/) uses Module-LWR over $\mathbb{Z}_q[x]/(x^{256} + 1)$ with $q = 2^{13}$, $p = 2^{10}$ and ranks 2, 3 and 4.
- **Rounding in LWE schemes.** ML-KEM compresses its ciphertexts and the Kyber round 3 analysis counts the rounding as extra noise (LWE plus LWR); see [CRYSTALS-Kyber](/crystals-kyber/) and [core-SVP hardness](/core-svp-hardness/).
- **Bounded samples.** Several hardness results hold only for a number of samples $m$ fixed before $q$ is chosen.

## Examples

**Small rounding.** With $q = 16$ and $p = 4$, $\lfloor x \rceil_4 = \lfloor x/4 \rceil \bmod 4$ maps $0, 1, \ldots, 15$ to $0,0,1,1,1,1,2,2,2,2,3,3,3,3,0,0$. Each value of $\mathbb{Z}_4$ is hit 4 times, because $4$ divides $16$.

**A toy instance.** Take $n = 3$, $q = 64$, $p = 8$ and $s = (5, 17, 40)$.

| $a$ | $\langle a, s \rangle \bmod 64$ | $(p/q) \langle a, s \rangle$ | $b$ |
|---|---|---|---|
| $(3, 60, 12)$ | 43 | 5.375 | 5 |
| $(33, 8, 51)$ | 37 | 4.625 | 5 |
| $(20, 2, 9)$ | 46 | 5.75 | 6 |
| $(47, 31, 6)$ | 42 | 5.25 | 5 |

Each $b$ hides the low 3 bits of a 6-bit value, so the hidden error has size at most $q/(2p) = 4$.

**Rounded LWE agrees with LWR.** If $|e| \le B$, then $\lfloor \langle a, s \rangle + e \rceil_p = \lfloor \langle a, s \rangle \rceil_p$ unless $\langle a, s \rangle$ lies within $B$ of a rounding boundary, which for uniform $a$ has probability at most $2Bp/q$. For $q = 2^{16}$, $p = 2^4$, $B = 2$ and 2000 samples, the expected number of disagreements is at most about 2; for $q = 2^6$, more than a tenth of the samples disagree.

**Non-example.** If $p = q$, rounding changes nothing, the samples are noiseless linear equations, and [Gaussian elimination](/gaussian-elimination-modular/) finds $s$ from $n$ independent samples.

## Known algorithms

- **As LWE.** Multiply $b$ by $q/p$: the result is $\langle a, s \rangle$ plus an error of size at most $q/(2p)$, roughly uniform. The primal and dual lattice attacks then apply, with costs estimated in the [core-SVP](/core-svp-hardness/) model; this is how Saber's parameters were chosen.
- **Algebraic attacks.** The error takes at most about $q/p$ values, so with enough samples the [Arora-Ge](/arora-ge-algorithm/) linearization applies when $q/p$ is small.
- **Combinatorial attacks.** [BKW](/bkw-algorithm/) applies with many samples, as for LWE.

The Python code with this page samples LWR, rounds LWE samples, and evaluates the toy direct PRF of BPR. It is for study only, uses parameters far too small for security, and is not constant time. For a real pseudorandom function use HMAC or KMAC from a FIPS 140 validated module or a standard library.

## Bounds

- **Superpolynomial ratio (BPR 2012).** If $q/p \ge B \cdot n^{\omega(1)}$, where $B$ bounds the LWE error, then decision LWR$_{n,q,p}$ is at least as hard as decision LWE$_{n,q,\chi}$, for any polynomial number of samples. The reduction rounds LWE samples: for uniform $a$, $\lfloor \langle a, s \rangle + e \rceil_p$ equals $\lfloor \langle a, s \rangle \rceil_p$ except with probability at most $2Bp/q$, which is negligible here, while rounded uniform values stay uniform when $p \mid q$.
- **Polynomial modulus with bounded samples (Alwen, Krenn, Pietrzak and Wichs 2013).** For a number of samples $m$ fixed in advance, LWR stays as hard as LWE with a polynomial modulus $q$ that grows with $m$, $B$ and $p$, at some loss in the parameters.
- **Smaller modulus (Bogdanov, Guo, Masny, Richelson and Rosen 2016).** Arguments with the Rényi divergence instead of the statistical distance reduce the modulus that the reduction needs for a bounded number of samples.
- **No unconditional result** is known for the parameters of Saber; its security, like that of ML-KEM, comes from attack estimates.

## Reductions

- **From LWE.** As above, in the three regimes of the Bounds section.
- **To LWE-like lattice problems.** LWR samples scaled by $q/p$ form a BDD instance on the same $q$-ary lattice as LWE, with a deterministic bounded error.

## Applications

- **Pseudorandom functions.** The BPR direct construction is $F(x) = \lfloor a^{\mathsf T} \prod_{i=1}^{k} S_i^{x_i} \rceil_p$ for $x \in \{0,1\}^k$, with $a$ uniform in $\mathbb{Z}_q^n$ and short square matrices $S_i$. Its security proof needs a very large $q$. BPR also give a construction from a synthesizer, $S(a, b) = \lfloor a \cdot b \rceil_p$ on matrices, in a tree of depth $\log k$.
- **Key encapsulation without noise sampling.** [Saber](/saber/) (Module-LWR) was a NIST round 3 finalist. Its rounding is a shift of the coefficients, which is cheap and needs no random error.

## References
