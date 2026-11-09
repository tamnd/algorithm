---
tag: E18YDV
kind: problem
slug: integer-programming-fixed-dimension
name: Integer programming in fixed dimension
aliases:
- fixed-dimension integer programming
- integer programming with a fixed number of variables
area: optimization/integer-programming
level: advanced
summary: Integer programming where the number of variables is a fixed constant.
prereqs: [integer-feasibility, mixed-integer-programming, lattice, polyhedron]
see_also: [lenstra-algorithm, kannan-algorithm, lenstra-theorem, frank-tardos-algorithm, papadimitriou-pseudopolynomial-theorem, barvinok-algorithm, fixed-parameter-tractable, land-doig-algorithm]
sources:
  - paper: doi:10.1287/moor.8.4.538
    title: H. W. Lenstra Jr., Integer programming with a fixed number of variables, Mathematics of Operations Research 8(4), 1983
    locator: pp. 538 to 548
  - paper: doi:10.1287/moor.12.3.415
    title: R. Kannan, Minkowski's convex body theorem and integer programming, Mathematics of Operations Research 12(3), 1987
    locator: pp. 415 to 440
  - paper: doi:10.1007/s10107-024-02084-1
    title: D. Dadush, F. Eisenbrand and T. Rothvoss, From approximate to exact integer programming, Mathematical Programming, 2024
    locator: introduction (history of running times)
  - paper: doi:10.1109/FOCS57990.2023.00060
    title: V. Reis and T. Rothvoss, The subspace flatness conjecture and faster integer programming, FOCS 2023
    locator: pp. 974 to 988 (main theorem)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 17 (sizes of solutions) and Chapter 18 (Lenstra's algorithm)
  - paper: doi:10.1287/moor.19.4.769
    title: A. I. Barvinok, A polynomial time algorithm for counting integral points in polyhedra when the dimension is fixed, Mathematics of Operations Research 19(4), 1994
    locator: main theorem (pp. 769 to 779, unsure)
---

Integer programming in fixed dimension asks for the best integer point of a [polyhedron](/polyhedron/) in $\mathbb{R}^n$, where $n$ is a constant and only the number of constraints and the size of the numbers grow. For each fixed $n$ the problem is solvable in polynomial time, by [Lenstra's theorem](/lenstra-theorem/), while [integer feasibility](/integer-feasibility/) with $n$ part of the input is [NP-complete](/np-complete/). The algorithms that solve it use lattices: they find a direction in which the polyhedron is thin and branch on the hyperplanes orthogonal to it.

## In plain words

Usually, finding a best whole-number solution of a system of inequalities is very hard. This problem keeps the number of unknowns fixed, say at three or ten, and lets the number of inequalities and the size of the numbers in them be as large as they like.

In this setting there is a fast method in theory. A shape with no whole-number point inside must be thin in some whole-number direction. So the method either finds a whole-number point near the middle of the shape, or it cuts the shape into a few parallel slices, each with one fewer unknown, and solves each slice in the same way.

## Definition

Fix $n \ge 1$. The input is $A \in \mathbb{Q}^{m \times n}$, $b \in \mathbb{Q}^m$ and $c \in \mathbb{Q}^n$, of total size $s$ in binary. The task is to solve
$$\max\{c^\top x : A x \le b,\ x \in \mathbb{Z}^n\},$$
that is, to report that no integer point satisfies $A x \le b$, or that $c^\top x$ is unbounded on these points, or to return an optimal integer point. The running time is measured as a function of $m$ and $s$, for each fixed $n$. The feasibility version only asks whether $\{x \in \mathbb{Z}^n : A x \le b\}$ is empty.

## Variants

- **Mixed integer programs with few integer variables.** Only $n$ variables must be integer, and any number of continuous variables are allowed. Lenstra's paper covers this case.
- **Parameterized form.** The time is written as $f(n) \cdot s^{O(1)}$, with $f$ independent of $s$. In this form the problem is [fixed-parameter tractable](/fixed-parameter-tractable/) in $n$, and the research goal is a small $f$.
- **Counting.** Count the integer points of a polyhedron of fixed dimension. The [Barvinok algorithm](/barvinok-algorithm/) does this in polynomial time for fixed $n$.
- **Fixed number of constraints.** Fixing $m$ instead of $n$ gives a different problem, with a pseudopolynomial algorithm by [Papadimitriou's theorem](/papadimitriou-pseudopolynomial-theorem/).

## Examples

**Dimension 1.** The constraints give an interval $[\ell, u]$. It has an integer point if and only if $\lceil \ell \rceil \le \lfloor u \rfloor$, and the optimum is at $\lceil \ell \rceil$ or $\lfloor u \rfloor$.

**A long thin strip.** For an integer $K \ge 1$ let
$$P_K = \{x \in \mathbb{R}^2 : 0 \le x_1, x_2 \le K,\ 1/3 \le x_1 - x_2 \le 2/3\}.$$
It has no integer point, since $x_1 - x_2$ is an integer at integer points. The direction $d = (1, -1)$ shows this at once, because no integer lies in $[1/3, 2/3]$. [Branch and bound](/land-doig-algorithm/) that branches on single variables needs at least $K + 1$ leaves. Each leaf is a box with integer bounds whose LP is empty, so the values of $x_1 - x_2$ on the box form an interval that avoids $[1/3, 2/3]$. If one box held two points $(i, i)$ and $(j, j)$ with $i < j$, it would also hold $(j, i)$ and $(i, j)$, with differences $j - i \ge 1$ and $i - j \le -1$, so the interval would meet $[1/3, 2/3]$. So the $K + 1$ points $(i, i)$ lie in different leaves.

**The strip from the algorithm page.** The strip $36/5 \le 3x_1 + 5x_2 \le 39/5$, $x \ge 0$ has no integer point. [Lenstra's algorithm](/lenstra-algorithm/) proves it with one hyperplane at each of two levels.

## Known algorithms

| algorithm | time for fixed $n$ | year | note |
|---|---|---|---|
| [Lenstra](/lenstra-algorithm/) | $2^{O(n^3)} s^{O(1)}$ | 1983 | LLL and rounding |
| [Kannan](/kannan-algorithm/) | $n^{O(n)} s^{O(1)}$ | 1987 | exact shortest vectors |
| Dadush | $2^{O(n)} n^n s^{O(1)}$ | 2012 | ellipsoid coverings |
| Reis and Rothvoss | $(\log 2n)^{O(n)} s^{O(1)}$ | 2023 | randomized; subspace flatness |

The running times are those given in the sources; the summary of Dadush, Eisenbrand and Rothvoss (2024) lists the same history. The [Frank-Tardos algorithm](/frank-tardos-algorithm/) is a preprocessing step that replaces the objective by one of polynomially bounded size with the same optimal solutions, which keeps the numbers in these algorithms small.

## Bounds

- **Polynomial for fixed n.** All the algorithms above run in time polynomial in $s$ for each fixed $n$.
- **Hardness in n.** With $n$ part of the input, integer feasibility is NP-complete even for $0/1$ variables, so no algorithm polynomial in both $n$ and $s$ exists unless $\mathrm{P} = \mathrm{NP}$.
- **Branches per level.** A polyhedron without integer points is thin in some integer direction. The LLL version of Lenstra's algorithm finds a direction with at most $n^2 2^{n/2} + 1$ hyperplanes, and the exact version of Kannan's algorithm one with at most $n^3$ hyperplanes, by the transference bound of Banaszczyk. Both bounds are proved on the algorithm pages.
- **Size of solutions.** If an integer point exists, one of size polynomial in $s$ exists, and the same holds for an optimal point of a bounded program (Schrijver, Chapter 17).

## Reductions

- **Optimization to feasibility.** A binary search on $t$ with the extra constraint $c^\top x \ge t$ needs a number of feasibility calls that is polynomial in $s$, by the bound on the size of an optimal point.
- **Unbounded to bounded.** Adding a box $|x_j| \le 2^{p(s)}$ for a suitable polynomial $p$ keeps an integer point if one exists. Unboundedness of the integer program is decided with the LP relaxation, because a rational polyhedron with an integer point has an integer hull with the same recession cone.
- **Equations.** If the system contains equations $C x = e$, the [Hermite normal form](/hermite-normal-form/) gives all integer solutions as $x = x_0 + U y$ with $y \in \mathbb{Z}^{n - r}$, where $r$ is the rank of $C$. This lowers the dimension.
- **From integer feasibility.** Every instance of integer feasibility with $n$ variables is an instance of this problem for that $n$; the restriction is only that $n$ is fixed.

## Applications

- **Parameterized algorithms.** Many problems have a formulation as an integer program whose number of variables depends only on a parameter $k$. Lenstra's algorithm then gives a fixed-parameter tractable algorithm in $k$.
- **Few types of objects.** Scheduling and packing problems with a constant number of distinct job or item types can be written with one integer variable per type or per configuration, which keeps $n$ small.
- **Lattice point questions.** Deciding whether a thin convex region contains an integer point, as in the examples above, is the basic step of algorithms for related lattice questions.

## References
