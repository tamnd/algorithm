---
tag: M8YC0B
kind: theorem
slug: fundamental-theorem-of-statistical-learning
name: Fundamental theorem of statistical learning
aliases:
- fundamental theorem of PAC learning
- VC characterization of PAC learnability
area: machine-learning/supervised-learning
level: advanced
summary: "For binary classes under the 0-1 loss, uniform convergence, agnostic PAC learnability, PAC learnability and finite VC dimension are equivalent, with sample sizes set by the VC dimension."
prereqs: [agnostic-pac-learning, sauer-shelah-lemma, rademacher-complexity]
see_also: [vc-dimension, pac-learning, empirical-risk-minimization, no-free-lunch-theorem-learning, epsilon-net-theorem, structural-risk-minimization, generalization-error]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Theorem 6.7 (the equivalences), Theorem 6.8 (the quantitative version), Theorem 6.6, Theorem 6.11, Section 5.1 (Theorem 5.1, no free lunch), Theorem 26.5 and Lemma 26.8, Chapter 28 (proofs of the sample sizes)
  - paper: doi:10.1145/76359.76371
    title: A. Blumer, A. Ehrenfeucht, D. Haussler and M. K. Warmuth, Learnability and the Vapnik-Chervonenkis dimension, Journal of the ACM 36(4), 1989
    locator: pp. 929 to 965 (finite VC dimension is necessary and sufficient for PAC learnability)
  - paper: doi:10.1137/1116025
    title: V. N. Vapnik and A. Ya. Chervonenkis, On the uniform convergence of relative frequencies of events to their probabilities, Theory of Probability and Its Applications 16(2), 1971
    locator: pp. 264 to 280 (uniform convergence from the growth function)
  - paper: doi:10.1016/0890-5401(89)90002-3
    title: A. Ehrenfeucht, D. Haussler, M. Kearns and L. Valiant, A general lower bound on the number of examples needed for learning, Information and Computation 82(3), 1989
    locator: pp. 247 to 261 (the lower bound of order (d + ln(1/delta))/epsilon)
  - paper: "S. Hanneke, The optimal sample complexity of PAC learning, Journal of Machine Learning Research 17(38), 2016"
    locator: pp. 1 to 15 (an improper learner with sample size of order (d + ln(1/delta))/epsilon)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Corollary 3.19 (VC generalization bounds), Theorems 3.20 and 3.23 (lower bounds)
---

The fundamental theorem of statistical learning says that for a binary [hypothesis class](/hypothesis-class/) under the 0-1 loss, four properties are the same: uniform convergence, [agnostic PAC learnability](/agnostic-pac-learning/), [PAC learnability](/pac-learning/), and finite [VC dimension](/vc-dimension/). When they hold, [empirical risk minimization](/empirical-risk-minimization/) is a learner, and the VC dimension $d$ fixes the number of examples up to constant factors: about $(d + \ln(1/\delta))/\varepsilon^2$ in the agnostic case, and between $(d + \ln(1/\delta))/\varepsilon$ and $(d \ln(1/\varepsilon) + \ln(1/\delta))/\varepsilon$ in the realizable case. The result joins the uniform convergence theorem of Vapnik and Chervonenkis (1971) with the PAC model of Valiant, as Blumer, Ehrenfeucht, Haussler and Warmuth (1989) showed. The name and the form below are those of Shalev-Shwartz and Ben-David (2014), Theorems 6.7 and 6.8.

## Statement

Let $H$ be a class of functions $X \to \{0, 1\}$ and let the loss be the 0-1 loss. Notation: $n$ is the number of examples, $L_D$ the true risk and $L_S$ the empirical risk.

**Theorem 6.7 (equivalences).** The following are equivalent.

1. $H$ has the uniform convergence property.
2. Any ERM rule is a successful agnostic PAC learner for $H$.
3. $H$ is agnostic PAC learnable.
4. $H$ is PAC learnable.
5. Any ERM rule is a successful PAC learner for $H$.
6. $H$ has a finite VC dimension.

**Theorem 6.8 (quantitative version).** Let $\mathrm{VC}(H) = d < \infty$. There are absolute constants $C_1, C_2$ such that

- $H$ has uniform convergence with $C_1 \dfrac{d + \ln(1/\delta)}{\varepsilon^2} \le m^{UC}_H(\varepsilon, \delta) \le C_2 \dfrac{d + \ln(1/\delta)}{\varepsilon^2}$;
- $H$ is agnostic PAC learnable with $C_1 \dfrac{d + \ln(1/\delta)}{\varepsilon^2} \le m_H(\varepsilon, \delta) \le C_2 \dfrac{d + \ln(1/\delta)}{\varepsilon^2}$;
- $H$ is PAC learnable with $C_1 \dfrac{d + \ln(1/\delta)}{\varepsilon} \le m_H(\varepsilon, \delta) \le C_2 \dfrac{d \ln(1/\varepsilon) + \ln(1/\delta)}{\varepsilon}$.

The theorem does not give the constants. The upper bounds are achieved by ERM.

## In plain words

For yes-or-no prediction, one number decides whether learning from examples is possible at all. That number is the largest group of points on which the family of rules can produce every pattern of answers. If it is finite, then picking the rule that makes the fewest mistakes on the training data works, and the training error is close to the true error for every rule at once. If it is infinite, every method fails on some data source. The same number also gives the amount of data needed, up to constant factors.

## Proof

The proof is a cycle of implications: $1 \Rightarrow 2$, $2 \Rightarrow 3$, $3 \Rightarrow 4$, $2 \Rightarrow 5$, $5 \Rightarrow 4$, $4 \Rightarrow 6$ and $6 \Rightarrow 1$.

**$1 \Rightarrow 2$.** On an $\varepsilon/2$-representative sample, an ERM output $h_S$ satisfies, for every $h \in H$,
$$L_D(h_S) \le L_S(h_S) + \tfrac{\varepsilon}{2} \le L_S(h) + \tfrac{\varepsilon}{2} \le L_D(h) + \varepsilon.$$
So $m_H(\varepsilon, \delta) \le m^{UC}_H(\varepsilon/2, \delta)$ (Shalev-Shwartz and Ben-David, Corollary 4.4).

**$2 \Rightarrow 3$, $2 \Rightarrow 5$, $3 \Rightarrow 4$, $5 \Rightarrow 4$.** These hold by definition. In the realizable case $\min_{h \in H} L_D(h) = 0$, so an agnostic learner is a PAC learner, and a successful ERM rule is a learner.

**$4 \Rightarrow 6$ (no free lunch).** Suppose $\mathrm{VC}(H) = \infty$, and let $A$ be any learner that uses $m$ examples. Choose a set $C$ of $2m$ points that $H$ shatters. For each of the $T = 2^{2m}$ functions $f_j : C \to \{0, 1\}$, let $D_j$ be the uniform distribution on $C$ with labels from $f_j$. Each $D_j$ is realizable by $H$, because $H$ shatters $C$. We show that some $j$ has $\mathbb{E}_S[L_{D_j}(A(S))] \ge 1/4$.

Fix one of the $k = (2m)^m$ sequences of $m$ points of $C$, and let $S^j$ be that sequence labelled by $f_j$. At least $p \ge m$ points $v_1, \ldots, v_p$ of $C$ are not in the sequence. For any $h$,
$$L_{D_j}(h) \ge \frac{1}{2m} \sum_{r=1}^{p} 1[h(v_r) \ne f_j(v_r)] \ge \frac{1}{2p} \sum_{r=1}^{p} 1[h(v_r) \ne f_j(v_r)].$$
Pair each $j$ with the $j'$ such that $f_{j'}$ differs from $f_j$ only at $v_r$. The two samples $S^j$ and $S^{j'}$ are equal, so $A$ returns the same $h$ on both, and $h$ is wrong at $v_r$ for exactly one of the pair. So the average over $j$ of $1[A(S^j)(v_r) \ne f_j(v_r)]$ is $1/2$ for each $r$, and the average over $j$ of $L_{D_j}(A(S^j))$ is at least $\frac{1}{2p} \cdot p \cdot \frac{1}{2} = \frac{1}{4}$. This holds for each sequence, so it holds for the average over sequences, which is $\frac{1}{T}\sum_j \mathbb{E}_S[L_{D_j}(A(S))]$. A maximum is at least an average, so some $j$ has $\mathbb{E}_S[L_{D_j}(A(S))] \ge 1/4$.

Let $L = L_{D_j}(A(S)) \in [0, 1]$. Then $\frac{1}{4} \le \mathbb{E}[L] \le \Pr[L \ge \frac{1}{8}] + \frac{1}{8}(1 - \Pr[L \ge \frac{1}{8}])$, so $\Pr[L \ge 1/8] \ge 1/7$. For $\varepsilon = 1/8$ and $\delta < 1/7$ no number $m$ of examples suffices, so $H$ is not PAC learnable. This is Theorem 5.1 and Theorem 6.6 of Shalev-Shwartz and Ben-David; see the [no-free-lunch theorem](/no-free-lunch-theorem-learning/).

**$6 \Rightarrow 1$ (finite VC dimension gives uniform convergence).** Let $\mathrm{VC}(H) = d$, fix a sample $S$ of size $n \ge d$, and let $A = \{(1[h(x_i) \ne y_i])_{i=1}^n : h \in H\} \subseteq \{0, 1\}^n$ be the set of loss vectors. A loss vector is fixed by the restriction of $h$ to $x_1, \ldots, x_n$, so by the [Sauer-Shelah lemma](/sauer-shelah-lemma/), $|A| \le \tau_H(n) \le (en/d)^d$. Each vector has Euclidean norm at most $\sqrt{n}$. Massart's lemma (Lemma 26.8) bounds the empirical [Rademacher complexity](/rademacher-complexity/):
$$R(A) \le \frac{\sqrt{n}\sqrt{2 \ln |A|}}{n} \le \sqrt{\frac{2d \ln(en/d)}{n}}.$$
Theorem 26.5 of Shalev-Shwartz and Ben-David (symmetrization and McDiarmid's inequality, for a loss in $[0, 1]$) then gives, with probability at least $1 - \delta/2$, for all $h \in H$,
$$L_D(h) - L_S(h) \le 2\sqrt{\frac{2d \ln(en/d)}{n}} + \sqrt{\frac{2 \ln(4/\delta)}{n}}.$$
The loss $1 - \ell$ has the same Rademacher complexity, because $-\sigma$ has the same distribution as $\sigma$. So the same bound holds for $L_S(h) - L_D(h)$ with probability $1 - \delta/2$. With probability at least $1 - \delta$, every $h$ then has $|L_D(h) - L_S(h)| \le \varepsilon$ as soon as $n \ge C\,(d \ln(d/\varepsilon) + \ln(1/\delta))/\varepsilon^2$ for an absolute constant $C$. This is uniform convergence. $\blacksquare$

**The sharp sample sizes.** The argument above loses a factor $\ln(d/\varepsilon)$ in the agnostic upper bound. Shalev-Shwartz and Ben-David prove this weaker bound in Section 28.1 and state that the sharp bound $O((d + \ln(1/\delta))/\varepsilon^2)$ needs a finer chaining argument. The realizable upper bound $O((d \ln(1/\varepsilon) + \ln(1/\delta))/\varepsilon)$ comes from the $\varepsilon$-net argument of Section 28.3 (see the [$\varepsilon$-net theorem](/epsilon-net-theorem/)). The lower bounds come from a shattered set of size $d$ with a distribution that is hard to learn, as in the proof of $4 \Rightarrow 6$ (Section 28.2; Ehrenfeucht, Haussler, Kearns and Valiant 1989).

## Consequences

- **ERM is enough.** For binary classes, if anything learns, ERM learns, at the optimal agnostic rate. The design question becomes the choice of class, and the computational cost of ERM over it.
- **Learnability is a property of the class alone.** It does not depend on the distribution, and a class of infinite VC dimension cannot be learned by any learner. Nonuniform learning over a countable union of finite VC classes is the topic of [structural risk minimization](/structural-risk-minimization/).
- **Numbers.** For halfspaces in $\mathbb{R}^{d}$, the VC dimension is $d + 1$, so the agnostic sample size grows linearly with the dimension; dimension free bounds need a margin, see the [margin bound](/margin-generalization-bound/).
- **Generalization gap.** For every $h$ in a class of VC dimension $d$, $L_D(h) \le L_S(h) + O(\sqrt{(d \ln(n/d) + \ln(1/\delta))/n})$ with probability $1 - \delta$ (Mohri, Rostamizadeh and Talwalkar, Corollary 3.19). See [generalization error](/generalization-error/).

## Tightness

- **Realizable rate.** Hanneke (2016) gave an improper learner, a majority vote of ERM outputs on well chosen subsamples, with sample size $O((d + \ln(1/\delta))/\varepsilon)$. With the lower bound of Ehrenfeucht et al., the optimal realizable sample complexity is $\Theta((d + \ln(1/\delta))/\varepsilon)$. Some ERM rules on some classes need the extra factor $\ln(1/\varepsilon)$, so the upper bound of Theorem 6.8 cannot be improved for every ERM rule.
- **Agnostic rate.** The bound $\Theta((d + \ln(1/\delta))/\varepsilon^2)$ is tight up to constants. Mohri, Rostamizadeh and Talwalkar (Theorem 3.23) show that for any learner some distribution forces an excess error above $\sqrt{d/(320n)}$ with probability at least $1/64$.
- **Beyond binary classification.** The equivalences fail in other settings. For general losses there are learnable problems without uniform convergence, where ERM fails (Shalev-Shwartz, Shamir, Srebro and Sridharan 2010). For multiclass labels with an infinite label set, the Natarajan dimension does not decide learnability. For online learning, the Littlestone dimension replaces the VC dimension, and thresholds on $[0, 1]$ have VC dimension 1 but infinite Littlestone dimension.

## History

Vapnik and Chervonenkis (1971) proved that finite VC dimension gives uniform convergence of empirical frequencies to probabilities, uniformly over a class of events. Valiant (1984) defined PAC learning with an emphasis on computation. Blumer, Ehrenfeucht, Haussler and Warmuth (1989) connected the two, and showed that a class is PAC learnable if and only if its VC dimension is finite, with the sample sizes above. Ehrenfeucht, Haussler, Kearns and Valiant (1989) proved the matching lower bound. Haussler (1992) extended the analysis to the agnostic model. The gap of $\ln(1/\varepsilon)$ in the realizable case stayed open until Hanneke (2016). The form with six equivalent conditions is from the textbook of Shalev-Shwartz and Ben-David.

## References
