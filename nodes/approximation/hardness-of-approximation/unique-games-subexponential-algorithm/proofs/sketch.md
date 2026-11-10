---
title: The ABS algorithm, with enumeration and the label-extended bound in full and the decomposition cited
proves: [statement]
status: sketch
---

This file follows Arora, Barak and Steurer, Sections 2, 4 and 5 of the full version. It proves in full the eigenspace enumeration (their Theorem 2.2), the bound on the label-extended graph (their Lemma 5.2) and the final count (their Lemma 5.4). The decomposition theorem (their Theorem 4.1, in the trace form of their Theorem 4.5) and the rank bound for small-set expanders (their Theorem 2.3) are cited, and their proofs are only outlined. Constants are not tracked.

## Notation

A regular graph $G$ on vertex set $V$, $|V| = N$, is identified with its symmetric stochastic matrix. Its eigenvalues are $1 = \lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_N \ge -1$. For $S \subseteq V$ the *expansion* is $\Phi(S) = \Pr_{(i,j)}[j \notin S \mid i \in S]$ for a random edge, the measure is $\mu(S) = |S|/N$, and $\operatorname{rank}_{\tau}(G)$ is the number of eigenvalues with $|\lambda| > \tau$. The graph is *lazy* if half of the weight at each vertex is a self-loop. A lazy graph has all eigenvalues in $[0, 1]$. For $\eta \in (0,1)$ the *trace rank* is

$$\operatorname{rank}^*_{1-\eta}(G) = \inf_{t \ge 1} \frac{\operatorname{Tr}(G^{2t})}{(1-\eta)^{2t}} \ge \operatorname{rank}_{1-\eta}(G),$$

where the inequality holds because each eigenvalue above $1 - \eta$ adds more than $(1-\eta)^{2t}$ to the trace and the others add a nonnegative amount.

## Eigenspace enumeration, in full

**Claim (Theorem 2.2).** Let $m = \operatorname{rank}_{1-\eta}(G)$. There is an algorithm of time $\exp(O(m \log(1/\varepsilon))) \operatorname{poly}(N)$ that outputs a list of sets with the following property: if $S \subseteq V$ has $\Phi(S) \le \varepsilon$, some listed set has symmetric difference with $S$ of size at most $8(\varepsilon/\eta)|S|$.

*Proof.* Let $\delta = \mu(S)$, and let $\chi_S$ be the vector with $\chi_S(i) = 1/\sqrt{\delta}$ for $i \in S$ and $0$ otherwise, normalized so that $\frac1N \sum_i \chi_S(i)^2 = 1$. With this inner product $\langle \chi_S, G \chi_S \rangle = 1 - \Phi(S) \ge 1 - \varepsilon$. Let $U$ be the span of the eigenvectors with eigenvalue above $1 - \eta$, so $\dim U \le m$. Write $\chi_S = \sqrt{1-\gamma}\, u + \sqrt{\gamma}\, u^\perp$ with unit vectors $u \in U$ and $u^\perp \perp U$. The space $U$ is invariant under $G$, so the cross terms vanish and

$$1 - \varepsilon \le (1 - \gamma)\langle u, Gu\rangle + \gamma \langle u^\perp, G u^\perp\rangle \le (1 - \gamma) + \gamma(1 - \eta) = 1 - \gamma\eta .$$

So $\gamma \le \varepsilon/\eta$, and $\|\chi_S - \sqrt{1-\gamma}\,u\|^2 = \gamma \le \varepsilon/\eta$. Enumerate a $\sqrt{\varepsilon/\eta}$-net of the unit ball of $U$, which has $\exp(O(m \log(\eta/\varepsilon)))$ points. With a net of radius $(\sqrt2 - 1)\sqrt{\varepsilon/\eta}$, which still has $\exp(O(m \log(\eta/\varepsilon)))$ points, some net point $v$ has $\|v - \chi_S\| \le \sqrt{\gamma} + (\sqrt2 - 1)\sqrt{\varepsilon/\eta} \le \sqrt{2\varepsilon/\eta}$. For each net point $v$ and each of the $N$ possible values of $|S|$, list the set $S' = \{ i : v_i \ge 1/(2\sqrt{\delta}) \}$. A vertex in the symmetric difference of $S$ and $S'$ has $|v_i - \chi_S(i)| \ge 1/(2\sqrt\delta)$, so it adds at least $\frac{1}{4\delta N}$ to $\|v - \chi_S\|^2$. So at most $4\delta N \cdot 2\varepsilon/\eta = 8(\varepsilon/\eta)|S|$ vertices differ. $\square$

## The label-extended graph, in full

For a unique game on a constraint graph $G$ with label set $[k]$, the *label-extended graph* $\hat G$ has vertex set $V \times [k]$, and each constraint $(i, j, \pi)$ of weight $w$ gives edges of weight $w$ from $(i, a)$ to $(j, \pi(a))$ for every $a$. Each cloud $C_i = \{i\} \times [k]$ has the same weights as $i$, so $\hat G$ is regular and stochastic. A labeling $\ell$ gives the set $S_\ell = \{(i, \ell(i))\}$, with one vertex per cloud, and $\Phi(S_\ell)$ equals the fraction of constraints that $\ell$ violates.

**Claim (Lemma 5.2).** If $G$ is lazy, then $\operatorname{rank}^*_{1-\eta}(\hat G) \le k \cdot \operatorname{rank}^*_{1-\eta}(G)$.

*Proof.* The entry $(\hat G^t)_{(i,a),(i,a)}$ is the total weight of closed walks of length $t$ from $i$ in $G$ whose composed bijection fixes $a$. Summing over $a$, each closed walk of $G$ is counted once for each fixed point of its composed bijection, which is at most $k$. So $\operatorname{Tr}(\hat G^{t}) \le k \operatorname{Tr}(G^{t})$ for every $t$, and the claim follows from the definition of the trace rank. The self-loops with the identity bijection keep $\hat G$ lazy, so its eigenvalues are nonnegative. $\square$

## The cited results, in outline

**Rank bound for small-set expanders (Theorem 2.3, cited).** If $G$ is regular and $\operatorname{rank}_{1-\eta}(G) \ge N^{100\eta/\gamma}$, then some set of at most $N^{1 - \eta/\gamma}$ vertices has expansion at most $\sqrt{\gamma}$. *Outline.* The trace $\operatorname{Tr}(G^{2t}) = \sum_i \|G^t e_i\|^2$ is at least $m (1 - \eta)^{2t}$ for $m = \operatorname{rank}_{1-\eta}(G)$. So for some start vertex $i$ the $t$-step random walk has collision probability at least $m(1-\eta)^{2t}/N$, which is large compared with the uniform value $1/N$. A local form of Cheeger's inequality then finds a level set of the vector $(\tfrac12 I + \tfrac12 G)^t e_i$ that is small and has small expansion. The proof goes through a bound on Schatten norms (their Theorem 3.1).

**Decomposition (Theorems 4.1 and 4.5, cited).** In polynomial time, the vertices of $G$ can be split into parts $A_1, \ldots, A_q$ such that at most an $O(\varepsilon \log(1/\varepsilon))$ fraction of the edges cross between parts and each induced graph, made regular by self-loops, has $\operatorname{rank}^*_{1-\varepsilon^5}(G[A_t]) \le N^{100\varepsilon}$. *Outline.* With $\eta = \varepsilon^5$ and $\gamma = \varepsilon^4$, Theorem 2.3 finds, in any part of high rank, a set of at most $N^{1-\varepsilon}$ vertices with expansion $O(\varepsilon^2)$. Cut such sets off one by one, and charge each cut edge to the set it leaves. Each set pays $O(\varepsilon^2)$ times its size. Recurse into the removed sets. Each level of recursion shrinks the sets by a factor $N^{-\varepsilon}$, so after $O(\varepsilon^{-1}\log(1/\varepsilon))$ levels only sets of size at most $N^{\varepsilon}$ can still have high rank, and these have rank at most their size. Each vertex is charged $O(\varepsilon^2)$ per level, which gives the total cost $O(\varepsilon \log(1/\varepsilon))$.

## The algorithm and its analysis

Input: a unique game on $G$ with $n$ vertices, $k$ labels and value at least $1 - \varepsilon^6$.

1. Make $G$ lazy with identity self-loops. The optimal labeling now violates at most an $\varepsilon^6/2$ fraction of the weight, and a labeling that violates a $\beta$ fraction of the lazy game violates at most $2\beta$ of the original.
2. Apply the decomposition to get $A_1, \ldots, A_q$, and drop the crossing constraints.
3. For each $t$, the label-extended graph of the part is $\hat G[\hat A_t]$ with $\hat A_t = A_t \times [k]$. By Lemma 5.2, $\operatorname{rank}_{1-\varepsilon^5}(\hat G[\hat A_t]) \le \operatorname{rank}^*_{1-\varepsilon^5}(\hat G[\hat A_t]) \le k n^{100\varepsilon}$.
4. Run the enumeration with $\eta = \varepsilon^5$ on each $\hat G[\hat A_t]$. For each listed set $S$, define a labeling of $A_t$ that gives $i$ a label from $S \cap C_i$ when it is not empty, and an arbitrary label otherwise. Keep the best labeling of each part.

*Time.* Step 4 takes $\exp(O(k n^{100\varepsilon} \log(1/\varepsilon))) \operatorname{poly}(n)$ time per part, and there are at most $n$ parts.

**Claim (Lemma 5.4).** Let $\varepsilon_t$ be the fraction of the constraints inside $A_t$ that the optimal labeling violates. The labeling kept for $A_t$ violates at most a $40\varepsilon_t/\eta$ fraction of them.

*Proof.* The set $S_{\mathrm{opt}}$ of the optimal labeling in $\hat A_t$ has $|A_t|$ vertices and expansion at most $\varepsilon_t$ in $\hat G[\hat A_t]$. The list contains a set $S$ with $|S \triangle S_{\mathrm{opt}}| \le 8(\varepsilon_t/\eta)|A_t|$. The labeling built from $S$ gives a set $S'$ with one vertex per cloud and $S' \cap C_i \subseteq S \cap C_i$ when the latter is not empty, so $|S \triangle S'| = \sum_i \big| |S \cap C_i| - 1 \big| \le |S \triangle S_{\mathrm{opt}}|$, since $S_{\mathrm{opt}}$ has exactly one vertex per cloud. So $S'$ and $S_{\mathrm{opt}}$ differ in at most $16(\varepsilon_t/\eta)|A_t|$ vertices, and the labelings differ on at most a $16\varepsilon_t/\eta$ fraction of $A_t$. Each changed vertex can break only the constraints at that vertex, and in a regular graph the constraints at a $\beta$ fraction of the vertices are at most a $2\beta$ fraction of all constraints. So the built labeling violates at most $\varepsilon_t + 32\varepsilon_t/\eta \le 40\varepsilon_t/\eta$ of the constraints of $A_t$. The kept labeling is at least as good. $\square$

*Count.* Let $\mu_t$ be the weight of the constraints inside $A_t$, as a fraction of the total weight. The optimal labeling violates at most an $\varepsilon^6/2$ fraction of the lazy weight, so $\sum_t \mu_t \varepsilon_t \le \varepsilon^6/2$. The output violates at most $\sum_t \mu_t \cdot 40\varepsilon_t/\eta \le 20\varepsilon^6/\varepsilon^5 = 20\varepsilon$ of the total weight inside the parts, plus the $O(\varepsilon \log(1/\varepsilon))$ fraction of cut constraints. Undoing the lazy step at most doubles this. So the output satisfies a $1 - O(\varepsilon \log(1/\varepsilon))$ fraction of the constraints. $\blacksquare$
