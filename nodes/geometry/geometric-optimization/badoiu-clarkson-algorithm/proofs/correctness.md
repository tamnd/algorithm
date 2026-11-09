---
title: The Badoiu-Clarkson center after k steps is within r*/sqrt(k) of the optimal center, and its farthest points form a core set
proves: [correctness]
status: full
---

**Setting.** $P$ is a finite nonempty set of points in $\mathbb{R}^d$ with the Euclidean inner product $\langle \cdot, \cdot \rangle$ and norm $|\cdot|$. For a finite nonempty set $Q$, $B(c_Q, r_Q)$ is its minimum enclosing ball, which exists and is unique (see the [minimum enclosing ball](/minimum-enclosing-ball/) page). We write $c^* = c_P$ and $r^* = r_P$. The algorithm sets $c_1 = p_1 \in P$, and for $i \ge 1$ picks $q_i \in P$ with $|q_i - c_i| = \max_{p \in P} |p - c_i|$ and sets $c_{i+1} = c_i + (q_i - c_i)/(i + 1)$.

**Lemma 0 (the center is in the hull of the contact points).** Let $Q$ be finite and nonempty and $T = \{p \in Q : |p - c_Q| = r_Q\}$. Then $c_Q$ lies in the convex hull of $T$.

*Proof.* Suppose not. The convex hull of $T$ is compact and convex, so by the separation theorem there is a unit vector $u$ with $\langle p - c_Q, u \rangle > 0$ for all $p \in T$. For small $t > 0$ put $c = c_Q + t u$. For $p \in T$, $|p - c|^2 = r_Q^2 - 2t \langle p - c_Q, u \rangle + t^2 < r_Q^2$ once $t < 2 \min_{p \in T} \langle p - c_Q, u \rangle$. For $p \in Q \setminus T$, $|p - c_Q| < r_Q$, and $|p - c| \le |p - c_Q| + t < r_Q$ for small $t$. So for some $t > 0$ all points of $Q$ are at distance less than $r_Q$ from $c$, and a ball of smaller radius centered at $c$ contains $Q$, which contradicts minimality. (If $T$ were empty the same argument with any $u$ works, and so $T$ is not empty.) $\square$

**Lemma 1 (a far point exists).** Let $Q$ be finite and nonempty. For every point $c \in \mathbb{R}^d$ there is $p \in Q$ with $|p - c|^2 \ge r_Q^2 + |c - c_Q|^2$.

*Proof.* If $c = c_Q$, take any $p \in T$. Otherwise, by Lemma 0 write $c_Q = \sum_{p \in T} \lambda_p p$ with $\lambda_p \ge 0$ and $\sum \lambda_p = 1$. Then $\sum_{p \in T} \lambda_p \langle p - c_Q, c - c_Q \rangle = \langle c_Q - c_Q, c - c_Q \rangle = 0$, so some $p \in T$ has $\langle p - c_Q, c - c_Q \rangle \le 0$. For it,

$$|p - c|^2 = |p - c_Q|^2 + |c - c_Q|^2 - 2\langle p - c_Q, c - c_Q \rangle \ge r_Q^2 + |c - c_Q|^2. \qquad \square$$

**Lemma 2 (one step).** Let $Q$ be finite and nonempty, $c$ a point, and $q \in Q$ a point of $Q$ farthest from $c$. For $i \ge 1$ let $c' = c + (q - c)/(i + 1)$. Then

$$|c' - c_Q|^2 \le \frac{i^2 |c - c_Q|^2 + r_Q^2}{(i + 1)^2}.$$

*Proof.* Put $u = c - c_Q$, $v = q - c$, $a = 1/(i + 1)$. Because $q \in Q \subseteq B(c_Q, r_Q)$, $|u + v|^2 \le r_Q^2$, that is $2 \langle u, v \rangle \le r_Q^2 - |u|^2 - |v|^2$. Because $q$ is farthest and by Lemma 1, $|v|^2 \ge r_Q^2 + |u|^2$. Now $c' - c_Q = u + a v$, and since $0 < a \le 1/2$ the coefficient $a - a^2$ is positive:

$$|u + av|^2 = |u|^2 + 2a\langle u, v \rangle + a^2 |v|^2 \le (1 - a)|u|^2 + a\, r_Q^2 - (a - a^2) |v|^2 \le (1 - a)|u|^2 + a\, r_Q^2 - (a - a^2)(r_Q^2 + |u|^2).$$

The right side is $(1 - a)^2 |u|^2 + a^2 r_Q^2 = \bigl(i^2 |u|^2 + r_Q^2\bigr)/(i + 1)^2$. $\square$

**Theorem 1.** For every $k \ge 1$, $|c_k - c^*|^2 \le r^{*2}/k$, and every $p \in P$ satisfies $|p - c_k| \le (1 + 1/\sqrt{k})\, r^*$.

*Proof.* Let $e_i = i^2 |c_i - c^*|^2$. Since $c_1 = p_1 \in B(c^*, r^*)$, $e_1 \le r^{*2}$. Lemma 2 with $Q = P$, $c = c_i$ and $q = q_i$ gives $(i + 1)^2 |c_{i+1} - c^*|^2 \le i^2 |c_i - c^*|^2 + r^{*2}$, that is $e_{i+1} \le e_i + r^{*2}$. By induction $e_k \le k\, r^{*2}$, so $|c_k - c^*|^2 \le r^{*2}/k$. For $p \in P$, $|p - c_k| \le |p - c^*| + |c^* - c_k| \le r^* + r^*/\sqrt{k}$. $\square$

So with $k \ge 1/\varepsilon^2$ centers, the ball $B(c_k, \max_{p \in P} |p - c_k|)$ contains $P$ and has radius at most $(1 + \varepsilon) r^*$.

**Theorem 2 (core set).** Let $q_k$ be a point of $P$ farthest from $c_k$, and $S = \{p_1, q_1, \dots, q_k\}$. Then every $p \in P$ satisfies $|p - c_S| \le (1 + 2/\sqrt{k})\, r_S$.

*Proof.* We repeat the proof of Theorem 1 with $Q = S$. The centers $c_i$ are those computed on $P$. For each $i \le k$, $q_i \in S$, and $q_i$ is a point of $S$ farthest from $c_i$, because it is farthest among all of $P \supseteq S$. So Lemma 2 applies with $Q = S$, and $c_1 = p_1 \in S \subseteq B(c_S, r_S)$. As before, $|c_k - c_S| \le r_S/\sqrt{k}$. Since $q_k \in S$, $|q_k - c_k| \le |q_k - c_S| + |c_S - c_k| \le r_S + r_S/\sqrt{k}$. For any $p \in P$, $|p - c_k| \le |q_k - c_k|$ by the choice of $q_k$, so

$$|p - c_S| \le |p - c_k| + |c_k - c_S| \le r_S + \frac{r_S}{\sqrt{k}} + \frac{r_S}{\sqrt{k}}. \qquad \blacksquare$$
