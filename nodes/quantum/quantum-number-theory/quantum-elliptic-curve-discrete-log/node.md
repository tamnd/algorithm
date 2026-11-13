---
tag: RB6N46
kind: algorithm
slug: quantum-elliptic-curve-discrete-log
name: Quantum elliptic curve discrete logarithm
aliases:
- Proos-Zalka algorithm
area: quantum/quantum-number-theory
level: research
summary: Shor's discrete logarithm algorithm on an elliptic curve group. Controlled additions of fixed points compute aP + bQ in superposition, and a Fourier transform reveals x with Q = xP.
solves: [elliptic-curve-discrete-logarithm-problem]
model: quantum-circuit-model
complexity:
  vars: {n: "the length of the field prime p in binary, about the length of the group order r"}
  time: {gates_per_run: O(n^3), toffoli_roetteler_et_al: 448 n^3 log2(n) + 4090 n^3, expected_runs: O(1)}
  space: {data_qubits: 3n, total_qubits_roetteler_et_al: 9n + 2 log2(n) + 10}
properties: {deterministic: false, exact: true, las_vegas: true, quantum: true}
history:
  year: 2003
  people: [John Proos, Christof Zalka, Peter W. Shor]
  note: Shor's 1994 algorithm covers any group with efficient operations; Proos and Zalka gave the first detailed circuit for elliptic curves in 2003.
prereqs: [quantum-discrete-logarithm, elliptic-curve-discrete-logarithm-problem, quantum-fourier-transform, quantum-modular-inversion, reversible-computation]
see_also: [discrete-logarithm-in-bqp, elliptic-curve-cryptography, ecdsa, shor-algorithm, pollard-rho-discrete-logarithm, quantum-resource-estimation-factoring, post-quantum-cryptography, uncomputation]
sources:
  - paper: doi:10.26421/QIC3.4-3
    title: "John Proos and Christof Zalka, Shor's discrete logarithm quantum algorithm for elliptic curves, Quantum Information and Computation 3(4):317-344, 2003"
    locator: the circuit with controlled additions of fixed points and the estimate of about 1000 qubits for a 160-bit curve against about 2000 qubits for 1024-bit RSA
  - paper: doi:10.1007/978-3-319-70697-9_9
    title: "Martin Roetteler, Michael Naehrig, Krysta M. Svore and Kristin Lauter, Quantum resource estimates for computing elliptic curve discrete logarithms, ASIACRYPT 2017, LNCS 10625, Springer, pp. 241-270"
    locator: the circuit with 9n + 2 ceil(log2 n) + 10 qubits and at most 448 n^3 log2 n + 4090 n^3 Toffoli gates, and the estimates for the NIST curves
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: Section 6 and the remark that the method applies to other groups with efficient operations
  - url: https://www.cs.umd.edu/~amchilds/qa/qa.pdf
    title: Andrew M. Childs, Lecture Notes on Quantum Algorithms, University of Maryland, version of 17 April 2025
    locator: Chapter 7, quantum attacks on elliptic curve cryptography
  - book: isbn:9781420071467
    title: Lawrence C. Washington, Elliptic Curves, Number Theory and Cryptography, second edition, Chapman and Hall/CRC, 2008
    locator: Section 2.2 (the group law) and Chapter 5 (the discrete logarithm problem)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 14, Pollard rho on elliptic curves as the best classical attack
---

The quantum elliptic curve discrete logarithm algorithm finds $x$ from points $P$ and $Q = xP$ on an elliptic curve over a finite field, in time polynomial in the field size in bits. It is [Shor's discrete logarithm algorithm](/quantum-discrete-logarithm/) with the group $E(\mathbb{F}_p)$: two exponent registers in superposition control additions of fixed points to an accumulator, and a Fourier transform of the exponents gives a pair $(c, d)$ with $d \equiv xc \pmod r$. Proos and Zalka built the reversible point addition, and later work counted its gates for the curves used in practice. The algorithm breaks [elliptic curve cryptography](/elliptic-curve-cryptography/), including [ECDSA](/ecdsa/) and elliptic curve Diffie-Hellman, on a large enough quantum computer.

## In plain words

Points on an elliptic curve can be added to each other with a fixed rule. Adding a point to itself many times gives a target point. The problem is to find how many times, and normal computers need about the square root of the group size in steps for good curves.

The quantum computer holds all counts at once in two counters. For each bit of each counter it adds a fixed, known point to an accumulator, but only when that bit is one. At the end the accumulator holds a mix of the two given points for every pair of counts. A Fourier transform turns this into a pattern, and a measurement gives a short equation for the secret count. One run is usually enough when the group size is prime.

## The problem

The input is a curve $E: y^2 = x^3 + Ax + B$ over $\mathbb{F}_p$, a point $P$ of known order $r$, and a point $Q \in \langle P \rangle$. The output is the unique $x$ with $0 \le x < r$ and $xP = Q$. This is the [elliptic curve discrete logarithm problem](/elliptic-curve-discrete-logarithm-problem/). In cryptography $r$ is a prime close to $p$, so $n = \lceil \log_2 p \rceil$ is also about the length of $r$.

Notation on this page: $O$ is the point at infinity, $\omega = e^{2\pi i/r}$, and $F_r$ is the Fourier transform of $\mathbb{Z}_r$, which maps $|a\rangle$ to $r^{-1/2} \sum_c \omega^{ac} |c\rangle$. Each exponent register has $\lceil \log_2 r \rceil$ qubits, and qubit 0 is its least significant bit; $a_j$ is bit $j$ of $a$. The accumulator holds a point in compressed form: its $x$ coordinate and the parity of its $y$ coordinate, with a reserved code for $O$. Two points with the same $x$ have $y$ and $p - y$, which have different parities, so the code is unique.

## The algorithm

The function $f(a, b) = aP + bQ = (a + xb)P$ hides the subgroup $\{(-xt, t)\}$ of $\mathbb{Z}_r \times \mathbb{Z}_r$. The quantum part evaluates $f$ as in the Proos-Zalka circuit: a sequence of controlled additions of the constant points $2^j P$ and $2^j Q$, which are computed classically by double-and-add.

```pseudo id=main
QECDLOG(P, Q, r)                           ▷ P has order r, Q = xP
L1  (x⋆, M) ← (0, 1)                       ▷ invariant: x ≡ x⋆ (mod M)
L2  repeat
L3      prepare r^(-1) Σ_{a,b ∈ Z_r} |a⟩|b⟩|O⟩       ▷ F_r on each exponent register
L4      for each j: if a_j = 1 then add the constant point 2^j P to the accumulator
L5      for each j: if b_j = 1 then add the constant point 2^j Q to the accumulator
L6      apply F_r to each exponent register
L7      measure the exponent registers; call the result (c, d)
L8      solve c·x ≡ d (mod r): x ≡ x0 (mod m) with m = r/gcd(c, r)
L9      (x⋆, M) ← merge of x ≡ x⋆ (mod M) and x ≡ x0 (mod m)
L10 until M = r and x⋆·P = Q
L11 return x⋆
```

Lines L4 and L5 are the costly part. Each step is an in-place addition $|R\rangle \mapsto |R + C\rangle$ of a known point $C$. It computes the slope $\lambda = (y_R - y_C)/(x_R - x_C)$ with a reversible [modular inversion](/quantum-modular-inversion/), forms the new coordinates, and then erases the old point and $\lambda$ with [uncomputation](/uncomputation/), which works because $R = (R + C) - C$. Line L8 uses a [modular inverse](/modular-inverse/), and line L9 is the [Chinese remainder theorem](/chinese-remainder-theorem/). When $r$ is prime, line L8 gives $x = d c^{-1} \bmod r$ for every $c \ne 0$.

## Example

Take $E: y^2 = x^3 + x + 6$ over $\mathbb{F}_7$. It has 11 points, so its group is cyclic of prime order $r = 11$, and $P = (1, 1)$ generates it. The multiples of $P$ are $P, (2, 4), (6, 5), (4, 5), (3, 1), (3, 6), (4, 2), (6, 2), (2, 3), (1, 6)$, and then $O$. Let $Q = (4, 5) = 4P$, so $x = 4$.

The exponent registers have 4 qubits each, and the accumulator has 4 qubits (3 bits for $x \in \{0, \dots, 6\}$ or the code 7 for $O$, and 1 parity bit), so the circuit has 12 qubits. Line L4 adds the constants $P, 2P, 4P, 8P = (1,1), (2,4), (4,5), (6,2)$ under the control of $a_0, \dots, a_3$, and line L5 adds $Q, 2Q, 4Q, 8Q = (4,5), (6,2), (3,1), (1,6)$ under the control of $b_0, \dots, b_3$. Each pair $(c, 4c \bmod 11)$ then has probability exactly $1/11$:

| c | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d | 0 | 4 | 8 | 1 | 5 | 9 | 2 | 6 | 10 | 3 | 7 |

For example, $(c, d) = (3, 1)$ gives $x = 1 \cdot 3^{-1} = 1 \cdot 4 = 4 \pmod{11}$. Every outcome except $c = 0$ gives $x$, so one run succeeds with probability $10/11$. These probabilities come from an exact state-vector simulation of the 12-qubit circuit, with each controlled addition applied as a permutation of the basis states.

## Correctness

A controlled addition of a fixed point $C$ permutes the point codes, because $R \mapsto R + C$ is a bijection of the curve, so lines L4 and L5 are unitary. They add $\sum_j a_j 2^j P = aP$ and $bQ$, so they map $|a\rangle|b\rangle|O\rangle$ to $|a\rangle|b\rangle|(a + xb)P\rangle$. Group the terms by $s = a + xb \bmod r$. After line L6 the amplitude of $|c\rangle|d\rangle|sP\rangle$ is

$$\frac{\omega^{sc}}{r^2} \sum_{b=0}^{r-1} \omega^{b(d - xc)},$$

which is $\omega^{sc}/r$ if $d \equiv xc \pmod r$ and 0 otherwise. So $c$ is uniform and $d = xc \bmod r$, and the classical part is the same as for $\mathbb{Z}_p^*$ up to the sign of $d$. The full proof, with the run count, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

All counts are in the [quantum circuit model](/quantum-circuit-model/) for a curve over $\mathbb{F}_p$ with $n$-bit $p$.

- **One run.** Lines L4 and L5 do about $2n$ controlled point additions. Each needs a modular inversion and a few modular multiplications, so with schoolbook arithmetic one run costs $O(n^3)$ gates. Roetteler, Naehrig, Svore and Lauter gave a circuit with at most $448 n^3 \log_2 n + 4090 n^3$ Toffoli gates. For a 256-bit curve this is about $1.3 \cdot 10^{11}$ Toffoli gates.
- **Qubits.** The data use $2n$ exponent qubits and $2n$ coordinate qubits, but with a semiclassical Fourier transform the exponent bits are used one at a time. The circuit of Roetteler and others uses $9n + 2\lceil \log_2 n \rceil + 10$ logical qubits, which is 2330 for $n = 256$. Proos and Zalka estimated about 1000 qubits for a 160-bit curve, against about 2000 for 1024-bit RSA.
- **Runs.** For prime $r$, one run succeeds with probability $(r - 1)/r$. For any $r$ the expected number of runs is less than 2.775.

The best classical attack on a well-chosen curve is generic: [Pollard's rho](/pollard-rho-discrete-logarithm/) needs about $\sqrt{\pi r/2}$ group operations, which is about $2^{128}$ for $n = 256$.

## Properties

- **Las Vegas.** Line L10 checks $x_\star P = Q$, so a returned answer is always right.
- **Fewer qubits than factoring at equal security.** A 256-bit curve has about the security of 3072-bit RSA, but the quantum attack needs far fewer logical qubits, because the registers scale with $n$ and not with the RSA modulus size.
- **Generic in the group.** The algorithm uses only point addition and unique encodings. Changing the curve changes only the classical constants and the field arithmetic.
- **Exceptional cases are rare.** The affine addition formula fails when $R = \pm C$ or $R = O$. In a superposition over many exponents these cases have small total weight, so practical circuits ignore them and accept a small loss in success probability.

## Variants and improvements

- **Power-of-2 transform.** Real circuits use the transform of $\mathbb{Z}_{2^m}$, which is easy to build, instead of the exact $F_r$. Then $c/2^m$ is close to $k/r$ and $d/2^m$ is close to $xk/r$ modulo 1 for some $k$, and rounding gives $k$ and $xk$. In an exact simulation of the example curve with $m = 4$, one run gives $x$ by rounding with probability 0.69 to 0.90, depending on $x$, against $10/11 \approx 0.91$ with the exact transform.
- **Semiclassical transform.** The exponent registers can be replaced by one qubit that is measured and reset after each controlled addition, as for [Shor's algorithm](/shor-algorithm/).
- **Projective coordinates.** Some circuits avoid one inversion per addition by working in projective coordinates, at the cost of more multiplications and more qubits.
- **Other groups.** The same structure gives discrete logarithms in [class groups](/quantum-class-group-algorithm/) and in Jacobians of curves, once their group law has a reversible circuit.

## When to use it

Use it only on a fault-tolerant quantum computer with a few thousand logical qubits and about $10^{11}$ logical gates. It is the main reason that elliptic curve systems such as ECDSA, EdDSA and elliptic curve Diffie-Hellman are being replaced by [post-quantum cryptography](/post-quantum-cryptography/). Because it needs fewer qubits than factoring at the same security level, elliptic curve keys may fall before RSA keys. On classical computers, use Pollard's rho, which is the best known method for good curves.

## Pitfalls

- **Encodings must be unique.** Projective coordinates are not unique, because $(X : Y : Z)$ and $(\lambda X : \lambda Y : \lambda Z)$ are the same point. Convert to a unique form before the accumulator is used for interference, or the amplitudes of one point do not add up.
- **Ignored exceptional cases.** A circuit that computes the wrong sum on the rare inputs $R = \pm C$ still works with a slightly lower success probability, but only if the error is small. Do not use such a circuit on tiny curves, where the exceptional cases are a large part of the superposition.
- **Garbage must be erased.** The slope $\lambda$ and the old point must be uncomputed. Garbage that depends on $a$ and $b$ stays entangled with the exponent registers and destroys the interference.
- **The order of $P$.** The analysis needs the exact order $r$. For curves with a cofactor, work in the subgroup of prime order and check that $Q$ is in it.

## Implementations

## History

Shor's 1994 algorithm already applied to any group with efficient operations, and Koblitz and Miller had proposed elliptic curve cryptography in 1985. Proos and Zalka (2003) gave the first detailed quantum circuit for elliptic curve discrete logarithms and showed that it needs fewer qubits than factoring at the same security level. Roetteler, Naehrig, Svore and Lauter (2017) gave Toffoli counts and qubit counts for the NIST prime curves, and later work reduced these counts further.

## References
