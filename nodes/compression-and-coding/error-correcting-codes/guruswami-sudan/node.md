---
tag: S3KZM9
kind: algorithm
slug: guruswami-sudan
name: Guruswami-Sudan algorithm
aliases:
- list decoding of Reed-Solomon codes
- Guruswami-Sudan list decoder
- Sudan list decoder
area: compression-and-coding/error-correcting-codes
level: research
summary: "List decoder for Reed-Solomon codes: interpolate a bivariate polynomial with zeros of multiplicity r at the received points, then find its y-roots. Corrects up to n - sqrt(n(k-1)) errors."
solves: [list-decoding]
model: word-ram
complexity:
  vars: {n: the code length, k: the dimension, r: the multiplicity, p: the field size}
  time: {worst: O(n^3 r^6 + p n r^2)}
  space: {extra: Θ(n^2 r^4)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1999
  people: [Venkatesan Guruswami, Madhu Sudan]
  note: Sudan gave the decoder with simple zeros in 1997; Guruswami and Sudan added multiplicities in 1999 and reached the Johnson radius.
prereqs: [list-decoding, reed-solomon-code, berlekamp-welch]
see_also: [reed-solomon-decoding, gaussian-elimination, hermite-interpolation, multivariate-interpolation, polynomial-factorization-over-finite-fields, concatenated-codes, hadamard-code, locally-decodable-codes]
sources:
  - paper: doi:10.1006/jcom.1997.0439
    title: M. Sudan, Decoding of Reed Solomon codes beyond the error-correction bound, Journal of Complexity 13(1), 1997
    locator: The interpolation of a bivariate polynomial with simple zeros and the factoring step, with the agreement bound of about sqrt(2kn)
  - paper: doi:10.1109/18.782097
    title: V. Guruswami and M. Sudan, Improved decoding of Reed-Solomon and algebraic-geometry codes, IEEE Transactions on Information Theory 45(6), 1999
    locator: The interpolation with multiplicities and the condition t > sqrt(kn) for polynomials of degree at most k
  - paper: doi:10.1109/18.817522
    title: R. M. Roth and G. Ruckenstein, Efficient decoding of Reed-Solomon codes beyond half the minimum distance, IEEE Transactions on Information Theory 46(1), 2000
    locator: The recursive algorithm that finds the y-roots of Q(x, y) one coefficient at a time
  - url: https://cse.buffalo.edu/faculty/atri/courses/coding-theory/book/
    title: V. Guruswami, A. Rudra and M. Sudan, Essential Coding Theory (book draft)
    locator: The chapter on the list decoding of Reed-Solomon codes (Sudan's algorithm, multiplicities and the Johnson bound)
---

The Guruswami-Sudan algorithm is a polynomial time [list decoder](/list-decoding/) for [Reed-Solomon codes](/reed-solomon-code/). A codeword is $(f(a_1), \ldots, f(a_n))$ for a message polynomial $f$ of degree less than $k$. Classical decoders, such as [Berlekamp-Welch](/berlekamp-welch/), correct at most $\lfloor (n-k)/2 \rfloor$ errors. The Guruswami-Sudan algorithm outputs every message whose codeword is within distance $e$ of the received word, for every $e < n - \sqrt{n(k-1)}$. It has two steps. First it finds a nonzero bivariate polynomial $Q(x, y)$ of low weighted degree that has a zero of multiplicity $r$ at each received point $(a_i, y_i)$. This is a linear system. Then it finds all factors $y - f(x)$ of $Q$ with $\deg f < k$. Sudan's algorithm of 1997 is the case $r = 1$.

## In plain words

The sender evaluates a short polynomial at many points. Many values change on the way, so many that more than one message can explain what arrives. The decoder draws one curve in the plane that goes through every received point. The curve is described by a polynomial in two variables, kept small in degree. Any message that matches enough of the points must lie fully on this curve, because a small polynomial cannot have too many zeros without being zero. So the decoder takes the curve apart into its pieces and reads off each message that is a piece. If the curve passes through each point several times, it can be a bit larger, and it catches messages that match fewer points. The result is a short list in place of one answer.

## The problem

The input is a prime field $\mathbb{F}_p$ (any finite field works the same way), $n$ distinct points $a_1, \ldots, a_n$, a received word $y_1, \ldots, y_n$, the dimension $k$ with $2 \le k \le n$, and a multiplicity $r \ge 1$. The output is every polynomial $f$ with $\deg f < k$ that agrees with the received word in at least $t$ places, that is $f(a_i) = y_i$ for at least $t$ indices $i$. The decoder sets $t$ from $n$, $k$ and $r$, and the radius is $e = n - t$.

The *$(1, k-1)$-weighted degree* of the monomial $x^i y^j$ is $i + (k-1) j$. It is chosen so that $x^i f(x)^j$ has degree at most $i + (k-1)j$. Let $N(D)$ be the number of monomials of weighted degree at most $D$:

$$N(D) = \sum_{j=0}^{\lfloor D/(k-1) \rfloor} \bigl(D - j(k-1) + 1\bigr).$$

$Q$ has a zero of multiplicity $r$ at $(a, b)$ if $Q(x + a, y + b)$ has no monomial of total degree less than $r$. The coefficient of $x^u y^v$ in $Q(x+a, y+b)$ is the Hasse derivative

$$Q^{[u,v]}(a, b) = \sum_{i, j} \binom{i}{u} \binom{j}{v} q_{ij} \, a^{i-u} b^{j-v},$$

which is linear in the coefficients $q_{ij}$ of $Q$. So one point gives $r(r+1)/2$ linear conditions, one for each $(u, v)$ with $u + v < r$.

## The algorithm

```pseudo id=main
GURUSWAMI-SUDAN(a_1 .. a_n, y_1 .. y_n, k, r)    ▷ every f with deg f < k and agreement at least t
L1  D ← the least integer with N(D) > n r (r + 1)/2
L2  t ← ⌊D / r⌋ + 1
L3  find Q ≠ 0 of (1, k − 1)-weighted degree at most D with Q^[u,v](a_i, y_i) = 0 for all i and all u + v < r
L4  C ← all f with deg f < k such that y − f(x) divides Q(x, y)    ▷ Roth-Ruckenstein
L5  keep the f in C that agree with y in at least t places
L6  return the kept list
```

Line L3 is a homogeneous linear system with $n r (r+1)/2$ equations and $N(D)$ unknowns. Line L1 makes the unknowns more than the equations, so [Gaussian elimination](/gaussian-elimination/) finds a nonzero solution.

Line L4 uses the recursion of Roth and Ruckenstein. Write $f = f_0 + f_1 x + \cdots + f_{k-1} x^{k-1}$. If $y - f(x)$ divides $Q$, then $f_0$ is a root of $Q(0, y)$, after $Q$ has been divided by the highest power of $x$ that divides it. For each root $\gamma$ of $Q(0, y)$, the recursion goes on with

$$Q'(x, y) = Q(x, x y + \gamma),$$

whose factors $y - g(x)$ match the factors $y - (\gamma + x g(x))$ of $Q$. The coefficient of $y^l$ in $Q'$ is $x^l \sum_{j \ge l} \binom{j}{l} \gamma^{j-l} Q_j(x)$, where $Q_j$ is the coefficient of $y^j$ in $Q$. After $k$ levels, each path gives one candidate $f$. The roots of $Q(0, y)$ are univariate roots over the field. The implementation here tries all $p$ elements, which is fine for a small field. For a large field, a root finding method for polynomials over finite fields takes this place.

Line L5 is needed because $Q$ can have factors $y - f(x)$ that agree with $y$ in fewer than $t$ places. They are correct factors but not part of the promised list.

## Example

Take $\mathbb{F}_7$, the points $1, 2, 3, 4, 5, 6$, and $k = 2$, so the messages are lines $f = f_0 + f_1 x$. The code has $n = 6$ and minimum distance $5$, so unique decoding corrects $2$ errors. The received word is

$$y = (0, 0, 0, 4, 5, 6).$$

The line $f = 0$ agrees in the first three places, and the line $f = x$ agrees in the last three. Both are at distance $3$.

**Sudan, $r = 1$.** There are $6$ conditions. $N(2) = 6$ and $N(3) = 10$, so $D = 3$ and $t = 4$. Sudan's decoder promises only the lines with $4$ or more agreements. There are none, so its list is empty.

**Guruswami-Sudan, $r = 2$.** Each point gives $3$ conditions, so there are $18$. $N(4) = 15$ and $N(5) = 21$, so $D = 5$ and $t = \lfloor 5/2 \rfloor + 1 = 3$. The radius is now $3$. One valid interpolation polynomial is

$$Q(x, y) = y^2 (y - x)^2.$$

Its weighted degree is $4 \le 5$. At the points $(1, 0), (2, 0), (3, 0)$ the factor $y^2$ has a double zero, and at $(4, 4), (5, 5), (6, 6)$ the factor $(y - x)^2$ has a double zero. (The linear system has a solution space of dimension at least $3$, so an implementation can find a different $Q$. The output list is the same.)

The root search runs as follows.

| level | polynomial | after division by $x^m$ | roots of $Q(0, y)$ |
|---|---|---|---|
| 0 | $y^2 (y - x)^2$ | $y^2 (y - x)^2$ | $\gamma = 0$ |
| 1 | $Q(x, xy) = x^4 y^2 (y - 1)^2$ | $y^2 (y - 1)^2$ | $\gamma = 0$ and $\gamma = 1$ |

The two paths give $(f_0, f_1) = (0, 0)$ and $(0, 1)$, that is $f = 0$ and $f = x$. Both agree in $3 \ge t$ places, so the list is $\{0, x\}$. A brute force search over all $49$ lines gives the same list.

## Correctness

The proof has three parts. The full argument is in the proof file.

1. **A polynomial $Q$ exists.** The conditions of line L3 are linear and homogeneous, and line L1 makes the unknowns more than the equations. So a nonzero solution exists.
2. **Every good $f$ is a factor.** Let $f$ agree with $y$ in at least $t$ places, and let $R(x) = Q(x, f(x))$. The weighted degree bound gives $\deg R \le D$. At each agreeing point $a_i$, the multiplicity $r$ of $Q$ at $(a_i, f(a_i))$ makes $(x - a_i)^r$ divide $R$. So $R$ has at least $t r > D$ roots counted with multiplicity, and $R = 0$. Then $y - f(x)$ divides $Q(x, y)$.
3. **The root search finds every factor.** If $y - g(x)$ divides $Q$, then after the division by $x^m$, the constant $g(0)$ is a root of the nonzero polynomial $Q(0, y)$, and $y - (g(x) - g(0))/x$ divides $Q(x, xy + g(0))$. By induction on the level, the recursion follows the path of $g$ to the end.

Line L5 then keeps exactly the good $f$.

## Complexity

Let $m = N(D)$ be the number of unknowns. It is about $n r (r+1)/2 + 1$, so Gaussian elimination on the system of line L3 costs $O(m^3) = O(n^3 r^6)$ field operations and $O(m^2) = O(n^2 r^4)$ space.

The polynomial $Q$ has $y$-degree $L \le D/(k-1)$, and $D$ is about $r \sqrt{n (k-1)}$. Roth and Ruckenstein show that each level of the recursion has at most $L$ live paths. With a root search that tries all $p$ field elements, each path costs $O(pL)$ for the roots and a polynomial in $n$ and $r$ for the substitution. Over $k$ levels the root search costs $O(p n r^2)$, and the substitutions are dominated by the interpolation.

Faster interpolation methods replace the generic elimination. Koetter's algorithm builds $Q$ one condition at a time and keeps a small set of candidate polynomials, so it never forms the full matrix. Methods based on the basis reduction of polynomial matrices are faster still.

## Properties

- **Radius.** With multiplicity $r$, the decoder corrects up to $e_r = n - \lfloor D_r / r \rfloor - 1$ errors. As $r$ grows, $D_r / r$ tends to $\sqrt{n(k-1)}$, so the radius tends to the Johnson radius. The exact limit is: every $e < n - \sqrt{n(k-1)}$ is reached for a large enough $r$, and no $r$ goes beyond it. The largest integer radius is $n - \lfloor \sqrt{n(k-1)} \rfloor - 1$. In the notation of Guruswami and Sudan, where $f$ has degree at most $k$, the condition is $t > \sqrt{kn}$.
- **Sudan's radius.** With $r = 1$, $D$ is at most about $\sqrt{2n(k-1)}$, so Sudan's decoder needs an agreement of at most about $\sqrt{2nk}$. The exact count $N(D)$ shows that it beats unique decoding only at low rate, for $k/n$ below about $1/3$.
- **Relative radius.** For rate $R = k/n$, the fraction of errors tends to $1 - \sqrt{R}$, which is more than the unique decoding fraction $(1 - R)/2$ at every rate below $1$.
- **Small values.** For $n = 16$ over $\mathbb{F}_{17}$:

| $k$ | unique decoding | Sudan ($r = 1$) | $r = 2$ | limit |
|---|---|---|---|---|
| 2 | 7 | 10 ($D = 5$, $t = 6$) | 11 ($D = 9$, $t = 5$) | 11 |
| 4 | 6 | 7 ($D = 8$, $t = 9$) | 8 ($D = 15$, $t = 8$) | 8 |

- **List size.** Every output is a factor $y - f(x)$ of $Q$, so the list has at most $\deg_y Q \le D/(k-1)$ entries.
- **Deterministic.** Over a small field with the brute force root search, every step is deterministic. Over a large field, the fastest univariate root finders are randomized.

## Variants and improvements

- **Sudan's algorithm.** The case $r = 1$, published first. It is simpler, since every condition is a plain evaluation $Q(a_i, y_i) = 0$.
- **Berlekamp-Welch as a special case.** With $Q$ of degree $1$ in $y$, $Q = Q_0(x) + Q_1(x) y$, the method is the [Berlekamp-Welch](/berlekamp-welch/) decoder with $E = Q_1$, up to sign.
- **Algebraic soft decision decoding.** Koetter and Vardy let the multiplicity of each point depend on the reliability of the received symbol, and allow several candidate symbols per position.
- **Algebraic-geometry codes.** Guruswami and Sudan applied the same method to algebraic-geometry codes, with functions on a curve in place of polynomials.
- **Beyond the Johnson radius.** Parvaresh and Vardy used several related polynomials, and Guruswami and Rudra used folded Reed-Solomon codes, to list decode up to a fraction $1 - R - \varepsilon$ of errors. That is the list decoding capacity for large alphabets.
- **Fast root finding.** The Roth-Ruckenstein recursion is the usual method. Over large fields, the roots of $Q(0, y)$ come from a univariate root finder, for example by [factorization over finite fields](/polynomial-factorization-over-finite-fields/).

## When to use it

Use it when the channel can make more errors than half the minimum distance and a short list of candidates is useful, for example when a check sum or an outer code picks the right entry. It is also a standard tool in complexity theory, in proofs about hardness amplification and pseudorandomness, where the list decoding of polynomials is the key step. For a channel with few errors, a unique decoder such as [Berlekamp-Massey](/berlekamp-massey/) with Chien search and Forney is much faster.

## Pitfalls

- **The list can be empty.** If no codeword agrees in $t$ places, the output is empty. It does not mean that the received word has more than $n - t$ errors from every codeword. A word with $n - t + 1$ errors can still be found by chance, but the decoder does not promise it.
- **Line L5 is needed.** $Q$ can have factors $y - f(x)$ with less agreement than $t$. Without the filter, the output is not the promised list.
- **Divide by $x^m$ before the root search.** If $x$ divides $Q$, then $Q(0, y)$ is zero and every field element looks like a root. The division keeps the search finite and correct.
- **The weighted degree.** The degree bound is on $i + (k-1) j$, not on the total degree $i + j$. With the total degree, the bound $\deg Q(x, f(x)) \le D$ fails.
- **Multiplicity costs much more time.** The number of conditions grows like $r^2$, and the cost of elimination like $r^6$. A small $r$ often gives most of the gain. In the table above, $r = 2$ already reaches the limit.
- **Off by one in $k$.** Some texts use $k$ for the dimension and others for the degree bound. The limit is $n - \sqrt{n(k-1)}$ for the dimension $k$ and $n - \sqrt{nk}$ for the degree bound $k$.
- **$k = 1$.** With constant messages, the weight $k - 1$ is $0$ and the weighted degree no longer bounds the $y$-degree. Constant messages are decoded by a majority vote in any case.

## Implementations

## History

Before 1997, the known efficient decoders for Reed-Solomon codes stopped at half the minimum distance. Madhu Sudan showed in 1997 that a bivariate interpolation followed by a factorization step list decodes beyond that bound at low rate. The method grew out of the Berlekamp-Welch decoder, which is the case of degree $1$ in $y$, and out of earlier work on the reconstruction of polynomials from noisy values. Venkatesan Guruswami and Sudan added multiplicities in a paper published in 1999. This lifted the radius to $n - \sqrt{n(k-1)}$ at every rate, the Johnson radius for these codes, and the method also covered algebraic-geometry codes. Ron Roth and Gitit Ruckenstein gave the efficient recursive root finder in 2000. Koetter and Vardy turned the multiplicities into a soft decision decoder in 2003. Parvaresh and Vardy in 2005, and Guruswami and Rudra in 2008, went beyond the Johnson radius with related codes.

## References
