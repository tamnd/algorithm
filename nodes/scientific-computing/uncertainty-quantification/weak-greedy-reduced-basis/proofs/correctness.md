---
title: The weak greedy loop stops, certifies the error on the training set, and makes weak greedy steps
proves: [correctness, termination]
status: full
---

We assume exact arithmetic and the setting of the reduced basis method: $(u, v)_X = u^T X v$ with a symmetric positive definite $X$, $a(u, v; \mu) = v^T A(\mu) u$, coercivity $a(v, v; \mu) \ge \alpha(\mu) \|v\|_X^2$, continuity $|a(u, v; \mu)| \le \gamma(\mu) \|u\|_X \|v\|_X$ and $0 < \alpha_{LB}(\mu) \le \alpha(\mu)$. For a subspace $X_j$, $u_j(\mu) \in X_j$ is the Galerkin solution, $e_j(\mu) = u(\mu) - u_j(\mu)$, and $\Delta_j(\mu)$ is the bound of the reduced basis method. The empty space $X_0 = \{0\}$ has $u_0 = 0$. We use three facts that the proof file of the reduced basis method shows, and that hold for $X_0$ in the same way, with residual $F$.

- (R) Reliability and effectivity: $\|e_j(\mu)\|_X \le \Delta_j(\mu) \le (\gamma(\mu)/\alpha_{LB}(\mu)) \|e_j(\mu)\|_X$.
- (P) Reproduction: if $u(\mu) \in X_j$, then $u_j(\mu) = u(\mu)$ and $\Delta_j(\mu) = 0$.
- (E) Line L4 computes $\Delta_j$ exactly from the tables, and line L3 keeps $Z$ an $X$-orthonormal basis of $X_j = \operatorname{span}\{u(\mu_1), \ldots, u(\mu_j)\}$ as long as each new snapshot is not in $X_{j-1}$.

**Lemma 1 (Cea in the X norm).** $\|e_j(\mu)\|_X \le (\gamma(\mu)/\alpha(\mu)) \operatorname{dist}_X(u(\mu), X_j)$.

*Proof.* Galerkin orthogonality gives $a(e_j, w; \mu) = 0$ for all $w \in X_j$. For any $v \in X_j$, $u_j - v \in X_j$, so $\alpha \|e_j\|_X^2 \le a(e_j, e_j; \mu) = a(e_j, u - v; \mu) \le \gamma \|e_j\|_X \|u - v\|_X$. Divide by $\|e_j\|_X$ (the claim is clear if it is 0) and take the infimum over $v$. $\square$

**Lemma 2 (no repeated choice).** Suppose the loop does not stop at step $j$, so the largest bound $\Delta_j(\mu_k)$ is above $\varepsilon_{tol} \ge 0$. Then $u(\mu_k) \notin X_j$, and in particular $\mu_k$ is not one of $\mu_1, \ldots, \mu_j$.

*Proof.* If $u(\mu_k) \in X_j$, then (P) gives $\Delta_j(\mu_k) = 0 \le \varepsilon_{tol}$, a contradiction. Each chosen $u(\mu_i)$, $i \le j$, is in $X_j$. $\square$

The first parameter comes from line L1. Its snapshot $u(\mu_1)$ is not 0 when $F \ne 0$, since $A(\mu_1)$ is invertible. (If $F = 0$, all bounds are 0 and the first test stops the loop with $u = 0$ exact.) So by Lemma 2 and induction, each snapshot that line L3 adds is outside the current span, the dimension grows by one at each step, and (E) holds at each step.

**Theorem 1 (termination).** The loop stops after at most $\min(m, r_{max})$ steps.

*Proof.* By Lemma 2 the chosen parameters are distinct points of $\Xi$, so there are at most $m$ of them. After $m$ steps, every $u(\mu)$ with $\mu \in \Xi$ is in $X_m$, so by (P) every bound is 0 and the test of line L6 holds. The test also holds when $Z$ has $r_{max}$ columns. $\square$

**Theorem 2 (certification).** At the return of line L7 with $r$ vectors, $\|u(\mu) - u_r(\mu)\|_X \le \varepsilon_r$ for all $\mu \in \Xi$. If the loop stops by the tolerance, $\varepsilon_r \le \varepsilon_{tol}$.

*Proof.* $\varepsilon_r$ is the largest bound over $\Xi$ (line L5), and each bound is at least the error by (R). $\square$

**Theorem 3 (weak greedy step).** Let $\kappa = \max_{\mu \in \Xi} \gamma(\mu)^2 / (\alpha(\mu)\, \alpha_{LB}(\mu))$. The parameter $\mu^\ast$ that the algorithm chooses after $X_j$ (by line L1 for $j = 0$, by line L5 for $j \ge 1$) satisfies

$$\operatorname{dist}_X(u(\mu^\ast), X_j) \ge \frac{1}{\kappa} \max_{\mu \in \Xi} \operatorname{dist}_X(u(\mu), X_j) .$$

*Proof.* For each $\mu \in \Xi$, $\Delta_j(\mu^\ast) \ge \Delta_j(\mu)$ by the choice. Then

$$\operatorname{dist}_X(u(\mu^\ast), X_j) \ge \frac{\alpha(\mu^\ast)}{\gamma(\mu^\ast)} \|e_j(\mu^\ast)\|_X \ge \frac{\alpha(\mu^\ast)\, \alpha_{LB}(\mu^\ast)}{\gamma(\mu^\ast)^2} \Delta_j(\mu^\ast) \ge \frac{1}{\kappa} \Delta_j(\mu) \ge \frac{1}{\kappa} \|e_j(\mu)\|_X \ge \frac{1}{\kappa} \operatorname{dist}_X(u(\mu), X_j) .$$

The first step is Lemma 1. The second and the fourth are the two sides of (R). The third is the choice and the definition of $\kappa$. The last holds because $u_j(\mu) \in X_j$. Take the maximum over $\mu$. For $j = 0$ the bound of the empty basis is $\|F\|_{X'}/\alpha_{LB}(\mu)$ and line L1 maximizes it, so the same chain holds. $\square$

**Corollary (the model problem).** For $A(\mu) = K + \mu M$, $X = K + \bar{\mu} M$ and $\alpha_{LB}(\mu) = \min(1, \mu/\bar{\mu})$, the reduced basis proof file shows $\gamma(\mu) \le \max(1, \mu/\bar{\mu})$. With $\alpha \ge \alpha_{LB}$, $\kappa \le \max_{\Xi} (\gamma/\alpha_{LB})^2$, which is $10^2 = 100$ for $\bar{\mu} = 10$ and $\Xi \subset [1, 100]$.

By Theorem 3, the algorithm is a weak greedy algorithm with parameter $1/\kappa$ on the compact set $\{u(\mu) : \mu \in \Xi\}$ in the sense of Binev et al. and of DeVore, Petrova and Wojtaszczyk, so their rate theorems apply to $\sigma_n = \max_{\Xi} \operatorname{dist}_X(u(\mu), X_n)$. $\blacksquare$
