---
tag: 6MXGD3
kind: problem
slug: secretary-problem
name: Secretary problem
aliases:
- marriage problem
- optimal stopping of candidates
- optimal stopping problem
- best choice problem
area: online-and-streaming/competitive-analysis
level: intro
summary: Choose the best of n candidates seen in random order, with only relative ranks and no recall. The optimal rule is a cutoff rule, and its success probability tends to 1/e.
prereqs: [random-permutation, online-algorithm, harmonic-series]
see_also: [one-over-e-stopping-rule, prophet-inequality, online-hiring-problem, hiring-problem, competitive-ratio, yao-minimax-principle, optional-stopping-theorem, matroid]
sources:
  - paper: doi:10.1214/ss/1177012493
    title: "Thomas S. Ferguson, Who solved the secretary problem?, Statistical Science 4(3) (1989), 282-296"
    locator: Section 2 (the classical problem, the optimal rule, the recursion for the optimal cutoff and the limit 1/e) and Sections 1 and 3 (history and variants)
  - paper: "E. B. Dynkin, The optimum choice of the instant for stopping a Markov process, Soviet Mathematics Doklady 4 (1963), 627-629"
    locator: the solution of the problem as an optimal stopping problem for the Markov chain of records
  - paper: doi:10.1080/01621459.1966.10502008
    title: "John P. Gilbert and Frederick Mosteller, Recognizing the maximum of a sequence, Journal of the American Statistical Association 61(313) (1966), 35-73"
    locator: Section 2 (the no-information problem and the optimal cutoffs) and the later sections on the full-information problem
  - paper: "Robert Kleinberg, A multiple-choice secretary algorithm with applications to online auctions, Proceedings of the 16th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2005, 630-631"
    locator: the k-choice secretary algorithm with ratio 1 - O(1/sqrt(k))
  - paper: "Moshe Babaioff, Nicole Immorlica and Robert Kleinberg, Matroids, secretary problems, and online mechanisms, Proceedings of the 18th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2007, 434-443"
    locator: the matroid secretary problem and its O(log r) algorithm
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Section 5.4.4 (the on-line hiring problem)
---

The secretary problem asks for a rule that picks the best of $n$ candidates who arrive in uniformly random order, when the rule sees only how each candidate ranks against the earlier ones, must accept or reject each candidate at once, and may accept only one. The optimal rule observes about $n/e$ candidates and then accepts the first one who beats all before; its probability of success tends to $1/e \approx 0.368$. It is the base example of optimal stopping and of [online algorithms](/online-algorithm/) in the random order model. The algorithm itself is on the page of the [1/e stopping rule](/one-over-e-stopping-rule/).

## In plain words

A manager must hire one secretary. The candidates come one at a time in a random order, and the manager knows how many will come. After each interview the manager knows only whether this person is better or worse than each earlier person. The manager must hire or send away each person before the next interview, and a person sent away does not come back.

The manager wins only by hiring the very best person of all. If the manager hires too early, a better person may still come. If the manager waits too long, the best person may already be gone. The best plan is to look at a little more than a third of the people without hiring, and then hire the first person who is better than everybody so far. This wins about 37 times in 100.

## Definition

Let the candidates have distinct values $v_1, \ldots, v_n$, and let $\pi$ be a uniformly random permutation of $\{1, \ldots, n\}$. Candidate $\pi(i)$ arrives at step $i$. The *relative rank* $R_i \in \{1, \ldots, i\}$ of step $i$ is $1$ plus the number of earlier candidates better than the candidate of step $i$. Step $i$ is a *record* if $R_i = 1$.

A *stopping rule* $\tau$ is a random time in $\{1, \ldots, n\} \cup \{\infty\}$ such that the event $\{\tau = i\}$ depends only on $R_1, \ldots, R_i$ and on random bits of the rule that are independent of $\pi$. The rule *succeeds* if $\tau < \infty$ and the candidate of step $\tau$ is the best of all $n$. The problem is to find

$$p_n = \max_{\tau} \Pr[\text{the rule } \tau \text{ succeeds}]$$

and a rule that attains it. The number $n$ is known in advance. The rule sees ranks, not values, and it cannot recall a rejected candidate.

This is a maximization problem with no [competitive ratio](/competitive-ratio/) in the usual sense: the guarantee is a probability of success over the random order. When the order is chosen by an adversary, no constant probability is possible (see Bounds).

## Variants

- **Cutoff rules.** The rule with cutoff $r$ rejects steps $1$ to $r$ and stops at the first record after step $r$. This is the [1/e stopping rule](/one-over-e-stopping-rule/) when $r = \lfloor n/e \rfloor$.
- **Full information.** The values are i.i.d. from a known continuous distribution and the rule sees them. The optimal rule uses a threshold that decreases with the number of candidates left, and its success probability tends to about $0.5802$ (Gilbert and Mosteller 1966).
- **Expected rank.** The goal is to minimize the expected rank of the chosen candidate, not to maximize the chance of the best. The optimal expected rank stays bounded as $n \to \infty$; Ferguson (1989) surveys this variant.
- **Several choices.** The rule may accept up to $k$ candidates and gains their total value. Kleinberg (2005) gives a rule that gains a $1 - O(1/\sqrt{k})$ fraction of the best possible total, in expectation over the random order. This is the secretary problem on a [uniform matroid](/uniform-matroid/).
- **Matroid secretary.** The accepted set must be independent in a [matroid](/matroid/). Babaioff, Immorlica and Kleinberg (2007) give an $O(\log \rho)$-competitive rule for a matroid of rank $\rho$ and ask whether a constant is possible.
- **Known distributions, expected value.** If the values are independent with known distributions and the goal is the expected value, the right benchmark is the expected maximum, and the [prophet inequality](/prophet-inequality/) gives one half of it.
- **Hiring without a limit.** A company that keeps hiring and wants both a high hiring rate and high quality is the different [online hiring problem](/online-hiring-problem/).

## Examples

**Three candidates.** Call the values 1, 2, 3, with 3 best. The cutoff rule with $r = 1$ rejects the first candidate and hires the first later one who beats it.

| order | hired | success |
|---|---|---|
| 1, 2, 3 | 2 | no |
| 1, 3, 2 | 3 | yes |
| 2, 1, 3 | 3 | yes |
| 2, 3, 1 | 3 | yes |
| 3, 1, 2 | none | no |
| 3, 2, 1 | none | no |

The rule succeeds on 3 of the 6 orders, so its success probability is $1/2$. The rule with $r = 0$ (hire the first) and the rule with $r = 2$ succeed with probability $1/3$. So $p_3 = 1/2$.

**Exact optima.** With $P_n(r)$ the success probability of the cutoff rule with cutoff $r$ (formula below), the optimal cutoff $r^*$ and the optimum $p_n$ are:

| $n$ | 3 | 4 | 5 | 6 | 8 | 10 | 20 | 100 | 1000 |
|---|---|---|---|---|---|---|---|---|---|
| $r^*$ | 1 | 1 | 2 | 2 | 3 | 3 | 7 | 37 | 368 |
| $p_n$ | 1/2 | 11/24 | 13/30 | 77/180 | 459/1120 | 3349/8400 | 0.38421 | 0.37104 | 0.36820 |

The values $p_n$ decrease toward $1/e = 0.36788$ in this table.

**A non-example.** If the manager may call back a rejected candidate, the problem is trivial: interview everyone and hire the best, which succeeds with probability 1. The [hiring problem](/hiring-problem/) of CLRS is different again: it hires each new best and counts the cost of the hires.

## Known algorithms

- [1/e stopping rule](/one-over-e-stopping-rule/): cutoff $\lfloor n/e \rfloor$, success probability $1/e + O(1/n)$, at most $n - 1$ comparisons and $O(1)$ space.
- The cutoff rule with the optimal cutoff $r^*$ below: success probability exactly $p_n$.
- A rule that stops at a uniformly random step: success probability $1/n$ on every order, also against an adversary.

## Bounds

The results below are proved on this page in full. Write $S(r) = \sum_{j=r+1}^{n-1} 1/j$ for $0 \le r \le n - 1$ (an empty sum is 0).

**Success probability of a cutoff rule.** For $1 \le r \le n - 1$,

$$P_n(r) = \frac{r}{n} \sum_{j=r+1}^{n} \frac{1}{j-1} = \frac{1 + r\,S(r)}{n},$$

and $P_n(0) = 1/n$, which the second form also gives. The proof is on the page of the [1/e stopping rule](/one-over-e-stopping-rule/): the rule succeeds exactly when the best is at a step $j > r$ and the best of the first $j - 1$ steps is among the first $r$, which has probability $\frac1n \cdot \frac{r}{j-1}$ for each $j$.

**Lemma 1 (independent ranks).** Under a uniformly random order, $R_1, \ldots, R_n$ are independent, and $R_i$ is uniform on $\{1, \ldots, i\}$.

*Proof.* The map from the permutation to $(R_1, \ldots, R_n)$ is one to one: the candidate of step $n$ is the one of rank $R_n$ among all $n$, the candidate of step $n - 1$ is the one of rank $R_{n-1}$ among the other $n - 1$, and so on. The set $\{1\} \times \{1, 2\} \times \cdots \times \{1, \ldots, n\}$ has $n!$ elements, as many as the permutations, so the map is a bijection. A uniform permutation therefore gives a uniform point of this product set, which is the claim. $\square$

**Lemma 2 (value of stopping).** If the rule stops at a step $i$ that is not a record, it fails. If it stops at a record $i$, it succeeds with probability $i/n$, whatever $R_1, \ldots, R_{i-1}$ are.

*Proof.* A step that is not a record has a better earlier candidate. Stopping at a record $i$ succeeds if and only if no later step is a record. By Lemma 1 this event is independent of $R_1, \ldots, R_i$ and has probability $\prod_{k=i+1}^{n} (1 - 1/k) = \prod_{k=i+1}^{n} \frac{k-1}{k} = \frac{i}{n}$. $\square$

**Theorem 1 (a cutoff rule is optimal).** There is an $r$ such that the cutoff rule with cutoff $r$ attains $p_n$. So $p_n = \max_{0 \le r \le n-1} P_n(r)$.

*Proof.* Let $u_i$ be the largest success probability that a rule can get from steps $i + 1, \ldots, n$, given that it has not stopped at steps $1$ to $i$. By Lemma 1, the future ranks $R_{i+1}, \ldots, R_n$ are independent of the past, and by Lemma 2 the value of each stop depends only on the step and on whether it is a record. So $u_i$ does not depend on the past ranks, and backward induction over the finite horizon gives

$$u_n = 0, \qquad u_{i-1} = \frac1i \max\left(\frac{i}{n},\, u_i\right) + \left(1 - \frac1i\right) u_i \quad (1 \le i \le n).$$

Here $1/i$ is the probability that step $i$ is a record. At a record the best choice is to stop if $i/n \ge u_i$ and to go on otherwise; at a step that is not a record, going on is never worse. A random choice between these options cannot beat the better option. So $p_n = u_0$, and an optimal rule stops at the first record $i$ with $i/n \ge u_i$. The recursion gives $u_{i-1} \ge u_i$, so $u_i$ does not increase with $i$, while $i/n$ increases. So the set of steps with $i/n \ge u_i$ is $\{r+1, \ldots, n\}$ for some $r$ (it holds $n$, since $u_n = 0$). The optimal rule is then the cutoff rule with this $r$. $\square$

**Theorem 2 (the optimal cutoff).** For $0 \le r \le n - 2$, $P_n(r+1) - P_n(r) = (S(r) - 1)/n$. So for $n \ge 3$ the optimal cutoff is $r^* = \min\{r \ge 1 : S(r) \le 1\}$, and $P_n$ increases strictly up to $r^*$ and does not increase after it.

*Proof.* Since $S(r) = S(r+1) + \frac{1}{r+1}$, we get $(r+1) S(r+1) - r S(r) = S(r+1) - \frac{r}{r+1} = S(r) - 1$. Divide by $n$ and use the form $P_n(r) = (1 + rS(r))/n$. The sums $S(r)$ decrease in $r$, so the sign of $P_n(r+1) - P_n(r)$ changes at most once, from positive to non-positive. For $n \ge 3$, $S(0) = H_{n-1} > 1$, so $r^* \ge 1$, and $S(n-2) = \frac{1}{n-1} \le 1$, so $r^*$ exists. $\square$

For example, at $n = 10$: $S(2) = \frac13 + \cdots + \frac19 = \frac{3349}{2520} > 1$ and $S(3) = \frac14 + \cdots + \frac19 = \frac{2509}{2520} \le 1$, so $r^* = 3$, as in the table. Then $P_{10}(3) = (1 + 3 \cdot \frac{2509}{2520})/10 = \frac{3349}{8400}$.

**Theorem 3 (the limit).** $P_n(\lfloor n/e \rfloor) \le p_n \le 1/e + 1/n$ for $n \ge 3$, and $p_n \to 1/e$.

*Proof.* For $1 \le r \le n - 1$ and $x = r/n$, comparing $\sum_{i=r}^{n-1} 1/i$ with $\int dt/t$ from above and below gives $-x \ln x \le P_n(r) \le 1/n - x\ln x$. Since $-x \ln x \le 1/e$ on $(0, 1)$, every cutoff rule gives at most $1/e + 1/n$, and so does every rule, by Theorem 1. For $r = \lfloor n/e \rfloor$, $x \to 1/e$, so the lower bound $-x \ln x$ tends to $1/e$. The [1/e stopping rule](/one-over-e-stopping-rule/) page gives each step. $\square$

**Adversarial order.** If an adversary chooses the order, no rule succeeds with probability more than $1/n$, and stopping at a uniformly random step gets exactly $1/n$.

*Proof.* The upper bound uses [Yao's principle](/yao-minimax-principle/). Let $k$ be uniform on $\{1, \ldots, n\}$, and let the order be increasing up to step $k$ and decreasing after it, so the best is at step $k$. Up to step $k$ each step is a record, and after it no step is a record. A deterministic rule that has not stopped has seen only records up to step $k$, so it stops at a fixed step $s$ (or never) if the records go on. It succeeds only if $k = s$, with probability at most $1/n$. A randomized rule is a mixture of deterministic rules, so it also succeeds with probability at most $1/n$ on this distribution, and so on some fixed order. The rule that stops at a uniform random step picks the best with probability $1/n$ on every order. $\blacksquare$

## Reductions

- **To the record process.** Lemma 1 turns the problem into a question about independent events: step $i$ is a record with probability $1/i$, independently of the rest. All the proofs above use only this. The same reduction gives the expected number of records $H_n$ in the [hiring problem](/hiring-problem/).
- **To a finite-horizon stopping problem.** The recursion for $u_i$ is the dynamic program of an optimal stopping problem. Dynkin (1963) treats it as the stopping of the Markov chain of records.
- **From the matroid and the $k$-choice versions.** With $k = 1$, or with a matroid of rank 1, these variants are the classic problem, so each of them is at least as hard.

## Applications

- **Online auctions.** A seller who receives bids in random order and must accept or reject each bid at once faces a secretary problem. Kleinberg (2005) uses the $k$-choice version to design auctions that are truthful for bidders in random order.
- **Search with final decisions.** Choosing a flat, a parking place or an offer when each option must be taken or left at once fits the model when the order is close to random and only the best counts.
- **Analysis of online algorithms.** The random order model of online algorithms, used for online matching and packing, starts from this problem: the input is adversarial, but its order is random.

## References
