---
tag: ER2ENS
kind: technique
slug: sparse-tableau-analysis
name: Sparse tableau analysis
aliases:
- sparse tableau formulation
- STA formulation
area: eda/logic-and-circuit-simulation
level: advanced
summary: Write a circuit with all node voltages, branch voltages and branch currents as unknowns, a larger but sparser system that a sparse solver orders as a whole.
prereqs: [kirchhoff-circuit-laws, modified-nodal-analysis, sparse-matrix]
see_also: [schur-complement, fill-in, markowitz-pivoting, sparse-linear-systems, tellegen-theorem, adjoint-sensitivity-analysis, gaussian-elimination, dc-operating-point-analysis]
sources:
  - paper: doi:10.1109/TCT.1971.1083223
    title: Gary D. Hachtel, Robert K. Brayton and Fred G. Gustavson, The sparse tableau approach to network analysis and design, IEEE Transactions on Circuit Theory 18(1), 101 to 113, 1971
    locator: the tableau of KCL, KVL and branch equations, its sparse LU with a structural pivot order, and its use for sensitivity and implicit integration
  - paper: doi:10.1109/TCS.1975.1084079
    title: Chung-Wen Ho, Albert E. Ruehli and Pierce A. Brennan, The modified nodal approach to network analysis, IEEE Transactions on Circuits and Systems 22(6), 504 to 509, 1975
    locator: the comparison of the modified nodal system with the tableau
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 2, Section 2.4.1 (sparse tableau analysis) and Section 2.4.3 (unique solvability)
  - book: "Leon O. Chua and Pen-Min Lin, Computer-Aided Analysis of Electronic Circuits: Algorithms and Computational Techniques, Prentice-Hall, 1975"
    title: Leon O. Chua and Pen-Min Lin, Computer-Aided Analysis of Electronic Circuits, Prentice-Hall, 1975
    locator: the chapter on the tableau formulation of network equations
---

Sparse tableau analysis writes a lumped circuit as one linear system whose unknowns are all node voltages, all branch voltages and all branch currents, with one row for each node law, each branch voltage and each element law. For $n$ nodes besides ground and $b$ branches the system has $n + 2b$ unknowns, far more than [modified nodal analysis](/modified-nodal-analysis/), but almost all of its entries are $0$ or $\pm 1$, and a sparse solver orders the whole system at once. It is a technique of the circuit simulation half of the logic and circuit simulation sub-area. Hachtel, Brayton and Gustavson of IBM gave it in 1971 together with a sparse LU method for it.

## In plain words

A circuit gives three kinds of facts. Currents balance at every connection point. The voltage across each part is the difference of the voltages at its two ends. Each part has its own law, such as a resistor's current being its voltage divided by its resistance.

The tableau method writes down all three kinds of facts, as they are, without substituting one into another. Every voltage and every current becomes an unknown. The system is much bigger than the one that nodal methods build, but each row touches only a few unknowns, and most numbers in it are one or minus one.

A solver for sparse systems then picks a good order of elimination for the whole system. In effect it decides by itself which substitutions to make, instead of following the fixed choice that nodal methods make before the solve.

## When it applies

The tableau applies to any lumped circuit whose element laws are linear in the branch voltages and currents, and to each Newton iteration and each implicit time step of a nonlinear or dynamic circuit, after the same linearization and [companion models](/companion-model/) that MNA uses. Its strength is generality: every element law of the form "a linear combination of branch voltages and branch currents equals a known value" fits, including current-controlled sources, ideal transformers and elements with no admittance form, with no special stamp. It needs a sparse solver; with dense elimination it costs far more than MNA for the same circuit.

## The template

**The system.** Use the circuit graph and the reduced incidence matrix $A \in \{-1, 0, 1\}^{n \times b}$ of [Kirchhoff's circuit laws](/kirchhoff-circuit-laws/). Write the element laws as $K_v v + K_i i = s$, with $K_v, K_i \in \mathbb{R}^{b \times b}$ and one row per branch: a resistor gives $-G v_j + i_j = 0$, a voltage source $v_j = s_j$, a current source $i_j = s_j$, a voltage-controlled current source $i_j - g v_c = 0$ where $v_c$ is the branch voltage of its control port, and a current-controlled current source $i_j - \beta i_c = 0$. The tableau is

$$T \begin{pmatrix} e \\ v \\ i \end{pmatrix} = \begin{pmatrix} 0 & 0 & A \\ -A^{\mathsf T} & I_b & 0 \\ 0 & K_v & K_i \end{pmatrix} \begin{pmatrix} e \\ v \\ i \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ s \end{pmatrix}.$$

The first block row is KCL, the second is KVL in the form $v = A^{\mathsf T} e$, and the third is the element laws.

```pseudo id=main
SPARSE-TABLEAU(netlist, n)
L1  b ← the number of branches; number the unknowns e_1..e_n, v_1..v_b, i_1..i_b
L2  for each branch j from p to q do
L3      put +1 at (KCL p, i_j), −1 at (KCL q, i_j); put 1 at (KVL j, v_j), −1 at (KVL j, e_p), +1 at (KVL j, e_q)    ▷ skip node 0
L4      put the row of the element law of j into (K_v, K_i, s)      ▷ hole: the branch law
L5  π ← ORDER(T)                                                       ▷ hole: the pivot order
L6  factor T with the order π and solve for (e, v, i)                  ▷ hole: the sparse LU
L7  return e, v, i
```

The holes are the branch law of line L4, the pivot order of line L5 and the sparse LU of line L6. Hachtel, Brayton and Gustavson choose the order mainly from the structure of $T$, which does not change between Newton iterations and time steps, so that one ordering serves the whole analysis.

**Why the tableau is the circuit.** A vector $(e, v, i)$ solves $T(e, v, i) = (0, 0, s)$ exactly when $i$ satisfies KCL, $v$ satisfies KVL with node voltages $e$, and every element law holds. This is the definition of a solution of the circuit, so the solution set of the tableau is the solution set of the circuit, with no elimination and no assumption on the elements.

**Theorem (the tableau is MNA with more unknowns).** For a circuit of positive resistors, independent voltage sources and independent current sources, $\det T = \pm \det M$, where $M$ is the MNA matrix of the same circuit. So $T$ is nonsingular exactly when $M$ is, that is, when the voltage sources form no loop and the resistors and voltage sources connect every node to ground, and the two systems have the same node voltages and source currents.

*Proof.* The proof uses the [Schur complement](/schur-complement/) identity: when the top left block is an identity,

$$\det \begin{pmatrix} I & B \\ C & D' \end{pmatrix} = \det(D' - C B),$$

which follows from multiplying on the right by $\begin{pmatrix} I & -B \\ 0 & I \end{pmatrix}$, of determinant 1, to get the block lower triangular matrix $\begin{pmatrix} I & 0 \\ C & D' - CB \end{pmatrix}$. Permuting rows and columns changes a determinant only by a sign.

*Step 1: remove $v$.* The KVL rows have the identity block $I_b$ in the columns of $v$, and they say $v = A^{\mathsf T} e$. The Schur complement with respect to this block replaces $v$ by $A^{\mathsf T} e$ in the other rows. What remains is the system in $(e, i)$

$$\begin{pmatrix} 0 & A \\ K_v A^{\mathsf T} & K_i \end{pmatrix} \begin{pmatrix} e \\ i \end{pmatrix} = \begin{pmatrix} 0 \\ s \end{pmatrix},$$

and its determinant is $\pm \det T$.

*Step 2: remove the currents of resistors and current sources.* Order the branches as resistors, voltage sources and current sources, and split $A = (A_R \; A_V \; A_I)$. The law rows of the resistors are $i_R - G A_R^{\mathsf T} e = 0$, and those of the current sources are $i_I = s_I$; in the columns of $i_R$ and $i_I$ these rows form an identity block. The Schur complement with respect to it substitutes $i_R = G A_R^{\mathsf T} e$ and $i_I = s_I$ into the remaining rows. The KCL rows become $A_R G A_R^{\mathsf T} e + A_V i_V = -A_I s_I$, and the law rows of the voltage sources stay $A_V^{\mathsf T} e = s_V$. That is the MNA system $M (e, i_V) = z$, with determinant $\pm \det T$. Each step is a substitution that can be undone, so the solutions correspond one to one. $\blacksquare$

The MNA theorem gives the condition for $\det M \ne 0$. For general element laws the same two steps show that the tableau is nonsingular exactly when the reduced system in $(e, i)$ of Step 1 is.

**Worked example.** The circuit of the [MNA page](/modified-nodal-analysis/) has a 6 V source from node 1 to ground, $2\ \Omega$ from node 1 to node 2, $3\ \Omega$ from node 2 to ground and a 1 A source from ground into node 2. Take the branches $V = (1 \to 0)$, $R_1 = (1 \to 2)$, $R_2 = (2 \to 0)$ and $I = (0 \to 2)$, so $n = 2$, $b = 4$, and the tableau has $2 + 8 = 10$ unknowns. Its rows are KCL $i_V + i_{R1} = 0$ and $-i_{R1} + i_{R2} - i_I = 0$; KVL $v_V = e_1$, $v_{R1} = e_1 - e_2$, $v_{R2} = e_2$, $v_I = -e_2$; and the laws $v_V = 6$, $i_{R1} - v_{R1}/2 = 0$, $i_{R2} - v_{R2}/3 = 0$, $i_I = 1$. The solution is $e = (6, 24/5)$, $v = (6, 6/5, 24/5, -24/5)$ and $i = (-3/5, 3/5, 8/5, 1)$, the same node voltages and source current as MNA. The tableau has 20 nonzeros in a $10 \times 10$ matrix, a density of 0.2, while the MNA matrix has 6 nonzeros in a $3 \times 3$ matrix, a density of about 0.67.

**Cost.** The tableau has $N = n + 2b$ unknowns. $A$ has at most $2b$ nonzeros, $-A^{\mathsf T}$ the same, $I_b$ has $b$, and a two-terminal element law has at most 2, so $T$ has at most $7b$ nonzeros for two-terminal elements. Building it takes $\Theta(n + b)$ time. The cost of the solve is the cost of sparse LU with the chosen order, which depends on the fill-in. If the solver pivots first on the KVL identity block and on the law rows of resistors and sources, it reproduces the MNA elimination, at the cost of MNA plus the substitutions of the proof above, which take time linear in the number of nonzeros of $T$; a good structural order can do better on circuits where another elimination order creates less fill. Whether it does better on a given class of circuits is measured, not proved.

## Classic examples

- [DC operating point analysis](/dc-operating-point-analysis/) of a nonlinear circuit, with each device law replaced by its Newton linearization in the rows of $K_v$ and $K_i$.
- [Transient circuit analysis](/transient-circuit-analysis/), where Hachtel, Brayton and Gustavson combine the tableau with implicit variable-order integration, so that each step is one sparse solve with a fixed structure.
- [Adjoint sensitivity analysis](/adjoint-sensitivity-analysis/): the transposed tableau $T^{\mathsf T}$ is the tableau of the adjoint network, and the same LU factors solve it.
- Circuits with current-controlled sources, ideal transformers or ideal operational amplifiers, whose laws fit the tableau rows directly but need extra unknowns and special stamps in MNA.

## Variations

- **Modified nodal analysis.** MNA is the tableau after the elimination of all branch voltages and of the currents of the elements with an admittance form, done before the solve. It fixes part of the elimination order in advance in exchange for a much smaller system, and most simulators since SPICE2 use it.
- **Two-graph and reduced tableaux.** Some formulations keep only the branch currents of a chosen set of elements, or eliminate the KVL rows only, to sit between MNA and the full tableau.
- **Nonlinear tableau.** With nonlinear element laws $f(v, i) = s$ the tableau becomes $F(e, v, i) = 0$, and Newton's method solves it with the Jacobian $T$ whose $K_v$ and $K_i$ hold the partial derivatives of $f$.
- **Dynamic tableau.** With capacitors and inductors the law rows contain derivatives, $K_v v + K_i i + L_v \dot v + L_i \dot i = s$, and an implicit integration formula turns each time step into one tableau of the static form.

## Pitfalls

- **Dense solution destroys the point.** Solved by dense elimination, the tableau costs $\Theta((n + 2b)^3)$, far more than MNA. It is only useful with a sparse LU that exploits the many $\pm 1$ entries.
- **Pivoting on numbers breaks the fixed order.** Numerical pivoting picks pivots by size and can change the elimination order from one Newton iteration to the next, which loses the precomputed structure. Structural pivot orders need a check that the chosen pivots are not too small, and a fallback.
- **The same singular cases as MNA.** By the theorem, a loop of voltage sources or a cut set of current sources makes the tableau singular too; the extra unknowns do not remove the problem.
- **The name.** In this area the abbreviation for static timing analysis is common, so this page writes "sparse tableau" in full.
- **Memory.** The tableau holds about $7b$ nonzeros before fill, against about $4b$ for MNA. On large circuits the extra rows cost memory even when the factor time is similar.

## Exercises

1. Write the tableau of the example in full as a $10 \times 10$ matrix, and count its nonzeros.
2. Carry out Step 1 and Step 2 of the proof on the example by hand, and check that the result is the MNA matrix of the MNA page.
3. Write the tableau row of a current-controlled voltage source $v_j = r\, i_c$, and explain why MNA needs an extra current unknown for it.
4. Show that the transpose of the tableau of a circuit of resistors and independent sources is again the tableau of a circuit on the same graph, up to signs and a permutation.

## References
