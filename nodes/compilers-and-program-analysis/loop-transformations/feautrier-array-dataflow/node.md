---
tag: 61C0MP
kind: algorithm
slug: feautrier-array-dataflow
name: Array dataflow analysis
aliases:
- Feautrier array dataflow
- value-based dependence analysis
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Finds for each read of an array element the exact iteration that last wrote it, by parametric integer programming.
model: word-ram
complexity:
  vars: {s: the number of statements that write the array, d: the depth of the deepest loop nest, L: the size of the largest quast that is built, P: the cost of one call of parametric integer programming (exponential in the worst case)}
  time: {worst: O(s d (P + L))}
  space: {extra: O(L)}
properties: {deterministic: true, recursive: true}
prereqs: [data-dependence, loop-carried-dependence, lexicographic-order, dual-simplex-method, gomory-cutting-plane-algorithm, polyhedral-model]
see_also: [dependence-testing, omega-test, presburger-arithmetic, array-privatization, reaching-definitions, feautrier-scheduling, lexicographic-optimization, chvatal-gomory-cut]
sources:
  - paper: doi:10.1007/BF01407931
    title: Paul Feautrier, Dataflow analysis of array and scalar references, International Journal of Parallel Programming 20(1), 1991, 23-53
    locator: the definition of the source function, the candidate sets by depth, the use of PIP for each candidate set and the combination of the partial results into one quast
  - paper: doi:10.1051/ro/1988220302431
    title: Paul Feautrier, Parametric integer programming, RAIRO Recherche Opérationnelle 22(3), 1988, 243-268
    locator: the parametric dual simplex method, the quast (quasi-affine selection tree) form of the solution, and the Gomory cuts with new parameters for the integer case
---

Array dataflow analysis takes a read of an array element in a loop program and finds, for every iteration that does the read, the exact iteration that last wrote that element before it. Paul Feautrier gave the method in 1991 for *static control programs*, where every loop bound and every array subscript is an affine function of the loop counters and of some integer size parameters. For each possible writer, the set of candidate iterations is a [polyhedron](/polyhedron/) that depends on the reading iteration, and its [lexicographic](/lexicographic-order/) maximum is found by parametric integer programming. The answer is a *quast*, a tree of affine tests whose leaves are affine formulas, and it holds for all values of the parameters at once.

## In plain words

A program reads an array cell. Which earlier step put the value there? Ordinary dependence tests only say "some earlier step of that statement may have written this cell". This analysis says exactly which one. It looks at each statement that writes the array and asks: of the steps of this statement that wrote this cell before the read, which one was the latest? The steps form a shape bounded by straight lines, so this is an optimization over the whole numbers inside the shape. The answer is not one number but a small decision tree, because it depends on where the read happens and on the size of the arrays. At the end, the trees for all the writers are combined, and the latest writer wins. If no writer exists, the read sees the initial value.

## The problem

**Input.** A static control program: statements in nested loops, with affine loop bounds and affine subscripts in the loop counters and in integer parameters $N$ that are only known at run time, and a context, a set of affine constraints on $N$. Statement $S$ is inside $d_S$ loops, with counters $\vec{s} = (s_1, \dots, s_{d_S})$. Its iteration domain $D_S$ is a polyhedron, bounded for each value of $N$. It writes the array element $A[f_S(\vec{s})]$, where $f_S$ is affine. A read $A[g(\vec{t})]$ in statement $T$ is given.

**Execution order.** The program runs in its text order. Instance $S(\vec{s})$ runs before $T(\vec{t})$ if they agree on the first $l - 1$ of their $c_{ST}$ common loops and $s_l < t_l$ for some $l \le c_{ST}$, or if they agree on all common loops and $S$ comes before $T$ in the text of the innermost common loop. In the [polyhedral model](/polyhedral-model/) this is the lexicographic order of the $(2d + 1)$-dimensional schedule vectors $(\beta_0, s_1, \beta_1, \dots, s_d, \beta_d)$, where $\beta_k$ is the text position at depth $k$.

**Output.** The *source* function $\sigma(\vec{t}, N)$: for each $N$ in the context and each $\vec{t} \in D_T$, the instance $S(\vec{s})$ that runs last among the instances that write $A[g(\vec{t})]$ before $T(\vec{t})$, or $\bot$ if there is none. It is given as a quast, a tree with nodes "if $e \ge 0$" for affine $e$, nodes "let $q = \lfloor e / D \rfloor$" that add new integer parameters, and leaves that are $\bot$ or $S(\vec{h})$ with $\vec{h}$ affine in $\vec{t}$, $N$ and the new parameters.

## The algorithm

The algorithm splits the earlier writes into candidate sets. Each set comes from one writing statement and one *depth*: the depth is the loop that carries the order, or "same iteration" if the two instances share all common loops. Inside one candidate set, a later instance has a lexicographically greater vector $\vec{s}$, so the latest writer is the lexicographic maximum of an integer polyhedron with parameters $\vec{t}$ and $N$. Parametric integer programming (PIP) computes this maximum as a quast. A final merge compares the leaves of the quasts by their schedule vectors.

```pseudo id=main
SOURCE(T, t, A[g(t)])                 ▷ the read A[g(t)] in the instance T(t)
L1  Q <- the quast "no source"
L2  for each statement S that writes A[f_S(s)] do
L3      for each depth l in 1 .. c_ST, and "same iteration" if S is before T in the text do
L4          C <- { s in D_S : f_S(s) = g(t), s_1..s_{l-1} = t_1..t_{l-1}, s_l <= t_l - 1 }
L5          K <- PIP-LEXMAX(C) with the parameters t and N
L6          Q <- MERGE(Q, K): at each leaf, keep the source that runs later
L7  return Q

PIP(rows, context)                    ▷ each row: x_i = c_i(p) + sum_j a_ij n_j >= 0
L8  if the context has no point then return "no solution"
L9  while some row has c_i(p) < 0 on the whole context do pivot on it, or return "no solution" if no a_ij > 0
L10 if some row has c_i(p) of both signs on the context then
        return if c_i >= 0 then PIP(rows, context and c_i >= 0) else PIP(rows, context and c_i <= -1)
L11 k <- an unknown x_k whose constant c_k(p) is not integer-valued
L12 if there is none then return the leaf (c_1(p), ..., c_n(p))
L13 if the fractional part f of c_k is a constant then add the cut row -f + sum_j frac(-a_kj) n_j >= 0 and go to L9
L14 add the parameter q = floor(D f(p) / D) and the cut row q - f(p) + sum_j frac(-a_kj) n_j >= 0, and go to L9
```

For the "same iteration" depth, line L4 uses $s_1 = t_1, \dots, s_c = t_c$ for all $c = c_{ST}$ common loops and no strict inequality.

**PIP.** The tableau describes every unknown and every constraint as $x_i = c_i(p) + \sum_j a_{ij} n_j$, where the $n_j \ge 0$ are the current nonbasic variables and $c_i(p)$ is affine in the parameters $p$. At the start, the nonbasic variables are the unknowns. The constant column is the current solution. Line L9 is the [dual simplex method](/dual-simplex-method/) with a lexicographic pivot rule. Among the columns $j$ with $a_{rj} > 0$, it picks the one whose whole column divided by $a_{rj}$ is lexicographically least, so that the columns stay lexicographically positive and the basic solution stays the lexicographic minimum. The sign of $c_i(p)$ depends on $p$, so the test is a feasibility test of the context plus one constraint, and when both signs occur, line L10 splits the context into two parts. Lines L13 and L14 are [Gomory cuts](/gomory-cutting-plane-algorithm/). When the fractional part depends on $p$, it is not affine, and Feautrier writes it with a new parameter $q = \lfloor e / D \rfloor$. The new parameter is defined by the two context constraints $D q \le e \le D q + D - 1$.

**Maximum instead of minimum.** PIP finds a lexicographic minimum over $x \ge 0$. The implementation sets $x_k = M - s_k$ for a symbolic parameter $M$ that is larger than every other value. The sign of a form with an $M$ term is the sign of its $M$ coefficient.

**Merge.** Line L6 walks the two quasts together, adding the tests of both to the context. At a pair of leaves $S(\vec{h})$ and $S'(\vec{h}')$, it compares the schedule vectors $\theta_S(\vec{h})$ and $\theta_{S'}(\vec{h}')$ one component at a time. Each comparison is a three-way split on the sign of an affine difference, and the first nonzero difference decides. Branches whose context has no point are dropped.

## Example

Take a lower triangular matrix-vector product:

```
for i = 0 to N - 1:
S1:   y[i] = 0
      for j = 0 to i:
S2:       y[i] = y[i] + L[i][j] * x[j]
```

Consider the read of `y[i]` in $S2(t_1, t_2)$. Both statements write `y`.

- $S1$ has one common loop with $S2$. At depth 1, the candidates satisfy $s_1 = t_1$ (same element) and $s_1 \le t_1 - 1$, which is empty. At the "same iteration" depth, $S1$ comes before the $j$ loop in the text, and the set is $\{s_1 : s_1 = t_1\}$. Its maximum is $S1(t_1)$.
- $S2$ has two common loops with itself. Depth 1 is empty again. At depth 2 the set is $\{(s_1, s_2) : s_1 = t_1,\ 0 \le s_2 \le t_2 - 1\}$. PIP returns $(t_1, t_2 - 1)$ if $t_2 \ge 1$ and no solution otherwise. "Same iteration" does not apply, because an instance does not run before itself.

The merge compares $\theta_{S1}(t_1) = (0, t_1, 0)$ with $\theta_{S2}(t_1, t_2 - 1) = (0, t_1, 1, t_2 - 1, 0)$. They differ first in the third component, so $S2$ is later. The source is

$$\sigma(t_1, t_2) = \begin{cases} S2(t_1, t_2 - 1) & \text{if } t_2 \ge 1, \\ S1(t_1) & \text{otherwise.} \end{cases}$$

The implementation prints this tree. A memory-based test says only that the read depends on $S1$ and on many instances of $S2$; the source keeps one instance.

**A new parameter.** In

```
for i = 0 to N:      S1: A[2i] = ...
for j = 0 to 2N:     S2: B[j] = A[j]
```

the candidates for the read in $S2(t)$ are $\{s : 0 \le s \le N,\ 2s = t\}$. The rational maximum is $s = t/2$, which is not an integer for odd $t$. Line L14 adds $q = \lfloor t / 2 \rfloor$, and the result is: if $2q - t \ge 0$, that is, $t$ is even, the source is $S1(q)$; otherwise there is no source and the read sees the initial value of `A[t]`. A test such as $t$ even cannot be written with affine tests on $t$ and $N$ alone, which is why quasts need the new parameters.

**Along a diagonal.** For `A[i+j] = A[i+j] + 1` inside two loops over $0 \le i, j \le N$, the source of the read in $S(t_1, t_2)$ is $S(t_1 - 1, t_2 + 1)$ if $t_1 \ge 1$ and $t_2 \le N - 1$, and the initial value otherwise. The candidate set at depth 2 is empty, because $s_1 = t_1$ and $s_1 + s_2 = t_1 + t_2$ force $s_2 = t_2$.

## Correctness

The full proof is in [the proof page](proofs/correctness.md). It has four steps. First, an instance $S(\vec{s})$ writes $A[g(\vec{t})]$ before $T(\vec{t})$ exactly when $\vec{s}$ is in one of the candidate sets of line L4, and these sets are disjoint. Second, inside one candidate set, the order of execution is the lexicographic order of $\vec{s}$, because all its points belong to one statement. Third, PIP returns the integer lexicographic minimum for every parameter value of the context: the lexicographic dual simplex keeps the basic solution equal to the minimum of the rational relaxation, splits partition the context, and every Gomory cut is satisfied by all integer points and cuts off a fractional basic solution. Fourth, the merge keeps, for each parameter value, the later of two instances, because it compares the full schedule vectors. So the result is the latest of all earlier writes of the element, which is the definition of the source. The method is exact: it makes no approximation, as long as bounds and subscripts are affine.

## Complexity

The algorithm runs one PIP for each writing statement $S$ and each depth, at most $s(d + 1)$ calls for one read. PIP solves integer programs, so it is NP-hard in general, and the quast it returns can have exponentially many leaves. PIP terminates by the same argument as Gomory's method with a lexicographic rule, but the number of cuts has no polynomial bound. The merge visits each pair of leaves and does at most $2d + 1$ three-way splits, each with a few rational feasibility tests. In practice the candidate sets have few constraints and the quasts are small, and the cost is close to that of a few exact dependence tests per read.

The implementation on this page uses an exact rational simplex for the context tests and computes the brute-force sources on small loop bounds only for testing.

## Properties

- **Exact.** For static control programs the result is the exact source at every iteration and every value of the parameters.
- **Value based.** It reports the flow of values, not the reuse of memory cells. A write that is overwritten before the read gives no edge, unlike a memory-based [data dependence](/data-dependence/).
- **Parametric.** The result holds for all sizes $N$ at once. The tests in the tree are affine, plus the new parameters of the form $\lfloor e / D \rfloor$.
- **A function.** For each read the source is one instance or $\bot$, never a set. This makes the result a direct input for array expansion into single assignment form and for [array privatization](/array-privatization/).

## Variants and improvements

- **Fuzzy array dataflow analysis.** Barthou, Collard and Feautrier extend the method to programs with conditionals and non-affine subscripts. The source then becomes a set of possible instances, described with new free parameters.
- **Presburger formulation.** Pugh and Wonnacott compute the same value-based dependences as formulas of [Presburger arithmetic](/presburger-arithmetic/) and solve them with the [omega test](/omega-test/).
- **Last write trees.** Maydan, Amarasinghe and Lam compute the same trees with faster tests that are exact for the common cases, and use them for array privatization.
- **Scalars.** A scalar is an array of dimension zero, so the same algorithm gives exact [reaching definitions](/reaching-definitions/) inside loops at the level of instances.
- **Scheduling input.** [Feautrier's scheduling](/feautrier-scheduling/) and the [affine scheduling problem](/affine-scheduling-problem/) use the source functions as the dependence edges of the program. A schedule has to respect only the flow from source to read, after array expansion has removed the other dependences.

## When to use it

Use it when the compiler needs to know where a value comes from, not only whether two accesses touch the same cell: to expand arrays into single assignment form and remove false dependences, to privatize arrays, to find parallelism that the memory-based dependences hide, or to build the dataflow graph for polyhedral scheduling. If only the legality of one transformation is needed, the cheaper [dependence tests](/dependence-testing/) are enough.

## Pitfalls

- **Affine only.** The candidate sets are polyhedra only when bounds and subscripts are affine in the counters and the parameters. An index array `A[P[i]]`, a product `i * j` in a subscript, or a data-dependent `if` takes the program out of the model. The plain method then does not apply; the fuzzy variant gives sets of possible sources.
- **Bounded domains.** The maximum exists only if the candidate set is bounded for each parameter value. A loop with no upper bound, or a context that allows negative sizes where the code expects positive ones, makes the problem ill posed.
- **Integers, not rationals.** The rational maximum of a candidate set can be a point that is not an iteration, as in the even-index example. The Gomory cuts and the new parameters are needed, and leaving them out gives a wrong source.
- **Context feasibility.** The tests that drop a branch must be sound for integers. A rational test may keep a branch that has no integer point, which only makes the tree larger, but a test that drops a branch with an integer point gives a wrong answer.
- **Aliasing.** The method assumes that two different array names never share memory. Programs where arrays overlap need a different model.

## Implementations

## History

Paul Feautrier published parametric integer programming in 1988 and the array dataflow analysis built on it in 1991, as part of his work on automatic parallelization. The 1991 paper defines the source function and gives the result as a quast. Around 1993, Maydan, Amarasinghe and Lam, and Pugh and Wonnacott gave other ways to compute the same exact information. Feautrier used the source functions as the dependence input of his scheduling algorithm in 1992, and the analysis became a standard part of the [polyhedral model](/polyhedral-model/). Polyhedral libraries such as isl still compute exact dataflow with parametric integer programming.

## References
