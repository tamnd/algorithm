---
tag: WQVME9
kind: theorem
slug: deficiency-zero-theorem
name: Deficiency zero theorem
aliases:
- Feinberg deficiency zero theorem
- Horn-Jackson-Feinberg theorem
area: biology/systems-biology
level: advanced
summary: "Weakly reversible with deficiency 0: for every choice of positive rate constants, one equilibrium per positive stoichiometric compatibility class, locally asymptotically stable relative to its class."
history:
  year: 1972
  people: [Fritz Horn, Roy Jackson, Martin Feinberg]
  note: Horn and Jackson introduced complex balancing and its Lyapunov function in 1972, and Horn and Feinberg related complex balancing to the network structure in the same year. Feinberg later stated the theorem in its standard form.
prereqs: [chemical-reaction-network, stoichiometric-matrix, mass-action-kinetics]
see_also: [lyapunov-function, lyapunov-stability, strongly-connected-components, convex-function, perron-frobenius-theorem, chemical-master-equation, michaelis-menten-kinetics, genetic-toggle-switch]
sources:
  - book: isbn:9783030038571
    title: Martin Feinberg, Foundations of Chemical Reaction Network Theory, Springer, 2019
    locator: Chapter 7 (The Deficiency Zero Theorem) and Chapter 16 (Deficiency Zero Theory Foundations and Some Key Propositions)
  - paper: doi:10.1016/0009-2509(87)80099-4
    title: Martin Feinberg, Chemical reaction network structure and the stability of complex isothermal reactors I. The deficiency zero and deficiency one theorems, Chemical Engineering Science 42(10), 1987, 2229-2268
    locator: the statement of the deficiency zero theorem, for networks that are weakly reversible and for networks that are not
  - paper: doi:10.1007/BF00251225
    title: F. Horn and R. Jackson, General mass action kinetics, Archive for Rational Mechanics and Analysis 47(2), 1972, 81-116
    locator: complex balanced systems, the uniqueness of the equilibrium in each class, and the Lyapunov function
  - paper: doi:10.1007/BF00255665
    title: Martin Feinberg, Complex balancing in general kinetic systems, Archive for Rational Mechanics and Analysis 49, 1972, 187-194
    locator: the conditions on the network under which every equilibrium is complex balanced
  - paper: "F. Horn, Necessary and sufficient conditions for complex balancing in chemical kinetics, Archive for Rational Mechanics and Analysis 49, 1972, 172-186"
    title: Horn 1972
    locator: the deficiency of a network and the condition for complex balancing for all rate constants
---

The deficiency zero theorem says that some reaction networks behave in a simple way for every choice of rate constants. The deficiency of a network is $\delta = c - l - s$, where $c$ is the number of complexes, $l$ the number of linkage classes and $s$ the rank of the [stoichiometric matrix](/stoichiometric-matrix/). If $\delta = 0$ and the network is weakly reversible, then with [mass action kinetics](/mass-action-kinetics/), each positive stoichiometric compatibility class has exactly one equilibrium, and it is locally asymptotically stable relative to its class. The network cannot oscillate or switch. If $\delta = 0$ and the network is not weakly reversible, there is no positive equilibrium at all. The conditions are on the reaction graph only, so they can be checked without any rate constant.

## Statement

**Setting.** A [chemical reaction network](/chemical-reaction-network/) has $m$ species and $c$ complexes (the distinct left and right sides of the reactions). Complex $j$ is a vector $y_j \in \mathbb{Z}^m_{\ge 0}$, and $Y$ is the $m \times c$ matrix with columns $y_j$. The reactions are the edges $j \to i$ of a directed graph on the complexes, with rate constants $k_{j \to i} > 0$. The incidence matrix $I_a$ is $c \times r$, with $-1$ at the source and $+1$ at the target of each reaction. The stoichiometric matrix is $S = Y I_a$, and $s = \operatorname{rank} S$.

With mass action, reaction $j \to i$ has the rate $k_{j \to i}\, x^{y_j}$, where $x^{y} = \prod_k x_k^{y_k}$. (This page uses the deterministic convention in which $2A$ has the rate $k a^2$. In the stochastic reading the constant for $2A$ is $c = 2k/(N_A V)$ and the propensity is $c\, x(x-1)/2$.) Put $\Psi_j(x) = x^{y_j}$ and let $A_k$ be the $c \times c$ matrix with $(A_k)_{ij} = k_{j \to i}$ for $i \ne j$ and $(A_k)_{jj} = -\sum_i k_{j \to i}$. Then
$$\dot x = S\, v(x) = Y A_k \Psi(x).$$

**Definitions.**
- A *linkage class* is a connected component of the reaction graph, with the directions ignored. There are $l$ of them.
- The network is *weakly reversible* if each linkage class is strongly connected, or equally, if each reaction lies on a directed cycle.
- The *deficiency* is $\delta = c - l - s$. It is a nonnegative integer.
- The *stoichiometric compatibility class* of $x_0$ is $(x_0 + \operatorname{im} S) \cap \mathbb{R}^m_{\ge 0}$. It is *positive* if it meets $\mathbb{R}^m_{> 0}$; its positive part is $(x_0 + \operatorname{im} S) \cap \mathbb{R}^m_{> 0}$. Every trajectory stays in its class.
- A state $x > 0$ is *complex balanced* if $A_k \Psi(x) = 0$: at each complex, the total rate of the reactions that make it equals the total rate of those that use it.

**Theorem.** Let a mass action network have deficiency zero.
1. If it is not weakly reversible, then for every choice of positive rate constants it has no positive equilibrium, and no periodic orbit through a positive state.
2. If it is weakly reversible, then for every choice of positive rate constants, each positive stoichiometric compatibility class contains exactly one positive equilibrium. This equilibrium is complex balanced and locally asymptotically stable relative to its class. No positive state other than an equilibrium lies on a periodic orbit.

The theorem does not say that every positive trajectory converges to the equilibrium of its class. That claim is the *global attractor conjecture* (see Tightness).

## In plain words

Count three numbers from the drawing of the network: the complexes, the pieces of the drawing, and the number of independent directions in which the reactions move the state. If the first minus the second minus the third is zero, the reactions are "as independent as the drawing allows". Then any balance of the species at an equilibrium must be a balance at each complex. When every arrow lies on a cycle, such a balance exists, it is unique inside each set of states with the same conserved amounts, and an entropy-like function decreases toward it. When some arrow is not on a cycle, flow through that arrow cannot be balanced, so no positive steady state exists.

## Proof

**Step 1. The deficiency is a dimension.** For a graph with $c$ vertices and $l$ components, $\operatorname{rank} I_a = c - l$. For the product,
$$\operatorname{rank}(Y I_a) = \operatorname{rank} I_a - \dim(\ker Y \cap \operatorname{im} I_a).$$
So $\delta = c - l - s = \dim(\ker Y \cap \operatorname{im} I_a) \ge 0$. Also $A_k \Psi(x) = I_a v(x)$, so $A_k \Psi(x) \in \operatorname{im} I_a$. If $\delta = 0$ and $x > 0$ is an equilibrium, then $A_k \Psi(x)$ lies in $\ker Y \cap \operatorname{im} I_a = \{0\}$. So **every positive equilibrium of a deficiency zero network is complex balanced.**

**Step 2. Part 1.** Let $x > 0$ be an equilibrium. By Step 1, $I_a v = 0$ with $v = v(x)$, and every $v_{j \to i} > 0$. So $v$ is a positive circulation: at each complex the inflow equals the outflow. Suppose the reaction $j \to i$ is on no directed cycle. Let $U$ be the set of complexes that can be reached from $i$. Then $j \notin U$, and no reaction leaves $U$ (its target would be reachable). Sum the balance over $U$: the total flow into $U$ from outside equals the total flow out of $U$, which is $0$. But the flow into $U$ is at least $v_{j \to i} > 0$. This is a contradiction, so every reaction lies on a cycle, and the network is weakly reversible.

For a periodic orbit $x(t) > 0$ with period $T$, integrate: $0 = x(T) - x(0) = Y I_a \bar v$ with $\bar v = \int_0^T v(x(t))\,dt > 0$. As in Step 1, $I_a \bar v = 0$, and the same argument applies.

**Step 3. A complex balanced state exists.** Let the network be weakly reversible. On a linkage class $L$, the block of $A_k$ is $-(\text{a Laplacian})$ of a strongly connected graph. Its columns sum to zero. For large $\lambda$, $A_k + \lambda I$ on $L$ is nonnegative and irreducible with the positive left eigenvector $\mathbf 1$ for $\lambda$. By the [Perron-Frobenius theorem](/perron-frobenius-theorem/), $\lambda$ is its Perron root, and the kernel of the block is spanned by one vector $\rho^L > 0$. So $\ker A_k$ consists of the vectors equal to $\kappa_L \rho^L$ on each $L$.

We need $x > 0$ with $\Psi_j(x) = \kappa_L \rho_j$ for $j \in L$. Take logarithms with $z = \ln x$: $y_j \cdot z - \ln \kappa_L = \ln \rho_j$. So $\ln \rho$ must lie in $\operatorname{im} Y^{\mathsf T} + \operatorname{span}\{\mathbf 1_L\}$. The vectors constant on each linkage class are exactly $\ker I_a^{\mathsf T}$. The orthogonal complement of $\operatorname{im} Y^{\mathsf T} + \ker I_a^{\mathsf T}$ is $\ker Y \cap \operatorname{im} I_a$, which is $\{0\}$ when $\delta = 0$. So the sum is $\mathbb{R}^c$, and a solution $x^*$ exists. It is an equilibrium, because $Y A_k \Psi(x^*) = 0$.

**Step 4. The set of positive equilibria.** By Steps 1 and 3, $x > 0$ is an equilibrium if and only if $\Psi(x)/\Psi(x^*)$ (entry by entry) is constant on each linkage class. With $u = \ln x - \ln x^*$, the ratio for complex $j$ is $e^{y_j \cdot u}$. So the condition is $(y_i - y_j) \cdot u = 0$ for $i, j$ in the same linkage class. Each reaction vector is such a difference, and each such difference is a sum of reaction vectors along a path. So the condition is $u \perp \operatorname{im} S$:
$$E = \{x > 0 : \ln x - \ln x^* \in (\operatorname{im} S)^\perp\}.$$

**Step 5. Exactly one in each class.** *Uniqueness.* Let $x, x' \in E$ lie in the same class. Then $x - x' \in \operatorname{im} S$ and $\ln x - \ln x' \in (\operatorname{im} S)^\perp$, so
$$\sum_k (x_k - x'_k)(\ln x_k - \ln x'_k) = 0.$$
Each term is $\ge 0$, and it is $0$ only if $x_k = x'_k$. So $x = x'$.

*Existence.* Let $P$ be the closure of a positive class, a closed convex set. The function
$$G(x) = \sum_k \big( x_k (\ln x_k - \ln x^*_k - 1) + x^*_k \big)$$
is continuous on $\mathbb{R}^m_{\ge 0}$, strictly [convex](/convex-function/), and tends to infinity as $|x| \to \infty$. So it has a minimum on $P$. The minimum is not on the boundary: if $\hat x \in P$ has $\hat x_k = 0$ for $k \in Z \neq \emptyset$, and $p$ is a positive point of $P$, then the derivative of $G(\hat x + t(p - \hat x))$ is $\sum_k (p_k - \hat x_k) \ln\big((\hat x_k + t(p_k - \hat x_k))/x^*_k\big)$, which tends to $-\infty$ as $t \to 0^+$ because of the terms in $Z$. At a positive minimizer, the gradient $\ln x - \ln x^*$ is orthogonal to $\operatorname{im} S$, so the minimizer is in $E$.

**Step 6. Stability.** Let $\bar x$ be the equilibrium of the class, and use $G$ with $\bar x$ in place of $x^*$. With $\mu = Y^{\mathsf T}(\ln x - \ln \bar x)$, so that $\Psi_j(x) = \Psi_j(\bar x) e^{\mu_j}$,
$$\frac{dG}{dt} = (\ln x - \ln \bar x)^{\mathsf T}\, Y A_k \Psi(x) = \sum_{j \to i} k_{j \to i}\, \Psi_j(\bar x)\, e^{\mu_j} (\mu_i - \mu_j).$$
Since $e^a (b - a) \le e^b - e^a$, with equality only for $a = b$,
$$\frac{dG}{dt} \le \sum_{j \to i} k_{j \to i}\, \Psi_j(\bar x)\, (e^{\mu_i} - e^{\mu_j}) = \sum_{q} e^{\mu_q} \big( \text{inflow}_q(\bar x) - \text{outflow}_q(\bar x) \big) = 0,$$
by complex balance at $\bar x$. Equality needs $\mu_i = \mu_j$ for each reaction, that is $\ln x - \ln \bar x \perp \operatorname{im} S$, so $x \in E$. In the class, this is only $\bar x$. On the class, $G$ has a strict minimum at $\bar x$, and its small sublevel sets are compact and positive. So $G$ is a strict [Lyapunov function](/lyapunov-function/) on the class, and $\bar x$ is locally asymptotically stable relative to its class ([Lyapunov stability](/lyapunov-stability/)). On a periodic orbit $G$ would have to return to its start while it strictly decreases, so only equilibria lie on periodic orbits. $\square$

## Consequences

**Checks by hand.** The test needs only the graph:

| Network | $c$ | $l$ | $s$ | $\delta$ | weakly reversible | conclusion |
|---|---|---|---|---|---|---|
| $E + S \rightleftharpoons C \rightleftharpoons E + P$ | 3 | 1 | 2 | 0 | yes | one stable equilibrium per class |
| $E + S \rightleftharpoons C \to E + P$ | 3 | 1 | 2 | 0 | no | no positive equilibrium |
| $A \rightleftharpoons 2A$ | 2 | 1 | 1 | 0 | yes | one equilibrium, $a = k_1/k_2$ |
| $2A \rightleftharpoons B$ | 2 | 1 | 1 | 0 | yes | one equilibrium per value of $a + 2b$ |
| $\emptyset \rightleftharpoons A$, $2A \rightleftharpoons 3A$ | 4 | 2 | 1 | 1 | yes | the theorem says nothing |

**The reversible enzyme.** For $E + S \rightleftharpoons C \rightleftharpoons E + P$ with all four rate constants $1$, total enzyme $e + c = 1$ and total substrate $s + c + p = 2$, complex balance gives $e s = c$ and $e p = c$. So $p = s$, $c = s/(1 + s)$ and $2 s^2 + s - 2 = 0$. The equilibrium is $s = p = (\sqrt{17} - 1)/4 = 0.780776$, $c = 0.438447$ and $e = 0.561553$. A Runge-Kutta run from $s = 2$, $e = 1$ reaches it. The irreversible scheme of [Michaelis-Menten kinetics](/michaelis-menten-kinetics/) has the same deficiency, but the reaction $C \to E + P$ is on no cycle, so by part 1 the substrate always runs out.

**No switches and no clocks with deficiency zero.** By the theorem, a mass action network with $\delta = 0$ never has two positive equilibria in one class and never has a positive periodic orbit, for any rate constants. So a mass action model of a bistable switch, such as a reaction scheme for the [genetic toggle switch](/genetic-toggle-switch/), or of an oscillator, such as the [repressilator](/repressilator/), must have $\delta \ge 1$.

**The stochastic reading.** For a complex balanced network, Anderson, Craciun and Kurtz (2010) showed that the stationary law of the [chemical master equation](/chemical-master-equation/) on each closed set of states is a product of Poisson factors $\prod_k \lambda_k^{x_k}/x_k!$, restricted to the set, where $\lambda$ is a complex balanced equilibrium of the ODE with suitably scaled constants. For $2A \rightleftharpoons B$ with $c_1 = c_2 = 1$ per second and six molecules of $A$, $\lambda = (1, 0.5)$ gives the [stationary distribution](/stationary-distribution/) $(1, 15, 45, 15)/76$ on $x_B = 0, 1, 2, 3$, the same law that detailed balance gives on the [chemical reaction network](/chemical-reaction-network/) page.

## Tightness

**Weak reversibility is needed for part 2.** The irreversible enzyme scheme has $\delta = 0$ and no positive equilibrium.

**Deficiency zero is needed.** The Schlögl network $\emptyset \rightleftharpoons A$, $2A \rightleftharpoons 3A$ is weakly reversible with $\delta = 1$. With the rate constants $6, 11, 6, 1$ in the order $\emptyset \to A$, $A \to \emptyset$, $2A \to 3A$, $3A \to 2A$,
$$\dot a = 6 - 11 a + 6 a^2 - a^3 = -(a - 1)(a - 2)(a - 3).$$
There are three positive equilibria in the single class $\mathbb{R}_{\ge 0}$. The slopes of the right side are $-2$, $1$ and $-2$, so $a = 1$ and $a = 3$ are stable and $a = 2$ is not. Runge-Kutta runs from $0.5$ and $1.9$ go to $1$, and runs from $2.1$ and $5$ go to $3$. Feinberg's deficiency one theorem (1987) covers part of the case $\delta = 1$.

**Mass action is needed.** The proof uses $\Psi_j(x) = x^{y_j}$ in Steps 3, 4 and 6. With other rate laws, such as [Hill functions](/hill-equation/), the conclusion can fail.

**Local, not global.** The theorem gives local stability relative to the class, and $G$ decreases along every positive trajectory. It does not exclude that a trajectory approaches the boundary of the class, where some species is zero. The statement that every positive trajectory converges to the equilibrium of its class is the global attractor conjecture. Craciun (2015) posted a proposed proof for the general case. This page does not treat the conjecture as a theorem.

**Zero eigenvalues.** The Jacobian at $\bar x$ maps into $\operatorname{im} S$, so it has at least $m - s$ zero eigenvalues, one for each conservation law. Stability holds only relative to the class, never in all of $\mathbb{R}^m$ when $s < m$.

## History

Horn and Jackson (1972) defined complex balanced mass action systems and proved, for them, the uniqueness of the equilibrium in each class and its stability with the function $G$. In the same volume, Horn (1972) and Feinberg (1972) asked when complex balancing holds for all rate constants, and the deficiency appeared as the answer: for a weakly reversible network, complex balancing for every choice of rate constants holds exactly when $\delta = 0$. Feinberg's 1987 paper gave the theorem in the two-part form above, together with the deficiency one theorem, and his 2019 book gives the full proof.

## References
