---
tag: TQ55V4
kind: problem
slug: online-hiring-problem
name: Online hiring problem
aliases:
- hiring problem of Broder et al.
- Lake Wobegon hiring
area: online-and-streaming/competitive-analysis
level: core
summary: A company interviews a stream of candidates with random scores and hires without a fixed limit, trading the speed of hiring against the quality of the staff.
prereqs: [uniform-distribution, expected-value, median]
see_also: [secretary-problem, one-over-e-stopping-rule, hiring-problem, hire-assistant, prophet-inequality, online-algorithm, harmonic-series, geometric-distribution]
sources:
  - paper: doi:10.1137/07070629X
    title: "Andrei Z. Broder, Adam Kirsch, Ravi Kumar, Michael Mitzenmacher, Eli Upfal and Sergei Vassilvitskii, The hiring problem and Lake Wobegon strategies, SIAM Journal on Computing 39(4) (2009), 1233-1255"
    locator: Section 2 (the model and the threshold and maximum strategies), Section 3 (hiring above the mean, Propositions 3.2 and 3.3), Section 4 (hiring above the median, Propositions 4.2 and 4.3); first in SODA 2008, 1184-1193
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Section 5.4.4, which uses the name on-line hiring problem for the one-hire secretary problem
---

The online hiring problem of Broder, Kirsch, Kumar, Mitzenmacher, Upfal and Vassilvitskii (2008) models a company that grows by interviewing a stream of candidates and deciding at once whether to hire each one, with no limit on the number of hires. The company wants two things that pull against each other: to hire quickly, and to make the quality of its staff high. Hiring a candidate who is better than the mean, or than the median, of the current staff are the two main rules, and they give exact tradeoffs between the number of interviews and the quality gap. This problem is not the [secretary problem](/secretary-problem/), where exactly one candidate is hired and the goal is to pick the best.

## In plain words

A new company wants to grow, and candidates come to interviews one at a time. Each candidate gets a score, and the company must hire or reject the candidate at the end of the interview. The company can hire as many people as it likes.

If it hires everyone, it grows fast but its staff stays average. If it hires only people better than everyone already there, the staff becomes very good, but hires soon become so rare that the company stops growing. Good rules sit between these two. One rule hires a candidate who is better than the average of the current staff. Another hires a candidate who is better than the middle person of the current staff. The second rule makes the staff better, and the first makes the company grow faster.

## Definition

Candidates arrive one at a time with scores $Q_1, Q_2, \ldots$, independent and uniform on $[0, 1]$. The company starts with one employee of score $q < 1$, and we write $g = 1 - q$. At each interview the company sees the score and decides at once to hire or to reject; a rejected candidate does not return. A *strategy* is such a rule. It may use the scores of the current staff, but not future scores.

For a strategy and for $n \ge 1$, measure:

- $T_n$, the number of interviews until the staff has grown by $n$ hires;
- $G_n = 1 - (\text{mean score of the staff})$, the *gap* of the mean after $n$ hires, or the gap of the median for median rules.

A good strategy keeps $\mathbb{E}[T_n]$ small, so that the company grows fast, and makes $\mathbb{E}[G_n]$ tend to $0$ quickly, so that the quality rises. There is no single objective: the problem asks for the tradeoff between the two.

## Variants

- **Other score distributions.** The exact formulas on this page use uniform scores. Other distributions change the rates, because the chance to beat the bar depends on the tail of the distribution near the top.
- **Quantile rules.** A rule can hire above any fixed quantile of the current staff. The median is one case, and the maximum is the extreme case.
- **The one-hire version.** If only one person may be hired and the goal is the best of a known number $n$ of candidates, the problem becomes the [secretary problem](/secretary-problem/). CLRS (Section 5.4.4) calls that version the "on-line hiring problem"; the name of this page follows Broder et al. The CLRS [hiring problem](/hiring-problem/) and its [HIRE-ASSISTANT](/hire-assistant/) procedure count the cost of hiring each new best candidate, which is a third problem.

## Examples

Let $g = 1/2$, so the first employee has score $1/2$, and stop after 100 hires.

| strategy | hire rule | gap after 100 hires | expected interviews |
|---|---|---|---|
| hire everyone | always | mean gap tends to $1/2$ | $100$ |
| fixed threshold $t$ | $Q \ge t$ | mean gap tends to $(1 - t)/2$ | $100/(1 - t)$ |
| above the mean | $Q \ge$ mean of staff | $\mathbb{E}[G_{100}] \approx 0.0561$ | about $1290$ |
| above the median | $Q \ge$ median of staff | $\mathbb{E}[G'_{50}] = 1/52 \approx 0.0192$ | $5100$ |
| above the maximum | $Q \ge$ best of staff | $\mathbb{E}[G_n] = g/2^n$ | infinite |

The number for the mean rule comes from a seeded simulation of 4000 runs; the others are exact. The median rule here hires in pairs, as defined below, so 100 hires are 50 rounds.

A fixed threshold hires at a constant rate but never raises the quality above $(1 + t)/2$. The maximum rule gives a gap that halves with each hire, but the waiting time for the next hire has infinite expectation, so the company stalls.

## Known algorithms

- **Hire above a threshold $t$.** Hire rate $1 - t$, and the mean score tends to $(1 + t)/2$.
- **Hire above the maximum.** The best score has gap $g/2^n$ in expectation after $n$ hires. After the first hire this gap $U$ is uniform on $[0, g]$, and the wait for the second hire has expectation $\mathbb{E}[1/U] = \infty$.
- **Hire above the mean (Lake Wobegon strategy).** $\mathbb{E}[G_n] = \Theta(1/\sqrt{n})$ and $\mathbb{E}[T_n] = \Theta(n^{3/2})$ (Propositions 3.2 and 3.3 of Broder et al.).
- **Hire above the median.** After $k$ rounds of two hires, $\mathbb{E}[G'_k] = 2g/(k + 2) = \Theta(1/k)$ and $\mathbb{E}[T'_k] = k(k+1)/g = \Theta(k^2)$ (Propositions 4.2 and 4.3).

The name "Lake Wobegon strategy" refers to a fictional town where all the children are above average: each new hire is above the current average of the company.

## Bounds

**Theorem 1 (the mean rule).** Under the mean rule, $\mathbb{E}[G_n] = g \prod_{j=1}^{n} \left(1 - \frac{1}{2(j+1)}\right) = \Theta(1/\sqrt{n})$.

*Proof.* After $j - 1$ hires the staff has $j$ people with mean gap $G_{j-1}$. The next hire has a score uniform on $[1 - G_{j-1}, 1]$, so its own gap $U$ is uniform on $[0, G_{j-1}]$ and $\mathbb{E}[U \mid G_{j-1}] = G_{j-1}/2$. The new mean gap is $G_j = (j G_{j-1} + U)/(j + 1)$, so

$$\mathbb{E}[G_j \mid G_{j-1}] = G_{j-1}\,\frac{j + 1/2}{j + 1} = G_{j-1}\left(1 - \frac{1}{2(j+1)}\right).$$

Take expectations and multiply over $j = 1, \ldots, n$, with $G_0 = g$. For the order of growth, $\ln(1 - x) = -x + O(x^2)$ gives $\ln \prod_j (1 - \frac{1}{2(j+1)}) = -\frac12 \sum_{j=1}^{n} \frac{1}{j+1} + O(1) = -\frac12 \ln n + O(1)$, by the [harmonic series](/harmonic-series/). So the product is $\Theta(n^{-1/2})$. $\square$

**Theorem 2 (the median rule).** Let the staff have $2k + 1$ people after round $k$, with median gap $G'_k$, and let each round hire the next two candidates with a score at least the current median. Then $\mathbb{E}[G'_k] = \frac{2g}{k+2}$ and $\mathbb{E}[T'_k] = \frac{k(k+1)}{g}$.

*Proof.* Claim: after round $k$, given the median $m$, the $k$ scores above the median are independent and uniform on $[m, 1]$. For $k = 0$ there are none. Suppose the claim holds after round $j - 1$, with median $m$ and gap $G' = 1 - m$. Round $j$ adds two scores, each uniform on $[m, 1]$ and independent. The staff now has $2j + 1$ people, and $j + 1$ of them lie above the old median, all i.i.d. uniform on $[m, 1]$. The new median is the smallest of these $j + 1$ scores. Given that minimum, the other $j$ scores are i.i.d. uniform above it, which proves the claim.

The new gap is $G' \cdot X$, where $X$ is the largest of $j + 1$ independent uniform $[0, 1]$ values, with density $(j+1)x^j$, independent of the past. So $\mathbb{E}[X] = \frac{j+1}{j+2}$ and $\mathbb{E}[1/X] = \frac{j+1}{j}$. Multiplying, $\mathbb{E}[G'_k] = g \prod_{j=1}^{k} \frac{j+1}{j+2} = \frac{2g}{k+2}$ and $\mathbb{E}[1/G'_{k}] = \frac1g \prod_{j=1}^{k} \frac{j+1}{j} = \frac{k+1}{g}$.

During round $j$ the median is fixed, so each interview hires with probability $G'_{j-1}$, and the two hires take $2/G'_{j-1}$ interviews in expectation, as a sum of two [geometric](/geometric-distribution/) waits. So $\mathbb{E}[T'_k] = \sum_{j=1}^{k} 2\,\mathbb{E}[1/G'_{j-1}] = \sum_{j=1}^{k} \frac{2j}{g} = \frac{k(k+1)}{g}$. $\square$

**The tradeoff.** Each hire under a rule with gap $G$ costs about $1/G$ interviews, so a gap that falls like $1/n^{\beta}$ forces about $n^{1 + \beta}$ interviews for $n$ hires. The mean rule ($\beta = 1/2$) and the median rule ($\beta = 1$) sit on this curve. Broder et al. also show that both processes have weak concentration, linked to the lognormal distribution, so single runs can differ much from the mean.

## Reductions

- **To products of independent factors.** Both proofs reduce the gap to a product of independent random factors, one per hire or round. The logarithm of the gap is then a sum of independent terms, which explains the lognormal behavior.
- **From the secretary problem.** With a budget of one hire and a known horizon, the problem is the [secretary problem](/secretary-problem/), solved by the [1/e stopping rule](/one-over-e-stopping-rule/).

## Applications

- **Growth of selective groups.** The model describes companies, clubs or committees that grow by adding members who must pass a bar set by the current members. It explains why "hire only above the average" improves quality steadily but slowly, and why stricter bars slow growth sharply.
- **Selection in data streams.** Keeping a growing set of high-quality items from a stream, such as documents for an index or answers for a search result, with a bar that depends on the items kept so far, has the same tradeoff.

## References
