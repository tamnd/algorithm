---
tag: Q0TDK8
kind: technique
slug: cutting-plane-method-integer-programming
name: Cutting-plane method
aliases:
- cutting planes
- cutting plane algorithm
- cutting-plane method for integer programming
area: optimization/integer-programming
level: core
summary: Repeatedly add valid inequalities that cut off the current fractional LP optimum.
prereqs: [lp-relaxation, integer-hull, simplex-method, dual-simplex-method]
see_also: [gomory-cutting-plane-algorithm, chvatal-gomory-cut, branch-and-cut, separation-oracle, gomory-mixed-integer-cut, cover-inequality, chvatal-gomory-finite-convergence, traveling-salesman-problem]
sources:
  - paper: "George B. Dantzig, D. Ray Fulkerson and Selmer M. Johnson, Solution of a large-scale traveling-salesman problem, Journal of the Operations Research Society of America 2 (1954), 393 to 410"
    locator: the first cutting plane computation, with subtour elimination constraints added as needed
  - paper: doi:10.1090/S0002-9904-1958-10224-4
    title: Ralph E. Gomory, Outline of an algorithm for integer solutions to linear programs, Bulletin of the American Mathematical Society 64(5), 1958
    locator: the first general cutting plane algorithm with a finiteness proof
  - paper: "Martin Grötschel, László Lovász and Alexander Schrijver, The ellipsoid method and its consequences in combinatorial optimization, Combinatorica 1 (1981), 169 to 197"
    locator: the equivalence of separation and optimization
  - paper: "Manfred Padberg and Giovanni Rinaldi, A branch-and-cut algorithm for the resolution of large-scale symmetric traveling salesman problems, SIAM Review 33 (1991), 60 to 100"
    locator: cut pools, cut management and the name branch and cut
  - paper: "James E. Kelley, The cutting-plane method for solving convex programs, Journal of the Society for Industrial and Applied Mathematics 8 (1960), 703 to 712"
    locator: the cutting plane method for convex programs
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 8 (cutting plane algorithms)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 5 (valid inequalities and the cutting plane method) and Chapter 7 (separation and optimization)
---

The cutting-plane method solves an integer program by solving a sequence of linear programs. It starts from the [LP relaxation](/lp-relaxation/). Each time the LP optimum is fractional, it finds a valid inequality, a *cut*, that every integer feasible point satisfies but the LP optimum does not, adds it, and solves again. The LP bound gets better with every cut, and if the LP optimum becomes integral, it is optimal for the integer program. Dantzig, Fulkerson and Johnson (1954) used the idea to solve a 49-city [traveling salesman problem](/traveling-salesman-problem/), and Gomory (1958) gave the first general algorithm that ends after finitely many cuts. Today the method runs inside [branch and cut](/branch-and-cut/), where cuts tighten the relaxation at each node of a branch and bound tree.

## In plain words

The LP relaxation lets the unknowns take fractional values, so its best answer is often a corner of the region that has fractions in it. A cut is a new straight-line rule that slices off that corner and keeps every whole-number answer.

After the cut, the solver finds the best corner of the smaller region. If it still has fractions, the solver finds another cut and repeats. The region shrinks toward the hull of the whole-number answers. When the best corner is a whole-number point, the solver can stop: no whole-number answer was removed, so none can be better.

## When it applies

- An integer or mixed-integer program $\max\{c^T x : Ax \le b,\ x \ge 0,\ x_j \in \mathbb{Z} \text{ for } j \in I\}$ with a solvable LP relaxation. The LP pages use $\min$ with $Ax = b$, and slack variables convert one form into the other.
- A *separation* routine: given a point $x^*$, it returns valid inequalities that $x^*$ breaks, or reports that it found none. The routine can be general, like [Chvátal-Gomory](/chvatal-gomory-cut/) or [GMI](/gomory-mixed-integer-cut/) cuts from the simplex tableau, or specific to the problem, like subtour or [cover](/cover-inequality/) inequalities.
- An LP solver that can add rows and restart from the last basis, usually the [dual simplex method](/dual-simplex-method/), since a cut makes the old basis primal infeasible but keeps it dual feasible.

## The template

```pseudo id=main
CUTTING-PLANE(A, b, c, I)                        ▷ max c x, A x ≤ b, x ≥ 0, x_j integer for j ∈ I
L1  Q ← { x ≥ 0 : A x ≤ b }
L2  loop
L3      solve max { c x : x ∈ Q }
L4      if Q is empty then return INFEASIBLE
L5      x* ← an optimal vertex
L6      if x*_j is integral for all j ∈ I then return x*      ▷ optimal
L7      C ← SEPARATE(x*)                                     ▷ valid cuts with α x* > β
L8      if C is empty then return x*, c x*                    ▷ upper bound only: branch
L9      Q ← Q ∩ { x : α x ≤ β for all (α, β) ∈ C }
L10     remove old cuts that have been slack for many rounds (optional)
```

**Why the answer is right.** Let $P_I$ be the [integer hull](/integer-hull/). Every cut is valid for the integer feasible points, so $P_I \subseteq Q$ holds at every step. Hence $c^T x^* \ge z^*$ for each LP optimum, so the LP value is an upper bound that never increases. If $x^*$ is integral on $I$, it is feasible for the integer program, and its value equals the bound, so it is optimal. If $Q$ becomes empty, $P_I$ is empty, so the program has no feasible point.

**When it ends.** With Gomory's cuts from the tableau and a lexicographic rule, the method ends after finitely many steps for pure integer programs with rational data, as shown on the [Gomory algorithm](/gomory-cutting-plane-algorithm/) page. The [finite convergence theorem](/chvatal-gomory-finite-convergence/) gives the reason: finitely many rounds of all Chvátal-Gomory cuts reach $P_I$. With other separators, or with mixed-integer variables, the loop may not end, and line L8 hands the current bound to branch and bound.

**Separation and optimization.** Grötschel, Lovász and Schrijver (1981) showed, with the [ellipsoid method](/ellipsoid-method/), that linear optimization over a polytope is polynomial if and only if separation over it is polynomial. So a family of cuts that describes $P_I$ and has a polynomial [separation oracle](/separation-oracle/) gives a polynomial algorithm, even if the family is exponentially large. Matching with the blossom inequalities is the classic case. If the integer program is NP-hard, no such family exists unless P = NP.

**Example.** Take $\max\ x_1 + x_2$ subject to $3x_1 + 2x_2 \le 6$, $-3x_1 + 2x_2 \le 0$, $x \in \mathbb{Z}^2_+$. The integer points are $(0,0)$, $(1,0)$, $(2,0)$ and $(1,1)$, so $z^* = 2$.

| Round | LP optimum | LP value | Cut added | Multipliers |
|---|---|---|---|---|
| 0 | $(1, \tfrac32)$ | $\tfrac52$ | $x_2 \le 1$ | $\tfrac14, \tfrac14$ on the two rows: $x_2 \le \lfloor \tfrac32 \rfloor$ |
| 1 | $(\tfrac43, 1)$ | $\tfrac73$ | $x_1 + x_2 \le 2$ | $\tfrac13$ on $3x_1 + 2x_2 \le 6$ and on $x_2 \le 1$: $x_1 + x_2 \le \lfloor \tfrac73 \rfloor$ |
| 2 | $(1, 1)$ or $(2, 0)$ | $2$ | none | the optimum is integral |

Both cuts are Chvátal-Gomory cuts. The first removes $(1, \tfrac32)$ and the second removes $(\tfrac43, 1)$. After two cuts, the optimal face of the LP is the segment from $(1,1)$ to $(2,0)$, and both of its vertices are integral.

## Classic examples

- **Traveling salesman.** Dantzig, Fulkerson and Johnson (1954) started with the degree constraints and added subtour elimination constraints and a few other cuts only when the LP solution broke them. Concorde follows the same plan with many more families and has solved instances with tens of thousands of cities.
- **Gomory's algorithm.** [Gomory's cutting plane algorithm](/gomory-cutting-plane-algorithm/) uses fractional cuts from the simplex tableau and ends after finitely many cuts for pure integer programs.
- **General 0-1 programs.** Crowder, Johnson and Padberg (1983) added lifted cover inequalities for each knapsack row and solved large 0-1 problems from industry.
- **Matching.** For [maximum matching](/maximum-matching/), the degree constraints together with the blossom inequalities describe the [matching polytope](/matching-polytope/). Padberg and Rao (1982) gave a polynomial separation routine for the blossom inequalities, so a cutting plane method with them solves weighted matching through linear programming.

## Variations

- **Branch and cut.** Cuts are added at the root and at nodes of the branch and bound tree. Cuts valid for the whole problem go into a cut pool and are reused at other nodes.
- **Rounds and cut selection.** Solvers separate many families in one round, then keep a subset of the cuts chosen by violation, by the angle with the objective and by how different they are from each other.
- **Kelley's method.** For convex programs $\max\{c^T x : g(x) \le 0\}$, Kelley (1960) cut off $x^*$ with the tangent plane $g(x^*) + \nabla g(x^*)^T (x - x^*) \le 0$. The same loop, with a different separation routine, underlies outer approximation for mixed-integer nonlinear programs and the [Benders decomposition](/benders-decomposition/).
- **Central cutting plane methods.** The ellipsoid method and analytic center methods cut through the center of the current region instead of at an LP vertex, which gives bounds on the number of cuts.

## Pitfalls

- **Tailing off.** The bound often improves fast in the first rounds and then very slowly. Stop when the gain per round is small and branch instead.
- **Numerical safety.** Cuts computed in floating point can be slightly invalid and cut off the true optimum. Solvers scale cuts, reject cuts with a large range of coefficients, and relax the right side a little. Exact solvers recompute cuts in rational arithmetic.
- **Growing LPs and unstable bases.** Each round adds rows, and cuts derived from cuts, as in repeated Gomory rounds, give dense rows and ill-conditioned bases. Remove cuts that stay slack, and limit the rank of cuts derived from other cuts.
- **Local cuts used globally.** A cut that uses the bounds of a branch and bound node is valid only in its subtree. Storing it in the global pool can remove the optimum.
- **An optimal face, not a vertex.** At the end, the LP may have an optimal face with both integral and fractional vertices. The test in line L6 needs an integral optimal vertex, so a solver may need one more pivot or a small change of the objective.

## Exercises

1. In the example, find the Gomory fractional cut from the optimal tableau row of $x_2$ in round 0, and check that it is $x_2 \le 1$ in the original variables.
2. Show that the cut $x_1 + x_2 \le 2$ defines a facet of the integer hull of the example.
3. Prove that if every cut is valid for $P_I$, the LP values never increase from one round to the next.
4. Give a two-variable integer program for which some separation routine returns valid cuts forever without reaching an integral LP optimum.

## References
