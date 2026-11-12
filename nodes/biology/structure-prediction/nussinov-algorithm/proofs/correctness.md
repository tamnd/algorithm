---
title: The Nussinov algorithm returns a secondary structure with the largest number of pairs
proves: [correctness]
status: full
---

We fix the sequence $s = s_1 \cdots s_n$, the set of allowed pairs and the hairpin minimum $m \ge 0$. For an interval $[i, j]$, a structure of $[i, j]$ is a secondary structure whose pairs have both ends in $[i, j]$. We write $\mathrm{OPT}(i, j)$ for the largest size of a structure of $[i, j]$, with $\mathrm{OPT}(i, j) = 0$ when $j \le i$, because then no pair fits.

**Lemma 1 (decomposition).** Let $j - i \ge 1$. Each structure $P$ of $[i, j]$ has exactly one of these forms.

1. Base $j$ is unpaired in $P$, and $P$ is a structure of $[i, j - 1]$.
2. $P = \{(k, j)\} \cup A \cup B$ for one $k$ with $i \le k \le j - m - 1$ and $(s_k, s_j)$ allowed, where $A$ is a structure of $[i, k - 1]$ and $B$ is a structure of $[k + 1, j - 1]$.

Conversely, each set of form 1 or form 2 is a structure of $[i, j]$.

*Proof.* If base $j$ has no partner, every pair of $P$ lies in $[i, j - 1]$, which is form 1. Otherwise $j$ has exactly one partner $k$, because no base is in two pairs. The pair $(k, j)$ is in $P$, so $(s_k, s_j)$ is allowed and $j - k - 1 \ge m$, that is $k \le j - m - 1$. Take another pair $(a, b)$ of $P$ with $a < b$. Its ends are not $k$ or $j$, and $b \le j$, so $b < j$. If $a < k < b$, then $a < k < b < j$, so $(a, b)$ and $(k, j)$ cross, which is not allowed. So either $b < k$, and the pair lies in $[i, k - 1]$, or $k < a$, and the pair lies in $[k + 1, j - 1]$. Let $A$ and $B$ be the two groups. Each is a subset of $P$, so each is a secondary structure, and $P$ has form 2. The two forms are different (base $j$ is paired or not), and in form 2 the value $k$ is the partner of $j$, so it is unique.

For the converse, a set of form 1 is a structure of $[i, j]$. In form 2, the pair $(k, j)$ is allowed and long enough. The sets $A$, $B$ and $\{(k, j)\}$ use disjoint bases. A pair of $A$ and a pair of $B$ do not cross, because all ends of the first are smaller than all ends of the second. A pair $(a, b)$ of $A$ or $B$ does not cross $(k, j)$: for $A$ we have $a < b < k < j$, and for $B$ we have $k < a < b < j$. Pairs inside $A$ or inside $B$ do not cross because $A$ and $B$ are secondary structures. $\square$

**Lemma 2 (the table).** After lines L1 to L6, $N[i, j] = \mathrm{OPT}(i, j)$ for all $1 \le i \le j \le n$, and the value 0 that the algorithm uses for $j \le i$ is $\mathrm{OPT}(i, j)$.

*Proof.* By induction on $d = j - i$. For $d \le 0$ the value is 0, which is correct. Let $d \ge 1$, and assume the claim for all spans less than $d$. Lines L4 to L6 compute

$$N[i, j] = \max\Big(N[i, j - 1],\ \max_k \big(N[i, k - 1] + 1 + N[k + 1, j - 1]\big)\Big),$$

with $k$ over $i \le k \le j - m - 1$ and $(s_k, s_j)$ allowed. The intervals $[i, j - 1]$, $[i, k - 1]$ and $[k + 1, j - 1]$ have spans less than $d$. The loops of lines L1 and L2 fill all cells of span less than $d$ before any cell of span $d$, so these cells hold their final values, which are the OPT values by the induction hypothesis.

*Upper bound.* Take an optimal structure $P$ of $[i, j]$. If it has form 1 of Lemma 1, then $|P| \le \mathrm{OPT}(i, j - 1) = N[i, j - 1]$. If it has form 2, then $|P| = 1 + |A| + |B| \le 1 + \mathrm{OPT}(i, k - 1) + \mathrm{OPT}(k + 1, j - 1)$ for an index $k$ that line L6 tries. So $\mathrm{OPT}(i, j) \le N[i, j]$.

*Lower bound.* The value $N[i, j - 1]$ is the size of an optimal structure of $[i, j - 1]$, which is a structure of $[i, j]$ by the converse of Lemma 1. Each value $N[i, k - 1] + 1 + N[k + 1, j - 1]$ is the size of the set $\{(k, j)\} \cup A \cup B$ with $A$ and $B$ optimal for their intervals, and this set is a structure of $[i, j]$ by the converse of Lemma 1. So $N[i, j] \le \mathrm{OPT}(i, j)$. $\square$

**Lemma 3 (the traceback).** Lines L7 to L13 stop and return a structure $P$ of $[1, n]$ with $|P| = N[1, n]$.

*Proof.* We use this invariant, which holds at the start of each pass of line L8:

> **(T)** The intervals on the stack $T$ are pairwise disjoint subintervals of $[1, n]$. No base of an interval on $T$ is an end of a pair of $P$. Each pair of $P$ is allowed and long enough, and no two pairs of $P$ cross. A pair of $P$ and an interval $[a, b]$ on $T$ are related in one of two ways: the pair lies outside $[a, b]$ on one side, or the pair encloses $[a, b]$. Finally, $|P| + \sum_{[a, b] \in T} N[a, b] = N[1, n]$.

At the start $P$ is empty and $T$ holds $[1, n]$, so (T) holds. Line L9 pops an interval $[i, j]$. If $j - i < 1$, then $N[i, j] = 0$ and dropping it keeps the sum. If line L10 succeeds, the interval is replaced by $[i, j - 1]$ with the same value. Otherwise $N[i, j] \ne N[i, j - 1]$, so by Lemma 2 the maximum of line L6 came from some $k$, and line L12 finds one. Line L13 removes $[i, j]$ (value $N[i, j]$), adds the pair $(k, j)$ (one pair) and pushes $[i, k - 1]$ and $[k + 1, j - 1]$ (values with sum $N[i, j] - 1$), so the sum stays $N[1, n]$. The new pair has its ends in $[i, j]$, which held no end of a pair of $P$, and it is allowed and long enough. It does not cross an old pair, because each old pair lies outside $[i, j]$ on one side or encloses it. The two new intervals lie inside $(k, j)$ or to its left, and they keep the relation with each old pair that $[i, j]$ had. So (T) holds after each pass.

Each pass removes an interval of span $d \ge 0$ and pushes only intervals of span less than $d$, so the sum of $(\text{span} + 2)^2$ over the stack decreases, and the loop stops. When it stops, $T$ is empty, so by (T) the set $P$ is a secondary structure of $[1, n]$ with $|P| = N[1, n]$. $\square$

**Theorem.** NUSSINOV returns $N[1, n] = \mathrm{OPT}(1, n)$ and a secondary structure $P$ of $s$ with $|P| = \mathrm{OPT}(1, n)$, that is, a structure with the largest number of pairs.

*Proof.* Lemma 2 gives $N[1, n] = \mathrm{OPT}(1, n)$, and Lemma 3 gives the structure. $\blacksquare$

**Counting.** Lemma 1 says that each structure of $[i, j]$ has exactly one form, with a unique $k$ in form 2. So if max is replaced by sum and the term $N[i, k - 1] + 1 + N[k + 1, j - 1]$ by the product $C[i, k - 1] \cdot C[k + 1, j - 1]$, with $C = 1$ on empty intervals, the same recurrence counts the structures of $[i, j]$ without double counting. A weight per pair as a factor in the product gives the sum of the weights of the structures.
