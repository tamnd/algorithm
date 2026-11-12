---
tag: 6VJ956
kind: problem
slug: elliptic-curve-discrete-logarithm-problem
name: Elliptic curve discrete logarithm problem
aliases:
- ECDLP
- elliptic curve discrete log problem
area: number-theory/discrete-logarithm
level: advanced
summary: Given points P and Q on an elliptic curve over a finite field, find x with Q = xP. For well chosen curves only generic methods are known, needing about r^(1/2) steps for prime order r.
prereqs: [discrete-logarithm-problem, elliptic-curve-cryptography]
see_also: [pollard-rho-discrete-logarithm, menezes-okamoto-vanstone-reduction, weil-descent-attack, semaev-summation-polynomial-index-calculus, ecdsa, ecdh, quantum-elliptic-curve-discrete-log, generic-group-model]
sources:
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 14, Sections 14.2 to 14.4 (rho and the speedup by equivalence classes such as the negation map); Chapter 15, Sections 15.7 and 15.8 (Weil descent and summation polynomials); Chapter 26, Section 26.4 (reduction to finite fields by pairings)
  - book: isbn:9781420071467
    title: Lawrence C. Washington, Elliptic Curves, Number Theory and Cryptography, second edition, Chapman and Hall/CRC, 2008
    locator: Chapter 5, The discrete logarithm problem (generic attacks, the MOV and Frey-Rück attacks, anomalous curves)
  - paper: doi:10.1109/18.259647
    title: Alfred J. Menezes, Tatsuaki Okamoto and Scott A. Vanstone, Reducing elliptic curve logarithms to logarithms in a finite field, IEEE Transactions on Information Theory 39(5), 1993
    locator: pages 1639 to 1646 (the reduction by the Weil pairing, polynomial time for supersingular curves)
  - paper: doi:10.1007/s001459900052
    title: Nigel P. Smart, The discrete logarithm problem on elliptic curves of trace one, Journal of Cryptology 12(3), 1999
    locator: "pages 193 to 196 (a linear time attack when #E(F_p) = p)"
  - paper: doi:10.1090/s0025-5718-1987-0866109-5
    title: Neal Koblitz, Elliptic curve cryptosystems, Mathematics of Computation 48(177), 1987
    locator: pages 203 to 209 (the proposal to base cryptography on this problem)
  - paper: doi:10.1007/3-540-39799-x_31
    title: Victor S. Miller, Use of elliptic curves in cryptography, CRYPTO 1985, Lecture Notes in Computer Science 218
    locator: pages 417 to 426 (the independent proposal, and the remark that index calculus does not apply)
  - paper: doi:10.1504/ijact.2012.045590
    title: Joppe W. Bos, Marcelo E. Kaihara, Thorsten Kleinjung, Arjen K. Lenstra and Peter L. Montgomery, Solving a 112-bit prime elliptic curve discrete logarithm problem on game consoles using sliding FFT, International Journal of Applied Cryptography 2(3), 2012
    locator: the main result (a rho computation on the standard curve secp112r1)
---

The elliptic curve discrete logarithm problem is the [discrete logarithm problem](/discrete-logarithm-problem/) in the group of points of an elliptic curve over a finite field: given points $P$ and $Q$ on $E(\mathbb{F}_q)$, find an integer $x$ with $Q = xP$, or report that $Q \notin \langle P \rangle$. For curves chosen with care, no algorithm is known that beats the generic ones, which need about $\sqrt r$ group operations for a point of prime order $r$. This is why [elliptic curve cryptography](/elliptic-curve-cryptography/) reaches $128$-bit security with $256$-bit keys, where finite field systems need keys of about $3000$ bits. A few families of curves are weak: those with a small embedding degree, anomalous curves, and some curves over extension fields.

## In plain words

An elliptic curve over a finite field is a finite set of points with a rule for adding two points to get a third. Adding a point to itself again and again walks through a cycle of points, just as repeated multiplication does for numbers. The problem is to find how many times a starting point was added to itself to reach a given point.

For numbers modulo a prime, the fastest attacks use the fact that numbers can be split into small prime factors. Points on a curve have no such splitting into small pieces that anyone knows how to use. So the best general attack is the square root method that works in every group, and a curve whose cycle is long enough is out of reach. Some special curves have hidden structure, and those must be avoided.

## Definition

Let $q$ be a prime power and $E$ an elliptic curve over $\mathbb{F}_q$, for odd characteristic given by $y^2 = x^3 + a x + b$ with $4a^3 + 27b^2 \ne 0$. The points $E(\mathbb{F}_q)$, with the point at infinity $\mathcal{O}$ as the identity, form a finite abelian group written additively, of order $\#E(\mathbb{F}_q) = q + 1 - t$ with $|t| \le 2\sqrt q$ (Hasse's bound). The group is cyclic or a product of two cyclic groups.

**Input.** The curve $E$ over $\mathbb{F}_q$, a point $P$ of known order $r$, and a point $Q$. In cryptography $r$ is a large prime and $\#E(\mathbb{F}_q) = h r$ with a small cofactor $h$.

**Output.** The integer $x \in \{0, \dots, r - 1\}$ with $Q = xP$, or "no solution". If $r$ is prime and $r^2 \nmid \#E(\mathbb{F}_q)$, the subgroup of order $r$ is unique, and $Q \in \langle P \rangle$ exactly when $rQ = \mathcal{O}$.

**Cost model.** Algorithms are counted in group operations: one point addition or doubling costs a constant number of multiplications and one inversion in $\mathbb{F}_q$ in affine coordinates, $O(\log^2 q)$ bit operations with schoolbook arithmetic. The input size is $\Theta(\log q)$, and $r \approx q$ for curves of prime order, so a generic cost of $\sqrt r$ is exponential in the input size.

## Variants

- **Prime fields.** $q = p$ prime, the standard choice (for example the NIST curves and Curve25519). Only generic attacks are known for curves with large embedding degree and $\#E \ne p$.
- **Binary and extension fields.** $q = 2^m$ or $q = p^n$ with $n > 1$. Weil descent and summation polynomials can apply when $n$ has suitable factors; Koblitz curves over $\mathbb{F}_2$ have a Frobenius endomorphism that speeds up rho by a factor of about $\sqrt{m}$.
- **Small embedding degree.** If $r \mid q^k - 1$ for small $k$, a pairing maps the problem into $\mathbb{F}_{q^k}^*$ ([MOV reduction](/menezes-okamoto-vanstone-reduction/)). Supersingular curves have $k \le 6$. Pairing based cryptography uses such curves on purpose, with sizes chosen against both problems.
- **Anomalous curves.** If $\#E(\mathbb{F}_p) = p$ (trace $t = 1$), the problem is solved in polynomial time by lifting to the $p$-adic numbers (Smart, and independently Semaev and Satoh-Araki).
- **Interval and multiple instances.** The exponent lies in a known interval ([interval problem](/interval-discrete-logarithm-problem/)), or many $Q_i$ share the same base; rho and kangaroo adapt to both.
- **Hyperelliptic curves.** The same problem in the Jacobian of a curve of genus $g \ge 2$; index calculus applies when $g$ is large, with cost about $q^{2 - 2/g}$ for fixed $g$.

## Examples

Let $E : y^2 = x^3 + 2x + 2$ over $\mathbb{F}_{17}$. It has $19$ points, so $E(\mathbb{F}_{17})$ is cyclic of prime order, and $P = (5, 1)$ generates it. The multiples are

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $kP$ | $(5,1)$ | $(6,3)$ | $(10,6)$ | $(3,1)$ | $(9,16)$ | $(16,13)$ | $(0,6)$ | $(13,7)$ | $(7,6)$ |

and $(19 - k)P = -kP = (x, -y)$, so $10P = (7, 11)$, $13P = (16, 4)$ and $18P = (5, 16)$. For $Q = (16, 4)$ the answer is $x = 13$. The pairs $\pm kP$ share their $x$-coordinate, so a method that works with $x$-coordinates only sees $10$ classes instead of $19$ points: this is the negation map speedup of rho.

The curve has $19 = 17 + 1 - t$ points with $t = -1$; it is not anomalous ($t \ne 1$), and its embedding degree is the order of $17$ modulo $19$, which is $9$, so the MOV reduction would lead to $\mathbb{F}_{17^9}$, a much larger field.

## Known algorithms

Let $r$ be the largest prime factor of the order of $P$.

- **Generic.** [Pohlig-Hellman](/pohlig-hellman/) reduces to order $r$. [Baby-step giant-step](/baby-step-giant-step/) takes $O(\sqrt r)$ operations and memory, proved. [Pollard's rho](/pollard-rho-discrete-logarithm/) takes about $\sqrt{\pi r/2}$ operations, and $\sqrt{\pi r / 4}$ with the negation map, heuristic, with [distinguished points](/distinguished-points/) and [parallel collision search](/parallel-collision-search/) for many processors. [Pollard's kangaroo](/pollard-kangaroo/) solves the interval version.
- **Pairings.** The [MOV](/menezes-okamoto-vanstone-reduction/) and Frey-Rück reductions map the problem to $\mathbb{F}_{q^k}^*$ in time polynomial in $k \log q$; useful when $k$ is small.
- **Anomalous curves.** Polynomial time, by the $p$-adic elliptic logarithm.
- **Extension fields.** [Weil descent](/weil-descent-attack/) (Gaudry, Hess and Smart) maps some curves over $\mathbb{F}_{q^n}$ to Jacobians of higher genus curves over $\mathbb{F}_q$, where index calculus is faster. [Summation polynomials](/semaev-summation-polynomial-index-calculus/) give index calculus on $E(\mathbb{F}_{q^n})$ directly, with heuristic cost $\tilde O(q^{2 - 2/n})$ for fixed $n$ (Gaudry) and subexponential time for some families of $q$ and $n$ (Diem).
- **Quantum.** [Shor's algorithm](/quantum-elliptic-curve-discrete-log/) solves the ECDLP in polynomial time on a quantum computer.

## Bounds

For a point of prime order $r$, the [generic lower bound](/shoup-generic-lower-bound/) of $\Omega(\sqrt r)$ applies to all algorithms that use only the group law, and rho meets it. For curves over prime fields with large embedding degree and trace $t \ne 1$, no algorithm faster than $r^{1/2 - \varepsilon}$ is known for any $\varepsilon > 0$, and the problem is believed to need $r^{1/2 + o(1)}$ operations classically. So a curve with a $256$-bit prime order subgroup is believed to give $128$-bit security. Among the largest ECDLP instances solved on a standard curve over a prime field is the $112$-bit curve secp112r1, which Bos and coauthors solved with rho on a cluster of game consoles.

## Reductions

- **To prime order.** Pohlig-Hellman reduces the problem to the prime order subgroups of $\langle P \rangle$.
- **To finite fields.** The MOV and Frey-Rück reductions map $\langle P \rangle$ of order $r$ injectively into the $r$-th roots of unity in $\mathbb{F}_{q^k}^*$, where $k$ is the embedding degree, and so reduce the ECDLP to the [finite field DLP](/finite-field-discrete-logarithm-problem/).
- **To higher genus.** Weil descent reduces the ECDLP over $\mathbb{F}_{q^n}$ to a discrete logarithm in the Jacobian of a curve over $\mathbb{F}_q$.
- **Diffie-Hellman.** The elliptic curve [computational Diffie-Hellman](/computational-diffie-hellman/) problem reduces to the ECDLP. Conversely, Maurer's method reduces the discrete logarithm in a group of prime order $r$ to CDH when an auxiliary elliptic curve over $\mathbb{F}_r$ of smooth order is available.

## Applications

- **Key exchange.** [ECDH](/ecdh/), with keys of $256$ bits for $128$-bit security.
- **Signatures.** [ECDSA](/ecdsa/), Schnorr signatures over curves, and EdDSA all derive the public key as $Q = xP$ from the secret $x$.
- **Pairing based cryptography.** Identity based encryption, short signatures and many zero knowledge systems use curves of small embedding degree, whose security depends on the ECDLP and on the finite field DLP in $\mathbb{F}_{q^k}^*$ together.
- **Parameter validation.** Standards require the curve order to have a large prime factor, the embedding degree to be large and the trace not to be $1$, which rules out the special attacks above.

## References
