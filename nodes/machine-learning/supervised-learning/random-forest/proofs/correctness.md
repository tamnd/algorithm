---
title: The strength and correlation bound of random forests, and the out-of-bag estimate
proves: [correctness]
status: full
---

We use the notation of Breiman (2001), Section 2. A tree is $h(x, \Theta)$, where the random vector $\Theta$ holds all the random choices of one tree: its bootstrap sample and its feature draws. The trees of a forest use independent copies of $\Theta$ with the same distribution. The pair $(X, Y)$ is a random example, independent of $\Theta$. Probabilities and expectations over $\Theta$ are written $P_\Theta$ and $\mathbb{E}_\Theta$, and those over $(X, Y)$ are written $P_{X,Y}$ and $\mathbb{E}_{X,Y}$. The training set is fixed throughout.

### Definitions

The margin of the forest in the limit of many trees is

$$mr(X, Y) = P_\Theta(h(X, \Theta) = Y) - \max_{j \ne Y} P_\Theta(h(X, \Theta) = j).$$

The forest classifies $(X, Y)$ correctly exactly when $mr(X, Y) > 0$, and its generalization error is $PE^* = P_{X,Y}(mr(X, Y) < 0)$. The strength is $s = \mathbb{E}_{X,Y}\, mr(X, Y)$.

Let $\hat\jmath(X, Y) = \arg\max_{j \ne Y} P_\Theta(h(X, \Theta) = j)$, with a fixed rule for ties. The raw margin of one tree is

$$rmg(\Theta, X, Y) = I(h(X, \Theta) = Y) - I(h(X, \Theta) = \hat\jmath(X, Y)).$$

Its values are in $\{-1, 0, 1\}$, and $mr(X, Y) = \mathbb{E}_\Theta\, rmg(\Theta, X, Y)$, because $\hat\jmath$ depends only on $(X, Y)$.

For fixed $\Theta$, let $sd(\Theta)$ be the standard deviation of $rmg(\Theta, X, Y)$ over $(X, Y)$, and $\mathrm{var}(\Theta) = sd(\Theta)^2$. For fixed $\Theta$ and $\Theta'$, let $\rho(\Theta, \Theta')$ be the correlation of $rmg(\Theta, X, Y)$ and $rmg(\Theta', X, Y)$ over $(X, Y)$, so that $\rho(\Theta, \Theta')\, sd(\Theta)\, sd(\Theta')$ is their covariance (we take the product to be this covariance, which is 0, when a standard deviation is 0). The mean correlation is

$$\bar\rho = \frac{\mathbb{E}_{\Theta, \Theta'}[\rho(\Theta, \Theta')\, sd(\Theta)\, sd(\Theta')]}{\mathbb{E}_{\Theta, \Theta'}[sd(\Theta)\, sd(\Theta')]},$$

where $\Theta$ and $\Theta'$ are independent with the same distribution.

### Theorem (Breiman 2001, Theorem 2.3)

If $s > 0$, then

$$PE^* \le \frac{\bar\rho\,(1 - s^2)}{s^2}.$$

### Proof

**Step 1: the variance of the margin.** Let $\Theta'$ be an independent copy of $\Theta$. For fixed $(x, y)$,

$$mr(x, y)^2 = \left(\mathbb{E}_\Theta\, rmg(\Theta, x, y)\right)\left(\mathbb{E}_{\Theta'}\, rmg(\Theta', x, y)\right) = \mathbb{E}_{\Theta, \Theta'}[rmg(\Theta, x, y)\, rmg(\Theta', x, y)],$$

by independence. Also $s^2 = \mathbb{E}_{\Theta, \Theta'}\left[\mathbb{E}_{X,Y} rmg(\Theta, X, Y)\; \mathbb{E}_{X,Y} rmg(\Theta', X, Y)\right]$, since both factors have mean $s$ over $\Theta$ and they are independent. Subtract and exchange the order of the expectations (all quantities are bounded):

$$\mathrm{var}_{X,Y}(mr) = \mathbb{E}_{X,Y}[mr^2] - s^2 = \mathbb{E}_{\Theta, \Theta'}\left[\mathrm{cov}_{X,Y}\big(rmg(\Theta, X, Y), rmg(\Theta', X, Y)\big)\right] = \mathbb{E}_{\Theta, \Theta'}[\rho(\Theta, \Theta')\, sd(\Theta)\, sd(\Theta')].$$

**Step 2: the mean correlation.** By the definition of $\bar\rho$ and the independence of $\Theta$ and $\Theta'$,

$$\mathrm{var}(mr) = \bar\rho\; \mathbb{E}_{\Theta, \Theta'}[sd(\Theta)\, sd(\Theta')] = \bar\rho\, \left(\mathbb{E}_\Theta\, sd(\Theta)\right)^2.$$

If $\mathbb{E}_\Theta\, sd(\Theta) = 0$, both sides are 0 and $\bar\rho$ can be taken as 0. Since $\mathrm{var}(mr) \ge 0$, also $\bar\rho \ge 0$ whenever it is defined.

**Step 3: Jensen's inequality.** The square is convex, so $(\mathbb{E}_\Theta\, sd(\Theta))^2 \le \mathbb{E}_\Theta\, sd(\Theta)^2 = \mathbb{E}_\Theta\, \mathrm{var}(\Theta)$. With $\bar\rho \ge 0$,

$$\mathrm{var}(mr) \le \bar\rho\; \mathbb{E}_\Theta\, \mathrm{var}(\Theta).$$

**Step 4: the bound on the mean variance.** For fixed $\Theta$, $\mathrm{var}(\Theta) = \mathbb{E}_{X,Y}[rmg^2] - (\mathbb{E}_{X,Y}\, rmg)^2 \le 1 - (\mathbb{E}_{X,Y}\, rmg(\Theta, X, Y))^2$, because $rmg^2 \le 1$. Take $\mathbb{E}_\Theta$ and use Jensen's inequality again, $\mathbb{E}_\Theta[Z^2] \ge (\mathbb{E}_\Theta Z)^2$ with $Z = \mathbb{E}_{X,Y}\, rmg(\Theta, X, Y)$, whose mean is $s$:

$$\mathbb{E}_\Theta\, \mathrm{var}(\Theta) \le 1 - \mathbb{E}_\Theta[Z^2] \le 1 - s^2.$$

**Step 5: Chebyshev's inequality.** If $mr < 0$ and $s > 0$, then $mr - s < -s$, so $|mr - s| > s$. By [Chebyshev's inequality](/chebyshev-inequality/),

$$PE^* = P_{X,Y}(mr < 0) \le P_{X,Y}(|mr - s| \ge s) \le \frac{\mathrm{var}(mr)}{s^2}.$$

Steps 3 and 4 give $\mathrm{var}(mr) \le \bar\rho\,(1 - s^2)$, and the theorem follows. $\square$

**Remarks.** The proof uses no property of trees, so the bound holds for any randomized classifier $h(x, \Theta)$. It also holds when $\Theta$ is uniform over a finite set of trees and $(X, Y)$ is uniform over a finite set of examples: the tests check each step on such finite distributions, where all expectations are exact averages. The bound is loose, but it shows the two levers: a larger strength $s$ and a smaller correlation $\bar\rho$ both lower it.

### The forest converges as trees are added

For a fixed $(x, y)$ and label $j$, the fraction of the first $B$ trees with $h(x, \Theta_b) = j$ is an average of $B$ independent indicators, so by the strong [law of large numbers](/law-of-large-numbers/) it converges almost surely to $P_\Theta(h(x, \Theta) = j)$. Breiman (2001, Theorem 1.2) uses this, together with the fact that a tree can take only finitely many forms on a finite training set, to show that the generalization error of the forest converges almost surely to $PE^*$ as $B \to \infty$. So adding trees does not make the forest overfit; it only reduces the random part of its error.

### The out-of-bag estimate uses no tree that saw the example

Line L10 votes over the trees $b$ with $i \notin S_b$. Each such tree is a function of its bootstrap sample $S_b$ and its feature draws only, and $S_b$ does not contain example $i$. So, given the other examples, these trees are independent of $(x_i, y_i)$, and their vote on $x_i$ is a prediction on an example that none of them was trained on. This is the property that the OOB error of line L11 relies on: it is a held-out estimate for a forest of about $B / e$ trees, since each tree leaves out row $i$ with probability $(1 - 1/n)^n \le 1/e$.
