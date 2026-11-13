---
tag: KW8GH0
kind: algorithm
slug: higher-order-trotter-suzuki
name: Higher-order Trotter-Suzuki formulas
aliases:
- Suzuki formulas
- Suzuki recursive product formulas
area: quantum/quantum-simulation
level: advanced
summary: "Suzuki's recursion S_2k(x) = S_(2k-2)(px)^2 S_(2k-2)((1-4p)x) S_(2k-2)(px)^2 builds product formulas of every even order 2k, with error O(t^(2k+1)/r^(2k)) and 5^(k-1) symmetric stages per step."
solves: [hamiltonian-simulation]
model: quantum-circuit-model
complexity:
  vars: {L: the number of terms, t: the evolution time, e: the error in the spectral norm, k: half the order, h: the spectral norm of H}
  time: {order_2k: O(5^(2k) L (L h t)^(1+1/(2k)) / e^(1/(2k))), best_k: O(L^2 h t exp(2 (ln 5 ln(L h t / e))^(1/2)))}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, ancilla_free: true, error_norm: spectral, negative_time_steps: true}
history:
  year: 1990
  people: [Masuo Suzuki]
  note: Suzuki gave the fractal recursion in 1990 and 1991. Berry, Ahokas, Cleve and Sanders (2007) analyzed it for quantum simulation and chose the order that minimizes the cost.
prereqs: [trotter-suzuki-product-formulas]
see_also: [lie-trotter-product-formula, commutator-scaling, multi-product-formulas, qdrift, optimal-hamiltonian-simulation, symplectic-integrators, operator-splitting, hamiltonian-simulation]
sources:
  - paper: doi:10.1016/0375-9601(90)90962-N
    title: Masuo Suzuki, Fractal decomposition of exponential operators with applications to many-body theories and Monte Carlo simulations, Physics Letters A 146(6), 1990, pages 319 to 323
    locator: the recursive construction of decompositions of every order
  - paper: doi:10.1063/1.529425
    title: Masuo Suzuki, General theory of fractal path integrals with applications to many-body theories and statistical physics, Journal of Mathematical Physics 32(2), 1991, pages 400 to 407
    locator: the general fractal scheme of every order and the theorem that some time steps must be negative for order 3 and above
  - paper: doi:10.1007/s00220-006-0150-x
    title: Dominic W. Berry, Graeme Ahokas, Richard Cleve and Barry C. Sanders, Efficient quantum algorithms for simulating sparse Hamiltonians, Communications in Mathematical Physics 270(2), 2007, pages 359 to 371 (arXiv:quant-ph/0508139)
    locator: Theorem 1 (number of exponentials), Lemma 1 (error of one step) and equation (8) (choice of r)
  - paper: doi:10.1103/PhysRevX.11.011020
    title: Andrew M. Childs, Yuan Su, Minh C. Tran, Nathan Wiebe and Shuchen Zhu, Theory of Trotter error with commutator scaling, Physical Review X 11(1), 2021, article 011020 (arXiv:1912.08854)
    locator: Theorem 11 and Corollary 12 (error and step count of a p-th order formula with nested commutators)
---

The higher-order Trotter-Suzuki formulas are product formulas for $e^{-iHt}$, $H = H_1 + \cdots + H_L$, whose error per step is $O(\delta^{2k+1})$ for any chosen $k$. Suzuki's recursion builds the formula $S_{2k}$ of order $2k$ from five copies of the formula of order $2k - 2$, run for the times $p\delta, p\delta, (1-4p)\delta, p\delta, p\delta$ with $p = 1/(4 - 4^{1/(2k-1)})$. The middle time $(1-4p)\delta$ is negative, so the circuit runs parts of the evolution backward. Starting from the symmetric second order step of the [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/), the formula of order $2k$ has $5^{k-1}$ symmetric stages. With $r$ steps the error is $O(t^{2k+1}/r^{2k})$, so the number of steps for error $\epsilon$ grows as $t^{1+1/(2k)}/\epsilon^{1/(2k)}$, close to linear in $t$. The price is the factor $5^{k-1}$ per step, and in practice orders 4 and 6 are the useful ones.

## In plain words

The symmetric product formula is accurate because it is a mirror image of itself, which cancels half of the error terms. Suzuki found a way to combine five copies of a mirror formula into a new mirror formula with a still smaller error. Four copies run forward for a little less than a quarter of the time each, and the middle copy runs backward for the missing amount, so the total time is right. The lengths are chosen so that the main errors of the five copies cancel. The new formula can be combined in the same way again, and every round makes the error shrink faster when the steps get shorter. Each round also makes one step five times longer, so high rounds only pay off for long times or very small errors.

## The problem

The input is a Hamiltonian $H = \sum_{j=1}^L c_j P_j$ given as a [Pauli string decomposition](/pauli-string-decomposition/) (or any sum of Hermitian terms whose exponentials we can apply), a time $t$, an error $\epsilon$ and an even order $2k \ge 2$. The output is a circuit $V$ of exponentials $e^{-i\theta P_j}$ with $\|V - e^{-iHt}\| \le \epsilon$ in the spectral norm. The task is [Hamiltonian simulation](/hamiltonian-simulation/).

## The algorithm

Write $x = -i\delta$ and $H_j = c_jP_j$. The second order step is
$$S_2(x) = e^{xH_1/2} \cdots e^{xH_{L-1}/2} \, e^{xH_L} \, e^{xH_{L-1}/2} \cdots e^{xH_1/2},$$
and for $k \ge 2$
$$S_{2k}(x) = S_{2k-2}(p_k x)^2 \, S_{2k-2}((1 - 4p_k)x) \, S_{2k-2}(p_k x)^2, \qquad p_k = \frac{1}{4 - 4^{1/(2k-1)}}.$$
Unfolding the recursion, $S_{2k}(x) = S_2(w_1x) \cdots S_2(w_m x)$ with $m = 5^{k-1}$ weights $w_i$. WEIGHTS computes them; SUZUKI lays out the circuit, whose pairs $(P, \theta)$ mean $e^{-i\theta P}$, applied in the order of the list.

```pseudo id=main
WEIGHTS(order)                                         ▷ order = 2k, even
L1  if order = 2 then
L2      return [1]
L3  p ← 1 / (4 - 4^(1/(order - 1)))
L4  w ← WEIGHTS(order - 2)
L5  return p·w, p·w, (1 - 4p)·w, p·w, p·w              ▷ five lists joined, 5^(k-1) weights

SUZUKI(((c_1, P_1), ..., (c_L, P_L)), t, r, order)
L6  δ ← t / r
L7  repeat r times
L8      for each weight w in WEIGHTS(order)
L9          for j ← 1 to L - 1: append (P_j, c_j w δ / 2)
L10         append (P_L, c_L w δ)
L11         for j ← L - 1 down to 1: append (P_j, c_j w δ / 2)
L12 replace each run of neighbors with the same string (P, θ), (P, θ') by (P, θ + θ')
L13 return the list
```

Line L3 uses $2k - 1 = $ order $- 1$. Lines L9 to L11 are the symmetric step $S_2(w\delta)$ for one weight. Line L12 joins the last half exponential of $H_1$ of each stage with the first one of the next stage, so $r$ steps cost
$$2(L-1)\,5^{k-1}\,r + 1$$
exponentials. The weights add up to 1, and some of them are negative: for order 4 they are $p_2 = 0.41449$ four times and $1 - 4p_2 = -0.65796$ in the middle. For order 6, 25 weights, the most negative is $-0.24546$.

## Example

Take $H = ZZ + 0.8\,XI + 0.8\,IX$ on two qubits (the last letter acts on qubit 0). The page's simulator computes the exact $e^{-iHt}$ by eigendecomposition, checked against a scaled Taylor series with squaring, and the spectral norm of the error of each formula.

**Order 4 for $r = 1$.** With $p = 0.41449$ and $q = -0.65796$, the step is $S_2(p\delta)S_2(p\delta)S_2(q\delta)S_2(p\delta)S_2(p\delta)$. Each $S_2$ is 5 exponentials, $(ZZ, w/2), (XI, 0.4w), (IX, 0.8w), (XI, 0.4w), (ZZ, w/2)$ for $\delta = 1$, and the four joins of $ZZ$ between stages leave $2 \cdot 2 \cdot 5 + 1 = 21$ exponentials. The middle stage has the time $q\delta < 0$.

**Errors as $r$ doubles, at $t = 1$.**

| $r$ | order 2 | order 4 | ratio | order 6 | ratio |
|---|---|---|---|---|---|
| 1 | 0.6353 | 0.05138 | | 5.202e-4 | |
| 2 | 0.1325 | 2.344e-3 | 21.9 | 5.331e-6 | 97.6 |
| 4 | 0.03129 | 1.424e-4 | 16.5 | 7.630e-8 | 69.9 |
| 8 | 7.708e-3 | 8.865e-6 | 16.1 | 1.167e-9 | 65.4 |
| 16 | 1.920e-3 | 5.537e-7 | 16.0 | 1.814e-11 | 64.3 |

The ratios tend to $2^4 = 16$ and $2^6 = 64$, the orders 4 and 6.

**Cost for a target error.** The least $r$ with true error at most $\epsilon$ (found by a search over $r$), and the number of exponentials:

| $t$ | $\epsilon$ | order 2 | order 4 | order 6 |
|---|---|---|---|---|
| 1 | 0.1 | 3 steps, 13 | 1 step, 21 | 1 step, 101 |
| 1 | 1e-3 | 23 steps, 93 | 3 steps, 61 | 1 step, 101 |
| 1 | 1e-6 | 701 steps, 2805 | 14 steps, 281 | 3 steps, 301 |
| 4 | 0.1 | 13 steps, 53 | 4 steps, 81 | 2 steps, 201 |
| 4 | 1e-3 | 127 steps, 509 | 12 steps, 241 | 4 steps, 401 |
| 4 | 1e-6 | 4010 steps, 16041 | 69 steps, 1381 | 11 steps, 1101 |

At $\epsilon = 0.1$ the second order formula is the cheapest; at $\epsilon = 10^{-3}$ order 4 is; order 6 wins only at $t = 4$ and $\epsilon = 10^{-6}$.

## Correctness

Two facts carry the proof. First, $S_2$ is symmetric, $S_2(x)S_2(-x) = I$, and the palindromic recursion keeps this, so each $S_{2k}(x) = e^{F(x)}$ with an odd function $F$: the error terms of even degree vanish. Second, if $S_{2k-2}(y) = e^{yH + y^{2k-1}E + O(y^{2k+1})}$, then the five stages multiply to $e^{xH + (4p^{2k-1} + (1-4p)^{2k-1})x^{2k-1}E + O(x^{2k})}$, and the choice of $p$ makes $4p^{2k-1} + (1-4p)^{2k-1} = 0$. Oddness removes the term of degree $2k$, so $S_{2k}(x) = e^{xH + O(x^{2k+1})}$. Every stage is unitary for real $\delta$, so errors of the $r$ steps add, giving $O(t^{2k+1}/r^{2k})$. The full proof is below.

## Complexity

- **Explicit bound (Berry, Ahokas, Cleve and Sanders 2007, Lemma 1).** Let $\tau = \|H\|t$ and assume every term has $\|H_j\| \le \|H\|$. If $4L5^{k-1}\tau/r \le 1$ and $(16/3)(2 \cdot 5^{k-1}L\tau)^{2k+1}/r^{2k} \le 1$, then $\|S_{2k}(-it/r)^r - e^{-iHt}\| \le 5(2 \cdot 5^{k-1}L\tau)^{2k+1}/r^{2k}$.
- **Steps and exponentials (their equation (8) and Theorem 1).** With $r = \lceil 4 \cdot 5^{k-1/2}(L\tau)^{1+1/(2k)}/\epsilon^{1/(2k)} \rceil$ the error is at most $\epsilon$, and the number of exponentials is at most $2L5^{2k}(L\tau)^{1+1/(2k)}/\epsilon^{1/(2k)}$. The factor $5^{2k}$ grows with $k$ while the factor $(L\tau/\epsilon)^{1/(2k)}$ shrinks. The best choice is $k \approx \frac12\sqrt{\log_5(L\tau/\epsilon)} + 1$, which gives $4L^2\tau\, e^{2\sqrt{\ln 5\,\ln(L\tau/\epsilon)}}$ exponentials, that is $L^2\tau$ times a factor that grows slower than any power of $L\tau/\epsilon$.
- **These bounds are loose.** For the example at $t = 1$ ($\|H\| = 1.887$), equation (8) asks for $r = 2196$ at order 4 and $\epsilon = 10^{-3}$, where 3 steps suffice. Bounds with nested commutators (see [commutator scaling](/commutator-scaling/)) are much closer: Childs, Su, Tran, Wiebe and Zhu (2021) give error $O(\tilde\alpha_{\mathrm{comm}} t^{p+1}/r^p)$ for a formula of order $p$, where $\tilde\alpha_{\mathrm{comm}}$ is a sum of norms of nested commutators of depth $p + 1$.
- **Qubits.** The $n$ system qubits; no ancillas.

## Properties

- **Negative times.** For order 3 and above, every product formula of this kind has some negative times (Suzuki 1991). On a quantum computer this costs nothing, since $e^{+i\theta P}$ is as easy as $e^{-i\theta P}$. For dissipative equations, such as diffusion, it makes the formulas unstable, which is why numerical analysts use other methods there.
- **Symmetric.** $S_{2k}(x)S_{2k}(-x) = I$ for every $k$.
- **Exact for commuting terms.** If all $H_j$ commute, every stage is exact and so is the formula.
- **Unitary.** Each stage is unitary, so errors add linearly over steps and never grow faster.
- **Only even orders.** The recursion raises the order by 2 at each level, because the odd terms cancel by symmetry.

## Variants and improvements

- **Other coefficients.** The fivefold recursion is not the only one. A threefold recursion $S(p x)S((1-2p)x)S(p x)$ with $p = 1/(2 - 2^{1/(2k-1)})$ also raises the order by 2 with $3^{k-1}$ stages, but its middle step is longer and its error constant larger. Formulas found by solving the order conditions numerically have fewer stages for orders 4, 6 and 8.
- **Multi-product formulas.** [Multi-product formulas](/multi-product-formulas/) reach high order by a linear combination of low-order formulas instead of a product.
- **Randomized and commutator-aware variants.** Random orderings of the terms and the commutator bounds of [commutator scaling](/commutator-scaling/) lower the step counts in practice. [qDRIFT](/qdrift/) samples the terms instead.
- **Methods beyond product formulas.** For very small $\epsilon$, [optimal Hamiltonian simulation](/optimal-hamiltonian-simulation/) has cost additive in $t$ and $\log(1/\epsilon)$, at the price of ancilla qubits.

## When to use it

Use order 4, sometimes order 6, when the simulation is long or the error target small, and the device should have no ancillas. For a lattice model and a fault-tolerant cost, order 4 or 6 with commutator bounds is often the cheapest product formula. For short times or moderate errors the second order formula is cheaper, as the tables show, because the extra stages are not paid back. Orders above 8 almost never pay off.

## Pitfalls

- **Higher order is not always better.** Each order multiplies the cost of a step by 5. At $t = 1$ and $\epsilon = 0.1$ in the example the second order formula needs 13 exponentials and order 6 needs 101.
- **Large steps.** The error of a high order formula is small only when the step is small. At $t = 4$ with order 4, the error is 0.2196 for $r = 1$ and 1.298 for $r = 2$: it is not monotone in $r$ until the steps are short enough. Do not extrapolate from one large step.
- **The bound is not the error.** The explicit bounds can be off by orders of magnitude; equation (8) of Berry and others asks for 2196 steps where 3 suffice in the example. Use commutator bounds or numerical checks on small sizes when the constant matters.
- **Order numbering.** Berry, Ahokas, Cleve and Sanders call $S_{2k}$ the formula of order $k$. This page calls it order $2k$, as Suzuki and most later work do.
- **Rounding of weights.** The order conditions $\sum w_i = 1$ and $\sum w_i^{m} = 0$ for odd $m < 2k$ are cancellations of numbers of both signs. Compute $p_k$ in floating point and do not round it to a few digits.

## Implementations

## History

Suzuki (1990, 1991) gave the fractal recursion, which builds decompositions of exponential operators of every order from a symmetric one, and proved that for order 3 and above some of the time steps must be negative. Yoshida (1990) found the same kind of construction for symplectic integrators of classical [Hamiltonian systems](/hamiltonian-systems/). In quantum computing, Berry, Ahokas, Cleve and Sanders (2007) used Suzuki's formulas to simulate sums of terms with $O((L\|H\|t)^{1+1/(2k)})$ exponentials and chose $k$ to minimize the cost. Childs, Su, Tran, Wiebe and Zhu (2021) proved error bounds of every order with nested commutators, which explained why the formulas are much better on local Hamiltonians than the norm bounds say.

## References
