---
tag: B5J3MT
kind: theorem
slug: privacy-amplification-by-subsampling
name: Privacy amplification by subsampling
aliases:
- amplification by sampling
area: security-and-privacy/differential-privacy
level: advanced
summary: "An (epsilon, delta)-DP mechanism run on a Poisson sample with rate q is (ln(1 + q(e^epsilon - 1)), q delta)-DP under add/remove, about q(e^epsilon - 1); without replacement it holds under replace."
history:
  year: 2008
  people: [Shiva Prasad Kasiviswanathan, Homin K. Lee, Kobbi Nissim, Sofya Raskhodnikova, Adam Smith, Borja Balle, Gilles Barthe, Marco Gaboardi]
  note: "Kasiviswanathan et al. used amplification by sampling in their work on private learning (FOCS 2008, SIAM Journal on Computing 2011). Balle, Barthe and Gaboardi gave tight bounds for each sampling scheme and neighbor relation in 2018."
prereqs: [approximate-differential-privacy, sequential-composition-theorem]
see_also: [dp-sgd, moments-accountant, privacy-amplification-by-shuffling, randomized-response, renyi-differential-privacy, numerical-privacy-accounting, subsample-and-aggregate, bernoulli-sampling]
sources:
  - url: "https://arxiv.org/abs/1807.01647"
    title: "Borja Balle, Gilles Barthe and Marco Gaboardi, Privacy amplification by subsampling: tight analyses via couplings and divergences, NeurIPS 2018, arXiv 1807.01647"
    locator: "the bounds for Poisson subsampling with add/remove neighbors and for sampling without replacement with replace neighbors, proved by couplings and advanced joint convexity"
  - paper: "Shiva Prasad Kasiviswanathan, Homin K. Lee, Kobbi Nissim, Sofya Raskhodnikova and Adam Smith, What can we learn privately?, SIAM Journal on Computing 40(3), 2011"
    locator: "the lemma that running a private algorithm on a random sample of the data improves its privacy parameter"
  - url: "https://arxiv.org/abs/1908.10530"
    title: "Ilya Mironov, Kunal Talwar and Li Zhang, Renyi differential privacy of the sampled Gaussian mechanism, arXiv 1908.10530, 2019"
    locator: "Definition 3 (Poisson sampling with add/remove neighbors) and Table 1 (bounds for the subsampled Gaussian under different sampling schemes)"
---

Privacy amplification by subsampling says that a private mechanism becomes more private when it runs on a random sample of the data that the observer does not see. If each record joins the sample independently with probability $q$ (Poisson sampling), and the mechanism is $(\varepsilon, \delta)$-differentially private under add/remove neighbors, then the mechanism on the sample is $(\ln(1 + q(e^{\varepsilon} - 1)), q\delta)$-DP. For small $\varepsilon$ the new parameter is about $q(e^{\varepsilon} - 1)$, which is about $q\varepsilon$. A person who is probably not in the sample can lose little. The theorem is a key step in the analysis of [DP-SGD](/dp-sgd/), where each step uses a small random batch, and of the [moments accountant](/moments-accountant/). The exact bound depends on the sampling scheme and on the neighbor relation, so a page or a system that uses it must name both.

## Statement

A dataset is a finite multiset of records. Under add/remove, $x \sim x'$ when one of them is the other plus one record. Under replace, $x \sim x'$ when they have the same size and differ in one record.

**Poisson subsampling.** $\mathrm{Poi}_q(x)$ keeps each record of $x$ independently with probability $q \in [0, 1]$. The sample stays hidden; only the output of the mechanism is released.

**Sampling without replacement.** For datasets of size $n$ and $1 \le m \le n$, $\mathrm{WOR}_m(x)$ is a uniform random subset of $m$ records of $x$. Write $q = m/n$.

**Theorem.** Let $\varepsilon \ge 0$, $\delta \in [0, 1]$, and $\varepsilon_q = \ln(1 + q(e^{\varepsilon} - 1))$.

1. **(Poisson, add/remove.)** If $M$ is $(\varepsilon, \delta)$-DP under add/remove, then $M \circ \mathrm{Poi}_q$ is $(\varepsilon_q, q\delta)$-DP under add/remove.
2. **(Without replacement, replace; Balle, Barthe and Gaboardi.)** If $M$ is $(\varepsilon, \delta)$-DP under replace on datasets of size $m$, then $M \circ \mathrm{WOR}_m$ is $(\varepsilon_q, q\delta)$-DP under replace on datasets of size $n$.

Both bounds are tight for pure DP ($\delta = 0$). Since $\ln(1 + z) \le z$, $\varepsilon_q \le q(e^{\varepsilon} - 1)$, and for $\varepsilon \le 1$, $\varepsilon_q \le 2q\varepsilon$.

## In plain words

Suppose a survey picks each person by a coin flip, with a small chance of being picked, and keeps the list of picked people secret. Then it runs a private analysis on the picked people only.

An observer who wants to learn about you must first guess whether you were picked. Most of the time you were not, and then the result does not depend on you at all. When you were picked, you get the usual protection.

Together, this gives a much stronger protection than the analysis gives alone. When the chance of being picked is small and the analysis is already quite private, the leak shrinks by about that chance. When the analysis leaks a lot, the gain is much smaller.

## Proof

The proof of part 1 is full. Part 2 is a marked sketch.

**Part 1.** Let $x' = x \cup \{r\}$. A Poisson sample of $x'$ is a Poisson sample $T$ of $x$, with $r$ added with probability $q$, independently of $T$. Fix an event $S$ of outputs and write

$$A = E_T\left[\Pr[M(T) \in S]\right], \qquad B = E_T\left[\Pr[M(T \cup \{r\}) \in S]\right].$$

Then $\Pr[M(\mathrm{Poi}_q(x)) \in S] = A$ and $\Pr[M(\mathrm{Poi}_q(x')) \in S] = (1-q)A + qB$. For each $T$, the sets $T$ and $T \cup \{r\}$ are add/remove neighbors, so averaging the DP inequality over $T$ gives

$$B \le e^{\varepsilon} A + \delta \qquad\text{and}\qquad A \le e^{\varepsilon} B + \delta.$$

Write $u = e^{\varepsilon}$, so $e^{\varepsilon_q} = 1 + q(u - 1)$.

*From $x'$ to $x$.* $(1-q)A + qB \le (1 - q + qu)A + q\delta = e^{\varepsilon_q}A + q\delta$.

*From $x$ to $x'$.* The second inequality gives $B \ge (A - \delta)/u$, so $(1-q)A + qB \ge (1 - q + q/u)A - q\delta/u$. The identity

$$(1 + q(u-1))\left(1 - q + \frac{q}{u}\right) = 1 + \frac{q(1-q)(u-1)^2}{u} \ge 1$$

gives $1/(1 - q + q/u) \le e^{\varepsilon_q}$. Hence $A \le e^{\varepsilon_q}\left((1-q)A + qB\right) + e^{\varepsilon_q}q\delta/u$. Finally $e^{\varepsilon_q}/u = (1 + q(u-1))/u \le 1$, so the last term is at most $q\delta$.

The case $x = x' \cup \{r\}$ is the same pair in the other order, and both orders are covered.

**Part 2 (sketch).** Let $x'$ be $x$ with record $r$ replaced by $r'$. Couple the two samples: draw $\mathrm{WOR}_m(x)$, and replace $r$ by $r'$ when it is drawn. The samples differ, in one record, only when $r$ is drawn, which has probability $m/n = q$. So the output law under $x'$ is $(1-q)A + qB'$ against $(1-q)A + qB$ under $x$, where each pair of components comes from replace neighbors. Balle, Barthe and Gaboardi bound such mixtures by their advanced joint convexity of the hockey-stick divergence, which gives $(\varepsilon_q, q\delta)$. The full proof is in their paper (NeurIPS 2018, arXiv 1807.01647), in the section on sampling without replacement. $\blacksquare$

## Consequences

- **The numbers.** For $q = 0.01$ and $\varepsilon = 1$, $\varepsilon_q = \ln(1 + 0.01(e - 1)) = 0.017037$, close to $q(e - 1) = 0.017183$. For $q = 0.01$ and $\varepsilon = 5$, $\varepsilon_q = 0.9059$, far above $q\varepsilon = 0.05$. The form "about $q\varepsilon$" is a heuristic for small $\varepsilon$ only.
- **Private learning.** [DP-SGD](/dp-sgd/) runs a Gaussian mechanism on a random batch at each step. The [moments accountant](/moments-accountant/) uses a sharper form of amplification, for the Renyi divergence of the subsampled Gaussian, and then composes the steps.
- **Other schemes.** Sampling with replacement and fixed-size samples under add/remove neighbors have different bounds. Balle, Barthe and Gaboardi list them. A system must use the bound of the scheme that it runs.
- **Related amplification.** [Privacy amplification by shuffling](/privacy-amplification-by-shuffling/) is a different effect: it hides who sent each local report, not who is in the sample.

## Tightness

Let a special record $v$ be absent from $x$, and let $x' = x \cup \{v\}$. Let $M(T)$ apply [randomized response](/randomized-response/) with parameter $\varepsilon$ to the bit "$v$ is in $T$". This bit changes by at most 1 between add/remove neighbors, so $M$ is $\varepsilon$-DP. On $x$, the bit is 0, and $M$ outputs 1 with probability $1/(1 + u)$. On $x'$, the bit is 1 with probability $q$, and $M$ outputs 1 with probability

$$q\frac{u}{1+u} + (1-q)\frac{1}{1+u} = \frac{1 + q(u-1)}{1+u}.$$

The ratio is exactly $1 + q(u - 1) = e^{\varepsilon_q}$. So $M \circ \mathrm{Poi}_q$ is not $\varepsilon''$-DP for any $\varepsilon'' < \varepsilon_q$, and part 1 is tight.

## History

Kasiviswanathan, Lee, Nissim, Raskhodnikova and Smith used amplification by sampling in their study of what can be learned privately (FOCS 2008; SIAM Journal on Computing 2011), and the effect appears in work of Smith from the same period. Later papers stated many versions, with different sampling schemes and neighbor relations. Balle, Barthe and Gaboardi (NeurIPS 2018) gave a uniform method through couplings and divergences, and tight bounds for each scheme. Abadi et al. (2016) and Mironov, Talwar and Zhang (2019) analyzed the subsampled Gaussian mechanism directly, which is sharper than amplification followed by composition.

## References
