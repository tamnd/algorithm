---
title: The minimal test collection loop stops only when the judgments fix the sign of the difference in average precision
proves: [correctness]
status: full
---

Let $A$ and $B$ be rankings with no repeated document, and let $P$ be the set of the $m$ documents in $A$ or $B$. Let $x_d = 1$ if document $d$ is relevant and 0 otherwise, and let $R$ be the number of relevant documents in the whole collection, inside or outside $P$. Write $r_A(d)$ for the rank of $d$ in $A$, from 1. Lines refer to the pseudocode on the page.

**Claim 1 (the quadratic form).** For $i, j \in P$ with $i \le j$, let $a_{ii} = 1/r_A(i)$ and $a_{ij} = 1/\max(r_A(i), r_A(j))$ when both are in $A$, and 0 otherwise; define $b_{ij}$ in the same way for $B$, and let $c_{ij} = a_{ij} - b_{ij}$. Then

$$D(x) = \sum_{i \le j} c_{ij} x_i x_j = R \, (\mathrm{AP}(A) - \mathrm{AP}(B)),$$

where AP is 0 when $R = 0$. So when $R > 0$, $D$ has the sign of $\mathrm{AP}(A) - \mathrm{AP}(B)$.

*Proof.* If $R = 0$ then every $x_d = 0$, both sides are 0. Otherwise, by the definition of average precision,

$$R \cdot \mathrm{AP}(A) = \sum_{i \in A} \frac{x_i}{r_A(i)} \sum_{j \in A, \, r_A(j) \le r_A(i)} x_j.$$

The term for $j = i$ is $x_i / r_A(i) = a_{ii} x_i x_i$, since $x_i^2 = x_i$. Each pair $i \ne j$ of documents of $A$ appears once, in the sum of the lower-ranked one, with factor $1 / \max(r_A(i), r_A(j)) = a_{ij}$. So $R \cdot \mathrm{AP}(A) = \sum_{i \le j} a_{ij} x_i x_j$. The same holds for $B$, and the difference is $D$. Relevant documents outside $P$ change $R$ but no term of $D$. $\square$

Fix the judgments made so far: a set $S$ of documents judged relevant, a set $N$ judged not relevant, and the set $T = P \setminus (S \cup N)$ not judged. A completion is any choice of $x_d \in \{0, 1\}$ for $d \in T$.

**Claim 2 (the bounds of line L4).** Let $K = \sum_{i \le j, \; i, j \in S} c_{ij}$ and let $F$ be the set of pairs $i \le j$ with no document in $N$ and at least one in $T$. With $\mathrm{lo} = K + \sum_{F} \min(0, c_{ij})$ and $\mathrm{hi} = K + \sum_{F} \max(0, c_{ij})$, every completion has $\mathrm{lo} \le D \le \mathrm{hi}$.

*Proof.* Split $D$ by pairs. A pair with a document in $N$ gives 0. A pair inside $S$ gives $c_{ij}$, and these sum to $K$. A pair in $F$ gives $c_{ij} x_i x_j \in \{0, c_{ij}\}$, which lies between $\min(0, c_{ij})$ and $\max(0, c_{ij})$. Add the bounds. $\square$

This is the stopping condition of Carterette, Allan and Sitaraman, where the sum of the negative $c_{ij}$ over $F$ is moved to the other side.

**Claim 3 (the stop is sound).** If the loop returns 1 in line L5, then $\mathrm{AP}(A) > \mathrm{AP}(B)$ for every completion and every relevance of the documents outside $P$; the same holds with $<$ for $-1$, and with $=$ for 0.

*Proof.* If $\mathrm{lo} > 0$, Claim 2 gives $D > 0$ for every completion. Then some $x_d = 1$, so $R > 0$, and Claim 1 gives $\mathrm{AP}(A) > \mathrm{AP}(B)$. The case $\mathrm{hi} < 0$ is the same. If $\mathrm{lo} = \mathrm{hi}$ and neither test before it fired, then $\mathrm{lo} \le 0 \le \mathrm{hi} = \mathrm{lo}$, so $D = 0$ for every completion, and by Claim 1 the difference is 0, also when $R = 0$. $\square$

**Claim 4 (termination).** The loop makes at most $m$ judgments, and with no budget it always returns a sign.

*Proof.* Each pass that does not return judges one document of $T$ in line L10, so $|T|$ falls by 1. When $T = \emptyset$, $F$ is empty and $\mathrm{lo} = \mathrm{hi} = K$, so one of the three tests of line L5 fires. $\square$

**Claim 5 (the weights of line L8).** For $i \in T$, let $w^R_i = \sum_{j \in S \cup \{i\}} \max(0, c_{ij})$, $v^R_i = \sum_{j \in S \cup \{i\}} \max(0, -c_{ij})$, $w^N_i = \sum_{j \in S \cup T} \max(0, -c_{ij})$ and $v^N_i = \sum_{j \in S \cup T} \max(0, c_{ij})$, with $c_{ij}$ read as $c_{ji}$ when $j < i$. Judging $i$ relevant raises lo by $w^R_i$ and lowers hi by $v^R_i$; judging it not relevant raises lo by $w^N_i$ and lowers hi by $v^N_i$.

*Proof.* Only the pairs that contain $i$ change. If $i$ is judged relevant, the pairs with $j \in S \cup \{i\}$ leave $F$ and become constants, so their part of lo goes from $\min(0, c_{ij})$ to $c_{ij}$, a rise of $\max(0, c_{ij})$, and their part of hi goes from $\max(0, c_{ij})$ to $c_{ij}$, a fall of $\max(0, -c_{ij})$; the pairs with $j \in T \setminus \{i\}$ stay in $F$. If $i$ is judged not relevant, every pair with $j \in S \cup T$ leaves $F$ and becomes 0, so lo rises by $-\min(0, c_{ij})$ and hi falls by $\max(0, c_{ij})$. $\square$

All four weights are at least 0, so lo never falls and hi never rises. The choice rule only affects how many judgments are needed, not the soundness of Claim 3.

**Claim 6 (the stop is not necessary).** The sign can be fixed while $\mathrm{lo} \le 0 < \mathrm{hi}$.

*Proof.* Let $A = (3, 2, 4, 1)$ and $B = (3, 4, 1, 2)$, with documents 2 and 4 judged relevant and 1 judged not relevant. Then $K = c_{22} + c_{24} + c_{44} = 1/4 + 1/12 - 1/6 = 1/6$, and the pairs in $F$ are $(3, 3)$, $(2, 3)$ and $(3, 4)$ with $c = 0$, $1/4$ and $-1/6$. So $\mathrm{lo} = 1/6 - 1/6 = 0$ and $\mathrm{hi} = 1/6 + 1/4 = 5/12$, but $D = 1/6$ when $x_3 = 0$ and $D = 1/6 + 1/4 - 1/6 = 1/4$ when $x_3 = 1$, both positive. The bound treats the two pairs that contain document 3 as if they could take their worst values apart, which they cannot. $\square$

**Cost.** Line L1 builds $O(m^2)$ coefficients. In each pass, line L4 reads every pair once, $O(m^2)$, and each weight in line L8 reads one row, $O(m)$, so the scan of line L7 is $O(m^2)$. With at most $m$ passes the total is $O(m^3)$ time and $O(m^2)$ space. $\blacksquare$
