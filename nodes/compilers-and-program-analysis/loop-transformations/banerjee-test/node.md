---
tag: PS0MQH
kind: algorithm
slug: banerjee-test
name: Banerjee test
aliases:
- Banerjee inequalities
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Reports independence when the constant of a subscript equation lies outside the real bounds of the equation over the loop bounds.
solves: [dependence-testing]
model: word-ram
complexity:
  vars: {m: the number of subscripts, k: the depth of the loop nest}
  time: {worst: O(m k), best: O(k)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [dependence-testing, dependence-direction-vector]
see_also: [gcd-test, practical-dependence-tests, fourier-motzkin-elimination, omega-test, integer-feasibility, loop-interchange, loop-carried-dependence, feautrier-array-dataflow]
sources:
  - book: "Utpal Banerjee, Dependence Analysis for Supercomputing, Kluwer Academic Publishers, 1988"
    locator: the bounds of a linear function over a rectangle with direction constraints, and the test built on them
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 3 (the Banerjee inequality with direction vectors, the positive and negative parts, and the hierarchical search for direction vectors)
  - book: "Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996"
    locator: the chapter on dependence testing (the Banerjee bounds for each direction, and the search over the direction vector hierarchy)
  - paper: "Gina Goff, Ken Kennedy and Chau-Wen Tseng, Practical dependence testing, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), 1991"
    locator: the Banerjee test as the general test for MIV subscripts, used after the exact single-index tests
---

The Banerjee test is a [dependence test](/dependence-testing/) that uses the loop bounds. For one subscript pair, it computes the smallest and the largest value that the left side of the dependence equation can take when every loop index runs over the real interval of its loop. If the constant of the equation lies outside that range, no pair of iterations can touch the same element, and the references are independent. The bounds have a closed form for each level and each direction ($<$, $=$, $>$ or $*$), so the test costs a few operations per loop and can refine a [direction vector](/dependence-direction-vector/) one level at a time. The range is exact over the reals but not over the integers, so the answer "maybe" can be wrong; the answer "independent" never is.

## In plain words

The two accesses touch the same element when some expression in the loop indices equals some constant. Each index can only take values inside its loop. So the expression has a smallest and a largest possible value, and both are easy to compute: for each loop, push the index to the end of its range that makes the term smallest, or largest. If the constant is below the smallest value or above the largest, the two accesses can never meet. The test can also ask the same question for pairs where the second access comes in a later, the same or an earlier iteration of each loop, which tells the compiler which loops carry the dependence. It works with fractions, not whole numbers, so it sometimes says "maybe" when the indices could only meet between two whole values.

## The problem

A rectangular loop nest of depth $k$ runs loop $l$ over $L_l \le i_l \le U_l$. Two references to an array of $m$ dimensions have the subscripts $a_{r0} + \sum_l a_{rl} i_l$ (source) and $b_{r0} + \sum_l b_{rl} j_l$ (sink). A direction vector $\vec{\psi} \in \{<, =, >, *\}^k$, in Wolfe's notation ($<$ at level $l$ means $i_l < j_l$, the sink runs in a later iteration of loop $l$), restricts the pairs. The question is whether there are integer $\vec{i}$, $\vec{j}$ in the bounds with $i_l \,\psi_l\, j_l$ and, for each dimension $r$,

$$\sum_{l=1}^{k} \bigl(a_{rl} i_l - b_{rl} j_l\bigr) = b_{r0} - a_{r0}.$$

The test answers "independent" or "maybe"; it must never answer "independent" when such vectors exist. The search over direction vectors returns the set of plain vectors that the test cannot rule out.

## The algorithm

Write $t^+ = \max(t, 0)$ and $t^- = \max(-t, 0)$, so $t = t^+ - t^-$, and $N = U - L$. For a strict direction the integer constraint $x < y$ becomes the real constraint $x + 1 \le y$.

```pseudo id=main
BANERJEE-TEST(a, b, L, U, psi):
L1  for each dimension r do
L2      c <- b_r0 - a_r0
L3      lo <- 0; hi <- 0
L4      for l <- 1 to k do
L5          range <- LEVEL-BOUNDS(a_rl, b_rl, L_l, U_l, psi_l)
L6          if range is empty then return "independent"
L7          lo <- lo + min(range); hi <- hi + max(range)
L8      if c < lo or c > hi then return "independent"
L9  return "maybe"

LEVEL-BOUNDS(a, b, L, U, d):        bounds of a*x - b*y over the region of d
L10 if d = "*" then return [a+ L - a- U - b+ U + b- L,  a+ U - a- L - b+ L + b- U]
L11 if d = "=" then e <- a - b; return [e+ L - e- U,  e+ U - e- L]
L12 if d = "<" then (empty if N < 1); v0 <- (a - b) L - b
        return [v0 - (a- + b)+ (N - 1),  v0 + (a+ - b)+ (N - 1)]
L13 if d = ">" then (empty if N < 1); v0 <- (a - b) L + a
        return [v0 - (b+ - a)+ (N - 1),  v0 + (a + b-)+ (N - 1)]
```

The region of a level is a rectangle for $*$, a diagonal segment for $=$, and a triangle for $<$ and $>$. The formulas are the extremes of $a x - b y$ over its corners: $(L, L+1)$, $(L, U)$ and $(U-1, U)$ for $<$, and $(L+1, L)$, $(U, L)$ and $(U, U-1)$ for $>$.

**Search over direction vectors.** Start with $(*, \dots, *)$. If the test says "maybe", replace the first $*$ by each of $<$, $=$, $>$ and test the three vectors; go on until no $*$ is left. A vector that tests "independent" is cut with all its refinements. The leaves are the direction vectors that the test cannot rule out.

## Example

The loop

```
for i = 1 to 4:
  for j = 1 to 4:
    X[i + 2*j] = X[i + 2*j - 1] + 1
```

has $a = (1, 2)$, $a_0 = 0$ for the write and $b = (1, 2)$, $b_0 = -1$ for the read, so $c = -1$. The left side is $(i - i') + 2(j - j')$, where $(i', j')$ is the iteration of the read. The search over directions gives these ranges:

| $\vec{\psi}$ | range of the left side | $-1$ inside? |
|---|---|---|
| $(*, *)$ | $[-9, 9]$ | yes, refine |
| $(<, *)$ | $[-9, 5]$ | yes, refine |
| $(<, <)$ | $[-9, -3]$ | no |
| $(<, =)$ | $[-3, -1]$ | yes |
| $(<, >)$ | $[-1, 5]$ | yes |
| $(=, *)$ | $[-6, 6]$ | yes, refine |
| $(=, <)$, $(=, =)$, $(=, >)$ | $[-6, -2]$, $[0, 0]$, $[2, 6]$ | no |
| $(>, *)$ | $[-5, 9]$ | yes, refine |
| $(>, <)$ | $[-5, 1]$ | yes |
| $(>, =)$, $(>, >)$ | $[1, 3]$, $[3, 9]$ | no |

The result is $\{(<, =), (<, >), (>, <)\}$, and enumeration of all $256$ pairs of iterations gives the same set, so here the test is exact. The vectors $(<, =)$ and $(<, >)$ are flow dependences from the write to the read, for example $(1, 1) \to (2, 1)$ and $(1, 2) \to (4, 1)$. The vector $(>, <)$ has the read first: it is an anti dependence from the read to the write, with direction $(<, >)$ after reversal, for example the read in $(1, 2)$ and the write in $(2, 1)$, both on $X[4]$. No vector starts with $=$, so the inner loop carries nothing and is parallel. The direction $(<, >)$ makes [loop interchange](/loop-interchange/) illegal.

**Independent by the bounds only.** For `A[i] = A[i + 10]` with $1 \le i \le 5$, the GCD test says "maybe" (the gcd is $1$), but $i - j$ lies in $[-4, 4]$ and $c = 10$ does not. The Banerjee test says "independent".

**Maybe without a dependence.** For `A[2*i] = A[3*i + 2]` with $1 \le i \le 3$, the range for $*$ is $[-7, 3]$, which holds $c = 2$. Refined, $<$ gives $[-7, -4]$, $=$ gives $[-3, -1]$ and $>$ gives $[0, 3]$, so the test keeps $(>)$. The point $(i, j) = (2.5, 1)$ solves the equation in the real triangle, but no integer point does: the loop writes $A[2], A[4], A[6]$ and reads $A[5], A[8], A[11]$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Its steps:

1. **The regions are convex hulls of their corners.** Each region of a level (rectangle, segment, triangle) is the set of convex combinations of the corners listed above; the proof writes the weights out.
2. **The closed forms are the extremes over the corners.** A linear function on a convex hull takes its minimum and maximum at corners, and the formulas of lines L10 to L13 evaluate them, using the positive and negative parts to choose the right corner.
3. **The sum of the extremes is the extreme of the sum.** The left side is a sum of one term per level, and the region of a direction vector is a product of the level regions, so each term can be pushed to its extreme on its own. So $lo$ and $hi$ are the minimum and the maximum of the left side over the whole region.
4. **Exactness over the reals.** The region is convex, so the segment from the minimizing point to the maximizing point stays in it, and the left side takes every value in $[lo, hi]$ along it. So the test answers "maybe" for one subscript exactly when a real solution exists in the region.
5. **Soundness.** An integer dependence with direction $\vec{\psi}$ is a real point of the region (an integer $x < y$ gives $x + 1 \le y$) that solves each equation, so the test answers "maybe".
6. **The search loses nothing.** The region of a refined vector is inside the region of the coarser one, so a cut vector would also fail every refinement.

## Complexity

One call of LEVEL-BOUNDS costs $O(1)$ operations, so a direction vector costs $O(k)$ per subscript and $O(mk)$ for the reference. The search tests at most $1 + 3 + \dots + 3^k$ vectors, so $O(3^k m k)$ time in the worst case, with a recursion stack of depth $k$. In practice most branches are cut near the root, and nests are shallow. The test needs $O(1)$ extra space for one direction vector.

## Properties

- **Conservative in one direction only.** "Independent" is a proof; "maybe" is not a proof of dependence.
- **Exact over the reals.** For one subscript and a rectangular region, "maybe" holds exactly when a real solution exists (Theorem 2 of the proof).
- **Not exact over the integers.** It ignores divisibility, which the [GCD test](/gcd-test/) checks; the two are often run together on the same equation.
- **One subscript at a time.** Like the GCD test, it does not join the equations of a multidimensional reference.
- **Direction aware.** It is the classic test for computing direction vectors, because each direction has its own closed form.

## Variants and improvements

- **Trapezoidal bounds.** Banerjee's book extends the bounds to loops whose bounds are affine in outer indices, such as triangular loops. The closed forms then include the coefficients of the bounds.
- **Combined GCD and Banerjee test.** Run the GCD test first on the equation for each direction vector; it is cheap and catches divisibility that the real bounds miss.
- **Exact tests for simple subscripts.** For subscripts with one index, the exact SIV tests of the [practical tests](/practical-dependence-tests/) replace the Banerjee test, and the Banerjee test is kept for the remaining MIV subscripts.
- **Real elimination of the whole system.** [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) decides real feasibility of all subscripts and bounds together, which catches coupled subscripts; the [omega test](/omega-test/) makes it exact over the integers.
- **Symbolic bounds.** When a bound is a parameter $n$, the extremes are affine functions of $n$, and the test asks whether $c$ can lie between them for some $n$.

## When to use it

Use it for subscripts with several loop indices in a nest with known bounds, after the exact tests for single-index subscripts, and use the hierarchical search when the transformations need direction vectors (interchange, parallelization, vectorization). For exact answers, or for coupled subscripts that matter, use the [omega test](/omega-test/) or a polyhedral library.

## Pitfalls

- **Using $x < y$ over the reals.** The strict real triangle $x < y$ has the same closure as $x \le y$ and gives wider bounds. The test must use $x + 1 \le y$, which is valid for integers and gives the closed forms above.
- **Forgetting empty regions.** For a loop with one iteration ($U = L$), the directions $<$ and $>$ have no pairs; the test must answer "independent" for them, not compute bounds from a formula with $N - 1 = -1$.
- **Reading "maybe" as "dependent".** The example `A[2*i] = A[3*i + 2]` shows a "maybe" without a dependence.
- **Mixing up the notation.** On this page $<$ means that the sink index is larger. In the plus-zero-minus notation of the dragon book the same direction is written $+$.
- **A direction vector with $>$ first.** A leaf such as $(>, <)$ is not a dependence from the source to the sink. It is a dependence from the sink to the source, and its direction is the reversed vector.

## Implementations

## History

Utpal Banerjee developed the bounds test at the University of Illinois in the second half of the 1970s, in David Kuck's group, for the Parafrase parallelizing compiler. The form with direction vectors, where each level has its own bounds for $<$, $=$ and $>$, was worked out in the 1980s and is the form in Wolfe's book and in Allen and Kennedy's book, which also give the hierarchical search. Banerjee's 1988 book collects the tests with their proofs, including the bounds for trapezoidal loops.

## References
