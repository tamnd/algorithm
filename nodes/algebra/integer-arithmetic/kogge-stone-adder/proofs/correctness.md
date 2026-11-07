---
title: The Kogge-Stone adder computes the sum
proves: [correctness, termination]
status: full
---

Let $a = \sum_{i<n} a_i2^i$ and $b = \sum_{i<n} b_i2^i$ with bits $a_i, b_i$, and let $c_0 \in \{0, 1\}$. The carries of the addition are defined by the recurrence

$$c_{i+1} = g_i \vee (p_i \wedge c_i), \qquad g_i = a_i \wedge b_i, \quad p_i = a_i \oplus b_i ,$$

and the full adder identity $a_i + b_i + c_i = (p_i \oplus c_i) + 2c_{i+1}$ gives, by induction on $i$ (as on the page of the [ripple-carry adder](/ripple-carry-adder/)), $a + b + c_0 = \sum_{i<n} (p_i \oplus c_i)2^i + c_n2^n$. So it suffices to show that the network computes $c_1, \ldots, c_n$.

**Block signals.** For $0 \le k \le i < n$ define the block function $F_{i:k}(x)$, the carry out of position $i$ when the carry into position $k$ is $x$: $F_{k:k}(x) = g_k \vee (p_k \wedge x)$ and $F_{i:k}(x) = g_i \vee (p_i \wedge F_{i-1:k}(x))$. Every such function has the form $F(x) = G \vee (P \wedge x)$ for bits $G, P$, since compositions of maps of this form keep the form:

$$G_1 \vee (P_1 \wedge (G_2 \vee (P_2 \wedge x))) = (G_1 \vee (P_1 \wedge G_2)) \vee ((P_1 \wedge P_2) \wedge x) .$$

Write $(G_{i:k}, P_{i:k})$ for the pair of $F_{i:k}$. The identity shows that, for $k \le j < i$,

$$(G_{i:k}, P_{i:k}) = (G_{i:j+1}, P_{i:j+1}) \circ (G_{j:k}, P_{j:k}), \qquad (G, P) \circ (G', P') = (G \vee (P \wedge G'), P \wedge P'),$$

because $F_{i:k} = F_{i:j+1} \circ F_{j:k}$ as functions. Composition of functions is associative, so $\circ$ is associative on the pairs that arise.

**Folding the carry in.** Line L2 replaces $g_0$ by $g_0' = g_0 \vee (p_0 \wedge c_0) = c_1$. With $g_0'$ in place of $g_0$, the block function of $0..i$ satisfies $F'_{i:0}(0) = F_{i:0}(c_0) = c_{i+1}$, and its $G$ part is $G'_{i:0} = F'_{i:0}(0) = c_{i+1}$. From now on $g_0$ means $g_0'$.

**Lemma.** For $t = 0, 1, \ldots, L$ with $L = \lceil \log_2 n \rceil$, after $t$ iterations of the loop of line L4 (so $d = 2^t$), position $i$ holds $(G[i], P[i]) = (G_{i:k}, P_{i:k})$ with $k = \max(0, i - 2^t + 1)$.

*Proof.* By induction on $t$. For $t = 0$, line L3 sets $(G[i], P[i]) = (g_i, p_i) = (G_{i:i}, P_{i:i})$, and $\max(0, i) = i$.

Assume the claim after $t$ iterations, with $d = 2^t$, and consider line L5, which uses the values of iteration $t$ for all positions. For $i < d$, position $i$ is not updated, and $\max(0, i - 2d + 1) = 0 = \max(0, i - d + 1)$, so the claim holds. For $i \ge d$, position $i$ holds the block $i - d + 1..i$, since $i - d + 1 \ge 1 > 0$, and position $i - d$ holds the block $k'..i - d$ with $k' = \max(0, i - 2d + 1)$. These two blocks are adjacent, so their combination is the pair of the block $k'..i$, as claimed, with $2d = 2^{t+1}$. $\square$

**Theorem.** KOGGE-STONE-ADD terminates and returns the $n + 1$ bits of $a + b + c_0$.

*Proof.* The variable $d$ doubles in each iteration, so the loop stops after $L = \lceil \log_2 n \rceil$ iterations, with $2^L \ge n$. By the lemma with $t = L$, every position $i \le n - 1 < 2^L$ holds the pair of the block $0..i$, so $G[i] = G'_{i:0} = c_{i+1}$. Line L7 therefore sets the true carries $c_0, \ldots, c_n$, and line L8 computes $s_i = p_i \oplus c_i$. By the identity at the start, $\sum_{i<n} s_i2^i + c_n2^n = a + b + c_0$. $\blacksquare$

**Only $G$ is needed for short blocks.** If $i < 2d$, the block held by position $i$ after the update starts at 0, and only its $G$ part is used later (by line L7, or by position $i + d'$ for larger $d'$, which needs only $G$ from a block that starts at 0, since the combination $(G, P) \circ (G', P')$ uses $P'$ only in the $P$ part of the result). So the implementation computes the $P$ part only for $i \ge 2d$.
