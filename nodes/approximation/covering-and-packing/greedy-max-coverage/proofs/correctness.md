---
title: Greedy maximum coverage covers at least 1 − (1 − 1/k)^k of the optimum
proves: [correctness]
status: full
---

The input is a family of sets $S_1, \ldots, S_m$ and an integer $k \ge 1$. For a list $A$ of indices, $\text{cov}(A) = |\bigcup_{j \in A} S_j|$. OPT is the largest value of $\text{cov}(A)$ over the lists of at most $k$ distinct indices, and $O$ is such a list with $\text{cov}(O) = \text{OPT}$. Let $G_i$ be the list of the first $i$ sets chosen by GREEDY-MAX-COVERAGE, $R_i = \bigcup_{j \in G_i} S_j$, and $c_i = |R_i|$, so $c_0 = 0$.

**Lemma 1 (feasibility).** The output holds at most $k$ distinct indices, and the returned set of elements is $R_t$, where $t$ is the number of chosen sets.

*Proof.* Line L2 runs at most $k$ times, and line L5 appends one index per run. Line L5 runs only when the gain in line L3 is positive. A set already in $G_i$ has gain $|S_j \setminus R_i| = 0$, so it is never chosen again. Line L5 adds $S_j$ to the covered set each time it appends $j$, so the covered set is $R_t$. $\square$

**Lemma 2 (the step inequality).** If the loop picks a set in round $i + 1$, then

$$\text{OPT} - c_{i+1} \le \left(1 - \frac{1}{k}\right)(\text{OPT} - c_i).$$

*Proof.* The sets of $O$ cover OPT elements, and at most $c_i$ of them are in $R_i$. So at least $\text{OPT} - c_i$ elements of $\bigcup_{j \in O} S_j$ are not in $R_i$. Each of them is in a set of $O$, and $O$ has at most $k$ sets, so some $j \in O$ has

$$|S_j \setminus R_i| \ge \frac{\text{OPT} - c_i}{k}.$$

Line L3 picks a set with the largest gain, so $c_{i+1} - c_i \ge (\text{OPT} - c_i)/k$. Subtract both sides from $\text{OPT} - c_i$. $\square$

**Lemma 3 (an early stop is optimal).** If the loop stops in line L4 after $i$ picks, then $c_i \ge \text{OPT}$.

*Proof.* Line L4 stops only when each set has gain 0, so each set of the family, and in particular each set of $O$, is a subset of $R_i$. So $\bigcup_{j \in O} S_j \subseteq R_i$ and $\text{OPT} \le c_i$. $\square$

**Theorem.** GREEDY-MAX-COVERAGE returns at most $k$ sets that cover

$$\text{ALG} \ge \left(1 - \left(1 - \frac{1}{k}\right)^k\right) \text{OPT} \ge \left(1 - \frac{1}{e}\right) \text{OPT}$$

elements, in the worst case.

*Proof.* If the loop stops early, Lemma 3 gives ALG $\ge$ OPT. Else the loop makes $k$ picks, and Lemma 2 holds for $i = 0, 1, \ldots, k - 1$. Since $\text{OPT} - c_0 = \text{OPT}$, induction on $i$ gives

$$\text{OPT} - c_i \le \left(1 - \frac{1}{k}\right)^i \text{OPT} \quad \text{for } i = 0, 1, \ldots, k.$$

With $i = k$ this is ALG $= c_k \ge (1 - (1 - 1/k)^k)\,\text{OPT}$. Finally, $1 - x \le e^{-x}$ for each real $x$, so $(1 - 1/k)^k \le e^{-1}$. $\blacksquare$

**Remark.** The proof uses two facts about the function $\text{cov}$: adding sets never lowers it (monotonicity), and the gain of a set never grows when more sets are already chosen (submodularity). The second fact is used in Lemma 2, where the gains of the sets of $O$ over $R_i$ add up to at least the number of elements of $O$ not in $R_i$. The [Nemhauser-Wolsey-Fisher theorem](/nemhauser-wolsey-fisher-theorem/) proves the same bound for each monotone submodular function.
