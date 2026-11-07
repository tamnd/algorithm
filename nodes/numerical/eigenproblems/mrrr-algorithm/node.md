---
tag: B3BDXW
kind: algorithm
slug: mrrr-algorithm
name: MRRR algorithm
aliases:
- multiple relatively robust representations
- MR3 algorithm
- Dhillon-Parlett algorithm
area: numerical/eigenproblems
level: advanced
summary: Computes all eigenvectors of a symmetric tridiagonal matrix in O(n^2) time, one twisted factorization per vector, by shifting clusters until their eigenvalues have large relative gaps.
solves: [tridiagonal-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of T", c: "the number of count sweeps in bisection"}
  time: {typical: Θ(n^2), worst: O(n^3)}
  space: {extra: O(n^2)}
  flops: {counts: "6 c n", vectors: "18 n^2", lapack_typical: "O(n^2)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
history:
  year: 1997
  people: [Inderjit S. Dhillon, Beresford N. Parlett]
  note: Dhillon's 1997 Berkeley thesis, written with Parlett, combined Fernando's twisted factorizations with relatively robust representations; the method became LAPACK's xSTEMR in 2006.
prereqs: [tridiagonal-eigenproblem, inverse-iteration, sturm-sequence-eigenvalue-count]
see_also: [bisection-eigenvalue-algorithm, dqds-algorithm, divide-and-conquer-eigensolver, qr-algorithm, symmetric-eigenproblem, tridiagonalization, rayleigh-quotient-iteration, weyls-inequality]
sources:
  - paper: "Inderjit S. Dhillon and Beresford N. Parlett, Multiple representations to compute orthogonal eigenvectors of symmetric tridiagonal matrices, Linear Algebra and its Applications 387, 2004"
    title: Multiple representations to compute orthogonal eigenvectors of symmetric tridiagonal matrices
    locator: Linear Algebra Appl. 387 (2004), pp. 1 to 28
  - paper: "Inderjit S. Dhillon and Beresford N. Parlett, Orthogonal eigenvectors and relative gaps, SIAM Journal on Matrix Analysis and Applications 25(3), 2004"
    title: Orthogonal eigenvectors and relative gaps
    locator: SIAM J. Matrix Anal. Appl. 25(3) (2004), pp. 858 to 899
  - paper: "Inderjit S. Dhillon, Beresford N. Parlett and Christof Vömel, The design and implementation of the MRRR algorithm, ACM Transactions on Mathematical Software 32(4), 2006"
    title: The design and implementation of the MRRR algorithm
    locator: ACM Trans. Math. Software 32(4) (2006), pp. 533 to 560
  - paper: "Beresford N. Parlett and Inderjit S. Dhillon, Relatively robust representations of symmetric tridiagonals, Linear Algebra and its Applications 309, 2000"
    title: Relatively robust representations of symmetric tridiagonals
    locator: Linear Algebra Appl. 309 (2000), pp. 121 to 151
  - paper: "K. Vince Fernando, On computing an eigenvector of a tridiagonal matrix. Part I: Basic results, SIAM Journal on Matrix Analysis and Applications 18(4), 1997"
    title: "On computing an eigenvector of a tridiagonal matrix. Part I: Basic results"
    locator: SIAM J. Matrix Anal. Appl. 18(4) (1997), pp. 1013 to 1034
  - paper: "Inderjit S. Dhillon, Beresford N. Parlett and Christof Vömel, Glued matrices and the MRRR algorithm, SIAM Journal on Scientific Computing 27(2), 2005"
    title: Glued matrices and the MRRR algorithm
    locator: SIAM J. Sci. Comput. 27(2) (2005), pp. 496 to 510
  - paper: "James W. Demmel, Osni A. Marques, Beresford N. Parlett and Christof Vömel, Performance and accuracy of LAPACK's symmetric tridiagonal eigensolvers, SIAM Journal on Scientific Computing 30(3), 2008"
    title: Performance and accuracy of LAPACK's symmetric tridiagonal eigensolvers
    locator: SIAM J. Sci. Comput. 30(3) (2008), pp. 1508 to 1526
  - paper: "Paul R. Willems and Bruno Lang, A framework for the MR^3 algorithm: theory and implementation, SIAM Journal on Scientific Computing 35(2), 2013"
    title: "A framework for the MR^3 algorithm: theory and implementation"
    locator: SIAM J. Sci. Comput. 35(2) (2013), pp. A740 to A766
---

The MRRR algorithm (multiple relatively robust representations, also written MR³) computes the eigenvalues and orthonormal eigenvectors of a real symmetric tridiagonal matrix $T$ with $O(n)$ work per eigenpair, so all of them cost $O(n^2)$ flops instead of the $O(n^3)$ of the [QR algorithm](/qr-algorithm/) with vectors. Each eigenvector comes from one twisted factorization of $L D L^T - \hat\lambda I$, a form of [inverse iteration](/inverse-iteration/) that needs no iteration and no Gram-Schmidt. The difficulty is that close eigenvalues make such vectors lose orthogonality. MRRR's answer is to shift: for a cluster it builds a new factorization $L D L^T - \tau I = L_+ D_+ L_+^T$ with $\tau$ next to the cluster, in which the cluster's eigenvalues are small and therefore far apart in the relative sense, and repeats until every eigenvalue is relatively isolated. It is LAPACK's `xSTEMR`, the fastest tridiagonal eigensolver for most matrices.

## In plain words

A common shortcut finds each special direction of a matrix in one quick pass, if its special value is known very precisely and is well separated from the others. Values that sit close together spoil this: the directions come out tilted toward each other. The trick here is to change the point of view. Moving the zero point right next to a tight group makes the members of the group tiny numbers, and tiny numbers that differ in their leading digits are far apart in relative terms. The method stores each new point of view in a special factored form that keeps those leading digits exact, and repeats until every value stands alone.

## The problem

**Notation.** $T$ is real symmetric tridiagonal of order $n$, with diagonal $a_1, \dots, a_n$ and off-diagonal $b_1, \dots, b_{n-1}$. On this page the eigenvalues are in **increasing** order, $\lambda_1 \le \dots \le \lambda_n$ (the order of the output; $\lambda_n$ is the largest), with orthonormal eigenvectors $v_i$. A representation is $L D L^T = T - \sigma I$ with $L$ unit lower bidiagonal (entries $l_i$) and $D = \operatorname{diag}(d_i)$. The relative gap of an eigenvalue $\mu$ of a representation is $\mathrm{relgap}(\mu) = \min_{\mu' \ne \mu} |\mu' - \mu| / |\mu|$, and $\mathrm{gaptol} = 10^{-3}$. $u$ is the unit roundoff.

**Input.** $a$ and $b$.

**Output.** $\hat\lambda_1 \le \dots \le \hat\lambda_n$ and unit vectors $\hat z_1, \dots, \hat z_n$ with residuals $\|T \hat z_i - \hat\lambda_i \hat z_i\|_2 = O(n u \|T\|_2)$ and $|\hat z_i^T \hat z_j| = O(n u / \mathrm{gaptol})$ for $i \ne j$, under the hypotheses stated in the Correctness section.

A representation $L D L^T$ is **relatively robust** for a set of its eigenvalues if small relative changes in every $l_i$ and $d_i$ cause only small relative changes in those eigenvalues and small changes in their eigenvectors, measured against relative gaps. A positive definite $L D L^T$ (a Cholesky factor) is relatively robust for all its eigenvalues (Demmel and Kahan 1990).

## The algorithm

```pseudo id=main
MRRR(a, b)
L1  split T where |bᵢ| ≤ 2u‖T‖; handle each unreduced block (a 1 × 1 block is its own eigenpair)
L2  σ ← just below the Gershgorin interval; L D Lᵀ ← T − σ I     ▷ positive definite root
L3  μ₁ < … < μₘ ← eigenvalues of L D Lᵀ by bisection on the qd count, to relative accuracy u
L4  push (L, D, σ, indices 1..m, μ) on a stack
L5  while the stack is not empty do pop (L, D, σ, I, μ)
L6      split I into groups: neighbours with gap < gaptol · |μ| share a group
L7      for each group G of size 1, G = {i} do
L8          ẑᵢ ← twisted factorization of L D Lᵀ − μᵢ I at the best twist;  λ̂ᵢ ← σ + μᵢ
L9      for each group G of size ≥ 2 do choose τ next to one end of G with small growth of
              L₊ D₊ L₊ᵀ ← L D Lᵀ − τ I                      ▷ stationary qd transform
L10         refine μᵢ − τ for i ∈ G by bisection on L₊ D₊ L₊ᵀ   ▷ now large relative gaps
L11         push (L₊, D₊, σ + τ, G, refined values)
L12 return all (λ̂ᵢ, ẑᵢ) in increasing order
```

**The qd transforms.** The stationary transform of line L9 computes $L_+ D_+ L_+^T = L D L^T - \tau I$ by $s_1 = -\tau$, $D^+_i = d_i + s_i$, $L^+_i = d_i l_i / D^+_i$, $s_{i+1} = L^+_i l_i s_i - \tau$, $D^+_n = d_n + s_n$, without ever forming the tridiagonal. The number of negative $D^+_i$ is the number of eigenvalues below $\tau$ (Sylvester's law of inertia), which is the count that bisection uses in lines L3 and L10; this is the [Sturm count](/sturm-sequence-eigenvalue-count/) applied to a factored matrix. The progressive transform runs the same idea from the bottom and gives $L D L^T - \mu I = U_- D_- U_-^T$ with $p_n = d_n - \mu$, $D^-_{i+1} = d_i l_i^2 + p_{i+1}$, $U^-_i = d_i l_i / D^-_{i+1}$, $p_i = p_{i+1} d_i / D^-_{i+1} - \mu$.

**Twisted factorizations.** For each $k$, combining the top $k - 1$ rows of the stationary factorization with the bottom $n - k$ rows of the progressive one gives a twisted factorization with middle pivot $\gamma_k = s_k + p_k + \mu$. Line L8 picks $r$ with the least $|\gamma_r|$, sets $z_r = 1$, and fills the rest by $z_i = -L^+_i z_{i+1}$ upward and $z_{i+1} = -U^-_i z_i$ downward. Then $(L D L^T - \mu I) z = \gamma_r e_r$ exactly in exact arithmetic, so the residual of $z / \|z\|$ is $|\gamma_r| / \|z\|$, and $\gamma_r = 1 / ((L D L^T - \mu I)^{-1})_{rr}$. Fernando (1997) showed that a twist index with small $|\gamma_r|$ always exists when $\mu$ is close to an eigenvalue; this is one step of inverse iteration with the best possible right-hand side $e_r$.

**Choosing the new shift.** Line L9 tries $\tau = \mu_{\text{first}} - \delta$ and $\tau = \mu_{\text{last}} + \delta$ with $\delta = 4u \max|\mu|$, doubling $\delta$ up to four times, and accepts the first $\tau$ for which $\max_i |D^+_i| \le 8 (\text{spectral diameter})$; small element growth is the practical sign of a relatively robust representation. Failing that it accepts the candidate with the least growth if that growth is below $2^{20}$ times the diameter. If no shift qualifies, or the tree is already 12 levels deep, the implementation finishes the cluster by trying twisted vectors at several twist indices, keeping those that are independent of the ones already kept, and ends with a [Rayleigh-Ritz](/rayleigh-ritz-method/) step inside their span. This fallback is reached on glued matrices whose clusters are equal to working precision; LAPACK handles that case differently (see Variants).

## Example

Wilkinson's matrix $W_9^+$ has $a = (4, 3, 2, 1, 0, 1, 2, 3, 4)$ and $b_i = 1$. Its eigenvalues are

$$-1.125422415673, \; 0.254718759826, \; 0.952584219075, \; 1.822717080887, \; 2.178284739550,$$
$$3.177282919113, \; 3.247396472579, \; 4.745281240174, \; 4.747156984469,$$

and the two largest differ by only $1.876 \times 10^{-3}$.

1. **Root.** The Gershgorin interval is $[-2, 6]$, so $\sigma = -2 - 1.4 \times 10^{-14}$, and $T - \sigma I = L D L^T$ with $D = (6, 4.833333, 3.793103, 2.736364, 1.634551, 2.388211, 3.581277, 4.720770, 5.788170)$, all positive.
2. **Root eigenvalues.** Bisection on the qd count gives $\mu = \lambda - \sigma$, from $0.874578$ to $6.745281$ and $6.747157$. The neighbouring relative gaps are $0.61$, $0.24$, $0.23$, $0.085$, $0.19$, $0.013$, $0.22$ and $2.78 \times 10^{-4}$. The first seven eigenvalues are singletons; the last two form a cluster because $2.78 \times 10^{-4} < 10^{-3}$.
3. **Singletons.** Each gets one twisted factorization; for example $\lambda_1$ uses the twist index $r = 5$, with residual $|\gamma_5| / \|z\| = 1.7 \times 10^{-16}$.
4. **The cluster.** The shift at the left end, $\tau = 6.745281$, gives a factorization with $\max |D^+_i| = 1.26 \times 10^{12}$: rejected. The right end, $\tau = 6.7471569844691581$, gives $\max |D^+_i| = 3.33$: accepted. In the child representation the two eigenvalues are $-1.8757 \times 10^{-3}$ and $-2.7 \times 10^{-15}$, with relative gap $1.0$, so both are singletons. Their twisted factorizations use $r = 9$ and $r = 1$.
5. **Result.** The vectors of the pair are $\pm(0.550094, 0.409975, 0.165427, 0.044170, 0, -0.044170, -0.165427, -0.409975, -0.550094)$ and $\pm(0.548707, 0.409970, 0.167575, 0.050386, 0.021228, 0.050386, 0.167575, 0.409970, 0.548707)$. The tree has depth 1 and 2 representations, there are 9 twisted factorizations and 572 count sweeps, and all nine vectors are orthogonal to within $3.1 \, n u$. The eigenvalues agree with exact rational Sturm counts, and they sum to the trace $20$. These numbers come from the implementation and are checked by its tests.

## Correctness

The full proofs are in [proofs/correctness.md](proofs/correctness.md). In exact arithmetic:

- **The transforms.** The stationary and progressive qd recurrences give exact factorizations of $L D L^T - \tau I$, and their negative pivots count the eigenvalues below the shift. So every representation on the stack equals $T - \sigma I$ for its accumulated shift $\sigma$, and bisection brackets each eigenvalue: the returned $\hat\mu$ is within $u |\mu|$ of the true eigenvalue $\mu$ of the representation.
- **Twisted vectors (proved).** $(L D L^T - \hat\mu I) z = \gamma_r e_r$ and $\gamma_r = 1 / ((L D L^T - \hat\mu I)^{-1})_{rr}$. If $\delta = |\mu - \hat\mu|$ is less than $g / (2n)$, where $g$ is the distance from $\hat\mu$ to the other eigenvalues, then $\min_k |\gamma_k| \le 2n\delta$, the residual of $\hat z$ is at most $2n\delta$, and $\sin\angle(\hat z, v) \le 2n\delta / g$. With $\delta \le u|\mu|$ this is $2nu / \mathrm{relgap}(\mu)$: relative gaps, not absolute ones, control the angle.
- **Bookkeeping and termination (proved).** The groups partition each node's indices, so every eigenvalue gets exactly one value and one vector. The tree depth is capped, bisection stops after a bounded number of steps, and the shift search and the fallback try finitely many candidates.

In floating point, the guarantees rest on the theorems of Dhillon and Parlett (2004a, 2004b): the qd transforms are mixed relatively stable (the computed result is exact for tiny relative perturbations of input and output), a relatively robust representation determines its eigenvalues and eigenvectors to high relative accuracy, and so vectors computed from different representations are orthogonal to $O(nu/\mathrm{gaptol})$ and have residuals $O(nu\|T\|_2)$. The hypothesis is that every representation used is relatively robust for its cluster. The element-growth test is only a heuristic check of that hypothesis, which is why the guarantee is conditional; Willems and Lang (2013) give a version with checkable conditions. The tests observe residuals up to $1.3 \, nu\|T\|_2$ and orthogonality up to $9 \, nu$ on random matrices and glued Wilkinson matrices, and $68 \, nu$ on $W_{21}^+$.

## Complexity

**Count sweeps (counted).** One stationary qd count costs about $6n$ flops. Bisection to full relative accuracy uses about 53 sweeps per eigenvalue plus a few for the bracket and for each tree level, so $c \approx 55n$ to $64n$ sweeps were observed for random matrices with $n$ from 25 to 200. That is about $350n^2$ flops for the eigenvalues, a large constant. LAPACK computes the root eigenvalues with the [dqds algorithm](/dqds-algorithm/) instead and refines by Rayleigh quotient corrections, which costs a small multiple of $n^2$.

**Vectors (counted).** Each twisted factorization costs about $18n$ flops for the two transforms, the $\gamma_k$, the solve and the normalization, so $18n^2$ for all vectors. There is exactly one per eigenvalue when no cluster falls back.

**Bounds.** With bounded depth and bisection steps, the total without fallbacks is $O(n^2)$; this is proved for the implementation, since each node costs $O(n)$ per index and the depth is capped. A fallback cluster of size $g$ may try up to $n$ twist indices per member, $O(g n^2)$, so the worst case of the implementation is $O(n^3)$. LAPACK's `xSTEMR` has the same structure, and its cost is $O(n^2)$ for all but pathological matrices (Demmel, Marques, Parlett and Vömel 2008).

**Space.** The output vectors take $n^2$ numbers. Each representation on the stack takes $2n$ numbers; in the worst case $O(n)$ of them are pending, so $O(n^2)$ extra memory, while typical trees keep only a few. LAPACK stores the representations inside the eigenvector array and needs only $O(n)$ extra.

**Subsets.** $k$ selected eigenpairs cost $O(kn)$, which none of the QR-based or divide-and-conquer methods offers.

## Properties

- **$O(n)$ per eigenpair, with no reorthogonalization.** Orthogonality comes from accuracy, not from Gram-Schmidt, so the vectors can be computed independently and in parallel.
- **Embarrassingly parallel subsets.** Any set of eigenvalue indices can be processed without the others, as in [bisection](/bisection-eigenvalue-algorithm/).
- **Not backward stable in the usual strong sense.** Residuals are small, but orthogonality is $O(nu/\mathrm{gaptol})$, typically $10^{-14}$ to $10^{-13}$ for $n$ in the thousands, slightly worse than the QR algorithm or [divide and conquer](/divide-and-conquer-eigensolver/) (Demmel et al. 2008).
- **High relative accuracy available.** If $T$ itself is positive definite and given as $L D L^T$ (for example from a bidiagonal SVD problem), the root needs no shift and small eigenvalues are computed to high relative accuracy.
- **Deterministic.** No random numbers are used.

## Variants and improvements

- **dqds for the root eigenvalues.** LAPACK computes the eigenvalues of the root representation with the [dqds algorithm](/dqds-algorithm/), which is faster than bisection when all are wanted, and switches to bisection for subsets.
- **Rayleigh quotient correction.** Instead of bisecting each eigenvalue to full accuracy, LAPACK refines it with $\mu \leftarrow \mu + \gamma_r / \|z\|^2$, the [Rayleigh quotient](/rayleigh-quotient-iteration/) correction, with bisection as a safeguard.
- **Glued matrices.** For clusters of eigenvalues equal to working precision, Dhillon, Parlett and Vömel (2005) perturb the root representation by random relative amounts of a few ulps, which separates the cluster without harming the backward error.
- **Checkable robustness.** Willems and Lang (2013) replace the growth heuristic with conditions that can be verified, and adapt MR³ to the bidiagonal SVD.
- **Bidiagonal SVD.** The singular value decomposition of a bidiagonal matrix can be computed by MR³ on the associated tridiagonals with coupling relations that keep left and right vectors consistent (Großer and Lang 2003; Willems and Lang 2013).

## When to use it

Use MRRR when many or all eigenvectors of a symmetric tridiagonal matrix are needed and $O(n^3)$ is too slow, or when a subset of eigenpairs is needed: LAPACK `xSYEVR` reduces a dense matrix by [tridiagonalization](/tridiagonalization/) and calls `xSTEMR`. For the most accurate orthogonality, or for matrices with large tight clusters, [divide and conquer](/divide-and-conquer-eigensolver/) is usually as fast for all eigenpairs and somewhat more accurate. For eigenvalues only, dqds or the QR algorithm cost $O(n^2)$ as well and are simpler.

## Pitfalls

- **Absolute gaps are the wrong criterion.** Inverse iteration declares a cluster when eigenvalues are close in absolute terms and then reorthogonalizes, which costs $O(n k^2)$ for a cluster of size $k$. MRRR's clustering is relative to the current shift; mixing the two criteria breaks the method.
- **Forming the shifted tridiagonal.** Computing $T - \tau I$ explicitly and refactoring loses the relative accuracy of small eigenvalues near $\tau$. The shift must be applied to the factors with the stationary qd transform.
- **Element growth.** A shift inside or too close to a cluster can produce huge $D^+_i$, as the left-end shift in the example did ($1.26 \times 10^{12}$). Such a representation is not robust; try the other end or move the shift away.
- **Eigenvalues equal to working precision.** On glued matrices, clusters cannot be split by shifting, and a naive implementation returns identical vectors. Detect it and use different twist indices, random perturbations of the root, or a small Gram-Schmidt step.
- **Splitting.** Off-diagonal entries below $u\|T\|$ must be set to zero first; otherwise the root factorization of a nearly reducible matrix has eigenvalues equal to working precision across the two parts.
- **Zero pivots.** An exact zero $D^+_i$ must be replaced by a tiny number so that the counts and the transforms stay defined, as in the Sturm count.

## Implementations

## History

Inverse iteration with reorthogonalization was the standard way to get eigenvectors of a tridiagonal matrix from accurate eigenvalues, at a cost that grows as $O(nk^2)$ for clusters of size $k$. Fernando (1997) introduced twisted factorizations to choose the best right-hand side for one inverse iteration step. Parlett and Dhillon (2000) developed relatively robust representations, and Dhillon's 1997 Berkeley thesis, supervised by Parlett, combined the two into an $O(n^2)$ algorithm that needs no reorthogonalization. The theory appeared in two 2004 papers, the analysis of glued matrices in 2005, and the LAPACK routine `xSTEMR` with Vömel in 2006. Willems and Lang (2013) gave a framework with verifiable conditions.

## References
