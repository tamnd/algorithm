---
title: UG-hardness of sparsest cut and multicut, the cube lemma in full and the reduction as a sketch
proves: [statement]
status: sketch
---

This file proves in full the cube lemma that gives completeness. The rest of the reduction of Chawla, Krauthgamer, Kumar, Rabani and Sivakumar (CKKRS) is a sketch: the soundness analysis uses Friedgut's junta theorem (KKL in the conference version), which is cited, and the weights and constants are not tracked. Khot and Vishnoi prove a similar result with a different analysis.

## The cube lemma, in full

Let $Q_m$ be the cube graph on $\{0,1\}^m$, where $x$ and $y$ are adjacent when they differ in one coordinate. For $x \in \{0,1\}^m$ let $\bar x$ be the antipodal point, with every coordinate flipped. There are $2^{m-1}$ antipodal pairs.

**Lemma.** For every $S \subseteq \{0,1\}^m$, the number of edges of $Q_m$ with one end in $S$ is at least the number of antipodal pairs that $S$ separates. A coordinate cut $S = \{x : x_i = 0\}$ cuts exactly $2^{m-1}$ edges and separates all $2^{m-1}$ pairs.

*Proof.* Let $e_j$ be the $j$-th unit vector. For each $x$ define the path

$$P_x : x,\ x \oplus e_1,\ x \oplus e_1 \oplus e_2,\ \ldots,\ x \oplus e_1 \oplus \cdots \oplus e_m = \bar x .$$

Each antipodal pair $\{x, \bar x\}$ has the two paths $P_x$ and $P_{\bar x}$. If $S$ separates the pair, each of the two paths crosses the cut at least once. So the number of pairs (path, cut edge on it) is at least $2 \cdot \mathrm{sep}(S)$.

Now count from the other side. An edge $\{y, y \oplus e_j\}$ of direction $j$ is the $j$-th step of $P_x$ exactly when $x \oplus e_1 \oplus \cdots \oplus e_{j-1}$ is $y$ or $y \oplus e_j$. That gives exactly two paths through the edge. So the number of pairs (path, cut edge on it) is exactly $2 \cdot |\delta(S)|$. Together, $|\delta(S)| \ge \mathrm{sep}(S)$.

For the coordinate cut, the cut edges are those of direction $i$, which are $2^{m-1}$, and $x$ and $\bar x$ always differ in coordinate $i$, so every pair is separated. $\square$

So with unit capacities and unit antipodal demands, the sparsest cut of $Q_m$ has sparsity exactly $1$, and a coordinate cut reaches it. A direct search over all cuts for $m = 2, 3, 4$ agrees.

## The reduction, a sketch

**Input.** A unique game on a regular graph $H = (W, F)$ with label set $[m]$, a bijection $\pi_{uv}$ on each edge, and the promise that the value is at least $1 - \eta$ or at most $\delta$.

**The graph.** For each $v \in W$ take a copy $\{v\} \times \{0,1\}^m$ of the cube, with its cube edges. For each constraint $(u, v)$ and each $x$, add an edge from $(u, x)$ to $(v, \pi_{uv}(x))$, where $\pi_{uv}$ acts on $x$ by permuting coordinates, so that coordinate $a$ of the first cube matches coordinate $\pi_{uv}(a)$ of the second. The constraint edges get a weight $\lambda$ relative to the cube edges, chosen as a function of $m$ and $\eta$. The demand pairs are the antipodal pairs $\{(v, x), (v, \bar x)\}$ of every cube.

**Completeness.** Let $\ell$ satisfy a $1 - \eta$ fraction of the constraints. Cut every cube along coordinate $\ell(v)$, consistently across constraint edges where this is possible. By the cube lemma this separates every antipodal pair at a cost of a $1/m$ fraction of the cube edges. A constraint edge $(u, x) \to (v, \pi_{uv}(x))$ crosses the cut only if $\ell(v) \ne \pi_{uv}(\ell(u))$, so the constraint edges cost at most an $\eta$ fraction of their weight. This gives a multicut of small cost, and a cut of small sparsity.

**Soundness, in outline.** Take a solution that separates most antipodal pairs at a cost at most $L$ times the completeness cost. On a typical cube $v$ the restriction is a function $f_v : \{0,1\}^m \to \{0,1\}$ (the side of the cut, or the component) with total influence $O(L)$ after the normalization of the cube edges, and the antipodal condition forces $f_v$ to be far from constant. Friedgut's junta theorem says that a function with total influence $I$ is $\gamma$-close to a function of $\exp(O(I/\gamma))$ coordinates. Because the constraint edges are cheap to cut only in a small fraction, for most constraints $(u, v)$ the functions $f_u$ and $f_v \circ \pi_{uv}$ are close, so their juntas share a coordinate under $\pi_{uv}$. Labeling each $v$ by a random coordinate of its junta satisfies an $\exp(-O(L))$ fraction of the constraints. If the game has value at most $\delta$, this forces $L \ge \Omega(\log(1/\delta))$. The choice of $\lambda$ and the completeness bound force $L \le O(1/\eta)$ for the completeness case to be cheaper. Together these give the factor $L(n) = c_1 \min\{1/\eta, \log(1/\delta)\}$, with $n^{c_2}$ in place of $n$ because the graph has size $|W| 2^m$ and $m = O(\log |W|)$.

**From multicut to sparsest cut.** The hardness is first proved for a bicriteria form of multicut: separate most of the demand pairs at small cost. An algorithm that finds a cut within a factor $C$ of the sparsest cut can be applied again and again, each time removing the demand pairs it separates, until most pairs are separated. Each round separates demand at a cost of at most $C$ times the optimal multicut cost per unit of demand, so the rounds together give a bicriteria multicut within $O(C)$ of the optimum. So a $C$-approximation for sparsest cut would solve the hard bicriteria multicut problem, and this is a Cook reduction. $\blacksquare$
