---
title: Leaps and bounds returns exactly the best subsets of each size, because a subset never fits better than a superset
proves: [correctness, termination]
status: full
---

The arithmetic is exact. The intercept is in every model, the columns of $X$ together with $\mathbf 1$ are linearly independent, and $\mathrm{RSS}(S)$ is the least squares residual sum of squares of $y$ on $\mathbf 1$ and $X_S$. "Swept on $S$" means the centered cross-product matrix $A$ after the sweeps on the indices of $S$. The facts about sweeps used below are proved as Lemmas 1 to 4 of the proof on the [stepwise regression](/stepwise-regression/) page: the swept matrix depends only on the set; a sweep on $S$ has $A[y,y] = \mathrm{RSS}(S)$; the pivots are nonzero when the columns are independent; and the reverse sweep on $k$ turns the matrix swept on $S$ into the matrix swept on $S \setminus \{k\}$.

**Lemma 1 (the bound).** If $T \subseteq U$ then $\mathrm{RSS}(T) \ge \mathrm{RSS}(U)$.

*Proof.* Let $L_T$ and $L_U$ be the column spaces of $(\mathbf 1, X_T)$ and $(\mathbf 1, X_U)$. Every column of the first matrix is a column of the second, so $L_T \subseteq L_U$. $\mathrm{RSS}(S) = \min_{v \in L_S}\|y - v\|^2$, and a minimum over a larger set is not larger. $\square$

**Lemma 2 (the node invariant).** Whenever $\mathrm{VISIT}(F, C, R, B)$ is called, $F \cap C = \emptyset$, $R$ is swept on $F$, $B$ is swept on $F \cup C$, and both $F$ and $F \cup C$ have been recorded with their exact RSS.

*Proof.* By induction on the calls. The call of line L4 has $F = \emptyset$, $C = \{1, \dots, m\}$, $R = A$ and $B$ swept on all columns by line L2, and line L3 recorded both sets. Suppose the invariant holds at a call that reaches line L8 and picks $j \in C$. Line L9 sweeps $R$ on $j \notin F$, so $R'$ is swept on $F \cup \{j\}$, and records $F \cup \{j\}$ with $R'[y,y] = \mathrm{RSS}(F \cup \{j\})$. The call of line L10 has the sets $F \cup \{j\}$ and $C \setminus \{j\}$, whose union is $F \cup C$, recorded before; so the invariant holds there. Line L11 reverse sweeps $B$ on $j \in F \cup C$, so $B'$ is swept on $(F \cup C) \setminus \{j\}$, and records that set with its exact RSS. The call of line L12 has the sets $F$, recorded before, and $C \setminus \{j\}$, with union $(F \cup C) \setminus \{j\}$, just recorded. $R$ is unchanged and still swept on $F$. Every pivot is nonzero because every set involved is a subset of $\{1, \dots, m\}$, whose columns are independent with $\mathbf 1$. $\square$

**Lemma 3 (termination).** The search makes at most $2^{m+1} - 1$ calls of VISIT.

*Proof.* Each call that branches makes two calls with $|C|$ smaller by 1, and a call with $C = \emptyset$ makes none. So the calls form a binary tree of depth at most $m$, with at most $2^{m+1} - 1$ nodes. $\square$

**Lemma 4 (every subset is recorded or cut).** For every $T \subseteq \{1, \dots, m\}$, either $T$ is recorded, or some call $\mathrm{VISIT}(F, C, R, B)$ with $F \subseteq T \subseteq F \cup C$ returned at line L7.

*Proof.* The root call has $\emptyset \subseteq T \subseteq \{1, \dots, m\}$. Take a call with $F \subseteq T \subseteq F \cup C$. If $T = F$ or $T = F \cup C$, it is recorded by Lemma 2. Otherwise $C \ne \emptyset$, so line L6 does not return. If line L7 returns, the second case holds. Otherwise the call branches on some $j \in C$: if $j \in T$, then $F \cup \{j\} \subseteq T \subseteq F \cup C$ for the call of line L10, and if $j \notin T$, then $F \subseteq T \subseteq (F \cup C) \setminus \{j\}$ for the call of line L12. By Lemma 3 this descent ends, and it can end only in one of the two cases. $\square$

**Theorem.** For each size $s$, let $\mathcal L_s$ be the final list of size $s$ and $c_s$ the RSS of its $k$-th entry ($\infty$ if it has fewer than $k$ entries). Then $\mathcal L_s$ holds $\min(k, \binom ms)$ distinct subsets of size $s$ with their exact RSS, and every subset $T$ of size $s$ that is not in $\mathcal L_s$ has $\mathrm{RSS}(T) \ge c_s$. So $\mathcal L_s$ is a list of $k$ best subsets of size $s$.

*Proof.* The record operation keeps, for each size, the $k$ smallest RSS values among the distinct subsets offered to it, with ties kept in the order of arrival. So the cutoff of each size never increases over time, and a recorded subset that is not in the final list was pushed out by $k$ subsets with RSS at most its own. Now take $T$ of size $s$ not in $\mathcal L_s$. If $T$ was recorded, it was pushed out or not taken, so $\mathrm{RSS}(T) \ge c_s$. Otherwise, by Lemma 4, a call with $F \subseteq T \subseteq F \cup C$ returned at line L7 at some time $\tau$. Then $|F| \le s \le |F| + |C|$, so the test of line L7 included $s$, and with $c_s(\tau)$ the cutoff of size $s$ at time $\tau$,

$$\mathrm{RSS}(T) \ge \mathrm{RSS}(F \cup C) = B[y,y] \ge c_s(\tau) \ge c_s,$$

by Lemma 1, Lemma 2, the test of line L7 and the fact that cutoffs do not increase. In both cases $\mathrm{RSS}(T) \ge c_s$. If $\binom ms \ge k$, a cutoff $c_s(\tau)$ is finite only after $k$ subsets of size $s$ were recorded, and no cut can happen for size $s$ while $c_s = \infty$; so if fewer than $k$ subsets of size $s$ were ever recorded, no subset of size $s$ was cut, all were recorded by Lemma 4, and the list holds $\binom ms$ of them. $\square$

**Corollary (criteria).** Let $g(r, s)$ be increasing in $r$ for each $s$, as AIC, BIC, Mallows' $C_p$ and minus the adjusted $R^2$ are as functions of $(\mathrm{RSS}, |S|)$. With $k = 1$, the subset that minimizes $g(\mathrm{RSS}(S), |S|)$ over all $S$ can be taken among the $m + 1$ size winners. *Proof.* For any $S$ of size $s$ with winner $W_s$, $\mathrm{RSS}(W_s) \le \mathrm{RSS}(S)$ by the theorem, so $g(\mathrm{RSS}(W_s), s) \le g(\mathrm{RSS}(S), s)$. $\square$
