---
tag: KQ7W60
kind: problem
slug: parametric-max-flow-problem
name: Parametric maximum flow problem
aliases:
- parametric flow
area: graphs/flows-and-cuts
level: research
summary: Compute maximum flows as capacities vary linearly with a parameter.
prereqs: [max-flow-problem, min-cut-problem, push-relabel]
see_also: [maximum-weight-closure, fractional-programming, parametric-search, submodular-function, hao-orlin, baseball-elimination, image-segmentation-graph-cuts, max-flow-min-cut-theorem]
sources:
  - paper: doi:10.1137/0218003
    title: Giorgio Gallo, Michael D. Grigoriadis and Robert E. Tarjan, A fast parametric maximum flow algorithm and applications, SIAM Journal on Computing 18(1), 30 to 55 (1989)
    locator: the whole paper (the monotone parametric model, the nesting of minimum cuts, the algorithm with the time of one push-relabel run, and the applications)
  - paper: doi:10.1287/opre.1080.0524
    title: Dorit S. Hochbaum, The pseudoflow algorithm, a new algorithm for the maximum-flow problem, Operations Research 56(4), 992 to 1009 (2008)
    locator: the parametric use of the pseudoflow algorithm
---

The parametric maximum flow problem asks for the [maximum flow](/max-flow-problem/) and [minimum cut](/min-cut-problem/) of a network whose capacities depend on a real parameter $\lambda$, for every value of $\lambda$ at once. In the *monotone* case studied by Gallo, Grigoriadis and Tarjan, the capacities of the edges out of the source do not decrease in $\lambda$, those of the edges into the sink do not increase, and all others are constant. Then the minimum cuts are nested as $\lambda$ grows, there are at most $n - 1$ distinct ones, and all of them, with the breakpoints of the cut function, can be found in the time of a single [push-relabel](/push-relabel/) run, $O(nm \log(n^2/m))$. This makes many ratio problems, such as the densest subgraph, as cheap as one maximum flow.

## In plain words

Some flow questions have a knob. Turning it up lets more come out of the source, or makes it cheaper to cut the links into the sink. For each knob setting there is a best flow and a cheapest cut, and you want to know them for every setting, or the setting where some condition changes.

The good news is that, in the common case where the knob only touches the links out of the source and into the sink, the cheapest cut moves in one direction only: as the knob goes up, the source side only grows. So there are few different answers, at most one per vertex, and a clever method finds all of them for the price of one ordinary flow computation, by reusing its work as the knob turns.

## Definition

**Input.** A directed graph $G = (V, E)$ with source $s$ and sink $t$, and capacities $c_\lambda(e) \ge 0$ that depend on a real parameter $\lambda$ in an interval $I$. Capacities and $\lambda$ are real. Parallel and antiparallel edges are allowed; each edge has its own capacity function, and the residual graph treats antiparallel pairs as separate edges.

**The monotone model.** For all edges:

- $c_\lambda(s, v)$ is nondecreasing in $\lambda$;
- $c_\lambda(v, t)$ is nonincreasing in $\lambda$;
- $c_\lambda(u, v)$ is constant for $u \ne s$ and $v \ne t$.

Reversing all edges and swapping $s$ with $t$ turns the opposite monotone direction into this one. The *linear* case has $c_\lambda(e) = a_e + b_e \lambda$.

**Output.** The function $\kappa(\lambda)$, the minimum cut capacity, which equals the maximum flow value, over $I$, together with a minimum cut for each piece. Common forms of the question: all breakpoints of $\kappa$; the largest $\lambda$ with $\kappa(\lambda) \ge$ a given bound; or the $\lambda$ where the minimum cut stops being $\{s\}$.

## Variants

- **Given values only.** Maximum flows for a sorted list $\lambda_1 < \cdots < \lambda_q$; this is the setting of the Gallo-Grigoriadis-Tarjan algorithm, which handles $q = O(n)$ values in the time of one push-relabel run when the values are processed in increasing order, or all in decreasing order.
- **All breakpoints.** In the linear case, $\kappa$ is the minimum of linear functions, one per cut, so it is piecewise linear and concave, and its breakpoints can be found by a divide-and-conquer search over $\lambda$.
- **Non-monotone parameters.** If interior edges depend on $\lambda$, the nesting can fail, and the number of breakpoints of $\kappa$ is no longer bounded by $n$; examples with exponentially many breakpoints are known.
- **Parametric minimum cut in undirected graphs** and parametric versions of other flow problems, such as [min-cost flow](/min-cost-flow-problem/) with a parameter in the costs.

## Examples

**A small linear instance.** The network has $s \to a$ and $s \to b$ of capacity $\lambda$, $a \to b$ of capacity 1, $a \to t$ of capacity 1 and $b \to t$ of capacity 4, for $\lambda \ge 0$. The four cuts give

| source side $S$ | capacity |
|---|---|
| $\{s\}$ | $2\lambda$ |
| $\{s, a\}$ | $\lambda + 1 + 1 = \lambda + 2$ |
| $\{s, b\}$ | $\lambda + 4$ |
| $\{s, a, b\}$ | $1 + 4 = 5$ |

So $\kappa(\lambda) = 2\lambda$ on $[0, 2]$, $\lambda + 2$ on $[2, 3]$ and $5$ for $\lambda \ge 3$. The minimum cuts $\{s\} \subset \{s, a\} \subset \{s, a, b\}$ grow with $\lambda$, and $\kappa$ is concave with breakpoints 2 and 3.

**A zero-capacity edge.** At $\lambda = 0$ the source edges above have capacity 0, and $\kappa(0) = 0$ with the cut $\{s\}$. An edge of capacity 0 for all $\lambda$ never matters.

**No $s$-$t$ path.** If $G$ has no $s$-$t$ path, $\kappa(\lambda) = 0$ for all $\lambda$, and the set of vertices that $s$ reaches is a minimum cut throughout.

## Known algorithms

| method | time | notes |
|---|---|---|
| one maximum flow per value | $q$ times a max flow | no reuse |
| Gallo-Grigoriadis-Tarjan | $O(nm \log(n^2/m))$ for $O(n)$ values or all breakpoints | push-relabel, warm-started; for all breakpoints it runs from both ends of the parameter range |
| pseudoflow (Hochbaum) | the time of one pseudoflow run | also warm-started |
| binary or Newton search on $\lambda$ | $O(\log)$ or few max flows | for one target value only; see [parametric search](/parametric-search/) |

**Why warm starts work.** When $\lambda$ grows, the capacities of source edges grow and those of sink edges shrink. Push-relabel keeps a preflow and valid distance labels. Raising a source edge's capacity and saturating it keeps the labels valid, since the source has label $n$ and its edges are saturated. Lowering a sink edge's capacity below its flow is fixed by reducing the flow on it, which only creates excess at a vertex, which a preflow allows. Edges into $t$ have label 0 at their head and stay valid. So the next run starts from the old labels, and since labels only grow, the total work over all values is bounded like a single run.

## Bounds

**Nesting.** Fix $\lambda_1 < \lambda_2$, and let $S_1$ be the minimal minimum cut at $\lambda_1$ and $S_2$ any minimum cut at $\lambda_2$. Then $S_1 \subseteq S_2$. *Proof.* Write $g(S) = c_{\lambda_2}(S) - c_{\lambda_1}(S)$. Only source and sink edges differ, so $g(S) = \sum_{v \notin S} \Delta_{s v} + \sum_{v \in S} \Delta_{v t}$, where $\Delta_{sv} \ge 0$ and $\Delta_{vt} \le 0$ are the changes. Adding a vertex to $S$ removes a nonnegative term and adds a nonpositive one, so $g$ does not increase as $S$ grows; in particular $g(S_1 \cup S_2) \le g(S_2)$. The cut function is [submodular](/submodular-function/), so

$$c_{\lambda_1}(S_1 \cap S_2) + c_{\lambda_2}(S_1 \cup S_2) \le c_{\lambda_1}(S_1) + c_{\lambda_1}(S_2) + g(S_1 \cup S_2) \le c_{\lambda_1}(S_1) + c_{\lambda_2}(S_2).$$

Since $c_{\lambda_2}(S_1 \cup S_2) \ge c_{\lambda_2}(S_2)$, this gives $c_{\lambda_1}(S_1 \cap S_2) \le c_{\lambda_1}(S_1)$, so $S_1 \cap S_2$ is a minimum cut at $\lambda_1$, and by the minimality of $S_1$, $S_1 \cap S_2 = S_1$. $\square$

So the minimal minimum cuts form a chain of sets that hold $s$ and not $t$, and there are at most $n - 1$ distinct ones. In the linear case $\kappa$ is the minimum of the linear capacity functions of these cuts over their ranges, so it is concave and piecewise linear with at most $n - 2$ breakpoints. Without monotonicity, neither bound holds.

## Reductions

- **Densest subgraph.** To maximize $|E(S)| / |S|$ over nonempty $S$, ask for each $\lambda$ whether some $S$ has $|E(S)| - \lambda |S| > 0$. This is a [maximum-weight closure](/maximum-weight-closure/) problem: a node for each edge with weight 1, a node for each vertex with weight $-\lambda$, and each edge node requires its two ends. Only the sink capacities depend on $\lambda$, monotonically, so one parametric run finds the optimum ratio.
- **Ratio problems in general.** Maximizing $a(S) / b(S)$ over closures with $b > 0$ becomes the parametric question of the sign of $\max_S a(S) - \lambda b(S)$, the approach of [fractional programming](/fractional-programming/).
- **Selection and scheduling.** Problems in Gallo, Grigoriadis and Tarjan's paper include scheduling with deadlines on identical machines, and the lexicographically optimal flow.
- **Baseball elimination.** Asking how many more wins a team needs is a parametric question over the [baseball elimination](/baseball-elimination/) network.

## Applications

- Densest subgraph and community detection.
- Image segmentation and labeling, where a parameter weighs data against smoothness; see [graph cuts](/image-segmentation-graph-cuts/).
- Open-pit mining with a parameter for the price of ore.
- Sensitivity analysis: how the maximum flow changes as some supplies or demands grow.

## References
