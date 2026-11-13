---
tag: QMN0TF
kind: problem
slug: order-finding
name: Order finding
aliases:
- multiplicative order problem
- period of a modular exponential
area: quantum/quantum-number-theory
level: advanced
summary: Given coprime a and N, find the least r > 0 with a^r = 1 (mod N). No classical polynomial-time method is known; Shor's algorithm solves it on a quantum computer.
prereqs: [multiplicative-order, multiplicative-group-modulo-n, modular-exponentiation]
see_also: [shor-algorithm, factoring-to-order-finding, phase-estimation-problem, carmichael-function, discrete-logarithm-problem, integer-factorization, fourier-sampling, baby-step-giant-step]
sources:
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: the section on factoring (order finding in quantum polynomial time)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.3.1 (the order-finding problem and its quantum algorithm) and Section 5.3.2 (factoring reduces to order finding)
  - paper: arxiv:quant-ph/9911124
    title: Richard Cleve, The query complexity of order-finding, Proceedings of the 15th IEEE Conference on Computational Complexity, 2000
    locator: the classical query lower bounds for order finding with a black-box permutation
  - paper: "Gary L. Miller, Riemann's hypothesis and tests for primality, Journal of Computer and System Sciences 13(3):300-317, 1976"
    title: Gary L. Miller, Riemann's hypothesis and tests for primality
    locator: factoring from the order of elements, and the link between computing orders and factoring
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 4.6 (the order of a group element when the factorization of the group order is known)
---

Order finding is the problem of computing the [multiplicative order](/multiplicative-order/) of $a$ modulo $N$: the least $r > 0$ with $a^r = 1 \pmod N$, for coprime $a$ and $N$. The input has about $2 \log_2 N$ binary digits, and no classical algorithm is known that runs in time polynomial in $\log N$. On a quantum computer, [Shor's algorithm](/shor-algorithm/) solves it in polynomial time. Factoring reduces to order finding, and order finding reduces to factoring, so the two problems stand or fall together.

## In plain words

Take a number and keep multiplying it by itself, each time keeping only the remainder after division by a fixed modulus. Sooner or later the remainder comes back to one, and from then on the same values repeat. The task is to find how many steps the cycle takes.

For a small modulus you can just walk around the cycle. For a modulus with hundreds of digits, the cycle can be far too long to walk, and no shortcut is known on a normal computer unless you already know how the modulus splits into primes. A quantum computer can find the cycle length without walking it.

## Definition

**Input.** Integers $N \ge 2$ and $a$ with $1 \le a < N$ and $\gcd(a, N) = 1$. The input length is $n = \lceil \log_2 N \rceil$.

**Output.** The order $r = \operatorname{ord}_N(a)$, the least positive integer with $a^r = 1 \pmod N$.

The order exists because $a$ is a unit of the [group of units modulo N](/multiplicative-group-modulo-n/), a finite group. It divides the [Carmichael function](/carmichael-function/) $\lambda(N)$ and therefore $\varphi(N)$, so $1 \le r < N$. An exponent $m$ has $a^m = 1$ if and only if $r$ divides $m$.

**As a period.** The function $f(x) = a^x \bmod N$ on the integers has period $r$: $f(x + r) = f(x)$ for each $x$, and $f(0), \dots, f(r - 1)$ are distinct. So order finding is the search for the period of a function that is one-to-one inside each period. This is where the alias "period of a modular exponential" comes from.

## Variants

- **Black-box order finding.** The group is given only by an oracle for multiplication, with unique labels for its elements. The quantum method works the same way for any such group.
- **Period finding.** The input is an oracle for a function $f$ on the integers that has period $r$ and is one-to-one inside a period. This is the hidden subgroup problem for the group of integers, which [Fourier sampling](/fourier-sampling/) solves, and modular order finding is the case $f(x) = a^x \bmod N$.
- **Order of a subgroup.** For several elements $a_1, \dots, a_d$, find the lattice of exponent vectors $z$ with $\prod_i a_i^{z_i} = 1$. Regev's algorithm uses this form; see [Regev's factoring algorithm](/regev-factoring-algorithm/).
- **Order from a multiple.** If a multiple $m$ of $r$ is given together with the prime factors of $m$, the order is easy to find; this is the classical case when $\lambda(N)$ is known in factored form.
- **Discrete logarithm.** Given $a$ and $b = a^x$, find $x$. It is a different problem, but the same quantum tools solve it; see the [discrete logarithm problem](/discrete-logarithm-problem/).

## Examples

- $N = 15$, $a = 7$. The powers are $7, 4, 13, 1$, so $r = 4$.
- $N = 21$. The twelve units have these orders.

| a | 1 | 2 | 4 | 5 | 8 | 10 | 11 | 13 | 16 | 17 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| order | 1 | 6 | 3 | 6 | 2 | 6 | 6 | 2 | 3 | 6 | 6 | 2 |

Here $\lambda(21) = \operatorname{lcm}(2, 6) = 6$, and each order divides 6. No unit has order 12 = $\varphi(21)$, so the group is not cyclic.

- $N = 91 = 7 \cdot 13$, $a = 2$. The order of 2 is 3 modulo 7 and 12 modulo 13, so by the [Chinese remainder theorem](/chinese-remainder-theorem/) the order modulo 91 is $\operatorname{lcm}(3, 12) = 12$. This route needs the factors of $N$.

## Known algorithms

- **Repeated multiplication.** Compute $a, a^2, a^3, \dots$ until the value is 1. This takes $r$ multiplications, which can be close to $N$.
- **From the factorization.** With the prime factors of $N$ and of each $p - 1$, compute $\lambda(N)$ and divide out primes while the power stays 1. This takes $O(n)$ [modular exponentiations](/modular-exponentiation/), but getting the factors is the hard part.
- **Baby-step giant-step.** The [baby-step giant-step](/baby-step-giant-step/) method finds $r$ with $O(\sqrt{N})$ multiplications and as much memory.
- **Shor's algorithm.** [Shor's algorithm](/shor-algorithm/) finds $r$ on a quantum computer with $O(n^3)$ gates per run and a constant expected number of runs. It is [phase estimation](/quantum-phase-estimation/) followed by [continued-fraction post-processing](/continued-fraction-post-processing/).

## Bounds

- **Quantum.** In the [quantum circuit model](/quantum-circuit-model/), order finding takes $O(n^3)$ gates with schoolbook arithmetic and about $O(n^2 \log n \log\log n)$ gates with fast multiplication, with constant success probability.
- **Classical, modular case.** The best known classical method factors $N$ and the numbers $p - 1$ with the [general number field sieve](/general-number-field-sieve/), in heuristic time $\exp(O(n^{1/3} (\log n)^{2/3}))$. No superpolynomial classical lower bound is known for the modular problem.
- **Classical, black-box case.** For order finding with a black-box permutation, Cleve proved that a randomized classical algorithm needs about $2^{n/3}$ queries, divided by a factor that depends on the allowed size of the queried exponents. A quantum algorithm needs only a polynomial number of queries. This separation is in the [query model](/quantum-query-model/), not for the modular problem itself.

## Reductions

- **Factoring to order finding.** For odd $N$ that is not a prime power, the order of a random unit $a$ gives a factor $\gcd(a^{r/2} - 1, N)$ with probability at least $1/2$; see [factoring to order finding](/factoring-to-order-finding/). So a fast order-finding algorithm factors $N$.
- **Order finding to factoring.** With an oracle for [factoring](/integer-factorization/), factor $N$, then factor each $p - 1$, then compute the order from $\lambda(N)$ as in the list above. The calls are on numbers smaller than $N$, so the reduction runs in polynomial time.
- **To phase estimation.** The order is the denominator of the eigenphases $s/r$ of the unitary $|y\rangle \mapsto |a y \bmod N\rangle$, so it is an instance of the [phase estimation problem](/phase-estimation-problem/).

## Applications

- **Factoring.** Order finding is the quantum core of factoring, and therefore of the attack on [RSA](/rsa-cryptosystem/).
- **Group exponent.** The least common multiple of the orders of a few random units is $\lambda(N)$ with high probability.
- **Period finding in general.** The same method finds the period of other functions that can be computed fast, such as the periods used in the quantum algorithms for discrete logarithms and for [Pell's equation](/pell-equation/).

## References
