---
tag: AXWXEX
kind: definition
slug: max-min-fairness
name: Max-min fairness
aliases:
- max-min fair allocation
- max-min fair share
area: systems/networking-algorithms
level: intro
summary: A feasible allocation of rates in which no flow can get more without taking from a flow that has the same rate or less. Progressive filling computes it.
prereqs: [pareto-optimality]
see_also: [proportional-fairness, network-utility-maximization, fair-queueing, generalized-processor-sharing, dominant-resource-fairness, congestion-control, aimd, weighted-fair-queueing]
sources:
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: Section 6.5 (fairness, max-min fair flow control, the bottleneck characterization and the filling algorithm)
  - paper: doi:10.1109/90.879343
    title: Jeonghoon Mo and Jean Walrand, Fair end-to-end window-based congestion control, IEEE/ACM Transactions on Networking 8(5), 2000
    locator: pages 556 to 567 (alpha-fair allocations, with max-min fairness as the limit for large alpha)
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control and Stochastic Networks Perspective, Cambridge University Press, 2014
    locator: Chapter 2 (fairness of resource allocations, among them max-min fairness)
---

Max-min fairness is a rule for sharing the capacity of a network between flows. An allocation of rates is max-min fair when it is feasible and no flow can get a higher rate without lowering the rate of a flow that has the same rate or less. So the network first makes the smallest rate as large as it can, then the next smallest, and so on. On one link with flows that all want more than their share, it is the equal split. In a network it is computed by *progressive filling*: raise all rates together until a link is full, freeze the flows on that link, and continue with the others.

## Definition

A network has links $\ell \in L$ with capacities $c_\ell > 0$, and flows $s \in S$, each with a fixed route, a set of links $L(s) \subseteq L$. A rate vector $x = (x_s)_{s \in S}$ is *feasible* if $x_s \ge 0$ for all $s$ and

$$\sum_{s : \ell \in L(s)} x_s \le c_\ell \quad \text{for every link } \ell.$$

**Max-min fair.** A feasible $x$ is max-min fair if for every feasible $y$ and every flow $s$ with $y_s > x_s$, there is a flow $t$ with $x_t \le x_s$ and $y_t < x_t$.

**Bottleneck.** Link $\ell$ is a bottleneck for flow $s$ under $x$ if $\ell \in L(s)$, the link is full ($\sum_{t : \ell \in L(t)} x_t = c_\ell$), and $x_s \ge x_t$ for every flow $t$ that uses $\ell$.

Bertsekas and Gallager prove three facts. A feasible $x$ is max-min fair if and only if every flow has a bottleneck. The max-min fair vector exists and is unique. Progressive filling computes it:

1. Start with all rates at 0 and all flows active.
2. Raise the rates of the active flows together until some link is full.
3. Freeze the flows that use a full link. If some flow is still active, go to step 2.

Each round fills at least one link, so there are at most $|L|$ rounds. When a flow is frozen, the full link is a bottleneck for it, because no flow on that link was raised further.

An equivalent statement: among all feasible vectors, the max-min fair one has the lexicographically largest vector of rates sorted from small to large. A flow with a limited demand $d_s$ fits the same definition through an extra link of capacity $d_s$ that only flow $s$ uses. *Weighted* max-min fairness with weights $w_s > 0$ applies the definition to the normalized rates $x_s / w_s$.

## Examples and non-examples

**One link with demands.** A link of capacity 10 has three flows with demands 2, 4 and 10. Progressive filling raises all three to 2, where the first demand is met. Then the other two rise to 4, where the second demand is met. The last flow gets the remaining $10 - 2 - 4 = 4$. The max-min fair rates are $(2, 4, 4)$. The equal split $(10/3, 10/3, 10/3)$ is not feasible, because the first flow cannot use more than 2.

**A small network.** Links A, B and C have capacities 1, 2 and 3. Five flows use the routes $\{A\}$, $\{A, B\}$, $\{B\}$, $\{B, C\}$ and $\{C\}$.

| step | raise by | rates of flows 1 to 5 | left on A, B, C | full link |
|---|---|---|---|---|
| 1 | 1/2 | 1/2, 1/2, 1/2, 1/2, 1/2 | 0, 1/2, 2 | A: freeze flows 1 and 2 |
| 2 | 1/4 | 1/2, 1/2, 3/4, 3/4, 3/4 | 0, 0, 3/2 | B: freeze flows 3 and 4 |
| 3 | 3/2 | 1/2, 1/2, 3/4, 3/4, 9/4 | 0, 0, 0 | C: freeze flow 5 |

The max-min fair vector is $(1/2, 1/2, 3/4, 3/4, 9/4)$. Its sorted rates $(1/2, 1/2, 3/4, 3/4, 9/4)$ are lexicographically larger than those of any other feasible vector. Flows 1 and 2 have bottleneck A, flows 3 and 4 have bottleneck B, and flow 5 has bottleneck C.

**Non-example: Pareto optimal but not max-min fair.** In the same network, $x = (1, 0, 2, 0, 3)$ is feasible and Pareto optimal: every link is full, so no rate can grow without lowering another. But it is not max-min fair. Flow 2 can get $1/2$ if flow 1 gives up $1/2$ on link A and flow 3 gives up $1/2$ on link B, and both of them have larger rates than flow 2. Flow 2 has no bottleneck: A and B are full, but flow 2 does not have the largest rate on either of them.

**The linear network.** One long flow uses links $1, \ldots, n$, and one short flow uses each link alone. All capacities are 1. Every link has two flows, so progressive filling gives every flow $1/2$. The total is $(n + 1)/2$, while giving the long flow nothing gives the larger total $n$. Max-min fairness gives up total rate to protect the long flow. [Proportional fairness](/proportional-fairness/) gives the long flow $1/(n+1)$ here.

## Related definitions

- **[Pareto optimality](/pareto-optimality/).** Every max-min fair allocation is Pareto optimal, because each flow has a full bottleneck. The converse is false, as the non-example shows.
- **[Proportional fairness](/proportional-fairness/)** maximizes $\sum_s \log x_s$ instead. It favors flows that use few links.
- **Alpha-fairness.** Mo and Walrand define allocations that maximize $\sum_s x_s^{1 - \alpha}/(1 - \alpha)$. The value $\alpha = 1$ gives proportional fairness, and the limit $\alpha \to \infty$ gives max-min fairness. See [network utility maximization](/network-utility-maximization/).
- **Packet schedulers.** On one link, [generalized processor sharing](/generalized-processor-sharing/) and [fair queueing](/fair-queueing/) give the backlogged flows their max-min fair shares, and [weighted fair queueing](/weighted-fair-queueing/) gives the weighted shares.
- **[Dominant resource fairness](/dominant-resource-fairness/)** extends max-min fairness to users that need several resources, by applying it to each user's largest share of any resource.
- **Congestion control.** [AIMD](/aimd/) converges to the equal share on one link, which is the max-min fair point there.

## References
