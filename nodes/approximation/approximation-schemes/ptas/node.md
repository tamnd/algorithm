---
tag: JZX9QJ
kind: definition
slug: ptas
name: Polynomial-time approximation scheme (PTAS)
aliases:
- PTAS
- approximation scheme
- polynomial time approximation scheme
area: approximation/approximation-schemes
level: core
summary: Family of (1+ε)-approximation algorithms for every fixed ε>0, each running in polynomial time in the input size for that ε.
prereqs: [approximation-ratio, polynomial-time, np-hard]
see_also: [eptas, fptas, apx, asymptotic-ptas, hochbaum-shmoys-makespan-ptas, arora-euclidean-tsp-ptas, baker-technique, ptas-reduction]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 3 (Rounding data and dynamic programming), Sections 3.1 and 3.2 (the definition of a PTAS and the scheme for identical machines)
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 3 (the classes APX, PTAS and FPTAS, and the gap technique)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 9 (Bin packing) and Chapter 10 (Minimum makespan scheduling)
  - title: Sartaj Sahni, Approximate algorithms for the 0/1 knapsack problem, Journal of the ACM 22(1), 1975
    locator: the scheme that enumerates the subsets of at most k items
  - title: Dorit S. Hochbaum and David B. Shmoys, Using dual approximation algorithms for scheduling problems, theoretical and practical results, Journal of the ACM 34(1), 1987
    locator: the PTAS for makespan on identical machines
---

A polynomial-time approximation scheme, or PTAS, is a family of approximation algorithms, one for each accuracy $\varepsilon > 0$, where the algorithm for $\varepsilon$ returns a solution within a factor $1 + \varepsilon$ of the optimum for a minimization problem, or $1 - \varepsilon$ for a maximization problem, and runs in time polynomial in the input size when $\varepsilon$ is fixed. The time can grow very fast with $1/\varepsilon$, as in $n^{O(1/\varepsilon)}$. A problem with a PTAS can be approximated as well as we like, which is the best we can hope for with an NP-hard problem. The class PTAS sits in a chain $\mathrm{FPTAS} \subseteq \mathrm{EPTAS} \subseteq \mathrm{PTAS} \subseteq \mathrm{APX} \subseteq \mathrm{NPO}$, and each step is strict under a standard assumption.

## Definition

Let $\Pi$ be an optimization problem in [NPO](/npo-class/). We use the conventions of [the approximation ratio](/approximation-ratio/) page: $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ with $\rho \ge 1$ for minimization and $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$ for maximization.

An algorithm $A$ is a **polynomial-time approximation scheme** for $\Pi$ when, on input an instance $I$ and a rational number $\varepsilon > 0$, it returns a feasible solution with

$$
\mathrm{ALG}(I, \varepsilon) \le (1 + \varepsilon) \cdot \mathrm{OPT}(I) \ \ \text{(minimization)}, \qquad \mathrm{ALG}(I, \varepsilon) \ge (1 - \varepsilon) \cdot \mathrm{OPT}(I) \ \ \text{(maximization)},
$$

and, for each fixed $\varepsilon > 0$, its running time is bounded by a polynomial in $|I|$. The polynomial may depend on $\varepsilon$, in its degree as well as in its constant. The class **PTAS** is the set of NPO problems that have such an algorithm.

The forms of the running time give the finer classes:

| form of the time | example | class |
|---|---|---|
| $\mathrm{poly}(\lvert I \rvert, 1/\varepsilon)$ | $O(n^3 / \varepsilon)$ | [FPTAS](/fptas/) |
| $f(1/\varepsilon) \cdot \mathrm{poly}(\lvert I \rvert)$, with the degree fixed | $O(2^{1/\varepsilon} n)$ | [EPTAS](/eptas/) |
| $\lvert I \rvert^{g(1/\varepsilon)}$ | $O(n^{\lceil 1/\varepsilon \rceil + 1})$ or $n^{O(1/\varepsilon^2)}$ | PTAS |

Notes on the definition:

- **The guarantee is absolute.** It holds on each instance. A scheme with $\mathrm{ALG} \le (1 + \varepsilon)\mathrm{OPT} + c(\varepsilon)$ is an [asymptotic PTAS](/asymptotic-ptas/), a weaker notion.
- **One algorithm or a family.** Some books define a PTAS as a family $\{A_\varepsilon\}$ of algorithms, one for each $\varepsilon$, and others as one algorithm with $\varepsilon$ as an input. The second form needs the algorithm to be uniform in $\varepsilon$. All the schemes on this site are of the second form.
- **A PTAS is in APX.** Fix $\varepsilon = 1$ for minimization, or $\varepsilon = 1/2$ for maximization. This gives a polynomial-time algorithm with ratio $2$, or $1/2$, so $\mathrm{PTAS} \subseteq$ [APX](/apx/).
- **Randomized schemes.** A scheme whose bound holds in expectation, or with high probability, is a randomized PTAS. Some dense problems first had randomized schemes.

## Examples and non-examples

**Knapsack by partial enumeration (Sahni, 1975).** This scheme is a PTAS for the [0/1 knapsack problem](/knapsack-problem/) but not an FPTAS. Let $k = \lceil 1 / \varepsilon \rceil$. For each set $G$ of at most $k$ items with $w(G) \le W$, let $p_{\min}$ be the least profit in $G$. Go through the other items with profit at most $p_{\min}$ in order of $p_j / w_j$, largest first, and add each one that still fits. Return the best of all these sets.

*Proof of the ratio.* Let $O$ be an optimal set. If $|O| \le k$, then $G = O$ is tried and the result is optimal. Otherwise let $G$ be the $k$ items of $O$ with the largest profits, and $p_{\min}$ the least of them. The items of $O \setminus G$ have profit at most $p_{\min}$ and fit in the capacity $C = W - w(G)$, so the [fractional knapsack](/fractional-knapsack/) optimum on the allowed items with capacity $C$ is at least $p(O \setminus G)$. That fractional optimum takes the items in order of $p_j / w_j$ up to one split item $s$, and the greedy step takes at least all the items before $s$. So the greedy step gets at least $p(O \setminus G) - p_s \ge p(O \setminus G) - p_{\min}$. The result is at least $p(G) + p(O \setminus G) - p_{\min} = \mathrm{OPT} - p_{\min}$, and $p_{\min} \le p(G) / k \le \mathrm{OPT} / k \le \varepsilon \cdot \mathrm{OPT}$. $\square$

*Time.* There are $O(n^k)$ sets $G$, and each greedy pass takes $O(n)$ time after one sort, so the time is $O(n^{\lceil 1/\varepsilon \rceil + 1})$. For $\varepsilon = 0.1$ and $n = 100$ this is about $10^{22}$ steps, while the [knapsack FPTAS](/knapsack-fptas/) needs about $n^3/\varepsilon = 10^7$.

*Example.* Take profits $56, 22, 12, 45, 58, 53$, weights $2, 7, 3, 8, 9, 6$ and $W = 15$, where $\mathrm{OPT} = 131$. A script gives these results:

| $k$ | sets $G$ tried | best value found | bound $(1 - 1/k)\,\mathrm{OPT}$ |
|---|---|---|---|
| 0 (greedy only) | 1 | 121 | none |
| 1 | 7 | 126 | 0 |
| 2 ($\varepsilon = 1/2$) | 22 | 126 | 65.5 |
| 3 ($\varepsilon = 1/3$) | 42 | 131 | 87.3 |

For $k = 3$, the optimum $\{1, 2, 6\}$ has only 3 items, so it is one of the sets $G$.

**Makespan on identical machines.** The [Hochbaum and Shmoys PTAS](/hochbaum-shmoys-makespan-ptas/) (1987) uses [dual approximation](/dual-approximation/): guess the makespan $T$, round the large jobs, and pack them exactly by a dynamic program over machine configurations. The time is $n^{O(1/\varepsilon^2)}$.

**Euclidean TSP.** For points in the plane, the [Arora PTAS](/arora-euclidean-tsp-ptas/) (1998) finds a tour of length at most $(1 + \varepsilon)\mathrm{OPT}$ by [portal-based dissection](/portal-based-dissection/). Mitchell (1999) gave a scheme by a different method. Metric TSP in general has no PTAS unless P = NP.

**Planar graphs.** [Baker's technique](/baker-technique/) gives a PTAS for maximum independent set, minimum vertex cover and many other problems on [planar graphs](/planar-graph/), with time $2^{O(1/\varepsilon)} n$. See also the [shifting technique](/shifting-technique/) for geometric problems.

**Multiple knapsack.** The [Chekuri and Khanna PTAS](/chekuri-khanna-ptas/) guesses the large profits on a geometric grid and packs them by an LP for the [generalized assignment problem](/generalized-assignment-problem/).

**Dense max cut.** For graphs with $\Omega(n^2)$ edges, max cut has a PTAS by sampling; see [the dense max cut PTAS](/dense-max-cut-ptas/).

**Non-example: APX-hard problems.** Under P ≠ NP, no [APX-hard](/apx-completeness/) problem has a PTAS. Examples are max 3SAT, where $7/8 + \delta$ is NP-hard for each $\delta > 0$ ([max 3SAT inapproximability](/max-3sat-inapproximability/)), minimum [vertex cover](/vertex-cover/), and [metric TSP](/metric-tsp/). These hardness results come from the [PCP theorem](/pcp-theorem/).

**The separation PTAS ⊊ APX: bin packing.** [Bin packing](/bin-packing/) is in APX, because next fit uses at most $2 \cdot \mathrm{OPT} - 1$ bins (proved on [the approximation ratio](/approximation-ratio/) page). But no polynomial-time algorithm has an absolute ratio $\rho < 3/2$ unless P = NP.

*Proof.* Let $a_1, \ldots, a_n$ be an instance of the [partition problem](/partition-problem/), with $\sum_i a_i = 2B$. If some $a_i > B$, the answer is no. Otherwise make the bin packing instance with sizes $a_i / B \le 1$. Their sum is 2, so $\mathrm{OPT} \ge 2$, and $\mathrm{OPT} = 2$ exactly when the numbers split into two sets of sum $B$. Let $A$ have ratio $\rho < 3/2$. If $\mathrm{OPT} = 2$, then $\mathrm{ALG} \le \rho \cdot 2 < 3$, so $\mathrm{ALG} = 2$. If $\mathrm{OPT} \ge 3$, then $\mathrm{ALG} \ge 3$. So $\mathrm{ALG} = 2$ decides partition in polynomial time. $\square$

So bin packing has no PTAS unless P = NP. It has an [asymptotic PTAS](/asymptotic-ptas/), which shows that the hardness lives on instances with small optima. See [bin packing inapproximability](/bin-packing-inapproximability/).

## Related definitions

The chain of classes and the problems that separate them, each under the stated assumption:

| inclusion | separating problem | why it is in the larger class | why not in the smaller class | page with the proof |
|---|---|---|---|---|
| FPTAS ⊊ EPTAS | $P \Vert C_{\max}$; multiple knapsack | EPTAS by Alon et al. (1998); by Jansen (2010) | strongly NP-hard; no FPTAS for 2 knapsacks, if P ≠ NP | [FPTAS](/fptas/) |
| EPTAS ⊊ PTAS | independent set in unit disk graphs | PTAS by shifting | W[1]-hard by the size, if FPT ≠ W[1] | [EPTAS](/eptas/) |
| PTAS ⊊ APX | bin packing; max 3SAT | next fit has ratio 2 | no ratio below 3/2, if P ≠ NP | this page |
| APX ⊊ NPO | general TSP; set cover | they are in NPO | no constant ratio, if P ≠ NP | [APX](/apx/) |

- **EPTAS and FPTAS.** The schemes with time $f(1/\varepsilon) \cdot \mathrm{poly}(n)$ form the class [EPTAS](/eptas/), and those with time $\mathrm{poly}(n, 1/\varepsilon)$ form the class [FPTAS](/fptas/).
- **APX.** [APX](/apx/) is the class of NPO problems with a constant ratio. Its complexity side, with complete problems, is on the [APX class](/apx-class/) page.
- **PTAS reductions.** A [PTAS reduction](/ptas-reduction/) maps a scheme for the target problem to a scheme for the source problem. [L-reductions](/l-reduction/) are a special case. They define APX-hardness.
- **Asymptotic PTAS.** An [APTAS](/asymptotic-ptas/) needs the bound $(1 + \varepsilon)\mathrm{OPT}$ only up to an additive term $c(\varepsilon)$.

## References
