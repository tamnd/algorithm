---
tag: CCJ8NY
kind: technique
slug: modified-nodal-analysis
name: Modified nodal analysis
aliases:
- MNA
- MNA stamps
area: eda/logic-and-circuit-simulation
level: intro
summary: Write a circuit as linear equations in the node voltages plus the currents of voltage sources and inductors, each element adding a fixed stamp to the matrix.
prereqs: [kirchhoff-circuit-laws, gaussian-elimination, laplacian-matrix]
see_also: [sparse-tableau-analysis, tellegen-theorem, companion-model, dc-operating-point-analysis, adjoint-sensitivity-analysis, electrical-flow, lu-decomposition, klu-solver]
sources:
  - paper: doi:10.1109/TCS.1975.1084079
    title: Chung-Wen Ho, Albert E. Ruehli and Pierce A. Brennan, The modified nodal approach to network analysis, IEEE Transactions on Circuits and Systems 22(6), 504 to 509, 1975
    locator: the formulation with node voltages plus the currents of voltage sources and current-defined branches, and the element stamps
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 2, Section 2.4.2 (nodal analysis), Section 2.4.3 (unique solvability), Section 2.4.4 (modified nodal analysis) and Section 2.5.1 (dynamic element stamps)
  - book: isbn:9780442011949
    title: Jiri Vlach and Kishore Singhal, Computer Methods for Circuit Analysis and Design, second edition, Van Nostrand Reinhold, 1994
    locator: the chapters on the formulation of network equations (nodal and modified nodal formulation, element stamps)
  - book: isbn:9780070501690
    title: Lawrence T. Pillage, Ronald A. Rohrer and Chandramouli Visweswariah, Electronic Circuit and System Simulation Methods, McGraw-Hill, 1994
    locator: the early chapters on nodal and modified nodal formulation and element stamps
  - paper: "Laurence W. Nagel, SPICE2: A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, Electronics Research Laboratory, University of California, Berkeley, 1975"
    title: Laurence W. Nagel, SPICE2, A Computer Program to Simulate Semiconductor Circuits, Memorandum UCB/ERL M520, University of California, Berkeley, May 1975
    locator: the chapter on the formulation of the circuit equations
---

Modified nodal analysis (MNA) writes a lumped circuit as a square linear system $Mx = z$ whose unknowns are the voltages of the nodes other than ground plus the currents of the elements whose current is not a function of node voltages, mainly voltage sources and inductors. Each element adds a small fixed pattern of entries, its *stamp*, to $M$ and $z$, so a simulator builds the system in one pass over the netlist. MNA belongs to the circuit simulation half of the logic and circuit simulation sub-area. Ho, Ruehli and Brennan introduced it in 1975, and SPICE and almost every later circuit simulator use it as the base of DC, transient and AC analysis.

## In plain words

A circuit simulator needs equations it can hand to a linear solver. Modified nodal analysis gets them from one rule: at each connection point, the current that flows in must flow out.

Give each connection point a voltage, measured against a chosen ground point. A resistor's current then follows from the two voltages at its ends. A current source's current is known. A voltage source is the odd one out: its current can be anything, so the method adds that current as one more unknown and adds one more equation, which fixes the voltage difference across the source.

Each part writes its own few numbers into the matrix at the rows and columns of the points it touches. Add the contributions of all parts, solve once, and you have every voltage and every source current.

## When it applies

MNA applies to any lumped circuit, that is, any circuit that obeys [Kirchhoff's laws](/kirchhoff-circuit-laws/). It gives a linear system when every element law is linear. The other analyses reduce to that case:

- **Nonlinear DC.** Each Newton iteration of [DC operating point analysis](/dc-operating-point-analysis/) replaces a nonlinear device by its linearization, a conductance in parallel with a current source, and solves one MNA system.
- **Transient.** Each time step replaces a capacitor or inductor by its [companion model](/companion-model/) and solves one MNA system, or one Newton sequence of them, in [transient circuit analysis](/transient-circuit-analysis/).
- **AC.** In [small-signal AC analysis](/ac-small-signal-analysis/) a capacitor is the complex admittance $j\omega C$, and the system is complex.

The technique needs a ground node. The system is square and nonsingular for the circuits described in the theorem below; the Pitfalls section lists what breaks it.

## The template

**Notation.** The nodes are $0, 1, \ldots, n$, with node 0 as ground. Element currents follow the associated reference direction of the [circuit laws page](/kirchhoff-circuit-laws/): a current is counted from the first node of an element, through the element, to its second node. The unknown vector is $x = (e_1, \ldots, e_n, j_1, \ldots, j_m)$: node voltages first, then one current for each element that needs one. Row $k \le n$ of $Mx = z$ is KCL at node $k$: the currents that leave node $k$ through the elements sum to zero, with the known source currents moved to the right side. Row $n + r$ is the law of the $r$-th element with a current unknown.

```pseudo id=main
MNA(netlist, n)
L1  m ← the number of elements of netlist that need a current unknown
L2  M ← (n + m) × (n + m) zero matrix; z ← zero vector of length n + m
L3  r ← 0
L4  for each element el of netlist do
L5      if el needs a current unknown then r ← r + 1; give el the index n + r
L6      ADD-STAMP(M, z, el)        ▷ add the entries of el; skip every entry in row 0 or column 0
L7  x ← SOLVE(M, z)                ▷ report "singular" if M has no inverse
L8  return e_k = x_k for k = 1, ..., n (e_0 = 0), and the currents x_(n+1), ..., x_(n+m)
```

The holes are ADD-STAMP, which holds the element laws, and SOLVE, which is [Gaussian elimination](/gaussian-elimination/) with [partial pivoting](/partial-pivoting/) for small dense systems and sparse LU with a fill-reducing order, such as [Markowitz pivoting](/markowitz-pivoting/) or the [KLU solver](/klu-solver/), in a production simulator. Line L6 drops the entries of ground because $e_0 = 0$ is known and the KCL row of ground is the negative sum of the other KCL rows.

**The stamps.** For an element between nodes $p$ and $q$ ($p$ is the first node):

| Element | Entries of $M$ | Entries of $z$ |
|---|---|---|
| conductance $G$ (resistor $1/G$) | $+G$ at $(p,p)$ and $(q,q)$; $-G$ at $(p,q)$ and $(q,p)$ | none |
| current source $s$, from $p$ through it to $q$ | none | $-s$ at $p$; $+s$ at $q$ |
| voltage source $e_p - e_q = s$, current $j$ at index $k$ | $+1$ at $(p,k)$ and $(k,p)$; $-1$ at $(q,k)$ and $(k,q)$ | $s$ at $k$ |
| voltage-controlled current source, current $g(e_c - e_d)$ from $p$ to $q$ | $+g$ at $(p,c)$ and $(q,d)$; $-g$ at $(p,d)$ and $(q,c)$ | none |
| inductor $L$ at DC, current $j$ at index $k$ | as a voltage source with $s = 0$ | none |

A capacitor is an open circuit at DC and stamps nothing. In a transient step its companion model stamps a conductance and a current source.

**Why the stamps are right.** Row $k \le n$ must say $\sum (\text{currents leaving node } k) = 0$. A conductance from $p$ to $q$ carries $G(e_p - e_q)$ out of $p$ and the same amount into $q$, that is $-G(e_p - e_q) = G(e_q - e_p)$ out of $q$: this is the entries $+G, -G$ in row $p$ and $-G, +G$ in row $q$. A current source moves the known current $s$ out of $p$ and into $q$; moved to the right side, this is $-s$ in row $p$ and $+s$ in row $q$. The current $j$ of a voltage source leaves $p$ and enters $q$, which is the column entries $+1$ in row $p$ and $-1$ in row $q$; its own row is $e_p - e_q = s$. A controlled source carries $g(e_c - e_d)$ out of $p$ and into $q$, which gives the four entries. Every unknown voltage is a node voltage, so every branch voltage is a difference of node voltages and KVL holds by construction. Summing the contributions of all elements gives exactly KCL at every node plus one law for each current unknown, and nothing else, so a vector $x$ solves $Mx = z$ if and only if the node voltages and the source currents it describes satisfy KCL, KVL and all element laws.

**Block form.** Order the branches as resistors (conductances $G = \operatorname{diag}(g_1, \ldots)$, all $g > 0$), voltage sources and current sources, and split the reduced incidence matrix $A$ of the circuit laws page into $A_R$, $A_V$ and $A_I$. Then

$$M = \begin{pmatrix} A_R G A_R^{\mathsf T} & A_V \\ A_V^{\mathsf T} & 0 \end{pmatrix}, \qquad z = \begin{pmatrix} -A_I\, s_I \\ s_V \end{pmatrix}.$$

The block $A_R G A_R^{\mathsf T}$ is the weighted [Laplacian matrix](/laplacian-matrix/) of the resistor graph with the row and column of ground removed.

**Theorem (when MNA is nonsingular).** For a circuit of positive resistors, independent voltage sources and independent current sources, $M$ is nonsingular if and only if both of these hold:

1. the voltage sources contain no loop (no cycle, no two sources in parallel and no source with both ends on one node), that is, the columns of $A_V$ are independent;
2. the resistors and the voltage sources together connect every node to ground, that is, there is no cut set made of current sources only and no floating node, which is the same as the rows of $(A_R \; A_V)$ being independent.

*Lemma.* Let $A_S$ be the submatrix of $A$ made of the columns of a set $S$ of branches. The columns of $A_S$ are independent if and only if $S$ has no cycle, and the rows of $A_S$ are independent if and only if $S$ connects every node to ground. *Proof.* If $S$ has a cycle, add its columns with sign $+1$ for branches traversed along their direction and $-1$ against: each node of the cycle is entered once and left once, so the sum is zero. If $S$ is a forest, every tree of $S$ with at least one branch has at least two leaves, so some leaf $k$ is not ground; among the columns of $S$, row $k$ has one nonzero, so a zero combination gives that column the coefficient 0; remove the leaf and repeat. For the rows: if $S$ connects every node to ground, it contains a spanning tree, whose $n$ columns are independent by the first part, so the rank is $n$. If not, let $C$ be the set of nodes of a component of $S$ that does not contain ground, and let $x$ be its indicator vector. Each branch of $S$ has both ends in $C$ or both outside, so $(A^{\mathsf T} x)_j = x_p - x_q = 0$ (with $x_0 = 0$) on the columns of $S$, and $x \ne 0$. $\square$

*Proof of the theorem.* Assume 1 and 2, and let $M (x, y) = 0$, that is, $A_R G A_R^{\mathsf T} x + A_V y = 0$ and $A_V^{\mathsf T} x = 0$. Multiply the first equation by $x^{\mathsf T}$ and use the second:

$$0 = x^{\mathsf T} A_R G A_R^{\mathsf T} x + (A_V^{\mathsf T} x)^{\mathsf T} y = \sum_{r} g_r \big((A_R^{\mathsf T} x)_r\big)^2.$$

All $g_r > 0$, so $A_R^{\mathsf T} x = 0$. With $A_V^{\mathsf T} x = 0$ this says $(A_R \; A_V)^{\mathsf T} x = 0$, so $x = 0$ by condition 2. Then the first equation gives $A_V y = 0$, so $y = 0$ by condition 1. The kernel is zero, and $M$ is nonsingular.

Conversely, if condition 1 fails, the lemma gives $y \ne 0$ with $A_V y = 0$, and $M(0, y) = (A_V y, 0) = 0$: a current can circulate around the loop of sources. If condition 2 fails, the lemma gives $x \ne 0$ with $A_R^{\mathsf T} x = 0$ and $A_V^{\mathsf T} x = 0$, and $M(x, 0) = (A_R G A_R^{\mathsf T} x, A_V^{\mathsf T} x) = 0$: the voltage of the cut-off part can shift by any constant. In both cases $M$ is singular. $\blacksquare$

The same argument with a monotone nonlinearity in place of $G$ is the uniqueness result of [Tellegen's theorem](/tellegen-theorem/). With controlled sources or negative resistances the graph conditions are neither necessary nor sufficient: a resistor of $1\ \Omega$ in parallel with one of $-1\ \Omega$ gives a zero conductance and a singular $M$, and a controlled source that draws $g e_k$ out of node $k$ acts as a conductance and can make a node with no resistor nonsingular.

**Worked example.** Node 1 has a 6 V source to ground, a $2\ \Omega$ resistor joins nodes 1 and 2, a $3\ \Omega$ resistor joins node 2 to ground, and a 1 A source drives current from ground into node 2. With $x = (e_1, e_2, j)$:

$$\begin{pmatrix} 1/2 & -1/2 & 1 \\ -1/2 & 5/6 & 0 \\ 1 & 0 & 0 \end{pmatrix} \begin{pmatrix} e_1 \\ e_2 \\ j \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ 6 \end{pmatrix}.$$

Row 3 gives $e_1 = 6$. Row 2 gives $-3 + \tfrac{5}{6} e_2 = 1$, so $e_2 = 24/5$. Row 1 gives $3 - \tfrac{12}{5} + j = 0$, so $j = -3/5$: the current of the source from its plus node through it to ground is $-3/5$ A, so the source delivers $3/5$ A to the circuit. The conditions of the theorem hold: one source, no loop, and the resistors and the source connect both nodes to ground. A second source between node 1 and ground, or deleting the $2\ \Omega$ and $3\ \Omega$ resistors so that node 2 meets only the current source, makes $M$ singular, and the code reports it.

**Cost.** Let the netlist have $E$ elements and let $N = n + m$. Lines L1 to L6 take $\Theta(E)$ time, and each element of the table adds at most 4 entries to $M$, so $M$ has at most $4E$ nonzeros before summing. Line L7 with dense elimination takes $\Theta(N^3)$ time and $\Theta(N^2)$ space. With sparse LU the cost depends on the fill-in that the pivot order creates, and no bound below the dense one holds for every circuit graph. Small fill on real circuit matrices is a measured property, not a theorem. The code of this page uses a dense exact solver over fractions, so it detects singularity exactly.

## Classic examples

- [DC operating point analysis](/dc-operating-point-analysis/): one MNA solve per Newton iteration, with the device linearizations stamped as conductances and current sources.
- [Transient circuit analysis](/transient-circuit-analysis/): one MNA solve per Newton iteration of each time step, with [companion models](/companion-model/) for capacitors and inductors.
- [Small-signal AC analysis](/ac-small-signal-analysis/): one complex MNA solve per frequency.
- [Adjoint sensitivity analysis](/adjoint-sensitivity-analysis/): one solve with $M^{\mathsf T}$ gives the derivatives of one output with respect to all parameters.
- [Power grid analysis](/power-grid-analysis/): a resistive grid with current loads is a large nodal system, often with no voltage sources inside the grid.
- [PRIMA](/prima/) and [asymptotic waveform evaluation](/asymptotic-waveform-evaluation/): model order reduction starts from the MNA form $G x + C \dot x = B u$ of a linear RC or RLC network.

## Variations

- **Nodal analysis.** Without voltage sources and inductors, $m = 0$ and $M = A_R G A_R^{\mathsf T}$, the grounded Laplacian. It is symmetric, and positive definite exactly when the resistors connect every node to ground, so [Cholesky decomposition](/cholesky-decomposition/) or the conjugate gradient method applies. A voltage source with a series resistor can be replaced by a current source with a parallel conductance (a Norton equivalent) to stay in this form.
- **More stamps.** A voltage-controlled voltage source $e_p - e_q = \mu (e_c - e_d)$ has a current unknown $j$ at index $k$, the entries $+1$ at $(p,k)$ and $(k,p)$, $-1$ at $(q,k)$ and $(k,q)$, $-\mu$ at $(k,c)$ and $+\mu$ at $(k,d)$. Current-controlled sources use the current unknown of the branch that controls them. An inductor in a transient step has the row $e_p - e_q - L\, dj/dt = 0$, discretized by the companion model.
- **Dynamic form.** With capacitors and inductors, MNA gives $G x + C \dot x = u(t)$, or $f(x) + \frac{d}{dt} q(x) = u(t)$ for nonlinear devices with charges $q$. This is a system of [differential-algebraic equations](/differential-algebraic-equations/), because $C$ is singular in general; its index is 1 or 2 for the usual elements.
- **Sparse tableau analysis.** [Sparse tableau analysis](/sparse-tableau-analysis/) keeps all branch voltages and branch currents as unknowns. Its system is larger and sparser, and MNA is what remains after the branch unknowns of the voltage-defined elements are eliminated.
- **Reduced MNA.** A voltage source to ground fixes its node voltage, so the node and the current unknown can be removed before the solve, and a symmetric conductance block remains. Simulators do this to keep the matrix small and to avoid the zero diagonal.

## Pitfalls

- **A zero diagonal.** The row of a voltage source has a zero on the diagonal, so elimination in the natural order fails even when $M$ is nonsingular. Use pivoting, or order each source current next to a node of the source.
- **Loops of voltage sources and cut sets of current sources.** The theorem shows that they make $M$ singular. At DC an inductor is a zero-volt source, so a loop of inductors and voltage sources is singular. A capacitor is an open circuit, so a node that meets only capacitors and current sources floats. SPICE adds a tiny conductance gmin from such nodes to ground, see [gmin stepping](/gmin-stepping/), and many simulators check the topology first and report the faulty node.
- **Sign conventions.** A current source "from $p$ to $q$" means the current flows through the source from $p$ to $q$, so it leaves the circuit at $p$ and enters at $q$. Mixing this with the opposite convention flips all the source currents in the answer. The current unknown of a voltage source is negative when the source delivers power.
- **Bad scaling.** Conductances of $10^{-12}$ next to $10^{3}$ and rows of $\pm 1$ next to rows of conductances make $M$ badly scaled, and partial pivoting on the raw matrix can pick poor pivots. Simulators scale rows or use threshold pivoting.
- **Floating subcircuits that are not errors.** A transformer winding or an isolated logic block that has no DC path to ground is a valid design, but its MNA matrix at DC is singular. The usual fix is a large resistor to ground from one node of each floating part.
- **Asymmetry.** $M$ is symmetric for resistors and independent sources, but controlled sources and linearized transistors make it nonsymmetric, so solvers for symmetric matrices do not apply in general.

## Exercises

1. Write the MNA system of a $10$ V source at node 1, a $1\ \Omega$ resistor from node 1 to node 2 and a $4\ \Omega$ resistor from node 2 to ground, and solve it by hand. (Answer: $e = (10, 8)$, $j = -2$.)
2. Show that for a circuit of positive resistors and current sources only, $M$ is symmetric positive definite if and only if the resistors connect every node to ground.
3. A voltage-controlled current source draws $2 e_1$ from node 2 to ground, a 1 V source sets $e_1$, and a $5\ \Omega$ resistor joins node 2 to ground. Find the gain $e_2 / e_1$. (Answer: $-10$.)
4. Prove the VCVS stamp of the Variations section, and give a circuit with one VCVS and positive resistors whose $M$ is singular although the graph conditions of the theorem hold.
5. Show that the number of nonzeros of $M$ is at most $4E$ before summing, and give a circuit where summing makes some of them cancel.

## References
