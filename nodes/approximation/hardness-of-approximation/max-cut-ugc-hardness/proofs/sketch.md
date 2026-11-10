---
title: UG-hardness of max cut, the noise test in full and the composition as a sketch
proves: [statement]
status: sketch
---

This file proves the analysis of the noise test in full, from the Majority Is Stablest theorem, which is cited. It then sketches the composition of the test with a unique game. O'Donnell, Theorem 7.40, proves the composition in general, and Khot, Kindler, Mossel and O'Donnell prove it for max cut. The constants of the sketch are not tracked.

## Notation

Functions are on $\{-1,1\}^n$. For $\rho \in [-1, 1]$, a pair $(x, x')$ is *$\rho$-correlated* if $x$ is uniform and each $x'_i$ equals $x_i$ with probability $\tfrac12 + \tfrac12\rho$ and $-x_i$ otherwise, independently. Then $\mathbb{E}[x_i x'_i] = \rho$, and for $f$ with Fourier expansion $f = \sum_S \hat f(S) \chi_S$,

$$\operatorname{Stab}_\rho[f] = \mathbb{E}[f(x) f(x')] = \sum_{S} \rho^{|S|} \hat f(S)^2 = \sum_{k=0}^n \rho^k W^k[f], \qquad W^k[f] = \sum_{|S| = k} \hat f(S)^2 .$$

The degree-$d$ influence of coordinate $i$ is $\operatorname{Inf}_i^{\le d}[f] = \sum_{S \ni i, |S| \le d} \hat f(S)^2$.

## The cited input

**Majority Is Stablest (Mossel, O'Donnell and Oleszkiewicz 2010; O'Donnell, Section 11.7).** For every $\rho \in (0, 1)$ and $\gamma > 0$ there are $\tau > 0$ and $d$ such that every $g : \{-1,1\}^n \to [-1, 1]$ with $\mathbb{E}[g] = 0$ and $\operatorname{Inf}_i^{\le d}[g] \le \tau$ for all $i$ satisfies

$$\operatorname{Stab}_\rho[g] \le 1 - \tfrac{2}{\pi} \arccos \rho + \gamma .$$

## The noise test, in full

Fix $\theta \in (\tfrac{\pi}{2}, \pi)$ and let $\rho = \cos\theta \in (-1, 0)$. The test reads $f : \{-1,1\}^n \to [-1, 1]$ at a $\rho$-correlated pair and accepts with probability $\tfrac12 - \tfrac12 f(x) f(x')$. For $\pm 1$ valued $f$ this is the event $f(x) \ne f(x')$. So

$$\Pr[\text{accept}] = \tfrac12 - \tfrac12 \operatorname{Stab}_\rho[f] .$$

**Completeness.** If $f(x) = x_i$, then $\operatorname{Stab}_\rho[f] = \rho$, so the test accepts with probability $\tfrac12 - \tfrac12\cos\theta$.

**Soundness.** Let $\gamma > 0$, and take $\tau, d$ from the cited theorem for $-\rho \in (0,1)$ and $\gamma$. Suppose $\operatorname{Inf}_i^{\le d}[f] \le \tau$ for all $i$. Split the sum by the parity of $k$. For even $k$, $\rho^k W^k[f] \ge 0$. For odd $k$, $\rho^k = -(-\rho)^k$. So

$$\operatorname{Stab}_\rho[f] \ge - \sum_{k \text{ odd}} (-\rho)^k W^k[f] = - \operatorname{Stab}_{-\rho}[f^{\mathrm{odd}}], \qquad f^{\mathrm{odd}} = \sum_{|S| \text{ odd}} \hat f(S) \chi_S .$$

The function $f^{\mathrm{odd}}(x) = \tfrac12 (f(x) - f(-x))$ takes values in $[-1, 1]$, has mean $\hat f^{\mathrm{odd}}(\emptyset) = 0$, and has $\operatorname{Inf}_i^{\le d}[f^{\mathrm{odd}}] \le \operatorname{Inf}_i^{\le d}[f] \le \tau$, because it keeps a subset of the Fourier terms. The cited theorem and $\arccos(-\rho) = \arccos(\cos(\pi - \theta)) = \pi - \theta$ give

$$\operatorname{Stab}_{-\rho}[f^{\mathrm{odd}}] \le 1 - \tfrac{2}{\pi}(\pi - \theta) + \gamma = \tfrac{2\theta}{\pi} - 1 + \gamma .$$

So

$$\Pr[\text{accept}] \le \tfrac12 + \tfrac12 \operatorname{Stab}_{-\rho}[f^{\mathrm{odd}}] \le \tfrac{\theta}{\pi} + \tfrac{\gamma}{2} .$$

The contrapositive is the form used below: if the test accepts $f$ with probability more than $\tfrac{\theta}{\pi} + \tfrac{\gamma}{2}$, then some coordinate $i$ has $\operatorname{Inf}_i^{\le d}[f] > \tau$. This needs no folding, because the odd part removes the mean. $\square$

## The composition, a sketch

Start from a unique game $\mathcal{U}$ that is bipartite with sides $U$ and $V$, label set $[n]$, and a bijection $\pi_{uv}$ on each edge, where a labeling satisfies $(u, v)$ if $\ell(u) = \pi_{uv}(\ell(v))$. We assume that every $u \in U$ has the same degree, which the UGC allows. For $x \in \{-1,1\}^n$ write $(x \circ \pi)_j = x_{\pi(j)}$. Then for every $h$ the function $y \mapsto h(y \circ \pi)$ has $\operatorname{Inf}_{\pi(k)}^{\le d}[h(\cdot \circ \pi)] = \operatorname{Inf}_k^{\le d}[h]$, because coordinate $k$ of $h$ reads coordinate $\pi(k)$ of $y$.

**The graph.** The vertices are the points of $V \times \{-1,1\}^n$, so a cut is a family of functions $f_v : \{-1,1\}^n \to \{-1,1\}$, one per $v \in V$. The edge weights are the probabilities of the following test. Pick a uniform $u \in U$ and two uniform neighbors $v, w$ of $u$, independently. Pick a $\rho$-correlated pair $(x, x')$. Accept if $f_v(x \circ \pi_{uv}) \ne f_w(x' \circ \pi_{uw})$. The value of a cut is its acceptance probability. When $\mathcal{U}$ has bounded degree and $n$ is a constant, the graph has polynomial size.

**Completeness.** Let $\ell$ satisfy a $1 - \eta$ fraction of the edges of $\mathcal{U}$, and set $f_v(y) = y_{\ell(v)}$. If both edges $(u, v)$ and $(u, w)$ are satisfied, which happens with probability at least $1 - 2\eta$ by the union bound, then $\pi_{uv}(\ell(v)) = \ell(u) = \pi_{uw}(\ell(w))$. So $f_v(x \circ \pi_{uv}) = x_{\pi_{uv}(\ell(v))} = x_{\ell(u)}$ and $f_w(x' \circ \pi_{uw}) = x'_{\ell(u)}$, and the check accepts with probability $\tfrac12 - \tfrac12\cos\theta$. The value of the cut is at least $(1 - 2\eta)(\tfrac12 - \tfrac12\cos\theta)$.

**Soundness.** Suppose some cut has value more than $\tfrac{\theta}{\pi} + \gamma$. For $u \in U$ let $g_u(y) = \mathbb{E}_v[f_v(y \circ \pi_{uv})]$, the average over the neighbors of $u$, which takes values in $[-1, 1]$. Given $u$, the two neighbors are independent, so

$$\Pr[\text{accept} \mid u] = \tfrac12 - \tfrac12 \operatorname{Stab}_\rho[g_u] .$$

By averaging, at least a $\gamma/2$ fraction of $u$ have $\Pr[\text{accept} \mid u] > \tfrac{\theta}{\pi} + \tfrac{\gamma}{2}$. By the noise test analysis, each such $u$ has a coordinate $i$ with $\operatorname{Inf}_i^{\le d}[g_u] > \tau$. The degree-$d$ influence $\operatorname{Inf}_i^{\le d}[g] = \sum_{S \ni i, |S| \le d} \hat g(S)^2$ is a convex function of $g$, so with $k_v = \pi_{uv}^{-1}(i)$,

$$\tau < \operatorname{Inf}_i^{\le d}[g_u] \le \mathbb{E}_v \operatorname{Inf}_i^{\le d}[f_v(\cdot \circ \pi_{uv})] = \mathbb{E}_v \operatorname{Inf}_{k_v}^{\le d}[f_v] .$$

Each influence is at most $1$, so at least a $\tau/2$ fraction of the neighbors $v$ of $u$ have $\operatorname{Inf}_{k_v}^{\le d}[f_v] \ge \tau/2$. The degree-$d$ influences of a function sum to $\sum_{|S| \le d} |S| \hat f(S)^2 \le d$, so a function has at most $d/\tau$ coordinates of influence more than $\tau$ and at most $2d/\tau$ of influence at least $\tau/2$. Label each $u$ by a uniform coordinate among those with $\operatorname{Inf}^{\le d}[g_u] > \tau$, or arbitrarily if there is none, and each $v$ by a uniform coordinate among those with $\operatorname{Inf}^{\le d}[f_v] \ge \tau/2$, or arbitrarily. For a good $u$ and a good neighbor $v$, the labels are $i$ and $k_v$ with probability at least $\frac{\tau}{d} \cdot \frac{\tau}{2d}$, and then $\pi_{uv}(\ell(v)) = i = \ell(u)$. So the expected fraction of satisfied edges is at least $\frac{\gamma}{2} \cdot \frac{\tau}{2} \cdot \frac{\tau^2}{2d^2}$, and $\operatorname{val}(\mathcal{U}) \ge c(\gamma, \theta) = \frac{\gamma \tau^3}{8 d^2} > 0$.

**Conclusion.** Given $\theta \in (\tfrac{\pi}{2}, \pi)$ and $\delta > 0$, pick $\theta' \in (\theta, \pi)$ with $\theta'/\pi < \theta/\pi + \delta/2$. Since $\tfrac12 - \tfrac12\cos$ is strictly increasing on $(0, \pi)$, there is $\eta > 0$ with $(1 - 2\eta)(\tfrac12 - \tfrac12\cos\theta') \ge \tfrac12 - \tfrac12\cos\theta$. Run the reduction with $\theta'$ and $\gamma = \delta/2$, and use the UGC with completeness $1 - \eta$ and soundness below $c(\gamma, \theta')$. A game of value at least $1 - \eta$ gives a graph of value at least $\tfrac12 - \tfrac12\cos\theta$. A game of value below $c(\gamma, \theta')$ gives a graph of value at most $\theta'/\pi + \gamma < \theta/\pi + \delta$. This is the statement. $\blacksquare$
