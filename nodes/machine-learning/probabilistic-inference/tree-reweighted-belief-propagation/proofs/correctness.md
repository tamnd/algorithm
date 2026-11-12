---
title: TRW fixed points are locally consistent, the TRW objective bounds log Z, and rho = 1 on a tree is exact
proves: [correctness]
status: full
---

We use the model, the messages, the pseudomarginals $\tau$ and the objective $B$ of the page. The distribution is $p(x) = \exp(\langle \theta, \phi(x) \rangle - \log Z)$ with all potentials finite, so $p > 0$. The vector $\rho$ comes from a probability distribution $\rho(T)$ over the spanning trees $T$ of the graph, $\rho_{st} = \sum_{T \ni (s,t)} \rho(T)$, and every $\rho_{st} > 0$. For marginals $\mu$, write $H_T(\mu) = \sum_s H(\mu_s) - \sum_{(s,t) \in T} I_{st}(\mu_{st})$.

**Lemma 1 (the tree entropy bounds the entropy).** Let $q$ be a positive distribution with single and pairwise marginals $\mu$, and let $T$ be a spanning tree. Then $H(q) \le H_T(\mu)$.

*Proof.* Let $q_T(x) = \prod_s \mu_s(x_s) \prod_{(s,t) \in T} \frac{\mu_{st}(x_s, x_t)}{\mu_s(x_s) \mu_t(x_t)}$. It sums to 1: take a leaf $\ell$ of $T$ with neighbor $u$; the only terms with $x_\ell$ are $\mu_\ell(x_\ell) \cdot \mu_{\ell u}(x_\ell, x_u) / (\mu_\ell(x_\ell) \mu_u(x_u))$, and their sum over $x_\ell$ is $1$. Remove $\ell$ and repeat until one node is left, whose $\mu_s$ sums to 1. So $q_T$ is a distribution, and $\mathrm{KL}(q \| q_T) \ge 0$. Now $\log q_T(x)$ is a sum of functions of single variables and of edges, so its expected value under $q$ depends only on $\mu$: $\mathbb{E}_q[\log q_T] = -\sum_s H(\mu_s) + \sum_{(s,t) \in T} I_{st}(\mu_{st}) = -H_T(\mu)$. Hence $0 \le \mathrm{KL}(q \| q_T) = -H(q) + H_T(\mu)$. $\square$

**Theorem 1 (upper bound).** Let $\mu$ be the true single and pairwise marginals of $p$. Then $B(\mu) \ge \log Z$, and so $\max_{\tau \in \mathbb{L}} B(\tau) \ge \log Z$, where $\mathbb{L}$ is the local polytope.

*Proof.* Average Lemma 1 over $\rho(T)$: $H(p) \le \sum_T \rho(T) H_T(\mu) = \sum_s H(\mu_s) - \sum_{(s,t)} \rho_{st} I_{st}(\mu_{st})$, because $\sum_T \rho(T) = 1$ and each edge appears with total weight $\rho_{st}$. Also $\log p(x) = \langle \theta, \phi(x) \rangle - \log Z$, so $-H(p) = \mathbb{E}_p[\log p] = \langle \theta, \mu \rangle - \log Z$, that is $\log Z = \langle \theta, \mu \rangle + H(p)$. Together, $\log Z \le \langle \theta, \mu \rangle + \sum_s H(\mu_s) - \sum \rho_{st} I_{st}(\mu_{st}) = B(\mu)$. The true marginals are locally consistent, so $\mu \in \mathbb{L}$. $\square$

**Lemma 2 (local consistency at fixed points).** At a fixed point of the messages, $\sum_{x_t} \tau_{st}(x_s, x_t) = \tau_s(x_s)$ for every edge.

*Proof.* Write $P_t(x_t) = \exp(\theta_t(x_t)) \prod_{v \in N(t) \setminus s} M_{vt}(x_t)^{\rho_{vt}} / M_{st}(x_t)^{1 - \rho_{st}}$ and $P_s$ in the same way with $s$ and $t$ swapped. Then $\tau_{st} \propto \exp(\theta_{st}/\rho_{st}) P_s(x_s) P_t(x_t)$, and

$$\sum_{x_t} \tau_{st}(x_s, x_t) \propto P_s(x_s) \sum_{x_t} \exp(\theta_{st}(x_s, x_t)/\rho_{st}) P_t(x_t) = P_s(x_s)\, c\, M_{ts}(x_s),$$

with a constant $c > 0$, by the message rule at the fixed point. And $P_s(x_s) M_{ts}(x_s) = \exp(\theta_s(x_s)) \prod_{v \in N(s) \setminus t} M_{vs}^{\rho_{vs}} \cdot M_{ts}^{1 - (1 - \rho_{st})} = \exp(\theta_s(x_s)) \prod_{v \in N(s)} M_{vs}(x_s)^{\rho_{vs}}$, which is the unnormalized $\tau_s$. Both sides sum to 1. $\square$

**Theorem 2 (the tree case).** If the graph is a tree, the only spanning tree is the graph itself, so $\rho_{st} = 1$ for every edge. Then the TRW messages are the sum-product messages, the iteration converges for every damping $\lambda \in [0, 1)$, and at the limit $\tau$ are the exact marginals and $B(\tau) = \log Z$.

*Proof.* With $\rho = 1$, the factor $M_{st}^{1 - \rho_{st}}$ is $1$, the exponents $\rho_{vt}$ are 1, and $\theta_{st}/\rho_{st} = \theta_{st}$, so the update is the sum-product update. On a tree, the message on a directed edge $(t, s)$ depends only on the messages that come from the subtree on the side of $t$. By induction on the height $h$ of that subtree, the message tends to the exact sum-product message: for $h = 0$ ($t$ a leaf) the target does not change, and the damped iteration $m \leftarrow \mathrm{normalize}((1 - \lambda) m^\ast + \lambda m)$ toward a fixed normalized target $m^\ast$ moves the distance by a factor $\lambda$; for larger $h$, the inputs tend to their limits and the update is continuous in them, so the target tends to the exact message and the damped iteration follows it. The exact sum-product messages on a tree give the exact marginals $\mu$. Then $p$ is the tree distribution $q_T$ of Lemma 1 with $T$ the graph, so $\mathrm{KL}(p \| q_T) = 0$, $H(p) = H_T(\mu)$, and the proof of Theorem 1 holds with equality: $B(\mu) = \log Z$. $\blacksquare$

**Remark (the variational meaning).** The function $B$ is concave on $\mathbb{L}$, and the fixed points of the TRW messages are exactly the points of $\mathbb{L}$ that satisfy the Lagrangian conditions for $\max_{\mathbb{L}} B$, so at a fixed point $B(\tau) = \max_{\mathbb{L}} B \ge \log Z$ (Wainwright, Jaakkola and Willsky 2005). Lemma 2 is the consistency half of that statement. Nothing here says that the message iteration converges on a graph with cycles; a run that does not converge gives no bound.
