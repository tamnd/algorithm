---
tag: QN7FSW
kind: algorithm
slug: semidefinite-relaxation-detection
name: Semidefinite relaxation detection
aliases:
- SDR detector
area: communications/mimo-communications
level: advanced
summary: Relaxes ML detection of BPSK or 4-QAM vectors to a semidefinite program over matrices with unit diagonal, solves it, and rounds the solution to a symbol vector, with a lower bound that can prove ML.
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {N: the number of real binary symbols, m: the number of real receive dimensions, k: the rank of the low-rank factor, T: the number of mixing sweeps, J: the number of Jacobi sweeps, R: the number of rounding draws}
  time: {worst: O(N^2 m + T N^2 k + J N^3 + R N^2)}
  space: {extra: O(N^2 + N m)}
properties: {deterministic: "for a fixed seed", exact_ml: false, exact_without_noise: true, gives_lower_bound: true, certifies_ml_when_tight: true, constellations: "BPSK and 4-QAM", needs_noise_level: false}
history:
  year: 2001
  people: [Peter H. Tan, Lars K. Rasmussen]
  note: "Tan and Rasmussen applied semidefinite programming to multiuser detection in CDMA in 2001, and Ma, Davidson, Wong, Luo and Ching studied it as a quasi-ML detector in 2002."
prereqs: [mimo-detection, semidefinite-programming, convex-relaxation]
see_also: [maximum-cut, randomized-rounding, lagrangian-duality, jacobi-eigenvalue-algorithm, coordinate-descent, lattice-reduction-aided-detection, k-best-detector, interior-point-method]
sources:
  - paper: doi:10.1109/49.942507
    title: Peter H. Tan and Lars K. Rasmussen, The application of semidefinite programming for detection in CDMA, IEEE Journal on Selected Areas in Communications 19(8), 1442-1449, 2001
    locator: the semidefinite relaxation of binary multiuser detection and its randomized rounding
  - paper: "Wing-Kin Ma, Timothy N. Davidson, Kon Max Wong, Zhi-Quan Luo and Pak-Chung Ching, Quasi-maximum-likelihood multiuser detection using semi-definite relaxation with application to synchronous CDMA, IEEE Transactions on Signal Processing 50(4), 912-922, 2002"
    locator: the SDR detector as a quasi-ML detector and its comparison with ML
  - paper: "Joakim Jaldén and Björn Ottersten, The diversity order of the semidefinite relaxation detector, IEEE Transactions on Information Theory 54(4), 1406-1422, 2008"
    locator: the proof that SDR has the diversity order of ML for BPSK over real-valued i.i.d. Rayleigh fading
  - paper: doi:10.1145/227683.227684
    title: Michel X. Goemans and David P. Williamson, Improved approximation algorithms for maximum cut and satisfiability problems using semidefinite programming, Journal of the ACM 42(6), 1115-1145, 1995
    locator: the random hyperplane rounding of the vectors of a semidefinite solution
---

Semidefinite relaxation (SDR) detection is an approximate method for the [MIMO detection](/mimo-detection/) problem with binary symbols: BPSK, or 4-QAM, which is BPSK in each real dimension. ML detection then minimizes a quadratic form over the corners $\{-1, +1\}^N$ of a cube, a problem of the same kind as [maximum cut](/maximum-cut/) and NP-hard in general. SDR writes the quadratic form with the rank-one matrix $v v^T$ and replaces that matrix by any positive semidefinite matrix with a unit diagonal. The result is a [semidefinite program](/semidefinite-programming/), a [convex relaxation](/convex-relaxation/) that is solvable in polynomial time. Its value is a lower bound on the ML metric. A rounding step turns its solution into a symbol vector. When the rounded vector has a metric equal to the lower bound, the vector is proved to be ML (a theorem). The implementation is a teaching solver, described below.

## In plain words

The receiver must choose a sign, plus or minus, for each of several signals so that the total error is smallest. Trying every choice takes too long. The receiver first solves an easier problem, where each sign may be any arrow of length one in a space with a few dimensions, not only plus or minus. The easier problem has no traps and can be solved well. Its best error is never larger than the best error of the real problem. Then the receiver cuts the space with random flat walls and gives each signal the sign of the side its arrow is on. If the result is as good as the lower limit, the receiver knows it has the best answer.

## The problem

The model is $y = H x + w$ with $H \in \mathbb{C}^{m_c \times n_c}$ known, $x$ a vector of BPSK or 4-QAM points, and $w \sim \mathcal{CN}(0, N_0 I)$. In the real-valued form (as on the [LR-aided detection](/lattice-reduction-aided-detection/) page), every real symbol is $a\, b_i$ with $b_i \in \{-1, +1\}$, where $a = 1$ for BPSK and $a = 1/\sqrt 2$ for unit-energy 4-QAM. With $G = a H_r$ (an $m \times N$ real matrix) and the real received vector $y_r$, ML detection is

$$\min_{b \in \{-1, +1\}^N} \|y_r - G b\|^2.$$

With one more sign $t$ and $v = (b, t) \in \{-1, +1\}^{N+1}$,

$$\|y_r - G (t b)\|^2 = v^T Q v, \qquad Q = \begin{pmatrix} G^T G & -G^T y_r \\ -y_r^T G & y_r^T y_r \end{pmatrix},$$

so $b$ is recovered from an optimal $v$ as $t\, b$ (a closed form). The SDR is

$$\min\ \mathrm{tr}(Q X) \quad \text{subject to} \quad X_{ii} = 1, \ X \succeq 0,$$

whose dual is $\max \sum_i \lambda_i$ subject to $Q - \mathrm{Diag}(\lambda) \succeq 0$ (by [Lagrangian duality](/lagrangian-duality/)).

## The algorithm

```pseudo id=main
SDR-DETECT(y, H, S, R)
L1  (G, y_r) ← REAL-VALUED MODEL(y, H)             ▷ x = a b with b in {-1, +1}^N
L2  Q ← the homogeneous matrix of (G, y_r)
L3  repeat for T sweeps or until the vectors stop moving
L4      for i ← 0 to N: u_i ← -g / ‖g‖ with g = Σ_{j≠i} Q_ij u_j    ▷ mixing method, X = U Uᵀ
L5  λ_i ← (Q U Uᵀ)_ii for each i
L6  lower ← Σ λ_i + (N + 1) λ_min(Q - Diag(λ))      ▷ a valid dual bound
L7  b ← (sign(u_i · u_N))_{i<N}                     ▷ deterministic rounding
L8  repeat R times: draw r ~ N(0, I); b ← sign(u_N · r) (sign(u_i · r))_{i<N}; keep the b with the smallest metric
L9  return the points a b as constellation indices, and the bound
```

An interior-point method solves the SDR to any accuracy in polynomial time, but it is long to write. The teaching solver of lines L3 and L4 is the mixing method: it writes $X = U U^T$ with unit rows $u_i \in \mathbb{R}^k$, so the diagonal constraint holds by construction, and it minimizes $\mathrm{tr}(Q U U^T)$ over one $u_i$ at a time. With the others fixed, the objective is $2 u_i \cdot g + \text{const}$, which $u_i = -g / \|g\|$ minimizes exactly. The rank is $k = \lceil \sqrt{2 (N + 1)} \rceil + 1$, enough to hold an optimal solution, because some optimal $X$ has a rank $r$ with $r (r + 1) / 2 \le N + 1$ (a theorem of Barvinok and Pataki). The solver does not prove that it reached the optimum. Lines L5 and L6 make that unnecessary for the bound: for any unit vectors, $\lambda + \lambda_{\min} \mathbf 1$ is dual feasible, so line L6 is a valid lower bound on the SDR value and so on the ML metric. The smallest eigenvalue comes from the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/).

Line L8 is the random hyperplane rounding of Goemans and Williamson: each vector gets the sign of its side of a random hyperplane, relative to the side of $u_N$, the vector of $t$. This is a form of [randomized rounding](/randomized-rounding/).

## Example

Take BPSK over $H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$ and $y = (0.5, 0.6)$, the example of the [ZF page](/zero-forcing-mimo-detector/), sent with $x = (+1, -1)$. Here $N = 2$ and

$$Q = \begin{pmatrix} 5 & 3 & -1.6 \\ 3 & 2 & -1.1 \\ -1.6 & -1.1 & 0.61 \end{pmatrix}.$$

The four sign vectors have the metrics 0.61 for $(+1, -1)$, 2.61, 8.21 and 19.01, so ML gives $(+1, -1)$ with 0.61. The solver of the implementation (seed 0) stops after 25 sweeps with $\mathrm{tr}(Q X) \approx 0.59720$, and line L6 gives the lower bound $\approx 0.59720$, so the SDR value is about 0.5972 (a measurement on this example). It is below 0.61, so the relaxation is not tight here, and no rank-one matrix is optimal. The rounding still returns $(+1, -1)$, the ML vector, with metric 0.61. The bound shows that no vector can have a metric below 0.5972, but it cannot prove that 0.61 is optimal; the brute-force list above does.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows the homogeneous form $v^T Q v = \|y_r - G (t b)\|^2$ (a closed form), that the SDR value is at most the ML metric (a theorem), and that line L6 is a lower bound on the SDR value for any unit vectors, by weak duality (a theorem). So if the rounded vector has a metric equal to the bound, it is an ML vector (a theorem). It shows that each update of line L4 does not increase the objective (a theorem). Without noise and with $G$ of full column rank, the only optimal $X$ is $v v^T$ for the transmitted $v$, and the rounding of that matrix returns the transmitted vector (a theorem).

Jaldén and Ottersten (2008) proved that SDR detection has the same diversity order as ML detection for BPSK over real-valued i.i.d. Rayleigh fading (a theorem of the reference, not proved here).

## Complexity

The homogeneous matrix costs $O(N^2 m)$. A sweep of the mixing method costs $O(N^2 k)$, so $T$ sweeps cost $O(T N^2 k)$ with $k = O(\sqrt N)$. The Jacobi method costs $O(N^3)$ per sweep, and it needs a few sweeps $J$ for full accuracy. Each rounding draw costs $O(N k + N^2)$ for the signs and the metric. The total is $O(N^2 m + T N^2 k + J N^3 + R N^2)$ in the [real RAM](/real-ram/) (a closed form). The number of sweeps $T$ depends on the instance; the solver has no bound on it in terms of $N$. A general [interior-point method](/interior-point-method/) solves the SDR to a fixed accuracy in polynomial time, which is what makes SDR detection polynomial, against the exponential worst case of ML.

## Properties

- **Lower bound.** Line L6 is a lower bound on the ML metric for any vectors $u_i$, whether the solver converged or not (theorem).
- **Certificate.** When the rounded metric equals the bound, the result is ML (theorem). The test with seed 1905 (3x3 4-QAM, i.i.d. Rayleigh, $E_s / N_0 = 5$ dB, 40 vectors) found this certificate on 21 vectors (a measurement).
- **Exact without noise.** With $w = 0$ and $G$ of full column rank, the SDR has the unique solution $v v^T$ (theorem).
- **Measured agreement with ML.** In the same test, SDR agreed with ML on 39 of 40 vectors and ZF on 30 (a measurement).
- **Only binary symbols.** The constraint $X_{ii} = 1$ models $b_i^2 = 1$. Larger constellations need more constraints, see below.
- **Randomized.** The solver starts from random vectors, and the rounding draws random hyperplanes; a fixed seed makes the result reproducible.

## Variants and improvements

- **Interior-point solvers.** Solve the SDR with a general SDP solver, which gives the optimum to a set accuracy and a dual certificate directly. The detection papers above used such solvers.
- **Low-rank solvers.** The mixing method of this page and the low-rank method of Burer and Monteiro work on $X = U U^T$ with a small number of columns, at a much lower cost per iteration than an interior-point method.
- **Higher-order constellations.** For 16-QAM, write each real symbol as a sum of two binary variables with weights 2 and 1, or add bound constraints on the diagonal of $X$. Several such relaxations exist, and they are not equally tight.
- **Rounding.** Use the sign of the leading eigenvector of $X$, or the column of $X$ that belongs to $t$, or many random hyperplanes followed by a local search that flips single signs.
- **Soft output.** Use the candidates of the rounding as a list for bit LLRs, as in the [list sphere decoder](/list-sphere-decoder/).

## When to use it

Use SDR detection when the symbols are binary or 4-QAM, the number of real dimensions is moderate (tens to a few hundreds), and the receiver needs a quality close to ML with a polynomial cost, or a certificate that a decision is ML. For small $N$ a [K-best detector](/k-best-detector/) or [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) is cheaper. For large systems with fast fading, the SDP solve is too slow in practice, and [MMSE detection](/mmse-mimo-detector/) or [AMP](/amp-mimo-detection/) is preferred.

## Pitfalls

- **Trusting the solver value.** A low-rank or first-order solver can stop before the optimum. Its value $\mathrm{tr}(Q X)$ is then not a lower bound. Only a dual feasible point, as in line L6, gives a valid bound.
- **Forgetting the homogenizing sign.** The rounded vector must be multiplied by the sign of $t$; otherwise half of the rounding draws return the negated vector.
- **A singular channel.** With $N > m$, $G^T G$ is singular, the noiseless solution is no longer unique, and the relaxation is weaker.
- **Scaling of 4-QAM.** The binary variables are $\pm 1$, but the unit-energy 4-QAM points are $(\pm 1 \pm j) / \sqrt 2$, so $G$ must include the factor $a = 1/\sqrt 2$.
- **Comparing metrics.** The rounding must compare the true metric $\|y_r - G b\|^2$ of each candidate, not the inner products of the vectors.

## Implementations

## History

Goemans and Williamson showed in 1995 that a semidefinite relaxation with random hyperplane rounding gives a 0.878-approximation for maximum cut, which started the use of SDR for problems over $\{-1, +1\}^N$. Tan and Rasmussen (2001) applied it to multiuser detection in CDMA, and Ma, Davidson, Wong, Luo and Ching (2002) studied it as a quasi-ML detector, with results that applied to MIMO detection. Jaldén and Ottersten proved in 2008 that the SDR detector has the diversity order of ML for BPSK over real-valued Rayleigh fading. Later work extended the relaxation to larger constellations and to soft output.

## References
