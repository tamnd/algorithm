---
title: The natural policy gradient is the compatible critic and improves the tabular policy
proves: [correctness]
status: full
---

Notation is that of the page. $\psi(s, a) = \nabla_\theta \log \pi_\theta(a \mid s)$, $d = d^\pi$ is the discounted visitation, $\nabla J = \sum_s d(s) \sum_a \pi(a \mid s) \psi(s, a) Q^\pi(s, a)$ by the policy gradient theorem, and $F = \sum_s d(s) \sum_a \pi(a \mid s) \psi(s, a) \psi(s, a)^\top$. A natural gradient is any $x$ with $F x = \nabla J$.

**Lemma 1 (the score has mean zero).** $\sum_a \pi(a \mid s) \psi(s, a) = \nabla_\theta \sum_a \pi(a \mid s) = \nabla_\theta 1 = 0$ for every $s$.

**Claim 1 (compatible function approximation, Kakade's Theorem 1).** Let $\epsilon(w) = \sum_s d(s) \sum_a \pi(a \mid s) (w^\top \psi(s, a) - Q^\pi(s, a))^2$. Then $w$ minimizes $\epsilon$ if and only if $F w = \nabla J$. The same holds with $Q^\pi$ replaced by $A^\pi = Q^\pi - V^\pi$.

*Proof.* $\epsilon$ is a convex quadratic in $w$, so $w$ is a minimizer if and only if $\nabla \epsilon(w) = 0$. $\nabla \epsilon(w) = 2 \sum_s d(s) \sum_a \pi(a \mid s) \psi(s, a) (\psi(s, a)^\top w - Q^\pi(s, a)) = 2(F w - \nabla J)$. A minimizer exists because the normal equations of a least squares problem are always consistent, so a natural gradient exists. Replacing $Q^\pi$ by $A^\pi$ changes $\nabla J$ by $\sum_s d(s) V^\pi(s) \sum_a \pi(a \mid s) \psi(s, a) = 0$ by Lemma 1. $\square$

**Claim 2 (tabular softmax).** Let $\pi(a \mid s) = e^{\theta_{s,a}} / \sum_b e^{\theta_{s,b}}$. Then $F$ is block diagonal with block $d(s)(\mathrm{diag}(\pi_s) - \pi_s \pi_s^\top)$, and if $d(s) > 0$ for every $s$, the natural gradients are exactly the vectors $x_{s,a} = A^\pi(s, a) + c_s$ with arbitrary constants $c_s$.

*Proof.* $\partial \log \pi(a \mid s) / \partial \theta_{t,b} = [t = s]([a = b] - \pi(b \mid s))$, so $\psi(s, a) = e_{s,a} - \sum_b \pi(b \mid s) e_{s,b}$ is supported on the coordinates of state $s$. Hence $F$ has no entries between different states, and its block for $s$ is $d(s) \sum_a \pi(a \mid s) (e_a - \pi_s)(e_a - \pi_s)^\top = d(s)(\mathrm{diag}(\pi_s) - \pi_s \pi_s^\top)$. By Lemma 1 and the same computation, the gradient block is $d(s) \sum_a \pi(a \mid s)(e_a - \pi_s) A^\pi(s, a) = d(s)(\mathrm{diag}(\pi_s) - \pi_s\pi_s^\top) A^\pi(s, \cdot)$, using $\sum_a \pi(a \mid s) A^\pi(s, a) = 0$. So $x = A^\pi$ solves $F x = \nabla J$. The kernel of $M_s = \mathrm{diag}(\pi_s) - \pi_s\pi_s^\top$: if $M_s v = 0$ then $\pi(a \mid s)(v_a - \pi_s^\top v) = 0$ for all $a$, and since $\pi(a \mid s) > 0$, $v_a = \pi_s^\top v$ for all $a$, so $v$ is constant; constants are in the kernel because $\pi_s^\top \mathbf{1} = 1$. With $d(s) > 0$ the kernel of the block is the same, which gives all solutions. $\square$

**Claim 3 (the exact step).** The step $\theta' = \theta + \eta x$ with $x$ from Claim 2 gives $\pi'(a \mid s) = \pi(a \mid s) e^{\eta A^\pi(s, a)} / Z_s$, with $Z_s = \sum_b \pi(b \mid s) e^{\eta A^\pi(s, b)}$, whatever the constants $c_s$.

*Proof.* $e^{\theta_{s,a} + \eta A^\pi(s,a) + \eta c_s} / \sum_b e^{\theta_{s,b} + \eta A^\pi(s,b) + \eta c_s}$; the factor $e^{\eta c_s}$ cancels, and dividing numerator and denominator by $\sum_b e^{\theta_{s,b}}$ gives the formula. $\square$

**Claim 4 (monotone improvement).** For every $\eta \ge 0$, $\sum_a \pi'(a \mid s) A^\pi(s, a) \ge 0$ for every $s$, hence $V^{\pi'}(s) \ge V^\pi(s)$ for every $s$.

*Proof.* Fix $s$ and write $u_a = A^\pi(s, a)$, $p_a = \pi(a \mid s)$, so $\sum_a p_a u_a = 0$. Let $\phi(\eta) = \log \sum_a p_a e^{\eta u_a}$. Then $\phi'(\eta) = \sum_a \pi'(a \mid s) u_a$ and $\phi''(\eta)$ is the variance of $u$ under $\pi'$, which is $\ge 0$. So $\phi'$ is nondecreasing and $\phi'(\eta) \ge \phi'(0) = \sum_a p_a u_a = 0$. Now $\sum_a \pi'(a \mid s) Q^\pi(s, a) = V^\pi(s) + \sum_a \pi'(a \mid s) A^\pi(s, a) \ge V^\pi(s)$ for every $s$, and the policy improvement theorem gives $V^{\pi'} \ge V^\pi$. $\square$

**Claim 5 (greedy limit).** As $\eta \to \infty$, $\pi'(\cdot \mid s)$ converges to $\pi(\cdot \mid s)$ restricted to $\arg\max_a A^\pi(s, a)$ and renormalized. For a softmax policy every action has positive probability, so the limit puts all its mass on the greedy actions.

*Proof.* Let $u^* = \max_a u_a$. Then $\pi'(a \mid s) = p_a e^{\eta(u_a - u^*)} / \sum_b p_b e^{\eta(u_b - u^*)}$. Terms with $u_a < u^*$ go to 0, and the others stay at $p_a$, so the limit is $\pi$ restricted to the maximizers and renormalized. $\square$

The limit in Claim 5 is greedy with respect to $A^\pi$, that is, a policy iteration step. Claims 1 to 4 together show that the exact natural policy gradient is well defined, that line L6 with $\epsilon \to 0$ and exact estimates computes it, and that for the tabular softmax every step improves the value in every state. $\blacksquare$
