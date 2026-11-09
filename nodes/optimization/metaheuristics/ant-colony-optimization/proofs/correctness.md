---
title: MMAS keeps its pheromone in bounds, keeps the shortest tour built so far, and builds an optimal tour with probability tending to 1
proves: [correctness]
status: full
---

We use the pseudocode of the page on a symmetric instance with $n \ge 3$ cities and $d_{ij} = d_{ji} > 0$. Let $L^*$ be the length of an optimal tour, and let $\eta_{\min}$ and $\eta_{\max}$ be the smallest and largest of the values $\eta_{ij} = 1/d_{ij}$. We assume $\alpha, \beta \ge 0$, $0 < \rho \le 1$ and $\tau_{\min} \le \tau_0 \le \tau_{\max}$. We write $\tau^{(t)}$ for the pheromone at the end of iteration $t$, and $\tau^{(0)}$ for the values of line L1. Lines L6 to L8 keep $\tau$ symmetric, because they treat $\tau_{ij}$ and $\tau_{ji}$ in the same way.

**Claim 1 (bounds).** For all $t \ge 0$ and all $i, j$, $\tau_{\min} \le \tau^{(t)}_{ij} \le \tau_{\max}$.

*Proof.* For $t = 0$ this is the assumption on $\tau_0$. For $t \ge 1$, line L8 is the last change in iteration $t$, and it sets each value to $\min(\tau_{\max}, \max(\tau_{\min}, x))$, which lies in $[\tau_{\min}, \tau_{\max}]$ for every real $x$. $\square$

**Claim 2 (bound without the clamp).** Let $\tau_{\min} = 0$ and $\tau_{\max} = \infty$, and let $M = \max(\tau_0, 1/(\rho L^*))$. Then $0 \le \tau^{(t)}_{ij} \le M$ for all $t$, $i$ and $j$.

*Proof.* By induction on $t$. For $t = 0$, $\tau^{(0)}_{ij} = \tau_0 \le M$. In iteration $t \ge 1$, line L6 multiplies each value by $1 - \rho \ge 0$, and line L7 adds $1/L(best)$ to an edge or adds nothing. The tour $best$ is a tour, so $L(best) \ge L^*$ and $1/L(best) \le 1/L^* \le \rho M$. Hence $0 \le \tau^{(t)}_{ij} \le (1 - \rho) M + \rho M = M$. $\square$

**Claim 3 (the best tour).** At the end of iteration $t$, $best$ is a shortest tour among all tours built in iterations $1$ to $t$. So $L(best)$ never increases.

*Proof.* By induction on $t$. Before iteration 1 no tour exists and $L(best) = \infty$. In iteration $t$, line L4 picks a shortest tour $ib$ of the iteration. Line L5 keeps the old $best$ if $L(best) \le L(ib)$ and takes $ib$ otherwise, so the new $L(best)$ is the minimum of the old one and $L(ib)$. $\square$

**Claim 4 (each iteration can build an optimal tour).** Let $\tau_{\min} > 0$, and let
$$q = \frac{\tau_{\min}^\alpha \, \eta_{\min}^\beta}{(n - 1)\, \tau_{\max}^\alpha \, \eta_{\max}^\beta}, \qquad p_{\min} = q^{n-1}.$$
Then $p_{\min} > 0$, and in every iteration, given everything that happened before it, each ant builds an optimal tour with probability at least $p_{\min}$.

*Proof.* At the start of iteration $t$, the pheromone is $\tau^{(t-1)}$, and by Claim 1 all its values lie in $[\tau_{\min}, \tau_{\max}]$. Fix an optimal tour $s^*$. Let an ant start at city $c$. The tour $s^*$ passes through $c$, so there is an order $c = c_1, c_2, \ldots, c_n$ of the cities that follows $s^*$. The ant builds this order exactly when, for $k = 1, \ldots, n - 1$, its $k$-th move goes from $c_k$ to $c_{k+1}$. At that move the set $U$ of unvisited cities contains $c_{k+1}$ and has at most $n - 1$ elements. Each weight $\tau_{il}^\alpha \eta_{il}^\beta$ lies between $\tau_{\min}^\alpha \eta_{\min}^\beta$ and $\tau_{\max}^\alpha \eta_{\max}^\beta$, because $\alpha, \beta \ge 0$. So the probability of the move is at least
$$\frac{\tau_{\min}^\alpha \eta_{\min}^\beta}{|U| \, \tau_{\max}^\alpha \eta_{\max}^\beta} \ge q.$$
The moves are made one after the other, so the probability of all $n - 1$ moves is the product of the conditional probabilities, which is at least $q^{n-1} = p_{\min}$. This holds for every start city $c$, so it holds for the uniform random start. All factors in $q$ are positive, so $p_{\min} > 0$. $\square$

**Claim 5 (convergence in value).** Let $\tau_{\min} > 0$. The probability that no optimal tour has been built in iterations $1$ to $t$ is at most $(1 - p_{\min})^t$. Hence $L(best) = L^*$ from some iteration on, with probability 1.

*Proof.* Let $A_k$ be the event that iteration $k$ builds no optimal tour. By Claim 4, the first ant of iteration $k$ builds an optimal tour with probability at least $p_{\min}$, given any history of iterations $1$ to $k - 1$. So $P(A_k \mid A_1, \ldots, A_{k-1}) \le 1 - p_{\min}$ whenever the condition has positive probability. By the chain rule,
$$P(A_1 \cap \cdots \cap A_t) = \prod_{k=1}^t P(A_k \mid A_1 \cap \cdots \cap A_{k-1}) \le (1 - p_{\min})^t.$$
This tends to 0. By Claim 3, once an optimal tour has been built, $L(best) = L^*$ in all later iterations. The events "no optimal tour by iteration $t$" decrease in $t$, so the probability that no optimal tour is ever built is the limit, 0. $\square$

**Claim 6 (the pheromone after the optimum is found).** Let $t_0$ be an iteration with $L(best) = L^*$ at its end, and let $\tau_{\min} > 0$. Let $c = 1/(\rho L^*)$ and $x^* = \min(\tau_{\max}, \max(\tau_{\min}, c))$. Then $best$ does not change after $t_0$, and for $t \ge t_0$:

1. each edge of $best$ satisfies $|\tau^{(t)}_{ij} - x^*| \le (1 - \rho)^{t - t_0} \, |\tau^{(t_0)}_{ij} - x^*|$, so it converges to $x^*$;
2. each other edge satisfies $\tau^{(t)}_{ij} = \tau_{\min}$ for all $t \ge t_0 + K$, where $K$ is the smallest integer $k \ge 0$ with $(1 - \rho)^k \tau_{\max} \le \tau_{\min}$.

*Proof.* Line L5 changes $best$ only to a strictly shorter tour, and no tour is shorter than $L^*$, so $best$ is fixed after $t_0$. Let $\pi(x) = \min(\tau_{\max}, \max(\tau_{\min}, x))$, the projection onto $[\tau_{\min}, \tau_{\max}]$. It satisfies $|\pi(x) - \pi(y)| \le |x - y|$.

For an edge of $best$, lines L6 to L8 give $\tau^{(t)}_{ij} = h(\tau^{(t-1)}_{ij})$ with $h(x) = \pi((1 - \rho) x + \rho c)$, since $1/L^* = \rho c$. Then $|h(x) - h(y)| \le (1 - \rho)|x - y|$. The point $x^*$ is a fixed point of $h$. If $\tau_{\min} \le c \le \tau_{\max}$, then $x^* = c$ and $h(c) = \pi(c) = c$. If $c > \tau_{\max}$, then $x^* = \tau_{\max}$ and $(1 - \rho)\tau_{\max} + \rho c > \tau_{\max}$, so $h(\tau_{\max}) = \tau_{\max}$. If $c < \tau_{\min}$, then $x^* = \tau_{\min}$ and $(1 - \rho)\tau_{\min} + \rho c < \tau_{\min}$, so $h(\tau_{\min}) = \tau_{\min}$. Hence $|\tau^{(t)}_{ij} - x^*| = |h(\tau^{(t-1)}_{ij}) - h(x^*)| \le (1 - \rho)|\tau^{(t-1)}_{ij} - x^*|$, and part 1 follows by induction.

For an edge not in $best$, line L7 adds nothing, so $\tau^{(t)}_{ij} = \max(\tau_{\min}, (1 - \rho)\tau^{(t-1)}_{ij})$. The value starts at most $\tau_{\max}$ by Claim 1. By induction, $\tau^{(t_0 + k)}_{ij} = \max(\tau_{\min}, (1 - \rho)^k \tau^{(t_0)}_{ij}) \le \max(\tau_{\min}, (1 - \rho)^k \tau_{\max})$. For $k \ge K$ the second term is at most $\tau_{\min}$, so the value equals $\tau_{\min}$. $K$ is finite: if $\rho = 1$ then $K \le 1$, and if $\rho < 1$ then $(1 - \rho)^k \to 0$. $\square$

**Remarks.** Claim 5 is the convergence in value of Stützle and Dorigo (2002). It does not say that the probability of building an optimal tour in one iteration tends to 1. With a fixed $\tau_{\min} > 0$, Claim 6 shows that the pheromone tends to a fixed matrix, and under that matrix each ant still builds a non-optimal tour with positive probability. Gutjahr (2000, 2002) proved that this probability tends to 1 for variants in which $\tau_{\min}$ or $\rho$ goes to 0 slowly with time. The bound $p_{\min}$ is very small for large $n$, so Claim 5 gives no practical bound on the running time. $\blacksquare$
