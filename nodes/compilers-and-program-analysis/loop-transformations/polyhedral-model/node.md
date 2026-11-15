---
tag: 2D6R5Q
kind: model
slug: polyhedral-model
name: Polyhedral model
aliases:
- polytope model
- polyhedral compilation
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Represents a loop nest with affine bounds and accesses as integer points in polyhedra, with affine schedules and access functions.
prereqs: [polyhedron, data-dependence, loop-transformation-legality, lexicographic-order]
see_also: [feautrier-array-dataflow, affine-scheduling-problem, feautrier-scheduling, pluto-algorithm, polyhedral-scanning, unimodular-transformations, presburger-arithmetic, barvinok-algorithm]
sources:
  - paper: doi:10.1145/321406.321418
    title: Richard M. Karp, Raymond E. Miller and Shmuel Winograd, The organization of computations for uniform recurrence equations, Journal of the ACM 14(3), 1967, 563-590
    locator: systems of uniform recurrence equations on the lattice points of a region, their computability and their schedules
  - paper: doi:10.1007/BF01407931
    title: Paul Feautrier, Dataflow analysis of array and scalar references, International Journal of Parallel Programming 20(1), 1991, 23-53
    locator: static control programs, iteration domains, the sequencing predicate and the exact source of each read by parametric integer programming
  - paper: doi:10.1007/BF01407835
    title: Paul Feautrier, Some efficient solutions to the affine scheduling problem, Part I, one-dimensional time, International Journal of Parallel Programming 21(5), 1992, 313-347
    locator: affine schedules, the affine form of Farkas' lemma, and the linear program for one-dimensional schedules
  - paper: doi:10.1007/BF01379404
    title: Paul Feautrier, Some efficient solutions to the affine scheduling problem, Part II, multidimensional time, International Journal of Parallel Programming 21(6), 1992, 389-420
    locator: multidimensional affine schedules, their existence for every static control program, and the greedy construction
  - paper: "Cédric Bastoul, Code generation in the polyhedral model is easier than you think, Proceedings of the 13th International Conference on Parallel Architectures and Compilation Techniques (PACT), 2004, 7-16"
    locator: scattering functions, the scanning of unions of polyhedra and the CLooG code generator
  - paper: doi:10.1145/1375581.1375595
    title: Uday Bondhugula, Albert Hartono, J. Ramanujam and P. Sadayappan, A practical automatic polyhedral parallelizer and locality optimizer, PLDI 2008, 101-113
    locator: the polyhedral representation used by Pluto (domains, dependence polyhedra, statement-wise affine transformations) and the tiling hyperplanes
  - paper: doi:10.1287/moor.19.4.769
    title: Alexander I. Barvinok, A polynomial time algorithm for counting integral points in polyhedra when the dimension is fixed, Mathematics of Operations Research 19(4), 1994, 769-779
    locator: the main theorem (counting the integer points of a rational polyhedron in fixed dimension in polynomial time)
---

The polyhedral model describes a loop nest by sets of integer points instead of by its text. Each execution of a statement, a *statement instance*, is an integer point $S(\vec{i})$ in a [polyhedron](/polyhedron/), the *iteration domain*. Each array reference is an affine function from the instance to the array cell it touches. The order of execution is an affine *schedule* that maps each instance to a date, a vector of integers compared in [lexicographic order](/lexicographic-order/). Dependences become sets of pairs of points described by linear constraints. With this, questions about the program (which instance writes the value that this one reads, is this reordering legal, how should the code look after the change) become questions about linear inequalities over the integers. Its roots are the uniform recurrence equations of Karp, Miller and Winograd (1967) and the [hyperplane method](/lamport-hyperplane-method/) of Lamport (1974). Feautrier gave it its general form for array programs in 1988 to 1992. It is the basis of the [Pluto](/pluto-algorithm/) compiler, of CLooG and isl, and of the polyhedral optimizers in GCC (Graphite) and LLVM (Polly).

## The machine

**Programs.** The model covers a *static control part* (SCoP): a part of a program built from `for` loops, `if` statements and assignments, such that

- the bounds of each loop are maxima and minima of affine functions of the outer loop indices and of the *parameters*;
- each condition of an `if` is a conjunction of affine inequalities in the same quantities;
- each array subscript is an affine function of the loop indices and the parameters;
- the parameters, such as the size $N$, are integers that do not change inside the part.

Integer division and remainder by a constant are often allowed too (quasi-affine expressions), since they can be written with extra integer variables. Scalars are arrays with zero dimensions.

**Iteration domains.** A statement $S$ inside $d_S$ loops has the domain

$$\mathcal{D}_S(\vec{N}) = \{\, \vec{i} \in \mathbb{Z}^{d_S} : A_S \vec{i} + B_S \vec{N} + \vec{c}_S \ge \vec{0} \,\},$$

the integer points of a polyhedron that depends on the parameters $\vec{N}$. Each point is one instance $S(\vec{i})$.

**Accesses.** Each reference of $S$ to an array $X$ is an affine function $f(\vec{i}) = F \vec{i} + G \vec{N} + \vec{h}$. The instance $S(\vec{i})$ reads or writes the cell $X[f(\vec{i})]$.

**Schedules.** A schedule gives each statement an affine map $\theta_S(\vec{i}) = \Theta_S \vec{i} + \Gamma_S \vec{N} + \vec{\gamma}_S \in \mathbb{Z}^m$. The machine runs the instances in increasing lexicographic order of their dates. Instances with equal dates may run in any order, or at the same time. The original program has the *2d+1 schedule*: interleave the loop indices with the textual position of each statement at each depth. For example, the schedule of a statement that is the second one inside the first loop of the program is $(0, i, 1)$.

**Dependences.** A pair of instances depends if both touch the same cell, at least one writes it, and the first comes first in the original schedule. For two references $f$ of $S$ and $g$ of $T$, the dependent pairs are

$$\mathcal{P}_{S,T} = \{\, (\vec{s}, \vec{t}) : \vec{s} \in \mathcal{D}_S,\ \vec{t} \in \mathcal{D}_T,\ f(\vec{s}) = g(\vec{t}),\ \theta^0_S(\vec{s}) \prec \theta^0_T(\vec{t}) \,\}.$$

The order $\prec$ is a disjunction (equal in the first $l - 1$ entries and smaller in entry $l$), so $\mathcal{P}_{S,T}$ is a union of polyhedra, one per level $l$. These are *dependence polyhedra*.

**Execution and equivalence.** A new schedule $\theta$ is *legal* if $\theta_S(\vec{s}) \prec \theta_T(\vec{t})$ for every dependent pair. Then every instance reads the same values as in the original order, by the reordering theorem on the [legality page](/loop-transformation-legality/). Code generation turns the domains and the new schedule back into loops that visit each instance once, in schedule order; see [polyhedral scanning](/polyhedral-scanning/).

**What falls outside.** Subscripts such as `A[B[i]]` or `A[i*j]`, loops with `while`, bounds that depend on data, pointers with unknown targets, and calls with unknown side effects are not affine. A compiler either leaves such code out of the SCoP, or treats it with over-approximations, which lose the exactness of the analysis.

## What it counts

The model is a representation, so it fixes what an analysis or a transformation can see and measure, not a single cost.

- **Instances, not statements.** Each dependence is known for each pair of instances, exactly, as a set of integer points. This is finer than a [distance vector](/dependence-distance-vector/) or a [direction vector](/dependence-direction-vector/), which summarize the set.
- **Size independent of the parameters.** A domain or a dependence polyhedron has as many constraints as the program text gives, whatever the value of $N$. The cost of the analysis depends on the number of statements, loops and references, not on the number of instances.
- **Quality of a schedule.** A schedule is judged by the number of sequential dimensions (each dimension that carries a dependence is a sequential loop), by which dimensions are parallel (no dependence carried there), by its latency (the number of distinct dates, which bounds the parallel time with unbounded processors), and by locality measures. Pluto, for example, bounds the dependence distance along each new dimension, which is a measure of reuse distance and of communication volume.
- **Cost of the operations.** The basic operations are tests of integer emptiness, projection, lexicographic minimum of integer points, and counting. Integer emptiness is integer linear programming, which is NP-complete in general but polynomial when the dimension is fixed. [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) can make the number of constraints grow doubly exponentially in the number of eliminated variables. In practice the dimensions are small (the depth of a loop nest), so these operations are fast enough.

A legal schedule is only a correct one. It can be slower than the original program, for example if it makes the inner loop jump through memory, or adds loops with large overhead. The objective functions of polyhedral schedulers are heuristics for speed, not proofs of it.

## Relation to other models

- **Dependence abstractions.** Distance vectors, direction vectors and dependence levels are summaries of dependence polyhedra. The [Allen-Kennedy algorithm](/allen-kennedy-algorithm/) uses levels only, and the [unimodular transformations](/unimodular-transformations/) of a perfect nest use distance or direction vectors. A unimodular transformation is the special case of an affine schedule in which every statement gets the same square unimodular matrix $\Theta$, without the constant parts.
- **Uniform recurrence equations.** Karp, Miller and Winograd studied computations on the lattice points of a region in which each value depends on values at constant offsets. This is the case of the polyhedral model where every dependence has a constant distance. Their schedules, and the hyperplane method of Lamport for loops, are one-dimensional affine schedules of this case.
- **Presburger arithmetic.** Sets of integer points defined by affine constraints with existential quantifiers, unions and differences can all be written in [Presburger arithmetic](/presburger-arithmetic/). Tools such as the [Omega test](/omega-test/) and isl work with these Presburger sets. They are closed under projection, union and difference, while the integer points of a single polyhedron are not.
- **Abstract interpretation.** The [polyhedra domain](/polyhedra-domain/) of abstract interpretation also uses convex polyhedra, but as over-approximations of the values of variables. The polyhedral model uses them to describe exactly the instances of a program whose control does not depend on data.
- **Work and span.** A schedule with one dimension and latency $L$ runs the program in $L$ parallel steps with unbounded processors. So $L$ is at least the length of the longest chain of dependences, which is the span of the computation in the [work-span model](/work-span-model/).

## Known results in the model

- **Exact array dataflow.** For a static control program, the source of each read (the last instance that wrote the cell before the read) is a piecewise affine function of the instance and the parameters, given by a quasi-affine selection tree. Feautrier computes it with parametric integer programming; see [array dataflow analysis](/feautrier-array-dataflow/).
- **Linear legality.** The condition that $\theta_T(\vec{t}) - \theta_S(\vec{s}) \ge 1$ for all points of a dependence polyhedron is an infinite set of constraints. The affine form of [Farkas' lemma](/farkas-lemma/) turns it into a finite set of linear equalities on the coefficients of the schedule and on new nonnegative multipliers. So the search for a one-dimensional affine schedule is a linear program; see the [affine scheduling problem](/affine-scheduling-problem/).
- **Existence of schedules.** A one-dimensional affine schedule may not exist. A loop nest whose instances form one chain of $N^2$ dependent steps, such as a running sum over a square array, has latency $N^2$, and no affine function of the instance can give that latency with coefficients that do not depend on $N$. A multidimensional affine schedule always exists for a static control program: the 2d+1 schedule of the original order is one. Feautrier's greedy method builds one in which each dimension satisfies as many dependences as it can; see [Feautrier scheduling](/feautrier-scheduling/).
- **Code generation.** The integer points of a union of parameterized polyhedra can be scanned in lexicographic order by loops whose bounds come from [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) (Ancourt and Irigoin, 1991). Quilleré, Rajopadhye and Wilde (2000) and Bastoul's CLooG (2004) separate the domains of several statements to avoid guards in the loop bodies; see [polyhedral scanning](/polyhedral-scanning/).
- **Tiling for locality and parallelism.** The tiling hyperplanes of the [Pluto algorithm](/pluto-algorithm/) are found one at a time by a lexicographic minimum of an integer program that bounds the dependence distances, and they give tileable bands with outer parallel or pipelined loops.
- **Counting.** The number of instances of a statement, of distinct cells touched, or of cache misses in some models, is the number of integer points of a parametric polyhedron. Barvinok's algorithm counts the integer points of a polyhedron of fixed dimension in polynomial time, and its parametric form gives the count as a piecewise quasi-polynomial in the parameters; see the [Barvinok algorithm](/barvinok-algorithm/).

**Example.** Take the triangular matrix-vector product

```
for i = 0 to N-1:
  S1: y[i] = 0
  for j = 0 to i:
    S2: y[i] = y[i] + L[i][j] * x[j]
```

The domains are $\mathcal{D}_{S1} = \{ S1[i] : 0 \le i \le N - 1 \}$ and $\mathcal{D}_{S2} = \{ S2[i, j] : 0 \le i \le N - 1,\ 0 \le j \le i \}$, with $N$ and $N(N + 1)/2$ points. The original schedules, without the constant first entry of the 2d+1 form, are $\theta^0_{S1}(i) = (i, 0, 0)$ and $\theta^0_{S2}(i, j) = (i, 1, j)$. The write of $y[i]$ by $S_2$ and its read by a later $S_2$ give the dependence polyhedron $\{ (S2[i, j], S2[i', j']) : i' = i,\ 0 \le j < j' \le i \le N - 1 \}$ of all memory-based flow dependences. The value that $S2[i, j']$ reads comes only from $S2[i, j' - 1]$ for $j' \ge 1$, and from $S1[i]$ for $j' = 0$; that is the exact dataflow. The schedule $\theta_{S1}(i) = (0, i)$ and $\theta_{S2}(i, j) = (j + 1, i)$ is also legal: it initializes all of $y$ first, then runs the $j$ loop outside, and the inner loop over $i$ (from $j$ to $N - 1$) is parallel.

## References
