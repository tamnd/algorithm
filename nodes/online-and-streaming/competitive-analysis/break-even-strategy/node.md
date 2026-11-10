---
tag: 04HWFP
kind: algorithm
slug: break-even-strategy
name: Break-even strategy
aliases:
- buy after break-even
area: online-and-streaming/competitive-analysis
level: intro
summary: Rent until the total rent equals the purchase price, then buy; it is 2-competitive for ski rental.
solves: [ski-rental-problem]
model: word-ram
complexity:
  vars: {n: the number of days}
  time: {worst: O(n)}
  space: {extra: O(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1986
  people: [Anna R. Karlin, Mark S. Manasse, Larry Rudolph, Daniel D. Sleator]
  note: Karlin, Manasse, Rudolph and Sleator used the rent-or-buy argument for snoopy caching in their FOCS 1986 paper, published in Algorithmica in 1988, and called algorithms with this kind of guarantee competitive.
prereqs: [ski-rental-problem]
see_also: [take-the-stairs-strategy, bahncard-problem, competitive-ratio, randomized-online-algorithm, tcp-acknowledgment-problem, doubling-trick]
sources:
  - paper: doi:10.1007/BF01762111
    title: "Anna R. Karlin, Mark S. Manasse, Larry Rudolph and Daniel D. Sleator, Competitive snoopy caching, Algorithmica 3(1) (1988), 79-119"
    locator: the rent-or-buy strategy that pays at most twice the optimum
  - paper: doi:10.1007/BF01189993
    title: "Anna R. Karlin, Mark S. Manasse, Lyle A. McGeoch and Susan Owicki, Competitive randomized algorithms for nonuniform problems, Algorithmica 11(6) (1994), 542-571"
    locator: the deterministic rent-or-buy strategy as the baseline for the randomized e/(e-1) algorithm
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: the rent-or-buy (ski rental) example of competitive analysis
---

The break-even strategy solves the [ski rental problem](/ski-rental-problem/) online: rent as long as the rent paid so far, plus one more rent, stays below the purchase price, and buy on the first day where it would reach the price. With rent 1 per day and price $B$, it rents on days 1 to $B - 1$ and buys on day $B$, and it pays at most $2 - 1/B$ times the offline optimum on every season. No deterministic online rule does better.

## In plain words

You pay a small fee each day, or a big fee once. You do not know how many days you will need the thing. The break-even rule says: keep paying the small fee until the small fees would add up to the big fee, and then pay the big fee.

If the need ends early, you paid only small fees, which was the best choice. If the need lasts, you paid about the big fee twice: once in small fees and once for real. A person who knew the future would have paid the big fee at least once in that case. So you never pay more than about twice the best possible amount, whatever happens.

## The problem

Each day the player needs one unit of a resource. If it does not own the resource, it rents it for $r > 0$ or buys it for $p > 0$; after a purchase every later day is free. The number $n$ of days is not known in advance. The offline optimum is $\mathrm{OPT}(n) = \min(n r, p)$. The standard form is $r = 1$ and $p = B$.

**Notation.** $\sigma$ is the request sequence (here, $n$ days), $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, and $c$ is the competitive ratio.

## The algorithm

```pseudo id=main
BREAK-EVEN(r, p)                       ▷ rent r per day, buy price p
L1  paid ← 0, owned ← false
L2  for each new day d = 1, 2, … do
L3      if owned then use the resource at no cost
L4      else if paid + r ≥ p then buy for p, owned ← true
L5      else rent for r, paid ← paid + r
```

On day $d$ before a purchase, $\mathrm{paid} = (d - 1) r$. So line L4 buys on the first day $d$ with $d r \ge p$, which is day $m = \lceil p/r \rceil$. With $r = 1$ and $p = B$, it buys on day $B$.

## Example

Take $r = 1$ and $B = 10$.

| season length $n$ | actions | $\mathrm{ALG}(n)$ | $\mathrm{OPT}(n)$ | ratio |
|---|---|---|---|---|
| 3 | rent, rent, rent | 3 | 3 | 1 |
| 9 | rent on days 1 to 9 | 9 | 9 | 1 |
| 10 | rent on days 1 to 9, buy on day 10 | 19 | 10 | 1.9 |
| 100 | the same, then 90 free days | 19 | 10 | 1.9 |

The worst season ends on the purchase day. For $B = 4$, the exact worst ratio of "buy on day $j$" is $4, 5/2, 2, 7/4, 2, 9/4, 5/2$ for $j = 1, \ldots, 7$. The minimum $7/4 = 2 - 1/4$ is at $j = B = 4$.

## Correctness

Let $m = \lceil p/r \rceil$. If $n < m$, the rule rents every day and pays $n r$; since $n r < p$, this is $\mathrm{OPT}(n)$. If $n \ge m$, it pays $(m - 1) r + p$, and $\mathrm{OPT}(n) = p$ because $n r \ge m r \ge p$. So

$$\mathrm{ALG}(n) \le \left(1 + \frac{(m - 1) r}{p}\right) \mathrm{OPT}(n) < 2 \cdot \mathrm{OPT}(n),$$

with equality in the first step for $n = m$. When $p/r$ is an integer, the factor is $2 - r/p$, which is $2 - 1/B$ for $r = 1$, $p = B$. The guarantee is strict: there is no additive constant. The lower bound, that every deterministic rule has ratio at least $2 - 1/B$, is on the [ski rental](/ski-rental-problem/) page. The full proof, with the lines of the pseudocode, is below.

## Complexity

The rule does $O(1)$ work per day: one comparison and one addition. A season of $n$ days takes $O(n)$ time in total. It stores two values, $\mathrm{paid}$ and $\mathrm{owned}$, so the extra space is $O(1)$.

## Properties

- **Online and deterministic.** The decision on day $d$ depends only on $d$ and the two prices.
- **Strictly competitive.** The ratio $1 + (\lceil p/r \rceil - 1) r / p$ holds with additive constant 0, and it is always below 2.
- **Optimal among deterministic rules.** Any other buy day has a larger worst ratio, so the rule is the unique optimal deterministic rule for $B \ge 2$.
- **Not optimal against an oblivious adversary.** A random buy day lowers the expected ratio to $1/(1 - (1 - 1/B)^B) < e/(e-1) \approx 1.582$. See [randomized online algorithm](/randomized-online-algorithm/).

## Variants and improvements

- **Buy after the rent equals the price.** The rule "rent for $B$ days, buy on day $B + 1$" also has ratio at most 2: it pays $2B$ against $\mathrm{OPT} = B$ on $B + 1$ days. It is the reading in the summary of this page. Buying on day $B$ is better by $1/B$.
- **Randomized break-even (Karlin, Manasse, McGeoch and Owicki 1994).** Buy on day $j \le B$ with probability proportional to $(1 - 1/B)^{B - j}$. Its expected cost is exactly $c_B \cdot \mathrm{OPT}(n)$ for every $n$, with $c_B = 1/(1 - (1 - 1/B)^B)$; for $B = 4$, $c_4 = 256/175$.
- **Continuous time.** For waiting problems, such as spin or block, wait until the cost of waiting equals the cost of the switch, then switch. The ratio is 2. The [take-the-stairs strategy](/take-the-stairs-strategy/) is this rule for an elevator, where it gives $2 - E/S$.
- **Discount cards.** In the [Bahncard problem](/bahncard-problem/), the rule SUM buys a card when the regular cost of the recent trips reaches the break-even point $C/(1 - \beta)$.
- **TCP acknowledgment.** Send the acknowledgments when the total delay cost of the waiting packets equals the cost of one acknowledgment. See the [TCP acknowledgment problem](/tcp-acknowledgment-problem/).
- **With predictions.** Trust a prediction of the season length to buy earlier or later, while the worst case stays bounded. See [learning-augmented algorithms](/learning-augmented-algorithms/).

## When to use it

Use the break-even rule for a single rent-or-buy decision when nothing is known about the length of the need and a guarantee is required on every input: power-down of idle devices, spin or block in locks, keep or drop a cached copy. If a good distribution of the lengths is known, choose the buy day that minimizes the expected cost under it instead. If the decision repeats many times and the adversary does not see the coins, the randomized rule gives a better expected ratio.

## Pitfalls

- **Off by one.** "Rent until the rent equals the price" can mean buy on day $B$ or on day $B + 1$. The first gives $2 - 1/B$, the second gives 2.
- **Non-integer prices.** With rent $r$ and price $p$, the buy day is $\lceil p/r \rceil$, and the ratio is $1 + (\lceil p/r \rceil - 1) r/p$, not $2 - r/p$.
- **The additive constant.** Since $\mathrm{OPT} \le p$, a ratio with an additive constant $b \ge p$ says nothing. The guarantee of the rule is strict.
- **Buying is final.** The analysis assumes that buying ends all costs. If owning has a running cost, or the item expires, the problem is different, for example the Bahncard problem.

## Implementations

## History

The rent-or-buy argument appears in the work of Karlin, Manasse, Rudolph and Sleator on snoopy caching (FOCS 1986, Algorithmica 1988), where a cache keeps updating a shared block until the update cost equals the cost of dropping and fetching it again. The same paper introduced the term competitive for such guarantees. Karlin, Manasse, McGeoch and Owicki (1994) gave the randomized version with ratio tending to $e/(e-1)$.

## References
