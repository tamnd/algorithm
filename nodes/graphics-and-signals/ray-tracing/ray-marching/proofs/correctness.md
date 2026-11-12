---
title: Fixed-step ray marching never reports a hit before the first root, and finds it when the first inside interval is at least one step long
proves: [correctness, termination]
status: full
---

Let $F : [t_0, t_1] \to \mathbb{R}$ be continuous with $F(t_0) > 0$, let $\Delta > 0$ and let $k \ge 0$ be the number of bisection steps. The samples of line L4 are $s_j = \min(t_0 + j\Delta, t_1)$ for $j = 1, 2, \ldots$, until the first $j$ with $s_j = t_1$. Write $Z = \{t \in [t_0, t_1] : F(t) \le 0\}$. If $Z$ is not empty, let $t^* = \min Z$, which exists because $Z$ is closed and bounded, and let $I = [t^*, e]$ be the connected component of $Z$ that contains $t^*$. We use exact real arithmetic.

**Claim.**

1. The program stops after at most $\lceil (t_1 - t_0)/\Delta \rceil + k$ evaluations after the first.
2. If it returns none, then $F > 0$ at every sample. If it returns $b$, then $F(b) \le 0$, there is a root of $F$ in $[b - \Delta/2^k, b]$, and $t^* \le b$.
3. If $Z$ is not empty and $e - t^* \ge \Delta$ or $e = t_1$, the program returns $b$ with $t^* \le b < t^* + \Delta/2^k$ when $k \ge 1$, and $t^* \le b \le t^* + \Delta$ when $k = 0$.
4. If $F$ is $L$-Lipschitz, $F(s) > 0$, $F(s') > 0$ and $F(s) + F(s') > L(s' - s)$, then $F > 0$ on $[s, s']$.

**Termination (1).** Each pass of the loop of line L3 increases $j$ by one. Since $s_j = t_1$ for $j = \lceil (t_1 - t_0)/\Delta \rceil$, the test of line L3 fails after at most that many passes. The bisection loop of line L8 runs $k$ times and then returns.

**Safety (2).** If the program returns none, it evaluated $F$ at every sample and each value was positive, else line L6 would have returned. Suppose it returns at line L11 from the pass with samples $s_{j-1} < s_j$ (with $s_0 = t_0$). Then $F(s_{j-1}) > 0$, because either $j - 1 = 0$ and $F(t_0) > 0$, or the pass $j - 1$ did not return. And $F(s_j) \le 0$ by line L6. Lines L7 to L10 keep the invariant

$$F(a) > 0, \qquad F(b) \le 0, \qquad b - a = (s_j - s_{j-1}) / 2^i$$

after $i$ steps. It holds for $i = 0$ by line L7. In a step, $m$ is the midpoint. If $F(m) > 0$ the new pair is $(m, b)$, otherwise $(a, m)$; both keep the signs, and the length halves. After $k$ steps, $b - a \le \Delta / 2^k$. Since $F(a) > 0 \ge F(b)$ and $F$ is continuous, the intermediate value theorem gives a root in $[a, b] \subseteq [b - \Delta/2^k, b]$. Since $F(b) \le 0$, $b \in Z$, so $t^* \le b$.

**First root (3).** First, $I$ contains a sample. If $e = t_1$, the last sample $t_1$ is in $I$. If $e - t^* \ge \Delta$, the closed interval $[t^*, e]$ of length at least $\Delta$ contains a point $t_0 + j\Delta$ with $j \ge 1$ (because $t^* > t_0$), and that point is at most $e \le t_1$, so it is the sample $s_j$. Let $s_j$ be the first sample in $I$. No sample before $s_j$ is in $Z$: a sample before $t^*$ is not in $Z$ by the definition of $t^*$, and a sample in $[t^*, s_j)$ would be in $I$ and earlier than $s_j$. So the program reaches pass $j$, and line L6 returns there. Also $s_{j-1} < t^*$: otherwise $s_{j-1} \in [t^*, s_j) \subseteq I$.

On the bracket $[s_{j-1}, s_j]$, $F > 0$ on $[s_{j-1}, t^*)$ by the definition of $t^*$, and $F \le 0$ on $[t^*, s_j]$ because this interval is inside $I$. So for each midpoint, $F(m) > 0$ if and only if $m < t^*$. By induction on the steps, $a < t^* \le b$ holds after every step: it holds at the start, and a step that moves $a$ to $m$ has $m < t^*$, a step that moves $b$ to $m$ has $m \ge t^*$. After $k$ steps $b - a \le \Delta / 2^k$, and $a < t^* \le b$ gives $0 \le b - t^* < \Delta/2^k$. For $k = 0$, $b = s_j \le s_{j-1} + \Delta < t^* + \Delta$.

**Certificate (4).** Suppose $F(r) \le 0$ for some $r \in [s, s']$. Since $F(s) > 0 \ge F(r)$, the Lipschitz bound gives $F(s) \le F(s) - F(r) \le L(r - s)$. In the same way, $F(s') \le L(s' - r)$. Adding, $F(s) + F(s') \le L(s' - s)$, which contradicts the hypothesis. So $F > 0$ on $[s, s']$.

**Remark (the condition in 3 is necessary).** For each $\Delta$ and each grid of samples, the function $F(t) = |t - c| - \varepsilon$ with $2\varepsilon < \Delta$ and $c$ the midpoint of two consecutive samples is positive at every sample, so the program returns none, although $Z = [c - \varepsilon, c + \varepsilon]$ is not empty. $\blacksquare$
