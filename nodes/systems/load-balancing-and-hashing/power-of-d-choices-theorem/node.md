---
tag: AKHE82
kind: theorem
slug: power-of-d-choices-theorem
name: Power of d choices theorem
aliases:
- two-choice theorem
- balanced allocations theorem
- Azar-Broder-Karlin-Upfal theorem
area: systems/load-balancing-and-hashing
level: advanced
summary: "If each of n balls goes to the least loaded of d >= 2 random bins out of n, the maximum load is ln ln n / ln d + O(1) with probability 1 - o(1/n), against about ln n / ln ln n for one choice."
prereqs: [power-of-two-choices, balls-into-bins-max-load, chernoff-bound, union-bound]
see_also: [power-of-two-choices, balls-into-bins-max-load, balls-into-bins, random-load-balancing, cuckoo-hashing-load-threshold, high-probability-bounds, load-balancing-problem]
sources:
  - paper: doi:10.1137/S0097539795288490
    title: Yossi Azar, Andrei Z. Broder, Anna R. Karlin and Eli Upfal, Balanced allocations, SIAM Journal on Computing 29(1), 1999
    locator: pp. 180 to 200, the main theorem on the greedy d-choice process (upper and lower bound ln ln n / ln d + Theta(1)) and its layered induction proof; conference version at STOC 1994
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 17, Section 17.1.1 (the upper bound, with beta_6 = n / 2e and beta_(i+1) = e beta_i^d / n^(d-1)) and Section 17.2 (the lower bound)
  - paper: doi:10.1137/S009753970444435X
    title: Petra Berenbrink, Artur Czumaj, Angelika Steger and Berthold Vöcking, Balanced allocations, the heavily loaded case, SIAM Journal on Computing 35(6), 2006
    locator: pp. 1350 to 1385, the bound m/n + ln ln n / ln d + O(1) for any number m of balls
  - paper: "Berthold Vöcking, How asymmetry helps load balancing, Journal of the ACM 50(4), 2003"
    locator: pp. 568 to 589, the Always-Go-Left bound ln ln n / (d ln phi_d) + O(1)
---

The power of d choices theorem of Azar, Broder, Karlin and Upfal says that when $n$ balls go one by one into $n$ bins, and each ball joins the least loaded of $d \ge 2$ bins drawn uniformly at random, the maximum load is $\ln\ln n/\ln d + \Theta(1)$ with probability $1 - o(1/n)$. With one random bin per ball it is $(1 + o(1))\ln n/\ln\ln n$ ([maximum load of balls into bins](/balls-into-bins-max-load/)), so a second choice gives an exponential improvement and each further choice only a constant factor. It is the guarantee behind [the power of two choices](/power-of-two-choices/) in load balancing and two-choice hashing. Its proof, the layered induction, is a standard tool of randomized analysis.

## Statement

**Process.** There are $n$ bins, all empty. Balls $1, \ldots, n$ arrive in order. Ball $t$ draws $d$ bins independently and uniformly from the $n$ bins, with replacement, and goes into a drawn bin whose current load is least. Ties are broken by any rule, even one that depends on the past.

**Theorem (Azar, Broder, Karlin and Upfal).** For each fixed $d \ge 2$, with probability $1 - o(1/n)$ the maximum load after the $n$ balls satisfies

$$ \frac{\ln\ln n}{\ln d} - O(1) \;\le\; \max_j X_j \;\le\; \frac{\ln\ln n}{\ln d} + O(1). $$

**Explicit upper bound (layered induction).** Let $\beta_6 = n/(2e)$, $\beta_{i+1} = e\,\beta_i^d/n^{d-1}$, and let $i^\ast$ be the least $i \ge 6$ with $\beta_i^d / n^{d-1} < 2\ln n$. Then for $n \ge 16$

$$ \Pr\bigl[\max_j X_j \ge i^\ast + 3\bigr] \le \frac{i^\ast + 1}{n^2} + \binom n2\Bigl(\frac{6\ln n}{n}\Bigr)^{2d}, \qquad i^\ast \le 6 + \lceil\log_d\log_2 n\rceil. $$

So the maximum load is at most $\ln\ln n/\ln d + 9 + 0.37/\ln d$ with that probability. The constant is loose; the point of the theorem is the leading term.

## In plain words

Count the bins that hold at least some number of balls. A new ball lands on top of such a bin only if all of its random picks are such bins. If a quarter of the bins are that full, two picks both hit them only one time in sixteen. So the share of bins one level higher is roughly the square of the share at this level. Squaring a small number again and again makes it tiny very fast: a half becomes a quarter, a sixteenth, a two hundred fifty-sixth. After a number of levels that is about the logarithm of the logarithm of the number of bins, no bin is left.

With one pick, the share only shrinks by a constant factor at each level, which is why the fullest bin is much higher.

## Proof

The full proof of the upper bound is in the proof file. The outline:

1. **Heights.** Give each ball a height, the load of its bin just after the ball arrives. Let $\nu_i$ be the number of bins with load at least $i$ and $\mu_i$ the number of balls with height at least $i$. A bin with load at least $i$ holds a ball of height exactly $i$, so $\nu_i \le \mu_i$.
2. **Base.** At most $n/6$ bins can hold 6 or more of $n$ balls, so $\nu_6 \le n/6 \le \beta_6$ always.
3. **One level.** If at most $\beta_i$ bins have load at least $i$ during the whole process, each ball reaches height $i + 1$ with probability at most $p_i = (\beta_i/n)^d$, because all $d$ choices must have load at least $i$. The number of such balls is then dominated by a binomial variable $\mathrm{Bin}(n, p_i)$, even though the balls are dependent. A [Chernoff bound](/chernoff-bound/) with $1 + \delta = e$ gives $\Pr[\nu_{i+1} > e\,n\,p_i = \beta_{i+1}] \le e^{-n p_i} \le n^{-2}$ while $n p_i \ge 2\ln n$.
4. **Doubly exponential decay.** The substitution $\delta_i = e^{1/(d-1)}\beta_i/n$ turns the recursion into $\delta_{i+1} = \delta_i^d$ with $\delta_6 \le 1/2$, so $\beta_{6+j} \le n\,2^{-d^j}$, and the induction stops after $\lceil\log_d\log_2 n\rceil$ levels.
5. **Last levels.** Once $n p_i < 2\ln n$, fewer than $6\ln n$ balls reach the next level with probability $1 - O(n^{-2})$, and then at most one ball reaches the level after with probability $1 - O((\ln n)^{2d}/n^{2d-2})$. A bin with load $i^\ast + 3$ would need two such balls.
6. **Union bound.** The failure probabilities of all levels add up to $o(1/n)$ by the [union bound](/union-bound/).

The lower bound runs the induction in the other direction, with lower tail bounds at each level. The proof file gives its outline and the locators of the full proof.

## Consequences

- **Load balancing.** [The power of two choices](/power-of-two-choices/) sends each job to the less loaded of two random servers and keeps the busiest server at $\ln\ln n/\ln 2 + O(1)$ jobs for $n$ jobs. Mitzenmacher's supermarket model is the dynamic version with queues.
- **Hashing.** Two-choice hashing puts each key into the shorter of two chains and gets a longest chain of $O(\log\log n)$ with $n$ keys in $n$ chains. [Cuckoo hashing](/cuckoo-hashing/) is a different use of two choices: each cell holds one key and keys move, see its [load threshold](/cuckoo-hashing-load-threshold/).
- **Diminishing returns.** Going from $d = 2$ to $d$ divides the leading term by $\log_2 d$ only. The jump from one to two choices is the large one.
- **Any number of balls.** Berenbrink, Czumaj, Steger and Vöcking proved that with $m \ge n$ balls the maximum load is $m/n + \ln\ln n/\ln d + O(1)$ with high probability, so the gap to the mean does not grow with $m$. For one choice the gap is $\Theta(\sqrt{m\ln n/n})$.

## Tightness

**The leading term is exact.** The lower bound of the theorem shows that $\ln\ln n/\ln d$ cannot be replaced by $c\ln\ln n/\ln d$ with $c < 1$ for the symmetric rule. Vöcking's Always-Go-Left rule, which splits the bins into $d$ groups and breaks ties toward the left group, reaches $\ln\ln n/(d\ln\phi_d) + O(1)$, with $\phi_d$ the growth rate of the $d$-step Fibonacci numbers. So the constant depends on the rule, not only on $d$.

**The recursion for real sizes.** The thresholds of the proof, with $n p_i = \beta_i^d/n^{d-1}$:

| $n$ | $d$ | $\beta_6, \beta_7, \ldots, \beta_{i^\ast}$ | $n p_i$ | $i^\ast$ | proof bound $i^\ast + 2$ | $\ln\ln n/\ln d$ |
| --- | --- | --- | --- | --- | --- | --- |
| $10^4$ | 2 | 1839, 920, 230 | 338, 84.6, 5.29 | 8 | 10 | 3.20 |
| $10^6$ | 2 | 183940, 91970, 22992, 1437 | 33800, 8460, 529, 2.07 | 9 | 11 | 3.79 |
| $10^6$ | 3 | 183940, 16917 | 6220, 4.84 | 7 | 9 | 2.39 |
| $10^9$ | 2 | $1.84 \times 10^8$, $9.20 \times 10^7$, $2.30 \times 10^7$, $1.44 \times 10^6$, 5613 | $3.38 \times 10^7$ down to 0.0315 | 10 | 12 | 4.37 |

**Simulation.** Seeded runs of the process (Python `random.Random(13)`; 30 runs for $n = 10^3$ and $10^4$, 8 runs for $10^5$):

| $n$ | $d$ | observed maximum load | largest excess over $\ln\ln n/\ln d$ |
| --- | --- | --- | --- |
| $10^3$ | 2 | 3 | 0.21 |
| $10^3$ | 3 | 2 to 3 | 1.24 |
| $10^4$ | 2 | 3 to 4 | 0.80 |
| $10^4$ | 3 | 3 | 0.98 |
| $10^5$ | 2 | 3 to 4 | 0.47 |
| $10^5$ | 3 | 3 | 0.78 |

Every run lies below $\ln\ln n/\ln d + 2$, far below the proof bound $i^\ast + 2$. The observed maximum for one choice at the same sizes is 4 to 10 ([maximum load of balls into bins](/balls-into-bins-max-load/)).

## History

Azar, Broder, Karlin and Upfal presented the theorem at STOC 1994 under the title "Balanced allocations", and the journal version appeared in SIAM Journal on Computing in 1999. Mitzenmacher's thesis of 1996 gave the queueing version. Vöcking showed in 2003 that asymmetric tie breaking improves the constant, and Berenbrink, Czumaj, Steger and Vöcking extended the bound to any number of balls in 2006. The textbook proof with $\beta_6 = n/(2e)$ follows Mitzenmacher and Upfal.

## References
