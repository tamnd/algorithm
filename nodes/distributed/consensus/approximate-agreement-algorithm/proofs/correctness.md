---
title: The trimmed midpoint halves the spread and keeps validity when n > 3t
proves: [correctness]
status: full
---

**Setting.** Synchronous rounds, $n$ processes, a set $C$ of correct processes with $|C| \ge n - t$, and $n > 3t$. In round $r$ each correct process $p$ holds a value $x_p^{r}$, with $x_p^{0} = x_p$. Let

$$m_r = \min_{p \in C} x_p^{r}, \qquad M_r = \max_{p \in C} x_p^{r}, \qquad D_r = M_r - m_r.$$

In round $r + 1$, a correct process $p$ gets a multiset $V_p$ of $n$ values (lines L2 and L3). It holds $x_q^{r}$ for each $q \in C$, because messages from correct processes arrive in the round, and $n - |C| \le t$ other values, one for each faulty process. A missing value is replaced by $x_p^r$, which a faulty process could have sent, so it is just another faulty value. Let $a_p$ and $b_p$ be the $(t+1)$-th smallest and the $(t+1)$-th largest element of $V_p$, that is, the smallest and largest kept values (line L4). Line L5 sets $x_p^{r+1} = (a_p + b_p)/2$.

**Lemma 1 (the kept range is inside the correct range).** For each correct $p$, $m_r \le a_p \le b_p \le M_r$.

*Proof.* Every element of $V_p$ that is smaller than $m_r$ is a faulty value, so there are at most $t$ of them. Hence the $(t+1)$-th smallest element is at least $m_r$: $a_p \ge m_r$. The same argument at the top gives $b_p \le M_r$. Finally $a_p \le b_p$ because $V_p$ has $n \ge 2t + 1$ elements, so the $(t+1)$-th smallest is at most the $(t+1)$-th largest. $\square$

**Lemma 2 (a common kept point).** Let $u_1 \le u_2 \le \cdots \le u_{|C|}$ be the values $x_q^r$, $q \in C$, in sorted order, and let $c = u_{t+1}$. Then $a_p \le c \le b_p$ for every correct $p$.

*Proof.* $c$ exists because $|C| \ge n - t > 2t \ge t + 1$. The multiset $V_p$ contains $u_1, \ldots, u_{t+1}$, which are $t + 1$ elements that are at most $c$, so the $(t+1)$-th smallest element of $V_p$ is at most $c$: $a_p \le c$. It also contains $u_{t+1}, \ldots, u_{|C|}$, which are $|C| - t \ge n - 2t$ elements that are at least $c$. Since $n > 3t$, $n - 2t \ge t + 1$, so the $(t+1)$-th largest element of $V_p$ is at least $c$: $b_p \ge c$. $\square$

**Theorem 1 (one round).** $m_r \le m_{r+1}$, $M_{r+1} \le M_r$ and $D_{r+1} \le D_r / 2$.

*Proof.* By Lemma 1, $x_p^{r+1} = (a_p + b_p)/2 \in [m_r, M_r]$ for every correct $p$, which gives the first two claims. Take two correct processes $p$ and $q$. By Lemmas 1 and 2, $a_p, a_q \in [m_r, c]$ and $b_p, b_q \in [c, M_r]$. So

$$|x_p^{r+1} - x_q^{r+1}| = \frac{|(a_p - a_q) + (b_p - b_q)|}{2} \le \frac{|a_p - a_q| + |b_p - b_q|}{2} \le \frac{(c - m_r) + (M_r - c)}{2} = \frac{D_r}{2}.$$

Taking the largest such difference gives $D_{r+1} \le D_r/2$. $\square$

**Theorem 2 (approximate agreement).** Let $\Delta \ge D_0$ and $R = \lceil \log_2(\Delta/\varepsilon) \rceil$ when $\Delta > \varepsilon$, and $R = 0$ otherwise. After $R$ rounds the outputs of the correct processes satisfy agreement, validity and termination.

*Proof.* Termination: each process runs a fixed number $R$ of rounds and outputs. Validity: by Theorem 1 and [induction](/induction/) on $r$, $[m_r, M_r] \subseteq [m_0, M_0]$, the range of the correct inputs. Agreement: by Theorem 1 and induction, $D_R \le D_0 / 2^R \le \Delta / 2^R$. If $R = 0$ then $D_0 \le \Delta \le \varepsilon$. Otherwise $2^R \ge \Delta / \varepsilon$, so $D_R \le \varepsilon$. $\square$

**The factor $1/2$ is tight for this rule.** Take $n = 4$, $t = 1$, correct values $0, 1, 1$. The faulty process sends $-1000$ to the process with value 0, which keeps $0, 1$ and moves to $1/2$, and $+1000$ to the others, which keep $1, 1$ and stay at 1. The spread goes from 1 to $1/2$.

**Where $n > 3t$ is used.** Only in Lemma 2, to have $t + 1$ correct values at least $u_{t+1}$. With $n = 3t$ the lemma fails, and the run with $n = 3$, $t = 1$ on the page shows that the spread can stay the same forever.
