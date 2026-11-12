---
tag: RJ5067
kind: problem
slug: network-utility-maximization
name: Network utility maximization
aliases:
- NUM
- network utility maximization problem
area: systems/networking-algorithms
level: advanced
summary: Choose the rates of flows with fixed routes so that the sum of their concave utilities is largest, subject to the capacities of the links. Link prices from the dual give decentralized rate controls.
prereqs: [proportional-fairness, dual-decomposition, convex-optimization-problem]
see_also: [max-min-fairness, congestion-control, tcp-vegas, ecn, active-queue-management, backpressure-routing, kkt-conditions, lagrangian-duality]
sources:
  - paper: doi:10.1002/ett.4460080106
    title: Frank Kelly, Charging and rate control for elastic traffic, European Transactions on Telecommunications 8(1), 1997
    locator: pages 33 to 37 (the system problem and its split into user problems and a network problem)
  - paper: doi:10.1057/palgrave.jors.2600523
    title: Frank Kelly, Aman Maulloo and David Tan, Rate control for communication networks, shadow prices, proportional fairness and stability, Journal of the Operational Research Society 49(3), 1998
    locator: pages 237 to 252 (the primal and dual rate control algorithms and their stability by Lyapunov functions)
  - paper: doi:10.1109/90.811451
    title: Steven H. Low and David E. Lapsley, Optimization flow control I, basic algorithm and convergence, IEEE/ACM Transactions on Networking 7(6), 1999
    locator: pages 861 to 874 (the dual problem, the gradient projection algorithm for the link prices, and its convergence for a small step size)
  - paper: doi:10.1109/90.879343
    title: Jeonghoon Mo and Jean Walrand, Fair end-to-end window-based congestion control, IEEE/ACM Transactions on Networking 8(5), 2000
    locator: pages 556 to 567 (the alpha-fair utility functions)
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control and Stochastic Networks Perspective, Cambridge University Press, 2014
    locator: Chapter 2 (network utility maximization, primal and dual algorithms, and the relation to TCP)
  - paper: doi:10.1145/506147.506152
    title: Steven H. Low, Larry L. Peterson and Limin Wang, Understanding TCP Vegas, a duality model, Journal of the ACM 49(2), 2002
    locator: pages 207 to 235 (TCP Vegas as a dual algorithm with queueing delay as the price)
---

Network utility maximization (NUM) is the problem of choosing the rates of flows in a network so that the total utility is as large as possible, without exceeding the capacity of any link. Each flow has a fixed route and a concave utility function of its rate. Kelly framed rate control this way in 1997, and with Maulloo and Tan in 1998 he showed that the dual variables of the link constraints act as prices that the network can compute locally and the sources can respond to locally. Low and Lapsley gave the dual gradient algorithm in 1999. The choice of the utility sets the fairness: logarithms give [proportional fairness](/proportional-fairness/), and the limit of the $\alpha$-fair family gives [max-min fairness](/max-min-fairness/).

## In plain words

Many users send data through a network of links, and each link has a speed limit. Each user is happier with more speed, but less so for each extra unit. The goal is to choose the speed of each user so that the total happiness is as large as possible and no link is overloaded.

No one needs to solve this centrally. Each link puts a price on its use: the price goes up when too much data wants to pass, and down when the link has room. Each user adds up the prices along its path and picks the speed that is best for it at that total price. When the prices settle, the speeds solve the problem.

## Definition

**Input.** A set of links $L$ with capacities $c_\ell > 0$. A set of sources $S$. Source $s$ uses a fixed route $L(s) \subseteq L$. The routing matrix $R$ has $R_{\ell s} = 1$ if $\ell \in L(s)$ and 0 otherwise. Each source has a utility $U_s$ that is increasing, strictly concave and continuously differentiable on an interval $I_s$ of rates, for example $I_s = [m_s, M_s]$.

**Problem.**

$$\max_{x} \sum_{s \in S} U_s(x_s) \quad\text{subject to}\quad R x \le c, \quad x_s \in I_s.$$

**Output.** The optimal rate vector $x^*$. It is unique, because the objective is strictly concave and the feasible set is convex.

**The dual.** With a price $p_\ell \ge 0$ for each link, and the route price $q_s = \sum_{\ell \in L(s)} p_\ell$, the dual function is

$$D(p) = \sum_{s} \max_{x_s \in I_s} \big( U_s(x_s) - x_s q_s \big) + \sum_\ell p_\ell c_\ell.$$

The inner problems separate: source $s$ needs only its own route price, and its best rate is $x_s(q_s) = U_s'^{-1}(q_s)$, clipped to $I_s$. The problem is convex with linear constraints, so the dual minimum equals the primal maximum. At the optimum, $p_\ell > 0$ only on full links. The method is [dual decomposition](/dual-decomposition/), and the optimality conditions are the [KKT conditions](/kkt-conditions/).

## Variants

- **Weighted and $\alpha$-fair utilities.** $U_s(x) = w_s\, x^{1-\alpha}/(1-\alpha)$, with $w_s \log x$ for $\alpha = 1$. These are the utilities of Mo and Walrand.
- **Primal form with penalties.** Kelly, Maulloo and Tan also use a soft version: maximize $\sum_s U_s(x_s) - \sum_\ell \int_0^{y_\ell} f_\ell(z)\, dz$, where $y_\ell$ is the load of link $\ell$ and $f_\ell$ is a price that grows with the load.
- **Multipath.** A source may split its rate over several routes, and the utility depends on the total.
- **Cross-layer.** With wireless links the capacity region depends on scheduling, and the rates, routes and schedules are chosen together. [Backpressure routing](/backpressure-routing/) solves such a problem with queue lengths as prices.
- **Inelastic traffic.** With utilities that are not concave, for example a step at a minimum rate, the problem is not convex and the dual method can fail.

## Examples

**A line network.** Links 1 and 2 have capacity 1. Flow 0 uses both links, flow 1 uses link 1 and flow 2 uses link 2. All utilities are $\log x$. Source $s$ picks $x_s = 1/q_s$. Each link updates its price by the projected gradient step of Low and Lapsley,

$$p_\ell \leftarrow \max\big(0,\; p_\ell + \gamma (y_\ell - c_\ell)\big),$$

where $y_\ell$ is the load of the link. With $\gamma = 0.5$ and both prices starting at 1:

| step | $p_1 = p_2$ | $x_0$ | $x_1 = x_2$ | load of each link |
|---|---|---|---|---|
| 0 | 1 | 0.5 | 1 | 1.5 |
| 1 | 1.25 | 0.4 | 0.8 | 1.2 |
| 2 | 1.35 | 0.3704 | 0.7407 | 1.1111 |
| 5 | 1.4603 | 0.3424 | 0.6848 | 1.0272 |
| 10 | 1.4949 | 0.3345 | 0.6689 | 1.0034 |
| 40 | 1.5 | 0.3333 | 0.6667 | 1.0 |

The prices converge to $3/2$, and the rates to $(1/3, 2/3, 2/3)$, the proportionally fair point. Flow 0 pays $3/2$ on each of its two links, so its rate is $1/3$. The short flows pay $3/2$ and get $2/3$. With $\gamma = 1$ this symmetric case reaches the optimum in one step. A step that is too large makes the prices oscillate.

**The same network with other utilities.** With $U_s = -1/x$ ($\alpha = 2$) the long flow gets $1/(1 + \sqrt{2}) \approx 0.414$. With $U_s = x$ the problem is a [linear program](/linear-programming-problem/), and the optimum $(0, 1, 1)$ starves the long flow.

## Known algorithms

- **Dual gradient projection (Low and Lapsley).** Each link updates its price from its own load, and each source sets its rate from the sum of the prices on its route, as in the example. It converges for a step size below a bound that depends on the curvature of the utilities, the length of the longest route and the largest number of sources on a link, also with delays and asynchronous updates. See [dual decomposition](/dual-decomposition/) and [dual ascent](/dual-ascent/).
- **Primal algorithm (Kelly, Maulloo and Tan).** Each source changes its rate by $\dot x_s = \kappa_s (w_s - x_s q_s)$, where $q_s$ is the sum of load-based link prices. A Lyapunov function shows that the rates converge to the optimum of the penalty problem.
- **Dual algorithm (Kelly, Maulloo and Tan).** Links change their prices with the excess load, and sources respond with $x_s = w_s / q_s$.
- **Primal-dual methods.** Both rates and prices move at the same time.
- **TCP as a distributed algorithm.** [TCP Vegas](/tcp-vegas/) is a dual method with queueing delay as the price, as Low, Peterson and Wang showed. Srikant and Ying relate loss-based TCP to primal algorithms in which the loss or marking rate is the price.
- **Central solvers.** For a known network, any method for [convex optimization problems](/convex-optimization-problem/), for example an interior-point method, solves NUM directly.

## Bounds

The optimal rates are unique, but the prices need not be unique when the routing matrix has dependent rows. When the curvature of every utility is bounded away from zero on $I_s$, the dual function has a Lipschitz gradient, so a fixed small step makes the dual gradient method converge, and the rates converge to $x^*$. With a step that is too large it can oscillate or diverge. With linear utilities the dual is not smooth, the rates given by the prices are not unique, and the price updates become [subgradient](/subgradient/) steps.

## Reductions

- **Proportional fairness** is NUM with $U_s = w_s \log x_s$.
- **Max-min fairness** is the limit of NUM with $\alpha$-fair utilities as $\alpha \to \infty$.
- **Maximum total throughput** is NUM with linear utilities, a linear program.
- **The single link** with utilities $U_s$ reduces to a search for one price $p$ with $\sum_s x_s(p) = c$, which a [bisection](/bisection-method/) on $p$ solves.

## Applications

- **Design and analysis of congestion control.** NUM explains what equilibrium a TCP variant reaches, and it guides new controls. See [congestion control](/congestion-control/).
- **Active queue management.** An [AQM](/active-queue-management/) scheme can compute the price of its link, and [ECN](/ecn/) marks can carry the price to the sources.
- **Wireless and cross-layer design.** Joint choice of rates, routes and transmission schedules, with backpressure as the price signal.
- **Pricing.** Kelly reads the dual variables as shadow prices that a network could charge, so that users that maximize their own surplus reach the system optimum.

## References
