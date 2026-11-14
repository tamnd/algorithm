---
tag: 72RW35
kind: theorem
slug: tellegen-theorem
name: Tellegen's theorem
aliases:
- Tellegen's power theorem
area: eda/logic-and-circuit-simulation
level: core
summary: For any branch voltages that obey KVL and any branch currents that obey KCL on the same graph, the sum of their products is zero, whatever the elements are.
prereqs: [kirchhoff-circuit-laws, incidence-matrix]
see_also: [adjoint-sensitivity-analysis, modified-nodal-analysis, dc-operating-point-analysis, electrical-flow, cycle-basis, rank-nullity-theorem]
sources:
  - paper: "B. D. H. Tellegen, A general network theorem, with applications, Philips Research Reports 7, 259 to 269, 1952"
    title: B. D. H. Tellegen, A general network theorem, with applications, Philips Research Reports 7, 259 to 269, 1952
    locator: the theorem (the sum of voltage times current over the branches is zero for any voltages and currents that obey Kirchhoff's laws) and its applications to network theorems
  - book: "Paul Penfield Jr., Robert Spence and Simon Duinker, Tellegen's Theorem and Electrical Networks, MIT Press, 1970"
    title: Paul Penfield Jr., Robert Spence and Simon Duinker, Tellegen's Theorem and Electrical Networks, MIT Research Monograph, MIT Press, 1970
    locator: the whole book (the general form with Kirchhoff operators, and its use for sensitivity, reciprocity and bounds)
  - paper: doi:10.1109/TCT.1969.1082965
    title: S. W. Director and R. A. Rohrer, The generalized adjoint network and network sensitivities, IEEE Transactions on Circuit Theory 16(3), 318 to 323, 1969
    locator: the adjoint network and the sensitivity formula, derived from Tellegen's theorem
  - book: "Charles A. Desoer and Ernest S. Kuh, Basic Circuit Theory, McGraw-Hill, 1969"
    title: Charles A. Desoer and Ernest S. Kuh, Basic Circuit Theory, McGraw-Hill, 1969
    locator: the chapter on network theorems (Tellegen's theorem, with conservation of energy and reciprocity as consequences)
---

Tellegen's theorem says that on any circuit graph, the branch voltages $v$ of one solution of [Kirchhoff's voltage law](/kirchhoff-circuit-laws/) and the branch currents $i$ of one solution of Kirchhoff's current law satisfy $\sum_j v_j i_j = 0$. The proof uses only the two laws, so it holds for any elements, linear or not, and even when $v$ and $i$ come from two different circuits on the same graph or from two different times. It is a theorem of the circuit simulation half of the logic and circuit simulation sub-area, and it is the basis of [adjoint sensitivity analysis](/adjoint-sensitivity-analysis/). It is not the result called "Tellegen's principle" on the algebra pages (such as matrix-vector multiplication and multipoint evaluation), which is a different theorem about the transposition of linear algorithms.

## Statement

Let a directed graph have nodes $0, 1, \ldots, n$ and branches $1, \ldots, b$, and let $\bar A \in \{-1, 0, 1\}^{(n+1) \times b}$ be its full incidence matrix: $\bar A_{kj} = +1$ if branch $j$ leaves node $k$, $-1$ if it enters node $k$, and 0 otherwise (a branch whose two ends are the same node has a zero column). The graph need not be connected.

**Theorem (Tellegen, 1952).** Let $v \in \mathbb{R}^b$ satisfy KVL, that is $v = \bar A^{\mathsf T} e$ for some $e \in \mathbb{R}^{n+1}$, and let $i \in \mathbb{R}^b$ satisfy KCL, that is $\bar A i = 0$. Then

$$\sum_{j=1}^{b} v_j\, i_j = 0.$$

The same holds over the complex numbers, and for vectors of functions of time or frequency: $v$ and $i$ only have to satisfy the laws on the same graph with the same branch directions.

**Converse.** If $v \in \mathbb{R}^b$ has $v^{\mathsf T} i = 0$ for every $i$ with $\bar A i = 0$, then $v$ satisfies KVL. If $i$ has $v^{\mathsf T} i = 0$ for every $v$ that satisfies KVL, then $i$ satisfies KCL. So the KVL space and the KCL space are orthogonal complements in $\mathbb{R}^b$.

## In plain words

Give every wire of a circuit a voltage and a current. Multiply the two for each wire and add up the products. If the voltages come from node potentials and the currents balance at every node, the total is always zero.

The surprise is how little this needs. It does not matter what the parts are, resistors, transistors or sources. It does not matter whether the voltages and the currents come from the same circuit: you can take the voltages from one circuit and the currents from another circuit wired the same way, or from different moments in time. Only the wiring counts.

When the voltages and the currents come from the same circuit at the same moment, each product is the power of one part, and the theorem says that the power the sources give out is the power that the other parts take in.

## Proof

**The theorem.** By KVL, $v = \bar A^{\mathsf T} e$, and by KCL, $\bar A i = 0$. Then

$$\sum_{j} v_j i_j = v^{\mathsf T} i = (\bar A^{\mathsf T} e)^{\mathsf T} i = e^{\mathsf T} (\bar A i) = e^{\mathsf T} 0 = 0.$$

The same computation, written branch by branch, shows where the cancellation comes from. Branch $j$ from node $p$ to node $q$ contributes $(e_p - e_q) i_j = e_p i_j + e_q(-i_j)$. Collecting the terms of each node $k$ gives $e_k \sum_j \bar A_{kj} i_j$, which is $e_k$ times the net current that leaves node $k$, and that is zero by KCL. No property of any element is used. Over $\mathbb{C}$ the same steps hold with the plain product $v^{\mathsf T} i$ (no conjugate), and for functions the identity holds at each argument. $\blacksquare$

**The converse.** Let $W = \{\bar A^{\mathsf T} e : e \in \mathbb{R}^{n+1}\}$, the range of $\bar A^{\mathsf T}$, and $K = \{i : \bar A i = 0\}$, the kernel of $\bar A$. The theorem says $W \subseteq K^{\perp}$. For any real matrix the kernel of $\bar A$ is the orthogonal complement of the range of $\bar A^{\mathsf T}$, because $\bar A i = 0$ holds exactly when every row of $\bar A$ is orthogonal to $i$, that is, when $i \perp W$. So $K = W^{\perp}$, and in finite dimension $K^{\perp} = W^{\perp\perp} = W$. The first claim of the converse is $v \in K^{\perp} = W$, and the second is $i \in W^{\perp} = K$. $\blacksquare$

**Worked check.** Take nodes 1, 2 and ground 0 and the branches $b_1 = (0 \to 1)$, $b_2 = (1 \to 2)$, $b_3 = (2 \to 0)$, $b_4 = (1 \to 0)$. The node voltages $e_1 = 6$, $e_2 = 24/5$ (with $e_0 = 0$) give $v = (-6, 6/5, 24/5, 6)$. The currents $i' = (2, 1, 1, 1)$ come from a different circuit on the same graph; they satisfy KCL, since node 1 has $-2 + 1 + 1 = 0$ and node 2 has $-1 + 1 = 0$. Then $v^{\mathsf T} i' = -12 + 6/5 + 24/5 + 6 = 0$.

## Consequences

**Conservation of power.** With $v$ and $i$ from one circuit at one time, $v_j i_j$ is the power that branch $j$ absorbs under the associated reference direction, and $\sum_j v_j i_j = 0$ says that the power delivered by the branches with $v_j i_j < 0$ equals the power absorbed by the others.

**Uniqueness for monotone resistors.** Let a circuit consist of independent voltage sources, independent current sources and resistors whose current is a strictly increasing function of their voltage, $i_j = g_j(v_j)$. Assume that the voltage sources form no loop and that the graph without the current sources is connected. Then the circuit has at most one solution. *Proof.* For two solutions, the differences $\Delta v$ and $\Delta i$ satisfy KVL and KCL, so $\sum_j \Delta v_j \Delta i_j = 0$. A voltage source has $\Delta v_j = 0$ and a current source has $\Delta i_j = 0$, so their terms vanish. A resistor term is $(v_j - v'_j)(g_j(v_j) - g_j(v'_j)) \ge 0$, with equality only when $v_j = v'_j$. So every resistor has $\Delta v_j = 0$ and $\Delta i_j = 0$. Write $\Delta v = \bar A^{\mathsf T} \Delta e$ with $\Delta e_0 = 0$. Every branch that is not a current source has $\Delta e_p = \Delta e_q$ at its ends, and these branches connect every node to ground, so $\Delta e = 0$ and $\Delta v = 0$. KCL then reduces to $\bar A_V \Delta i_V = 0$ on the voltage-source columns, which are independent because they form no loop, so $\Delta i = 0$. The same argument with the linear case of [modified nodal analysis](/modified-nodal-analysis/) gives its nonsingularity condition. Existence needs more, and [DC operating point analysis](/dc-operating-point-analysis/) shows circuits with no solution and with several.

**Reciprocity.** Let a network of linear resistors $v_k = R_k i_k$ have two ports, and let $(v, i)$ and $(\hat v, \hat i)$ be two solutions with any sources at the ports. Tellegen's theorem applied to $(v, \hat i)$ and to $(\hat v, i)$ gives $\sum_j v_j \hat i_j = 0 = \sum_j \hat v_j i_j$. On each resistor $v_k \hat i_k = R_k i_k \hat i_k = \hat v_k i_k$, so the resistor terms cancel in the difference, and the port terms satisfy $v_1 \hat i_1 + v_2 \hat i_2 = \hat v_1 i_1 + \hat v_2 i_2$. With a unit current into port 1 in the first experiment, a unit current into port 2 in the second, and both ports otherwise open, this says that the open-circuit voltage at port 2 in the first experiment equals the open-circuit voltage at port 1 in the second.

**Adjoint sensitivity.** Director and Rohrer apply the theorem to a circuit and to an *adjoint* circuit on the same graph, and to the perturbed circuit. The terms of the unchanged elements cancel as in the reciprocity proof, and what remains expresses the change of one output as a sum over the changed elements of products of original and adjoint branch quantities. One solve of the adjoint circuit then gives the derivative of that output with respect to every parameter; [adjoint sensitivity analysis](/adjoint-sensitivity-analysis/) gives the algorithm and its proof.

## Tightness

- **Both laws are needed.** On the graph of the worked check, $i'' = (1, 1, 1, 1)$ breaks KCL at node 1 and gives $v^{\mathsf T} i'' = -6 + 6/5 + 24/5 + 6 = 6 \ne 0$. With $v'' = (1, 0, 0, 0)$, which breaks KVL on the loop $b_1, b_4$, and $i' = (2, 1, 1, 1)$, the sum is $2 \ne 0$.
- **The same graph and the same directions.** If $v$ satisfies KVL on one graph and $i$ satisfies KCL on a graph with the same number of branches but different ends, the sum can be anything. Reversing the reference direction of one branch for $i$ but not for $v$ also breaks the identity.
- **The converse shows that the theorem is as strong as the two laws together.** By the converse, the statement "$v^{\mathsf T} i = 0$ for every KCL vector $i$" is equivalent to KVL, and dually for KCL. So KVL for $v$ together with the identity for all $v$ gives back KCL for $i$, and dually: the theorem cannot be weakened to need less than one of the two laws for each side.

## History

Bernard Tellegen of the Philips research laboratories published the theorem in 1952 in the Philips Research Reports, with applications to network theorems. Penfield, Spence and Duinker wrote a monograph on it in 1970, with a general form in which the voltages and the currents are transformed by any pair of linear operators that keep Kirchhoff's laws. Director and Rohrer used it in 1969 to define the adjoint network and to compute all first-order sensitivities of a circuit at the cost of one extra analysis.

## References
