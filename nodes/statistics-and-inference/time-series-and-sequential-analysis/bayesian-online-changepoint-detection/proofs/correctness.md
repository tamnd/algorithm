---
title: The BOCPD recursion computes the exact run-length posterior and the evidence of the renewal change-point model
proves: [correctness]
status: full
---

Notation is that of the page. The model has three parts. (i) The segmentation is a renewal process: with $r_1 = 1$, and given $r_1, \ldots, r_{t-1}$, the run length $r_t$ equals 1 with probability $H(r_{t-1})$ and $r_{t-1} + 1$ otherwise. (ii) Each segment $j$ has a parameter $\theta_j$, and $\theta_1, \theta_2, \ldots$ are i.i.d. from the prior $\pi$ and independent of the segmentation. (iii) Given the segmentation and the parameters, $x_1, x_2, \ldots$ are independent, and a point of segment $j$ has density $p(\cdot \mid \theta_j)$. All densities are with respect to a fixed measure, and $\pi_t^{(r)} = p(x_t \mid x_{t-r..t-1})$ is the predictive density of the page, computed under the model of one segment, with $\pi_t^{(0)}$ the prior predictive. Write $\mathbf r_t = (r_1, \ldots, r_t)$ and $J_t(r) = p(r_t = r, x_{1..t})$.

The sequence $\mathbf r_t$ determines the segmentation of $1, \ldots, t$, and $r_t = r$ means that the current segment is $\{t - r + 1, \ldots, t\}$.

**Lemma 1 (transition).** $P(r_t = \cdot \mid \mathbf r_{t-1}, x_{1..t-1}) = P(r_t = \cdot \mid r_{t-1})$, given by $H(r_{t-1})$ for the value 1 and $1 - H(r_{t-1})$ for the value $r_{t-1} + 1$.

*Proof.* By (i), $r_t$ is a function of $r_{t-1}$ and a fresh coin with success probability $H(r_{t-1})$, independent of everything else before time $t$. The data $x_{1..t-1}$ are, by (ii) and (iii), functions of $\mathbf r_{t-1}$, the parameters and independent noise, all independent of that coin given $\mathbf r_{t-1}$. So conditioning on $x_{1..t-1}$ as well as on $\mathbf r_{t-1}$ does not change the law of the coin. $\square$

**Lemma 2 (predictive).** For $r \in \{1, \ldots, t\}$, $p(x_t \mid \mathbf r_t, x_{1..t-1}) = \pi_t^{(r_t - 1)}$ on the event $r_t = r$. In particular this conditional density depends on $\mathbf r_t$ only through $r_t$.

*Proof.* Fix $\mathbf r_t$ with $r_t = r$. The segmentation of $1, \ldots, t$ is then fixed, and the current segment $j$ is $\{t - r + 1, \ldots, t\}$. By (ii) and (iii), the points of segments other than $j$ are functions of parameters $\theta_i$, $i \ne j$, and noise, all independent of $(\theta_j, x_{t-r+1}, \ldots, x_t)$. So, given $\mathbf r_t$, the vector $(x_{t-r+1}, \ldots, x_t)$ is independent of the other earlier points, and
$$p(x_t \mid \mathbf r_t, x_{1..t-1}) = p(x_t \mid \mathbf r_t, x_{t-r+1..t-1}).$$
Given $\mathbf r_t$, the points $x_{t-r+1}, \ldots, x_t$ are i.i.d. given $\theta_j$ with $\theta_j \sim \pi$, which is the model of one segment, so the right side is $\int p(x_t \mid \theta)\pi(\theta \mid x_{t-r+1..t-1})\,d\theta = \pi_t^{(r-1)}$. $\square$

**Lemma 3 (the joint recursion).** $J_1(1) = \pi_1^{(0)}$, and for $t \ge 2$,
$$J_t(r + 1) = J_{t-1}(r)\,(1 - H(r))\,\pi_t^{(r)} \quad (1 \le r \le t - 1), \qquad J_t(1) = \pi_t^{(0)}\sum_{r=1}^{t-1}J_{t-1}(r)\,H(r).$$

*Proof.* For $t = 1$, $r_1 = 1$ and $x_1$ has the prior predictive density. For $t \ge 2$, by the chain rule,
$$p(\mathbf r_t, x_{1..t}) = p(\mathbf r_{t-1}, x_{1..t-1})\,P(r_t \mid \mathbf r_{t-1}, x_{1..t-1})\,p(x_t \mid \mathbf r_t, x_{1..t-1}).$$
By Lemmas 1 and 2 the last two factors are $P(r_t \mid r_{t-1})$ and $\pi_t^{(r_t - 1)}$, which depend on $\mathbf r_{t-1}$ only through $r_{t-1}$. Sum over $r_1, \ldots, r_{t-2}$ with $r_{t-1}$ and $r_t$ fixed:
$$p(r_{t-1}, r_t, x_{1..t}) = J_{t-1}(r_{t-1})\,P(r_t \mid r_{t-1})\,\pi_t^{(r_t - 1)}.$$
If $r_t = r + 1 \ge 2$, the only $r_{t-1}$ with positive transition probability is $r$, with probability $1 - H(r)$, which gives the first formula. If $r_t = 1$, every $r_{t-1}$ contributes with probability $H(r_{t-1})$, which gives the second. $\square$

**Theorem.** After line L7 at step $t$, $P(r) = P(r_t = r \mid x_{1..t})$ for every $r \in \{1, \ldots, t\}$, the stored statistics stats$(r)$ summarize $x_{t-r+1..t}$, and $Z_{\mathrm{all}} = p(x_{1..t})$. The step costs $O(t)$ predictive evaluations and updates.

*Proof.* By induction on $t$. Before step 1, $P$ is empty and $Z_{\mathrm{all}} = 1 = p(\text{no data})$. Suppose the claim holds after step $t - 1$, so $P(r) = J_{t-1}(r)/p(x_{1..t-1})$ and stats$(r)$ summarizes the last $r$ points. Then line L3 computes $\pi(r) = \pi_t^{(r)}$ and $\pi_0 = \pi_t^{(0)}$. Lines L4 and L5 compute $J(\cdot) = J_t(\cdot)/p(x_{1..t-1})$ by Lemma 3; for $t = 1$, line L5 gives $J(1) = \pi_1^{(0)} = J_1(1)$ directly. Line L6 moves each statistic up by one run length and adds $x_t$, so stats$(r + 1)$ summarizes $x_{t-r..t}$, and stats$(1)$ summarizes $x_t$ alone. At line L7, $Z = \sum_r J_t(r)/p(x_{1..t-1}) = p(x_{1..t})/p(x_{1..t-1}) = p(x_t \mid x_{1..t-1})$, so $Z_{\mathrm{all}}$ becomes $p(x_{1..t})$, and $P = J/Z = J_t/p(x_{1..t})$, which is the posterior by [Bayes' theorem](/bayes-theorem/). Each step loops over at most $t - 1$ stored run lengths. $\blacksquare$

**Pruning.** If run lengths with small posterior are dropped and the rest renormalized, the recursion is applied to a truncated distribution, and the result is an approximation. Its error is not bounded here.
