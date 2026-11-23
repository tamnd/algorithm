---
tag: 6Z9Z2W
kind: theorem
slug: privacy-amplification-by-shuffling
name: Privacy amplification by shuffling
aliases:
- shuffle model amplification
area: security-and-privacy/differential-privacy
level: research
summary: "Shuffling the reports of n users with epsilon_0-LDP randomizers gives central (epsilon, delta)-DP with epsilon = O(sqrt(e^epsilon_0 log(1/delta)/n)), for epsilon_0 up to about ln(n/log(1/delta))."
history:
  year: 2019
  people: [Úlfar Erlingsson, Vitaly Feldman, Ilya Mironov, Ananth Raghunathan, Kunal Talwar, Abhradeep Thakurta]
  note: "Erlingsson et al. proved amplification by shuffling at SODA 2019, for small epsilon_0. Balle, Bell, Gascón and Nissim (CRYPTO 2019) extended the range of epsilon_0, and Feldman, McMillan and Talwar (FOCS 2021) gave the clone analysis with the bound stated here."
prereqs: [local-differential-privacy, approximate-differential-privacy]
see_also: [privacy-amplification-by-subsampling, randomized-response, rappor, post-processing-theorem, advanced-composition-theorem, renyi-differential-privacy, numerical-privacy-accounting, differential-privacy-definition]
sources:
  - url: "https://arxiv.org/abs/2012.12803"
    title: "Vitaly Feldman, Audra McMillan and Kunal Talwar, Hiding among the clones: a simple and nearly optimal analysis of privacy amplification by shuffling, IEEE FOCS 2021, pages 954 to 964"
    locator: "Theorem 3.1 (the bound and the condition on epsilon_0) and its proof in Section 3 (the decomposition of each report into clones of the two inputs of the first user)"
  - paper: "Úlfar Erlingsson, Vitaly Feldman, Ilya Mironov, Ananth Raghunathan, Kunal Talwar and Abhradeep Thakurta, Amplification by shuffling: from local to central differential privacy via anonymity, ACM-SIAM SODA 2019, pages 2468 to 2479"
    locator: the first amplification theorem for shuffled local reports, for small epsilon_0
  - paper: "Borja Balle, James Bell, Adrià Gascón and Kobbi Nissim, The privacy blanket of the shuffle model, CRYPTO 2019, LNCS 11693, pages 638 to 667"
    locator: the privacy blanket decomposition and the amplification bound for larger epsilon_0
  - paper: "Albert Cheu, Adam Smith, Jonathan Ullman, David Zeber and Maxim Zhilyaev, Distributed differential privacy via shuffling, EUROCRYPT 2019, LNCS 11476, pages 375 to 403"
    locator: the definition of the shuffle model and its protocols for counting and summation
  - paper: "Vitaly Feldman, Audra McMillan and Kunal Talwar, Stronger privacy amplification by shuffling for Renyi and approximate differential privacy, ACM-SIAM SODA 2023, pages 4966 to 4981"
    locator: the sharper bounds and the Renyi version of the clone analysis
---

Privacy amplification by shuffling says that local reports become much more private when they are sent through a shuffler, which removes the senders and outputs the reports in a uniformly random order. If each of $n$ users sends a report from an $\varepsilon_0$-[locally private](/local-differential-privacy/) randomizer, the shuffled reports are $(\varepsilon, \delta)$-differentially private in the central sense with $\varepsilon$ of order $\sqrt{e^{\varepsilon_0}\log(1/\delta)/n}$. For $\varepsilon_0 \le 1$ this is of order $\varepsilon_0\sqrt{\log(1/\delta)/n}$. So users can add little noise locally, with a weak local guarantee, and still get a strong central guarantee, as long as nobody can link the reports to the users. Erlingsson et al. proved the first version in 2019. The bound below is that of Feldman, McMillan and Talwar (2021), who show that each report hides the report of any one user among many "clones". The theorem is the basis of the shuffle model, which sits between the local and the central models of [differential privacy](/differential-privacy-definition/).

## Statement

There are $n$ users with data $x_1, \ldots, x_n$ in a domain $\mathcal X$. The neighbor relation is replace: two data sets differ in the value of one user, and $n$ is public. User $i$ runs a randomizer $R^{(i)}$ that may depend on the earlier reports $y_1, \ldots, y_{i-1}$, and that is $\varepsilon_0$-LDP for each fixed value of them. The shuffled mechanism $\mathcal A_s$ draws a uniformly random permutation $\pi$ of the users, runs the randomizers in the order $\pi(1), \ldots, \pi(n)$, and outputs the reports in that order, so the observer does not learn which user sent which report.

**Theorem (Feldman, McMillan and Talwar, Theorem 3.1).** Let $\delta \in [0, 1]$ and

$$\varepsilon_0 \le \ln\left(\frac{n}{16\ln(2/\delta)}\right).$$

Then $\mathcal A_s$ is $(\varepsilon, \delta)$-DP under replace, with

$$\varepsilon \le \ln\left(1 + \frac{e^{\varepsilon_0} - 1}{e^{\varepsilon_0} + 1}\left(\frac{8\sqrt{e^{\varepsilon_0}\ln(4/\delta)}}{\sqrt n} + \frac{8e^{\varepsilon_0}}{n}\right)\right).$$

As a consequence, $\varepsilon = O\big((1 - e^{-\varepsilon_0})\sqrt{e^{\varepsilon_0}\ln(1/\delta)/n}\big)$. For $\varepsilon_0 > 1$ this is $O(\sqrt{e^{\varepsilon_0}\ln(1/\delta)/n})$, and for $\varepsilon_0 \le 1$ it is $O(\varepsilon_0\sqrt{\ln(1/\delta)/n})$.

The most common case has the same randomizer $R$ for all users and no dependence on the earlier reports. Then the output is the multiset of the reports $R(x_1), \ldots, R(x_n)$.

## In plain words

Each user adds some noise to their own answer, enough for a weak protection on its own. Then all answers go through a mixer that throws away the names and the order.

An observer who wants to learn your value now sees a pile of answers and does not know which one is yours. Because of the noise, every other answer has some chance of looking exactly like an answer you could have given. With many users, there are many such look-alikes, and they hide your answer.

The protection gets stronger as the number of users grows, roughly with its square root.

## Proof

This is a marked sketch. The full proof is the proof of Theorem 3.1 in Section 3 of Feldman, McMillan and Talwar (FOCS 2021, arXiv 2012.12803). Steps 1 and 2 below are complete for non-adaptive randomizers; step 3 only outlines the computation of the constants.

**Step 1 (clones).** Fix the two values $x_1^0$ and $x_1^1$ of the user who changes, and write $P_0 = R(x_1^0)$ and $P_1 = R(x_1^1)$ for one randomizer $R$. For every input $x$ and every report $y$, the LDP condition gives $R(x)(y) \ge e^{-\varepsilon_0}P_b(y)$ for $b = 0, 1$, so

$$R(x) = \frac{e^{-\varepsilon_0}}{2}P_0 + \frac{e^{-\varepsilon_0}}{2}P_1 + (1 - e^{-\varepsilon_0})\,L(x)$$

for a probability distribution $L(x)$, which is the remaining mass, divided by $1 - e^{-\varepsilon_0}$. So each other user can be simulated as follows: with probability $p = e^{-\varepsilon_0}$ it is a clone and sends a draw from $P_0$ or $P_1$ with equal chance, and otherwise it sends a draw from $L(x)$.

**Step 2 (a reduction to two counts).** After the shuffle, the output is a multiset of reports. Let $U$ be the number of reports drawn from $P_0$ and $V$ the number drawn from $P_1$, counting user 1 and the clones. Given $(U, V)$, the multiset can be generated without knowing $x_1$: draw $U$ reports from $P_0$, $V$ from $P_1$, one from each $L(x_i)$ of the users who are not clones, and shuffle. So the shuffled output is a post-processing of $(U, V)$, and by the [post-processing theorem](/post-processing-theorem/) it suffices to bound the privacy of $(U, V)$. Let $C \sim \mathrm{Bin}(n - 1, p)$ be the number of clones and $A \mid C \sim \mathrm{Bin}(C, 1/2)$. Then $(U, V) = (A + 1, C - A)$ when $x_1 = x_1^0$, and $(U, V) = (A, C - A + 1)$ when $x_1 = x_1^1$. For $u + v = c + 1$,

$$\frac{\Pr[(U, V) = (u, v) \mid x_1^0]}{\Pr[(U, V) = (u, v) \mid x_1^1]} = \frac{\binom{c}{u - 1}}{\binom{c}{u}} = \frac{u}{v}.$$

So the privacy loss of the pair is exactly $\ln(U/V)$.

**Step 3 (concentration).** $C$ is close to $(n - 1)e^{-\varepsilon_0}$ and $U, V$ are each close to $C/2$, within $O(\sqrt{C\ln(1/\delta)})$ except with probability $\delta$. Then $\ln(U/V) = O(\sqrt{\ln(1/\delta)/C}) = O(\sqrt{e^{\varepsilon_0}\ln(1/\delta)/n})$. The condition on $\varepsilon_0$ makes $C$ large enough for these tail bounds. Feldman, McMillan and Talwar carry out this step with Chernoff and Hoeffding bounds. They obtain the factor $(e^{\varepsilon_0} - 1)/(e^{\varepsilon_0} + 1)$ by also splitting the report of user 1: with $Q_0 = (e^{\varepsilon_0}P_0 - P_1)/(e^{\varepsilon_0} - 1)$ and $Q_1 = (e^{\varepsilon_0}P_1 - P_0)/(e^{\varepsilon_0} - 1)$, which are distributions by the LDP condition, $P_0 = (e^{\varepsilon_0}Q_0 + Q_1)/(e^{\varepsilon_0} + 1)$ and $P_1 = (Q_0 + e^{\varepsilon_0}Q_1)/(e^{\varepsilon_0} + 1)$, and $Q_0 + Q_1 = P_0 + P_1$, so the clones can be taken as clones of $Q_0$ and $Q_1$. They also handle adaptive randomizers, where the decomposition of step 1 is applied to each randomizer given the earlier reports. $\blacksquare$

## Consequences

**The numbers.** For $\delta = 10^{-6}$, the bound of the theorem gives these values. The condition column is $\ln(n/(16\ln(2/\delta)))$, the largest $\varepsilon_0$ that the theorem allows.

| $n$ | $\varepsilon_0$ | condition | $\varepsilon$ |
|---|---|---|---|
| 1000 | 1 | 1.4604 | 0.5662 |
| $10^4$ | 1 | 3.7630 | 0.2140 |
| $10^4$ | 2 | 3.7630 | 0.5009 |
| $10^5$ | 1 | 6.0656 | 0.0726 |
| $10^5$ | 4 | 6.0656 | 0.5346 |
| $10^6$ | 1 | 8.3682 | 0.0235 |

With $10^5$ users, local reports with the weak guarantee $\varepsilon_0 = 4$ become central reports with $\varepsilon \approx 0.53$.

- **Frequency estimation.** Local protocols such as [randomized response](/randomized-response/) and [RAPPOR](/rappor/) can run with a larger $\varepsilon_0$, and so with less noise, when a shuffler is in place. The error of a count then gets close to that of the central model.
- **Many rounds.** When users report many times, each round is amplified, and the rounds compose. The Renyi version of the clone analysis (Feldman, McMillan and Talwar, SODA 2023) fits [Renyi DP](/renyi-differential-privacy/) accounting.
- **Trust.** The guarantee holds only against an observer who sees the shuffled output. The shuffler, or anyone who can link reports to users, still sees $\varepsilon_0$-LDP reports. In practice the shuffler is built with trusted hardware, mixnets or cryptographic protocols.
- **Compared with subsampling.** [Amplification by subsampling](/privacy-amplification-by-subsampling/) hides whether a user took part. Shuffling hides which report belongs to the user. Both need the hidden randomness to stay hidden.

## Tightness

The theorem is an upper bound with explicit constants, and it is not exact. For binary randomized response with $\varepsilon_0 = 1$, $n = 10^4$ and $\delta = 10^{-6}$, these are measurements made for this page:

- the closed form above gives $\varepsilon = 0.2140$;
- the exact privacy of the two counts $(U, V)$ of step 2, computed numerically, gives $0.1214$;
- the refined pair of step 3, where the report of user 1 is also split into $Q_0$ and $Q_1$, gives $0.0530$ when computed numerically;
- the exact privacy of shuffled randomized response itself, where the output is the number of ones, gives $0.0357$ when all other users hold 0, and $0.0352$ when half of them hold 1.

So the closed form is about six times the true value here, and the numerical value of the refined clone bound is within a factor of 1.5 of it. The gap comes from the tail bounds of step 3 and from the users who are not clones, whose reports add more noise that the analysis ignores. For this reason Feldman, McMillan and Talwar also give a numerical procedure for the clone bound, and accountants for the shuffle model compute it numerically.

Some condition on $\varepsilon_0$ is needed. If $\varepsilon_0$ is so large that the expected number of clones $(n - 1)e^{-\varepsilon_0}$ is below 1, then often no other report looks like a report of $x_1^0$, and the report of user 1 is visible in the shuffled output.

## History

Bittau et al. (SOSP 2017) built the Prochlo system, which encodes, shuffles and then analyzes user reports, and noted that the shuffle improves privacy. Erlingsson, Feldman, Mironov, Raghunathan, Talwar and Thakurta (SODA 2019) proved the first amplification theorem, for $\varepsilon_0$ below a constant. In the same year, Cheu, Smith, Ullman, Zeber and Zhilyaev (EUROCRYPT 2019) defined the shuffle model as a model of computation and gave protocols for counting and summation, and Balle, Bell, Gascón and Nissim (CRYPTO 2019) introduced the privacy blanket, a decomposition of each report into a part that does not depend on the input, which allowed larger $\varepsilon_0$. Feldman, McMillan and Talwar (FOCS 2021) gave the clone analysis, with the bound above for all $\varepsilon_0$ up to about $\ln n$, and sharpened it with a Renyi version at SODA 2023.

## References
