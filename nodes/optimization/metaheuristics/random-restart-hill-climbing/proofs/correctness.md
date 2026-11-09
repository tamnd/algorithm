---
title: Random restarts return a local minimum, and fail with probability at most (1 - p)^R
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The set of solutions $S$ is finite, $f : S \to \mathbb{R}$ is the objective to minimize, $N$ is the neighborhood, and $f^* = \min_S f$. HILL-CLIMBING is the deterministic algorithm of the [hill climbing](/hill-climbing/) page, with a fixed rule and a fixed order of the neighbors, so its output $H(x_0)$ is a function of the start $x_0$. The starts $x^{(1)}, \ldots, x^{(R)}$ of line L3 are independent random variables with the same distribution $D$ on $S$.

**Theorem 1 (what is returned).** The algorithm stops after at most $R$ runs. It returns $b$ with $f(b) = \min_r f(H(x^{(r)}))$ over the runs made, and $b$ is a local minimum of $N$.

*Proof.* Each run of HILL-CLIMBING stops and returns a local minimum, by the theorem of the hill climbing page. The loop of line L2 makes at most $R$ passes. We claim the invariant: after $r$ runs, $b$ is the end of one of these runs and $f(b)$ is the least value among their ends. Before the first run nothing is claimed, and line L5 sets $b$ to the first end. In a later run with end $x$, line L5 replaces $b$ by $x$ exactly when $f(x) < f(b)$, so the new $f(b)$ is $\min(f(b), f(x))$, which is the least value among the first $r + 1$ ends. A stop at line L6 or after $R$ runs returns this $b$. As the end of a run, $b$ is a local minimum. $\square$

**Theorem 2 (probability of success).** Fix a threshold $\tau \ge f^*$ and let $G = \{x \in S : f(x) \le \tau\}$ be the set of good solutions. With $\tau = f^*$, $G$ is the set of global minima. Suppose that $p = \Pr_{x_0 \sim D}[H(x_0) \in G] > 0$. Then without a target, after $R$ runs

$$\Pr[b \notin G] = (1 - p)^R \le e^{-pR}.$$

So $R \ge \ln(1/\delta) / p$ runs give $\Pr[b \notin G] \le \delta$. With the target of line L6 set to $\tau$ and no limit on $R$, the number of runs until the first good end has the geometric distribution with mean $1/p$.

*Proof.* By Theorem 1, $f(b) \le f(H(x^{(r)}))$ for each run $r$. If some run ends in $G$, then $f(b) \le \tau$, so $b \in G$. If no run ends in $G$, then $b$, which is one of the ends, is not in $G$. So $b \notin G$ exactly when every run ends outside $G$. The events $\{H(x^{(r)}) \notin G\}$ are independent, because the starts are independent and $H$ is a fixed function, and each has probability $1 - p$. So $\Pr[b \notin G] = (1-p)^R$.

For the bound, $1 - p \le e^{-p}$ for each real $p$, since $e^{-p}$ is convex and $1 - p$ is its tangent at $p = 0$. So $(1-p)^R \le e^{-pR}$. If $R \ge \ln(1/\delta)/p$, then $e^{-pR} \le e^{-\ln(1/\delta)} = \delta$.

The number of runs $T$ until the first good end satisfies $\Pr[T > t] = (1 - p)^t$ by the same argument, which is the geometric distribution with success probability $p$. Its mean is $\sum_{t \ge 0} \Pr[T > t] = \sum_{t \ge 0} (1-p)^t = 1/p$. $\square$

**Corollary (a lower bound for $p$).** Let $G$ be the set of global minima, and let $D$ be the uniform distribution on $S$. Then $p \ge |G| / |S| \ge 1 / |S|$. So $\Pr[b \notin G] \to 0$ as $R \to \infty$, and random-restart hill climbing finds a global minimum with probability tending to 1.

*Proof.* A start $x_0 \in G$ has $f(y) \ge f^* = f(x_0)$ for each neighbor $y$, so hill climbing returns $x_0$ at once, and $H(x_0) \in G$. So $p \ge \Pr[x_0 \in G] = |G|/|S|$. Theorem 2 then gives $\Pr[b \notin G] \le (1 - 1/|S|)^R \to 0$. $\blacksquare$

**What this does not say.** The corollary is a limit statement. With $p = 1/|S|$, the bound needs about $|S| \ln(1/\delta)$ runs, which for $n$-bit strings is exponential in $n$: no better than enumeration. The useful bound is Theorem 2 with the true $p$ of the instance, and $p$ is not known in advance for a real instance.
