---
title: RYSER returns the permanent
proves: [correctness]
status: full
---

Notation: $A = (a_{ij})$ is an $n \times n$ matrix over a commutative ring, $[n] = \{1, \ldots, n\}$, and $\operatorname{per}(A) = \sum_{\pi \in S_n} \prod_{i=1}^{n} a_{i \pi(i)}$. For $k \ge 1$, $\rho(k)$ is the number of trailing zero bits of $k$, and $g(k) = k \oplus \lfloor k/2 \rfloor$. For an integer $x \ge 0$, $\operatorname{set}(x) = \{ j \in [n] : \text{bit } j - 1 \text{ of } x \text{ is } 1 \}$. For $S \subseteq [n]$, let $P(S) = \prod_{i=1}^{n} \sum_{j \in S} a_{ij}$.

**Lemma 1 (Ryser's formula).** For $n \ge 1$, $\operatorname{per}(A) = (-1)^n \sum_{S \subseteq [n]} (-1)^{|S|} P(S)$.

*Proof.* Fix $S$. Expanding the product of the $n$ sums by distributivity gives

$$P(S) = \sum_{f : [n] \to S} \prod_{i=1}^{n} a_{i f(i)},$$

one term for each choice of one column $f(i) \in S$ for each row $i$. Every map $f : [n] \to S$ is a map $f : [n] \to [n]$ whose image $\operatorname{im} f$ is contained in $S$. So

$$\sum_{S \subseteq [n]} (-1)^{n - |S|} P(S) = \sum_{f : [n] \to [n]} c_f \prod_{i=1}^{n} a_{i f(i)}, \qquad c_f = \sum_{\operatorname{im} f \subseteq S \subseteq [n]} (-1)^{n - |S|}.$$

Let $m = |\operatorname{im} f|$. The sets $S$ with $\operatorname{im} f \subseteq S \subseteq [n]$ are $\operatorname{im} f \cup U$ for the subsets $U$ of the $n - m$ columns outside the image, and $n - |S| = (n - m) - |U|$. So

$$c_f = \sum_{t=0}^{n-m} \binom{n-m}{t} (-1)^{n-m-t} = (1 - 1)^{n-m},$$

by the binomial theorem. This is 1 when $m = n$ and 0 when $m < n$. A map $f : [n] \to [n]$ with $|\operatorname{im} f| = n$ is a bijection, that is, a permutation $\pi \in S_n$. So the sum equals $\sum_{\pi \in S_n} \prod_i a_{i \pi(i)} = \operatorname{per}(A)$. Finally $(-1)^{n - |S|} = (-1)^n (-1)^{|S|}$. $\square$

**Lemma 2 (the Gray code).** For $k \ge 1$, $g(k) \oplus g(k - 1) = 2^{\rho(k)}$. The values $g(1), \ldots, g(2^n - 1)$ are the integers $1, \ldots, 2^n - 1$ in some order, each once.

*Proof.* The map $x \mapsto \lfloor x/2 \rfloor$ acts on each bit position on its own, so $g(x \oplus y) = g(x) \oplus g(y)$. Write $k = q \cdot 2^{\rho(k)+1} + 2^{\rho(k)}$; then $k - 1 = q \cdot 2^{\rho(k)+1} + 2^{\rho(k)} - 1$, so $k \oplus (k - 1) = 2^{\rho(k)+1} - 1$, and $g(2^{\rho(k)+1} - 1) = (2^{\rho(k)+1} - 1) \oplus (2^{\rho(k)} - 1) = 2^{\rho(k)}$. This gives the first claim. For the second, if $g(x) = g(y)$ then $z = x \oplus y$ satisfies $z = \lfloor z/2 \rfloor$, so $z = 0$ and $x = y$. The highest one bit of $g(x)$ is the highest one bit of $x$, so $g$ maps $[0, 2^n)$ into itself, one to one, hence onto, and $g(0) = 0$. $\square$

**Lemma 3 (loop invariant).** For $n \ge 1$ and each $k$ with $0 \le k \le 2^n - 1$, after $k$ passes of the loop of line L3:

1. $S = \operatorname{set}(g(k))$;
2. $r[i] = \sum_{j \in S} a_{ij}$ for each $i \in [n]$;
3. $\text{total} = \sum_{t=1}^{k} (-1)^{|\operatorname{set}(g(t))|} P(\operatorname{set}(g(t)))$.

*Proof.* By induction on $k$. For $k = 0$, line L2 sets $S = \emptyset = \operatorname{set}(0)$, all $r[i] = 0$, which is the empty sum, and total $= 0$, the empty sum.

Assume the claim after $k - 1$ passes, with $1 \le k \le 2^n - 1$. Line L4 sets $j = \rho(k) + 1$, and $\rho(k) \le n - 1$ because $k < 2^n$. By Lemma 2, $\operatorname{set}(g(k))$ is $\operatorname{set}(g(k - 1))$ with column $j$ added if it was absent and removed if it was present. Line L5 does exactly this to $S$, so (1) holds, and it sets $s = +1$ when $j$ enters and $s = -1$ when $j$ leaves. Line L6 then adds $s \cdot a_{ij}$ to $r[i]$, which turns $\sum_{j' \in S_{\text{old}}} a_{ij'}$ into $\sum_{j' \in S_{\text{new}}} a_{ij'}$, so (2) holds. By (1) and (2), the product $r[1] \cdots r[n]$ in line L7 is $P(\operatorname{set}(g(k)))$ and the sign is $(-1)^{|\operatorname{set}(g(k))|}$, so (3) holds. $\square$

**Theorem.** RYSER$(A)$ returns $\operatorname{per}(A)$.

*Proof.* If $n = 0$, line L1 returns 1, which is the permanent of the empty matrix (the empty product over the one permutation of the empty set). Let $n \ge 1$. The loop of line L3 runs for $k = 1, \ldots, 2^n - 1$. By Lemma 3 (3) and Lemma 2, at the end total $= \sum_{\emptyset \ne S \subseteq [n]} (-1)^{|S|} P(S)$. The empty set has $P(\emptyset) = \prod_{i=1}^{n} 0 = 0$, since $n \ge 1$, so total $= \sum_{S \subseteq [n]} (-1)^{|S|} P(S)$. Line L8 returns $(-1)^n$ times this, which is $\operatorname{per}(A)$ by Lemma 1. $\blacksquare$
