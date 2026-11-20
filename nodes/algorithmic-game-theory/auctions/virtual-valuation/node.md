---
tag: BH13N1
kind: definition
slug: virtual-valuation
name: Virtual valuation
aliases:
- virtual value
area: algorithmic-game-theory/auctions
level: core
summary: "For a value v drawn from F with density f, the quantity v - (1 - F(v)) / f(v). The expected revenue of a truthful mechanism equals the expected virtual value of the winners."
prereqs: [myerson-lemma, independent-private-values, single-parameter-environment]
see_also: [myerson-optimal-auction, regular-distribution, ironing, reserve-price, revenue-equivalence-theorem, bulow-klemperer-theorem, monotone-allocation-rule]
sources:
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the expression of the expected revenue of an incentive compatible mechanism through the virtual valuation
  - paper: doi:10.1086/261643
    title: "Jeremy Bulow and John Roberts, The simple economics of optimal auctions, Journal of Political Economy 97(5) (1989), 1060-1090"
    locator: the virtual valuation as the marginal revenue of a monopolist facing the demand curve 1 - F
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 5, Revenue-maximizing auctions, Section 5.2 (virtual valuations and the identity of expected revenue and expected virtual welfare)
  - paper: "Jason D. Hartline, Mechanism Design and Approximation, book draft, version with Chapters 1 to 7 revised in September 2021, https://jasonhartline.com/MDnA/"
    locator: Chapter 3, Optimal mechanisms (revenue curves in quantile space and virtual values as their slopes)
---

The virtual valuation of a bidder with value $v$ drawn from a distribution $F$ with density $f$ is $\varphi(v) = v - (1 - F(v))/f(v)$. It is the part of the value that a seller can turn into revenue: for every truthful mechanism, the expected payment of a bidder equals the expected virtual value it gets, so expected revenue equals expected *virtual welfare*. [Myerson's lemma](/myerson-lemma/) gives the payment rule that makes a monotone allocation truthful, and it does not need a prior. The virtual valuation needs the prior, and it turns the expected value of those payments into a sum of virtual values that a seller can maximize.

## Definition

Let $F$ be a distribution of values with density $f > 0$ on an interval $[a, b]$, with $0 \le a < b \le \infty$. The **virtual valuation** of $F$ is

$$\varphi(v) = v - \frac{1 - F(v)}{f(v)}, \qquad a \le v \le b.$$

**Quantile form.** Write $q = 1 - F(v)$ for the probability that a value is at least $v$, and $R(q) = q \cdot F^{-1}(1 - q)$ for the revenue of the posted price that sells with probability $q$. This is the *revenue curve*. Since $dv/dq = -1/f(v)$, the derivative is $R'(q) = v - q/f(v) = \varphi(v)$. The virtual value is the marginal revenue of selling with a slightly higher probability (Bulow and Roberts 1989).

**Discrete form.** For a distribution on $s_1 < \cdots < s_K$ with probabilities $f_k > 0$, write $q_k = \Pr[v \ge s_k]$ and $s_{K+1} q_{K+1} = 0$. The virtual value of $s_k$ is the slope of the revenue curve between the points of $s_{k+1}$ and $s_k$:

$$\varphi(s_k) = \frac{s_k q_k - s_{k+1} q_{k+1}}{f_k}.$$

**The revenue identity.** Take $n$ bidders with independent values $v_i \sim F_i$ in a [single-parameter environment](/single-parameter-environment/). Let $(x, p)$ be a DSIC mechanism, so each $x_i$ is a [monotone allocation rule](/monotone-allocation-rule/) and $p_i$ is the payment of Myerson's lemma with $p_i = 0$ at the lowest value. Then for each bidder $i$,

$$\mathbb{E}_v[p_i(v)] = \mathbb{E}_v[\varphi_i(v_i)\, x_i(v)],$$

and summing over the bidders, the expected revenue is $\mathbb{E}_v[\sum_i \varphi_i(v_i) x_i(v)]$. The proof writes $p_i(v) = v_i x_i(v) - \int_a^{v_i} x_i(z, v_{-i})\, dz$ and integrates by parts over $v_i$. The same identity holds for the interim rules of a BIC mechanism. With the discrete form, the sums play the role of the integrals.

## Examples and non-examples

- **Uniform values.** For $U[0, 1]$, $\varphi(v) = v - (1 - v)/1 = 2v - 1$. For $U[a, b]$, $\varphi(v) = 2v - b$. The zero $1/2$ of $2v - 1$ is the optimal [reserve price](/reserve-price/).
- **The identity at work.** One bidder with value in $U[0, 1]$ and the posted price $1/2$: the expected virtual value of the winner is $\int_{1/2}^1 (2v - 1)\, dv = 1/4$, which is the revenue $\frac12 \cdot \frac12$. Two such bidders in a [Vickrey auction](/vickrey-auction/): the winner has the larger value $\max(v_1, v_2)$, with mean $2/3$, so the expected virtual welfare is $2 \cdot 2/3 - 1 = 1/3$. This is the expected second-highest value, the revenue of the Vickrey auction.
- **Exponential values.** For $F(v) = 1 - e^{-\lambda v}$, $(1 - F)/f = 1/\lambda$, so $\varphi(v) = v - 1/\lambda$.
- **Equal-revenue distribution.** For $F(v) = 1 - 1/v$ on $[1, \infty)$, $f(v) = 1/v^2$ and $(1 - F(v))/f(v) = v$, so $\varphi(v) = 0$ for every $v$. Every posted price $p \ge 1$ earns $p \cdot (1/p) = 1$, and the revenue curve is flat.
- **A non-monotone virtual valuation.** Values $2, 3, 5$ with probabilities $1/2, 1/6, 1/3$ give $q = (1, 1/2, 1/3)$ and $\varphi = (1, -1, 5)$. The value 3 has a lower virtual value than the value 2, so the distribution is not [regular](/regular-distribution/), and an auction must use the [ironed](/ironing/) virtual values.
- **Not a value.** A virtual value can be negative, as for $v < 1/2$ under $U[0, 1]$. Selling to such a bidder at any price that keeps the mechanism truthful lowers the expected revenue, which is why optimal auctions sometimes keep the item.
- **Not the same as the bid.** Two bidders can have the same value and different virtual values. With $v_1 \sim U[0, 1]$ and $v_2 \sim U[0, 2]$, the value $0.9$ has virtual value $0.8$ for bidder 1 and $-0.2$ for bidder 2.

## Related definitions

- **Regular distribution.** A distribution whose virtual valuation is nondecreasing, equivalently whose revenue curve is concave ([regular distribution](/regular-distribution/)).
- **Hazard rate.** With $h(v) = f(v)/(1 - F(v))$, $\varphi(v) = v - 1/h(v)$. A nondecreasing hazard rate (MHR) makes $\varphi$ increasing, with slope at least 1.
- **Ironed virtual valuation.** The slope $\bar\varphi$ of the concave hull of the revenue curve. It equals $\varphi$ for regular distributions and is nondecreasing for all distributions ([ironing](/ironing/)).
- **Virtual welfare.** The sum $\sum_i \varphi_i(v_i) x_i$. [Myerson's optimal auction](/myerson-optimal-auction/) maximizes the ironed version pointwise.
- **Monopoly price.** For a regular $F$, the price $\varphi^{-1}(0)$, which maximizes $p(1 - F(p))$, the revenue from one bidder.
- **Revenue equivalence.** The identity shows that the expected revenue depends only on the allocation rule, which is the [revenue equivalence theorem](/revenue-equivalence-theorem/) for independent private values.

## References
