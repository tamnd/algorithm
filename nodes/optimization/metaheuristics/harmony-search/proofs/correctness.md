---
title: Harmony search keeps its memory in the box with values that never get worse, is a (μ+1) evolution strategy, and converges in value when HMCR < 1
proves: [correctness]
status: full
---

We use the pseudocode of the page for minimizing $f$ on the box $B = \prod_{j=1}^D [\ell_j, u_j]$ with $\ell_j < u_j$. Let $M_t$ be the memory after iteration $t$, with $M_0$ from line L1, and let $f^* = \min_B f$ when $f$ is continuous.

**Claim 1 (feasibility).** Every vector built in line L3 and every vector of every $M_t$ lies in $B$.

*Proof.* By induction on $t$. The vectors of $M_0$ are drawn in $B$. In iteration $t$, each coordinate $x_j$ is either a random draw in $[\ell_j, u_j]$, or a coordinate of a vector of $M_{t-1}$, which lies in $[\ell_j, u_j]$ by induction, possibly changed by a step and then clipped to $[\ell_j, u_j]$. So $x \in B$. $M_t$ consists of vectors of $M_{t-1}$ and possibly $x$. $\square$

**Claim 2 (monotone memory).** Let $v_{(1)}(t) \le \cdots \le v_{(H)}(t)$ be the sorted values of $f$ on $M_t$. Then $v_{(r)}(t) \le v_{(r)}(t - 1)$ for every $r$ and $t$. Line L6 returns a vector with the smallest value of $f$ among all vectors evaluated.

*Proof.* If line L5 does nothing, $M_t = M_{t-1}$. Otherwise it removes a vector with value $v_{(H)}(t - 1)$ and adds $x$ with $f(x) < v_{(H)}(t - 1)$. The remaining values are $v_{(1)}(t-1), \ldots, v_{(H-1)}(t-1)$. Adding $f(x)$ to them gives a sorted list whose $r$-th entry is at most $v_{(r)}(t-1)$ for $r \le H - 1$, since adding an element never raises an order statistic, and whose largest entry is $\max(v_{(H-1)}(t-1), f(x)) \le v_{(H)}(t-1)$. For the second statement: a rejected $x$ has $f(x) \ge v_{(H)}(t - 1) \ge v_{(1)}(t)$, and an accepted one is in $M_t$, so $v_{(1)}(t)$ is the smallest value seen up to iteration $t$. $\square$

**Claim 3 (equivalence with a $(\mu + 1)$-ES).** Consider the $(\mu + 1)$-ES with $\mu = H$ whose offspring is built, in each coordinate $j$ in order, as follows: with probability HMCR, take the coordinate $j$ of a uniform random parent (global discrete recombination) and then, with probability PAR, add $\text{bw} \cdot U(-1, 1)$ and clip (uniform mutation); otherwise draw the coordinate uniformly in $[\ell_j, u_j]$ (reset mutation). Its selection removes the worst of the $\mu$ parents and the offspring, the offspring on a tie, otherwise the same parent that line L4 picks, and keeps the others in place. If both methods start from the same population and use the same random numbers in the same order, they have the same population after every iteration.

*Proof.* By induction on $t$. Suppose that $M_{t-1}$ equals the ES population $P_{t-1}$, in the same order. The construction of line L3 and the construction of the offspring above read the same random numbers in the same order and apply the same rule to the same vectors, so $x$ equals the offspring. Line L5 keeps $M_{t-1}$ unchanged if $f(x) \ge f(w)$, and the ES then removes the offspring, since it is worst or tied with the worst. If $f(x) < f(w)$, line L5 puts $x$ in place of $w$, and the ES removes the same parent $w$, which is now the unique worst of the $\mu + 1$ individuals or the one picked by the shared tie rule, and puts the offspring in its place. In both cases $M_t = P_t$. $\square$

So the distributions of the two runs are the same as well, for every $f$, which is the sense in which HS is a special case of evolution strategies (Weyland 2010).

**Claim 4 (convergence in value).** Let $\text{HMCR} < 1$ and let $f$ be continuous on $B$. For every $\varepsilon > 0$ there is $q_\varepsilon > 0$ such that $P(v_{(1)}(t) \ge f^* + \varepsilon) \le (1 - q_\varepsilon)^t$.

*Proof.* Let $A = \{y \in B : f(y) < f^* + \varepsilon\}$. It contains a minimizer $y^*$ of $f$, and since $f$ is continuous, it contains $B \cap N$ for an open ball $N$ around $y^*$. Such a set has positive volume, so $\lambda(A) > 0$, where $\lambda$ is the volume. In each iteration, with probability $(1 - \text{HMCR})^D$ every coordinate of $x$ is a random draw, and then $x$ is uniform in $B$ and lies in $A$ with probability $\lambda(A)/\lambda(B)$. These draws do not depend on the past, so
$$q_\varepsilon = (1 - \text{HMCR})^D \, \frac{\lambda(A)}{\lambda(B)} > 0$$
is a lower bound on $P(x \in A)$ given any history. Suppose that $v_{(1)}(t - 1) \ge f^* + \varepsilon$. Then $f(w) \ge v_{(1)}(t - 1) \ge f^* + \varepsilon > f(x)$ whenever $x \in A$, so $x$ enters $M_t$ and $v_{(1)}(t) < f^* + \varepsilon$. By Claim 2, $v_{(1)}$ stays below $f^* + \varepsilon$ after that. With $E_t$ the event $v_{(1)}(t) \ge f^* + \varepsilon$, we get $P(E_t \mid E_{t-1}) \le 1 - q_\varepsilon$, and the chain rule gives the bound. $\square$

**Remark.** Claim 4 is the argument for pure random search, and $q_\varepsilon$ falls exponentially with $D$, so it gives no useful time bound. It does show that the reset mutation alone makes the method converge in value. With $\text{HMCR} = 1$, the claim can fail: if all memory vectors share the value $c$ in coordinate $j$ and $\text{PAR} = 0$, every later vector has $x_j = c$. $\blacksquare$
