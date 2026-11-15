---
tag: HA12CT
kind: algorithm
slug: ranking-function-synthesis
name: Linear ranking function synthesis
aliases:
- Podelski-Rybalchenko ranking functions
area: compilers-and-program-analysis/verification-and-synthesis
level: research
summary: Decides whether a simple linear loop has a linear ranking function and finds one, by linear programming.
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of rows of the loop relation, L: the cost of one exact linear program with 2m unknowns and 3n + 1 constraints}
  time: {worst: O(m n + L)}
  space: {extra: O(n (m + n))}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2004
  people: [Andreas Podelski, Andrey Rybalchenko]
  note: Podelski and Rybalchenko (VMCAI 2004) reduced the existence of a linear ranking function for a single-path linear loop to one linear program and proved the method complete over the rationals.
prereqs: [termination-proof, farkas-lemma, linear-programming-problem]
see_also: [farkas-invariant-generation, transition-invariants, size-change-termination, variant-function, total-correctness, lexicographic-order, integer-hull, halting-problem]
sources:
  - paper: doi:10.1007/978-3-540-24622-0_20
    title: Andreas Podelski and Andrey Rybalchenko, A complete method for the synthesis of linear ranking functions, Proceedings of VMCAI 2004, LNCS 2937
    locator: pp. 239 to 251, the theorem with the multipliers lambda1, lambda2 and the conditions lambda1 A' = 0, (lambda1 - lambda2) A = 0, lambda2 (A + A') = 0, lambda2 b < 0, and the construction of the ranking function and its bound
  - paper: doi:10.1145/2629488
    title: Amir M. Ben-Amram and Samir Genaim, Ranking functions for linear-constraint loops, Journal of the ACM 61(4), 2014
    locator: article 26, the proof that the existence of a linear ranking function over the integers is coNP-complete, and the PTIME result over the rationals
  - paper: doi:10.1007/3-540-45319-9_6
    title: Michael A. Colon and Henny B. Sipma, Synthesis of linear ranking functions, Proceedings of TACAS 2001, LNCS 2031
    locator: pp. 67 to 81, the earlier synthesis method with polyhedral cones
  - paper: doi:10.1145/1133981.1134029
    title: Byron Cook, Andreas Podelski and Andrey Rybalchenko, Termination proofs for systems code, Proceedings of PLDI 2006
    locator: the Terminator tool, which calls a ranking function synthesizer on each path it finds
  - url: https://arxiv.org/abs/1004.0944
    title: Roberto Bagnara, Fred Mesnard, Andrea Pescetti and Enea Zaffanella, The automatic synthesis of linear ranking functions, the complete unabridged version, arXiv 1004.0944
    locator: the comparison of the Podelski-Rybalchenko method with the other complete methods for linear ranking functions
---

Linear ranking function synthesis decides whether a loop of the form "while some linear constraints hold, update the variables linearly" has a linear function of the variables that is bounded below and drops by at least 1 on every turn, and finds one if it exists. Podelski and Rybalchenko showed that the whole question is one [linear program](/linear-programming-problem/): two vectors of nonnegative multipliers, three matrix equations and one inequality, obtained with [Farkas' lemma](/farkas-lemma/). A solution gives the ranking function directly, which is a [termination proof](/termination-proof/); no solution means that no linear ranking function exists over the rationals.

## In plain words

To show that a loop stops, find a number that you can compute from the variables, that goes down by at least one on every turn, and that can never go below some floor. It can only go down so many times, so the loop must stop. This page looks for the simplest kind of such number, a weighted sum of the variables. The conditions "it goes down on every turn" and "it stays above the floor" must follow from the loop's own conditions. An old result says this happens exactly when the needed inequality is a sum of the loop's inequalities with nonnegative weights. So the search for the weights of the function becomes a search for those other weights, and that is a standard problem with an exact answer.

## The problem

The loop is a single-path linear loop over $n$ rational variables. Its body is one relation $R = \{(x, x') : A x + A' x' \le b\}$ between the state $x$ before a turn and the state $x'$ after it, with $m$ rows. A guard and an assignment, $\mathbf{while}\ Gx \le g\ \mathbf{do}\ x := Ux + u$, give such a relation, and so does a nondeterministic body like $x' \le x - 1$. A *linear ranking function* is a vector $\rho$ with numbers $\delta_0$ and $\delta > 0$ such that every $(x, x') \in R$ has $\rho \cdot x \ge \delta_0$ and $\rho \cdot x - \rho \cdot x' \ge \delta$. The output is such a function, scaled so that $\delta \ge 1$, or "none".

Termination of general programs is undecidable, by the [halting problem](/halting-problem/) and [Rice's theorem](/rice-theorem/), so every method is incomplete for some programs. This one is complete for its class: it decides in polynomial time whether a linear ranking function exists over $\mathbb{Q}$. Over the integers the same question is [coNP](/co-np/)-complete, as Ben-Amram and Genaim proved.

## The algorithm

```pseudo id=main
LINEAR-RANKING(A, A', b)
L1  find lambda1, lambda2 >= 0 with
L2      lambda1 A' = 0
L3      (lambda1 - lambda2) A = 0
L4      lambda2 (A + A') = 0
L5      lambda2 b <= -1
L6  if no solution exists then return none
L7  rho <- lambda2 A'
L8  return (rho, bound -lambda1 b, decrease -lambda2 b)
```

The multipliers $\lambda_1$ and $\lambda_2$ have one entry per row of the loop. $\lambda_1$ is a certificate that $\rho \cdot x$ is bounded below: a nonnegative combination of the rows that mentions only $x$ (line L2) and equals $-\rho \cdot x \le \lambda_1 b$. $\lambda_2$ is a certificate of the decrease: a combination that equals $-\rho \cdot x + \rho \cdot x' \le \lambda_2 b$. Both must name the same $\rho$, which is line L3 together with line L4, and the decrease must be positive, which is line L5 after scaling. The code solves the system with an exact two-phase [simplex method](/simplex-method/) over the rationals and minimizes the sum of the multipliers to keep the numbers small.

## Example

The loop is $\mathbf{while}\ x \ge y + 1\ \mathbf{do}\ (x, y) := (x - 1, y + 1)$. Over the variables $(x, y, x', y')$ it has five rows: the guard, and two rows for each of the equalities $x' = x - 1$ and $y' = y + 1$.

| row | $A x + A' x' \le b$ | $\lambda_1$ | $\lambda_2$ |
|---|---|---|---|
| 1 | $-x + y \le -1$ | $1/2$ | 0 |
| 2 | $-x + x' \le -1$ | 0 | $1/2$ |
| 3 | $x - x' \le 1$ | 0 | 0 |
| 4 | $-y + y' \le 1$ | 0 | 0 |
| 5 | $y - y' \le -1$ | 0 | $1/2$ |

The sum of the rows with weights $\lambda_2$ is $\tfrac12(-x + x') + \tfrac12(y - y') \le -1$, that is, $\rho \cdot x - \rho \cdot x' \ge 1$ for $\rho = (\tfrac12, -\tfrac12)$, which is $\lambda_2 A'$. The sum with weights $\lambda_1$ is $\tfrac12(-x + y) \le -\tfrac12$, that is, $\rho \cdot x \ge \tfrac12$, with no $x'$ in it. So $(x - y)/2$ is a ranking function with bound $1/2$ and decrease 1. From $(x, y) = (5, 0)$ it takes the values $5/2, 3/2, 1/2$ at the states that take a step, and the run stops after 3 steps, within the bound $(5/2 - 1/2)/1 + 1 = 3$.

## Correctness

The full proof is in the proof file.

1. **Soundness.** From L3 and L4, $\rho = \lambda_2 A' = -\lambda_2 A = -\lambda_1 A$. For $(x, x') \in R$: $\rho \cdot x = -\lambda_1 (A x + A' x') \ge -\lambda_1 b$ by L2 and $\lambda_1 \ge 0$, and $\rho \cdot x - \rho \cdot x' = -\lambda_2 (A x + A' x') \ge -\lambda_2 b \ge 1$ by L5.
2. **Completeness over $\mathbb{Q}$.** Suppose $(\rho, \delta_0, \delta)$ is a linear ranking function. If $R$ is empty, Farkas' lemma gives $\lambda$ with $\lambda [A \; A'] = 0$ and $\lambda b < 0$; take $\lambda_1 = \lambda_2 = \lambda$, scaled. Otherwise the affine Farkas lemma, applied to the two implications "$R$ implies $-\rho \cdot x \le -\delta_0$" and "$R$ implies $-\rho \cdot x + \rho \cdot x' \le -\delta$", gives $\lambda_1$ and $\lambda_2$ that satisfy L2 to L4 and $\lambda_2 b \le -\delta < 0$. Scale both by $1/\min(\delta, 1)$.
3. **Termination.** With a ranking function, a run from $x_0$ has at most $\lfloor(\rho \cdot x_0 - \delta_0)/\delta\rfloor + 1$ steps, because $\rho$ drops by $\delta$ on each step and is at least $\delta_0$ before each step. This holds over $\mathbb{Q}^n$ and so over $\mathbb{Z}^n$.

## Complexity

Building the system takes $O(mn)$ time. It has $2m$ nonnegative unknowns, $3n$ equalities and one inequality, and one exact linear program solves it, in time $L$. Linear programming is polynomial with the [ellipsoid method](/ellipsoid-method/) or [interior-point methods](/interior-point-method/), so the problem is in polynomial time over the rationals; the simplex method of the code is exponential in the worst case but fast at these sizes. The tableau has $3n + 1$ rows and $O(m + n)$ columns.

On 500 random loops of the tests (seed 77, two variables, one or two random guard rows, a random affine update with small integer coefficients), 158 got a ranking function and 342 got "none"; for 80 of the 342, an integer run from a sampled start state repeated a state, so the loop does not terminate.

## Properties

- **A decision procedure.** For single-path linear loops over $\mathbb{Q}$, "none" is a proof that no linear ranking function exists, not a timeout.
- **Certificates both ways.** A solution is a checkable certificate of termination. When the system has no solution, Farkas' lemma applied to it gives a certificate of that too.
- **Nondeterminism is free.** The relation need not be a function: any polyhedron of pairs works, so havoc, bounds on inputs and abstracted operations fit.
- **Only one phase.** The function must decrease on every turn from every state. Loops whose progress has phases need a lexicographic or multiphase function.

## Variants and improvements

- **Lexicographic ranking functions.** A tuple of linear functions, ordered by the [lexicographic order](/lexicographic-order/), proves termination of loops with several paths or phases. Ben-Amram and Genaim give complete PTIME synthesis over the rationals for these too.
- **Integer loops.** Over $\mathbb{Z}$ one first replaces the relation by its [integer hull](/integer-hull/), which can be exponentially larger; Ben-Amram and Genaim show that the integer problem is coNP-complete.
- **Many paths.** For a program with several paths, Terminator by Cook, Podelski and Rybalchenko finds a path that is not yet covered, synthesizes a ranking function for it with this method, and checks the [transition invariant](/transition-invariants/) built from all of them.
- **Earlier methods.** Colon and Sipma synthesized linear ranking functions with polyhedral cones in 2001. Bagnara, Mesnard, Pescetti and Zaffanella compare the complete methods.
- **With invariants.** A loop often needs an invariant to terminate, such as $y \ge 1$ that comes from the code before it. Add it to the guard first, or find it together with the ranking function with the [constraint-based method](/farkas-invariant-generation/), which uses the same Farkas encoding.

## When to use it

Use it inside a termination prover, on each loop or each path a model checker finds, after strengthening the loop with known invariants. It is cheap, exact and gives a certificate. If it says "none", try a lexicographic or multiphase ranking function, look for a missing invariant, or for integer programs try the integer hull. For whole programs with recursion, [size-change termination](/size-change-termination/) is a different decidable method.

## Pitfalls

- **Rational is not integer.** The loop $2x \ge 1 \wedge 2x \le 1$, $x' = x$ never runs over the integers, so every function ranks it there, but the rational state $1/2$ loops for ever and the method says "none". The loop $x \ge 0$, $x := 10 - 2x$ terminates from every integer, since the distance to $10/3$ doubles each step, but $10/3$ is a rational fixed point. A "none" says nothing about integer termination. A function that is found does prove integer termination.
- **Termination without a linear ranking function.** The loop $x \ge 0$, $x' = x + y$, $y' = y - 1$ terminates from every rational state, but $\rho \cdot x - \rho \cdot x' = -p y + q$ must be positive for every $y$, which forces $\rho = (0, q)$, and then $\rho \cdot x = q y$ is not bounded below. The tests check that every $\rho$ in $\{-3, \ldots, 3\}^2$ fails.
- **Forgetting the bound.** A function that only decreases, such as $x$ for $x' = x - 1$ without a guard, proves nothing; $\lambda_1$ is there to prove the floor.
- **Decrease by a positive amount, not just down.** Over $\mathbb{Q}$, decreasing by ever smaller amounts need not stop. The method asks for a fixed $\delta > 0$, scaled to 1.
- **Reading the tests as a proof.** The linear program is exact. The tests also sample integer and rational transitions and run the loop; those checks are bounded, evidence and not proof.

## Implementations

## History

Floyd's method of 1967 already proved termination with a function into a [well-founded](/well-founded-relation/) set. Colon and Sipma gave an algorithm for linear ranking functions with polyhedral cones in 2001. Podelski and Rybalchenko gave the linear-programming characterization at VMCAI 2004 and proved it complete for single-path linear loops over the rationals. They built on it in the same year with transition invariants, and in 2006 with Cook in the Terminator tool, which proved termination of Windows device drivers. Ben-Amram and Genaim settled the integer case in 2014: deciding whether a linear ranking function exists over the integers is coNP-complete.

## References
