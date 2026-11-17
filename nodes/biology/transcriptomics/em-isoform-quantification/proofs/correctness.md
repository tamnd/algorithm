---
title: EM for transcript abundances never lowers the likelihood, and each fixed point with full support is a global maximum
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $m$ transcripts with effective lengths $\ell_t > 0$. The reads are grouped into equivalence classes: a class $e$ is a nonempty set of transcripts and $c_e > 0$ is the number of reads in it. $N = \sum_e c_e$. The parameter $\alpha$ is in the simplex $\Delta = \{\alpha : \alpha_t \ge 0, \sum_t \alpha_t = 1\}$, and $\alpha_t$ is the probability that a read comes from transcript $t$. For a class $e$ let

$$p_e(\alpha) = \sum_{t \in e} \frac{\alpha_t}{\ell_t}, \qquad \log L(\alpha) = \sum_e c_e \log p_e(\alpha).$$

The set $D = \{\alpha \in \Delta : p_e(\alpha) > 0 \text{ for every class } e\}$ is where $\log L$ is finite. One round of lines L3 to L7 maps $\alpha \in D$ to $\alpha' = M(\alpha)$ with

$$r_{e,t} = \frac{\alpha_t / \ell_t}{p_e(\alpha)} \ (t \in e), \qquad n_t = \sum_{e \ni t} c_e\, r_{e,t}, \qquad \alpha'_t = \frac{n_t}{N}.$$

## 1. The iterates are well defined

**Lemma 1.** If $\alpha \in D$, then $\alpha' \in \Delta$, and $\alpha'_t > 0$ for every transcript $t$ that is in some class and has $\alpha_t > 0$. In particular, the iterates that start at the uniform point of line L1 stay in $D$.

*Proof.* For each class, $\sum_{t \in e} r_{e,t} = 1$ by the definition of $p_e$. So $\sum_t n_t = \sum_e c_e = N$ and $\sum_t \alpha'_t = 1$, and all $n_t \ge 0$. If $t \in e$ and $\alpha_t > 0$, then $r_{e,t} > 0$ and $n_t \ge c_e r_{e,t} > 0$. The uniform start has $\alpha_t = 1/m > 0$ for all $t$, so after each round every transcript that is in a class keeps a positive value, by induction. Each class holds at least one transcript, so $p_e > 0$ for every class, and the next iterate is in $D$. $\square$

## 2. The likelihood never decreases

**Lemma 2.** For $\alpha \in D$ and every $\beta \in \Delta$ with $\beta_t > 0$ wherever $n_t > 0$,

$$\log L(\beta) - \log L(\alpha) \ \ge\ \sum_{t : n_t > 0} n_t \log \frac{\beta_t}{\alpha_t}.$$

*Proof.* Fix a class $e$. Only the members $t \in e$ with $\alpha_t > 0$ have $r_{e,t} > 0$, and these weights sum to 1. Then

$$\frac{p_e(\beta)}{p_e(\alpha)} \ \ge\ \sum_{t \in e,\ \alpha_t > 0} \frac{\beta_t/\ell_t}{p_e(\alpha)} = \sum_{t \in e,\ \alpha_t > 0} r_{e,t}\, \frac{\beta_t}{\alpha_t}.$$

The logarithm is concave, so by Jensen's inequality the log of this weighted mean is at least the weighted mean of the logs:

$$\log p_e(\beta) - \log p_e(\alpha) \ \ge\ \sum_{t \in e,\ \alpha_t > 0} r_{e,t} \log \frac{\beta_t}{\alpha_t}.$$

Multiply by $c_e$ and add over all classes. The coefficient of $\log(\beta_t / \alpha_t)$ is $\sum_{e \ni t} c_e r_{e,t} = n_t$. $\square$

**Theorem 1 (monotonicity).** For $\alpha \in D$ and $\alpha' = M(\alpha)$,

$$\log L(\alpha') - \log L(\alpha) \ \ge\ N \cdot \mathrm{KL}(\alpha' \,\|\, \alpha) \ \ge\ 0,$$

with equality only if $\alpha' = \alpha$.

*Proof.* Put $\beta = \alpha'$ in Lemma 2. Then $\beta_t = n_t / N > 0$ wherever $n_t > 0$, and $n_t = N \alpha'_t$, so the right side is $N \sum_t \alpha'_t \log(\alpha'_t / \alpha_t) = N \cdot \mathrm{KL}(\alpha' \| \alpha)$, with $0 \log 0 = 0$. The Kullback-Leibler divergence of two distributions is at least 0 and is 0 only when they are equal (Gibbs' inequality). $\square$

Lemma 2 also explains line L7. For fixed counts $n_t$, the function $\beta \mapsto \sum_t n_t \log \beta_t$ on $\Delta$ is largest at $\beta_t = n_t / N$, again by Gibbs' inequality. So line L7 maximizes the lower bound of Lemma 2, which is the M step of the EM algorithm, and the E step is the computation of the $r_{e,t}$ in lines L5 and L6.

The values $\log L(\alpha^{(k)})$ form a nondecreasing sequence. They are bounded above, because $p_e(\alpha) \le \max_t 1/\ell_t$ for all $\alpha \in \Delta$. So the sequence of likelihood values converges. This proof does not show that the iterates themselves converge, and line L8 is a practical stopping rule, not part of the theory.

## 3. A fixed point with full support is a global maximum

**Theorem 2.** $\log L$ is concave on $D$. If $\alpha \in D$ is a fixed point, $M(\alpha) = \alpha$, and $\alpha_t > 0$ for every $t$, then $\log L(\alpha) \ge \log L(\beta)$ for every $\beta \in \Delta$.

*Proof.* Each $p_e$ is a linear function of $\alpha$, and $\log$ is concave and increasing, so each $c_e \log p_e$ is concave on the convex set $D$, and so is their sum.

The partial derivatives at $\alpha \in D$ are

$$g_t = \frac{\partial \log L}{\partial \alpha_t} = \sum_{e \ni t} \frac{c_e}{\ell_t\, p_e(\alpha)}, \qquad \text{so} \qquad \alpha_t g_t = \sum_{e \ni t} c_e r_{e,t} = n_t.$$

At a fixed point, $n_t = N \alpha_t$ for all $t$. Where $\alpha_t > 0$ this gives $g_t = N$. With full support, $g_t = N$ for all $t$.

Take $\beta \in D$. A concave differentiable function lies below its tangent plane, so

$$\log L(\beta) \ \le\ \log L(\alpha) + \sum_t g_t (\beta_t - \alpha_t) = \log L(\alpha) + N \Big(\sum_t \beta_t - \sum_t \alpha_t\Big) = \log L(\alpha).$$

For $\beta \in \Delta \setminus D$ some $p_e(\beta) = 0$ and $\log L(\beta) = -\infty$. $\square$

## 4. What is not true

**Fixed points with a zero can be poor.** Take three transcripts of the same length $\ell$, and the classes $\{1, 2\}$ and $\{1, 3\}$ with 10 reads each. At $\alpha = (0, \tfrac12, \tfrac12)$ the counts are $n = (0, 10, 10)$, so $M(\alpha) = \alpha$. But $\log L(0, \tfrac12, \tfrac12) = 20 \log \frac{1}{2\ell}$ and $\log L(1, 0, 0) = 20 \log \frac1\ell$, which is larger. A zero never becomes positive again in line L6, so EM cannot leave this point. This is why line L1 starts with every $\alpha_t > 0$. Theorem 2 needs full support at the fixed point, and a limit of EM can still have zeros.

**The maximum need not be unique.** If two transcripts $u$ and $v$ have $\ell_u = \ell_v$ and are in exactly the same classes, then $p_e$ depends only on $\alpha_u + \alpha_v$. Every split of that sum gives the same likelihood, so the maxima form a segment. The concavity of Theorem 2 is not strict, and EM returns the split that its start point gives. Li, Ruotti, Stewart, Thomson and Dewey (2010) describe this case as a plateau of the likelihood surface. $\blacksquare$
