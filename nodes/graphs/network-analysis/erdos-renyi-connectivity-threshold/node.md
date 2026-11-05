---
tag: SHJSNE
kind: theorem
slug: erdos-renyi-connectivity-threshold
name: Erdős-Rényi connectivity threshold
aliases:
- connectivity threshold
area: graphs/network-analysis
level: advanced
summary: G(n,p) becomes connected sharply at p = ln(n)/n.
prereqs: [erdos-renyi-model, chebyshev-inequality, markov-inequality, cayley-formula, inclusion-exclusion-principle]
see_also: [erdos-renyi-model, erdos-renyi-giant-component-theorem, giant-component, connected-components, poisson-distribution, cayley-formula, probabilistic-method, hamiltonian-cycle]
sources:
  - paper: "Paul Erdős and Alfréd Rényi, On random graphs I, Publicationes Mathematicae Debrecen 6, 290 to 297 (1959)"
    locator: the whole paper (the probability that a random graph with (n log n)/2 + cn edges is connected tends to exp(−e^(−2c)))
  - paper: doi:10.1214/aoms/1177706098
    title: Edgar N. Gilbert, Random graphs, Annals of Mathematical Statistics 30(4), 1141 to 1144 (1959)
    locator: the whole paper (the recurrence for the probability that G(n,p) is connected, and its asymptotics)
  - book: isbn:9781107118508
    title: Alan Frieze and Michał Karoński, Introduction to Random Graphs, Cambridge University Press, 2016
    locator: Chapter 4, Connectivity, Section 4.1 (the threshold for connectivity and the limit exp(−e^(−c)) via isolated vertices and small components)
  - book: isbn:9780521797221
    title: Béla Bollobás, Random Graphs, second edition, Cambridge University Press, 2001
    locator: Chapter 7, Connectivity and matchings (the connectivity threshold and the hitting time of connectivity and of minimum degree 1)
---

The connectivity threshold of the [Erdős-Rényi model](/erdos-renyi-model/) says that the random graph $G(n, p)$ changes from almost surely disconnected to almost surely connected in a narrow window around $p = \ln n / n$. Write $p = (\ln n + c)/n$. If $c \to -\infty$ the graph has isolated vertices, if $c \to +\infty$ it is connected, and for a fixed $c$ the probability of being connected tends to $e^{-e^{-c}}$. The proof shows that isolated vertices are the last obstacle: once there are none, there is a.a.s. no other small component either. Erdős and Rényi proved the result in 1959 for the model with a fixed number of edges.

## Statement

Let $G(n, p)$ be the random simple graph on $n$ labelled vertices in which each of the $\binom{n}{2}$ pairs is an edge with probability $p$, independently. Let $X$ be its number of isolated vertices. An event holds *asymptotically almost surely* (a.a.s.) if its probability tends to 1 as $n \to \infty$. Let $p = (\ln n + c_n)/n$ for a real sequence $c_n$.

**Theorem.**

1. If $c_n \to -\infty$, then a.a.s. $X \ge 1$, so $G(n, p)$ is not connected.
2. If $c_n \to +\infty$, then a.a.s. $G(n, p)$ is connected.
3. If $c_n \to c \in \mathbb{R}$, then for each $k \ge 0$, $\Pr[X = k] \to e^{-\mu} \mu^k / k!$ with $\mu = e^{-c}$, and

$$\Pr[G(n, p) \text{ is connected}] \to e^{-e^{-c}}.$$

So $\ln n/n$ is a sharp threshold for connectivity, with a window of width $O(1/n)$ around it.

The graph is undirected and unweighted. The statement is about the whole graph. Near the threshold, the proof shows that a.a.s. the graph is one [giant component](/giant-component/) plus some isolated vertices, so it is disconnected only because of isolated vertices.

## In plain words

Build a random network on many points by joining each pair with the same small chance. Raise that chance slowly. For a long time, a few points have no link at all, so the network falls apart.

The theorem says that the last lonely points get their first link at a very precise moment, when each point has about as many links as the natural logarithm of the number of points. Just before, some point is surely alone. Just after, the network is surely in one piece.

The surprising part is that being in one piece needs nothing more than having no lonely point. Larger separate groups disappear much earlier.

## Proof

Write $\lambda = np = \ln n + c_n$. All limits are as $n \to \infty$.

**Step 0 (reductions).** Couple the models for two values $p' \le p$ by giving each pair an independent uniform $U_e \in [0, 1]$ and keeping it in $G(n, p)$ when $U_e \le p$; then $G(n, p') \subseteq G(n, p)$. Connectivity is preserved by adding edges, and so is the absence of isolated vertices. So for part 2 we may replace $c_n$ by $\min(c_n, \ln \ln n)$, which still tends to $\infty$, and for part 1 by $\max(c_n, -\ln \ln n)$, which still tends to $-\infty$. From now on $|c_n| \le \ln \ln n$, so $\ln n - \ln \ln n \le \lambda \le 2 \ln n$ for large $n$, $p \to 0$ and $np^2 \to 0$.

**Step 1 (the expected number of isolated vertices).** A vertex is isolated when none of its $n - 1$ pairs is an edge, so $\mathbb{E}[X] = n(1 - p)^{n-1}$. For $0 \le p \le 1/2$, $-p - p^2 \le \ln(1 - p) \le -p$. Hence

$$\ln \mathbb{E}[X] = \ln n + (n - 1)\ln(1 - p) = \ln n - \lambda + O(p + np^2) = -c_n + o(1),$$

so $\mathbb{E}[X] = e^{-c_n + o(1)}$.

**Step 2 (factorial moments).** For $k \ge 1$, let $(X)_k = X(X-1)\cdots(X-k+1)$, the number of ordered $k$-tuples of distinct isolated vertices. A fixed set of $k$ vertices is isolated when none of the $\binom{k}{2} + k(n - k)$ pairs that touch it is an edge, so

$$\mathbb{E}[(X)_k] = (n)_k\, (1 - p)^{k(n-1) - \binom{k}{2}}.$$

For fixed $k$, $(n)_k/n^k \to 1$ and $(1 - p)^{-\binom{k}{2}} \to 1$, so $\mathbb{E}[(X)_k] = (1 + o(1))\, \mathbb{E}[X]^k$.

**Part 1.** By Step 1, $\mathbb{E}[X] \to \infty$. By Step 2 with $k = 2$, $\mathbb{E}[X(X-1)] = (1 + o(1))\mathbb{E}[X]^2$, so

$$\mathrm{Var}[X] = \mathbb{E}[X(X-1)] + \mathbb{E}[X] - \mathbb{E}[X]^2 = o(\mathbb{E}[X]^2) + \mathbb{E}[X].$$

By the [Chebyshev inequality](/chebyshev-inequality/), $\Pr[X = 0] \le \Pr\bigl[|X - \mathbb{E}X| \ge \mathbb{E}X\bigr] \le \mathrm{Var}[X]/\mathbb{E}[X]^2 = o(1) + 1/\mathbb{E}[X] \to 0$.

**Step 3 (no component of middle size).** Assume $c_n \ge -a$ for a constant $a$ (and $|c_n| \le \ln \ln n$ as above). Let $Y$ be the number of sets $S$ with $2 \le |S| \le n/2$ that are the vertex set of a component. We show $\mathbb{E}[Y] \to 0$.

If $S$ with $|S| = k$ is a component, then $G[S]$ is connected, so it contains a [spanning tree](/spanning-tree/) of $S$, and no pair between $S$ and $V \setminus S$ is an edge. By [Cayley's formula](/cayley-formula/) there are $k^{k-2}$ trees on $S$. The $k - 1$ pairs of a tree and the $k(n - k)$ pairs leaving $S$ are distinct, so by independence and the union bound over the trees,

$$\Pr[S \text{ is a component}] \le k^{k-2} p^{k-1} (1 - p)^{k(n-k)}.$$

With $\binom{n}{k} \le (en/k)^k$ and $1 - p \le e^{-p}$, the expected number $T_k$ of components with $k$ vertices satisfies

$$T_k \le \Bigl(\frac{en}{k}\Bigr)^k k^{k-2} p^{k-1} e^{-pk(n-k)} = \frac{n}{k^2 \lambda}\, (e\lambda)^k e^{-k\lambda} e^{k^2 \lambda/n}.$$

Note $e^{-\lambda} = e^{-c_n}/n \le e^a/n$ and $k^2 \lambda \ge 1$ for large $n$.

- *Case $2 \le k \le n/\lambda$.* Then $e^{k^2\lambda/n} \le e^k$, so $T_k \le n\,(e^{2+a}\lambda/n)^k$. Since $\lambda \le 2 \ln n$, the ratio $r = e^{2+a}\lambda/n$ is below $1/2$ for large $n$, and $\sum_{k \ge 2} T_k \le n \cdot 2r^2 = O(\ln^2 n / n) \to 0$.
- *Case $n/\lambda < k \le n/2$.* Then $n - k \ge n/2$, so $e^{-pk(n-k)} \le e^{-k\lambda/2}$ and $T_k \le n\,(e\lambda e^{-\lambda/2})^k$. Here $e\lambda e^{-\lambda/2} = e\lambda e^{-c_n/2}/\sqrt{n} \le 2e^{1 + a/2} \ln n / \sqrt n < 1/2$ for large $n$, so $T_k \le n 2^{-k}$, and the sum over $k > n/\lambda \ge n/(2\ln n)$ is at most $2n\, 2^{-n/(2 \ln n)} \to 0$.

So $\mathbb{E}[Y] \to 0$, and by the [Markov inequality](/markov-inequality/) a.a.s. $Y = 0$.

**Part 2.** If $G$ is disconnected, its smallest component has $k \le n/2$ vertices, so $X \ge 1$ or $Y \ge 1$. By Step 1, $\mathbb{E}[X] = e^{-c_n + o(1)} \to 0$; by Step 3 with $a = 0$, $\mathbb{E}[Y] \to 0$. So $\Pr[G \text{ disconnected}] \le \mathbb{E}[X] + \mathbb{E}[Y] \to 0$.

**Part 3.** Here $c_n \to c$, so $|c_n| \le \ln \ln n$ for large $n$ and Step 0 is not needed. By Steps 1 and 2, $\mathbb{E}[(X)_k] \to \mu^k$ for each fixed $k$, with $\mu = e^{-c}$.

*The Poisson limit for $k = 0$.* For an integer $x \ge 0$ and $j \ge 0$, the identity $\sum_{i=0}^{j} (-1)^i \binom{x}{i} = (-1)^j \binom{x-1}{j}$ for $x \ge 1$ shows that the truncated sum is at least $[x = 0]$ for even $j$ and at most $[x = 0]$ for odd $j$ (for $x = 0$ it equals 1). Taking expectations, with $\mathbb{E}\binom{X}{i} = \mathbb{E}[(X)_i]/i!$, gives the Bonferroni inequalities of the [inclusion-exclusion principle](/inclusion-exclusion-principle/):

$$\sum_{i=0}^{2J+1} (-1)^i \frac{\mathbb{E}[(X)_i]}{i!} \le \Pr[X = 0] \le \sum_{i=0}^{2J} (-1)^i \frac{\mathbb{E}[(X)_i]}{i!}.$$

Let $n \to \infty$ with $J$ fixed: the two sides tend to the partial sums $\sum_{i \le 2J+1} (-\mu)^i/i!$ and $\sum_{i \le 2J} (-\mu)^i/i!$, which tend to $e^{-\mu}$ as $J \to \infty$. So $\Pr[X = 0] \to e^{-\mu}$. The same argument applied to $\Pr[X = k] = \mathbb{E}\bigl[\binom{X}{k} [X - k = 0]\bigr]$, with $\sum_{i \ge 0} (-1)^i \binom{X}{k}\binom{X - k}{i}$ and $\binom{X}{k}\binom{X-k}{i} = \binom{k+i}{k}\binom{X}{k+i}$, gives $\Pr[X = k] \to e^{-\mu}\mu^k/k!$.

*Connectivity.* The graph is connected if and only if $X = 0$ and $Y = 0$, apart from the case $n = 1$. So $\Pr[X = 0] - \Pr[Y \ge 1] \le \Pr[\text{connected}] \le \Pr[X = 0]$. Since $c_n \ge c - 1$ for large $n$, Step 3 applies with $a = |c| + 1$, and $\Pr[Y \ge 1] \le \mathbb{E}[Y] \to 0$. So $\Pr[\text{connected}] \to e^{-\mu} = e^{-e^{-c}}$. $\blacksquare$

## Consequences

- **Sharp threshold.** The probability of being connected moves from near 0 to near 1 while $p$ changes by $O(1/n)$, a small fraction of $\ln n / n$. This is the standard example of a sharp threshold.
- **Isolated vertices decide.** The proof shows that at $p = (\ln n + c)/n$ the graph is a.a.s. one giant component plus isolated vertices. Bollobás and Thomason showed more: in the random graph process that adds edges one by one in random order, the graph becomes connected a.a.s. at the very edge that removes the last isolated vertex.
- **$G(n, M)$.** The same limit holds for the model with $M = \frac{n}{2}(\ln n + c)$ edges, which is the form Erdős and Rényi proved: they wrote $M = \frac12 n \ln n + c' n$, and the limit $e^{-e^{-2c'}}$ is the same statement with $c = 2c'$.
- **Mean degree.** At the threshold the mean degree is about $\ln n$, so a random network needs a mean degree that grows with $n$ to be connected; with constant mean degree it always has isolated vertices.
- **Higher connectivity.** The same method shows that $p = (\ln n + (k - 1)\ln \ln n + c)/n$ is the threshold for minimum degree $k$ and for $k$-connectivity, and for $k = 2$ also for a [Hamiltonian cycle](/hamiltonian-cycle/).

## Tightness

The window cannot be narrowed: for each fixed $c$, the limit $e^{-e^{-c}}$ is strictly between 0 and 1, so no sequence $p = (\ln n + O(1))/n$ makes the graph a.a.s. connected or a.a.s. disconnected.

The limit is approached slowly. Exact values from Gilbert's recurrence $C_m = 1 - \sum_{k=1}^{m-1} \binom{m-1}{k-1} C_k (1 - p)^{k(m-k)}$, where $C_k$ is the probability that $G(k, p)$ is connected, give:

| $c$ | $p$ for $n = 1000$ | $\Pr[\text{connected}]$, $n = 100$ | $\Pr[\text{connected}]$, $n = 1000$ | $e^{-e^{-c}}$ |
|---|---|---|---|---|
| $-1$ | 0.00591 | 0.0686 | 0.0678 | 0.0660 |
| 0 | 0.00691 | 0.3886 | 0.3740 | 0.3679 |
| 1 | 0.00791 | 0.7176 | 0.6981 | 0.6922 |
| 2 | 0.00891 | 0.8910 | 0.8770 | 0.8734 |

For $n = 1000$ and $c = 0$, $\mathbb{E}[X] = 1000 \cdot (1 - p)^{999} \approx 0.983$, and $e^{-0.983} \approx 0.374$ already matches the exact probability to three digits: almost all of the error in the limit comes from $\mathbb{E}[X]$ not yet being $e^{-c}$, not from larger components.

The proof needs $c_n$ to be compared with $\ln n$: if $p = \alpha \ln n / n$ with a constant $\alpha < 1$, the expected number of isolated vertices is about $n^{1 - \alpha} \to \infty$, and with $\alpha > 1$ it is about $n^{1-\alpha} \to 0$.

## History

Erdős and Rényi proved the theorem in 1959, in the first of their papers on random graphs, for a uniform graph with a given number of edges. In the same year Gilbert studied $G(n, p)$, gave the recurrence for the probability of connectivity, and its asymptotic form. Later work found the hitting time version (Bollobás and Thomason, 1985) and the thresholds for $k$-connectivity and for Hamiltonian cycles (Komlós and Szemerédi, Bollobás, in the 1980s).

## References
