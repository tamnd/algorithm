---
title: A thin tree gives a tour of cost at most c(T) + 2 alpha LP*, and an outline of why max entropy trees are thin
proves: [correctness]
status: sketch
---

This file has two parts. Part 1 is a full proof that the lines L6 to L10 turn each spanning tree $T$ of the support into a tour of cost at most $c(T) + 2\alpha_T \cdot \text{LP}^*$, where $\alpha_T$ is the thinness of $T$, and that the cheapest of the sampled trees costs at most $2 \cdot \text{LP}^*$ with high probability. It uses Hoffman's circulation theorem and the integrality of network flows, which are cited. Part 2 is only an outline of the theorem of Asadpour, Goemans, Mądry, Oveis Gharan and Saberi that a max entropy tree is $O(\log n / \log\log n)$-thin with high probability. Part 2 is not a proof.

## Part 1: from a thin tree to a tour (full)

The costs $c(u, v) \ge 0$ on the ordered pairs of $V$, $|V| = n \ge 3$, satisfy the directed triangle inequality $c(u, w) \le c(u, v) + c(v, w)$, as shortest path costs do. For $U \subseteq V$, $\delta^+(U)$ is the set of arcs that leave $U$ and $\delta^-(U)$ the set of arcs that enter $U$. The ATSP LP is

$$\min\ c \cdot x \quad \text{s.t.} \quad x(\delta^+(v)) = x(\delta^-(v)) = 1 \ (v \in V), \quad x(\delta^+(U)) \ge 1 \ (\emptyset \ne U \subsetneq V), \quad x \ge 0,$$

with optimal solution $x^*$ and value LP*. Each tour is feasible, so $\text{LP}^* \le \text{OPT}$. For an unordered pair $e = \{u, v\}$, $z_e = (1 - 1/n)(x^*_{uv} + x^*_{vu})$ and $c(e) = \min(c(u, v), c(v, u))$. For an undirected cut, $\delta(U)$ is the set of pairs with one end in $U$.

**Definition (thinness).** A spanning tree $T$ is $\alpha$-thin with respect to $z$ if $|T \cap \delta(U)| \le \alpha \cdot z(\delta(U))$ for each $\emptyset \ne U \subsetneq V$. The thinness $\alpha_T$ is the least such $\alpha$.

**Lemma 1 (cuts of $x^*$).** For each $U$, $x^*(\delta^+(U)) = x^*(\delta^-(U))$, and so $z(\delta(U)) \le 2x^*(\delta^+(U))$.

*Proof.* Sum $x^*(\delta^+(v)) - x^*(\delta^-(v)) = 0$ over $v \in U$. Each arc inside $U$ is counted once with each sign, so the sum is $x^*(\delta^+(U)) - x^*(\delta^-(U)) = 0$. Then $z(\delta(U)) = (1 - 1/n)(x^*(\delta^+(U)) + x^*(\delta^-(U))) \le 2x^*(\delta^+(U))$. $\square$

**Lemma 2 (a cheap circulation, Asadpour et al., Theorem 4.2).** Let $A$ be the arcs of $T$, each oriented in its cheaper direction, so $c(A) = c(T)$. There is an integral circulation $g$ with $g_a \ge 1$ for each $a \in A$ and $c \cdot g \le c(T) + 2\alpha_T \cdot \text{LP}^*$.

*Proof.* Put the lower bound $l_a = 1$ on the arcs $a \in A$ and $l_a = 0$ on the other arcs, and the upper bound $u_a = l_a + 2\alpha_T x^*_a$. By Hoffman's circulation theorem, a circulation $f$ with $l \le f \le u$ exists if $l \le u$ and $l(\delta^-(U)) \le u(\delta^+(U))$ for each $U$. The first condition is clear. For the second,

$$l(\delta^-(U)) \le |T \cap \delta(U)| \le \alpha_T\, z(\delta(U)) \le 2\alpha_T\, x^*(\delta^+(U)) \le u(\delta^+(U)),$$

by the definition of $\alpha_T$ and Lemma 1. Since $c \ge 0$, $c \cdot f \le c \cdot u = c(A) + 2\alpha_T\, c \cdot x^* = c(T) + 2\alpha_T \text{LP}^*$. Now drop the upper bounds. The least cost circulation with $f \ge l$ costs at most $c \cdot f$, and because the constraint matrix of a circulation problem is totally unimodular and $l$ is integral, it has an integral optimum $g$. $\square$

**Lemma 3 (line L7 finds the least such circulation).** The arcs $A$ plus the extra arcs of line L7 form a least cost integral circulation $g$ with $g \ge 1$ on $A$.

*Proof.* Write $g = 1_A + h$ with $h \ge 0$ integral. For $g$ to be a circulation, $h$ must send $b(v) = \deg^-_A(v) - \deg^+_A(v)$ units out of each vertex with $b(v) > 0$ and bring $-b(v)$ units into each vertex with $b(v) < 0$. An integral such $h$ splits into unit paths from a vertex with $b > 0$ to a vertex with $b < 0$, plus cycles. Cycles cost at least 0, and by the directed triangle inequality a path from $s$ to $t$ costs at least $c(s, t)$. So the least cost $h$ is a set of direct arcs that pairs the units of surplus with the units of deficit at the least total cost, and that is what line L7 computes. $\square$

**Lemma 4 (the tour).** The tour $H$ of lines L8 and L9 has $c(H) \le c(T) + 2\alpha_T \cdot \text{LP}^*$.

*Proof.* In the multigraph $F$ of line L7, each vertex has equal in-degree and out-degree, and $F$ is connected when the directions are ignored, because it holds the spanning tree $A$. A balanced digraph that is weakly connected is strongly connected and has an Euler circuit, so line L8 succeeds and $c(W) = c \cdot g$. Line L9 keeps the first visit of each vertex. Each arc of $H$ replaces a part of $W$, the parts do not overlap, and by the directed triangle inequality each arc costs at most its part. So $c(H) \le c \cdot g$, and Lemmas 2 and 3 give the bound. $\square$

**Lemma 5 (a cheap sampled tree).** If each tree has the marginals $z$, then $\mathbb{E}[c(T)] \le (1 - 1/n)\text{LP}^*$. With $k$ independent samples, the cheapest one costs more than $2 \cdot \text{LP}^*$ with probability at most $2^{-k}$.

*Proof.* $\mathbb{E}[c(T)] = \sum_e c(e) z_e \le (1 - 1/n)\sum_{u \ne v} c(u, v) x^*_{uv}$, because $c(e)$ is at most both arc costs. By Markov's inequality, one sample costs more than $2 \cdot \text{LP}^*$ with probability at most $1/2$. The samples are independent. $\square$

**Theorem (proved here, given the thinness).** If the cheapest sampled tree $T$ is $\alpha$-thin, line L10 returns a tour with $\text{ALG} \le c(T) + 2\alpha \cdot \text{LP}^*$. With $k = 2\lceil \ln n \rceil$ samples, $c(T) \le 2 \cdot \text{LP}^*$ with probability at least $1 - n^{-2\ln 2} \ge 1 - 1/n$. So if each sampled tree is $\beta$-thin, then $\text{ALG} \le (2 + 2\beta) \cdot \text{LP}^* \le (2 + 2\beta) \cdot \text{OPT}$. $\blacksquare$

## Part 2: max entropy trees are thin (an outline, not a proof)

Asadpour et al. prove that, for $n \ge 5$, a tree from the $\lambda$-uniform distribution with marginals (close to) $z$ is $\beta$-thin with $\beta = 4\ln n / \ln\ln n$ with probability at least $1 - 1/n$. With a union bound over the $k$ samples and Part 1, this gives $\text{ALG} \le (2 + 8\ln n/\ln\ln n) \cdot \text{LP}^*$ with high probability. The steps are these.

1. **One cut.** For a fixed $U$, the number $|T \cap \delta(U)|$ is a sum of indicator variables with mean $z(\delta(U))$. The edges of a $\lambda$-uniform spanning tree are negatively correlated, so the upper tail of a Chernoff bound holds as for independent variables: $\Pr[|T \cap \delta(U)| > (1 + \delta)\mu] \le \big(e^\delta/(1+\delta)^{1+\delta}\big)^\mu$ with $\mu = z(\delta(U))$.
2. **The bound for one cut is small.** With $1 + \delta = \beta$, this probability is at most $(e/\beta)^{\beta\mu}$, and for $\beta = 4\ln n/\ln\ln n$ and $n \ge 5$ this is at most $n^{-2.5\mu}$. It is very small, and smaller for larger cuts.
3. **Count the cuts.** Each cut has $z(\delta(U)) \ge 2(1 - 1/n)$, so the minimum cut of $z$ is close to 2. By Karger's bound, the number of cuts of value at most $\gamma$ times the minimum cut is at most $n^{2\gamma}$. Group the cuts by their value and use a union bound over each group. The small probability of step 2 wins against the count of step 3.
4. **The approximate fit.** The weights $\lambda$ are found only approximately, so the marginals are within a factor $1 + \varepsilon$ of $z$ for a small constant $\varepsilon$. This changes the constants in steps 1 and 2 a little, and Lemma 5 then holds with a factor $1 + \varepsilon$.

So Part 1 is the result that is proved here, and the thinness bound $4\ln n/\ln\ln n$, and with it the ratio $O(\log n / \log\log n)$, is cited from the paper.
