---
tag: THRRQW
kind: theorem
slug: rrt-star-asymptotic-optimality
name: Asymptotic optimality of RRT*
aliases:
- Karaman-Frazzoli optimality
area: games-and-search/planning
level: research
summary: RRT* converges to the optimal cost if the near radius is large enough. The 2011 proof has a gap, and Solovey et al. (2020) proved it with the exponent 1/(d+1).
prereqs: [rrt-star, random-geometric-graph]
see_also: [rapidly-exploring-random-tree, probabilistic-roadmap, motion-planning, kinodynamic-planning, union-bound, markov-inequality, poisson-distribution, binomial-distribution]
sources:
  - paper: doi:10.1177/0278364911406761
    title: Sertac Karaman and Emilio Frazzoli, Sampling-based algorithms for optimal motion planning, International Journal of Robotics Research 30(7), 2011
    locator: pages 846 to 894. Numbering of arXiv:1105.1186. Section 2.1 (Problems 2 and 3, the cost function), Section 3.1 (SampleFree), Algorithm 6 (RRT*), Definition 24 and Lemma 25 (asymptotic optimality, zero-one law), Assumption 27 and Lemma 28, Theorems 31 to 39, Lemma 42, Appendix G (proof of Theorem 38, Lemmas 71 and 72)
  - paper: doi:10.1109/ICRA40945.2020.9196553
    title: Kiril Solovey, Lucas Janson, Edward Schmerling, Emilio Frazzoli and Marco Pavone, Revisiting the asymptotic optimality of RRT*, Proceedings of the IEEE International Conference on Robotics and Automation, 2020
    locator: pages 2189 to 2195. Numbering of arXiv:1909.09688v2. Definitions 2 and 3 (robust paths, robust optimum), Section III-B (the logical gap), Theorem 1, Lemmas 1 to 4, Claim 1, Remark 2, and Section V (the open question on the exponent 1/d)
  - paper: "Sertac Karaman and Emilio Frazzoli, Incremental sampling-based algorithms for optimal motion planning, arXiv:1005.0416, 2010, short version at Robotics: Science and Systems 2010"
    locator: the first statement of RRT* and of its asymptotic optimality
  - paper: doi:10.1109/LRA.2018.2888947
    title: Michal Kleinbort, Kiril Solovey, Zakary Littlefield, Kostas E. Bekris and Dan Halperin, Probabilistic completeness of RRT for geometric and kinodynamic planning with forward propagation, IEEE Robotics and Automation Letters 4(2), 2019
    locator: Theorem 1 (the geometric RRT covers a chain of balls along a path with clearance, with probability exponentially close to 1), used in Lemma 1 of Solovey et al.
  - paper: "Lucas Janson, Edward Schmerling, Ashley Clark and Marco Pavone, Fast marching tree, a fast marching sampling-based method for optimal motion planning in many dimensions, International Journal of Robotics Research 34(7), 2015, 883-921"
    locator: the proof of asymptotic optimality of FMT*, which the proof of Solovey et al. follows
---

The asymptotic optimality theorem for [RRT\*](/rrt-star/) states that the cost $Y_n$ of the best path in the RRT\* tree after $n$ iterations converges to the optimal cost $c^*$ as $n \to \infty$, if the problem has a robust optimal path and the near radius shrinks slowly enough. Karaman and Frazzoli stated it in 2011 for the radius $\gamma (\log n / n)^{1/d}$, with convergence with probability 1 (Theorem 38). In 2020, Solovey, Janson, Schmerling, Frazzoli and Pavone found a gap in that proof. They gave a new proof for the larger radius $\gamma (\log n / n)^{1/(d+1)}$, with convergence in probability to within any factor $1 + \varepsilon$. It is open whether the exponent $1/d$ is enough.

## Statement

**The setting of Karaman and Frazzoli.** The space is $\mathcal{X} = (0, 1)^d$ with $d \ge 2$. The obstacle set $\mathcal{X}_{obs}$ is such that $\mathcal{X} \setminus \mathcal{X}_{obs}$ is open, and $\mathcal{X}_{free}$ is the closure of $\mathcal{X} \setminus \mathcal{X}_{obs}$. The start $x_{init}$ is in $\mathcal{X}_{free}$, and the goal region $\mathcal{X}_{goal}$ is an open subset of $\mathcal{X}_{free}$. A path is a continuous map $\sigma : [0, 1] \to \mathbb{R}^d$ of bounded variation, and it is feasible if it stays in $\mathcal{X}_{free}$, starts at $x_{init}$ and ends in the closure of $\mathcal{X}_{goal}$. Paths are compared in the norm $\lVert \sigma \rVert_{BV} = \int_0^1 \lVert \sigma(\tau) \rVert \, d\tau + \mathrm{TV}(\sigma)$, where $\mathrm{TV}$ is the total variation, the length of the path.

**The cost.** The cost $c$ maps paths to $\mathbb{R}_{\ge 0}$. It is $0$ only on constant paths, and it is *monotone*, $c(\sigma_1) \le c(\sigma_1 \mid \sigma_2)$ for a concatenation, and *bounded*, $c(\sigma) \le k_c \, \mathrm{TV}(\sigma)$ for a constant $k_c$. The algorithm is stated for an additive cost, such as the length, but the analysis does not need this.

**Clearance and robustness.** A path has *strong $\delta$-clearance* if every point of it is the center of a ball of radius $\delta$ inside $\mathcal{X}_{free}$. A free path $\sigma$ has *weak $\delta$-clearance* if a homotopy $\psi$ in the free paths joins $\psi(0) = \sigma$ to a path $\psi(1)$ with strong $\delta$-clearance, such that each $\psi(\alpha)$ with $\alpha > 0$ has strong $\delta_\alpha$-clearance for some $\delta_\alpha > 0$. A path $\sigma^*$ is a *robustly optimal solution* if it is an optimal feasible path, it has weak $\delta$-clearance for some $\delta > 0$, and $c(\sigma_n) \to c(\sigma^*)$ for every sequence of free paths with $\lVert \sigma_n - \sigma^* \rVert_{BV} \to 0$.

**The algorithm.** RRT\* draws i.i.d. uniform samples from $\mathcal{X}_{free}$ (the procedure SampleFree), steers by at most $\eta > 0$, and takes as near vertices those within $\min\{\gamma (\log |V| / |V|)^{1/d}, \eta\}$ of the new vertex, where $|V|$ is the current number of vertices and $\log$ is natural. Let $Y_n$ be the cost of the best path from $x_{init}$ into $\mathcal{X}_{goal}$ in the tree after $n$ iterations, with $Y_n = \infty$ if there is none. Write $\mu$ for the Lebesgue measure and $\zeta_d$ for the volume of the unit ball in $\mathbb{R}^d$.

**Definition 24 (asymptotic optimality).** An algorithm is asymptotically optimal if for every problem $(\mathcal{X}_{free}, x_{init}, \mathcal{X}_{goal})$ and cost $c$ that admit a robustly optimal solution with finite cost $c^*$,

$$\Pr\left[ \limsup_{n \to \infty} Y_n = c^* \right] = 1.$$

**Theorem 38 (Karaman and Frazzoli, 2011).** If

$$\gamma > \left( 2 \left( 1 + \frac{1}{d} \right) \right)^{1/d} \left( \frac{\mu(\mathcal{X}_{free})}{\zeta_d} \right)^{1/d},$$

then RRT\* is asymptotically optimal.

**The setting of Solovey et al.** The space is $\mathcal{C} = [0, 1]^d$ with $d \ge 2$, the free space is $\mathcal{F}$, the start is $s$ and the target is a single point $t$. The cost is the length. A path $\sigma$ from $s$ to $t$ in $\mathcal{F}$ is *robust* if $B_\delta(\sigma) \subset \mathcal{F}$ for some $\delta > 0$, where $B_\delta(\sigma)$ is the union of the balls of radius $\delta$ centered on $\sigma$. The problem is *robustly feasible* if a robust path exists, and the *robust optimum* is $c^* = \inf \{ c(\sigma) : \sigma \text{ robust} \}$. The authors note that these definitions are slightly different from those of Karaman and Frazzoli, and that the gap does not depend on this difference. The near radius is $\min\{r(|V|), \eta\}$.

**Theorem 1 (Solovey, Janson, Schmerling, Frazzoli and Pavone, 2020).** Let $(\mathcal{F}, s, t)$ be robustly feasible, and fix $\eta > 0$, $\varepsilon \in (0, 1)$, $\theta \in (0, 1/4)$ and $\mu \in (0, 1)$. Let $r(n) = \gamma (\log n / n)^{1/(d+1)}$ with

$$\gamma \ge (2 + \theta) \left( \frac{(1 + \varepsilon/4) \, c^*}{(d + 1) \, \theta \, (1 - \mu)} \cdot \frac{|\mathcal{F}|}{\zeta_d} \right)^{1/(d+1)}.$$

Let $\sigma_n$ be the path that RRT\* returns after $n$ iterations, with cost $\infty$ if there is none. Then $\lim_{n \to \infty} \Pr[c(\sigma_n) \le (1 + \varepsilon) c^*] = 1$.

Here $\mu$ is a parameter of the proof, not the measure, and $|\mathcal{F}|$ is the volume of $\mathcal{F}$.

## In plain words

RRT\* grows a tree of straight pieces from the start. Each new point picks the best parent among the points in a small circle around it, and it can give a better route to its neighbors. The theorem says that if the circle is not too small, the best route in the tree gets as close as you like to the shortest route, as the number of points grows.

The circle must shrink, or the work per point grows. If it shrinks too fast, the tree misses the narrow places of the best route. The question is the right speed.

The first proof checked that each pair of neighbor regions along the best route gets points in a good order. But the tree needs one chain of points, in order, through all regions. The new proof gives each region its own window of time, which costs a slightly larger circle.

## Proof

The proof below follows the two papers. Parts 1 and 4 are complete arguments. Part 2 gives the structure of the original proof, and part 3 the gap.

**Part 1. Facts that both proofs use.**

*(a) $Y_n$ is non-increasing.* Costs in the tree never increase, and the set of goal vertices only grows, by Lemma 3 of the [RRT\* correctness proof](/rrt-star/proofs/correctness/). So $\lim_n Y_n$ exists in $[0, \infty]$ for every run. In the setting of Karaman and Frazzoli, $Y_n \ge c^*$, because every path in the tree is feasible and $c^*$ is the optimal cost. So asymptotic optimality means $\lim_n Y_n = c^*$ with probability 1, and Lemma 25 shows by the Kolmogorov zero-one law that, given that a solution is found, this event has probability 0 or 1.

*(b) The radius at the current size is at least the radius at the final size.* The tree has $|V| \le n + 1$ vertices after $n$ iterations, and $x \mapsto \log x / x$ decreases for $x \ge e$. So, up to the shift by one, $r(|V|) \ge r(n)$ in every iteration up to $n$, and both proofs use $r(n)$ as a lower bound for the radius of every iteration up to $n$.

*(c) A path with positive clearance near the optimum.* Lemma 50 of Karaman and Frazzoli: if $\sigma^*$ has weak $\delta$-clearance and $\delta_n \to 0$ with $0 \le \delta_n \le \delta$, there are paths $\sigma_n$ with strong $\delta_n$-clearance and $\lVert \sigma_n - \sigma^* \rVert_{BV} \to 0$. The proof moves along the homotopy $\psi$ to the largest $\alpha_n$ such that $\psi(\alpha_n)$ stays in the closure of the $\delta_n$-interior, and shows $\alpha_n \to 0$. By robustness, $c(\sigma_n) \to c^*$. So it is enough to show that the tree contains paths that converge to $\sigma_n$ in the BV norm.

*(d) The same vertices as the RRT.* On the same random points, RRT\* and the [RRT](/rapidly-exploring-random-tree/) have the same vertex set (Lemma 4 of the RRT\* correctness proof). Results on the vertices of the RRT carry over.

**Part 2. The proof of Karaman and Frazzoli (Appendix G).** It assumes $\eta \ge \mathrm{diam}(\mathcal{X})$ for simplicity and says that the result holds for every $\eta > 0$.

*A marked point process.* Let $X_1, \dots, X_n$ be i.i.d. uniform in $\mathcal{X}_{free}$, each with an independent uniform mark $Y_i \in [0, 1]$ that gives its place in the order of insertion, and give $x_{init}$ the mark $0$. Let $G_n$ have a directed edge from $X_{i'}$ to $X_i$ when $Y_{i'} < Y_i$ and $\lVert X_i - X_{i'} \rVert \le r_n$, with $r_n = \gamma (\log n / n)^{1/d}$. This graph has no directed cycle. The subgraph $G'_n$ keeps for each vertex only its best parent. The proof states that $G'_n$ is equivalent to the RRT\* tree when $\eta$ is large, and that the best costs in $G_n$ and $G'_n$ have the same $\limsup$.

*Balls along the path.* Put $\delta_n = \min\{\delta, 4 r_n\}$, take $\sigma_n$ from part 1(c), and cover $\sigma_n$ with $M_n$ balls $B_{n, 1}, \dots, B_{n, M_n}$ of radius $r_n$ centered on $\sigma_n$, with consecutive centers $2 r_n$ apart. Let $A_{n, m}$ be the event that there are points $X_i \in B_{n, m}$ and $X_{i'} \in B_{n, m+1}$ with $Y_{i'} \le Y_i$, and $A_n = \bigcap_m A_{n, m}$.

*Lemma 71: $A_n$ holds for all large $n$, with probability 1.* The proof Poissonizes: with $\mathrm{Poisson}(\rho n)$ points for a constant $\rho \in (0, 1)$, the point process is Poisson, counts in disjoint balls are independent, and $\Pr[\mathrm{Poisson}(\rho n) > n] \le e^{-a n}$ for a constant $a > 0$. The number $N_{n, m}$ of points in $B_{n, m}$ has mean $n \zeta_d r_n^d / \mu(\mathcal{X}_{free}) = \alpha \log n$ with

$$\alpha = \frac{\zeta_d \gamma^d}{\mu(\mathcal{X}_{free})}.$$

A large deviation bound gives $\Pr[N_{n, m} < (1 - \epsilon) \alpha \log n] \le n^{-\alpha H(\epsilon)}$, with $H(\epsilon) = \epsilon + (1 - \epsilon) \log(1 - \epsilon)$, which tends to 1 as $\epsilon \to 1$. If each of the two balls has $k$ points, $A_{n, m}$ fails only if every mark in $B_{n, m+1}$ is larger than every mark in $B_{n, m}$, and the chance of that is $(k!)^2 / (2k)! = 1 / \binom{2k}{k} \le 2^{-k}$. With a suitable $\epsilon$, these bounds give $\Pr[A^c_{n, m}] \le 3 n^{-\alpha/2} + e^{-a n}$. The number of balls is $M_n \le b (n / \log n)^{1/d}$ for a constant $b$, so by the [union bound](/union-bound/)

$$\Pr[A_n^c] \le b \left( \frac{n}{\log n} \right)^{1/d} \left( 3 n^{-\alpha/2} + e^{-a n} \right).$$

The sum over $n$ is finite when $\alpha / 2 - 1/d > 1$, that is, $\alpha > 2(1 + 1/d)$, which is the hypothesis of Theorem 38 on $\gamma$. The Borel-Cantelli lemma then shows that $A_n^c$ occurs only finitely often.

*Lemma 72 and the end.* Let $\sigma'_n$ be the path in the tree closest to $\sigma_n$ in the BV norm. Lemma 72 states that $\lVert \sigma'_n - \sigma_n \rVert_{BV} \to 0$ with probability 1. Its proof is omitted in the paper, as "similar to that of Lemma 55", the corresponding lemma for PRM\*. Then $\sigma'_n \to \sigma^*$, and robustness gives $c(\sigma'_n) \to c^*$.

*Two points to note in the printed text.* Lemma 71 is stated with the hypothesis $\gamma > 4 (\mu(\mathcal{X}_{free}) / \zeta_d)^{1/d}$, while its proof uses only $\alpha > 2(1 + 1/d)$, the constant of Theorem 38. For $\mu(\mathcal{X}_{free}) = 1$ the first is $2.2568$, $2.4814$ and $3.0421$ for $d = 2, 3, 6$, and the second is $0.9772$, $0.8603$ and $0.8759$. Also, the balls have radius $r_n$ and centers $2 r_n$ apart, so two points in consecutive balls can be up to $4 r_n$ apart, more than the connection radius $r_n$. The text states that such points are joined by an edge without a further argument.

**Part 3. The gap (Solovey et al., Section III-B).** The argument shows that for each $m$ there is *a pair* of points in $B_{n, m}$ and $B_{n, m+1}$ in a good order. It does not show that there is *one chain* $X_{j_1}, X_{j_2}, \dots, X_{j_{M_n}}$ with $X_{j_i} \in B_{n, i}$ and $j_1 \le j_2 \le \dots \le j_{M_n}$, which is what a path in the tree through all the balls needs. The pairs for $m$ and $m + 1$ can use two different points of $B_{n, m+1}$. Solovey et al. give an example in which the order of the samples makes RRT\* wire a long chain of such points in the direction opposite to the path. RRT\* rewires only locally: a vertex changes its parent only when a new sample lands near it. So the chain is reversed only if new samples arrive along it in the right order, and the argument above does not show that this happens.

Remark 2 of Solovey et al. points out a second issue: the proof treats the vertices of RRT\* as uniform samples, which they are not, because of STEER, and setting $\eta = \infty$ does not solve this. One way to see the last point: with $\eta$ large, $x_{new}$ is the uniform sample, but it becomes a vertex only if the segment from its nearest vertex is free, which depends on the earlier vertices.

**Part 4. The proof of Solovey et al.** Fix $\varepsilon, \theta, \mu, \eta$ as in Theorem 1. By robust feasibility, there is a robust path $\sigma_\varepsilon$ from $s$ to $t$ and a $\delta > 0$ with $c(\sigma_\varepsilon) \le (1 + \varepsilon/4) c^*$ and $B_\delta(\sigma_\varepsilon) \subset \mathcal{F}$. Write $r = r(n)$.

*Balls and time windows.* Let $M_n = \lceil c(\sigma_\varepsilon) (2 + \theta) / (\theta r) \rceil$, and pick points $x_1 = s, x_2, \dots, x_{M_n} = t$ on $\sigma_\varepsilon$ with $\lVert x_i - x_{i-1} \rVert \le \theta r / (2 + \theta)$. Let $B_{n, i}$ be the ball of radius $r / (2 + \theta)$ around $x_i$. Let $n_0 = \mu n$. The first window $T_0$ is the iterations $1, \dots, n_0$, and the rest are cut into $M_n$ consecutive windows $T_1, \dots, T_{M_n}$ of $(n - n_0) / M_n$ iterations each. Let $V_i$ be the vertices added in window $T_i$. The windows are the new idea: a vertex of $V_i$ is always added before a vertex of $V_{i+1}$.

*Claim 1 (consecutive balls are within the radius).* For $x \in B_{n, i}$ and $x' \in B_{n, i+1}$,

$$\lVert x - x' \rVert \le \frac{r}{2 + \theta} + \frac{\theta r}{2 + \theta} + \frac{r}{2 + \theta} = r.$$

So if $X_{j_i} \in V_i \cap B_{n, i}$ and $X_{j_{i+1}} \in V_{i+1} \cap B_{n, i+1}$ is the new vertex of iteration $j_{i+1}$, then $X_{j_i}$ is a near vertex by part 1(b). For $n$ large, $r < \delta$ and $\eta$, so both balls lie in $B_\delta(\sigma_\varepsilon)$, the segment is free, and the choice of the best parent gives $\mathrm{cost}(X_{j_{i+1}}) \le \mathrm{cost}(X_{j_i}) + \lVert X_{j_i} - X_{j_{i+1}} \rVert$ at that iteration.

*Lemma 1 (event $E_1$: no steering near the path after $n_0$).* Let $E_1$ be the event that every random point $x_{rand}$ of an iteration $j > n_0$ that falls in some $B_{n, i}$ is added unchanged, $x_{new} = x_{rand}$. Then $\Pr[E_1] \ge 1 - a e^{-b n}$ for constants $a, b > 0$. Put $\kappa = \min\{\eta, \delta\} / 10$ and points $z_1, \dots, z_\ell$ on $\sigma_\varepsilon$ at distance at most $\kappa$ apart. Theorem 1 of Kleinbort et al. (2019) gives that, with probability at least $1 - a e^{-b n}$, the RRT has a vertex in every $B_\kappa(z_k)$ after $n_0 = \mu n$ iterations, and by part 1(d) so does RRT\*. For $n$ large, each $B_{n, i}$ lies in some $B_\kappa(z_k)$. A random point in $B_\kappa(z_k)$ then has its nearest vertex within $2\kappa < \eta$, so STEER does not change it, and the segment lies in $B_{3\kappa}(z_k) \subset \mathcal{F}$. This lemma needs $\eta$ fixed and positive. Given $E_1$, the vertices of $V_i$ in $B_{n, i}$ are uniform samples.

*Lemma 2 (event $E_2$: every ball has a vertex from its window).* Let $E_2$ be the event that $V_i \cap B_{n, i} \ne \emptyset$ for every $i$. Given $E_1$, by the union bound and $1 - x \le e^{-x}$,

$$\Pr[E_2^c \mid E_1] \le M_n \left( 1 - \frac{\zeta_d r^d}{(2 + \theta)^d |\mathcal{F}|} \right)^{(n - n_0)/M_n} \le M_n \exp\left( - \xi \, n \, r^{d+1} \right) = M_n \, n^{-\xi \gamma^{d+1}},$$

with $\xi = \theta \zeta_d (1 - \mu) / (c(\sigma_\varepsilon) (2 + \theta)^{d+1} |\mathcal{F}|)$, using $(n - n_0)/M_n \approx n (1 - \mu) \theta r / (c(\sigma_\varepsilon)(2 + \theta))$ and $n r^{d+1} = \gamma^{d+1} \log n$. The rounding in $M_n$ changes the exponent by a factor $1 - O(r)$, and since $r \log n \to 0$ this changes the bound only by a factor that tends to 1. Since $M_n$ is of order $(n / \log n)^{1/(d+1)}$, the bound tends to 0 when $\xi \gamma^{d+1} \ge 1/(d + 1)$, which is

$$\gamma \ge (2 + \theta) \left( \frac{c(\sigma_\varepsilon) |\mathcal{F}|}{(d + 1) \theta \zeta_d (1 - \mu)} \right)^{1/(d+1)},$$

and the hypothesis of Theorem 1 implies it, because $c(\sigma_\varepsilon) \le (1 + \varepsilon/4) c^*$. With equality, the bound is of order $(\log n)^{-1/(d+1)}$, which still tends to 0. Since $\Pr[E_1] \to 1$, also $\Pr[E_2] \to 1$. This is where the exponent $1/(d+1)$ comes from: a window has about $n r$ iterations, a ball has volume of order $r^d$, and a ball misses its window with probability about $e^{-c \, n r^{d+1}}$.

*Lemma 3 (event $E_3$: few small balls are empty).* Fix new constants $\alpha, \beta \in (0, \theta \varepsilon / 16)$, not those of part 2, and let $B^\beta_{n, i}$ be the ball of radius $\beta r / (2 + \theta)$ around $x_i$. Let $E_3$ be the event that at most $\alpha M_n$ of the $i$ have $V_i \cap B^\beta_{n, i} = \emptyset$. Given $E_1$, the same computation gives for each $i$ the probability $n^{-\beta^d \xi \gamma^{d+1}}$ at most that the small ball is empty. So the expected number $K$ of empty small balls is at most $M_n n^{-\beta^d \xi \gamma^{d+1}}$, and by [Markov's inequality](/markov-inequality/) $\Pr[K > \alpha M_n] \le n^{-\beta^d \xi \gamma^{d+1}} / \alpha \to 0$.

*Lemma 4 (the cost on $E_2 \cap E_3$).* For $1 < i < M_n$, let $X_{j_i}$ be a vertex of $V_i \cap B^\beta_{n, i}$ if there is one, and otherwise of $V_i \cap B_{n, i}$, and let $X_{j_1} = s$ and $X_{j_{M_n}} = t$. The windows make $j_1 < j_2 < \dots < j_{M_n}$, which is the chain that part 3 asks for. By Claim 1 and induction on $i$, using that costs never increase, $\mathrm{cost}(t) \le \sum_{i=2}^{M_n} \lVert X_{j_i} - X_{j_{i-1}} \rVert$. Each term is at most the distance $\theta r / (2 + \theta)$ between the centers plus the offsets of the two end points from their centers, and an offset is at most $\beta r / (2 + \theta)$ in a small ball and $r / (2 + \theta)$ otherwise. Each vertex is an end point of at most two terms, and at most $\alpha M_n$ vertices are not in their small balls, so

$$\mathrm{cost}(t) \le \frac{M_n r}{2 + \theta} \left( \theta + 2\beta + 2\alpha \right) \le \left( c(\sigma_\varepsilon) + \frac{\theta r}{2 + \theta} \right) \left( 1 + \frac{2\alpha + 2\beta}{\theta} \right).$$

Since $(2\alpha + 2\beta)/\theta < \varepsilon/4$ and $r \to 0$, for $n$ large this is less than $(1 + \varepsilon/4)^2 c^* + o(1) < (1 + \varepsilon) c^*$, because $(1 + \varepsilon/4)^2 = 1 + \varepsilon/2 + \varepsilon^2/16 < 1 + \varepsilon$ for $\varepsilon \in (0, 1)$.

*The end.* $\Pr[E_2 \cap E_3] \ge 1 - \Pr[E_2^c] - \Pr[E_3^c] \to 1$, and on $E_2 \cap E_3$, Lemma 4 gives $c(\sigma_n) \le (1 + \varepsilon) c^*$ for $n$ large. $\blacksquare$

## Consequences

- **Almost sure convergence from Theorem 1.** By part 1(a), the cost of the returned path does not increase along a run, so the events $\{c(\sigma_n) \le (1 + \varepsilon) c^*\}$ grow with $n$. Theorem 1 then gives that with probability 1, $\lim_n c(\sigma_n) \le (1 + \varepsilon) c^*$, and over $\varepsilon = 1/k$ for all $k$, $\lim_n c(\sigma_n) \le c^*$ with probability 1. This short step is not stated in the paper. So with the larger radius, the length of the returned path converges with probability 1 to at most the robust optimum.
- **The same method for other planners.** Karaman and Frazzoli use the same plan for PRM\* (Theorem 34, the same kind of radius with the constant $2(1 + 1/d)^{1/d}$ in place of $(2(1 + 1/d))^{1/d}$), RRG (Theorem 36), and the $k$-nearest versions with $k > e(1 + 1/d)$ for PRM\* and RRG (Theorems 35 and 37) and $k > 2^{d+1} e (1 + 1/d)$ for RRT\* (Theorem 39). The gap of part 3 is about the order of the samples. PRM\* joins every pair of samples within the radius, so the order plays no role there.
- **The cost per iteration.** With the radius of Theorem 38, a ball of radius $r(n)$ holds $\alpha \log n$ samples in expectation, and Lemma 42 gives $O(\log n)$ expected calls of the checker per iteration. Karaman and Frazzoli conclude that the total time of RRT\* is within a constant factor of that of the RRT. With the radius of Theorem 1, the expected count is $\zeta_d \gamma^d n^{1/(d+1)} (\log n)^{d/(d+1)} / |\mathcal{F}|$, a power of $n$. The table gives both for $d = 2$ and $|\mathcal{F}| = 1$, with $\gamma$ equal to 1.1 times the threshold of Theorem 38, and with the threshold of Theorem 1 for $\varepsilon = 0.5$, $\theta = 0.2$, $\mu = 0.5$ and $c^* = 1$.

| $n$ | radius, exponent $1/2$ | samples in the ball | radius, exponent $1/3$ | samples in the ball |
|---|---|---|---|---|
| $10^3$ | 0.0893 | 25.1 | 0.4445 | 620.6 |
| $10^4$ | 0.0326 | 33.4 | 0.2271 | 1619.7 |
| $10^5$ | 0.0115 | 41.8 | 0.1135 | 4049.2 |
| $10^6$ | 0.0040 | 50.2 | 0.0560 | 9851.3 |

The radius of Theorem 1 is capped by $\eta$ in the algorithm, and its constant comes from a proof, so the table compares bounds, not tuned settings.

- **What the theorem does not give.** Neither proof gives a rate of convergence. And by Lemma 28, under Assumption 27 (the points of all optimal paths have measure 0), no sampling planner has an optimal path after a finite number of samples with positive probability, so the convergence holds only in the limit.

## Tightness

- **The rewiring is needed.** The RRT, which keeps the nearest vertex as parent, is not asymptotically optimal (Theorem 33). Its best cost converges with probability 1 to a value above $c^*$.
- **The logarithm is needed in the roadmap analogues.** The simplified PRM with radius $\gamma n^{-1/d}$ (Theorem 32) and with a fixed number $k$ of nearest neighbors (Theorem 31) is not asymptotically optimal. A ball of radius $\gamma n^{-1/d}$ holds a constant expected number of samples, and the [random geometric graph](/random-geometric-graph/) on the samples has gaps along the path.
- **The exponent is open.** Solovey et al. leave open whether the exponent $1/(d+1)$ can be lowered to $1/d$. They note that the practical success of RRT\* and its extensions with the exponent $1/d$ is some evidence that it can.
- **The clearance hypothesis is needed.** Let $\mathcal{X}_{free}$ be two closed squares in the plane that meet at one corner point $p$, with $x_{init}$ in one and $\mathcal{X}_{goal}$ in the interior of the other. Every feasible path passes through $p$, so no path has weak $\delta$-clearance. An edge of the tree is a segment between two vertices, and a vertex is a sample or lies on a segment from a vertex toward a sample. For an edge to pass through the fixed point $p$, a new sample must fall on a line that the earlier vertices fix, which has probability 0. So with probability 1 the tree never leaves the first square, and $Y_n = \infty$ for all $n$.

## History

Karaman and Frazzoli posted RRT\* and PRM\* in May 2010 (arXiv:1005.0416, with a short version at Robotics: Science and Systems 2010), and the full paper appeared in the International Journal of Robotics Research in 2011. It was the first proof that sampling planners can converge to optimal paths, and it used the theory of random geometric graphs. Solovey et al. note that a large number of later works appeal to the optimality of RRT\* for their own guarantees. In 2015, Janson, Schmerling, Clark and Pavone proved the asymptotic optimality of FMT\* with a related ball argument. In 2019, Kleinbort, Solovey, Littlefield, Bekris and Halperin gave a full proof of probabilistic completeness for the RRT. Solovey, Janson, Schmerling, Frazzoli and Pavone, with Frazzoli an author of the original paper, posted the gap and the new proof in September 2019 (arXiv:1909.09688) and published it at ICRA 2020.

## References
