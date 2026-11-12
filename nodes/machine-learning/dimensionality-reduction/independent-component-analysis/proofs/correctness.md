---
title: Whitening plus kurtosis-maximizing rotations recovers the sources
proves: [correctness]
status: full
---

We use the pseudocode and notation of the page. The model is $x = A s$ with $A$ invertible ($d \times d$) and $s = (s_1, \ldots, s_d)$ a vector of independent sources with mean 0 and variance 1. The fourth cumulant of a variable $u$ with mean 0 is $\operatorname{kurt}(u) = E[u^4] - 3 (E[u^2])^2$, and $\kappa_j = \operatorname{kurt}(s_j)$. The contrast of a vector $y$ is $\Phi(y) = \sum_i \operatorname{kurt}(y_i)^2$.

**Lemma 1 (whitening leaves a rotation).** Let $C = E[x x^{\top}] = E \Lambda E^{\top}$ and $V = \Lambda^{-1/2} E^{\top}$ as in line L1. Then $z = V x$ has $E[z z^{\top}] = I$, and $Q = V A$ is orthogonal, so $z = Q s$.

*Proof.* $V C V^{\top} = \Lambda^{-1/2} E^{\top} E \Lambda E^{\top} E \Lambda^{-1/2} = I$. Since $E[s s^{\top}] = I$, $C = A A^{\top}$, so $Q Q^{\top} = V A A^{\top} V^{\top} = V C V^{\top} = I$. $\square$

So after line L1 the search is over orthogonal matrices only: any $W$ with $W z = W Q s$ independent must make $P = W Q$ orthogonal and, by the theorem below, a signed permutation.

**Lemma 2 (kurtosis of a mixture).** If $s_1, \ldots, s_d$ are independent with mean 0, then for every real vector $p$,
$$ \operatorname{kurt}\Bigl(\sum_j p_j s_j\Bigr) = \sum_j p_j^4 \kappa_j . $$

*Proof.* Expand $E[(\sum_j p_j s_j)^4]$. By independence and mean 0, every term with an index that appears exactly once has expectation 0. What remains is $\sum_j p_j^4 E[s_j^4] + 3 \sum_{j \ne l} p_j^2 p_l^2 E[s_j^2] E[s_l^2]$. Also $(E[(\sum_j p_j s_j)^2])^2 = (\sum_j p_j^2 E[s_j^2])^2 = \sum_j p_j^4 (E[s_j^2])^2 + \sum_{j \ne l} p_j^2 p_l^2 E[s_j^2] E[s_l^2]$. Subtract 3 times the second line from the first. $\square$

**Theorem 1 (the contrast identifies the sources).** Assume at most one $\kappa_j$ is 0. For every orthogonal $P$, with $y = P s$,
$$ \Phi(y) \le \sum_j \kappa_j^2 , $$
with equality if and only if $P$ is a signed permutation matrix.

*Proof.* By Lemma 2, $\operatorname{kurt}(y_i) = \sum_j P_{ij}^4 \kappa_j$. Put $a_j = P_{ij}^4 \ge 0$. By the Cauchy-Schwarz inequality, $(\sum_j a_j |\kappa_j|)^2 \le (\sum_j a_j)(\sum_j a_j \kappa_j^2)$, and $\sum_j a_j = \sum_j P_{ij}^4 \le \sum_j P_{ij}^2 = 1$ because each $|P_{ij}| \le 1$. So
$$ \operatorname{kurt}(y_i)^2 \le \Bigl(\sum_j P_{ij}^4 |\kappa_j|\Bigr)^2 \le \sum_j P_{ij}^4 \kappa_j^2 . $$
Sum over $i$ and swap the sums: $\Phi(y) \le \sum_j \kappa_j^2 \sum_i P_{ij}^4 \le \sum_j \kappa_j^2$, with the same bound $\sum_i P_{ij}^4 \le \sum_i P_{ij}^2 = 1$ for the columns.

If $P$ is a signed permutation, each $y_i$ is $\pm s_j$ for one $j$ and equality holds. Conversely, equality forces $\sum_i P_{ij}^4 = 1$ for each $j$ with $\kappa_j \ne 0$. Since $\sum_i P_{ij}^2 = 1$, this means column $j$ has one entry $\pm 1$ and the other entries 0. At most one column is not covered. It is a unit vector orthogonal to the other columns, which are distinct signed unit vectors, so it is also a signed unit vector at the one remaining position. $\square$

Comon's identifiability theorem is more general: if at most one source is Gaussian, then any $W$ that makes the components of $W x$ pairwise independent satisfies $W A = \Pi D$ with $\Pi$ a permutation and $D$ diagonal. Its proof uses the Darmois-Skitovich theorem. Theorem 1 is the special form for the fourth-order contrast that this implementation maximizes. It needs the stronger condition that at most one source has zero kurtosis.

**Lemma 3 (the pair step is exact).** Let $y_i$ and $y_j$ be two rows of the current data, with sample mean 0, sample variance 1 and sample covariance 0. For $c = \cos \theta$ and $s = \sin \theta$, the rotated rows $u = c y_i + s y_j$ and $v = -s y_i + c y_j$ again have sample variance 1 and covariance 0, and
$$ \operatorname{kurt}(u) = \sum_{a=0}^{4} \binom{4}{a} c^a s^{4-a} m_a - 3 , \qquad \operatorname{kurt}(v) = \sum_{a=0}^{4} \binom{4}{a} (-s)^a c^{4-a} m_a - 3 , $$
where $m_a$ is the sample mean of $y_i^a y_j^{4-a}$.

*Proof.* The rotation is orthogonal, so it keeps the $2 \times 2$ sample covariance equal to $I$. Expand $(c y_i + s y_j)^4$ and $(-s y_i + c y_j)^4$ with the binomial theorem and average. $\square$

So line L5 evaluates the pair contrast for any angle in $O(1)$ time after one pass over the data, and the other rows do not change. A rotation by $\theta + \pi/2$ only swaps the two rows and changes one sign, so $[0, \pi/2)$ covers every case.

**Theorem 2 (the sample contrast never decreases, and whiteness is kept).** After each execution of line L6, the rows of $z$ still have sample covariance $I$, and $\Phi$ of the rows is at least its value before the step. The loop stops after at most the given number of sweeps.

*Proof.* Each step is an orthogonal map on two rows, so the sample covariance stays $I$ (Lemma 3). The search in line L5 includes $\theta = 0$, and the implementation applies the rotation only if the pair contrast increases, so $\operatorname{kurt}(y_i)^2 + \operatorname{kurt}(y_j)^2$ does not decrease, and the other terms of $\Phi$ do not change. The loop count is bounded by the sweep limit. $\square$

The sample contrast is also bounded: for a sample with variance 1, $1 \le m_4 \le n$, so each kurtosis lies in $[-2, n - 3]$. A nondecreasing bounded sequence converges, so the gains in line L7 tend to 0.

**Consistency.** As $n \to \infty$, the sample moments converge to the population moments by the law of large numbers, and the sample contrast converges to $\Phi$ uniformly over the compact set of orthogonal $P$. By Theorem 1 its maximizers are the signed permutations. So a global maximizer of the sample contrast gives $B A$ close to a signed permutation for large $n$. The Jacobi sweeps find a local maximum; with two sources this is a global one, because line L5 searches every angle.

**Cost.** Line L1 takes $\Theta(n d^2)$ for the covariance, $O(d^3)$ for the eigendecomposition and $\Theta(n d^2)$ to apply $V$. Line L5 takes $\Theta(n)$ for the five moments and $\Theta(G)$ for a grid of $G$ angles. Line L6 takes $\Theta(n)$. So a sweep costs $\Theta(d^2 (n + G))$, and $S$ sweeps cost $O(n d^2 + d^3 + S d^2 (n + G))$. The extra memory is $\Theta(n d + d^2)$ for the whitened data and the matrices.
