---
title: The A-buffer resolve equals the per-cell front-to-back composite in fragment order
proves: [correctness]
status: full
---

We use the pseudocode and the definitions of the page. Fix a pixel with cells $C$, $|C| = s$. For a triangle $t$ with index $k$ that covers at least one cell, its fragment $f_k$ has the key $(z_k, k)$, where $z_k$ is the plane depth of $t$ at the pixel center, and the mask $M_k$ of the cells it covers. Keys are distinct, because the indices are. For a cell $c$, let $k_1, \dots, k_r$ be the indices of the triangles that cover $c$, in increasing order of key. The *target* at $c$ is
$$\mathrm{out}(c) = \sum_{q = 1}^{r} \Big(\prod_{p < q} (1 - \alpha_{k_p})\Big) \alpha_{k_q} \, \mathrm{col}_{k_q} + \Big(\prod_{p \le r} (1 - \alpha_{k_p})\Big) \mathrm{bg},$$
the front-to-back over composite. The claim is that RESOLVE returns $\frac1s \sum_{c \in C} \mathrm{out}(c)$.

**Lemma 1 (insert).** After all triangles are inserted, the full fragment $\phi$ (if any) is the opaque fragment with the least key among those whose mask is $C$, and the list holds exactly the other fragments with a key less than the key of $\phi$, or all other fragments if there is no $\phi$.

*Proof.* By induction on the number of inserts. Line L4 drops $f$ when its key is greater than the key of the current $\phi$; then $f$ is behind $\phi$, and also behind any later full fragment, whose key is smaller still. Lines L5 and L6 make $f$ the full fragment when it is opaque, covers $C$ and was not dropped, so its key is less than that of the old $\phi$; line L6 then removes the list entries behind $f$. Line L7 adds every other fragment that was not dropped. So a fragment is missing from the final structure exactly when some opaque full fragment with a smaller key was present at its insert or came later. The full fragment with the least key is the last one set, since keys only go down at line L6. $\square$

**Lemma 2 (the dropped fragments do not matter).** Let $\phi$ have key $\kappa$. In $\mathrm{out}(c)$, each term of a triangle with key greater than $\kappa$ is 0.

*Proof.* $\phi$ covers every cell and has $\alpha = 1$, so the product $\prod (1 - \alpha)$ over the triangles in front of such a term includes the factor $1 - 1 = 0$. The background term is 0 for the same reason. $\square$

So $\mathrm{out}(c)$ can be computed from the fragments of line L8 alone, in the order of line L8, which is the order of the keys: the list is sorted by key, and every key in the list is less than $\kappa$ by Lemma 1.

**Lemma 3 (the invariant of lines L10 to L13).** Before the $q$-th fragment $g_q$ of the order, the sets $M$ of the pairs $(M, \tau)$ in $G$ are disjoint, and for each cell $c$:

1. $c$ is in some set of $G$ if and only if $\prod_{p < q,\, c \in M_{g_p}} (1 - \alpha_{g_p}) > 0$;
2. if $c$ is in the set of $(M, \tau)$, then $\tau = \prod_{p < q,\, c \in M_{g_p}} (1 - \alpha_{g_p})$;
3. the sum holds $\sum_c S_q(c)$, where $S_q(c)$ is the sum of the terms of $\mathrm{out}(c)$ for $g_1, \dots, g_{q - 1}$.

*Proof.* Before the first fragment, $G = \{(C, 1)\}$ and the sum is 0, so the claims hold with empty products. Assume them before $g_q$, with mask $M_q$ and opacity $\alpha$. Line L11 splits each $(M, \tau)$ into $M \cap M_q$ and $M \setminus M_q$, which are disjoint and lie in $M$, so the new sets stay disjoint. For a cell $c$ in $M \cap M_q$ the term of $g_q$ in $\mathrm{out}(c)$ is $\tau \alpha \, \mathrm{col}$ by claim 2, and line L12 adds it once for each such cell, which is claim 3 for these cells. Their transmittance becomes $\tau (1 - \alpha)$, kept by line L13 when it is positive, that is when $\alpha < 1$ (for $\tau > 0$ by claim 1). A cell in $M \setminus M_q$ is not covered by $g_q$, so its product and its sum do not change, and line L13 keeps it with $\tau$. A cell in no set of $G$ has a zero product, so the term of $g_q$ at it is 0 and nothing is added. So all three claims hold before $g_{q + 1}$. $\square$

**Theorem.** RESOLVE returns $\frac1s \sum_{c \in C} \mathrm{out}(c)$.

*Proof.* After the last fragment, Lemma 3 says the sum holds all fragment terms of all cells, and each cell with a positive transmittance is in exactly one set of $G$, with that transmittance. Line L14 adds $\tau \cdot \mathrm{bg}$ for each such cell, which is its background term; a cell in no set has a zero background term. By Lemma 2 the dropped fragments add nothing. Line L15 divides by $s$. $\blacksquare$

**Remark.** The theorem uses the order of the keys, which come from the depths at the pixel center. When the order of the triangles by plane depth is the same at each cell center of the pixel as at the pixel center, for example when each triangle has a constant depth, $\mathrm{out}(c)$ is also the composite in the true order at $c$, and the A-buffer equals exact supersampling with $s$ samples. When two triangles cross inside the pixel, the two orders differ at some cells, and the A-buffer is only an approximation there.
