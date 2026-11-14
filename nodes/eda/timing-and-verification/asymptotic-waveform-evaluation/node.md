---
tag: 5A3DBS
kind: algorithm
slug: asymptotic-waveform-evaluation
name: Asymptotic waveform evaluation
aliases:
- AWE
area: eda/timing-and-verification
level: advanced
summary: Pillage and Rohrer's reduced model of a linear circuit that matches 2q moments of its response by a q-pole Pade approximation.
solves: [model-order-reduction]
model: real-ram
complexity:
  vars: {n: the number of nodes of the circuit, q: the number of poles of the model, I: the number of sweeps of the root finder}
  time: {worst: Θ(n³ + q n² + q³ + I q²), average: Θ(n³ + q n² + q³ + I q²), best: Θ(n³ + q n² + q³ + I q²)}
  space: {extra: Θ(n² + q²)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1990
  people: [Lawrence T. Pillage, Ronald A. Rohrer]
  note: Pillage and Rohrer matched the first 2q moments of a linear circuit with q poles and made the moment method a standard tool for interconnect delay. The one-pole case is the Elmore delay of 1948.
prereqs: [rc-tree, elmore-delay, pade-approximation]
see_also: [prima, transfer-function, durand-kerner-method, partial-fraction-decomposition, routh-hurwitz-criterion, neumann-series, cramers-rule, parasitic-extraction]
sources:
  - paper: doi:10.1109/43.45867
    title: Lawrence T. Pillage and Ronald A. Rohrer, Asymptotic waveform evaluation for timing analysis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 9(4), 352 to 366, 1990
    locator: the moment recurrence, the Padé approximation with q poles from 2q moments, the residues and the step response
  - paper: doi:10.1063/1.1697872
    title: W. C. Elmore, The transient response of damped linear networks with particular regard to wideband amplifiers, Journal of Applied Physics 19(1), 55 to 63, 1948
    locator: the first moment of the impulse response as a delay, the one-pole case of AWE
---

Asymptotic waveform evaluation (AWE) replaces a large linear RC or RLC circuit, such as an [RC tree](/rc-tree/) of an extracted wire, by a small model with $q$ poles. It computes the moments of the transfer function, the coefficients of its Taylor series at $s = 0$, by repeated solves with the conductance matrix. From $2q$ moments it builds the [Padé approximation](/pade-approximation/) $P(s)/Q(s)$ with $q$ poles, then the poles, the residues and the response in closed form. Pillage and Rohrer published it in 1990. With $q = 1$ it gives the [Elmore delay](/elmore-delay/). With $q = n$ it gives the exact transfer function. In between, the model can have unstable poles although the circuit is stable.

## In plain words

A wire with many resistors and capacitors responds to a step at its input with a smooth rise at its output. The exact rise is a sum of many decaying exponentials, one per node. AWE keeps only a few of them.

It does not simulate the circuit in time. It solves for the voltages once at DC, and then again with the capacitors fed by the previous solution, a few times. Each solve gives one number, a moment. From $2q$ moments it fits a ratio of two polynomials that has $q$ poles and agrees with the first $2q$ moments. The poles and residues of this ratio give a formula for the response, from which the delay at 50 percent can be read.

## The problem

The input is a linear circuit in nodal form,
$$ (G + sC) \, x(s) = b \, u(s), \qquad y(s) = l^T x(s), $$
with $n \times n$ real matrices $G$ (conductances, invertible) and $C$ (capacitances), an input vector $b$, an output vector $l$, and an order $q$. The transfer function is $H(s) = l^T (G + sC)^{-1} b$, and its expansion at $s = 0$ is
$$ H(s) = \sum_{k \ge 0} m_k s^k, \qquad m_k = l^T (-G^{-1} C)^k G^{-1} b. $$
The output is a rational function $P(s)/Q(s)$ with $\deg P \le q - 1$, $\deg Q \le q$ and $Q(0) = 1$ whose expansion agrees with $m_0, \ldots, m_{2q-1}$, together with its poles $p_i$ (the roots of $Q$) and residues $k_i$. This is a [model order reduction](/model-order-reduction/) problem: a model of order $q$ for a circuit of order $n$.

## The algorithm

```pseudo id=main
AWE(G, C, b, l, q)
L1  x_0 ← G⁻¹ b                                          ▷ the DC solution, one LU of G
L2  for k ← 1 to 2q − 1 do x_k ← G⁻¹ (−C x_{k−1})         ▷ reuse the LU of G
L3  m_k ← lᵀ x_k for k = 0 .. 2q − 1                      ▷ the moments
L4  b_0 ← 1; solve Σ_{j=1..q} b_j m_{k−j} = −m_k for k = q .. 2q − 1
L5  a_k ← Σ_{j=0..k} b_j m_{k−j} for k = 0 .. q − 1
L6  p_1 .. p_q ← the roots of Q(s) = Σ_{j=0..q} b_j s^j
L7  k_i ← P(p_i) / Q′(p_i) for i = 1 .. q, where P(s) = Σ_k a_k s^k
L8  return P, Q, the poles p_i and the residues k_i
```

Lines L1 to L3 compute the moments. Line L4 is the Hankel system of the Padé approximation: it makes the coefficients of $s^q, \ldots, s^{2q-1}$ in $Q(s) H(s)$ vanish. Line L5 takes the low-order part of $Q(s) H(s)$ as the numerator. Line L6 finds the poles, for example by the [Durand-Kerner method](/durand-kerner-method/). Line L7 is the [partial fraction decomposition](/partial-fraction-decomposition/) $P/Q = \sum_i k_i/(s - p_i)$ for simple poles. The response to a unit step is then
$$ y(t) = m_0 + \sum_{i=1}^q \frac{k_i}{p_i} e^{p_i t}. $$
The implementation computes lines L1 to L5 in exact rational arithmetic and lines L6 and L7 in floating point. It checks the stability of $Q$ exactly by the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/).

## Example

**A stable model.** Take a ladder of three sections, with $R = (1, 1, 1)$, $C = (1, 2, 1)$ and a unit step source at its left end, and the output at the far end. The DC solution is all ones, so $m_0 = 1$, and the moments are $1, -8, 56, -386, 2656, -18272$. The Elmore delay is $-m_1 = 1 \cdot 1 + 2 \cdot 2 + 1 \cdot 3 = 8$.

| $q$ | $P(s)$ | $Q(s)$ | poles | 50 percent delay |
| --- | --- | --- | --- | --- |
| 1 | $1$ | $1 + 8s$ | $-0.125$ | $8 \ln 2 = 5.5452$ |
| 2 | $1 - s/4$ | $1 + \tfrac{31}{4} s + 6 s^2$ | $-0.1454$, $-1.1463$ | 5.9428 |
| 3 | $1$ | $1 + 8s + 8s^2 + 2s^3$ | $-0.1454$, $-1.4030$, $-2.4516$ | 5.9404 |

For $q = 2$, line L4 solves $-8 b_1 + b_2 = -56$ and $56 b_1 - 8 b_2 = 386$, so $b_1 = 31/4$ and $b_2 = 6$, and line L5 gives $a_0 = 1$ and $a_1 = -8 + 31/4 = -1/4$. The model with $q = 3$ is the exact transfer function. The two-pole model has the right dominant pole to four digits and a 50 percent delay within 0.04 percent of the exact 5.9404. The one-pole model is 6.7 percent early here.

**An unstable model.** Take the same circuit with the output at the middle node. The moments are $1, -7, 48, -330$, and line L4 solves $-7 b_1 + b_2 = -48$ and $48 b_1 - 7 b_2 = 330$, so $Q(s) = 1 + 6s - 6s^2$. Its roots are $-0.1455$ and $+1.1455$. The model has a pole in the right half-plane, and its step response grows without bound, although every pole of the circuit is negative. The model with $q = 3$ at this node is exact and stable.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Moments.** Lines L1 to L3 give the Taylor coefficients of $H$ at 0, by the [Neumann series](/neumann-series/) of $(I + s G^{-1} C)^{-1}$.
- **2q moments are matched.** If the Hankel matrix of line L4 is invertible, then $H - P/Q = O(s^{2q})$, and $P/Q$ is the only rational function of that type with this property.
- **q = n is exact.** By [Cramer's rule](/cramers-rule/), $H = N/D$ with $D = \det(G + sC)$ of degree at most $n$ and $\deg N \le n - 1$, so with $q = n$ the model is $H$ itself and $Q = D/D(0)$.
- **Residues and the step response.** For simple poles, line L7 gives the partial fractions, the step response has the form above, and $y(0) = 0$.
- **Elmore delay.** For an RC tree, $m_0 = 1$ and $-m_1$ is the Elmore delay at the output.
- **Stability is not guaranteed.** The unstable example above is a proof that AWE with $q = 2$ can give a pole in the right half-plane for a stable RC tree.

What is proved is the matching of moments, not an error bound on the waveform or the delay for $q < n$. The rest is measured. On 300 random RC trees with 3 to 6 nodes and integer $R$ and $C$ from 1 to 9 (Python `random.Random(9)`), at all 1296 outputs, the model with $q = 2$ was unstable at 112 outputs (8.6 percent). At the other 1184, the mean relative error of the 50 percent delay against the exact model was 3.1 percent for $q = 2$ and 46 percent for $q = 1$. The error was more than 10 percent at 44 outputs for $q = 2$ and at 541 for $q = 1$. The worst cases were near the driver, where a slow pole with a small residue appears.

## Complexity

- **Moments.** With dense matrices, one LU factorization of $G$ costs $\Theta(n^3)$, and each of the $2q$ moments costs $\Theta(n^2)$ for a product with $C$ and two triangular solves. For an RC tree, $G$ is a tree Laplacian plus a diagonal, and each moment takes $\Theta(n)$ time by two passes over the tree, as in the Elmore delay.
- **Padé and residues.** The Hankel system costs $\Theta(q^3)$, the numerator $\Theta(q^2)$, and each sweep of the root finder $\Theta(q^2)$. No bound on the number of sweeps is proved here. In practice $q$ is 2 to 4, so this part is small.
- **Space.** The LU factors take $\Theta(n^2)$ for dense matrices, and only two moment vectors are needed at a time.
- **Compared with simulation.** A time-domain simulation solves one linear system per time step, and needs many steps to resolve the fastest and the slowest time constants. AWE needs $2q$ solves with one matrix.

## Properties

- **Not exact for $q < n$.** It is an approximation of the transfer function near $s = 0$, so it is good for the slow parts of the response and less good for the start of the step response.
- **The moments are exact.** In exact arithmetic, the first $2q$ moments of the model equal those of the circuit.
- **Not stable in general.** The Padé approximation does not keep the stability of the circuit, as the example shows. The model also need not be passive, so it can make a larger circuit unstable when it is connected to other parts.
- **Ill-conditioned in floating point.** The moments grow or shrink like powers of the time constants, so the Hankel matrix becomes nearly singular as $q$ grows. In floating point, AWE is useful only for small $q$. The implementation here avoids this problem by exact arithmetic, which costs more time.

## Variants and improvements

- **Moment shifting and frequency scaling.** Expand at a point $s_0 \ne 0$, or scale $s$, to reduce the spread of the moments.
- **Complex frequency hopping.** Expand at several points and combine the poles found near each of them.
- **Krylov methods.** The moments span the Krylov subspace of $-G^{-1}C$ and $G^{-1}b$. Padé via Lanczos (PVL) of Feldmann and Freund computes the same Padé model from a Lanczos process without forming the moments. [PRIMA](/prima/) uses an Arnoldi basis and a congruence transform, matches $q$ block moments instead of $2q$, and keeps the model passive.
- **Closed-form delay metrics.** Formulas in the first two or three moments of an RC tree give fast delay estimates that are always defined, with no poles to compute.

## When to use it

- To get a delay and a slew of an RC or RLC interconnect that is more accurate than the Elmore delay, with a cost of a few linear solves.
- For a few low-order models where the result is checked for stability, and where a lower order is used if it is not stable.
- Not when the reduced model is connected back to a simulator and must be passive. Use PRIMA or a similar projection method.

## Pitfalls

- **Unstable poles.** Always check the poles. A model with a pole in the right half-plane, as in the example, has a response that grows without bound. The usual fix is to use a lower order, or to drop the unstable poles and refit the residues.
- **Singular Hankel matrix.** With one capacitor, the moments are $(-\tau)^k$ and the Hankel matrix for $q = 2$ is singular. A circuit with fewer distinct poles than $q$ has no model with $q$ poles.
- **Rounding of the moments.** In floating point, the moments must be scaled, or the Hankel matrix is singular to working precision already for small $q$.
- **Multiple poles.** Line L7 assumes simple poles. For a double pole the response has a term $t e^{pt}$, and the residue formula divides by $Q'(p) = 0$.

## Implementations

## History

Elmore (1948) used the first moment of the impulse response as the delay of an amplifier, which is the case $q = 1$. Padé approximation of a series is much older. Pillage and Rohrer (1990) used the moments of the circuit equations to build models with $q$ poles for the timing analysis of interconnect, and AWE was widely used for RC and RLC delay calculation in the 1990s. The problems with stability and with conditioning led to Krylov-subspace methods such as PVL (1995) and PRIMA (1998).

## References
