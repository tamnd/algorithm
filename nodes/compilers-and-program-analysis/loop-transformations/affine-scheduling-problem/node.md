---
tag: E2WERK
kind: problem
slug: affine-scheduling-problem
name: Affine scheduling
aliases:
- multidimensional affine scheduling
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Find affine functions that map each statement instance to a time point and respect every dependence, to expose parallelism.
prereqs: [polyhedral-model, data-dependence, lexicographic-order, farkas-lemma, linear-programming-problem]
see_also: [feautrier-scheduling, pluto-algorithm, lamport-hyperplane-method, feautrier-array-dataflow, polyhedral-scanning, loop-transformation-legality, wavefront-parallelism, critical-path]
sources:
  - paper: doi:10.1007/BF01407835
    title: Paul Feautrier, Some efficient solutions to the affine scheduling problem, Part I, One-dimensional time, International Journal of Parallel Programming 21(5), 1992, 313-347
    locator: the definition of affine schedules and their latency, the affine form of Farkas' lemma, and the linear program for one-dimensional schedules
  - paper: doi:10.1007/BF01379404
    title: Paul Feautrier, Some efficient solutions to the affine scheduling problem, Part II, Multidimensional time, International Journal of Parallel Programming 21(6), 1992, 389-420
    locator: multidimensional schedules, the programs with no one-dimensional schedule, and the proof that every static control program has a multidimensional affine schedule
  - paper: doi:10.1145/321406.321418
    title: Richard M. Karp, Raymond E. Miller and Shmuel Winograd, The organization of computations for uniform recurrence equations, Journal of the ACM 14(3), 1967, 563-590
    locator: linear schedules for systems of uniform recurrence equations and the conditions for their existence
  - paper: doi:10.1145/1375581.1375595
    title: Uday Bondhugula, Albert Hartono, J. Ramanujam and P. Sadayappan, A practical automatic polyhedral parallelizer and locality optimizer, PLDI 2008, 101-113
    locator: the formulation with weak and strong satisfaction per dimension and the objective that bounds dependence distances
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Corollary 7.1h (the affine form of Farkas' lemma)
---

The affine scheduling problem asks for a *schedule* of a loop program: a function that gives each run of each statement, each *instance*, a time, so that every instance runs after the instances it depends on. The schedule must be affine in the loop counters and in the size parameters of the program, one function per statement. Instances that get the same time can run in parallel, so a good schedule exposes parallelism, and the loops of the new program come from the schedule. The problem is the core of the [polyhedral model](/polyhedral-model/). Its key fact, due to Feautrier, is that the affine form of [Farkas' lemma](/farkas-lemma/) turns "respect every dependence" into a finite set of linear constraints.

## In plain words

A loop program runs its statements in a fixed order, many times over. Some runs need a value that an earlier run produced, so they must stay after it. All other runs could happen at the same moment. A schedule is a timetable: it gives each run a time. The timetable is legal if every run comes after the runs it needs. A compiler wants a short timetable that it can turn back into loops. So the timetable must be a simple formula, a sum of the loop counters times some constants. Sometimes one number per run is not enough, because a long chain of runs each needs the one before. Then the time is a list of numbers, compared like words in a dictionary, and the program keeps some outer loops in order and runs the inner ones in parallel.

## Definition

**Input.** A static control program with integer parameters $N$ in a context $K$. Statement $S$ has an iteration domain $D_S \subseteq \mathbb{Z}^{d_S}$, a polyhedron that depends on $N$. A set of dependence edges $e : S \to T$, each with a dependence polyhedron $P_e$ of pairs $(\vec{s}, \vec{t})$, $\vec{s} \in D_S$, $\vec{t} \in D_T$, such that $T(\vec{t})$ must run after $S(\vec{s})$. The edges come from [dependence analysis](/data-dependence/) or from [array dataflow analysis](/feautrier-array-dataflow/).

**One-dimensional schedule.** For each statement, an affine function

$$\theta_S(\vec{s}) = \vec{a}_S \cdot \vec{s} + \vec{b}_S \cdot N + c_S$$

with integer coefficients, such that for every edge $e : S \to T$ and every $(\vec{s}, \vec{t}) \in P_e$,

$$\theta_T(\vec{t}) - \theta_S(\vec{s}) \ge 1, \tag{legality}$$

and, in Feautrier's formulation, $\theta_S(\vec{s}) \ge 0$ on $D_S$. Instances with the same time run in parallel. The *latency* is the largest time used, $\max_S \max_{D_S} \theta_S$.

**Multidimensional schedule.** For each statement, an affine map $\Theta_S : \mathbb{Z}^{d_S} \to \mathbb{Z}^m$, such that $\Theta_S(\vec{s}) <_{\mathrm{lex}} \Theta_T(\vec{t})$ for every edge and every pair in $P_e$, where $<_{\mathrm{lex}}$ is the [lexicographic order](/lexicographic-order/). Dimension $k$ of the schedule *strongly satisfies* an edge at a pair when $\Theta_T - \Theta_S$ is $0$ in the dimensions before $k$ and at least $1$ in dimension $k$. It *weakly satisfies* it when the difference is at least $0$. An outer dimension becomes a sequential loop, and a dimension that strongly satisfies no remaining edge becomes a parallel loop.

**Goal.** Find a legal schedule, or decide that none exists in the class, and optimize an objective: the latency, the number of dimensions, the number of outer parallel loops, or a measure of locality.

**The affine form of Farkas' lemma.** Let $P = \{x : A x + \vec{b} \ge 0\}$ be a nonempty polyhedron. An affine form $\psi$ is nonnegative on all of $P$ if and only if

$$\psi(x) = \lambda_0 + \vec{\lambda} \cdot (A x + \vec{b}) \quad \text{for some } \lambda_0 \ge 0,\ \vec{\lambda} \ge 0.$$

The "if" part is clear, since every term is nonnegative on $P$. The "only if" part is Corollary 7.1h of Schrijver. Apply it with $\psi = \theta_T(\vec{t}) - \theta_S(\vec{s}) - 1$ on $P_e$, where $P_e$ includes the context on $N$. Both sides are affine in $(\vec{s}, \vec{t}, N)$, so they are equal exactly when the coefficients of each variable and the constants are equal. Each such equation is linear in the unknown schedule coefficients and in the multipliers $\lambda$. So the infinite family of legality constraints, one per pair of instances, becomes a finite system of linear equalities and inequalities, with one block of multipliers per edge. The legal one-dimensional schedules are the projection of a polyhedron onto the schedule coefficients.

## Variants

- **Uniform dependences.** Every edge has a constant distance vector $\vec{d}$, so legality is $\vec{a} \cdot \vec{d} \ge 1$ for one shared $\vec{a}$. This is the setting of Karp, Miller and Winograd and of the [hyperplane method](/lamport-hyperplane-method/).
- **Linear or affine, shared or per statement.** The schedule may be the same for all statements, or each statement may have its own coefficients (the affine-by-statement schedules of Feautrier). It may or may not depend on $N$.
- **Rational schedules.** Some formulations allow rational coefficients and take the floor of the time. A rational schedule that satisfies $\theta_T - \theta_S \ge 1$ can be scaled to an integer one by multiplying by the common denominator, at the cost of a longer latency.
- **Weak and strong constraints per dimension.** In multidimensional scheduling, each dimension must weakly satisfy every edge that no outer dimension has strongly satisfied, and the algorithm decides which edges it satisfies strongly. Feautrier's algorithm maximizes the number of edges strongly satisfied per dimension; the [Pluto algorithm](/pluto-algorithm/) asks every dimension to weakly satisfy all remaining edges, which makes the band of dimensions tileable.
- **Objectives.** Minimal latency (Feautrier, Part I), minimal number of dimensions and so maximal parallelism (Feautrier, Part II), or minimal dependence distances for locality and communication (Bondhugula and others).

## Examples

**Both loops in parallel.** Take

```
for i = 0 to N:   S1: x[i] = f(i)
for j = 0 to N:   S2: y[j] = x[N - j]
```

The one edge $S1 \to S2$ has $P_e = \{(i, j) : i = N - j,\ 0 \le j \le N\}$. With $\theta_1(i) = a_1 i + b_1 N + c_1$ and $\theta_2(j) = a_2 j + b_2 N + c_2$, substitute $i = N - j$:

$$\psi = (a_2 + a_1) j + (b_2 - a_1 - b_1) N + (c_2 - c_1 - 1) = \lambda_0 + \lambda_1 j + \lambda_2 (N - j) + \lambda_3 N,$$

where the last term comes from the context $N \ge 0$. Equating coefficients gives $a_2 + a_1 = \lambda_1 - \lambda_2$, $b_2 - a_1 - b_1 = \lambda_2 + \lambda_3$ and $c_2 - c_1 - 1 = \lambda_0$, with all $\lambda \ge 0$. The choice $\theta_1 = 0$, $\theta_2 = 1$ with all $\lambda = 0$ solves it. All of $S1$ runs at time 0 and all of $S2$ at time 1: both loops are parallel, and the latency is 1.

**A wavefront.** In `A[i][j] = A[i-1][j] + A[i][j-1]` over $1 \le i, j \le N$, the distances are $(1, 0)$ and $(0, 1)$. Legality is $a_1 \ge 1$ and $a_2 \ge 1$, so $\theta = i + j$ is legal, with latency $2N - 2$ after a shift. Each anti-diagonal runs in parallel; this is [wavefront parallelism](/wavefront-parallelism/).

**No one-dimensional schedule.** Take the running sum over a square:

```
for i = 0 to N:
    for j = 0 to N:
S:      s = s + A[i][j]
```

Each instance reads the `s` written by the one just before it, so the $(N + 1)^2$ instances form one chain, and each must have a time at least 1 larger than the one before. A one-dimensional schedule therefore takes at least $(N + 1)^2$ different values on the square. But an affine $\theta(i, j) = a i + b j + c N + d$, with integer constants $a, b, c, d$ that do not depend on $N$, takes integer values between its minimum and its maximum on the square, and these differ by $(|a| + |b|) N$. So it takes at most $(|a| + |b|) N + 1$ values. For $N > |a| + |b|$ this is less than $(N + 1)^2$, so no one-dimensional affine schedule works for all $N$. The two-dimensional schedule $\Theta(i, j) = (i, j)$ is legal: it is the original order.

The same argument proves a general limit: if the domains fit in a box of side $O(N)$, every one-dimensional affine schedule has latency $O(N)$, so a program with a dependence chain longer than linear in $N$ has none.

**A multidimensional schedule always exists.** For a static control program, the original schedule $\Theta_S(\vec{s}) = (\beta^S_0, s_1, \beta^S_1, \dots, s_{d_S}, \beta^S_{d_S})$, padded with zeros to a common length, is affine, and the program runs the instances in its lexicographic order. Every dependence goes from an instance that runs earlier to one that runs later, so this schedule is legal. Feautrier proves this in Part II. So the multidimensional problem always has a solution, and the question is only how good it can be.

## Known algorithms

- [Lamport's hyperplane method](/lamport-hyperplane-method/): one linear schedule shared by all statements, for uniform dependences.
- [Feautrier's scheduling algorithm](/feautrier-scheduling/): one linear program per dimension, built with the affine form of Farkas' lemma; it finds a one-dimensional schedule of minimal latency when one exists, and a multidimensional one otherwise.
- [The Pluto algorithm](/pluto-algorithm/): tiling hyperplanes found one at a time by lexicographic minimization of a bound on dependence distances.
- [The Allen-Kennedy algorithm](/allen-kennedy-algorithm/) and [unimodular transformations](/unimodular-transformations/): special cases with less information (dependence levels) or with one shared linear map.

## Bounds

- **One-dimensional existence and minimal latency.** With the Farkas multipliers, both are [linear programs](/linear-programming-problem/) whose size is linear in the total number of constraints of the dependence polyhedra and domains. Rational linear programs are solvable in polynomial time, for example by the [ellipsoid method](/ellipsoid-method/) or an [interior point method](/interior-point-method/), so both questions are polynomial in this size, and an integer schedule follows by scaling. Here the model is exact rational arithmetic, with cost polynomial in the bit length.
- **Multidimensional existence.** Always yes for static control programs, by the original schedule.
- **A lower bound on latency.** Any legal schedule, affine or not, needs at least as many time steps as the longest chain of dependent instances, the [critical path](/critical-path/) of the instance graph. The running sum shows that one-dimensional affine schedules can miss this bound by more than a constant factor: the chain has $(N + 1)^2$ instances, while affine schedules only reach $O(N)$ distinct times.
- **Optimal schedules in general.** Without the affine restriction, the best schedule is a longest path computation in the graph of all instances, whose size grows with $N$. The affine restriction gives a problem whose size does not depend on $N$, at the price of possible suboptimality.

## Reductions

- **Legality to linear constraints.** Through the affine form of Farkas' lemma, as in the definition, one system per edge.
- **Objectives with integrality to integer programming.** Requiring integer coefficients with a bounded range, or a lexicographic minimum of a cost vector as in Pluto, gives an integer linear program, solved by [lexicographic optimization](/lexicographic-optimization/) with parametric integer programming or by branch and bound.
- **Schedule to code.** Turning a schedule into loops is [polyhedral scanning](/polyhedral-scanning/): the new loop nest visits the points of the transformed domains in lexicographic order.

## Applications

Automatic parallelization of loop nests, where outer dimensions become sequential loops and the rest parallel loops; loop [tiling](/loop-tiling/) after a transformation that makes all dependence distances nonnegative; the synthesis of systolic arrays and of hardware pipelines in [high-level synthesis](/high-level-synthesis/); and polyhedral compilers such as Pluto, PPCG and Polly.

A legal schedule is not a fast one. The original schedule is always legal and fully sequential. Latency counts time steps, not the cost of synchronization, the size of the parallel loops or the cache misses, so a schedule with minimal latency can run slower than another legal schedule. The objective that an algorithm optimizes is a model of speed, not a proof of it.

## References
