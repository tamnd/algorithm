---
title: HUBER returns the midpoint of the set of minimizers of the Huber objective
proves: [correctness]
status: full
---

**Setting.** $x_1, \ldots, x_n$ are real, $n \ge 1$, $k > 0$ and $\sigma > 0$ (the case $\sigma = 0$ ends at line L1). Put $c = k\sigma$, $Q(\theta) = \sum_i \rho_k((x_i - \theta)/\sigma)$ and $\Lambda(\theta) = \sum_i \psi_k((x_i - \theta)/\sigma)$. Let $b[0] < \cdots < b[M]$ be the distinct values of $x_i \pm c$.

**Lemma 1.** $\Lambda$ is continuous and nonincreasing on $\mathbb R$, and linear on each segment $[b[j], b[j+1]]$.

*Proof.* $\psi_k$ is continuous and nondecreasing, and $\theta \mapsto (x_i - \theta)/\sigma$ is continuous and decreasing. So each term is continuous and nonincreasing, and so is the sum. Take $\theta$ in the open segment $(b[j], b[j+1])$. No value $x_i \pm c$ lies in it, so for each $i$ the sign of $x_i - \theta - c$ and of $x_i - \theta + c$ is the same for all $\theta$ in the segment. So each $i$ is in one of three fixed classes: $x_i - \theta > c$ (the term is $k$), $x_i - \theta < -c$ (the term is $-k$), or $|x_i - \theta| \le c$ (the term is $(x_i - \theta)/\sigma$). Each term is an affine function of $\theta$ on the open segment, so $\Lambda$ is affine there. By continuity it is affine on the closed segment. $\square$

**Lemma 2.** The minimizers of $Q$ are exactly the roots of $\Lambda$, and they form a nonempty closed interval inside $[b[0], b[M]]$.

*Proof.* $\rho_k$ is convex and differentiable with $\rho_k' = \psi_k$: on $|u| < k$ the derivative is $u$, on $|u| > k$ it is $\pm k$, and at $u = \pm k$ both one-sided derivatives are $\pm k$. So $Q$ is convex and differentiable with $Q'(\theta) = -\Lambda(\theta)/\sigma$. A differentiable convex function is minimal at $\theta$ if and only if its derivative is 0 there. At $\theta = b[0] = \min x_i - c$ every $x_i - \theta \ge c$, so $\Lambda(b[0]) = nk > 0$. In the same way $\Lambda(b[M]) = -nk < 0$. By continuity there is a root in $(b[0], b[M])$. A nonincreasing function is positive left of its least root and negative right of its greatest root, and the root set of a continuous monotone function is a closed interval. $\square$

**Lemma 3 (line L4 and line L5).** Line L4 ends with $\Lambda(b[t-1]) > 0 \ge \Lambda(b[t])$, and line L5 gives the least root $\theta_{lo}$ of $\Lambda$.

*Proof.* The search keeps the invariant $\Lambda(b[lo - 1]) > 0$ and $\Lambda(b[hi]) \le 0$. It holds at the start with $lo = 1$ and $hi = M$ by Lemma 2. A step with $\Lambda(b[mid]) \le 0$ sets $hi = mid$, and a step with $\Lambda(b[mid]) > 0$ sets $lo = mid + 1$, so the invariant holds. The range $[lo, hi]$ shrinks at each step and the loop ends with $lo = hi = t$. Since $\Lambda$ is nonincreasing and $\Lambda(b[t-1]) > 0$, no root is $\le b[t-1]$. By Lemma 1, $\Lambda$ is affine on $[b[t-1], b[t]]$, it goes from a positive value to a value $\le 0$, so it has exactly one root in this segment, at the point that line L5 computes. This is the least root. $\square$

**Lemma 4 (line L6 and line L7).** Line L6 ends with $\Lambda(b[u]) \ge 0 > \Lambda(b[u+1])$, and line L7 gives the greatest root $\theta_{hi}$.

*Proof.* The same argument with the invariant $\Lambda(b[lo]) \ge 0$ and $\Lambda(b[hi + 1]) < 0$, which holds at the start with $lo = 0$ and $hi = M - 1$. No root is $\ge b[u+1]$, and on $[b[u], b[u+1]]$ the affine function $\Lambda$ goes from a value $\ge 0$ to a negative value, so its unique root there is the greatest root. $\square$

**Theorem.** HUBER returns the midpoint of the set of minimizers of $Q$.

*Proof.* By Lemma 2 this set is $[\theta_{lo}, \theta_{hi}]$, and by Lemmas 3 and 4 lines L5 and L7 compute its two ends. Line L8 returns $(\theta_{lo} + \theta_{hi})/2$. $\square$

**When the root is unique.** If some $x_i$ satisfies $|x_i - \hat\theta| < c$ at a root $\hat\theta$, then $\Lambda$ has slope at most $-1/\sigma$ near $\hat\theta$ and the root is unique. If the root set is a segment of positive length, then $\Lambda = 0$ on it, so no point is in the linear class on its interior.
