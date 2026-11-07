---
tag: E2T01W
kind: algorithm
slug: paterson-stockmeyer-algorithm
name: Paterson-Stockmeyer algorithm
aliases:
- Paterson-Stockmeyer method
- rectangular splitting
- baby-step giant-step polynomial evaluation
area: algebra/polynomial-arithmetic
level: advanced
summary: Evaluates a degree-n polynomial with O(sqrt(n)) nonscalar multiplications by baby-step giant-step splitting.
solves: [polynomial-evaluation]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the polynomial}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n^(1/2))}
  nonscalar_multiplications: {worst: 2(n + 1)^(1/2), best: 2(n + 1)^(1/2)}
  ring_operations: {worst: O(n), best: O(n)}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1973
  people: [Michael S. Paterson, Larry J. Stockmeyer]
  note: Paterson and Stockmeyer showed in 1973 that a polynomial of degree n can be evaluated with O(n^(1/2)) multiplications of two expressions in the argument, and that about n^(1/2) are needed in general.
prereqs: [horner-rule, polynomial]
see_also: [estrin-scheme, brent-kung-composition, polynomial-evaluation, horners-rule-optimality, baby-step-giant-step, polynomial-composition, homomorphic-encryption]
sources:
  - paper: doi:10.1137/0202007
    title: Michael S. Paterson and Larry J. Stockmeyer, On the number of nonscalar multiplications necessary to evaluate polynomials, SIAM Journal on Computing 2(1), 60-66, 1973
    locator: the algorithms with O(n^(1/2)) nonscalar multiplications and the lower bound
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 4.4.3, Rectangular series splitting
---

The Paterson-Stockmeyer algorithm evaluates a polynomial $f$ with scalar coefficients at a point $X$ for which products $X \cdot Y$ are expensive, such as a matrix or a large number. It splits $f$ into blocks of about $\sqrt{n}$ coefficients, computes the powers $X^0, \ldots, X^k$ once, forms each block with cheap scalar multiplications only, and joins the blocks by [Horner's rule](/horner-rule/) in $X^k$. This uses at most $2\lceil\sqrt{n+1}\,\rceil - 2$ expensive products, against $n$ for Horner's rule.

Notation: $R$ is a commutative ring, $f = \sum_{i=0}^{n} a_i x^i \in R[x]$ is a list of coefficients with the constant term first, and $A$ is an associative $R$-algebra with unit $1_A$, for example the $d \times d$ matrices over $R$, or $R$ itself. The point $X$ is an element of $A$, and $f(X) = \sum_i a_i X^i$. A nonscalar multiplication is a product of two elements of $A$. A scalar multiplication is a product $c \cdot P$ with $c \in R$ and $P \in A$. Costs count operations in $A$ in the algebraic complexity model, and the nonscalar multiplications are counted apart.

## In plain words

Suppose you must put a square matrix into a polynomial of degree one hundred. Multiplying two matrices is slow, but multiplying a matrix by a number or adding two matrices is fast. Horner's rule does one hundred slow products. Instead, compute the first ten or eleven powers of the matrix once. Cut the polynomial into pieces of ten coefficients. Each piece is a sum of those powers times numbers, which needs no slow product. Then join the pieces with Horner's rule, using the tenth power as the step, which needs about ten more slow products. So about twenty slow products replace one hundred.

## The problem

**Input:** a list $a = [a_0, \ldots, a_n]$ of elements of $R$ and an element $X$ of the $R$-algebra $A$.

**Output:** $f(X) = \sum_{i=0}^{n} a_i X^i$, with $X^0 = 1_A$.

This is [polynomial evaluation](/polynomial-evaluation/) at one point. The goal is to use few nonscalar multiplications, with $O(n)$ scalar multiplications and additions.

## The algorithm

Choose a block size $k \ge 1$ and let $m = \lceil (n+1)/k \rceil$ be the number of blocks. Pad with $a_i = 0$ for $i > n$. The identity behind the method is

$$f(X) = \sum_{j=0}^{m-1} B_j\, (X^k)^j, \qquad B_j = \sum_{i=0}^{k-1} a_{jk+i}\, X^i.$$

The powers $X^0, \ldots, X^k$ are the baby steps. Horner's rule in $Y = X^k$ takes the giant steps. The default block size is $k = \lceil \sqrt{n+1}\, \rceil$, which makes $m \le k$.

```pseudo id=main
PATERSON-STOCKMEYER(a_0, ..., a_n; X)
L1  k ← ⌈√(n + 1)⌉;  m ← ⌈(n + 1)/k⌉
L2  P_0 ← 1_A;  P_1 ← X
L3  for i ← 2 to min(k, n) do P_i ← P_{i-1} · X        ▷ baby steps, nonscalar
L4  for j ← 0 to m - 1 do B_j ← Σ_{i=0}^{k-1} a_{jk+i} · P_i   ▷ scalar products only
L5  S ← B_{m-1}
L6  for j ← m - 2 downto 0 do
L7      S ← S · P_k + B_j                              ▷ giant steps, nonscalar
L8  return S
```

Line L3 computes $P_k = X^k$ only when it is needed, that is when $m \ge 2$, which forces $k \le n$. In line L4 the terms with $jk + i > n$ are left out.

## Example

Evaluate $f = 1 + 2x + 3x^2 + \cdots + 9x^8$, so $n = 8$, at $X = 2$ over $\mathbb{Z}$. Then $k = \lceil \sqrt{9}\, \rceil = 3$ and $m = 3$.

| step | values |
|---|---|
| baby steps (L2, L3) | $P_0, P_1, P_2, P_3 = 1, 2, 4, 8$ |
| block $B_0$ (L4) | $1 + 2 \cdot 2 + 3 \cdot 4 = 17$ |
| block $B_1$ | $4 + 5 \cdot 2 + 6 \cdot 4 = 38$ |
| block $B_2$ | $7 + 8 \cdot 2 + 9 \cdot 4 = 59$ |
| L5 | $S = 59$ |
| L7, $j = 1$ | $S = 59 \cdot 8 + 38 = 510$ |
| L7, $j = 0$ | $S = 510 \cdot 8 + 17 = 4097$ |

So $f(2) = 4097 = 8 \cdot 2^9 + 1$. The nonscalar products are $P_2$, $P_3$ and the two giant steps: 4 in total, against 8 for Horner's rule. For a matrix argument, the same steps with $X = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$, whose powers are $X^i = \begin{pmatrix} 1 & i \\ 0 & 1 \end{pmatrix}$, give $f(X) = \begin{pmatrix} f(1) & f'(1) \\ 0 & f(1) \end{pmatrix} = \begin{pmatrix} 45 & 240 \\ 0 & 45 \end{pmatrix}$. A script checked both results and the counts.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Each index $t$ in $0, \ldots, n$ has one way to be written as $t = jk + i$ with $0 \le i < k$, so the blocks hold every coefficient once, and $a_t X^t = a_{jk+i} X^i (X^k)^j$. Hence $f(X) = \sum_j B_j (X^k)^j$. The loop of lines L6 and L7 is Horner's rule for the polynomial $\sum_j B_j y^j$ at $y = X^k$. Its invariant is $S = \sum_{t \ge j} B_t (X^k)^{t-j}$ after the step for $j$. The elements $X^i$, $B_j$ and $S$ are all polynomials in $X$, so they commute with each other even when $A$ is not commutative, and Horner's rule is valid for them.

## Complexity

All bounds are proved, in the algebraic model, with the nonscalar multiplications counted apart.

- **Nonscalar multiplications.** Line L3 does $\min(k, n) - 1$ products and line L7 does $m - 1$. For $m \ge 2$ the total is $k + m - 2$. With $k = \lceil\sqrt{n+1}\,\rceil$ we have $m \le k$, so the total is at most $2\lceil\sqrt{n+1}\,\rceil - 2$. For $n = 100$ it is $10 + 9 = 19$, against $100$ for Horner's rule.
- **Scalar multiplications and additions.** Line L4 does one scalar multiplication per coefficient, $n + 1$ in all. Lines L4 and L7 do $n$ additions in all, since each one joins two terms of the final sum.
- **Other block sizes.** For any $k$, the count is $\min(k, n) - 1 + \lceil (n+1)/k \rceil - 1$. The sum $k + (n+1)/k$ is smallest near $k = \sqrt{n+1}$, so the default is close to the best choice for this scheme.
- **Space.** $k + 1$ powers and $m$ blocks, so $\Theta(\sqrt{n})$ elements of $A$. The blocks can also be formed one at a time inside the loop, which leaves $k + 2$ elements.
- **Total cost for matrices.** For $d \times d$ matrices, with matrix products costing $\Theta(d^\omega)$ for some $2 < \omega \le 3$, the cost is $O(\sqrt{n}\, d^\omega + n d^2)$, against $O(n d^\omega)$ for Horner's rule.

**Lower bound.** Paterson and Stockmeyer proved that about $\sqrt{n}$ nonscalar multiplications are necessary for most polynomials of degree $n$. So the method is optimal up to a constant factor. They also gave a refined scheme with a smaller constant.

**In practice (observed).** The gain is real when a nonscalar product costs much more than a scalar product and an addition. For $d \times d$ matrices, the ratio is about $d$. For a multiprecision argument with small integer or rational coefficients, a scalar product is a multiplication by a small number, so it is cheap. The best $k$ in practice also depends on memory, because $k$ powers must be stored. When all products cost the same, for example for $X$ in $R$ itself, the method has no advantage over Horner's rule.

## Properties

- **Exact.** In exact arithmetic the result equals $f(X)$ computed by Horner's rule.
- **Works in any associative algebra with unit.** Commutativity of $A$ is not needed, only that the scalars commute with $A$.
- **Few nonscalar products, more storage.** It keeps $\Theta(\sqrt{n})$ powers, while Horner's rule keeps one element.
- **Not online.** All coefficients must be known before the giant steps start.

## Variants and improvements

- **Modular composition.** The [Brent-Kung algorithm](/brent-kung-composition/) applies the same splitting with $X = g \bmod h$ in $R[x]/(h)$, and replaces the scalar step by one matrix product. This gives composition modulo $h$ in $O(\sqrt{n}\, M(n) + n^{(\omega+1)/2})$ operations.
- **Power series.** Brent and Zimmermann describe the same idea as rectangular series splitting for evaluating a truncated power series at a multiprecision number, where most products are by small numbers (Section 4.4.3).
- **Matrix functions.** Truncated Taylor and Pade approximations of functions of matrices, such as the matrix exponential, are evaluated this way to save matrix products.
- **Fewer stored powers.** A smaller $k$ uses less memory and more giant steps.
- **Short chains instead.** When the goal is a short chain of dependent operations, not few products, use [Estrin's scheme](/estrin-scheme/).
- **Homomorphic encryption.** Evaluating a polynomial on encrypted data counts products of two ciphertexts, which are the expensive operation, so [homomorphic encryption](/homomorphic-encryption/) libraries use this splitting.

## When to use it

Use the Paterson-Stockmeyer algorithm when the argument is a matrix, a polynomial modulo another polynomial, a large number, or a ciphertext, and the coefficients are scalars, so that products of two arguments are much more expensive than additions and scalar products. Use [Horner's rule](/horner-rule/) when all multiplications cost about the same, when memory is tight, or when the degree is small.

## Pitfalls

- **Coefficients that are not scalars.** If the coefficients are themselves elements of $A$, then line L4 does nonscalar products and the saving is lost.
- **Off by one in the blocks.** Block $j$ holds $a_{jk}, \ldots, a_{jk+k-1}$, and the last block may be short. Reading past $a_n$ or dropping $a_{mk-1}$ gives a wrong value.
- **Computing a power that is not used.** $X^k$ is needed only when there are at least two blocks; for a matrix argument one extra product is a large cost.
- **Using the wrong unit.** The block $B_j$ starts from $a_{jk}\, 1_A$, the identity of $A$, not from the scalar $a_{jk}$.
- **Memory for large matrices.** The $k + 1$ powers of a large matrix can need more memory than is available.

## Implementations

## History

Michael Paterson and Larry Stockmeyer published the method in 1973 in the SIAM Journal on Computing. They counted the multiplications in which both factors depend on the argument, and they showed that $O(\sqrt{n})$ of them suffice and that about $\sqrt{n}$ are necessary in general. They pointed to matrix polynomials as the main use, and to polynomials with rational coefficients, where a product with an integer can be replaced by additions. Brent and Kung used the same splitting in 1978 for composition of power series and of polynomials modulo a polynomial. The idea also appears in multiprecision libraries as rectangular splitting for elementary functions.

## References
