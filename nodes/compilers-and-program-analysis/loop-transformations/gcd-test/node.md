---
tag: M4BM5N
kind: algorithm
slug: gcd-test
name: GCD test
aliases:
- greatest common divisor dependence test
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Reports independence when the gcd of the coefficients of a linear subscript equation does not divide its constant term.
solves: [dependence-testing]
model: word-ram
complexity:
  vars: {m: the number of subscripts, k: the depth of the loop nest, C: the largest absolute value of a coefficient}
  time: {worst: O(m k log C), best: O(k)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [dependence-testing, greatest-common-divisor, bezouts-identity]
see_also: [banerjee-test, practical-dependence-tests, linear-diophantine-equation, extended-euclidean-algorithm, hermite-normal-form, dependence-direction-vector, omega-test]
sources:
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 3 (the GCD test for MIV subscripts, with direction vectors)
  - book: "Utpal Banerjee, Dependence Analysis for Supercomputing, Kluwer Academic Publishers, 1988"
    locator: the gcd test for one linear Diophantine equation and its generalization to systems
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 11.6 (the GCD test for linear Diophantine equations in array data-dependence analysis)
  - book: "Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996"
    locator: the chapter on dependence testing (the GCD test, with and without direction vectors)
---

The GCD test is the oldest and cheapest [dependence test](/dependence-testing/). Two references to an array, such as `A[2*i]` and `A[2*i + 1]`, touch the same element only if a linear equation in the loop indices has an integer solution. By [Bezout's identity](/bezouts-identity/), such an equation has an integer solution exactly when the [gcd](/greatest-common-divisor/) of its coefficients divides its constant term. The GCD test checks this one condition for each subscript. If it fails for some subscript, the references are independent. If it holds, the test says "maybe": it ignores the loop bounds, so a solution may exist only outside the iteration space.

## In plain words

Write the condition "both references touch the same element" as an equation. The unknowns are the loop indices of the two accesses, and they must be whole numbers. Every combination of the unknowns gives a multiple of the greatest common divisor of their coefficients, and no other values. So if the constant of the equation is not such a multiple, the equation has no whole-number solution at all, and the two references never meet. If the constant is a multiple, there is a solution somewhere, but maybe not inside the loops. The test then cannot rule the dependence out and says "maybe". It is cheap, it never answers wrongly in the safe direction, and it catches the classic case of even against odd positions.

## The problem

A loop nest of depth $k$ has two references to an array of $m$ dimensions. Dimension $r$ of the source has the subscript $a_{r0} + \sum_l a_{rl} i_l$, and the sink has $b_{r0} + \sum_l b_{rl} j_l$, with integer coefficients. A direction vector $\vec{\psi} \in \{<, =, >, *\}^k$ may restrict the pairs (this page uses Wolfe's notation: $<$ at level $l$ means $i_l < j_l$, see [direction vector](/dependence-direction-vector/)). The question is whether there are integer vectors $\vec{i}$, $\vec{j}$ in the loop bounds with

$$\sum_{l=1}^{k} a_{rl} i_l - \sum_{l=1}^{k} b_{rl} j_l = b_{r0} - a_{r0} \quad (r = 1, \dots, m)$$

and $i_l \,\psi_l\, j_l$ for each $l$. The GCD test answers "independent" or "maybe". It must never answer "independent" when such vectors exist.

## The algorithm

Let $E$ be the set of levels with $\psi_l$ equal to "=". At such a level the two indices are one variable, with coefficient $a_l - b_l$.

```pseudo id=main
GCD-TEST-SUBSCRIPT(a, b, psi):
L1  c <- b_0 - a_0
L2  g <- 0
L3  for l <- 1 to k do
L4      if psi_l = "=" then g <- gcd(g, a_l - b_l)
L5      else g <- gcd(g, a_l, b_l)
L6  if g = 0 then return ("maybe" if c = 0 else "independent")
L7  if c mod g != 0 then return "independent"
L8  return "maybe"

GCD-TEST(src, snk, psi):
L9  for each dimension r do
L10     if GCD-TEST-SUBSCRIPT(src_r, snk_r, psi) = "independent" then return "independent"
L11 return "maybe"
```

Line L6 handles a subscript pair that uses no index at all (a ZIV pair): the two subscripts are equal for all iterations or for none. The entries $<$, $>$ and $*$ are treated alike, because the gcd cannot use them (see Correctness).

A witness is easy to get when the answer is "maybe": the [extended Euclidean algorithm](/extended-euclidean-algorithm/), run over the coefficients one at a time, gives integers with $\sum_v \alpha_v x_v = G$, and multiplying by $c / G$ solves the equation. The implementation returns it from `solve_linear`.

## Example

```
for i = 1 to 10:
  for j = 1 to 10:
    A[3*i + 2*j] = A[i + 4*j + 1] + 1
```

The equation between the write in $(i, j)$ and the read in $(i', j')$ is $3i + 2j - i' - 4j' = 1$.

**With $\vec{\psi} = (*, *)$.** The gcd of $3, 2, 1, 4$ is $1$, which divides $1$. The answer is "maybe". The witness from the extended Euclidean algorithm is $(i, j, i', j') = (0, 0, -1, 0)$, outside the bounds, but there are also solutions inside, such as $(1, 2, 2, 1)$: $S(1, 2)$ writes $A[7]$ and $S(2, 1)$ reads $A[7]$.

**With $\vec{\psi} = (=, *)$.** Now $i = i'$, and the trace is:

| line | action | $g$ |
|---|---|---|
| L1 | $c = 1 - 0$ | |
| L2 | | $0$ |
| L4, $l = 1$ | $\psi_1$ is "=": add $a_1 - b_1 = 3 - 1 = 2$ | $2$ |
| L5, $l = 2$ | add $a_2 = 2$ and $b_2 = 4$ | $2$ |
| L7 | $1 \bmod 2 = 1$ | independent |

So no dependence has "=" at the outer level: every dependence of this loop is carried by the $i$ loop, and the $j$ loop can run in parallel for each $i$. Enumeration of the box confirms it: the 236 solutions have the direction vectors $(<, *)$ and $(>, *)$ only, never $(=, *)$.

**A case the test cannot decide.** For `A[2*i] = A[3*i + 2]` with $1 \le i \le 3$, the gcd of $2$ and $3$ is $1$, and the answer is "maybe". But the loop writes $A[2], A[4], A[6]$ and reads $A[5], A[8], A[11]$, so there is no dependence. The [Banerjee test](/banerjee-test/) also fails here; the exact SIV test of the [practical tests](/practical-dependence-tests/) succeeds.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has two parts.

**Exactness without bounds.** By [Bezout's identity](/bezouts-identity/) for $n$ variables, the values of $\sum_v \alpha_v x_v$ over integer vectors $\vec{x}$ are exactly the multiples of $G = \gcd(\alpha_1, \dots, \alpha_n)$. After the substitution $i_l = j_l$ for $l \in E$, the equation of one subscript has the coefficients $a_l - b_l$ for $l \in E$ and $a_l, -b_l$ for the other levels, and lines L2 to L5 compute their gcd. So the test answers "maybe" for a subscript exactly when its equation, with the "=" entries and nothing else, has an integer solution.

**Soundness.** A real dependence in the bounds with direction $\vec{\psi}$ solves this relaxed equation for every subscript. So every subscript gives "maybe", and so does the whole test. The answer "independent" is a proof of independence.

**Why $<$ and $>$ do not help.** Writing $j_l = i_l + \delta_l$ with $\delta_l \ge 1$ gives the coefficients $a_l - b_l$ and $b_l$, and $\gcd(a_l - b_l, b_l) = \gcd(a_l, b_l)$. The gcd is the same, and the inequality $\delta_l \ge 1$ is lost.

## Complexity

Each gcd of numbers at most $C$ in absolute value takes $O(\log C)$ division steps, and a subscript needs at most $2k$ of them. The whole test takes $O(m k \log C)$ time and $O(1)$ extra space. A test that stops at the first independent subscript can end after $O(k)$ steps when the gcds are small. A full search over direction vectors multiplies the cost by the number of vectors tested, at most $3^k$ and usually far fewer.

## Properties

- **Conservative in one direction only.** "Independent" is always right. "Maybe" can be wrong in the sense that no dependence exists.
- **Exact for one equation without bounds.** For a single subscript and no bounds it decides the question.
- **Blind to bounds and to $<$, $>$.** Only the "=" entries of a direction vector change the result.
- **One subscript at a time.** It does not combine the subscripts of a multidimensional reference, so it misses independence that only the system shows.
- **Weak in practice.** The gcd is often $1$, for instance whenever some coefficient is $\pm 1$, and then the test always says "maybe".

## Variants and improvements

- **Generalized GCD test.** Solve the whole system of $m$ equations at once over the integers, with the [Hermite normal form](/hermite-normal-form/) or the Smith normal form. This decides integer solvability of the system without bounds, so it catches coupled subscripts such as $A[i][i]$ against $A[j][j + 1]$. Banerjee's book gives this version.
- **Bounds after the gcd.** The general solution of one equation, from the witness and the kernel, is a lattice of points; intersecting it with the bounds is the exact SIV test for two variables. See [practical dependence tests](/practical-dependence-tests/).
- **Combined with Banerjee.** Compilers run the GCD test and the [Banerjee test](/banerjee-test/) on the same equation; each catches cases the other misses.
- **Exact integer tests.** The [omega test](/omega-test/) solves the full integer program, including bounds and directions.

## When to use it

Use it as the first test on a subscript pair with several indices, before more costly tests: it costs a few gcds and catches stride patterns such as even against odd elements. Do not rely on it alone. With loop bounds known, a solution outside the bounds is common, and the test cannot see it. For single-index subscripts, the exact SIV tests are just as cheap and stronger.

## Pitfalls

- **Answering "dependent" for "maybe".** The test proves only independence. A "maybe" means that the compiler must assume a dependence, not that one exists.
- **Dropping a nonzero constant in a ZIV pair.** If all coefficients are $0$, the gcd is $0$; the subscripts are equal only when the constants are equal. Treating $\gcd = 0$ as "divides everything" gives a wrong "maybe", which is safe, but treating it as "divides nothing" gives a wrong "independent" for $A[5]$ against $A[5]$, which is not safe.
- **Using the gcd of the "<" substitution as stronger.** Substituting $j_l = i_l + \delta_l$ does not change the gcd; only "=" does.
- **Testing each subscript and concluding about the system.** Each subscript of $A[i][i]$ against $A[j][j+1]$ passes, but the system has no solution. The test is still sound, just weak.
- **Symbolic terms.** A subscript such as `A[n*i]` with unknown $n$ has no integer coefficient; the test must treat the term as unknown and answer "maybe", or test with $n$ as an extra variable.

## Implementations

## History

The GCD test came out of the work on dependence analysis for parallelizing Fortran compilers at the University of Illinois in the 1970s, in the group of David Kuck. Utpal Banerjee's 1988 book states it with the bounds test that carries his name, and extends it to systems of equations with unimodular matrices. Allen and Kennedy and the dragon book present it as the basic test for subscripts with several indices.

## References
