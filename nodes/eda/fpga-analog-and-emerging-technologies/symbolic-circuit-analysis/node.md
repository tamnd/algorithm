---
tag: RMKR18
kind: problem
slug: symbolic-circuit-analysis
name: Symbolic circuit analysis
aliases:
- symbolic analysis of analog circuits
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: Compute network functions of a linear or linearized circuit as expressions in the symbolic element values, to give designers insight into which parameters matter.
prereqs: [modified-nodal-analysis, determinant, cramers-rule, transfer-function]
see_also: [determinant-decision-diagram, approximate-symbolic-analysis, ac-small-signal-analysis, matrix-tree-theorem, signal-flow-graph, masons-gain-formula, laplace-expansion, analog-circuit-sizing]
sources:
  - paper: "Georges Gielen, Herman Walscharts and Willy Sansen, ISAAC: a symbolic simulator for analog integrated circuits, IEEE Journal of Solid-State Circuits 24(6), 1587 to 1597, 1989"
    title: G. Gielen, H. Walscharts and W. Sansen, ISAAC, a symbolic simulator for analog integrated circuits, IEEE Journal of Solid-State Circuits 24(6), 1587 to 1597, December 1989
    locator: the program ISAAC, its symbolic network functions in s and the element values, and the pruning of small terms
  - book: isbn:9780792391616
    title: Georges Gielen and Willy Sansen, Symbolic Analysis for Automated Design of Analog Integrated Circuits, Kluwer Academic Publishers, 1991
    locator: the chapters on the formulation of the circuit equations, the symbolic solution methods and the expanded and nested forms
  - paper: "Piet Wambacq, Georges Gielen and Willy Sansen, Symbolic network analysis methods for practical analog integrated circuits: a survey, IEEE Transactions on Circuits and Systems II 45(10), 1331 to 1341, 1998"
    title: P. Wambacq, G. Gielen and W. Sansen, Symbolic network analysis methods for practical analog integrated circuits, a survey, IEEE Transactions on Circuits and Systems II 45(10), 1331 to 1341, October 1998
    locator: the classes of exact methods (determinant, tree enumeration, signal-flow graph) and the growth of the number of terms
  - paper: "C.-J. Richard Shi and Xiang-Dong Tan, Canonical symbolic analysis of large analog circuits with determinant decision diagrams, IEEE Transactions on Computer-Aided Design 19(1), 1 to 18, 2000"
    title: C.-J. R. Shi and X.-D. Tan, Canonical symbolic analysis of large analog circuits with determinant decision diagrams, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 19(1), 1 to 18, January 2000
    locator: exact analysis of large circuits through a shared graph of the determinant
---

Symbolic circuit analysis is the problem of computing a [network function](/transfer-function/) of a linear circuit, for example a voltage gain, as a formula in the frequency variable $s$ and in the names of some or all element values, not as numbers. Its topic is symbolic circuit analysis, one of the five topics of this sub-area. The input is usually the small-signal circuit of an analog block at its operating point, and the formula tells a designer which elements set a gain, a pole or a zero. The hard part is size: the expanded formula can have a number of terms that grows exponentially with the circuit.

## In plain words

A circuit simulator answers with numbers: at this frequency, the gain is this much. A designer often wants to know why. Which transistor sets the gain? Which capacitor sets the bandwidth? A formula in the names of the parts answers these questions, because you can read which names appear and how.

Symbolic analysis produces such a formula. It writes the circuit equations with names in place of numbers and solves them by algebra. The answer is a fraction: a sum of products of names, divided by another sum of products.

For a small circuit the formula is short and useful. For a larger circuit the number of products explodes, and a full formula is too long to read. Exact methods store it in a compact shared form. Approximate methods keep only the products that matter.

## Definition

**Input.** A linear time-invariant circuit with $n$ nodes besides ground: resistors, capacitors, inductors and the four kinds of controlled sources, for example the small-signal model of an analog circuit. Each element value is a symbol or a number, and the set $X = \{x_1, \ldots, x_p\}$ holds the symbols. An input port and an output port (an independent source and a node voltage or branch current).

**Equations.** [Modified nodal analysis](/modified-nodal-analysis/) in the Laplace domain gives a square system

$$Y(s, X) \, v = b,$$

where each entry of $Y$ is a sum of terms $\pm x$, $\pm s x$ or $\pm x / s$, or of numbers times such terms. For a current $I$ that enters node $i$, $b = I e_i$. By [Cramer's rule](/cramers-rule/), the voltage of node $j$ gives

$$H(s, X) = \frac{v_j}{I} = \frac{C_{ij}(s, X)}{\det Y(s, X)},$$

where $C_{ij} = (-1)^{i+j} M_{ij}$ is the cofactor and $M_{ij}$ the minor of $Y$ without row $i$ and column $j$.

**Output.** The network function $H$ as a ratio of two polynomials in $s$ and $X$. In the expanded form, both are written as

$$N(s, X) = \sum_k s^k \sum_{t \in T_k} c_t \prod_{x \in t} x, \qquad D(s, X) = \sum_k s^k \sum_{t \in U_k} d_t \prod_{x \in t} x,$$

with numeric coefficients $c_t, d_t$, after all cancellations. The size of the output is the number of terms $\sum_k |T_k| + \sum_k |U_k|$.

**Objective.** Exact analysis must return $H$ exactly, in some agreed form. Approximate analysis must return a shorter $\hat H$ whose error is at most a given $\varepsilon$ at a given nominal point of the element values, with the error defined on the coefficients of each power of $s$ or on $|H(j\omega)|$ over a band.

## Variants

- **Fully symbolic or partly symbolic.** All element values are symbols, or only some, with numbers for the rest. In the limit, only $s$ is a symbol, and the output is a numeric rational function of $s$, which is the output of [AC small-signal analysis](/ac-small-signal-analysis/) in a closed form.
- **Expanded or nested form.** The expanded form is a flat sum of products, and the nested form keeps sums inside products, as in $(a + b)(c + d)$. A nested form can be exponentially shorter, but the reader cannot see the size of each term in it.
- **Exact or approximate.** See [approximate symbolic analysis](/approximate-symbolic-analysis/).
- **Element-level or entry-level symbols.** A symbol for each element value gives the formula a designer wants. A symbol for each entry of $Y$ gives a shorter determinant expansion, but each entry is a sum of element values, and the terms must then be expanded again.
- **Small-signal or large-signal.** The problem is defined for linear circuits. A nonlinear circuit is first linearized at an operating point, so the formula is valid only for small signals near that point.

## Examples

**A two-node amplifier.** Node 1 has a conductance $G_1$ to ground, and a current source $I$ drives it. A capacitor $C_f$ joins nodes 1 and 2. A transconductance $g_m$ draws the current $g_m v_1$ out of node 2, and a conductance $G_L$ joins node 2 to ground. This is the small-signal model of a common-source stage with a feedback capacitor. The nodal system is

$$\begin{pmatrix} G_1 + s C_f & -s C_f \\ g_m - s C_f & G_L + s C_f \end{pmatrix} \begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} I \\ 0 \end{pmatrix}.$$

The product of the diagonal gives $G_1 G_L$, $s C_f G_1$, $s C_f G_L$ and $s^2 C_f^2$. The off-diagonal entries give $+ s C_f g_m$ and $- s^2 C_f^2$, and the last one cancels $s^2 C_f^2$. So

$$H(s) = \frac{v_2}{I} = \frac{-(g_m - s C_f)}{G_1 G_L + s \, C_f (G_1 + G_L + g_m)}.$$

The formula shows at a glance what a simulation does not: a zero in the right half plane at $s = g_m / C_f$, and one pole whose time constant grows with $g_m$, which is the Miller effect. With $G_1 = 100\ \mu\mathrm{S}$, $G_L = 10\ \mu\mathrm{S}$, $g_m = 1\ \mathrm{mS}$ and $C_f = 1\ \mathrm{pF}$, the low-frequency value is $-g_m / (G_1 G_L) = -10^6\ \Omega$, the pole is at $-9.009 \times 10^5$ rad/s and the zero is at $10^9$ rad/s.

**A ladder.** A ladder of $n$ nodes has an admittance $y_i$ from each node $i$ to ground, and a conductance $g_i$ between nodes $i$ and $i + 1$. A current $I$ enters node 1, and the output is $v_n$. The cofactor is $g_1 g_2 \cdots g_{n-1}$, one term. The determinant, expanded in the element values, has $F_{2n}$ terms, where $F_k$ is the $k$-th [Fibonacci number](/fibonacci-numbers/):

| nodes $n$ | 1 | 2 | 3 | 5 | 10 | 20 |
|---|---|---|---|---|---|---|
| terms of $\det Y$ | 1 | 3 | 8 | 55 | 6,765 | 102,334,155 |

For $n = 2$, $\det Y = y_1 y_2 + y_1 g_1 + y_2 g_1$. If each $y_i = G_i + s C_i$ is also expanded, the counts for $n = 1$ to 5 are 2, 8, 30, 112 and 418.

## Known algorithms

- **Determinant expansion.** Expand $\det Y$ and $C_{ij}$ by [Laplace expansion](/laplace-expansion/) or by elimination. ISAAC (Gielen, Walscharts and Sansen 1989) used this kind of method on a nodal matrix and is exact, apart from its optional pruning. The time is at least the number of terms.
- **Tree enumeration.** For a circuit of admittances only, each term of $\det Y$ is a spanning tree of the circuit graph with ground (see the Bounds). Enumerating spanning trees gives the terms with no cancellation. Controlled sources need a pair of graphs, one for currents and one for voltages, and common trees of the two. Exact.
- **Signal-flow graphs.** Write the equations as a [signal-flow graph](/signal-flow-graph/) and apply [Mason's gain formula](/masons-gain-formula/), which sums over paths and sets of loops that do not touch. Exact, but the loop sums can produce terms that cancel.
- **[Determinant decision diagrams](/determinant-decision-diagram/)** (Shi and Tan 2000). Store the determinant and its cofactors as one shared graph, with one path for each term. Exact, and the graph can be exponentially smaller than the list of terms.
- **[Approximate symbolic analysis](/approximate-symbolic-analysis/).** Prune the circuit or the matrix before the expansion, prune the search during the expansion, or prune the terms after it, under an error bound at a nominal point. The result is short, and its error bound holds only at that point.

## Bounds

**Lower bound from the output size.** An algorithm that writes the expanded form needs time at least the number of terms. For the ladder, this number is $F_{2n} = \Theta(\varphi^{2n})$, with $\varphi^2 = (3 + \sqrt 5)/2 \approx 2.618$. So the expanded form of an exact answer takes exponential time and space on this family, whatever the method.

*Proof that the ladder has $F_{2n}$ terms.* The ladder is a circuit of admittances, so $Y$ is the weighted [Laplacian matrix](/laplacian-matrix/) of the circuit graph with the ground row and column removed. The circuit graph has the ground and $n$ nodes, edges $y_i$ from ground to each node, and edges $g_i$ between nodes $i$ and $i + 1$. By the weighted [matrix-tree theorem](/matrix-tree-theorem/), $\det Y$ is the sum, over all spanning trees of this graph, of the product of the weights of the tree's edges. Different trees have different edge sets, so with distinct symbols they give different monomials, each with coefficient $+1$, and nothing cancels. So the number of terms is the number of spanning trees, which is $\det Y$ with every weight equal to 1.

With weights 1, $Y$ is tridiagonal with $-1$ off the diagonal. For $n = 1$ it is $(1)$, with determinant $1 = F_2$. For $n \ge 2$ its diagonal is $(2, 3, \ldots, 3, 2)$. Let $P_k$ be the determinant of the $k \times k$ tridiagonal matrix with diagonal $(2, 3, \ldots, 3)$ and $-1$ off the diagonal. Expansion along the last row gives $P_k = 3 P_{k-1} - P_{k-2}$ for $k \ge 2$, with $P_0 = 1 = F_1$ and $P_1 = 2 = F_3$. The Fibonacci numbers satisfy $F_{m+2} = F_{m+1} + F_m = 2F_m + F_{m-1} = 3 F_m - F_{m-2}$, so $P_k = F_{2k+1}$ by induction. Expansion of $Y$ along its last row gives $\det Y = 2 P_{n-1} - P_{n-2} = 2F_{2n-1} - F_{2n-3} = F_{2n-1} + F_{2n-2} = F_{2n}$. $\square$

**What is polynomial.** The number of terms of an admittance-only circuit is a determinant with weights 1, so it can be counted in polynomial time by [Gaussian elimination](/gaussian-elimination/), without listing the terms. The value of $H$ at given numbers takes $O(n^3)$ arithmetic operations. A nested form exists with polynomial size: the steps of Gaussian elimination on the symbolic matrix, kept as a sequence of $O(n^3)$ expressions, compute $\det Y$ wherever no pivot is zero. A determinant decision diagram is also exact, but its size depends on the matrix and the order of its entries, and it is exponential for a dense matrix.

## Reductions

- **To determinants.** By Cramer's rule, a network function is a ratio of a cofactor and the determinant of the MNA matrix. Each is the determinant of a square matrix with polynomial entries. So exact symbolic analysis reduces to the symbolic [determinant](/determinant/) of a sparse matrix.
- **To spanning trees.** For a circuit of admittances, the determinant is the weighted spanning tree polynomial of the circuit graph, by the matrix-tree theorem. So exact analysis of such a circuit reduces to the enumeration of spanning trees.
- **From numeric AC analysis.** Numeric AC analysis at one frequency is the special case with no symbols, solved by sparse LU in place of expansion.

## Applications

- **Insight in design.** The formula shows which elements set the gain, the poles, the zeros and the rejection ratios of an amplifier, and how.
- **Equations for sizing.** Approximate symbolic formulas give fast models of the performance of a topology, which an [analog circuit sizing](/analog-circuit-sizing/) tool can evaluate many times.
- **Repeated evaluation.** A compiled exact formula or a determinant decision diagram evaluates the response for many values of the elements, for example in a Monte Carlo loop or a sensitivity analysis, without a new LU factorization each time.
- **Teaching and checking.** A short formula checks a hand analysis, and a hand analysis checks a simulator.

## References
