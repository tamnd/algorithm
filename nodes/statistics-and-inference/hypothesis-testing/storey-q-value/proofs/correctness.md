---
title: Storey's q-values are minimal estimated FDRs, and the Storey-Taylor-Siegmund procedure has FDR at most (1 - lambda^(m_0)) q under independence
proves: [correctness]
status: full
---

We prove three things. First, the lines of the page compute the q-values of the definition, and rejecting $\hat q_i \le q$ is BH at level $q/\hat\pi_0$ (Proposition 1). Second, the uncapped estimate of $\pi_0$ is biased upward (Proposition 2). Third, the modified procedure of Storey, Taylor and Siegmund (2004) has $\text{FDR} \le (1 - \lambda^{m_0})q$ when the null p-values are independent of each other and of the non-null ones and valid (Theorem 4). The proof of Theorem 4 is a leave-one-out argument, not the martingale proof of the paper; it also covers discrete valid p-values, which is what the exact grid test in the code uses. The asymptotic control of the plain procedure under weak dependence is only cited.

**Setting.** P-values $p_1, \dots, p_m \in [0, 1]$, $0 \le \lambda < 1$, a level $q \in (0, 1]$, $N(t) = \#\{j : p_j \le t\}$ and $W = \#\{j : p_j > \lambda\} = m - N(\lambda)$. $I_0$ is the set of true nulls, $m_0 = |I_0|$, and a null p-value is valid when $P(p_i \le u) \le u$ for all $u$.

**Proposition 1 (what the lines compute).** Let $\hat\pi_0 = \min(1, W/(m(1 - \lambda)))$ and $\widehat{\text{FDR}}(t) = \hat\pi_0mt/\max(N(t), 1)$. Lines L3 to L6 compute $\hat q_{(r)} = \min_{j \ge r}\min(1, \hat\pi_0mp_{(j)}/j)$, and this equals $\min\{\min(1, \widehat{\text{FDR}}(t)) : t \ge p_{(r)}, t \in \{p_1, \dots, p_m\}\}$, the definition that the tests use as a brute force. For $q \le 1$, $\{i : \hat q_i \le q\}$ is the rejected set of BH at level $q/\hat\pi_0$ when $\hat\pi_0 > 0$.

*Proof.* The loop keeps a running minimum from the right, starting at 1, which gives the formula. For $t = p_{(j)}$, $N(t) \ge j$, with equality when $j$ is the last rank among values equal to $p_{(j)}$. So $\widehat{\text{FDR}}(p_{(j)}) = \hat\pi_0mp_{(j)}/j'$ for the last such rank $j'$, which is the smallest of the terms $\hat\pi_0mp_{(l)}/l$ over the ranks $l$ tied with $j$. Hence the minimum over the data points $t \ge p_{(r)}$ equals the minimum over ranks $j \ge r$. Finally $\hat q_{(r)} \le q$ if and only if $\hat\pi_0mp_{(j)} \le jq$ for some $j \ge r$, that is, $p_{(j)} \le j(q/\hat\pi_0)/m$ for some $j \ge r$, which is the rejection of rank $r$ by BH at level $q/\hat\pi_0$ (Lemma 1 in the proof for the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/)). $\square$

If $\hat\pi_0 = 0$, every p-value is at most $\lambda$, every q-value is 0, and everything is rejected. This is one reason for the modified estimator below.

**Proposition 2 (upward bias).** If each null p-value is valid, then $E[W/(m(1 - \lambda))] \ge m_0/m$.

*Proof.* For $i \in I_0$, $P(p_i > \lambda) = 1 - P(p_i \le \lambda) \ge 1 - \lambda$. So $E[W] \ge \sum_{i \in I_0}P(p_i > \lambda) \ge m_0(1 - \lambda)$. $\square$

**The modified procedure.** Let $\hat\pi_0^* = (1 + W)/(m(1 - \lambda))$ and $t_k = \min(\lambda, kq/(m\hat\pi_0^*)) = \min(\lambda, kq(1 - \lambda)/(1 + W))$. The procedure rejects the $k$ smallest p-values for the largest $k$ with $p_{(k)} \le t_k$, or nothing. The thresholds are nondecreasing in $k$, so, as in Lemma 1 of the BH proof, the number of rejections is $R = \max\{k : N(t_k) \ge k\}$ and the rejected set is $\{i : p_i \le t_R\}$.

**Lemma 3 (step-up with fixed thresholds, leave one out).** Let $0 \le s_1 \le \dots \le s_m$ be fixed thresholds and consider the step-up procedure that rejects $\{j : p_j \le s_R\}$ with $R = \max\{k : N(s_k) \ge k\}$. Fix $i$, let $R^{(i)}$ be its number of rejections when $p_i$ is replaced by 0, and suppose $s_1 \ge 0$ so that $R^{(i)} \ge 1$. Then $H_i$ is rejected with $R = k$ exactly when $p_i \le s_k$ and $R^{(i)} = k$.

*Proof.* The proof of Lemma 3 in the proof for the Benjamini-Hochberg procedure uses only that the thresholds are nondecreasing, so it applies word for word with $s_k$ in place of $kq/m$. $\square$

**Theorem 4 (Storey, Taylor and Siegmund).** Suppose that the null p-values are valid, that each null p-value is independent of all the other p-values, and that the null p-values are mutually independent. Then the modified procedure has
$$\text{FDR} \le (1 - \lambda^{m_0})q \le q.$$

*Proof.* Fix $i \in I_0$ and let $W_{-i} = \#\{j \ne i : p_j > \lambda\}$, a function of the other p-values only. Define the fixed thresholds, given the other p-values, $s_k = \min(\lambda, kq(1 - \lambda)/(1 + W_{-i}))$.

*Step 1: on the event that matters, the procedure is the fixed one.* If $p_i \le \lambda$, then $W = W_{-i}$, so $t_k = s_k$ for all $k$ and the two procedures make the same decisions. If $p_i > \lambda$, then $H_i$ is rejected by neither, since both have thresholds at most $\lambda$. So in all cases $\mathbf 1\{H_i \text{ rejected}\}/\max(R, 1) = \mathbf 1\{H_i \text{ rejected by } s\}/\max(R_s, 1)$, where $R_s$ is the number of rejections with the thresholds $s$.

*Step 2: condition on the others.* Given $(p_j)_{j \ne i}$, the thresholds $s_k$ and the count $R_s^{(i)}$ of Lemma 3 are fixed, and $p_i$ keeps its law, by independence. By Lemma 3,
$$E\left[\frac{\mathbf 1\{H_i \text{ rejected}\}}{\max(R, 1)} \,\middle|\, (p_j)_{j \ne i}\right] = \sum_{k=1}^m \frac1k P(p_i \le s_k)\mathbf 1\{R_s^{(i)} = k\} \le \sum_{k=1}^m \frac{s_k}{k}\mathbf 1\{R_s^{(i)} = k\} \le \frac{q(1 - \lambda)}{1 + W_{-i}},$$
because $s_k/k \le q(1 - \lambda)/(1 + W_{-i})$ and exactly one indicator is 1.

*Step 3: average over $W_{-i}$.* $W_{-i} \ge B$, where $B$ is the number of null $j \ne i$ with $p_j > \lambda$. The $m_0 - 1$ events $\{p_j > \lambda\}$ are independent, each with probability at least $1 - \lambda$, so $B$ is stochastically larger than a binomial variable $B'$ with $n = m_0 - 1$ trials and success probability $r = 1 - \lambda$. Since $x \mapsto 1/(1 + x)$ is decreasing,
$$E\left[\frac1{1 + W_{-i}}\right] \le E\left[\frac1{1 + B'}\right] = \sum_{b=0}^n \binom nb\frac{r^b(1 - r)^{n-b}}{b + 1} = \frac1{(n + 1)r}\sum_{b=0}^n \binom{n+1}{b+1}r^{b+1}(1 - r)^{n-b} = \frac{1 - (1 - r)^{n+1}}{(n + 1)r},$$
using $\binom nb/(b + 1) = \binom{n+1}{b+1}/(n + 1)$ and the binomial theorem with the missing term $b + 1 = 0$. With $n + 1 = m_0$ and $r = 1 - \lambda$ this is $(1 - \lambda^{m_0})/(m_0(1 - \lambda))$.

*Step 4: sum.* Taking expectations in Step 2 and using Step 3,
$$E\left[\frac{\mathbf 1\{H_i \text{ rejected}\}}{\max(R, 1)}\right] \le q(1 - \lambda)\cdot\frac{1 - \lambda^{m_0}}{m_0(1 - \lambda)} = \frac{(1 - \lambda^{m_0})q}{m_0}.$$
Summing over the $m_0$ true nulls gives $\text{FDR} \le (1 - \lambda^{m_0})q$. If $m_0 = 0$ the FDR is 0. $\square$

The added 1 in $\hat\pi_0^*$ is what makes Step 3 work: it turns $1/W$, whose mean is infinite when $W$ can be 0, into $1/(1 + W)$, whose mean has the closed form above. The limit $t \le \lambda$ is what makes Step 1 work: a rejected null p-value is never counted in $W$.

**Theorem 5 (equivalent threshold form).** The modified procedure rejects $\{i : p_i \le \hat t\}$, where $\hat t = \sup\{t \in [0, \lambda] : \hat\pi_0^*mt \le q\max(N(t), 1)\}$, the definition of Storey, Taylor and Siegmund.

*Proof.* Write $c = \hat\pi_0^*m$ and let $A = \{t \in [0, \lambda] : ct \le q\max(N(t), 1)\}$, the set of admissible $t$. It contains 0.

$A$ contains its supremum. Take $t_n \in A$ with $t_n \to \hat t$ and $t_n \le \hat t$. Since $N$ is nondecreasing, $ct_n \le q\max(N(t_n), 1) \le q\max(N(\hat t), 1)$, and letting $n \to \infty$ gives $c\hat t \le q\max(N(\hat t), 1)$. Also $\hat t \le \lambda$. So $\hat t \in A$.

Let $j = N(\hat t)$. If $j \ge 1$, then $p_{(j)} \le \hat t \le \lambda$ and $cp_{(j)} \le c\hat t \le qj$, so $p_{(j)} \le t_j$ and $j \le R$. If $R \ge 1$, then $p_{(R)} \le t_R \le \lambda$ and $cp_{(R)} \le qR \le qN(p_{(R)})$, so $p_{(R)} \in A$ and $\hat t \ge p_{(R)}$, which gives $j \ge R$. Hence $N(\hat t) = R$ in all cases. A set of the form $\{i : p_i \le t\}$ with exactly $R$ elements is the set of the $R$ smallest p-values, with no tie split, so $\{i : p_i \le \hat t\} = \{i : p_i \le t_R\}$. $\square$

The test file checks Theorem 5 directly: it computes $\hat t$ as the largest admissible point among 0, $\lambda$, the p-values and the points $jq/(m\hat\pi_0^*)$, where the supremum must be attained, and compares the rejected sets in exact arithmetic.

**What is cited, not proved.** Storey, Taylor and Siegmund (2004, Theorems 4 to 7) show that, for large $m$, under convergence conditions on the empirical distribution functions of the null and non-null p-values that allow weak dependence, the plain procedure with $\hat\pi_0$ controls the FDR asymptotically and the q-values are simultaneously conservative. The tests measure the plain procedure in one model with $m = 40$ and find an FDR of 0.112 at $q = 0.1$, which shows that the plain version has no finite-sample guarantee.
