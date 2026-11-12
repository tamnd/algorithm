---
tag: 3MG65J
kind: concept
slug: rademacher-complexity
name: Rademacher complexity
aliases:
- Rademacher average
- empirical Rademacher complexity
area: machine-learning/supervised-learning
level: research
summary: "How well a function class correlates with random signs on the sample. Twice it, plus a confidence term, bounds the generalization gap of every function in the class."
prereqs: [agnostic-pac-learning, hoeffding-inequality, azuma-inequality]
see_also: [vc-dimension, sauer-shelah-lemma, margin-generalization-bound, structural-risk-minimization, fundamental-theorem-of-statistical-learning, generalization-error, support-vector-machine, jensens-inequality]
sources:
  - paper: "P. L. Bartlett and S. Mendelson, Rademacher and Gaussian complexities: risk bounds and structural results, Journal of Machine Learning Research 3, 2002"
    locator: pp. 463 to 482
  - paper: doi:10.1109/18.930926
    title: V. Koltchinskii, Rademacher penalties and structural risk minimization, IEEE Transactions on Information Theory 47(5), 2001
    locator: pp. 1902 to 1914
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Chapter 26 (Definition 26.1, Lemma 26.2, Theorem 26.5, Lemma 26.7, Lemma 26.8 Massart, Lemma 26.9 contraction, Lemma 26.10 linear classes, Theorem 26.12)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Section 3.1 (Definitions and Theorem 3.3), Theorem 3.5 (binary classification), Theorem 3.7 (Massart's lemma), Lemma 5.7 (Talagrand's contraction lemma)
  - book: isbn:9783540520139
    title: Michel Ledoux and Michel Talagrand, Probability in Banach Spaces, Springer, 1991
    locator: Chapter 4 (the contraction principle for Rademacher averages)
---

The Rademacher complexity of a class of functions measures how well the class can fit random noise on a sample. Draw independent random signs $\sigma_1, \ldots, \sigma_n \in \{-1, +1\}$, one per example, and ask how large the correlation $\frac{1}{n}\sum_i \sigma_i f(z_i)$ can be made by the best $f$ in the class; the expected value of this maximum is the empirical Rademacher complexity. Koltchinskii (2001) and Bartlett and Mendelson (2002) made it a standard tool of learning theory. With probability $1 - \delta$, every function in a class with values in $[0, 1]$ has true mean at most its sample mean plus twice the Rademacher complexity plus $O(\sqrt{\ln(1/\delta)/n})$. Unlike the [VC dimension](/vc-dimension/), it depends on the data, it applies to real valued classes, and it gives dimension free bounds for norm bounded linear predictors.

## In plain words

Take your training examples and give each one a random label, plus or minus, by coin flips. Now ask the family of models to agree with these random labels as much as it can. A simple family cannot agree with noise much better than chance. A rich family can follow almost any pattern of coin flips. Do this for many fresh rounds of coin flips and take the average agreement. That average is the Rademacher complexity. If the family can fit noise well, a good fit to the real labels is weak evidence; if it cannot, a good fit is strong evidence that the model will work on new data.

## The idea

**Definitions.** Let $A \subseteq \mathbb{R}^n$ be a set of vectors and let $\sigma$ be uniform on $\{-1, +1\}^n$. Define
$$R(A) = \mathbb{E}_\sigma\Big[\sup_{a \in A} \frac{1}{n} \sum_{i=1}^n \sigma_i a_i\Big].$$
For a class $F$ of functions $Z \to \mathbb{R}$ and a sample $S = (z_1, \ldots, z_n)$, the **empirical Rademacher complexity** is $\hat R_S(F) = R(F \circ S)$ with $F \circ S = \{(f(z_1), \ldots, f(z_n)) : f \in F\}$. The **Rademacher complexity** is its expectation over samples of size $n$ from $D$: $R_n(F) = \mathbb{E}_{S \sim D^n}[\hat R_S(F)]$. This is the form of Shalev-Shwartz and Ben-David (Definition 26.1) and of Mohri, Rostamizadeh and Talwalkar (Section 3.1). Some authors, Bartlett and Mendelson among them, put an absolute value inside the supremum or a factor 2 in front; the bounds then change by constants.

For learning, $F$ is the loss class $\ell \circ H = \{z \mapsto \ell(h, z) : h \in H\}$. For binary classification with labels in $\{-1, +1\}$ and the 0-1 loss, $\hat R_S(\ell \circ H) = \frac{1}{2}\hat R_S(H)$ (Mohri, Rostamizadeh and Talwalkar, Lemma 3.4).

**The generalization bound.** Let $F$ map into $[0, 1]$. With probability at least $1 - \delta$ over $S$, for every $f \in F$,
$$\mathbb{E}_D[f] \le \frac{1}{n}\sum_{i=1}^n f(z_i) + 2R_n(F) + \sqrt{\frac{\ln(1/\delta)}{2n}},$$
$$\mathbb{E}_D[f] \le \frac{1}{n}\sum_{i=1}^n f(z_i) + 2\hat R_S(F) + 3\sqrt{\frac{\ln(2/\delta)}{2n}}.$$
This is Theorem 3.3 of Mohri, Rostamizadeh and Talwalkar; Theorem 26.5 of Shalev-Shwartz and Ben-David has the same form with other constants. The second line uses only the sample, so it can be computed.

*Proof sketch.* Let $\Phi(S) = \sup_{f \in F} (\mathbb{E}_D[f] - \hat{\mathbb{E}}_S[f])$. Changing one example changes $\Phi$ by at most $1/n$, so by McDiarmid's bounded difference inequality (a form of the [Azuma inequality](/azuma-inequality/)), $\Phi(S) \le \mathbb{E}[\Phi] + \sqrt{\ln(1/\delta)/(2n)}$ with probability $1 - \delta$. To bound $\mathbb{E}[\Phi]$, draw a ghost sample $S'$ of the same size. Then $\mathbb{E}_D[f] = \mathbb{E}_{S'}[\hat{\mathbb{E}}_{S'} f]$, and moving the supremum inside the expectation gives
$$\mathbb{E}[\Phi] \le \mathbb{E}_{S, S'}\Big[\sup_f \frac{1}{n}\sum_i (f(z'_i) - f(z_i))\Big] = \mathbb{E}_{S, S', \sigma}\Big[\sup_f \frac{1}{n}\sum_i \sigma_i (f(z'_i) - f(z_i))\Big] \le 2R_n(F).$$
The equality holds because swapping $z_i$ and $z'_i$ does not change the distribution, and a sign $\sigma_i = -1$ is such a swap. The last step splits the supremum of a sum into two suprema. For the second line, apply McDiarmid once more to $\hat R_S(F)$, which also changes by at most $1/n$, and split $\delta$ in two. $\blacksquare$

**Tools to bound it.**

- **Massart's lemma.** If $A$ is finite with $N$ vectors, then $R(A) \le \max_{a \in A} \|a - \bar a\|_2 \sqrt{2 \ln N}/n$, where $\bar a$ is the mean of $A$ (Shalev-Shwartz and Ben-David, Lemma 26.8; Mohri et al., Theorem 3.7 without the centering). For a binary class of VC dimension $d$, the [Sauer-Shelah lemma](/sauer-shelah-lemma/) gives $N \le (en/d)^d$, so $\hat R_S(H) \le \sqrt{2d \ln(en/d)/n}$.
- **Contraction.** If each $\varphi_i : \mathbb{R} \to \mathbb{R}$ is $\rho$-Lipschitz, then $R(\{(\varphi_1(a_1), \ldots, \varphi_n(a_n)) : a \in A\}) \le \rho R(A)$ (Shalev-Shwartz and Ben-David, Lemma 26.9; Mohri et al., Lemma 5.7, Talagrand's lemma; the principle goes back to Ledoux and Talagrand). It moves a bound from a class of scores to the class of their Lipschitz losses, such as the [hinge loss](/hinge-loss/) or the ramp loss.
- **Convex hulls.** $R(\mathrm{conv}(A)) = R(A)$, because a linear function of $a$ takes its maximum over a convex hull at a vertex (Lemma 26.7). This is why voting classifiers, such as [AdaBoost](/adaboost/) outputs, are no more complex than their base class.
- **Linear classes.** For $H = \{x \mapsto \langle w, x \rangle : \|w\|_2 \le B\}$ and points with $\|x_i\|_2 \le r$, $\hat R_S(H) \le B\sqrt{\sum_i \|x_i\|^2}/n \le Br/\sqrt{n}$ (Lemma 26.10). *Proof.* The supremum of $\frac{1}{n}\langle w, \sum_i \sigma_i x_i\rangle$ over $\|w\| \le B$ is $\frac{B}{n}\|\sum_i \sigma_i x_i\|$, and by [Jensen's inequality](/jensens-inequality/), $\mathbb{E}\|\sum_i \sigma_i x_i\| \le \sqrt{\mathbb{E}\|\sum_i \sigma_i x_i\|^2} = \sqrt{\sum_i \|x_i\|^2}$, because the cross terms have mean zero. $\blacksquare$ The bound has no dimension in it.

**Computing it.** For a finite set $A$, $R(A)$ is an average over $2^n$ sign vectors, so exact computation is practical only for small $n$. A Monte Carlo estimate is unbiased and simple:

```pseudo id=main
RADEMACHER-MC(A, T)                           ▷ A ⊆ ℝ^n finite, T independent draws
L1  total ← 0
L2  repeat T times
L3      draw σ uniformly from {−1, +1}^n
L4      total ← total + max_{a ∈ A} (1/n) Σ_{i=1..n} σ_i a_i
L5  return total / T
```

Each draw lies in $[-r, r]$ with $r = \max_{a} \frac{1}{n}\sum_i |a_i|$, so by [Hoeffding's inequality](/hoeffding-inequality/) the estimate is within $2r\sqrt{\ln(2/\delta)/(2T)}$ of $R(A)$ with probability $1 - \delta$. Each draw costs one maximization over $A$, which for an infinite class is an ERM problem with the labels $\sigma_i$. So for classes where ERM is hard, the empirical Rademacher complexity is hard to compute as well.

## Examples

**Small sets.** Exact values by enumeration over all sign vectors:

| $A$ | $n$ | $R(A)$ |
|---|---|---|
| one vector | any | 0 |
| all of $\{-1, +1\}^4$ | 4 | 1 |
| $\{(1,1,1,1), (-1,-1,-1,-1)\}$ | 4 | $3/8$ |

A single vector has $R = 0$ because $\mathbb{E}[\sigma_i] = 0$. The full cube fits every sign vector exactly. For the two constant vectors, $R = \mathbb{E}|\sigma_1 + \cdots + \sigma_4|/4 = 1.5/4$.

**Thresholds.** Let the points be $n$ distinct reals and $H = \{x \mapsto \mathrm{sign}(x - t)\}$ with values in $\{-1, +1\}$. On sorted points, $H \circ S$ has the $n + 1$ vectors that are $-1$ on a prefix and $+1$ on the rest. Exact values:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|---|---|
| $\hat R_S(H)$ | 1 | 3/4 | 2/3 | 19/32 | 11/20 | 49/96 | 467/1024 | 1067/2560 |

For $n = 10$ the value is about $0.4168$, and Massart's lemma gives the upper bound $0.781$. A Monte Carlo estimate with 1000 draws (seed 1) gives $0.4192$, inside the Hoeffding tolerance $0.0859$ for $\delta = 0.05$; with 100000 draws it gives $0.41656$.

**Contraction, checked.** The implementation checks on random finite sets that the ramp function $t \mapsto \min(1, \max(0, 1 - t))$, which is 1-Lipschitz, does not increase $R$, and that $t \mapsto 2t$ multiplies $R$ by exactly 2. It also checks the linear class bound $\mathbb{E}\|\sum_i \sigma_i x_i\|/n \le \sqrt{\sum_i \|x_i\|^2}/n \le r/\sqrt{n}$, and Massart's lemma on random sets.

## Where it is used

- **Margin bounds.** Contraction with the ramp loss and the linear class bound give the bound $L_D(h) \le \hat L_{S,\gamma}(h) + 2r/(\gamma\sqrt{n}) + O(\sqrt{\ln(1/\delta)/n})$ for linear predictors of norm at most 1 and margin $\gamma$, with no dependence on the dimension. See the [margin bound](/margin-generalization-bound/) and the [support vector machine](/support-vector-machine/).
- **Boosting and voting.** The convex hull rule bounds the complexity of weighted votes of base classifiers by that of the base class, which explains why [boosting](/boosting/) can keep improving the margin without overfitting.
- **Model selection.** Koltchinskii (2001) used the empirical Rademacher complexity as a data dependent penalty in [structural risk minimization](/structural-risk-minimization/).
- **Binary classes.** With Massart's lemma and the Sauer-Shelah lemma, it gives the uniform convergence step in the proof of the [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/).
- **Kernels and neural networks.** For kernel classes the linear bound holds in feature space with $r^2 = \max_i K(x_i, x_i)$. For networks, bounds in terms of products of weight norms are proved by peeling one layer at a time with contraction.
- **Local Rademacher complexity.** Restricting the supremum to functions with small variance gives faster rates of order $1/n$ in favourable cases, an extension due to Bartlett, Bousquet and Mendelson and to Koltchinskii.

## References
