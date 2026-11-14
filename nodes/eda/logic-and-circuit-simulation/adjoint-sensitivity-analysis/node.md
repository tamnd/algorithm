---
tag: XP8WTV
kind: algorithm
slug: adjoint-sensitivity-analysis
name: Adjoint sensitivity analysis
aliases:
- Director-Rohrer adjoint network
- adjoint network method
area: eda/logic-and-circuit-simulation
level: core
summary: Director and Rohrer's method that gets the sensitivity of one output to every circuit parameter from a single solve of the adjoint network built by Tellegen's theorem.
model: real-ram
complexity:
  vars: {N: the number of MNA unknowns, P: the number of parameters, K: the number of outputs}
  time: {worst: "O(N^3 + K (N^2 + P))"}
  space: {extra: "O(N^2 + P)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1969
  people: [Stephen W. Director, Ronald A. Rohrer]
  note: Director and Rohrer derived the adjoint network from Tellegen's theorem in 1969, so that one extra analysis gives the derivatives of an output with respect to all elements.
prereqs: [modified-nodal-analysis, tellegen-theorem, lu-decomposition]
see_also: [automatic-differentiation, backpropagation, sparse-tableau-analysis, dc-operating-point-analysis, companion-model, kirchhoff-circuit-laws, klu-solver, gradient-descent]
sources:
  - paper: doi:10.1109/TCT.1969.1082965
    title: Stephen W. Director and Ronald A. Rohrer, The generalized adjoint network and network sensitivities, IEEE Transactions on Circuit Theory 16(3), 318 to 323, 1969
    locator: the adjoint network defined element by element through Tellegen's theorem, and the sensitivity formulas for resistors, sources and controlled sources
  - paper: doi:10.1109/TCT.1971.1083223
    title: Gary D. Hachtel, Robert K. Brayton and Fred G. Gustavson, The sparse tableau approach to network analysis and design, IEEE Transactions on Circuit Theory 18(1), 101 to 113, 1971
    locator: the sensitivity computation with the transposed tableau, which reuses the LU factors of the analysis
  - book: isbn:9780442011949
    title: Jiří Vlach and Kishore Singhal, Computer Methods for Circuit Analysis and Design, second edition, Van Nostrand Reinhold, 1994
    locator: the chapter on sensitivities (adjoint system and the transposed matrix); the chapter number was not checked
  - book: isbn:9780898716597
    title: Andreas Griewank and Andrea Walther, Evaluating Derivatives, Principles and Techniques of Algorithmic Differentiation, second edition, SIAM, 2008
    locator: the reverse mode and its cost bound (a gradient for a small multiple of the cost of the function), of which the adjoint method is the linear-solve case
---

Adjoint sensitivity analysis computes the derivatives of one circuit output, such as a node voltage, with respect to every parameter of the circuit, such as every resistance and every source value, at the cost of one extra linear solve. The extra solve is with the transposed [MNA](/modified-nodal-analysis/) matrix, which is the MNA matrix of the adjoint network, and it reuses the LU factors of the original analysis. It is an algorithm of the circuit simulation half of the logic and circuit simulation sub-area, given by Director and Rohrer in 1969 from [Tellegen's theorem](/tellegen-theorem/).

## In plain words

Suppose you want to know how much an output voltage moves if you change each resistor a little. The obvious way is to change one resistor, solve the circuit again, and repeat for every resistor. With a thousand resistors that is a thousand solves.

The adjoint method needs only one more solve. It builds a second circuit, the adjoint, on the same wires: it removes the original sources, drives the output point with a unit current, and swaps the input and output of each controlled source. The voltages of this circuit say how strongly each place in the circuit influences the output. The sensitivity to each resistor then comes from a product of two numbers: the voltage across it in the original circuit and the voltage across it in the adjoint.

## The problem

Given a linear resistive circuit with parameters $p_1, \ldots, p_P$ (resistances, conductances, gains of controlled sources, values of independent sources), its MNA system $M(p)\, x = z(p)$ with $M$ nonsingular, and an output $\varphi = c^{\mathsf T} x$, compute $\varphi$ and the gradient $\partial \varphi / \partial p_k$ for every $k$. For several outputs $c_1, \ldots, c_K$, compute the $K$ gradients. The same problem arises at a [DC operating point](/dc-operating-point-analysis/) of a nonlinear circuit, with $M$ the Jacobian there, and at each time step of a transient analysis with [companion models](/companion-model/).

## The algorithm

Differentiate $M x = z$: $M\, \partial x / \partial p_k = \partial z / \partial p_k - (\partial M / \partial p_k)\, x$. The *direct method* solves this for every $k$, $P$ solves. The adjoint method moves the inverse onto the output instead:

$$\frac{\partial \varphi}{\partial p_k} = c^{\mathsf T} M^{-1}\Big(\frac{\partial z}{\partial p_k} - \frac{\partial M}{\partial p_k} x\Big) = \lambda^{\mathsf T}\Big(\frac{\partial z}{\partial p_k} - \frac{\partial M}{\partial p_k} x\Big), \qquad M^{\mathsf T} \lambda = c.$$

```pseudo id=main
ADJOINT-SENSITIVITY(netlist, c)
L1  (M, z) ← the MNA stamps of netlist
L2  LU ← FACTOR(M)
L3  x ← SOLVE(LU, z)
L4  λ ← SOLVE-TRANSPOSED(LU, c)                ▷ Mᵀ λ = c: the adjoint circuit
L5  φ ← cᵀ x
L6  for each element k with parameter p_k do
L7      s_k ← λᵀ (∂z/∂p_k − (∂M/∂p_k) x)        ▷ at most four entries, by the table below
L8  return φ, (s_1, ..., s_P)
```

Each element touches at most four entries of $M$ and two of $z$, so line L7 is a short formula. Write $x_a - x_b$ for the difference of node voltages, with $x_0 = 0$ at ground, and the same for $\lambda$:

| element (as on the MNA page) | parameter | $\partial \varphi / \partial p$ |
|---|---|---|
| conductance $G$ from $p$ to $q$ | $G$ | $-(\lambda_p - \lambda_q)(x_p - x_q)$ |
| resistor $R$ from $p$ to $q$ | $R$ | $(\lambda_p - \lambda_q)(x_p - x_q) / R^2$ |
| current source $s$ from $p$ to $q$ | $s$ | $-(\lambda_p - \lambda_q)$ |
| voltage source $s$ with current row $m$ | $s$ | $\lambda_m$ |
| VCCS $g(e_c - e_d)$ from $p$ to $q$ | $g$ | $-(\lambda_p - \lambda_q)(x_c - x_d)$ |

**The adjoint network.** The stamps of resistors, conductances and voltage sources are symmetric, and the transpose of the stamp of a VCCS from $p$ to $q$ controlled by $e_c - e_d$ is the stamp of a VCCS from $c$ to $d$ controlled by $e_p - e_q$, with the same gain. So $M^{\mathsf T}$ is the MNA matrix of the adjoint network: the same circuit with every controlled source turned around and every independent source set to zero. The right side $c$ is its excitation: for $\varphi = e_k$, a 1 A source driving current into node $k$; for $\varphi$ the current of a voltage source, a 1 V value of that source. The vector $\lambda$ is the solution of this circuit, its node voltages and source currents. For a reciprocal circuit, one without controlled sources, the adjoint network is the circuit itself.

## Example

Take the circuit of the MNA page: a 6 V source at node 1, $R_1 = 2\ \Omega$ from node 1 to node 2, $R_2 = 3\ \Omega$ from node 2 to ground, and a 1 A source into node 2, with output $\varphi = e_2$. Its MNA system has

$$M = \begin{pmatrix} 1/2 & -1/2 & 1 \\ -1/2 & 5/6 & 0 \\ 1 & 0 & 0 \end{pmatrix}, \quad z = \begin{pmatrix} 0 \\ 1 \\ 6 \end{pmatrix}, \quad x = \begin{pmatrix} 6 \\ 24/5 \\ -3/5 \end{pmatrix}.$$

$M$ is symmetric. Solve $M^{\mathsf T} \lambda = (0, 1, 0)$: the last row gives $\lambda_1 = 0$, the second $\tfrac56 \lambda_2 = 1$, so $\lambda_2 = 6/5$, and the first gives $\lambda_3 = \tfrac12 \lambda_2 = 3/5$. In circuit terms, the adjoint is the circuit with the 6 V source shorted and the 1 A source removed, driven by 1 A into node 2: node 2 sees $2\ \Omega \parallel 3\ \Omega = 6/5\ \Omega$. The table then gives

- the source $E$: $\lambda_3 = 3/5$;
- $R_1$: $(\lambda_1 - \lambda_2)(x_1 - x_2)/R_1^2 = (-6/5)(6/5)/4 = -9/25$;
- $R_2$: $\lambda_2 x_2 / R_2^2 = (6/5)(24/5)/9 = 16/25$;
- the 1 A source, from ground into node 2: $-(\lambda_0 - \lambda_2) = 6/5$.

By hand, $e_2 = R_2 (E + R_1 I)/(R_1 + R_2)$, whose partial derivatives are $R_2/(R_1 + R_2) = 3/5$, $R_2(I R_2 - E)/(R_1 + R_2)^2 = -9/25$, $R_1(E + R_1 I)/(R_1 + R_2)^2 = 16/25$ and $R_1 R_2/(R_1 + R_2) = 6/5$. One transposed solve gave all four.

## Correctness

The identity behind line L7 is exact: from $M x = z$ and $M^{\mathsf T} \lambda = c$, $\partial \varphi / \partial p_k = c^{\mathsf T} \partial x / \partial p_k = \lambda^{\mathsf T} M\, \partial x / \partial p_k = \lambda^{\mathsf T}(\partial z / \partial p_k - (\partial M / \partial p_k) x)$, where $x$ is differentiable in $p$ because $M$ is nonsingular and its entries are smooth in $p$. The table follows by reading off the entries of each stamp. Director and Rohrer's form of the same result uses only [Kirchhoff's laws](/kirchhoff-circuit-laws/): Tellegen's theorem applied to the perturbed original circuit and the adjoint network, which share one graph, gives $\sum_b (\delta v_b\, \hat\imath_b - \hat v_b\, \delta i_b) = 0$, and the adjoint element laws are chosen so that every unperturbed element drops out of this sum. The [full proof](proofs/correctness.md) gives both forms, the table, and the identification of $M^{\mathsf T}$ with the adjoint network.

## Complexity

With dense LU, line L2 costs $\Theta(N^3)$ and each of lines L3 and L4 costs $\Theta(N^2)$; lines L6 and L7 cost $O(1)$ per parameter, $O(P)$ in all. For $K$ outputs the total is $O(N^3 + K(N^2 + P))$, against $O(N^3 + P(N^2 + K))$ for the direct method, which solves once per parameter. So the adjoint method wins when there are fewer outputs than parameters, the usual case in circuit optimization, where one cost function depends on many element values. With a sparse LU, as in SPICE, the same counts hold with the costs of a sparse factorization and sparse triangular solves. The extra space is the factors, $O(N^2)$ dense, and the gradient, $O(P)$. The code of this page counts the operations, and its tests check that $K$ outputs use one factorization, one forward solve and $K$ transposed solves.

## Properties

- **Exact.** In exact arithmetic the result is the true gradient, not an estimate; the tests check equality with exact fractions against the direct method.
- **One solve per output.** The work for all $P$ derivatives of one output is one transposed solve plus $O(P)$, whatever $P$ is.
- **Reuses the factors.** $M^{\mathsf T} = U^{\mathsf T} L^{\mathsf T} P_r$ for $P_r M = L U$, so the transposed solve uses the same LU factors; no new factorization is needed.
- **Local in the circuit.** Each derivative needs only the original and adjoint voltages at the element's own nodes and, for a controlled source, at its control nodes.
- **Linear in the output.** For a weighted sum of outputs, the adjoint vector is the same weighted sum of their adjoint vectors.

## Variants and improvements

- **Nonlinear DC.** At an operating point of a nonlinear circuit, use the Jacobian of the last Newton iteration as $M$ and the partial derivatives of the device equations in place of $\partial M/\partial p$ and $\partial z/\partial p$; the identity is the implicit function theorem.
- **AC sensitivity.** In [small-signal AC analysis](/ac-small-signal-analysis/) the matrix is complex, $M = G + j\omega C$; the adjoint uses $M^{\mathsf T}$, not the conjugate transpose, and gives the derivatives of a complex transfer function.
- **Transient sensitivity.** For a time-domain output, the adjoint system runs backward in time, with the transposed companion models of each step; it needs the forward solution at every time point, which is stored or recomputed, as in [gradient checkpointing](/gradient-checkpointing/).
- **Noise analysis.** [Circuit noise analysis](/circuit-noise-analysis/) uses the same adjoint solve: the transfer from every noise source to one output is one adjoint solution.
- **Second derivatives.** The derivatives of the gradient follow from one more forward solve per direction, as in second-order [automatic differentiation](/automatic-differentiation/).
- **Tableau form.** In [sparse tableau analysis](/sparse-tableau-analysis/) the adjoint is the transposed tableau, and Hachtel, Brayton and Gustavson used it with the same LU factors.

## When to use it

Use it when there are many parameters and few outputs: gradients of a cost function for circuit optimization and sizing, the sensitivity of a delay or a gain to every element, worst-case and statistical analysis that needs the derivative of one output with respect to every device. When there are many outputs and few parameters, use the direct method, one forward solve per parameter. For a check of a few derivatives, finite differences are simpler, but each costs a full analysis and gives only a few correct digits.

## Pitfalls

- **Transpose, not the same matrix.** With controlled sources $M$ is not symmetric, and solving with $M$ instead of $M^{\mathsf T}$ gives wrong results that still look reasonable. The controlled sources of the adjoint network must be turned around.
- **Signs of the excitation.** The sign of $c$ fixes the direction of the unit source of the adjoint network; mixing the conventions of the current direction for sources and outputs flips signs in the table.
- **Resistance or conductance.** The derivative with respect to $R$ is $-1/R^2$ times the derivative with respect to $G = 1/R$; using one formula for the other is a common error.
- **AC conjugation.** In complex analysis the adjoint uses the plain transpose; the conjugate transpose gives the derivatives of the wrong function.
- **Singular matrix.** If the circuit has a voltage-source loop or a current-source cut set, $M$ is singular and the output has no derivative; the code reports this as an error.

## Implementations

## History

Bode studied the sensitivity of feedback amplifiers in the 1940s, one parameter at a time. Director and Rohrer (1969) defined the adjoint network element by element and used [Tellegen's theorem](/tellegen-theorem/) to show that one analysis of it gives the sensitivities to all elements; they applied it to the automated design of networks in the same years. Hachtel, Brayton and Gustavson (1971) gave the matrix form with the transposed sparse tableau and its LU factors. The same idea, under the name of the reverse mode, became the core of [automatic differentiation](/automatic-differentiation/) and of [backpropagation](/backpropagation/) in neural networks.

## References
