---
title: The averaged multiplicative weights solver gives a feasible fractional routing within a factor 1 + ε of optimal plus an additive term in 1/T, and a valid lower bound
proves: [correctness]
status: full
---

**Setting.** $G = (V, E)$ has $|E| = M$ edges with capacities $c_e > 0$. There are $k \ge 1$ nets, and net $i$ has a finite nonempty set $\mathcal{R}_i$ of routes, each a set of edges. For a choice of weights $x$, the load of $e$ is $\mathrm{load}_e(x) = \sum_i \sum_{P \in \mathcal{R}_i, P \ni e} x_{iP}$. The fractional optimum is

$$\lambda^* = \min \{ \lambda : \textstyle\sum_{P \in \mathcal{R}_i} x_{iP} = 1 \text{ for all } i,\ x \ge 0,\ \mathrm{load}_e(x) \le \lambda c_e \text{ for all } e \}.$$

The feasible set is a nonempty polyhedron (take any one route per net and $\lambda$ large), $\lambda \ge 0$ on it, and the objective is linear, so the minimum is attained, by the existence of optimal vertices of linear programs. Fix an optimal $x^*$.

The oracle returns, for nonnegative edge lengths $\ell$, a route $P \in \mathcal{R}_i$ with the least length $\ell(P) = \sum_{e \in P} \ell_e$. For the Dijkstra oracle, $\mathcal{R}_i$ is the set of simple paths between the two pins, and a shortest walk under positive lengths is a simple path, so Dijkstra's algorithm is such an oracle.

In round $t$ write $w^t$ for the weights at line L3, $W^t = \sum_e w^t_e$, $\ell^t_e = w^t_e / (W^t c_e)$, $P^t_i$ for the route of net $i$, $\mathrm{load}^t_e = |\{ i : e \in P^t_i \}|$, and $\mathrm{LB}_t = \sum_e \ell^t_e \mathrm{load}^t_e$. Let $u^t_e = \mathrm{load}^t_e / (\rho c_e)$ with $\rho = k / \min_e c_e$.

**Lemma 1 (feasible average).** For each net $i$, the weights $x_{iP} = \mathrm{count}(i, P) / T$ of line L8 are nonnegative, they are positive only on routes of $\mathcal{R}_i$, and they add up to 1. Moreover $\mathrm{load}_e(x) = \frac{1}{T} \sum_{t=1}^{T} \mathrm{load}^t_e$.

*Proof.* Each of the $T$ rounds adds 1 to exactly one counter of net $i$, at a route returned by the oracle, so the counters of net $i$ add up to $T$. For the load, $\mathrm{load}_e(x) = \frac1T \sum_i \sum_{P \ni e} \mathrm{count}(i, P)$, and $\sum_{P \ni e} \mathrm{count}(i, P)$ is the number of rounds in which the route of net $i$ contains $e$. Summing over $i$ and exchanging the sums gives $\frac1T \sum_t \mathrm{load}^t_e$. $\square$

**Lemma 2 (lower bound).** For every round $t$, $\mathrm{LB}_t \le \lambda^*$. Hence $\mathrm{LB} = \max_t \mathrm{LB}_t \le \lambda^* \le \lambda_{\mathrm{frac}}$.

*Proof.* The lengths satisfy $\sum_e \ell^t_e c_e = \sum_e w^t_e / W^t = 1$. Since $\ell^t_e \mathrm{load}^t_e$ sums the length of each edge once for each route on it, $\mathrm{LB}_t = \sum_i \ell^t(P^t_i) = \sum_i \min_{P \in \mathcal{R}_i} \ell^t(P)$. A minimum is at most any weighted average with weights that add up to 1, so

$$\mathrm{LB}_t \le \sum_i \sum_{P \in \mathcal{R}_i} x^*_{iP}\, \ell^t(P) = \sum_e \ell^t_e\, \mathrm{load}_e(x^*) \le \sum_e \ell^t_e\, \lambda^* c_e = \lambda^*.$$

The middle equality exchanges the sums over routes and edges. The last inequality uses $\ell^t_e \ge 0$ and the constraint $\mathrm{load}_e(x^*) \le \lambda^* c_e$. By Lemma 1, $x$ is feasible with $\lambda = \lambda_{\mathrm{frac}}$, so $\lambda^* \le \lambda_{\mathrm{frac}}$. $\square$

This is [weak duality](/weak-duality/) for the dual $\lambda^* = \max_{\ell \ge 0,\ \sum_e \ell_e c_e = 1} \sum_i \min_P \ell(P)$ of the problem; only the direction "at most" is needed here.

**Lemma 3 (width).** $0 \le u^t_e \le 1$ for all $t$ and $e$.

*Proof.* $0 \le \mathrm{load}^t_e \le k$, since each net puts at most one route on $e$, and $\rho c_e \ge \rho \min_e c_e = k$. $\square$

**Lemma 4.** For $\varepsilon > 0$ and $u \in [0, 1]$, $(1 + \varepsilon)^u \le 1 + \varepsilon u$.

*Proof.* The function $f(u) = (1 + \varepsilon)^u$ is convex, with $f(0) = 1$ and $f(1) = 1 + \varepsilon$. A convex function lies below its chord on $[0, 1]$, so $f(u) \le (1 - u) \cdot 1 + u (1 + \varepsilon) = 1 + \varepsilon u$. $\square$

**Theorem (upper bound).** For $0 < \varepsilon \le 1$ and $T \ge 1$,

$$\lambda_{\mathrm{frac}} \ \le\ \frac{\varepsilon}{\ln(1 + \varepsilon)}\, \lambda^* + \frac{\rho \ln M}{T \ln(1 + \varepsilon)} \ \le\ (1 + \varepsilon)\, \lambda^* + \frac{\rho \ln M}{T \ln(1 + \varepsilon)}.$$

*Proof.* Line L7 sets $w^{t+1}_e = w^t_e (1 + \varepsilon u^t_e)$. Sum over $e$ and write $p^t_e = w^t_e / W^t$:

$$W^{t+1} = W^t \Big( 1 + \varepsilon \sum_e p^t_e u^t_e \Big).$$

Here $\sum_e p^t_e u^t_e = \frac{1}{\rho} \sum_e \frac{w^t_e}{W^t c_e} \mathrm{load}^t_e = \mathrm{LB}_t / \rho \le \lambda^* / \rho$ by Lemma 2. With $1 + z \le e^z$ and $W^1 = M$,

$$W^{T+1} \le M \exp\Big( \frac{\varepsilon}{\rho} \sum_{t=1}^{T} \mathrm{LB}_t \Big) \le M \exp\Big( \frac{\varepsilon T \lambda^*}{\rho} \Big).$$

For one edge $e$, let $S_e = \sum_{t=1}^{T} u^t_e$. By Lemmas 3 and 4, $w^{T+1}_e = \prod_t (1 + \varepsilon u^t_e) \ge \prod_t (1 + \varepsilon)^{u^t_e} = (1 + \varepsilon)^{S_e}$. All weights are positive, so $w^{T+1}_e \le W^{T+1}$. Take logarithms:

$$S_e \ln(1 + \varepsilon) \le \ln M + \frac{\varepsilon T \lambda^*}{\rho}.$$

By Lemma 1, $\mathrm{load}_e(x) / c_e = \frac{1}{T} \sum_t \mathrm{load}^t_e / c_e = \rho S_e / T$. Multiply the inequality by $\rho / (T \ln(1 + \varepsilon))$:

$$\frac{\mathrm{load}_e(x)}{c_e} \le \frac{\rho \ln M}{T \ln(1 + \varepsilon)} + \frac{\varepsilon}{\ln(1 + \varepsilon)} \lambda^*.$$

This holds for every edge, so it holds for the maximum, $\lambda_{\mathrm{frac}}$. For the second form, $\ln(1 + \varepsilon) = \int_0^\varepsilon \frac{ds}{1 + s} \ge \frac{\varepsilon}{1 + \varepsilon}$, so $\frac{\varepsilon}{\ln(1 + \varepsilon)} \le 1 + \varepsilon$. $\square$

**Corollary (rounds needed).** If $0 < \varepsilon \le 1$, $\lambda^* > 0$ and $T \ge 2 \rho \ln M / (\varepsilon^2 \lambda^*)$, then $\lambda_{\mathrm{frac}} \le (1 + 2 \varepsilon) \lambda^*$.

*Proof.* From the last step, $\ln(1 + \varepsilon) \ge \varepsilon / (1 + \varepsilon) \ge \varepsilon / 2$ for $\varepsilon \le 1$. So the additive term is at most $2 \rho \ln M / (T \varepsilon) \le \varepsilon \lambda^*$. Add it to $(1 + \varepsilon) \lambda^*$. $\square$

**Lemma 5 (rounding).** Line L9 picks route $P$ for net $i$ with probability $x_{iP}$, independently over the nets. Then the expected load of edge $e$ after rounding is $\mathrm{load}_e(x) \le \lambda_{\mathrm{frac}} c_e$, and the load is a sum of $k$ independent 0-1 variables, one per net.

*Proof.* The indicator that net $i$ uses $e$ has expectation $\sum_{P \ni e} x_{iP}$. Sum over $i$ by linearity of expectation. Independence holds because each net draws its own random number. $\square$

With unit capacities, Lemma 5 is the only input that the analysis on the [randomized rounding](/randomized-rounding/) page needs, with $\lambda_{\mathrm{frac}}$ in place of the LP optimum. It gives congestion $O(\log M / \log \log M) \cdot \max(\lambda_{\mathrm{frac}}, 1)$ with high probability.
