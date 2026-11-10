---
tag: 7AHTMQ
kind: problem
slug: metrical-task-systems
name: Metrical task systems
aliases:
- MTS
- metrical task system
- metrical task system problem
area: online-and-streaming/competitive-analysis
level: advanced
summary: Choose a state in a metric space for each task, paying a task cost plus the movement between states.
prereqs: [competitive-ratio, online-algorithm, offline-optimum, metric-space]
see_also: [work-function, work-function-algorithm, metrical-service-systems, k-server-problem, page-migration-problem, paging-problem, randomized-online-algorithm, metric-tree-embedding]
sources:
  - paper: "Allan Borodin, Nathan Linial and Michael E. Saks, An optimal on-line algorithm for metrical task system, Journal of the ACM 39(4) (1992), 745-763"
    title: "Borodin, Linial and Saks, An optimal on-line algorithm for metrical task system (1992)"
    locator: the definition of a metrical task system, the lower bound 2n - 1 for every deterministic algorithm on every n-state metric, the matching upper bound, and the randomized bounds 2H_n and H_n on the uniform metric
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: the chapter on metrical task systems (the model, the cruel adversary, work functions and the work function algorithm)
  - url: https://arxiv.org/abs/cs/0406034
    title: "Amos Fiat and Manor Mendel, Better algorithms for unfair metrical task systems and applications, SIAM Journal on Computing 32(6) (2003)"
    locator: the randomized bounds O(log n log log n) on hierarchically well separated trees and O((log n log log n)^2) on every metric
  - url: https://arxiv.org/abs/1807.04404
    title: "Sebastien Bubeck, Michael B. Cohen, James R. Lee and Yin Tat Lee, Metrical task systems on trees via mirror descent and unfair gluing, SODA 2019"
    locator: the randomized bounds O(log n) on HSTs and O(log^2 n) on every n-point metric
  - url: https://arxiv.org/abs/2211.05753
    title: "Sebastien Bubeck, Christian Coester and Yuval Rabani, The randomized k-server conjecture is false!, STOC 2023"
    locator: the lower bound Omega(log^2 n) for randomized MTS algorithms on some n-point metrics
---

A metrical task system (MTS) is an online problem on a finite [metric space](/metric-space/) of $n$ states. Tasks arrive one at a time. Each task gives a processing cost for every state, and the algorithm must choose a state for the task before it sees the next one. It pays the distance it moves plus the cost of the task in the new state. Borodin, Linial and Saks defined the model in 1987 (journal version 1992) and proved that the best deterministic [competitive ratio](/competitive-ratio/) is exactly $2n - 1$ on every metric with $n$ states. With randomization the answer is $\Theta(\log^2 n)$ in the worst case over metrics. The model contains [paging](/paging-problem/), the [k-server problem](/k-server-problem/) and many other online problems as special cases.

## In plain words

A machine can be in one of a few modes. Changing from one mode to another costs time, and the cost depends on the two modes. Jobs arrive one at a time. Each job runs fast in some modes and slowly in others. Before each job you choose the mode, and you do not know the next jobs.

If you change mode at every job, the change costs can be large. If you never change, a bad run of jobs can cost a lot. A good rule changes mode only after it has paid about as much in job costs as the change would cost. The best rule that never guesses pays at most about twice the number of modes times the best possible cost in hindsight, and no rule that never guesses can do better.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $S$, $d$ | the set of states and a metric on it |
| $n$ | the number of states, $n = \lvert S \rvert$ |
| $\sigma = r_1, \ldots, r_m$ | the request sequence: $m$ tasks |
| $r_t(x)$ | the cost of task $t$ in state $x$, in $[0, \infty]$ |
| $s_0$ | the start state, the same for the algorithm and the optimum |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the cost of the online algorithm and of the optimal offline schedule |
| $c$ | the competitive ratio |
| $D$, $\delta$ | the largest and the smallest distance between two distinct states |

**Input.** A metric space $(S, d)$ with $n$ states, a start state $s_0$, and tasks $r_1, \ldots, r_m$ that arrive online. Each task is a vector $r_t : S \to [0, \infty]$.

**Output.** States $s_1, \ldots, s_m$. The algorithm must fix $s_t$ after it sees $r_t$ and before it sees $r_{t+1}$.

**Cost.** $\mathrm{cost}(s_1, \ldots, s_m) = \sum_{t=1}^{m} \big( d(s_{t-1}, s_t) + r_t(s_t) \big)$.

**Competitive ratio.** A deterministic algorithm is $c$-competitive if there is a constant $b$, which may depend on the metric but not on $\sigma$, with $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$. The bounds below use such a constant $b$ (it is not $0$). For a randomized algorithm, $\mathbb{E}[\mathrm{ALG}(\sigma)]$ replaces $\mathrm{ALG}(\sigma)$, against an [oblivious adversary](/oblivious-adversary/) unless the text says otherwise.

**The offline optimum.** $\mathrm{OPT}(\sigma) = \min_x w_m(x)$, where the [work function](/work-function/) is $w_0(x) = d(s_0, x)$ and

$$w_t(x) = \min_{y \in S} \big( w_{t-1}(y) + r_t(y) + d(y, x) \big).$$

The value $w_t(x)$ is the least cost to serve $r_1, \ldots, r_t$ and end in state $x$. The recurrence is a dynamic program with $O(m n^2)$ time, so OPT is easy to compute offline.

## Variants

- **Metrical service systems.** Every cost is $0$ or $\infty$, so a task is a set of allowed states. This is the [metrical service systems](/metrical-service-systems/) problem of Chrobak and Larmore.
- **Uniform MTS.** All distances are $1$. This is the case where the randomized bounds of order $\log n$ are tight.
- **Unfair MTS.** The online algorithm pays $\alpha$ times the task cost of the optimum, or the optimum pays a different distance. Bartal, Blum, Burch and Tomkins, Seiden, and Fiat and Mendel use it as a step to glue the solutions of subspaces of a tree metric.
- **Infinite state spaces.** The [k-server problem](/k-server-problem/) on a metric $M$ is an MTS whose states are the configurations of $k$ servers. The [page migration problem](/page-migration-problem/) is a task system with a different cost structure, a "relaxed task system".
- **Related problems.** Convex function chasing replaces $S$ by $\mathbb{R}^d$ and the tasks by convex functions. MTS with predictions, and MTS in the experts setting, ask for regret against a fixed state.

## Examples

**Three states on a line.** Let the states $a, b, c$ be the points $0, 1, 3$ on a line, so $d(a, b) = 1$, $d(b, c) = 2$ and $d(a, c) = 3$. Start in $a$. The tasks, as vectors $(r(a), r(b), r(c))$, and the work functions are:

| $t$ | $r_t$ | $w_t = (w_t(a), w_t(b), w_t(c))$ | $\min_x w_t(x)$ |
|---|---|---|---|
| 0 | | $(0, 1, 3)$ | $0$ |
| 1 | $(2, 0, 5)$ | $(2, 1, 3)$ | $1$ |
| 2 | $(0, 3, 1)$ | $(2, 3, 4)$ | $2$ |
| 3 | $(4, 1, 0)$ | $(5, 4, 4)$ | $4$ |
| 4 | $(0, 0, 3)$ | $(5, 4, 6)$ | $4$ |

So $\mathrm{OPT} = 4$, for example with the schedule $a, a, b, b$ or $a, a, c, b$. The rule "never move" pays $2 + 0 + 4 + 0 = 6$. The [work function algorithm](/work-function-algorithm/) stays in $a$ for tasks 1 and 2, moves to $b$ for task 3 and stays there for task 4. It pays $2 + 0 + (1 + 1) + 0 = 4$.

**The cruel adversary on two states.** Let $S = \{0, 1\}$ with $d(0, 1) = 1$. Each task costs $\varepsilon = 1/2$ in the current state of the algorithm and $0$ in the other state. The work function algorithm behaves as follows:

| $t$ | $w_t$ | the move | $\mathrm{ALG}$ so far | $\mathrm{OPT}$ so far |
|---|---|---|---|---|
| 1 | $(1/2, 1)$ | stays in 0 | $1/2$ | $1/2$ |
| 2 | $(1, 1)$ | stays in 0 | $1$ | $1$ |
| 3 | $(3/2, 1)$ | stays in 0 | $3/2$ | $1$ |
| 4 | $(2, 1)$ | stays in 0 | $2$ | $1$ |
| 5 | $(2, 1)$ | moves to 1 | $3$ | $1$ |
| 6 | $(2, 3/2)$ | stays in 1 | $7/2$ | $3/2$ |
| 7 | $(2, 2)$ | stays in 1 | $4$ | $2$ |
| 8 | $(2, 5/2)$ | stays in 1 | $9/2$ | $2$ |
| 9 | $(2, 3)$ | stays in 1 | $5$ | $2$ |
| 10 | $(2, 3)$ | moves to 0 | $6$ | $2$ |

Each cycle of five tasks costs the algorithm $3$ and the optimum $1$, so the ratio tends to $3 = 2n - 1$. The algorithm pays $2$ in task costs, which is twice the distance, before it moves.

**Special cases.** [Paging](/paging-problem/) with $k$ pages in a cache and $k + 1$ pages in total is an MTS with $k + 1$ states (the missing page) and the uniform metric: a request to the missing page has cost $\infty$ in that state and $0$ elsewhere. [List update](/list-update-problem/) on $\ell$ items is an MTS on the $\ell!$ orders, with the number of inversions as the metric, if all exchanges are paid. These embeddings give weak bounds, because $n$ is large, but they show what the model covers.

## Known algorithms

- **Work function algorithm (WFA).** Move to a state $x$ that minimizes $w_t(x) + d(s_{t-1}, x)$, with $w_t(x) = w_{t-1}(x) + r_t(x)$. It is $(2n - 1)$-competitive on every metric, which is optimal for deterministic algorithms. See [work function algorithm](/work-function-algorithm/) and the proof below.
- **Traversal rules.** BLS also gave a simpler rule that visits the states in a fixed order along a spanning tree, and leaves a state when the task cost paid there reaches the length of the edge to the next state. Its ratio is $O(n)$, with a larger constant than $2n - 1$.
- **Randomized algorithms on the uniform metric.** BLS gave a randomized algorithm for the uniform metric that is $2 H_n$-competitive against an oblivious adversary, where $H_n = \sum_{i=1}^{n} 1/i$ is the [harmonic number](/harmonic-series/). It uses the same idea as randomized marking for paging: leave a state only when its task cost has grown, and then go to a random state that is still cheap.
- **Randomized algorithms on general metrics.** Embed the metric into a random hierarchically well separated tree with distortion $O(\log n)$ ([FRT embedding](/frt-tree-embedding/)), and solve MTS on the tree. Bartal, Blum, Burch and Tomkins (1997) got the first polylogarithmic ratio. Fiat and Mendel (2003) reached $O((\log n \log\log n)^2)$. Bubeck, Cohen, Lee and Lee (2019) used mirror descent with an entropic regularizer and got $O(\log n)$ on HSTs and $O(\log^2 n)$ on every metric. Coester and Lee (2019) gave a simpler entropic algorithm with the same bounds.

## Bounds

All bounds count the ratio $c$ with an additive constant $b$ that depends on the metric only.

| Setting | Lower bound | Upper bound |
|---|---|---|
| deterministic, every metric with $n$ states | $2n - 1$ (BLS 1992) | $2n - 1$ (BLS 1992) |
| randomized, oblivious, uniform metric | $H_n$ (BLS 1992) | $2H_n$ (BLS 1992); $H_n + O(\sqrt{\log n \log\log n})$ (Irani and Seiden 1998) |
| randomized, oblivious, HSTs | | $O(\log n)$ (Bubeck, Cohen, Lee and Lee 2019) |
| randomized, oblivious, every metric | $\Omega(\log n / \log\log n)$ (Bartal, Linial, Mendel and Naor 2005) | $O(\log^2 n)$ (Bubeck, Cohen, Lee and Lee 2019) |
| randomized, oblivious, worst metric | $\Omega(\log^2 n)$ (Bubeck, Coester and Rabani 2023) | $O(\log^2 n)$ |

The lower bound of Bubeck, Coester and Rabani holds for some $n$-point metrics, so $\Theta(\log^2 n)$ is the answer for the worst metric. Against an [adaptive offline adversary](/adaptive-offline-adversary/), randomization does not help, so the deterministic bound $2n - 1$ holds there too (Ben-David, Borodin, Karp, Tardos and Wigderson 1994).

**Theorem 1 (upper bound).** Let the work function algorithm choose $s_t$ among the states $x$ that minimize $w_t(x) + d(s_{t-1}, x)$, and among those a state with $w_t(s_t) = w_{t-1}(s_t) + r_t(s_t)$. Such a state exists, and then $\mathrm{ALG}(\sigma) \le (2n - 1)\,\mathrm{OPT}(\sigma) + 2nD$.

*Proof.* Two facts follow from the recurrence. *Lipschitz:* $w_t(x) \le w_t(y) + d(y, x)$, since a schedule that ends in $y$ can move to $x$. *Monotone:* $w_t \ge w_{t-1}$, since the costs are nonnegative and $w_{t-1}(y) + d(y, x) \ge w_{t-1}(x)$ by the Lipschitz property.

*Existence.* Take a minimizer $x^*$ of $w_t(x) + d(s_{t-1}, x)$. Take $y$ that achieves the minimum in $w_t(x^*) = w_{t-1}(y) + r_t(y) + d(y, x^*)$. Then $w_t(y) \le w_{t-1}(y) + r_t(y) = w_t(x^*) - d(y, x^*) \le w_t(y)$, so equality holds, and $w_t(y) + d(s_{t-1}, y) \le w_t(x^*) - d(y, x^*) + d(s_{t-1}, y) \le w_t(x^*) + d(s_{t-1}, x^*)$. So $y$ is also a minimizer, and it has the support property.

*Potential.* Let $\Phi_t = 2 \sum_{x} w_t(x) - w_t(s_t)$. Write $w = w_{t-1}$, $w' = w_t$, $s = s_{t-1}$ and $s' = s_t$. The choice of $s'$ against the candidate $s$ gives $w'(s') + d(s, s') \le w'(s)$. With $r_t(s') = w'(s') - w(s')$, the cost of the step is

$$d(s, s') + r_t(s') \le w'(s) - w'(s') + w'(s') - w(s') = w'(s) - w(s').$$

The change of the potential is $\Phi_t - \Phi_{t-1} = 2 \sum_x (w'(x) - w(x)) - w'(s') + w(s)$. So the step cost is at most the change of $\Phi$ if $(w'(s) - w(s)) + (w'(s') - w(s')) \le 2 \sum_x (w'(x) - w(x))$. Every term $w'(x) - w(x)$ is nonnegative. If $s' \ne s$, the left side has two different terms of the sum. If $s' = s$, it is twice one term. In both cases the inequality holds.

*Sum.* So $\mathrm{ALG}(\sigma) \le \Phi_m - \Phi_0$. Here $\Phi_0 = 2 \sum_x d(s_0, x) \ge 0$. Let $L = \min_x w_m(x) = \mathrm{OPT}(\sigma)$. By the Lipschitz property $w_m(x) \le L + D$ for every $x$, and $w_m(s_m) \ge L$. So $\Phi_m \le 2n(L + D) - L = (2n - 1) L + 2nD$. $\square$

**Theorem 2 (lower bound, BLS).** Let $(S, d)$ be any metric with $n \ge 2$ states. For every deterministic online algorithm and every $c < 2n - 1$, there is no constant $b$ with $\mathrm{ALG}(\sigma) \le c\,\mathrm{OPT}(\sigma) + b$ for all $\sigma$.

*Proof.* Fix $\varepsilon > 0$. The *cruel adversary* knows the algorithm, so it knows the current state $a$ of the algorithm. It gives the task $r(a) = \varepsilon$ and $r(x) = 0$ for $x \ne a$. Use the same potential $\Phi = 2 \sum_x w(x) - w(s)$, with $s$ the state of the online algorithm, and let $\delta > 0$ be the smallest distance.

*Effect of one task.* For $x \ne a$, the candidate $y = x$ in the recurrence gives $w'(x) \le w(x)$, and monotonicity gives equality. Only $w(a)$ can change: $w'(a) = w(a) + \eta$ with $0 \le \eta \le \varepsilon$.

*Stay in $a$.* The algorithm pays $\varepsilon$, and $\Delta\Phi = 2\eta - \eta = \eta \le \varepsilon$.

*Move to $b \ne a$.* The algorithm pays $d(a, b)$, and $\Delta\Phi = 2\eta - w(b) + w(a) \le 2\varepsilon + d(a, b) \le d(a, b)\,(1 + 2\varepsilon/\delta)$, by the Lipschitz property and $d(a, b) \ge \delta$.

So each step has $\Delta\Phi \le (1 + 2\varepsilon/\delta) \cdot \mathrm{cost}$, and after $m$ tasks $(1 + 2\varepsilon/\delta)\,\mathrm{ALG} \ge \Phi_m - \Phi_0$. With $L = \mathrm{OPT}$ as before, $\Phi_m \ge 2nL - (L + D) = (2n - 1)L - D$. So

$$\Big(1 + \frac{2\varepsilon}{\delta}\Big)\,\mathrm{ALG} \ge (2n - 1)\,\mathrm{OPT} - D - \Phi_0 .$$

Each step costs the algorithm at least $\min(\varepsilon, \delta)$, so $\mathrm{ALG} \to \infty$ as $m \to \infty$. If $\mathrm{OPT}$ stays bounded, $\mathrm{ALG} - c\,\mathrm{OPT} \to \infty$. If $\mathrm{OPT} \to \infty$, choose $\varepsilon$ so small that $(2n - 1)/(1 + 2\varepsilon/\delta) > c$, and again $\mathrm{ALG} - c\,\mathrm{OPT} \to \infty$. $\square$

The bound does not depend on the shape of the metric. This is the main surprise of the BLS paper: on a line, a star or a uniform space with $n$ points, the deterministic answer is the same $2n - 1$.

## Reductions

- **Paging and k-server.** The k-server problem on $N$ points is an MTS on the $\binom{N}{k}$ configurations, so Theorem 1 gives a ratio of order $\binom{N}{k}$. The [work function algorithm](/work-function-algorithm/) for k-server uses the same work function on configurations, and Koutsoupias and Papadimitriou proved $2k - 1$ for it, which is far better than the MTS bound.
- **Metrical service systems.** An MSS is an MTS with costs in $\{0, \infty\}$. The $2n - 1$ bound of MTS does not apply directly to the infinite costs, and MSS has its own bounds in terms of the request width.
- **Tree embeddings.** A randomized algorithm on HSTs with ratio $c$ gives ratio $O(c \log n)$ on every metric, through a probabilistic tree embedding with distortion $O(\log n)$. This is how $O(\log n)$ on HSTs gives $O(\log^2 n)$ on every metric.
- **Experts.** If the movement cost is $0$, an MTS on the uniform metric becomes the experts problem with a switching cost, and [multiplicative weights](/multiplicative-weights-update/) is the analogue of the randomized algorithms.

## Applications

- **Power management.** A device with sleep states, where waking up costs energy and each state has a running cost, is an MTS on a line. The [ski rental problem](/ski-rental-problem/) is close to the case of two states.
- **Process migration and data placement.** Moving a process or a file between machines pays the distance, and each request pays according to the location. The [page migration problem](/page-migration-problem/) is the version for one file.
- **Self-adjusting data structures.** A data structure that can change its shape, at a price, to serve queries more cheaply is an MTS on its shapes, as in list update.
- **A test bed for techniques.** Work functions, potential arguments, tree embeddings and mirror descent with entropy were all developed or tested first on MTS.

## References
