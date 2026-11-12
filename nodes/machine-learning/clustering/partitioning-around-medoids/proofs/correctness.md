---
title: PAM stops at a single-swap local optimum, which is within a factor 5 of the optimum in a metric
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a symmetric $n \times n$ dissimilarity matrix $D$ with a zero diagonal and an integer $k$ with $1 \le k \le n$. For a set $M$ of medoids, $\mathrm{cost}(M) = \sum_{j} \min_{m \in M} D[j][m]$. For an object $j$, $D_j$ is its least dissimilarity to $M$, attained at the medoid $m_j$, and $E_j$ its least dissimilarity to $M \setminus \{m_j\}$ (undefined when $k = 1$).

**Lemma 1 (BUILD).** Line L5 adds an object $i \notin M$ that minimizes $\mathrm{cost}(M \cup \{i\})$, and BUILD returns $k$ distinct objects.

*Proof.* Before line L4, $\mathrm{near}[j] = \min_{m \in M} D[j][m]$: this holds after line L2, and line L5 keeps it because $\min(\mathrm{near}[j], D[j][i]) = \min_{m \in M \cup \{i\}} D[j][m]$. So $\mathrm{cost}(M \cup \{i\}) = \sum_j \min(\mathrm{near}[j], D[j][i]) = \mathrm{cost}(M) - \sum_j \max(\mathrm{near}[j] - D[j][i], 0) = \mathrm{cost}(M) - g(i)$. The largest gain gives the least new cost. Line L4 looks only at $i \notin M$, so the medoids are distinct, and the loop of line L3 stops with $|M| = k$. $\square$

**Lemma 2 (the swap change).** For $m \in M$ and $h \notin M$, let $M' = M \setminus \{m\} \cup \{h\}$. Then $\mathrm{cost}(M') - \mathrm{cost}(M) = \sum_j (\mathrm{new}_j - D_j)$, where $\mathrm{new}_j = \min(E_j, D[j][h])$ if $m_j = m$ (and $D[j][h]$ if $k = 1$), and $\mathrm{new}_j = \min(D_j, D[j][h])$ otherwise.

*Proof.* The least dissimilarity of $j$ to $M'$ is the least of its dissimilarities to $M \setminus \{m\}$ and to $h$. If $m_j = m$, the least dissimilarity to $M \setminus \{m\}$ is $E_j$ (and there is none when $k = 1$). If $m_j \ne m$, then $m_j \in M \setminus \{m\}$, and the least dissimilarity to $M \setminus \{m\}$ is still $D_j$. Sum over $j$. $\square$

So line L8 computes the exact change of the cost, in $O(n)$ time per pair once $D_j$, $m_j$ and $E_j$ are known.

**Lemma 3 (termination).** SWAP stops after finitely many passes. If the entries of $D$ are integers, it makes at most $\mathrm{cost}(M_0) - \mathrm{OPT}$ swaps, where $M_0$ is the output of BUILD and $\mathrm{OPT}$ the least cost of $k$ medoids.

*Proof.* Line L10 runs only when line L9 found $T(m, h) < 0$, so by Lemma 2 each swap lowers the cost strictly. So no medoid set occurs twice, and there are $\binom{n}{k}$ sets. With integer entries each swap lowers the cost by at least 1, and the cost never goes below $\mathrm{OPT}$. $\square$

**Theorem 1 (local optimum).** The output $M$ has $k$ distinct medoids, and no replacement of one medoid by one non-medoid lowers $\mathrm{cost}(M)$.

*Proof.* A swap keeps the size and replaces a medoid by a non-medoid, so the medoids stay distinct. SWAP returns at line L9 only when the least $T(m, h)$ over all pairs is at least 0; by Lemma 2 that is the claim. $\square$

**Theorem 2 (locality gap, Arya et al. 2004 with $p = 1$).** If $D$ is a metric (a pseudometric suffices), each set $S$ of $k$ medoids with the property of Theorem 1 has $\mathrm{cost}(S) \le 5\,\mathrm{OPT}$.

*Proof.* Let $O$ be an optimal set of $k$ medoids. For an object $j$, let $S_j = d(j, S)$ and $O_j = d(j, O)$, attained at $s_j \in S$ and $o_j \in O$. Let $N_S(s)$ be the objects with $s_j = s$, and $N_O(o)$ the objects with $o_j = o$. Each $o \in O$ is *captured* by a nearest point $\eta(o) \in S$ to $o$ (ties broken in a fixed way).

*The pairs.* Let $S_0$, $S_1$ and $S_{2}$ be the points of $S$ that capture no point, exactly one point and at least two points of $O$. Pair each $s \in S_1$ with the one point it captures. Let $R$ be the number of the other points of $O$; they are captured by $S_2$, so $|S_2| \le R/2$. Since $|S| = |O| = k$, we have $|S_0| + |S_2| = k - |S_1| = R$, so $|S_0| \ge R/2$. Pair the $R$ other points of $O$ with points of $S_0$, each point of $S_0$ used at most twice. Now each $o \in O$ is in exactly one pair, each $s \in S$ is in at most two pairs, and in each pair $(s, o)$ the point $s$ captures no point of $O$ other than $o$.

*One pair.* Fix a pair $(s, o)$ and let $S' = S \setminus \{s\} \cup \{o\}$. If $o \notin S$, this is a single swap, so $\mathrm{cost}(S') \ge \mathrm{cost}(S)$ by the local optimality. If $o \in S$, then $S'$ is $S$ or $S$ without $s$, and again $\mathrm{cost}(S') \ge \mathrm{cost}(S)$, because removing a medoid does not lower the cost. Bound $\mathrm{cost}(S')$ by a particular assignment:

- an object $j \in N_O(o)$ goes to $o$, at dissimilarity $O_j$;
- an object $j \in N_S(s) \setminus N_O(o)$ goes to $s' = \eta(o_j)$. Here $o_j \ne o$, so $s$ does not capture $o_j$, and $s' \ne s$ is in $S'$. By the triangle inequality and the choice of $s'$ as nearest to $o_j$, $d(j, s') \le d(j, o_j) + d(o_j, s') \le O_j + d(o_j, s_j) \le O_j + O_j + S_j$;
- each other object keeps its medoid $s_j \ne s$, which is in $S'$.

So $0 \le \mathrm{cost}(S') - \mathrm{cost}(S) \le \sum_{j \in N_O(o)} (O_j - S_j) + \sum_{j \in N_S(s) \setminus N_O(o)} 2 O_j \le \sum_{j \in N_O(o)} (O_j - S_j) + \sum_{j \in N_S(s)} 2 O_j$.

*All pairs.* Add the $k$ inequalities. Each $o$ occurs once and the sets $N_O(o)$ partition the objects, so the first sums give $\mathrm{OPT} - \mathrm{cost}(S)$. Each $s$ occurs at most twice and the sets $N_S(s)$ partition the objects, so the second sums give at most $4\,\mathrm{OPT}$. So $0 \le \mathrm{OPT} - \mathrm{cost}(S) + 4\,\mathrm{OPT}$, that is, $\mathrm{cost}(S) \le 5\,\mathrm{OPT}$. $\blacksquare$

By Theorem 1, the output of PAM satisfies the hypothesis of Theorem 2. Without the triangle inequality, Theorem 1 still holds but Theorem 2 does not apply.
