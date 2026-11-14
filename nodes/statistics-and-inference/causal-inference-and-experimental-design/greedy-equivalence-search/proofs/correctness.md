---
title: GES stops after at most n(n - 1) operators; the Gaussian BIC is score equivalent and, for large N, locally consistent; with these properties and faithfulness the output is the true class by the cited theorem of Chickering (2002)
proves: [correctness, termination]
status: partial
---

**What is proved and what is cited.** This file proves that GES stops, that the Gaussian BIC gives the same score to Markov equivalent DAGs, and that for a large enough sample size it is locally consistent: adding one parent raises the score exactly when the new parent is dependent on the child given the old parents. Two results of Chickering (2002) are cited and not proved: that a valid Insert or Delete gives a class whose score changes by the local formula of lines L5 and L11, and the large-sample optimality theorem, which turns local consistency into the statement that GES returns the true class. The tests check the full claim against exhaustive search over all DAGs on three and four nodes.

**Setting.** The variables are $V$ with $|V| = n$. A score is decomposable when the score of a DAG $D$ is $\sum_{v \in V} s(v, \mathrm{pa}_D(v))$. It is score equivalent when Markov equivalent DAGs have the same score; then the score of a class is the score of any of its DAGs. The Gaussian BIC local score with $N$ samples and covariance matrix $\Sigma$ (positive definite) is

$$s(v, P) = -\frac N2 \log \sigma^2_{v \mid P} - \frac{|P|}{2}\log N, \qquad \sigma^2_{v \mid P} = \Sigma_{vv} - \Sigma_{vP}\Sigma_{PP}^{-1}\Sigma_{Pv}.$$

This is $-\frac12$ times the [BIC](/bayesian-information-criterion/) of the regression of $v$ on $P$, with the terms that do not depend on $P$ dropped.

**Lemma 1 (termination).** GES applies at most $\binom n2$ Insert operators and at most $\binom n2$ Delete operators, and then stops.

*Proof.* An Insert$(X, Y, T)$ needs $X$ and $Y$ non-adjacent. It adds the edge $X \to Y$ and only orients edges between $T$ and $Y$, so the PDAG $h$ of line L7 has the skeleton of the current class plus one edge. A consistent extension of $h$ has the skeleton of $h$, and the CPDAG of a DAG has the skeleton of that DAG. So each Insert adds exactly one edge to the skeleton and removes none. The skeleton has at most $\binom n2$ edges, so the forward phase applies at most $\binom n2$ operators and then finds no valid operator with a positive change, or none at all. In the same way each Delete removes exactly one edge, so the backward phase applies at most as many Delete operators as there are edges. Each step examines finitely many operators. $\square$

The lemma does not need score equivalence or the validity theorem. It also bounds the work: at most $n(n - 1)$ steps, each with at most $n(n - 1)2^{n - 2}$ operators.

**Lemma 2 (two Schur identities).** Let $P \subseteq V$ and $X, Y \notin P$. Then

$$\sigma^2_{X \mid P}\,\sigma^2_{Y \mid P \cup \{X\}} = \frac{\det \Sigma_{P \cup \{X, Y\}}}{\det \Sigma_P} = \sigma^2_{Y \mid P}\,\sigma^2_{X \mid P \cup \{Y\}},$$

and $\sigma^2_{Y \mid P \cup \{X\}} = \sigma^2_{Y \mid P}(1 - \rho^2)$, where $\rho$ is the partial correlation of $X$ and $Y$ given $P$.

*Proof.* For a positive definite block matrix, $\det \Sigma_{Q \cup \{v\}} = \det \Sigma_Q \cdot \sigma^2_{v \mid Q}$, because $\sigma^2_{v \mid Q}$ is the Schur complement of $\Sigma_Q$. Apply this twice: $\det \Sigma_{P \cup \{X, Y\}} = \det \Sigma_{P \cup \{X\}}\,\sigma^2_{Y \mid P \cup \{X\}} = \det \Sigma_P\,\sigma^2_{X \mid P}\,\sigma^2_{Y \mid P \cup \{X\}}$. The other order gives the right side. For the second claim, let $r_X$ and $r_Y$ be the residuals of the regressions of $X$ and $Y$ on $P$. The linear span of $P \cup \{X\}$ is the span of $P$ and $r_X$, and $r_X$ is orthogonal to $P$. So the residual variance of $Y$ on $P \cup \{X\}$ is $\operatorname{Var}(r_Y) - \operatorname{Cov}(r_Y, r_X)^2/\operatorname{Var}(r_X) = \sigma^2_{Y \mid P}(1 - \rho^2)$, with $\rho = \operatorname{Corr}(r_X, r_Y)$. $\square$

**Lemma 3 (score equivalence).** Markov equivalent DAGs have the same Gaussian BIC score, for every $N$ and every positive definite $\Sigma$.

*Proof.* An edge $X \to Y$ of a DAG $D$ is covered when $\mathrm{pa}(Y) = \mathrm{pa}(X) \cup \{X\}$. Reversing a covered edge gives a DAG (a new cycle through $Y \to X$ would need a directed path from $X$ to $Y$ of length at least two, whose last inner node is a parent of $Y$ and so of $X$, which closes a cycle in $D$). We cite the transformational characterization (Chickering 1995, restated in Chickering 2002): two DAGs are Markov equivalent exactly when one is reached from the other by a sequence of covered edge reversals. So it is enough to show that one reversal keeps the score. Let $P = \mathrm{pa}(X)$. Only the families of $X$ and $Y$ change, from $(X, P)$ and $(Y, P \cup \{X\})$ to $(X, P \cup \{Y\})$ and $(Y, P)$. The penalty terms count $|P| + |P| + 1$ parents in both cases. The likelihood terms are $-\frac N2 \log$ of the two products of Lemma 2, which are equal. $\square$

**Lemma 4 (local consistency for large N).** Fix $\Sigma$. There is $N_0$ such that for all $N \ge N_0$, all $Y$, all $P \subseteq V \setminus \{Y\}$ and all $X \notin P \cup \{Y\}$,

$$s(Y, P \cup \{X\}) - s(Y, P) > 0 \iff \rho_{XY \cdot P} \ne 0.$$

*Proof.* By Lemma 2 the change is $\Delta = -\frac N2 \log(1 - \rho^2) - \frac12\log N$. If $\rho = 0$, then $\Delta = -\frac12 \log N < 0$ for $N \ge 2$. If $\rho \ne 0$, then $c = -\log(1 - \rho^2) > 0$ and $\Delta = \frac12(cN - \log N)$, which is positive once $N / \log N > 1/c$. There are finitely many triples $(Y, P, X)$, so one $N_0$ works for all of them. $\square$

For a Gaussian distribution, $\rho_{XY \cdot P} = 0$ exactly when $X \perp Y \mid P$. If the distribution is also faithful to a DAG $G$, this holds exactly when $P$ d-separates $X$ and $Y$ in $G$. So for $N \ge N_0$ the score with the true covariance is decomposable, score equivalent and locally consistent. The tests use the limit of this order as $N \to \infty$ with exact fractions: $\Delta > 0$ exactly when $\sigma^2_{Y \mid P} > \sigma^2_{Y \mid P \cup \{X\}}$, or the two are equal and the change removes a parent.

**Cited results.** Chickering (2002) proves two facts about the operators. First, Insert$(X, Y, T)$ is valid (the result is a class that contains a DAG with $X \to Y$ added) exactly when $\mathrm{NA}_{Y, X} \cup T$ is a clique and every semi-directed path from $Y$ to $X$ meets $\mathrm{NA}_{Y, X} \cup T$, and then the score changes by the formula of line L5; Delete$(X, Y, H)$ is valid exactly when $\mathrm{NA}_{Y, X} \setminus H$ is a clique, and the score changes by the formula of line L11. Second, the optimality theorem: if the score is decomposable, score equivalent and locally consistent for a distribution faithful to a DAG $G$, then the forward phase ends at a class in which every d-separation is an independence of the distribution (an independence map), and the backward phase ends at the class of $G$. Its proof uses the theorem, also in Chickering (2002), that Meek's conjecture holds: if every independence of $D'$ holds in $D$, then $D$ is reached from $D'$ by covered edge reversals and single edge deletions. With Lemmas 3 and 4 this gives: with the true covariance and $N \ge N_0$, GES returns the CPDAG of $G$. With a sample covariance, the score is consistent as $N \to \infty$, and the same theorem gives the true class with probability tending to 1.

**What the tests check.** For every DAG on three and on four nodes (25 and 543 DAGs), with random weights and the exact limit score, GES returns the class of the true DAG and the class of the best of all DAGs found by exhaustive search. With the float BIC at $N = 10^6$, GES returns the best class over all 543 DAGs every time. Lemma 3 is checked exactly with fractions on all 543 DAGs on four nodes, and Lemma 4 with the d-separation oracle.
