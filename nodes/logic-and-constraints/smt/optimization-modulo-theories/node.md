---
tag: N1ZTCF
kind: problem
slug: optimization-modulo-theories
name: Optimization modulo theories
aliases:
- OMT
- SMT optimization
- optimizing SMT
area: logic-and-constraints/smt
level: research
summary: Optimize an objective subject to SMT constraints over theories such as linear arithmetic.
prereqs: [smt-problem, linear-programming-problem, linear-real-arithmetic-satisfiability]
see_also: [maxsmt, simplex-for-smt, lexicographic-optimization, multi-objective-optimization, pareto-front, binary-search-on-answer, linear-integer-arithmetic-satisfiability, incremental-solving]
sources:
  - paper: "Roberto Sebastiani and Silvia Tomasi, Optimization in SMT with LA(Q) cost functions, International Joint Conference on Automated Reasoning (IJCAR 2012), Lecture Notes in Computer Science 7364, Springer, 2012"
    locator: the definition of OMT over linear rational arithmetic, and the linear, binary and adaptive search with local simplex optimization
  - paper: "Roberto Sebastiani and Silvia Tomasi, Optimization modulo theories with linear rational costs, ACM Transactions on Computational Logic 16(2) (2015)"
    locator: the journal version, with the inline search inside the CDCL loop and the proofs of termination and correctness
  - paper: doi:10.1007/11814948_18
    title: Robert Nieuwenhuis and Albert Oliveras, On SAT modulo theories and optimization problems, Theory and Applications of Satisfiability Testing (SAT 2006), Lecture Notes in Computer Science 4121, Springer, 2006
    locator: optimization in DPLL(T) with a theory of the cost bound that is made stronger during the search
  - paper: doi:10.1007/978-3-662-46681-0_14
    title: Nikolaj Bjørner, Anh-Dung Phan and Lars Fleckenstein, νZ, an optimizing SMT solver, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2015), Lecture Notes in Computer Science 9035, Springer, 2015
    locator: the objective commands of Z3, with lexicographic, Pareto and independent (box) combinations of objectives
  - paper: "Yi Li, Aws Albarghouthi, Zachary Kincaid, Arie Gurfinkel and Marsha Chechik, Symbolic optimization with SMT solvers, Principles of Programming Languages (POPL 2014)"
    locator: the SYMBA algorithm, which optimizes several linear objectives with unbounded directions (to be checked)
  - paper: "Christos H. Papadimitriou, On the complexity of integer programming, Journal of the ACM 28(4) (1981)"
    locator: the bound on the size of optimal integer solutions, used for the NP upper bound of OMT over LIA
---

Optimization modulo theories (OMT) asks for a model of an [SMT](/smt-problem/) formula that minimizes or maximizes an objective term, such as $2x + y$ over the reals. The formula may have arbitrary Boolean structure over theory atoms, so OMT extends [linear programming](/linear-programming-problem/) and integer programming with disjunctions and other theories, and extends SMT with an objective. Solvers combine an SMT solver with a local optimizer for each conjunction of literals, usually [simplex](/simplex-for-smt/). [MaxSMT](/maxsmt/) is the special case whose objective is a weighted count of violated soft formulas; OMT allows any term of the theory and several objectives.

## In plain words

The input is a list of rules about numbers, with "and", "or" and "not" between them, and a quantity to make as small as possible. The task is to find values that keep all rules and give the smallest quantity, or to report that the quantity can go down forever, or that no values keep the rules.

A solver finds some values that keep the rules. It then improves them as far as possible without changing which basic rules are true. Then it asks for values whose quantity is strictly smaller, and repeats until there are none.

## Definition

**Input.** A formula $\varphi$ in a theory $T$ (QF_LRA, QF_LIA, QF_BV and so on) and an objective term $f$ of a numeric sort, in the variables of $\varphi$.

**Output.** One of:

- a model $M$ of $\varphi$ such that $f^M \le f^{M'}$ for each model $M'$ of $\varphi$ (an *optimal* model, and the optimum $f^M$);
- *unbounded*: for each value $c$ there is a model with $f < c$;
- *infimum not attained*: the infimum $\inf f$ over the models is finite but no model reaches it, as for $x > 0$ with the objective $x$ over the reals; solvers report the infimum, often as $c + \epsilon$;
- *unsatisfiable*: $\varphi$ has no model.

Maximization is minimization of $-f$.

**Several objectives.** With objectives $f_1, \ldots, f_k$:

- *lexicographic*: minimize $f_1$, then $f_2$ among the optimal models for $f_1$, and so on (see [lexicographic optimization](/lexicographic-optimization/));
- *Pareto*: find the models on the [Pareto front](/pareto-front/), where no other model is at least as good in all objectives and better in one;
- *independent (box)*: the optimum of each $f_i$ on its own.

**How OMT and MaxSMT differ.** MaxSMT takes soft formulas with weights and minimizes the weight of the violated ones. OMT takes an arbitrary term. A MaxSMT instance is the OMT instance with $f = \sum_i w_i \cdot \mathrm{ite}(S_i, 0, 1)$; but the methods differ, because MaxSMT solvers use unsatisfiable cores of the soft formulas, while OMT solvers over arithmetic use simplex on the objective.

## Variants

- **OMT over LRA.** The common case, decided by SMT search plus simplex.
- **OMT over LIA.** Mixed integer programming with Boolean structure; solvers use branch and bound and cuts in the theory solver.
- **OMT over bit-vectors.** Minimize an unsigned or signed bit-vector term; solvers fix the bits of the objective from the most significant bit down.
- **Multi-objective OMT.** Lexicographic, Pareto and box combinations, as above.
- **MaxSMT.** The objective is a weighted count of violated soft formulas.
- **OMT over nonlinear arithmetic.** Decidable over the reals by [Tarski's theorem](/tarski-decidability-theorem/), since the optimum is definable in first-order logic; undecidable over the integers.

## Examples

Let $x, y$ be reals with $0 \le x \le 3$, $0 \le y \le 3$, $x + y \ge 2$, and the disjunction $x \ge 2 \vee y \ge 2.5$. Minimize $f = 2x + y$. A script with exact rational arithmetic enumerated the vertices of each case and also checked a grid of step $0.1$.

The feasible set is the union of two polygons, so plain linear programming does not apply. The linear search with local optimization runs as follows:

| step | Boolean assignment found | local optimum by simplex | new bound |
|---|---|---|---|
| 1 | $x \ge 2$, not $y \ge 2.5$ | $f = 4$ at $(2, 0)$ | $f < 4$ |
| 2 | not $x \ge 2$, $y \ge 2.5$ | $f = 2.5$ at $(0, 2.5)$ | $f < 2.5$ |
| 3 | none: $\varphi \wedge f < 2.5$ is unsatisfiable | | optimum $2.5$ |

The case where both $x \ge 2$ and $y \ge 2.5$ hold has the local optimum $6.5$, and the bound $f < 4$ removes it without a simplex call.

With two objectives, minimizing $x$ and $y$:

- lexicographic, $y$ first and then $2x + y$, gives $y = 0$ and then $(2, 0)$ with $f = 4$;
- the Pareto front consists of the two points $(0, 2.5)$ and $(2, 0)$.

## Known algorithms

| method | idea | notes |
|---|---|---|
| linear search with local optimization (Sebastiani and Tomasi 2012) | find a model; run simplex on $f$ under the current literals; add $f < c$; repeat | each step at least reaches the optimum of one Boolean case |
| binary search on the value of $f$ | ask for $f \le c$ for a middle value $c$ between bounds | needs a finite bound; mixed with linear search in practice ([binary search on the answer](/binary-search-on-answer/)) |
| inline search in CDCL(T) (Sebastiani and Tomasi 2015; Nieuwenhuis and Oliveras 2006) | keep the bound $f < c$ as a theory constraint inside one search, and make it stronger at each model | no restarts of the solver; conflicts with the bound drive learning |
| SYMBA (Li et al. 2014) | treat several linear objectives together, and find unbounded directions from the models | for many objectives at once |
| bit-wise search for bit-vectors | decide the bits of $f$ from the top, one [incremental](/incremental-solving/) call per bit | $w$ calls for width $w$ |
| νZ (Bjørner et al. 2015) | MaxSMT engines, simplex for arithmetic objectives, and lexicographic, Pareto and box combinations | the optimization layer of Z3 |
| Pareto enumeration | after each Pareto optimal model, block the region it dominates | finds the whole front when it is finite |

## Bounds

**Theorem (termination of the linear search over LRA).** Let $\varphi$ be a QF_LRA formula with atoms $a_1, \ldots, a_n$ and a linear objective $f$. Suppose that at each step the search finds a model $M$ of $\varphi \wedge f < c$ (with $c = +\infty$ at first), takes the set $\mu$ of atom literals true in $M$, and replaces $M$ by an optimal point of $f$ over the polyhedron of $\mu$; if $f$ is unbounded below there, it stops with "unbounded". Then the search stops after at most $2^n + 1$ steps, and the last value of $c$ is the optimum.

*Proof.* Each step $k$ gives a set of literals $\mu_k$ and a value $c_k = \min \{ f(p) : p \models \mu_k \}$. The model found at step $k + 1$ satisfies $f < c_k$, so $\mu_{k+1} \ne \mu_j$ for all $j \le k$: each point of the polyhedron of $\mu_j$ has $f \ge c_j \ge c_k$. So the sets $\mu_k$ are pairwise distinct, and there are at most $2^n$ of them. When $\varphi \wedge f < c$ is unsatisfiable, no model has a value below $c$, and the last local optimum has the value $c$, so it is optimal. Each model of $\varphi$ satisfies some $\mu$ that makes $\varphi$ true, so the infimum over $\varphi$ is the least of the local infima. $\square$

If $\mu$ contains strict inequalities, the local infimum may not be attained. Solvers then compute it on the closure and use $f < c$ or $f \le c$ to keep the answer exact.

**Complexity.**

- *OMT over LRA.* The decision version, "is there a model with $f \le c$?", is NP-complete, since QF_LRA is NP-complete and the bound is one more atom. If the optimum is attained, it is attained at a vertex of the polyhedron of some $\mu$, so it is a rational of polynomial size.
- *OMT over LIA.* The decision version is NP-complete. If the optimum of an integer program is finite, it is attained at a solution of polynomial bit size (Papadimitriou 1981), so the optimum has polynomial size and binary search finds it with polynomially many NP calls.
- *Over nonlinear integer arithmetic,* satisfiability alone is undecidable ([Hilbert's tenth problem](/hilberts-tenth-problem/)), so OMT is undecidable too.

## Reductions

- **To SMT with a bound.** The optimum is found by a sequence of SMT calls with $f < c$ or $f \le c$.
- **From MaxSMT.** Use the objective $\sum_i w_i \cdot \mathrm{ite}(S_i, 0, 1)$.
- **From linear and mixed integer programming.** A conjunction of linear constraints with $f$ is an LP or a MIP.
- **Disjunctive programming to OMT.** Disjunctive constraints, which integer programming models with big-M constants, are written directly.

## Applications

- Scheduling and planning with resources, where the constraints mix Boolean choices and timing.
- Worst-case execution time: maximize the execution time of a path in a program, encoded as a formula.
- Static analysis: compute the best bounds of a variable for an abstract domain, by optimizing $x$ and $-x$ at a program point (SYMBA).
- Test generation and verification of neural networks and controllers with linear pieces.
- Configuration and layout problems with preferences.

## References
