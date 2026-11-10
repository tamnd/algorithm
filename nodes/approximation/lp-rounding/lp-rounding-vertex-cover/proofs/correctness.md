---
title: Rounding the vertex cover LP at 1/2 gives a cover of weight at most twice the LP value
proves: [correctness]
status: full
---

**Statement.** Let $G = (V, E)$ be a graph with no self-loops and weights $w(v) \ge 0$. Let $x$ be a feasible solution of the vertex cover LP, that is, $x_u + x_v \ge 1$ for each edge $\{u, v\}$ and $x_v \ge 0$ for each $v$. Let $C = \{v \in V : x_v \ge 1/2\}$. Then:

1. $C$ is a vertex cover of $G$;
2. $w(C) \le 2 \sum_{v \in V} w(v) x_v$;
3. if $x$ is optimal, then $w(C) \le 2 \cdot \text{LP}^* \le 2 \cdot \text{OPT}$.

**Setup.** LP-ROUND-VC computes $x$ in line L1. The loop of lines L3 and L4 visits each vertex once and adds $v$ to $C$ exactly when $x_v \ge 1/2$, so after line L4 the set $C$ equals $\{v : x_v \ge 1/2\}$. Line L5 returns it.

**Step 1: $C$ is a cover.** Take an edge $\{u, v\}$. Assume, for a contradiction, that $u \notin C$ and $v \notin C$. Then $x_u < 1/2$ and $x_v < 1/2$, so $x_u + x_v < 1$. This contradicts the constraint of the edge. So $u \in C$ or $v \in C$. This holds for each edge, so $C$ is a vertex cover.

**Step 2: the weight bound.** For each $v \in C$, we have $x_v \ge 1/2$, so $2 x_v \ge 1$. Multiply by $w(v) \ge 0$: $w(v) \le 2 w(v) x_v$. Sum over $C$:

$$w(C) = \sum_{v \in C} w(v) \le \sum_{v \in C} 2 w(v) x_v \le \sum_{v \in V} 2 w(v) x_v.$$

The last step adds the terms $2 w(v) x_v$ for $v \notin C$, and each of them is at least 0 because $w(v) \ge 0$ and $x_v \ge 0$.

**Step 3: comparison with OPT.** If $x$ is optimal, then $\sum_v w(v) x_v = \text{LP}^*$, and step 2 gives $w(C) \le 2 \cdot \text{LP}^*$. Let $C^*$ be a minimum weight cover. Its indicator vector $\mathbf{1}_{C^*}$ satisfies $x_u + x_v \ge 1$ for each edge, because $C^*$ holds an endpoint of each edge, and it is nonnegative. So it is feasible for the LP, and $\text{LP}^* \le \sum_v w(v) [v \in C^*] = w(C^*) = \text{OPT}$. Hence $w(C) \le 2 \cdot \text{LP}^* \le 2 \cdot \text{OPT}$.

**Termination.** Line L1 is a call to an LP solver that halts. The loop of line L3 runs exactly $n$ times. So the algorithm halts. $\blacksquare$
