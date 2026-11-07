---
tag: VW4WSE
kind: algorithm
slug: fast-multipoint-evaluation
name: Fast multipoint evaluation
aliases:
- subproduct-tree evaluation
- remainder tree evaluation
area: algebra/polynomial-arithmetic
level: advanced
summary: Evaluates a polynomial at n points in O(M(n) log n) by remainder descent down the subproduct tree.
solves: [multipoint-evaluation]
model: blum-shub-smale-machine
complexity:
  vars: {n: "the number of points, which also bounds the number of coefficients of f", M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(M(n) log n), best: O(M(n) log n)}
  space: {extra: O(n log n)}
  ring_operations: {worst: 11M(n)(log2 n + 1) + O(n log n)}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1972
  people: [Robert T. Moenck, Allan Borodin, Charles M. Fiduccia]
  note: Fiduccia (1972) and Moenck and Borodin (1972) reduced evaluation at many points to divisions by products of linear factors; with fast division this gives O(M(n) log n).
prereqs: [multipoint-evaluation, fast-polynomial-division, horner-rule]
see_also: [subproduct-tree, fast-interpolation, newton-power-series-inversion, fft-polynomial-multiplication, evaluation-interpolation-paradigm, pollard-strassen, factorial-modulo-prime, reed-solomon-code]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 10.1, Fast multipoint evaluation (the subproduct tree and the descent of remainders); Section 9.1, Division with remainder using Newton iteration
  - paper: doi:10.1145/860854.860870
    title: Alin Bostan, Gregoire Lecerf and Eric Schost, Tellegen's principle into practice, Proceedings of ISSAC 2003, 37-44
    locator: the transposed algorithms for multipoint evaluation and their constants
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of polynomials
---

Fast multipoint evaluation computes $f(u_0), \ldots, f(u_{n-1})$ for a polynomial $f$ of degree less than $n$ with $O(M(n) \log n)$ ring operations, instead of the $\Theta(n^2)$ of Horner's rule at each point. It builds the subproduct tree of the linear factors $x - u_i$ and then walks down the tree: at each node it replaces the polynomial by its remainder modulo the node, which keeps the values at the points below the node. At a leaf $x - u_i$ the remainder is the constant $f(u_i)$. With FFT multiplication the cost is $O(n \log^2 n)$.

Notation: $R$ is a commutative ring with $1$, a polynomial is the list of its coefficients with the constant term first, and $M(n)$ is the cost of multiplying two polynomials of degree less than $n$ over $R$. We assume that $M(k)/k$ is nondecreasing and that $M(2k) \le 4M(k)$, as von zur Gathen and Gerhard do. Costs count ring operations in the algebraic complexity model. $R$ need not be a field: every divisor is monic.

## In plain words

The value of a polynomial at a number is the remainder after dividing by x minus that number. The remainder also stays correct if you first divide by a bigger polynomial that has this number as a root, and then divide the remainder again. The method uses this. It first multiplies the factors x minus each number in pairs, then the pairs in pairs, and so on, which gives a tree of products. Then it starts at the top: it divides the polynomial by the product of all factors, then each remainder by the two products of the halves, and so on down the tree. The remainders get smaller at each step. At the bottom, each remainder is a single number, the wanted value.

## The problem

**Input:** $f \in R[x]$ and points $u_0, \ldots, u_{n-1} \in R$, with $n \ge 0$. The usual case is $\deg f < n$; the algorithm accepts any degree.

**Output:** the list $f(u_0), \ldots, f(u_{n-1})$.

This is [multipoint evaluation](/multipoint-evaluation/). The points need not be distinct.

## The algorithm

The **subproduct tree** of the points has the leaves $m_{0,i} = x - u_i$ at level $0$. Node $k$ of level $j + 1$ is the product of nodes $2k$ and $2k + 1$ of level $j$; if level $j$ has an odd number of nodes, its last node is copied up without change. The top level has one node, $m = \prod_i (x - u_i)$, and there are $h = \lceil \log_2 n \rceil$ levels above the leaves. Every node is monic, and the nodes at one level are pairwise products over disjoint sets of points.

```pseudo id=main
FAST-MULTIPOINT-EVAL(f, u_0, ..., u_{n−1})
L1  if n = 0 then return the empty list
L2  build the subproduct tree; levels 0, ..., h; m_{h,0} = ∏ (x − u_i)
L3  r ← [f mod m_{h,0}]
L4  for j ← h − 1 down to 0 do
L5      r' ← empty list
L6      for each node k of level j do                ▷ its parent is node ⌊k/2⌋
L7          append r[⌊k/2⌋] mod m_{j,k} to r'
L8      r ← r'
L9  return the constant terms of r, in order
```

Each remainder in line L7 is a division with remainder by a monic polynomial, done by [fast polynomial division](/fast-polynomial-division/) with Newton inversion. If the dividend already has smaller degree than the divisor, there is nothing to do; this happens for a node copied up without a sibling and, when $\deg f < n$, at line L3.

## Example

Evaluate $f = 5x^4 + 4x^3 + 3x^2 + 2x + 1$ at $0, 1, 2, 3, 4$ over $\mathbb{Z}$. The subproduct tree, with the remainders that the descent computes next to each node:

| level | nodes | remainders |
|---|---|---|
| 3 | $x^5 - 10x^4 + 35x^3 - 50x^2 + 24x$ | $f$ itself, since $\deg f < 5$ |
| 2 | $x^4 - 6x^3 + 11x^2 - 6x$, and $x - 4$ copied up | $34x^3 - 52x^2 + 32x + 1$, and $1593$ |
| 1 | $x^2 - x$, $x^2 - 5x + 6$, and $x - 4$ | $14x + 1$, $418x - 707$, and $1593$ |
| 0 | $x$, $x - 1$, $x - 2$, $x - 3$, $x - 4$ | $1$, $15$, $129$, $547$, $1593$ |

At level 2, $f \bmod (x^4 - 6x^3 + 11x^2 - 6x)$ is $f - 5 \cdot (x^4 - 6x^3 + 11x^2 - 6x)$, since the quotient is the constant $5$. The node $x - 4$ is copied up from level 0, so its remainder is $f(4) = 1593$ already at level 2. At level 1, $14x + 1$ has the values $1$ and $15$ at $0$ and $1$, and $418x - 707$ has the values $129$ and $547$ at $2$ and $3$. Horner's rule gives the same five values $1, 15, 129, 547, 1593$. A script produced the table from the implementation.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The invariant is: after the remainders for level $j$ are computed, the remainder at node $k$ of level $j$ has the same value as $f$ at every point below that node, and has degree less than the degree of the node. It holds at the top by the definition of the remainder, since $f - (f \bmod m)$ is a multiple of $m$ and $m$ vanishes at every point. It passes from a node to a child because the child divides the node, so the child also vanishes at the points below it. At a leaf $x - u_i$, a polynomial of degree less than $1$ is a constant, and that constant is $f(u_i)$.

## Complexity

All bounds count ring operations in the algebraic complexity model and are proved under the assumptions on $M$ stated above.

- **The tree.** At each level, the products have operands whose numbers of coefficients sum to at most $2n$, so the level costs at most $M(2n) \le 4M(n)$. With $h = \lceil \log_2 n \rceil$ levels, the tree costs at most $4M(n) \lceil \log_2 n \rceil$.
- **The descent.** Let a node of degree $D$ have children of degrees $d_1 + d_2 = D$. Its remainder has degree less than $D$, so dividing it by the first child needs a quotient of at most $d_2$ coefficients, and by the [cost theorem for fast division](/fast-polynomial-division/) this costs at most $6M(d_2) + M(d_1) + O(D)$. The two children together cost at most $7M(d_1) + 7M(d_2) + O(D) \le 7M(D) + O(D)$, and a level costs at most $7M(n) + O(n)$.
- **Total.** At most $11 M(n) \lceil \log_2 n \rceil + O(n \log n)$, that is $O(M(n) \log n)$.

The constant 11 is a safe bound from this proof, not the best known. Von zur Gathen and Gerhard, Section 10.1, give a smaller one, and the transposed algorithm of Bostan, Lecerf and Schost lowers it further.

**Space.** The tree holds $n + 1$ coefficients per level, so $O(n \log n)$ ring elements. The descent needs $O(n)$ more.

| multiplication | $M(n)$ | fast multipoint evaluation |
|---|---|---|
| schoolbook | $\Theta(n^2)$ | $\Theta(n^2)$, slower than Horner's rule |
| Karatsuba | $O(n^{\log_2 3})$ | $O(n^{\log_2 3})$, since the levels form a geometric series |
| FFT over a ring with suitable roots of unity | $O(n \log n)$ | $O(n \log^2 n)$ |

**In practice (observed).** Horner's rule at each point costs about $n^2$ multiplications with a very small constant, so it is faster for small $n$. The crossover depends on the ring, the multiplication and the machine, and implementations find it by measurement. Most of the time is spent in the top few levels, where the polynomials are large. A common speedup is to stop the descent at nodes of small degree and use Horner's rule there.

## Properties

- **Exact.** Over $\mathbb{Z}$, $\mathbb{Z}/m\mathbb{Z}$ or $\mathbb{Q}$, the values are exact.
- **No inversions in $R$.** Every divisor is monic, so the method works over any commutative ring, including $\mathbb{Z}$ and $\mathbb{Z}/m\mathbb{Z}$ with composite $m$.
- **The tree depends only on the points.** For many polynomials and the same points, the tree and the inverses for the divisions can be computed once.
- **Repeated points are allowed.** The invariant does not need the points to be distinct.
- **Not numerically stable.** Over floating point numbers, the remainders in the top levels have huge coefficients for most point sets, and the values lose all accuracy.

## Variants and improvements

- **Stopping early.** At nodes of degree below a cutoff, evaluate the remainder by [Horner's rule](/horner-rule/) at each point below the node.
- **Transposed evaluation.** Bostan, Lecerf and Schost compute the transpose of the power sum problem by the transposition principle; the resulting algorithm uses middle products instead of divisions and has a smaller constant.
- **Scaled remainder trees.** Instead of the remainders, carry the truncated power series $f / m$ down the tree, which replaces each division by one middle product. Bernstein gives this form for integers as the [scaled remainder tree](/scaled-remainder-tree/).
- **Fast interpolation.** The same tree, used upward with linear combinations, gives [fast interpolation](/fast-interpolation/) and fast Chinese remaindering in $O(M(n) \log n)$.
- **Special points.** At roots of unity, the [FFT](/fast-fourier-transform/) costs $O(n \log n)$; at a geometric progression, the chirp z-transform costs $O(M(n))$.
- **General moduli.** The same descent computes $f \bmod m_i$ for any monic $m_i$, not only linear ones, which is the first half of fast Chinese remaindering.

## When to use it

Use it to evaluate a polynomial of large degree at many arbitrary points, when fast multiplication is available, for example inside [Pollard-Strassen](/pollard-strassen/) factoring, [factorials modulo a prime](/factorial-modulo-prime/), and modular algorithms that evaluate and interpolate. For a few points or small degree, use [Horner's rule](/horner-rule/). For roots of unity, use the FFT. Over floating point numbers, do not use it for general points.

## Pitfalls

- **Recursion in the descent.** A recursive descent is natural, and its depth is only $\lceil \log_2 n \rceil$; but the tree must be stored or rebuilt, and the iterative version by levels is simpler. The implementation builds the levels in a loop.
- **An odd number of nodes.** A node without a sibling must be carried up unchanged, and its remainder then passes down unchanged too. Pairing it with a dummy factor would add a wrong point.
- **Dividing when not needed.** If the dividend already has smaller degree than the divisor, the remainder is the dividend; calling the division then costs time and, in some implementations, fails on a quotient of negative length.
- **The degree of $f$.** If $\deg f \ge n$, line L3 must do a real division. Skipping it gives wrong values.
- **Floating point.** Over $\mathbb{R}$, the coefficients of $\prod (x - u_i)$ grow exponentially for points spread over an interval, so this method is useless there without special care.

## Implementations

## History

Borodin and Munro, Fiduccia, and Moenck and Borodin observed around 1972 that evaluation at many points is a sequence of divisions with remainder by products of linear factors. Combined with division in $O(M(n))$ by Newton inversion, which Sieveking and Kung found at the same time, this gives $O(M(n) \log n)$. Strassen in 1973 proved a lower bound of $\Omega(n \log n)$ nonscalar operations for the problem. The textbook form with the subproduct tree is in von zur Gathen and Gerhard, Chapter 10, and Bostan, Lecerf and Schost improved the constant in 2003 with the transposition principle.

## References
