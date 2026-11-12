---
title: The Zuker algorithm returns a secondary structure of minimum energy
proves: [correctness]
status: full
---

We fix the sequence $s_1 \cdots s_n$, the allowed pairs, the hairpin minimum $m$, the loop bound $L$ and the loop energies $H$, $\mathrm{IL}$ and $a + b k + c u$ of the page. A structure is allowed if it is a secondary structure and each of its bulges and interior loops has $u_1 + u_2 \le L$. The energy of a structure is the sum of the energies of the loops closed by its pairs; the exterior loop has energy 0.

For a pair $(i, j)$ of a structure $P$, the pairs *directly inside* $(i, j)$ are the pairs $(k, l)$ of $P$ with $i < k < l < j$ such that no pair $(p, q)$ of $P$ has $i < p < k < l < q < j$. Because pairs nest, these pairs are disjoint intervals, and the loop closed by $(i, j)$ is a hairpin, an internal loop (stack, bulge or interior loop) or a multiloop when there are 0, 1 or at least 2 of them.

We define the sets of partial structures that the tables optimize.

- $\mathcal{V}(i, j)$: the allowed structures of $[i, j]$ that contain the pair $(i, j)$. The cost of $Q$ is the sum of the energies of the loops closed by its pairs.
- $\mathcal{W}_1(i, j)$: the allowed structures $Q$ of $[i, j]$ that contain a pair $(i, l)$ with $l \le j$, where the bases $l + 1, \ldots, j$ are unpaired. The cost is $\mathrm{cost}(Q) + b + c (j - l)$, where $\mathrm{cost}(Q)$ is the cost in $\mathcal{V}(i, l)$.
- $\mathcal{W}(i, j)$: the allowed structures $Q$ of $[i, j]$ with at least one pair. The cost is the sum of the loop energies of $Q$, plus $b$ for each outermost pair of $Q$, plus $c$ for each base of $[i, j]$ that no outermost pair encloses.

These are the parts of a multiloop: an outermost pair of the part is a branch, and the uncovered bases are the unpaired bases of the loop. We write $\mathrm{opt}$ for the smallest cost, with $\infty$ for an empty set.

**Lemma 1 (decomposition).** Let $(i, j)$ be an allowed pair with $j - i - 1 \ge m$.

1. Each $Q \in \mathcal{V}(i, j)$ is of exactly one of these kinds: no pair directly inside $(i, j)$ (cost $H(i, j)$); one pair $(k, l)$ directly inside, with $Q \setminus \{(i, j)\} \in \mathcal{V}(k, l)$ and $(k - i - 1) + (j - l - 1) \le L$ (cost $\mathrm{IL}(i, j, k, l)$ plus the cost of the rest); or at least two pairs directly inside. In the last case, let $u$ be the left end of the last of them. Then $i + 2 \le u \le j - 1$, the pairs of $Q$ in $[i + 1, u - 1]$ form a member of $\mathcal{W}(i + 1, u - 1)$, the pairs in $[u, j - 1]$ form a member of $\mathcal{W}_1(u, j - 1)$, and the cost of $Q$ is $a + b$ plus their costs.
2. Each $Q \in \mathcal{W}_1(i, j)$ either contains $(i, j)$, and then its cost is $b$ plus its cost in $\mathcal{V}(i, j)$, or leaves $j$ unpaired, and then it is a member of $\mathcal{W}_1(i, j - 1)$ with $c$ added to the cost.
3. Each $Q \in \mathcal{W}(i, j)$ has a last outermost pair $(u, l)$. The part in $[u, j]$ is a member of $\mathcal{W}_1(u, j)$. The part in $[i, u - 1]$ is empty, with cost $c (u - i)$ for its uncovered bases, or a member of $\mathcal{W}(i, u - 1)$.

In each item, the converse holds: each combination of the stated kind is a member of the set, with the stated cost.

*Proof.* Item 1. The pair $(i, j)$ closes one loop, and its kind is fixed by the number of pairs directly inside. With no pair inside, the loop is a hairpin with $j - i - 1$ unpaired bases, and the other pairs of $Q$ do not exist (any pair inside would contain a pair directly inside). With one pair $(k, l)$, every other pair of $Q$ lies inside $(k, l)$, so the rest is a member of $\mathcal{V}(k, l)$; the loop is allowed, so $u_1 + u_2 \le L$. With at least two pairs directly inside, the last one starts at some $u$. The first pair directly inside starts at $i + 1$ or later and ends before $u$, so $i + 2 \le u$, and $u < j$. The pairs in $[i + 1, u - 1]$ include at least one pair directly inside $(i, j)$, so they form a member of $\mathcal{W}(i + 1, u - 1)$, whose outermost pairs are the branches of the multiloop in that part. The pairs in $[u, j - 1]$ have the single outermost pair $(u, l)$, followed by the unpaired bases $l + 1, \ldots, j - 1$, which is a member of $\mathcal{W}_1(u, j - 1)$. The multiloop has $k$ inner branches and the closing pair, so its energy is $a + b(k + 1) + c u'$, where $u'$ counts the unpaired bases. The terms $b$ for the inner branches and $c$ for the unpaired bases are in the costs of the two parts, and the closing pair gives the extra $a + b$. No pair crosses the cut at $u$, because the pairs directly inside are disjoint and all other pairs lie inside them. The three kinds are disjoint, and in each kind the parts ($k$, $l$ or $u$) are fixed by $Q$.

Item 2. The pair at $i$ is $(i, l)$, and $l = j$ or $l < j$. In the second case, $j$ is unpaired and the cost changes by $c$ when $j$ is removed.

Item 3. The outermost pairs of $Q$ are disjoint intervals, so there is a last one $(u, l)$, and all bases after $l$ are uncovered. Every pair that starts at $u$ or later lies inside $(u, l)$, so the part in $[u, j]$ is a member of $\mathcal{W}_1(u, j)$. The part before $u$ has no pair or at least one.

For the converse, a combination of the stated kind is a set of pairs in disjoint intervals or nested inside a pair, so it is a secondary structure; its loops are the loops of the parts and the one new loop, which is allowed; and the cost is the sum of the parts by the definitions. $\square$

**Lemma 2 (the tables).** After lines L1 to L8, for all $i < j$: $V[i, j] = \mathrm{opt}\, \mathcal{V}(i, j)$, $\mathrm{WM1}[i, j] = \mathrm{opt}\, \mathcal{W}_1(i, j)$ and $\mathrm{WM}[i, j] = \mathrm{opt}\, \mathcal{W}(i, j)$.

*Proof.* By induction on $d = j - i$. For $d \le m$ no pair fits, all three sets are empty, and the cells keep the value $\infty$. Let $d \ge m + 1$. The recurrence of $V$ in lines L4 to L6 is the minimum over the three kinds of Lemma 1 item 1, and it reads only cells of span less than $d$, which are correct by induction. By Lemma 1 and its converse, the minimum over each kind is the stated loop energy plus the optimal costs of the parts, because the cost of the whole is a sum of the costs of independent parts. So $V[i, j]$ is correct; if $(s_i, s_j)$ is not allowed, $\mathcal{V}(i, j)$ is empty and the cell stays $\infty$. Line L7 is item 2; it reads $V[i, j]$, computed in the same pass, and $\mathrm{WM1}[i, j - 1]$, of smaller span. Line L8 is item 3; for $u = i$ it reads $\mathrm{WM1}[i, j]$ from line L7, and all other cells have smaller span. $\square$

**Lemma 3 (the exterior loop).** After line L9, $F[j]$ is the smallest energy of an allowed structure of $s_1 \cdots s_j$, for $0 \le j \le n$.

*Proof.* By induction on $j$. $F[0] = 0$ is the energy of the empty structure. For $j \ge 1$, base $j$ is unpaired, which gives a structure of the prefix of length $j - 1$, or it pairs with some $k$. Then no pair crosses $(k, j)$, so the structure is a structure of $s_1 \cdots s_{k-1}$ together with a member of $\mathcal{V}(k, j)$. The exterior loop costs 0, so the energy is the sum. Line L9 takes the minimum over these cases, with optimal parts by induction and Lemma 2. $\square$

**Theorem.** ZUKER returns $F[n]$, the minimum energy of an allowed structure of $s$, and a structure $P$ with $E(P) = F[n]$.

*Proof.* Lemma 3 with $j = n$ gives the value. For the traceback, each popped cell $X$ has a finite value. By Lemmas 1 to 3, the value of $X$ is the minimum of finitely many cases, so some case gives the value exactly, and line L10 finds one. The invariant is that the energy of the pairs added so far, counted by the loops they close outside the cells on the stack, plus the sum of the values of the cells on the stack, equals $F[n]$; and the cells on the stack are disjoint intervals whose structures can be chosen freely. The step for a cell replaces its value by the cost of its case, which is the energy of one loop (or 0) plus the values of the new cells, so the invariant holds. Each new cell has a smaller span, or is the same interval in a later table in the order $F$, $V$, $\mathrm{WM}$, $\mathrm{WM1}$, $V$ in the steps of lines L8 and L7, so the traceback stops. At the end the stack is empty, and $P$ is an allowed structure with $E(P) = F[n]$ by the converse parts of Lemma 1. $\blacksquare$
