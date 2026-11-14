---
title: The pass computes the log-rank table, the centred terms are uncorrelated hypergeometric deviations, and the statistic is asymptotically chi-square with one degree of freedom
proves: [correctness]
status: full
---

Let the data be $(y_i, \delta_i, g_i)$, $i = 1, \ldots, n$, with distinct event times $t_1 < \cdots < t_k$ of the pooled sample, $n_j = \#\{i : y_i \ge t_j\}$, $n_{1j} = \#\{i : y_i \ge t_j, g_i = 1\}$, $n_{0j} = n_j - n_{1j}$, $d_j = \#\{i : y_i = t_j, \delta_i = 1\}$ and $d_{1j} = \#\{i : y_i = t_j, \delta_i = 1, g_i = 1\}$.

**Claim 1 (the pass computes the table).** Line L9 is executed once for each $j$, in increasing order of $t_j$, and at that moment $r = n_j$, $r_1 = n_{1j}$, $d = d_j$ and $d_1 = d_{1j}$. So the returned $U$ and $V$ are $\sum_j w_j (d_{1j} - E_{1j})$ and $\sum_j w_j^2 V_j$.

*Proof.* After the sort of line L1, the inner loop of line L6 reads exactly the subjects whose time equals the current distinct time $u$, and sets $m$, $m_1$, $d$, $d_1$ to the numbers of subjects, group-1 subjects, events and group-1 events at $u$. Invariant: at the start of the group at $u$, $r = \#\{i : y_i \ge u\}$ and $r_1 = \#\{i : y_i \ge u, g_i = 1\}$. It holds at the first group, where $r = n$ and $r_1 = \sum_i g_i$ by line L2. Line L10 subtracts all subjects at $u$, censored or not, so afterwards $r = \#\{i : y_i > u\}$, which is the count at risk at the next distinct time; the same holds for $r_1$. Line L7 skips the times with no event, and at an event time $u = t_j$ the invariant gives $r = n_j$ and $r_1 = n_{1j}$. Line L8 then computes $E_{1j}$ and $V_j$ by their formulas, and line L9 adds the terms. $\square$

## The null distribution

The asymptotic claims are proved for event and censoring times on a finite grid $\tau_1 < \cdots < \tau_K$, which covers all data recorded in days, weeks or months. The conditions are:

1. All times $T_i$ and $C_i$ take values in $\{\tau_1, \ldots, \tau_K\}$, and a subject censored at $\tau_l$ is at risk at $\tau_l$, so $y_i = \min(T_i, C_i)$ and $\delta_i = 1\{T_i \le C_i\}$.
2. The pairs $(T_i, C_i)$ are independent across subjects, identically distributed within each group, and $T_i$ is independent of $C_i$. The censoring distribution may differ between the groups.
3. Under $H_0$ both groups have the same discrete hazard $h_l = P(T = \tau_l \mid T \ge \tau_l)$ at each $\tau_l$.
4. The group sizes satisfy $n_1/n \to p \in (0, 1)$ as $n \to \infty$.
5. $\sigma^2 > 0$, with $\sigma^2$ defined in Claim 4. It holds when some $\tau_l$ has $0 < h_l < 1$ and positive probability of being at risk in both groups.

Write $R_{il} = 1\{y_i \ge \tau_l\}$ and $X_{il} = 1\{y_i = \tau_l, \delta_i = 1\}$. A grid time with no event contributes nothing to $U$ or $V$, so sums over the event times $t_j$ equal sums over all $\tau_l$ with $d_l = 0$ terms included.

**Claim 2 (hypergeometric conditional law).** Under conditions 1 to 3, let $\mathcal F_l$ be the history of the whole sample strictly before $\tau_l$ together with the labels, and $\mathcal G_l = \mathcal F_l \vee \sigma(d_l)$. Given $\mathcal G_l$, the set of subjects that fail at $\tau_l$ is uniform among the $\binom{n_l}{d_l}$ subsets of size $d_l$ of the risk set. Hence $d_{1l}$ given $\mathcal G_l$ is hypergeometric with

$$E[d_{1l} \mid \mathcal G_l] = \frac{d_l\, n_{1l}}{n_l} = E_{1l}, \qquad \mathrm{Var}(d_{1l} \mid \mathcal G_l) = \frac{n_{1l}\, n_{0l}\, d_l (n_l - d_l)}{n_l^2 (n_l - 1)} = V_l.$$

*Proof.* For a subject at risk at $\tau_l$, the history says only that $T_i \ge \tau_l$ and $C_i \ge \tau_l$, and by condition 2 the other subjects carry no information about it. So $P(X_{il} = 1 \mid \mathcal F_l) = P(T_i = \tau_l \mid T_i \ge \tau_l, C_i \ge \tau_l) = P(T_i = \tau_l \mid T_i \ge \tau_l) = h_l$ by the independence of $T_i$ and $C_i$ and condition 3, whatever the group. Given $\mathcal F_l$ the failure indicators of the $n_l$ subjects at risk are therefore independent Bernoulli($h_l$). For any fixed subset $A$ of the risk set with $|A| = d$, the probability that exactly $A$ fails is $h_l^d (1 - h_l)^{n_l - d}$, which does not depend on $A$, so given the total $d_l = d$ all subsets of size $d$ are equally likely.

Let $Z_a$ indicate that the group-1 subject $a$ fails. Then $P(Z_a = 1) = d/n$ and, for $a \ne b$, $P(Z_a = Z_b = 1) = d(d-1)/(n(n-1))$, writing $n = n_l$, $n_1 = n_{1l}$, $d = d_l$. The mean of $d_{1l} = \sum_a Z_a$ is $n_1 d/n$. Since

$$\frac{d(d-1)}{n(n-1)} - \frac{d^2}{n^2} = \frac{d\,[n(d-1) - d(n-1)]}{n^2(n-1)} = -\frac{d(n-d)}{n^2(n-1)},$$

the variance is

$$n_1 \frac{d}{n}\Big(1 - \frac{d}{n}\Big) - n_1(n_1 - 1)\frac{d(n-d)}{n^2(n-1)} = \frac{n_1 d(n-d)}{n^2}\Big(1 - \frac{n_1 - 1}{n - 1}\Big) = \frac{n_1 (n - n_1)\, d(n-d)}{n^2(n-1)}.$$

For $n = 1$ the variance is 0, which is the convention of line L8. $\square$

**Claim 3 (uncorrelated increments, exact mean and variance).** Let the weight $w_l$ be $\mathcal G_l$-measurable and bounded, which holds for all five weight rules, and let $D_l = w_l(d_{1l} - E_{1l})$. Then $E[D_l \mid \mathcal G_l] = 0$, $E[D_l^2 \mid \mathcal G_l] = w_l^2 V_l$ and $E[D_l D_m] = 0$ for $l < m$. Consequently $E[U_w] = 0$ and $\mathrm{Var}(U_w) = E[V_w]$ exactly, for every $n$.

*Proof.* The first two identities are Claim 2 multiplied by the $\mathcal G_l$-measurable $w_l$. For $l < m$, $D_l$ is determined by the history before $\tau_m$, so it is $\mathcal G_m$-measurable and $E[D_l D_m] = E[D_l\, E[D_m \mid \mathcal G_m]] = 0$. Summing gives $E[U_w] = 0$ and $E[U_w^2] = \sum_l E[D_l^2] = \sum_l E[w_l^2 V_l] = E[V_w]$. $\square$

So $V$ is an unbiased estimate of the null variance of $U$ in finite samples. The normal approximation is asymptotic.

**Claim 4 (asymptotic normality).** Under conditions 1 to 5 and $H_0$, for the log-rank weight $w_l = 1$, $U/\sqrt V \to N(0, 1)$ in distribution, so $X^2 = U^2/V \to \chi^2_1$.

*Proof.* Let $\pi_{gl} = P(y \ge \tau_l \mid \text{group } g)$, $a_l = p\,\pi_{1l}$, $b_l = (1 - p)\,\pi_{0l}$, $m_l = a_l + b_l$, and for $m_l > 0$ set $q_l = a_l/m_l$ and $\hat q_l = n_{1l}/n_l$. Drop the grid points with $m_l = 0$, at which nobody is ever at risk.

*Step 1 (an exact identity).* For each $l$ with $n_l > 0$, $\sum_i (g_i - \hat q_l) R_{il} = n_{1l} - \hat q_l n_l = 0$ and $\sum_i (g_i - \hat q_l) X_{il} = d_{1l} - \hat q_l d_l = d_{1l} - E_{1l}$. Hence, for any numbers $h_l$,

$$U = \sum_l \sum_i (g_i - \hat q_l)(X_{il} - h_l R_{il}) = \sum_i \psi_i + \sum_l (q_l - \hat q_l)\, M_l,$$

with $\psi_i = \sum_l (g_i - q_l)(X_{il} - h_l R_{il})$ and $M_l = \sum_i (X_{il} - h_l R_{il})$.

*Step 2 (moments of one subject).* Fix $i$ and let $\varepsilon_l = X_{il} - h_l R_{il}$. By the argument of Claim 2, $E[X_{il} \mid R_{il} = 1] = h_l$, and $\varepsilon_l = 0$ when $R_{il} = 0$, so $E[\varepsilon_l] = 0$. Since $X_{il}^2 = X_{il}$ and $X_{il} R_{il} = X_{il}$, $E[\varepsilon_l^2] = h_l E R_{il} - 2h_l^2 E R_{il} + h_l^2 E R_{il} = h_l(1 - h_l) E R_{il}$. For $l < m$, $\varepsilon_m \ne 0$ only if $y_i \ge \tau_m$, and then $X_{il} = 0$ and $R_{il} = 1$, so $\varepsilon_l \varepsilon_m = -h_l \varepsilon_m$ and $E[\varepsilon_l \varepsilon_m] = -h_l E[\varepsilon_m] = 0$. Therefore $E[\psi_i] = 0$ and

$$\mathrm{Var}(\psi_i) = \sum_l (g_i - q_l)^2\, h_l (1 - h_l)\, \pi_{g_i l}.$$

*Step 3 (CLT for the main term).* The $\psi_i$ are independent, bounded by $\sum_l (1 + h_l) \le 2K$, and

$$\frac1n \sum_i \mathrm{Var}(\psi_i) = \frac{n_1}{n}\sum_l (1 - q_l)^2 h_l(1 - h_l)\pi_{1l} + \frac{n_0}{n}\sum_l q_l^2 h_l(1 - h_l)\pi_{0l} \to \sum_l h_l(1 - h_l)\big[a_l (1 - q_l)^2 + b_l q_l^2\big].$$

Since $a_l(b_l/m_l)^2 + b_l(a_l/m_l)^2 = a_l b_l/m_l$, the limit is $\sigma^2 = \sum_l h_l (1 - h_l)\, a_l b_l/m_l$, positive by condition 5. The total variance grows like $n\sigma^2 \to \infty$ while the summands stay bounded, so the Lindeberg condition holds, and the Lindeberg-Feller [central limit theorem](/central-limit-theorem/) gives $n^{-1/2}\sum_i \psi_i \to N(0, \sigma^2)$.

*Step 4 (the remainder vanishes).* By Step 2, $M_l$ is a sum of $n$ independent mean-zero terms with variance at most $1/4$ each, so $E[(n^{-1/2} M_l)^2] \le 1/4$ and $n^{-1/2}M_l$ is bounded in probability. By the [law of large numbers](/law-of-large-numbers/), $n_{1l}/n \to a_l$ and $n_l/n \to m_l > 0$ in probability, so $\hat q_l \to q_l$. Each product $(q_l - \hat q_l)\, n^{-1/2} M_l$ tends to 0 in probability, and so does their finite sum. By [Slutsky's theorem](/slutsky-theorem/), $n^{-1/2} U \to N(0, \sigma^2)$.

*Step 5 (the variance estimate).* By the law of large numbers, $n_{1l}/n \to a_l$, $n_{0l}/n \to b_l$, $n_l/n \to m_l$, and $d_l/n \to E[X_{il}]$ averaged over the groups, which is $h_l m_l$. So $V_l/n = (n_{1l}/n)(n_{0l}/n)(d_l/n)((n_l - d_l)/n)/((n_l/n)^2 ((n_l - 1)/n)) \to a_l b_l h_l m_l \cdot m_l (1 - h_l)/m_l^3 = h_l(1 - h_l) a_l b_l/m_l$, by continuity of this rational function where $m_l > 0$. Summing over the $K$ grid points, $V/n \to \sigma^2$ in probability. By Slutsky's theorem, $U/\sqrt V = (n^{-1/2}U)/\sqrt{V/n} \to N(0, 1)$, and by continuity of $x \mapsto x^2$, $X^2 \to \chi^2_1$. $\square$

The same proof covers a weight with $w_l/c_n \to \omega_l$ in probability for deterministic constants $c_n$ and $\omega_l$: Gehan's $w_l = n_l$ with $c_n = n$, Tarone and Ware's $\sqrt{n_l}$ with $c_n = \sqrt n$, and the Peto-Peto and Fleming-Harrington weights with $c_n = 1$, since $\hat S$ and the Peto product converge to deterministic limits at each grid point. The exact identity of Step 1 holds term by term, so $U_w/c_n = \sum_i \sum_l \omega_l (g_i - q_l)\varepsilon_{il} + o_P(n^{1/2})$, and the limit variance $\sum_l \omega_l^2 h_l(1 - h_l) a_l b_l/m_l$ is the limit of $V_w/(c_n^2 n)$. For continuous time, the same result follows from Rebolledo's martingale central limit theorem applied to the counting process martingales $N_{gi}(t) - \int_0^t R_{gi}(s)\, dH(s)$; see Andersen, Borgan, Gill and Keiding (1993), Chapter V.

The size of the test in finite samples is not proved. The tables on the algorithm page give measured sizes.

## The score test and the permutation test

**Claim 5 (score test of the Cox model).** With the covariate $x_i = g_i$, the Cox log partial likelihood with Breslow's handling of ties is $\ell(\beta) = \sum_j [\beta d_{1j} - d_j \log(n_{0j} + n_{1j} e^\beta)]$. Its derivative at $\beta = 0$ is $U$, and its negative second derivative at $\beta = 0$ is $\sum_j d_j n_{1j} n_{0j}/n_j^2$, which equals $V$ when every $d_j = 1$.

*Proof.* $\frac{d}{d\beta} d_j \log(n_{0j} + n_{1j}e^\beta) = d_j n_{1j} e^\beta/(n_{0j} + n_{1j} e^\beta)$, which is $E_{1j}$ at $\beta = 0$, so $\ell'(0) = \sum_j (d_{1j} - E_{1j}) = U$. Differentiating again gives $d_j n_{1j} n_{0j} e^\beta/(n_{0j} + n_{1j}e^\beta)^2$, which is $d_j n_{1j} n_{0j}/n_j^2$ at $\beta = 0$. When $d_j = 1$, $V_j = n_{1j} n_{0j} (n_j - 1)/(n_j^2 (n_j - 1)) = n_{1j} n_{0j}/n_j^2$. $\square$

**Claim 6 (exact permutation test).** If, in addition to conditions 2 and 3, both groups have the same censoring distribution, then under $H_0$ the pairs $(y_i, \delta_i)$ are independent and identically distributed over all $n$ subjects. Given the multiset of pairs, every assignment of the labels with $n_1$ ones is equally likely, so the permutation p-value $P^*(|U^*| \ge |U|)$ over the $\binom{n}{n_1}$ relabellings satisfies $P(p \le \alpha) \le \alpha$ for every $\alpha$, and the Monte Carlo version with $(1 + \#)/(1 + b)$ has the same property. If the censoring distributions differ, the pairs are not exchangeable between groups, and the permutation test can have any size.

*Proof.* The joint law of i.i.d. pairs is invariant under permutations of the subjects, and the labels are fixed in advance, so conditioning on the multiset makes all relabellings equiprobable. The validity of a p-value defined as the tail proportion of a statistic over a group of transformations under which the data are invariant, including the $(1 + \#)/(1 + b)$ rule, is proved on the [permutation test](/permutation-test/) page. $\square$

## Cost

The sort costs $O(n \log n)$ comparisons. Lines L4 to L10 advance $i$ once for each subject, and lines L7 to L9 run at most once per distinct time, each with $O(1)$ arithmetic operations, so the pass costs $O(n)$. The space is the sorted index array, $O(n)$, plus $O(k)$ for the optional table of rows.
