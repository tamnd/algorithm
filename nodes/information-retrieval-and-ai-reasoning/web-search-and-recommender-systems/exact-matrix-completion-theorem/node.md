---
tag: HK9Z9D
kind: theorem
slug: exact-matrix-completion-theorem
name: Exact matrix completion by nuclear norm minimization
aliases:
- Candes-Recht theorem
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: research
summary: Nuclear norm minimization recovers an incoherent rank r matrix exactly, with high probability, from about r (n1 + n2) log^2 n2 uniformly random entries (Recht 2011).
prereqs: [matrix-completion, singular-value-decomposition, semidefinite-programming]
see_also: [convex-relaxation, compressed-sensing, restricted-isometry-property, basis-pursuit, lagrangian-duality, subgradient, matrix-factorization-recommendation, alternating-least-squares]
sources:
  - url: https://www.jmlr.org/papers/volume12/recht11a/recht11a.pdf
    title: Benjamin Recht, A simpler approach to matrix completion, Journal of Machine Learning Research 12, 3413-3430, 2011
    locator: Definition 1 (coherence), Theorem 2 (assumptions A0 and A1, the bound m of Equation 1 and the failure probability), Section 3 (Proposition 3, sampling with replacement, and Theorem 4, the noncommutative Bernstein inequality), Section 4 (the proof, conditions 6 to 10 and the partition into p batches of size q)
  - paper: doi:10.1007/s10208-009-9045-5
    title: Emmanuel J. Candès and Benjamin Recht, Exact matrix completion via convex optimization, Foundations of Computational Mathematics 9(6), 717-772, 2009
    locator: Abstract and Section 1 (the bound m of order n^(6/5) r log n for most matrices of rank r, and n^(5/4) r log n for all ranks; the assumptions A0 and A1)
  - paper: doi:10.1109/TIT.2010.2044061
    title: Emmanuel J. Candès and Terence Tao, The power of convex relaxation, near-optimal matrix completion, IEEE Transactions on Information Theory 56(5), 2053-2080, 2010
    locator: Section 1 (the strong incoherence property; Theorem 1.2, m of order mu^2 n r log^6 n; Theorem 1.7 and Equations 1.20 and 1.21, the lower bound of order mu0 n r log n for any method)
  - paper: doi:10.1109/TIT.2011.2104999
    title: David Gross, Recovering low-rank matrices from few coefficients in any basis, IEEE Transactions on Information Theory 57(3), 1548-1566, 2011
    locator: Abstract and main results (O(n r nu log^2 n) random coefficients in any basis with coherence nu, by the golfing scheme)
---

The exact matrix completion theorem says that a low-rank matrix whose singular vectors are spread out can be recovered exactly, with high probability, from a small set of its entries chosen uniformly at random, by taking the matrix of least nuclear norm that agrees with them. The nuclear norm is the sum of the singular values, and minimizing it is a [convex relaxation](/convex-relaxation/) of minimizing the rank that can be solved as a [semidefinite program](/semidefinite-programming/). Candès and Recht (2009) proved the first such result, with about $n^{6/5} r \log n$ entries for an $n \times n$ matrix of rank $r$. Candès and Tao (2010) brought the count down to $n r$ times a power of $\log n$, under a stronger incoherence condition. The form stated on this page is the theorem of Recht (2011), which needs about $r (n_1 + n_2) \log^2 n_2$ entries under the weaker conditions of Candès and Recht. The page calls it the exact matrix completion theorem; each bound below is credited to the paper that proved it.

## Statement

Let $M$ be an $n_1 \times n_2$ real matrix of rank $r$ with [singular value decomposition](/singular-value-decomposition/) $M = U \Sigma V^*$, where $n_1 \le n_2$, $\Sigma$ is $r \times r$, $U$ is $n_1 \times r$ and $V$ is $n_2 \times r$.

**Coherence (Recht 2011, Definition 1).** For a subspace $\mathcal U$ of $\mathbb R^n$ of dimension $r$ with orthogonal projection $P_{\mathcal U}$,

$$\mu(\mathcal U) = \frac{n}{r} \max_{1 \le i \le n} \lVert P_{\mathcal U} e_i \rVert^2 .$$

It lies between 1 (all basis vectors equally close to $\mathcal U$) and $n/r$ (some $e_i$ lies in $\mathcal U$).

**Theorem (Recht 2011, Theorem 2).** Assume

- **A0.** The column space and the row space of $M$ have coherence at most $\mu_0$.
- **A1.** Every entry of $U V^*$ has absolute value at most $\mu_1 \sqrt{r / (n_1 n_2)}$.

Suppose $m$ entries of $M$ are observed, with locations $\Omega$ sampled uniformly at random. If

$$m \ge 32 \max\{\mu_1^2, \mu_0\}\, r (n_1 + n_2)\, \beta \log^2(2 n_2)$$

for some $\beta > 1$, then the problem

$$\text{minimize } \lVert X \rVert_* \quad \text{subject to } X_{ij} = M_{ij} \text{ for all } (i, j) \in \Omega$$

has a unique minimizer, equal to $M$, with probability at least

$$1 - 6 \log(n_2) (n_1 + n_2)^{2 - 2\beta} - n_2^{2 - 2\beta^{1/2}} .$$

Here $\lVert X \rVert_* = \sum_k \sigma_k(X)$ is the nuclear norm. The theorem has no condition on the rank, on the ratio $n_2 / n_1$, or on the condition number of $M$. By the Cauchy-Schwarz inequality, $\mu_1 \le \mu_0 \sqrt r$, so A0 alone gives the theorem with $\max\{\mu_1^2, \mu_0\}$ replaced by $\mu_0^2 r$.

## In plain words

A big table of numbers has a simple structure: it is the sum of a few rank-one pieces. You see only a random few percent of its entries. Among all tables that agree with what you see, pick the one with the smallest sum of singular values. The theorem says that this pick is the true table, with probability close to 1, as long as you see somewhat more entries than the table has free parameters, times $\log^2$ of its size.

There is one condition. The table must not hide its information in a few places. A table that is zero except for one entry cannot be found unless that entry is seen. The coherence numbers $\mu_0$ and $\mu_1$ measure how spread out the information is.

## Proof

This is a sketch of the proof in Recht (2011), Sections 3 and 4. Let $T$ be the space of matrices $U A^* + B V^*$, with orthogonal projections $P_T$ and $P_{T^\perp}$, and let $R_\Omega(X) = \sum_{k=1}^m \langle e_{a_k} e_{b_k}^*, X \rangle\, e_{a_k} e_{b_k}^*$ be the sampling operator, which counts an entry once per time it is drawn.

1. **Sampling with replacement (Proposition 3).** The probability that the program fails when $\Omega$ is a uniform set of $m$ distinct entries is at most the probability that it fails when $m$ entries are drawn independently and uniformly with replacement. So it suffices to prove the theorem for draws with replacement, which are independent and allow the use of sums of independent random matrices.

2. **A deterministic condition (Section 4, conditions 6 and 7).** Suppose
$$\Bigl\lVert \tfrac{n_1 n_2}{m} P_T R_\Omega P_T - P_T \Bigr\rVert \le \tfrac12, \qquad \lVert R_\Omega \rVert \le \tfrac83 \beta^{1/2} \log n_2,$$
and that some $Y$ in the range of $R_\Omega$ has $\lVert P_T(Y) - U V^* \rVert_F \le \sqrt{r / (2 n_2)}$ and $\lVert P_{T^\perp}(Y) \rVert < \tfrac12$ (operator norm). For a nonzero $Z$ with $R_\Omega(Z) = 0$, the first two bounds show that $P_T(Z)$ is small compared with $P_{T^\perp}(Z)$. The variational form $\lVert A \rVert_* = \sup_{\lVert B \rVert \le 1} \langle A, B \rangle$, with $B = U V^* + U_\perp V_\perp^*$ chosen to align with $P_{T^\perp}(Z)$, and $\langle Y, Z \rangle = 0$ give $\lVert M + Z \rVert_* > \lVert M \rVert_*$. So $M$ is the unique minimizer. $Y$ is an approximate dual certificate, in the sense of [Lagrangian duality](/lagrangian-duality/): $U V^* + P_{T^\perp}(\cdot)$ is a [subgradient](/subgradient/) of the nuclear norm at $M$.

3. **Building the certificate (the golfing scheme).** Split the $m$ draws into $p \ge \tfrac34 \log(2 n_2)$ independent batches $\Omega_1, \dots, \Omega_p$ of size $q \ge \tfrac{128}{3} \max\{\mu_0, \mu_1^2\} r (n_1 + n_2) \beta \log(n_1 + n_2)$. Set $W_0 = U V^*$, $Y_k = \tfrac{n_1 n_2}{q} \sum_{j \le k} R_{\Omega_j}(W_{j-1})$ and $W_k = U V^* - P_T(Y_k)$. If each batch satisfies the analogue of the first bound of step 2 (condition 8), then $\lVert W_k \rVert_F \le \tfrac12 \lVert W_{k-1} \rVert_F$, so $\lVert W_p \rVert_F \le 2^{-p} \sqrt r$, which gives the first certificate bound. Two more conditions per batch (conditions 9 and 10), on the largest entry of $W_k$ and on the operator norm of $(\tfrac{n_1 n_2}{q} R_{\Omega_j} - I)(W_{j-1})$, give $\lVert P_{T^\perp}(Y_p) \rVert < \tfrac12$ by summing a geometric series.

4. **Probabilities.** Each condition is a bound on a sum of independent zero-mean random matrices, and the noncommutative Bernstein inequality (Theorem 4) bounds its failure probability. Assumptions A0 and A1 bound the size and the variance of the summands, which is where $\mu_0$ and $\mu_1$ enter. A union bound over the conditions and the batches gives the stated failure probability, and $m = p q$ gives the stated bound on $m$.

The batch construction is due to Gross, Liu, Flammia, Becker and Eisert (2010) and Gross (2011), as Recht states in Section 4. The earlier proofs of Candès and Recht (2009) and Candès and Tao (2010) built the certificate from a series whose terms they bounded with decoupling inequalities and long combinatorial moment bounds.

## Consequences

- **Rating prediction.** A ratings table that is close to low rank, with ratings missing at random, is the model case for [matrix factorization](/matrix-factorization-recommendation/) recommenders; the theorem says when the exact, noise-free version can be solved by a convex program. Real ratings are noisy and are not missing uniformly at random, so the theorem does not apply to them as stated. Whether a completed matrix gives good recommendations is measured on held-out data, never proved by this theorem.
- **Random models.** Applying the theorem to the models of Candès and Recht (2009, Section 2), Recht reports that $c_u r (n_1 + n_2) \log^5 n_2$ entries suffice when the row and column spaces are drawn uniformly at random, $c_u r (n_1 + n_2) \log^4 n_2$ when also $r > \log n_2$, and $c_i \mu_0^2 r (n_1 + n_2) \log^3 n_2$ when the singular vectors have entries of magnitude at most $\sqrt{\mu_0 / n_1}$, for numerical constants $c_u$ and $c_i$.
- **Polynomial time.** The program is a semidefinite program, so under the hypotheses a rank-minimization problem that is [NP-hard](/np-hard/) in general is solved exactly in polynomial time.
- **The parallel with compressed sensing.** The nuclear norm plays the part of the $\ell_1$ norm in [compressed sensing](/compressed-sensing/) and [basis pursuit](/basis-pursuit/), and the singular values play the part of the entries of a sparse vector. Entry sampling does not have the [restricted isometry property](/restricted-isometry-property/), since a matrix with one nonzero entry is in the kernel of most samples; incoherence is the condition that takes its place.

A numerical experiment that hides entries of a random low-rank matrix and solves the program can show the effect, but it does not test the theorem. The theorem is a bound on a failure probability, over the random choice of $\Omega$, for every matrix that meets A0 and A1 with the stated constants. A finite run checks one matrix and a few draws, does not check that the constants are the right ones, and cannot see a failure probability as small as the bound. This page has no such experiment.

## Tightness

- **One log factor.** Candès and Tao (2010, Theorem 1.7 and Equation 1.21) prove that, in the Bernoulli sampling model, any method that recovers every rank-$r$ matrix with coherence $\mu_0$ with probability at least $1 - \delta$ needs about $\mu_0 n r \log(n / (2\delta))$ entries. Recht's bound is above this by one factor of $\log n_2$ and a constant; Recht describes it as optimal up to a small numerical constant and one logarithmic factor.
- **Degrees of freedom.** A rank-$r$ matrix of size $n \times n$ has $r (2n - r)$ degrees of freedom, so at least that many entries are needed by counting. The extra $\log n$ comes from the coupon collector effect: with fewer than about $n \log n$ random entries some row or column is not seen at all, and then no method can recover it.
- **Coherence is needed.** The matrix $e_1 e_1^*$ has rank one and coherence $n$; it cannot be recovered unless the entry $(1, 1)$ is sampled. So some bound like A0 is necessary, and the number of entries must grow with the coherence.
- **The sampling model matters.** The proof uses uniform random locations. For adversarial or structured missing patterns, low-rank completion with missing data is NP-hard in general (Gillis and Glineur, 2011, cited on the [matrix completion](/matrix-completion/) page).

## History

The nuclear norm was used as a heuristic for rank minimization long before there was a theory for it; Recht (2011, Section 1) cites Fazel, Hindi and Boyd (2001) and Fazel's thesis (2002), among others. Recht, Fazel and Parrilo (SIAM Review, 2010) gave the first guarantees, for most instances of rank minimization with enough random linear constraints. Candès and Recht (Foundations of Computational Mathematics, 2009) proved the first exact completion result for entry sampling, with about $n^{6/5} r \log n$ entries for most rank-$r$ matrices, or $n^{5/4} r \log n$ for all ranks, under A0 and A1. Candès and Tao (IEEE Transactions on Information Theory, 2010) proved $C \mu^2 n r \log^6 n$ under their strong incoherence property, together with the lower bound above. Keshavan, Montanari and Oh (IEEE Transactions on Information Theory, 2010) gave bounds of a similar size, in special cases, for a different algorithm. Gross (IEEE Transactions on Information Theory, 2011) found the golfing scheme, which handles sampling in any basis with $O(n r \nu \log^2 n)$ coefficients. Recht (Journal of Machine Learning Research, 2011) used it to give the short proof of the bound stated here. The alias "Candes-Recht theorem" names the 2009 paper; the near-optimal $n r$ polylog bounds are due to Candès and Tao and to Recht and Gross.

## References
