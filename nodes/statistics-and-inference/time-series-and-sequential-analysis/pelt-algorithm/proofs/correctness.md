---
title: The pruning rule of PELT never removes an optimal last change point, so PELT returns the exact optimal partitioning
proves: [correctness]
status: full
---

Notation is that of the page. For $0 \le s < t \le n$, $C(s, t)$ is the cost of the segment $x_{s+1}, \ldots, x_t$. A segmentation of $x_1, \ldots, x_t$ is a set of change points $0 < \tau_1 < \cdots < \tau_m < t$, and its penalized cost is $\sum_{j=0}^{m}C(\tau_j, \tau_{j+1}) + \beta m$ with $\tau_0 = 0$ and $\tau_{m+1} = t$. Let $\mathrm{OPT}(t)$ be the smallest penalized cost over all segmentations of $x_1, \ldots, x_t$, and $\mathrm{OPT}(0) = -\beta$. We assume that there is a constant $K$ with
$$C(a, s) + C(s, b) + K \le C(a, b) \quad \text{for all } 0 \le a < s < b \le n. \tag{P}$$
For $s < T$ write $V_T(s) = \mathrm{OPT}(s) + C(s, T) + \beta$.

**Lemma 1 (optimal partitioning).** For $1 \le t \le n$, $\mathrm{OPT}(t) = \min_{0 \le s < t}V_t(s)$. If $s$ attains the minimum, then an optimal segmentation of $x_1, \ldots, x_s$ followed by the segment $x_{s+1..t}$ is an optimal segmentation of $x_1, \ldots, x_t$.

*Proof.* Group the segmentations of $x_1, \ldots, x_t$ by their last change point $s = \tau_m$, with $s = 0$ when there is none. For $s \ge 1$, the segmentations with last change point $s$ are exactly the segmentations of $x_1, \ldots, x_s$ followed by the segment $x_{s+1..t}$, and the penalized cost is the cost of the first part plus $C(s, t) + \beta$, since one change point is added. The smallest such cost is $V_t(s)$. For $s = 0$ the only segmentation is one segment, of cost $C(0, t) = -\beta + C(0, t) + \beta = V_t(0)$. Taking the minimum over $s$ gives the recursion, and the second claim follows from the same grouping. $\square$

**Lemma 2 (pruning).** Let $0 \le s < t < T \le n$. If $\mathrm{OPT}(s) + C(s, t) + K > \mathrm{OPT}(t)$, then $V_T(s) > V_T(t)$.

*Proof.* By (P) with $a = s$, split point $t$ and $b = T$, $C(s, T) \ge C(s, t) + C(t, T) + K$. Hence
$$V_T(s) = \mathrm{OPT}(s) + C(s, T) + \beta \ge \mathrm{OPT}(s) + C(s, t) + K + C(t, T) + \beta > \mathrm{OPT}(t) + C(t, T) + \beta = V_T(t). \quad\square$$

**Lemma 3 (the invariant).** For every $t$, when line L3 runs: (a) $F(s) = \mathrm{OPT}(s)$ for every $s < t$; (b) $R \subseteq \{0, \ldots, t - 1\}$ and $t - 1 \in R$; (c) every $s \in \{0, \ldots, t - 1\} \setminus R$ has $V_t(s) > V_t(s')$ for some $s' \in \{0, \ldots, t-1\}$.

*Proof.* By induction on $t$. For $t = 1$, line L1 gives $F(0) = -\beta = \mathrm{OPT}(0)$ and $R = \{0\}$, and (c) is empty.

Assume the invariant at $t$. We first show that line L3 sets $F(t) = \mathrm{OPT}(t)$. By (a), the values computed at line L3 are $V_t(s)$ for $s \in R$, so $F(t) \ge \mathrm{OPT}(t)$ by Lemma 1. Let $s^*$ be a minimizer of $V_t$ over $\{0, \ldots, t-1\}$. By (c), $s^*$ is not outside $R$, since a point outside $R$ is strictly beaten by some point and so is not a minimizer. So $s^* \in R$ and $F(t) = V_t(s^*) = \mathrm{OPT}(t)$. This gives (a) at $t + 1$.

Line L5 keeps $t$, so (b) holds at $t + 1$. For (c) at $t + 1$, let $s \le t$ with $s \notin R$ after line L5. Either $s$ was outside $R$ before step $t$, or it was removed at line L5 of step $t$. In the second case $\mathrm{OPT}(s) + C(s, t) + K > F(t) = \mathrm{OPT}(t)$, so Lemma 2 gives $V_{t+1}(s) > V_{t+1}(t)$. In the first case, $s$ was removed at line L5 of some step $u < t$, and the same argument at that step gives $\mathrm{OPT}(s) + C(s, u) + K > \mathrm{OPT}(u)$, so Lemma 2 with $T = t + 1 > u$ gives $V_{t+1}(s) > V_{t+1}(u)$. In both cases $s$ is strictly beaten. $\square$

**Theorem.** If (P) holds, PELT returns $F(n) = \mathrm{OPT}(n)$ and an optimal segmentation. Moreover, at every $t$ the minimizers of $V_t$ over $R$ are exactly the minimizers of $V_t$ over $\{0, \ldots, t-1\}$, so last$(t)$ is the smallest minimizer of the full recursion and PELT returns the same change points as optimal partitioning without pruning.

*Proof.* By Lemma 3, $F(t) = \mathrm{OPT}(t)$ for every $t$. Every minimizer over the full set lies in $R$, as shown in the proof of Lemma 3, and the minimum values over $R$ and over the full set agree, so the two sets of minimizers are equal. Then last$(t)$ attains the minimum in Lemma 1. Back-tracking at line L6 builds, from the end, a segmentation whose last segment is $x_{\text{last}(t)+1..t}$ in front of an optimal segmentation of $x_1, \ldots, x_{\text{last}(t)}$. By Lemma 1 and induction on $t$, the result is optimal. The loop at line L6 stops because last$(t) < t$. $\blacksquare$

**The condition for the usual costs.** If $C(s, t) = \min_\theta \sum_{i=s+1}^{t}\ell(x_i, \theta)$ for some loss $\ell$, for example the residual sum of squares or minus a maximized log likelihood, then (P) holds with $K = 0$: using one parameter for both parts gives
$$C(a, b) = \min_\theta\Bigl[\sum_{i=a+1}^{s}\ell(x_i, \theta) + \sum_{i=s+1}^{b}\ell(x_i, \theta)\Bigr] \ge C(a, s) + C(s, b).$$
If (P) holds for some $K$, it holds for every smaller $K$, and then line L5 removes fewer points, so the result stays exact.

**Cost.** Step $t$ evaluates $\lvert R \rvert \le t$ segment costs, so the total is at most $n(n+1)/2$. The expected linear cost under conditions on the data is a theorem of Killick, Fearnhead and Eckley (2012) and is not proved here.
