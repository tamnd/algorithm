---
tag: 85ZVS8
kind: concept
slug: work-function
name: Work function
aliases:
- work functions
- offline cost function
area: online-and-streaming/competitive-analysis
level: advanced
summary: For a configuration, the minimum cost of serving the requests so far and ending in that configuration.
prereqs: [metrical-task-systems, offline-optimum, metric-space]
see_also: [work-function-algorithm, k-server-problem, metrical-service-systems, k-server-conjecture, bellman-equation, potential-function]
sources:
  - paper: "Allan Borodin, Nathan Linial and Michael E. Saks, An optimal on-line algorithm for metrical task system, Journal of the ACM 39(4) (1992), 745-763"
    title: "Borodin, Linial and Saks, An optimal on-line algorithm for metrical task system (1992)"
    locator: the offline cost of ending in each state, and the algorithm for metrical task systems that is based on it
  - paper: "Marek Chrobak and Lawrence L. Larmore, The server problem and on-line games, in On-Line Algorithms, DIMACS Series in Discrete Mathematics and Theoretical Computer Science 7 (1992), 11-64"
    title: "Chrobak and Larmore, The server problem and on-line games (1992)"
    locator: the definition of work functions for server problems, their basic properties and the work function algorithm
  - paper: "Elias Koutsoupias and Christos H. Papadimitriou, On the k-server conjecture, Journal of the ACM 42(5) (1995), 971-983"
    title: "Koutsoupias and Papadimitriou, On the k-server conjecture (1995)"
    locator: the quasiconvexity lemma for work functions and the proof that the work function algorithm is (2k - 1)-competitive
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: the chapters on metrical task systems and on the k-server problem (work functions and the work function algorithm)
---

The work function of an online problem maps each configuration $X$ to the least cost with which an offline algorithm can serve all requests so far and end in $X$. It is the value function of the offline dynamic program, computed forward in time. The minimum of the work function is the [offline optimum](/offline-optimum/) so far. Work functions are the main tool for [metrical task systems](/metrical-task-systems/) and for the [k-server problem](/k-server-problem/): the [work function algorithm](/work-function-algorithm/) is defined with them, and the best deterministic bounds for both problems ($2n - 1$ and $2k - 1$) are proved with them.

## In plain words

Think of a delivery van that must serve a list of jobs. At each moment, you can ask a question about the past: if I had known all of today's jobs in advance, what is the cheapest way to have done them and to stand now at this place? The answer for each place is one number, and the list of these numbers is the work function.

The smallest number in the list is the best cost in hindsight. The numbers also show which places are cheap places to be. A good online rule uses this list. It stays near the places where the best past plans end, and it does not chase the newest job without a reason.

## The idea

**Notation.** The configurations form a set $S$ with a metric $d$. For [metrical task systems](/metrical-task-systems/), $S$ is the set of $n$ states. For the k-server problem on a metric space $M$, $S$ is the set of multisets of $k$ points of $M$, and $d(X, Y)$ is the cost of a minimum matching between $X$ and $Y$. The request sequence is $\sigma = r_1, \ldots, r_m$, the start configuration is $X_0$, and $\mathrm{OPT}(\sigma)$ is the cost of the optimal offline schedule.

**Definition.** For $t = 0, 1, \ldots, m$, $w_t(X)$ is the least cost to serve $r_1, \ldots, r_t$, starting in $X_0$ and ending in $X$. In an MTS a request is a cost vector $r_t : S \to [0, \infty]$, and

$$w_0(X) = d(X_0, X), \qquad w_t(X) = \min_{Y \in S} \big( w_{t-1}(Y) + r_t(Y) + d(Y, X) \big).$$

The term $Y$ is the configuration in which the offline schedule serves $r_t$, and $d(Y, X)$ moves it to $X$ afterwards. In the k-server problem a request is a point $r$, the cost is $0$ if $r \in Y$ and $\infty$ otherwise, and the recurrence becomes

$$w_t(X) = \min_{x \in X} \big( w_{t-1}(X - x + r) + d(r, x) \big).$$

Here $X - x + r$ is $X$ with one copy of $x$ replaced by $r$. The offline schedule moves the server that will end at $x$ through $r$ instead.

**Basic properties.** Let $w = w_{t-1}$ and $w' = w_t$.

1. **Optimum.** $\mathrm{OPT}(r_1, \ldots, r_t) = \min_X w_t(X)$.
2. **Lipschitz.** $\lvert w_t(X) - w_t(Y) \rvert \le d(X, Y)$. A schedule that ends in $Y$ can move to $X$ at cost $d(X, Y)$. This holds for $w_0$ by the triangle inequality, and the recurrence keeps it.
3. **Monotone.** $w' \ge w$ when all costs are nonnegative. In the recurrence, $w(Y) + r_t(Y) + d(Y, X) \ge w(Y) + d(Y, X) \ge w(X)$ by the Lipschitz property.
4. **Locality of one request.** If $r_t(Y) = 0$ for all $Y \ne Z$, then $w'(X) = w(X)$ for all $X \ne Z$, and $w(Z) \le w'(Z) \le w(Z) + r_t(Z)$. This is the step that the cruel adversary uses in the lower bound for MTS.
5. **Support.** For each $X$ there is a $Y$ with $w'(X) = w'(Y) + d(Y, X)$ and $w'(Y) = w(Y) + r_t(Y)$. Take $Y$ as the minimizer in the recurrence. So every value of $w'$ is explained by a configuration where the new request was served at its full cost.
6. **Finitely many shapes.** If all distances and costs are integers, $w_t - \min w_t$ takes values in $\{0, 1, \ldots, D\}$, where $D$ is the diameter. So the work functions, up to an additive constant, form a finite set. Chrobak and Larmore use this to compute exact competitive ratios for small cases as finite games.

**Quasiconvexity.** For the k-server problem, Koutsoupias and Papadimitriou proved that every work function is quasiconvex: for any two configurations $X$ and $Y$, there is a bijection $h : X \to Y$ such that $w(X) + w(Y) \ge w(X - x + h(x)) + w(Y - h(x) + x)$ for every $x \in X$. This lemma is the heart of their proof that the work function algorithm is $(2k - 1)$-competitive.

**The work function algorithm.** After request $r_t$, move to a configuration $X$ that minimizes $w_t(X) + d(X_{t-1}, X)$, among those that can serve $r_t$. The first term pulls the algorithm toward the configurations where the best offline schedules end. The second term keeps it from moving far. The algorithm that uses only the first term is the "retrospective" rule, and the algorithm that uses only the second is the greedy rule; both are bad on their own. See [work function algorithm](/work-function-algorithm/).

**Computing it.** For an MTS with $n$ states, one step of the recurrence takes $O(n^2)$ time, so the work function after $m$ tasks costs $O(m n^2)$ time and $O(n)$ space. For the k-server problem on $N$ points the configurations number $\binom{N + k - 1}{k}$, so the work function is exponential in $k$. This is why the work function algorithm is mostly a tool of analysis.

**The forward and backward views.** The work function runs the [Bellman equation](/bellman-equation/) forward from the start. The usual offline dynamic program for OPT runs backward from the end and needs the whole sequence. The forward form needs only the past, so an online algorithm can keep it.

## Examples

**Three states on a line.** Let $a, b, c$ be the points $0, 1, 3$ of the line, with start state $a$. The tasks are given as $(r(a), r(b), r(c))$.

| $t$ | $r_t$ | $w_t(a)$ | $w_t(b)$ | $w_t(c)$ | OPT so far |
|---|---|---|---|---|---|
| 0 | | 0 | 1 | 3 | 0 |
| 1 | $(2, 0, 5)$ | 2 | 1 | 3 | 1 |
| 2 | $(0, 3, 1)$ | 2 | 3 | 4 | 2 |
| 3 | $(4, 1, 0)$ | 5 | 4 | 4 | 4 |
| 4 | $(0, 0, 3)$ | 5 | 4 | 6 | 4 |

For example, $w_2(b) = 3$: the schedule that moves to $b$ and serves both tasks there costs $1 + 0 + 3 = 4$, and the schedule that serves both tasks in $a$ and then moves to $b$ costs $2 + 0 + 1 = 3$. Each row is $1$-Lipschitz: $\lvert w(a) - w(c) \rvert \le 3$, and so on. Each value is at least the value above it.

**The support rule.** In row 3, the work function algorithm sits in $a$ and compares $w_3(x) + d(a, x)$: the values are $5, 5, 7$. States $a$ and $b$ tie, but $w_3(a) = 5 < w_2(a) + r_3(a) = 6$, so $a$ is not a support state, and its value comes from a schedule that ended in $b$. The algorithm moves to $b$. Its total cost is $4$, equal to OPT on this input.

**Two servers on four points.** Let the points $a, b, c, d$ be at $0, 1, 3, 4$ on a line, with two servers that start at $\{a, b\}$. The work function has one value for each of the six pairs:

| request | $ab$ | $ac$ | $ad$ | $bc$ | $bd$ | $cd$ | OPT so far |
|---|---|---|---|---|---|---|---|
| start | 0 | 2 | 3 | 3 | 4 | 6 | 0 |
| $c$ | 4 | 2 | 3 | 3 | 4 | 6 | 2 |
| $a$ | 4 | 2 | 3 | 3 | 4 | 6 | 2 |
| $d$ | 6 | 4 | 3 | 5 | 4 | 6 | 3 |
| $b$ | 6 | 6 | 5 | 5 | 4 | 6 | 4 |

After the request at $c$, the value of $ab$ rises from $0$ to $4$: a schedule that ends in $ab$ must send the server from $b$ to $c$ and back. The values of the pairs that contain $c$ do not change. The request at $a$ changes nothing, because the cheapest schedules already have a server at $a$. The k-server form of the recurrence and the general MTS form give the same table.

## Where it is used

- **Metrical task systems.** The $(2n - 1)$-competitive algorithm of Borodin, Linial and Saks, and the potential $2 \sum_x w(x) - w(s)$ that proves both the upper and the lower bound, are on the [metrical task systems](/metrical-task-systems/) page.
- **The k-server problem.** The [work function algorithm](/work-function-algorithm/) is $(2k - 1)$-competitive on every metric (Koutsoupias and Papadimitriou 1995), and $k$-competitive for $k = 2$ (Chrobak and Larmore), and on the line, on weighted stars and on metrics with $k + 2$ points (Bartal and Koutsoupias 2004). The open [k-server conjecture](/k-server-conjecture/) asks whether it is $k$-competitive in general.
- **Metrical service systems.** For [metrical service systems](/metrical-service-systems/) the work function decides which allowed states are still worth keeping.
- **Page migration.** Chrobak, Larmore, Reingold and Westbrook used work functions to design algorithms for the [page migration problem](/page-migration-problem/) and to prove lower bounds for it.
- **Lower bound searches.** Because work functions up to a constant form a finite set on small integer instances, a computer can search the game between the algorithm and the adversary over them, and find the exact ratio for small cases.

## References
