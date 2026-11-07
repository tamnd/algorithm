---
tag: 8S5NXW
kind: algorithm
slug: zeilberger-algorithm
name: Zeilberger's algorithm
aliases: [fast creative telescoping, Zeilberger's fast algorithm, parametrized Gosper algorithm, the fast Zeilberger algorithm]
area: algebra/computer-algebra
level: advanced
summary: Computes a recurrence satisfied by a definite hypergeometric sum via creative telescoping.
solves: [definite-summation]
model: blum-shub-smale-machine
complexity:
  vars: {J: "the order of the telescoper found", m: "the number of unknowns at the last order (at most D + J + 2)", D: "Gosper's degree bound for the certificate polynomial"}
  time: {worst: O(J m^3)}
  space: {extra: O(m^2)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [gosper-algorithm, creative-telescoping, hypergeometric-term]
see_also: [creative-telescoping, gosper-algorithm, wz-method, definite-summation, petkovsek-hyper-algorithm, holonomic-function, hypergeometric-term, binomial-coefficient]
sources:
  - paper: doi:10.1016/0012-365X(90)90120-7
    title: Doron Zeilberger, A fast algorithm for proving terminating hypergeometric identities, Discrete Mathematics 80(2), 1990
    locator: pp. 207 to 211 (the algorithm)
  - paper: doi:10.1016/S0747-7171(08)80044-2
    title: Doron Zeilberger, The method of creative telescoping, Journal of Symbolic Computation 11(3), 1991
    locator: pp. 195 to 204 (creative telescoping and the proof that the method terminates for proper hypergeometric terms)
  - book: isbn:9781568810638
    title: Marko Petkovšek, Herbert S. Wilf and Doron Zeilberger, A = B, A K Peters, 1996
    locator: Chapter 6, Zeilberger's algorithm; Chapter 5 for Gosper's algorithm; Chapter 4 for the fundamental theorem
  - paper: doi:10.1073/pnas.75.1.40
    title: R. William Gosper Jr., Decision procedure for indefinite hypergeometric summation, Proceedings of the National Academy of Sciences 75(1), 1978
    locator: pp. 40 to 42
  - paper: doi:10.1007/BF02100618
    title: Herbert S. Wilf and Doron Zeilberger, An algorithmic proof theory for hypergeometric (ordinary and q) multisum/integral identities, Inventiones Mathematicae 108, 1992
    locator: pp. 575 to 633 (the fundamental theorem for proper hypergeometric terms)
  - paper: doi:10.1006/jsco.1995.1071
    title: Peter Paule and Markus Schorn, A Mathematica version of Zeilberger's algorithm for proving binomial coefficient identities, Journal of Symbolic Computation 20(5-6), 1995
    locator: pp. 673 to 698 (the Gosper-Petkovšek form with a parameter, the implementation fastZeil)
  - paper: doi:10.1016/S0196-8858(02)00504-3
    title: S. A. Abramov, When does Zeilberger's algorithm succeed?, Advances in Applied Mathematics 30(3), 2003
    locator: pp. 424 to 441 (the exact criterion for the existence of a telescoper)
  - paper: doi:10.1016/j.jsc.2004.10.002
    title: Mohamud Mohammed and Doron Zeilberger, Sharp upper bounds for the orders of the recurrences output by the Zeilberger and q-Zeilberger algorithms, Journal of Symbolic Computation 39(2), 2005
    locator: pp. 201 to 207
  - paper: doi:10.1016/j.aam.2005.09.003
    title: Moa Apagodu and Doron Zeilberger, Multi-variable Zeilberger and Almkvist-Zeilberger algorithms and the sharpening of Wilf-Zeilberger theory, Advances in Applied Mathematics 37(2), 2006
    locator: pp. 139 to 152 (order bounds)
  - paper: doi:10.1145/2755996.2756648
    title: Shaoshi Chen, Hui Huang, Manuel Kauers and Ziming Li, A modified Abramov-Petkovšek reduction and creative telescoping for hypergeometric terms, ISSAC 2015
    locator: pp. 117 to 124 (reduction-based telescoping)
  - book: isbn:9781447164630
    title: Wolfram Koepf, Hypergeometric Summation, second edition, Springer, 2014
    locator: Chapter 7, Zeilberger's algorithm
---

Zeilberger's algorithm takes a definite sum $S(n) = \sum_k F(n, k)$ of a hypergeometric term and finds a linear recurrence $\sum_{j=0}^{J} a_j(n) S(n + j) = 0$ with polynomial coefficients, together with a rational certificate that proves it. It is [creative telescoping](/creative-telescoping/) made into an algorithm: for $J = 0, 1, 2, \ldots$ it runs [Gosper's algorithm](/gosper-algorithm/) on $\sum_j a_j F(n + j, k)$ with the $a_j$ as unknowns, and the unknowns enter one linear system. For proper hypergeometric terms, such as products of binomial coefficients, it always stops, and it finds the recurrence of least order that comes from telescoping. With the recurrence and a few initial values, identities such as $\sum_k \binom{n}{k}^2 = \binom{2n}{n}$ are proved by a computer.

## In plain words

A sum such as the sum of the squares of a row of Pascal's triangle has a different number of terms for each row, so there is no direct formula to work with. Zeilberger's idea is to look for a short rule that links the sums of a few consecutive rows, such as "the next sum is a fixed multiple of this one".

The method guesses such a rule with unknown multipliers. Then it asks whether the combined term, summed over the position in the row, telescopes: whether each term is the difference of two consecutive values of some partner expression. That question has an exact test, Gosper's method, and with the unknowns it becomes a set of linear equations. If they have a solution, the rule is found and the partner expression proves it. If not, the method tries a rule that links one more row.

## The problem

**Notation.** $K$ is a field of characteristic $0$, here $K = \mathbb{Q}$, and $\mathbb{F} = K(n)$. Polynomials are in $k$ with coefficients in $K[n]$ or $\mathbb{F}$, and $\mathrm{LC}$ is the leading coefficient in $k$. A term $F(n, k)$ is *hypergeometric* if $F(n + 1, k) / F(n, k)$ and $F(n, k + 1) / F(n, k)$ are rational functions of $n$ and $k$. It is *proper hypergeometric* if
$$F(n, k) = \mathrm{poly}(n, k)\, x^k \prod_i (a_i n + b_i k + c_i)!^{e_i}$$
with a polynomial poly, a constant $x$, integers $a_i, b_i, c_i$ and $e_i = \pm 1$. Binomial coefficients $\binom{an + c}{bk + d}$ have this form.

**Input.** A proper hypergeometric term $F$, given by poly, $x$ and the list of factorials.

**Output.** The least $J \ge 0$, polynomials $a_0(n), \ldots, a_J(n)$, not all zero, and a rational function $R(n, k)$ with
$$\sum_{j=0}^{J} a_j(n)\, F(n + j, k) = G(n, k + 1) - G(n, k), \qquad G = R F. \tag{1}$$
The left side is the *telescoper* and $R$ is the *certificate*. If $F(n, k) = 0$ for $k$ outside a finite range that depends on $n$ (natural boundaries), summing (1) over all $k$ gives $\sum_j a_j(n) S(n + j) = 0$.

## The algorithm

```pseudo id=main
ZEILBERGER(F)                                       ▷ F proper hypergeometric in n and k
L1  for J = 0, 1, 2, ...
L2    write F(n + j, k) = H(k) φ_j(k) for 0 ≤ j ≤ J, with φ_j polynomial; H(k+1)/H(k) = num(k)/den(k)
L3    Gosper-Petkovšek form: num/den = q(k)/r(k+1) · c(k+1)/c(k), gcd(q(k), r(k+h)) = 1 for all h ≥ 1
L4    P(k) ← c(k) Σ_j a_j φ_j(k), with unknowns a_0, ..., a_J in K(n)
L5    D ← Gosper's degree bound for f in q(k) f(k+1) − r(k) f(k) = P(k)
L6    f ← f_0 + f_1 k + ... + f_D k^D; one linear equation over K(n) for each power of k
L7    if the system has a solution with some a_j ≠ 0: clear denominators in n
L8      return J, a_0..a_J and R = r(k) f(k) / (c(k) φ_0(k))
```

Line L2 pulls a common hypergeometric factor $H$ out of all shifted terms. The factorials of $F(n + j, k)$ differ from those of $H$ by finitely many linear factors, which go into $\varphi_j$. Line L3 is the step of Gosper's algorithm that removes common factors $k + u$ of $q$ and $k + w$ of $r$ with $u - w$ a positive integer. For proper terms all factors are linear in $k$, so this needs no resultant. Lines L4 to L6 are Gosper's equation for $t = \sum_j a_j F(n + j, k)$, and the unknowns $a_j$ enter only the right side $P$, linearly. So the system in the unknowns $(a_0, \ldots, a_J, f_0, \ldots, f_D)$ is linear and homogeneous. The code solves it by fraction-free elimination over $K[n]$, which keeps all entries polynomial.

## Example

Take $F(n, k) = \binom{n}{k}^2$. Order $J = 0$ fails, because $\binom{n}{k}^2$ has no hypergeometric antidifference in $k$. For $J = 1$, line L2 gives $H(k) = n!^2 / \bigl(k!^2 (n + 1 - k)!^2\bigr)$, $\varphi_0 = (n + 1 - k)^2$ and $\varphi_1 = (n + 1)^2$. The ratio is $H(k + 1) / H(k) = (n + 1 - k)^2 / (k + 1)^2$, so $q(k) = (k - n - 1)^2$, $r(k) = k^2$ and $c = 1$. Here $\deg q = \deg r = 2$ with equal leading coefficients, and $s = 2(n + 1)$ is not a constant, so the degree bound is $D = 2 - 2 + 1 = 1$. Gosper's equation is
$$(k - n - 1)^2 \bigl(f_0 + f_1 (k + 1)\bigr) - k^2 (f_0 + f_1 k) = a_0 (n + 1 - k)^2 + a_1 (n + 1)^2.$$
The coefficients of $k^0$, $k^1$ and $k^2$ give three linear equations in four unknowns, and the solution is $a_0 = -2(2n + 1)$, $a_1 = n + 1$, $f = 2k - 3n - 3$. So
$$(n + 1) F(n + 1, k) - 2(2n + 1) F(n, k) = G(n, k + 1) - G(n, k), \qquad R = \frac{k^2 (2k - 3n - 3)}{(n + 1 - k)^2}.$$
Summing over $k$ gives $(n + 1) S(n + 1) = 2(2n + 1) S(n)$. With $S(0) = 1$, this is the recurrence of $\binom{2n}{n}$, which proves the identity.

The same code finds the classical recurrences below, and the tests check each by exact evaluation:

| Sum | Order | Recurrence |
|---|---|---|
| $\sum_k \binom{n}{k}$ | 1 | $S(n + 1) - 2 S(n) = 0$ |
| $\sum_k \binom{n}{k}^2$ | 1 | $(n + 1) S(n + 1) - 2(2n + 1) S(n) = 0$ |
| $\sum_k \binom{n}{k}^3$ (Franel) | 2 | $(n + 2)^2 S(n + 2) - (7n^2 + 21n + 16) S(n + 1) - 8(n + 1)^2 S(n) = 0$ |
| $\sum_k \binom{n}{k}^2 \binom{n + k}{k}^2$ (Apéry) | 2 | $(n + 2)^3 S(n + 2) - (2n + 3)(17n^2 + 51n + 39) S(n + 1) + (n + 1)^3 S(n) = 0$ |
| $\sum_k (-1)^k \binom{n}{k}$ | 0 | $S(n) = 0$ for $n \ge 1$ (Gosper-summable) |

The last row shows why small $n$ need care. The certificate is $R = -k/n$, so $G(n, k) = (-1)^{k+1} \binom{n-1}{k-1}$ for $n \ge 1$, and $R$ has a pole at $n = 0$. Indeed $S(0) = 1$.

## Correctness

The proof file proves three facts. First, any answer satisfies (1): if $f$ solves Gosper's equation $q f(k + 1) - r f(k) = P$, then $G = r f t / P$ is an antidifference of $t = \sum_j a_j F(n + j, k)$, and this is $R F$ with $R = r f / (c \varphi_0)$. Second, the returned $J$ is least: if a telescoper of a smaller order existed, $t$ would have a hypergeometric antidifference at that order, and by Gosper's theorem the linear system there would have a solution with the $a_j$ not all zero. Third, the result holds over $K(n)$ even though the code clears denominators, because the equations are linear and homogeneous.

Termination is a theorem of Wilf and Zeilberger (1992): every proper hypergeometric term satisfies a $k$-free recurrence, and this gives a telescoper. For terms that are hypergeometric but not proper, a telescoper may not exist. Abramov (2003) gave the exact criterion. An example is $1 / (n^2 + k^2)$.

## Complexity

The cost model is arithmetic operations in $K(n)$, or ring operations in $K[n]$ for the fraction-free version. At order $J$ the system has $m \le D + J + 2$ unknowns and about $D + \deg q + 1$ equations, and elimination costs $O(m^3)$ operations. Summed over the orders $0, \ldots, J$, the cost is $O(J m^3)$ operations, a proved bound for the procedure. $D$ comes from Gosper's bound. It can be as large as an integer that appears in the input, so it is not bounded by the input size in general, the same as for Gosper's algorithm.

The bit cost over $\mathbb{Q}$ also depends on the degrees in $n$ of the entries. These grow during elimination, and in practice this growth, not the number of operations, limits the method. Mohammed and Zeilberger (2005) and Apagodu and Zeilberger (2006) gave upper bounds for the order $J$ in terms of the factorials of $F$, and these bounds are sharp for many examples. For the examples above, the code takes milliseconds. Sums with many factorials and order 3 or 4 are where the cost becomes large, which matches the experience reported for fastZeil and similar implementations.

## Properties

- Sound: every answer is certified by $R$, and (1) can be checked by rational function arithmetic.
- Complete for proper hypergeometric terms: it always stops, and the order is least among telescopers with rational certificates.
- The telescoper of least order may not give the recurrence of least order for $S(n)$. The sum can satisfy a shorter recurrence that does not come from telescoping, and then a factorization of the recurrence operator is needed.
- The recurrence holds for $n$ where the boundary terms of $G$ vanish. Check small $n$ separately.
- Deterministic, and not recursive.

## Variants and improvements

- **The WZ method.** If the conjectured closed form $s(n)$ is known, run the algorithm on $F(n, k) / s(n)$. The result is a recurrence of order 1 with equal coefficients, which is a [WZ pair](/wz-method/).
- **Solving the recurrence.** The recurrence can be solved for hypergeometric closed forms with [Petkovšek's algorithm Hyper](/petkovsek-hyper-algorithm/). If Hyper finds none, the sum has no closed form as a sum of a fixed number of hypergeometric terms.
- **q-analogue.** The q-Zeilberger algorithm handles q-hypergeometric terms in the same way.
- **Almkvist and Zeilberger.** The continuous analogue (1990) finds differential equations for integrals of hyperexponential functions.
- **Holonomic generalization.** Chyzak's algorithm and other methods for [holonomic functions](/holonomic-function/) find telescopers for a larger class, in several variables, with Ore algebras.
- **Reduction-based telescoping.** Chen, Huang, Kauers and Li (2015) separate the computation of the telescoper from that of the certificate. The certificate can be much larger than the telescoper, and this version need not compute it.
- **Order bounds and guessing.** Systems often start at an order found from the bounds, or guess a recurrence from values and then prove it.

## When to use it

Use it to prove or find identities for definite sums of products of binomial coefficients, factorials and powers, and to get recurrences for sequences given by such sums. It is the standard tool in computer algebra systems for this task. If the summand is not proper hypergeometric, first check whether a telescoper exists (Abramov's criterion), or use holonomic methods. For indefinite sums, where the upper limit is the variable, use [Gosper's algorithm](/gosper-algorithm/) directly.

## Pitfalls

- Forgetting the boundary terms. The recurrence for $S(n)$ needs $G(n, k) \to 0$ at both ends of the summation range. For sums with fixed limits, or with terms that do not vanish outside, add the boundary terms.
- Assuming the least telescoper order is the least recurrence order of the sum.
- Testing (1) only at a few points where a factorial has a pole. Compare as rational functions after division by $F(n, k)$, or evaluate only where all factorial arguments are nonnegative.
- Dividing the content of the $a_j$ out of the certificate as well. $f$ need not be divisible by the content. In the code the content goes to the denominator of $R$.
- Specializing $n$ to numbers before the linear algebra. The system must be solved over $K(n)$. A solution for a few numerical $n$ does not give the polynomial coefficients without interpolation and a proof.
- Expecting small certificates. $R$ can have much larger degree than the $a_j$, as in the Apéry example.

## Implementations

## History

Sister Mary Celine Fasenmyer (1945 and 1947) found recurrences for hypergeometric sums by solving linear systems for $k$-free recurrences of the summand, a slow but general method. Gosper (1978) gave the decision procedure for indefinite hypergeometric summation. Zeilberger (1990) combined the two ideas: he ran Gosper's algorithm with unknown coefficients, which gave a much faster algorithm, and he called the general approach creative telescoping (1991). Wilf and Zeilberger (1990 and 1992) proved that the method always terminates for proper hypergeometric terms and introduced WZ pairs. The book A = B (1996) by Petkovšek, Wilf and Zeilberger made the method widely known. Paule and Schorn (1995) wrote the Mathematica package fastZeil, Koepf described Maple and other implementations, and Abramov (2003) settled when a telescoper exists.

## References
