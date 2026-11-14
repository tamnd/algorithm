---
title: The fixed-dissection linear program gives min-variation fill, and fixed windows bound floating windows
proves: [correctness]
status: full
---

**Setting.** The layout is $R = [0, n]^2$ with features $F$, a finite union of rectangles. A tile side $t > 0$ divides $n$, so $R$ is cut into an $m \times m$ grid of tiles $T_{ij}$ with $m = n/t$. For an integer $r \ge 1$ with $rt \le n$, let $w = rt$. A *fixed window* is a block of $r \times r$ tiles; a *floating window* is any square $x + [0, w]^2 \subseteq R$. Tile $T_{ij}$ has feature area $a_{ij}$ and slack $s_{ij} \ge 0$. For a fill amount $p = (p_{ij})$ and a fixed window $W$, write $a(W) = \sum_{T_{ij} \subseteq W} a_{ij}$, $p(W) = \sum_{T_{ij} \subseteq W} p_{ij}$, and $D_p(W) = (a(W) + p(W))/w^2$.

**Continuous model.** A fill is a choice of $p_{ij} \in [0, s_{ij}]$ for every tile, and its fill shapes in $T_{ij}$ have total area $p_{ij}$ and lie in $T_{ij}$. The fixed problem is: maximize $\min_W D_p(W)$ over fills with $\max_W D_p(W) \le U$, the minimum and maximum over fixed windows.

**Lemma 1 (density of a fixed window).** For any fill, the density of a fixed window $W$ is $D_p(W)$.

*Proof.* $W$ is the union of its $r^2$ tiles, which meet only on their boundaries, of area zero. Fill shapes in a tile lie in that tile and do not overlap features, since they lie in the slack. So the area of features and fill in $W$ is $\sum_{T_{ij} \subseteq W} (a_{ij} + p_{ij}) = a(W) + p(W)$. $\square$

**Theorem 1 (the linear program is the fixed problem).** Consider the program of lines L3 to L6: variables $p_{ij} \ge 0$ and $M \ge 0$, maximize $M$ subject to $p_{ij} \le s_{ij}$, $p(W) \le U w^2 - a(W)$ and $M - p(W) \le a(W)$ for every fixed window $W$. If $a(W) \le U w^2$ for every $W$, the program has an optimal solution $(p^*, M^*)$, the optimum of the fixed problem is $M^*/w^2$, and $p^*$ is an optimal fill. If $a(W) > U w^2$ for some $W$, the fixed problem has no feasible fill.

*Proof.* Infeasible case: every fill has $p(W) \ge 0$, so $D_p(W) \ge a(W)/w^2 > U$.

Feasible case. *Feasibility.* The origin $p = 0$, $M = 0$ satisfies all constraints, since the right-hand sides $s_{ij}$, $U w^2 - a(W)$ and $a(W)$ are all nonnegative. *Boundedness.* For any window $W_0$, $M \le a(W_0) + p(W_0) \le a(W_0) + \sum s_{ij}$. A feasible bounded linear program has an optimal solution, by the fundamental theorem of linear programming.

*From fills to program points.* Let $p$ be a fill feasible for the fixed problem and let $M = \min_W (a(W) + p(W))$. Then $0 \le p_{ij} \le s_{ij}$, $a(W) + p(W) \le U w^2$ by Lemma 1, and $M \le a(W) + p(W)$ for every $W$, with $M \ge 0$. So $(p, M)$ is feasible with objective $w^2 \min_W D_p(W)$. Hence the program optimum $M^*$ is at least $w^2$ times the fixed optimum.

*From program points to fills.* Let $(p, M)$ be feasible. Then $p$ is a fill with $D_p(W) \le U$ for all $W$, and $M \le a(W) + p(W)$ for all $W$ gives $\min_W D_p(W) \ge M/w^2$. So the fixed optimum is at least $M^*/w^2$, and $p^*$ attains it. $\square$

**Lemma 2 (overlap of shifted squares).** Let $Q = [x, x + w] \times [y, y + w]$ and $Q' = [x', x' + w] \times [y', y' + w]$ with $|x - x'| \le \delta$ and $|y - y'| \le \delta$, where $0 \le \delta \le w$. Then $\operatorname{area}(Q \setminus Q') = \operatorname{area}(Q' \setminus Q) \le w^2 - (w - \delta)^2$.

*Proof.* $Q \cap Q'$ is the rectangle of sides $w - |x - x'|$ and $w - |y - y'|$, both at least $w - \delta \ge 0$. So $\operatorname{area}(Q \cap Q') \ge (w - \delta)^2$, and both differences have area $w^2 - \operatorname{area}(Q \cap Q')$. $\square$

**Theorem 2 (floating windows, Kahng et al. 1998, Theorem 8).** Let $G \subseteq R$ be any measurable set (features and fill together), and suppose every fixed window $W$ has $\operatorname{area}(G \cap W)/w^2 \in [L, U]$. Then every floating window $Q$ has

$$ L - \varepsilon_r \le \frac{\operatorname{area}(G \cap Q)}{w^2} \le U + \varepsilon_r, \qquad \varepsilon_r = \frac{1}{r} - \frac{1}{4r^2}. $$

*Proof.* Let $Q = (x, y) + [0, w]^2 \subseteq R$, so $x, y \in [0, n - w]$. Let $x'$ be a multiple of $t$ nearest to $x$, and $y'$ likewise. Since $0$ and $n - w = (m - r)t$ are multiples of $t$, the rounding stays in $[0, n - w]$, so $Q' = (x', y') + [0, w]^2$ is a fixed window, and $|x - x'|, |y - y'| \le t/2$. By Lemma 2 with $\delta = t/2 = w/(2r)$,

$$ \operatorname{area}(Q \setminus Q') \le w^2 - \Big(w - \frac{w}{2r}\Big)^2 = w^2 \Big(\frac{1}{r} - \frac{1}{4r^2}\Big) = w^2 \varepsilon_r. $$

Then $\operatorname{area}(G \cap Q) \le \operatorname{area}(G \cap Q') + \operatorname{area}(Q \setminus Q') \le U w^2 + \varepsilon_r w^2$, and $\operatorname{area}(G \cap Q) \ge \operatorname{area}(G \cap Q') - \operatorname{area}(Q' \setminus Q) \ge L w^2 - \varepsilon_r w^2$. Divide by $w^2$. $\square$

**Proposition 3 (the bounds are attained).** Suppose $n \ge w + t$. Let $G = (t/2, t/2) + [0, w]^2$. The floating window $G$ has density $1$, and every fixed window has density at most $(1 - \frac{1}{2r})^2 = 1 - \varepsilon_r$. For the complement $R \setminus G$, the window $G$ has density $0$ and every fixed window has density at least $\varepsilon_r$.

*Proof.* A fixed window $Q' = (it, jt) + [0, w]^2$ meets $G$ in a rectangle whose sides are $w - |it - t/2|$ and $w - |jt - t/2|$ (or zero). Since $i$ is an integer, $|it - t/2| \ge t/2$, so each side is at most $w - t/2$, and the density is at most $(w - t/2)^2/w^2 = (1 - \frac{1}{2r})^2$. For $i = j = 0$ the bound holds with equality. For the complement, the density of each fixed window is $1$ minus its density for $G$, so it is at least $1 - (1 - \frac{1}{2r})^2 = \varepsilon_r$. $\square$

So with $U = 1 - \varepsilon_r$ the upper bound of Theorem 2 is reached, and with $L = \varepsilon_r$ the lower bound is. Kahng et al. state that the bounds are tight; this proposition shows it for one value of $U$ and one of $L$ for every $r$.

**Corollary 4 (quality of the LP fill for floating windows).** Let $M^*$ be the program optimum and $p^*$ the LP fill. Let $\mathrm{OPT}$ be the largest minimum floating-window density over fills with every floating-window density at most $U$. Then with $p^*$ every floating window has density in $[M^*/w^2 - \varepsilon_r, U + \varepsilon_r]$, and $M^*/w^2 \ge \mathrm{OPT}$.

*Proof.* With $p^*$, every fixed window has density in $[M^*/w^2, U]$ by Theorem 1, and Theorem 2 gives the first claim. Fixed windows are floating windows, so a fill that meets $U$ on all floating windows meets it on all fixed windows, and its minimum over fixed windows is at least its minimum over floating windows. So it is feasible for the fixed problem with value at least its floating value, and Theorem 1 gives $M^*/w^2 \ge \mathrm{OPT}$. $\square$

So the LP fill reaches a floating minimum within $\varepsilon_r$ of the floating optimum, and exceeds the floating bound $U$ by at most $\varepsilon_r$. Running the program with $U - \varepsilon_r$ in place of $U$ removes the excess, at the cost of a lower optimum.

**About the solver.** Line L7 uses the simplex method with Bland's rule, which terminates with an optimal basic solution on a feasible bounded program (Bland, 1977); this is cited, not proved here. The implementation also returns the dual vector $y$ from the final tableau. For any $x \ge 0$ with $Ax \le b$ and $y \ge 0$ with $A^{\mathsf T} y \ge c$, weak duality gives $c^{\mathsf T} x \le y^{\mathsf T} A x \le y^{\mathsf T} b$, so equality $c^{\mathsf T} x = b^{\mathsf T} y$ proves that $x$ is optimal. The tests check exactly these conditions in exact arithmetic, so each tested optimum is certified independently of the pivoting.
