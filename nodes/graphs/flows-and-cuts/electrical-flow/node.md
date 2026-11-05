---
tag: 3ZBGPG
kind: concept
slug: electrical-flow
name: Electrical flow
aliases:
- electrical flow problem
area: graphs/flows-and-cuts
level: advanced
summary: The flow of least energy for given demands in a resistor network, computed by one Laplacian linear system solve.
prereqs: [laplacian-matrix, s-t-flow, flow-conservation]
see_also: [almost-linear-max-flow, interior-point-method, multiplicative-weights-update, conjugate-gradient-method, sparsification, max-flow-problem, spectral-methods, linear-system-solving]
sources:
  - paper: doi:10.1145/1993636.1993674
    title: Paul Christiano, Jonathan A. Kelner, Aleksander Madry, Daniel A. Spielman and Shang-Hua Teng, Electrical flows, Laplacian systems, and faster approximation of maximum flow in undirected graphs, STOC 2011, 273 to 282
    locator: Section 2 (electrical flows, energy and effective resistance) and Section 3 (the multiplicative weights algorithm)
  - paper: doi:10.1137/090771430
    title: Daniel A. Spielman and Shang-Hua Teng, Nearly linear time algorithms for preconditioning and solving symmetric, diagonally dominant linear systems, SIAM Journal on Matrix Analysis and Applications 35(3), 835 to 885 (2014)
    locator: the main theorem (Laplacian systems in nearly linear time)
  - book: isbn:9781107160156
    title: Russell Lyons and Yuval Peres, Probability on Trees and Networks
    locator: Chapter 2, Random Walks and Electric Networks (Kirchhoff's laws, Thomson's principle and effective resistance)
  - paper: doi:10.1109/FOCS.2013.35
    title: Aleksander Madry, Navigating central path with electrical flows, from flows to matchings, and back, FOCS 2013, 253 to 262
    locator: the whole paper (an interior point method whose steps are electrical flows)
---

An electrical flow is the flow that a battery drives through a network of resistors. For an undirected graph with a resistance $r_e > 0$ on each edge and a demand vector $b$ that sums to zero, it is the unique flow with net outflow $b$ that minimizes the energy $\sum_e r_e f_e^2$. It is given by vertex potentials $\phi$ that solve the linear system $L\phi = b$ with the weighted [Laplacian matrix](/laplacian-matrix/) $L$, so it can be computed in nearly linear time. Electrical flows are the inner step of the fastest approximate and exact [maximum flow](/max-flow-problem/) algorithms of the 2010s.

## In plain words

Connect a battery to two points of a mesh of wires. Current enters at one point and leaves at the other, and it spreads over every route, more over short, thick wires and less over long, thin ones. Each point gets a voltage, and the current in each wire is the voltage difference across it divided by its resistance. Of all ways to send the same total current, nature picks the one that wastes the least energy as heat. Finding those voltages means solving one system of linear equations, and there are very fast methods for this kind of system.

## The idea

**Setting.** Let $G = (V, E)$ be an undirected graph with $n$ vertices and $m$ edges, and $r_e > 0$ a real resistance on each edge; $1/r_e$ is the conductance. Fix an arbitrary orientation $e = (u, v)$ of each edge to give flows a sign: $f_e > 0$ means flow from $u$ to $v$, $f_e < 0$ means flow from $v$ to $u$. A demand vector $b \in \mathbb{R}^V$ has $\sum_v b_v = 0$; for an s-t flow of value $F$, $b_s = F$, $b_t = -F$ and $b_v = 0$ otherwise. Let $B$ be the $m \times n$ signed incidence matrix ($B_{e,u} = 1$, $B_{e,v} = -1$ for $e = (u, v)$), $R = \operatorname{diag}(r)$, and $L = B^{\mathsf T} R^{-1} B$ the weighted Laplacian.

**Definition.** A flow $f \in \mathbb{R}^E$ meets the demands if $B^{\mathsf T} f = b$, which is [flow conservation](/flow-conservation/) with net outflow $b_v$ at $v$. Its energy is $\mathcal{E}(f) = \sum_e r_e f_e^2$. The **electrical flow** for $b$ is the flow meeting $b$ of least energy.

**Kirchhoff and Ohm.** The electrical flow is $f = R^{-1} B \phi$, that is $f_{(u,v)} = (\phi_u - \phi_v)/r_e$ (Ohm's law), where the potentials $\phi$ solve $L \phi = b$ (Kirchhoff's current law). *Why.* Minimize $\mathcal{E}(f)$ subject to $B^{\mathsf T} f = b$. With a multiplier $\phi$ the optimality condition is $2Rf = 2B\phi$, so $f = R^{-1}B\phi$, and then $B^{\mathsf T} R^{-1} B \phi = b$. Conversely any $f = R^{-1}B\phi$ with $L\phi = b$ is optimal: for another flow $g$ meeting $b$, $d = g - f$ has $B^{\mathsf T} d = 0$, so $\sum_e r_e f_e d_e = \phi^{\mathsf T} B^{\mathsf T} d = 0$ and $\mathcal{E}(g) = \mathcal{E}(f) + \mathcal{E}(d) \ge \mathcal{E}(f)$. This is Thomson's principle. Equivalently, around every cycle the sum of $r_e f_e$, signed by direction, is zero (Kirchhoff's voltage law), so an electrical flow never circulates around a cycle.

**Existence and uniqueness.** $L$ is symmetric positive semidefinite, and its kernel is spanned by the indicator vectors of the connected components. So $L\phi = b$ has a solution exactly when $b$ sums to zero on each component, $\phi$ is unique up to a constant on each component, and $f$ is unique. In particular an s-t electrical flow exists if and only if $s$ and $t$ are connected.

**Effective resistance and energy.** For one unit from $s$ to $t$, $R_{\text{eff}}(s, t) = \phi_s - \phi_t = b^{\mathsf T} L^{+} b$, and the energy equals $R_{\text{eff}}(s, t)$. Adding an edge or lowering a resistance never raises $R_{\text{eff}}$ (Rayleigh monotonicity).

**Computing it.** $L$ is symmetric and diagonally dominant. Spielman and Teng showed that $L\phi = b$ can be solved to accuracy $\varepsilon$ in $\tilde O(m \log(1/\varepsilon))$ time; later solvers are simpler and faster. For small graphs, [Gaussian elimination](/gaussian-elimination/) on $L$ with one vertex per component grounded ($\phi = 0$) works, and the [conjugate gradient method](/conjugate-gradient-method/) is a common practical choice.

**Direction, capacities, and edge cases.**

- The graph is undirected. An electrical flow may use an edge in either direction, and the sign only refers to the chosen orientation. On a directed network it can send flow against an arc, so it is not directly a feasible flow there.
- Electrical flows have no capacities. Algorithms that use them for maximum flow encode capacities in the resistances, for example $r_e$ growing as the flow on $e$ nears its capacity, and check the congestion $|f_e|/c_e$ afterwards.
- Two antiparallel edges between $u$ and $v$ are, in an undirected graph, two parallel resistors: they act as one edge of conductance $1/r_1 + 1/r_2$, and the current splits between them in proportion to their conductances.
- An edge of capacity 0 corresponds to an infinite resistance, that is, conductance 0, which is the same as deleting the edge. An edge of resistance 0 is a short circuit; contract it.
- Resistances and flows are real numbers; with rational resistances the electrical flow is rational.

## Examples

**A bridge network.** Vertices $s, a, b, t$ and edges with resistances $s a$ 1, $s b$ 2, $a b$ 1, $a t$ 2, $b t$ 1. Send one unit from $s$ to $t$ and ground $\phi_t = 0$. Solving $L\phi = b$ gives $\phi_s = 7/5$, $\phi_a = 4/5$, $\phi_b = 3/5$. By Ohm's law the currents are $s \to a$ $3/5$, $s \to b$ $2/5$, $a \to b$ $1/5$, $a \to t$ $2/5$, $b \to t$ $3/5$. Check conservation at $a$: $3/5$ in, $1/5 + 2/5$ out. The energy is $1 \cdot 9/25 + 2 \cdot 4/25 + 1 \cdot 1/25 + 2 \cdot 4/25 + 1 \cdot 9/25 = 7/5$, equal to $R_{\text{eff}}(s, t) = \phi_s - \phi_t$. Splitting the unit evenly over $s\,a\,t$ and $s\,b\,t$ instead costs $\tfrac14 (1 + 2) + \tfrac14 (2 + 1) = 3/2 > 7/5$.

**The running network with unit resistances.** Take the network $s a$, $s c$, $a b$, $a c$, $a d$, $c d$, $d b$, $b t$, $d t$, ignore capacities and directions, and give every edge resistance 1. One unit from $s$ to $t$ gives the potentials $s$ $15/11$, $a$ $9/11$, $c$ $10/11$, $d$ $6/11$, $b$ $5/11$, $t$ $0$, so $R_{\text{eff}}(s, t) = 15/11$. On the edge $a c$ the current is $(\phi_a - \phi_c)/1 = -1/11$: it flows from $c$ to $a$, against the direction of the arc $a \to c$ in the directed network, which shows that an electrical flow is not a flow of the directed network.

**No path.** The directed network with arcs $s \to a$ 5 and $t \to a$ 5 has no s-t path, but as an undirected graph it joins $s$ to $t$ through $a$. So the electrical flow exists: with unit resistances one unit goes from $s$ to $a$ and from $a$ to $t$, the second step against the arc $t \to a$, with energy 2. If instead $s$ and $t$ lie in different components, for example with only the edges $s a$ and $t c$, then the demand vector $b$ does not sum to zero on the component of $s$, the system $L\phi = b$ has no solution, and there is no electrical flow; formally $R_{\text{eff}}(s, t) = \infty$.

**Parallel edges.** Two edges between $u$ and $v$ with resistances 1 and 3 carry $3/4$ and $1/4$ of a unit current, and act like one edge of resistance $3/4$.

## Where it is used

- **Approximate maximum flow in undirected graphs.** Christiano, Kelner, Madry, Spielman and Teng (2011) run [multiplicative weights](/multiplicative-weights-update/) over electrical flows: resistances grow on congested edges, and averaging the flows gives a $(1 - \varepsilon)$-approximate maximum flow in $\tilde O(m n^{1/3} \varepsilon^{-11/3})$ time. Later work by Sherman and by Kelner, Lee, Orecchia and Sidford reached almost-linear time for approximate undirected maximum flow, with other tools.
- **Interior point methods for exact maximum flow.** Each Newton step of an [interior point method](/interior-point-method/) for flow problems is an electrical flow with resistances from the barrier function. Madry (2013) used this to get $\tilde O(m^{10/7})$ for unit capacity maximum flow, and Lee and Sidford (2014) $\tilde O(m \sqrt{n} \log^2 U)$ for integer capacities up to $U$. The [almost-linear maximum flow](/almost-linear-max-flow/) algorithm of 2022 uses an interior point method too, but its steps solve min-ratio cycle problems with dynamic data structures instead of Laplacian systems.
- **[Sparsification](/sparsification/).** Spielman and Srivastava sample edges with probability proportional to $R_{\text{eff}}$ times conductance to get spectral sparsifiers.
- **Random walks.** The commute time between $s$ and $t$ is $2 \cdot (\text{total conductance}) \cdot R_{\text{eff}}(s, t)$, and the number of spanning trees and the probability that an edge lies in a uniform random spanning tree are given by effective resistances.
- **Graph learning and clustering.** Effective resistance is a distance on vertices used in [spectral methods](/spectral-methods/) and semi-supervised learning.

## References
