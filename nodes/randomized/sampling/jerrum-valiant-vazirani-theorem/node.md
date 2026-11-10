---
tag: Z95ZM0
kind: theorem
slug: jerrum-valiant-vazirani-theorem
name: Jerrum-Valiant-Vazirani theorem
aliases:
- counting and sampling are interreducible
- counting-sampling equivalence
- JVV theorem
- equivalence of approximate counting and almost uniform sampling
area: randomized/sampling
level: research
summary: For self-reducible problems, approximate counting and approximate uniform sampling are polynomially equivalent.
prereqs: [self-reducibility, fpras, total-variation-distance, hoeffding-inequality, median-trick]
see_also: [fpras, approximate-counting, self-reducibility, karp-luby-estimator, mixing-time, rapid-mixing, counting-perfect-matchings, rejection-sampling]
sources:
  - paper: doi:10.1016/0304-3975(86)90174-X
    title: Mark R. Jerrum, Leslie G. Valiant and Vijay V. Vazirani, Random generation of combinatorial structures from a uniform distribution, Theoretical Computer Science 43, 169 to 188, 1986
    locator: the definitions of self-reducible relations, randomized approximate counting and almost uniform generation, and the theorems that show the two are interreducible for self-reducible relations
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Algorithms and Complexity, Lectures in Mathematics ETH Zurich, Birkhauser, 2003
    locator: the chapter on sampling and counting (the definitions of FPRAS and FPAUS and the reductions between them)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 11 (The Monte Carlo Method), the section on going from approximate sampling to approximate counting, with independent sets as the example
  - paper: doi:10.1145/1008731.1008738
    title: Mark Jerrum, Alistair Sinclair and Eric Vigoda, A polynomial-time approximation algorithm for the permanent of a matrix with nonnegative entries, Journal of the ACM 51(4), 671 to 697, 2004
    locator: the main theorem (an FPRAS for the permanent of a nonnegative matrix), obtained through an almost uniform sampler
---

## Statement

Let $R$ be a relation between instances $x$ and witnesses $w$, and let $W(x) = \{w : (x, w) \in R\}$ and $N(x) = |W(x)|$. For example, $x$ is a graph and $W(x)$ is its set of matchings.

- An *FPRAS* for $R$ is a randomized algorithm that, given $x$ and $\varepsilon \in (0, 1]$, outputs $\tilde N$ with $e^{-\varepsilon} N(x) \le \tilde N \le e^{\varepsilon} N(x)$ with probability at least $3/4$, in time polynomial in $|x|$ and $1/\varepsilon$. See [FPRAS](/fpras/).
- An *FPAUS* (fully polynomial almost uniform sampler) for $R$ is a randomized algorithm that, given $x$ and $\delta \in (0, 1]$, outputs an element of $W(x)$ or the symbol $\bot$, with a distribution within [total variation distance](/total-variation-distance/) $\delta$ of the uniform distribution on $W(x)$, in time polynomial in $|x|$ and $\log(1/\delta)$. If $W(x)$ is empty, the target distribution is the one that always outputs $\bot$.

$R$ is *self-reducible* (in the simple form used here) when witnesses of $x$ are bit strings of a length $m(x)$ that is polynomial in $|x|$ and computable in polynomial time, and there is a polynomial-time map $(x, a) \mapsto x_a$ for $a \in \{0, 1\}$ such that, when $m(x) \ge 1$:

- $W(x_a) = \{w' : a w' \in W(x)\}$, the witnesses of $x$ that begin with $a$, with the first bit removed;
- $m(x_a) = m(x) - 1$ and $|x_a| \le |x|$;

and when $m(x) = 0$ one can decide in polynomial time whether the empty string is a witness. See [self-reducibility](/self-reducibility/).

**Theorem (Jerrum, Valiant and Vazirani 1986).** Let $R$ be self-reducible.

1. If $R$ has an FPRAS, then $R$ has an FPAUS.
2. If $R$ has an FPAUS, then $R$ has an FPRAS.

So for self-reducible problems, approximate counting and almost uniform sampling are equally hard, up to polynomial factors.

## In plain words

Self-reducible means that the answers to a problem split into two groups, by their first choice, and each group is the answer set of a smaller problem of the same kind.

If you can count, you can sample: count both groups, step into one of them with chance in proportion to its size, and repeat until the answer is complete. Each answer is then reached with about the same chance.

If you can sample, you can count: draw many samples, see what fraction falls in the bigger group, and step into it. The total count is the count at the end of the path divided by the product of all those fractions.

## Proof

Write $m = m(x)$ and let $x = x^{(0)}, x^{(1)}, \ldots, x^{(m)}$ be a path in which each $x^{(i+1)}$ is $x^{(i)}_a$ for some bit $a$. Self-reducibility gives the identity
$$N(x^{(i)}) = N(x^{(i)}_0) + N(x^{(i)}_1),$$
because each witness of $x^{(i)}$ begins with 0 or with 1. All instances on a path have size at most $|x|$.

**Part 2 (sampling to counting).** Fix $\varepsilon \in (0, 1]$. If $W(x)$ is empty, a sample from the FPAUS with $\delta = 1/8$ is $\bot$ with probability at least $7/8$, while for nonempty $W(x)$ it is a witness with probability at least $7/8$. So the majority of 9 samples decides whether $N(x) = 0$, with error probability below $0.003$, and we output 0 in that case. Otherwise build the path step by step. At $x^{(i)}$:

- draw $t$ independent samples from the FPAUS on $x^{(i)}$ with $\delta = \varepsilon / (24m)$;
- let $\hat p_a$ be the fraction of the samples that are witnesses beginning with $a$, choose the $a$ with the larger $\hat p_a$, and set $x^{(i+1)} = x^{(i)}_a$ and $\hat p^{(i)} = \hat p_a$.

At the end, $x^{(m)}$ has one witness, the empty string, because the path only enters parts that contained a sample. Output $\tilde N = 1 / \prod_i \hat p^{(i)}$.

Let $p^{(i)} = N(x^{(i+1)}) / N(x^{(i)})$ be the true fraction of the chosen part. Then the product telescopes:
$$\prod_{i=0}^{m-1} p^{(i)} = \frac{N(x^{(m)})}{N(x^{(0)})} = \frac{1}{N(x)}.$$
For one step, $E[\hat p_a]$ is the probability that the sampler outputs a witness beginning with $a$, which is within $\delta$ of $p_a = N(x^{(i)}_a)/N(x^{(i)})$. Let $\eta = \varepsilon/(24m)$. By the [Hoeffding inequality](/hoeffding-inequality/), $|\hat p_a - E[\hat p_a]| \le \eta$ for both $a$ except with probability $4 e^{-2t\eta^2}$. With $t = \lceil (288 m^2/\varepsilon^2) \ln(20m) \rceil$, this is at most $1/(5m)$. On the good event, $|\hat p_a - p_a| \le \eta + \delta = 2\eta$ for both $a$. The sampler outputs $\bot$ with probability at most $\delta = \eta$, so $\hat p_0 + \hat p_1 \ge 1 - 3\eta$, the chosen $\hat p_a$ is at least $1/2 - 3\eta/2$, and $p_a \ge 1/2 - 7\eta/2 > 1/3$. So the relative error is at most $2\eta \cdot 3 = \varepsilon/(4m) \le 1/4$, and from $1 - y \ge e^{-2y}$ and $1 + y \le e^{y}$ for $0 \le y \le 1/2$,
$$e^{-\varepsilon/(2m)} \le \hat p^{(i)} / p^{(i)} \le e^{\varepsilon/(2m)}.$$
By the [union bound](/union-bound/), the zero test and all $m$ steps are good except with probability $1/5 + 0.003 < 1/4$, and then $\tilde N / N(x)$ lies between $e^{-\varepsilon/2}$ and $e^{\varepsilon/2}$. The algorithm uses $O(m^3 \log m / \varepsilon^2)$ calls to the sampler with $\log(1/\delta) = O(\log(m/\varepsilon))$, so its time is polynomial in $|x|$ and $1/\varepsilon$.

**Part 1 (counting to sampling).** First boost the FPRAS with the [median trick](/median-trick/): the median of $O(\log(1/\beta))$ runs is accurate, within $e^{\pm\varepsilon}$, except with probability $\beta$. A single *walk* does this, with $\varepsilon = 1/m$:

1. Compute an estimate $\tilde N$ of $N(x)$ once, before all walks. If $\tilde N = 0$, output $\bot$.
2. Walk down from $x$. At $x^{(i)}$, compute estimates $\tilde N_0, \tilde N_1$ of $N(x^{(i)}_0), N(x^{(i)}_1)$, choose $a$ with probability $r^{(i)} = \tilde N_a / (\tilde N_0 + \tilde N_1)$, and set $x^{(i+1)} = x^{(i)}_a$.
3. At the end, let $w$ be the bits chosen and $P = \prod_i r^{(i)}$. Accept $w$ with probability $\min\{1, \alpha / P\}$, where $\alpha = e^{-3}/\tilde N$.

Run up to $T = \lceil e^4 \ln(2/\delta) \rceil$ walks and output the first accepted $w$, or $\bot$ if none is accepted.

Consider first an *ideal* run in which every estimate is accurate. An accurate estimate of 0 is 0, so a walk never enters an empty part, and $w \in W(x)$. Each ratio $r^{(i)}$ is within a factor $e^{\pm 2/m}$ of the true ratio $N(x^{(i+1)})/N(x^{(i)})$, so $P \ge e^{-2}/N(x)$ by the telescoping product. Also $\tilde N \ge e^{-1} N(x)$, so $\alpha \le e^{-2}/N(x) \le P$ and the minimum in step 3 is $\alpha / P$. Fix a witness $w$. The walk follows the path of $w$ with probability $E\big[\prod_i r^{(i)}\big]$, where the estimates along the path are random, and it then accepts with probability $\alpha / \prod_i r^{(i)}$. The two factors cancel inside the expectation, so
$$\Pr[\text{a walk outputs } w] = \alpha \quad \text{for every } w \in W(x).$$
So an accepted output is exactly uniform on $W(x)$, and a walk accepts with probability $N(x)\,\alpha = e^{-3} N(x)/\tilde N \ge e^{-4}$. All $T$ walks reject with probability at most $(1 - e^{-4})^T \le \delta/2$. So the ideal run is within total variation distance $\delta/2$ of uniform.

The real run uses at most $1 + 2mT$ estimates. Boost each one to fail with probability $\beta = \delta / (2(1 + 2mT))$. The real run and the ideal run can be coupled so that they agree unless some estimate is inaccurate, which happens with probability at most $\delta/2$. So the real output is within $\delta$ of uniform. Each estimate takes time polynomial in $|x|$ and $m$, times $O(\log(1/\beta)) = O(\log(m/\delta))$, and $T = O(\log(1/\delta))$, so the time is polynomial in $|x|$ and $\log(1/\delta)$. $\blacksquare$

## Consequences

- **Counting through Markov chains.** For most hard counting problems the known FPRAS goes through part 2: design a Markov chain whose stationary distribution is uniform on $W(x)$, prove that it [mixes rapidly](/rapid-mixing/), and use it as the sampler. Jerrum and Sinclair counted matchings this way in 1989, Dyer, Frieze and Kannan estimated the volume of a convex body in 1991, and Jerrum, Sinclair and Vigoda gave an FPRAS for the permanent of a nonnegative matrix in 2004, which counts [perfect matchings](/counting-perfect-matchings/) of bipartite graphs. See [mixing time](/mixing-time/) and [Glauber dynamics](/glauber-dynamics/).
- **Sampling from exact counts.** When $N$ can be computed exactly in polynomial time, the walk of part 1 with exact counts outputs an exactly uniform witness with no rejection. Examples are spanning trees through the [matrix tree theorem](/matrix-tree-theorem/) and perfect matchings of planar graphs through the [Kasteleyn method](/kasteleyn-method/).
- **DNF formulas.** The [Karp-Luby estimator](/karp-luby-estimator/) is an FPRAS for the number of satisfying assignments of a DNF formula, and setting a variable keeps a DNF formula a DNF formula, so part 1 gives an almost uniform sampler. Here the estimator also samples directly.
- **Hardness transfers too.** If a self-reducible problem has no FPRAS, it has no FPAUS. For example, the number of satisfying assignments of a CNF formula cannot be approximated in polynomial time unless NP = RP, since an FPRAS must tell 0 apart from at least 1, so CNF solutions cannot be sampled almost uniformly either.

**Example with exact numbers.** Let $x$ be the cycle on 5 vertices, witnesses its matchings, and let the bits say, edge by edge, whether the edge is in the matching. The cycle has $N = 11$ matchings: the empty one, 5 with one edge and 5 with two edges. Deciding the first edge splits them into 8 without it (the matchings of a path on 5 vertices) and 3 with it (a path on 3 vertices). Following the larger part each time, the path visits paths on 5, 4, 3, 2 vertices and then an empty graph, with fractions
$$\frac{8}{11} \cdot \frac{5}{8} \cdot \frac{3}{5} \cdot \frac{2}{3} \cdot \frac{1}{2} = \frac{1}{11},$$
so the inverse of the product is $11$, as part 2 says. In part 1 with exact counts, the empty matching is reached with probability exactly this product, $1/11$, and the same holds for every other matching.

## Tightness

- **Approximate, not exact.** The theorem relates approximate counting to almost uniform sampling only. Exact counting can be much harder: counting perfect matchings of bipartite graphs is #P-complete (Valiant 1979), yet it has an FPRAS and an FPAUS.
- **The precision can be weakened.** Sinclair and Jerrum (1989) showed that, for self-reducible problems, a counter that is only correct within a polynomial factor can be boosted to an FPRAS, by a Markov chain on the tree of the self-reduction. So the dividing line is between counting within some polynomial factor and not counting at all.
- **Self-reducibility matters.** Both reductions use the split of $W(x)$ into $W(x_0)$ and $W(x_1)$. Without it, the samples give no handle on the size of $W(x)$, and a count gives no handle on how to build a single witness.
- **Polynomial cost.** The reductions lose polynomial factors: part 2 uses $O(m^3 \log m / \varepsilon^2)$ samples. Direct methods are often faster, for example a Markov chain with simulated annealing for counting.

## History

Schnorr defined self-reducibility in 1976, and Valiant defined the class #P of counting problems in 1979. Stockmeyer showed in 1983 that #P functions can be approximated in randomized polynomial time with an NP oracle. Jerrum, Valiant and Vazirani published the equivalence of approximate counting and almost uniform generation in Theoretical Computer Science in 1986. In the same paper they used it to show that cycles in a directed graph cannot be sampled almost uniformly unless NP = RP. Broder proposed a Markov chain for sampling perfect matchings in 1986. Sinclair and Jerrum proved it mixes rapidly for dense graphs in 1989, which made the theorem the base of the Markov chain Monte Carlo method for approximate counting. The theorem is different from the [Valiant-Vazirani theorem](/valiant-vazirani-theorem/) of the same year, which reduces SAT to unique SAT.

## References
