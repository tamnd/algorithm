---
title: The forward-backward recursions give the MMI objective and its exact gradient
proves: [correctness]
status: full
---

We use the notation of the page. A graph $G$ has emitting states $j$ with pdf ids $\mathrm{pdf}(j)$, arcs $i \to j$ with log weights $w(i, j)$, initial log weights $\mathrm{init}(j)$ and final log weights $\mathrm{final}(j)$; a missing weight is $-\infty$. The frames are $t = 1, \ldots, T$ and $\ell_t(p)$ is the log likelihood of pdf $p$ at frame $t$. A path is a state sequence $q = q_1 \ldots q_T$ (parallel arcs count as different paths), and its score is

$$s(q) = \mathrm{init}(q_1) + \sum_{t=2}^{T} w(q_{t-1}, q_t) + \mathrm{final}(q_T) + \kappa \sum_{t=1}^{T} \ell_t(\mathrm{pdf}(q_t)).$$

Let $Z_G = \sum_q e^{s(q)}$ over the paths of $G$. The proofs use probabilities; $\oplus$ in log space is $+$ on probabilities, and the code stores logs.

**Lemma 1 (forward).** After lines L2 and L3, $e^{\alpha_t(j)}$ is the sum of $e^{\mathrm{init}(q_1) + \sum_{\tau=2}^{t} w(q_{\tau-1}, q_\tau) + \kappa \sum_{\tau=1}^{t} \ell_\tau(\mathrm{pdf}(q_\tau))}$ over the partial paths $q_1 \ldots q_t$ with $q_t = j$, and the value of line L3 is $\ln Z_G$.

*Proof.* By induction on $t$. For $t = 1$ the only partial path is $j$, and line L2 sets $\alpha_1(j) = \mathrm{init}(j) + \kappa \ell_1(\mathrm{pdf}(j))$. For $t \ge 2$, a partial path that ends in $j$ is a partial path of length $t - 1$ that ends in some $i$, followed by an arc $i \to j$. Its weight is the weight of the shorter path times $e^{w(i, j)}$ times $e^{\kappa \ell_t(\mathrm{pdf}(j))}$. Summing over $i$ and the arcs gives the recursion of line L2 by distributivity. A full path is a partial path of length $T$ times its final weight, so line L3 sums $e^{s(q)}$ over all paths. $\square$

**Lemma 2 (backward).** After line L4, $e^{\beta_t(i)}$ is the sum of $e^{\sum_{\tau=t+1}^{T} (w(q_{\tau-1}, q_\tau) + \kappa \ell_\tau(\mathrm{pdf}(q_\tau))) + \mathrm{final}(q_T)}$ over the suffixes $q_{t+1} \ldots q_T$ that follow $q_t = i$.

*Proof.* By induction downwards from $t = T$, where the only suffix is empty and $\beta_T(i) = \mathrm{final}(i)$. A suffix after $i$ at frame $t$ is an arc $i \to j$, the emission of $j$ at frame $t + 1$, and a suffix after $j$ at frame $t + 1$, which is the recursion of line L4. $\square$

**Lemma 3 (posteriors).** $e^{\alpha_t(j) + \beta_t(j) - \ln Z_G}$ is the posterior probability, under the distribution $P_G(q) = e^{s(q)} / Z_G$ on the paths, that $q_t = j$. So $\gamma^G_t(p)$ of line L5 is $P_G(\mathrm{pdf}(q_t) = p)$, and $\sum_p \gamma^G_t(p) = 1$ for each $t$.

*Proof.* Every path with $q_t = j$ splits in one way into a partial path that ends in $j$ at frame $t$ and a suffix after $j$, and $s(q)$ is the sum of the two parts. So $e^{\alpha_t(j) + \beta_t(j)}$ is the sum of $e^{s(q)}$ over the paths with $q_t = j$ (Lemmas 1 and 2). Dividing by $Z_G$ gives the posterior. Each path has exactly one state at frame $t$, so the posteriors sum to 1. $\square$

**Theorem.** If $Z_{\mathrm{num}} > 0$ and $Z_{\mathrm{den}} > 0$, line L6 returns $F = \ln Z_{\mathrm{num}} - \ln Z_{\mathrm{den}}$, and line L7 returns

$$\frac{\partial F}{\partial \ell_t(p)} = \kappa \left( \gamma^{\mathrm{num}}_t(p) - \gamma^{\mathrm{den}}_t(p) \right).$$

*Proof.* The value of $F$ follows from Lemma 1 for both graphs. For the gradient, $s(q)$ depends on $\ell_t(p)$ only through the term $\kappa \ell_t(\mathrm{pdf}(q_t))$, so $\partial s(q) / \partial \ell_t(p) = \kappa [\mathrm{pdf}(q_t) = p]$. Then

$$\frac{\partial \ln Z_G}{\partial \ell_t(p)} = \frac{1}{Z_G} \sum_q e^{s(q)} \kappa [\mathrm{pdf}(q_t) = p] = \kappa P_G(\mathrm{pdf}(q_t) = p) = \kappa \gamma^G_t(p)$$

by Lemma 3. Subtract the result for the denominator from the result for the numerator. $\square$

**Corollary 1.** For each frame, $\sum_p \partial F / \partial \ell_t(p) = \kappa (1 - 1) = 0$. So adding the same constant to all $\ell_t(p)$ of a frame does not change $F$, and the gradient carries no information about the scale of the frame.

**Corollary 2 (a log posterior).** If every path of the numerator graph is also a path of the denominator graph with the same score, then $Z_{\mathrm{num}} \le Z_{\mathrm{den}}$ and $F \le 0$. Then $e^F$ is the posterior probability of the reference under the model in which the denominator graph holds all transcripts. $F = 0$ when the two graphs have the same paths, and then the gradient is 0.

*Proof.* The sum over the numerator paths is part of the sum over the denominator paths, and all terms are positive. With equal path sets the two posteriors of Lemma 3 are equal. $\square$

**Remark (the extended Baum-Welch update).** For discrete output distributions $b_p(v)$ and $\kappa = 1$, the derivative of $F$ with respect to $\ln b_p(v)$ is $c^{\mathrm{num}}_p(v) - c^{\mathrm{den}}_p(v)$, the difference of the counts of symbol $v$ under pdf $p$; this follows from the theorem by the chain rule, because $\ell_t(p) = \ln b_p(\mathrm{obs}_t)$. The update

$$b'_p(v) = \frac{c^{\mathrm{num}}_p(v) - c^{\mathrm{den}}_p(v) + D b_p(v)}{\sum_{v'} \left( c^{\mathrm{num}}_p(v') - c^{\mathrm{den}}_p(v') + D b_p(v') \right)}$$

keeps $b'$ a distribution when $D$ makes every numerator positive. Gopalakrishnan, Kanevsky, Nádas and Nahamoo (1991) proved that for a large enough $D$ this update does not decrease a rational function such as $e^F$. The proof here does not cover that result; the tests check it on small cases and check the counts against finite differences.
