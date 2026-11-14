---
title: The maxT step-down procedure is closed testing with permutation tests of the maximum, and it controls the family-wise error rate strongly under the randomization hypothesis for the true nulls
proves: [correctness]
status: full
---

We prove four things about MAXT-STEP-DOWN. First, the lines compute the adjusted p-values of the formula on the page (Lemma 1). Second, these are exactly the adjusted p-values of the closed testing procedure whose local test of $H_I$ is the permutation test of $\max_{j \in I}T_j$ (Theorem 2). Third, the procedure controls the family-wise error rate strongly in finite samples when the joint law of the true-null part of the data is invariant under the group (Theorem 3). Fourth, the step-down adjusted p-values lie between the marginal and the single-step ones (Proposition 4). All four are proved here. The gain in power over Holm is only measured, in the tests.

**Setting.** Data $Z$ take values in a set $\mathcal Z$ on which a finite group $G$ acts, with $B = |G|$. Statistics $T_1, \dots, T_m : \mathcal Z \to \mathbb R$, with observed values $t_j = T_j(Z)$. Write $T_j(g) = T_j(gZ)$ for the row of $g$; the identity $e$ gives $T_j(e) = t_j$. Line L1 sorts so that $t_{(1)} \ge \dots \ge t_{(m)}$, where $(k)$ is the index of rank $k$; ties are broken by the sort and do not affect any statement below. Let $S_k = \{(k), \dots, (m)\}$ be the tail of ranks $k$ and later. For a nonempty set $I$ of indices, let $M_I(g) = \max_{j \in I}T_j(g)$ and define the local p-value
$$\hat p_I = \frac{\#\{g \in G : M_I(g) \ge M_I(e)\}}{B}.$$
In the two-sample case $G$ is the symmetric group on the $n$ units, and the statistics depend on $g$ only through the set of units it puts in group 1; by Claim 1 in the proof for the [permutation test](/permutation-test/), counting over the $\binom n{n_1}$ splits gives the same fractions as counting over $G$.

**Lemma 1 (what the lines compute).** For each $k$, the count at line L5 equals $\#\{g : M_{S_k}(g) \ge t_{(k)}\}$, and line L7 returns
$$\tilde p_{(k)} = \max_{j \le k}\hat p_{S_j}.$$

*Proof.* For a fixed row $g$, the loop at lines L3 to L5 runs $k$ from $m$ down to 1 and keeps $u = \max_{l \ge k}T_{(l)}(g) = M_{S_k}(g)$ after line L4, by induction on $m - k$. So line L5 adds 1 to count$[k]$ exactly when $M_{S_k}(g) \ge t_{(k)}$. Since the ranks are sorted by decreasing $t$, $M_{S_k}(e) = \max_{l \ge k}t_{(l)} = t_{(k)}$, so count$[k]/B = \hat p_{S_k}$. Lines L6 and L7 take the running maximum. $\square$

**Theorem 2 (closed testing).** For every $i$, $\tilde p_i = \max\{\hat p_I : i \in I\}$. So rejecting $\{i : \tilde p_i \le \alpha\}$ is the closed testing procedure with local tests "reject $H_I$ when $\hat p_I \le \alpha$".

*Proof.* Let $i$ have rank $k$. Each tail $S_j$ with $j \le k$ contains $i$, so by Lemma 1, $\tilde p_i \le \max\{\hat p_I : i \in I\}$. Conversely, take any $I$ that contains $i$, and let $j$ be the smallest rank in $I$; then $j \le k$ and $I \subseteq S_j$. Since the ranks are sorted by decreasing $t$, $M_I(e) = t_{(j)} = M_{S_j}(e)$. For every $g$, $M_I(g) \le M_{S_j}(g)$, because $I \subseteq S_j$. So every $g$ counted in $\hat p_I$, with $M_I(g) \ge t_{(j)}$, also has $M_{S_j}(g) \ge t_{(j)}$, and $\hat p_I \le \hat p_{S_j} \le \tilde p_i$. Closed testing rejects $H_i$ when every $H_I$ with $i \in I$ is rejected, that is, when $\max_{I \ni i}\hat p_I \le \alpha$. $\square$

**The assumption.** Let $I_0$ be the set of true nulls, $m_0 = |I_0| \ge 1$. Assume that each $T_j$ with $j \in I_0$ is a function $T_j(z) = f_j(\pi(z))$ of a part $\pi(z)$ of the data, the null part, that the action of $G$ passes to the null part, $\pi(gz) = g\pi(z)$, and that
$$g\pi(Z) \text{ has the same law as } \pi(Z) \text{ for every } g \in G. \tag{RH}$$
In the two-sample case, $\pi(Z)$ is the $n \times m_0$ table of the true-null variables, $g$ permutes its rows, and (RH) holds when these rows are exchangeable; for example when the units are independent and the vector of null variables has the same joint law in the two groups. Nothing is assumed about the other variables or about the dependence between the statistics.

**Theorem 3 (strong FWER control).** Under (RH), for every $\alpha \in (0, 1)$, the procedure that rejects $\{i : \tilde p_i \le \alpha\}$ has $P(V \ge 1) \le \alpha$.

*Proof.* By Lemma 1 the adjusted p-values are nondecreasing in the rank, so the rejected set is a set of ranks $1, \dots, r$. Let $k^*$ be the smallest rank of a true null. If any true null is rejected, then rank $k^*$ is rejected, so $\hat p_{S_{k^*}} \le \tilde p_{(k^*)} \le \alpha$. All true nulls have rank at least $k^*$, so $I_0 \subseteq S_{k^*}$, and by the argument in the proof of Theorem 2, with $I = I_0$ and $j = k^*$, $\hat p_{I_0} \le \hat p_{S_{k^*}}$. Hence
$$\{V \ge 1\} \subseteq \{\hat p_{I_0} \le \alpha\}.$$
Now $\hat p_{I_0}$ is the permutation p-value of the single statistic $M_{I_0}(z) = \max_{j \in I_0}f_j(\pi(z))$, which is a function of the null part only. Under (RH), Claim 2 in the proof for the permutation test, applied to the data $\pi(Z)$, the group $G$ and the statistic $\max_{j \in I_0}f_j$, gives $P(\hat p_{I_0} \le \alpha) \le \alpha$. For completeness, the argument is this. Let $g_0$ be uniform on $G$ and independent of $Z$. By (RH), $\pi(Z)$ and $g_0\pi(Z)$ have the same law, so $\hat p_{I_0}$ has the same law as the p-value computed from $g_0\pi(Z)$. Since $\{gg_0 : g \in G\} = G$, that p-value is the rank of $v_{g_0}$ among the values $v_g = M_{I_0}(g\pi(Z))$, $g \in G$, divided by $B$, where the rank of $v_h$ is $\#\{g : v_g \ge v_h\}$. Given $Z$, $g_0$ is uniform, and by the rank lemma at most $\alpha B$ elements have rank at most $\alpha B$, so the conditional probability is at most $\alpha$. $\square$

The proof uses the permuted statistics of the false nulls only through the inequality $M_{I_0}(g) \le M_{S_{k^*}}(g)$, which holds whatever they are. This is why no condition on the false nulls is needed. It also shows which condition on the true nulls is needed: (RH) for the joint law of all of them, not for each one separately.

**Random permutations.** If $G$ is replaced by the identity together with $b$ elements drawn independently and uniformly from $G$, the count $\hat p_{I_0} = (1 + c)/(1 + b)$ is still valid, by Claim 3 in the proof for the permutation test, and the proof of Theorem 3 goes through with that claim in place of Claim 2. Lemma 1 and Theorem 2 are statements about any table of rows, so they hold unchanged.

**Proposition 4 (order).** For each $i$, with marginal p-value $p_i^{\text{marg}} = \#\{g : T_i(g) \ge t_i\}/B$ and single-step p-value $p_i^{\text{ss}} = \#\{g : \max_lT_l(g) \ge t_i\}/B$,
$$p_i^{\text{marg}} \le \tilde p_i \le p_i^{\text{ss}}.$$

*Proof.* Let $i$ have rank $k$. The marginal p-value is $\hat p_{\{i\}}$, which is at most $\tilde p_i$ by Theorem 2. For $j \le k$, $M_{S_j}(g) \le \max_lT_l(g)$ and $t_{(j)} \ge t_{(k)} = t_i$, so $\{g : M_{S_j}(g) \ge t_{(j)}\} \subseteq \{g : \max_lT_l(g) \ge t_i\}$, and each term of the maximum in Lemma 1 is at most $p_i^{\text{ss}}$. $\square$

So the step-down procedure rejects every hypothesis that the single-step maxT procedure rejects, and no hypothesis whose marginal permutation test does not reject.

**What is measured, not proved.** The tests check Lemma 1 and Theorem 2 against closed testing over all subsets, on random integer tables and on two-sample data with all 70 splits of 8 units, in exact rational arithmetic, and Proposition 4 on random tables. They measure the FWER (0.030 at $\alpha = 0.05$) and the power in one correlated model. That maxT beats Holm on correlated data is an observation in that model, not a theorem; there is no general inequality between the two, since Holm uses marginal p-values and maxT uses raw statistics on possibly different scales.
