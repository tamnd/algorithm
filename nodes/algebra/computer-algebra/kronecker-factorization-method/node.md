---
tag: 9JH5VC
kind: algorithm
slug: kronecker-factorization-method
name: Kronecker's factorization method
aliases:
- Kronecker method for factoring
- Schubert-Kronecker method
- factorization by interpolation of divisors
area: algebra/computer-algebra
level: advanced
summary: Factors univariate integer polynomials by interpolating at integer points and searching divisors.
solves: [polynomial-factorization-over-integers]
model: word-ram
complexity:
  vars: {d: the degree of f, k: the largest number of positive divisors of a value f(a_i)}
  time: {worst: O(d^3 (2k)^(d/2 + 1))}
  space: {extra: O(d^2)}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  year: 1882
  people: [Leopold Kronecker, Friedrich Theodor von Schubert]
  note: Kronecker gave the method in 1882 as a proof that factorization in Z[x] is computable; Schubert had described the same idea in 1793.
prereqs: [polynomial-factorization, lagrange-interpolation, divisor, polynomial-long-division, primitive-polynomial]
see_also: [polynomial-factorization-over-integers, zassenhaus-algorithm, hensel-lifting, lll-algorithm, rational-root-theorem, kronecker-substitution, enumerating-divisors, integer-factorization]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 4.6.2, Factorization of polynomials (factoring over the integers, with Kronecker's method and its history)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 15 and Chapter 16, Hensel lifting and factoring polynomials over the integers (the modern algorithms that replace Kronecker's method, with historical notes)
  - paper: "Leopold Kronecker, Grundzüge einer arithmetischen Theorie der algebraischen Grössen, Journal für die reine und angewandte Mathematik 92, 1882"
    locator: the finite procedure for factoring a polynomial with integer coefficients
---

Kronecker's method factors a polynomial $f \in \mathbb{Z}[x]$ with a finite search. If $g$ is a factor of degree $e$, then $g(a)$ divides $f(a)$ for every integer $a$. Pick $e + 1$ integers $a_0, \ldots, a_e$ with $f(a_i) \ne 0$. Each value $g(a_i)$ is one of the finitely many divisors of $f(a_i)$, and $e + 1$ values determine $g$ by [Lagrange interpolation](/lagrange-interpolation/). So trying every tuple of divisors, interpolating, and testing divisibility finds every factor of degree $e$, or proves there is none. Running $e = 1, 2, \ldots, \lfloor d/2 \rfloor$ yields the complete factorization. The method shows that factoring in $\mathbb{Z}[x]$ is computable, but the number of tuples grows exponentially with the degree. Practical systems use the [Zassenhaus algorithm](/zassenhaus-algorithm/) with [Hensel lifting](/hensel-lifting/), or [lattice reduction](/lll-algorithm/) for a polynomial-time bound.

## In plain words

Suppose a polynomial splits as a product of two smaller ones. Plug in a whole number: the value of the polynomial splits as a product of the two smaller values. A whole number has only finitely many divisors, so each small factor can take only finitely many values there. Do this at enough points, try every combination of divisors, and rebuild a candidate polynomial through those values. If a candidate divides the original, you have found a factor. If no combination works, there is no factor of that degree. This always finishes, but the number of combinations grows very fast, so the method is only practical for small degrees.

## The problem

**Input.** A primitive polynomial $f \in \mathbb{Z}[x]$ of degree $d \ge 1$ with a positive leading coefficient. Here $\mathbb{Z}$ is a ring, and a general $f$ is first split into its content, an integer, and its primitive part.

**Output.** Irreducible polynomials $g_1, \ldots, g_r \in \mathbb{Z}[x]$ of positive degree and positive leading coefficient with $f = g_1 \cdots g_r$. By Gauss's lemma these are also the irreducible factors of $f$ over $\mathbb{Q}$, up to constants. See [factoring over the integers](/polynomial-factorization-over-integers/).

## The algorithm

The search runs over the degree $e$ of the smallest factor not yet found. Any factor of degree $e$ that it finds is irreducible, because $f$ has no nonconstant factor of smaller degree at that point. Fixing $g(a_0) > 0$ removes the sign ambiguity between $g$ and $-g$.

```pseudo id=main
KRONECKER(f)                           ▷ f ∈ Z[x] primitive, lc f > 0
L1  factors ← [];  e ← 1
L2  while 2e ≤ deg f do
L3      choose distinct integers a_0, ..., a_e with f(a_i) ≠ 0
L4      D_0 ← positive divisors of f(a_0);  D_i ← ± divisors of f(a_i) for i ≥ 1
L5      for each (δ_0, ..., δ_e) in D_0 × ... × D_e do
L6          g ← the polynomial of degree ≤ e with g(a_i) = δ_i for all i
L7          if g ∈ Z[x], deg g = e and g divides f then leave the loop with g
L8      if a factor g was found then append g, with lc g > 0, to factors;  f ← f / g
L9      else e ← e + 1                          ▷ f has no factor of degree e
L10 if deg f ≥ 1 then append f to factors        ▷ no factor of degree ≤ deg f / 2
L11 return factors
```

Line L3 needs $e + 1$ integers that are not roots of $f$, which exist because $f$ has at most $d$ roots. The implementation takes candidates $0, \pm 1, \pm 2, \ldots$ and prefers those where $f(a)$ has few divisors, which keeps the product at line L5 small. Line L7 checks integrality and the exact degree before the more expensive trial division.

## Example

Factor $f = x^4 + 4$. The implementation picks the points $1$ and $-1$ for $e = 1$, where $f$ takes the value $5$, and adds $0$ for $e = 2$, where $f(0) = 4$.

| $e$ | points | values $f(a_i)$ | tuples | result |
|---|---|---|---|---|
| 1 | $1, -1$ | $5, 5$ | $2 \cdot 4 = 8$ tried; $6$ give integer $g$ of degree $1$; none divides $f$ | no linear factor, $e \leftarrow 2$ |
| 2 | $1, -1, 0$ | $5, 5, 4$ | $2 \cdot 4 \cdot 6 = 48$ in all; the $8$th, $(1, 5, 2)$, gives $g = x^2 - 2x + 2$, which divides $f$ | append $x^2 - 2x + 2$, $f \leftarrow x^2 + 2x + 2$ |
| 2 | | | $2e = 4 > \deg f = 2$, so the loop ends | append $x^2 + 2x + 2$ |

So $x^4 + 4 = (x^2 - 2x + 2)(x^2 + 2x + 2)$, the identity of Sophie Germain. The polynomial has no rational root, so the rational root test alone would not find this factorization.

## Correctness

If $f = g h$ in $\mathbb{Z}[x]$ with $\deg g = e$, then $f(a_i) = g(a_i) h(a_i)$, so $g(a_i)$ is a nonzero divisor of $f(a_i)$. Replacing $g$ by $-g$ if needed makes $g(a_0) > 0$. So $(g(a_0), \ldots, g(a_e))$ is one of the tuples of line L5, and since a polynomial of degree at most $e$ is determined by $e + 1$ values, line L6 rebuilds exactly $g$. Hence line L7 succeeds for some tuple whenever $f$ has a factor of degree $e$, and only for true factors. The invariant "$f$ has no nonconstant factor of degree less than $e$" then shows that each appended factor is irreducible. The full proof is in the proof file below.

## Complexity

The cost model is the word RAM, counting arithmetic operations on integers. The integers involved, the values $f(a_i)$, their divisors and the interpolated coefficients, have size polynomial in $d$ and the size of $f$, so each operation costs a polynomial number of word operations, which the count below does not show. Let $k$ be the largest number of positive divisors of a value $f(a_i)$. These bounds are proved:

- **Tuples.** For degree $e$ there are at most $k (2k)^{e}$ tuples, and $e \le d/2$.
- **Per tuple.** Interpolation costs $O(e^2)$ operations on rationals, and trial division $O(de)$ operations.
- **Total.** At most $d$ rounds of the outer loop, each at most $(2k)^{d/2 + 1}$ tuples costing $O(d^2)$, give $O(d^3 (2k)^{d/2 + 1})$ operations, and $O(d^2)$ extra space for the interpolation.

On top of this, line L4 must factor the integers $f(a_i)$, which costs time exponential in their length by trial division. The search is exponential in $d$ even when $k$ is small: with $k = 2$, as for prime values, an irreducible $f$ of degree $d$ needs about $4^{d/2}$ tuples. In practice the method is usable only up to degree about $6$ to $10$, an observation that depends on the coefficients. The [Zassenhaus algorithm](/zassenhaus-algorithm/) is exponential only in the number of modular factors, and lattice reduction gives a polynomial-time algorithm.

## Properties

- **Complete.** It finds every factorization, so it proves irreducibility when it finds nothing.
- **Deterministic.** The points and the order of the tuples are fixed.
- **Exponential.** Both the divisor search and the factoring of the values $f(a_i)$ are exponential.
- **Generalizes.** By [Kronecker substitution](/kronecker-substitution/) $x_2 = x_1^N$, a multivariate polynomial becomes univariate, so the method also factors in $\mathbb{Z}[x_1, \ldots, x_n]$, which was Kronecker's purpose.

## Variants and improvements

- **Good points.** Choose points where $|f(a)|$ is small or prime, so that $k$ is small. Points with $f(a) = \pm 1$ or a prime help most.
- **More points than needed.** Use more than $e + 1$ points and keep only tuples consistent with all of them, which rejects many candidates before interpolation.
- **Degree $1$.** For $e = 1$ the method reduces to the [rational root theorem](/rational-root-theorem/): a linear factor $qx - p$ needs $p \mid f(0)$ and $q \mid \operatorname{lc} f$.
- **Bounds on coefficients.** Mignotte's bound limits the coefficients of a factor, which rules out tuples whose interpolant is too large.
- **Modern replacement.** Factor modulo a prime, lift with [Hensel lifting](/hensel-lifting/), and recombine, as in the [Zassenhaus algorithm](/zassenhaus-algorithm/), or recombine with [LLL](/lll-algorithm/) as in van Hoeij's method.

## When to use it

Use it for teaching, for very small degrees, and as a reference oracle when testing faster factoring code. It needs only integer arithmetic, divisor enumeration and interpolation. For anything beyond small degrees use the modular methods of [polynomial factorization over the integers](/polynomial-factorization-over-integers/).

## Pitfalls

- **Forgetting negative divisors.** A factor can take negative values. Only one value may be restricted to positive divisors, to remove the $\pm g$ symmetry.
- **Roots among the points.** If $f(a) = 0$, every integer divides $f(a)$ and the search is infinite. Skip roots, or split off $x - a$ first.
- **Accepting non-integral interpolants.** The interpolant through integer values can have rational coefficients, and it is then not a factor in $\mathbb{Z}[x]$.
- **Searching all degrees.** Factors of degree above $d/2$ are cofactors of smaller ones. Searching them only doubles the work.
- **Content.** A non-primitive $f$ has constant factors, and $f = 2x + 2$ would otherwise yield the factor $2$ of degree $0$. Remove the content first.

## Implementations

## History

Schubert described the method in 1793, and Kronecker rediscovered it and published it in 1882, as part of his program of making algebra finite and constructive. Knuth, in Section 4.6.2, gives the method together with this history. It was the standard proof that factoring in $\mathbb{Z}[x]$ is decidable until the modular algorithms of Berlekamp (1967) and Zassenhaus (1969) made factoring practical, and Lenstra, Lenstra and Lovász (1982) made it polynomial time.

## References
