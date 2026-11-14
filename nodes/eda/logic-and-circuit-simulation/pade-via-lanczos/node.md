---
tag: JW00K7
kind: algorithm
slug: pade-via-lanczos
name: Pade via Lanczos
aliases:
- PVL
- Feldmann-Freund PVL
area: eda/logic-and-circuit-simulation
level: advanced
summary: Feldmann and Freund's reduced-order model of a linear circuit that matches 2q moments of the transfer function stably using the nonsymmetric Lanczos process.
model: real-ram
complexity:
  vars: {N: the number of MNA unknowns, q: the number of Lanczos steps (the order of the model), F: the cost of one sparse LU factorization of G + s0 C, s: the cost of one solve with those factors plus one product with C}
  time: {worst: "O(F + q s + q N)"}
  space: {extra: "O(N + q)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1995
  people: [Peter Feldmann, Roland W. Freund]
  note: Feldmann and Freund computed the Padé approximant of a circuit transfer function with the nonsymmetric Lanczos process instead of from explicit moments, which removed the numerical limit on the order that AWE had.
prereqs: [asymptotic-waveform-evaluation, lanczos-algorithm, pade-approximation, ac-small-signal-analysis]
see_also: [prima, biconjugate-gradient, krylov-subspace, model-order-reduction, elmore-delay, passivity, transfer-function, circuit-noise-analysis]
sources:
  - paper: doi:10.1109/43.384428
    title: Peter Feldmann and Roland W. Freund, Efficient linear circuit analysis by Padé approximation via the Lanczos process, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 14(5), 639 to 649, 1995
    locator: the PVL algorithm, the theorem that q Lanczos steps give the Padé approximant with 2q matched moments, the look-ahead Lanczos process and the comparison with AWE
  - paper: doi:10.6028/jres.045.026
    title: Cornelius Lanczos, An iteration method for the solution of the eigenvalue problem of linear differential and integral operators, Journal of Research of the National Bureau of Standards 45(4), from page 255, 1950
    locator: the two-sided (biorthogonal) form of the process for a nonsymmetric matrix
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 7.1, Lanczos biorthogonalization (the recurrences, the biorthogonality and the breakdowns)
  - paper: doi:10.1109/43.45867
    title: Lawrence T. Pillage and Ronald A. Rohrer, Asymptotic waveform evaluation for timing analysis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 9(4), 352 to 366, 1990
    locator: the Padé model from explicit moments that PVL replaces
---

Padé via Lanczos (PVL) replaces a large linear circuit, such as an extracted interconnect, by a small model whose transfer function agrees with that of the circuit in its first $2q$ Taylor coefficients (moments) around an expansion point. It is the same Padé approximant that [asymptotic waveform evaluation](/asymptotic-waveform-evaluation/) computes, but Feldmann and Freund (1995) obtain it from $q$ steps of the nonsymmetric [Lanczos process](/lanczos-algorithm/), which never forms the moments and so stays accurate at orders where AWE fails. It belongs to the circuit simulation half of the logic and circuit simulation sub-area, next to [PRIMA](/prima/), which gives up some moments to keep passivity.

## In plain words

A long wire on a chip, cut into many small resistors, capacitors and inductors, has thousands of equations. Its effect at its two ends can usually be described by a formula with a few terms. Model order reduction finds such a formula.

AWE finds it by measuring a list of numbers, the moments, and fitting a fraction of two polynomials to them. The trouble is that the later moments all look alike, so in computer arithmetic they carry almost no new information, and the fit stops getting better after about eight terms. PVL builds the same fraction another way: it walks step by step through the directions that the circuit reaches from its input and from its output, keeping each new direction separate from the old ones. Each step adds one pole to the model, and the accuracy keeps improving.

## The problem

The circuit is linear, in [modified nodal analysis](/modified-nodal-analysis/) form in the Laplace domain, $(G + sC)x = b\,u$, with input $u$ and output $y = l^{\mathsf T} x$, so its [transfer function](/transfer-function/) is $H(s) = l^{\mathsf T}(G + sC)^{-1} b$. This is the matrix pair of [AC analysis](/ac-small-signal-analysis/). Choose an expansion point $s_0$ with $K = G + s_0 C$ nonsingular, and put $A = -K^{-1} C$ and $r = K^{-1} b$. Then

$$H(s_0 + \sigma) = l^{\mathsf T}(I - \sigma A)^{-1} r = \sum_{k \ge 0} m_k \sigma^k, \qquad m_k = l^{\mathsf T} A^k r.$$

The $m_k$ are the moments at $s_0$. Input: $G$, $C$, $b$, $l$, $s_0$ and the order $q$. Output: a model $H_q$ of order $q$ with $H_q(s_0 + \sigma) - H(s_0 + \sigma) = O(\sigma^{2q})$. This is the $[q-1/q]$ [Padé approximant](/pade-approximation/) of $H$ at $s_0$.

## The algorithm

```pseudo id=main
PVL(G, C, b, l, s₀, q)
L1  factor K = G + s₀C by sparse LU;  r ← K⁻¹ b
L2  v₁ ← r/ρ₁;  w₁ ← l/η₁;  d₁ ← w₁ᵀv₁;  if d₁ = 0 then report breakdown
L3  for k = 1, ..., q
L4      u ← A v_k = −K⁻¹(C v_k);  t ← Aᵀ w_k = −Cᵀ(K⁻ᵀ w_k)
L5      α_k ← w_kᵀ u / d_k;  β_k ← η_k d_k / d_{k−1};  γ_k ← ρ_k d_k / d_{k−1}   (β₁ = γ₁ = 0)
L6      ρ_{k+1} v_{k+1} ← u − α_k v_k − β_k v_{k−1};  η_{k+1} w_{k+1} ← t − α_k w_k − γ_k w_{k−1}
L7      d_{k+1} ← w_{k+1}ᵀ v_{k+1};  if d_{k+1} = 0 and k < q then report breakdown
L8  T_q ← the tridiagonal matrix with diagonal α₁..α_q, subdiagonal ρ₂..ρ_q, superdiagonal β₂..β_q
L9  return H_q(s) = (lᵀr) e₁ᵀ (I − (s − s₀) T_q)⁻¹ e₁
```

The right vectors $v_k$ span the [Krylov subspace](/krylov-subspace/) of $A$ and $r$, and the left vectors $w_k$ that of $A^{\mathsf T}$ and $l$. The coefficients make the two sequences biorthogonal, $w_i^{\mathsf T} v_j = 0$ for $i \ne j$, with three-term recurrences, as in the [biconjugate gradient method](/biconjugate-gradient/). The scale factors $\rho_{k+1}$ and $\eta_{k+1}$ are free; the code divides by the largest entry, which keeps rational arithmetic exact. Line L4 solves with $K$ and with $K^{\mathsf T}$, both with the factors of line L1, so the whole run costs one factorization.

The model is cheap to use. $H_q$ at any $s$ costs one tridiagonal solve of order $q$. Its poles are $s_0 + 1/\lambda$ for the nonzero eigenvalues $\lambda$ of $T_q$, and its residues come from the eigenvectors, which give a time-domain response as a sum of $q$ exponentials. In a circuit simulator the model is written back as a small set of equations and connected to the rest of the circuit.

## Example

**Two nodes by hand.** Node 1 has 1 S to ground and 1 S to node 2, each node has 1 F to ground, a current of 1 A enters node 1, and the output is the voltage of node 2. So $G = \begin{pmatrix} 2 & -1 \\ -1 & 1 \end{pmatrix}$, $C = I$, $b = e_1$, $l = e_2$, and $H(s) = 1/(s^2 + 3s + 1)$. At $s_0 = 0$, $A = -G^{-1}$ with $G^{-1} = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix}$, and the moments are $1, -3, 8, -21, 55$.

Step 1: $r = (1, 1)$, $v_1 = (1, 1)$, $w_1 = (0, 1)$, $d_1 = 1$. Then $A v_1 = (-2, -3)$ and $A^{\mathsf T} w_1 = (-1, -2)$, so $\alpha_1 = -3$. With $q = 1$ the model is $H_1 = 1/(1 + 3s)$, with moments $1, -3, 9$: two match, the third does not. Its pole $-1/3$ is the reciprocal of the [Elmore delay](/elmore-delay/) 3, against the dominant pole $(-3 + \sqrt 5)/2 = -0.382$ of the circuit.

Step 2: $v_2 = (-2, -3) + 3(1, 1) = (1, 0)$ and $w_2 = (-1, -2) + 3(0, 1) = (-1, 1)$, both with scale 1, and $d_2 = -1$: the left and right vectors are not equal and $d_2$ is negative, which a symmetric process would never give. $\beta_2 = \eta_2 d_2/d_1 = -1$, and $A v_2 = (-1, -1)$ gives $\alpha_2 = 0$. So $T_2 = \begin{pmatrix} -3 & -1 \\ 1 & 0 \end{pmatrix}$ and $e_1^{\mathsf T}(I - sT_2)^{-1} e_1 = 1/(1 + 3s + s^2)$: with $q = 2 = N$ the model is exact.

**An RC line.** 60 sections of 10 Ω and 10 fF, driven by a current source with 50 Ω and loaded by 1 MΩ, output at the far end, expanded at $s_0 = 0$. The table gives the largest error over 121 log-spaced frequencies from 1 MHz to 10 GHz, divided by the largest $|H|$, for PVL and for AWE in floating point (Padé from explicit moments by a Hankel solve):

| q | 1 | 2 | 4 | 6 | 8 | 12 | 16 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PVL | 0.17 | 0.025 | $1.3 \times 10^{-5}$ | $8.7 \times 10^{-11}$ | $6.4 \times 10^{-14}$ | $6.4 \times 10^{-14}$ | $6.4 \times 10^{-14}$ |
| AWE | 0.17 | 0.025 | $1.3 \times 10^{-5}$ | $5.0 \times 10^{-8}$ | $4.9 \times 10^{-8}$ | $5.1 \times 10^{-8}$ | $5.0 \times 10^{-8}$ |

The two agree while the moments carry information. From $q = 6$ AWE stalls near $5 \times 10^{-8}$, while PVL reaches rounding level.

**An RLC line.** 20 sections of 2 Ω, 1 nH and 1 pF (41 unknowns), with 25 Ω at the source and 50 Ω at the load, from 100 MHz to 3 GHz at 121 linear points, expanded at $s_0 = 2\pi \times 10^9\ \mathrm{s^{-1}}$. The band holds several resonances, so a low order cannot follow it:

| q | 12 | 16 | 20 | 24 | 30 |
| --- | --- | --- | --- | --- | --- |
| PVL | 0.31 | $5.7 \times 10^{-4}$ | $1.3 \times 10^{-7}$ | $1.9 \times 10^{-10}$ | $1.3 \times 10^{-11}$ |
| AWE | 0.31 | 0.014 | 0.018 | 0.094 | $3.3 \times 10^{4}$ |

At $q = 36$ the AWE Hankel solve meets a zero pivot: the explicit moments shrink by a factor near $10^{-10}$ per step and are 0 in floating point from $m_{34}$ on.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. **q = 1 in full.** $T_1 = (\alpha_1)$ with $\alpha_1 = m_1/m_0$, so $H_1 = m_0/(1 - \sigma \alpha_1)$ matches $m_0$ and $m_1$.
2. **Any q, without breakdown.** The vectors are biorthogonal; $A^j v_1 = V_q T_q^j e_1$ for $j < q$; and $W_q^{\mathsf T} A V_q = D_q T_q$ is the transpose of the left recurrence's matrix times $D_q$. Together these give $m_k = (l^{\mathsf T} r)\, e_1^{\mathsf T} T_q^k e_1$ for $k \le 2q - 1$. This is Feldmann and Freund's theorem, which they also prove with look-ahead.
3. $H_q$ has a numerator of degree at most $q - 1$ and a denominator of degree $q$, so it is the Padé approximant, the model of AWE; with $q = N$ it equals $H$.

Breakdown, rounding and passivity are not covered by the proof. The tests check, in exact rational arithmetic:

- The hand example, step by step.
- 40 random unsymmetric systems of order 3 to 6 (seed 91), every order $q \le N$, real expansion points from $-1$ to 2: the first $2q$ moments of the model equal the exact moments in every case, and moment $2q$ differs in all 141 cases with $q < N$.
- With seed 92, the model equals the AWE rational function at three rational points for each order.
- With seed 93, $q = N$ reproduces $H$ at three points.
- The transposed solve with the LU factors of $K$ equals a direct solve with $K^{\mathsf T}$ (seed 94).

In floating point they check the two lines above: PVL below $10^{-12}$ at $q = 8$ on the RC line and below $10^{-10}$ at $q = 30$ on the RLC line, while AWE stays above $10^{-9}$ and above $10^{-3}$.

## Complexity

Line L1 is one sparse factorization, cost $F$. Each step costs one solve with $K$, one with $K^{\mathsf T}$, two products with $C$ and $O(N)$ for the dot products and vector updates, so $q$ steps cost $O(F + q s + q N)$. Only the last two vectors of each sequence are kept, $O(N)$, and $T_q$ takes $O(q)$. Evaluating the model at $M$ frequencies costs $O(Mq)$ with a tridiagonal solver. AWE has the same cost for the moments; the difference is accuracy, not time. The implementation uses dense LU, so its $F$ is $O(N^3)$ and its $s$ is $O(N^2)$.

## Properties

- **Padé accuracy.** $2q$ moments from $q$ steps, the most that a model of order $q$ with $q - 1$ zeros can match.
- **Numerically stable in practice.** The vectors are rescaled at every step, and the recurrence orthogonalizes against the previous directions, so the information that AWE loses to rounding is kept. The tables are measurements, not a bound.
- **Not passive in general.** The model of a passive RLC circuit can have poles in the right half plane or produce energy at its ports. [Passivity](/passivity/) is not part of the Padé conditions.
- **One input and one output.** PVL is for a single transfer function; matrix-Padé variants with block Lanczos handle several ports.
- **The expansion point sets the band.** Accuracy is best near $s_0$ and fades with distance from it.

## Variants and improvements

- **Look-ahead Lanczos.** When $d_k$ is 0 or tiny, look-ahead steps over the gap with small blocks. Feldmann and Freund use this version.
- **Several ports.** A block version of the Lanczos process handles circuits with several inputs and outputs and matches block moments.
- **PRIMA.** The Arnoldi process and a congruence projection give passive models of RLC circuits at the price of matching $q$ block moments instead of $2q$: [PRIMA](/prima/).
- **Several expansion points.** Rational Krylov methods combine expansions at several $s_0$ to cover a wide band.

## When to use it

Use PVL to reduce a large linear network with one input and one output, such as an interconnect line or a filter, for a fast frequency or time response, or for many [noise](/circuit-noise-analysis/) or AC evaluations. Use it instead of AWE whenever more than a few poles are needed. When the model is connected back to a nonlinear circuit for transient simulation, prefer a passive method such as PRIMA, or check the poles and the passivity of the PVL model.

## Pitfalls

- **Breakdown.** $d_k = 0$ with nonzero vectors stops the plain process. The code reports it; a robust code needs look-ahead.
- **Unstable poles.** A model of a stable circuit can have a pole with positive real part, which turns into a growing exponential in a time-domain simulation. Discard or reflect such poles, or use a passive method.
- **Loss of biorthogonality.** In floating point the vectors drift away from biorthogonality, as in every Lanczos process. The accuracy can stall: on the RLC line with the expansion point at $2\pi \times 3 \times 10^9\ \mathrm{s^{-1}}$, the error stopped at $2.1 \times 10^{-5}$ from $q = 24$ to $q = 41$.
- **The expansion point.** $s_0 = 0$ suits RC circuits and step responses; resonant RLC lines need a point inside the band, or several points.
- **Comparing with AWE at low order.** At low order the two give the same model; the difference appears only where the explicit moments lose accuracy.

## Implementations

## History

Lanczos (1950) gave the two-sided process for nonsymmetric matrices, with left and right vectors that are biorthogonal. AWE (Pillage and Rohrer, 1990) made Padé approximation from moments a standard tool for interconnect analysis, but its explicit moments limit the useful order. Feldmann and Freund (1995) showed that the Lanczos process gives the same Padé approximant without the explicit moments, with look-ahead against breakdown, and named the method PVL. PVL gives no passivity guarantee, and PRIMA (1997 and 1998) was presented as a passive alternative.

## References
