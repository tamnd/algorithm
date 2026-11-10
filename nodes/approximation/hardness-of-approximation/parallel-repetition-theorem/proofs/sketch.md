---
title: Parallel repetition, the two easy bounds in full and the upper bound as a sketch
proves: [statement]
status: sketch
---

This file proves the two easy bounds of the statement in full and gives the upper bound of Raz and Holenstein as a sketch. The sketch follows Holenstein's proof. It names each step and the inequality that the step uses, but it does not prove the correlated sampling lemma or the divergence bounds, and it does not track constants. For the full proof see Holenstein (2009), the main theorem and its proof. Arora and Barak, Chapter 22, Section 22.3, state the theorem and use it.

## Notation

$G = (X, Y, A, B, \mu, V)$ is a game with $\operatorname{val}(G) = 1 - \varepsilon$, and $s = |A| \cdot |B|$. In $G^{\otimes k}$ the verifier draws $(x_j, y_j) \sim \mu$ independently for $j = 1, \ldots, k$, sends $\bar x = (x_1, \ldots, x_k)$ to the first prover and $\bar y = (y_1, \ldots, y_k)$ to the second, receives $\bar a \in A^k$ and $\bar b \in B^k$, and accepts when $V(x_j, y_j, a_j, b_j) = 1$ for all $j$. For a fixed strategy and $S \subseteq [k]$, $W_S$ is the event that the check passes in every coordinate of $S$.

## The lower bound, in full

*Claim:* $\operatorname{val}(G^{\otimes k}) \ge \operatorname{val}(G)^k$. Let $(f, g)$ be an optimal strategy for $G$. In $G^{\otimes k}$ the first prover answers $(f(x_1), \ldots, f(x_k))$ and the second answers $(g(y_1), \ldots, g(y_k))$. The $k$ question pairs are independent, and the check in coordinate $j$ depends only on the pair $(x_j, y_j)$, so the $k$ checks are independent events of probability $\operatorname{val}(G)$ each. They all pass with probability $\operatorname{val}(G)^k$. $\square$

## The trivial upper bound, in full

*Claim:* $\operatorname{val}(G^{\otimes k}) \le \operatorname{val}(G)$. Let $(F, H)$ be any strategy for $G^{\otimes k}$. Build a randomized strategy for $G$: the provers share a random string that gives pairs $(x_j, y_j) \sim \mu$ for $j = 2, \ldots, k$. On question $x$ the first prover forms $\bar x = (x, x_2, \ldots, x_k)$ and answers the first coordinate of $F(\bar x)$. On question $y$ the second prover forms $\bar y = (y, y_2, \ldots, y_k)$ and answers the first coordinate of $H(\bar y)$. The tuple $(\bar x, \bar y)$ has the distribution of $G^{\otimes k}$, and the check of $G$ is the check of coordinate $1$, which passes whenever all $k$ checks pass. So the randomized strategy wins $G$ with probability at least the value of $(F, H)$. A randomized strategy wins with probability at most $\operatorname{val}(G)$, since it is an average of deterministic ones. $\square$

## The upper bound, a sketch

**Goal.** Fix a strategy for $G^{\otimes k}$. We build a set $S$ of coordinates, one at a time, such that $\Pr[W_S]$ falls by a factor $1 - \varepsilon/2$ at each step, for $t = \Omega(\varepsilon^2 k / \log s)$ steps. Then $\Pr[W_{[k]}] \le \Pr[W_S] \le (1 - \varepsilon/2)^t$, which is $(1 - \varepsilon^3)^{\Omega(k / \log s)}$.

**Step 1, the main lemma.** Let $S \subseteq [k]$ with $|S| = t$ and suppose $\Pr[W_S] = 2^{-d}$. The lemma says that for a uniformly random coordinate $j \notin S$,

$$\mathbb{E}_j \Pr[W_{\{j\}} \mid W_S] \le \operatorname{val}(G) + O\Big(\sqrt{\tfrac{d + t \log s}{k - t}}\Big).$$

If the error term is at most $\varepsilon/2$, some $j \notin S$ has $\Pr[W_{\{j\}} \mid W_S] \le 1 - \varepsilon/2$. Adding $j$ to $S$ gives $\Pr[W_{S \cup \{j\}}] \le (1 - \varepsilon/2) \Pr[W_S]$.

**Step 2, conditioning changes the questions only a little.** Condition on $W_S$ and on the answers in the coordinates of $S$. This event has probability at least $2^{-d} s^{-t}$, because there are at most $s^t$ answer tuples on $S$. The questions in the $k - t$ coordinates outside $S$ were independent before the conditioning. A standard bound on the Kullback-Leibler divergence says that conditioning a product distribution of $k - t$ independent parts on an event of probability $2^{-D}$ changes the average part by divergence at most $D / (k - t)$. With $D = d + t \log s$ and Pinsker's inequality, for a typical $j$ the conditioned distribution of $(x_j, y_j)$ is within statistical distance $O(\sqrt{D / (k - t)})$ of $\mu$.

**Step 3, embed one game in coordinate $j$.** Suppose that $\Pr[W_{\{j\}} \mid W_S]$ were larger than $\operatorname{val}(G) + \gamma$ for the error term $\gamma$. The provers of a single game $G$ receive $(x, y) \sim \mu$ and want to act as if $(x, y)$ were the pair of coordinate $j$ in the conditioned repeated game. Each needs the other questions of the repeated game. Raz's idea is a family of *dependency-breaking* variables: for each coordinate $i \ne j$ outside $S$ fix either $x_i$ or $y_i$ at random, and fix both questions in $S$ together with the answers in $S$. Given these variables and $x$, the first prover's remaining questions are independent of $y$, and symmetrically for the second prover. So each prover can sample its own missing questions from its own conditional distribution.

**Step 4, correlated sampling.** The two provers must agree on the dependency-breaking variables without communication, but each knows only its own question, so their conditional distributions differ. Holenstein's correlated sampling lemma says that two parties with shared randomness, holding distributions $P$ and $Q$ at statistical distance $\eta$, can each output a sample, from $P$ and from $Q$, so that the two samples are equal with probability at least $1 - 2\eta$. Step 2 bounds the distance by $O(\gamma)$, so the provers agree with probability $1 - O(\gamma)$. They then answer coordinate $j$ of the strategy of $G^{\otimes k}$. This wins $G$ with probability more than $\operatorname{val}(G) + \gamma - O(\gamma)$, and with the right constants this exceeds $\operatorname{val}(G)$, a contradiction. This proves the lemma.

**Step 5, count the steps.** Let $T = \lfloor c \varepsilon^2 k / \log s \rfloor$ for a small constant $c$, and let $q = (1 - \varepsilon/2)^T$. Start with $S = \emptyset$. While $|S| < T$ and $\Pr[W_S] \ge q$, apply Step 1. During the process $d \le T \log_2 (1/(1 - \varepsilon/2)) = O(\varepsilon T)$ and $|S| \le T \le k/2$, so the error term is $O(\sqrt{(\varepsilon T + T \log s)/k})$, which is at most $\varepsilon/2$ when $c$ is small enough. So each step multiplies $\Pr[W_S]$ by at most $1 - \varepsilon/2$. The process ends either with $\Pr[W_S] < q$ or after $T$ steps with $\Pr[W_S] \le (1 - \varepsilon/2)^T = q$. In both cases $\Pr[W_{[k]}] \le \Pr[W_S] \le q$. By Bernoulli's inequality $(1 - \varepsilon/2)^{\varepsilon^2} \le 1 - \varepsilon^3/2$, so $q \le (1 - \varepsilon^3/2)^{\Omega(k / \log s)}$. $\blacksquare$

**Projection games.** Rao's improvement for projection games replaces the $t \log s$ term: in a projection game the second prover's answer is a function of the first prover's answer on an accepted pair, and Rao shows that conditioning on $W_S$ can be handled without paying for the answers. The bound becomes $(1 - \varepsilon^2)^{\Omega(k)}$ with no dependence on $s$. This file does not sketch that argument.
