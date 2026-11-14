---
title: Cycle ratio iteration returns the least clock period of a skew schedule and stops
proves: [correctness, termination, round bound]
status: full
---

Registers are $1, \ldots, n$. Each path $p$ from register $i$ to register $j$ has delays $d_{\min}(p) \le d_{\max}(p)$, and $t_s$, $t_h$ are the setup and hold times. A schedule $c \in \mathbb{Q}^n$ and a period $T$ are *valid* when every path meets

$$ c_i - c_j \le T - d_{\max}(p) - t_s \quad \text{(setup)}, \qquad c_j - c_i \le d_{\min}(p) - t_h \quad \text{(hold)}. $$

The *constraint graph* $G$ has the registers as nodes, for each path a setup edge $j \to i$ of weight $T - d_{\max}(p) - t_s$, and a hold edge $i \to j$ of weight $d_{\min}(p) - t_h$. Each edge weight has the form $a T + b$ with $a \in \{0, 1\}$. For a cycle $C$ of $G$ let $k_C$ be its number of setup edges and $b_C$ the sum of the constants $b$, so its weight at period $T$ is $w_C(T) = k_C T + b_C$. Write $S_C = -b_C$.

**Lemma 1 (validity and cycles).** A period $T$ has a valid schedule if and only if $w_C(T) \ge 0$ for every simple cycle $C$ of $G$.

*Proof.* This is the theorem of [difference constraints](/difference-constraints/). If $c$ is valid, each edge $v \to u$ of weight $w$ has $c_u - c_v \le w$, and the sum around a cycle telescopes to $0 \le w_C(T)$. Conversely, if no cycle is negative, add a node $z$ with an edge of weight 0 to every register. No cycle through $z$ exists, so shortest path distances $\delta$ from $z$ are finite, and $\delta(u) \le \delta(v) + w$ for every edge, so $c = \delta$ is valid. A closed walk of negative weight contains a simple cycle of negative weight, so simple cycles suffice. $\square$

**Lemma 2 (the set of valid periods).** If some simple cycle $C$ has $k_C = 0$ and $S_C > 0$, no period is valid. Otherwise, and when there is at least one path, the valid periods are exactly the $T \ge T^*$ with
$$ T^* = \max \Big\{ \frac{S_C}{k_C} : C \text{ a simple cycle of } G,\ k_C \ge 1 \Big\}. $$

*Proof.* A cycle with $k_C = 0$ has weight $-S_C$ for every $T$, so the first case is clear by Lemma 1. In the other case the cycles with $k_C = 0$ never fail, and a cycle with $k_C \ge 1$ holds if and only if $T \ge S_C / k_C$. A path $p$ from $i$ to $j \ne i$ gives the 2-cycle of its two edges, with $k_C = 1$, and a path from $i$ to $i$ gives a setup loop with $k_C = 1$, so the maximum is over a nonempty finite set. $\square$

**Lemma 3 (the start is a lower bound).** Let $T_0 = \max_p (d_{\max}(p) - d_{\min}(p) + t_s + t_h)$. Then $T_0 \le T^*$.

*Proof.* Take a valid pair $(T^*, c)$ and a path $p$ from $i$ to $j$. Adding its setup and hold inequalities gives $0 \le T^* - d_{\max}(p) - t_s + d_{\min}(p) - t_h$. $\square$

**Lemma 4 (Bellman-Ford).** With all distances set to 0 at the start, [Bellman-Ford](/bellman-ford/) at a fixed $T$ either makes no change in some round among the first $n$, and then the distances form a valid schedule, or it changes a distance in round $n$, and then the walk back along the predecessor edges from that node reaches a simple cycle of negative weight.

*Proof.* The start with all distances 0 is the state after one round from the extra node $z$ of Lemma 1. A round with no change means every edge satisfies $\delta(u) \le \delta(v) + w$, which is validity. If no cycle is negative, every shortest path from $z$ has at most $n$ edges, so all distances are final after $n - 1$ more rounds and round $n$ makes no change. If round $n$ makes a change, the standard argument of [negative cycle detection](/negative-cycle-detection/) applies: the predecessor graph then holds a cycle, every cycle of the predecessor graph has negative weight, and walking back $n$ steps from a node changed in round $n$ ends on that cycle. $\square$

**Theorem 1 (correctness).** If the hold edges alone have a negative cycle, the algorithm returns that no period is valid, and this is true. Otherwise it returns $T^*$ and a valid schedule for $T^*$.

*Proof.* The first part is Lemma 2, since a cycle of hold edges has $k_C = 0$, and Lemma 4 run on the hold edges finds such a cycle when there is one (their weights do not depend on $T$). Now assume no such cycle. We show the invariant $T \le T^*$. It holds at the start by Lemma 3. Suppose Bellman-Ford finds a negative simple cycle $C$ at the current $T$. Then $k_C \ge 1$, since cycles with $k_C = 0$ are all hold cycles, which are not negative. So $k_C T - S_C < 0$, and the new period $T' = S_C / k_C$ satisfies $T < T' \le T^*$, the second by the definition of $T^*$. When Bellman-Ford finds no negative cycle, $T$ is valid with the schedule of Lemma 4, so $T \ge T^*$ by Lemma 2, and with the invariant $T = T^*$. Subtracting the smallest distance from all of them keeps every difference, so the shifted schedule is valid and has $\min c = 0$. $\square$

**Theorem 2 (termination).** The loop stops after at most as many rounds as $G$ has simple cycles, plus one.

*Proof.* In each round that does not stop, the period becomes $S_C / k_C$ for the cycle $C$ found, and it only grows later. So in every later round $w_C(T) \ge 0$, and $C$ is not found again. $G$ has finitely many simple cycles. $\square$

**Theorem 3 (round bound for integer data).** If all delays and the setup and hold times are integers, the number of rounds is at most $1 + n^2 (T^* - T_0)$, and each round takes $O(n m)$ time for $m$ paths.

*Proof.* Every period after the first is $S_C / k_C$ with $S_C$ an integer and $1 \le k_C \le n$, since a simple cycle has at most $n$ edges. Two distinct such values $a / k$ and $a' / k'$ differ by $|a k' - a' k| / (k k') \ge 1 / n^2$. The periods after the first round strictly increase and lie in $(T_0, T^*]$, so there are at most $n^2 (T^* - T_0)$ of them. Bellman-Ford does $n$ rounds over $2m$ edges. $\square$

**Corollary (no hold constraints).** If only the setup edges are present, every cycle consists of setup edges, so $k_C$ is its length and $T^*$ is the largest mean of $d_{\max}(p) + t_s$ over the cycles of paths. This is a maximum mean cycle, which [Karp's algorithm](/karp-minimum-mean-cycle/) finds in $O(n m)$ time after negating the weights.
