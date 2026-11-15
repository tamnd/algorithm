---
title: The chains are stochastic, the teleported chain converges, and local Kemenization is locally optimal
proves: [correctness]
status: full
---

Let $\tau_1, \ldots, \tau_k$ be rankings of items from the union $U$, with $n = |U|$. A ranking may be partial. For a list $\tau$ and an item $x$ in it, $\tau(x)$ is its rank, and "$\tau$ puts $Q$ above $P$" means $\tau(Q) < \tau(P)$. Write $Q \succ P$ when strictly more of the lists that rank both $P$ and $Q$ put $Q$ above $P$ than put $P$ above $Q$. The matrix $M$ is the one that line L2 builds, and $M_\varepsilon = (1 - \varepsilon) M + (\varepsilon / n) J$ is the matrix of line L3, where $J$ is the $n \times n$ matrix of ones.

**Lemma 1.** For each of MC1 to MC4, every row of $M$ is a probability distribution.

*Proof.* The entries are sums of nonnegative terms, so it is enough to show that each row sums to 1. For MC1 the row of $P$ spreads weight $1/|S|$ on each element of a nonempty multiset $S$; $S$ holds $P$ itself, since each list that holds $P$ ranks $P$ at or above $P$. For MC2 the row is the average, over the lists that hold $P$, of a uniform distribution on a nonempty set. For MC3 the row is the average, over the lists that hold $P$, of a distribution that sends each of the $|\tau|$ items $Q$ of $\tau$ either to $Q$ or to $P$, with weight $1/|\tau|$ each. For MC4 each of the $n$ items $Q$ sends weight $1/n$ either to $Q$ or to $P$. Each item of $U$ is in at least one list, so the set of lists that hold $P$ is never empty. $\square$

The matrix $M_\varepsilon$ is then stochastic too, because $J/n$ is stochastic and the set of stochastic matrices is convex.

**Lemma 2 (contraction).** Let $0 < \varepsilon \le 1$. For any two probability row vectors $\mu, \nu$, $\lVert \mu M_\varepsilon - \nu M_\varepsilon \rVert_1 \le (1 - \varepsilon) \lVert \mu - \nu \rVert_1$.

*Proof.* Let $x = \mu - \nu$. Its entries sum to 0, so $x J = 0$ and $x M_\varepsilon = (1 - \varepsilon) x M$. For a stochastic $M$, $\lVert x M \rVert_1 = \sum_j |\sum_i x_i M_{ij}| \le \sum_i |x_i| \sum_j M_{ij} = \lVert x \rVert_1$. $\square$

**Theorem 1.** For $0 < \varepsilon \le 1$, $M_\varepsilon$ has exactly one stationary distribution $\pi$, and the vectors $\pi_t$ of line L5, started from the uniform vector of line L4, satisfy $\lVert \pi_t - \pi \rVert_1 \le 2 (1 - \varepsilon)^t$.

*Proof.* The set of probability vectors with the $L_1$ distance is complete, and by Lemma 2 the map $\mu \mapsto \mu M_\varepsilon$ is a contraction on it. By the Banach fixed point theorem it has exactly one fixed point $\pi$, which is a stationary distribution, and no other stationary distribution exists. Since $\pi M_\varepsilon = \pi$, Lemma 2 gives $\lVert \pi_t - \pi \rVert_1 \le (1 - \varepsilon)^t \lVert \pi_0 - \pi \rVert_1 \le 2 (1 - \varepsilon)^t$. $\square$

So line L5 stops after at most $\lceil \ln(2/\mathrm{tol}) / \varepsilon \rceil + 1$ steps, since $(1 - \varepsilon)^t \le e^{-\varepsilon t}$, and the order of line L6 is the order of the unique $\pi$, up to items whose probabilities differ by less than the error.

**Theorem 2 (MC4 and a Condorcet winner).** Take $\varepsilon = 0$ and the chain MC4. Suppose some item $w$ satisfies $w \succ y$ for every $y \ne w$. Then $w$ is absorbing, the stationary distribution is unique and equal to the unit vector $e_w$, and power iteration from any start converges to it.

*Proof.* From $w$, a move to $Q \ne w$ needs $Q \succ w$, which fails because $w \succ Q$ and the relation is asymmetric. So the row of $w$ is $e_w$. From any $P \ne w$, the chain picks $Q = w$ with probability $1/n$ and then moves, because $w \succ P$. So for any distribution $\mu$, the mass off $w$ after one step is at most $(1 - 1/n)$ times the mass off $w$ before: mass at $w$ stays, and each state $P \ne w$ sends at least $\mu_P / n$ to $w$. After $t$ steps the mass off $w$ is at most $(1 - 1/n)^t$, which tends to 0. A stationary $\pi$ is its own image after $t$ steps for each $t$, so its mass off $w$ is 0, and $\pi = e_w$. $\square$

**Theorem 3 (MC3 after one step).** Let all $k$ lists be full rankings of $U$, and let $R(Q) = \sum_{l=1}^{k} \tau_l(Q)$ be the total rank of $Q$. For MC3 with $\varepsilon = 0$, one step from the uniform vector gives

$$\pi_1(Q) = \frac{1}{n} \left( 1 + \frac{k(n + 1) - 2 R(Q)}{k n} \right).$$

So the order of $\pi_1$ is the order of increasing total rank, which is the Borda order.

*Proof.* Each list holds each item. From $P \ne Q$, the chain moves to $Q$ when it picks a list $\tau$ (probability $1/k$) with $\tau(Q) < \tau(P)$ and then picks $Q$ (probability $1/n$). So $M_{PQ} = |\{l : \tau_l(Q) < \tau_l(P)\}| / (k n)$. Summing over $P \ne Q$ counts, for each list, the items below $Q$: $\sum_{P \ne Q} M_{PQ} = \sum_l (n - \tau_l(Q)) / (k n)$. The chain leaves $Q$ for $R'$ when it picks a list with $\tau(R') < \tau(Q)$ and then $R'$, so $1 - M_{QQ} = \sum_l (\tau_l(Q) - 1)/(k n)$. Then $\pi_1(Q) = \frac{1}{n} (\sum_{P \ne Q} M_{PQ} + M_{QQ}) = \frac{1}{n} (1 + \sum_l (n + 1 - 2 \tau_l(Q))/(k n))$, which is the formula. $\square$

**Lemma 3 (one swap).** Let $\sigma$ be a ranking of $U$ in which $y$ is directly above $x$, and let $\sigma'$ be $\sigma$ with the two swapped. Then $K(\sigma', \tau_1, \ldots, \tau_k) = K(\sigma, \tau_1, \ldots, \tau_k) - a + b$, where $K$ is the sum over the lists of the number of pairs that both rank in opposite orders, $a$ is the number of lists that rank both and put $x$ above $y$, and $b$ the number that put $y$ above $x$.

*Proof.* The swap changes the relative order of the pair $\{x, y\}$ only. Every other pair keeps its order in $\sigma'$, so its disagreements do not change. The pair $\{x, y\}$ was a disagreement for the $a$ lists before the swap and is one for the $b$ lists after. $\square$

So $x \succ y$ means exactly that the swap lowers $K$. A ranking is *locally Kemeny optimal* when no swap of two neighbours lowers $K$, that is, when no item is directly below an item that it beats.

**Theorem 4 (local Kemenization).** Lines L7 to L9 return a permutation $\rho$ of the input order $\sigma$ such that (a) $\rho$ is locally Kemeny optimal, (b) $K(\rho) \le K(\sigma)$, and (c) if $C \subset U$ is a nonempty proper subset with $x \succ y$ for all $x \in C$ and $y \notin C$, then the items of $C$ are the first $|C|$ items of $\rho$.

*Proof.* (a) Invariant: after the step that inserts the $m$-th item of $\sigma$, the output list holds the first $m$ items of $\sigma$ and no item of it is directly below an item that it beats. It holds after the first step. Assume it before the insertion of $x$. The new item starts at the bottom and moves up only past a neighbour that it beats. When it stops, its upper neighbour $u$ (if any) is not beaten by $x$. Its lower neighbour $v$ (if any) is the item it passed last, so $x \succ v$ and, by asymmetry, $v$ does not beat $x$. The pair $(u, v)$ is no longer adjacent. All other adjacent pairs were adjacent before, in the same order, so the invariant holds.

(b) Consider the full ranking that has the current output list on top and the items of $\sigma$ not yet inserted below it, in the order of $\sigma$. At the start it is $\sigma$, and at the end it is $\rho$. Appending the next item does not change it. Each swap in line L9 exchanges two neighbours of this full ranking, with the lower one beating the upper one, so by Lemma 3 it lowers $K$ by $b - a \ge 1$.

(c) Suppose not. Then some $y \notin C$ is above some $x \in C$ in $\rho$. Walk down $\rho$ from $y$ to $x$: the walk starts outside $C$ and ends inside $C$, so at some step an item $y' \notin C$ is directly above an item $x' \in C$. By hypothesis $x' \succ y'$, which contradicts (a). $\square$

Each of the four theorems is checked on random small inputs in `impl/python/test_markov_chain_rank_aggregation.py`, with Theorem 1 compared against an exact solve of $\pi M_\varepsilon = \pi$ over the rationals.
