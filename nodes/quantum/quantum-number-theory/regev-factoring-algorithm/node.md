---
tag: GJ2PQ0
kind: algorithm
slug: regev-factoring-algorithm
name: Regev's factoring algorithm
aliases:
- Regev 2023 quantum factoring
area: quantum/quantum-number-theory
level: research
summary: A quantum factoring algorithm that runs a circuit of O(n^(3/2) log n) gates about sqrt(n) times and finds a square root of 1 mod N by lattice reduction. It rests on a number-theoretic heuristic.
solves: [integer-factorization]
model: quantum-circuit-model
complexity:
  vars: {n: "the length of N in binary", d: "the number of small bases, d = sqrt(n)"}
  time: {gates_per_run: O(n^(3/2) log n), runs: sqrt(n) + 4, gates_per_run_schoolbook: O(n^(5/2)), total_gates: O(n^2 log n), classical_postprocessing: poly(n)}
  space: {qubits: O(n^(3/2)), qubits_ragavan_vaikuntanathan: O(n log n)}
properties: {deterministic: false, exact: true, las_vegas: true, quantum: true, heuristic: true}
history:
  year: 2023
  people: [Oded Regev]
  note: Regev posted the algorithm in August 2023; the journal version appeared in the Journal of the ACM in 2025.
prereqs: [shor-algorithm, lll-algorithm, dual-lattice, quantum-fourier-transform, nontrivial-square-root-of-one]
see_also: [ekera-hastad-algorithm, quantum-resource-estimation-factoring, factoring-to-order-finding, quantum-modular-exponentiation, shortest-vector-problem, smooth-number, quadratic-sieve, harvey-van-der-hoeven-multiplication]
sources:
  - paper: arxiv:2308.06572
    title: "Oded Regev, An Efficient Quantum Factoring Algorithm, arXiv:2308.06572 (version 3, January 2024); journal version in Journal of the ACM 72(1), 2025, doi:10.1145/3708471"
    locator: Theorem 1.1, Section 3 (the quantum procedure), Lemma 4.4 and Corollary 4.5, Claim 5.1 and the proof of Theorem 1.1 (numbering of the arXiv version)
  - paper: arxiv:2310.00899
    title: Seyoon Ragavan and Vinod Vaikuntanathan, Space-Efficient and Noise-Robust Quantum Factoring, CRYPTO 2024
    locator: the abstract (O(n log n) qubits, O(n^(3/2) log n) gates, and post-processing that tolerates a constant fraction of corrupted runs)
  - paper: arxiv:2311.05545
    title: "Martin Ekerå and Joel Gärtner, Extending Regev's factoring algorithm to compute discrete logarithms, PQCrypto 2024, LNCS 14772, pages 211-242"
    locator: the extension to discrete logarithms and the analysis of the post-processing
  - paper: doi:10.1007/BF01457454
    title: "Arjen K. Lenstra, Hendrik W. Lenstra Jr. and László Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261:515-534, 1982"
    locator: the reduction algorithm and the bound on the first reduced vector
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: the section on factoring
  - paper: "Jean-Pierre Seifert, Using fewer qubits in Shor's factorization algorithm via simultaneous Diophantine approximation, CT-RSA 2001"
    title: "Jean-Pierre Seifert, Using fewer qubits in Shor's factorization algorithm via simultaneous Diophantine approximation, CT-RSA 2001"
    locator: the idea of several shorter runs with lattice post-processing
  - paper: arxiv:2502.09772
    title: Przemysław Pawlitko, Natalia Moćko, Marcin Niemiec and Piotr Chołda, Implementation and Analysis of Regev's Quantum Factorization Algorithm, 2025
    locator: the simulation results and the comparison with Shor's algorithm on small integers
---

Regev's factoring algorithm is a quantum algorithm that factors an $n$-bit integer $N$ by running a quantum circuit of $O(n^{3/2} \log n)$ gates $\sqrt{n} + 4$ times and then doing polynomial-time classical post-processing. It is a multidimensional form of [Shor's algorithm](/shor-algorithm/): the exponent is a vector of $\sqrt{n}$ small exponents of small primes, and the classical step uses [lattice reduction](/lll-algorithm/) where Shor uses continued fractions. Its correctness rests on a number-theoretic heuristic that is not proved. Each run is cheaper than one run of Shor's circuit, but the total gate count over all runs is about the same.

## In plain words

Shor's method raises one random number to one huge power in superposition. That power is the expensive part. Regev's method instead takes about the square root of $n$ tiny primes and raises each of them to a moderate power. Products of tiny numbers are cheap, and only a few multiplications of large numbers are left.

Each run of the circuit gives a noisy hint about which combinations of the tiny primes multiply to 1 modulo $N$. One hint is not enough. After a few more runs than there are primes, a classical lattice algorithm combines the hints and finds such a combination with small exponents.

From that combination we get a number whose square is 1 modulo $N$. If it is not 1 or $-1$, a greatest common divisor gives a factor. That a good combination with small exponents exists is believed but not proved.

## The problem

Given a composite integer $N$, find a nontrivial factor, as in [integer factorization](/integer-factorization/). Even $N$ and perfect powers are handled classically, so the quantum part can assume that $N$ is odd and not a prime power. Let $b_1, \dots, b_d$ be the first $d$ primes, none of which divides $N$, and $a_i = b_i^2$. The algorithm works with two lattices in $\mathbb{Z}^d$:

$$\mathcal{L} = \Bigl\{ z \in \mathbb{Z}^d : \prod_i a_i^{z_i} \equiv 1 \pmod N \Bigr\}, \qquad \mathcal{L}_0 = \Bigl\{ z \in \mathbb{Z}^d : \prod_i b_i^{z_i} \equiv \pm 1 \pmod N \Bigr\} \subseteq \mathcal{L}.$$

The map $h(z) = \prod_i a_i^{z_i} \bmod N$ is a group homomorphism from $\mathbb{Z}^d$ to the units modulo $N$ with kernel $\mathcal{L}$, so $\det \mathcal{L}$ equals the size of the image of $h$, which is at most $N$. For any $u \in \mathcal{L} \setminus \mathcal{L}_0$, the number $x = \prod_i b_i^{u_i} \bmod N$ is a [nontrivial square root of 1](/nontrivial-square-root-of-one/), and $\gcd(x - 1, N)$ is a factor. The task is to find such a $u$.

**Regev's assumption.** For $d = \sqrt{n}$ there is a vector in $\mathcal{L} \setminus \mathcal{L}_0$ of Euclidean length at most $T = \exp(O(\sqrt{n}))$. By Minkowski's theorem $\mathcal{L}$ has nonzero vectors of length at most $\sqrt{d} \, 2^{n/d}$, and heuristically at least half of the vectors of $\mathcal{L}$ are outside $\mathcal{L}_0$, but no proof is known. The assumption is in the spirit of those about [smooth numbers](/smooth-number/) in subexponential classical factoring.

## The algorithm

The parameters are $d$, a radius $R$ and a power of two $D$ with $2\sqrt{d} R \le D < 4 \sqrt{d} R$. Regev takes $d = \sqrt{n}$ and $R = \exp(C \sqrt{n})$ for a large enough constant $C$. Below, $\rho_R(z) = \exp(-\pi \|z\|^2 / R^2)$ is the Gaussian function, $e_j$ is the $j$-th unit vector, and the QFT is the [quantum Fourier transform](/quantum-fourier-transform/).

```pseudo id=main
REGEV(N, d, D, R)                                ▷ N is composite
L1  if N is even or N = r^k with k ≥ 2 then return 2 or r
L2  b_1, ..., b_d ← the first d primes; if some b_i divides N then return b_i
L3  a_i ← b_i^2 for i = 1, ..., d
L4  for k ← 1 to d + 4 do                        ▷ independent runs of the circuit
L5      prepare the state Σ_z ρ_R(z) |z⟩ over z ∈ {−D/2, ..., D/2 − 1}^d
L6      compute |e⟩ = |Π_i a_i^(z_i + D/2) mod N⟩, squaring once per bit of the exponents
L7      apply the QFT over (Z_D)^d to |z⟩ and measure it; call the result w_k ∈ (Z_D)^d
L8  B ← the basis of L' with columns (e_j ; w_(1,j), ..., w_(d+4,j)) and (0 ; D e_k)
L9  B ← LLL(B)
L10 for each vector of B do u ← its first d coordinates
L11     if u ≠ 0 and Π_i a_i^(u_i) ≡ 1 (mod N) then
L12         x ← Π_i b_i^(u_i) mod N
L13         if x ≢ ±1 (mod N) then return gcd(x − 1, N)
L14 return FAIL                                  ▷ run REGEV again
```

**Line L6.** Let $s_i = z_i + D/2$ and process the bits of all $s_i$ together, from the most significant. Start with $e = 1$. For each bit position $j$, square $e$, then multiply $e$ by the product of the $a_i$ whose $s_i$ has bit $j$ set. The product of the selected $a_i$ is a number of $O(d \log d)$ bits, computed in a binary tree on small numbers. So the only operations on $n$-bit numbers are $\log_2 D$ squarings and $\log_2 D$ multiplications by a small number. This is the source of the saving. The computation is made reversible as on the [quantum modular exponentiation](/quantum-modular-exponentiation/) page; the register $|e\rangle$ is never used again.

**Line L8.** The lattice $\mathcal{L}'$ has dimension $2d + 4$. Regev scales the last $d + 4$ rows by a factor $S$; the choice $S = D$ makes every entry an integer. If $u \in \mathcal{L}$, then every $\langle u, w_k \rangle$ is close to a multiple of $D$, so $\mathcal{L}'$ has a short vector whose first $d$ coordinates are $u$.

**Lines L9 to L13.** LLL finds vectors of $\mathcal{L}'$ that are short up to a factor $2^{O(d)}$. Their first $d$ coordinates are tested for membership in $\mathcal{L}$ and then for $\mathcal{L}_0$. All post-processing uses exact integers.

## Example

Take $N = 77 = 7 \cdot 11$, $d = 2$, $b = (2, 3)$, $a = (4, 9)$, $D = 64$ and $R = 16$, which satisfies $2\sqrt{2} \cdot 16 \le 64 < 4\sqrt{2} \cdot 16$.

The numbers 4 and 9 generate a subgroup of 15 units modulo 77, so $\det \mathcal{L} = 15$. A basis of $\mathcal{L}$ is $(1, -2)$ and $(-6, -3)$: indeed $9^2 = 81 \equiv 4$, so $4 \cdot 9^{-2} \equiv 1$, and the two vectors have determinant $-15$. The vector $(2, -4)$ is in $\mathcal{L}_0$, since $2^2 \cdot 3^{-4} \equiv 1$, but $(1, -2)$ is not.

The simulator computes the exact outcome distribution of lines L5 to L7 and draws $d + 4 = 6$ samples with seed 1:

$$w = (8, 4),\ (54, 29),\ (48, 55),\ (16, 8),\ (31, 46),\ (28, 47).$$

For $u = (1, -2)$ the values $\langle u, w_k \rangle$ reduced to $(-32, 32]$ modulo 64 are $0, -4, 2, 0, 3, -2$, all small. LLL on the $8 \times 8$ basis of line L8 returns, as its first vector, $(1, -2, 0, -4, 2, 0, 3, -2)$: the lift of $u$. Line L11 accepts $u = (1, -2)$. Line L12 gives $x = 2 \cdot 3^{-2} \bmod 77 = 2 \cdot 60 \bmod 77 = 43$, and $43^2 = 1849 = 24 \cdot 77 + 1$. Since $43 \ne \pm 1$, line L13 returns $\gcd(42, 77) = 7$.

**Measured success rates.** In the simulator, with $d = 2$, $D = 64$, $R = 16$ and one attempt for each seed from 0 to 19, the attempt returned a factor for 20 of 20 seeds when $N$ is 35, 55, 65, 77, 91, 143, 187 or 323, and for 18 or 19 of 20 seeds when $N$ is 85, 119, 209, 221 or 247. For $N = 437 = 19 \cdot 23$, where $\det \mathcal{L} = 99$, it succeeded once in 20. The radius must grow with $\det \mathcal{L}$, which is why $R$ grows with $N$ in the theorem.

## Correctness

Three facts make the algorithm work. The full proof is in [proofs/correctness.md](proofs/correctness.md).

**Every answer is right.** Line L13 returns a value only for $u \in \mathcal{L}$ and $x \not\equiv \pm 1$. Then $x^2 = \prod_i a_i^{u_i} \equiv 1$, so $N$ divides $(x - 1)(x + 1)$ but neither factor, and $\gcd(x - 1, N)$ is a nontrivial factor. This holds with no assumption.

**The quantum step samples the dual lattice with Gaussian noise.** Since the register $|e\rangle$ is never used, the $z$ register holds a Gaussian restricted to one coset of $\mathcal{L}$. After the QFT, the outcome $w$ satisfies, for short $u$ and up to error terms that come from the edges of the box and are tiny when $D$ is large compared with $R$,

$$\mathbb{E}\bigl[e^{2\pi i \langle u, w \rangle / D}\bigr] = \begin{cases} e^{-\pi \|u\|^2 / (2R^2)} & \text{if } u \in \mathcal{L}, \\ 0 & \text{if } u \notin \mathcal{L}. \end{cases}$$

So $w/D$ is close to a point of the [dual lattice](/dual-lattice/) $\mathcal{L}^*$ modulo $\mathbb{Z}^d$, which is the multidimensional form of the peaks in Shor's algorithm. Regev shows more: $w/D$ is a uniform coset of $\mathcal{L}^*/\mathbb{Z}^d$ plus noise of length about $\sqrt{d}/R$.

**Lattice reduction recovers $\mathcal{L}$.** With $d + 4$ samples, with probability at least $1/4$ the samples generate $\mathcal{L}^*/\mathbb{Z}^d$ well enough that every short vector of $\mathcal{L}'$ has its first $d$ coordinates in $\mathcal{L}$ (Regev's Lemma 4.4). LLL returns vectors of length at most $2^{O(d)} T$ that generate every vector of $\mathcal{L}'$ of length at most $T$. Under the assumption, one of them comes from $u \in \mathcal{L} \setminus \mathcal{L}_0$, as long as $R > 2^{d + n/d} T$. With $d = \sqrt{n}$ this holds for $R = \exp(C\sqrt{n})$.

## Complexity

The quantum bounds are in the [quantum circuit model](/quantum-circuit-model/); gate counts are for one run.

- **Gates per run.** Line L6 does $\log_2 D = O(\sqrt{n})$ squarings of $n$-bit numbers. With [fast multiplication](/harvey-van-der-hoeven-multiplication/) each costs $O(n \log n)$, so line L6 costs $O(n^{3/2} \log n)$. The products of small numbers add $O(\log D \cdot d \log^3 d)$, line L5 costs $d(\log D + \mathrm{poly}(\log d))$, and the approximate QFT costs $O(d \log D \cdot (\log \log D + \log d))$. In total, $O(n^{3/2} \log n)$, against $O(n^2 \log n \log\log n)$ for one run of Shor's algorithm with fast multiplication.
- **With schoolbook arithmetic.** Fast multiplication does not pay at RSA sizes. With schoolbook squaring, one run costs about $n^{5/2}$ gates, against about $n^3$ for Shor.
- **Runs.** $d + 4 = \sqrt{n} + 4$ runs per attempt. The total over all runs is $O(n^2 \log n)$ gates, about the same as one run of Shor's circuit.
- **Qubits.** The exponent register has $d \log_2 D = O(n)$ qubits, but the reversible repeated squaring keeps about $\sqrt{n}$ intermediate $n$-bit values, so the circuit uses $O(n^{3/2})$ qubits, against $O(n)$ for Shor.
- **Depth.** Regev notes that the depth is smaller than in Shor's original circuit by a factor of about $\sqrt{n}$, up to logarithmic factors.
- **Classical work.** LLL in dimension $2d + 4$ with entries of $O(\sqrt{n})$ bits runs in polynomial time.

## Properties

- **Las Vegas.** A returned value is always a nontrivial factor; only the chance of success depends on the heuristic.
- **Heuristic.** The success bound needs Regev's assumption on short vectors in $\mathcal{L} \setminus \mathcal{L}_0$. Shor's algorithm needs no such assumption.
- **Independent runs.** The $d + 4$ runs share no quantum state, so they can run on different machines or one after another.
- **Small bases.** The bases are fixed small primes, not random residues; the randomness is in the quantum measurement only.
- **Asymptotic.** The saving is in the exponent of $n$. Regev states that the hidden constants may make the algorithm worse than Shor's at sizes such as 2048 bits.

## Variants and improvements

- **Ragavan and Vaikuntanathan (2024).** Exponentiation with Fibonacci numbers in the exponent, adapted from a classical idea of Kaliski, cuts the space to $O(n \log n)$ qubits while keeping $O(n^{3/2} \log n)$ gates per run. Their post-processing uses lattice reduction to detect and discard corrupted runs, so it still works when a constant fraction of the runs are wrong.
- **Ekerå and Gärtner (2024).** The same multidimensional idea computes discrete logarithms and orders, with an analysis of how many runs the post-processing really needs.
- **Larger dimension.** With $d = n^{1/2 + \varepsilon}$ and $R = \exp(C n^{1/2 - \varepsilon})$, each run costs $\tilde{O}(n^{3/2 - \varepsilon})$ gates and there are $n^{1/2 + \varepsilon}$ runs, but the post-processing must solve a hard lattice problem in time $\exp(\tilde{O}(n^{2\varepsilon}))$. If lattice problems were classically easy, circuits of size $\tilde{O}(n)$ would factor.
- **Better reduction in practice.** [BKZ](/bkz-algorithm/) and other reductions find much shorter vectors than the worst-case LLL bound, so a smaller $R$, and smaller circuits, may work in practice.

## When to use it

Regev's algorithm matters as a result about circuit size. Today it is a research subject, not a practical choice: for RSA-sized moduli, the most detailed cost estimates are for optimized forms of Shor's algorithm and the [Ekerå-Håstad algorithm](/ekera-hastad-algorithm/); see [quantum resource estimation for factoring](/quantum-resource-estimation-factoring/). Consider it when the cost that matters is the size or depth of one run, not the total gate count or the qubit count, and when the error rate allows many independent short runs.

## Pitfalls

- **An unproved assumption.** The algorithm is heuristic. A proof that it factors needs the short-vector assumption on $\mathcal{L} \setminus \mathcal{L}_0$.
- **Small bases that divide $N$.** If some $b_i$ divides $N$, $a_i$ is not a unit and $\mathcal{L}$ is not defined; line L2 must test this first.
- **Too small a radius.** If $R$ is small compared with the lengths of the vectors of $\mathcal{L}$, the outcomes carry almost no information and LLL returns vectors outside $\mathcal{L}$. Line L11 then rejects every vector. The measured rates above show this effect for $N = 437$.
- **Floating-point post-processing.** The lattice of line L8 has entries of $O(\sqrt{n})$ bits and dimension $2d + 4$. Run LLL in exact or carefully bounded arithmetic, and test membership in $\mathcal{L}$ exactly, as in line L11.
- **Counting gates.** The saving is per run. The total number of gates over all runs is not smaller than for Shor's algorithm, and the qubit count is larger unless the method of Ragavan and Vaikuntanathan is used.
- **Prime $N$.** For prime $N$, the only square roots of 1 are $\pm 1$, so $\mathcal{L} = \mathcal{L}_0$ and the algorithm never succeeds. Test primality first.

## Implementations

## History

Seifert (2001) first suggested running a cheaper factoring circuit several times and combining the outputs by simultaneous Diophantine approximation, which saves a constant factor. Ekerå and Håstad (2017) used several runs and lattice post-processing for short discrete logarithms and RSA moduli. In August 2023 Oded Regev posted the first algorithm with an asymptotic saving in circuit size over Shor's algorithm; it appeared in the Journal of the ACM in 2025. Ragavan and Vaikuntanathan reduced its space and made it robust to noise (CRYPTO 2024), and Ekerå and Gärtner extended it to discrete logarithms (PQCrypto 2024).

## References
