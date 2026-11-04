---
title: The Horowitz-Sahni algorithm finds a subset with the target sum when one exists
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. For a set $T$ of indices, write $\sigma(T) = \sum_{k \in T} a_k$. A list is *sorted* when its sums are in non-decreasing order.

**Lemma 1 (SORTED-SUMS).** Let $lo \le hi + 1$. SORTED-SUMS$(a, lo, hi)$ returns a sorted list that holds the entry $(\sigma(T), T)$ exactly once for each subset $T \subseteq \{lo, \ldots, hi\}$, and no other entry.

*Proof.* We show by induction on the number of iterations of line L12 this invariant: before the iteration with $k$, the list $S$ is sorted and holds $(\sigma(T), T)$ exactly once for each $T \subseteq \{lo, \ldots, k-1\}$, and nothing else.

*Base.* Before the first iteration, line L11 gives $S = [(0, \emptyset)]$. The only subset of the empty set is $\emptyset$, with $\sigma(\emptyset) = 0$. A list with one entry is sorted.

*Step.* Assume the invariant before the iteration with $k$. Line L13 maps each entry $(s, T)$ of $S$ to $(s + a_k, T \cup \{k\})$. Since $k \notin T$, the new entry is $(\sigma(T \cup \{k\}), T \cup \{k\})$. The map adds the same number $a_k$ to each sum, so it keeps the order of the sums, and $S'$ is sorted. The subsets of $\{lo, \ldots, k\}$ are of two kinds: those without $k$, which are the sets $T$ of $S$, and those with $k$, which are the sets $T \cup \{k\}$ of $S'$. Each subset is of exactly one kind and is made from exactly one $T$. MERGE of two sorted lists returns a sorted list with the entries of both, each once (see [merging sorted lists](/merging-sorted-lists/)). So after line L14 the invariant holds for $k + 1$.

*End.* The loop runs for $k = lo, \ldots, hi$, a finite range, so it stops. After the last iteration, the invariant with $k = hi + 1$ is the claim. $\square$

**Lemma 2 (the split).** Let $h = \lfloor n/2 \rfloor$, $L = \{1, \ldots, h\}$ and $U = \{h+1, \ldots, n\}$. For each $I \subseteq \{1, \ldots, n\}$ there is exactly one pair $(T_A, T_B)$ with $T_A \subseteq L$, $T_B \subseteq U$ and $I = T_A \cup T_B$, namely $T_A = I \cap L$ and $T_B = I \cap U$. Then $\sigma(I) = \sigma(T_A) + \sigma(T_B)$.

*Proof.* $L$ and $U$ are disjoint and their union is $\{1, \ldots, n\}$. So $I = (I \cap L) \cup (I \cap U)$, and any pair with the two conditions must have $T_A = I \cap L$ and $T_B = I \cap U$. The sum over a disjoint union is the sum of the two sums. $\square$

By Lemma 1 and Lemma 2, there is a set $I$ with $\sigma(I) = t$ if and only if there are positions $p$ and $q$ with $A[p].s + B[q].s = t$. Call such a pair of positions a *solution pair*.

**Lemma 3 (the scan).** At each test of line L5, the following invariant holds:

> **(P)** No solution pair $(p, q)$ has $p < i$ or $q > j$.

*Initialization.* Line L4 sets $i = 0$ and $j = |B| - 1$. No position is less than 0 and no position of $B$ is more than $|B| - 1$, so (P) holds.

*Maintenance.* Assume (P) and that the loop body runs, so $0 \le i < |A|$ and $0 \le j < |B|$. Let $s = A[i].s + B[j].s$ (line L6). If $s = t$, line L7 returns, and there is no next test. If $s < t$, take any $q$. If $q > j$, then $(i, q)$ is not a solution pair by (P). If $q \le j$, then $B[q].s \le B[j].s$ because $B$ is sorted, so $A[i].s + B[q].s \le s < t$. So no solution pair has $p = i$, and line L8 sets $i \leftarrow i + 1$ with (P) still true. If $s > t$, take any $p$. If $p < i$, then $(p, j)$ is not a solution pair by (P). If $p \ge i$, then $A[p].s \ge A[i].s$ because $A$ is sorted, so $A[p].s + B[j].s \ge s > t$. So no solution pair has $q = j$, and line L9 sets $j \leftarrow j - 1$ with (P) still true. $\square$

**Termination.** Let $\Phi = i + (|B| - 1 - j)$. At line L4, $\Phi = 0$. Each iteration that does not return increases $\Phi$ by exactly 1. While the loop runs, $i \le |A| - 1$ and $j \ge 0$, so $\Phi \le |A| + |B| - 2$ at each test that enters the loop. So the loop runs at most $|A| + |B| - 1$ times.

**Theorem.** HOROWITZ-SAHNI$(a, t)$ stops. It returns a set $I \subseteq \{1, \ldots, n\}$ with $\sigma(I) = t$ if such a set exists, and NONE otherwise.

*Proof.* Termination is shown above. Lemma 1 holds for lines L2 and L3, so $A$ and $B$ are sorted and hold the subsets of the two halves.

*Case 1: line L7 returns.* Then $A[i].s + B[j].s = t$. By Lemma 1, $A[i] = (\sigma(T_A), T_A)$ with $T_A \subseteq L$ and $B[j] = (\sigma(T_B), T_B)$ with $T_B \subseteq U$. By Lemma 2, $I = T_A \cup T_B$ has $\sigma(I) = t$.

*Case 2: line L10 returns NONE.* The loop stopped, so $i = |A|$ or $j = -1$. By (P), no solution pair has $p < |A|$ in the first case, or $q > -1$ in the second case. Each position of $A$ is less than $|A|$, and each position of $B$ is more than $-1$. So there is no solution pair, and by Lemma 2 there is no set $I$ with $\sigma(I) = t$.

In both cases the result is right. If a set with sum $t$ exists, Case 2 is impossible, so the algorithm returns such a set. $\blacksquare$
