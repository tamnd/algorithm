---
tag: C7XFRF
kind: problem
slug: one-in-three-sat
name: One-in-three SAT
aliases:
- 1-in-3-SAT
- exactly-one 3-SAT
area: complexity/reductions-catalogue
level: advanced
summary: Decide whether a formula of three-literal clauses has an assignment that makes exactly one literal true in every clause. NP-complete, even with no negated literals.
prereqs: [3-sat, np-complete, polynomial-time-reduction]
see_also: [not-all-equal-sat, schaefer-dichotomy-theorem, exact-cover, exact-cover-by-3-sets, zero-one-equations, xor-sat, gadget-reduction, parsimonious-reduction]
sources:
  - paper: doi:10.1145/800133.804350
    title: Thomas J. Schaefer, The complexity of satisfiability problems, Proceedings of the 10th Annual ACM Symposium on Theory of Computing, 1978, pages 216 to 226
    locator: the dichotomy theorem, with the relation "exactly one of three" among the NP-complete cases
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A9.1, problem LO4 (One-in-three 3SAT), with the comment that it stays NP-complete with no negated literals
---

One-in-three SAT asks whether a formula made of clauses with three literals has an assignment under which every clause has exactly one true literal. It is [NP-complete](/np-complete/), and Schaefer (1978) showed that it stays NP-complete when no literal is negated. In that monotone form, each clause is a set of three variables and exactly one of them must be true, so the problem is a form of [exact cover](/exact-cover/) in which every element is in exactly three sets. Its rigid "exactly one" condition makes it a convenient source for reductions to puzzles, tilings and number problems, where a gadget must be used in exactly one way.

## In plain words

Three friends share a car, and exactly one of them must drive each day. Some friends are in several groups, and a person who drives drives for every group they belong to. Can we choose drivers so that each group has exactly one?

Ordinary satisfiability asks for at least one true literal in each clause. Here "at least one" becomes "exactly one", which is stricter. It still contains ordinary satisfiability: a small chain of three exactly-one clauses, with four helper variables, can be completed exactly when at least one of three given literals is true. Replacing every clause by this chain turns any 3-SAT question into a one-in-three question.

## Definition

**Instance.** A formula $\varphi = C_1 \land \cdots \land C_m$ over variables $x_1, \ldots, x_n$, in which each clause $C_j$ is a list of three literals. In the monotone (positive) form, every literal is a variable.

**Question.** Is there an assignment under which every clause has exactly one true literal?

**Encoding.** The formula is a list of clauses, with variable indices in binary. The certificate is the assignment, and the verifier counts the true literals of each clause, in linear time on a [word RAM](/word-ram/) and in polynomial time on the [multitape Turing machine](/multitape-turing-machine/). So the problem is in NP.

**Complexity.** NP-complete under Karp (polynomial-time many-one) reductions, from [3-SAT](/3-sat/). It stays NP-complete with no negated literals (Schaefer 1978; Garey and Johnson problem LO4).

## Variants

- **Monotone one-in-three SAT.** No negated literals. A solution is a set $S$ of true variables that meets every clause in exactly one variable, which is [exact cover](/exact-cover/) of the clauses by the sets "clauses that contain $x_i$". It is NP-complete.
- **Exactly one in two.** The clause "exactly one of $a, b$" means $a \ne b$, so the problem with two literals per clause is a system of equations modulo 2 and is in P; see [XOR-SAT](/xor-sat/).
- **Exactly one of three, modulo 2.** Replacing "exactly one" by "an odd number" gives the linear equation $a \oplus b \oplus c = 1$, which [Gaussian elimination](/gaussian-elimination/) solves. This is why the integer count, not the parity, makes the problem hard.
- **Not all equal.** Asking for at least one true and one false literal gives [not-all-equal SAT](/not-all-equal-sat/). Every one-in-three assignment is also a not-all-equal assignment.

## Examples

**The gadget.** Write $R(p, q, r)$ for "exactly one of $p, q, r$ is true". The clause $(x \lor y \lor z)$ becomes
$$R(\lnot x, a, b) \land R(b, y, c) \land R(c, d, \lnot z)$$
with new variables $a, b, c, d$. A script listed, for each value of $(x, y, z)$, all values of $(a, b, c, d)$ that satisfy the three clauses:

| $x y z$ | extensions $a b c d$ |
|---|---|
| 000 | none |
| 001 | 0010 |
| 010 | 0000 |
| 011 | 0001 |
| 100 | 0100 |
| 101 | 0101 and 1010 |
| 110 | 1000 |
| 111 | 1001 |

So the chain can be completed if and only if at least one of $x, y, z$ is true.

**The reduction on a small formula.** Take
$$\varphi = (x_1 \lor x_2 \lor \lnot x_3) \land (\lnot x_1 \lor x_2 \lor x_3) \land (\lnot x_1 \lor \lnot x_2 \lor \lnot x_3),$$
with the 5 satisfying assignments $000, 010, 011, 101, 110$. The reduction gives 15 variables and 9 clauses. The script found 6 one-in-three assignments, which restrict to exactly the 5 satisfying assignments: for $010$ the third clause gets the pattern $(\lnot x_1, \lnot x_2, \lnot x_3) = (1, 0, 1)$, which has two extensions, and the other assignments extend in one way each. So the reduction is not [parsimonious](/parsimonious-reduction/).

- **Forward.** For $x = 010$, the first clause has $(x, y, z) = (x_1, x_2, \lnot x_3) = (0, 1, 1)$, which extends by $a b c d = 0001$.
- **Backward.** Every solution of the 9 clauses gives an assignment of $x_1, x_2, x_3$, and each one satisfies $\varphi$.

**Removing negations.** The script then replaced each negated literal $\lnot v$ by a new variable $v'$ and added $R(v, v', F)$ for each such $v$, and $R(F, F, G)$ once. Here $x_1$, $x_2$ and $x_3$ occur negated, so the monotone instance has $15 + 3 + 2 = 20$ variables and $9 + 3 + 1 = 13$ clauses. On 120 random formulas, and on 60 dense formulas of which 20 are unsatisfiable, both the instance with negations and the monotone instance had a solution exactly when the formula was satisfiable.

## Known algorithms

- **Brute force.** Try all $2^n$ assignments.
- **Branching.** Setting one variable of a clause to true sets the other two to false, so branching on the clauses propagates far. Exact cover solvers, such as Knuth's Algorithm X, apply directly to the monotone form; see [exact cover](/exact-cover/).
- **Through SAT solvers.** Write $R(p, q, r)$ as the four clauses $(p \lor q \lor r)$, $(\lnot p \lor \lnot q)$, $(\lnot p \lor \lnot r)$, $(\lnot q \lor \lnot r)$ and use a [CDCL](/cdcl/) solver.

## Bounds

- **NP-completeness.** No polynomial-time algorithm exists unless P = NP.
- **Dichotomy.** In [Schaefer's dichotomy theorem](/schaefer-dichotomy-theorem/), the relation $R$ is none of 0-valid, 1-valid, Horn, dual-Horn, bijunctive or affine, so the problem with only this relation, and no constants or negations, is NP-complete.

## Reductions

**From 3-SAT (Karp reduction).** Let $\varphi$ have clauses $C_j = (x_j \lor y_j \lor z_j)$, where $x_j, y_j, z_j$ are literals.

- *Map.* For each clause, add four new variables $a_j, b_j, c_j, d_j$ and the three clauses $R(\lnot x_j, a_j, b_j)$, $R(b_j, y_j, c_j)$, $R(c_j, d_j, \lnot z_j)$. The result has $n + 4m$ variables and $3m$ clauses, and is written in linear time.
- *Gadget lemma.* For fixed values of $x, y, z$, the three clauses have a solution in $a, b, c, d$ if and only if at least one of $x, y, z$ is true.
  - If $x = y = z = 0$: the first clause $R(1, a, b)$ forces $a = b = 0$; the second, $R(0, 0, c)$, forces $c = 1$; then the third is $R(1, d, 1)$, which has two true literals. So there is no solution.
  - Otherwise the table under Examples gives a solution for each of the seven other values.
- *If $\varphi$ is satisfiable, then the new formula has a one-in-three assignment.* Take a satisfying assignment. Each clause has a true literal, so by the lemma its gadget variables can be set. The gadgets of different clauses have disjoint new variables, so these choices do not conflict.
- *If the new formula has a one-in-three assignment, then $\varphi$ is satisfiable.* Take any solution and restrict it to $x_1, \ldots, x_n$. For each clause $C_j$ its gadget is satisfied, so by the lemma one of $x_j, y_j, z_j$ is true.

**Removing negations.** Replace every negated literal $\lnot v$ by a new variable $v'$, and add the clauses $R(v, v', F)$ and $R(F, F, G)$ with two new variables $F$ and $G$. The clause $R(F, F, G)$ forces $F = 0$ and $G = 1$, because two copies of $F$ cannot hold exactly one true literal unless $F$ is false. Then $R(v, v', F)$ forces $v' = \lnot v$. So the monotone formula has a solution if and only if the original one does.

**To exact cover and zero-one equations.** For a monotone instance, take the clauses as rows and the variables as columns, with a 1 where a variable is in a clause. A one-in-three assignment is then exactly a 0-1 solution of $Ax = \mathbf{1}$, which is the [zero-one equations](/zero-one-equations/) problem. This needs the three variables of each clause to be distinct. In the monotone formula above only $R(F, F, G)$ repeats a variable; first substitute its forced values $F = 0$ and $G = 1$, which leaves rows with two 1s for the clauses $R(v, v', F)$.

## Applications

- **Puzzles and tilings.** Many NP-completeness proofs for puzzles start from one-in-three SAT, because a piece that must be placed in exactly one of three positions is easy to build.
- **Number problems.** Through exact cover, one-in-three SAT leads to [3-dimensional matching](/three-dimensional-matching/), [subset sum](/subset-sum-problem/) and other number problems.
- **Constraint satisfaction.** It is a standard example of a hard Boolean constraint language in the [Schaefer dichotomy](/schaefer-dichotomy-theorem/).

## References
