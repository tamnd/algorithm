---
title: LR insertion keeps the spline and the weighted partition of unity, keeps weights positive, and terminates with no traversed B-spline
proves: [correctness]
status: full
---

We use the notation of the page. A B-spline $B$ of bidegree $(p, q)$ is given by local knot vectors $x_0 \le \cdots \le x_{p+1}$ and $y_0 \le \cdots \le y_{q+1}$, and $B(x, y) = N[x_0, \ldots, x_{p+1}](x)\, N[y_0, \ldots, y_{q+1}](y)$, where $N[t]$ is the univariate B-spline on the knots $t$. The state is a set $\mathcal{L}$ of triples $(B, \gamma, c)$ with distinct $B$. Write $s = \sum_{\mathcal{L}} \gamma c B$ and $w = \sum_{\mathcal{L}} \gamma B$.

**Lemma 1 (one-knot split).** Let $t_0 \le \cdots \le t_{p+1}$ with $t_0 < t_{p+1}$, and $t_0 < a < t_{p+1}$. Let $\tau$ be the sorted knots $t_0, \ldots, t_{p+1}, a$. Then

$$N[t] = \alpha_1 N[\tau_0, \ldots, \tau_{p+1}] + \alpha_2 N[\tau_1, \ldots, \tau_{p+2}]$$

with $\alpha_1 = \min(1, (a - t_0)/(t_p - t_0))$ (and $\alpha_1 = 1$ if $t_p = t_0$) and $\alpha_2 = \min(1, (t_{p+1} - a)/(t_{p+1} - t_1))$ (and $\alpha_2 = 1$ if $t_{p+1} = t_1$). Both $\alpha_i$ lie in $(0, 1]$.

*Proof.* Embed $t$ in an open knot vector $T$ of degree $p$ that contains $t$ as consecutive knots $T_r, \ldots, T_{r+p+1}$, with $p + 1$ extra copies of a knot below $t_0$ at the start and above $t_{p+1}$ at the end. Then $N[t]$ is the B-spline $N_r$ of $T$, with coefficient vector $e_r$. Insert $a$ by [Boehm's rule](/boehm-knot-insertion/): if $T_k \le a < T_{k+1}$, the new coefficients are $d_i = e_r(i)$ for $i \le k - p$, $d_i = e_r(i-1)$ for $i > k$, and $d_i = \lambda_i e_r(i) + (1 - \lambda_i) e_r(i-1)$ with $\lambda_i = (a - T_i)/(T_{i+p} - T_i)$ for $k - p < i \le k$. Only $d_r$ and $d_{r+1}$ can be nonzero, and the new B-splines of index $r$ and $r + 1$ have the knots $\tau_0, \ldots, \tau_{p+1}$ and $\tau_1, \ldots, \tau_{p+2}$.

For $d_r$: if $r \le k - p$, then $T_{r+p} \le T_k \le a$, so $t_p \le a$, $\alpha_1 = 1$ and $d_r = 1$. Otherwise $r > k - p$ and also $r \le k$, since $t_0 = T_r \le a$ and $a < t_{p+1}$; then $a < T_{r+p} = t_p$ because $k < r + p$, so $d_r = \lambda_r = (a - t_0)/(t_p - t_0) = \alpha_1$, which is less than 1. For $d_{r+1}$: if $r + 1 > k$, then $a < T_{r+1} = t_1$, $d_{r+1} = e_r(r) = 1$, and $(t_{p+1} - a)/(t_{p+1} - t_1) > 1$, so $\alpha_2 = 1$. Otherwise $r + 1 \le k$, so $t_1 \le a$, and $r + 1 > k - p$ because $T_{r+p+1} = t_{p+1} > a \ge T_k$ gives $k < r + p + 1$; then $d_{r+1} = 1 - \lambda_{r+1} = (T_{r+p+1} - a)/(T_{r+p+1} - T_{r+1}) = \alpha_2 \le 1$. The denominators are positive in each case, and $\alpha_1 > 0$ because $a > t_0$ and $\alpha_2 > 0$ because $a < t_{p+1}$. $\square$

**Lemma 2 (invariants of one step).** Lines L5 to L8 do not change $s$ or $w$, and they keep all weights positive.

*Proof.* Say $\mu$ is vertical with value $a$; the horizontal case is the same with the roles swapped. Line L5 removes $(B, \gamma, c)$, and line L6 applies Lemma 1 to the $x$ knots: $B = \alpha_1 B_1 + \alpha_2 B_2$, where $B_i$ has the new $x$ knots and the same $y$ knots. Line L8 adds $\gamma\alpha_i c B_i$ to $s$ and $\gamma\alpha_i B_i$ to $w$. If $B_i$ is new, it is stored with weight $\gamma\alpha_i$ and coefficient $c$. If $B_i$ is stored as $(B_i, \gamma', c')$, it becomes $(B_i, \gamma'', c'')$ with $\gamma'' = \gamma' + \gamma\alpha_i$ and $c'' = (\gamma' c' + \gamma\alpha_i c)/\gamma''$, and $\gamma'' c'' B_i = \gamma' c' B_i + \gamma\alpha_i c B_i$ and $\gamma'' B_i = \gamma' B_i + \gamma\alpha_i B_i$. In both cases the two additions sum to $\gamma c B$ and $\gamma B$, which line L5 removed. Weights are sums of products of positive numbers, by Lemma 1. $\square$

**Lemma 3 (termination).** Let $V_x$ and $V_y$ be the finite sets of values of the vertical and horizontal mesh lines after line L1. For a B-spline $B$ let $\Phi(B)$ be the number of $v \in V_x$ with $x_0 < v < x_{p+1}$ and $v \notin \{x_i\}$, plus the same count in $y$. If $B$ is split in line L6, each child $B_i$ has $\Phi(B_i) \le \Phi(B) - 1$. Hence the loop of lines L3 to L9 ends.

*Proof.* Take a vertical split at $a$. The $y$ knots do not change, so the $y$ count does not change. The support of $B_1$ in $x$ is $[\tau_0, \tau_{p+1}] \subseteq [x_0, x_{p+1}]$, and its knots are all the $\tau_j$ with $j \le p + 1$. Every old knot $x_i$ with $\tau_0 < x_i < \tau_{p+1}$ is among $\tau_1, \ldots, \tau_p$, so it is a knot of $B_1$, and so is $a$ when it lies inside. So a value $v \in V_x$ counted for $B_1$ lies strictly inside the support of $B$ and is not an old knot, so it is counted for $B$; and $a$ is counted for $B$ but not for $B_1$. The same holds for $B_2$. Now let $P = \sum 3^{\Phi(B)}$ over the keys in the set, an integer at least 0. A split removes one key with $\Phi = \varphi \ge 1$ and adds at most two new keys with $\Phi \le \varphi - 1$; a merge adds no key. So $P$ falls by at least $3^\varphi - 2 \cdot 3^{\varphi-1} \ge 1$, and there are finitely many splits. Each iteration either splits or removes one entry from $Q$ without adding any, and the entries added to $Q$ are those of line L2 and two per split. So the number of iterations is finite. $\square$

**Lemma 4 (no traversed B-spline at the end).** When INSERT returns, no stored B-spline is traversed by a mesh line.

*Proof.* Every key in the set at the end was put in $Q$ in line L2 or line L9, after the last time its triple changed. When it was taken from $Q$, line L4 found no traversing line, because it is still in the set and line L5 removes every key that has one. The mesh does not change after line L1, and the traversal test depends only on the key and the mesh, so the answer is the same at the end. $\square$

**Theorem.** Start from the tensor product spline on open knot vectors, with all weights 1. After any sequence of INSERT calls, (1) $s$ is the original spline, (2) $w = 1$ on the domain, (3) all weights are positive, and (4) no B-spline is traversed by a mesh line.

*Proof.* At the start every $\gamma = 1$, so $w$ is the sum of the tensor B-splines, which is 1 on the domain by the [partition of unity](/partition-of-unity/) of B-splines on open knot vectors in each direction. Line L1 changes only the mesh. By Lemma 2 every step of the loop keeps $s$, $w$ and the positivity of the weights, by Lemma 3 the loop ends, and by Lemma 4 the end state has no traversed B-spline. A refused segment restores the state, so it changes nothing. Induction over the calls gives the claims. $\blacksquare$
