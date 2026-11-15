---
tag: K23N8A
kind: algorithm
slug: farkas-invariant-generation
name: Constraint-based invariant generation
aliases:
- Farkas lemma invariant synthesis
area: compilers-and-program-analysis/verification-and-synthesis
level: research
summary: Finds linear inductive invariants by writing an invariant template and solving the conditions it must meet with Farkas' lemma.
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of rows of Init and of all transitions, k: the number of transitions, M: the set of allowed multipliers, L: the cost of one exact linear program with O(n + m) unknowns and O(n k) rows}
  time: {worst: O((|M| + 1)^k L)}
  space: {extra: O(n k (n + m))}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2003
  people: [Michael A. Colon, Sriram Sankaranarayanan, Henny B. Sipma]
  note: Colon, Sankaranarayanan and Sipma (CAV 2003) encoded initiation and consecution of a linear template with Farkas' lemma and solved the nonlinear constraints by quantifier elimination; Sankaranarayanan, Sipma and Manna (SAS 2004) made it scale by fixing the multipliers.
prereqs: [farkas-lemma, linear-programming-problem, loop-invariant-synthesis]
see_also: [houdini-algorithm, ranking-function-synthesis, polyhedra-domain, abstract-interpretation, widening-operator, simplex-method, quantifier-elimination, integer-hull]
sources:
  - paper: doi:10.1007/978-3-540-45069-6_39
    title: Michael A. Colon, Sriram Sankaranarayanan and Henny B. Sipma, Linear invariant generation using non-linear constraint solving, Proceedings of CAV 2003, LNCS 2725
    locator: Section 2 (Theorem 1, Farkas' lemma), Section 3 (the initiation and consecution tables with the multiplier mu, Theorem 2), Section 4 (solving the constraints) and Fig. 1
  - paper: doi:10.1007/978-3-540-27864-1_7
    title: Sriram Sankaranarayanan, Henny B. Sipma and Zohar Manna, Constraint-based linear-relations analysis, Proceedings of SAS 2004, LNCS 3148
    locator: pp. 53 to 68, the simplifications of the constraint solving step that make the method scale
  - paper: doi:10.1145/1375581.1375616
    title: Sumit Gulwani, Saurabh Srivastava and Ramarathnam Venkatesan, Program analysis as constraint solving, Proceedings of PLDI 2008
    locator: the template-based invariant generation with Farkas' lemma and its reduction to SAT
  - paper: doi:10.1007/978-3-540-24622-0_20
    title: Andreas Podelski and Andrey Rybalchenko, A complete method for the synthesis of linear ranking functions, Proceedings of VMCAI 2004, LNCS 2937
    locator: pp. 239 to 251, the same use of Farkas' lemma for termination instead of invariance
---

Constraint-based invariant generation finds a linear [loop invariant](/loop-invariant/) by solving for its coefficients. It fixes a template $c \cdot x + d \le 0$ with unknown $c$ and $d$, writes the two conditions of an [inductive invariant](/inductive-invariant/) as "this system of inequalities implies that one", and turns each implication into linear constraints on $c$, $d$ and some multipliers with [Farkas' lemma](/farkas-lemma/). One [linear program](/linear-programming-problem/) per choice of cases then gives an invariant, or proves that none of the allowed form exists.

## In plain words

Instead of running the loop forward and guessing where it settles, write down the shape of the fact you want, "some number times $i$ plus some number times $j$ plus a constant stays below zero", with the numbers left blank. Two things must be true: the fact holds at the start, and one turn of the loop keeps it. Each of these says that some known inequalities force one more inequality. An old result from linear algebra says exactly when that happens: the new inequality must be a sum of the known ones, each times a nonnegative weight. Asking for such weights gives equations in the blanks. Solve them, and every answer is a proven fact about the loop.

## The problem

The input is a loop over $n$ rational variables. Its initial states are $\mathit{Init} = \{x : Px \le p\}$, and it has $k$ transitions, each a relation $\tau_i = \{(x, x') : A_i x + A'_i x' \le t_i\}$ between the state $x$ before and the state $x'$ after one step. Guards and assignments like $\mathbf{if}\ i < n\ \mathbf{then}\ i := i + 1$ are such relations. The input also has a point $x_{\mathrm{bad}}$ that should be proved unreachable. The output is an inequality $c \cdot x + d \le 0$ that holds on $\mathit{Init}$, is kept by every transition over $\mathbb{Q}^n$, and is false at $x_{\mathrm{bad}}$; or "none".

This is the linear case of [loop invariant synthesis](/loop-invariant-synthesis/). The general problem is undecidable, by [Rice's theorem](/rice-theorem/). Here the program is linear, the template is a single linear inequality and the states are rational, and the question becomes decidable: by Theorem 2 below it is a formula of real arithmetic, which [quantifier elimination](/quantifier-elimination/) decides, and with fixed multipliers it is a finite set of linear programs.

## The algorithm

```pseudo id=main
FARKAS-INVARIANT(P x <= p, transitions A_i x + A'_i x' <= t_i, x_bad, M)
L1  for each choice of one case per transition: (cons, mu) with mu in M, or dis
L2      S <- { lambda_0 P = c,  lambda_0 p <= -d }
L3      for each transition i with multipliers lambda_i >= 0
L4          if case_i = (cons, mu): add mu c + lambda_i A_i = 0, lambda_i A'_i = c, lambda_i t_i <= (mu - 1) d
L5          else: add c + lambda_i A_i = 0, lambda_i A'_i = 0, lambda_i t_i - d <= -1
L6      add c . x_bad + d >= 1
L7      if S has a solution with all lambda >= 0 then return (c, d)
L8  return none
```

The unknowns are $c$, $d$ and the multipliers; $\mu$ is a number fixed by the choice. Line L2 is initiation: by Farkas' lemma, every point of $Px \le p$ satisfies $c \cdot x \le -d$ exactly when $c$ is a nonnegative combination $\lambda_0 P$ of the rows with $\lambda_0 p \le -d$. Line L4 is consecution: the rows $c \cdot x \le -d$ (weight $\mu$) and $A_i x + A'_i x' \le t_i$ (weights $\lambda_i$) must add up to $c \cdot x' \le -d$. Line L5 is the other way to satisfy consecution: the transition cannot fire from any state of the invariant, and the rows add up to the contradiction $0 < 0$. Line L6 asks the invariant to exclude the bad point; it also fixes the scale, since $(c, d) = (0, 0)$ is excluded. Before the loop, the code checks with one linear program that $\mathit{Init}$ is not empty, and drops every transition with an empty relation.

The product $\mu c$ in line L4 is the only nonlinear term. Colon, Sankaranarayanan and Sipma kept $\mu$ as an unknown and solved the nonlinear system by quantifier elimination. Fixing $\mu$ to a value from a small set $M$, as later work does with $M = \{0, 1\}$, makes each choice a linear program. $\mu = 0$ means the transition forces the invariant by itself, whatever the old state; $\mu = 1$ means it keeps $c \cdot x + d$ from growing. The code solves the programs with an exact two-phase [simplex method](/simplex-method/) over the rationals.

## Example

The loop of Colon, Sankaranarayanan and Sipma (Fig. 1 of the paper) starts with $(i, j) = (2, 0)$ and repeats for ever one of two steps: $i := i + 4$, or $(i, j) := (i + 2, j + 1)$. The reachable states are $(2 + 4a + 2b, b)$ for $a, b \ge 0$. With $M = \{1, 0\}$, tried in this order:

| bad point | first feasible choice | invariant found | read as |
|---|---|---|---|
| $(0, 0)$ | (cons 1, cons 1) | $-i + 2 \le 0$ | $i \ge 2$ |
| $(3, 1)$ | (cons 1, cons 1) | $-i + 2j + 2 \le 0$ | $i \ge 2j + 2$ |
| $(10, -1)$ | (cons 1, cons 1) | $-j \le 0$ | $j \ge 0$ |
| $(6, 2)$ | none of the 9 | none | reachable: $(2,0) \to (4,1) \to (6,2)$ |

Check the second row by hand. Initiation: the rows $i = 2$ and $j = 0$ with weights $-1$ and $2$ give $-i + 2j = -2$, so $-i + 2j + 2 \le 0$ holds at the start; equality rows may have weights of any sign. Consecution of the first step: the row $i' - i = 4$ with weight $-1$ and $j' - j = 0$ with weight $2$, plus the old invariant with $\mu = 1$, sum to $-i' + 2j' + 2 \le -4$, which is stronger than needed. The second step gives $-i' + 2j' + 2 \le 0$ exactly. Target: $-3 + 2 + 2 = 1 \ge 1$. The paper lists $j \ge 0$ and $i \ge 2j + 2$ as the generators of all inductive inequalities of this loop; $i \ge 2$ follows from them. Each run of the algorithm returns one inequality; running it with several bad points collects several.

## Correctness

The full proof is in the proof file. Its steps:

1. **Affine Farkas lemma.** If $Ay \le b$ has a rational solution, then all its solutions satisfy $w \cdot y \le \delta$ if and only if $\lambda A = w$ and $\lambda b \le \delta$ for some $\lambda \ge 0$. The system has no solution if and only if $\lambda A = 0$ and $\lambda b < 0$ for some $\lambda \ge 0$. Both follow from [linear programming duality](/dual-linear-program/).
2. **Exact conditions.** With $\mathit{Init}$ and every transition nonempty, $c \cdot x + d \le 0$ is inductive over $\mathbb{Q}$ if and only if initiation has multipliers as in L2 and every transition satisfies the case cons for some $\mu \ge 0$ or the case dis. In the case dis, $\mu$ can always be scaled to 1, so only the consecution multiplier $\mu$ restricts the method.
3. **Soundness.** A returned $(c, d)$ satisfies these conditions, so it is inductive over $\mathbb{Q}$, hence over $\mathbb{Z}$, and holds in every reachable state by induction on the run. It is false at the bad point by L6.
4. **Completeness relative to $M$.** If some inductive inequality excludes the bad point and its consecution multipliers lie in $M$, scale its coefficients and multipliers by a large enough positive number; it then satisfies the system of its choice of cases with the rows $\le -1$ and $\ge 1$. The algorithm tries every choice, so it does not return "none".

With $\mu$ free, step 2 is exactly Theorem 2 of the paper: the method is sound and complete for the single linear inequalities that are inductive over the rationals.

## Complexity

There are $(|M| + 1)^k$ choices of cases, one linear program each, plus $k + 1$ emptiness checks. Each program has $n + 1$ free unknowns $c$, $d$ and one multiplier per row, $O(n + m)$ unknowns in all, and $O(nk)$ constraints: $n$ equalities for initiation, $2n$ per transition, and $k + 2$ inequalities. So the time is $O((|M| + 1)^k L)$, where $L$ is the cost of one program. Linear programming is polynomial with the [ellipsoid method](/ellipsoid-method/) or [interior-point methods](/interior-point-method/); the simplex method of the code is exponential in the worst case but fast on these sizes. The exponential factor in $k$ comes from the case split; the paper's original method instead pays for quantifier elimination over the reals, which is doubly exponential in the worst case for [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/). The space is the simplex tableau, $O(nk(n + m))$ numbers.

## Properties

- **No widening.** Unlike [abstract interpretation](/abstract-interpretation/) with the [polyhedra domain](/polyhedra-domain/), the method does not iterate and extrapolate, so it does not lose an invariant to a [widening](/widening-operator/) step. The paper's INCREMENT example shows an invariant $i \ge 1$ that the classic polyhedra analysis misses and the constraint method finds.
- **Goal-directed.** The target row L6 asks for an invariant that proves something. Without it, the solutions form a polyhedral cone, and its generators are all the inductive inequalities at once, which is what the paper computes.
- **Exact arithmetic matters.** A floating-point solver can return coefficients that are inductive only up to rounding. The code works over the rationals, and the tests check each answer with a separate exact linear program.
- **Rational, not integer.** The invariants are inductive over $\mathbb{Q}^n$. For an integer program they are sound, but some integer invariants have no rational counterpart; see the pitfalls.

## Variants and improvements

- **Nonlinear solving.** The original method keeps $\mu$ as an unknown and eliminates the quantifiers over the reals, which is complete for the template but costly. Sankaranarayanan, Sipma and Manna simplified this step so that it scales to larger loops.
- **Several locations.** For a program with several cut points, put one template at each and write one table per path between them. The unknowns are shared, so it is still one system per choice of cases.
- **Conjunctions.** A template with $k$ inequalities is much harder, because consecution of one inequality may need the others. In practice one strengthens the transitions with the inequalities already found and runs again.
- **Termination.** The same Farkas encoding, applied to "decreases by at least 1 and is bounded below", gives [linear ranking function synthesis](/ranking-function-synthesis/).
- **Boolean encodings.** Gulwani, Srivastava and Venkatesan encode the same constraints, with bounded integer coefficients, into SAT, and handle templates with disjunctions.
- **Nonlinear templates.** Polynomial invariants can use the same idea with a Positivstellensatz in place of Farkas' lemma, which leads to [semidefinite programs](/semidefinite-programming/).

## When to use it

Use it when the invariant you need is a linear relation between several variables with coefficients you cannot guess, the loop body is linear or can be over-approximated by linear relations, and the loop is small. If you can guess the candidates, [Houdini](/houdini-algorithm/) is cheaper. If you need many invariants of a fixed simple shape for a large program, the [octagon](/octagon-domain/) or [interval](/interval-domain/) domains scale better.

## Pitfalls

- **Rational is not integer.** For $x := 0$ followed by $\mathbf{while}\ 2x \le 1\ \mathbf{do}\ x := 2x + 1$, the reachable states are 0 and 1, and $x \le 1$ is inductive over the integers. But $x = 1/2$ satisfies the guard and goes to 2, so every rational inductive inequality holds at 2, and the algorithm returns "none" for the bad point 2. Tighten the guard to its [integer hull](/integer-hull/) $x \le 0$ first; then $x \le 1$ is found. The tests check both.
- **A finite $M$ misses invariants.** For $x := 1$ followed by $x := 2x$ for ever, $x \ge 1$ is inductive, but its only consecution certificate has $\mu = 2$. With $M = \{0, 1\}$ the algorithm returns "none" for the bad point $-1$; with $2 \in M$ it finds $x \ge 1$.
- **Forgetting the disabled case.** Without line L5, a transition that can never fire from the invariant still needs a consecution certificate, and the method can miss invariants that only hold because a guard is false.
- **One inequality is not enough.** For $x := 1$ followed by $x := x + 2$ for ever, the reachable set is the odd positive numbers; no linear inequality separates it from 2. A single inequality can only describe a half-space, and conjunctions only a convex set.
- **Mistaking the test oracle for a proof.** The linear programs decide inductiveness over $\mathbb{Q}$ exactly. The tests also check the answers on a box of integer states and on random runs; those are bounded checks, evidence and not proof.

## Implementations

## History

Colon, Sankaranarayanan and Sipma presented the method at CAV 2003. They encoded initiation and consecution of a linear template with Farkas' lemma, observed that consecution is nonlinear because of the multiplier $\mu$, and solved the constraints by quantifier elimination with factorization heuristics. They proved that the constraints describe exactly the inductive inequalities and showed loops where the method beats polyhedra analysis with widening. Sankaranarayanan, Sipma and Manna made the method scale at SAS 2004. In the same years Podelski and Rybalchenko used Farkas' lemma for ranking functions, and Gulwani, Srivastava and Venkatesan later generalized templates and solved them with SAT solvers. Real tools now pass these constraints to LP, SMT or SAT solvers.

## References
