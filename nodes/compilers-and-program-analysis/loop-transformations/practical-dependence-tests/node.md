---
tag: B1R5XX
kind: algorithm
slug: practical-dependence-tests
name: Subscript-wise dependence tests
aliases:
- ZIV SIV MIV tests
- delta test
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Classifies subscript pairs by the number of loop indices they use and applies an exact test to each class, joining results by the delta test.
solves: [dependence-testing]
model: word-ram
complexity:
  vars: {m: the number of subscripts, k: the depth of the loop nest, C: the largest absolute value of a coefficient}
  time: {worst: O(m^2 k + m log C + 3^k m k), best: O(m k)}
  space: {extra: O(m k)}
properties: {deterministic: true, recursive: false}
prereqs: [dependence-testing, gcd-test, banerjee-test]
see_also: [dependence-distance-vector, loop-carried-dependence, omega-test, extended-euclidean-algorithm, linear-diophantine-equation, disjoint-set, loop-interchange, allen-kennedy-algorithm]
sources:
  - paper: "Gina Goff, Ken Kennedy and Chau-Wen Tseng, Practical dependence testing, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), 1991"
    locator: the ZIV, SIV and MIV classes, separable and coupled subscripts, the strong, weak-zero, weak-crossing and exact SIV tests, the delta test and the measurements on scientific programs
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 3, Dependence Testing (subscript partitioning, the single-subscript tests, the delta test and the order in which the tests are applied)
  - book: "Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996"
    locator: the chapter on dependence testing (single-index subscripts and the exact test for two variables)
  - book: "Utpal Banerjee, Dependence Analysis for Supercomputing, Kluwer Academic Publishers, 1988"
    locator: the exact test for one linear equation in two variables with bounds
---

The practical dependence tests, as organized by Goff, Kennedy and Tseng, solve the [dependence testing](/dependence-testing/) problem one subscript at a time, with the cheapest exact test that fits each subscript. A subscript pair is ZIV if it uses no loop index, SIV if it uses one, and MIV if it uses more. Most subscripts in real code are ZIV or SIV, and for these there are exact tests that cost a few arithmetic operations and also give the [distance](/dependence-distance-vector/) or the [direction](/dependence-direction-vector/) of the dependence. Subscripts that share a loop index are *coupled*; the **delta test** passes the facts found by the SIV tests (a distance, or a fixed value of an index) into the other subscripts of the group, which often turns them into SIV subscripts too. Only the MIV subscripts that remain go to a general test such as the [GCD](/gcd-test/) and [Banerjee](/banerjee-test/) tests.

## In plain words

An array access with several dimensions gives one condition per dimension. Look at each one. If it uses no loop variable, it is true always or never, and that settles it. If it uses one loop variable, a short formula tells exactly which pairs of iterations satisfy it, for instance "the second access is always one iteration later". If two conditions share a loop variable, the answer from one is used to simplify the other, and the process is repeated until nothing more can be learned. Only conditions that still mix several loop variables at the end go to the slower, approximate tests. When none are left, the answer is exact: the compiler knows the exact directions and often the exact distances of the dependence.

## The problem

As in [dependence testing](/dependence-testing/): a rectangular nest of depth $k$ with loop $l$ over $L_l \le i_l \le U_l$, two references with affine subscripts, one equation per dimension

$$\sum_{l=1}^{k} \bigl(a_{rl} i_l - b_{rl} j_l\bigr) = b_{r0} - a_{r0}, \qquad r = 1, \dots, m,$$

for the source iteration $\vec{i}$ and the sink iteration $\vec{j}$. Output: "independent", or the set of direction vectors that may occur, the distance at each level where it is fixed, and a flag that says whether the set is exact. The page uses Wolfe's notation: $<$ at level $l$ means $i_l < j_l$. A direction vector whose first non-$=$ entry is $>$ belongs to the dependence from the sink reference to the source reference, as described on the [direction vector](/dependence-direction-vector/) page. The answer "independent" must never be given when a dependence exists.

## The algorithm

The tests keep, for each level $l$, the exact set $S_l$ of pairs $(i_l, j_l)$ allowed by the SIV equations seen so far. Each $S_l$ is the whole square, empty, one point, or the integer points of a segment $(x_0 + p t, y_0 + q t)$.

```pseudo id=main
PRACTICAL-TEST(subscript pairs, bounds):
L1  for each subscript pair that uses no loop index (ZIV) do
L2      if its two constants differ then return "independent"
L3  partition the other pairs into coupled groups: pairs that share a level go together
L4  for each group do (the delta test)
L5      S_l <- all pairs in [L_l, U_l]^2, for each level l
L6      repeat
L7          rewrite each pending pair with the facts of the S_l (a point, a fixed i_l, a fixed j_l, or a distance)
L8          if a pair uses no level now: if its constant is not 0 then return "independent"; drop it
L9          if a pair uses one level l now: S_l <- S_l ∩ {solutions} (strong, weak-zero, weak-crossing or exact SIV test); drop it
L10         if some S_l is empty then return "independent"
L11     until a pass changes nothing; the pending pairs are the MIV pairs
L12     D <- the direction vectors of the group allowed by the S_l and by the GCD and Banerjee tests on each MIV pair
L13     if D is empty then return "independent"
L14 return the product of the sets D, the distances fixed by the S_l, and exact = (no MIV pair is left)
```

**The SIV tests.** Write the SIV equation of level $l$ as $a i - b j = c$, so the two subscripts are $a i + c_1$ and $b j + c_2$ with $c = c_2 - c_1$.

| test | when | solutions |
|---|---|---|
| strong SIV | $a = b$ | $j - i = d = (c_1 - c_2)/a$; a dependence exists if and only if $d$ is an integer and $\lvert d \rvert \le U - L$ |
| weak-zero SIV | $a = 0$ or $b = 0$ | one index is fixed: $i = c/a$ or $j = -c/b$, which must be an integer in the bounds |
| weak-crossing SIV | $a = -b$ | $i + j = c/a$: the pairs cross at the middle $c/(2a)$ |
| exact SIV | other | the extended Euclidean algorithm gives the solutions $(x_0 + (b/g) t, y_0 + (a/g) t)$, cut to the bounds |

All four are exact for one equation in the bounds. The strong SIV test gives the distance at once.

**The delta step (line L7).** A level state gives one of four facts, and each one simplifies the other equations of the group:

- one point $(x^*, y^*)$: the terms of level $l$ become a constant;
- a fixed $i_l$ ($p = 0$, from weak-zero): the term $a_l i_l$ becomes a constant;
- a fixed $j_l$ ($q = 0$): the term $b_l j_l$ becomes a constant;
- a fixed distance $j_l = i_l + d$ ($p = q$, from strong SIV): the terms become $(a_l - b_l) i_l - b_l d$, which leaves only one index of that level.

An equation that loses all but one level becomes an SIV equation, and the loop goes on.

**The MIV pairs (line L12).** For each combination of level directions allowed by the states, each remaining equation must pass a GCD test and a Banerjee test, where the range of each level is taken from its exact state when it has one, and from the Banerjee formulas when the level is still free.

## Example

```
for i = 1 to 6:
  for j = 1 to 6:
    A[i+1][i+j] = A[i][i+j] + 1
```

Let $(i, j)$ be the iteration of the write and $(i', j')$ that of the read. The subscript pairs are $i + 1 = i'$ (SIV, level 1) and $i + j = i' + j'$ (MIV, levels 1 and 2). They share level 1, so they form one coupled group.

| step | action | result |
|---|---|---|
| L9 | strong SIV on $i - i' = -1$: $d_1 = 1$, $\lvert d_1 \rvert \le 5$ | $S_1 = \{(t, t+1) : 1 \le t \le 5\}$ |
| L7 | rewrite $i + j - i' - j' = 0$ with $i' = i + 1$ | $j - j' = 1$, now SIV at level 2 |
| L9 | strong SIV: $d_2 = -1$ | $S_2 = \{(t, t-1) : 2 \le t \le 6\}$ |
| L11 | no pair left; a pass changes nothing | no MIV pair, so the result is exact |
| L12 | level 1 allows only $<$, level 2 only $>$ | $D = \{(<, >)\}$ |

So there is exactly one flow dependence, with distance $(1, -1)$, carried by the $i$ loop. The $j$ loop can run in parallel, and [loop interchange](/loop-interchange/) is illegal, because it would turn $(1, -1)$ into $(-1, 1)$. A test that looks at each subscript on its own would only learn that the second subscript allows many directions.

**Proving independence.** For `A[i][i] = A[i][i+1]` the first pair gives the strong SIV distance $0$, so $S_1 = \{(t, t)\}$. The delta step rewrites the second pair $i - i' = 1$ with $i' = i$ into $0 = 1$, and line L8 answers "independent". The GCD test says "maybe" for each subscript.

**Exact SIV beats the general tests.** For `A[2*i] = A[3*i + 2]` with $1 \le i \le 3$, the GCD and Banerjee tests say "maybe". The exact SIV test finds the solutions $(1 + 3t, 2t)$ of $2i - 3i' = 2$ and cuts them to the bounds: $j = 2t \ge 1$ needs $t \ge 1$, and $i = 1 + 3t \le 3$ needs $t \le 0$. The set is empty: independent.

**A pair that stays MIV.** For `X[i+j] = X[i+j-1]` in a $4 \times 4$ nest, the only equation uses both levels and no SIV fact exists, so it stays MIV. Line L12 tests all nine combinations with the GCD and Banerjee tests and keeps $(=, <)$, $(<, =)$, $(<, >)$ and $(>, <)$. The result is marked as not exact, although here enumeration of all pairs gives the same four vectors. The first three are flow dependences from the write to the read; $(>, <)$ is an anti dependence from the read to the write, with direction $(<, >)$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Its main steps:

1. **Strong SIV is exact.** $a i + c_1 = a j + c_2$ means $a (j - i) = c_1 - c_2$, so every solution has $j - i = d = (c_1 - c_2)/a$; this needs $d$ to be an integer, and $\lvert d \rvert \le U - L$ because both indices lie in $[L, U]$. Conversely, if both hold, the pairs $(t, t + d)$ with $\max(L, L - d) \le t \le \min(U, U - d)$ are solutions, and this range is not empty.
2. **The other SIV tests are exact.** Each describes the integer solutions of one equation in two variables as a lattice line ([Bezout](/bezouts-identity/) for the exact test), and cutting a line to a box is exact with floor and ceiling divisions.
3. **The delta step keeps the solution set.** Each rewrite replaces a term by an expression equal to it on every pair of the level state, so the solution set of the group never changes. A dropped equation is $0 = 0$, and an answer "independent" comes from an equation $0 = c$ with $c \ne 0$, or from an empty level state.
4. **Soundness.** Every real solution lies in the level states, satisfies each remaining MIV equation, and so passes the GCD and Banerjee filters with its own direction vector.
5. **Exactness.** If no MIV equation remains, the solution set is the product of the level states, so every combination of nonempty direction parts is realized.

## Complexity

Classification and the union-find partition take $O(mk)$ time. The delta loop runs at most $m + 1$ passes, because each pass that changes something removes an equation. A pass rewrites at most $m$ equations in $O(k)$ each, and each SIV test costs a few divisions and at most one extended gcd, $O(\log C)$. So the delta test costs $O(m^2 k + m \log C)$. The MIV filter tests at most $3^k$ combinations of directions with $m$ equations of $k$ terms, $O(3^k m k)$; it runs only for groups that keep MIV equations, and the [Banerjee](/banerjee-test/) hierarchy cuts most combinations early. When every subscript is ZIV or separable SIV, the whole test costs $O(mk)$ plus the size of the output.

## Properties

- **Conservative in one direction only.** "Independent" is always right. When MIV pairs remain, the direction set can contain vectors without a dependence.
- **Exact on ZIV and SIV.** Without MIV pairs, the answer, the direction set and the distances are exact.
- **Distances for free.** The strong SIV test and the delta step give exact distances, which [unimodular transformations](/unimodular-transformations/) and [loop skewing](/loop-skewing/) need.
- **Rectangular bounds.** The tests above assume constant bounds; triangular bounds weaken the SIV tests to "maybe" on the bounds, or need a general test.

## Variants and improvements

- **RDIV subscripts.** Goff, Kennedy and Tseng also treat subscripts such as `A[i]` against `A[j]` where $i$ and $j$ are indices of two *different* loops (restricted double index variable). They are handled like exact SIV with the two loops' bounds.
- **Symbolic constants.** If $c_1 - c_2$ is a symbolic expression such as $n$ or $n - 1$, the strong SIV test can still decide when the expression is known to be larger than the trip count, or give a symbolic distance.
- **Other coupled-subscript tests.** The lambda test of Li, Yew and Zhu and the power test of Wolfe and Tseng handle coupled MIV subscripts with linear combinations or with Fourier-Motzkin elimination over the integer solutions.
- **Exact general test.** The [omega test](/omega-test/) replaces the GCD and Banerjee filter for the remaining MIV pairs and makes the whole result exact.
- **Hierarchical directions.** Instead of the product at line L12, refine the direction vector one level at a time and cut a branch at the first failed test, as in the [Banerjee test](/banerjee-test/).

## When to use it

It is the default dependence analyzer of loop optimizers for Fortran-like code with affine subscripts and rectangular nests: the common cases are decided exactly and fast, with distances, and the costly general tests run only on the few MIV subscripts left. For triangular nests, symbolic bounds or value-based dependences, a polyhedral analysis ([omega test](/omega-test/), [Feautrier's dataflow](/feautrier-array-dataflow/)) is more precise.

## Pitfalls

- **Testing subscripts separately and intersecting the answers.** For coupled subscripts, the direction sets of the subscripts can each be nonempty while the system has no solution, as in `A[i][i] = A[i][i+1]`. Intersecting direction sets is sound, but weaker than the delta step.
- **Forgetting the bound in the strong SIV test.** $d$ can be an integer and still be larger than the trip count; then there is no dependence.
- **Sign of the distance.** With the subscripts $a i + c_1$ (source) and $a j + c_2$ (sink), the distance is $j - i = (c_1 - c_2)/a$, not $(c_2 - c_1)/a$. A sign error turns a flow dependence into an anti dependence.
- **Weak-zero at the ends of the loop.** A weak-zero solution such as $i = 1$ for `A[i] = A[1]` hits only the first iteration; peeling that iteration removes the dependence, which is the classic use of the test.
- **Weak-crossing at the middle.** For `A[i] = A[n - i + 1]` all dependences cross the middle iteration; splitting the loop there removes them.
- **Calling the result exact when MIV pairs remain.** Only the result without MIV pairs is exact.

## Implementations

## History

Goff, Kennedy and Tseng presented the subscript classification, the named SIV tests and the delta test in "Practical dependence testing" at PLDI 1991, from their work on the parallelizing compiler systems at Rice University. They measured, on scientific Fortran programs, that ZIV and SIV subscripts are by far the most common, and that most coupled subscripts become SIV after the delta step. The exact test for one equation in two variables is older; it is in Banerjee's work. Allen and Kennedy's book gives the whole suite as the standard dependence tester.

## References
