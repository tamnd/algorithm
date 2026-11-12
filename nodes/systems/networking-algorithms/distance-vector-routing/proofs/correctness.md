---
title: Synchronous distance-vector routing reaches the capped distances within ceil(I/c) + n - 1 rounds
proves: [correctness, termination, time.worst]
status: full
---

**Statement.** Let $G = (V, E)$ be a connected or disconnected undirected graph with $n$ routers and link costs $w(x, y) \ge c > 0$, fixed from round 0 on. Fix a destination $t$ and an integer $I > 0$. Let $\delta(x)$ be the distance from $x$ to $t$, $\infty$ if there is no path. The values $D_0(x) \in [0, I]$ for $x \ne t$ are arbitrary, and $D_r(t) = 0$ for all $r$. In round $r \ge 1$, each router $y$ sends to each neighbour $x$ the value $S_{r-1}(y \to x)$, which is $D_{r-1}(y)$, except that a router $y \ne t$ whose next hop $h_{r-1}(y)$ is $x$ sends nothing (simple split horizon) or $I$ (poison reverse) when that mode is on. Then for $x \ne t$

$$D_r(x) = \min\Bigl(I, \min_{y} \bigl(w(x, y) + S_{r-1}(y \to x)\bigr)\Bigr),$$

over the neighbours $y$ that sent a value, and $h_r(x)$ is a neighbour that attains the inner minimum when it is less than $I$, and nil otherwise. (In round 0 the next hops are arbitrary.) Claim: for every $r \ge R = \lceil I/c \rceil + n - 1$ and every $x$, $D_r(x) = \min(I, \delta(x))$; and if $\delta(x) < I$, then following $h_r$ from $x$ gives a path to $t$ of cost $\delta(x)$.

The table of each router is this computation run for every destination at once, so the claim covers all tables.

**Step 1 (lower bound).** For all $r \ge 0$ and $x \ne t$: $D_r(x) \ge \min(I, \delta(x), rc)$.

By induction on $r$. For $r = 0$ the right side is $\min(I, \delta(x), 0) = 0 \le D_0(x)$. Let $r \ge 1$. $D_r(x)$ is $I$ or $w(x, y) + S_{r-1}(y \to x)$ for some neighbour $y$. If it is $I$, the bound holds. If $S_{r-1}(y \to x) = I$ (a poisoned entry), the term is at least $I$. If $y = t$, the term is at least $w(x, t) \ge \delta(x)$. Otherwise $S_{r-1}(y \to x) = D_{r-1}(y) \ge \min(I, \delta(y), (r-1)c)$ by the induction hypothesis, so the term is at least $\min(w + I, w + \delta(y), w + (r - 1)c) \ge \min(I, \delta(x), rc)$, because $w(x, y) + \delta(y) \ge \delta(x)$ by the triangle inequality and $w(x, y) \ge c$. So the minimum is at least $\min(I, \delta(x), rc)$.

**Step 2 (consequence).** Let $R_0 = \lceil I/c \rceil$. For $r \ge R_0$, $rc \ge I$, so Step 1 gives $D_r(x) \ge \min(I, \delta(x))$. Also $D_r(x) \le I$ by the cap. So if $\delta(x) \ge I$, then $D_r(x) = I$ for all $r \ge R_0$. This is the count to infinity: a router that is cut off from $t$ reaches $I$ after at most $\lceil I/c \rceil$ rounds and not much sooner in the worst case.

**Step 3 (upper bound).** Fix a shortest path tree $T$ toward $t$ on the routers with $\delta(x) < \infty$, and let $k(x)$ be the number of links from $x$ to $t$ in $T$; $k(x) \le n - 1$. We show by induction on $k$: for all $r \ge R_0 + k$ and every $x$ with $k(x) = k$, $D_r(x) = \min(I, \delta(x))$.

For $k = 0$, $x = t$ and $D_r(t) = 0$.

Let $k(x) = k \ge 1$, let $y$ be the parent of $x$ in $T$, so $\delta(x) = w(x, y) + \delta(y)$ and $k(y) = k - 1$, and let $r \ge R_0 + k$. By Step 2, $D_r(x) \ge \min(I, \delta(x))$, so we need $D_r(x) \le \min(I, \delta(x))$. If $\delta(x) \ge I$, this holds by the cap. So let $\delta(x) < I$; then $\delta(y) < \delta(x) < I$. By the induction hypothesis with $r - 1 \ge R_0 + k - 1$, $D_{r-1}(y) = \delta(y)$.

We show that $y$ does not hold back or poison its value toward $x$, that is, $y = t$ or $h_{r-1}(y) \ne x$. If $y = t$, then $t$ sends 0 to all neighbours. Otherwise $k \ge 2$, and suppose $h_{r-1}(y) = x$. Then $\delta(y) = D_{r-1}(y) = w(y, x) + S_{r-2}(x \to y)$, and $S_{r-2}(x \to y)$ is $D_{r-2}(x)$ or $I$. Since $r - 2 \ge R_0 + k - 2 \ge R_0$, Step 2 gives $D_{r-2}(x) \ge \min(I, \delta(x)) = \delta(x)$. In both cases $\delta(y) \ge w(y, x) + \delta(x) > \delta(x) > \delta(y)$, which is a contradiction.

So $S_{r-1}(y \to x) = \delta(y)$, and $D_r(x) \le \min(I, w(x, y) + \delta(y)) = \min(I, \delta(x))$.

**Step 4 (all routers).** Every router with $\delta(x) < \infty$ has $k(x) \le n - 1$, so by Step 3 its value is $\min(I, \delta(x))$ for all $r \ge R_0 + n - 1 = R$. Every router with $\delta(x) = \infty$ has $D_r(x) = I$ for $r \ge R_0$ by Step 2. So $D_r(x) = \min(I, \delta(x))$ for every $x$ and every $r \ge R$.

**Step 5 (next hops).** Let $r \ge R + 1$ and $\delta(x) < I$, $x \ne t$. Then $D_r(x) = \delta(x) = w(x, h) + S_{r-1}(h \to x)$ with $h = h_r(x)$, and $S_{r-1}(h \to x) \ge D_{r-1}(h) \ge \min(I, \delta(h))$ (or it is $I$, which is impossible since $\delta(x) < I$). So $\delta(x) \ge w(x, h) + \delta(h)$, and with the triangle inequality, $\delta(x) = w(x, h) + \delta(h)$, with $\delta(h) < \delta(x)$. So each next hop lies on a shortest path, the distance falls by at least $c$ at each hop, and the walk from $x$ reaches $t$ after finitely many hops with total cost $\delta(x)$. In particular no forwarding loop exists from round $R + 1$ on.

**End.** After the last change, every router holds $\min(I, \delta(x))$ from round $\lceil I/c \rceil + n - 1$ on, and its next hops follow shortest paths one round later, in each of the three modes. With integer costs, $c \ge 1$, the bound is $O(n + I)$ rounds. $\blacksquare$
