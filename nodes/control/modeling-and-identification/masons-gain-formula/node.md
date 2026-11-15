---
tag: D9D5KK
kind: theorem
slug: masons-gain-formula
name: Mason's gain formula
aliases:
- Mason's rule
area: control/modeling-and-identification
level: core
summary: The gain of a signal-flow graph from a source to a node equals the sum over forward paths of the path gain times the determinant of the loops off the path, divided by the graph determinant.
prereqs: [signal-flow-graph, determinant]
see_also: [signal-flow-graph, block-diagram-reduction, cramers-rule, gaussian-elimination, symbolic-circuit-analysis, matrix-tree-theorem, schur-complement, transfer-function]
sources:
  - paper: doi:10.1109/JRPROC.1956.275147
    title: Samuel J. Mason, Feedback theory, further properties of signal flow graphs, Proceedings of the IRE 44(7), 1956
    locator: pp. 920 to 926 (the general gain formula and its proof by the expansion of a determinant)
  - paper: doi:10.1109/JRPROC.1953.274449
    title: Samuel J. Mason, Feedback theory, some properties of signal flow graphs, Proceedings of the IRE 41(9), 1953
    locator: pp. 1144 to 1156 (the graphs, their node equations and their reduction rules)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 3.2.3, Mason's Rule and the Signal Flow Graph (an online section)
---

Mason's gain formula gives the gain from an input to an output of a linear [signal-flow graph](/signal-flow-graph/) directly from the drawing. One lists the forward paths from the input to the output, the loops, and which loops do not touch each other, and the formula combines their gains into one fraction. In control it turns a block diagram with several feedback loops into a [transfer function](/transfer-function/) in one step, and in circuit theory it gives transfer functions as formulas in the element values. The formula is a combinatorial form of [Cramer's rule](/cramers-rule/) for the node equations of the graph.

## Statement

**Setting.** A signal-flow graph has nodes $x_1, \dots, x_n$, one source node $u$ with no incoming edges, and a gain on each edge, with parallel edges merged. The node equations are $(I - W)x = b\,u$, where $w_{ij}$ is the gain of the edge $x_j \to x_i$ and $b_i$ the gain of the edge $u \to x_i$. A *loop* is a closed path with no repeated node, and two subgraphs *touch* if they have a common node. The *determinant* of a graph is

$$\Delta = 1 - \sum_a L_a + \sum_{a,b} L_a L_b - \sum_{a,b,c} L_a L_b L_c + \cdots,$$

where $L_a$ is the gain of loop $a$, and the $j$-th sum runs over the sets of $j$ loops that touch none of each other.

**Theorem (Mason, 1956).** If $\Delta \ne 0$, the gain from $u$ to a node $y = x_t$ is

$$T = \frac{y}{u} = \frac{1}{\Delta} \sum_k P_k\, \Delta_k,$$

where $P_k$ is the gain of the $k$-th forward path from $u$ to $y$, and $\Delta_k$ is the determinant of the graph that is left when the nodes of the $k$-th path are removed (so $\Delta_k$ uses only the loops that do not touch that path). Moreover $\Delta = \det(I - W)$.

## In plain words

Draw every route from the input to the output and multiply the gains along each route. Then look at the feedback loops. The bottom of the fraction starts at one, takes away each loop gain, adds back the product for each pair of loops that share no node, takes away the product for each such triple, and so on. Each route on top gets the same kind of correction, but only from the loops that do not cross that route. The answer is the corrected sum of the routes divided by the bottom. The bottom is the same for every output, and it is zero exactly when the equations of the graph have no unique solution.

## Proof

The proof has two claims. The first shows that the determinant of the graph is the matrix determinant. The second gets the gain from the first claim, applied to a larger graph.

**Claim 1.** $\det(I - W) = \sum_S (-1)^{|S|} \prod_{L \in S} \operatorname{gain}(L)$, where $S$ runs over the sets of pairwise disjoint loops, the empty set included. This sum is $\Delta$.

*Proof.* By the Leibniz formula, $\det(I - W) = \sum_\sigma \operatorname{sgn}(\sigma) \prod_i (I - W)_{i \sigma(i)}$ over the permutations $\sigma$ of $\{1, \dots, n\}$. For $\sigma(i) \ne i$ the factor is $-w_{i\sigma(i)}$. For $\sigma(i) = i$ the factor is $1 - w_{ii}$; expand it as the choice of $1$ or $-w_{ii}$. After the expansion, each term is fixed by $\sigma$ and a set $F$ of fixed points at which $-w_{ii}$ was chosen. Let $U$ be the set of points moved by $\sigma$, together with $F$, and $m = |U|$. The term is

$$\operatorname{sgn}(\sigma)\, (-1)^m \prod_{i \in U} w_{i\sigma(i)}.$$

The cycles of $\sigma$ on $U$, with the points of $F$ as cycles of length one, are disjoint. A cycle $i \mapsto \sigma(i) \mapsto \sigma^2(i) \mapsto \cdots$ uses the factors $w_{i\sigma(i)}, w_{\sigma(i)\sigma^2(i)}, \dots$, which are the gains of the edges $\sigma(i) \to i$, $\sigma^2(i) \to \sigma(i)$, and so on. So the product is not zero exactly when every cycle is a loop of the graph (read backward), and then the product is the product of the loop gains. Conversely, a set of disjoint loops gives exactly one pair $(\sigma, F)$. If the term has $c$ loops, $\operatorname{sgn}(\sigma) = (-1)^{m - c}$, because a cycle of length $\ell$ has sign $(-1)^{\ell - 1}$ and a cycle of length one has sign $+1$. The total sign is $(-1)^{m - c}(-1)^m = (-1)^c$. Summing over all terms gives the claim. $\square$

**Claim 2.** $\Delta\, T = \sum_k P_k \Delta_k$.

*Proof.* Make $u$ an ordinary node $x_0$ and add one edge $y \to x_0$ with a gain $g$, a free element of the field. The new graph has no source, and its matrix is

$$I - W' = \begin{pmatrix} 1 & -g\, e_t^{\mathsf T} \\ -b & I - W \end{pmatrix},$$

where $e_t$ is the $t$-th unit vector. Because $I - W$ is invertible, the [Schur complement](/schur-complement/) formula gives

$$\det(I - W') = \det(I - W)\,\bigl(1 - g\, e_t^{\mathsf T}(I - W)^{-1} b\bigr) = \Delta\,(1 - g\,T),$$

since $T = e_t^{\mathsf T}(I - W)^{-1} b$ is the $t$-th node value for $u = 1$.

Now compute the same determinant with Claim 1 on the new graph. The only edge into $x_0$ is $y \to x_0$. So a loop of the new graph either avoids $x_0$, and then it is a loop of the old graph, or it passes through $x_0$, and then it is a forward path $P_k$ from $u$ to $y$ closed by the edge $y \to x_0$, with gain $g P_k$. Two loops through $x_0$ touch, so a set of disjoint loops has at most one of them. The sets with none give $\Delta$. The sets with the loop $g P_k$ add to it any set of disjoint old loops that do not touch $P_k$, and they give $(-1)\, g P_k\, \Delta_k$. So

$$\det(I - W') = \Delta - g \sum_k P_k \Delta_k.$$

Both expressions are polynomials of degree at most one in $g$, and they are equal as polynomials, so the coefficients of $g$ agree: $\Delta T = \sum_k P_k \Delta_k$. $\square$

With $\Delta \ne 0$, Claim 2 gives the formula, and Claim 1 gives $\Delta = \det(I - W)$. This proves the theorem.

**A worked example.** Take the nodes $a, b, c, d$, the source $u$, and the edges $u \xrightarrow{1} a$, $a \xrightarrow{G_1} b$, $b \xrightarrow{-H_1} a$, $b \xrightarrow{G_2} c$, $c \xrightarrow{G_3} d$, $d \xrightarrow{-H_2} c$ and $u \xrightarrow{G_4} c$, with the output $d$. The loops are $a \to b \to a$ with gain $-G_1 H_1$ and $c \to d \to c$ with gain $-G_3 H_2$. They do not touch, so

$$\Delta = 1 + G_1 H_1 + G_3 H_2 + G_1 H_1 G_3 H_2 = (1 + G_1 H_1)(1 + G_3 H_2).$$

The forward path $u \to a \to b \to c \to d$ has gain $G_1 G_2 G_3$ and touches both loops, so $\Delta_1 = 1$. The forward path $u \to c \to d$ has gain $G_4 G_3$ and does not touch the first loop, so $\Delta_2 = 1 + G_1 H_1$. Hence

$$T = \frac{G_1 G_2 G_3 + G_4 G_3 (1 + G_1 H_1)}{(1 + G_1 H_1)(1 + G_3 H_2)}.$$

With $G_1 = 2$, $H_1 = 0.5$, $G_2 = 3$, $G_3 = 4$, $H_2 = 0.25$ and $G_4 = 1$, this gives $\Delta = 4$, the numerator $24 + 8 = 32$ and $T = 8$. Solving the four node equations by [Gaussian elimination](/gaussian-elimination/) gives $d = 8$ for $u = 1$ as well.

## Consequences

- **The block diagram rules.** Each rule of [block diagram reduction](/block-diagram-reduction/) is a small case. Two blocks in series form one path with no loop, so $T = G_1 G_2$. Two blocks in parallel form two paths, so $T = G_1 + G_2$. A negative feedback loop has the path $G$ and the loop $-GH$, so $T = G/(1 + GH)$.
- **The closed-loop characteristic equation.** For a graph whose gains are transfer functions, $\Delta(s) = 0$ is the characteristic equation of the interconnection, and $\Delta$ is the same for every input and output. So all closed-loop transfer functions of one diagram share the denominator $\Delta$, up to cancellations.
- **Symbolic analysis.** The formula gives the transfer function as an explicit sum of products of the gains. [Symbolic circuit analysis](/symbolic-circuit-analysis/) uses this to show how each element value enters a circuit's response.
- **Cost (a measurement of the count).** The number of loops can grow exponentially with the number of nodes. In the complete directed graph on $n$ nodes, the number of loops of length at least 2 is $\sum_{k=2}^{n} \binom{n}{k}(k - 1)!$, which is 84 for $n = 5$, 1,112,073 for $n = 10$ and about $3.49 \times 10^{17}$ for $n = 20$. Gaussian elimination solves the same node equations in $O(n^3)$ arithmetic operations. So the formula is a tool for small graphs and for formulas, not a numeric algorithm for large ones.

## Tightness

- **The products of nontouching loops are needed.** In the worked example, the sum of the single loops alone gives $1 + 1 + 1 = 3$ in place of $\Delta = 4$, and then $T$ would be wrong. Only when every two loops touch is $\Delta = 1 - \sum_a L_a$.
- **The cofactor $\Delta_k$ is needed.** With $\Delta_2 = 1$ in place of $1 + G_1 H_1$, the example gives $28/4 = 7$, not 8. A path that misses a loop is still multiplied by that loop's factor.
- **The hypothesis $\Delta \ne 0$ cannot be dropped.** A node $x$ with a self-loop of gain 1 and an edge $u \xrightarrow{1} x$ gives $x = x + u$, which has no solution for $u \ne 0$. Here $\Delta = 0$ and the formula has no meaning.
- **Linearity cannot be dropped.** The proof uses the determinant of the node equations, so it fails for a graph with a product or a saturation at a node.

## History

Samuel J. Mason, at the Research Laboratory of Electronics of MIT, introduced signal-flow graphs in a 1953 paper on feedback theory, with the node equations and rules to reduce a graph step by step. His 1956 paper, "Further properties of signal flow graphs", gave the general gain formula and its proof by the expansion of the determinant of the node equations; it also appeared in 1955 as an MIT Research Laboratory of Electronics technical report. Control textbooks teach the formula as "Mason's rule", as the hand method for diagrams with several loops.

## References
