---
tag: 392NHT
kind: definition
slug: proportional-fairness
name: Proportional fairness
aliases:
- proportional fair allocation
- proportionally fair rate allocation
area: systems/networking-algorithms
level: advanced
summary: A feasible rate allocation in which any other feasible allocation lowers the sum of the proportional changes. It is the allocation that maximizes the sum of the logarithms of the rates.
prereqs: [max-min-fairness, utility-function]
see_also: [network-utility-maximization, proportional-fair-scheduling, tcp-vegas, tcp-reno, kkt-conditions, dual-decomposition, congestion-control, convex-optimization-problem]
sources:
  - paper: doi:10.1002/ett.4460080106
    title: Frank Kelly, Charging and rate control for elastic traffic, European Transactions on Telecommunications 8(1), 1997
    locator: pages 33 to 37 (the definition of proportional fairness and its weighted form)
  - paper: doi:10.1057/palgrave.jors.2600523
    title: Frank Kelly, Aman Maulloo and David Tan, Rate control for communication networks, shadow prices, proportional fairness and stability, Journal of the Operational Research Society 49(3), 1998
    locator: pages 237 to 252 (proportional fairness as the solution of the system problem with logarithmic utilities)
  - paper: doi:10.1109/90.879343
    title: Jeonghoon Mo and Jean Walrand, Fair end-to-end window-based congestion control, IEEE/ACM Transactions on Networking 8(5), 2000
    locator: pages 556 to 567 (alpha-fairness, with proportional fairness at alpha = 1 and max-min fairness as the limit)
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control and Stochastic Networks Perspective, Cambridge University Press, 2014
    locator: Chapter 2 (utility maximization, proportional fairness and alpha-fairness)
---

Proportional fairness is a rule for sharing network capacity, defined by Kelly in 1997. A feasible allocation of rates is proportionally fair if, compared with it, every other feasible allocation has a sum of proportional changes of at most zero: what some flows gain in percent, others lose at least as much in percent. When the feasible set is convex, this is the same as maximizing $\sum_s \log x_s$, the sum of the logarithms of the rates. Proportional fairness lies between the largest total rate and [max-min fairness](/max-min-fairness/): it gives less to flows that use many links, but never nothing.

## Definition

A network has links $\ell$ with capacities $c_\ell > 0$, and flows $s = 1, \ldots, n$ with fixed routes $L(s)$. The feasible set is

$$X = \Big\{ x \ge 0 : \sum_{s : \ell \in L(s)} x_s \le c_\ell \text{ for every link } \ell \Big\},$$

and every flow uses at least one link. More generally, $X$ can be any convex and compact set of rate vectors.

**Proportionally fair.** A vector $x^* \in X$ with all $x^*_s > 0$ is proportionally fair if for every $x \in X$

$$\sum_{s=1}^{n} \frac{x_s - x^*_s}{x^*_s} \le 0.$$

**Weighted.** With weights $w_s > 0$, $x^*$ is proportionally fair with weights $w$ if $\sum_s w_s (x_s - x^*_s)/x^*_s \le 0$ for every $x \in X$. Kelly reads $w_s$ as the price per unit time that user $s$ is willing to pay.

**The equivalent optimization.** For convex $X$, $x^*$ is proportionally fair with weights $w$ if and only if it maximizes $U(x) = \sum_s w_s \log x_s$ over $X$. The reason is the first-order condition for a concave function on a convex set: $x^*$ maximizes $U$ exactly when $\nabla U(x^*) \cdot (x - x^*) \le 0$ for all $x \in X$, and $\partial U/\partial x_s = w_s/x_s$. Since $U$ is strictly concave, the proportionally fair vector is unique. By the [KKT conditions](/kkt-conditions/), it has link prices $p_\ell \ge 0$, positive only on full links, with

$$x^*_s = \frac{w_s}{\sum_{\ell \in L(s)} p_\ell}.$$

So each flow pays the sum of the prices on its route per unit of rate, and gets a rate proportional to what it pays.

**Alpha-fairness.** Mo and Walrand put proportional fairness in a family. For $\alpha > 0$, the $\alpha$-fair vector maximizes $\sum_s w_s\, x_s^{1-\alpha}/(1 - \alpha)$ over $X$, with $w_s \log x_s$ in place of the term at $\alpha = 1$. The value $\alpha \to 0$ gives the largest total rate, $\alpha = 1$ gives proportional fairness, and $\alpha \to \infty$ gives max-min fairness.

## Examples and non-examples

**The linear network.** One long flow uses links $1, \ldots, n$, and one short flow uses each link alone. All capacities are 1. By symmetry the short flows have the same rate $y$, and each link is full, so the long flow has $1 - y$. Maximize $\log(1 - y) + n \log y$: the derivative $-1/(1 - y) + n/y$ is zero at $y = n/(n+1)$. So the long flow gets $1/(n+1)$ and each short flow gets $n/(n+1)$. The prices are $p_\ell = (n+1)/n$, and the long flow pays $n$ of them, so its rate is $1/(n \cdot (n+1)/n) = 1/(n+1)$.

For $n = 2$, $x^* = (1/3, 2/3, 2/3)$, with the long flow first. For any feasible $x$,

$$\frac{x_0 - 1/3}{1/3} + \frac{x_1 - 2/3}{2/3} + \frac{x_2 - 2/3}{2/3} = \tfrac{3}{2}(x_0 + x_1) + \tfrac{3}{2}(x_0 + x_2) - 3 \le \tfrac{3}{2} + \tfrac{3}{2} - 3 = 0,$$

by the two link constraints, so $x^*$ satisfies the definition.

**Non-example: max-min fairness.** The max-min fair vector of the same network is $(1/2, 1/2, 1/2)$. The move to $(1/3, 2/3, 2/3)$ gives the proportional changes $-1/3$, $+1/3$ and $+1/3$, with sum $1/3 > 0$. So the max-min fair vector is not proportionally fair.

**Non-example: the largest total.** The vector $(0, 1, 1)$ has the largest total rate, 2, but the long flow gets nothing, and the definition needs $x^*_s > 0$. Its sum of logarithms is $-\infty$.

**The long flow under alpha-fairness.** In the linear network with $n$ links, the $\alpha$-fair rate of the long flow is $1/(1 + n^{1/\alpha})$:

| $n$ | $\alpha = 0.5$ | $\alpha = 1$ | $\alpha = 2$ | $\alpha = 4$ | $\alpha = 16$ | $\alpha \to \infty$ |
|---|---|---|---|---|---|---|
| 2 | 0.2000 | 0.3333 | 0.4142 | 0.4568 | 0.4892 | 0.5 |
| 5 | 0.0385 | 0.1667 | 0.3090 | 0.4007 | 0.4749 | 0.5 |
| 10 | 0.0099 | 0.0909 | 0.2403 | 0.3599 | 0.4641 | 0.5 |

## Related definitions

- **[Max-min fairness](/max-min-fairness/)** protects the smallest rate first. It is the limit of $\alpha$-fairness for large $\alpha$, and it gives the long flow of the linear network $1/2$ for every $n$.
- **[Network utility maximization](/network-utility-maximization/)** is the general problem of maximizing $\sum_s U_s(x_s)$ over $X$. Proportional fairness is the case $U_s = w_s \log x_s$, and Kelly, Maulloo and Tan give decentralized rate controls that reach it.
- **[Proportional fair scheduling](/proportional-fair-scheduling/)** is a different thing with a similar name: a scheduler for a wireless link with changing channel rates, which picks the user with the largest ratio of current rate to average rate. This page is about a static allocation of link capacities.
- **TCP Vegas.** In equilibrium, [TCP Vegas](/tcp-vegas/) reaches a weighted proportionally fair allocation, with queueing delay as the price.
- **[Pareto optimality](/pareto-optimality/).** A proportionally fair vector is Pareto optimal, because any vector that is at least as large in every entry and larger in one would make the sum in the definition positive.

## References
