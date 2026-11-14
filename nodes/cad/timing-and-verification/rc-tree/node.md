---
tag: 8HVCRS
kind: definition
slug: rc-tree
name: RC tree model
aliases:
- resistor-capacitor tree
area: cad/timing-and-verification
level: core
summary: A tree of resistors with capacitors to ground at the nodes, the standard model of an on-chip interconnect net driven from its root.
prereqs: [rooted-tree, laplacian-matrix]
see_also: [elmore-delay, asymptotic-waveform-evaluation, prima, parasitic-extraction, rectilinear-steiner-tree-problem, van-ginneken-buffer-insertion, tsay-zero-skew, impulse-response]
sources:
  - paper: doi:10.1109/TCAD.1983.1270037
    title: Jorge Rubinstein, Paul Penfield Jr. and Mark A. Horowitz, Signal delay in RC tree networks, IEEE Transactions on Computer-Aided Design 2(3), 202 to 211, 1983
    locator: the definition of an RC tree, the common path resistances R_ik, and the bounds on the step response
  - paper: doi:10.1063/1.1697872
    title: W. C. Elmore, The transient response of damped linear networks with particular regard to wideband amplifiers, Journal of Applied Physics 19(1), 55 to 63, 1948
    locator: the delay defined as the first moment of the impulse response of a network with a monotone step response
  - paper: doi:10.1145/217474.217556
    title: Rohini Gupta, Byron Krauter, Bogdan Tutuianu, John Willis and Lawrence T. Pileggi, The Elmore delay as a bound for RC trees with generalized input signals, Proceedings of the 32nd Design Automation Conference, 364 to 369, 1995
    locator: the properties of the impulse response of an RC tree (non-negative, unimodal) used for the bound
  - book: doi:10.1007/978-0-387-93820-2
    title: J. Bhasker and Rakesh Chadha, Static Timing Analysis for Nanometer Designs, A Practical Approach, Springer, 2009
    locator: Chapter 4, Interconnect Parasitics (RC trees and the representation of wires by RC sections)
---

The RC tree model describes an on-chip interconnect net, or the output of a gate driving it, as an electrical tree: each wire segment is a resistor, each node has a capacitor to ground, and a voltage source drives the root. It is the standard input of interconnect delay models such as the [Elmore delay](/elmore-delay/), and of model order reduction methods such as [AWE](/asymptotic-waveform-evaluation/) and [PRIMA](/prima/). The tree structure gives it two useful facts: the inverse of its conductance matrix holds the resistances of common root paths, and its step response at every node rises monotonically. The name is also written "RC interconnect tree"; it is not the [rake-compress tree](/rake-compress-tree/), a data structure for dynamic forests that some authors also call an RC-tree.

## Definition

**RC tree.** An RC tree is a [rooted tree](/rooted-tree/) with nodes $0, 1, \ldots, n$, where node 0 is the *source*, together with

- a resistance $R_k > 0$ on the edge from each node $k \ge 1$ to its parent $p(k)$,
- a capacitance $C_k \ge 0$ from each node $k \ge 1$ to ground,
- an input voltage $u(t)$ applied at node 0 against ground.

There is no resistor to ground and no capacitor between two nodes that are not ground. A driver with output resistance $R_d$ is modeled by one more edge of resistance $R_d$ next to the source. A node with $C_k > 0$ and no children is a *sink*, such as the input pin of a gate.

**Equations.** Let $v(t) \in \mathbb{R}^n$ be the node voltages, $C = \mathrm{diag}(C_1, \ldots, C_n)$, and $G$ the $n \times n$ conductance matrix: $G_{kk}$ is the sum of $1/R$ over the edges at $k$, and $G_{jk} = -1/R_k$ if $j = p(k)$ or $-1/R_j$ if $k = p(j)$, and 0 otherwise. Kirchhoff's current law at each node gives
$$ C \, v'(t) = -G \, v(t) + b \, u(t), $$
where $b_k = 1/R_k$ if $p(k) = 0$ and $b_k = 0$ otherwise. $G$ is the weighted [Laplacian matrix](/laplacian-matrix/) of the tree with the row and column of the source removed. It is symmetric and positive definite, since the tree is connected, and $G \mathbf{1} = b$, so for a constant input $u = 1$ the final voltage is 1 at every node.

**Common path resistance.** For nodes $i$ and $k$, let $R_{ik}$ be the sum of the resistances on the common part of the paths from the source to $i$ and from the source to $k$. Then
$$ (G^{-1})_{ik} = R_{ik}. $$
*Proof.* Column $k$ of $G^{-1}$ is the vector of node voltages when the source is grounded and a current of 1 is injected at node $k$. In a tree, this current flows to ground along the unique path from $k$ to the source, and through no other edge, because every other edge leads into a subtree with no other path to ground, and no current flows in or out of it. So the voltage at node $i$ is the voltage drop along the part of the path from $k$ to the source that the path from $i$ to the source also uses, which is $R_{ik}$. $\square$

**Monotone step response.** For $u = 1$ from $t = 0$ and $v(0) = 0$, each node voltage $v_k(t)$ is non-decreasing and tends to 1. *Proof.* The matrix $A = -C^{-1} G$ (assume $C_k > 0$ for all $k$) has non-negative entries off the diagonal. For a large enough $c$, $A + cI$ is a non-negative matrix, so $e^{At} = e^{-ct} e^{(A + cI)t}$ has only non-negative entries. Then $v'(t) = e^{At} C^{-1} b \ge 0$ entry by entry. The eigenvalues of $C^{-1} G$ are those of the symmetric positive definite matrix $C^{-1/2} G C^{-1/2}$, so they are real and positive, and $v(t) \to G^{-1} b = \mathbf{1}$. $\square$

Thus the impulse response $h_k(t) = v_k'(t)$ at each node is a non-negative function with total area 1, a probability density on $t \ge 0$. The [Elmore delay](/elmore-delay/) is its mean. The monotonicity argument uses only that $C$ is diagonal and $G$ has non-positive entries off the diagonal, so it also holds for RC meshes with grounded capacitors. The formula for $G^{-1}$ needs the tree.

## Examples and non-examples

**A ladder of three sections.** Nodes 1, 2, 3 in a chain from the source, with $R_k = 1$ and $C_k = 1$. Then $R_{ik} = \min(i, k)$:
$$ G = \begin{pmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 1 \end{pmatrix}, \qquad G^{-1} = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 2 & 2 \\ 1 & 2 & 3 \end{pmatrix}. $$
The Elmore delays $\sum_k R_{ik} C_k$ are 3, 5 and 6. The 50 percent delays of the step response, computed with the matrix exponential, are about 1.12, 3.40 and 4.50.

**A branching tree.** Node 1 hangs from the source with $R_1 = 2$, and nodes 2 and 3 hang from node 1 with $R_2 = 1$ and $R_3 = 3$; the capacitances are $C_1 = 1$, $C_2 = 2$, $C_3 = 1$. The common path resistances are $R_{11} = R_{12} = R_{13} = R_{23} = 2$, $R_{22} = 3$ and $R_{33} = 5$, and these are the entries of $G^{-1}$. The Elmore delay at node 2 is $2 \cdot 1 + 3 \cdot 2 + 2 \cdot 1 = 10$, and at node 3 it is $2 \cdot 1 + 2 \cdot 2 + 5 \cdot 1 = 11$.

**A distributed line.** A uniform wire with total resistance $R$ and capacitance $C$, cut into $n$ equal sections with the capacitance at the far end of each, is a ladder. Its far-end Elmore delay is $RC (n + 1) / (2n)$, which is $RC$ for $n = 1$, $2RC/3$ for $n = 3$ and tends to $RC/2$. So the lumped model of a long wire by one section doubles its Elmore delay.

**Non-example: an RC mesh.** A net with a loop, for example two wires from the driver that meet again at a sink, is not a tree. Its $G$ is still symmetric and positive definite, but its inverse is not given by common path resistances. In the loop of four nodes with all $R = 1$ (source to 1, 1 to 2, source to 3, 3 to 2), $(G^{-1})_{22} = 1$, while each of the two root paths to node 2 has resistance 2.

**Non-example: coupling capacitance.** A capacitor between two wires of different nets makes $C$ non-diagonal and couples the trees. The extracted network of a real chip has such capacitors; delay calculators often replace them by grounded capacitors, scaled by a switching factor.

**Non-example: an RLC line.** Wide wires and package traces have inductance. Their step response can overshoot and ring, so it is not monotone and the facts above fail. See the [Elmore delay](/elmore-delay/) page for an example.

## Related definitions

- **Elmore delay.** The delay $T_i = \sum_k R_{ik} C_k$, the first moment of the impulse response; see [Elmore delay](/elmore-delay/).
- **Downstream capacitance.** For an edge into node $k$, the total capacitance of the subtree of $k$. The Elmore delay to $i$ is also the sum, over the edges on the path to $i$, of the resistance times the downstream capacitance.
- **Moments.** The coefficients of the Taylor series of the transfer function at $s = 0$; [AWE](/asymptotic-waveform-evaluation/) matches them with a few poles, and [PRIMA](/prima/) matches them by a projection.
- **Routing trees.** The tree topology of a net is a [Steiner tree](/rectilinear-steiner-tree-problem/) built by the router. [Van Ginneken buffer insertion](/van-ginneken-buffer-insertion/) and [Tsay's zero-skew merge](/tsay-zero-skew/) work on RC trees with the Elmore delay.
- **Extraction.** The resistances and capacitances come from [parasitic extraction](/parasitic-extraction/) of the layout.

## References
