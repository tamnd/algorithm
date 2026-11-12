---
tag: E7P3Z6
kind: theorem
slug: consistent-hashing-max-load-bound
name: Consistent hashing load bound
aliases:
- Karger et al. load bound
- largest arc of a hash ring
area: systems/load-balancing-and-hashing
level: advanced
summary: "With one random point per server, the largest share of a hash ring is Theta(log n / n) w.h.p.; with v = Omega(log n) points per server, every share is within a constant factor of 1/n."
prereqs: [consistent-hashing, virtual-nodes, chernoff-bound, union-bound, chebyshev-inequality]
see_also: [balance-property, hash-ring, balls-into-bins-max-load, bounded-load-consistent-hashing, multi-probe-consistent-hashing, rendezvous-hashing, high-probability-bounds, load-skew]
sources:
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, distributed caching protocols for relieving hot spots on the World Wide Web, STOC 1997
    locator: pp. 654 to 663, Section 4.2 (buckets and items on the unit interval, kappa log C points per bucket, an item goes to the closest point) and Theorem 4.1 (balance, monotonicity, spread and load, with a proof sketch)
  - paper: doi:10.1111/j.1469-1809.1939.tb02216.x
    title: W. L. Stevens, Solution to a geometrical problem in probability, Annals of Eugenics 9(4), 1939
    locator: pp. 315 to 320, the probability that n random arcs of length a cover the circle, which is the law of the largest gap
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Section 4.2.1 (Theorem 4.4, the Chernoff bound used for the key counts) and Chapter 5 (balls into bins)
  - paper: doi:10.1145/383059.383071
    title: Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek and Hari Balakrishnan, Chord, a scalable peer-to-peer lookup service for Internet applications, SIGCOMM 2001
    locator: the load balance experiments, where each real node runs r virtual nodes and r = O(log N) evens out the keys per node
---

The consistent hashing load bound says how uneven the shares of a [hash ring](/hash-ring/) are. With $n$ servers at one random point each, the largest share is $\Theta(\log n/n)$ with high probability, about $\ln n$ times the average $1/n$, and its expected value is exactly $H_n/n$. With $v$ random points per server ([virtual nodes](/virtual-nodes/)), every share is within a factor $1 \pm O(\sqrt{\log n/v})$ of $1/n$ with high probability, so $v = \Theta(\log n)$ points give a constant factor. This is the [balance property](/balance-property/) of [consistent hashing](/consistent-hashing/) that Karger et al. stated in 1997, here with explicit constants and a full proof.

## Statement

**Model.** The ring is the circle $[0, 1)$. There are $n$ servers, and each has $v \ge 1$ points. All $nv$ points are independent and uniform, which models an ideal hash of the server names. A key goes to the first point clockwise from it, so each point owns the arc from the point before it. The *share* $A_s$ of server $s$ is the total length of the arcs of its points. The shares add up to 1, so the average share is $1/n$. Keys are independent uniform positions. The bounds hold over the random points (and the random keys in part (c)); they are not worst case. Let $H_n = 1 + 1/2 + \cdots + 1/n$ and $(y)_+ = \max(y, 0)$.

**Theorem.**

(a) *One point per server.* Let $n \ge 2$, $v = 1$, and let $L = \max_s A_s$. For $x \ge 0$,

$$ \Pr[L > x] = \sum_{k=1}^{n} (-1)^{k+1}\binom nk (1 - kx)_+^{\,n-1}, \qquad \mathbb E[L] = \frac{H_n}{n}, \qquad \mathbb E\bigl[\min_s A_s\bigr] = \frac1{n^2}. $$

For every $c > 0$ and $0 < \epsilon < 1$,

$$ \Pr\Bigl[L > \frac{(1+c)\ln n}{n-1}\Bigr] \le n^{-c}, \qquad \Pr\Bigl[L \le \frac{(1-\epsilon)\ln n}{n}\Bigr] \le e\,n^{-\epsilon}. $$

(b) *$v$ points per server.* For every $0 < \delta < 1$,

$$ \Pr\Bigl[\text{some share lies outside } \Bigl[\frac{1-\delta}{(1+\delta)n}, \frac{1+\delta}{(1-\delta)n}\Bigr]\Bigr] \le 2n\,e^{-v\delta^2/4}. $$

So $v \ge (4/\delta^2)\ln(2n^{c+1})$ points per server keep every share in that window with probability at least $1 - n^{-c}$. In the form "1 plus a small term": if $v \ge 16\ln(2n^{c+1})$ and $\delta = 2\sqrt{\ln(2n^{c+1})/v}$, then with probability at least $1 - n^{-c}$ every share lies in $[(1-2\delta)/n, (1+4\delta)/n]$.

(c) *Keys.* If every share is at most $\alpha/n$ and $m$ keys are placed, then for $0 < \epsilon \le 1$ some server gets at least $(1+\epsilon)\alpha m/n$ keys with probability at most $n\,e^{-\epsilon^2 m/(3n)}$. With the $v$ of (b) and $m \ge 3(c+1)n\ln n/\epsilon^2$, every server holds at most $(1+\epsilon)\frac{1+\delta}{1-\delta}\cdot\frac mn$ keys with probability at least $1 - 2n^{-c}$.

**Relation to Karger et al.** Theorem 4.1 of Karger et al. says that their family, with $\kappa\log C$ points per bucket, is balanced: in a fixed view $\mathcal V$, an item goes to a given bucket with probability $O(1/|\mathcal V|)$. They put points on the unit interval, send an item to the *closest* point, need only $\log C$-wise independent hashing, and give a proof sketch. Part (b) is the statement for the circle with the clockwise rule and fully random points. The proof file shows that the closest point rule on the circle gives the same window with failure probability $4n\,e^{-v\delta^2/4}$.

## In plain words

Throw a few darts at random on the rim of a wheel, one for each server. Each server gets the stretch of rim behind its dart. Random darts do not land evenly. Some fall close together and leave a tiny stretch, and somewhere there is a large empty stretch. With a thousand servers, the largest stretch is on average about seven and a half times the fair share, and the smallest is about a thousandth of it.

Now let every server throw many darts and add up its stretches. The sum of many random pieces is much steadier than one piece, so every server ends up close to its fair share. The number of darts that each server needs grows only with the logarithm of the number of servers.

## Proof

The full proof is in the proof file. The outline:

1. **Arcs are uniform on the simplex.** Turn the circle so that one point is at 0. The other points are independent and uniform, so the arcs are the spacings of uniform order statistics, and their joint law is uniform on $\{a \ge 0, \sum a = 1\}$. The labels of the points are a random order that is independent of the arc lengths.
2. **Several long arcs.** For a fixed set of $k$ arcs, $\Pr[\text{all } k \text{ are longer than } x] = (1 - kx)_+^{\,n-1}$: shifting each of the $k$ coordinates by $x$ and scaling maps the event onto the whole simplex. Inclusion and exclusion gives the law of $L$, and integrating the tail gives $\mathbb E[L] = \frac1n\sum_k (-1)^{k+1}\binom nk\frac1k = H_n/n$.
3. **Upper bound of (a).** The term $k = 1$ and the [union bound](/union-bound/) give $\Pr[L > x] \le n(1-x)^{n-1} \le n\,e^{-x(n-1)}$.
4. **Lower bound of (a).** Let $X$ count the arcs longer than $x$. Step 2 gives $\mathrm{Var}[X] \le \mathbb E[X] = n(1-x)^{n-1}$, because $(1 - 2x)_+ \le (1-x)^2$. By [Chebyshev's inequality](/chebyshev-inequality/), $\Pr[L \le x] = \Pr[X = 0] \le 1/\mathbb E[X]$, which is at most $e\,n^{-\epsilon}$ at $x = (1-\epsilon)\ln n/n$.
5. **Exponential representation for (b).** With $E_1, \ldots, E_{nv}$ independent exponential variables of mean 1 and $T$ their sum, the vector $E/T$ is uniform on the simplex. So $A_s = G_s/T$, where $G_s$ is the sum of the $v$ variables of server $s$, and $T = \sum_s G_s$.
6. **Concentration.** A Chernoff argument on the moment generating function $(1-\lambda)^{-v}$ gives $\Pr[G_s \notin (1 \pm \delta)v] \le 2e^{-v\delta^2/4}$. If every $G_s$ is in this range, then so is $T/n$, and each ratio $G_s/T$ is in the window. The union bound over the $n$ servers finishes (b).
7. **Keys.** Given the shares, a server's key count is binomial with parameters $m$ and $A_s \le \alpha/n$, and the [Chernoff bound](/chernoff-bound/) with the union bound gives (c).

## Consequences

- **Why virtual nodes are needed.** One point per server makes the busiest server hold about $\ln n$ times its fair share of the ring, and some server holds about $1/n$ of its fair share. Part (b) shows that $\Theta(\log n)$ points per server fix both ends at once. This is the reason for the $\kappa\log C$ points of Karger et al. and for the [virtual nodes](/virtual-nodes/) of Chord, Dynamo and Cassandra.
- **The price.** The ring holds $nv = \Theta(n\log n)$ points, and a lookup is a binary search over them, $O(\log(nv))$ time. Tighter balance costs more: the window $1 \pm \delta$ needs $v = O(\log n/\delta^2)$.
- **Servers of different size.** If server $s$ has $v_s$ points out of $V = \sum_s v_s$, the same proof puts each $A_s$ within the factors $(1 \pm \delta)/(1 \mp \delta)$ of $v_s/V$, with failure probability at most $2n\,e^{-\delta^2\min_s v_s/4}$. So shares follow the weights once the smallest server has $\Omega(\log n)$ points.
- **Each view separately.** The bound holds for any fixed set of $n$ servers, so in the [views model](/spread-and-load/) it applies to each view on its own. With the union bound it holds for polynomially many fixed views at once, at the cost of a larger constant in $v$.
- **Keys against shares.** Part (c) needs $m = \Omega(n\log n)$ keys. With fewer keys the count of keys adds its own randomness on top of the shares, as in [balls into bins](/balls-into-bins-max-load/).

## Tightness

**Part (a) is tight up to the constant in front of $\ln n$.** The largest share lies between $(1-\epsilon)\ln n/n$ and $(1+c)\ln n/(n-1)$ with high probability. Exact values from the formula for $n = 1000$ servers with one point each:

| event | exact probability | bound of the theorem |
| --- | --- | --- |
| $nL > 10$ | 0.0428 | 0.0436 (union bound $n(1 - x)^{n-1}$) |
| $nL > 12$ | 0.00577 | 0.00578 |
| $nL > 13.83$, that is $c = 1$ | 0.000908 | $n^{-1} = 0.001$ |
| $nL \le 6$ | 0.0766 | 0.408 (second moment $1/(n(1-x)^{n-1})$) |
| $nL \le 5$ | 0.00063 | 0.150 |
| $nL \le 3.454$, that is $\epsilon = 1/2$ | $5.4 \times 10^{-19}$ | $e\,n^{-1/2} = 0.086$ |

The mean of $nL$ is $H_{1000} = 7.485$, against $\ln 1000 = 6.91$. The union bound is almost exact in the upper tail. The second moment bound is far from the truth in the lower tail, but it is enough for the order $\ln n/n$.

**Part (b) has a loose constant.** The proof needs $v = 159$ points for $n = 100$ and $v = 233$ for $n = 1000$ to keep all shares within a factor 3 of $1/n$ (with $c = 1$ and $\delta = 1/2$), and $634$ and $929$ for a factor $5/3$ ($\delta = 1/4$). Simulated rings need far fewer points. The table gives $n$ times the largest share, for 20 rings per row (8 for the last row), all drawn from Python `random.Random(2026)`:

| $n$ | $v$ | mean | range | mean of $n$ times smallest share | $1 + \sqrt{2\ln n/v}$ |
| --- | --- | --- | --- | --- | --- |
| 100 | 1 | 5.50 | 3.63 to 8.12 | 0.011 | 4.03 |
| 100 | 4 | 2.74 | 2.09 to 3.74 | 0.172 | 2.52 |
| 100 | 16 | 1.73 | 1.53 to 2.01 | 0.473 | 1.76 |
| 100 | 64 | 1.32 | 1.22 to 1.48 | 0.701 | 1.38 |
| 100 | 256 | 1.16 | 1.10 to 1.22 | 0.858 | 1.19 |
| 1000 | 1 | 7.45 | 5.72 to 9.42 | 0.0009 | 4.72 |
| 1000 | 4 | 3.53 | 2.84 to 5.84 | 0.090 | 2.86 |
| 1000 | 16 | 2.01 | 1.79 to 2.33 | 0.396 | 1.93 |
| 1000 | 64 | 1.47 | 1.38 to 1.56 | 0.643 | 1.47 |
| 1000 | 256 | 1.20 | 1.18 to 1.23 | 0.803 | 1.23 |

The last column is the normal approximation to the largest of $n$ sums of $v$ exponential variables. It is a heuristic, not a proved bound, and it is poor for small $v$, but for $v \ge 16$ it matches the measured means within 0.1. It suggests that the factor $1 + \Theta(\sqrt{\log n/v})$ of part (b) has the right form; this page does not prove the matching lower bound.

**Part (c) cannot beat balls into bins.** Even with perfect shares of exactly $1/n$, placing $m = n$ keys gives a busiest server with $(1 + o(1))\ln n/\ln\ln n$ keys with high probability ([balls into bins](/balls-into-bins-max-load/)). So no number of virtual nodes makes the key counts even when there are few keys per server; [bounded-load consistent hashing](/bounded-load-consistent-hashing/) caps the counts directly.

## History

Karger, Lehman, Leighton, Panigrahy, Levine and Lewin introduced consistent hashing at STOC 1997. Their Theorem 4.1 states balance for buckets with $\kappa\log C$ points each on the unit interval, and their proof sketch counts the ways in which a bucket's points can own a large part of the interval. The exact law of the largest gap is a classical result of geometric probability: Stevens in 1939 gave the probability that $n$ random arcs of equal length cover the circle, which is the probability that no gap is longer than the arcs. Chord runs $O(\log N)$ virtual nodes on each real node to even out the keys, for the reason that part (b) makes exact.

## References
