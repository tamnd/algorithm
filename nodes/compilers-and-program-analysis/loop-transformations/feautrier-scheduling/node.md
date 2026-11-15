---
tag: 7EMC3G
kind: algorithm
slug: feautrier-scheduling
name: Feautrier scheduling algorithm
aliases:
- Feautrier's multidimensional scheduling
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Finds affine schedules with the affine form of Farkas' lemma and linear programming, satisfying as many dependences as possible per dimension.
model: word-ram
complexity:
  vars: {e: the number of dependence edges (pairs of accesses times depths), L: the cost of one linear program solve, M: the size of the largest linear program}
  time: {worst: O(e L)}
  space: {extra: O(M)}
properties: {deterministic: true, recursive: false}
prereqs: [lexicographic-order, linear-programming-problem, simplex-method, farkas-lemma, polyhedral-model, affine-scheduling-problem]
see_also: [pluto-algorithm, lamport-hyperplane-method, feautrier-array-dataflow, polyhedral-scanning, wavefront-parallelism, loop-transformation-legality, allen-kennedy-algorithm, critical-path]
sources:
  - paper: doi:10.1007/BF01407835
    title: Paul Feautrier, Some efficient solutions to the affine scheduling problem, Part I, One-dimensional time, International Journal of Parallel Programming 21(5), 1992, 313-347
    locator: the affine form of Farkas' lemma applied to dependence polyhedra, the linear constraints for legal one-dimensional schedules, and the nonnegativity of the schedule on the domains
  - paper: doi:10.1007/BF01379404
    title: Paul Feautrier, Some efficient solutions to the affine scheduling problem, Part II, Multidimensional time, International Journal of Parallel Programming 21(6), 1992, 389-420
    locator: the greedy construction of a multidimensional schedule, one dimension at a time, that strongly satisfies as many remaining dependences as possible, and the proof that it always terminates for static control programs
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Corollary 7.1h (the affine form of Farkas' lemma)
---

Feautrier's algorithm computes a multidimensional affine schedule for a static control program. It is one solution of the [affine scheduling problem](/affine-scheduling-problem/). It builds the schedule one dimension at a time. For each dimension it solves a [linear program](/linear-programming-problem/) that keeps every remaining dependence in order (weak satisfaction) and puts as many of them as possible strictly in order (strong satisfaction). The affine form of [Farkas' lemma](/farkas-lemma/) makes "in order on the whole dependence polyhedron" a finite set of linear constraints. The edges that are strongly satisfied leave, and the next dimension handles the rest. Paul Feautrier published the method in 1992. It always terminates, so every static control program gets a legal schedule, even when no one-dimensional schedule exists.

## In plain words

A loop program has many runs of each statement, and some runs must wait for others. We want a timetable given by simple formulas, one formula per statement, that keeps every needed order. Sometimes one formula cannot do it. The algorithm then builds the time as a list of numbers. For the first number it looks for a formula that never puts a run before a run it needs, and that puts as many needed pairs as possible strictly in order. Those pairs are now done. The pairs that the first number leaves tied are handled by the second number, and so on. Each step is one optimization problem with straight-line constraints, which a standard solver handles exactly. Every step finishes at least one pair, so the list ends. Runs with the same list of numbers can run at the same moment.

## The problem

**Input.** A static control program with integer parameters $N$ in a context $K$. Statement $S$ has depth $d_S$ and an iteration domain $D_S$, a polyhedron that is bounded for each $N$. The loop counters are nonnegative on $D_S$, which a shift of each loop gives. A set $E$ of dependence edges $e : S \to T$, each with a dependence polyhedron $P_e$ of pairs $(\vec{s}, \vec{t})$ such that $T(\vec{t})$ must run after $S(\vec{s})$. This page and its implementation use memory-based dependences (flow, anti and output), one polyhedron per pair of accesses and per depth $l$. At depth $l$, $s_k = t_k$ for $k < l$ and $t_l \ge s_l + 1$. At the "same iteration" depth, the two instances share all their common loops and $S$ comes first in the text.

**Output.** For each statement $S$, a list $\Theta_S = (\theta^1_S, \dots, \theta^m_S)$ of affine forms in $\vec{s}$ and $N$ such that $\Theta_S(\vec{s}) <_{\mathrm{lex}} \Theta_T(\vec{t})$ for every edge $e$ and every $(\vec{s}, \vec{t}) \in P_e$. The instances run in the [lexicographic order](/lexicographic-order/) of their time vectors, and instances with equal vectors may run in parallel.

**Weak and strong.** One dimension $\theta$ *weakly satisfies* $e$ if $\theta_T(\vec{t}) - \theta_S(\vec{s}) \ge 0$ on $P_e$, and *strongly satisfies* it if $\theta_T(\vec{t}) - \theta_S(\vec{s}) \ge 1$ on $P_e$. A list of dimensions is legal for $e$ when some dimension strongly satisfies $e$ and all earlier dimensions weakly satisfy it.

## The algorithm

Each dimension is the solution of a linear program whose unknowns are the coefficients of $\theta_S$ for every statement, one variable $\varepsilon_e \in [0, 1]$ per remaining edge, and the Farkas multipliers. The condition "$\theta_T(\vec{t}) - \theta_S(\vec{s}) \ge \varepsilon_e$ on $P_e$" becomes, by the affine Farkas lemma,

$$\theta_T(\vec{t}) - \theta_S(\vec{s}) - \varepsilon_e \equiv \lambda_{e,0} + \sum_i \lambda_{e,i}\, c_{e,i}(\vec{s}, \vec{t}, N), \qquad \lambda_e \ge 0,$$

where $c_{e,i} \ge 0$ are the constraints of $P_e$. The identity holds for all values of $\vec{s}$, $\vec{t}$ and $N$, so it means one linear equation per variable and one for the constant. The same lemma gives Feautrier's condition $\theta_S \ge 0$ on $D_S$.

```pseudo id=main
FEAUTRIER-SCHEDULE(program)
L1  E <- the dependence polyhedra P_e of the program, one per pair of accesses and depth
L2  while E is not empty do
L3      E' <- the edges still in E; theta_S has free coefficients, with theta_S >= 0 on D_S for each S
L4      for each e: S -> T in E' add 0 <= eps_e <= 1 and, by Farkas, theta_T(t) - theta_S(s) >= eps_e on P_e
L5      solve the linear program: maximize the sum of the eps_e; G <- { e : eps_e = 1 }
L6      solve it again with eps_e = 1 on G and eps_e = 0 elsewhere, minimizing the sum of |coefficients|
L7      scale theta to integer coefficients and append theta_S to Theta_S for every S
L8      E <- E minus G
L9      go to the next dimension
L10 return Theta
```

**Why $\varepsilon_e$ is 0 or 1.** Line L5 never returns a fraction. Take a feasible solution in which the smallest positive $\varepsilon_e$ is $\mu < 1$. Divide every $\theta_S$ by $\mu$. Every difference grows by the factor $1/\mu$, so each edge with $\varepsilon_e > 0$ now has a difference of at least 1 on $P_e$, and the others still have at least 0. The sum of the $\varepsilon_e$ grows. So at an optimum every $\varepsilon_e$ is 0 or 1, and the optimum is the largest number of remaining edges that one affine dimension can strongly satisfy while it weakly satisfies all the others.

**Line L6.** The optimum of L5 is not unique, and the vertex that the simplex method finds can have large coefficients. Line L6 keeps the same set $G$ and picks small coefficients, with a small weight on the constant terms. This is a choice of this implementation. Feautrier solves each dimension with parametric integer programming and takes a lexicographic minimum, which gives integer coefficients and, in Part I, puts a bound on the latency first. Any solution with the same $G$ is a correct dimension.

**Line L7.** The linear program works over the rationals. Multiplying all $\theta_S$ of one dimension by the least common multiple $D$ of the denominators keeps every difference at least 0, and the strong ones at least $D \ge 1$.

## Example

**Running sum.** For `for i = 0 to N: for j = 0 to N: S: s = s + A[i][j]`, every instance reads and writes `s`. There are two edges: $e_1$ at depth 1 ($t_1 \ge s_1 + 1$, with $s_2$ and $t_2$ free in $[0, N]$) and $e_2$ at depth 2 ($s_1 = t_1$, $t_2 \ge s_2 + 1$). The [affine scheduling problem](/affine-scheduling-problem/) page shows that no single affine form strongly satisfies both.

- In the first round, $\theta = a i + b j + c N + c_0$ must weakly satisfy $e_1$. On $e_1$ the difference $a(t_1 - s_1) + b(t_2 - s_2)$ takes the value $a - bN$ when $t_2 - s_2 = -N$, and for $N$ large this forces $b = 0$. Then $\theta = i$ strongly satisfies $e_1$ and gives difference 0 on $e_2$. The best sum is 1, and $G = \{e_1\}$.
- In the second round only $e_2$ is left, and $\theta = j$ strongly satisfies it.

The schedule is $\Theta_S(i, j) = (i, j)$, the original sequential order. This is correct: each instance needs the one before it, so there is no parallelism to find.

**Lower triangular matrix-vector product.**

```
for i = 0 to N - 1:
S1:   y[i] = 0
      for j = 0 to i:
S2:       y[i] = y[i] + L[i][j] * x[j]
```

The edges go from $S1(i)$ to $S2(i, j)$ and from $S2(i, j)$ to $S2(i, j')$ with $j' > j$. One round strongly satisfies all of them with $\theta_{S1}(i) = 0$ and $\theta_{S2}(i, j) = j + 1$. At time 0 all the $S1$ instances run in parallel. At time $j + 1$, every row $i \ge j$ adds its $j$-th term in parallel. The last instance runs at time $N$, so there are $N + 1$ time steps, against $N + N(N+1)/2$ instances that the sequential program runs one after the other.

**Two-dimensional stencil.** For `A[i][j] = A[i-1][j] + A[i][j-1]` over $1 \le i, j \le N$, one round gives $\theta(i, j) = i + j$, the [wavefront](/wavefront-parallelism/) schedule of [Lamport's hyperplane method](/lamport-hyperplane-method/).

**Reverse copy.** For `x[i] = f(i)` over $0 \le i \le N$ followed by `y[j] = x[N - j]` over $0 \le j \le N$, the schedule is $\theta_{S1} = 0$ and $\theta_{S2} = 1$. Each loop becomes fully parallel, and the two loops stay in sequence.

## Correctness

The full proof is in [the proof page](proofs/correctness.md). Here is the outline.

- **Each dimension is valid.** By the affine Farkas lemma, the linear constraints of line L4 hold exactly when $\theta_T - \theta_S \ge \varepsilon_e$ on the whole polyhedron $P_e$, for nonempty $P_e$. By the scaling argument above, the edges with $\varepsilon_e = 1$ are strongly satisfied, and all other remaining edges are weakly satisfied.
- **Each round makes progress.** If $E$ is not empty, some affine dimension strongly satisfies at least one edge of $E$ and weakly satisfies the others. Take the original schedule vector $(\beta_0, s_1, \beta_1, \dots)$, where $\beta_k$ is a text position, and the first position $p$ at which some edge of $E$ is strongly satisfied. All edges of $E$ have equal components before $p$, so the component at $p$ weakly satisfies all of them. It is also nonnegative when the loop counters are. So $G$ is never empty.
- **Termination.** Each round removes at least one edge, so there are at most $|E|$ rounds.
- **Legality.** An edge removed in round $r$ is weakly satisfied by rounds $1$ to $r - 1$, because it was still in $E$, and strongly satisfied by round $r$. So for each pair in $P_e$, the first nonzero component of the difference of the time vectors is positive.
- **One dimension when possible.** If a nonnegative one-dimensional schedule exists, it strongly satisfies every edge, so the first round has $G = E$ and the algorithm returns one dimension.

## Complexity

Building the edges takes one rational feasibility test per pair of accesses and depth, at most $e$ tests. There are at most $e$ rounds, each with two linear programs, so the total is $O(e)$ linear program solves, $O(e L)$. The linear programs have one unknown per schedule coefficient, per edge and per constraint of each $P_e$, and one equation per variable of each $P_e$. So $M$ is linear in the size of the dependence polyhedra. With the [simplex method](/simplex-method/), $L$ is exponential in the worst case and small in practice. With a polynomial algorithm for linear programming, the whole method runs in polynomial time. This is one reason Feautrier's method is practical, unlike exact searches for the schedule with the lowest latency.

The implementation on this page uses an exact simplex method over integer rows with Dantzig's rule and a lexicographic ratio test, which does not cycle.

## Properties

- **Always succeeds.** Every static control program gets a legal schedule. The number of dimensions is at most the number of edges.
- **Greedy.** Each dimension maximizes the number of strongly satisfied edges among the remaining ones. Edges that the outer dimensions satisfy leave the outer loops free of their constraints, which tends to make inner dimensions parallel.
- **Parallelism, not locality.** The objective counts satisfied edges. It does not look at reuse or at the size of the dependence distances.
- **Exact arithmetic.** Legality on the whole parametric polyhedron is exact. No point is sampled and nothing is rounded.

## Variants and improvements

- **One-dimensional schedules.** Feautrier's Part I asks for one affine form that strongly satisfies every edge, with a bound on the latency as the objective. When it exists, the latency is affine in $N$.
- **Integer solutions by PIP.** Feautrier solves each linear program with parametric integer programming, as in [array dataflow analysis](/feautrier-array-dataflow/). The lexicographic minimum gives integer coefficients directly.
- **Dataflow input.** With the exact source functions of array dataflow analysis as edges, after array expansion, only the true flow of values constrains the schedule, and more parallelism appears.
- **Pluto.** The [Pluto algorithm](/pluto-algorithm/) keeps the Farkas linearization and the per-dimension structure, but asks for hyperplanes that weakly satisfy a whole band of edges, so that the band can be tiled, and minimizes a bound on the dependence distances.
- **Uniform programs.** For uniform dependences, linear schedules go back to Karp, Miller and Winograd, and [Lamport's hyperplane method](/lamport-hyperplane-method/) is the one-dimensional case.

## When to use it

Use it to find the parallelism of a static control program automatically: the result says which loops are parallel and which must stay sequential, and it works for imperfect nests with many statements. When locality and tiling matter more than the degree of parallelism, the Pluto algorithm is the usual choice. For a single perfect loop nest with uniform dependences, a unimodular transformation or the hyperplane method is simpler.

## Pitfalls

- **Affine programs only.** The dependence polyhedra and the Farkas linearization need affine loop bounds and affine subscripts. Index arrays, non-affine subscripts and data-dependent conditions take the program out of the model.
- **A legal schedule can be slow.** The matrix-vector schedule $\theta_{S2} = j + 1$ runs the rows in parallel and walks down the columns of `L`, which has poor locality for a row-major array. It also needs one barrier per time step. The algorithm counts satisfied edges and knows nothing about caches, vector units or synchronization costs.
- **Large coefficients.** A vertex of the first linear program can have large coefficients, and scaling to integers can make them larger. Loops generated from such a schedule have large strides and many empty iterations. A second objective, as in line L6, or a lexicographic minimum, keeps them small.
- **Keep $\varepsilon_e \le 1$.** Without the bound, the linear program is unbounded, because the schedule can be scaled up without limit.
- **Empty polyhedra.** The affine Farkas lemma needs a nonempty $P_e$. An empty dependence polyhedron must be dropped before the schedule is built. Otherwise its Farkas equations can have no solution, or they restrict the schedule for no reason.
- **Memory-based edges limit parallelism.** Anti and output dependences force orders that array expansion could remove. Feeding the algorithm the exact dataflow edges gives more freedom, but then the generated code must expand the arrays.

## Implementations

## History

Paul Feautrier published the two parts of "Some efficient solutions to the affine scheduling problem" in 1992. Part I applies the affine form of Farkas' lemma to dependence polyhedra and finds one-dimensional schedules by linear programming. Part II shows that some programs have no one-dimensional schedule and gives the greedy construction of multidimensional schedules on this page. The work extends the linear schedules of Karp, Miller and Winograd (1967) for uniform recurrences and Lamport's hyperplane method (1974) to programs with affine dependences and many statements. Darte and Vivien later studied how much parallelism such schedules can find. In 2002, Vivien showed that, inside its own framework, the greedy method does not lose parallelism because of the way it is designed. In 2008, Bondhugula and his coauthors used the same linearization in the Pluto algorithm, with a cost function aimed at tiling and locality.

## References
