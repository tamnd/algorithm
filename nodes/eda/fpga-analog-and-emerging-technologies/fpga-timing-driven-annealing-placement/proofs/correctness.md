---
title: The annealing placer keeps a legal placement, its incremental cost change equals the change of the cost recomputed from scratch, the criticalities are exact, and it stops
proves: [correctness]
status: full
---

We use the notation of the page. A placement is a map $\mathrm{loc}$ from the $n$ blocks to the sites of an $n_x \times n_y$ grid. It is *legal* when it is injective. A net $e$ is a list of blocks, and its bounding box cost is $\mathrm{bb}(e) = q(|e|) \, (\Delta x(e) + 1 + \Delta y(e) + 1)$, where $\Delta x(e)$ and $\Delta y(e)$ are the spans of the coordinates of its blocks. $BB = \sum_e \mathrm{bb}(e)$. A connection $c = (u, v)$ joins the driver of a net to one of its sinks, with delay $d(c) = 1 + |x_u - x_v| + |y_u - y_v|$, and $T = \sum_c w_c \, d(c)$ with weights $w_c = \mathrm{crit}(c)^{CE}$ that stay fixed during a temperature.

**Lemma 1 (legality is kept).** If the placement is legal before a move, it is legal after it.

*Proof.* A move picks a block $a$ and a site $s \ne \mathrm{loc}(a)$. If $s$ is empty, $a$ moves to $s$, and no other block is at $s$. If block $b$ is at $s$, then $a$ and $b$ exchange sites. In both cases the sites of all other blocks are unchanged, and the map stays injective. The initial placement gives the blocks the first $n$ sites of a shuffled list of distinct sites, so it is legal. $\square$

**Lemma 2 (locality of the cost change).** Let $M$ be the set of moved blocks ($\{a\}$ or $\{a, b\}$). Let $E_M$ be the nets that hold a block of $M$, and $C_M$ the connections with an end in $M$. Then

$$BB' - BB = \sum_{e \in E_M} (\mathrm{bb}'(e) - \mathrm{bb}(e)), \qquad T' - T = \sum_{c \in C_M} w_c \, (d'(c) - d(c)),$$

where primes denote values after the move.

*Proof.* $\mathrm{bb}(e)$ depends only on the sites of the blocks of $e$. A net outside $E_M$ has no block of $M$, and the move changes only the sites of blocks of $M$, so its term is the same before and after. The same holds for $d(c)$ with $c \notin C_M$, and the weights do not change within a temperature. Subtracting the two sums term by term leaves the terms of $E_M$ and $C_M$. $\square$

The function that evaluates a move computes exactly these two sums: it applies the move, sums $\mathrm{bb}$ and $w_c \, d$ over $E_M$ and $C_M$, undoes the move, and subtracts. So the running totals, updated by these differences after each accepted move, are equal to $BB$ and $T$ recomputed from scratch, by induction over the accepted moves. At the start of each temperature the totals are set by a full recomputation, which starts the induction again with the new weights. (The implementation asserts this equality after every move when its check flag is set, up to rounding of floating point.) The move cost

$$\Delta C = \lambda \, \frac{T' - T}{T_{\mathrm{prev}}} + (1 - \lambda) \, \frac{BB' - BB}{BB_{\mathrm{prev}}}$$

is therefore the change of the normalized cost $\lambda T / T_{\mathrm{prev}} + (1 - \lambda) BB / BB_{\mathrm{prev}}$, whose normalizers are fixed during the temperature.

**Lemma 3 (criticalities).** Let the connections form a directed acyclic graph, and let $\ell(c)$ be the largest delay of a path through $c$, where the delay of a path is the sum of the delays of its connections, and $D = \max_c \ell(c) > 0$. Then the timing analysis returns $\mathrm{crit}(c) = \ell(c) / D$.

*Proof.* The procedure orders the blocks topologically by repeatedly taking blocks with no unprocessed fanin ([topological sort](/topological-sort/)). In that order, $\mathrm{arrival}(v)$ is the maximum of $\mathrm{arrival}(u) + d(u, v)$ over fanin connections, which by induction is the largest delay of a path that ends at $v$. In reverse order, $\mathrm{required}(u) = \min(D, \min_v (\mathrm{required}(v) - d(u, v)))$, which by induction is $D$ minus the largest delay of a path that starts at $u$. A path through $c = (u, v)$ is a path that ends at $u$, then $c$, then a path that starts at $v$, so $\ell(c) = \mathrm{arrival}(u) + d(c) + (D - \mathrm{required}(v))$. The returned value is $1 - (\mathrm{required}(v) - \mathrm{arrival}(u) - d(c)) / D = \ell(c) / D$. $\square$

**Lemma 4 (termination).** The number of temperatures is at most $1 + \log(T_0 \, m / 0.005) / \log(1 / 0.95)$ for $m$ nets and initial temperature $T_0 > 0$, and the placer stops.

*Proof.* Each temperature multiplies $T$ by $\alpha \in \{0.5, 0.8, 0.9, 0.95\}$, so after $k$ temperatures $T \le 0.95^k T_0$. The loop runs while $T \ge 0.005 / m$, so $0.95^{k} T_0 \ge 0.005 / m$ for every $k$ for which a temperature starts after the first, which bounds $k$ as stated. Each temperature and the final quench make a fixed number of moves, each of finite work. If $T_0 = 0$, the loop does not run. $\square$

None of this is about the quality of the result. With a finite schedule, simulated annealing gives no guarantee of an optimal placement; the convergence results for [simulated annealing](/simulated-annealing/) need a cooling schedule far slower than this one. How far from the optimum the placer ends on small instances is a measurement, reported on the page.

**Theorem 5.** The placer returns a legal placement, its accepted moves change $BB$ and $T$ by exactly the values it computes, and it stops.

*Proof.* Lemmas 1, 2 and 4. $\blacksquare$
