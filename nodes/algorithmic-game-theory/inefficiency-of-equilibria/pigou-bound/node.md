---
tag: WAHK5G
kind: theorem
slug: pigou-bound
name: Pigou bound
aliases:
- anarchy value
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: If a class of latency functions contains the constant functions, the price of anarchy of selfish routing with that class equals the worst ratio already reached in a two-link Pigou network.
prereqs: [roughgarden-tardos-four-thirds-bound, pigou-example]
see_also: [price-of-anarchy, wardrop-equilibrium, system-optimal-flow, selfish-routing-model, beckmann-potential, smoothness-framework, braess-paradox, atomic-linear-congestion-price-of-anarchy]
sources:
  - paper: doi:10.1016/S0022-0000(03)00044-8
    title: "Tim Roughgarden, The price of anarchy is independent of the network topology, Journal of Computer and System Sciences 67(2) (2003), 341-364"
    locator: the definition of the bound, the upper bound under a convexity assumption, and the lower bound for classes with a function that is positive at zero
  - paper: doi:10.1287/moor.1040.0098
    title: "Jose R. Correa, Andreas S. Schulz and Nicolas E. Stier-Moses, Selfish routing in capacitated networks, Mathematics of Operations Research 29(4) (2004), 961-976"
    locator: the upper bound for every class of continuous nondecreasing latencies, from the variational inequality
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 18, Tim Roughgarden, Routing games, Section 18.4.1 (Definition 18.18, Proposition 18.19, Proposition 18.20 and Theorem 18.21), Exercises 18.5 and 18.6, and Section 18.6 (notes)
  - book: isbn:9780262182430
    title: Tim Roughgarden, Selfish Routing and the Price of Anarchy, MIT Press, 2005
    locator: Chapter 3, How Bad Is Selfish Routing?, Section 3.3 (a general upper bound)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 11 (the Pigou bound as the price of anarchy of selfish routing)
  - paper: doi:10.1145/506147.506153
    title: "Tim Roughgarden and Eva Tardos, How bad is selfish routing?, Journal of the ACM 49(2) (2002), 236-259"
    locator: the special case of affine latencies and the polynomial example
  - paper: doi:10.1016/0191-2615(79)90022-5
    title: "M. J. Smith, The existence, uniqueness and stability of traffic equilibria, Transportation Research Part B 13(4) (1979), 295-304"
    locator: the variational inequality form of the equilibrium
  - book: "A. C. Pigou, The Economics of Welfare, Macmillan, London, 1920"
    locator: the two-road example of congestion
---

The Pigou bound $\alpha(\mathcal{C})$ of a class $\mathcal{C}$ of latency functions is the worst price of anarchy of a two-link network in the style of [Pigou's example](/pigou-example/): one link with a latency from $\mathcal{C}$ and one link with a constant latency. The theorem says that no network does worse. Every multicommodity instance with latencies in $\mathcal{C}$ has price of anarchy at most $\alpha(\mathcal{C})$, and if $\mathcal{C}$ contains the constant functions, two links already come arbitrarily close. So the price of anarchy of selfish routing depends on the latency functions and not on the network topology. For affine latencies the bound is the $4/3$ of the [Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/).

## Statement

Let $\mathcal{C}$ be a nonempty set of continuous nondecreasing functions $\ell : [0, \infty) \to [0, \infty)$.

**Definition.** The *Pigou bound* of $\mathcal{C}$ is

$$\alpha(\mathcal{C}) = \sup_{\ell \in \mathcal{C}} \; \sup_{x, r \ge 0} \; \frac{r \, \ell(r)}{x \, \ell(x) + (r - x)\, \ell(r)},$$

with $0/0 = 1$. The value $x = r$ gives 1, so $\alpha(\mathcal{C}) \ge 1$. For $x \ge r$ the ratio is at most 1, because $\ell(x) \ge \ell(r)$, so only $x < r$ matters. The bound may be $+\infty$.

**Theorem (Roughgarden 2003; Correa, Schulz and Stier-Moses 2004).** Consider nonatomic [selfish routing](/selfish-routing-model/) instances in any network with any number of commodities, with all latencies in $\mathcal{C}$. Equilibria are pure Wardrop equilibria, they exist, and all have the same cost ([Beckmann potential](/beckmann-potential/)).

1. *Upper bound.* Every such instance has price of anarchy at most $\alpha(\mathcal{C})$.
2. *Lower bound.* If $\mathcal{C}$ contains all constant functions, then for every $\varepsilon > 0$ some instance on two parallel links has price of anarchy at least $\alpha(\mathcal{C}) - \varepsilon$. The same conclusion holds, with a larger network, if some $\ell \in \mathcal{C}$ has $\ell(0) > 0$.

So for such classes the price of anarchy of the class is exactly $\alpha(\mathcal{C})$.

## In plain words

Take a family of delay curves, and build the simplest bad network from it: two parallel roads, one with a curve from the family and one with a fixed delay. Let the drivers choose freely and compare with the best plan. The worst loss over all such two-road networks is the Pigou bound. The theorem says that no network, however large and with however many groups of drivers, loses more than this. So to know how bad selfish routing can be for a family of delays, it is enough to study two roads. The shape of the delay curves matters, and the shape of the network does not.

## Proof

**Upper bound.** Let $f$ be a Wardrop equilibrium and $f^*$ a feasible flow. If $\alpha = \alpha(\mathcal{C})$ is infinite there is nothing to prove. Otherwise apply the definition on each edge with $\ell = \ell_e$, $r = f_e$ and $x = f^*_e$:

$$f_e \, \ell_e(f_e) \le \alpha \Big( f^*_e \, \ell_e(f^*_e) + (f_e - f^*_e)\, \ell_e(f_e) \Big).$$

This holds in all cases. If the denominator is positive it is the definition. If the denominator is 0 and $f^*_e < f_e$, then $\ell_e(f_e) = 0$ and both sides are 0. If $f^*_e \ge f_e$, the ratio is at most 1 and $\alpha \ge 1$. Sum over the edges:

$$C(f) \le \alpha \, C(f^*) + \alpha \sum_e \ell_e(f_e)\,(f_e - f^*_e) \le \alpha \, C(f^*).$$

The last step is the variational inequality $\sum_e \ell_e(f_e) f_e \le \sum_e \ell_e(f_e) f^*_e$ of a [Wardrop equilibrium](/wardrop-equilibrium/) (Smith 1979). $\square$

**Lower bound with constants.** Fix $\ell \in \mathcal{C}$ and $0 \le x < r$. Build two parallel links from $s$ to $t$ with $\ell_1 = \ell$ and the constant $\ell_2 = \ell(r)$, and rate $r$. All traffic on link 1 is an equilibrium: its latency $\ell(r)$ equals the latency of the empty link 2. Its cost is $r \ell(r)$. The flow with $x$ on link 1 and $r - x$ on link 2 is feasible with cost $x \ell(x) + (r - x) \ell(r)$. So the price of anarchy of this instance is at least the ratio in the definition, and the supremum over $\ell$, $x$ and $r$ gives $\alpha(\mathcal{C})$. $\square$

For a class with some $\ell(0) > 0$ but without all constants, the fixed delay is built from copies of that function in a larger network (NRTV Exercise 18.5; Roughgarden 2003 gives the solution).

**Example: affine functions.** Let $\ell(x) = a x + b$ with $a, b \ge 0$. The denominator is $a x^2 + b x + (r - x)(a r + b) = a x^2 - a r x + a r^2 + b r$, smallest at $x = r/2$ with value $\tfrac{3}{4} a r^2 + b r$. So the ratio is

$$\frac{a r^2 + b r}{\tfrac{3}{4} a r^2 + b r} \le \frac{4}{3},$$

with equality when $b = 0$. So $\alpha = 4/3$ for affine functions, reached by $\ell(x) = x$ and $r = 1$, which is Pigou's network.

## Consequences

- **Polynomial latencies.** For $\ell(x) = x^d$ and $r = 1$, the denominator $x^{d+1} + 1 - x$ is smallest at $x = (d + 1)^{-1/d}$, and this gives $\alpha_d = [1 - d (d + 1)^{-(d+1)/d}]^{-1}$. For a polynomial $\sum_j a_j x^j$ with nonnegative coefficients, the ratio is a ratio of two sums of nonnegative terms, so it is at most the largest ratio of the matching terms, and $\alpha_j$ grows with $j$. So polynomials of degree at most $d$ have Pigou bound $\alpha_d$. The values are about $1.333$ for $d = 1$, $1.626$ for $d = 2$, $1.896$ for $d = 3$, $2.151$ for $d = 4$, $3.512$ for $d = 10$ and $18.33$ for $d = 100$. They grow like $d / \ln d$, which is smaller than the $d + 1$ bound that the potential gives.
- **Concave latencies.** Nonnegative, nondecreasing, concave functions have Pigou bound $4/3$ too (NRTV Exercise 18.6).
- **Topology does not matter.** For every class with the constants, the worst case over all multicommodity networks equals the worst case over two parallel links with one commodity.
- **Braess's paradox.** The old equilibrium is feasible in the new network, so adding edges can raise the equilibrium cost by at most a factor $\alpha(\mathcal{C})$ ([Braess's paradox](/braess-paradox/)).
- **An equivalent form.** Write $\beta(\mathcal{C}) = \sup x(\ell(r) - \ell(x)) / (r \ell(r))$ over $\ell \in \mathcal{C}$ and $0 \le x \le r$ with $r\ell(r) > 0$. Then $\alpha = 1/(1 - \beta)$, and the proof above reads $\sum_e \ell_e(f_e) f^*_e \le C(f^*) + \beta C(f)$. This is the parameter of Correa, Schulz and Stier-Moses, and the inequality has the form of the [smoothness framework](/smoothness-framework/) with $\lambda = 1$ and $\mu = \beta$.

## Tightness

- **The constants are needed for the lower bound.** Let $\mathcal{C} = \{a x : a \ge 0\}$. Its Pigou bound is $4/3$, from $\ell(x) = x$ and $r = 1$. But in every instance with latencies $a_e x$, the potential is $\Phi(f) = \sum_e a_e f_e^2 / 2 = C(f)/2$, so the equilibrium, which minimizes $\Phi$, also minimizes $C$, and the price of anarchy is 1. The same holds for $\{a x^d : a \ge 0\}$ with a fixed $d$, where $\Phi = C/(d + 1)$.
- **The supremum need not be attained.** The theorem gives instances with ratio close to $\alpha(\mathcal{C})$. For polynomials of degree $d$ it is attained, by Pigou's network with $\ell(x) = x^d$.
- **Atomic players.** The bound is for nonatomic traffic. With atomic players of unit demand and affine costs, the price of anarchy is $5/2$, which is more than $4/3$ ([atomic linear congestion bound](/atomic-linear-congestion-price-of-anarchy/)).

## History

The two-link network goes back to Pigou (1920). Roughgarden and Tardos (2002) proved the $4/3$ bound for affine latencies and studied the polynomial variant of Pigou's example. Roughgarden (2003) defined $\alpha(\mathcal{C})$ and proved the upper bound under a convexity assumption on the latencies, the one used for the marginal cost form of the optimum, and proved the lower bound for classes with some $\ell(0) > 0$. Correa, Schulz and Stier-Moses (2004) proved the upper bound with no convexity assumption, using the variational inequality of Smith (1979). The bound is also called the anarchy value.

## References
