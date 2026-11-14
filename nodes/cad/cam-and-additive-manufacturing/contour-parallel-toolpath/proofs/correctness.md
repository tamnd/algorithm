---
title: With a step-over of at most the tool radius, the contour-parallel loops cut exactly the opening of the pocket
proves: [correctness, termination]
status: full
---

**Setting.** $P \subset \mathbb{R}^2$ is compact, $r > 0$ and $0 < s \le r$. For $x \in \mathbb{R}^2$ let $\delta(x) = \operatorname{dist}(x, \mathbb{R}^2 \setminus P)$, so $\delta(x) = 0$ for $x \notin P$. For $d > 0$ let $P_d = \{x : \delta(x) \ge d\}$. Let $d_k = r + ks$. Assume $P_r \ne \emptyset$, let $K$ be the largest $k$ with $P_{d_k} \ne \emptyset$, and let $\Gamma = \bigcup_{k=0}^{K} \partial P_{d_k}$ be the set of points visited by the loops. $D_r$ is the closed disk of radius $r$ at the origin, and $O_r(P) = P_r \oplus D_r$.

**Claim.** (a) $K$ exists, so CONTOUR-PARALLEL stops after $K + 1$ loops of lines L2 to L6. (b) For every $c \in \Gamma$, $c + D_r \subseteq P$. (c) $\Gamma \oplus D_r = O_r(P)$. (d) If $c + D_r \subseteq P$, then $c \in P_r$. So every path whose tool stays in $P$ cuts a subset of $O_r(P)$, and the loops cut all of it.

**Step 1 (facts on $\delta$).** $\delta$ is the distance to a set, so $|\delta(x) - \delta(y)| \le |x - y|$ for all $x, y$, and $\delta$ is continuous. Each $P_d$ with $d > 0$ is closed, as the preimage of $[d, \infty)$, and lies in $P$. If $x \in P_d$ is a limit of points not in $P_d$, then $\delta(x) \le d$ by continuity, so $\delta(x) = d$. Conversely, let $\delta(x) = d > 0$. The set $\mathbb{R}^2 \setminus P$ is open and nonempty ($P$ is bounded), so its closure $Z$ has a point $b$ with $|x - b| = d$. For $0 \le t \le d$ let $x_t = x + t(b - x)/d$. Then $\delta(x_t) \le |x_t - b| = d - t$, because $\operatorname{dist}(\cdot, \mathbb{R}^2 \setminus P) = \operatorname{dist}(\cdot, Z)$. So the points $x_t$ with $t > 0$ are not in $P_d$, and $x$ is a limit of them. Hence $\partial P_d = \{x : \delta(x) = d\}$.

**Step 2 (the distance to an offset curve).** Let $\delta(p) \ge d > 0$. Then some point $q \in \partial P_d$ has $|p - q| = \delta(p) - d$. *Proof.* Write $D = \delta(p)$ and take $b \in Z$ with $|p - b| = D$ as in Step 1. For $p_t = p + t(b - p)/D$, the bound $\delta(p_t) \le D - t$ holds as in Step 1, and the Lipschitz bound gives $\delta(p_t) \ge D - t$. So $\delta(p_t) = D - t$. Take $t = D - d$ and $q = p_t$. Then $\delta(q) = d$, so $q \in \partial P_d$ by Step 1, and $|p - q| = D - d$. $\square$

**Step 3 (termination).** $\delta$ is continuous on the compact set $P$ and is $0$ outside $P$, so it has a maximum $\delta_{\max}$. Then $P_d = \emptyset$ for $d > \delta_{\max}$. The value $d$ of line L6 grows by exactly $s > 0$ in each loop, so after at most $\lfloor (\delta_{\max} - r)/s \rfloor + 2$ tests of line L4 the offset is empty. The nonempty offsets are those with $d_k \le \delta_{\max}$, and they form an initial run $k = 0, \dots, K$ because $P_{d} \supseteq P_{d'}$ for $d \le d'$. This proves (a).

**Step 4 (the tool stays in the pocket).** Let $c \in \Gamma$. Then $c \in \partial P_{d_k} \subseteq P_{d_k} \subseteq P_r$, so $\delta(c) \ge r$. If a point $y$ with $|y - c| < r$ were outside $P$, then $\delta(c) \le |c - y| < r$. So the open disk of radius $r$ around $c$ lies in $P$, and the closed disk lies in $P$ because $P$ is closed. This proves (b). The same argument with $c \in P_r$ shows $P_r \oplus D_r \subseteq P$.

**Step 5 (maximality).** Let $c + D_r \subseteq P$. Every point outside $P$ is outside the closed disk, at distance more than $r$ from $c$, so $\delta(c) \ge r$ and $c \in P_r$. This proves (d).

**Step 6 (coverage).** $\Gamma \subseteq P_r$ gives $\Gamma \oplus D_r \subseteq O_r(P)$. For the other inclusion, let $p \in O_r(P)$, so $|p - c| \le r$ for some $c \in P_r$. We find a point of $\Gamma$ within $r$ of $p$.

*Case A: $\delta(p) \ge r$.* Let $k$ be the largest index with $d_k \le \delta(p)$. Then $p \in P_{d_k}$, so $k \le K$, and $\delta(p) < d_{k+1}$: for $k < K$ by the choice of $k$, and for $k = K$ because $P_{d_{K+1}} = \emptyset$. By Step 2 some $q \in \partial P_{d_k} \subseteq \Gamma$ has $|p - q| = \delta(p) - d_k < d_{k+1} - d_k = s \le r$.

*Case B: $\delta(p) < r$.* Let $g(t) = \delta(c + t(p - c))$ on $[0, 1]$. It is continuous, $g(0) \ge r$ and $g(1) < r$. Let $t^* = \sup\{t \in [0,1] : g(t) \ge r\}$. Then $g(t^*) \ge r$ by continuity, so $t^* < 1$, and $g(t) < r$ for all $t \in (t^*, 1]$. So $x^* = c + t^*(p - c)$ lies in $P_r$ and is a limit of points not in $P_r$, so $x^* \in \partial P_r = \partial P_{d_0} \subseteq \Gamma$. And $|p - x^*| = (1 - t^*)|p - c| \le r$.

In both cases $p \in \Gamma \oplus D_r$. This proves (c). $\blacksquare$

**The convex offset used by the code.** Let $P = \bigcap_{i=1}^{n} \{x : n_i \cdot x \le c_i\}$ with unit vectors $n_i$. The complement of $P$ is the union of the open half-planes $\{x : n_i \cdot x > c_i\}$. For $p \in P$, the distance from $p$ to the $i$-th open half-plane is $c_i - n_i \cdot p$, and the distance to a union is the minimum of the distances. So $\delta(p) = \min_i (c_i - n_i \cdot p)$ on $P$, and $P_d = \bigcap_i \{x : n_i \cdot x \le c_i - d\}$ for $d > 0$: a point outside $P$ violates some $n_i \cdot x \le c_i$ and so violates the moved inequality too. This is the set that OFFSET computes by clipping, and each clip is exact because the $n_i$ and $c_i$ are rational.
