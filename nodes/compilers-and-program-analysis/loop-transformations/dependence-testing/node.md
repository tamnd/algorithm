---
tag: N2BH62
kind: problem
slug: dependence-testing
name: Dependence testing
aliases:
- array dependence analysis
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Decide whether two array references in a loop nest can touch the same element, an integer programming problem over the iteration space.
prereqs: [data-dependence, dependence-direction-vector, integer-feasibility]
see_also: [gcd-test, banerjee-test, practical-dependence-tests, omega-test, fourier-motzkin-elimination, feautrier-array-dataflow, presburger-arithmetic, loop-transformation-legality]
sources:
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 3, Dependence Testing (subscript classification, the GCD and Banerjee tests, the SIV and MIV tests and the delta test)
  - book: "Utpal Banerjee, Dependence Analysis for Supercomputing, Kluwer Academic Publishers, 1988"
    locator: the dependence equations of a pair of affine references and the GCD and bounds tests
  - paper: "Gina Goff, Ken Kennedy and Chau-Wen Tseng, Practical dependence testing, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), 1991"
    locator: the empirical study of subscripts in real programs, the ZIV, SIV and MIV classes and the delta test
  - paper: "William Pugh, A practical algorithm for exact array dependence analysis, Communications of the ACM 35(8), 1992, pages 102 to 114"
    locator: exact dependence testing with the omega test and its cost in practice
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 11.6 (array data-dependence analysis as integer linear programming, the GCD test and the heuristics for the general case)
  - paper: doi:10.1145/322276.322287
    title: Christos H. Papadimitriou, On the complexity of integer programming, Journal of the ACM 28(4), 1981
    locator: the bound on the size of an integer solution, which puts integer feasibility in NP
---

## In plain words

Two statements in a loop nest touch an array, and at least one of them writes it. Can some run of the first statement and some run of the second touch the same element? If never, the compiler may reorder, run in parallel or vectorize them freely. If yes, it must keep their order. Each loop index takes integer values between its bounds, so the question is whether a small system of integer equations and inequalities has a solution. That is integer programming, which is hard in general. Compilers therefore run a mix of fast tests that are exact on the common cases and careful on the rest: when a test is not sure, it must answer "maybe", never "independent". Tests also report the distances or the directions of the dependence, because the transformations need them.

## Definition

**Input.** Two references to the same array of $m$ dimensions, with affine subscripts:

- a reference $X[F\vec{i} + \vec{f}]$ in statement $S$ with iteration domain $D_S = \{\vec{i} \in \mathbb{Z}^{k_S} : A\vec{i} + \vec{a} \ge 0\}$,
- a reference $X[G\vec{j} + \vec{g}]$ in statement $T$ with iteration domain $D_T = \{\vec{j} \in \mathbb{Z}^{k_T} : B\vec{j} + \vec{b} \ge 0\}$,

where $F, G, A, B$ are integer matrices and $\vec{f}, \vec{g}, \vec{a}, \vec{b}$ integer vectors. The two statements have $k$ common loops, the first $k$ entries of both vectors. Optionally, a direction vector $\vec{\psi} \in \{<, =, >, *\}^k$.

**Question.** Is there a pair $(\vec{i}, \vec{j})$ with

$$\vec{i} \in D_S, \quad \vec{j} \in D_T, \quad F\vec{i} + \vec{f} = G\vec{j} + \vec{g}, \quad i_l \;\psi_l\; j_l \text{ for } l = 1, \dots, k \; ?$$

The equations are the **dependence equations**, one per dimension. The relation $i_l \psi_l j_l$ is $i_l < j_l$, $i_l = j_l$, $i_l > j_l$ or no constraint, in the notation of [direction vectors](/dependence-direction-vector/) used here (Wolfe's; $<$ means that the second reference runs in a later iteration of loop $l$). The set of solutions is a set of integer points of a polyhedron, in the isl notation `{ S[i] -> T[j] : F i + f = G j + g and ... }`.

**Outputs that tests give.**

- *Decision:* "independent" if there is no solution, else "dependent". A *conservative* test may answer "maybe" in place of either; it must never answer "independent" when a solution exists.
- *Directions:* the set of plain direction vectors $\vec{\psi} \in \{<, =, >\}^k$ for which a solution exists.
- *Distances:* the set $\{\vec{j} - \vec{i}\}$ over the solutions on the common loops, or a summary of it.

**From solutions to dependences.** A solution with $\vec{i} \prec \vec{j}$ on the common loops is a dependence from $S$ to $T$; a solution with $\vec{j} \prec \vec{i}$ is a dependence from $T$ to $S$; a solution with $\vec{i} = \vec{j}$ is a loop-independent dependence in the direction of the order of $S$ and $T$ in the body (none if $S = T$ and the two references are the same access). Its kind (flow, anti, output) follows from which access writes. See [data dependence](/data-dependence/).

## Variants

- **Constant bounds.** All loops are rectangular with known integer bounds. This is the setting of the [GCD test](/gcd-test/), the [Banerjee test](/banerjee-test/) and the [practical tests](/practical-dependence-tests/).
- **Affine bounds.** Bounds of inner loops depend on outer indices (triangular loops). The question is still integer feasibility of a polyhedron. Banerjee's bounds were extended to trapezoidal domains; the [omega test](/omega-test/) handles any affine constraints.
- **Symbolic bounds.** A bound is a parameter $n$ not known at compile time. The question becomes "for some $n$" or "for all $n$", a formula of [Presburger arithmetic](/presburger-arithmetic/).
- **Memory-based against value-based.** The question above asks whether two accesses touch the same element at all (memory-based). The value-based question asks whether the value read was *last* written by the given write; it removes dependences through overwritten values. [Feautrier's array dataflow analysis](/feautrier-array-dataflow/) answers it exactly with parametric integer programming.
- **Nonaffine subscripts.** Subscripts such as `A[i*j]` or `A[B[i]]` are outside the affine model. Compilers assume a dependence, or test at run time.

## Examples

### A subscript that the GCD decides

```
for i = 1 to 100:
  A[2*i] = A[2*i + 1] + 1
```

The equation $2i = 2j + 1$ has no integer solution, since its left side is even and its right side is odd. The [GCD test](/gcd-test/) proves independence without the bounds.

### A real solution but no integer solution in the bounds

```
for i = 1 to 3:
  A[2*i] = A[3*i + 2] + 1
```

The equation is $2i - 3j = 2$. The gcd of $2$ and $3$ is $1$, which divides $2$, so the GCD test says "maybe". Over the box $1 \le i, j \le 3$ the value of $2i - 3j$ runs over the real interval $[-7, 3]$, which holds $2$, so the [Banerjee test](/banerjee-test/) also says "maybe". But the loop writes $A[2], A[4], A[6]$ and reads $A[5], A[8], A[11]$: there is no dependence. The integer solutions $(i, j) = (1 + 3t, 2t)$ need $t \ge 1$ for $j \ge 1$ and $t \le 0$ for $i \le 3$. Only an exact test, such as the exact SIV test of the [practical tests](/practical-dependence-tests/), finds this.

### A coupled pair

```
for i = 1 to 8:
  A[i][i] = A[i][i+1] + 1
```

Each dimension alone has solutions: $i = j$ for the first, and $i = j + 1$ for the second. Together they have none. A test that treats each dimension on its own says "maybe"; a test that joins the constraints, such as the delta test, says "independent".

### A dependence with a known distance

```
for i = 1 to 4:
  for j = 1 to 4:
    A[i+1][j] = A[i][j] + 1
```

The equations are $i + 1 = i'$ and $j = j'$. Every solution has the distance $(1, 0)$, so there is one flow dependence with direction vector $(<, =)$, carried by the outer loop. The inner loop is parallel, and interchange is legal.

## Known algorithms

| test | handles | exact? | cost |
|---|---|---|---|
| [GCD test](/gcd-test/) | one equation, no bounds | exact for one equation without bounds | $O(k \log C)$ per equation |
| [Banerjee test](/banerjee-test/) | one equation, bounds, directions | exact over the reals, not over the integers | $O(k)$ per equation and direction vector |
| [practical tests](/practical-dependence-tests/) (ZIV, SIV, MIV, delta) | all subscripts, constant bounds | exact when every coupled group reduces to single-index subscripts | near linear in the number of subscripts in practice |
| [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) | any affine constraints | exact over the reals | can grow doubly exponentially |
| [omega test](/omega-test/) | any affine constraints, symbolic bounds | exact over the integers | exponential in the worst case, fast in practice |
| [Feautrier's array dataflow](/feautrier-array-dataflow/) | value-based, parametric | exact | parametric integer programming |

All of them except the omega test and Feautrier's method are conservative. Their answer "independent" is a proof. Their answer "maybe" says only that they could not find a proof. Other tests in the literature, such as the lambda test of Li, Yew and Zhu, the I test of Kong, Klappholz and Psarris, and the power test of Wolfe and Tseng, sit between Banerjee and the omega test.

Most compilers use a cascade: cheap exact tests on simple subscripts first, a general test only on the rest. Goff, Kennedy and Tseng measured that most subscript pairs in scientific Fortran code are ZIV or SIV, where cheap exact tests exist.

**Directions.** Any of the tests can take a direction vector as extra constraints. To find the set of direction vectors, test $(*, \dots, *)$; if it is not independent, split the first $*$ into $<$, $=$ and $>$ and test each, and go on down. A branch that is proved independent is cut. The search tests at most $3^k + 3^{k-1} + \dots + 1$ vectors, and far fewer when most branches are cut early.

## Bounds

**Theorem.** Dependence testing with affine subscripts and affine bounds is NP-complete. It is NP-hard already for one subscript and loops that run from $0$ to $1$.

*Membership.* The question is the feasibility of an integer program with the variables $\vec{i}$ and $\vec{j}$: the equations, the domain inequalities and the direction constraints (a strict $i_l < j_l$ is $i_l + 1 \le j_l$ over the integers). [Integer feasibility](/integer-feasibility/) is in NP: if a system has an integer solution, it has one whose size in bits is polynomial in the size of the system (Papadimitriou 1981). That solution is the certificate.

*Hardness.* Reduce from [subset sum](/subset-sum-problem/). Take positive integers $w_1, \dots, w_k$ and a target $T$. Build the nest

```
for i1 = 0 to 1:
  ...
    for ik = 0 to 1:
      S: A[w1*i1 + ... + wk*ik] = 0
R: x = A[T]
```

$S$ writes $A[\sum_l w_l i_l]$ for each $(i_1, \dots, i_k) \in \{0, 1\}^k$, and $R$ runs after the nest. There is a flow dependence from $S$ to $R$ if and only if some 0-1 vector has $\sum_l w_l i_l = T$, that is, if and only if some subset of the $w_l$ sums to $T$. The nest has size polynomial in the input. So a polynomial algorithm for dependence testing would decide subset sum. For $w = (3, 5, 7)$ and $T = 12$, the iteration $(0, 1, 1)$ writes $A[12]$; for $T = 11$ no iteration does.

Subset sum is solvable in pseudo-polynomial time, so this shows only weak NP-hardness. An array with many dimensions gives strong NP-hardness from [exact cover](/exact-cover/): one 0-1 loop per set, one dimension per element of the universe with subscript $\sum_{s \ni e} i_s$, and a read of $A[1][1]\dots[1]$. All coefficients are $0$ or $1$.

**Fixed depth.** For a fixed number of loops, the integer program has a fixed number of variables, and [integer programming in fixed dimension](/integer-programming-fixed-dimension/) is polynomial (Lenstra 1983). Real loop nests are shallow, which is one reason why exact tests are fast in practice.

**Beyond affine.** With polynomial subscripts and unbounded loop indices, dependence testing is undecidable. A write `A[p(i1, ..., ik)]` in a nest whose indices range over all natural numbers, and a read of `A[0]`, are dependent if and only if the polynomial $p$ has a root in natural numbers, which is [Hilbert's tenth problem](/hilberts-tenth-problem/), undecidable by Matiyasevich's theorem.

## Reductions

- **To integer feasibility.** The definition is an instance of [integer feasibility](/integer-feasibility/) with $k_S + k_T$ variables and $m$ equations. Every exact test solves this integer program, and every conservative test solves a relaxation of it: the GCD test drops the bounds, the Banerjee test drops integrality.
- **To linear Diophantine equations.** Without bounds, each equation is a [linear Diophantine equation](/linear-diophantine-equation/), and a system of them is solved exactly with the [Hermite normal form](/hermite-normal-form/). This is the generalized GCD test.
- **To Presburger arithmetic.** With symbolic bounds, the question with its quantifiers over parameters is a sentence of [Presburger arithmetic](/presburger-arithmetic/), which the omega test decides.
- **From subset sum and exact cover,** as in the bounds section.

## Applications

- **Legality.** Every reordering transformation needs the dependences of the nest; the [legality theorem](/loop-transformation-legality/) checks them against the transformation.
- **Parallelization and vectorization.** A loop is parallel when it carries no dependence; [vectorization](/vectorization/) and the [Allen-Kennedy algorithm](/allen-kennedy-algorithm/) need the level of each dependence.
- **Interchange, skewing, tiling.** These need direction or distance vectors: [loop interchange](/loop-interchange/), [loop skewing](/loop-skewing/), [loop tiling](/loop-tiling/), [unimodular transformations](/unimodular-transformations/).
- **Polyhedral compilation.** The [polyhedral model](/polyhedral-model/) keeps the solution set itself as a relation and schedules with it.

## References
