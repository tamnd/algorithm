---
tag: 86HVR8
kind: algorithm
slug: ekera-hastad-algorithm
name: Ekerå-Håstad algorithm
aliases:
- Ekerå-Håstad short discrete log
area: quantum/quantum-number-theory
level: research
summary: A quantum algorithm for a discrete log d below 2^m in a group of unknown order. It factors RSA integers with a shorter exponent per run than Shor's algorithm.
solves: [short-discrete-logarithm]
model: quantum-circuit-model
complexity:
  vars: {m: "the bit length of the short logarithm d", s: "the tradeoff parameter, the number of runs in one batch", n: "the bit length of each RSA prime, so N has about 2n bits"}
  time: {exponent_bits_per_run: m + 2m/s, runs_per_batch: s, gates_per_run_rsa: O(n^3), classical_postprocessing_fixed_s: poly(m)}
  space: {exponent_qubits: m + 2m/s, work_qubits_rsa: O(n)}
properties: {deterministic: false, exact: true, las_vegas: true, quantum: true}
history:
  year: 2017
  people: [Martin Ekerå, Johan Håstad]
  note: Ekerå gave the one-run version for short discrete logarithms in 2016; Ekerå and Håstad added the tradeoff parameter s and the reduction from RSA factoring in 2017.
prereqs: [short-discrete-logarithm, quantum-discrete-logarithm, quantum-fourier-transform, lll-algorithm, closest-vector-problem]
see_also: [shor-algorithm, rsa-cryptosystem, interval-discrete-logarithm-problem, pollard-kangaroo, lattice-enumeration, quantum-resource-estimation-factoring, regev-factoring-algorithm, diffie-hellman]
sources:
  - paper: doi:10.1007/978-3-319-59879-6_20
    title: "Martin Ekerå and Johan Håstad, Quantum algorithms for computing short discrete logarithms and factoring RSA integers, Post-Quantum Cryptography (PQCrypto 2017), LNCS 10346, Springer, pp. 347-363"
    locator: the algorithm with the tradeoff parameter s, its lattice post-processing, and the reduction from RSA factoring to a short discrete logarithm (Section 5.2.4 of arXiv:1702.00249)
  - url: https://eprint.iacr.org/2016/1128
    title: Martin Ekerå, Modifying Shor's algorithm to compute short discrete logarithms, IACR Cryptology ePrint Archive, report 2016/1128
    locator: the one-run algorithm, the case s = 1 with exponent registers of 2m and m qubits
  - paper: arxiv:2309.01754
    title: "Martin Ekerå, On the success probability of the quantum algorithm for the short DLP, IACR Communications in Cryptology 3(1), 2026"
    locator: the lower bound on the success probability of one run, and the limited classical search that raises it to 1 - 10^-10
  - paper: doi:10.22331/q-2021-04-15-433
    title: "Craig Gidney and Martin Ekerå, How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits, Quantum 5:433, 2021"
    locator: the cost estimates for RSA-2048, which build on the Ekerå-Håstad reduction, and the count of 3n + 0.002 n lg n logical qubits for n-bit moduli
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: Section 6, the discrete logarithm algorithm that this method modifies
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 14.5, the kangaroo method as the classical baseline for short discrete logarithms
---

The Ekerå-Håstad algorithm is a quantum algorithm that finds a discrete logarithm $d$ with $x = g^d$ when $d$ is known to be shorter than $m$ bits, and it does not need the order of $g$. A parameter $s$ trades the number of runs against their size: $s$ runs, each with an exponent of only $m + 2\lceil m/s \rceil$ bits, give enough data for a lattice method to recover $d$. Because an RSA modulus $N = pq$ gives the short logarithm $d = (p + q - 2)/2$ of $g^{(N-1)/2}$, the algorithm also factors RSA integers. Each run then uses an exponent of slightly more than $\frac{1}{2}\log_2 N$ bits, against about $2\log_2 N$ bits in [Shor's algorithm](/shor-algorithm/).

## In plain words

Raising a known number to a secret power gives a public result. Here the secret power is known to be small. The usual quantum method needs to know how many distinct powers there are, and its counters must be long enough to cover all of them.

This method uses short counters and never needs the count. One run gives a pair of numbers that hides the secret only roughly. A few runs give a few such pairs. A classical lattice tool then finds all small secrets that fit every pair at once, and a quick test picks the true one.

For RSA, a known trick turns the secret primes into one small secret power. So finding that power factors the key, with shorter counters than Shor's method needs.

## The problem

The input is a group $G$ with efficient operations and unique encodings, an element $g$, an element $x = g^d$, and a bound $m$ with $0 \le d < 2^m$. The order $r$ of $g$ is unknown and can be much larger than $2^m$. The output is $d$. This is the [short discrete logarithm problem](/short-discrete-logarithm/). It differs from the [interval discrete logarithm problem](/interval-discrete-logarithm-problem/) mainly in what is known: here only the bound on $d$ is given, not the group order. The classical baseline is the [kangaroo method](/pollard-kangaroo/), with about $2^{m/2}$ group operations.

Notation on this page: $\ell = \lceil m/s \rceil$, $A = 2^{\ell + m}$, and $\{z\}$ is the residue of $z$ modulo $A$ in $[-A/2, A/2)$. The quantum Fourier transform of size $M$ maps $|a\rangle$ to $M^{-1/2} \sum_c e^{2\pi i ac/M}|c\rangle$. Qubit 0 of each register is its least significant bit. The analysis assumes $r \ge 2^{\ell + m} + (2^\ell - 1)d$, which holds in the cases of interest.

## The algorithm

One run prepares two exponent registers $a$ of $\ell + m$ qubits and $b$ of $\ell$ qubits, computes $g^a x^{-b} = g^{a - bd}$, and applies a Fourier transform to each register. The measured pair $(j, k)$ is likely to make $dj + 2^m k$ small modulo $A$. Each such pair is one approximate linear equation in $d$, and $s$ of them define a lattice in which $(\dots, d)$ is a vector close to a known target.

```pseudo id=main
EKERA-HASTAD(g, x, m, s)          ▷ x = g^d with 0 ≤ d < 2^m; the order of g is not needed
L1  ℓ ← ⌈m/s⌉
L2  repeat
L3      for i ← 1 to s do
L4          prepare 2^(-(2ℓ+m)/2) Σ_{a < 2^(ℓ+m), b < 2^ℓ} |a⟩|b⟩|0⟩      ▷ Hadamard gates
L5          apply |a⟩|b⟩|y⟩ → |a⟩|b⟩|y ⊕ g^a x^(-b)⟩
L6          apply the QFT of size 2^(ℓ+m) to the first register and of size 2^ℓ to the second
L7          measure both registers; call the result (j_i, k_i)
L8      L ← the lattice spanned by the rows (j_1, ..., j_s, 1) and 2^(ℓ+m)·e_i for i = 1..s
L9      v ← ({-2^m k_1}, ..., {-2^m k_s}, 0)
L10     LLL-reduce the basis of L and enumerate all u ∈ L with |u - v|^2 ≤ (s/4 + 1)·4^m
L11     for each such u whose last coordinate d' is in [0, 2^m) do
L12         if g^d' = x then return d'

EH-FACTOR(N, n, s)                ▷ N = pq with 2^(n-1) < p, q < 2^n
L13 pick g in Z_N^* at random
L14 x ← g^((N-1)/2) mod N         ▷ x = g^d with d = (p + q - 2)/2 < 2^n
L15 d ← EKERA-HASTAD(g, x, n, s); if it fails, go to L13
L16 c ← d + 1
L17 return c - sqrt(c^2 - N), c + sqrt(c^2 - N)
```

Line L5 is a [modular exponentiation](/quantum-modular-exponentiation/) with two exponents. The classical computer precomputes $g^{2^i}$ and $x^{-2^i}$, and the circuit multiplies the target by each of them under the control of one exponent bit. Line L10 uses the [LLL algorithm](/lll-algorithm/) and then [lattice enumeration](/lattice-enumeration/) in dimension $s + 1$; it is a bounded [closest vector](/closest-vector-problem/) search. Line L14 works because $(N - 1)/2 - d = \varphi(N)/2$ is a multiple of the exponent of $\mathbb{Z}_N^*$.

## Example

Take $N = 667 = 23 \cdot 29$, so $n = 5$ and the hidden value is $d = (23 + 29 - 2)/2 = 25$. Let $g = 2$, which has order 308 modulo 667. Line L14 gives $x = 2^{333} \bmod 667 = 330$, and indeed $2^{25} \equiv 330$. With $s = 3$ we get $\ell = 2$, so the registers have 7 and 2 qubits and the exponent has 9 bits. Order finding for a 10-bit $N$ would need an exponent of about 20 bits.

The order condition holds, because $308 \ge 128 + 3 \cdot 25 = 203$, so the outcome probabilities follow the closed form of the proof. All 512 pairs $(j, k)$ can occur. The most likely ones, such as $(0, 0)$, $(32, 3)$ and $(64, 2)$, have $25j + 32k \equiv 0 \pmod{128}$ and probability 0.0059 each. The good pairs, with $|\{25j + 32k\}| \le 8$, have total probability 0.381.

One batch measures $(101, 1)$, $(105, 2)$ and $(62, 0)$. For these, $\{25j + 32k\}$ is $-3$, $1$ and $14$, so the third pair is not good, but it is within $2^{m-1} = 16$. Line L8 gives the basis rows $(101, 105, 62, 1)$, $(128, 0, 0, 0)$, $(0, 128, 0, 0)$ and $(0, 0, 128, 0)$, and line L9 gives the target $v = (-32, -64, 0, 0)$. LLL turns this basis into $(20, 36, -8, 4)$, $(14, -26, 20, -10)$, $(5, 9, -2, 33)$ and $(21, -39, -34, -15)$. Six lattice vectors lie within the squared radius $(3/4 + 1) \cdot 4^5 = 1792$ of $v$. Their last coordinates are $-31, 2, -8, -4, -14$ and $25$, so line L11 tries $d' = 2$ and $d' = 25$. The squared distances are 828 for $d' = 2$ and 831 for $d' = 25$, so the wrong candidate is even a little closer. Line L12 rejects $2^2 = 4$ and accepts $2^{25} \equiv 330$. Then $c = 26$, $c^2 - N = 9$, and line L17 returns $26 - 3 = 23$ and $26 + 3 = 29$. In this example a batch of three runs contains $d$ among its candidates with probability about 0.63.

## Correctness

After line L5 the state is a sum of $|a\rangle|b\rangle|g^{a - bd}\rangle$. Group the terms by $e = a - bd$; under the order condition, distinct $e$ give orthogonal target states. After the transforms, the amplitude of $|j\rangle|k\rangle|g^e\rangle$ is $\frac{\omega^{ej}}{AB}\sum_{b} \omega^{bT}$, with $\omega = e^{2\pi i/A}$, $B = 2^\ell$ and $T = dj + 2^m k$, where $b$ runs over the $b < B$ with $0 \le e + bd < A$. If $|\{T\}| \le 2^{m-2}$, these terms lie on an arc shorter than a quarter circle, so they add up with little cancellation. A counting argument shows that at least $A/2$ pairs are good, and that one run gives a good pair with probability at least $1/8$.

For each $i$, the lattice vector with last coordinate $d$ that is nearest to $v$ differs from $v$ by $\{d j_i + 2^m k_i\}$ in coordinate $i$ and by $d$ in the last coordinate. So when every pair has $|\{d j_i + 2^m k_i\}| \le 2^{m-1}$, this vector is within the radius, and the enumeration finds it. Line L12 checks every candidate, so the output is always right. The full proof, with the RSA reduction, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Exponent length.** One run uses $m + 2\lceil m/s \rceil$ exponent bits. With $s = 1$ it uses $3m$ bits in one run. As $s$ grows, each run approaches $m$ bits, at the cost of $s$ runs and a lattice of dimension $s + 1$.
- **RSA.** For $N = pq$ with $n$-bit primes, $m = n \approx \frac{1}{2}\log_2 N$, so one run needs about $(\frac{1}{2} + \frac{1}{s})\log_2 N$ exponent bits. [Order finding](/order-finding/) needs about $2\log_2 N$. Each exponent bit costs one controlled modular multiplication, so one run costs $O(n^3)$ gates with schoolbook arithmetic.
- **Qubits.** With a semiclassical Fourier transform the exponent qubits can be replaced by one recycled control qubit, so the work register for numbers modulo $N$ dominates. Gidney and Ekerå estimated $3\log_2 N + 0.002\log_2 N \lg\log_2 N$ logical qubits for their RSA construction, which builds on this reduction.
- **Classical part.** The lattice has determinant $A^s = 2^{(\ell + m)s}$, which is about $2^{m(s+1)}$ when $s\ell \approx m$. So its shortest vectors have length near $2^m$, and only a few lattice vectors lie within the radius. LLL takes time polynomial in $m$ and $s$, and the enumeration grows exponentially in $s$, so $s$ stays moderate.

## Properties

- **Las Vegas.** Line L12 accepts only a $d'$ with $g^{d'} = x$, so a returned value is always a correct logarithm.
- **No group order needed.** Unlike Shor's discrete logarithm algorithm, this method never uses $r$. This is what makes it work in $\mathbb{Z}_N^*$, whose order is secret for an RSA modulus.
- **Uses the size of $d$, not of $r$.** The exponent length depends on $m$ only. It is short when $d$ is short, even if the group is much larger.
- **A tunable tradeoff.** The parameter $s$ trades shorter runs against more runs and a harder classical search.

## Variants and improvements

- **One run ($s = 1$).** Ekerå's 2016 algorithm uses exponent registers of $2m$ and $m$ qubits and one run. The 2017 paper with Håstad generalized it to any $s$.
- **High success probability in one run.** Ekerå later proved a lower bound for the success of one run and showed that a limited classical search, with meet-in-the-middle or random-walk methods, raises it to $1 - 10^{-10}$.
- **A shorter logarithm for RSA.** Because $2^{n-1} \le d < 2^n$, the element $x g^{-2^{n-1}}$ has the logarithm $d - 2^{n-1} < 2^{n-1}$, which saves one bit.
- **Short exponents in Diffie-Hellman.** Implementations of [Diffie-Hellman](/diffie-hellman/) in safe-prime groups often use exponents much shorter than the group order. This algorithm attacks them with a cost that depends on the exponent length only.
- **Order finding with side information.** Ekerå and Håstad also recast some order finding problems with partial knowledge of the order as short logarithms.

## When to use it

Use it when the logarithm is known to be short and the group order is unknown or larger than needed, and above all for factoring RSA integers on a quantum computer with limited coherence time. Cost estimates for factoring RSA-2048, such as that of Gidney and Ekerå, use this reduction because it shortens the expensive exponentiation. If the group order is known and $d$ is not short, the standard [quantum discrete logarithm](/quantum-discrete-logarithm/) algorithm is simpler. For general integers that are not products of two primes of similar size, use [Shor's algorithm](/shor-algorithm/).

## Pitfalls

- **Always check the candidates.** Several lattice vectors can lie within the radius, and in the example the wrong one is closer to the target. Without the test of line L12 the method can return a wrong value.
- **The order condition.** The analysis needs the order of $g$ to be at least $2^{\ell + m} + (2^\ell - 1)d$. If the order is small, distinct values of $a - bd$ collide and the distribution changes. In $\mathbb{Z}_N^*$ for RSA this is rarely a problem, and line L15 retries with a new $g$.
- **The bit length of $d$.** For RSA with $2^{n-1} < p, q < 2^n$, $d$ lies in $[2^{n-1}, 2^n)$, so $m = n$ is enough. The original paper uses $m = n + 1$, which is safe but costs one bit more than needed.
- **Sign and scaling conventions.** The target uses $-2^m k_i$ and the lattice rows use $j_i$. A different sign convention for the Fourier transform changes these signs, and then the true vector is not close to the target.
- **The runs must be independent.** The lattice needs $s$ fresh runs. Reusing one outcome $s$ times gives a degenerate lattice with many false candidates.

## Implementations

## History

Shor's 1994 algorithm computes discrete logarithms when the group order is known and uses exponent registers about as long as the order. In 2016 Ekerå showed that a short logarithm can be found with exponents of length about $3m$ and no knowledge of the order. In 2017 Ekerå and Håstad introduced the tradeoff parameter $s$ and the lattice post-processing, and they showed that factoring an RSA integer reduces to a short discrete logarithm. Gidney and Ekerå (2021) used this reduction in their estimate that RSA-2048 can be factored in about 8 hours with 20 million noisy qubits. Ekerå (2023) proved strong lower bounds on the success probability of one run.

## References
