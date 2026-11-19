---
title: Correctness of the RAPT pitch tracker
proves: [correctness]
status: full
---

RAPT is an estimator with costs set by hand, so we do not prove that its track is the true pitch. We prove the facts that the method relies on: the range of the NCCF and its value at the period, the bound on the spectral term $S$, and the optimality of the dynamic program.

## Lemma 1 (the NCCF is bounded)

If $e_m e_{m+k} > 0$, then $|\phi(k)| \le 1$.

*Proof.* With $u_j = x_{m+j}$ and $v_j = x_{m+k+j}$ for $0 \le j < n$, the numerator is $\sum_j u_j v_j$, and $e_m = \sum_j u_j^2$, $e_{m+k} = \sum_j v_j^2$. By the Cauchy-Schwarz inequality, $|\sum_j u_j v_j| \le \sqrt{\sum_j u_j^2} \sqrt{\sum_j v_j^2}$. Divide by the right side. $\square$

## Lemma 2 (the NCCF is 1 at the period)

If $x_{j + P} = x_j$ for all $j$ in $[m, m + n + K)$ and $e_m > 0$, then $\phi(qP) = 1$ for every integer $q \ge 1$ with $qP \le K$.

*Proof.* By induction on $q$, $x_{j + qP} = x_j$ for $m \le j < m + n$. So $v = u$ in Lemma 1, the numerator is $e_m$ and $e_{m+qP} = e_m$, and $\phi(qP) = e_m / \sqrt{e_m^2} = 1$. $\square$

Equality in Cauchy-Schwarz holds only when $v$ is a positive multiple of $u$. So in a periodic signal the value 1 marks the multiples of the period, and a peak of 1 at a lag that is not a multiple needs a signal that is periodic with that lag too. This is why each multiple of the period is a candidate and the lag cost LAG_WT is needed to prefer the shortest.

## Lemma 3 (the Itakura ratio is at least 1)

Let $R$ be the $(p+1) \times (p+1)$ Toeplitz matrix of an autocorrelation sequence $r_0, \ldots, r_p$ with $R$ positive definite, let $a_r = (1, -a_1, \ldots, -a_p)$ be the inverse filter from the Levinson-Durbin recursion on $r$, and let $b$ be any vector with $b_0 = 1$. Then $b^\top R b \ge a_r^\top R a_r > 0$, so $I = b^\top R b / a_r^\top R a_r \ge 1$ and $S = 0.2 / (I - 0.8) \in (0, 1]$.

*Proof.* Write $b = (1, -c)$ with $c \in \mathbb{R}^p$. Then $b^\top R b = r_0 - 2 c^\top \rho + c^\top T c$, with $\rho = (r_1, \ldots, r_p)$ and $T$ the leading $p \times p$ block of $R$, which is positive definite. This quadratic in $c$ has its unique minimum where $T c = \rho$, the normal equations of linear prediction. The Levinson-Durbin recursion solves exactly these equations, so $c = (a_1, \ldots, a_p)$ attains the minimum. The minimum is positive because $R$ is positive definite and $b \ne 0$. Then $I \ge 1$ gives $I - 0.8 \ge 0.2$ and $0 < S \le 1$. $\square$

The code computes $r$ from a windowed segment, which makes $R$ positive semidefinite, and positive definite unless the segment is degenerate; for a silent segment it returns $I = 1$. In floating point the computed $I$ can fall below 1 by rounding.

## Lemma 4 (the local costs are bounded)

For a voiced candidate with $0 < C \le 1$ and $0 < L \le K + 1$, the local cost $d = 1 - C(1 - \text{LAG\_WT}\, L / K)$ lies in $[0, 1 + \text{LAG\_WT}]$ when LAG_WT $\le 1$, and among candidates with equal $C$ it grows with $L$.

*Proof.* The factor $1 - \text{LAG\_WT}\, L / K$ lies in $[1 - \text{LAG\_WT}(1 + 1/K), 1)$, so $C$ times it lies in an interval inside $[-\text{LAG\_WT}, 1)$, and $d$ in $(0, 1 + \text{LAG\_WT}]$. For fixed $C > 0$, $d$ is increasing in $L$ with slope $C \cdot \text{LAG\_WT} / K > 0$. $\square$

So, for equal correlation, a shorter period always has the lower local cost, which is how RAPT breaks the tie of Lemma 2 between multiples of the period.

## Theorem (the dynamic program is optimal)

Let frame $i$ have candidates $0, \ldots, c_i - 1$ with local costs $d_i(j)$, and let $\delta_i(k, j)$ be the cost of moving from candidate $k$ of frame $i - 1$ to candidate $j$ of frame $i$. The cost of a path $j_1, \ldots, j_F$ is

$$\mathrm{cost}(j_1, \ldots, j_F) = d_1(j_1) + \sum_{i=2}^{F} \bigl( d_i(j_i) + \delta_i(j_{i-1}, j_i) \bigr).$$

The path returned by lines L5 to L9 has the least cost of all paths.

*Proof.* Let $V_i(j)$ be the least cost of a path over frames $1, \ldots, i$ that ends at candidate $j$ of frame $i$. We show $D_i(j) = V_i(j)$ by induction on $i$. For $i = 1$ a path is one candidate, so $V_1(j) = d_1(j) = D_1(j)$ by line L5. For $i \ge 2$, a path that ends at $j$ is a path over frames $1, \ldots, i - 1$ that ends at some $k$, followed by $j$, and its cost is the cost of the prefix plus $d_i(j) + \delta_i(k, j)$. For a fixed $k$ this is least when the prefix is a best path to $k$, of cost $V_{i-1}(k) = D_{i-1}(k)$ by the induction hypothesis. Minimizing over $k$ gives

$$V_i(j) = d_i(j) + \min_k \bigl( D_{i-1}(k) + \delta_i(k, j) \bigr),$$

which is line L7. So $D_F(j) = V_F(j)$, and line L8 picks $j_F$ with the least $V_F$, which is the least cost of any path.

For the back pointers, $\psi_i(j)$ attains the minimum above, so $V_i(j_i) = V_{i-1}(j_{i-1}) + d_i(j_i) + \delta_i(j_{i-1}, j_i)$ with $j_{i-1} = \psi_i(j_i)$. Summing these equations for $i = F$ down to 2 and adding $V_1(j_1) = d_1(j_1)$ shows that the path from line L9 has cost $V_F(j_F)$. $\square$

The proof needs no sign or bound on the costs, and no relation between the transition costs of different frames. So it holds for the costs of Talkin, which depend on the frame through $r_i$ and $S_i$, and for any other choice. Ties are broken toward the smallest candidate index, which does not change the cost.

## The transition costs

Two facts about the voiced-to-voiced cost $\delta = \text{FREQ\_WT} \min(\xi, \text{DOUBL\_C} + |\xi - \ln 2|)$ with $\xi = |\ln(L_j / L_k)|$ follow from the formula. It is symmetric in the two lags, since $\xi$ is. And for $\xi$ near $\ln 2$, a jump of one octave, the second term is the smaller one when $|\xi - \ln 2| < \ln 2 - \text{DOUBL\_C}$ and $\xi > \text{DOUBL\_C} + |\xi - \ln 2|$, so an octave jump costs $\text{FREQ\_WT} \cdot \text{DOUBL\_C} = 0.007$ with the defaults instead of $\text{FREQ\_WT} \ln 2 \approx 0.0139$.
