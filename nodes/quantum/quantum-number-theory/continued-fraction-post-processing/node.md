---
tag: 4E4EAV
kind: concept
slug: continued-fraction-post-processing
name: Continued-fraction post-processing
aliases:
- continued-fraction recovery of the order
area: quantum/quantum-number-theory
level: advanced
summary: The classical step of order finding. It expands the measured c/2^t as a continued fraction and reads the order r off the denominators of the convergents below N.
prereqs: [continued-fraction-convergents, euclidean-algorithm, multiplicative-order]
see_also: [shor-algorithm, order-finding, quantum-phase-estimation, continued-fraction, rational-approximation, lames-theorem, wiener-attack, stern-brocot-tree]
sources:
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: the section on factoring (the continued fraction step and the choice N^2 <= q < 2N^2)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.3.1 (the continued fractions algorithm in order finding) and Appendix 4 (continued fractions)
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, 2019 and later versions
    locator: Section 5.4, Continued fractions
  - book: isbn:9780486696300
    title: A. Ya. Khinchin, Continued Fractions, Dover edition
    locator: Chapter II (best approximations and Legendre's criterion)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition, Oxford University Press, 2008
    locator: Chapter 10, Continued fractions
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.5.3, Analysis of Euclid's algorithm
---

Continued-fraction post-processing is the classical step that turns the measured output of an [order-finding](/order-finding/) circuit into the order $r$. The circuit returns an integer $c$ such that $c/Q$, with $Q = 2^t \ge N^2$, is very close to a fraction $s/r$ with an unknown $s$. The step expands $c/Q$ as a [continued fraction](/continued-fraction/) and tests the denominators of its [convergents](/continued-fraction-convergents/) below $N$. It uses only exact integer arithmetic and $O(\log Q)$ steps of the [Euclidean algorithm](/euclidean-algorithm/).

## In plain words

The quantum part of order finding does not print the answer. It prints a long binary number that, read as a fraction, is very near a simple fraction whose bottom part is the answer. The question is how to find that simple fraction from the long one.

Continued fractions answer this. They list, from coarse to fine, the best simple fractions near any number. The fraction we want is always on that list, because it is so close. So we walk down the list, stop when the bottom parts get too large, and test each bottom part against the original problem. If the top and bottom parts of the hidden fraction share a factor, we only get a part of the answer, and a second run fixes it.

## The idea

**The setting.** In [Shor's algorithm](/shor-algorithm/), a good run gives an outcome $c$ with

$$\Bigl|\frac{c}{Q} - \frac{s}{r}\Bigr| \le \frac{1}{2Q}, \qquad 0 \le s < r < N \le \sqrt{Q}.$$

The values $s$ and $r$ are unknown. The same situation comes up whenever [phase estimation](/quantum-phase-estimation/) measures an eigenphase that is known to be a fraction with a small denominator.

**Only one fraction fits.** Let $p/q \ne p'/q'$ be two fractions with $q, q' < N$. Then

$$\Bigl|\frac{p}{q} - \frac{p'}{q'}\Bigr| = \frac{|p q' - p' q|}{q q'} \ge \frac{1}{q q'} > \frac{1}{N^2} \ge \frac{1}{Q}.$$

If both were within $1/(2Q)$ of $c/Q$, their distance would be at most $1/Q$. So at most one fraction with denominator below $N$ lies within $1/(2Q)$ of $c/Q$, and $c$ fixes $s/r$ in lowest terms. This is why the exponent register needs $Q \ge N^2$, that is, about $2n$ qubits for an $n$-digit $N$.

**The fraction is a convergent.** Legendre's criterion says: if $q \ge 1$, $\gcd(p, q) = 1$ and

$$\Bigl|x - \frac{p}{q}\Bigr| < \frac{1}{2q^2},$$

then $p/q$ is a convergent of $x$. Here $|c/Q - s/r| \le 1/(2Q) \le 1/(2N^2) < 1/(2r^2)$, so $s/r$ in lowest terms is a convergent of $c/Q$. The inequality must be strict. With equality the criterion fails for the usual expansion: $x = 1/2 = [0; 2]$ has the convergents $0/1$ and $1/2$, but $|1/2 - 1/1| = 1/(2 \cdot 1^2)$ and $1/1$ is not a convergent.

**The procedure.** Run the Euclidean algorithm on $(c, Q)$ to get the partial quotients $a_0, a_1, \dots$. Build the convergents with $h_k = a_k h_{k-1} + h_{k-2}$ and $k_k = a_k k_{k-1} + k_{k-2}$, starting from $h_{-1} = 1$, $h_{-2} = 0$, $k_{-1} = 0$ and $k_{-2} = 1$. Stop when $k_k \ge N$. For each denominator $q = k_k$, test whether $a^q = 1 \pmod N$; the first $q$ that passes is the answer of the run.

**What it returns.** The convergent is $s/r$ in lowest terms, so the run returns $r' = r / \gcd(s, r)$. If $\gcd(s, r) = 1$, this is $r$. If not, $r'$ is a proper divisor of $r$ and the test $a^{r'} = 1$ fails. Each passed test gives a multiple of $r$, because $a^q = 1$ only for multiples of $r$. The usual fixes are:

- Run again. A random $s$ is coprime to $r$ with probability $\varphi(r)/r = \Omega(1/\log\log r)$.
- Take the least common multiple of the denominators of two runs. If $\gcd(s_1, s_2, r) = 1$, the result is $r$.
- Try small multiples $2r', 3r', \dots$ of a failed denominator.

**Cost.** The number of partial quotients of $c/Q$ is $O(\log Q) = O(n)$ by [Lamé's theorem](/lames-theorem/). With schoolbook arithmetic on numbers of $O(n)$ binary digits, the whole expansion costs $O(n^2)$ bit operations by the standard analysis of the Euclidean algorithm, and each test $a^q \bmod N$ costs one [modular exponentiation](/modular-exponentiation/).

**Exact arithmetic.** The value $c/Q$ has up to $2n$ binary digits, which is 4096 for RSA-2048. A double-precision float keeps 53 binary digits, so a float expansion gives wrong partial quotients after a few steps. Use integers or exact rationals.

## Examples

**One good run.** Take $N = 21$, $a = 2$ and $Q = 512$, so the order is $r = 6$. The outcome $c = 85$ is the most likely outcome next to $s/r = 1/6$. The Euclidean algorithm gives $512 = 6 \cdot 85 + 2$, $85 = 42 \cdot 2 + 1$ and $2 = 2 \cdot 1$, so $85/512 = [0; 6, 42, 2]$.

| k | $a_k$ | convergent | below 21 | test $2^q \bmod 21$ |
|---|---|---|---|---|
| 0 | 0 | 0/1 | yes | $2^1 = 2$, fails |
| 1 | 6 | 1/6 | yes | $2^6 = 64 = 1$, passes |
| 2 | 42 | 42/253 | no | stop |

The run returns $r = 6$. The distance is $|85/512 - 1/6| = 1/1536 \le 1/1024$.

**Two runs that fail alone.** The outcome $c = 171$ gives $171/512 = [0; 2, 1, 170]$ with the convergents $0/1$, $1/2$, $1/3$ and $171/512$. The fraction near $c/Q$ is $s/r = 2/6 = 1/3$, so only the divisor 3 of $r$ appears, and $2^3 = 8$ fails. The outcome $c = 256$ gives $1/2 = 3/6$, and $2^2 = 4$ fails too. The least common multiple of the two denominators is $\operatorname{lcm}(3, 2) = 6$, and $2^6 = 1 \pmod{21}$.

**The exact case.** For $N = 15$, $a = 7$ and $Q = 256$, the order $r = 4$ divides $Q$, and the outcomes are exactly $0, 64, 128, 192$. The fractions are $0$, $1/4$, $1/2$ and $3/4$, so the runs with $s = 1$ and $s = 3$ return 4 directly.

## Where it is used

- **Shor's algorithm.** It is the last step of each run of [Shor's algorithm](/shor-algorithm/) for factoring.
- **Phase estimation in general.** Any use of [quantum phase estimation](/quantum-phase-estimation/) where the eigenphase is a fraction $s/r$ with $r$ below a known bound ends with this step.
- **Other periods.** Period-finding algorithms on the integers, such as the [quantum discrete logarithm](/quantum-discrete-logarithm/) algorithm, use the same rounding to a nearby fraction. Some newer methods replace it by lattice reduction, for example [Regev's algorithm](/regev-factoring-algorithm/) and the [Ekerå-Håstad algorithm](/ekera-hastad-algorithm/).
- **Classical cryptanalysis.** [Wiener's attack](/wiener-attack/) on RSA with a small private exponent uses the same fact: the unknown fraction is close enough to a known one that it must be a convergent.

## References
