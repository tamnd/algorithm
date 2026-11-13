---
tag: KD2HD3
kind: algorithm
slug: quantum-discrete-logarithm
name: Quantum discrete logarithm (Shor)
aliases:
- Shor's discrete logarithm algorithm
area: quantum/quantum-number-theory
level: advanced
summary: Computes x from g and h = g^x in a cyclic group in quantum polynomial time. Two exponent registers and a Fourier transform give a random linear relation in x per run.
solves: [discrete-logarithm-problem, finite-field-discrete-logarithm-problem]
model: quantum-circuit-model
complexity:
  vars: {n: "the length of the group order r in binary", r: "the order of g"}
  time: {gates_per_run: O(n^3), gates_per_run_fast_multiplication: O(n^2 log n log log n), expected_runs: O(1)}
  space: {data_qubits: 3n, ancilla_qubits: O(n)}
properties: {deterministic: false, exact: true, las_vegas: true, quantum: true}
history:
  year: 1994
  people: [Peter W. Shor]
  note: Shor gave the algorithm at FOCS 1994 together with the factoring algorithm, and the full version in SIAM Journal on Computing in 1997.
prereqs: [discrete-logarithm-problem, cyclic-group, quantum-fourier-transform, quantum-modular-exponentiation, chinese-remainder-theorem]
see_also: [shor-algorithm, order-finding, discrete-logarithm-in-bqp, quantum-elliptic-curve-discrete-log, ekera-hastad-algorithm, baby-step-giant-step, pollard-rho-discrete-logarithm, shoup-generic-lower-bound]
sources:
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: Section 6, the discrete logarithm algorithm with the Fourier transform modulo a power of 2, equations (6.4) to (6.19) and the bound 1/480 on the probability of a good outcome
  - paper: doi:10.1109/SFCS.1994.365700
    title: "Peter W. Shor, Algorithms for quantum computation: discrete logarithms and factoring, Proceedings of the 35th Annual Symposium on Foundations of Computer Science (FOCS), IEEE, 1994, pp. 124-134"
    locator: the first account of the discrete logarithm algorithm
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.4.2, the discrete logarithm as a hidden subgroup problem of Z_r x Z_r
  - url: https://www.cs.umd.edu/~amchilds/qa/qa.pdf
    title: Andrew M. Childs, Lecture Notes on Quantum Algorithms, University of Maryland, version of 17 April 2025
    locator: Chapter 5 (discrete log and the hidden subgroup problem, with the example in Z_7^*) and Section 4.4 (the Fourier transform of Z_N)
  - paper: doi:10.1103/RevModPhys.82.1
    title: "Andrew M. Childs and Wim van Dam, Quantum algorithms for algebraic problems, Reviews of Modern Physics 82(1):1-52, 2010"
    locator: the section on the abelian hidden subgroup problem and discrete logarithms
  - paper: arxiv:1905.09084
    title: Martin Ekerå, Revisiting Shor's quantum algorithm for computing general discrete logarithms, 2019 and later versions
    locator: the heuristic estimate that one run with the semiclassical Fourier transform succeeds with probability about 60% to 82%, and above 99% with a small classical search
  - paper: doi:10.1007/978-3-319-70697-9_9
    title: "Martin Roetteler, Michael Naehrig, Krysta M. Svore and Kristin Lauter, Quantum resource estimates for computing elliptic curve discrete logarithms, ASIACRYPT 2017, LNCS 10625, Springer, pp. 241-270"
    locator: the comparison of the logical qubit counts for elliptic curve logarithms and for factoring RSA moduli of the same security level
  - paper: arxiv:quant-ph/9511026
    title: Alexei Yu. Kitaev, Quantum measurements and the Abelian stabilizer problem, 1995
    locator: discrete logarithms as an instance of the abelian stabilizer problem
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapters 13 and 14, the classical generic algorithms (baby-step giant-step, Pollard rho and Pohlig-Hellman) for comparison
---

Shor's discrete logarithm algorithm finds $x$ from $g$ and $h = g^x$ in a [cyclic group](/cyclic-group/) of known order $r$, in time polynomial in $\log r$ on a quantum computer. It puts two exponent registers in superposition, computes $g^a h^{-b}$ in a third register, and applies a [Fourier transform](/quantum-fourier-transform/) to the exponents. Each measurement gives a pair $(c, d)$ with $d \equiv -xc \pmod r$, and fewer than 2.775 runs on average fix $x$. The algorithm breaks [Diffie-Hellman](/diffie-hellman/) and [DSA](/dsa/) in $\mathbb{Z}_p^*$ on a large enough machine, and the same circuit with point addition breaks [elliptic curve cryptography](/quantum-elliptic-curve-discrete-log/).

## In plain words

You know a starting number and a target number. The target is the start multiplied by itself some unknown count of times, with remainders taken after each step. You must find the count. Normal computers need a very long time for this when the numbers are large.

The quantum computer takes two counters and makes them hold all values at the same time. For each pair of values it computes a mix of the start and the target. Pairs that give the same result are linked by the secret count. A Fourier transform turns this link into a pattern, and one measurement gives a short equation that the count satisfies. Simple arithmetic solves the equation. If it gives only part of the answer, you run the circuit again and combine the parts. Two or three runs are usually enough.

## The problem

The input is a cyclic group $G = \langle g \rangle$ with known order $r$, given by a generator $g$ and an element $h \in G$. The output is the unique $x$ with $0 \le x < r$ and $g^x = h$. This is the [discrete logarithm problem](/discrete-logarithm-problem/). In the main case $G$ is a subgroup of $\mathbb{Z}_p^*$; see the [finite field discrete logarithm](/finite-field-discrete-logarithm-problem/). The algorithm needs only two things from $G$: a reversible circuit for the group operation, and a unique bit string for each element, so that equal elements give equal register contents. If $r$ is unknown, [order finding](/order-finding/) gives it first, with the same kind of circuit.

Notation on this page: $n = \lceil \log_2 r \rceil$, $\omega = e^{2\pi i/r}$, and $F_r$ is the Fourier transform of $\mathbb{Z}_r$, which maps $|a\rangle$ to $r^{-1/2} \sum_{c} \omega^{ac} |c\rangle$. Each exponent register has $n$ qubits and holds the values $0, \dots, r - 1$. Qubit 0 is the least significant bit of each register.

## The algorithm

The function $f(a, b) = g^a h^{-b}$ on $\mathbb{Z}_r \times \mathbb{Z}_r$ is constant on the cosets of the subgroup $H = \{(xt, t)\}$, because $f(a, b) = g^{a - xb}$. So the discrete logarithm is a hidden subgroup problem in $\mathbb{Z}_r \times \mathbb{Z}_r$, and Fourier sampling gives random elements of the dual of $H$, which are the pairs $(c, d)$ with $xc + d \equiv 0 \pmod r$. The classical part of the loop solves these congruences and merges them.

```pseudo id=main
QDLOG(g, h, r)                             ▷ g has order r, h = g^x
L1  (x⋆, M) ← (0, 1)                       ▷ invariant: x ≡ x⋆ (mod M)
L2  repeat
L3      prepare r^(-1) Σ_{a,b ∈ Z_r} |a⟩|b⟩|0⟩       ▷ F_r on each exponent register
L4      apply |a⟩|b⟩|y⟩ → |a⟩|b⟩|y ⊕ g^a h^(-b)⟩
L5      apply F_r to each exponent register
L6      measure the exponent registers; call the result (c, d)
L7      e ← gcd(c, r), m ← r/e
L8      x0 ← (-d/e)·(c/e)^(-1) mod m
L9      (x⋆, M) ← merge of x ≡ x⋆ (mod M) and x ≡ x0 (mod m)
L10 until M = r and g^x⋆ = h
L11 return x⋆
```

Line L3 applies $F_r$ to $|0\rangle$ in each exponent register, which gives the uniform superposition over $0, \dots, r - 1$. Line L4 is the costly step. It is a product of $2n$ controlled multiplications by the constants $g^{2^j}$ and $h^{-2^j}$, which are computed classically by [repeated squaring](/binary-exponentiation/); see [quantum modular exponentiation](/quantum-modular-exponentiation/). Line L8 uses a [modular inverse](/modular-inverse/) from the [extended Euclidean algorithm](/extended-euclidean-algorithm/), and line L9 is the [Chinese remainder theorem](/chinese-remainder-theorem/) for moduli that need not be coprime. The target register is never measured.

## Example

Take $p = 7$, $g = 3$ and $h = 2$. The powers of 3 modulo 7 are $1, 3, 2, 6, 4, 5$, so $r = 6$ and the answer is $x = 2$. Each exponent register has 3 qubits and the target register has 3 qubits, so the circuit has 9 qubits. One run gives each pair $(c, -2c \bmod 6)$ with probability exactly $1/6$:

| c | d | e = gcd(c, 6) | congruence from lines L7 and L8 | x fixed? |
|---|---|---|---|---|
| 0 | 0 | 6 | none (modulus 1) | no |
| 1 | 4 | 1 | x ≡ 2 (mod 6) | yes |
| 2 | 2 | 2 | x ≡ 2 (mod 3) | no |
| 3 | 0 | 3 | x ≡ 0 (mod 2) | no |
| 4 | 4 | 2 | x ≡ 2 (mod 3) | no |
| 5 | 2 | 1 | x ≡ 2 (mod 6) | yes |

So one run fixes $x$ with probability $1/3$. If the first run gives $c = 2$ and the second gives $c = 3$, line L9 merges $x \equiv 2 \pmod 3$ and $x \equiv 0 \pmod 2$ into $x \equiv 2 \pmod 6$. Two runs fail only if both values of $c$ are even or both are multiples of 3, so they succeed with probability $(1 - 1/4)(1 - 1/9) = 2/3$. The expected number of runs for $r = 6$ is 2.3. These distributions are exact probabilities from a state-vector simulation of the 9-qubit circuit.

## Correctness

After line L4 the state is $r^{-1} \sum_{a, b} |a\rangle|b\rangle|g^{a - xb}\rangle$. Group the terms by $s = a - xb \bmod r$: for fixed $s$ the pairs are $(s + xb, b)$. After line L5 the amplitude of $|c\rangle|d\rangle|g^s\rangle$ is

$$\frac{\omega^{sc}}{r^2} \sum_{b=0}^{r-1} \omega^{b(xc + d)},$$

which is $\omega^{sc}/r$ if $xc + d \equiv 0 \pmod r$ and 0 otherwise. So $c$ is uniform on $\mathbb{Z}_r$ and $d = -xc \bmod r$. With $e = \gcd(c, r)$, the congruence $cx \equiv -d$ fixes $x$ modulo $r/e$, and the true $x$ satisfies it, so the merged congruences never conflict. After $t$ runs the modulus is $r/\gcd(c_1, \dots, c_t, r)$, so the loop ends exactly when no prime factor $s$ of $r$ divides all the $c_i$. This has probability $\prod_{s \mid r} (1 - s^{-t})$. The full proof, with the bound of 2.775 on the expected number of runs, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

All bounds are in the [quantum circuit model](/quantum-circuit-model/). Take $G \le \mathbb{Z}_p^*$ with $p$ of $n$ bits.

- **One run.** Line L4 does $2n$ controlled modular multiplications. With [schoolbook multiplication](/schoolbook-multiplication/) each costs $O(n^2)$ gates, so line L4 costs $O(n^3)$ gates. The multiplications by $h^{-2^j}$ need the inverses of the constants, which are classical. The two Fourier transforms cost $O(n^2)$ gates, or $O(n \log n)$ with small rotations dropped.
- **Runs.** The expected number of runs is $\sum_{t \ge 0} (1 - \prod_{s \mid r}(1 - s^{-t}))$, which is less than 2.775 for every $r$. It is exactly 2 when $r$ is a power of 2 and $r/(r - 1)$ when $r$ is prime. For $r = 30030 = 2 \cdot 3 \cdot 5 \cdot 7 \cdot 11 \cdot 13$ it is about 2.503.
- **Qubits.** The data use $2n$ exponent qubits and $n$ qubits for the group element, plus the [ancillas](/ancilla-qubits/) of the arithmetic. With a semiclassical Fourier transform, the exponent qubits can be processed one at a time, and the count drops to about $n$ plus the arithmetic workspace.
- **Classical work.** Each run costs one gcd, one inverse and one merge, which is $O(n^2)$ bit operations.

The best classical methods are much slower. Generic methods such as [baby-step giant-step](/baby-step-giant-step/) and [Pollard's rho](/pollard-rho-discrete-logarithm/) need about $\sqrt{r}$ group operations, and [Shoup's bound](/shoup-generic-lower-bound/) shows that no generic classical algorithm does better. For $\mathbb{Z}_p^*$, the [number field sieve](/number-field-sieve-discrete-logarithm/) runs in subexponential time $L_p[1/3]$.

## Properties

- **Las Vegas.** Line L10 checks $g^{x_\star} = h$, so a returned answer is always right. Only the number of runs is random. See [Las Vegas algorithm](/las-vegas-algorithm/).
- **Generic in the group.** The proof uses only the group law and unique encodings. The same algorithm works in any cyclic group with an efficient reversible group operation, such as [elliptic curve groups](/quantum-elliptic-curve-discrete-log/) and class groups.
- **No continued fractions.** With the exact $F_r$, each outcome gives an exact congruence. The fractions only appear in the power-of-2 form below.
- **One relation per run.** A run gives one random element of the dual of $H$. A cyclic $H$ needs only one good element, which is why so few runs are enough.

## Variants and improvements

- **Shor's original form.** Shor used a Fourier transform modulo a power of 2, which is easier to build. For a generator $g$ of $\mathbb{Z}_p^*$, the registers hold $0, \dots, p - 2$, and $q$ is a power of 2 with $p < q < 2p$. An outcome $(c, d)$ is good when $|\{c(p-1)\}_q| \le q/12$ and a phase term is small, where $\{z\}_q$ is the residue of $z$ in $(-q/2, q/2]$. Shor showed that each good triple has probability at least $1/(20q^2)$ and that the good outcomes have total probability at least $1/480$. From a good pair, $x = -\mathrm{round}(d(p-1)/q) \cdot c'^{-1} \bmod (p - 1)$ with $c' = (c(p-1) - \{c(p-1)\}_q)/q$, if $c'$ is invertible. In exact simulations for $p \le 13$ the good outcomes have total probability 0.08 to 0.25, far above $1/480$, and this candidate is always right on good pairs.
- **Ekerå's analysis.** Ekerå (2019) studied the power-of-2 form with the semiclassical Fourier transform and estimated that one run succeeds with probability about 60% to 82%, and above 99% with a small classical search.
- **Short logarithms.** When $x$ is known to be small, the [Ekerå-Håstad algorithm](/ekera-hastad-algorithm/) uses shorter exponent registers; see the [short discrete logarithm](/short-discrete-logarithm/) problem. This also factors RSA moduli.
- **Elliptic curves.** For $E(\mathbb{F}_p)$, line L4 computes $aP + bQ$ with reversible point addition; see the [quantum elliptic curve discrete logarithm](/quantum-elliptic-curve-discrete-log/).
- **Unknown order.** If $r$ is not given, [order finding](/order-finding/) gives it. Alternatively, a hidden subgroup algorithm on $\mathbb{Z} \times \mathbb{Z}$ handles both steps at once.

## When to use it

Use the algorithm only on a fault-tolerant quantum computer with thousands of logical qubits. It is the reason that finite field and elliptic curve [Diffie-Hellman](/diffie-hellman/), [DSA](/dsa/) and [ECDSA](/ecdsa/) are not [post-quantum](/post-quantum-cryptography/). For elliptic curves of 256 bits, the qubit count is lower than for RSA of the same security level, so these systems may fall first. On classical computers, use [Pohlig-Hellman](/pohlig-hellman/) with [Pollard's rho](/pollard-rho-discrete-logarithm/) for generic groups and [index calculus](/index-calculus/) methods for finite fields.

## Pitfalls

- **Encodings must be unique.** If one group element has two bit strings in the target register, the interference in line L5 fails. Use reduced residues modulo $p$, or normalized coordinates for curve points.
- **The order must be right.** With a wrong $r$, the function $g^a h^{-b}$ is not periodic on $\mathbb{Z}_r \times \mathbb{Z}_r$ and the outcomes give wrong congruences. The check in line L10 catches a wrong answer but not the cause.
- **Do not discard runs with a common factor.** A run with $\gcd(c, r) > 1$ still gives $x$ modulo $r/\gcd(c, r)$. Keeping it lowers the expected number of runs.
- **Power-of-2 registers need rounding.** In Shor's original form, the outcome does not give an exact congruence. Use exact integer rounding for $d(p - 1)/q$ and check the candidate.
- **The direction of $h$.** The oracle uses $h^{-b}$. With $h^{b}$ the relation becomes $d \equiv xc$, and the sign of the answer flips.

## Implementations

## History

Peter Shor found the discrete logarithm algorithm together with the factoring algorithm in 1994, after Simon's algorithm had shown an exponential speedup for a hidden subgroup of $\mathbb{Z}_2^n$. He presented both at FOCS 1994 and published the full version in SIAM Journal on Computing in 1997. Kitaev (1995) put both problems in the frame of the abelian stabilizer problem, and the hidden subgroup view became the standard way to present them. Proos and Zalka (2003) worked out the circuit for elliptic curves, and Ekerå and Håstad (2017) gave the version for short logarithms.

## References
