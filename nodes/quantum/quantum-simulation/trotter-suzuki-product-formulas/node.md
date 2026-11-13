---
tag: B7XF2R
kind: algorithm
slug: trotter-suzuki-product-formulas
name: Trotter-Suzuki product formulas
aliases:
- Trotterization
- product formula simulation
area: quantum/quantum-simulation
level: core
summary: "Approximate e^(-iHt) for H = H_1 + ... + H_L by r steps, each a product of exponentials of single terms. First order error t^2 a/(2r), second order t^3 b/r^2, with commutator constants a and b."
solves: [hamiltonian-simulation]
model: quantum-circuit-model
complexity:
  vars: {L: the number of terms, t: the evolution time, e: the error in the spectral norm, a: the first order commutator constant, b: the second order commutator constant}
  time: {first_order: O(L a t^2/e), second_order: O(L t^(3/2) (b/e)^(1/2))}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, ancilla_free: true, error_norm: spectral, unitary_output: true}
history:
  year: 1996
  people: [Seth Lloyd]
  note: Trotter (1959) proved the product formula and Strang (1968) introduced the symmetric splitting for difference schemes. Lloyd (1996) used product formulas to simulate local Hamiltonians on a quantum computer.
prereqs: [hamiltonian-simulation, lie-trotter-product-formula]
see_also: [higher-order-trotter-suzuki, commutator-scaling, qdrift, multi-product-formulas, operator-splitting, symplectic-integrators, pauli-string-decomposition, universal-quantum-simulator]
sources:
  - paper: doi:10.1126/science.273.5278.1073
    title: Seth Lloyd, Universal quantum simulators, Science 273(5278), 1996, pages 1073 to 1078
    locator: the first order product formula for sums of local terms and its error
  - paper: doi:10.1103/PhysRevX.11.011020
    title: Andrew M. Childs, Yuan Su, Minh C. Tran, Nathan Wiebe and Shuchen Zhu, Theory of Trotter error with commutator scaling, Physical Review X 11(1), 2021, article 011020 (arXiv:1912.08854)
    locator: Proposition 15 (first order bound) and Proposition 16 (second order bound with the constants 1/12 and 1/24)
  - paper: doi:10.1137/0705041
    title: Gilbert Strang, On the construction and comparison of difference schemes, SIAM Journal on Numerical Analysis 5(3), 1968, pages 506 to 517
    locator: the symmetric splitting and its second order accuracy
  - paper: doi:10.1090/S0002-9939-1959-0108732-6
    title: H. F. Trotter, On the product of semi-groups of operators, Proceedings of the American Mathematical Society 10(4), 1959, pages 545 to 551
    locator: the product formula
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 4.7 (simulation of quantum systems), the first and second order Trotter formulas
---

The Trotter-Suzuki product formulas approximate the time evolution $e^{-iHt}$ of a Hamiltonian $H = H_1 + \cdots + H_L$ by a product of exponentials of the single terms. The time is cut into $r$ steps of length $\delta = t/r$, and in each step every term acts alone for a time $\delta$ (first order) or in a symmetric pattern of half steps (second order). Each $e^{-iH_j\delta}$ is a small circuit when $H_j$ acts on few qubits, so the whole product is a circuit of the [quantum circuit model](/quantum-circuit-model/) with no ancilla qubits. The first order formula has error at most $t^2\alpha_1/(2r)$ and the second order formula $t^3\beta_2/r^2$ in the spectral norm, where $\alpha_1$ and $\beta_2$ are sums of norms of commutators of the terms. The formulas solve the [Hamiltonian simulation](/hamiltonian-simulation/) problem, they are the algorithm behind the [universal quantum simulator](/universal-quantum-simulator/) theorem, and the limit theorem they rest on is the [Lie-Trotter product formula](/lie-trotter-product-formula/). The recursive formulas of every even order are on the [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/) page.

## In plain words

Several forces act on a system at the same time, and we can only apply one force at a time. So we cut the time into many short slices, and in each slice we apply the forces one after another. If the forces did not disturb each other, the result would be exact. They do disturb each other, and the error in each slice is small: it shrinks with the square of the slice length for the plain version. A better version goes forward through the forces with half slices, applies the last force for a whole slice, and comes back through the forces with half slices. This mirror pattern cancels the main part of the error, so its error per slice shrinks with the cube of the slice length. More slices cost more gates and give less error.

## The problem

The input is a Hamiltonian in the Pauli list access model, $H = \sum_{j=1}^{L} c_j P_j$ with real coefficients $c_j$ and $n$-qubit Pauli strings $P_j$ (a [Pauli string decomposition](/pauli-string-decomposition/)), a time $t > 0$ and an error $\epsilon > 0$. The output is a circuit $V$ with $\|V - e^{-iHt}\| \le \epsilon$ in the spectral norm. The method works for any Hermitian terms $H_j$ whose exponentials we can apply; Pauli strings are the common case because $e^{-i\theta P}$ is $2(w-1)$ CNOT gates and one rotation for a string of weight $w$ (see [digital quantum simulation](/digital-quantum-simulation/)).

Write $H_j = c_j P_j$ and $T_{j+1} = H_{j+1} + \cdots + H_L$. The two constants are
$$\alpha_1 = \sum_{j=1}^{L-1} \|[H_j, T_{j+1}]\|, \qquad \beta_2 = \sum_{j=1}^{L-1} \left( \frac{\|[T_{j+1}, [T_{j+1}, H_j]]\|}{12} + \frac{\|[H_j, [H_j, T_{j+1}]]\|}{24} \right).$$
Both are zero when all terms commute, and then both formulas are exact.

## The algorithm

The output is a list of pairs $(P, \theta)$. The circuit applies $e^{-i\theta P}$ for each pair, in the order of the list, so the first pair acts first.

```pseudo id=main
TROTTER(((c_1, P_1), ..., (c_L, P_L)), t, r, order)    ▷ order is 1 or 2
L1  δ ← t / r
L2  seq ← an empty list
L3  repeat r times
L4      if order = 1 then
L5          for j ← 1 to L: append (P_j, c_j δ) to seq
L6      else                                            ▷ order 2
L7          for j ← 1 to L - 1: append (P_j, c_j δ / 2) to seq
L8          append (P_L, c_L δ) to seq
L9          for j ← L - 1 down to 1: append (P_j, c_j δ / 2) to seq
L10 replace each run of neighbors with the same string (P, θ), (P, θ') by (P, θ + θ')
L11 return seq
```

Lines L5 and L7 to L9 build one step. In matrix form, with the first factor on the right, the first order step is $S_1(\delta) = e^{-iH_L\delta} \cdots e^{-iH_1\delta}$ and the second order step is the symmetric product
$$S_2(\delta) = e^{-iH_1\delta/2} \cdots e^{-iH_{L-1}\delta/2} \, e^{-iH_L\delta} \, e^{-iH_{L-1}\delta/2} \cdots e^{-iH_1\delta/2}.$$
Line L10 uses $e^{-i\theta P} e^{-i\theta' P} = e^{-i(\theta + \theta')P}$. For the second order formula it joins the last half step of $H_1$ in one step with the first half step of $H_1$ in the next, so $r$ steps cost $2(L-1)r + 1$ exponentials instead of $(2L-1)r$. This is why the second order formula costs only about twice the first order formula per step.

To meet an error $\epsilon$, choose the least $r$ with $t^2\alpha_1/(2r) \le \epsilon$ (first order) or $t^3\beta_2/r^2 \le \epsilon$ (second order), that is $r = \lceil t^2\alpha_1/(2\epsilon) \rceil$ or $r = \lceil t^{3/2}(\beta_2/\epsilon)^{1/2} \rceil$.

## Example

Take two qubits and $H = ZZ + 0.8\,XI + 0.8\,IX$ (an Ising pair in a transverse field; the last letter acts on qubit 0), with $t = 1$.

**The constants by hand.** $H_1 = ZZ$ and $T_2 = 0.8(XI + IX)$. $ZZ$ anticommutes with $XI$ and with $IX$, and $XI$ commutes with $IX$, so only $j = 1$ counts. $[ZZ, XI] = 2\,ZZ \cdot XI = 2i\,YZ$ and $[ZZ, IX] = 2i\,ZY$, so $[H_1, T_2] = 1.6i(YZ + ZY)$. The strings $YZ$ and $ZY$ commute and $YZ + ZY$ has the eigenvalues $\pm 2$ and $0$, so $\alpha_1 = 3.2$. In the same way $[T_2, [T_2, H_1]] = 5.12(ZZ - YY)$ with norm $10.24$ and $[H_1, [H_1, T_2]] = 3.2(XI + IX)$ with norm $6.4$, so $\beta_2 = 10.24/12 + 6.4/24 = 1.12$.

**The circuits for $r = 2$.** With $\delta = 0.5$, the first order list is
$(ZZ, 0.5), (XI, 0.4), (IX, 0.4), (ZZ, 0.5), (XI, 0.4), (IX, 0.4)$.
The second order list, after line L10 joins the two middle half steps of $ZZ$, is
$(ZZ, 0.25), (XI, 0.2), (IX, 0.4), (XI, 0.2), (ZZ, 0.5), (XI, 0.2), (IX, 0.4), (XI, 0.2), (ZZ, 0.25)$,
which is $2(L-1)r + 1 = 9$ exponentials.

**Errors against the bounds.** The page's simulator computes the exact $e^{-iHt}$ by eigendecomposition (checked against a scaled Taylor series with squaring), multiplies out the circuit, and takes the spectral norm of the difference.

| $r$ | first order error | bound $1.6/r$ | ratio | second order error | bound $1.12/r^2$ | ratio |
|---|---|---|---|---|---|---|
| 1 | 1.0697 | 1.6 | | 0.63531 | 1.12 | |
| 2 | 0.43666 | 0.8 | 2.45 | 0.13254 | 0.28 | 4.79 |
| 4 | 0.20562 | 0.4 | 2.12 | 0.031288 | 0.07 | 4.24 |
| 8 | 0.10126 | 0.2 | 2.03 | 0.0077082 | 0.0175 | 4.06 |
| 16 | 0.050439 | 0.1 | 2.01 | 0.0019200 | 0.004375 | 4.01 |
| 32 | 0.025196 | 0.05 | 2.00 | 0.00047955 | 0.0010938 | 4.00 |
| 64 | 0.012595 | 0.025 | 2.00 | 0.00011986 | 0.00027344 | 4.00 |

The ratio column is the error at $r/2$ divided by the error at $r$. Halving the step halves the first order error and quarters the second order error, so the observed orders are 1 and 2. Each bound holds and is about twice the true error here. For $\epsilon = 10^{-3}$ the bounds ask for $r = 1600$ first order steps (4800 exponentials) and $r = 34$ second order steps (137 exponentials). Scaling the measured errors gives the true least counts, about 810 first order steps, and a search over $r$ gives 23 second order steps (93 exponentials).

## Correctness

Two facts give both bounds. First, for unitaries, errors add: $\|U_1 U_2 - W_1 W_2\| \le \|U_1 - W_1\| + \|U_2 - W_2\|$, so $r$ steps have at most $r$ times the error of one step. Second, the error of one step follows from Duhamel's formula: if $S'(s) = -iG(s)S(s)$ with $S(0) = I$, then $\|S(\delta) - e^{-iH\delta}\| \le \int_0^\delta \|G(s) - H\|\,ds$. For the first order step $\|G(s) - H\| \le s\|[H_1, T_2]\|$, which gives $\delta^2/2$ times a commutator norm. For the symmetric step the first order part of $G(s) - H$ cancels, and what is left is $s^2/4$ and $s^2/8$ times the two double commutators, which integrate to the constants $1/12$ and $1/24$. Induction on the number of terms gives $\alpha_1$ and $\beta_2$. The full proof is below.

## Complexity

- **Exponentials.** The first order formula uses $Lr$ exponentials and the second order formula $2(L-1)r + 1$. With $r$ from the bounds, the first order cost is $O(L\alpha_1 t^2/\epsilon)$ and the second order cost $O(L t^{3/2}\beta_2^{1/2}/\epsilon^{1/2})$.
- **Gates.** Each exponential of a Pauli string of weight $w$ is $2(w-1)$ CNOT gates and one rotation, plus at most $2w$ one-qubit basis changes. Over a finite gate set, each rotation costs $O(\log(1/\epsilon'))$ T gates for a rotation error $\epsilon'$ by modern synthesis.
- **Qubits.** Exactly the $n$ system qubits. No ancilla qubits are used.
- **Depth.** Exponentials of terms on disjoint qubits can run in parallel. For a nearest-neighbor chain, ordering the terms as even bonds, odd bonds, then fields gives depth $O(1)$ per step.
- **Classical cost.** Computing the list takes $O(Lr)$ time. The exact constants $\alpha_1$ and $\beta_2$ are spectral norms of $2^n \times 2^n$ matrices. Upper bounds by the triangle inequality, such as $\alpha_1 \le \sum_{j<k} \|[H_j, H_k]\| = \sum 2|c_j c_k|$ over the anticommuting pairs of strings, need only the commutation pattern and take time polynomial in $L$ and $n$.

For the transverse-field Ising chain $\sum_i Z_iZ_{i+1} + \sum_i X_i$ on $n = 10$ sites at $t = 1$ and $\epsilon = 10^{-3}$, $\alpha_1 = 4(n-1) = 36$ and the first order bound asks for $r = 18\,000$ steps, that is $342\,000$ exponentials. The [commutator scaling](/commutator-scaling/) page gives the second order numbers and the growth with $n$.

## Properties

- **Exact for commuting terms.** If all terms commute, $\alpha_1 = \beta_2 = 0$ and one step is exact.
- **Unitary output.** The circuit is unitary for every $r$, so its error does not blow up: the formulas are stable for every step size, unlike explicit [Runge-Kutta methods](/runge-kutta-methods/) for stiff problems.
- **Symmetric second order.** $S_2(\delta) S_2(-\delta) = I$, so $S_2$ is time-reversible. This symmetry is what kills the even order error terms and makes the recursive construction of the [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/) formulas work.
- **Order dependence.** The error depends on the order in which the terms are listed. The bound $\alpha_1$ depends on it too.
- **Structure preserving.** The formulas are the quantum form of the splitting methods for [Hamiltonian systems](/hamiltonian-systems/): the symmetric step is the Strang splitting, and in classical mechanics the same pattern gives the leapfrog and other [symplectic integrators](/symplectic-integrators/).

## Variants and improvements

- **Higher orders.** Suzuki's recursion builds formulas of every even order $2k$ from the symmetric step, with $5^{k-1}$ symmetric stages per step: see [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/).
- **Randomized orderings.** Choosing the order of the terms at random in each step, or reversing it every other step, can lower the error. Random sampling of the terms themselves, with probability proportional to $|c_j|$, is [qDRIFT](/qdrift/), whose cost does not depend on $L$.
- **Grouping.** Terms that commute can be grouped, since a group of commuting Pauli strings can be exponentiated together with no error. This lowers $L$ and the constants.
- **Extrapolation.** [Multi-product formulas](/multi-product-formulas/) combine product formulas with different $r$ in a linear combination to cancel error terms.
- **Interaction picture.** When one part of $H$ is much larger than the rest, [interaction picture simulation](/interaction-picture-simulation/) handles it apart.
- **Better bounds.** The [commutator scaling](/commutator-scaling/) bounds for every order show that product formulas are close to optimal for lattice Hamiltonians.

## When to use it

Use a product formula when the Hamiltonian is a sum of few local terms, the device has few qubits to spare, and the target error is moderate. Product formulas need no ancillas and no controlled operations, which makes them the usual choice on early devices and for lattice models, where their commutator bounds are strong. The second order formula is almost always better than the first order one at the same cost per step. For long times and small errors, consider the [higher-order Trotter-Suzuki](/higher-order-trotter-suzuki/) formulas or methods based on a [block encoding](/block-encoding/), whose cost grows as $\log(1/\epsilon)$. For a Hamiltonian with very many small terms, [qDRIFT](/qdrift/) can be cheaper.

## Pitfalls

- **Bounds with norms only.** A bound written with $\|H_j\|\|H_k\|$ instead of commutators is valid but ignores the structure, and it can ask for many more steps. For the Ising chain on 10 sites the norm-only constant $\sum_{j \ne k} \|H_j\|\|H_k\| = 19^2 - 19 = 342$ against $\alpha_1 = 36$, so it asks for about ten times more steps.
- **The bound is not the error.** Both bounds were about twice the true error in the example. Fault-tolerant resource estimates often use the bound, since the true error is hard to compute for large $n$.
- **Conventions of the rotation.** $R_z(\phi) = e^{-i\phi Z/2}$, so $e^{-i\theta Z}$ is $R_z(2\theta)$. A factor of 2 lost here doubles the effective time.
- **Order of the factors.** The list is applied from first to last, which in matrix notation is right to left. Mixing the two conventions changes the circuit, though not the order of the error.
- **Identity terms.** A term $c\,I$ only adds a global phase $e^{-ict}$. It can be dropped from the circuit, but not when the circuit is controlled, as in [quantum phase estimation](/quantum-phase-estimation/), where it shifts the measured phase.
- **Error norms.** The bounds are in the spectral norm of the unitary. Errors in states or expected values can be smaller, and errors of random methods are in the diamond norm of a channel; the numbers are not directly comparable.

## Implementations

## History

Trotter (1959) proved the product formula $e^{A+B} = \lim_r (e^{A/r}e^{B/r})^r$ for semigroups of operators, extending the Lie product formula for matrices. Strang (1968) proposed the symmetric splitting for difference schemes of partial differential equations and showed that it is second order accurate. Suzuki (1976) studied product formulas for quantum statistical mechanics and later (1990, 1991) gave the recursive formulas of every even order. Lloyd (1996) turned the product formula into a quantum algorithm for local Hamiltonians, and Berry, Ahokas, Cleve and Sanders (2007) analyzed the higher order formulas for quantum simulation. Childs, Su, Tran, Wiebe and Zhu (2021) proved the commutator bounds of every order, which explained why product formulas do much better on lattice models than the older norm bounds said. The formulas are also the base of other numerical methods for [ODE initial value problems](/ode-initial-value-problem/), next to [exponential integrators](/exponential-integrators/) and [operator splitting](/operator-splitting/).

## References
