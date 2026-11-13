---
tag: TAWMDC
kind: problem
slug: short-discrete-logarithm
name: Short discrete logarithm problem
aliases:
- short DLP
area: quantum/quantum-number-theory
level: research
summary: Given g and x = g^d with d known to be below 2^m, find d, where the order of g may be unknown. RSA factoring reduces to it, and the Ekerå-Håstad algorithm solves it.
prereqs: [discrete-logarithm-problem, cyclic-group, multiplicative-order]
see_also: [interval-discrete-logarithm-problem, ekera-hastad-algorithm, pollard-kangaroo, baby-step-giant-step, quantum-discrete-logarithm, rsa-cryptosystem, diffie-hellman, order-finding]
sources:
  - paper: doi:10.1007/978-3-319-59879-6_20
    title: "Martin Ekerå and Johan Håstad, Quantum algorithms for computing short discrete logarithms and factoring RSA integers, Post-Quantum Cryptography (PQCrypto 2017), LNCS 10346, Springer, pp. 347-363"
    locator: the definition of the short discrete logarithm problem, the quantum algorithm with tradeoff parameter s, and the reduction from RSA factoring (Section 5.2.4 of arXiv:1702.00249)
  - url: https://eprint.iacr.org/2016/1128
    title: Martin Ekerå, Modifying Shor's algorithm to compute short discrete logarithms, IACR Cryptology ePrint Archive, report 2016/1128
    locator: the first quantum algorithm for short discrete logarithms in groups of unknown order
  - paper: arxiv:2309.01754
    title: "Martin Ekerå, On the success probability of the quantum algorithm for the short DLP, IACR Communications in Cryptology 3(1), 2026"
    locator: the lower bound on the success probability of one run, and its application to Diffie-Hellman with short exponents and to RSA
  - paper: doi:10.1007/3-540-68339-9_29
    title: "Paul C. van Oorschot and Michael J. Wiener, On Diffie-Hellman key agreement with short exponents, EUROCRYPT 1996, LNCS 1070, Springer, pp. 332-343"
    locator: the use of short exponents in Diffie-Hellman, and the classical attacks that combine the kangaroo method with Pohlig-Hellman
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 13.3 (baby-step giant-step in an interval) and Section 14.5 (the kangaroo method)
  - paper: doi:10.22331/q-2021-04-15-433
    title: "Craig Gidney and Martin Ekerå, How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits, Quantum 5:433, 2021"
    locator: the use of the reduction from RSA factoring to a short discrete logarithm in a full cost estimate
---

The short discrete logarithm problem asks for $d$ from $g$ and $x = g^d$ when $d$ is known to be less than $2^m$, and $2^m$ may be much smaller than the order of $g$. The order of $g$ need not be known, which is the main difference from the textbook [discrete logarithm problem](/discrete-logarithm-problem/). Classical generic methods need about $2^{m/2}$ group operations, and the quantum [Ekerå-Håstad algorithm](/ekera-hastad-algorithm/) needs exponents of only about $m$ bits per run. Factoring an RSA integer $N$ reduces to a short logarithm of about $\frac{1}{2}\log_2 N$ bits, which makes this problem central to quantum attacks on RSA.

## In plain words

Raise a known number to a secret power in some group, and publish the result. Normally the secret power can be any number up to the size of the group. In this problem the secret power is known to be small: it has only a given number of binary digits.

The size of the group may be unknown, and it may be huge. A good method should then cost an amount that depends on the length of the secret only. A normal computer needs about the square root of the number of possible secrets. A quantum computer needs work that grows only polynomially in the length of the secret. The best known use is against RSA, where the sum of the two secret primes can be read off as such a small power.

## Definition

Let $G$ be a group with efficient multiplication, inversion and equality tests, given by unique encodings. An instance is an element $g \in G$, an element $x \in G$, and a bound $m$, with the promise that $x = g^d$ for some integer $d$ with $0 \le d < 2^m$. The task is to output such a $d$. The order $r$ of $g$ is not part of the input, and the cost of a method is measured in $m$ and in the cost of group operations, not in $r$.

If $r \ge 2^m$, the answer is unique. If $r < 2^m$, several exponents in $[0, 2^m)$ can work, and any of them is accepted. The interesting case is $r \gg 2^m$, for example $r$ about $2^{2m}$ or larger, where a method that depends on $r$ costs far more than one that depends on $m$.

## Variants

- **Interval form.** If $d$ is known to lie in $[a, a + 2^m)$, then $x g^{-a} = g^{d - a}$ has a short logarithm. So the short problem and the [interval discrete logarithm problem](/interval-discrete-logarithm-problem/) are the same up to a shift. The names differ in emphasis: the interval problem is usually studied classically, and the short problem is the name in the quantum literature, where the unknown order is the key point.
- **Known order.** If $r$ is known, the standard [quantum discrete logarithm](/quantum-discrete-logarithm/) algorithm solves the problem, but its exponents have about $\log_2 r$ bits, not $m$.
- **Specific groups.** In $\mathbb{Z}_p^*$ and other finite fields, index calculus methods solve the full problem in subexponential time, so a short $d$ does not make these attacks harder. In elliptic curve groups no such method is known.
- **Order finding with side information.** Ekerå and Håstad recast some order finding problems, where part of the order is known, as short logarithm problems.

## Examples

**A safe-prime group.** Let $p = 107 = 2 \cdot 53 + 1$ and $g = 4$, which has prime order 53. A Diffie-Hellman party with a 4-bit exponent $d = 13$ publishes $x = 4^{13} \bmod 107 = 69$. Baby-step giant-step with blocks of 4 stores $g^0, \dots, g^3 = 1, 4, 16, 64$, then multiplies $x$ by $g^{-4} = 79$ repeatedly: $69, 101, 61, 4$. The value 4 is $g^1$ and appears after 3 giant steps, so $d = 3 \cdot 4 + 1 = 13$. This takes 8 group operations, against about $2\sqrt{53}$ for the full group.

**An RSA modulus.** Let $N = 667 = 23 \cdot 29$, so both primes have $n = 5$ bits. For $g = 2$, the element $x = 2^{(N-1)/2} \bmod 667 = 2^{333} \bmod 667 = 330$ equals $2^{25}$, with the short logarithm $d = (23 + 29 - 2)/2 = 25 < 2^5$. The order of 2 modulo 667 is 308, which an attacker does not know. From $d$ the factors follow: $c = d + 1 = 26$ and $c \pm \sqrt{c^2 - N} = 26 \pm 3$.

## Known algorithms

**Classical, generic.** These methods need only group operations and do not use $r$.

- **Exhaustive search** tries $g^0, g^1, \dots$ in turn, with at most $2^m$ multiplications.
- **[Baby-step giant-step](/baby-step-giant-step/)** stores $2^{m/2}$ baby steps and takes at most $2^{m/2}$ giant steps, so it costs about $2 \cdot 2^{m/2}$ operations and $2^{m/2}$ memory, in the worst case.
- **[Pollard's kangaroo method](/pollard-kangaroo/)** takes about $2 \cdot 2^{m/2}$ operations on average with constant memory, under a heuristic about random jumps. With distinguished points, van Oorschot and Wiener run it in parallel with a linear speedup.

**Classical, specific groups.** In $\mathbb{Z}_p^*$, [index calculus](/index-calculus/) and the [number field sieve](/number-field-sieve-discrete-logarithm/) find any logarithm in subexponential time in $\log p$. If the order of the group has small factors, van Oorschot and Wiener show how to combine [Pohlig-Hellman](/pohlig-hellman/) on the small part with the kangaroo method, which can make short exponents much weaker than their length suggests.

**Quantum.**

- **Order finding first.** One can find $r$ with [order finding](/order-finding/) and then run Shor's discrete logarithm algorithm. Both steps use exponents of about $\log_2 r$ bits or more, which is wasteful when $d$ is short.
- **Ekerå (2016).** One run with exponent registers of $2m$ and $m$ qubits, without the order, then classical post-processing.
- **[Ekerå-Håstad](/ekera-hastad-algorithm/) (2017).** A parameter $s$ gives $s$ runs with exponents of $m + 2\lceil m/s \rceil$ bits each. A lattice search in dimension $s + 1$ recovers $d$ from the $s$ outcomes.
- **Ekerå (2023).** A proven lower bound on the success probability of one run, which a limited classical search raises to $1 - 10^{-10}$ for every short $d$.

## Bounds

The generic classical methods above cost $O(2^{m/2})$ group operations, and no generic classical method with a better exponent is known. On a quantum computer the problem is in polynomial time in $m$ and the cost of group operations: the Ekerå-Håstad algorithm uses $O(1)$ batches of $s$ runs, each with $m + 2\lceil m/s \rceil$ controlled group operations, and classical work polynomial in $m$ for fixed $s$. For the RSA case this gives about $(\frac{1}{2} + \frac{1}{s})\log_2 N$ controlled multiplications per run, against about $2\log_2 N$ for [Shor's algorithm](/shor-algorithm/).

## Reductions

- **From RSA factoring.** Let $N = pq$ with distinct odd primes $2^{n-1} < p, q < 2^n$ and $g \in \mathbb{Z}_N^*$. Since $\varphi(N) = N - (p + q) + 1$ and $\varphi(N)/2$ is a multiple of the exponent of $\mathbb{Z}_N^*$, the element $x = g^{(N-1)/2}$ equals $g^d$ with $d = (p + q - 2)/2$. From $2^{n-1} + 1 \le p, q \le 2^n - 1$ we get $2^{n-1} \le d < 2^n$, so $m = n$ bits are enough. Then $c = d + 1 = (p + q)/2$, and $p, q = c \pm \sqrt{c^2 - N}$. Ekerå and Håstad state this reduction with $m = n + 1$ and the range $2^n \le d < 2^{n+1}$; the correct range is $2^{n-1} \le d < 2^n$, and the extra bit is harmless but not needed.
- **To the interval problem and back.** A shift by $g^{-a}$ maps one to the other, as in the variants above.
- **From the full problem with a known order.** If $r$ is known, the full discrete logarithm is a short logarithm with $m = \lceil \log_2 r \rceil$. So the short problem with unknown order is at least as general as the standard one.

## Applications

- **Quantum attacks on RSA.** The reduction above lets a quantum computer factor $N$ with shorter exponentiations than in order finding. The cost estimate of Gidney and Ekerå for RSA-2048, about 8 hours with 20 million noisy qubits, uses it.
- **Diffie-Hellman with short exponents.** [Diffie-Hellman](/diffie-hellman/) implementations in safe-prime groups often choose exponents much shorter than the group order to save time. Classically the security then rests on $2^{m/2}$, and on a quantum computer the Ekerå-Håstad algorithm attacks them with a cost that depends on $m$ only.
- **Cryptosystems that decrypt by a small logarithm.** Some homomorphic schemes put a small message in an exponent, and decryption solves a short logarithm by baby-step giant-step or the kangaroo method.

## References
