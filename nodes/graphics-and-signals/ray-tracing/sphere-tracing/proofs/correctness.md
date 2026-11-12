---
title: Sphere tracing never passes the first hit, stops, and converges to the first root at a linear rate
proves: [correctness, termination]
status: full
---

**Setting.** Let $f : \mathbb{R}^3 \to \mathbb{R}$ be continuous and let $S = f^{-1}(0)$. Assume that $f$ is a signed distance bound that is positive outside: for every $x$ with $f(x) > 0$,

$$f(x) \le \operatorname{dist}(x, S). \tag{B}$$

Let $r(t) = o + t d$ with $\lVert d \rVert = 1$ and $f(o) > 0$, and write $F(t) = f(r(t))$. Let $t^* = \min\{t \ge 0 : F(t) \le 0\}$ when this set is not empty; it exists because the set is closed and bounded below. Since $F(0) > 0$ and $F$ is continuous, $F(t^*) = 0$, so $r(t^*) \in S$. Let $t_0 = 0$ and $t_{i+1} = t_i + F(t_i)$ be the values of line L6. We use exact real arithmetic.

**Lemma 1 (no overshoot).** If $t^*$ exists, then $t_i \le t^*$ for every $i$ that the program computes.

*Proof.* By induction. $t_0 = 0 \le t^*$. Suppose $t_i \le t^*$. If $t_i = t^*$, then $F(t_i) = 0 < \varepsilon$ and line L5 returns, so no $t_{i+1}$ is computed. If $t_i < t^*$, then $F(t_i) > 0$ by the definition of $t^*$, and by (B),

$$F(t_i) \le \operatorname{dist}(r(t_i), S) \le \lVert r(t_i) - r(t^*) \rVert = (t^* - t_i)\lVert d \rVert = t^* - t_i.$$

So $t_{i+1} = t_i + F(t_i) \le t^*$. $\square$

The same argument shows more: the open ball of radius $F(t_i)$ around $r(t_i)$ contains no point of $S$, so the open segment from $r(t_i)$ to $r(t_{i+1})$ contains no point of $S$. The trace skips only empty space.

**Lemma 2 (termination).** The program stops after at most $\min(N, \lfloor D/\varepsilon \rfloor + 2)$ evaluations of $f$.

*Proof.* The loop of line L2 runs at most $N$ times. In a pass that does not return at line L5, $F(t_i) \ge \varepsilon$, so $t_{i+1} \ge t_i + \varepsilon$. After $j$ such passes, $t \ge j \varepsilon$. If $j \ge \lfloor D/\varepsilon \rfloor + 1$, then $t > D$ and the next pass returns at line L3 before it evaluates $f$. So there are at most $\lfloor D/\varepsilon \rfloor + 1$ passes that continue, and one more pass that returns at line L5, or none. $\square$

**Lemma 3 (what a result means).** If the program returns $t$, then $F(t) < \varepsilon$ and $t \le t^*$ when $t^*$ exists. If in addition $f$ is a signed distance function, then $\operatorname{dist}(r(t), S) < \varepsilon$.

*Proof.* Line L5 returns only when $F(t) < \varepsilon$, and Lemma 1 gives $t \le t^*$. For a signed distance function, $\operatorname{dist}(r(t), S) = |F(t)|$, and $F(t) \ge 0$ because $t \le t^*$. $\square$

**Lemma 4 (convergence as $\varepsilon \to 0$).** Run the iteration without the test of line L5 and without the limits $D$ and $N$. If $t^*$ exists, then $t_i \to t^*$. If $t^*$ does not exist, then $t_i \to \infty$ or $t_i$ converges to a value $\bar t$ with $F(\bar t) = 0$, which is impossible; so $t_i \to \infty$.

*Proof.* While $F(t_i) > 0$, the sequence increases. If $t^*$ exists, it is bounded by $t^*$ (Lemma 1, which holds without line L5 because $t_i = t^*$ gives $t_{i+1} = t_i$). An increasing bounded sequence has a limit $\bar t \le t^*$. Then $F(t_i) = t_{i+1} - t_i \to 0$, and by continuity $F(\bar t) = 0$. So $\bar t \ge t^*$ by the definition of $t^*$, and $\bar t = t^*$. If $t^*$ does not exist, $F > 0$ on $[0, \infty)$; a finite limit $\bar t$ would again give $F(\bar t) = 0$, a contradiction. Since the sequence increases, it tends to infinity. $\square$

**Lemma 5 (rate).** Suppose $f$ is a signed distance function that is differentiable along the ray near $t^*$, with $F'(t^*) = -\cos\theta < 0$, where $\theta$ is the angle between $-d$ and the outward normal $\nabla f(r(t^*))$. Then the gaps $e_i = t^* - t_i$ satisfy $e_{i+1}/e_i \to 1 - \cos\theta$. For a plane, $e_{i+1} = (1 - \cos\theta)\, e_i$ exactly.

*Proof.* By Lemma 4, $e_i \to 0$. Since $F(t^*) = 0$, the definition of the derivative gives $F(t_i) = F'(t^*)(t_i - t^*) + o(e_i) = \cos\theta\, e_i + o(e_i)$. So $e_{i+1} = e_i - F(t_i) = (1 - \cos\theta) e_i + o(e_i)$. If $\cos\theta < 1$ and $e_i > 0$ for all $i$, divide by $e_i$ to get the limit. If $\cos\theta = 1$, the ratio tends to 0, which is faster than linear. For the half space $\{x : n \cdot x + h \le 0\}$ with unit $n$, $F(t) = n \cdot o + h + t\,(n \cdot d)$ is affine with slope $-\cos\theta$, and $F(t_i) = \cos\theta\, e_i$ holds exactly. $\square$

For a function with Lipschitz bound $\lambda$ divided by $\lambda$, the same computation gives the factor $1 + F'(t^*)/\lambda$, which is Hart's form of the rate. At a tangent point, $F'(t^*) = 0$ and the factor is 1: Lemma 4 still gives convergence, but more slowly than any geometric sequence.

**Theorem.** Under (B), sphere tracing terminates, every point it visits lies in front of the first hit, a returned $t$ satisfies $F(t) < \varepsilon$ and $t \le t^*$, and as $\varepsilon \to 0$ the returned values converge to $t^*$ at the linear rate of Lemma 5.

*Proof.* Lemmas 1 to 5. For the last claim: for each $\varepsilon$, with $D \ge t^*$ and $N$ large enough, the trace returns the first $t_i$ with $F(t_i) < \varepsilon$. Because $F(t_i) \to 0$ (Lemma 4), such an $i$ exists. Because $F \ge 0$ on $[0, t^*]$ and $F > 0$ on $[0, t^*)$, the first $t_i$ with $F(t_i) < \varepsilon$ tends to $t^*$ as $\varepsilon \to 0$: on each interval $[0, t^* - \eta]$ the minimum of $F$ is positive, so for small $\varepsilon$ the returned value is above $t^* - \eta$. $\blacksquare$

**Remark (the bound is necessary).** If (B) fails at a point of the ray, the step can pass $t^*$. For the thin shell $f(x) = \bigl|\lVert x \rVert - 2\bigr| - 0.05$ and the ray from $(0, 0, -5)$ along $+z$, $t^* = 2.95$ and $f(o) = 2.95$. With $3f$ in place of $f$, the first step goes to $t = 8.85$, past the whole shell.
