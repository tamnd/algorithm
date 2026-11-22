---
tag: J93TRS
kind: algorithm
slug: reluplex
name: Reluplex
aliases:
- simplex with ReLU splitting
area: security-and-privacy/adversarial-machine-learning
level: research
summary: Extends the simplex method with lazy case splits on ReLU constraints to verify properties of ReLU networks exactly.
model: real-ram
complexity:
  vars: {R: the number of ReLU units, m: the number of rows of the tableau, n: the number of variables, s: the cost of one run of the simplex procedure}
  time: {worst: "O(2^R s)"}
  space: {extra: "O(R m n)"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 2017
  people: [Guy Katz, Clark Barrett, David L. Dill, Kyle Julian, Mykel J. Kochenderfer]
  note: Katz, Barrett, Dill, Julian and Kochenderfer presented Reluplex at CAV 2017 and used it to verify properties of the ACAS Xu collision avoidance networks. The same paper shows that the verification problem for ReLU networks is NP-complete.
prereqs: [simplex-for-smt, relu, smt-problem]
see_also: [neural-network-verification-problem, interval-bound-propagation, linear-bound-propagation, simplex-for-smt, smt-problem, mixed-integer-programming, dpll, randomized-smoothing]
sources:
  - url: https://arxiv.org/abs/1702.01135
    title: Guy Katz, Clark Barrett, David L. Dill, Kyle Julian and Mykel J. Kochenderfer, Reluplex, an efficient SMT solver for verifying deep neural networks, CAV 2017, LNCS 10426, pages 97 to 117 (the arXiv version is the extended version)
    locator: the derivation rules of Reluplex (the simplex rules, the ReLU repair rules and the case split), the proof that the procedure is sound and complete, the NP-completeness proof, and the ACAS Xu case study
  - paper: "Bruno Dutertre and Leonardo de Moura, A fast linear-arithmetic solver for DPLL(T), CAV 2006, LNCS 4144"
    locator: the general simplex with bounds that Reluplex extends, and its termination with Bland's rule
  - url: https://arxiv.org/abs/1902.06705
    title: Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry and Alexey Kurakin, On evaluating adversarial robustness, arXiv 2019
    locator: verified robustness as a lower bound on robust accuracy
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts used on this page
---

Reluplex decides exactly whether a ReLU network has an input in a given region whose output satisfies a given linear condition. It writes the network as a set of linear equations over real variables, with bounds on the variables and one pair of variables $(b, f)$ for each ReLU, tied by the constraint $f = \max(0, b)$. It then runs the [simplex procedure for SMT](/simplex-for-smt/) on the linear part and treats the ReLU pairs lazily: a broken pair is first repaired by changing one of its two variables, and only a pair that keeps breaking is split into its two linear phases, $b \le 0, f = 0$ and $b \ge 0, f = b$. The answer is SAT with a concrete input, which is a counterexample, or UNSAT, which is a proof. Katz et al. (2017) built it to verify networks of an aircraft collision avoidance system, and their paper also shows that the problem is NP-complete, so the worst case is exponential.

**Threat model.** Reluplex is a defense, a verifier, so the threat model is the one that the proof covers. For robustness the goal can be untargeted or targeted, as one query is asked for each other label. The knowledge is unlimited: the proof holds against a white-box attacker. The capability is any change at test time within the region of the query, for example $B_\infty(x, \epsilon) \cap [0,1]^d$.

## In plain words

A ReLU network is a chain of weighted sums and of units that turn negative numbers into zero. Without those units, the question "can some allowed input push the wrong class above the right one?" is a set of linear inequalities, and the simplex method answers it.

Each unit is a fork with two linear roads: off (input negative, output zero) or on (output equals input). Trying all roads of all units is too slow. Reluplex first solves the linear part while it ignores the forks, then fixes the units that disagree one at a time. Only when a unit keeps going wrong does it try both roads, one after the other.

If some road gives a solution, that solution is a real input that breaks the property. If every road fails, no such input exists.

## The problem

A query has real variables $x_1, \dots, x_n$, a set of linear equations, a lower bound $l_j$ and an upper bound $u_j$ for each variable (each may be absent), and a set $R$ of pairs $(b, f)$ with $f = \max(0, b)$. The question is whether some assignment meets all of them.

A network property becomes a query as follows. One variable is the constant 1, the inputs get the bounds of the region, each hidden unit gets a variable $b$ for its weighted sum (one equation) and a variable $f$ with $f \ge 0$ for its output, and one more variable is the linear output condition, such as $z_j - z_y$, with the bound $\ge 0$. The network is robust at $x$ for label $y$ when the query is UNSAT for every $j \ne y$. This is the [neural network verification problem](/neural-network-verification-problem/) for ReLU networks.

## The algorithm

The procedure keeps a tableau, in which each basic variable is a linear combination of the non-basic variables, and an assignment $\beta$ that meets every equation at all times. It changes $\beta$ with the operations of [simplex for SMT](/simplex-for-smt/): UPDATE sets a non-basic variable and changes the basic variables to match, and PIVOT-AND-UPDATE moves a basic variable to a value through a non-basic variable of its row and then swaps the two.

```pseudo id=main
RELUPLEX(T, l, u, β, R, τ)                     ▷ tableau T, bounds l and u, pairs R
L1  repairs[p] ← 0 for every pair p in R
L2  loop
L3      if a non-basic x_j is out of its bounds then
L4          UPDATE(x_j, the nearest bound)
L5      else if a basic x_i is out of its bounds then ▷ the least such i
L6          x_j ← the least non-basic of the row of x_i that can move x_i toward its bound
L7          if there is no such x_j then return UNSAT
L8          PIVOT-AND-UPDATE(x_i, x_j, the violated bound)
L9      else if some pair p = (b, f) in R has β(f) != max(0, β(b)) then
L10         if repairs[p] >= τ then return SPLIT(T, l, u, β, R, τ, p)
L11         repairs[p] ← repairs[p] + 1
L12         if f and b are both basic then pivot f with a non-basic, non-fixed variable of its row
L13         if f is non-basic then UPDATE(f, max(0, β(b))) else UPDATE(b, β(f))
L14     else return SAT, β
SPLIT(T, l, u, β, R, τ, p = (b, f))
L15 result ← RELUPLEX with u(b) ← min(u(b), 0), l(f) ← u(f) ← 0, and R - {p}
L16 if result is SAT then return result
L17 return RELUPLEX with l(b) ← max(l(b), 0), a new row e = f - b with l(e) = u(e) = 0, and R - {p}
```

Lines L3 to L8 are the simplex procedure with Bland's rule: the least index is chosen both for the variable to fix (line L5) and for the variable to pivot with (line L6). A basic variable that cannot move is a proof that the linear part has no solution (line L7). Lines L9 to L13 repair one broken ReLU pair by moving $f$ to $\max(0, b)$ or $b$ to $f$, after a pivot if both are basic (line L12). A repair can break a bound, so the loop goes back to the simplex steps. Line L10 stops the repairs of a pair after $\tau$ tries and splits it: line L15 tries the inactive phase and line L17 the active phase, each a purely linear constraint. The returned $\beta$ restricted to the inputs is the counterexample.

## Example

Take the network of the [interval bound propagation](/interval-bound-propagation/) page: $h = \mathrm{relu}(W_1 x + b_1)$ with $b^{(1)} = 2x_1 - x_2$ and $b^{(2)} = x_1 - 2x_2 + 0.5$, and the logits $z_0 = h_1 - h_2 + 1$, $z_1 = -2h_1 + 2h_2$. At $x = (0.5, 0.5)$ the label is $0$. To verify robustness on $[0.25, 0.75]^2$, Reluplex asks for an input with $z_1 - z_0 = -3 f_1 + 3 f_2 - 1 \ge 0$, with the pairs $f_1 = \max(0, b^{(1)})$ and $f_2 = \max(0, b^{(2)})$.

The first simplex steps (lines L5 to L8) raise $f_2$ to $1/3$ to meet the output bound, which breaks the second pair, since $b^{(2)} = 0.25$ at the start point. The repairs of lines L11 to L13 and the simplex steps then undo each other, and after $\tau = 5$ repairs line L10 splits the first pair, and later the second one. The search ends in four leaves, each a linear program:

| leaf | phase of unit 1 | phase of unit 2 | output $z_1 - z_0$ on the leaf | reason for UNSAT (line L7) |
|---|---|---|---|---|
| 1 | off, $2x_1 \le x_2$ | off | $-1$ | the output row is fixed at $-1 < 0$ |
| 2 | off, $2x_1 \le x_2$ | on | $3 b^{(2)} - 1$ | $b^{(2)} \le 0.5 - 3x_1 < 0$, so $b^{(2)} \ge 0$ fails |
| 3 | on | off | $-3 b^{(1)} - 1$ | $b^{(1)} \ge 0$ gives an output $\le -1$ |
| 4 | on | on | $0.5 - 3(x_1 + x_2)$ | $x_1 + x_2 \ge 0.5$ gives an output $\le -1$ |

Every leaf is UNSAT, so the answer is UNSAT: no input of the box changes the label. Interval bounds fail on this box, and linear bounds succeed with the lower bound $0.25$ on $z_0 - z_1$; the true minimum is $1$, which leaf 4 reaches at $x = (0.25, 0.25)$. On the larger box $[1/12, 11/12]^2$, for $\epsilon = 5/12$, the first simplex steps already end at line L14 with SAT and the input $x = (1/12, 1/12)$, where both logits are $2/3$. So $5/12$ is the exact robust radius of this point.

## Correctness

**Theorem (sound and complete).** For $\tau \ge 1$, RELUPLEX terminates. If it returns SAT, $\beta$ meets every equation, every bound and every pair of the query. If it returns UNSAT, the query has no solution.

The key facts are as follows. Every operation keeps the equations true, so at line L14 the assignment meets equations, bounds and pairs. Line L7 is reached only when every non-basic variable is within its bounds (line L3) and each one that could help $x_i$ is at its limit; then the row gives a bound on $x_i$ that every solution must meet, and it is violated. Every solution of the query satisfies one of the two phases of a pair, and each phase is exactly what line L15 or line L17 adds, so UNSAT in both branches is UNSAT for the query. For termination, each simplex phase ends by Bland's rule, as in [simplex for SMT](/simplex-for-smt/), each pair is repaired at most $\tau$ times before a split, and each split removes one pair. The full proof is in `proofs/correctness.md`.

## Complexity

- **Time.** The problem is NP-complete (Katz et al. 2017), so no polynomial method is expected. The split tree of lines L15 to L17 has at most $2^R$ leaves, each a run of the simplex procedure, and the simplex procedure with Bland's rule can itself take exponentially many pivots in the worst case, though it is fast in practice. Lazy splitting means that the tree is often much smaller than $2^R$: a pair that the repairs can fix is never split.
- **Space.** Each level of the recursion keeps a copy of the tableau, of size $O(m n)$ in a dense form, and the depth is at most $R$, so $O(R m n)$.
- **Pivot cost.** One pivot costs $O(m n)$ with a dense tableau.

## Properties

- **Exact (complete and sound).** SAT comes with a real counterexample and UNSAT is a proof, both in exact arithmetic (a theorem).
- **Exponential worst case.** The verification problem is NP-complete, so a large network can take a very long time. Exact verifiers reach much smaller networks than the incomplete bounds of [linear bound propagation](/linear-bound-propagation/) do.
- **Exact robust accuracy.** On the points it finishes, it gives the true answer, so it closes the gap between an attack (an upper bound on robust accuracy) and an incomplete certificate (a lower bound).
- **Lazy splits.** A pair is split only after $\tau$ failed repairs. A stable unit, whose bounds already fix its phase, is never split.

## Variants and improvements

- **Bound tightening.** Katz et al. derive tighter bounds of $b$ and $f$ from the rows of the tableau during the search. A pair whose bounds fix its phase becomes a linear constraint without a split. Interval bounds, as in [interval bound propagation](/interval-bound-propagation/), give a cheap start.
- **Conflict analysis.** When a branch is UNSAT, the solver can find which splits caused it and skip other branches with the same cause, as in [CDCL](/cdcl/) SAT solvers.
- **Marabou.** The successor tool of the same group (Katz et al. 2019) adds more activation functions, splitting heuristics, parallel search and other improvements.
- **Mixed integer programming.** The same problem can be written as a [mixed integer program](/mixed-integer-programming/) with one binary variable per unstable ReLU, and solved with a general MIP solver.
- **Branch and bound with linear bounds.** Modern complete verifiers split ReLU phases in a search tree and prune each node with [linear bound propagation](/linear-bound-propagation/) instead of a full simplex run.

## When to use it

Use Reluplex, or one of its successors, when an exact answer is needed for a small network: a safety property of a controller, a proof that a fixed point is robust, or a ground truth for testing an incomplete verifier. For large networks, use an incomplete bound such as [linear bound propagation](/linear-bound-propagation/) or a probabilistic certificate such as [randomized smoothing](/randomized-smoothing/), and accept that some points stay unknown.

## Pitfalls

- **Pivoting with the constant.** If line L12 pivots $f$ with a fixed variable, such as the variable that holds the constant 1, the following UPDATE moves a fixed variable off its value. The result is still correct, because the simplex steps move it back, but the repairs make no progress. Pivot only with a variable whose bounds are not equal.
- **A split that forgets $f \ge 0$.** Line L15 must fix $f$ to $0$, not only bound it above by $0$. If $f$ has no lower bound, a branch with $f < 0$ and $b \le 0$ meets the new bounds but breaks $f = \max(0, b)$.
- **Floating point.** The theorem holds in exact arithmetic. A solver on floats can report UNSAT wrongly after rounding; the tests of this page use exact rational numbers, and real tools check SAT answers by a forward pass.
- **No bound on the repairs.** Without line L10 the repairs and the simplex steps can undo each other forever, as in the example at $\epsilon = 0.25$.
- **A strict condition.** A property $z_j - z_y > 0$ needs a strict bound. The page asks for $z_j - z_y \ge 0$ instead, so a tie, as at $\epsilon = 5/12$, counts as a counterexample. This matches a certificate that asks for a strictly positive margin.

## Implementations

The code of this page is an abstract model on synthetic data. The verifier runs only on small ReLU networks that the tests build from a fixed seed, with weights from `mlkit.tiny_relu_net` or a seeded generator rounded to multiples of $1/8$, and it works in exact rational arithmetic (`fractions.Fraction`). It never reads real data or touches a real system. The tests check the example (UNSAT at $\epsilon = 1/4$ and the radius $5/12$), small linear programs, a single ReLU pair, and SAT or UNSAT on 500 random queries against the exact maximum from an enumeration of all activation patterns. They also check that each SAT answer is a true counterexample and meets every equation and pair.

## History

Verification of neural networks with SMT solvers was tried before 2017, with general solvers that split every ReLU in advance, and it scaled to very small networks only. Katz, Barrett, Dill, Julian and Kochenderfer presented Reluplex at CAV 2017. They extended the simplex procedure of Dutertre and de Moura (2006), which SMT solvers use for linear real arithmetic, with rules for ReLU pairs, and they verified properties of the deep networks that were proposed for the ACAS Xu airborne collision avoidance system, which were out of reach for earlier tools. The same paper proved that the verification problem for ReLU networks is NP-complete. The group later released Marabou (2019), and the idea of lazy case splits with linear bounds lives on in the branch-and-bound verifiers of today.

## References
