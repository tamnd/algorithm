---
title: Hochberg's step-up procedure lies inside closed Simes testing, so it controls the family-wise error rate whenever the Simes inequality holds
proves: [correctness]
status: full
---

We prove that HOCHBERG computes the step-up rule and its adjusted p-values (Lemma 1), that it rejects every hypothesis Holm rejects (Theorem 1), that every hypothesis it rejects is rejected by closed testing with Simes local tests (Theorem 2), that the Simes test has size exactly $\alpha$ for independent uniform p-values (Theorem 3), and hence that HOCHBERG controls the family-wise error rate strongly under independence (Corollary 4). The Simes inequality under MTP2 dependence (Sarkar 1998) and under other positive dependence (Sarkar and Chang 1997) is cited, not proved; Corollary 4 extends to those cases word for word. Finally we give a law under which the guarantee fails (Theorem 5). The tests check Theorems 1 and 2 against brute force, Theorem 3 by exact counting and simulation, and Theorem 5 in exact arithmetic.

**Setting.** P-values $p_1, \dots, p_m$, sorted as $p_{(1)} \le \dots \le p_{(m)}$ by line L1; $(k)$ is the index of rank $k$. $I_0$ is the set of true nulls, $m_0 = |I_0|$. For a nonempty set $I$ with $n = |I|$, $p_{(j:I)}$ is the $j$-th smallest of $\{p_i : i \in I\}$. The Simes test of $H_I$ rejects when $p_{(j:I)} \le j\alpha/n$ for some $j \in \{1, \dots, n\}$. Fix $0 < \alpha < 1$.

**Lemma 1 (what the lines compute).** Lines L2 and L3 end with $k = r = \max\{k : (m - k + 1)p_{(k)} \le \alpha\}$, or $r = 0$ if there is no such $k$, and line L4 rejects ranks $1, \dots, r$. Lines L5 to L7 give $\tilde p_{(j)} = \min_{l \ge j}\min(1, (m - l + 1)p_{(l)})$, and rank $j$ is rejected if and only if $\tilde p_{(j)} \le \alpha$.

*Proof.* The loop starts at $k = m$ and decreases $k$ while the test fails, so it stops at the largest $k$ that passes, or at 0. The running minimum starts at 1 and takes in the products from rank $m$ down, which is the formula. Rank $j$ is rejected if and only if $j \le r$, that is, if and only if some $l \ge j$ has $(m - l + 1)p_{(l)} \le \alpha$; since $\alpha < 1$, this is $\tilde p_{(j)} \le \alpha$. $\square$

**Theorem 1 (Hochberg contains Holm).** If Holm rejects $H_i$, so does HOCHBERG.

*Proof.* Holm rejects the ranks $1, \dots, s$, where every $j \le s$ has $(m - j + 1)p_{(j)} \le \alpha$. In particular rank $s$ passes, so $r \ge s$ in Lemma 1, and HOCHBERG rejects ranks $1, \dots, r \supseteq \{1, \dots, s\}$. $\square$

**Theorem 2 (Hochberg lies inside closed Simes testing).** Suppose HOCHBERG rejects $r \ge 1$ hypotheses, and let $I$ be any set that contains a rejected hypothesis. Then the Simes test rejects $H_I$.

*Proof.* Let $a = m - r + 1$, so that $p_{(r)} \le \alpha/a$ by Lemma 1, and let $n = |I|$. At most $m - r = a - 1$ indices have rank above $r$, so at least $n - a + 1$ elements of $I$ have rank at most $r$. Also at least one does, the rejected hypothesis in $I$. Let $j = \max(1, n - a + 1)$. Then at least $j$ elements of $I$ have p-values at most $p_{(r)}$, so $p_{(j:I)} \le p_{(r)} \le \alpha/a$. It remains to show $\alpha/a \le j\alpha/n$, that is, $n \le ja$.
- If $n \le a$, then $j = 1$ and $n \le a = ja$.
- If $n > a$, then $j = n - a + 1$ and $ja - n = (n - a + 1)a - n = (a - 1)(n - a) \ge 0$, since $a \ge 1$ and $n > a$.

In both cases $p_{(j:I)} \le j\alpha/n$, so the Simes test rejects $H_I$. $\square$

So with $I = I_0$: if HOCHBERG rejects any true null, then $I_0$ contains a rejected hypothesis, and the Simes test of the null p-values rejects $H_{I_0}$. Hence
$$P(V \ge 1) \le P\big(p_{(j:I_0)} \le j\alpha/m_0 \text{ for some } j\big). \tag{1}$$
Theorem 2 also says that every Hochberg rejection is a rejection of the closed procedure with Simes local tests, which is Hommel's procedure; the [closed testing principle](/closed-testing-principle/) gives the same bound (1). Only the Simes test of the one set $I_0$ matters.

**Theorem 3 (Simes 1986).** Let $U_1, \dots, U_n$ be independent and uniform on $(0, 1)$, and $0 \le \alpha \le 1$. Then $P(U_{(j)} \le j\alpha/n \text{ for some } j) = \alpha$.

*Proof.* By induction on $n$. For $n = 1$ the event is $U_1 \le \alpha$, of probability $\alpha$. Let $n \ge 2$ and assume the claim for $n - 1$ and every level in $[0, 1]$. Let $M = U_{(n)}$, which has density $nu^{n-1}$ on $(0, 1)$. Given $M = u$, the other $n - 1$ values are independent and uniform on $(0, u)$; after division by $u$ they are independent and uniform on $(0, 1)$, with order statistics $W_{(1)} \le \dots \le W_{(n-1)}$.
- If $u \le \alpha$, the event holds with $j = n$.
- If $u > \alpha$, the condition at $j = n$ fails, and for $j < n$ it reads $uW_{(j)} \le j\alpha/n$, that is, $W_{(j)} \le j\alpha'/(n - 1)$ with $\alpha' = \alpha(n - 1)/(nu)$. Since $u > \alpha$, $\alpha' < 1$, so by the induction hypothesis the conditional probability is $\alpha'$.

So
$$P = \int_0^\alpha nu^{n-1}\,du + \int_\alpha^1 nu^{n-1}\cdot\frac{\alpha(n - 1)}{nu}\,du = \alpha^n + \alpha(n - 1)\int_\alpha^1 u^{n-2}\,du = \alpha^n + \alpha(1 - \alpha^{n-1}) = \alpha. \qquad \square$$

**Corollary 4 (strong control under independence).** If the null p-values are independent and uniform, HOCHBERG has $P(V \ge 1) \le \alpha$ for every $I_0$, whatever the false null p-values are and however they depend on the null ones.

*Proof.* Bound (1) involves only the null p-values, and Theorem 3 with $n = m_0$ shows that its right side equals $\alpha$. $\square$

If the null p-values are only valid, $P(p_i \le u) \le u$, and independent, then each is stochastically larger than a uniform, the Simes event is a decreasing event in the p-values, and its probability is at most the uniform value $\alpha$. The tests confirm that on grids of discrete uniform p-values the probability is at most $\alpha$, with equality for $m = 2$ when both thresholds are grid points. Under MTP2 dependence the right side of (1) is at most $\alpha$ by Sarkar (1998), and for the positively dependent families of Sarkar and Chang (1997) as well; with those cited results Corollary 4 holds for them.

**Theorem 5 (failure under negative dependence).** Let $m = m_0 = 2$ and $0 < \alpha \le 1/2$. There is a joint law of $(p_1, p_2)$ with uniform marginals under which HOCHBERG has $P(V \ge 1) = 3\alpha/2$, while Holm has $P(V \ge 1) = \alpha$.

*Proof.* Split $(0, 1]$ into $B = (0, \alpha/2]$, $A = (\alpha/2, \alpha]$ and $C = (\alpha, 1]$, of lengths $\alpha/2$, $\alpha/2$ and $1 - \alpha$. Let the pair fall in $A \times A$ with probability $\alpha/2$, in $B \times C$ with probability $\alpha/2$, in $C \times B$ with probability $\alpha/2$ and in $C \times C$ with probability $1 - 3\alpha/2$, uniformly inside each block. The mass of $p_1$ in $B$ is $\alpha/2$, in $A$ is $\alpha/2$, and in $C$ is $\alpha/2 + 1 - 3\alpha/2 = 1 - \alpha$, each spread uniformly, so $p_1$ is uniform; the same holds for $p_2$. HOCHBERG rejects something when $\max(p_1, p_2) \le \alpha$ or $\min(p_1, p_2) \le \alpha/2$. The first event is $A \times A$, and the second is $B \times C \cup C \times B$; they are disjoint, so the error rate is $3\alpha/2$. Holm rejects something only when $\min(p_1, p_2) \le \alpha/2$, which has probability $\alpha$. $\square$

The tests build this law on the grid $\{1/40, \dots, 40/40\}$ with $\alpha = 1/10$ and confirm both numbers exactly.

**Termination and cost.** The sort terminates, and the two loops run at most $m$ times each with constant work per step.
