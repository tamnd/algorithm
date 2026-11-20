---
tag: Y8ZAS3
kind: technique
slug: ironing
name: Ironing
aliases:
- Myerson ironing
area: algorithmic-game-theory/auctions
level: advanced
summary: "Replaces the virtual valuation of an irregular distribution by the slope of the concave hull of its revenue curve. The result is monotone and keeps the optimal revenue."
prereqs: [virtual-valuation, regular-distribution, upper-and-lower-hull]
see_also: [myerson-optimal-auction, sequential-posted-pricing, reserve-price, isotonic-regression, pool-adjacent-violators, monotone-allocation-rule, convex-hull]
sources:
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the ironing procedure, which replaces the integral of the virtual valuation in quantile space by its convex hull, for distributions that are not regular
  - paper: doi:10.1086/261643
    title: "Jeremy Bulow and John Roberts, The simple economics of optimal auctions, Journal of Political Economy 97(5) (1989), 1060-1090"
    locator: ironing as the use of the concave hull of the revenue curve of a monopolist, with marginal revenue in place of the virtual valuation
  - paper: "Jason D. Hartline, Mechanism Design and Approximation, book draft, version with Chapters 1 to 7 revised in September 2021, https://jasonhartline.com/MDnA/"
    locator: Chapter 3, Optimal mechanisms (revenue curves, the ironed revenue curve as a concave hull, and the optimality of ironed virtual surplus maximization)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 13, Jason D. Hartline and Anna R. Karlin, Profit maximization in mechanism design (the optimal mechanism for distributions that are not regular)
---

Ironing turns the [virtual valuation](/virtual-valuation/) of a distribution that is not [regular](/regular-distribution/) into a nondecreasing function, the *ironed* virtual valuation, without loss of optimal revenue. It draws the revenue curve $R(q)$ in quantile space, replaces it by its least concave majorant $\bar R$, and uses the slope of $\bar R$ in place of the slope of $R$. On the intervals where $\bar R$ lies above $R$, the ironed value is constant, and an optimal mechanism treats all values in such an interval alike. [Myerson's lemma](/myerson-lemma/) says that a truthful allocation must be monotone in the value. Ironing is the step that makes the revenue-maximizing allocation of [Myerson's optimal auction](/myerson-optimal-auction/) monotone when the raw virtual valuation is not.

## In plain words

A seller wants to rank bidders by how much revenue each one brings. For most distributions of values, a bidder with a higher value brings more. For some distributions it does not: a value in a thin middle range can look worse to the seller than a lower value. But an auction cannot reward a lower bid over a higher one, or bidders would lie. Ironing fixes this by pooling. It finds the ranges where the ranking goes the wrong way and gives every value in such a range the same average score. The scores then never go down as the value goes up, and the seller loses nothing, because the best possible auction would treat these values alike anyway. The name comes from pressing out the bumps of a curve.

## When it applies

- A revenue problem with independent single-parameter agents whose value distribution is not regular, for example a bimodal one or a discrete one with a small middle mass.
- Any problem that asks to maximize $\mathbb{E}[\varphi(v) x(v)]$ over nondecreasing $x$, where $\varphi$ is not monotone. Ironing gives the optimal value $\mathbb{E}[\bar\varphi(v) x(v)]$, attained by any $x$ that is optimal for $\bar\varphi$ and constant on the ironed intervals.
- One buyer with a constraint on the sale probability: the best revenue with sale probability $q$ is $\bar R(q)$, reached by a random price between two hull vertices. This is the building block of [sequential posted pricing](/sequential-posted-pricing/).

## The template

For a discrete distribution on $s_1 < \cdots < s_K$, the revenue curve has the points $(0, 0)$ and $(q_k, s_k q_k)$ with $q_k = \Pr[v \ge s_k]$.

```pseudo id=main
IRON(s_1 < ... < s_K, f_1, ..., f_K)
L1  P ← (0, 0), then (q_k, s_k q_k) for k = K down to 1          ▷ increasing q
L2  H ← vertices of the upper concave hull of P (monotone chain)
L3  for each pair (a, b) of consecutive vertices of H:
L4      give every curve segment from a to b the slope of the chord from a to b
L5      if b ≥ a + 2: record the values of those segments as one ironed interval
L6  return the slopes, in increasing order of value, and the ironed intervals
```

The ironed value of $s_k$ is $\bar\varphi(s_k)$, the slope assigned to its segment. On an ironed interval it equals the $f$-weighted mean of the raw virtual values $\varphi(s_k) = (s_k q_k - s_{k+1} q_{k+1})/f_k$ of that interval. For a continuous distribution the same holds with $\bar R$ the least concave function above $R$ and $\bar\varphi(v) = \bar R'(1 - F(v))$. The proof that the slopes are nondecreasing, that they keep the virtual surplus of every allocation that is constant on ironed intervals, and that they never lower it for monotone allocations is in `proofs/correctness.md`.

## Classic examples

- **A discrete irregular distribution.** Values $2, 3, 5$ with probabilities $1/2, 1/6, 1/3$ have $q = (1, 1/2, 1/3)$ and revenue curve points $(0, 0)$, $(1/3, 5/3)$, $(1/2, 3/2)$ and $(1, 2)$. The raw virtual values are $(1, -1, 5)$. The point $(1/2, 3/2)$ lies below the chord from $(1/3, 5/3)$ to $(1, 2)$, of slope $1/2$, so the values 2 and 3 form one ironed interval and $\bar\varphi = (1/2, 1/2, 5)$. Check: $(1 \cdot \frac12 + (-1) \cdot \frac16)/(\frac12 + \frac16) = 1/2$.
- **The optimal auction.** With two bidders from the distribution above, Myerson's auction ranks by $\bar\varphi$, so bids 2 and 3 tie, and the expected revenue is 3. The Vickrey auction earns $89/36$. Ranking by the raw $\varphi$ is not monotone: the value 3 has $\varphi = -1$ and never wins, while the value 2 can win, so no payment rule makes that ranking truthful.
- **A single buyer.** The best posted price is a hull vertex: for the distribution above, price 2 sells for sure and earns 2, price 5 earns $5/3$, and price 3 earns only $3/2$, the point below the hull. To sell with probability exactly $1/2$, the best a seller can do is the price 5 or 2 with probability $3/4$ and $1/4$, which earns $\bar R(1/2) = 7/4$, while the price 3 earns $3/2$.
- **A negative ironed value.** Values $1, 2, 5$ with probabilities $1/2, 1/4, 1/4$ have $\varphi = (0, -1, 5)$ and $\bar\varphi = (-1/3, -1/3, 5)$. A single buyer is offered the price 5, for revenue $5/4$.

## Variations

- **Isotonic regression.** The ironed values are the weighted [isotonic regression](/isotonic-regression/) of the raw virtual values with weights $f_k$: the nondecreasing sequence closest to $\varphi$ in weighted squared error. The [pool adjacent violators](/pool-adjacent-violators/) algorithm computes it by merging adjacent blocks that are out of order into their weighted mean, which gives the same answer as the hull.
- **Myerson's form.** Myerson writes the quantile as $t = F(v)$ and takes the convex hull of $H(t) = \int_0^t \varphi(F^{-1}(u))\, du$. This is the same construction seen from the other end of the quantile axis.
- **Ironing in other mechanism design problems.** The same pooling of types appears as bunching in monopoly screening and in nonlinear pricing, whenever a pointwise optimum violates the monotonicity that incentive compatibility needs.
- **Ex ante relaxation.** The concave hull $\bar R$ is also the revenue curve of a seller who may randomize over prices. The ex ante relaxation of a multi-bidder problem uses $\bar R_i$ for each bidder.

## Pitfalls

- **Ironing in value space.** The hull must be taken of the revenue curve in quantile space, or of the integral of $\varphi$ against the quantile. Taking the hull of $\varphi$ as a function of the value, or averaging $\varphi$ without the weights $f$, gives wrong values.
- **Tie rule inside an ironed interval.** An optimal auction must treat all values in an ironed interval alike. A rule that breaks ties among equal ironed values in favor of the higher raw value is no longer constant on the interval, and its revenue drops below the ironed virtual surplus.
- **"Convex" or "concave".** The hull is concave in the revenue curve picture and convex in Myerson's picture. The two are the same object, but mixing the conventions flips the sign of the slopes.
- **Exact arithmetic.** For discrete distributions the hull test compares products of rationals. Floating point can merge or split ironed intervals by mistake.
- **Regular distributions.** If the distribution is regular, ironing changes nothing. A test that finds ironed intervals for a regular distribution has a bug.

## Exercises

1. Show that for any distribution on $[a, b]$ with $a \ge 0$, $\mathbb{E}[\varphi(v)] = \mathbb{E}[\bar\varphi(v)] = a$. (Both are the rise of a curve from $(0, 0)$ to $(1, a)$.)
2. Iron the distribution with values $1, 2, 3, 4, 6$ and probabilities $3/10, 1/10, 1/10, 1/10, 2/5$. (Answer: $\bar\varphi = (-7/3, -7/3, -7/3, -7/3, 6)$, with one ironed interval of four values.)
3. Show that the optimal revenue from one buyer with sale probability at most $q$ is $\bar R(q)$ when $\bar R$ is nondecreasing up to $q$, and that a lottery over at most two prices attains it.
4. Run the pool adjacent violators algorithm on the raw virtual values $(1, -1, 5)$ with weights $(1/2, 1/6, 1/3)$ and check that it gives $(1/2, 1/2, 5)$.

## References
