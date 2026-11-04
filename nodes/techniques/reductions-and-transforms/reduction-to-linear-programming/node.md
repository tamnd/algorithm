---
tag: 11AQPY
kind: technique
slug: reduction-to-linear-programming
name: Reduction to linear programming
aliases:
- LP formulation
- reduction to LP
area: techniques/reductions-and-transforms
level: core
summary: Modeling a problem as a linear program so that a general LP solver computes its solution.
prereqs: [reduction, linear-programming-problem]
see_also: [shortest-paths-lp-formulation, max-flow-lp-formulation, min-cost-flow-lp-formulation, total-unimodularity, lp-relaxation, lp-rounding-vertex-cover, lp-in-p, simplex-method]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 29, Linear programming (the section on formulating problems as linear programs, with shortest paths, maximum flow and minimum-cost flow); Chapter 35, Approximation algorithms (weighted vertex cover by linear programming)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 11.6, Linear programming and rounding, an application to vertex cover
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 19, Totally unimodular matrices, fundamental properties and examples (integral polyhedra, incidence matrices of bipartite and directed graphs)
  - paper: doi:10.1007/BF02579150
    title: "Narendra Karmarkar, A new polynomial-time algorithm for linear programming, Combinatorica 4(4) (1984), 373-395"
    locator: the interior-point algorithm and its polynomial bound in the bit length of the input
---

A reduction to linear programming solves a problem by writing it as a [linear program](/linear-programming-problem/): real variables, a linear objective, and linear constraints, so that an optimal solution of the program gives an answer to the problem. Shortest paths, maximum flow, minimum-cost flow and systems of difference constraints have exact formulations of this kind. Since a linear program with rational data can be solved in time polynomial in its bit length ([LP in P](/lp-in-p/)), every polynomial-size formulation gives a polynomial-time algorithm. The main trap is integrality: a linear program may return a fractional solution where the problem needs whole numbers.

## In plain words

Many problems ask for the best choice of some amounts under limits: how much to send along each pipe, how far each town is from the start, which machines to switch on. If every limit says "this sum of amounts is at most that number", and the goal is to make one sum as large or as small as possible, then the problem is a linear program. General solvers exist, so the work is to write the problem in this form and read the answer back.

The catch is that a linear program allows fractions. When the real question asks for a yes or no for each item, the program may answer "one half". For some problems with a special structure, the best answer is always whole. For others, the fractional answer is only a bound, and turning it into a whole answer is a separate problem.

## When it applies

- The answer is a vector of amounts, and each rule is a linear inequality or equation in these amounts.
- The objective is linear, or can be made linear with extra variables (for example a maximum of linear terms, or an absolute value).
- The problem is a flow, a path, a potential or a matching problem, where the constraint matrix often has the [total unimodularity](/total-unimodularity/) property and the optimum is integral.
- The problem is a hard 0-1 problem, and a lower or upper bound or a rounding scheme is wanted. Then the linear program is a [relaxation](/lp-relaxation/), not an exact model.

## The template

```pseudo id=main
SOLVE-BY-LP(x)                          ▷ x an instance of the problem
L1  choose variables v, objective c·v, constraints A v ≤ b from x
L2  (status, v*) ← LP-SOLVER(c, A, b)     ▷ simplex, ellipsoid or interior point
L3  if status = infeasible or unbounded
L4      return the answer that this status means for x
L5  if the problem needs integers and v* is not integral
L6      make v* integral (a vertex, rounding, or an exact integer method)
L7  return RECOVER(x, v*)
```

The holes are the model in line L1, the meaning of each status in line L4, and the integrality step in line L6. Three facts must be proved for each use: every solution of the problem gives a feasible point of the same objective value; every optimal point, or every optimal vertex, gives a solution of the problem; and infeasible or unbounded programs match the right answers, such as "no path" or "a negative cycle".

### What transfers

Let the program have $n$ variables, $m$ constraints and rational data of total bit length $L$.

- **Polynomial time.** The [ellipsoid method](/ellipsoid-method/) and [interior-point methods](/interior-point-method/) solve the program in time polynomial in $L$. Karmarkar's method uses $O(n^{3.5} L)$ arithmetic operations (Karmarkar, 1984). So a formulation that is built in polynomial time, with polynomial $n$, $m$ and bit length, gives a polynomial-time algorithm by the cost rule of [reductions for algorithms](/reductions-for-algorithms/).
- **Not strongly polynomial.** These bounds depend on the bit length $L$, not only on $n$ and $m$. No algorithm is known that solves every linear program in a number of arithmetic operations polynomial in $n$ and $m$ alone.
- **The simplex method.** The [simplex method](/simplex-method/) is fast in practice, but with the classical pivot rules some inputs make it take a number of pivots exponential in $n$ ([Klee-Minty cube](/klee-minty-cube/)). [Smoothed analysis](/smoothed-simplex-analysis/) explains its good behaviour on perturbed inputs.
- **Certificates.** [LP duality](/lp-duality/) gives with the optimum a dual solution that proves it optimal. For maximum flow the dual is a minimum cut.

### Integrality

An integer linear program adds the constraint $v \in \mathbb{Z}^n$. It is NP-hard in general, since vertex cover is a special case. Dropping the integer constraint gives the [LP relaxation](/lp-relaxation/), whose optimum is a bound on the integer optimum: at least as good, never worse.

A matrix is *totally unimodular* (TU) when every square submatrix has determinant $0$, $1$ or $-1$.

**Theorem (integral vertices).** Let $A$ be TU and $b$ integral. Then every vertex of $P = \{v : Av \le b\}$ is integral.

*Proof.* A vertex $v$ of $P$ is the unique solution of $A' v = b'$ for some $n$ rows of $A$ whose $n \times n$ submatrix $A'$ is nonsingular. By Cramer's rule, $v_j = \det(A'_j) / \det(A')$, where $A'_j$ is $A'$ with column $j$ replaced by $b'$. Here $\det(A') = \pm 1$ since $A$ is TU, and $\det(A'_j)$ is an integer since $A'_j$ has integer entries. So $v_j$ is an integer. $\square$

Adding the bounds $0 \le v \le u$ keeps the matrix TU: a square submatrix with a row from $\pm I$ has a row with one nonzero $\pm 1$, and expansion along that row reduces it to a smaller square submatrix, so induction on the order gives the claim. So the theorem also covers boxes. The converse direction and more criteria are in Schrijver, Chapter 19.

**Lemma (graphs).** The vertex-edge incidence matrix of a [bipartite graph](/bipartite-graph/) is TU. The vertex-arc incidence matrix of a directed graph, with $+1$ at the tail and $-1$ at the head, is TU.

*Proof.* Induction on the order $k$ of a square submatrix $B$. For $k = 1$ the entries are $0$ or $\pm 1$. Let $k > 1$. If a column of $B$ is zero, $\det B = 0$. If a column has exactly one nonzero entry, expand along it: $\det B = \pm \det B'$ with $B'$ of order $k - 1$, which is $0$ or $\pm 1$ by induction. Otherwise every column of $B$ has two nonzero entries. In the bipartite case, they are a $1$ in a row of a vertex of one side and a $1$ in a row of a vertex of the other side, so the sum of the rows of the first side minus the sum of the rows of the second side is zero. In the directed case, they are a $+1$ and a $-1$, so the sum of all rows is zero. In both cases the rows of $B$ are dependent and $\det B = 0$. $\square$

For a graph with an odd cycle the lemma fails. The incidence matrix of a triangle, with rows the vertices $1, 2, 3$ and columns the edges $12, 23, 13$, is

$$\begin{pmatrix} 1 & 0 & 1 \\ 1 & 1 & 0 \\ 0 & 1 & 1 \end{pmatrix}, \qquad \det = 2.$$

## Classic examples

### Shortest paths

For a directed graph with weights $w$, a source $s$ and a target $t$, the program (CLRS, Chapter 29) is

$$\text{maximize } d_t \quad \text{subject to} \quad d_v - d_u \le w(u, v) \ \text{for each arc } (u, v), \qquad d_s = 0.$$

*Why it is correct.* Delete first the vertices not reachable from $s$; they lie on no path from $s$. Assume that $t$ is reachable and that the graph has no negative cycle, and let $\delta(v)$ be the shortest-path distance from $s$. For a feasible $d$ and a shortest path $s = v_0, \ldots, v_k = t$, adding the constraints along the path gives $d_t - d_s \le \sum_i w(v_{i-1}, v_i) = \delta(t)$, so $d_t \le \delta(t)$. The distances satisfy $\delta(v) \le \delta(u) + w(u, v)$ for each arc, so $d = \delta$ is feasible and reaches $\delta(t)$. So the optimum is $\delta(t)$. If the graph has a negative cycle $C$, adding the constraints along $C$ gives $0 \le w(C) < 0$, since the left sides cancel, so the program is infeasible; [Bellman-Ford](/bellman-ford/) detects this case directly. Minimizing $d_t$ instead is a different program, which is unbounded when no path leads from $t$ to $s$. See [shortest paths as a linear program](/shortest-paths-lp-formulation/).

*Example.* Arcs $s \to a$ of weight $4$, $s \to b$ of weight $1$, $b \to a$ of weight $2$, $a \to t$ of weight $1$, $b \to t$ of weight $5$. With $d_s = 0$ the constraints are $d_a \le 4$, $d_b \le 1$, $d_a - d_b \le 2$, $d_t - d_a \le 1$, $d_t - d_b \le 5$. The optimum is $d_t = 4$ at the unique optimal point $d_a = 3$, $d_b = 1$, $d_t = 4$. The tight constraints are those of the arcs $s \to b$, $b \to a$, $a \to t$, which form the shortest path $s, b, a, t$ of length $1 + 2 + 1 = 4$. RECOVER reads the path from the tight arcs.

### Maximum flow

With a variable $f_{uv}$ for each arc,

$$\text{maximize } \sum_{(s, v)} f_{sv} - \sum_{(v, s)} f_{vs} \quad \text{subject to} \quad 0 \le f_{uv} \le c(u, v), \qquad \sum_{(u, v)} f_{uv} = \sum_{(v, w)} f_{vw} \ \text{ for } v \ne s, t.$$

The equality constraints use rows of the vertex-arc incidence matrix, which is TU by the lemma. An equation is two inequalities, a row and its negative; a square submatrix that holds both has determinant $0$, and any other is a submatrix of a TU matrix with some rows negated. The bounds keep the matrix TU as shown above. So with integer capacities every vertex is integral, the [flow integrality theorem](/flow-integrality-theorem/) in LP form. The dual program is the minimum cut. See [maximum flow as a linear program](/max-flow-lp-formulation/) and [max-flow linear program](/max-flow-linear-program/).

### Minimum-cost flow

Add a cost $a_{uv}$ per unit on each arc, a demand $b_v$ at each vertex, and minimize $\sum a_{uv} f_{uv}$ subject to the capacity bounds and $\sum_{(v, w)} f_{vw} - \sum_{(u, v)} f_{uv} = b_v$. The matrix is the same, so integer capacities and demands give an integral optimal vertex. Transportation and [assignment](/assignment-problem/) are special cases. See [min-cost flow as a linear program](/min-cost-flow-lp-formulation/) and the [min-cost flow problem](/min-cost-flow-problem/).

### Difference constraints

A system of $m$ constraints $x_j - x_i \le b_k$ in $n$ unknowns is a linear feasibility problem with zero objective. The [Bellman-Ford](/bellman-ford/) algorithm on the constraint graph solves it in $O(n^2 + nm)$ time without an LP solver, and with integer $b$ the solution it returns is integral. The system has no solution exactly when the constraint graph has a negative cycle, by the telescoping argument of the shortest-path program. See [difference constraints](/difference-constraints/).

### Vertex cover: the relaxation and its gap

For a graph $G = (V, E)$ with weights $w$, the integer program is: minimize $\sum_v w_v x_v$ subject to $x_u + x_v \ge 1$ for each edge $uv$ and $x_v \in \{0, 1\}$. The relaxation replaces $x_v \in \{0, 1\}$ by $0 \le x_v \le 1$. Its matrix is the transpose of the incidence matrix.

- If $G$ is bipartite, the matrix is TU and the relaxation has an integral optimal vertex. For the 4-cycle with unit weights the LP optimum is $2$, at $x = (0, 1, 0, 1)$, equal to the integer optimum. This is [König's theorem](/konig-theorem/) in LP form.
- For the triangle with unit weights the LP optimum is $3/2$, at $x = (1/2, 1/2, 1/2)$, and the integer optimum is $2$. The polytope has exactly five vertices: $(0,1,1)$, $(1,0,1)$, $(1,1,0)$, $(1,1,1)$ and $(1/2, 1/2, 1/2)$, and the objective is smallest at the fractional one. The ratio $2 / (3/2) = 4/3$ is the [integrality gap](/integrality-gap/) of this instance.
- In the same way the matching program of the triangle (maximize $x_{12} + x_{13} + x_{23}$, the sum at each vertex at most $1$, $x \ge 0$) has optimum $3/2$ at $(1/2, 1/2, 1/2)$, while a maximum matching has $1$ edge.

**Half-integrality.** Every vertex of the vertex cover relaxation has coordinates in $\{0, 1/2, 1\}$ ([half-integrality](/half-integrality/)). *Proof.* Let $x$ be feasible with some coordinate outside $\{0, 1/2, 1\}$. For a small $\varepsilon > 0$, let $y$ add $\varepsilon$ to each coordinate in $(0, 1/2)$ and subtract $\varepsilon$ from each coordinate in $(1/2, 1)$, and let $z$ do the opposite. A tight edge, $x_u + x_v = 1$, with $x_u \in (0, 1/2)$ has $x_v \in (1/2, 1)$, so its two changes cancel; a tight edge with $x_u = 1/2$ has $x_v = 1/2$ and does not change. Edges that are not tight and the bounds $0 \le x_v \le 1$ stay true for $\varepsilon$ small enough. So $y$ and $z$ are feasible, $y \ne z$, and $x = (y + z)/2$. Hence $x$ is not a vertex. $\square$

Taking every $v$ with $x_v \ge 1/2$ gives a cover of weight at most twice the optimum: [LP rounding for vertex cover](/lp-rounding-vertex-cover/).

## Variations

- **Integer programs.** When the matrix is not TU, use an exact integer method: branch and bound, [cutting planes](/cutting-plane-method-integer-programming/), or a solver for [mixed integer programs](/mixed-integer-programming/). The LP relaxation then gives the bounds.
- **Rounding.** For hard problems, solve the relaxation and round: [linear programming rounding](/linear-programming-rounding/), [randomized rounding](/randomized-rounding/), [iterative rounding](/iterative-rounding/), and the [primal-dual schema](/primal-dual-schema/), which avoids solving the program.
- **Fixed dimension.** With a constant number of variables, a linear program is solved in time linear in the number of constraints ([Megiddo's algorithm](/megiddo-fixed-dimension-lp/), [Seidel's algorithm](/seidel-linear-programming/)). Geometric problems such as the smallest enclosing circle fit the related framework of [LP-type problems](/lp-type-problem/).
- **Exponentially many constraints.** A formulation with exponentially many constraints, such as the [subtour elimination LP](/subtour-elimination-lp/), is still solvable in polynomial time by the ellipsoid method if a separation algorithm finds a violated constraint in polynomial time.
- **Other models.** Markov decision processes ([linear programming for MDPs](/linear-programming-for-mdps/)) and zero-sum games also reduce to linear programs.

## Pitfalls

- **Assuming integrality.** An LP solver may return a fractional optimum. The theorem above gives integral vertices when the matrix is TU and the right-hand side is integral; in other cases it gives nothing. The triangle shows a fractional optimal vertex.
- **An integral optimum value with a fractional optimal point.** Even with a TU matrix, an optimal face can contain fractional points. For the 4-cycle, the matching program has optimum $2$, reached both at an integral matching and at $x = (1/2, 1/2, 1/2, 1/2)$. Interior-point methods return a point inside the optimal face, so RECOVER must first move to a vertex.
- **Ignoring the status.** An infeasible or unbounded program has a meaning for the problem: no feasible schedule, a negative cycle, or an error in the model. Map each status to an answer.
- **The wrong direction of optimization.** The shortest-path program maximizes $d_t$, although the problem asks for a minimum. Minimizing $d_t$ gives a different program.
- **Strict inequalities.** A linear program allows only $\le$, $\ge$ and $=$. A rule such as $x < y$ needs integer data and a margin, as $x \le y - 1$, or a change of the model.
- **Bit length.** The polynomial bounds are in the bit length of the data. Numbers with many bits make the solver slow, and floating-point solvers can return slightly infeasible points.
- **A general solver where a special algorithm exists.** Shortest paths, flows and difference constraints have combinatorial algorithms that are much faster than a general LP solver. The LP form is most useful as a proof of polynomial time, as a source of duality, or when side constraints make the special algorithms fail.

## Exercises

1. Write the maximum bipartite matching problem as a linear program, and use the lemma to prove that it has an integral optimal vertex.
2. Write the minimization of $\max_i |a_i \cdot x - b_i|$ over $x \in \mathbb{R}^n$ as a linear program.
3. For the shortest-path example, write the dual program and give an optimal dual solution. Explain it as a unit of flow from $s$ to $t$.
4. Show that the vertex cover relaxation of the 5-cycle with unit weights has optimum $5/2$, and give the integer optimum.
5. Give a system of difference constraints with no solution, and the negative cycle in its constraint graph.

## References
