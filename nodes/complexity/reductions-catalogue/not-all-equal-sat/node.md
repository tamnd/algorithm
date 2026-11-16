---
tag: 3S4V1P
kind: problem
slug: not-all-equal-sat
name: Not-all-equal SAT
aliases:
- NAE-SAT
area: complexity/reductions-catalogue
level: advanced
summary: Decide whether a CNF formula has an assignment that gives every clause at least one true and at least one false literal. NP-complete, also with three literals per clause.
prereqs: [3-sat, np-complete, polynomial-time-reduction]
see_also: [one-in-three-sat, schaefer-dichotomy-theorem, maximum-cut, hypergraph, xor-sat, 2-sat, three-coloring, gadget-reduction]
sources:
  - paper: doi:10.1145/800133.804350
    title: Thomas J. Schaefer, The complexity of satisfiability problems, Proceedings of the 10th Annual ACM Symposium on Theory of Computing, 1978, pages 216 to 226
    locator: the dichotomy theorem, with the not-all-equal relation among the NP-complete cases
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A9.1, problem LO3 (Not-all-equal 3SAT), and Appendix A3.1, problem SP4 (Set splitting)
---

Not-all-equal SAT asks whether a formula in conjunctive normal form has an assignment under which no clause has all its literals equal: every clause must contain a true literal and a false literal. NAE-3SAT is the case with three literals per clause. Both are [NP-complete](/np-complete/); Schaefer (1978) put NAE-3SAT among the hard cases of his [dichotomy theorem](/schaefer-dichotomy-theorem/). The problem has a useful symmetry: if an assignment works, so does its complement. That symmetry makes it a natural source for reductions to problems with two equal sides, such as [max cut](/maximum-cut/) and coloring of [hypergraphs](/hypergraph/) with two colors.

## In plain words

Think of a set of teams, where each team has three players and each player is on a red side or a blue side. The rule is that no team may be all red or all blue. Is there a way to choose sides?

This looks like ordinary satisfiability, but with an extra rule: a clause must not be all true either. Swapping red and blue everywhere keeps every team mixed, so solutions come in pairs.

The proof of hardness adds one shared player, call it the referee, to every clause of an ordinary formula. We may assume the referee is false. Then a clause is mixed exactly when it has a true literal, which is ordinary satisfiability.

## Definition

**Instance.** A Boolean formula $\varphi = C_1 \land \cdots \land C_m$ in conjunctive normal form over variables $x_1, \ldots, x_n$. In NAE-3SAT each clause has exactly three literals.

**Question.** Is there an assignment under which every clause $C_j$ has at least one true literal and at least one false literal?

**Encoding.** The formula is a list of clauses, each a list of literals with variable indices in binary. The certificate is the assignment, and the verifier checks each clause in time linear in the formula length, which is polynomial on the [multitape Turing machine](/multitape-turing-machine/). So the problem is in NP.

**Complexity.** NP-complete under Karp (polynomial-time many-one) reductions, from [3-SAT](/3-sat/). It stays NP-complete with three literals per clause (Garey and Johnson problem LO3) and with no negated literals (Schaefer 1978).

## Variants

- **Monotone NAE-3SAT.** No literal is negated. Each clause is then a set of three variables that must not get one value, which is 2-coloring a 3-uniform [hypergraph](/hypergraph/), also called set splitting (Garey and Johnson problem SP4). It is NP-complete.
- **Two literals per clause.** $\mathrm{NAE}(a, b)$ means $a \ne b$, so NAE-2SAT is a system of equations modulo 2 and is in P; it is a special case of [XOR-SAT](/xor-sat/) and of [2-SAT](/2-sat/).
- **Exactly one true.** Asking for exactly one true literal per clause gives [one-in-three SAT](/one-in-three-sat/), also NP-complete.
- **Max NAE-SAT.** Maximize the number of NAE-satisfied clauses. With two literals per clause and no negations this is [max cut](/maximum-cut/).

## Examples

**Small cases.** The clause $\mathrm{NAE}(x_1, x_2, x_3)$ alone has 6 solutions out of 8: all except $000$ and $111$. The formula $\mathrm{NAE}(x_1, x_2, x_3) \land \mathrm{NAE}(x_1, \lnot x_2, x_3)$ has the 4 solutions $001, 011, 100, 110$, so it forces $x_1 \ne x_3$: if $x_1 = x_3$, one of the two clauses has all literals equal.

**The reduction on a small formula.** Take
$$\varphi = (x_1 \lor x_2 \lor \lnot x_3) \land (\lnot x_1 \lor x_2 \lor x_3) \land (\lnot x_1 \lor \lnot x_2 \lor \lnot x_3),$$
which has the 5 satisfying assignments $000, 010, 011, 101, 110$. The reduction below adds a shared variable $w$ and one variable $y_j$ per clause. A script built the result, with 7 variables and 6 clauses:
$$\mathrm{NAE}(x_1, x_2, y_1),\ \mathrm{NAE}(\lnot y_1, \lnot x_3, w),\ \mathrm{NAE}(\lnot x_1, x_2, y_2),\ \mathrm{NAE}(\lnot y_2, x_3, w),\ \mathrm{NAE}(\lnot x_1, \lnot x_2, y_3),\ \mathrm{NAE}(\lnot y_3, \lnot x_3, w).$$

- **Forward.** The satisfying assignment $x = 010$ with $w = 0$ extends: clause 1 has $x_2$ true, so $y_1$ is free, and so on for each clause.
- **Backward.** The script found 16 NAE assignments. By the symmetry, 8 of them have $w = 0$, and the other 8 are their complements. The 8 with $w = 0$ restrict to exactly the 5 satisfying assignments of $\varphi$.
- **A random check.** On 200 random 3-CNF formulas, and on 60 dense formulas of which 20 are unsatisfiable, the NAE instance had a solution exactly when the formula was satisfiable.

## Known algorithms

- **Brute force.** By the symmetry, fix one variable to false and try the other $2^{n-1}$ assignments.
- **Through SAT solvers.** Write each clause $\mathrm{NAE}(\ell_1, \ldots, \ell_k)$ as the two CNF clauses $(\ell_1 \lor \cdots \lor \ell_k)$ and $(\lnot \ell_1 \lor \cdots \lor \lnot \ell_k)$, and use a [CDCL](/cdcl/) solver.
- **Special cases.** NAE-2SAT is solved by [breadth-first search](/breadth-first-search/) on the graph of the equations $a \ne b$, in linear time.

## Bounds

- **NP-completeness.** No polynomial-time algorithm exists unless P = NP.
- **Dichotomy.** By [Schaefer's dichotomy theorem](/schaefer-dichotomy-theorem/), the not-all-equal relation on three variables is not 0-valid, 1-valid, Horn, dual-Horn, bijunctive or affine, and so it gives an NP-complete problem even without constants.

## Reductions

**From 3-SAT (Karp reduction).** Let $\varphi = C_1 \land \cdots \land C_m$ with $C_j = (a_j \lor b_j \lor c_j)$.

*Map.* Add one new variable $w$, shared by all clauses, and one new variable $y_j$ per clause. Replace $C_j$ by the two clauses
$$\mathrm{NAE}(a_j, b_j, y_j) \land \mathrm{NAE}(\lnot y_j, c_j, w).$$
The result has $n + m + 1$ variables and $2m$ clauses of three literals, and is written in linear time.

*Step 1: four literals.* First consider the formula $\psi$ with the clauses $\mathrm{NAE}(a_j, b_j, c_j, w)$.

- *If $\varphi$ is satisfiable, then $\psi$ is.* Take a satisfying assignment and set $w$ false. Each clause of $\psi$ has a true literal from $C_j$ and the false literal $w$.
- *If $\psi$ is satisfiable, then $\varphi$ is.* Take any NAE assignment of $\psi$. If $w$ is true, complement every variable; each clause still has a true and a false literal, so the result is again an NAE assignment, now with $w$ false. Each clause then has a true literal among $a_j, b_j, c_j$, since $w$ is false and not all literals are false. So the restriction to $x_1, \ldots, x_n$ satisfies $\varphi$.

*Step 2: splitting.* For all values of $a, b, c, w$: $\mathrm{NAE}(a, b, c, w)$ holds if and only if some $y$ gives $\mathrm{NAE}(a, b, y) \land \mathrm{NAE}(\lnot y, c, w)$.

- If $a = b$, take $y = \lnot a$. Then $\mathrm{NAE}(a, a, \lnot a)$ holds, and $\lnot y = a$, so the second clause is $\mathrm{NAE}(a, c, w)$, which holds because one of $c, w$ differs from $a$.
- If $a \ne b$, the first clause holds for any $y$. If $c = w$, take $y = c$, so that $\lnot y \ne c$; otherwise any $y$ works.
- Conversely, if $a = b = c = w = v$, the first clause forces $y = \lnot v$, and then the second clause is $\mathrm{NAE}(v, v, v)$, which fails.

A script checked this equivalence on all 16 values of $(a, b, c, w)$. Steps 1 and 2 together prove both directions of the reduction.

**To max cut.** Each clause $\mathrm{NAE}(a, b, c)$ becomes a triangle on its three literal vertices: a triangle has 2 cut edges when its ends are not all on one side, and 0 otherwise. Heavy edges between $x_i$ and $\lnot x_i$ force them to opposite sides. A cut of the right size then exists exactly when the formula has an NAE assignment, which is a standard proof that [max cut](/maximum-cut/) is NP-hard.

**To hypergraph 2-coloring.** Replace each negated literal $\lnot x$ by a new variable $x'$ and add the clause $\mathrm{NAE}(x, x')$, which forces $x' = \lnot x$. The result has no negations, so it is a 2-coloring problem for a [hypergraph](/hypergraph/) with edges of size 2 and 3. Garey and Johnson list this problem as set splitting.

## Applications

- **Source for symmetric problems.** Problems with two interchangeable sides, such as max cut, set splitting and partitioning a graph into two parts with constraints, are often proved NP-hard from NAE-3SAT, because its symmetry matches theirs.
- **Constraint satisfaction.** NAE-3SAT is a standard example of a hard Boolean constraint language in the [Schaefer dichotomy](/schaefer-dichotomy-theorem/) and in the study of approximation of constraint problems.

## References
