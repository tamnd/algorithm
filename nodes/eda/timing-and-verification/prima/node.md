---
tag: KQ4G00
kind: algorithm
slug: prima
name: PRIMA
aliases:
- passive reduced-order interconnect macromodeling
area: eda/timing-and-verification
level: advanced
summary: Odabasioglu, Celik and Pileggi's model order reduction by projection on a block Krylov subspace with Arnoldi, which keeps the reduced model passive.
solves: [model-order-reduction]
model: real-ram
complexity:
  vars: {n: the number of unknowns of the circuit, k: the order of the reduced model (at most q p for q blocks of p ports)}
  time: {worst: Θ(n³ + k n² + k² n), average: Θ(n³ + k n² + k² n), best: Θ(n³ + k n² + k² n)}
  space: {extra: Θ(n² + k n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1997
  people: [Altan Odabasioglu, Mustafa Celik, Lawrence T. Pileggi]
  note: Odabasioglu, Celik and Pileggi presented PRIMA at ICCAD 1997 and in IEEE TCAD in 1998, after AWE (1990) and PVL (1995) had shown that moment matching can give unstable or non-passive models.
prereqs: [model-order-reduction, krylov-subspace, arnoldi-iteration, passivity]
see_also: [asymptotic-waveform-evaluation, lanczos-algorithm, gram-schmidt-process, lu-decomposition, rc-tree, balanced-truncation, galerkin-method, kalman-yakubovich-popov-lemma]
sources:
  - paper: "Altan Odabasioglu, Mustafa Celik and Lawrence T. Pileggi, PRIMA: passive reduced-order interconnect macromodeling algorithm, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 17(8), 645 to 654, 1998"
    locator: the block Arnoldi algorithm, the congruence transform, the theorem on the matched block moments and the proof of passivity for RLC circuits in modified nodal form
  - paper: "Altan Odabasioglu, Mustafa Celik and Lawrence T. Pileggi, PRIMA: passive reduced-order interconnect macromodeling algorithm, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 58 to 65, 1997"
    locator: the conference version
  - paper: "Peter Feldmann and Roland W. Freund, Efficient linear circuit analysis by Padé approximation via the Lanczos process, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 14(5), 639 to 649, 1995"
    locator: PVL, the Padé model from the Lanczos process, which matches 2q moments but does not keep passivity
---

PRIMA reduces a large linear RLC circuit, such as the extracted model of a group of wires, to a small model that is passive: it does not create energy, so it can be connected to the rest of a circuit and simulated without making it unstable. It builds an orthonormal basis $X$ of the block [Krylov subspace](/krylov-subspace/) of the circuit equations by a block [Arnoldi iteration](/arnoldi-iteration/), and then projects the matrices by the congruence $X^T G X$, $X^T C X$, $X^T B$. Odabasioglu, Celik and Pileggi published it in 1997 and 1998. The model matches $q$ block moments of the transfer function, half as many as the Padé model of [AWE](/asymptotic-waveform-evaluation/), but it keeps passivity and stability, which AWE and PVL do not.

## In plain words

A model with the right moments, as in AWE, can still behave badly: it can have a pole in the right half-plane, or it can generate energy when it is connected to other parts. PRIMA chooses a few directions in the space of node voltages and currents, those that the input reaches in the first few steps of the equations. It then writes the circuit equations only in these directions.

The trick is the way the equations are cut down. Both sides of each matrix are multiplied by the same basis. This keeps the properties that make a circuit passive: resistors still only take energy, and capacitors and inductors still only store it. The price is that, for the same size, the model matches fewer moments than AWE.

## The problem

The input is a linear circuit in modified nodal form,
$$ (G + sC) \, x(s) = B \, u(s), \qquad y(s) = L^T x(s), \qquad H(s) = L^T (G + sC)^{-1} B, $$
with real matrices $G$ and $C$ of order $n$ ($G$ invertible), $p$ inputs in $B$ and outputs in $L$, and a number $q$ of blocks. For an RLC circuit, the unknowns are the node voltages and the inductor currents, and
$$ G = \begin{pmatrix} N & E \\ -E^T & R_b \end{pmatrix}, \qquad C = \begin{pmatrix} Q & 0 \\ 0 & H_L \end{pmatrix}, $$
with conductances $N$, the incidence matrix $E$ of the inductors, their series resistances $R_b$, the capacitances $Q$ and the inductances $H_L$. Then $G + G^T$ is positive semidefinite and $C$ is symmetric positive semidefinite. With $L = B$ (each port injects a current and observes its voltage), $H$ is the impedance matrix, and the circuit is passive.

The output is a reduced model $(\hat G, \hat C, \hat B, \hat L)$ of order $k \le qp$ whose block moments $\hat M_j$ agree with the moments $M_j = L^T (-G^{-1} C)^j G^{-1} B$ for $j < q$ and which is passive. This is a [model order reduction](/model-order-reduction/) problem with a [passivity](/passivity/) constraint.

## The algorithm

```pseudo id=main
PRIMA(G, C, B, L, q)
L1  R ← G⁻¹ B                                            ▷ one LU of G, p solves
L2  X_0 ← an orthonormal basis of the columns of R      ▷ Gram-Schmidt
L3  for k ← 1 to q − 1 do
L4      V ← G⁻¹ (−C X_{k−1})                              ▷ the next block of A = −G⁻¹C
L5      for j ← 0 to k − 1 do V ← V − X_j (X_jᵀ V)        ▷ block modified Gram-Schmidt
L6      X_k ← an orthonormal basis of the columns of V   ▷ drop dependent columns
L7  X ← [X_0, X_1, …, X_{q−1}]
L8  Ĝ ← Xᵀ G X;  Ĉ ← Xᵀ C X;  B̂ ← Xᵀ B;  L̂ ← Xᵀ L     ▷ the congruence transform
L9  return Ĝ, Ĉ, B̂, L̂
```

Lines L1 to L7 are the block Arnoldi process on $A = -G^{-1} C$ with the start block $R = G^{-1} B$, with [Gram-Schmidt](/gram-schmidt-process/) orthogonalization. All solves use one [LU decomposition](/lu-decomposition/) of $G$. Line L8 is the projection. It is a congruence: the same $X$ multiplies both sides of $G$ and $C$. The reduced transfer function is $\hat H(s) = \hat L^T (\hat G + s \hat C)^{-1} \hat B$. The implementation orthogonalizes each new vector twice and drops a vector whose norm falls below $10^{-10}$ of its norm before line L5. It also has helpers for the moments, the transfer function and the poles of a model.

## Example

**An RC ladder with one port.** Take three nodes in a chain, with $R = (1, 1, 1)$ from ground to node 0, node 0 to node 1 and node 1 to node 2, and $C = (1, 2, 1)$ from the nodes to ground. One port injects a current at node 0 and observes its voltage, so $B = L = e_0$ and $H(s)$ is the input impedance. Its moments are $1, -4, 26, -178, 1224, -8420$.

At DC all three nodes are at the same voltage, so $R = (1, 1, 1)$ and $X_0 = (1, 1, 1)/\sqrt 3$. With $q = 1$, $\hat G = 1/3$, $\hat C = 4/3$ and $\hat B = 1/\sqrt 3$, so $\hat H(s) = 1/(1 + 4s)$, with moments $1, -4, 16$. The first two moments agree. The second basis vector for $q = 2$ is $X_1 = (0.7926, -0.2265, -0.5661)$, and

| $q$ | moments of $\hat H$ | poles |
| --- | --- | --- |
| 1 | $1, -4, 16$ | $-0.25$ |
| 2 | $1, -4, 26, -178, 1223.6$ | $-0.1454$, $-1.9101$ |
| 3 | all | $-0.1454$, $-1.4030$, $-2.4516$ |

Here $G$ and $C$ are symmetric and $L = B$, so $2q$ moments agree, not only $q$. With $q = 3 = n$ the model is the circuit.

**An RLC ladder.** Take three nodes with a conductance 1 at node 0 only, capacitors 1 at all nodes, and two branches, each a resistor 1 in series with an inductor 1, between nodes 0 and 1 and between nodes 1 and 2. There are 5 unknowns. The impedance at node 0 has moments $1, -3, 14, -65, 297, -1352$. With $q = 2$ the reduced model of order 2 has the moments $1, -3, 14, -75$ and the poles $-0.18$ and $-0.958$. With $q = 3$, the moments agree up to $-65$, and the poles are $-0.220$ and $-0.876 \pm 0.935 i$. The circuit has the poles $-0.220$, $-0.808 \pm 0.934 i$ and $-0.582 \pm 1.626 i$. All poles are in the left half-plane, as the theory says.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **The basis.** The columns of $X$ are orthonormal and span the block Krylov subspace $\operatorname{span}\{R, AR, \ldots, A^{q-1} R\}$.
- **q block moments.** If $\hat G$ is invertible, then $\hat M_j = M_j$ for $j = 0, \ldots, q - 1$. The proof only uses that the span of $X$ contains the Krylov subspace.
- **2q block moments in the symmetric case.** If $G$ and $C$ are symmetric and $L = B$, as for an RC circuit, then $\hat M_j = M_j$ for $j = 0, \ldots, 2q - 1$. For one port the model is then the Padé model of AWE, and so in that case the Padé model is stable.
- **Full order.** With $n$ columns in $X$, $\hat H = H$.
- **Passivity.** If $G + G^T$ and $C$ are positive semidefinite and $L = B$, the same holds for the reduced model, and $\hat H(s) + \hat H(s)^H$ is positive semidefinite for $\operatorname{Re} s > 0$.
- **Stability.** Under the same conditions, with $\hat G$ invertible, all poles of $\hat H$ are in the closed left half-plane, and in the open one if $G + G^T$ is positive definite.

The proofs are in exact arithmetic. The tests check the moments against exact rational moments of RC and RLC ladders of 3 to 6 sections, the orthonormality of $X$ to $10^{-12}$, the poles and the positive-real condition at random points of the right half-plane in floating point. How many moments a model needs for a given accuracy of the waveform is not proved here; it depends on the circuit.

## Complexity

- **Time.** One LU factorization of $G$ takes $\Theta(n^3)$ for dense matrices. Each of the $k \le qp$ basis vectors costs a product with $C$ and two triangular solves, $\Theta(n^2)$, and two Gram-Schmidt passes against at most $k$ vectors, $\Theta(k n)$. The congruence takes $\Theta(k n^2 + k^2 n)$. In total $\Theta(n^3 + k n^2 + k^2 n)$. For sparse circuits, the factorization and the products cost about the number of nonzero entries of the factors and of $C$ instead.
- **Space.** The factors of $G$ and the $k$ basis vectors, $\Theta(n^2 + k n)$ for dense matrices.
- **Compared with AWE.** The same number of solves with $G$ gives the same Krylov subspace. AWE forms the moments directly, which is ill-conditioned for larger $q$, while PRIMA keeps an orthonormal basis, which is stable in floating point.

## Properties

- **Passive.** The reduced model of an RLC circuit with $L = B$ is passive, so it can be connected to other passive or active parts in a simulator.
- **Half the moments of Padé.** In general $q$ block moments are matched where a Padé model of the same order matches $2q$. For symmetric $G$ and $C$ the count is $2q$ again.
- **Not a realizable netlist.** The reduced matrices are dense and have no direct circuit form. Turning them into resistors and capacitors needs extra work.
- **Order grows with ports.** Each block has $p$ columns, so a model with many ports is large even for small $q$.
- **Numerically stable.** With reorthogonalization, the basis stays orthonormal to rounding error, so larger orders work, unlike AWE.

## Variants and improvements

- **Expansion points.** Use $G + s_0 C$ in place of $G$ for an $s_0 > 0$ to match moments at $s_0$, which avoids a singular $G$ and gives better accuracy at high frequency. Several points can be combined in one basis (multi-point or rational Krylov methods).
- **PVL and SyPVL.** Padé via Lanczos of Feldmann and Freund computes the Padé model with a [Lanczos process](/lanczos-algorithm/). It matches $2q$ moments, but the model need not be passive. Symmetric variants for RC circuits keep passivity.
- **Structure-preserving reduction.** Split $X$ by the blocks of the unknowns (voltages and currents) before the congruence. The model then keeps the RLC structure and, in some methods, matches more moments.
- **Balanced truncation.** [Balanced truncation](/balanced-truncation/) has an a priori error bound but costs $\Theta(n^3)$ for Lyapunov equations, too much for large circuits. Positive-real balanced truncation keeps passivity.

## When to use it

- To make small passive models of large RC or RLC interconnect networks for circuit simulation, timing and signal integrity analysis.
- When the model must be connected back to a simulator, where a non-passive model can create a growing response.
- Not when the number of ports is very large compared with the useful order, and not when a guaranteed error bound is needed.

## Pitfalls

- **$L \ne B$.** Passivity is proved only for $L = B$. A model of a transfer from one node to another (a voltage gain, not an impedance) has no such guarantee.
- **Singular $\hat G$.** For an RLC circuit, $\hat G$ can be singular although $G$ is not. The proof gives an example: an LC ladder with one conductance and $q = 2$ gives $\hat G = \operatorname{diag}(1/3, 0)$, so the model has a pole at $s = 0$ and does not match the moments. An expansion point $s_0 > 0$ avoids this.
- **Loss of orthogonality.** One Gram-Schmidt pass loses orthogonality after many steps. The proofs need the exact span, so reorthogonalize, and drop vectors that are nearly dependent.
- **Breaking the congruence.** Using a different basis on the left, or scaling the rows, keeps the moments but not passivity.

## Implementations

## History

Moment matching for interconnect started with AWE (Pillage and Rohrer, 1990), which forms the moments directly and can give unstable models. Feldmann and Freund (1995) computed the same Padé model stably with a Lanczos process (PVL), but its models need not be passive. Odabasioglu, Celik and Pileggi presented PRIMA at ICCAD 1997 and in IEEE TCAD in 1998: block Arnoldi with a congruence transform, with a proof that the reduced model is passive.

## References
