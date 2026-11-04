---
tag: KPZ1EJ
kind: model
slug: blum-shub-smale-machine
name: Blum-Shub-Smale machine
aliases:
- BSS machine
- real computation model
area: foundations/models-of-computation
level: research
summary: Machine whose registers hold elements of a ring such as the reals, with each arithmetic operation and test costing one step.
prereqs: [real-ram, turing-machine, np-complete]
see_also: [algebraic-computation-tree, hilbert-nullstellensatz, p, np, non-uniform-computation, unit-cost-model, quantifier-elimination, pspace]
sources:
  - paper: doi:10.1090/S0273-0979-1989-15750-9
    title: "Lenore Blum, Mike Shub and Steve Smale, On a theory of computation and complexity over the real numbers: NP-completeness, recursive functions and universal machines, Bulletin of the American Mathematical Society 21(1) (1989), 1 to 46"
    locator: the definition of the machine, the classes P and NP over R, the NP-completeness theorems, the universal machine and the Mandelbrot set
  - book: isbn:9780387982816
    title: "Lenore Blum, Felipe Cucker, Michael Shub and Steve Smale, Complexity and Real Computation, Springer (1998)"
    locator: Chapter 2, Definitions and First Properties of Computation; Chapter 3, Computation over a Ring; Chapter 4, Decision Problems and Complexity over a Ring; Chapter 5, The Class NP and NP-Complete Problems
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach, Cambridge University Press (2009)"
    locator: Chapter 16, Algebraic computation models, Section 16.3, The Blum-Shub-Smale Model
  - paper: doi:10.1016/S0747-7171(10)80003-3
    title: "James Renegar, On the computational complexity and geometry of the first-order theory of the reals, Part I, Journal of Symbolic Computation 13(3) (1992), 255 to 299"
    locator: the main theorem (the decision method and its bound on arithmetic operations)
  - paper: doi:10.1145/62212.62257
    title: "John F. Canny, Some algebraic and geometric computations in PSPACE, Proceedings of the 20th Annual ACM Symposium on Theory of Computing (STOC 1988), 460 to 469"
    locator: the existential theory of the reals is in PSPACE
  - paper: "arXiv:1912.02278"
    title: "Jeff Erickson, Ivor van der Hoog and Tillmann Miltzow, Smoothing the gap between NP and ER, full version of the paper in FOCS 2020 (doi:10.1109/FOCS46700.2020.00099)"
    locator: Section 2, the paragraph after Theorem 2 (the class ER and the Boolean part of NP over R without constants)
  - paper: doi:10.1016/0885-064X(92)90024-6
    title: "Felipe Cucker, P_R is not equal to NC_R, Journal of Complexity 8(3) (1992), 230 to 238"
    locator: the main theorem
  - paper: doi:10.1016/0885-064X(92)90007-X
    title: "Klaus Meer, A note on a P not equal to NP result for a restricted class of real machines, Journal of Complexity 8 (1992), 451 to 453"
    locator: the main theorem
  - paper: doi:10.1215/S0012-7094-95-08105-8
    title: "Michael Shub and Steve Smale, On the intractability of Hilbert's Nullstellensatz and an algebraic version of NP not equal to P?, Duke Mathematical Journal 81(1) (1995), 47 to 54"
    locator: the main theorem (the tau-conjecture implies that P is not NP over C)
---

A Blum-Shub-Smale machine (BSS machine) is a machine whose registers hold elements of a ring $R$, such as $\mathbb{R}$ or $\mathbb{C}$, with each arithmetic operation of $R$ and each test ($= 0$, or $\ge 0$ when $R$ is ordered) costing one step. Blum, Shub and Smale defined it in 1989 to give a theory of complexity for numerical problems, with the classes $\mathrm{P}_{\mathbb{R}}$ and $\mathrm{NP}_{\mathbb{R}}$ and a notion of [NP-completeness](/np-complete/) over $\mathbb{R}$. It is a formal model close to the [real RAM](/real-ram/), and it has a complexity theory of its own. Deciding whether a real polynomial of degree 4 has a real zero is $\mathrm{NP}_{\mathbb{R}}$-complete.

## The machine

Let $R$ be a ring. When $R$ is ordered, such as $\mathbb{R}$, the machine can test $x \ge 0$. Over a ring such as $\mathbb{C}$ it can only test $x = 0$. This page gives the machine in a simple form, close to the machines over $R^\infty$ of Blum, Cucker, Shub and Smale (1998, Chapters 2 and 3). The exact conventions differ between texts, for example in how the input size is given, but they give the same classes.

**State.** The state of the machine is a sequence $(x_k)_{k \in \mathbb{Z}}$ of elements of $R$, with only finitely many $x_k \ne 0$. Think of a tape that is infinite in both directions, with one element of $R$ in each cell. The machine computes only on the cells $x_1, \ldots, x_m$ near the origin, for a number $m$ fixed by the machine. To reach other cells it shifts the whole sequence.

**Input and size.** The input space is $R^\infty = \bigsqcup_{n \ge 0} R^n$. An input of **size** (dimension) $n$ is a vector $x = (x_1, \ldots, x_n) \in R^n$. The input node writes $x_1, \ldots, x_n$ into the cells $1, \ldots, n$, and it writes the size in unary: the cells $0, -1, \ldots, -(n-1)$ hold $1$, and all other cells hold $0$. The size must be part of the state, because a vector in $R^n$ may end with zeros. Without it, the inputs $(1, 1) \in \mathbb{R}^2$ and $(1, 1, 0) \in \mathbb{R}^3$ would give the same state.

**The program.** A machine is a finite directed graph with one input node and these other kinds of node.

- *Computation node.* It replaces $(x_1, \ldots, x_m)$ by $g(x_1, \ldots, x_m)$, where $g$ is a polynomial map with coefficients in $R$ (a rational map when $R$ is a field), and goes to its one successor. In a simple form, it does $x_i \leftarrow x_j \circ x_k$ with $\circ \in \{+, -, \times\}$ (and $\div$ in a field, by a non-zero element), or $x_i \leftarrow c$ for a constant $c \in R$, with $i, j, k \in \{1, \ldots, m\}$.
- *Branch node.* It has two exits. It tests $x_1 \ge 0$ in an ordered ring, or $x_1 = 0$ in general.
- *Shift node.* It shifts the whole sequence one place to the left ($x_k \leftarrow x_{k+1}$ for all $k$) or to the right ($x_k \leftarrow x_{k-1}$ for all $k$).
- *Output node.* It stops and gives an output. A machine that decides a set has two output nodes, *accept* and *reject*.

The machine has finitely many nodes, so it uses finitely many **constants**, the coefficients of its maps $g$. These can be any elements of $R$, such as $\pi$ in $\mathbb{R}$. The constants are part of the machine, and they are a main difference from a [Turing machine](/turing-machine/).

**Decision.** A machine **decides** a set $L \subseteq R^\infty$ if it halts on every input, and it accepts $x$ exactly when $x \in L$.

When $R = \mathbb{Z}_2$, the field with two elements, each cell holds a bit, and the machine is a model of classical Boolean computation. The theory then gives back the classical classes P and NP (Blum, Cucker, Shub and Smale 1998).

## What it counts

The **time** of a run is the number of nodes that the machine visits. Each node costs one step, whatever the values are. As in the [unit-cost model](/unit-cost-model/), a number is not charged for its size or its precision. The **cost function** of the machine is expressed in $n$, the dimension of the input, and not in a number of bits. So a time bound of $n^3$ means at most $n^3$ steps for each input in $R^n$. Bounds are for the worst case over $R^n$.

The model has no useful measure of space. One real number can encode an unbounded amount of information, for example a whole infinite bit sequence in its binary digits, so the number of cells in use says little. The theory studies time.

## Relation to other models

- **Real RAM.** The [real RAM](/real-ram/) is the programming model of computational geometry, with registers of exact reals, unit-cost operations, and integer registers for indirect addressing. The BSS machine has no integer registers. It reaches a cell by shifts, so to read cell $k$ it pays about $|k|$ steps, where a real RAM pays one step for an indexed access.
- **Turing machine.** Over $\mathbb{Z}_2$ the BSS machine gives the same classes as the [Turing machine](/turing-machine/). Over $\mathbb{R}$ the two are not comparable in a simple way: the BSS machine has exact real arithmetic at unit cost and real constants, but it has no access to the bits of a real.
- **Algebraic computation tree.** For each fixed $n$, the runs of a BSS machine over $\mathbb{R}$ with time at most $t$ on inputs in $\mathbb{R}^n$ unroll to an [algebraic computation tree](/algebraic-computation-tree/) of height at most $t$. The shifts only rename cells, so they add no node, and the constants of the machine become constants of the tree. So the tree lower bounds, such as $\Omega(n \log n)$ for [element distinctness](/element-distinctness/), are lower bounds on the running time of every BSS machine over $\mathbb{R}$ for these problems.
- **Non-uniform models.** The constants of a machine can act as advice, see [non-uniform computation](/non-uniform-computation/). The example below shows the effect.

## Known results in the model

**The classes.** A *decision problem over $R$* is a set $L \subseteq R^\infty$. Write $L_n = L \cap R^n$.

- $L \in \mathrm{P}_R$ if some BSS machine over $R$ decides $L$, and some polynomial $q$ bounds its time on every input in $R^n$ by $q(n)$.
- $L \in \mathrm{NP}_R$ if there are a BSS machine $M$ over $R$ and polynomials $p, q$ such that for each $n$ and each $x \in R^n$: $x \in L$ if and only if there is a **witness** $y \in R^{p(n)}$ such that $M$ accepts $(x, y)$ within time $q(n)$. The witness is a vector of ring elements, not a bit string.
- A **reduction** from $L$ to $L'$ is a function $f : R^\infty \to R^\infty$ that a machine computes in polynomial time, with $x \in L$ if and only if $f(x) \in L'$. A problem $L'$ is $\mathrm{NP}_R$-**complete** if $L' \in \mathrm{NP}_R$ and each problem in $\mathrm{NP}_R$ reduces to $L'$.
- $\mathrm{P}^0_R$ and $\mathrm{NP}^0_R$ are the same classes for machines whose only constants are $0$ and $1$.

Then $\mathrm{P}_R \subseteq \mathrm{NP}_R$, since a machine can ignore the witness. Whether $\mathrm{P}_R = \mathrm{NP}_R$ is open for $R = \mathbb{R}$ and for $R = \mathbb{C}$. See [P](/p/) and [NP](/np/) for the classical classes.

**Real constants are advice.** Take a set $S \subseteq \{1, 2, 3, \ldots\}$ and let $c_S = \sum_{i \in S} 4^{-i}$. The machine with the one constant $c_S$ decides the set $L_S = \{(1, 1, \ldots, 1) \in \mathbb{R}^n : n \in S\}$ in $O(n)$ steps. It shifts along the input and checks that each of $x_1, \ldots, x_n$ is $1$, and it finds $n$ by counting the cells of the unary size block. Then it sets $t \leftarrow c_S$ and does these steps for $j = 1, \ldots, n$: $t \leftarrow 4t$; if $t \ge 1$ then $b \leftarrow 1$ and $t \leftarrow t - 1$, else $b \leftarrow 0$. It accepts when the last value of $b$ is $1$. The reason is this invariant: before step $j$, $t = \sum_{i \in S, \, i \ge j} 4^{-(i-j+1)}$. For $j = 1$ this is $c_S$. After the multiplication by 4, $t$ equals $1$ if $j \in S$ (and $0$ otherwise) plus a remainder of at most $\sum_{k \ge 1} 4^{-k} = 1/3 < 1$. So $t \ge 1$ if and only if $j \in S$, and the subtraction keeps the invariant for $j + 1$. For example, $S = \{1, 3, 4, 6\}$ gives $c_S = 1105/4096$, and the values of $b$ for $j = 1, \ldots, 8$ are $1, 0, 1, 1, 0, 1, 0, 0$. If no Turing machine decides $S$, then no Turing machine decides the Boolean part $L_S \cap \{0,1\}^\infty = \{1^n : n \in S\}$, yet $L_S \in \mathrm{P}_{\mathbb{R}}$. So real constants give a non-uniform power.

**NP-completeness.** Let $\mathrm{HN}_R$ be this problem. The input is a list of polynomials $f_1, \ldots, f_m \in R[x_1, \ldots, x_n]$ in dense form, that is, as lists of coefficients, and the question is whether the $f_i$ have a common zero in $R^n$. Over $\mathbb{C}$ this is the feasibility form of [Hilbert's Nullstellensatz](/hilbert-nullstellensatz/): by the theorem, there is no common zero in $\mathbb{C}^n$ if and only if $1$ is in the ideal generated by the $f_i$. Over $\mathbb{R}$ that equivalence fails, since $x^2 + 1$ has no real zero and $1$ is not in the ideal $(x^2+1)$. Let $\text{4-FEAS}$ be the problem of whether one polynomial of degree at most $4$, in dense form, has a real zero.

> [!note]
> **Theorem (Blum, Shub and Smale, 1989).** The problem $\text{4-FEAS}$ over $\mathbb{R}$ is $\mathrm{NP}_{\mathbb{R}}$-complete. The problem $\mathrm{HN}_{\mathbb{R}}$ is $\mathrm{NP}_{\mathbb{R}}$-complete. The problem $\mathrm{HN}_{\mathbb{C}}$ is $\mathrm{NP}_{\mathbb{C}}$-complete.

*Proof for $\mathbb{R}$.*

1. *Membership in $\mathrm{NP}_{\mathbb{R}}$.* The witness is a point $y \in \mathbb{R}^n$. Evaluate each $f_i$ at $y$ from its coefficient list. Each monomial needs at most its degree many products, and the degree and the number of monomials are at most the length of the list, so this takes a number of steps polynomial in the size of the input. Accept if all values are $0$. The same argument puts $\text{4-FEAS}$ in $\mathrm{NP}_{\mathbb{R}}$.
2. *$\mathrm{HN}_{\mathbb{R}}$ reduces to $\text{4-FEAS}$.* First make each $f_i$ of degree at most 2. For a monomial $x_{i_1} x_{i_2} \cdots x_{i_d}$ with $d > 2$, add new unknowns $z_2, \ldots, z_d$ with the equations $z_2 - x_{i_1} x_{i_2} = 0$ and $z_j - z_{j-1} x_{i_j} = 0$ for $3 \le j \le d$, and replace the monomial by $z_d$. Each solution of the old system extends to exactly one solution of the new one, and the new system has polynomial size. Now let $F = \sum_i f_i^2$. Since each term is non-negative, $F(y) = 0$ exactly when every $f_i(y) = 0$. $F$ has degree at most 4, and its dense coefficient list has polynomial size. Conversely $\text{4-FEAS}$ is the case $m = 1$ of $\mathrm{HN}_{\mathbb{R}}$, so both are complete once one is.
3. *$\text{4-FEAS}$ is $\mathrm{NP}_{\mathbb{R}}$-hard.* Let $L \in \mathrm{NP}_{\mathbb{R}}$ with a machine $M$, a time bound $T = q(n)$ and a witness length $p = p(n)$. Fix an input $x \in \mathbb{R}^n$, and let $N = n + p$. At time $0$ the non-zero cells lie in $[-N + 1, N]$, a shift moves them by one place, and a computation node writes only cells $1, \ldots, m$. So for $t \le T$ all non-zero cells lie in $[-K, K]$ with $K = N + T + m$. Add to $M$ the rule that the two output nodes loop to themselves and change nothing, so that "accepts within $T$ steps" means "is at the accept node at time $T$". The unknowns are the witness $y \in \mathbb{R}^p$; the cell values $r_{t,k}$ for $0 \le t \le T$ and $-K \le k \le K$; an indicator $c_{t,v}$ for each time $t$ and node $v$; and the helpers $s_t, z_t, u_t, d_t$ for each $t$. The equations are these, where the equations that link time $t$ to time $t + 1$ are for $0 \le t < T$.
   - *Indicators.* $c_{t,v}(c_{t,v} - 1) = 0$ and $s_t(s_t - 1) = 0$, and $\sum_v c_{t,v} = 1$ for each $t$. So at each time exactly one node is marked.
   - *Start.* $c_{0,v_0} = 1$ for the node $v_0$ after the input node. $r_{0,k} = x_k$ for $1 \le k \le n$, $r_{0,n+k} = y_k$ for $1 \le k \le p$, $r_{0,k} = 1$ for $-N + 1 \le k \le 0$, and $r_{0,k} = 0$ for the other $k$.
   - *Computation node $v$ with map $g$ and successor $v'$.* $c_{t,v}(c_{t+1,v'} - 1) = 0$; $c_{t,v}(r_{t+1,i} - g_i(r_{t,1}, \ldots, r_{t,m})) = 0$ for $1 \le i \le m$; and $c_{t,v}(r_{t+1,k} - r_{t,k}) = 0$ for the other $k$. For a division $x_i \leftarrow x_j / x_k$ use $c_{t,v}(r_{t+1,i}\, r_{t,k} - r_{t,j}) = 0$ and $c_{t,v}(r_{t,k}\, d_t - 1) = 0$; the second equation forces $r_{t,k} \ne 0$.
   - *Shift node $v$ with successor $v'$, to the left.* $c_{t,v}(c_{t+1,v'} - 1) = 0$, $c_{t,v}(r_{t+1,k} - r_{t,k+1}) = 0$ for $-K \le k < K$, and $c_{t,v}\, r_{t+1,K} = 0$. A shift to the right is symmetric.
   - *Branch node $v$ with exits $v_1$ (when $x_1 \ge 0$) and $v_0'$.* $c_{t,v}(c_{t+1,v_1} - s_t) = 0$ and $c_{t,v}(c_{t+1,v_0'} - (1 - s_t)) = 0$. For the exit $v_1$, $c_{t,v}\, s_t\, (r_{t,1} - z_t^2) = 0$, which forces $r_{t,1} \ge 0$. For the exit $v_0'$, $c_{t,v}(1 - s_t)(r_{t,1} u_t^2 + 1) = 0$, which forces $r_{t,1} < 0$. The cells do not change: $c_{t,v}(r_{t+1,k} - r_{t,k}) = 0$ for every $k$.
   - *Output nodes.* For each output node $v$: $c_{t,v}(c_{t+1,v} - 1) = 0$ and $c_{t,v}(r_{t+1,k} - r_{t,k}) = 0$ for every $k$. Finally, $c_{T,\mathrm{acc}} = 1$.

   *Solutions are accepting runs.* Take a solution. By induction on $t$, the marked node at time $t$ and the values $r_{t,\cdot}$ are the node and the state of the run of $M$ on $(x, y)$ at time $t$. This holds at $t = 0$ by the start equations. If it holds at $t$, then only the equations of the marked node $v$ have $c_{t,v} = 1$, and they fix the node and the cells at time $t + 1$ as $M$ does. At a branch node the two inequalities forced by $z_t$ and $u_t$ make $s_t = 1$ exactly when $r_{t,1} \ge 0$. So $c_{T,\mathrm{acc}} = 1$ says that $M$ accepts $(x, y)$ within $T$ steps. Conversely, an accepting run gives a solution: set the indicators and the cells from the run, $s_t$ from the branch outcome, $z_t = \sqrt{r_{t,1}}$ when $r_{t,1} \ge 0$, $u_t = 1/\sqrt{-r_{t,1}}$ when $r_{t,1} < 0$, $d_t$ the inverse of the divisor, and the unused helpers $0$. So the system has a real solution if and only if some witness $y$ makes $M$ accept, that is, if and only if $x \in L$.

   The system has $O(T K)$ unknowns and equations, which is polynomial in $n$, and each equation has a degree bounded by a constant that depends only on $M$. Its coefficients are the entries of $x$, the constants of $M$, $0$ and $1$, so a machine with the constants of $M$ writes it in polynomial time. Step 2 then turns it into one polynomial of degree at most 4. This is a reduction from $L$ to $\text{4-FEAS}$.

The proof for $\mathbb{C}$ uses the same encoding of a run without the order: a branch tests $r = 0$, with the equations $c_{t,v}\, s_t\, r = 0$ and $c_{t,v}(1 - s_t)(r u_t - 1) = 0$, and the sum of squares is not available, so the result is a system of equations. That is why the complete problem over $\mathbb{C}$ is $\mathrm{HN}_{\mathbb{C}}$ and not one polynomial.

**Decidability.** Blum, Shub and Smale (1989) build universal machines and show that the halting problem for BSS machines over $\mathbb{R}$ is undecidable by a BSS machine. They also show that the Mandelbrot set is not decidable over $\mathbb{R}$ in this model.

**$\mathrm{NP}_{\mathbb{R}}$ is in exponential time.** Every problem in $\mathrm{NP}_{\mathbb{R}}$ is decidable, and $\mathrm{NP}_{\mathbb{R}} \subseteq \mathrm{EXP}_{\mathbb{R}}$. By the theorem above it is enough to decide $\text{4-FEAS}$. This is a sentence of the existential theory of the reals, which is decidable by the [quantifier elimination](/quantifier-elimination/) of Tarski. Renegar (1992) gives a decision method for $m$ polynomials of degree at most $d$ in $n$ unknowns with $(md)^{O(n)}$ arithmetic operations and tests, and it runs on a BSS machine. This is exponential in the size of the input.

**The link to Turing complexity.** The *Boolean part* of a class $C$ is $\mathrm{BP}(C) = \{L \cap \{0,1\}^\infty : L \in C\}$, read as a class of sets of bit strings. The Boolean part of $\mathrm{NP}^0_{\mathbb{R}}$ is the class $\exists\mathbb{R}$ of problems that reduce in polynomial time to the existential theory of the reals with integer coefficients (stated by Erickson, van der Hoog and Miltzow 2020, Section 2). It is known that $\mathrm{NP} \subseteq \exists\mathbb{R} \subseteq \mathrm{PSPACE}$; the second inclusion is the theorem of Canny (1988) that the existential theory of the reals is in [PSPACE](/pspace/). The constants matter here: the example above shows that $\mathrm{BP}(\mathrm{P}_{\mathbb{R}})$ already contains sets that no Turing machine decides.

**Separations in restricted settings.** Some separations are known.

- Cucker (1992) proved $\mathrm{NC}_{\mathbb{R}} \ne \mathrm{P}_{\mathbb{R}}$: some problem solvable in polynomial time over $\mathbb{R}$ has no algebraic circuits of polynomial size and polylogarithmic depth. Over the Booleans the question $\mathrm{NC} = \mathrm{P}$ is open.
- Meer (1992) proved $\mathrm{P} \ne \mathrm{NP}$ for real machines that can only add, subtract and test for equality.
- Shub and Smale (1995) showed that $\mathrm{P}_{\mathbb{C}} \ne \mathrm{NP}_{\mathbb{C}}$ follows from the $\tau$-conjecture, a statement about the number of integer roots of a univariate integer polynomial in terms of the size of the smallest straight-line program that computes it.

## References
