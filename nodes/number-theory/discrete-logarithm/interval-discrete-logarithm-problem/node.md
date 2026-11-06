---
tag: AYHMZQ
kind: problem
slug: interval-discrete-logarithm-problem
name: Interval discrete logarithm problem
aliases:
- bounded discrete logarithm
- discrete logarithm in an interval
area: number-theory/discrete-logarithm
level: advanced
summary: Find x in a known interval [a, b] with g^x = h. For width w = b - a, baby-step giant-step and the kangaroo method take about 2 w^(1/2) group operations, independent of the group order.
prereqs: [discrete-logarithm-problem]
see_also: [pollard-kangaroo, baby-step-giant-step, distinguished-points, parallel-collision-search, short-discrete-logarithm, homomorphic-encryption, generic-group-model]
sources:
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 13, Section 13.3 (baby-step giant-step in an interval); Chapter 14, Sections 14.5 to 14.7 (the kangaroo method, its distributed form, and the Gaudry-Schost algorithm)
  - paper: doi:10.1090/S0025-5718-1978-0491431-9
    title: John M. Pollard, Monte Carlo methods for index computation (mod p), Mathematics of Computation 32(143), 1978
    locator: pages 918 to 924 (the lambda method for a logarithm in an interval)
  - paper: doi:10.1007/s001450010010
    title: John M. Pollard, Kangaroos, Monopoly and discrete logarithms, Journal of Cryptology 13(4), 2000
    locator: pages 437 to 447 (the analysis of the kangaroo method and its parallel forms)
  - paper: doi:10.1007/PL00003816
    title: Paul C. van Oorschot and Michael J. Wiener, Parallel collision search with cryptanalytic applications, Journal of Cryptology 12(1), 1999
    locator: pages 1 to 28 (parallel kangaroos with distinguished points)
  - paper: doi:10.1007/978-3-540-30576-7_18
    title: Dan Boneh, Eu-Jin Goh and Kobbi Nissim, Evaluating 2-DNF formulas on ciphertexts, TCC 2005, Lecture Notes in Computer Science 3378
    locator: pages 325 to 341 (decryption by a discrete logarithm of a small message)
---

The interval discrete logarithm problem is the [discrete logarithm problem](/discrete-logarithm-problem/) with extra information: the exponent is known to lie in an interval $[a, b]$. Its cost depends on the width $w = b - a$ and not on the group order $n$: [baby-step giant-step](/baby-step-giant-step/) solves it in about $2\sqrt w$ group operations with $\sqrt w$ memory, and [Pollard's kangaroo method](/pollard-kangaroo/) in about $2\sqrt w$ operations with constant memory, heuristically. It arises when a secret exponent is short, when part of a key has leaked, and in decryption of schemes that encode small messages in an exponent.

## In plain words

Sometimes you know more than just the start and the target: you know the answer is a number between, say, one million and two million. Then you should not search through every possible exponent of the group, only through that window.

The square root trick still works inside the window. Split the window into blocks, remember the first block, and jump along the window a block at a time until you land in what you remembered. A version that needs almost no memory sends two runners along a path of random jumps, one starting from a known point and one from the target, and waits for one to land in the other's footprints.

## Definition

Let $G$ be a group, $g \in G$ of order $n$, and $h \in G$.

**Input.** $g$, $h$, and integers $a \le b$ with $w = b - a$.

**Output.** An integer $x \in [a, b]$ with $g^x = h$, or "no solution" if no exponent in $[a, b]$ works. For $w \ge n - 1$ every residue modulo $n$ is in range and this is the ordinary DLP.

**Normalization.** Put $h' = h \cdot g^{-a}$. Then $g^x = h$ with $x \in [a, b]$ exactly when $g^{x'} = h'$ with $x' = x - a \in [0, w]$. The shift costs $O(\log a)$ group operations, so one may assume $a = 0$.

**Cost model.** Algorithms are counted in group operations; one operation in $(\mathbb{Z}/p\mathbb{Z})^*$ costs $O(\log^2 p)$ bit operations with schoolbook arithmetic. For a generic algorithm the measure is $w$, not $n$.

## Variants

- **Short exponent.** $a = 0$ and $b = 2^k$ for $k$ much smaller than $\log n$; this is the case of Diffie-Hellman with short secret exponents, and of the quantum [short discrete logarithm](/short-discrete-logarithm/) problem.
- **Multiple intervals or partial leaks.** Some bits of $x$ are known; if the unknown bits are consecutive, it is an interval problem, and if not, the problem is a multidimensional variant: $x = x_0 + \sum_i x_i 2^{e_i}$ with each $x_i$ in a range. Gaudry and Schost's algorithm handles such multidimensional problems.
- **Many instances.** Several targets $h_1, \dots, h_k$ in the same interval; tame kangaroo trails can be reused across them.
- **Groups with fast inversion.** On elliptic curves, $-P$ is free, and the problem in $[-w/2, w/2]$ has a $\sqrt 2$-type speedup as for rho; Galbraith and Ruprai use this with the Gaudry-Schost method.

## Examples

In $\mathbb{F}_{23}^*$ with $g = 5$ and $h = 14$, suppose $x \in [18, 22]$, so $w = 4$. Since $5^{-18} \equiv 4 \pmod{23}$, the shifted target is $h' = 14 \cdot 4 \equiv 10$, and the problem is to find $x' \in [0, 4]$ with $5^{x'} = 10$. Baby-step giant-step with $m = \lceil \sqrt 5 \rceil = 3$ stores $5^0 = 1$, $5^1 = 5$ and $5^2 = 2$; the giant step factor is $5^{-3} \equiv 7$. The first giant step $h' = 10$ is not in the table, and the second, $10 \cdot 7 \equiv 1 = 5^0$, gives $x' = 3 \cdot 1 + 0 = 3$, so $x = 18 + 3 = 21$, which matches $5^{21} \equiv 14$. A search over all of $\mathbb{Z}/22\mathbb{Z}$ would need $m = 5$.

With the same $g$ and $h$ and the interval $[0, 10]$, there is no solution: the only exponent modulo $22$ that works is $21$, and $21 + 22k \notin [0, 10]$ for every $k$.

## Known algorithms

Let $w$ be the width.

- **Exhaustive search.** $w + 1$ multiplications, proved.
- **[Baby-step giant-step](/baby-step-giant-step/).** Run with $m = \lceil \sqrt{w + 1} \rceil$ on $h'$: at most $2\sqrt w + O(1)$ group operations and $\sqrt w$ stored elements in the worst case, proved; the interleaved version of Pollard has average case $(4/3)\sqrt w$ (Galbraith, Section 13.3).
- **[Pollard's kangaroo](/pollard-kangaroo/) (lambda) method.** A tame kangaroo starts at $g^{w}$ and a wild one at $h'$; both jump by $g^{s(y)}$ for a small set of jumps with mean about $\sqrt w / 2$. Expected $(2 + o(1))\sqrt w$ group operations and $O(1)$ memory, heuristic under a random walk assumption (Galbraith, Section 14.5).
- **Parallel kangaroos.** With [distinguished points](/distinguished-points/), $N$ processors get a linear speedup, about $(2 / N)\sqrt w$ operations each (van Oorschot and Wiener; Pollard 2000).
- **Kangaroos with more animals.** For $g$ of odd order, Galbraith, Pollard and Ruprai start wild kangaroos at both $h'$ and $h'^{-1}$ after centring the interval: three kangaroos take about $1.818 \sqrt w$ operations and four take about $1.714 \sqrt w$, heuristic (Galbraith, Section 14.5.5).
- **Gaudry-Schost.** A birthday method on a tame set and a wild set that overlap, built for multidimensional problems (Galbraith, Section 14.7). Combined with the four kangaroo idea it takes $(1.660 + o(1))\sqrt w$ operations, and in groups with fast inversion such as elliptic curves Galbraith and Ruprai reach $(1.36 + o(1))\sqrt w$, both heuristic.

## Bounds

In the [generic group model](/generic-group-model/), the argument of [Shoup's lower bound](/shoup-generic-lower-bound/) carries over: if $x$ is uniform in an interval of width $w$ with $w$ at most the largest prime factor of $n$, two distinct linear forms $a_i + b_i x$ agree for at most one $x$, so $m$ group operations find $x$ with probability $O(m^2 / w)$. Hence $\Omega(\sqrt w)$ operations are needed for constant success probability, and baby-step giant-step is optimal up to a constant factor. The best constant for low memory methods is open.

## Reductions

- **To the full DLP.** The interval problem is a special case of the DLP, and with $w \ge n$ it is the DLP.
- **From the DLP with partial information.** Knowing the top bits of $x$ reduces to an interval; knowing the bottom bits, $x \equiv x_0 \pmod{2^k}$, gives $h \cdot g^{-x_0} = (g^{2^k})^{x''}$ with $x''$ in an interval of width $w / 2^k$.
- **Combining with Pohlig-Hellman.** If $x \bmod m$ is known from small factors of $n$, the remaining unknown lies in an interval of width about $w / m$, and the kangaroo method finishes in $O(\sqrt{w / m})$ operations.
- **Counting points.** The order of an elliptic curve over $\mathbb{F}_q$ lies in the Hasse interval $[q + 1 - 2\sqrt q, q + 1 + 2\sqrt q]$; finding $N$ with $N P = \mathcal{O}$ is an interval problem in exponent form and costs $O(q^{1/4})$ operations by baby-step giant-step.

## Applications

- **Decryption of exponent encodings.** "Lifted" ElGamal and the scheme of Boneh, Goh and Nissim, which are additively [homomorphic](/homomorphic-encryption/), decrypt to $g^m$; recovering a small $m$ is an interval DLP.
- **Short exponents.** Diffie-Hellman with $160$-bit or $256$-bit exponents in a large group is only as strong as the interval problem of that width, plus any help from small factors of the group order (van Oorschot and Wiener's attack).
- **Side channels.** A partial leak of a secret key leaves an interval or a multidimensional variant, which kangaroo and Gaudry-Schost methods solve.
- **Point counting.** Baby-step giant-step in the Hasse interval, in Mestre's method and as the last step of Schoof's algorithm.

## References
