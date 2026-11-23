---
tag: B0BD8J
kind: definition
slug: local-differential-privacy
name: Local differential privacy
aliases:
- LDP
- local model of differential privacy
area: security-and-privacy/differential-privacy
level: core
summary: "Each user randomizes their own data before sending it, so that the output for any two inputs differs by at most a factor e^epsilon."
prereqs: [randomized-response, differential-privacy-definition]
see_also: [rappor, optimized-local-hashing, privacy-amplification-by-shuffling, geo-indistinguishability, approximate-differential-privacy, frequency-estimation, laplace-mechanism, sequential-composition-theorem]
sources:
  - paper: "Shiva Prasad Kasiviswanathan, Homin K. Lee, Kobbi Nissim, Sofya Raskhodnikova and Adam Smith, What can we learn privately?, SIAM Journal on Computing 40(3), 2011, pages 793 to 826"
    locator: the definitions of a local randomizer and of a local algorithm, and the equivalence of local learning with statistical query learning
  - paper: "John C. Duchi, Michael I. Jordan and Martin J. Wainwright, Minimax optimal procedures for locally private estimation, Journal of the American Statistical Association, 2018"
    locator: the minimax rates under local privacy, which show that the effective sample size drops from n to about n epsilon^2
  - paper: "Alexandre Evfimievski, Johannes Gehrke and Ramakrishnan Srikant, Limiting privacy breaches in privacy preserving data mining, ACM PODS 2003"
    locator: the amplification condition on a randomization operator, which is the e^epsilon bound on the ratio of report probabilities
  - paper: "Stanley L. Warner, Randomized response: a survey technique for eliminating evasive answer bias, Journal of the American Statistical Association 60(309), 1965, pages 63 to 69"
    locator: the randomized response survey design
---

Local differential privacy (LDP) is differential privacy without a trusted curator. Each user runs a randomized algorithm, a local randomizer, on their own data and sends only its output. The randomizer is $\varepsilon$-LDP if, for any two possible inputs of one user, the probability of each report changes by at most the factor $e^{\varepsilon}$. So the collector, or anyone who sees the reports, learns little about any one user's true value, even if the collector is not honest. The classic example is [randomized response](/randomized-response/). Google, Apple and Microsoft have used LDP to collect statistics from devices, with protocols such as [RAPPOR](/rappor/). The price is accuracy: for many tasks the error is of order $\sqrt n/\varepsilon$ for $n$ users, where the central model reaches $O(1/\varepsilon)$.

## Definition

Let $\mathcal X$ be the set of possible values of one user and $\mathcal Y$ a set of reports.

**Definition (local randomizer).** A randomized map $R : \mathcal X \to \mathcal Y$ is **$\varepsilon$-locally differentially private** if, for all $x, x' \in \mathcal X$ and every event $S \subseteq \mathcal Y$,

$$\Pr[R(x) \in S] \le e^{\varepsilon}\,\Pr[R(x') \in S].$$

It is **$(\varepsilon, \delta)$-LDP** if $\Pr[R(x) \in S] \le e^{\varepsilon}\Pr[R(x') \in S] + \delta$ for all $x, x'$ and $S$.

**Definition (local protocol).** In a non-interactive local protocol, user $i$ holds $x_i$, sends $y_i = R_i(x_i)$ with fresh randomness, and the analyst computes its result from $(y_1, \ldots, y_n)$ only. The protocol is $\varepsilon$-LDP if each $R_i$ is. In an interactive protocol, the randomizer that a user runs may depend on the earlier reports, and each randomizer must be $\varepsilon$-LDP given the past. When a user answers several times, the budgets add by [sequential composition](/sequential-composition-theorem/).

Three facts follow from the definition.

1. **Any two inputs.** The neighbor relation is not chosen by the analyst: every pair of values of one user must be protected. This is the replace relation applied to one user, with the data set of size 1.
2. **Central DP follows.** If each $R_i$ is $\varepsilon$-LDP, then the vector of reports is $\varepsilon$-[DP](/differential-privacy-definition/) in the central sense under replace: changing $x_i$ changes only the law of $y_i$. The converse fails; most central mechanisms are not local.
3. **Finite reports.** When $\mathcal Y$ is finite, $R$ is $\varepsilon$-LDP if and only if, for every report $y$, $\max_x \Pr[R(x) = y] \le e^{\varepsilon}\min_x \Pr[R(x) = y]$. So every report has positive probability under every input when $\varepsilon < \infty$.

## Examples and non-examples

**Randomized response.** For a bit $x$, report $x$ with probability $e^{\varepsilon}/(1 + e^{\varepsilon})$ and $1 - x$ otherwise. The ratio of the two probabilities of each report is exactly $e^{\varepsilon}$, so it is $\varepsilon$-LDP. With $\varepsilon = \ln 3$ the truth is reported with probability $3/4$. If $\hat q$ is the fraction of reports equal to 1, then $(\hat q - 1/4)/(1/2)$ is an unbiased estimate of the true fraction $\pi$. At $\pi = 1/2$ the standard deviation of the estimated count is $\sqrt n$, which is 1000 for $n = 10^6$ users. The central [Laplace mechanism](/laplace-mechanism/) with the same $\varepsilon$ adds a standard deviation of $\sqrt 2/\ln 3 = 1.287$ to the count.

**$k$-ary randomized response.** For a value in a set of size $k$, report the true value with probability $e^{\varepsilon}/(e^{\varepsilon} + k - 1)$ and each other value with probability $1/(e^{\varepsilon} + k - 1)$. With $k = 4$ and $\varepsilon = \ln 3$ the probabilities are $1/2$ and $1/6$, with the ratio 3. For large $k$ the true value is rarely sent, and hashing protocols such as [optimized local hashing](/optimized-local-hashing/) and RAPPOR do better for [frequency estimation](/frequency-estimation/).

**Laplace noise on a bounded value.** For $x \in [0, 1]$, the report $x + \mathrm{Lap}(1/\varepsilon)$ is $\varepsilon$-LDP, since any two inputs differ by at most 1. The average of $n$ reports estimates the mean, and the noise adds a standard deviation of $\sqrt{2/n}/\varepsilon$ to it.

**Non-example: noise added by the collector.** If users send true values and the collector adds Laplace noise to the total, the result is central DP but not LDP: the collector sees the raw data. LDP is a property of what leaves the user.

**Non-example: Laplace noise on an unbounded value.** For $x \in \mathbb R$ with no bound, $x + \mathrm{Lap}(b)$ is not $\varepsilon$-LDP for any $b$: the inputs 0 and $t$ give the density ratio $e^{t/b}$ at points beyond $t$, which grows without bound. The value must be clipped to a known range before the noise.

**Non-example: deterministic coding.** Sending a hash of the value, or the value with its last digits removed, is not $\varepsilon$-LDP for any finite $\varepsilon$: some report has probability 1 under one input and 0 under another. Such codings can be part of an LDP protocol only when noise follows them.

**Non-example: a rare leak.** The randomizer that sends $x$ with probability $\delta$ and a fixed symbol otherwise is $(0, \delta)$-LDP but not $\varepsilon$-LDP for any $\varepsilon$. Approximate LDP with a $\delta$ that is not tiny allows such leaks of single users.

## Related definitions

- [Differential privacy](/differential-privacy-definition/) in the central model trusts a curator with the raw data and adds noise to the result. LDP implies it under replace, with the same $\varepsilon$.
- [Privacy amplification by shuffling](/privacy-amplification-by-shuffling/) shows that if the local reports are sent through an anonymous shuffler, they are central DP with a much smaller $\varepsilon$. This shuffle model sits between the local and the central models.
- [Geo-indistinguishability](/geo-indistinguishability/) relaxes LDP for locations: the factor between two inputs is $e^{\varepsilon d}$, where $d$ is their distance.
- [Approximate DP](/approximate-differential-privacy/) gives the $(\varepsilon, \delta)$ version above.
- Kasiviswanathan, Lee, Nissim, Raskhodnikova and Smith (2011) defined local algorithms and showed that a concept class can be learned by a local algorithm exactly when it can be learned with statistical queries, up to polynomial factors. They also showed that some classes need interaction.
- Evfimievski, Gehrke and Srikant (2003) stated the same bound on report probabilities as an amplification condition for randomization operators in data mining, before the name LDP was used.
- Duchi, Jordan and Wainwright (2018) proved minimax rates for estimation under LDP, which show that for small $\varepsilon$ the effective number of samples drops from $n$ to about $n\varepsilon^2$.

## References
