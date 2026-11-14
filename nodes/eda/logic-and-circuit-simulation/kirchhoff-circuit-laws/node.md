---
tag: YT4QF0
kind: definition
slug: kirchhoff-circuit-laws
name: Kirchhoff's circuit laws
aliases:
- KCL and KVL
- Kirchhoff's current law
- Kirchhoff's voltage law
area: eda/logic-and-circuit-simulation
level: intro
summary: The currents into a node sum to zero and the voltages around a loop sum to zero, the constraints that every circuit simulator writes as equations.
prereqs: [directed-graph, incidence-matrix]
see_also: [electrical-flow, laplacian-matrix, tellegen-theorem, modified-nodal-analysis, sparse-tableau-analysis, fundamental-cycle, spanning-tree, flow-conservation]
sources:
  - paper: doi:10.1002/andp.18451400402
    title: G. Kirchhoff, Ueber den Durchgang eines elektrischen Stromes durch eine Ebene, insbesondere durch eine kreisförmige, Annalen der Physik und Chemie 64, 497 to 514, 1845
    locator: the passage that states the two laws for a network of linear conductors, their first statement
  - paper: doi:10.1002/andp.18471481202
    title: G. Kirchhoff, Ueber die Auflösung der Gleichungen, auf welche man bei der Untersuchung der linearen Vertheilung galvanischer Ströme geführt wird, Annalen der Physik und Chemie 72, 497 to 508, 1847
    locator: the whole paper (the independent equations of a network, counted with spanning trees)
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 2, Section 2.2 (topological constraints) and Section 2.3 (cycle space and bond space)
  - book: "Leon O. Chua and Pen-Min Lin, Computer-Aided Analysis of Electronic Circuits: Algorithms and Computational Techniques, Prentice-Hall, 1975"
    title: Leon O. Chua and Pen-Min Lin, Computer-Aided Analysis of Electronic Circuits, Prentice-Hall, 1975
    locator: the chapter on the topological formulation of network equations (incidence, loop and cut set matrices)
---

Kirchhoff's circuit laws are the two linear constraints that the wiring of a lumped circuit puts on its branch currents and branch voltages: the current law (KCL) says that the currents leaving any node sum to zero, and the voltage law (KVL) says that the branch voltages around any closed loop sum to zero. They depend only on the graph of the circuit, not on the elements, so a [circuit simulator](/modified-nodal-analysis/) writes them once from the netlist and adds the element laws. This page belongs to the circuit simulation half of the logic and circuit simulation sub-area, which works with nodal equations rather than with gate values. The same laws on a resistor network give the [electrical flow](/electrical-flow/) of graph algorithms, where Ohm's law, the [Laplacian matrix](/laplacian-matrix/) and Thomson's principle are worked out.

## Definition

**Circuit graph.** A lumped circuit has $n + 1$ nodes, numbered $0, 1, \ldots, n$, with node 0 as the ground (reference) node, and $b$ two-terminal branches. Each branch $j$ has a chosen direction from its first node to its second node, so the circuit is a connected [directed graph](/directed-graph/), possibly with parallel edges. Branch $j$ carries a current $i_j$, counted positive from the first node through the element to the second node, and a voltage $v_j$, the potential of the first node minus the potential of the second. This pairing of directions is the *associated reference direction*: with it, $v_j i_j$ is the power that branch $j$ absorbs.

**Reduced incidence matrix.** $A \in \{-1, 0, 1\}^{n \times b}$ has $A_{kj} = +1$ if branch $j$ leaves node $k$, $A_{kj} = -1$ if it enters node $k$, and $A_{kj} = 0$ otherwise. It is the signed [incidence matrix](/incidence-matrix/) with the row of ground deleted.

**Kirchhoff's current law.** A current vector $i \in \mathbb{R}^b$ satisfies KCL when the net current leaving every node is zero:

$$A\, i = 0, \qquad \text{that is} \qquad \sum_{j} A_{kj}\, i_j = 0 \quad \text{for } k = 1, \ldots, n.$$

The row of ground is the negative sum of the other rows, so it holds too. Summing the rows of a set $S$ of nodes gives the cut set form: the net current through the branches with one end in $S$ and one end outside $S$ is zero.

**Kirchhoff's voltage law.** A voltage vector $v \in \mathbb{R}^b$ satisfies KVL when the signed sum of the branch voltages around every closed loop is zero, a branch counting $+v_j$ when the loop runs along its direction and $-v_j$ against it. Equivalently, there are node voltages $e \in \mathbb{R}^n$ (with $e_0 = 0$) such that

$$v = A^{\mathsf T} e, \qquad \text{that is} \qquad v_j = e_{\text{first}(j)} - e_{\text{second}(j)}.$$

*Why the two forms agree.* If $v = A^{\mathsf T} e$, each loop sum telescopes to $e_u - e_u = 0$. Conversely, if every loop sum is zero, define $e_k$ as the signed sum of $v$ along any path from node $k$ to ground. Two such paths together form a closed walk, whose signed sum is zero, so $e_k$ does not depend on the path, and $v_j = e_{\text{first}(j)} - e_{\text{second}(j)}$ for every branch.

**Counting.** On a connected circuit graph $A$ has rank $n$: it has $n$ rows, and the $n$ columns of a [spanning tree](/spanning-tree/) are independent. To see this, take a leaf $k \ne 0$ of the tree. Among the tree columns, row $k$ has one nonzero, in the column of its leaf branch, so a zero combination of tree columns gives that column the coefficient 0; delete the leaf and repeat. So KCL is $n$ independent equations. KVL is $b - n$ independent equations, one for each [fundamental cycle](/fundamental-cycle/) of a spanning tree. Together with one law for each element, this gives $2b$ equations in the $2b$ branch unknowns, the count that [sparse tableau analysis](/sparse-tableau-analysis/) writes out in full.

## Examples and non-examples

**A four-branch circuit.** Take nodes 1, 2 and ground, and the branches $b_1 = (0 \to 1)$, $b_2 = (1 \to 2)$, $b_3 = (2 \to 0)$, $b_4 = (1 \to 0)$. Then

$$A = \begin{pmatrix} -1 & 1 & 0 & 1 \\ 0 & -1 & 1 & 0 \end{pmatrix}.$$

KCL reads $-i_1 + i_2 + i_4 = 0$ and $-i_2 + i_3 = 0$. KVL reads $v_1 = -e_1$, $v_2 = e_1 - e_2$, $v_3 = e_2$, $v_4 = e_1$, so the two independent loops give $v_1 + v_4 = 0$ and $v_2 + v_3 - v_4 = 0$. With $e = (6, 24/5)$ the branch voltages are $v = (-6, 6/5, 24/5, 6)$, and $i = (23/5, 8/5, 8/5, 3)$ satisfies KCL. Branch $b_1$ has $v_1 i_1 = -138/5 < 0$, so it delivers power, as a source does.

**Non-example: a current vector that breaks KCL.** In the same graph, $i = (1, 1, 1, 1)$ has $-i_1 + i_2 + i_4 = 1 \ne 0$ at node 1, so one ampere would have to collect at node 1.

**Non-example: laws that cannot hold together with the elements.** Two ideal voltage sources of 1 V and 2 V in parallel between node 1 and ground force $v = 1$ and $v = 2$ on the two branches of a two-branch loop. No voltage vector satisfies KVL and both element laws, so the circuit has no solution. Simulators reject such a loop of voltage sources, and the dual case, a cut set made only of current sources whose currents do not sum to zero.

**Non-example: outside the lumped model.** The laws assume that no charge collects at a node and that no changing magnetic flux links a loop. On a wire whose length is a fair fraction of the signal wavelength, or around a loop that a changing magnetic field passes through, the voltage between two points depends on the path, and KVL in the form above does not hold. Such parts are modeled with distributed models or with extra lumped elements.

## Related definitions

- [Flow conservation](/flow-conservation/) in network flows is KCL with demands: the same equation $A\, i = b$ with a right-hand side.
- [Tellegen's theorem](/tellegen-theorem/) follows from KCL and KVL alone: $v^{\mathsf T} i = 0$ for any $v$ that satisfies KVL and any $i$ that satisfies KCL on the same graph.
- [Modified nodal analysis](/modified-nodal-analysis/) uses the node voltages to satisfy KVL by construction and writes KCL at each node; [sparse tableau analysis](/sparse-tableau-analysis/) keeps both laws as separate rows.
- The KVL space $\{A^{\mathsf T} e\}$ and the KCL space $\{i : A i = 0\}$ are orthogonal complements in $\mathbb{R}^b$, the cut space and the cycle space of the graph. The [cycle basis](/cycle-basis/) page builds bases of the cycle space.
- For a diagonal $G$ of branch conductances, $A\, G A^{\mathsf T}$ is the weighted [Laplacian matrix](/laplacian-matrix/) with the row and the column of ground deleted. KCL becomes $A\, G A^{\mathsf T} e = 0$ plus source terms after Ohm's law $i = G v$ is substituted.

## References
