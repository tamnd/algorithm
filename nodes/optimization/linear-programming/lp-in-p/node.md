---
tag: 4T1B0W
kind: theorem
slug: lp-in-p
name: Linear programming is in P
aliases:
- Khachiyan's theorem
- polynomial solvability of linear programming
area: optimization/linear-programming
level: advanced
summary: Linear programs can be solved in polynomial time (Khachiyan, 1979).
prereqs: [linear-programming-problem, ellipsoid-method, strong-duality, hadamard-bound]
see_also: [ellipsoid-method, karmarkar-algorithm, interior-point-method, separation-oracle, klee-minty-cube, megiddo-fixed-dimension-lp, cramers-rule, farkas-lemma]
sources:
  - paper: doi:10.1016/0041-5553(80)90061-0
    title: L. G. Khachiyan, Polynomial algorithms in linear programming, USSR Computational Mathematics and Mathematical Physics 20(1), 1980
    locator: pages 53 to 72, the polynomial algorithm and its precision analysis
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Chapter 8, The ellipsoid method (volume reduction, the feasibility problem, the bounds on the size of basic solutions and the perturbation, and the optimization problem)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 10 (sizes of solutions and the complexity of linear programming) and Chapter 13 (Khachiyan's method for linear programming)
  - book: isbn:9783642782428
    title: Martin Grötschel, László Lovász and Alexander Schrijver, Geometric Algorithms and Combinatorial Optimization, second edition, Springer, 1993
    locator: Chapter 3, The ellipsoid method (the version with rounding and its precision analysis)
  - paper: doi:10.1287/opre.34.2.250
    title: Éva Tardos, A strongly polynomial algorithm to solve combinatorial linear programs, Operations Research 34(2), 1986
    locator: pages 250 to 256, running time independent of the sizes of b and c
  - paper: doi:10.1016/0020-0190(79)90152-2
    title: David Dobkin, Richard J. Lipton and Steven Reiss, Linear programming is log-space hard for P, Information Processing Letters 8(2), 1979
    locator: pages 96 to 97, the hardness under log-space reductions
---

The theorem that linear programming is in P says that a linear program with integer data can be solved in time polynomial in the number of bits of its data. Khachiyan proved it in 1979 with the [ellipsoid method](/ellipsoid-method/), and it settled a question that the exponential worst case of the [simplex method](/simplex-method/) on the [Klee-Minty cube](/klee-minty-cube/) had left open. The proof combines three facts: the vertices of a polyhedron have small rational coordinates, a perturbation turns an empty or nonempty system into one of tiny or not tiny volume, and the ellipsoid method tells these two cases apart in polynomially many steps. [Karmarkar's algorithm](/karmarkar-algorithm/) and other [interior-point methods](/interior-point-method/) give a second, practical proof.

## Statement

Let $A \in \mathbb{Z}^{m \times n}$, $b \in \mathbb{Z}^m$ and $c \in \mathbb{Z}^n$, and let $L$ be the encoding size of the data:
$$L = mn + m + n + \sum_{i,j} \lceil \log_2(|a_{ij}| + 1) \rceil + \sum_i \lceil \log_2(|b_i| + 1) \rceil + \sum_j \lceil \log_2(|c_j| + 1) \rceil.$$

**Theorem (Khachiyan, 1979).** There is an algorithm that, in time polynomial in $L$ on a Turing machine, decides whether the program maximize $c^\top x$ subject to $Ax \le b$ is infeasible, unbounded or has an optimum, and in the last case returns a rational optimal solution.

The bound counts bit operations, so it depends on the sizes of the numbers, not only on $m$ and $n$. Whether there is a *strongly polynomial* algorithm, with a number of arithmetic operations polynomial in $m$ and $n$ alone, is open.

## In plain words

A linear program asks for the best point in a region bounded by flat walls. The simplex method walks along the edges of the region, and on some regions the walk is exponentially long. The question was whether any method is fast on every program, where fast means a time that grows like a fixed power of the length of the input.

Khachiyan showed that the answer is yes. His method does not walk on the region. It traps the region inside an egg shape and halves the egg again and again, keeping the half that can still contain the region, until the egg is too small to hold any region that has a point in it. Small numbers in the input mean that a region with a point is never too thin, so this happens quickly.

## Proof

Write $\operatorname{size}$ for encoding size as above. Call a square submatrix of $[\,A \mid b\,]$ or of $[\,A^\top \mid c\,]$ a *subdeterminant* of the data.

**Lemma 1 (subdeterminants).** Every subdeterminant $D$ of the data has $|D| \le 2^L$.

*Proof.* By the [Hadamard bound](/hadamard-bound/), $|\det M| \le \prod_i \|M_i\|_2$ over the rows of $M$. Since $\|M_i\|_2 \le \sum_j |m_{ij}| \le \prod_j (1 + |m_{ij}|)$, we get $|\det M| \le \prod (1 + |m_{ij}|)$ over all entries of $M$, and each factor is at most $2^{\lceil \log_2(1 + |m_{ij}|) \rceil}$. Each entry of the data appears at most once in $M$, so $|\det M| \le 2^L$. $\square$

**Lemma 2 (small solutions).** If $P = \{x : Ax \le b\}$ is nonempty, it contains a point $x^0$ with $|x^0_j| \le 2^L$ for all $j$.

*Proof.* Write $x = x^+ - x^-$ and add slacks: $P$ is nonempty exactly when $\{(x^+, x^-, s) \ge 0 : Ax^+ - Ax^- + s = b\}$ is nonempty. A nonempty polyhedron in standard form has a [basic feasible solution](/basic-feasible-solution/). By [Cramer's rule](/cramers-rule/) its nonzero entries are quotients $D_1/D_2$ of determinants of square submatrices of $[\,A \mid -A \mid I \mid b\,]$ with $D_2 \ne 0$. A submatrix that uses both a column of $A$ and the same column of $-A$ is singular, and a unit column only removes a row from the expansion, so $|D_1| \le 2^L$ by Lemma 1, and $|D_2| \ge 1$ since it is a nonzero integer. So the point $x^0 = x^+ - x^-$ has $|x^0_j| \le 2^L$. $\square$

**Lemma 3 (perturbation).** Let $\varepsilon = 2^{-2L}$ and let $\mathbf{1}$ be the all-ones vector. Then $Ax \le b$ is feasible if and only if $Ax \le b + \varepsilon \mathbf{1}$ is feasible. If it is feasible, then $P_\varepsilon = \{x : Ax \le b + \varepsilon\mathbf{1},\ |x_j| \le 2^L + 1\}$ contains a cube of side $2\rho$ with $\rho = \varepsilon / (n 2^L)$.

*Proof.* If $Ax \le b$ is infeasible, the [Farkas lemma](/farkas-lemma/) gives $y \ge 0$ with $A^\top y = 0$ and $b^\top y < 0$. Scale to $b^\top y = -1$ and take $y$ a basic feasible solution of $\{y \ge 0 : A^\top y = 0,\ b^\top y = -1\}$; by Cramer's rule and Lemma 1 every $y_i \le 2^L$. Then $y^\top (b + \varepsilon \mathbf{1}) \le -1 + \varepsilon m 2^L < 0$, while $y^\top A x = 0$ for every $x$, so $Ax \le b + \varepsilon\mathbf{1}$ is infeasible too. If $Ax \le b$ is feasible, take $x^0$ from Lemma 2. For $\|x - x^0\|_\infty \le \rho$, $a_i^\top x \le b_i + \rho \sum_j |a_{ij}| \le b_i + \rho\, n 2^L = b_i + \varepsilon$, and $|x_j| \le 2^L + 1$. $\square$

**Feasibility in polynomial time.** Run the ellipsoid method on $P_\varepsilon$ from the ball of radius $R = \sqrt{n}\,(2^L + 1)$ around $0$, which contains $P_\varepsilon$. The separation step checks the $m + 2n$ inequalities in $O(mn)$ operations. Each step multiplies the volume of the ellipsoid by at most $e^{-1/(2(n+1))}$. After
$$N = \lceil 2n(n+1) \ln(R/\rho) \rceil + 1 = O(n^2 L)$$
steps the volume is below that of a cube of side $2\rho$, since $\ln(R/\rho) = O(L)$. So: if some center satisfies $Ax \le b + \varepsilon\mathbf{1}$, the system $Ax \le b$ is feasible by Lemma 3; if no center does in $N$ steps, $P_\varepsilon$ contains no such cube, and $Ax \le b$ is infeasible. The perturbed system has encoding size $O(L)$ after multiplication by $2^{2L}$. The exact ellipsoid needs square roots, but Khachiyan showed (see Grötschel, Lovász and Schrijver, Chapter 3) that rounding every number to $O(nL)$ bits and enlarging the ellipsoid by a factor slightly above $1$ at each step keeps the volume argument valid. So feasibility is decided in time polynomial in $L$.

**Optimization from feasibility.** By [strong duality](/strong-duality/), the program has an optimum if and only if the system
$$Ax \le b, \qquad A^\top y = c, \qquad y \ge 0, \qquad c^\top x \ge b^\top y$$
is feasible, and then the $x$ part of every solution is optimal. If this system is infeasible, decide feasibility of $Ax \le b$: if it is infeasible, so is the program; if it is feasible, the dual is infeasible (otherwise both would be feasible and an optimum would exist), so the program is unbounded. All these systems have encoding size $O(L)$.

**A solution from the decision.** Given a feasible system $Ax \le b$ (the combined system above, in this form), go through the rows $i = 1, \ldots, m$, and turn row $i$ into an equality $a_i^\top x = b_i$ if the system stays feasible. Let $I$ be the set of rows turned into equalities and $F = \{x : Ax \le b,\ a_I x = b_I\} \ne \emptyset$. Every row $j \notin I$ has $a_j^\top x < b_j$ on $F$, since $F$ only shrank after the test of $j$. Then $F = \{x : a_I x = b_I\}$: if some $z$ with $a_I z = b_I$ were outside $F$, the segment from a point of $F$ to $z$ would leave $F$ at a point of $F$ where some row $j \notin I$ is tight. So any solution of the linear equations $a_I x = b_I$, found by Gaussian elimination with [integer-preserving pivoting](/bareiss-algorithm/) in polynomial time, is a feasible point. This uses $m + 1$ feasibility tests, each polynomial. $\blacksquare$

## Consequences

- **The complexity of LP.** Linear programming is in P, while integer programming is NP-hard. LP is also P-complete: Dobkin, Lipton and Reiss (1979) showed that every problem in P reduces to LP in logarithmic space, so a fast parallel algorithm for LP is unlikely.
- **Implicit programs.** The ellipsoid method needs only a [separation oracle](/separation-oracle/), so the same proof shows that programs with exponentially many constraints, such as the matching and subtour programs, are solvable in polynomial time when their separation problem is.
- **Strongly polynomial cases.** Tardos (1986) gave an algorithm whose number of arithmetic operations is polynomial in the size of $A$ alone, independent of $b$ and $c$. So programs with small integer matrices, such as flow and transportation problems, are strongly polynomial. In fixed dimension, [Megiddo's algorithm](/megiddo-fixed-dimension-lp/) is linear in $m$.
- **Practical polynomial methods.** [Karmarkar's algorithm](/karmarkar-algorithm/) (1984) and later path-following [interior-point methods](/interior-point-method/) need $O(nL)$ and $O(\sqrt{n}\,L)$ iterations and are fast in practice, unlike the ellipsoid method.

## Tightness

- **The bits are needed.** The vertices of a polyhedron can need $\Theta(L)$ bits. The system $x_1 \le 2$, $x_{i+1} \le 2x_i$ for $i < n$, with the objective maximize $x_n$, has encoding size $O(n)$ and the optimum $x_n = 2^n$, which has $n + 1$ bits. So the time cannot be bounded by a polynomial in $m$ and $n$ that ignores how the numbers are written; it can only count arithmetic operations, which is the open strongly polynomial question.
- **The simplex method does not give the theorem.** With the classical pivot rules the simplex method needs exponentially many pivots on the [Klee-Minty cube](/klee-minty-cube/), even though each pivot is polynomial.
- **The ellipsoid method is not strongly polynomial.** Its number of iterations grows with $L$ even for fixed $m$ and $n$, because the volume bound depends on the sizes of the numbers.

## History

The ellipsoid method came from nonlinear optimization: Shor and, separately, Yudin and Nemirovski described it in the 1970s for convex programs. Khachiyan announced the polynomial bound for LP in a short note in Doklady in 1979 and gave the full proof in 1980. Gács and Lovász wrote out the details of the proof for the West in 1981, and the result was front-page news. Grötschel, Lovász and Schrijver (1981) then turned it into a general tool for combinatorial optimization through separation.

## References
