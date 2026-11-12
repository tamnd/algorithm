---
tag: 4YDQ2M
kind: theorem
slug: margin-generalization-bound
name: Margin-based generalization bound
aliases:
- margin bound
- large margin generalization bound
area: machine-learning/supervised-learning
level: research
summary: "A linear classifier of norm 1 on data of norm at most R has error at most its fraction of margin below gamma plus about 2R/(gamma sqrt(n)), with no dependence on the dimension."
prereqs: [rademacher-complexity, vc-dimension]
see_also: [support-vector-machine, adaboost, boosting, halfspace-learning, perceptron-convergence-theorem, hinge-loss, structural-risk-minimization, fundamental-theorem-of-statistical-learning]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Theorem 26.12 (bound for Lipschitz losses of norm bounded linear predictors), Theorem 26.13 and Remark 26.1 (hard-SVM, ramp loss), Theorem 26.14 (data dependent norm), Theorem 15.4 (hard-SVM, (gamma, rho)-margin)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Section 5.4 (Theorem 5.8 margin bound, Theorem 5.9 uniform over the margin, Theorem 5.10 and Corollary 5.11 for linear classes), Section 7.3 (Corollaries 7.5 and 7.6, margin bounds for ensembles)
  - paper: doi:10.1109/18.661502
    title: P. L. Bartlett, The sample complexity of pattern classification with neural networks, the size of the weights is more important than the size of the network, IEEE Transactions on Information Theory 44(2), 1998
    locator: pp. 525 to 536 (margin bounds from the fat-shattering dimension)
  - paper: doi:10.1214/aos/1024691352
    title: R. E. Schapire, Y. Freund, P. Bartlett and W. S. Lee, Boosting the margin, a new explanation for the effectiveness of voting methods, Annals of Statistics 26(5), 1998
    locator: pp. 1651 to 1686 (the margin bound for convex combinations of base classifiers)
  - paper: "P. L. Bartlett and S. Mendelson, Rademacher and Gaussian complexities: risk bounds and structural results, Journal of Machine Learning Research 3, 2002"
    locator: pp. 463 to 482 (margin bounds through Rademacher complexity)
---

A margin-based generalization bound controls the error of a classifier $x \mapsto \mathrm{sign}(f(x))$ by how confidently it classifies the training data. The margin of an example $(x, y)$ with $y \in \{-1, +1\}$ is $y f(x)$. For linear predictors $f(x) = \langle w, x \rangle$ with $\|w\| \le 1$ on inputs with $\|x\| \le R$, the true error is at most the fraction of training examples with margin below $\gamma$, plus about $2R/(\gamma\sqrt{n})$, plus a confidence term. The bound does not depend on the dimension $d$, while the [VC dimension](/vc-dimension/) of halfspaces is $d + 1$. Bartlett (1998) proved bounds of this type through the fat-shattering dimension, and Schapire, Freund, Bartlett and Lee (1998) used them to explain [boosting](/boosting/). This page states the form of Shalev-Shwartz and Ben-David (Theorem 26.12 with the ramp loss) and of Mohri, Rostamizadeh and Talwalkar (Theorem 5.9), proved through [Rademacher complexity](/rademacher-complexity/).

## Statement

Let $D$ be a distribution on $X \times \{-1, +1\}$ with $X = \{x \in \mathbb{R}^d : \|x\|_2 \le R\}$, and let $S$ be $n$ i.i.d. examples. For $\gamma > 0$ and a vector $w$, write
$$\hat L_\gamma(w) = \frac{1}{n}\,\big|\{i : y_i \langle w, x_i \rangle < \gamma\}\big|, \qquad L(w) = \Pr_{(x, y) \sim D}\big[y \langle w, x \rangle \le 0\big].$$

**Theorem A (fixed margin).** For every $\gamma > 0$ and $\delta \in (0, 1)$, with probability at least $1 - \delta$ over $S$, every $w$ with $\|w\|_2 \le 1$ satisfies
$$L(w) \le \hat L_\gamma(w) + \frac{2R}{\gamma\sqrt{n}} + \sqrt{\frac{2\ln(2/\delta)}{n}}.$$

**Theorem B (all margins at once).** With probability at least $1 - \delta$, every $w$ with $\|w\|_2 \le 1$ and every $\gamma \in (0, R]$ satisfy
$$L(w) \le \hat L_\gamma(w) + \frac{4R}{\gamma\sqrt{n}} + \sqrt{\frac{\ln \log_2(2R/\gamma)}{n}} + \sqrt{\frac{\ln(2/\delta)}{2n}}.$$

Theorem A is Theorem 26.12 of Shalev-Shwartz and Ben-David applied to the ramp loss. Theorem B is Theorem 5.9 of Mohri, Rostamizadeh and Talwalkar with their bound $R_n(H) \le R/\sqrt{n}$ for this class (Theorem 5.10); there the margin term is the ramp loss, which is at most $\hat L_\gamma(w)$. Since $\gamma$ may be chosen after the data, Theorem B can be applied with the margin that the learned $w$ actually achieves. In both, the dimension $d$ does not appear, and $d$ may be infinite, as in kernel methods.

## In plain words

A linear classifier draws a line through the data. Some training points lie far from the line on the correct side, others lie close to it or on the wrong side. The bound says: count the training points that are wrong or too close to the line. The error on new data is at most that fraction plus a term that shrinks when the safety gap is wide compared with the spread of the data, and when there is more data. The number of features does not matter. A classifier that separates the training data with a wide gap is safe even in a space with millions of features.

## Proof

**Theorem A.** Fix $\gamma$. Let $\varphi_\gamma(t) = \min(1, \max(0, 1 - t/\gamma))$, the ramp loss. For every real $t$,
$$1[t \le 0] \le \varphi_\gamma(t) \le 1[t < \gamma],$$
because $\varphi_\gamma = 1$ for $t \le 0$, $\varphi_\gamma = 0$ for $t \ge \gamma$, and $\varphi_\gamma \in [0, 1]$ in between. So $L(w) \le \mathbb{E}_D[\varphi_\gamma(y\langle w, x\rangle)]$ and $\frac{1}{n}\sum_i \varphi_\gamma(y_i \langle w, x_i \rangle) \le \hat L_\gamma(w)$.

The function $\varphi_\gamma$ is $(1/\gamma)$-Lipschitz and takes values in $[0, 1]$. Apply the bound of [Rademacher complexity](/rademacher-complexity/) to the class $F = \{(x, y) \mapsto \varphi_\gamma(y\langle w, x\rangle) : \|w\| \le 1\}$, in the form of Theorem 26.5 of Shalev-Shwartz and Ben-David: with probability at least $1 - \delta$, for every $w$,
$$\mathbb{E}_D[\varphi_\gamma(y\langle w, x\rangle)] \le \frac{1}{n}\sum_i \varphi_\gamma(y_i\langle w, x_i\rangle) + 2\,\mathbb{E}_S \hat R_S(F) + \sqrt{\frac{2\ln(2/\delta)}{n}}.$$
By the contraction lemma (Lemma 26.9), $\hat R_S(F) \le \frac{1}{\gamma}\hat R_S(\{(x, y) \mapsto y\langle w, x\rangle\})$. Multiplying coordinate $i$ by the fixed sign $y_i$ does not change the distribution of $\sigma_i y_i$, so this equals $\frac{1}{\gamma}\hat R_S(\{x \mapsto \langle w, x\rangle : \|w\| \le 1\})$. By the linear class bound (Lemma 26.10), this is at most $\frac{1}{\gamma}\cdot\frac{R}{\sqrt{n}}$. Combining the three displays gives Theorem A. $\blacksquare$

**Theorem B.** Use the fixed margin bound at the margins $\gamma_k = R/2^k$ for $k = 1, 2, \ldots$, and at level $k$ add $\sqrt{\ln k / n}$ to the deviation. By McDiarmid's inequality the failure probability at level $k$ is at most $e^{-2n\varepsilon^2}/k^2$, and these sum to at most $2e^{-2n\varepsilon^2}$, so a union bound makes all levels hold at once. For any $\gamma \in (0, R]$, take the $k$ with $\gamma_k < \gamma \le 2\gamma_k$. Then $\hat L_{\gamma_k}(w) \le \hat L_\gamma(w)$, the complexity term at $\gamma_k$ is at most twice that at $\gamma$, and $\ln k \le \ln\log_2(2R/\gamma)$. This is the proof of Mohri et al., Theorem 5.9, which gives the stated constants. $\blacksquare$

## Consequences

- **Support vector machines.** If the hard [support vector machine](/support-vector-machine/) separates the sample with margin $\gamma$ at $\|w\| = 1$, then $\hat L_\gamma(w) = 0$, and the error is at most $O(R/(\gamma\sqrt{n}) + \sqrt{\ln(1/\delta)/n})$. In the form of Shalev-Shwartz and Ben-David, Theorem 26.13: if some $w^\star$ has $y\langle w^\star, x\rangle \ge 1$ on the support of $D$ and $\|x\| \le R$, the hard-SVM output has error at most $\frac{2R\|w^\star\|}{\sqrt{n}} + (1 + R\|w^\star\|)\sqrt{\frac{2\ln(2/\delta)}{n}}$. The soft SVM minimizes the [hinge loss](/hinge-loss/), an upper bound on the ramp loss, plus a norm penalty, which is the trade-off the bound suggests.
- **Numbers.** For $R = 1$, $\gamma = 0.1$, $n = 10^5$ and $\delta = 0.05$, Theorem A gives the complexity term $2R/(\gamma\sqrt{n}) \approx 0.0632$ and the confidence term $\sqrt{2\ln 40/n} \approx 0.0086$. With $\gamma = 0.05$ the first term doubles to about $0.1265$. The VC bound for halfspaces in dimension $d = 10^4$, of the form $\sqrt{2(d+1)\ln(en/(d+1))/n}$ (Mohri et al., Corollary 3.19), is about $0.813$ at the same $n$.
- **Boosting.** A vote $f = \sum_t \alpha_t h_t$ with $\alpha_t \ge 0$ and $\sum_t \alpha_t = 1$ lies in the convex hull of the base class, which has the same Rademacher complexity as the base class. For a base class of VC dimension $d$, this gives, with probability $1 - \delta$, for every such $f$ and margin $\theta$, $L(f) \le \hat L_\theta(f) + \frac{2}{\theta}\sqrt{\frac{2d\ln(en/d)}{n}} + \sqrt{\frac{\ln(1/\delta)}{2n}}$ (Mohri et al., Corollary 7.6). Schapire, Freund, Bartlett and Lee (1998) proved a bound of order $\sqrt{d\ln^2(n/d)/(n\theta^2) + \ln(1/\delta)/n}$ by a different, sampling argument. Since [AdaBoost](/adaboost/) keeps increasing the margins of the training examples after the training error reaches zero, the bound explains why its test error can keep falling with more rounds.
- **Neural networks.** Bartlett (1998) showed that for networks with small weights, the bound depends on the size of the weights and the margin, not on the number of weights. Later norm based bounds for deep networks follow the same pattern.
- **Structural risk minimization over the norm.** Theorem B, and the data dependent bound of Shalev-Shwartz and Ben-David, Theorem 26.14, hold for all margins or norms at once, so they can be applied to the output of a learner, as in [structural risk minimization](/structural-risk-minimization/).

## Tightness

**The rate $(R/\gamma)^2$ cannot be removed.** Let $k \le (R/\gamma)^2$ and take the points $Re_1, \ldots, Re_k$ in $\mathbb{R}^k$. For any labels $y_1, \ldots, y_k \in \{-1, +1\}$, the vector $w = \frac{1}{\sqrt{k}}\sum_i y_i e_i$ has $\|w\| = 1$ and $y_i\langle w, Re_i\rangle = R/\sqrt{k} \ge \gamma$. So unit norm halfspaces realize every labeling of these $k$ points with margin $\gamma$. The no free lunch argument of the [fundamental theorem](/fundamental-theorem-of-statistical-learning/), applied to these points, shows that a learner with fewer than $k/2$ examples has error at least $1/8$ with probability at least $1/7$ on some distribution that is separable with margin $\gamma$. So the number of examples needed for constant error is at least of order $(R/\gamma)^2$, which matches $2R/(\gamma\sqrt{n})$ up to constants.

**The $\sqrt{\cdot}$ rate in the separable case.** When the data is separable with margin $\gamma$, the $1/\sqrt{n}$ rate of Theorem A is not tight. Bounds of order $(R/\gamma)^2/n$ up to logarithmic factors hold in this case; Shalev-Shwartz and Ben-David, Remark 26.1, note that a sample size of order $(R\|w^\star\|)^2/\varepsilon$ suffices, and the [perceptron convergence theorem](/perceptron-convergence-theorem/) gives the same quantity $(R/\gamma)^2$ as a mistake bound.

**Dependence on the margin distribution.** The bound uses only the fraction of points below one margin. Refined bounds use the whole distribution of margins, and bounds for boosting that use the least margin alone can be loose: algorithms that maximize the least margin do not always have lower test error.

## History

Vapnik showed that the VC dimension of halfspaces with margin $\gamma$ on data in a ball of radius $R$ is at most about $(R/\gamma)^2$, which motivated the support vector machine. Shawe-Taylor, Bartlett, Williamson and Anthony (1998) turned this into data dependent bounds through structural risk minimization. Bartlett (1998) used the fat-shattering dimension at scale $\gamma$ to bound the error of real valued classifiers by the empirical margin error, and applied it to neural networks. In the same year Schapire, Freund, Bartlett and Lee used margins to explain the behaviour of AdaBoost. Koltchinskii and Panchenko (2002) and Bartlett and Mendelson (2002) gave the proof through Rademacher complexity and contraction that is now standard.

## References
