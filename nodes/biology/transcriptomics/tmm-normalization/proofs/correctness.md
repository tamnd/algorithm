---
title: TMM returns the common log ratio when the changed genes fit inside the trim, and it is antisymmetric
proves: [correctness]
status: full
---

We prove three facts about the trimmed mean of M-values in exact arithmetic. Swapping the two samples inverts the factor (Lemma 2). Genes whose M values lie outside a band, and that are few enough to be trimmed, cannot move the factor out of that band (Lemma 3). If all the other genes share the same M value $m$, the factor is exactly $2^m$ (Theorem 4). The weights $1/v_g$ come from a delta-method approximation of the variance of $M_g$. That they are good weights is a heuristic and is not proved here. That real data have a majority of unchanged genes is a modelling assumption.

**Setting.** Two samples, obs and ref, with counts $o_g$ and $r_g$ and library sizes $N_o, N_r > 0$. Line L1 keeps the genes with $o_g > 0$ and $r_g > 0$; let $n$ be their number. For these genes,
$$M_g = \log_2\frac{o_g/N_o}{r_g/N_r}, \quad A_g = \tfrac12\left(\log_2\frac{o_g}{N_o} + \log_2\frac{r_g}{N_r}\right), \quad v_g = \frac{N_o - o_g}{N_o\,o_g} + \frac{N_r - r_g}{N_r\,r_g}.$$
We assume $o_g < N_o$ or $r_g < N_r$, so that $v_g > 0$. With trim fractions $\theta_M = 0.3$ and $\theta_A = 0.05$, let $\lambda_M = \lfloor n\theta_M\rfloor + 1$, $\eta_M = n + 1 - \lambda_M$, and $\lambda_A, \eta_A$ the same with $\theta_A$. Ranks are average ranks: a block of $t$ tied values that follows $u$ smaller values gets rank $u + (t+1)/2$. The kept set is $\mathcal K = \{g : \lambda_M \le \operatorname{rank}(M_g) \le \eta_M,\ \lambda_A \le \operatorname{rank}(A_g) \le \eta_A\}$, and
$$f = \frac{\sum_{g \in \mathcal K} M_g/v_g}{\sum_{g \in \mathcal K} 1/v_g}, \qquad \text{factor} = 2^f.$$
The code returns 1 when $\mathcal K$ is empty, when no gene is left after line L1, or when every $|M_g| < 10^{-6}$, as edgeR does.

**Lemma 1 (what the lines compute).** Lines L1 to L4 compute $M_g$, $A_g$ and $v_g$ for the genes with two positive counts. Line L5 computes the four rank bounds. Line L6 computes average ranks, line L7 forms $\mathcal K$, and lines L8 and L9 return $2^f$.

*Proof.* This is a direct reading of the code. The function average_ranks sorts the values and gives each block of equal values the mean of its positions, $(i + j)/2 + 1$ for 0-based positions $i, \dots, j$. This is $u + (t+1)/2$ with $u = i$ and $t = j - i + 1$. $\square$

**Lemma 2 (antisymmetry).** Let $f'$ be the value of $f$ with the roles of obs and ref swapped. Then $f' = -f$, so the two factors multiply to 1.

*Proof.* The swap keeps the same genes at line L1 and the same $n$, so the same bounds. It maps $M_g$ to $-M_g$ and keeps $A_g$ and $v_g$. Negating all values reverses the sorted order. A block of $t$ tied values that had $u$ smaller values now has $n - u - t$ smaller values, so its new rank is $n - u - t + (t+1)/2 = n + 1 - (u + (t+1)/2)$. So $\operatorname{rank}'(M_g) = n + 1 - \operatorname{rank}(M_g)$. The interval $[\lambda_M, \eta_M]$ is symmetric under $x \mapsto n + 1 - x$, because $\eta_M = n + 1 - \lambda_M$. Hence the kept set is the same, and $f' = \sum_{\mathcal K}(-M_g)/v_g \big/ \sum_{\mathcal K}1/v_g = -f$. $\square$

In floating point, $\log_2(x/y)$ and $-\log_2(y/x)$ can differ in the last bit, so values that tie in one direction may not tie in the other. The tests check the lemma on real-valued counts, where no two M values tie.

**Lemma 3 (outliers inside the trim).** Let $m_- \le m_+$, and split the genes into $L = \{g : M_g < m_-\}$, $S = \{g : m_- \le M_g \le m_+\}$ and $H = \{g : M_g > m_+\}$. If $|L| \le \lambda_M - 1$ and $|H| \le \lambda_M - 1$, then $\mathcal K \subseteq S$. If moreover $\mathcal K$ is not empty, then $m_- \le f \le m_+$.

*Proof.* Every value of $L$ is smaller than every value outside $L$, so the genes of $L$ fill the first $|L|$ sorted positions, and their average ranks lie between 1 and $|L| \le \lambda_M - 1$. In the same way the genes of $H$ fill the last $|H|$ positions, and their ranks are at least $n - |H| + 1 \ge n + 2 - \lambda_M = \eta_M + 1$. So no gene of $L$ or $H$ passes the rank test of line L7, and $\mathcal K \subseteq S$. Then $f$ is a mean of values in $[m_-, m_+]$ with positive weights $1/v_g$, so it lies in $[m_-, m_+]$. $\square$

**Theorem 4 (a majority with one common ratio).** Use the default trims $\theta_M = 0.3$ and $\theta_A = 0.05$. Suppose the genes of $S$ all have $M_g = m$ exactly, and $|L|, |H| \le \lambda_M - 1$ as in Lemma 3 with $m_- = m_+ = m$. Then $\mathcal K$ is not empty and $f = m$, so the factor is $2^m$. (The early return of the code when every $|M_g| < 10^{-6}$ gives 1 instead, which differs from $2^m$ by less than $10^{-6}$ in the exponent.)

*Proof.* By Lemma 3 it is enough to show that $\mathcal K$ is not empty. The genes of $S$ form one tie block after the $|L|$ genes of $L$, so they all have the rank $\rho = |L| + (|S| + 1)/2$. With $|S| = n - |L| - |H|$, this is $\rho = (n + 1 + |L| - |H|)/2$. Since $|H| \le \lambda_M - 1$, $\rho \ge (n + 2 - \lambda_M)/2$, and this is at least $\lambda_M$ when $3\lambda_M \le n + 2$. In the same way $\rho \le \eta_M$ when $3\lambda_M \le n + 2$. For $\theta_M = 0.3$, $3\lambda_M \le 0.9n + 3 \le n + 2$ when $n \ge 10$, and for $n = 1, \dots, 9$ the values $\lambda_M = 1, 1, 1, 2, 2, 2, 3, 3, 3$ satisfy $3\lambda_M \le n + 2$ one by one. So every gene of $S$ passes the M test.

The A test removes at most the $\lambda_A - 1$ lowest and the $\lambda_A - 1$ highest A ranks, so at most $2(\lambda_A - 1) \le 2n\theta_A = 0.1n$ genes. But $|S| \ge n - 2(\lambda_M - 1) \ge n - 0.6n = 0.4n > 0.1n$ (for $n \ge 1$, $|S| \ge 1$ because $2(\lambda_M - 1) \le 0.6n < n$). So some gene of $S$ passes both tests, and $\mathcal K \ne \emptyset$. $\square$

**Corollary 5 (the example of Robinson and Oshlack).** Let sample A express the same genes as sample B at the same level, and as many genes again that B does not express, with the same library size $N$. Then the TMM factor of A against B is $1/2$.

*Proof.* The genes that B does not express have $r_g = 0$ and are dropped at line L1. For the shared genes, A has half of B's count share, $o_g/N = \frac12 r_g/N$, so $M_g = -1$ for every gene left. This is Theorem 4 with $L = H = \emptyset$ and $m = -1$. $\square$

The effective library size of A is then $N/2$: half of A's reads go to the genes that B lacks. Dividing by the raw library size would make every shared gene look two times lower in A.

**Rounding.** Theorem 4 needs exact ties. When the common ratio is not a power of 2, rounding can split the block $S$ into two blocks of slightly different values. Each block gets its own average rank, and both can fall outside $[\lambda_M, \eta_M]$. Then $\mathcal K$ is empty and the code, like edgeR, returns 1. The tests contain such a case. With a small spread in the M values of $S$, no ties occur, and Lemma 3 applies.

**Normalization over many samples.** norm_factors computes $f_j$ for every sample against one reference sample and divides by $(\prod_j f_j)^{1/m}$. The product of the results is 1 by construction. The choice of the reference (the upper quartile rule of edgeR) is a heuristic.

**Complexity.** Lines L1 to L4 take $\Theta(n)$ time and the two rankings take $\Theta(n\log n)$. With $m$ samples, norm_factors takes $\Theta(n m\log n)$ time, plus $\Theta(nm\log n)$ for the upper quartiles. The extra space is $\Theta(n)$ per factor.
