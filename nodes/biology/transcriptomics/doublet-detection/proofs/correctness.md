---
title: The Scrublet score is the Bayes posterior of a doublet under a neighbor density model, and homotypic doublets cannot be told apart by profile
proves: [correctness]
status: full
---

Doublet detection has no exact answer, so there is no theorem that the method finds the doublets. We prove what the score means. Theorem 1 shows that line L8 is Bayes' rule with the prior $\rho$, when the neighbors at a point estimate the density of singlets and of doublets there. Lemma 2 gives its range and shape, and Lemma 3 explains the choice of $k_{adj}$. Lemma 4 shows a limit that holds for every method of this kind: after the normalization of line L2, a doublet of two cells of one type has the same expected profile as a singlet of that type. That the neighbor counts estimate the densities, and that simulated doublets look like real ones, are assumptions; the tests measure how well the scores separate doublets on simulated data.

**Setting.** There are $n$ observed profiles and $rn$ simulated doublets (line L1), and each profile has $k_{adj}$ nearest neighbors among all $(1 + r)n$ profiles (line L6). For one profile, $n_d$ of its neighbors are simulated. Line L7 sets $q = (n_d + 1)/(k_{adj} + 2)$ and line L8 sets
$$S(q) = \frac{q\rho/r}{1 - \rho - q(1 - \rho - \rho/r)}, \qquad 0 < \rho < 1, \; r > 0.$$

**Density model.** Near a point $x$ of the embedding, let $f_s(x)$ be the density of singlets and $f_d(x)$ the density of doublets, both normalized to integrate to 1. A real cell is a doublet with prior probability $\rho$. The model treats the $n$ observed profiles as singlets, so near $x$ they occur at a rate proportional to $n f_s(x)$, and the simulated doublets at a rate proportional to $rn f_d(x)$. The fraction $q$ then estimates $rf_d/(rf_d + f_s)$, and $(n_d + 1)/(k_{adj} + 2)$ is the Laplace estimate of that fraction: the posterior mean of a binomial proportion with a uniform prior.

**Theorem 1 (the score is a posterior).** Suppose $q = rf_d/(rf_d + f_s)$ with $f_s > 0$. Then
$$S(q) = \frac{\rho f_d}{\rho f_d + (1 - \rho)f_s},$$
which is the probability, by [Bayes' theorem](/bayes-theorem/), that a real cell at $x$ is a doublet.

*Proof.* From $q(rf_d + f_s) = rf_d$ we get $f_d/f_s = q/(r(1 - q))$, and $q < 1$ since $f_s > 0$. Divide the numerator and the denominator of the right side by $f_s$:
$$\frac{\rho f_d}{\rho f_d + (1 - \rho)f_s} = \frac{\rho q/(r(1 - q))}{\rho q/(r(1 - q)) + 1 - \rho} = \frac{\rho q/r}{\rho q/r + (1 - \rho)(1 - q)}.$$
The denominator is $\rho q/r + 1 - \rho - q + \rho q = 1 - \rho - q(1 - \rho - \rho/r)$, which is the denominator of $S(q)$. $\square$

The model is an approximation in one place: a fraction $\rho$ of the observed profiles are doublets, so the observed profiles occur at a rate proportional to $(1 - \rho)f_s + \rho f_d$, not $f_s$. Where $f_d > f_s$, which is where the doublets are, this rate is above $f_s$, so $q$ is smaller and the score is lower than the exact posterior. Where $f_d < f_s$ the score is a little higher.

**Lemma 2 (range and shape).** For $q \in (0, 1)$, $S(q) \in (0, 1)$ and $S$ is strictly increasing. At $q = r/(1 + r)$, the fraction of simulated profiles among all profiles, $S(q) = \rho$.

*Proof.* Write $S(q) = A/(A + B)$ with $A = \rho q/r > 0$ and $B = (1 - \rho)(1 - q) > 0$, from the proof of Theorem 1. So $0 < S < 1$. As $q$ grows, $A$ grows and $B$ falls, so $A/(A + B) = 1/(1 + B/A)$ grows strictly. At $q = r/(1 + r)$, $A = \rho/(1 + r)$ and $B = (1 - \rho)/(1 + r)$, so $S = \rho$. $\square$

So a cell whose neighborhood has the same mix as the whole data gets the prior, and the score moves away from the prior only when the neighborhood holds more or fewer simulated doublets than the global share. Because $q$ is never 0 or 1, the score is never 0 or 1.

**Lemma 3 (the adjusted neighbor count).** If the neighbors of a profile have the global mix, the expected number of observed neighbors among the $k_{adj} = k(1 + r)$ is $k$.

*Proof.* The global share of observed profiles is $n/((1 + r)n) = 1/(1 + r)$, and $k(1 + r) \cdot 1/(1 + r) = k$. $\square$

Line L5 rounds $k(1 + r)$ to an integer, so the statement holds up to rounding. The aim is that the resolution of the neighborhood among the real cells does not depend on how many doublets are simulated.

**Lemma 4 (homotypic doublets).** Let cells $a$ and $b$ have expected counts $E[x_a] = s_a\mu$ and $E[x_b] = s_b\mu$ with the same profile $\mu$ and any sizes $s_a, s_b > 0$. Then the expected doublet $E[x_a + x_b] = (s_a + s_b)\mu$ is a multiple of $\mu$, and after scaling to a fixed total at line L2 it equals the scaled expected singlet of the type.

*Proof.* $E[x_a + x_b] = E[x_a] + E[x_b] = (s_a + s_b)\mu$. Scaling to the total $T$ maps any positive multiple $c\mu$ to $T\mu/\sum_g\mu_g$, the same vector for every $c > 0$. $\square$

So the normalized profile of a homotypic doublet differs from a singlet of its type only by noise. The doublet has about twice the counts, so its noise is smaller, but its position in the embedding is the same in expectation. Scrublet, and every method that works on normalized profiles, finds mainly heterotypic doublets, of two different types, whose expected profile $s_a\mu_a + s_b\mu_b$ lies between two types where few singlets are.

**What the lines compute.** Line L1 draws the pairs with replacement, as Scrublet does. Lines L2 to L4 apply the same scaling, the same gene means and standard deviations, and the same principal axes to the observed and the simulated profiles, so that both are in one space; the axes are fitted on the observed cells only. Lines L5 to L8 compute $k_{adj}$, $n_d$, $q$ and $S(q)$. Line L9 takes the valley of the smoothed histogram of the simulated scores, which have one mode near the prior (homotypic simulated doublets) and one high mode (heterotypic ones). Line L10 compares each observed score with it.

**Complexity.** With $d$ genes, $p$ components and a fixed $r$, lines L1 to L3 take $O(nd)$ time, the covariance at line L4 takes $O(nd^2)$, the eigendecomposition $O(d^3)$ per Jacobi sweep, and the projection $O(ndp)$. The brute-force neighbor search at line L6 takes $O(n^2(p + \log n))$, which is the largest term for many cells; Scrublet uses an approximate search there.

**What the tests check.** The test file checks Theorem 1 against Bayes' rule written with the two densities, for many values of $\rho$, $r$, $k_{adj}$ and $n_d$, and Lemma 2 for the monotone shape, the range and the value $\rho$ at the global mix. It checks the adjusted $k$, the doublet sums and their draw order, the scaling, the threshold on a bimodal sample, and that a seed gives the same scores. For the group module it checks the neighbor search against sorting, the linear solver, the Jacobi eigenvectors and the Poisson draws. One simulation with three cell types measures how well heterotypic doublets are found and that homotypic doublets are not; this is a measurement, not a theorem.
