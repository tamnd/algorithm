---
tag: T7TCT3
kind: problem
slug: syndrome-decoding-problem
name: Syndrome decoding problem
aliases:
- SD problem
- decoding random linear codes
area: cryptography/post-quantum
level: advanced
summary: Given a parity check matrix H, a syndrome s and a weight w, find e of weight w with He = s. NP-complete in the worst case (1978), and the hard problem under code-based cryptography.
prereqs: [linear-code, parity-check-matrix, syndrome, hamming-weight, code-based-cryptography]
see_also: [information-set-decoding, nearest-codeword-problem, gilbert-varshamov-bound, mceliece-cryptosystem, learning-parity-with-noise, np-complete, syndrome-decoding, decision-problem]
sources:
  - paper: "Elwyn R. Berlekamp, Robert J. McEliece and Henk C. A. van Tilborg, On the inherent intractability of certain coding problems, IEEE Transactions on Information Theory 24(3), pages 384 to 386, 1978"
    locator: the whole paper (the problems Coset Weights and Subspace Weights, and their NP-completeness by a reduction from three-dimensional matching)
  - paper: "Jean-Bernard Fischer and Jacques Stern, An efficient pseudo-random generator provably as secure as syndrome decoding, Eurocrypt 1996, LNCS 1070, pages 245 to 255"
    locator: the main theorem (a search to decision reduction for syndrome decoding with random matrices)
  - paper: "Alexander Vardy, The intractability of computing the minimum distance of a code, IEEE Transactions on Information Theory 43(6), pages 1757 to 1766, 1997"
    locator: the whole paper (the minimum distance problem is NP-hard)
  - paper: "Matthieu Finiasz and Nicolas Sendrier, Security bounds for the design of code-based cryptosystems, Asiacrypt 2009, LNCS 5912, pages 88 to 105"
    locator: Section 2 (the syndrome decoding problem as the base of code-based schemes, and the number of solutions near the Gilbert-Varshamov distance)
  - paper: "Jacques Stern, A new identification scheme based on syndrome decoding, Crypto 1993, LNCS 773, pages 13 to 21"
    locator: the whole paper (a zero-knowledge identification scheme whose security rests on syndrome decoding)
  - paper: "Ghazal Kachigar and Jean-Pierre Tillich, Quantum information set decoding algorithms, PQCrypto 2017, LNCS 10346, pages 69 to 89"
    locator: the introduction, Table 1 (classical and quantum exponents for decoding at the Gilbert-Varshamov distance)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Code-based cryptography by Raphael Overbeck and Nicolas Sendrier (the decoding problems, their hardness, and the indistinguishability assumption for Goppa codes)
---

The syndrome decoding problem (SD) asks for a vector of a given small weight $w$ whose [syndrome](/syndrome/) under a given [parity check matrix](/parity-check-matrix/) $H$ is a given vector $s$: find $e$ with $He = s$ and $\mathrm{wt}(e) = w$. It is the same as finding the error in a noisy codeword of a [linear code](/linear-code/), because $H(c + e) = He$ for every codeword $c$. Berlekamp, McEliece and van Tilborg proved in 1978 that the decision version is [NP-complete](/np-complete/). For random codes, the best known algorithms, [information set decoding](/information-set-decoding/), take time exponential in $w$ even on a quantum computer. That is why SD is the hard problem under [code-based cryptography](/code-based-cryptography/): the [McEliece](/mceliece-cryptosystem/), Niederreiter, BIKE and HQC schemes are secure only if SD is hard for their codes.

**Notation.** All vectors and matrices are over $\mathbb{F}_2$. The code has length $n$, dimension $k$, rate $R = k/n$, and $r = n - k$. $H \in \mathbb{F}_2^{r \times n}$, $s \in \mathbb{F}_2^r$, and $\mathrm{wt}(x)$ is the [Hamming weight](/hamming-weight/). $S_w$ is the set of vectors of weight $w$ in $\mathbb{F}_2^n$, and $H_2$ is the binary entropy function. $\lambda$ is the security parameter, and $n$, $k$ and $w$ grow with it. $\mathcal{A}$ is an adversary and $\mathrm{Adv}$ its advantage. The statements are in the standard model, with no random oracle.

## In plain words

A string of bits passes through a noisy line, and a few bits flip. The receiver checks the string against a fixed set of parity rules. The pattern of broken rules, the syndrome, depends only on which bits flipped, not on the message.

The problem is to go back from the pattern of broken rules to the flipped bits, when you know that only a few bits flipped. For special codes, such as Goppa or Reed-Solomon codes, there are fast methods. For a code that looks random, no fast method is known: the only general way is to search, and the search grows exponentially with the number of flipped bits.

Code-based cryptography hides the fast method. The owner knows that the code is special, and everyone else sees a code that looks random.

## Definition

**Search SD.** Given $H \in \mathbb{F}_2^{r \times n}$, $s \in \mathbb{F}_2^{r}$ and an integer $w$, find $e \in \mathbb{F}_2^n$ with $He = s$ and $\mathrm{wt}(e) = w$ (some authors ask for $\mathrm{wt}(e) \le w$).

**Decision SD (worst case).** Given $H$, $s$ and $w$, decide whether some $e$ with $\mathrm{wt}(e) \le w$ satisfies $He = s$. Berlekamp, McEliece and van Tilborg call this problem *Coset Weights* (they state it with the generator matrix form $xA = y$, which is the same problem with $A = H^T$).

**Average case SD, the form used in cryptography.** The instance is random: $H$ is uniform in $\mathbb{F}_2^{r \times n}$, $e^\ast$ is uniform in $S_w$, and $s = He^\ast$. The advantage of an adversary $\mathcal{A}$ against search SD is

$$\mathrm{Adv}^{\mathrm{SD}}_{n,k,w}(\mathcal{A}) = \Pr\left[He' = s \text{ and } \mathrm{wt}(e') = w \;:\; e' \leftarrow \mathcal{A}(H, s)\right],$$

and the advantage against *decision SD* is the distinguishing advantage

$$\left| \Pr[\mathcal{A}(H, He^\ast) = 1] - \Pr[\mathcal{A}(H, u) = 1] \right|,$$

with $u$ uniform in $\mathbb{F}_2^r$. The SD assumption says that every probabilistic polynomial time $\mathcal{A}$ has a negligible advantage in $\lambda$, for the parameters $n(\lambda)$, $k(\lambda)$ and $w(\lambda)$ of the scheme.

**The Gilbert-Varshamov distance.** The expected number of solutions of a random instance is about $1 + \binom{n}{w}/2^{r}$: the planted one, plus the vectors of weight $w$ that hit $s$ by chance. The relative [Gilbert-Varshamov distance](/gilbert-varshamov-bound/) $\omega_{GV}$ is the root in $(0, 1/2)$ of $H_2(\omega) = 1 - R$. For $w < \omega_{GV} n$ the planted solution is unique with high probability, and for $w > \omega_{GV} n$ there are exponentially many solutions. The hardest instances for the known algorithms have $w$ near $\omega_{GV} n$.

## Variants

- **Codeword finding (Subspace Weights).** Given $H$ and $w$, find a nonzero codeword of weight $w$. Berlekamp, McEliece and van Tilborg proved the exact weight version NP-complete. Vardy (1997) proved that computing the minimum distance is NP-hard.
- **Decoding with a generator matrix.** Given $G \in \mathbb{F}_2^{k \times n}$ and $y = mG + e$, find $m$ and $e$. A parity check matrix of the code turns it into SD with $s = Hy^T$.
- **Quasi-cyclic SD.** $H$ is made of circulant blocks, as in [BIKE](/bike/) and [HQC](/hqc/). No reduction is known from the general problem, so it is a separate assumption.
- **SD over $\mathbb{F}_q$, and in other metrics.** The same problem in larger fields, or with the rank metric. They have their own algorithms and are not covered here.
- **Learning parity with noise.** [LPN](/learning-parity-with-noise/) is decoding of a random code with a Bernoulli noise and an unbounded number of samples, so it is an SD variant in which the attacker can ask for more rows of the code.

## Examples

Take the $[7, 4]$ [Hamming code](/hamming-code/), in which column $j$ of $H$ is the binary form of $j$:

$$H = \begin{pmatrix} 1&0&1&0&1&0&1 \\ 0&1&1&0&0&1&1 \\ 0&0&0&1&1&1&1 \end{pmatrix}, \qquad s = (1, 0, 1)^T, \qquad w = 1 .$$

The answer is the column equal to $s$, which is column 5, so $e = (0,0,0,0,1,0,0)$. For this code every syndrome has a unique solution of weight at most 1, because the Hamming code is perfect. With $w = 2$ the same $s$ has three solutions, $\{1, 4\}$, $\{2, 7\}$ and $\{3, 6\}$, because each pair of columns that adds to $(1,0,1)^T$ gives one.

For the Classic McEliece parameter set mceliece348864 the instance has $n = 3488$, $k = 2720$, $r = 768$ and $w = 64$. Plain search over all $\binom{3488}{64}$ supports is far out of reach, and even [Prange's algorithm](/prange-algorithm/) needs about $2^{142.8}$ rounds.

## Known algorithms

- **Exhaustive search.** Try all $\binom{n}{w}$ supports, or meet in the middle over two halves with about $\binom{n}{w/2}$ work and memory.
- **Information set decoding.** [Prange](/prange-algorithm/) (1962), [Lee-Brickell](/lee-brickell-algorithm/) (1988), [Stern](/stern-algorithm/) (1989), Dumer (1991), MMT (2011), BJMM (2012) and May-Ozerov (2015). At the Gilbert-Varshamov distance and the worst rate, their costs range from $2^{0.1207 n}$ for Prange to $2^{0.0966 n}$ for May-Ozerov. See [information set decoding](/information-set-decoding/) for the table.
- **Quantum algorithms.** [Grover search](/grover-search/) inside Prange gives $2^{0.06035 n}$, and quantum walks give $2^{0.05869 n}$ (Kachigar and Tillich 2017). No quantum algorithm is known that does better than a square root type gain.
- **Structured codes.** If the code has an efficient decoder and the structure is visible, the problem is easy: Reed-Solomon, BCH, Goppa and LDPC codes all have polynomial time decoders up to their design distance. The security of code-based schemes depends on hiding that structure.
- **Large weight.** If $w$ is close to $r/2$, a random solution of $He = s$ found by linear algebra has about the right weight, and the problem is easy.

## Bounds

The worst case decision problem is NP-complete (Berlekamp, McEliece and van Tilborg 1978), so no polynomial time algorithm exists unless P = NP. NP-hardness is a worst case statement, and it does not prove that random instances are hard. The evidence for the average case is the long history of attacks: for random codes the exponent at the Gilbert-Varshamov distance has gone from 0.1207 (1962) to 0.0966 (2015) in more than fifty years. For $w = o(n)$, which is the case of the McEliece schemes, all known ISD variants cost $2^{-w\log_2(1 - R)(1 + o(1))}$, so their gains are in the lower order terms.

## Reductions

- **NP-hardness.** Three-dimensional matching reduces to Coset Weights (Berlekamp, McEliece and van Tilborg 1978).
- **Search to decision.** For random instances, Fischer and Stern (1996) give a reduction from search SD to decision SD, in the style of the Goldreich-Levin theorem. So a distinguisher for $(H, He^\ast)$ against $(H, u)$ yields an algorithm that finds $e^\ast$.
- **SD and codeword finding.** Decoding $s$ with weight $w$ is the same as finding a codeword of weight $w + 1$ that has a 1 in the last position, in the code with parity check matrix $[H \mid s]$.
- **McEliece and Niederreiter.** Recovering the message of a McEliece ciphertext is SD for the public code, and Niederreiter encryption is SD by definition. Breaking them without the key needs either an SD algorithm or a way to tell the public code apart from a random code.

## Applications

- **Public key encryption and KEMs.** [McEliece](/mceliece-cryptosystem/) and Niederreiter (Goppa codes), [BIKE](/bike/) (quasi-cyclic MDPC codes) and [HQC](/hqc/) (quasi-cyclic codes with a public decoder). NIST selected HQC for standardization in March 2025.
- **Identification and signatures.** Stern's zero-knowledge identification scheme (1993) proves knowledge of a solution to an SD instance. With the Fiat-Shamir transform it gives signatures, and newer schemes with this design, such as SDitH, are in the NIST process for additional signatures.
- **Pseudorandom generators and hashing.** Fischer and Stern (1996) build a pseudorandom generator from the decision problem.

## References
