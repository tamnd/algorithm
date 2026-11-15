---
title: Sequentially thresholded least squares stops after at most p + 1 fits and recovers a sparse model from exact or slightly perturbed derivatives
proves: [correctness]
status: full
---

We work in exact real arithmetic, as in the real RAM, and assume that each least squares fit is exact. Fix one state component. $\Theta$ is the $M \times p$ library matrix of L1 and $b \in \mathbb{R}^M$ is the vector of derivatives of this component. For a set $S \subseteq \{1, \ldots, p\}$, $\Theta_S$ is the matrix of the columns in $S$, and $\operatorname{LS}(S)$ is the vector $\xi$ with $\xi_S = \Theta_S^{+} b$ and $\xi_k = 0$ for $k \notin S$. The threshold is $\lambda > 0$. We assume that $\Theta$ has full column rank $p$, so every $\Theta_S$ has full column rank and $\Theta_S^{+} = (\Theta_S^T \Theta_S)^{-1} \Theta_S^T$.

**The iteration.** STLSQ starts with $S_0 = \{1, \ldots, p\}$ and $\xi^{(0)} = \operatorname{LS}(S_0)$ (L3). For $t = 0, 1, \ldots$ it sets $S_{t+1} = \{k \in S_t : |\xi^{(t)}_k| \ge \lambda\}$ (L5). If $S_{t+1} = S_t$ it stops and returns $\xi^{(t)}$ (L7); otherwise it sets $\xi^{(t+1)} = \operatorname{LS}(S_{t+1})$ (L6). The code also stops after $p + 1$ fits.

**Lemma 1 (termination).** The sets satisfy $S_0 \supsetneq S_1 \supsetneq \cdots$ until the stop, so STLSQ stops after at most $p + 1$ least squares fits, and the cap of $p + 1$ fits never ends the loop before the stop rule would.

*Proof.* By definition $S_{t+1} \subseteq S_t$, and the loop continues only if $S_{t+1} \ne S_t$, so each continued step removes at least one index. Since $|S_0| = p$, there are at most $p$ such steps, each followed by one fit, plus the first fit: at most $p + 1$ fits. If $p + 1$ fits are done, then $p$ indices were removed, so the set is empty and $\xi = 0$. The next test would give the same empty set and stop with the same $\xi = 0$. So the cap does not change the result. $\square$

**Lemma 2 (fixed point).** The returned $\xi$ satisfies $\xi = \operatorname{LS}(S)$ for its final set $S$, $|\xi_k| \ge \lambda$ for every $k \in S$, and $\xi_k = 0$ for every $k \notin S$.

*Proof.* At the stop, $\xi = \xi^{(t)} = \operatorname{LS}(S_t)$ and $\{k \in S_t : |\xi_k| \ge \lambda\} = S_t$. Entries outside $S_t$ are zero by the definition of $\operatorname{LS}$. In the capped case of Lemma 1, $S = \emptyset$ and $\xi = 0$, and the statement holds trivially. $\square$

So every returned coefficient is either zero or at least $\lambda$ in size, and the nonzero ones are the least squares fit on their own columns. Zhang and Schaeffer (2019) prove that such fixed points approximate local minimizers of the problem $\min_\xi \lVert \Theta \xi - b \rVert^2 + \lambda^2 \lVert \xi \rVert_0$ and give conditions for convergence; that analysis is not repeated here.

**Theorem 1 (exact recovery).** Let $b = \Theta \xi^*$ with support $S^* = \{k : \xi^*_k \ne 0\}$, and let $0 < \lambda \le \min_{k \in S^*} |\xi^*_k|$. Then STLSQ returns $\xi^*$ after at most two fits.

*Proof.* $\Theta$ has full column rank and $\Theta \xi^* = b$, so the first fit gives $\xi^{(0)} = \Theta^{+} b = \xi^*$. Then $S_1 = S^*$, because every $k \in S^*$ has $|\xi^*_k| \ge \lambda$ and every other $k$ has $\xi^*_k = 0 < \lambda$. If $S^* = S_0$, the loop stops with $\xi^*$. Otherwise the second fit gives $\operatorname{LS}(S^*)$; $\Theta_{S^*} \xi^*_{S^*} = b$ and $\Theta_{S^*}$ has full column rank, so the fit is again $\xi^*$, and the next test gives $S^*$ again and stops. $\square$

**Theorem 2 (recovery under a small perturbation).** Let $b = \Theta \xi^* + e$, let $\mu = \min_{k \in S^*} |\xi^*_k| > \lambda$, and let

$$\delta = \max\big(\lVert \Theta^{+} e \rVert_\infty, \lVert \Theta_{S^*}^{+} e \rVert_\infty\big) < \min(\lambda, \mu - \lambda).$$

Then STLSQ returns $\operatorname{LS}(S^*)$, the least squares fit on the true support, whose nonzero entries are $\xi^*_{S^*} + \Theta_{S^*}^{+} e$.

*Proof.* The first fit is $\xi^{(0)} = \Theta^{+} (\Theta \xi^* + e) = \xi^* + \Theta^{+} e$. For $k \in S^*$, $|\xi^{(0)}_k| \ge \mu - \delta > \lambda$. For $k \notin S^*$, $|\xi^{(0)}_k| \le \delta < \lambda$. So $S_1 = S^*$. If $S^* = S_0$ the loop stops. Otherwise the second fit is $\operatorname{LS}(S^*)$ with entries $\xi^*_{S^*} + \Theta_{S^*}^{+} e$ on $S^*$, since $\Theta_{S^*}^{+} \Theta_{S^*} = I$. Each has size at least $\mu - \delta > \lambda$, so $S_2 = S^*$ and the loop stops. $\square$

**Theorem (correctness of SINDy).** L2 runs STLSQ once for each of the $n$ state components with the same $\Theta$. Under the full rank assumption, SINDy returns after at most $n(p + 1)$ least squares fits a coefficient matrix whose columns have the property of Lemma 2. If the derivatives are exact, $\dot x = \Xi^{*T} \theta(x)$ holds at the samples and $\lambda$ is at most the smallest nonzero entry of $\Xi^*$ in size, SINDy returns $\Xi^*$. With perturbed derivatives, the conclusion of Theorem 2 holds column by column.

*Proof.* Apply Lemmas 1 and 2 and Theorems 1 and 2 to each column. $\blacksquare$

**Remark (the error in the derivatives).** With central differences, $e$ is the difference error, of order $h^2$ times the third derivative of the state, plus the effect of measurement noise divided by $h$. Theorem 2 then says that the model structure is right when this error, mapped through $\Theta^{+}$, is smaller than both $\lambda$ and the gap $\mu - \lambda$. The page shows this case and the failures for $\lambda$ too small or too large as measurements.
