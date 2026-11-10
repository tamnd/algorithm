---
tag: FMBMA1
kind: definition
slug: approximation-ratio
name: Approximation ratio
aliases: [performance ratio, approximation factor, performance guarantee, approximation guarantee]
area: approximation/approximation-schemes
level: intro
summary: The worst case factor by which the cost of an approximation algorithm's solution may differ from the cost of an optimal solution.
prereqs: [np-hard, polynomial-time]
see_also: [ptas, fptas, apx, asymptotic-ptas, approximation-threshold, integrality-gap, competitive-ratio, vertex-cover-2-approximation]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 1, Section 1.1 (the definition of an α-approximation algorithm, with α < 1 for maximization)
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 35, the introduction (performance ratios) and Section 35.1
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 3 (performance ratio and relative error) and Chapter 4 (asymptotic approximation)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2005
    locator: Chapter 11, Section 11.1
  - title: David S. Johnson, Approximation algorithms for combinatorial problems, Journal of Computer and System Sciences 9(3), 1974
    locator: pages 256 to 278
---

The approximation ratio of an algorithm measures how far its answer can be from the best answer, in the worst case over all inputs. For a minimization problem it is the least $\rho \ge 1$ with $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. For a maximization problem this site writes the guarantee as $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$; some books use $1/\alpha \ge 1$ in its place. Many important problems are [NP-hard](/np-hard/), so no [polynomial-time](/polynomial-time/) exact algorithm is known for them. An approximation algorithm runs in polynomial time and gives up exactness, and its ratio says how much it can lose. A ratio of 1 means that the algorithm is always optimal. Variants of the definition bound the ratio only for large optima (the asymptotic ratio), bound the difference in place of the ratio (an additive guarantee), or bound the expected value for a randomized algorithm.

## Definition

**Optimization problems.** Let $\Pi$ be an optimization problem. Each instance $I$ has a finite, non-empty set $\mathcal{F}(I)$ of feasible solutions, and each feasible solution $S$ has a value $c(S) \ge 0$. The optimum is $\mathrm{OPT}(I) = \min_{S \in \mathcal{F}(I)} c(S)$ for a minimization problem and $\mathrm{OPT}(I) = \max_{S \in \mathcal{F}(I)} c(S)$ for a maximization problem. Let $A$ be an algorithm that returns a feasible solution for each instance. We write $\mathrm{ALG}(I)$, or $A(I)$, for the value of the returned solution. The problems of interest are in the class [NPO](/npo-class/): feasibility and the value can be checked in polynomial time.

**Minimization.** Let $\rho \ge 1$. The algorithm $A$ is a **$\rho$-approximation algorithm** when $A$ runs in polynomial time and, for every instance $I$,

$$
\mathrm{ALG}(I) \le \rho \cdot \mathrm{OPT}(I).
$$

**Maximization.** Let $0 < \alpha \le 1$. The algorithm $A$ is an **$\alpha$-approximation algorithm** when $A$ runs in polynomial time and, for every instance $I$,

$$
\mathrm{ALG}(I) \ge \alpha \cdot \mathrm{OPT}(I).
$$

**The ratio of an algorithm.** The approximation ratio of $A$ is the best constant in these inequalities. With the convention that instances with $\mathrm{OPT}(I) = 0$ need $\mathrm{ALG}(I) = 0$ for a minimization problem (and hold for free for a maximization problem),

$$
\rho_A = \sup_{I :\ \mathrm{OPT}(I) > 0} \frac{\mathrm{ALG}(I)}{\mathrm{OPT}(I)} \quad \text{(minimization)}, \qquad \alpha_A = \inf_{I :\ \mathrm{OPT}(I) > 0} \frac{\mathrm{ALG}(I)}{\mathrm{OPT}(I)} \quad \text{(maximization)}.
$$

A minimization algorithm with $\mathrm{ALG}(I) > 0$ on an instance with $\mathrm{OPT}(I) = 0$ has no finite ratio, because no $\rho$ gives $\mathrm{ALG}(I) \le \rho \cdot 0$. The supremum is the least valid $\rho$: for $\mathrm{OPT}(I) > 0$, the inequality $\mathrm{ALG}(I) \le \rho \cdot \mathrm{OPT}(I)$ is the same as $\rho \ge \mathrm{ALG}(I) / \mathrm{OPT}(I)$, so the valid $\rho$ form the closed set $[\rho_A, \infty)$. The same holds for $\alpha_A$ with the inequalities turned around. The ratio can also depend on the size $n$ of the input: $\rho(n)$ is the supremum over the instances of size $n$. Greedy set cover, with $\rho(n) = H_n$, is an example.

**Relative error.** For $\mathrm{OPT}(I) > 0$, a ratio of $1 + \varepsilon$ for a minimization problem means $(\mathrm{ALG} - \mathrm{OPT}) / \mathrm{OPT} \le \varepsilon$, and a ratio of $1 - \varepsilon$ for a maximization problem means $(\mathrm{OPT} - \mathrm{ALG}) / \mathrm{OPT} \le \varepsilon$. The number $\varepsilon$ is the relative error. Approximation schemes are stated in this form.

**Absolute and asymptotic ratios.** The ratios above are **absolute**: they hold on every instance, small or large. For a minimization problem, the **asymptotic ratio** of $A$ is

$$
\rho_A^{\infty} = \lim_{k \to \infty} \ \sup_{I :\ \mathrm{OPT}(I) \ge k} \frac{\mathrm{ALG}(I)}{\mathrm{OPT}(I)}.
$$

The limit exists, because the supremum does not grow as $k$ grows. If $\mathrm{ALG}(I) \le \rho \cdot \mathrm{OPT}(I) + c$ for every instance and a constant $c$, then $\rho_A^\infty \le \rho$, because $c / \mathrm{OPT}(I) \le c / k \to 0$. Many papers state an asymptotic result in this form, with the additive constant $c$ given. The asymptotic ratio is the right measure for problems such as [bin packing](/bin-packing/), where small instances encode NP-hard decision problems.

**Additive guarantees.** An algorithm has an **additive guarantee** $c$ when $\mathrm{ALG}(I) \le \mathrm{OPT}(I) + c$ (minimization) or $\mathrm{ALG}(I) \ge \mathrm{OPT}(I) - c$ (maximization) for every instance. An additive guarantee with a constant $c$ implies the asymptotic ratio 1. The guarantee $c$ can also be a function, as in $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$ for the [Karmarkar and Karp bin packing algorithm](/karmarkar-karp-bin-packing/).

**Randomized algorithms.** For a [randomized algorithm](/randomized-algorithm/), $\mathrm{ALG}(I)$ is a random variable over the coin flips of the algorithm, and the input is still the worst case. The algorithm has **expected ratio** $\rho$ when $\mathbb{E}[\mathrm{ALG}(I)] \le \rho \cdot \mathrm{OPT}(I)$ for every instance (or $\mathbb{E}[\mathrm{ALG}(I)] \ge \alpha \cdot \mathrm{OPT}(I)$ for maximization). It has ratio $\rho$ **with high probability** when $\Pr[\mathrm{ALG}(I) \le \rho \cdot \mathrm{OPT}(I)] \ge 1 - 1/n^{c}$ for a constant $c > 0$. An expected ratio is not an average over random inputs; that is average-case analysis, a different notion.

**The conventions in use.** The table shows how some standard sources write the same guarantees.

| source | minimization | maximization |
|---|---|---|
| this site | $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$, $\rho \ge 1$ | $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$, $\alpha \le 1$ |
| Williamson and Shmoys (Section 1.1) | $\alpha$-approximation with $\alpha > 1$ | $\alpha$-approximation with $\alpha < 1$ |
| Cormen et al. (Chapter 35) | $\max(C / C^*, C^* / C) \le \rho(n)$, so $\rho(n) \ge 1$ in both cases | the same formula |
| Ausiello et al. (Chapter 3) | performance ratio $\max(\mathrm{ALG}/\mathrm{OPT}, \mathrm{OPT}/\mathrm{ALG}) \ge 1$ | the same formula |

So a "2-approximation for max cut" in a book that uses ratios of at least 1 is a "1/2-approximation" on this site. The two statements say the same thing.

## Examples and non-examples

**Vertex cover by a maximal matching (ratio exactly 2).** This is an algorithm for the [vertex cover problem](/vertex-cover/), a minimization problem. The input is a graph $G = (V, E)$, and a vertex cover is a set $C \subseteq V$ that has an end of every edge. The algorithm finds a maximal matching $M$, a set of edges with no common ends that no further edge can join, and outputs the set $C$ of all ends of the edges of $M$, so $|C| = 2|M|$.

1. $C$ is a vertex cover. If an edge $uv$ had no end in $C$, then neither $u$ nor $v$ is matched, and $M \cup \{uv\}$ is a larger matching, which contradicts the choice of $M$.
2. $|M| \le \mathrm{OPT}$. An optimal cover $C^*$ has an end of each edge of $M$, and these ends are all different, because no two edges of $M$ share an end. This is the lower bound on $\mathrm{OPT}$ that the analysis uses.
3. So $|C| = 2|M| \le 2 \cdot \mathrm{OPT}$, and the ratio is at most 2.

The bound is tight. On the 4-cycle with vertices $a_1, b_1, a_2, b_2$ in order, a run that picks the edges $a_1 b_1$ and $a_2 b_2$ returns all four vertices. The set $\{a_1, a_2\}$ is a cover, and a single vertex has only two of the four edges, so $\mathrm{OPT} = 2$ and the ratio on this input is $4/2 = 2$. More generally, a graph of $k$ disjoint edges has $\mathrm{OPT} = k$ and $\mathrm{ALG} = 2k$. See the [vertex cover 2-approximation](/vertex-cover-2-approximation/).

**A random cut (expected ratio 1/2).** For max cut, a maximization problem, put each vertex on one side or the other with probability 1/2, independently. Each edge is cut with probability 1/2, so $\mathbb{E}[\mathrm{ALG}] = |E| / 2 \ge \mathrm{OPT} / 2$. This is a 1/2-approximation in expectation, in the convention $\alpha \le 1$, and a "2-approximation" in the convention of Cormen et al. On the 5-cycle, the 32 cuts have mean $5/2$ and the maximum is 4, so the ratio of the expected value to the optimum is $5/8$ on this input.

**Next fit for bin packing (absolute and asymptotic ratio 2).** Next fit keeps one open bin, and opens a new bin when the next item does not fit. Any two consecutive bins hold more than 1 in total, so with $k$ bins the total size $s$ is more than $\lfloor k/2 \rfloor$. Since $\mathrm{OPT} \ge s$ and $\mathrm{OPT}$ is an integer, $\mathrm{OPT} \ge \lfloor k/2 \rfloor + 1 \ge (k + 1)/2$, so $\mathrm{ALG} = k \le 2 \cdot \mathrm{OPT} - 1$. For the lower bound, take $4N$ items alternating between $1/2$ and $1/(2N)$. Next fit puts one item of each kind in each bin and uses $2N$ bins. The optimum uses $N$ bins for the halves and one bin for the $2N$ small items, so $\mathrm{OPT} = N + 1$, and the ratio $2N/(N + 1)$ tends to 2. A script confirms $\mathrm{ALG} = 2N$ and $\mathrm{OPT} = N + 1$ for $N = 2, 5, 10, 50$.

**Bin packing: an absolute bound and an asymptotic bound that differ.** No polynomial-time algorithm for bin packing has an absolute ratio below $3/2$ unless P = NP, because deciding whether $\mathrm{OPT} \le 2$ is the NP-complete [partition problem](/partition-problem/) (see [bin packing inapproximability](/bin-packing-inapproximability/)). But for each $\varepsilon > 0$ there is an algorithm with $\mathrm{ALG} \le (1 + \varepsilon)\mathrm{OPT} + 1$, the [bin packing APTAS](/bin-packing-aptas/), so the asymptotic ratio can be as close to 1 as we like. The hardness lives only on instances with small optima.

**Edge coloring (an additive guarantee).** By [Vizing's theorem](/vizing-theorem/), the edges of a simple graph with largest degree $\Delta$ can be colored with $\Delta + 1$ colors in polynomial time, and each coloring needs at least $\Delta$ colors. So $\mathrm{ALG} \le \mathrm{OPT} + 1$. Holyer (1981) showed that deciding whether $\Delta$ colors are enough is NP-complete even for $\Delta = 3$, so no algorithm has an absolute ratio below $4/3$ unless P = NP. See [edge coloring](/edge-coloring/).

**Greedy set cover (a ratio that grows with n).** The [greedy set cover algorithm](/greedy-set-cover/) picks, at each step, the set that covers the most elements not yet covered. Its ratio is at most $H_d \le H_n$, where $d$ is the size of the largest set, $n$ is the number of elements and $H_d = 1 + 1/2 + \cdots + 1/d$. It grows like $\ln n$, so this is a $\rho(n)$-approximation with $\rho(n)$ not a constant.

**Non-example: a heuristic without a proof.** A method can find good answers on every test input and still have no known ratio. A ratio is a statement about all inputs, so it needs a proof, not experiments.

**Non-example: general TSP.** For the [traveling salesman problem](/traveling-salesman-problem/) with arbitrary edge costs, no polynomial-time algorithm has a finite ratio $\rho(n)$ that is computable in polynomial time, unless P = NP, because such an algorithm would decide the [Hamiltonian cycle](/hamiltonian-cycle/) problem. See [general TSP inapproximability](/general-tsp-inapproximability/). With the triangle inequality, [Christofides' algorithm](/christofides-algorithm/) has ratio $3/2$.

**Non-example: an additive constant for knapsack.** No polynomial-time algorithm for the [0/1 knapsack problem](/knapsack-problem/) has an additive guarantee $\mathrm{ALG} \ge \mathrm{OPT} - c$ for a constant $c$, unless P = NP. Multiply each profit by $c + 1$. The weights do not change, so the feasible sets do not change, and the value of every set is now a multiple of $c + 1$. A set within $c$ of the new optimum must then be optimal. So the algorithm would solve knapsack exactly, which is NP-hard. A relative guarantee, as in the [knapsack FPTAS](/knapsack-fptas/), is not affected by this scaling.

## Related definitions

- **Approximation schemes.** A [PTAS](/ptas/) is a family of $(1 + \varepsilon)$-approximation algorithms, one for each $\varepsilon > 0$, each in polynomial time. An [EPTAS](/eptas/) has time $f(1/\varepsilon) \cdot \mathrm{poly}(n)$, and an [FPTAS](/fptas/) has time polynomial in $n$ and $1/\varepsilon$. An [asymptotic PTAS](/asymptotic-ptas/) bounds the asymptotic ratio in place of the absolute one.
- **APX.** [APX](/apx/) is the class of NPO problems with a constant-factor approximation algorithm. The complexity view of this class is on the [APX class](/apx-class/) page.
- **Approximation threshold.** The [approximation threshold](/approximation-threshold/) of a problem is the best ratio that a polynomial-time algorithm can reach. Hardness results give lower bounds on it, under assumptions such as P ≠ NP or the [unique games conjecture](/unique-games-conjecture/).
- **Integrality gap.** For a minimization problem and a relaxation with optimum $\mathrm{LP}(I) \le \mathrm{OPT}(I)$, the [integrality gap](/integrality-gap/) is the supremum of $\mathrm{OPT}(I) / \mathrm{LP}(I)$. An analysis that proves $\mathrm{ALG} \le \rho \cdot \mathrm{LP}$ cannot give a $\rho$ below the gap.
- **Competitive ratio.** An online algorithm sees the input one piece at a time. Its [competitive ratio](/competitive-ratio/) is the same worst case factor, but the comparison is with the best offline solution, and the limit is lack of information, not lack of time.

## References
