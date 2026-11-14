---
tag: MH2W70
kind: algorithm
slug: shor-algorithm
name: Shor's algorithm
aliases:
- Shor's factoring algorithm
- Shor's order-finding algorithm
area: quantum/quantum-number-theory
level: advanced
summary: Factors N in time polynomial in log N on a quantum computer. It finds the order of a random base with phase estimation and continued fractions, then splits N with a square root of 1.
solves: [integer-factorization, order-finding]
model: quantum-circuit-model
complexity:
  vars: {n: "the length of N in binary, n = ceil(log2 N)"}
  time: {gates_per_run: O(n^3), gates_per_run_fast_multiplication: O(n^2 log n log log n), expected_runs: O(log n), expected_runs_refined: O(1)}
  space: {data_qubits: 3n, ancilla_qubits: O(n), semiclassical_total: 2n + 3}
properties: {deterministic: false, exact: true, las_vegas: true, quantum: true}
history:
  year: 1994
  people: [Peter W. Shor]
  note: Shor gave quantum algorithms for factoring and discrete logarithms at FOCS 1994 and the full version in SIAM Journal on Computing in 1997.
prereqs: [order-finding, quantum-phase-estimation, continued-fraction-post-processing, factoring-to-order-finding, quantum-modular-exponentiation]
see_also: [integer-factorization, factoring-in-bqp, regev-factoring-algorithm, ekera-hastad-algorithm, quantum-discrete-logarithm, quantum-resource-estimation-factoring, rsa-cryptosystem, simon-algorithm]
sources:
  - paper: doi:10.1109/SFCS.1994.365700
    title: "Peter W. Shor, Algorithms for quantum computation: discrete logarithms and factoring, Proceedings of the 35th Annual Symposium on Foundations of Computer Science (FOCS), IEEE, 1994, pp. 124-134"
    locator: the order-finding circuit, the continued fraction step and the reduction from factoring
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: the section on factoring (the choice q with N^2 <= q < 2N^2, the probability analysis and the gate count)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.3 (order finding and factoring) and Appendix 4 (continued fractions and number theory)
  - paper: doi:10.1103/RevModPhys.68.733
    title: "Artur Ekert and Richard Jozsa, Quantum computation and Shor's factoring algorithm, Reviews of Modern Physics 68(3):733-753, 1996"
    locator: a full account of the algorithm and its analysis
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, 2019 and later versions
    locator: Chapter 5, Shor's factoring algorithm
  - paper: arxiv:quant-ph/9511026
    title: Alexei Yu. Kitaev, Quantum measurements and the Abelian stabilizer problem, 1995
    locator: order finding as phase estimation of the multiplication operator
  - paper: doi:10.1103/PhysRevLett.76.3228
    title: "Robert B. Griffiths and Chi-Sheng Niu, Semiclassical Fourier transform for quantum computation, Physical Review Letters 76(17):3228-3231, 1996"
    locator: the inverse QFT with measurements and classically controlled rotations, which needs one exponent qubit at a time
  - paper: arxiv:quant-ph/0205095
    title: "Stephane Beauregard, Circuit for Shor's algorithm using 2n+3 qubits, Quantum Information and Computation 3(2):175-185, 2003"
    locator: the circuit with 2n + 3 qubits, O(n^3 log n) gates and depth O(n^3)
  - paper: doi:10.1038/414883a
    title: "Lieven M. K. Vandersypen, Matthias Steffen, Gregory Breyta, Costantino S. Yannoni, Mark H. Sherwood and Isaac L. Chuang, Experimental realization of Shor's quantum factoring algorithm using nuclear magnetic resonance, Nature 414:883-887, 2001"
    locator: the factoring of 15 with a compiled seven-qubit circuit
  - paper: doi:10.1038/nature12290
    title: "John A. Smolin, Graeme Smith and Alexander Vargo, Oversimplifying quantum factoring, Nature 499:163-165, 2013"
    locator: compiled circuits that use the answer can be reduced until they show nothing about quantum factoring
  - paper: arxiv:1611.07995
    title: "Thomas Häner, Martin Roetteler and Krysta M. Svore, Factoring using 2n+2 qubits with Toffoli based modular multiplication, Quantum Information and Computation 17(7-8):673-684, 2017"
    locator: the circuit with 2n + 2 qubits
  - paper: doi:10.22331/q-2021-04-15-433
    title: "Craig Gidney and Martin Ekerå, How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits, Quantum 5:433, 2021"
    locator: the cost of the algorithm for 2048-bit moduli on a surface-code machine
  - paper: arxiv:2505.15917
    title: Craig Gidney, How to factor 2048 bit RSA integers with less than a million noisy qubits, 2025
    locator: the estimate of under a million noisy qubits and under a week
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition, Oxford University Press, 2008
    locator: Chapter X (continued fractions and Legendre's criterion) and Chapter XVIII (the order of magnitude of phi(n))
---

Shor's algorithm factors an integer $N$ on a quantum computer in time polynomial in $\log N$. It picks a random base $a$, finds the [order](/multiplicative-order/) $r$ of $a$ modulo $N$ with a quantum circuit, and then gets a factor from $\gcd(a^{r/2} - 1, N)$. The quantum part is [phase estimation](/quantum-phase-estimation/) of the map $y \mapsto a y \bmod N$, and a [continued fraction](/continued-fraction-post-processing/) step turns the measured number into $r$. No classical algorithm is known that factors in polynomial time, so the algorithm puts [integer factorization](/integer-factorization/) in [BQP](/bqp/) and breaks [RSA](/rsa-cryptosystem/) on a large enough machine.

## In plain words

Pick a number and keep multiplying it by itself, always keeping only the remainder after division by the number you want to split. The remainders repeat in a cycle. If you know the length of the cycle, a few greatest common divisor steps usually give a factor. Finding the cycle length is hard for a normal computer when the numbers are large.

A quantum computer can compute all the powers at the same time in one register. It then applies a Fourier transform, which turns the hidden repetition into a peak. One measurement gives a number close to a fraction whose bottom part is the cycle length. A classical method reads that fraction off. If the run fails, you run it again, and a few runs are enough.

## The problem

The input is a composite integer $N$. The output is a factor $f$ with $1 < f < N$ that divides $N$. This is the search form of [integer factorization](/integer-factorization/). Repeated calls on the factors give the full factorization, with at most $\log_2 N$ calls.

Notation on this page: $n = \lceil \log_2 N \rceil$ is the input length. For $\gcd(a, N) = 1$, the order $r$ is the least $r > 0$ with $a^r = 1 \pmod N$; see [order finding](/order-finding/). The exponent register has $t$ qubits, where $t$ is the least integer with $Q = 2^t \ge N^2$, so $N^2 \le Q < 2N^2$ and $t \le 2n$. The work register has $n$ qubits.

## The algorithm

SHOR handles the easy cases classically and calls ORDER, the quantum part, for a random base. ORDER returns a positive multiple $m$ of the order of $a$; in a successful run it returns $r$ itself. Lines L8 to L11 are the reduction of [factoring to order finding](/factoring-to-order-finding/), written so that any multiple of $r$ gives the same answer as $r$.

```pseudo id=main
SHOR(N)                                    ▷ N is composite
L1  if N is even then return 2
L2  if N = b^k for integers b ≥ 2 and k ≥ 2 then return b
L3  loop
L4      a ← a uniform random integer in [2, N - 2]
L5      g ← gcd(a, N)
L6      if g > 1 then return g
L7      m ← ORDER(a, N)                    ▷ a multiple of the order r of a
L8      write m = 2^s d with d odd, and set y ← a^d mod N
L9      if y ≠ 1 then                      ▷ y = 1 means that r is odd
L10         while y^2 mod N ≠ 1 do y ← y^2 mod N
L11         if y ≠ N - 1 then return gcd(y - 1, N)

ORDER(a, N)                                ▷ gcd(a, N) = 1
L12 t ← the least integer with 2^t ≥ N^2, and Q ← 2^t
L13 loop
L14     prepare |0⟩|1⟩: t exponent qubits at 0 and n work qubits at 1
L15     apply a Hadamard gate to each exponent qubit
L16     apply |x⟩|y⟩ → |x⟩|y a^x mod N⟩
L17     apply the inverse QFT to the exponent register and measure it; call the result c
L18     for each convergent p/q of c/Q with q < N, in order of q do
L19         if a^q mod N = 1 then return q
```

Line L2 needs no quantum help: for each $k \le \log_2 N$, an [integer k-th root](/integer-nth-root/) decides whether $N$ is a $k$-th power. Line L16 is the costly step. It is a reversible circuit for [modular exponentiation](/quantum-modular-exponentiation/) built from $t$ controlled multiplications by the constants $a^{2^j} \bmod N$, which are computed classically by [repeated squaring](/binary-exponentiation/). Line L17 uses the [quantum Fourier transform](/quantum-fourier-transform/), and line L18 uses the [convergents](/continued-fraction-convergents/) of $c/Q$, computed with exact integers by the [Euclidean algorithm](/euclidean-algorithm/). The work register is never measured. Measuring it after line L16 would not change the distribution of $c$.

## Example

Factor $N = 15$ with $a = 7$. Here $n = 4$, $t = 8$ and $Q = 256$. The powers of 7 modulo 15 are $1, 7, 4, 13, 1, \dots$, so $r = 4$. After line L16 the state is $\frac{1}{16}\sum_{x} |x\rangle |7^x \bmod 15\rangle$. Because $r$ divides $Q$, the inverse QFT sends all the weight to the four multiples of $Q/r = 64$.

| c | probability | c/Q | convergents | result of line L19 |
|---|---|---|---|---|
| 0 | 1/4 | 0 | 0/1 | none, the run fails |
| 64 | 1/4 | 1/4 | 0/1, 1/4 | q = 4 |
| 128 | 1/4 | 1/2 | 0/1, 1/2 | none: $7^2 = 4 \pmod{15}$ |
| 192 | 1/4 | 3/4 | 0/1, 1/1, 3/4 | q = 4 |

So one run gives $r = 4$ with probability exactly $1/2$. Then $m = 4 = 2^2 \cdot 1$, and line L8 sets $y = 7$. Line L10 squares once: $7^2 = 4$ and $4^2 = 1 \pmod{15}$, so the loop stops at $y = 4$. As $4 \ne 14$, line L11 returns $\gcd(3, 15) = 3$, and $\gcd(5, 15) = 5$ is the other factor. The base $a = 14$ fails: its order is 2 and $14 = -1 \pmod{15}$.

For $N = 21$ and $a = 2$, the order is $r = 6$, which does not divide $Q = 512$. The peaks then spread over neighbors: $c = 85$ has probability 0.114 and gives the convergent 1/6, while $c = 171$ gives 1/3 and fails. The exact probability that one run returns 6 is 0.328, against the lower bound 0.130 of the analysis below. These numbers come from a state-vector simulation of the full 14-qubit circuit (exact probabilities, no sampling), not from hardware.

## Correctness

Each value that SHOR returns is a factor. Lines L1, L2 and L6 are clear. ORDER returns only a $q$ with $a^q = 1$, so $r$ divides $m$. If $r = 2^u d'$ with $d'$ odd, the squaring of lines L8 to L10 first reaches 1 at $a^{2^u d}$, and the value just before it is $a^{2^{u-1} d} = (a^{r/2})^{d/d'} = a^{r/2}$, because $(a^{r/2})^2 = 1$ and $d/d'$ is odd. So line L11 sees $y = a^{r/2}$, which is not 1 because $r$ is minimal. If also $y \ne -1$, then $y$ is a [nontrivial square root of 1](/nontrivial-square-root-of-one/): $N$ divides $(y - 1)(y + 1)$ but neither factor, so $\gcd(y - 1, N)$ is a proper factor.

The loops end with high probability. After line L16, group the exponents $x$ by $k = x \bmod r$. The inverse QFT gives

$$\Pr[c] = \frac{1}{Q^2} \sum_{k=0}^{r-1} \Bigl| \sum_{j=0}^{m_k - 1} e^{2\pi i\, c r j / Q} \Bigr|^2, \qquad m_k = \lceil (Q - k)/r \rceil.$$

For each $s$ with $0 \le s < r$, the integer $c$ nearest to $sQ/r$ has $\Pr[c] \ge \frac{4}{\pi^2 r}\bigl(1 - \frac{\pi r}{2Q}\bigr)^2$. Then $|c/Q - s/r| \le 1/(2Q) < 1/(2r^2)$, so by Legendre's theorem $s/r$ is a convergent of $c/Q$. If $\gcd(s, r) = 1$, the first convergent with $a^q = 1$ is $s/r$ itself. There are $\varphi(r)$ such $s$, and $\varphi(r)/r = \Omega(1/\log\log r)$ by a theorem of Hardy and Wright. For odd $N$ that is not a prime power, at least half of the bases give an even $r$ with $a^{r/2} \ne -1$, so each pass of the loop of line L3 succeeds with probability at least $1/2$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

All bounds are in the [quantum circuit model](/quantum-circuit-model/), with the gates NOT, CNOT, [Toffoli](/toffoli-gate/), Hadamard and controlled phase rotations.

- **One run of ORDER.** Line L16 does $t \le 2n$ controlled modular multiplications. With [schoolbook](/schoolbook-multiplication/) multiplication from ripple-carry adders, each costs $O(n^2)$ gates, so line L16 costs $O(n^3)$ gates and $O(n^3)$ depth. With fast multiplication the count drops to about $O(n^2 \log n \log\log n)$, but the constants are large. The QFT on $t$ qubits costs $O(n^2)$ gates, or $O(n \log n)$ if the tiny rotations are dropped.
- **Runs.** By the bound above, one run gives $r$ with probability $\Omega(1/\log\log N)$, so ORDER needs $O(\log n)$ runs in expectation. With extra classical work, such as trying the least common multiple of two candidate denominators, a constant expected number of runs is enough. The loop of line L3 runs at most 2 times in expectation.
- **Qubits.** The direct circuit has $2n$ exponent qubits and $n$ work qubits as data, plus the ancillas of the arithmetic. The [ancilla](/ancilla-qubits/) count depends on the adder: Beauregard's circuit with a QFT adder uses $n + 2$ ancillas. With the semiclassical inverse QFT of Griffiths and Niu, the exponent register shrinks to one qubit that is measured and reset $2n$ times, for $2n + 3$ qubits in total.
- **Classical work.** Line L2, the gcds and the continued fractions cost $O(n^3)$ bit operations or less.

These are logical counts. A physical machine also pays the overhead of [quantum error correction](/quantum-error-correction/), which multiplies the qubit count by a factor in the hundreds or more; see [quantum resource estimation for factoring](/quantum-resource-estimation-factoring/).

## Properties

- **Las Vegas.** Each answer is checked: line L19 checks $a^q = 1$, and a returned factor divides $N$. The randomness only affects the running time. See [Las Vegas algorithm](/las-vegas-algorithm/).
- **Same circuit for each base.** Only the constants $a^{2^j} \bmod N$ change, and they are computed classically.
- **Tolerant of small errors.** The analysis only needs $|c/Q - s/r| \le 1/(2Q)$, so an approximate QFT and small gate errors still give the right convergent with a constant probability.
- **The order is all it needs.** The quantum part solves [order finding](/order-finding/), which is an instance of the [phase estimation problem](/phase-estimation-problem/); all the number theory is classical.

## Variants and improvements

- **Kitaev's form.** Kitaev phrased order finding as [phase estimation](/quantum-phase-estimation/) of the unitary $U|y\rangle = |a y \bmod N\rangle$, whose eigenvalues are $e^{2\pi i s/r}$. This is the form most textbooks use.
- **Semiclassical QFT.** Griffiths and Niu replace the inverse QFT by one-qubit measurements and rotations that depend on earlier outcomes. Then one control qubit is reused for every exponent bit.
- **Small-qubit circuits.** Beauregard (2003) uses $2n + 3$ qubits, and Häner, Roetteler and Svore (2017) use $2n + 2$ qubits with Toffoli-based arithmetic.
- **Ekerå and Håstad.** The [Ekerå-Håstad algorithm](/ekera-hastad-algorithm/) factors RSA moduli through a short discrete logarithm, with a shorter exponent register.
- **Regev's algorithm.** The [Regev factoring algorithm](/regev-factoring-algorithm/) uses a multidimensional exponent register and lattice post-processing, with about $n^{3/2}$ gates per run but about $\sqrt{n}$ runs.
- **Discrete logarithms.** The same idea, with two exponent registers, computes discrete logarithms; see [quantum discrete logarithm](/quantum-discrete-logarithm/).

## When to use it

Use Shor's algorithm only on a fault-tolerant quantum computer with thousands of logical qubits. For numbers of the size used in [RSA](/rsa-cryptosystem/), it is the only known polynomial-time method, and estimates put RSA-2048 within reach of about a million physical qubits. On today's computers, the [general number field sieve](/general-number-field-sieve/) is the best method for large $N$, and trial division, [Pollard's rho](/pollard-rho/) or the [quadratic sieve](/quadratic-sieve/) are better for small ones. The threat to RSA is the reason for [post-quantum cryptography](/post-quantum-cryptography/).

## Pitfalls

- **Floating-point continued fractions.** The value $c/Q$ has up to $2n$ binary digits. Compute the convergents with integers, not with floats.
- **A short exponent register.** With $Q < N^2$, two fractions with denominators below $N$ can be within $1/(2Q)$ of $c/Q$, and the convergent step can return a wrong denominator.
- **Using $a^{m/2}$ for a multiple $m$ of $r$.** If $m = 2r$, then $a^{m/2} = 1$ and $\gcd(0, N) = N$. Use the squaring sequence of lines L8 to L10, or reduce $m$ to $r$ first.
- **Prime powers and primes.** For $N = p^k$ every base fails, and for prime $N$ the loop never ends. Lines L1 and L2 and a primality test must run first.
- **Compiled demonstrations.** Most experiments that "factor" 15 or 21 use a circuit that was simplified with the known factors or the known order. Smolin, Smith and Vargo showed that such circuits prove nothing about quantum factoring.

## Implementations

## History

Peter Shor found the algorithm in 1994, after Simon's algorithm had shown an exponential quantum speedup for a related period-finding problem. He presented it at FOCS 1994, together with an algorithm for discrete logarithms, and published the full version in SIAM Journal on Computing in 1997. Kitaev (1995) gave the phase-estimation view, and Griffiths and Niu (1996) the semiclassical QFT. In 2001 Vandersypen and others ran a compiled seven-qubit version on 15 in a nuclear magnetic resonance experiment. In 2021 Gidney and Ekerå estimated that RSA-2048 needs 20 million noisy qubits for about 8 hours, and in 2025 Gidney lowered this to under a million qubits for under a week.

## References
