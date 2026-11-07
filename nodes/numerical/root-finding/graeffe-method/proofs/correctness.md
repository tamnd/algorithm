---
title: Correctness of Graeffe's method
proves: [correctness, termination, convergence-rate]
status: full
---

Let $p(x) = a_0x^n + \cdots + a_n = a_0\prod_{i=1}^n(x - r_i)$ with real $a_j$, $a_0 \ne 0$, $a_n \ne 0$ (after line L1) and $|r_1| \ge \cdots \ge |r_n| > 0$. Statements are in exact arithmetic; the remark at the end discusses rounding.

## Lemma 1 (the squaring step)

If $b$ are the coefficients of a polynomial $P(x) = b_0\prod(x - \rho_i)$ of degree $n$, the coefficients $c$ of line L4 are those of $Q(y) = b_0^2\prod(y - \rho_i^2)$.

*Proof.* $P(-x) = b_0\prod(-x - \rho_i) = (-1)^nb_0\prod(x + \rho_i)$, so $(-1)^nP(x)P(-x) = b_0^2\prod(x^2 - \rho_i^2) = Q(x^2)$. Write $P(x) = \sum_j b_jx^{n-j}$ and $P(-x) = \sum_l (-1)^{n-l}b_lx^{n-l}$. The coefficient of $x^{2n-2j}$ in $(-1)^nP(x)P(-x)$ is $\sum_{s + l = 2j}(-1)^{l}b_sb_l$. Pairing the term $(s, l) = (j - i, j + i)$ with $(j + i, j - i)$ for each $i \ge 1$ gives $(-1)^j\bigl(b_j^2 + 2\sum_{i \ge 1}(-1)^ib_{j-i}b_{j+i}\bigr)$, since $(-1)^{j+i} = (-1)^{j-i}$. Odd powers of $x$ cancel because the product is even. $\square$

By induction, after $k$ steps the coefficients are those of $a_0^{N}\prod(y - r_i^N)$ with $N = 2^k$. By Vieta, $b_j = (-1)^ja_0^Ne_j(r_1^N, \dots, r_n^N)$, where $e_j$ is the $j$-th elementary symmetric function and $e_0 = 1$.

## Lemma 2 (regular indices)

Fix $j$ with $1 \le j \le n - 1$ and $|r_j| > |r_{j+1}|$, and let $\lambda_j = |r_{j+1}/r_j| < 1$. Then
$$e_j(r_1^N, \dots, r_n^N) = (r_1 \cdots r_j)^N(1 + \eta_j), \qquad |\eta_j| \le \Bigl(\binom{n}{j} - 1\Bigr)\lambda_j^N.$$
The same holds trivially with $\eta_j = 0$ for $j = 0$ and $j = n$.

*Proof.* $e_j$ is the sum over $j$-element subsets $S$ of $\prod_{i \in S}r_i^N$. Any $S \ne \{1, \dots, j\}$ contains some $t > j$ and misses some $s \le j$. Then $\prod_{S}|r_i| \le |r_1 \cdots r_j| \cdot |r_t/r_s| \le |r_1 \cdots r_j|\lambda_j$, because the moduli are ordered: swap the indices one at a time and each swap does not increase the product. There are $\binom{n}{j} - 1$ such subsets. $\square$

## Theorem 1 (the moduli)

Let $0 = j_0 < j_1 < \cdots < j_t = n$ be the indices $j$ with $|r_j| > |r_{j+1}|$, together with 0 and $n$. For consecutive $i = j_{s-1}$, $l = j_s$, the roots $r_{i+1}, \dots, r_l$ have one common modulus $\rho$, and
$$\Bigl|\frac{b_l}{b_i}\Bigr|^{1/(N(l - i))} = \rho\,\Bigl|\frac{1 + \eta_l}{1 + \eta_i}\Bigr|^{1/(N(l - i))} = \rho\Bigl(1 + O\bigl(\lambda^N/N\bigr)\Bigr),$$
with $\lambda = \max_s\lambda_{j_s} < 1$. So the formula of L10 converges to the common modulus, and the relative error decreases like $\lambda^{2^k}/2^k$.

*Proof.* By Lemma 1, $|b_l/b_i| = |e_l/e_i|$, and by Lemma 2, $|e_l/e_i| = |r_{i+1}\cdots r_l|^N|1 + \eta_l|/|1 + \eta_i| = \rho^{N(l - i)}|1 + \eta_l|/|1 + \eta_i|$. Since $|\eta| = O(\lambda^N)$, the $N(l - i)$-th root of the last factor is $1 + O(\lambda^N/N)$. $\square$

## Theorem 2 (the deviations and the order)

At a regular index $j$ (one of the $j_s$), with $\eta_j^{(k)}$ the remainder after $k$ steps,
$$(-1)^j\frac{c_j}{b_j^2} = \frac{1 + \eta_j^{(k+1)}}{(1 + \eta_j^{(k)})^2}, \qquad d_j^{(k)} = \bigl|2\eta_j^{(k)}\bigr| + O(\lambda^{2N}).$$
If moreover $\eta_j^{(k)} = c\lambda_j^N(1 + o(1))$ for a constant $c > 0$, which holds for instance when all roots are real, with $c$ the number of subsets $S$ attaining $\prod_S|r_i| = \lambda_j|r_1\cdots r_j|$, then $d^{(k+1)} \approx (d^{(k)})^2/(2c)$. So the deviations converge with order $q = 2$ in the step number $k$, and the moduli error of Theorem 1 is about $d^{(k)}/(2N)$.

At an index $j$ strictly inside a group, the deviation does not tend to 0. For the simplest case, a group that is a single complex pair $\rho e^{\pm i\theta}$, $0 < \theta < \pi$, sitting at positions $j, j + 1$, the dominant part of $e_j$ is $P^N\rho^N\cdot 2\cos(N\theta)$, where $P$ is the product of the moduli above the pair. So asymptotically $(-1)^jc_j/b_j^2 \to 2\cos(2N\theta)/(4\cos^2(N\theta)) = 1 - 1/(2\cos^2(N\theta))$, and $d_j \ge 1/2$ in the limit. A real double root gives $d_j \to 1/2$. A pair $\pm r$ gives $b_j = 0$ exactly after one step, which L6 treats as irregular.

*Proof.* The first display follows from $b_j^{(k)} = (-1)^ja_0^N(r_1\cdots r_j)^N(1 + \eta_j^{(k)})$ and Lemma 1, which gives $c_j = b_j^{(k+1)}$. Expanding $(1 + \eta')/(1 + \eta)^2 = 1 - 2\eta + \eta' + O(\eta^2)$ and using $\eta' = O(\lambda^{2N})$ gives the second. If $\eta^{(k)} \approx c\lambda^N$, then $\eta^{(k+1)} \approx c\lambda^{2N} = (\eta^{(k)})^2/c$ and $d^{(k+1)} \approx 2(\eta^{(k)})^2/c = (d^{(k)})^2/(2c)$. The pair computation is the same expansion with the two dominant subsets carrying the conjugate factors $e^{\pm iN\theta}$. $\square$

## Termination and what the output means

Each pass of the loop L3 increases $k$, so the loop ends after at most $K$ steps; L8 may end it earlier. If it ends with status "separated", every $d_j \le$ tol. By Theorem 2 this happens for all large $k$ exactly when all the moduli are distinct, and then the error of each modulus is asymptotically at most about tol$/2^{k+1}$. This bound is asymptotic, not a guaranteed bound at the stopping step. If the loop ends at the cap, the set $R$ of L9 contains 0, $n$ and the indices that look regular. When $K$ is large enough that $\lambda^{2^K} \ll$ tol, these are exactly the $j_s$ of Theorem 1, so the groups are the true groups of equal moduli. When it is not, two close moduli may be merged into one group, and the reported value is then the geometric mean of the moduli in the group, which is exact by the same formula with the merged indices. Line L11 is correct because the conjugate of a non-real root of a real polynomial is a root of the same modulus, so a modulus carried by one root belongs to a real root, which is $\rho$ or $-\rho$.

## Rounding

The reference code stores the $b_j$ as 40-digit decimals with an exponent range of about $10^{18}$, so nothing overflows for $K \le 30$ and moduli in the double range. At a regular index the computed $c_j$ is dominated by $b_j^2$, so each step adds a relative error of a few units of the 40-digit precision. After the $N$-th root this error is divided by $N$. The moduli are then those of the polynomial with the given floating point coefficients, to the accuracy observed in the tests ($2 \times 10^{-16}$ relative on the Wilkinson polynomial of degree 20). Inside a group, cancellation can amplify the relative error of the irregular coefficients, but these coefficients are not used in L10. This rounding analysis is stated, not proved in detail.
