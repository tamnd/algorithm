---
tag: 34RZ0J
kind: algorithm
slug: interval-constraint-propagation
name: Interval constraint propagation
aliases:
- ICP
- interval narrowing
- HC4
- HC4Revise
- hull consistency propagation
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Narrows the interval domains of real variables by revising one constraint at a time with interval arithmetic. HC4 revises a constraint by a forward and a backward pass over its tree.
solves: [numeric-constraint-satisfaction]
model: floating-point-model
complexity:
  vars: {n: the number of variables, e: the total number of nodes in all constraint trees, k: the largest number of times one domain can shrink by the factor 1 - ρ}
  time: {worst: O(n k e)}
  space: {extra: O(n + e)}
properties: {deterministic: true, exact: false, online: false, recursive: false, in_place: false}
history:
  year: 1987
  people: [John G. Cleary, Ernest Davis, Frédéric Benhamou, Frédéric Goualard, Laurent Granvilliers, Jean-François Puget]
  note: Cleary (1987) and Davis (1987) introduced propagation over interval domains. Benhamou, Goualard, Granvilliers and Puget gave the HC4 algorithm in 1999.
prereqs: [interval-arithmetic, constraint-propagation, ac-3]
see_also: [numeric-constraint-satisfaction, bounds-consistency, interval-branch-and-bound, interval-newton-method, bisection-method, nonlinear-real-arithmetic-satisfiability, delta-satisfiability, global-optimization]
sources:
  - paper: "Frédéric Benhamou, Frédéric Goualard, Laurent Granvilliers and Jean-François Puget, Revising hull and box consistency, Proceedings of the International Conference on Logic Programming (ICLP 1999), MIT Press, 1999, pages 230 to 244"
    locator: the HC4 algorithm, the HC4Revise forward and backward pass, and the result that HC4Revise enforces hull consistency on a constraint in which each variable occurs once
  - paper: "John G. Cleary, Logical arithmetic, Future Computing Systems 2(2), 1987, pages 125 to 149"
    locator: relational interval arithmetic, the first interval narrowing of constraints in logic programming
  - paper: doi:10.1016/0004-3702(87)90091-9
    title: Ernest Davis, Constraint propagation with interval labels, Artificial Intelligence 32(3), 1987
    locator: pages 281 to 331 (propagation of interval labels, termination and the limits of local propagation)
  - paper: "Olivier Lhomme, Consistency techniques for numeric CSPs, Proceedings of IJCAI-93, 1993, pages 232 to 238"
    locator: 2B consistency (hull consistency) and 3B consistency for numeric CSPs, and the stopping rule on the size of a reduction
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 16, Continuous and interval constraints, by Frédéric Benhamou and Laurent Granvilliers (hull and box consistency, HC4, branch and prune)
  - book: isbn:9780898716696
    title: Ramon E. Moore, R. Baker Kearfott and Michael J. Cloud, Introduction to Interval Analysis, SIAM, 2009
    locator: Chapters 2 to 5 (interval arithmetic with outward rounding, the inclusion property, the dependency problem)
---

Interval constraint propagation (ICP) works on constraints over real variables, such as $y = x^2$ and $x + y = 2$. Each variable has an interval as its domain, and the box is the product of these intervals. ICP takes one constraint at a time and removes from the box the parts that cannot hold a solution of that constraint alone. It repeats this until no domain shrinks by more than a set fraction. HC4 (Benhamou, Goualard, Granvilliers and Puget, 1999) does one such step, called a *revise*, with two passes over the expression tree of the constraint. A forward pass computes an interval for each subexpression. A backward pass projects the allowed range back down to the variables. With outward rounding, ICP never removes a real solution. But it is a local method, and the box it returns can be much larger than the smallest box around the solutions. ICP is the propagation part of the solvers for [numeric constraint satisfaction problems](/numeric-constraint-satisfaction/).

## In plain words

Each unknown is known only to lie between two numbers. Take one rule, such as $x + y = 2$. If $y$ is between 0 and 10, then $x = 2 - y$ is between $-8$ and 2, so any part of the range of $x$ above 2 can go. Do the same for each unknown in the rule, then for the next rule, and keep going while the ranges still get noticeably smaller.

For a long formula, first work upward from the unknowns and compute a range for each part of the formula. Then cut the range of the whole formula down to what the rule allows, and work back down, cutting the range of each part. The computer rounds lower ends down and upper ends up, so a true solution is never cut away. The ranges that are left can still hold much that is not a solution.

## The problem

The input is a box $B = I_1 \times \cdots \times I_n$ of closed intervals, one for each real variable $x_1, \ldots, x_n$, and a set of constraints $c$ of the form $\ell_c \le f_c(x) \le u_c$. Each $f_c$ is an expression built from the variables and constants with $+$, $-$, $\times$ and squaring. The bounds $\ell_c$ and $u_c$ can be $-\infty$ or $+\infty$, and $\ell_c = u_c$ gives an equation. A *solution* is a point of $B$ that meets every constraint.

The output is a box $B' \subseteq B$ that contains every solution in $B$, or "empty" when ICP proves that $B$ has no solution. This is a [numeric CSP](/numeric-constraint-satisfaction/), and ICP does not solve it alone: it only narrows the box. Solvers alternate ICP with splitting of the box.

Notation: $n$ variables, $m$ constraints, $e$ the total number of nodes in the trees of all $f_c$, and $\rho \in (0, 1)$ the stopping ratio.

## The algorithm

The nodes of the tree of $f_c$ are listed in post-order, so that each child comes before its parent and the root is last. $J_k$ is the interval of node $k$. For a node $z = a \circ b$, the *projection* onto a child is the interval form of solving for that child: for $z = a + b$, $a \in z - b$ and $b \in z - a$; for $z = a - b$, $a \in z + b$ and $b \in a - z$; for $z = a \times b$, $a \in z / b$ when $0 \notin b$; for $z = a^2$, $a \in \pm\sqrt{z \cap [0, \infty)}$.

```pseudo id=main
HC4-REVISE(c, B)
L1  for each node k of f_c in post-order: J_k ← the interval value of k on B (variable: its domain; constant: itself; operation: interval operation on the children)
L2  J_root ← J_root ∩ [ℓ_c, u_c]
L3  if J_root = ∅ then return ∅
L4  for each node k in reverse post-order (root first):
L5      for each child a of k: J_a ← J_a ∩ (projection of J_k onto a)
L6      if some J_a = ∅ then return ∅
L7      if k is a leaf for the variable x then B(x) ← B(x) ∩ J_k
    return B

ICP(B, C, ρ)
L8  B ← the input box
L9  Q ← all constraints of C
L10 while Q ≠ ∅ do
L11     c ← remove the first constraint of Q
L12     B' ← HC4-REVISE(c, B)
L13     if B' = ∅ then return ∅
L14     for each variable x of c whose width shrank by more than the fraction ρ: add each constraint on x that is not in Q to Q
L15     B ← B'
L16 return B
```

Every interval operation rounds its lower end toward $-\infty$ and its upper end toward $+\infty$. The implementation uses round-to-nearest floating point and then moves each inexact result one floating-point number outward, which gives the same guarantee.

Line L14 also adds $c$ itself when one of its variables shrank, because HC4-REVISE is not idempotent when a variable occurs more than once in $f_c$. The stopping ratio $\rho$ is Lhomme's rule (1993): it stops the slow, near-endless narrowing that can occur on real domains, where a sequence of revisions can shrink a domain by smaller and smaller amounts.

## Example

Take $x, y \in [0, 10]$ with $c_1 : y - x^2 = 0$ and $c_2 : x + y = 2$. The only solution is $(1, 1)$. (The point $(-2, 4)$ also meets both equations, but it is outside the box.)

**One revise of $c_1$.** The tree has the nodes $x$, $x^2$, $y$ and $y - x^2$.

| pass | node | interval |
|---|---|---|
| forward | $x$ | $[0, 10]$ |
| forward | $x^2$ | $[0, 100]$ |
| forward | $y$ | $[0, 10]$ |
| forward | $y - x^2$ | $[-100, 10]$ |
| L2 | root, $\cap [0, 0]$ | $[0, 0]$ |
| backward | $y \in 0 + x^2$ | $[0, 10] \cap [0, 100] = [0, 10]$ |
| backward | $x^2 \in y - 0$ | $[0, 100] \cap [0, 10] = [0, 10]$ |
| backward | $x \in \pm\sqrt{[0, 10]}$ | $[0, 10] \cap [-3.1623, 3.1623] = [0, 3.1623]$ |

**Alternating revisions.** Revising $c_1$ and $c_2$ in turn gives, to four digits:

| revise | constraint | $x$ | $y$ |
|---|---|---|---|
| 1 | $c_1$ | $[0, 3.1623]$ | $[0, 10]$ |
| 2 | $c_2$ | $[0, 2]$ | $[0, 2]$ |
| 3 | $c_1$ | $[0, 1.4142]$ | $[0, 2]$ |
| 4 | $c_2$ | $[0, 1.4142]$ | $[0.5858, 2]$ |
| 5 | $c_1$ | $[0.7654, 1.4142]$ | $[0.5858, 2]$ |
| 6 | $c_2$ | $[0.7654, 1.4142]$ | $[0.5858, 1.2346]$ |
| 7 | $c_1$ | $[0.7654, 1.1111]$ | $[0.5858, 1.2346]$ |
| 8 | $c_2$ | $[0.7654, 1.1111]$ | $[0.8889, 1.2346]$ |

The boxes close in on $(1, 1)$, but each pair of revisions removes only a part of the rest. With $\rho = 10^{-3}$ the implementation stops after 116 revisions with both domains of width less than $2 \times 10^{-15}$, and both contain 1.

**Far from the hull.** Take $x, y \in [-2, 2]$ with $x^2 + y^2 = 1$ and $x - y = 0$. The solutions are $\pm(1/\sqrt 2, 1/\sqrt 2)$, and the smallest box around them is about $[-0.7071, 0.7071]^2$. ICP stops at $[-1, 1]^2$. On that box, each constraint alone has a solution for every value at each end of each domain, so no single revise can remove anything. The linear pair $x + y = 0$, $x - y = 0$ on $[-1, 1]^2$ is worse: its only solution is $(0, 0)$, and ICP removes nothing.

## Correctness

**Soundness.** Every solution in the input box is in the output box, and an "empty" answer means that the input box has no solution. The proof is by an invariant: during HC4-REVISE, for every solution $p$ in $B$ and every node $k$, the value of node $k$ at $p$ lies in $J_k$. The forward pass keeps it by the inclusion property of interval arithmetic, which outward rounding preserves in floating point. Line L2 keeps it because $f_c(p) \in [\ell_c, u_c]$. Each projection at line L5 keeps it, because it is an interval form of solving the node equation for one child. Line L7 then keeps $p$ in $B$. So HC4-REVISE removes no solution, and induction over the revisions of ICP gives the claim.

**Termination.** Line L14 adds a constraint to $Q$ only after some domain becomes unbounded-to-bounded or loses more than the fraction $\rho$ of its width. A domain of floating-point numbers can do this only finitely many times, so ICP stops.

**What the output means.** The output is a box that HC4 cannot narrow by more than $\rho$, not the hull of the solutions. When each variable occurs at most once in $f_c$ and the arithmetic is exact, HC4-REVISE makes the box hull consistent for $c$: each end of each domain is the end of the projection of the solutions of $c$ alone (Benhamou and colleagues, 1999). It is still local: it considers one constraint at a time. The full proof is in the proof file.

## Complexity

- **One revise.** HC4-REVISE does a constant number of interval operations for each node of $f_c$, so it costs $O(|f_c|)$.
- **The loop.** The first pass revises each constraint once, for $O(e)$. After that, each revision is caused by a shrinking of a variable $x$, and each shrinking adds the constraints on $x$, whose total size is at most $e$. A domain can shrink at most $k$ times, where $k \le 1 + \ln(w_0 / w_{\min}) / \rho$ for the first finite width $w_0$ and the smallest nonzero floating-point width $w_{\min}$. So the total is $O(e + n k e) = O(n k e)$ interval operations.
- **Space.** $O(e)$ for the node intervals and $O(n + m)$ for the box and the queue.

The bound $k$ is large for small $\rho$. In practice the number of revisions depends on the problem, as in the example, where 116 revisions reach the floating-point limit.

## Properties

- **Sound.** No real solution is lost, with outward rounding.
- **Incomplete as a solver.** A nonempty output box does not prove that a solution exists, and the box can be much larger than the hull of the solutions.
- **Deterministic.** The result depends on the order of the queue, but not on any random choice. Different orders can give different boxes, since the method stops at a ratio, not at an exact fixed point.
- **Dependency.** When a variable occurs more than once in a constraint, interval evaluation treats the occurrences as independent, and the narrowing is weaker. For example, $x - x$ on $[-1, 1]$ evaluates to $[-2, 2]$.

## Variants and improvements

- **Hull consistency, 2B consistency.** The local property that HC4 aims at. Lhomme (1993) called it 2B consistency. It is the continuous form of [bounds consistency](/bounds-consistency/).
- **Box consistency and BC3, BC4.** Box consistency treats each occurrence of a variable together, with a one-variable [interval Newton](/interval-newton-method/) search on each end of the domain (Benhamou, McAllester and Van Hentenryck, 1994). It is stronger for constraints with many occurrences of a variable and costs more. BC4 (Benhamou and colleagues, 1999) uses HC4 for variables that occur once and box narrowing for the rest.
- **3B consistency.** Try to shrink each end of each domain by a small slice, and remove the slice if ICP on it gives "empty" (Lhomme, 1993). This is the interval form of [singleton arc consistency](/singleton-arc-consistency/).
- **Branch and prune.** Alternate ICP with [bisection](/bisection-method/) of the widest domain until the boxes are small. With [interval Newton](/interval-newton-method/) steps on small boxes, a solver can also prove that a box holds a unique solution. For optimization this is [interval branch and bound](/interval-branch-and-bound/).
- **In SMT.** ICP is the core of $\delta$-complete solvers for [nonlinear real arithmetic](/nonlinear-real-arithmetic-satisfiability/). See [delta-satisfiability](/delta-satisfiability/).

## When to use it

Use ICP to narrow the domains of real variables before and during search, in global optimization, in verified solving of nonlinear systems, and in SMT for nonlinear real arithmetic. It is cheap for each revise and needs no derivatives. It is weak alone on systems that are coupled through many constraints, such as linear systems, where a linear relaxation or Gaussian elimination works better, and it gives no proof that a solution exists without an extra test such as interval Newton.

## Pitfalls

- **Rounding to nearest.** Without outward rounding, a revise can cut away a true solution by one unit in the last place, and a solver can then answer "no solution" for a problem that has one.
- **No stopping ratio.** Waiting for an exact fixed point can take a very long time on real domains, as in the example, where each revise removes only part of the rest.
- **Reading the box as the answer.** The output box can be far from the hull of the solutions, and it can hold no solution at all.
- **Division by an interval that holds 0.** The projection $a \in z / b$ needs care when $0 \in b$. The safe choice, used here, is to skip it. Extended division gives a union of two intervals and can narrow more.
- **Many occurrences of a variable.** Rewrite constraints to reduce the occurrences of each variable, or use box consistency, since HC4 is weak there.

## Implementations

## History

Cleary (1987) proposed relational interval arithmetic for logic programming, and Davis (1987) studied propagation of interval labels and its limits. BNR Prolog and later CLP(BNR) built on Cleary's work. Hyvönen (1992) studied tolerance propagation. Lhomme (1993) defined 2B and 3B consistency for numeric CSPs. Benhamou, McAllester and Van Hentenryck (1994) introduced box consistency, used in the Numerica system. Benhamou, Goualard, Granvilliers and Puget (1999) gave HC4 and BC4, which are the standard propagators in solvers such as RealPaver and Ibex.

## References
