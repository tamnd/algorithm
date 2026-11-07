---
tag: WM6YPR
kind: problem
slug: linear-diophantine-system
name: Linear Diophantine system
aliases: [integer linear system, system of linear Diophantine equations, integer solution of a linear system]
area: algebra/exact-linear-algebra
level: advanced
summary: Find integer vectors x satisfying Ax = b, or decide that none exist.
prereqs: [linear-diophantine-equation, unimodular-matrix, smith-normal-form]
see_also: [hermite-normal-form, kannan-bachem-algorithm, nullspace-computation, bezouts-identity, chinese-remainder-theorem, closest-vector-problem, dixon-p-adic-lifting, lll-algorithm]
sources:
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Section 4.1, The Hermite normal form (Corollary 4.1a, the integer analogue of the Farkas lemma), and Chapter 5, Algorithms for linear diophantine equations (polynomial-time solution and the size of the solutions)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer
    locator: Section 2.4.3, Applications of the Hermite normal form, and Section 2.4.4, The Smith normal form and applications
  - paper: doi:10.1137/0208040
    title: Ravindran Kannan and Achim Bachem, Polynomial algorithms for computing the Smith and Hermite normal forms of an integer matrix, SIAM Journal on Computing 8(4), 1979
    locator: pp. 499 to 507 (polynomial-time Hermite and Smith forms, and with them the general solution of a linear Diophantine system)
  - paper: doi:10.1098/rstl.1861.0016
    title: Henry J. S. Smith, On systems of linear indeterminate equations and congruences, Philosophical Transactions of the Royal Society of London 151, 1861
    locator: pp. 293 to 326 (the solvability of systems of linear indeterminate equations through the invariant factors)
---

A linear Diophantine system asks, for an integer matrix $A$ and an integer vector $c$, for all integer vectors $x$ with $A x = c$, or for a proof that there are none. The solution set, when it is not empty, is a particular solution plus the lattice of integer solutions of $A x = 0$. Solving over $\mathbb{Q}$ is not enough: a system can have rational solutions and no integer one. The [Smith](/smith-normal-form/) or [Hermite normal form](/hermite-normal-form/) solves the problem in polynomial time.

## In plain words

You have several linear equations with whole-number coefficients, and you want whole-number answers only. A single equation such as $6 x + 10 y = 3$ already shows the difficulty: there are fraction answers, but every whole-number choice gives an even left side, so there is no whole-number answer.

The method changes variables with whole-number moves that can be undone, until the equations are separate: each new equation involves one new variable times one number. Then each one is solvable exactly when that number divides the right side, and the free variables describe all the answers.

## Definition

**Notation.** $A$ is an $m \times n$ matrix over $\mathbb{Z}$ of rank $r$, and $c \in \mathbb{Z}^m$. $b$ is the maximum binary length of an entry of $A$ and $c$. $\Lambda = \{x \in \mathbb{Z}^n : A x = 0\}$ is the integer kernel, a [lattice](/lattice/) of rank $n - r$.

**Input.** $A$ and $c$.

**Output.** Either a vector $x_0 \in \mathbb{Z}^n$ with $A x_0 = c$ and a basis $k_1, \ldots, k_{n - r}$ of $\Lambda$, so that the solutions are exactly $x_0 + \mathbb{Z} k_1 + \cdots + \mathbb{Z} k_{n - r}$; or the answer "no integer solution", with a certificate.

**Solvability through the Smith form.** Let $U A V = S = \operatorname{diag}(s_1, \ldots, s_r, 0, \ldots, 0)$ with [unimodular](/unimodular-matrix/) $U$, $V$. Substitute $x = V y$, which is a bijection of $\mathbb{Z}^n$, and multiply by $U$, which is a bijection of $\mathbb{Z}^m$. The system becomes $S y = U c$, that is

$$s_i y_i = (U c)_i \quad (1 \le i \le r), \qquad 0 = (U c)_i \quad (r < i \le m).$$

So $A x = c$ has an integer solution if and only if $s_i \mid (U c)_i$ for $i \le r$ and $(U c)_i = 0$ for $i > r$. Then $y_i = (U c)_i / s_i$ for $i \le r$, $y_{r+1}, \ldots, y_n$ are free, $x_0 = V (y_1, \ldots, y_r, 0, \ldots, 0)^T$, and the last $n - r$ columns of $V$ are a basis of $\Lambda$.

**Theorem (integer Farkas lemma).** $A x = c$ has no integer solution if and only if there is a rational vector $y$ with $y^T A \in \mathbb{Z}^n$ and $y^T c \notin \mathbb{Z}$.

*Proof.* If $x$ is an integer solution and $y^T A$ is integral, then $y^T c = (y^T A) x \in \mathbb{Z}$. Conversely, suppose there is no integer solution, and let $u_i^T$ be row $i$ of $U$. Since $U A = S V^{-1}$, row $i$ of $U A$ is $s_i$ times row $i$ of $V^{-1}$ for $i \le r$, and zero for $i > r$. Case 1: $(U c)_i \ne 0$ for some $i > r$. Then $u_i^T A = 0$, and $y = u_i / (2 (U c)_i)$ gives $y^T A = 0$ and $y^T c = \tfrac12$. Case 2: otherwise $s_i \nmid (U c)_i$ for some $i \le r$. Then $y = u_i / s_i$ gives $y^T A$ equal to row $i$ of $V^{-1}$, which is integral because $V$ is unimodular, and $y^T c = (U c)_i / s_i \notin \mathbb{Z}$. $\square$

The theorem is the analogue of the Farkas lemma of linear programming, and the vector $y$ is a short certificate of unsolvability.

## Variants

- **One equation.** $a_1 x_1 + \cdots + a_n x_n = c$ is solvable if and only if $\gcd(a_1, \ldots, a_n) \mid c$, by [Bezout's identity](/bezouts-identity/); see [linear Diophantine equation](/linear-diophantine-equation/).
- **Congruences.** A system $A x \equiv c \pmod N$ is the Diophantine system $A x + N z = c$ in more unknowns. Simultaneous congruences $x \equiv a_i \pmod {m_i}$, with the [Chinese remainder theorem](/chinese-remainder-theorem/) as the coprime case, are the special case with one unknown.
- **Nonnegative or bounded solutions.** With $x \ge 0$ the problem is integer programming with equality constraints, which is NP-complete; with a bound on $\|x\|$ it is close to the [closest vector problem](/closest-vector-problem/), which is NP-hard. The unconstrained problem is in polynomial time.
- **Small solutions.** Find a solution and a kernel basis with small entries, using the [LLL algorithm](/lll-algorithm/) on the kernel basis and size reduction of the particular solution.
- **Over other rings.** Over $K[x]$ or any Euclidean domain the same method applies with the Smith form over that ring.

## Examples

**Solvable.** Let $A = \begin{pmatrix} 6 & 4 \\ 4 & 6 \end{pmatrix}$, whose Smith form is $S = \operatorname{diag}(2, 10) = U A V$ with $U = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$, $V = \begin{pmatrix} 1 & -2 \\ -1 & 3 \end{pmatrix}$. For $c = (2, 8)$, $U c = (2, 10)$, so $y = (1, 1)$ and $x = V y = (-1, 2)$. Check: $6 \cdot (-1) + 4 \cdot 2 = 2$ and $4 \cdot (-1) + 6 \cdot 2 = 8$. Since $r = n$, the solution is unique.

**Rational but not integral.** For the same $A$ and $c = (2, 2)$, $U c = (2, 4)$, and $10 \nmid 4$, so there is no integer solution, although $x = (\tfrac15, \tfrac15)$ solves the system over $\mathbb{Q}$. The certificate is $y^T = u_2^T / 10 = (\tfrac1{10}, \tfrac1{10})$: $y^T A = (1, 1)$ is integral and $y^T c = \tfrac25$ is not.

**One equation, three unknowns.** $6 x + 10 y + 15 z = 1$ has the solution $(1, 1, -1)$, since $\gcd(6, 10, 15) = 1$. The solutions form $(1, 1, -1) + \Lambda$, where $\Lambda$ is the rank $2$ lattice of integer solutions of $6 x + 10 y + 15 z = 0$, with basis $(5, -3, 0)$ and $(5, 0, -2)$.

**Edge cases.** With $n = 0$ the system is solvable exactly when $c = 0$. With $A = 0$ it is solvable exactly when $c = 0$, and then every $x \in \mathbb{Z}^n$ is a solution.

## Known algorithms

- **Smith normal form** with transforms, as in the definition; see [Smith normal form](/smith-normal-form/).
- **Column Hermite normal form.** Find unimodular $V$ with $A V = (H \mid 0)$, $H$ of full column rank $r$ in echelon form. Solve $H y' = c$ by forward substitution, checking at each step that the division is exact; the last $n - r$ columns of $V$ span $\Lambda$ (Cohen, Section 2.4.3). This is cheaper than the Smith form and is the usual method.
- **Polynomial time.** With the [Kannan-Bachem algorithm](/kannan-bachem-algorithm/) (1979) for the Hermite or Smith form, all numbers stay polynomially bounded, and the whole problem is solved in time polynomial in $m$, $n$ and $b$. Schrijver, Chapter 5, gives a direct polynomial-time method.
- **Lattice reduction** (Havas, Majewski and Matthews, 1998): extended gcd and Hermite form computations by LLL, which give much smaller solutions and kernel bases in practice.
- **Combining rational solutions.** Solve $A x = c$ over $\mathbb{Q}$ a few times, with [p-adic lifting](/dixon-p-adic-lifting/), for randomly perturbed systems, and combine the solutions with an integer combination whose denominators have gcd $1$. Mulders and Storjohann (2004) find and certify a solution this way at the cost of a few rational solves.

## Bounds

- **Complexity class.** The problem is in deterministic polynomial time (Kannan and Bachem, 1979). With $x \ge 0$ it is NP-complete even for one equation, which is a form of the subset sum problem.
- **Size of the solution.** If an integer solution exists, there is one whose entries have binary length bounded by a polynomial in $m$, $n$ and $b$, and the kernel lattice has a basis of polynomial size as well (Schrijver, Chapter 5). The proof goes through the Hermite normal form, whose entries are bounded by the [Hadamard bound](/hadamard-bound/) of the $r \times r$ minors.
- **Lower bound.** Reading the input costs $\Omega(m n)$, and no better general lower bound is known.

## Reductions

- **To normal forms.** Solving reduces to the Smith form or the column Hermite form with transform, as above.
- **To rational solving.** One rational solution and the [integer kernel](/nullspace-computation/) do not suffice by themselves, but a few rational solutions with coprime denominators do.
- **From congruences.** Systems of linear congruences, and with them the Chinese remainder problem with non-coprime moduli, are linear Diophantine systems.

## Applications

- **Lattice membership.** $c$ lies in the lattice spanned by the columns of $A$ if and only if $A x = c$ has an integer solution.
- **Integer programming.** Equality constraints $A x = c$ are removed by the substitution $x = x_0 + K z$ with $K$ a kernel basis, which leaves a problem in $n - r$ free integer variables.
- **Compilers.** Dependence tests for array accesses in loops ask whether linear Diophantine systems in the loop indices have solutions, starting with the gcd test for one equation.
- **Number theory and cryptanalysis.** Relations between logarithms in [index calculus](/index-calculus/), unit and class group computations, and the solution of knapsack-type congruences end with such systems.
- **Crystallography and combinatorics.** Integer relations among lattice vectors, and the balancing of reactions in integers.

## References
