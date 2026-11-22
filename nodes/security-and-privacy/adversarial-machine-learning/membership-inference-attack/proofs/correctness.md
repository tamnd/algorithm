---
title: The advantage of the membership game, the optimality of the threshold sweep, and the zero advantage against a model that ignores its data
proves: [correctness]
status: full
---

**Setting.** A threshold rule with cut $\tau \in \mathbb{R} \cup \{+\infty\}$ says MEMBER for a score $u$ when $u \ge \tau$. For finite lists IN of $n_{\text{in}} \ge 1$ scores and OUT of $n_{\text{out}} \ge 1$ scores, write $\text{tp}(\tau) = \lvert\{u \in \text{IN} : u \ge \tau\}\rvert$, $\text{fp}(\tau) = \lvert\{u \in \text{OUT} : u \ge \tau\}\rvert$, $\text{TPR}(\tau) = \text{tp}(\tau)/n_{\text{in}}$ and $\text{FPR}(\tau) = \text{fp}(\tau)/n_{\text{out}}$.

**Claim 1 (the advantage).** In the membership game, with a fair coin $b$, $2\Pr[\text{correct}] - 1 = \Pr[\text{MEMBER} \mid b = 0] - \Pr[\text{MEMBER} \mid b = 1]$.

*Proof.* The guess is correct when it says MEMBER and $b = 0$, or NONMEMBER and $b = 1$. So $\Pr[\text{correct}] = \tfrac{1}{2}\Pr[\text{MEMBER} \mid b = 0] + \tfrac{1}{2}\big(1 - \Pr[\text{MEMBER} \mid b = 1]\big)$. Multiply by 2 and subtract 1. $\square$

**Claim 2 (every rule is a candidate).** Let $U$ be the set of distinct scores of IN and OUT. For every $\tau$ there is a $\tau' \in U \cup \{+\infty\}$ with $\tau' \ge \tau$ and the same decision on every score of IN and OUT.

*Proof.* If no score is $\ge \tau$, take $\tau' = +\infty$: both rules say NONMEMBER for all scores. Else let $\tau'$ be the smallest score that is $\ge \tau$. A score $u \ge \tau'$ is $\ge \tau$. A score $u \ge \tau$ is a score $\ge \tau$, so $u \ge \tau'$ by the choice of $\tau'$. So the two rules agree on all scores. $\square$

**Claim 3 (the sweep).** best_threshold returns $(\tau^*, a^*)$ where $a^* = \max_\tau (\text{TPR}(\tau) - \text{FPR}(\tau))$ over all $\tau \in \mathbb{R} \cup \{+\infty\}$, and $\tau^*$ is the largest element of $U \cup \{+\infty\}$ that reaches $a^*$.

*Proof.* The code sorts the pairs by score in decreasing order and handles the distinct scores $u_1 > u_2 > \cdots > u_r$ in turn. *Invariant:* after the inner loop for $u_i$, tp and fp count the scores of IN and OUT that are $\ge u_i$. It holds after $u_1$, because the inner loop adds exactly the pairs of score $u_1$, and if it holds after $u_{i-1}$ it holds after $u_i$, because the pairs with score in $[u_i, u_{i-1})$ are exactly those of score $u_i$. So after $u_i$, tp $= \text{tp}(u_i)$ and fp $= \text{fp}(u_i)$, and key $= \text{tp}(u_i)\, n_{\text{out}} - \text{fp}(u_i)\, n_{\text{in}} = n_{\text{in}} n_{\text{out}} (\text{TPR}(u_i) - \text{FPR}(u_i))$. This is an integer, so the comparisons are exact. The start values $\tau = +\infty$, key $= 0$, are the values of the cut $+\infty$, for which $\text{tp} = \text{fp} = 0$. The candidates are seen in the order $+\infty, u_1, \ldots, u_r$, from the largest to the smallest, and a candidate replaces the best only when its key is strictly larger. So at the end the best is the first, which is the largest, candidate with the largest key. By Claim 2 every $\tau$ gives the same TPR and FPR as some candidate, so this key is the maximum over all $\tau$. Dividing by $n_{\text{in}} n_{\text{out}} > 0$ gives $a^*$. $\square$

**Claim 4 (TPR at a fixed FPR).** tpr_at_fpr returns $\max \{\text{TPR}(\tau) : \text{FPR}(\tau) \le \alpha\}$ over all $\tau \in \mathbb{R} \cup \{+\infty\}$, for $\alpha \ge 0$.

*Proof.* The same sweep and invariant give $\text{tp}(u_i)$ and $\text{fp}(u_i)$ after each distinct score, and the code keeps the largest $\text{tp}(u_i)/n_{\text{in}}$ among those with $\text{fp}(u_i)/n_{\text{out}} \le \alpha$. The start value $0$ is the TPR of the cut $+\infty$, whose FPR is $0 \le \alpha$. By Claim 2 every $\tau$ has the TPR and FPR of a candidate, so the maximum over the candidates is the maximum over all $\tau$. $\square$

**Claim 5 (a model that ignores its data).** Suppose the trained model $f$ is independent of the training set $S$, and $S$ consists of $n$ independent draws from $\mathcal{D}$. Then every attacker has advantage $0$.

*Proof.* Let $z$ be the challenge. If $b = 0$, $z$ is a uniform element of $S$, so $z$ has the law $\mathcal{D}$, and since $f$ is independent of $S$, it is independent of $z$. If $b = 1$, $z$ is a fresh draw from $\mathcal{D}$, again independent of $f$. So the pair $(z, f)$ has the same law in both cases, and so does the guess of any attacker, which is a function of $(z, f, n, \mathcal{D})$ and of its own coins. Then $\Pr[\text{MEMBER} \mid b = 0] = \Pr[\text{MEMBER} \mid b = 1]$, and by Claim 1 the advantage is $0$. $\square$

**The algorithm.** Lines L1 to L3 collect the scores of the shadow models on their members (IN) and on their nonmembers (OUT); line L4 is best_threshold, so by Claim 3 the cut maximizes TPR - FPR on the shadow scores; line L5 applies the cut to the target. Nothing is claimed about the advantage on the target, which depends on how well the shadow models stand in for it and is measured in the tests. In the test of Claim 5 the targets are trained on other draws, and the measured advantage of $-0.025$ on 160 members and 160 nonmembers is sampling noise around the value $0$. $\blacksquare$
