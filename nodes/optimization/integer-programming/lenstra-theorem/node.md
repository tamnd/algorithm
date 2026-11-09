---
tag: GTWN3A
kind: theorem
slug: lenstra-theorem
name: Lenstra's theorem
aliases:
- fixed-dimension integer programming is polynomial
- Lenstra's fixed-dimension theorem
area: optimization/integer-programming
level: advanced
summary: Integer programming with a fixed number of variables is solvable in polynomial time.
prereqs: [lenstra-algorithm, lll-algorithm, integer-feasibility, polyhedron]
see_also: [integer-programming-fixed-dimension, kannan-algorithm, frank-tardos-algorithm, papadimitriou-pseudopolynomial-theorem, eisenbrand-weismantel-proximity-theorem, np-complete]
sources:
  - paper: doi:10.1287/moor.8.4.538
    title: H. W. Lenstra Jr., Integer programming with a fixed number of variables, Mathematics of Operations Research 8(4), 1983
    locator: pp. 538 to 548 (main theorem, and the extension to a fixed number of integer variables)
  - paper: doi:10.1007/BF01457454
    title: A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261, 1982
    locator: pp. 515 to 534 (polynomial running time of basis reduction)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 17 (sizes of integer solutions) and Chapter 18 (Lenstra's algorithm)
  - paper: "F. Eisenbrand, Integer programming and algorithmic geometry of numbers, in 50 Years of Integer Programming 1958 to 2008, Springer, 2010"
    locator: sections on the flatness theorem and Lenstra's algorithm
---

## Statement

**Theorem (Lenstra, 1983).** For each fixed $n$ there is an algorithm that, given $A \in \mathbb{Q}^{m \times n}$, $b \in \mathbb{Q}^m$ and $c \in \mathbb{Q}^n$, decides whether $\{x \in \mathbb{Z}^n : A x \le b\}$ is empty, and if it is not, either finds an integer point $x^*$ that maximizes $c^\top x$ over this set or shows that $c^\top x$ is unbounded on it. The running time is bounded by a polynomial in the size $s$ of the input in binary, and the degree of this polynomial does not depend on $n$; only the constant factor does.

In the usual form, the time is $2^{O(n^3)} s^{O(1)}$. The same holds for mixed integer programs in which only $n$ of the variables must be integer, and the others are free.

## In plain words

Deciding whether a system of linear inequalities has a whole-number solution is hard in general. But if the number of unknowns is fixed, for example five, the problem can be solved quickly, however many inequalities there are and however large the numbers in them are. The cost grows very fast with the number of unknowns, but for each fixed number it grows only like a power of the input length.

The reason is a fact about shapes: a shape that contains no whole-number point must be thin in some whole-number direction. So the search can always split into a small number of slices of lower dimension.

## Proof

The proof uses [Lenstra's algorithm](/lenstra-algorithm/) and four facts.

1. **Correctness and branching.** For a bounded rational polyhedron $P \subseteq \mathbb{R}^n$, the algorithm returns an integer point of $P$ or proves that none exists, and every call in dimension $k$ creates at most $k^2 2^{k/2} + 1$ calls in dimension $k - 1$. This is proved on the page of the algorithm, from the bound for LLL-reduced bases and the nearest plane method.
2. **Small solutions.** If $\{x \in \mathbb{Z}^n : Ax \le b\}$ is not empty, it contains a point whose size is polynomial in $s$, and if $c^\top x$ is bounded on it, the maximum is reached at such a point (Schrijver, Chapter 17).
3. **Basis reduction is polynomial.** LLL on a rational basis runs in time polynomial in the dimension and the size of the input, and the vectors it returns have polynomial size (LLL 1982).
4. **Sizes in the recursion.** In each call, the vertices, the rounding matrix, the reduced basis, the direction $d$ and the unimodular matrix $W$ have sizes bounded by a polynomial in the size of the input of the call, whose degree depends only on the dimension (Lenstra 1983; Schrijver, Chapter 18).

*Feasibility.* By fact 2, adding the box $|x_j| \le 2^{p(s)}$ for a suitable polynomial $p$ does not change whether an integer point exists, and the box adds numbers of polynomial size. The polyhedron is now bounded, and fact 1 shows that the algorithm decides feasibility.

*Time of one call.* A call with $m$ constraints in dimension $k$ solves at most $\binom{m}{k} \le m^k$ linear systems to find the vertices, compares at most $\binom{m^k}{k+1}$ simplices, and runs LLL and the nearest plane method once. For fixed $k$, this is a polynomial in $m$ and the size of the numbers, by fact 3. The subproblems have the same number $m$ of constraints.

*Whole recursion.* The recursion has depth $n$, and by fact 1 it has at most $\prod_{k=1}^{n} (k^2 2^{k/2} + 1)$ nodes, a number that depends only on $n$. By fact 4, the input size of a call at depth $i$ is at most $p_i(s)$, where $p_i$ is a composition of $i$ polynomials whose degrees depend only on $n$. A composition of $n$ polynomials is a polynomial, so all calls take time polynomial in $s$, and so does the whole recursion.

*Optimization.* First decide whether $\max\{c^\top x : A x \le b\}$ is unbounded with a linear programming algorithm. If an integer point exists and the linear program is unbounded, the integer program is unbounded too, because the [integer hull](/integer-hull/) of a rational polyhedron with an integer point has the same recession cone as the polyhedron (Schrijver, Chapter 16). Otherwise, by fact 2, the optimal value is a rational number of polynomial size, and a binary search over the values of polynomial size, with the extra constraint $c^\top x \ge t$, finds it with polynomially many feasibility calls. Each call adds one constraint, which keeps the input size polynomial. $\blacksquare$

## Consequences

- **[Integer programming in fixed dimension](/integer-programming-fixed-dimension/)** is in polynomial time, for feasibility and for optimization.
- **Mixed integer programs with few integer variables.** Lenstra's paper extends the method to programs in which only $n$ variables must be integer and the number of continuous variables is arbitrary.
- **The flatness principle.** The proof shows that a convex body without integer points has small lattice width in some integer direction. This principle is the base of the later algorithms of [Kannan](/kannan-algorithm/), Dadush, and Reis and Rothvoss.
- **Small numbers.** Combined with the [Frank-Tardos algorithm](/frank-tardos-algorithm/), the size of the objective can be replaced by a size that depends only on $n$ and the range of the variables.

## Tightness

- **The dimension cannot be part of the input.** [Integer feasibility](/integer-feasibility/) is [NP-complete](/np-complete/) when $n$ is part of the input, even for $0/1$ variables. So a running time polynomial in both $n$ and $s$ would give $\mathrm{P} = \mathrm{NP}$.
- **A fixed number of constraints is not enough.** With $m = 1$ and $n$ part of the input, the problem contains the [knapsack problem](/knapsack-problem/), which is NP-hard. With $m$ fixed and the numbers given in unary, [Papadimitriou's theorem](/papadimitriou-pseudopolynomial-theorem/) gives a pseudopolynomial algorithm instead.
- **The dependence on n.** The bound $2^{O(n^3)}$ from the first analyses has been improved to $n^{O(n)}$ by Kannan, to $2^{O(n)} n^n$ by Dadush, and to $(\log 2n)^{O(n)}$ by Reis and Rothvoss with a randomized algorithm. Whether $2^{O(n)}$ is possible is open.

## History

Lenstra proved the theorem in a paper that appeared in Mathematics of Operations Research in 1983. It was one of the first applications of the LLL basis reduction algorithm of 1982. Kannan improved the dependence on $n$ in 1987, and Frank and Tardos showed in the same year that the numbers in the algorithms can be kept small.

## References
