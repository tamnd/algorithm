---
tag: E37PHH
kind: theorem
slug: fingerprinting-codes-lower-bound
name: Fingerprinting code lower bound
aliases:
- Bun-Ullman-Vadhan lower bound
area: security-and-privacy/differential-privacy
level: research
summary: "Fingerprinting codes show that answering d attribute means with (epsilon, delta)-DP and error below 1/2 needs about sqrt(d) rows, which the Gaussian mechanism nearly matches."
history:
  year: 2014
  people: [Mark Bun, Jonathan Ullman, Salil Vadhan]
  note: Bun, Ullman and Vadhan turned fingerprinting codes into lower bounds for approximate differential privacy at STOC 2014. Steinke and Ullman later made the bound for attribute means nearly tight.
prereqs: [differential-privacy-definition, approximate-differential-privacy]
see_also: [dinur-nissim-reconstruction-attack, packing-lower-bound, private-query-release, gaussian-mechanism, membership-inference-attack, mwem, smalldb-mechanism, advanced-composition-theorem]
sources:
  - paper: "Mark Bun, Jonathan Ullman and Salil Vadhan, Fingerprinting codes and the price of approximate differential privacy, STOC 2014, pages 1 to 10"
    locator: the reduction from fingerprinting codes to lower bounds for attribute means, and the lower bounds for arbitrary counting queries and for marginals
  - paper: doi:10.1007/978-3-319-57048-8_7
    title: "Salil Vadhan, The complexity of differential privacy, in Tutorials on the Foundations of Cryptography, Springer, 2017, pages 347 to 450"
    locator: "Section 5.3: Definitions 5.16 and 5.17 (fingerprinting codes), Theorem 5.18 (Tardos), Claim 5.19 (Boneh-Shaw), Theorem 5.20 (codes imply lower bounds for attribute means), Theorems 5.21, 5.22 and 5.23"
  - paper: "Gabor Tardos, Optimal probabilistic fingerprint codes, STOC 2003, pages 116 to 125"
    locator: fingerprinting codes of length O(n^2 log(n/negl)) for n users
  - paper: "Dan Boneh and James Shaw, Collusion-secure fingerprinting for digital data, IEEE Transactions on Information Theory 44(5), 1998, pages 1897 to 1905"
    locator: the definition of collusion-secure fingerprinting and a code of length about n^3
  - paper: "Thomas Steinke and Jonathan Ullman, Between pure and approximate differential privacy, arXiv:1501.06095"
    locator: the lower bound of order sqrt(d log(1/delta))/(epsilon n) for attribute means
  - paper: "Cynthia Dwork, Adam Smith, Thomas Steinke, Jonathan Ullman and Salil Vadhan, Robust traceability from trace amounts, FOCS 2015, pages 650 to 669"
    locator: robust forms of the codes with biased Bernoulli columns, and the link to tracing with summary statistics
---

The fingerprinting code lower bound says that approximate differential privacy cannot answer $d$ attribute means with small error unless the dataset has about $\sqrt d$ rows. A fingerprinting code is a way to give each of $n$ users a secret string of $d$ bits, so that a group of users who mix their strings cannot make a new string without being traced. Bun, Ullman and Vadhan (2014) saw that an accurate private mechanism for attribute means would be such a mix that cannot be traced, which contradicts the security of the code. With the codes of Tardos, of length $d = \tilde O(n^2)$, every $(1, 1/(10n))$-DP mechanism with error below $\frac{1}{2}$ on $d$ attribute means needs $n = \tilde\Omega(\sqrt d)$. Steinke and Ullman sharpened this to error $\Omega(\sqrt{d\log(1/\delta)}/(\varepsilon n))$, which the [Gaussian mechanism](/gaussian-mechanism/) matches up to a factor $O(\sqrt{\log\log d})$.

## Statement

**Setting.** A dataset is $x \in (\{0,1\}^d)^n$, $n$ rows of $d$ bits. Two datasets are neighbors if they differ in one row (replace). The attribute means are the $d$ counting queries $q_j(x) = \frac{1}{n}\sum_i x_{i,j}$. A mechanism $M$ outputs $a \in [0,1]^d$, and it has error $\alpha$ with failure $\beta$ if, for every $x$, $\max_j |a_j - q_j(x)| \le \alpha$ with probability at least $1 - \beta$.

**Definition 1 (fingerprinting code, syntax; Vadhan Definition 5.16).** A fingerprinting code of length $d = d(n)$ for $n$ users is a pair of randomized algorithms. $\mathrm{Gen}$ outputs an $n \times d$ matrix $C$ of bits, with row $i$ the codeword of user $i$, and a tracing key $tk$. $\mathrm{Trace}(tk, w)$ takes $w \in \{0,1\}^d$ and outputs a user in $[n]$ or $\bot$. For a set $S \subseteq [n]$ of users, $w$ is feasible for $S$ if for every column $j$, $w_j = C_{i,j}$ for some $i \in S$. So on every column where all rows of $C_S$ have the same bit, $w$ has that bit too.

**Definition 2 (security; Vadhan Definition 5.17).** The code is secure if for every $n$, every $S \subseteq [n]$ and every randomized map $P$ from $C_S$ to $\{0,1\}^d$,

$$P[w \text{ is feasible for } S \text{ and } \mathrm{Trace}(tk, w) \notin S] \le \mathrm{negl}(n), \quad w = P(C_S),$$

with the probability over $\mathrm{Gen}$ and $P$, and $\mathrm{negl}(n) = n^{-\omega(1)}$.

**Theorem 1 (Tardos; Vadhan Theorem 5.18).** For every $n$ there is a secure fingerprinting code of length $d = \tilde O(n^2)$ for $n$ users.

**Theorem 2 (codes give lower bounds; Bun, Ullman and Vadhan, Vadhan Theorem 5.20).** Suppose a secure fingerprinting code of length $d$ for $n + 1$ users exists. Then for all large $n$, no $(1, 1/(10n))$-DP mechanism on $(\{0,1\}^d)^n$ answers the $d$ attribute means with error $\alpha < \frac{1}{2}$ and failure $\beta \le 1/(10n)$.

**Theorem 3 (attribute means; Steinke and Ullman, Vadhan Theorem 5.21).** For every $d$, $\varepsilon \in (0,1)$ and $\delta \in (2^{-d}, 1/n^{1.1})$, every $(\varepsilon, \delta)$-DP mechanism that with high probability answers all $d$ attribute means with error at most $\alpha$ has

$$\alpha \ge \Omega\left(\min\left\{\frac{\sqrt{d\log(1/\delta)}}{\varepsilon n}, 1\right\}\right).$$

**Theorem 4 (arbitrary counting queries; Bun, Ullman and Vadhan, Vadhan Theorem 5.22).** For all $d, n, k$ with $n^{2.1} \le k \le 2^{2^{d/3}}$, there is a family $Q$ of $k$ counting queries on $X = \{0,1\}^d$ such that every $(\varepsilon, 1/(10n))$-DP mechanism that with high probability answers all of $Q$ with error at most $\alpha$ has

$$\alpha \ge \tilde\Omega\left(\left(\frac{\sqrt{\log|X|}\,\log|Q|}{\varepsilon n}\right)^{1/2}\right).$$

Vadhan Theorem 5.23 gives a bound of the same kind for $t$-way marginals; see the source for its exact range of $n$ and $t$.

**The lesson.** For approximate DP, about $\sqrt d/\varepsilon$ rows are needed to answer $d$ attribute means with constant error. No method, however clever, beats the Gaussian mechanism by more than a factor $O(\sqrt{\log\log d})$ on this task.

## In plain words

A film studio marks each customer's copy of a film in $d$ scenes, with a different pattern for each customer. If a few customers mix their copies, the studio can still name one of them. The pirates must obey one rule: if all their copies agree in a scene, the pirate copy has that mark too.

Now let the patterns be the rows of a dataset. An accurate private mechanism for the column means, rounded to 0 or 1, obeys the rule, so the studio can name someone in the dataset. But a private output depends little on one person, so that person is also named when left out. Then the studio accuses an innocent person too often, and the code is not secure. So the dataset must be too small for the mechanism to be accurate.

## Proof

Theorem 2 is proved in full. Theorems 1, 3 and 4 are stated with their locators and not proved here.

**Theorem 2.** Assume $M$ is $(1, 1/(10n))$-DP and answers the $d$ attribute means with error below $\frac{1}{2}$ and failure $\beta \le 1/(10n)$. We may assume that the law of $M(x)$ does not depend on the order of the rows, since $M$ can first permute the rows at random. Let $P = \mathrm{Round} \circ M$, where $\mathrm{Round}$ rounds each coordinate to the nearest bit. By post-processing, $P$ is $(1, 1/(10n))$-DP.

Generate $(C, tk)$ for $n + 1$ users and let $S = [n]$.

*Step 1: $P(C_S)$ is feasible with probability at least $1 - \beta$.* If all rows of $C_S$ have the bit $b$ in column $j$, then $q_j(C_S) = b$. When $M$ succeeds, $|a_j - b| < \frac{1}{2}$, so $\mathrm{Round}(a_j) = b$.

*Step 2: someone in $S$ is accused often.* By security, $P[w \text{ feasible and } \mathrm{Trace}(tk, w) \notin S] \le \nu$ with $\nu$ negligible, so $P[\mathrm{Trace}(tk, P(C_S)) \in S] \ge 1 - \beta - \nu$. There are $n$ users in $S$, so some fixed $i^* \in S$ has

$$P[\mathrm{Trace}(tk, P(C_S)) = i^*] \ge \frac{1 - \beta - \nu}{n}.$$

*Step 3: privacy moves the accusation to a set without $i^*$.* Let $S' = [n+1] \setminus \{i^*\}$. Up to the order of rows, $C_{S'}$ is $C_S$ with row $i^*$ replaced by row $n+1$, so for each fixed $(C, tk)$ the two datasets are neighbors. The event $\{\mathrm{Trace}(tk, \cdot) = i^*\}$ is a fixed set of outputs of $P$, so DP gives, for each $(C, tk)$ and then on average,

$$P[\mathrm{Trace}(tk, P(C_S)) = i^*] \le e \cdot P[\mathrm{Trace}(tk, P(C_{S'})) = i^*] + \frac{1}{10n}.$$

*Step 4: the code is broken.* Combine steps 2 and 3:

$$P[\mathrm{Trace}(tk, P(C_{S'})) = i^*] \ge \frac{1}{e}\left(\frac{1 - \beta - \nu}{n} - \frac{1}{10n}\right) \ge \frac{0.8 - \nu}{e n} > \frac{0.29}{n} - \nu.$$

Now apply Steps 1 and 2 to $S'$, which has $n$ users: $P(C_{S'})$ is feasible for $S'$ with probability at least $1 - \beta$, and security for $S'$ gives $P[\mathrm{Trace}(tk, P(C_{S'})) = i^*] \le \beta + \nu \le 0.1/n + \nu$, since $i^* \notin S'$. For large $n$, $0.29/n - \nu > 0.1/n + \nu$, because $\nu$ is negligible. This is a contradiction. $\blacksquare$

**From Theorem 2 to $\sqrt d$ rows.** With Theorem 1, a code for $n + 1$ users has length $d = \tilde O(n^2)$. A mechanism for more columns also answers fewer columns, so for all $d$ above this length no such mechanism exists on $n$ rows. Put the other way, a $(1, 1/(10n))$-DP mechanism with error below $\frac{1}{2}$ on $d$ attribute means needs $n \ge \tilde\Omega(\sqrt d)$. Vadhan notes that simple reductions then give $\alpha \ge \tilde\Omega(\sqrt d)/(\varepsilon n)$ in general.

**A hand example of Step 1.** Let $C_S$ have the rows $1011$, $1101$ and $1001$. Columns 1 and 4 are 1 in every row, and columns 2 and 3 have the mean $\frac{1}{3}$. If every mean is within $\frac{1}{2}$, then $a_1 > \frac{1}{2}$ and $a_4 > \frac{1}{2}$, so the rounded output starts and ends with 1. It is feasible for $S$ whatever the middle bits are.

## Consequences

- **The price of approximate DP.** For $d$ attribute means with $\delta > 0$, the error is $\tilde\Theta(\sqrt{d \log(1/\delta)}/(\varepsilon n))$. The [packing lower bound](/packing-lower-bound/) gives only $\Omega(\min\{d, \log(1/\delta)\}/(\varepsilon n))$ here, and the [reconstruction theorems](/dinur-nissim-reconstruction-attack/) give $\Omega(\sqrt d/n)$ only when $d < n$. Theorem 3 contains both (Vadhan, after Theorem 5.21).
- **Query release.** Theorem 4 shows that the error of private multiplicative weights, and so of [MWEM](/mwem/)-style methods, is nearly optimal for worst-case families of counting queries. This is a limit for every [private query release](/private-query-release/) method.
- **Roles switch.** In the proof the private mechanism plays the pirate, and the tracing algorithm plays the adversary against privacy. A tracing adversary decides only if a person is in the data, which is weaker than [reconstruction](/dinur-nissim-reconstruction-attack/), but it can still matter, for example if all the rows are patients with one disease.
- **The real-world lesson.** Homer et al. (2008) showed that exact summary statistics of genomic data can show if one person's DNA is in a study. After that, the US National Institutes of Health removed open online access to summary statistics of some genomic datasets (Zerhouni and Nabel 2008, cited by Vadhan as [62, 109]). Dwork, Smith, Steinke, Ullman and Vadhan (2015) show that the risk stays when the statistics are only approximate and the attacker knows little about the code. This page gives only the theorem and its lesson. The defense is noise of the size of Theorem 3, from a cryptographic source of randomness with exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020).

## Tightness

The bounds are nearly tight (theorems). For attribute means, the Gaussian mechanism with the composition bound of Vadhan Theorem 2.7 has error $O(\sqrt{d \log(1/\delta) \log\log d}/(\varepsilon n))$, which is Theorem 3 up to $O(\sqrt{\log\log d})$. For arbitrary families of counting queries, private multiplicative weights (Hardt and Rothblum; Vadhan Theorem 4.3) has error $O((\sqrt{\log|X| \log(1/\delta)}\,\log|Q|/(\varepsilon n))^{1/2})$. With $\delta = 1/(10n)$, Theorem 4 matches it up to the factor $\log(1/\delta)^{1/4}$ and log factors. Theorem 3 removes the restriction of Theorem 2 to $\varepsilon = 1$ and $\delta = 1/(10n)$. The range of $\delta$ in Theorem 3 is needed: for $\delta \le 2^{-d}$ the [packing lower bound](/packing-lower-bound/) of order $d/(\varepsilon n)$ takes over.

## History

Boneh and Shaw (1998) defined collusion-secure fingerprinting codes for digital content, with a code of length about $n^3$, and Tardos (2003) gave codes of the optimal length $\tilde O(n^2)$. Ullman (STOC 2013) used fingerprinting codes inside a cryptographic construction to show that answering $n^{2+o(1)}$ counting queries privately and efficiently is hard. Bun, Ullman and Vadhan (STOC 2014) proved the information-theoretic lower bounds for attribute means, arbitrary counting queries and marginals. Steinke and Ullman (2015) proved the bound with $\sqrt{\log(1/\delta)}$, and Dwork, Smith, Steinke, Ullman and Vadhan (FOCS 2015) made the tracing robust. Vadhan (2017, Section 5.3) gives the presentation used here.

## References
