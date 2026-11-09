---
title: Expected bounds and the tail estimate for Seidel's point location
proves: [time.build, time.query, time.query-with-rebuild, space.extra]
status: full
---

**Setting.** $S$ is a fixed set of $n \ge 1$ segments meeting only at shared end points, $s_1, \ldots, s_n$ a uniformly random order, $S_i = \{s_1, \ldots, s_i\}$, and $D_i$ the DAG after $i$ insertions. Costs are on the real RAM. $H_n = \sum_{i=1}^n 1/i$.

**Claim.** (a) For every fixed point $q$, the search path of $q$ in $D_n$ has expected length at most $12 H_n$. The expected size of $D_n$ is $O(n)$ and the expected build time is $O(n \log n)$. (b) For every fixed $q$ and $\lambda > 0$, the path of $q$ has more than $3 \lambda \ln(n+1)$ inner nodes with probability at most $(n+1)^{1 - \lambda \ln 1.25}$. (c) The longest search path over all query points exceeds $3 \lambda \ln(n+1)$ with probability at most $2 (n+1)^{3 - \lambda \ln 1.25}$. (d) If the rebuild test of line L5 uses the longest search path and $L = 3 \lambda \ln(n+1)$ with $\lambda \ln 1.25 \ge 5$, the expected number of rounds is at most $2$, so the build takes $O(n \log n)$ expected time and every query takes $O(\log n)$ time.

**Step 1 (expected bounds).** (a) is proved in [the complexity proof of the trapezoidal map](/trapezoidal-map/proofs/complexity/): the path of a fixed point grows by at most $3$ nodes in step $i$, only if the face of $T(S_i)$ that contains it depends on $s_i$, which happens with probability at most $4/i$ given the set $S_i$; the expected number of trapezoids created in step $i$ is at most $12 + 4/i$; and the search in step $i$ is a query in $D_{i-1}$.

**Step 2 (independence backwards).** Fix a point $q$ that is not an end point and lies on no segment (the general case reduces to this one as in that proof: the path of any point is a prefix of the path of a nearby such point). Let $X_i = 1$ if the face $\Delta_q(i)$ of $T(S_i)$ that contains $q$ depends on $s_i$, and $X_i = 0$ otherwise. The random order can be generated backwards: $s_n$ is uniform in $S$, then $s_{n-1}$ is uniform in $S \setminus \{s_n\}$, and so on, so given $s_n, \ldots, s_{i+1}$, the set $S_i$ is determined and $s_i$ is uniform in it. The face $\Delta_q(i)$ is determined by $S_i$ and depends on at most four of its segments (Step 2 of the trapezoidal map complexity proof), so

$$\Pr[X_i = 1 \mid s_n, \ldots, s_{i+1}] \le \frac{4}{i}.$$

Also, $X_j$ for $j > i$ is a function of $S_j$ and $s_j$, hence of $s_n, \ldots, s_{i+1}$.

**Step 3 (moment generating function).** Let $X = \sum_i X_i$ and $t = \ln 1.25$, so $e^t - 1 = 1/4$. Since $X_i \in \{0, 1\}$, $e^{t X_i} = 1 + (e^t - 1) X_i$, and by Step 2

$$\mathbb{E}[e^{t X_i} \mid s_n, \ldots, s_{i+1}] \le 1 + \frac{1}{4} \cdot \frac{4}{i} = 1 + \frac{1}{i}.$$

We show by induction on $k$ that $\mathbb{E}[e^{t (X_1 + \cdots + X_k)} \mid s_n, \ldots, s_{k+1}] \le \prod_{i=1}^{k} (1 + 1/i)$. For $k = 1$ this is the display. For the step, $X_{k+1}$ is a function of $s_n, \ldots, s_{k+1}$, so by the tower property

$$\mathbb{E}[e^{t(X_1 + \cdots + X_{k+1})} \mid s_n, \ldots, s_{k+2}] = \mathbb{E}\big[e^{t X_{k+1}} \, \mathbb{E}[e^{t(X_1 + \cdots + X_k)} \mid s_n, \ldots, s_{k+1}] \,\big|\, s_n, \ldots, s_{k+2}\big],$$

which is at most $\prod_{i \le k} (1 + 1/i) \cdot (1 + 1/(k+1))$ by the hypothesis and the display. With $k = n$, $\mathbb{E}[e^{tX}] \le \prod_{i=1}^{n} \frac{i+1}{i} = n + 1$.

**Step 4 (tail for a fixed point, b).** The path length of $q$ is at most $3X$, since it grows by at most $3$ exactly in the steps with $X_i = 1$. By Markov's inequality applied to $e^{tX}$,

$$\Pr[3X > 3 \lambda \ln(n+1)] \le \Pr[e^{tX} \ge e^{t \lambda \ln(n+1)}] \le \frac{n+1}{(n+1)^{\lambda \ln 1.25}} = (n+1)^{1 - \lambda \ln 1.25}.$$

**Step 5 (all query points, c).** Let $x_1 < \cdots < x_m$ be the sheared $x$-coordinates of the end points of $S$. They cut the plane into at most $2n + 1$ open slabs. In each slab, the segments of $S$ that cross it are disjoint inside it and cut it into at most $n + 1$ open cells. Two points of one cell get the same answer to every test of every $D_i$: an X-node compares with an end point, whose sheared $x$ is not inside the slab; a Y-node of a segment $t$ is reached only by points strictly inside the $x$-range of $t$, and if $t$ crosses the slab, the whole cell is on one side of it. So all points of a cell have the same search path, and every other point (on a segment or a wall) has a path that is a prefix of the path of a nearby cell point. There are at most $(2n+1)(n+1) \le 2(n+1)^2$ cells. By the union bound and (b),

$$\Pr[\text{longest search path} > 3 \lambda \ln(n+1)] \le 2(n+1)^2 (n+1)^{1 - \lambda \ln 1.25} = 2 (n+1)^{3 - \lambda \ln 1.25}.$$

**Step 6 (rebuilding, d).** If $\lambda \ln 1.25 \ge 5$, the bound of (c) is at most $2 (n+1)^{-2} \le 1/2$ for $n \ge 1$. The rounds are independent, so the number of rounds is geometric with success probability at least $1/2$, and its expectation is at most $2$. The cost of one round is the build plus the computation of the longest search path; by (a) the build costs $O(n \log n)$ expected. Given that the round is the last, or not, the conditional expectation of its cost is at most twice the unconditional one, since each event has probability at least $1/2$; summing over rounds, by Wald's identity the expected total build time is $O(n \log n)$ plus the expected cost of the depth tests. After the loop, every query takes at most $3 \lambda \ln(n+1) = O(\log n)$ steps. The code tests the longest path of the DAG instead, which is at least the longest search path; the guarantee after the loop still holds, but this proof does not bound the number of its rounds. $\blacksquare$
