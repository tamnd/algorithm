---
title: The delta rules are exact, and the counting algorithm maintains the view
proves: [correctness]
status: full
---

**Setting.** A *signed bag* over a schema is a function $B$ from tuples to integers with finite support; $B(t)$ is the multiplicity of $t$. Sum, selection, projection and natural join are defined on signed bags by
$$(B_1 + B_2)(t) = B_1(t) + B_2(t), \quad \sigma_p(B)(t) = [p(t)]\, B(t), \quad \pi_A(B)(u) = \sum_{t :\, t[A] = u} B(t),$$
$$(B_1 \bowtie B_2)(t) = B_1(t[X_1]) \cdot B_2(t[X_2]),$$
where $X_1, X_2$ are the schemas and $t$ ranges over tuples on $X_1 \cup X_2$. On ordinary bags (all multiplicities at least 0) these are the bag operators of SQL. A database $D$ maps each relation name to a signed bag, an update $\Delta D$ does too, and $D + \Delta D$ adds them name by name. For an expression $E$, DELTA$(E)$ is computed by lines L1 to L6 from the old database $D$.

**Lemma 1 (linearity).** Selection and projection are linear: $\sigma_p(B_1 + B_2) = \sigma_p(B_1) + \sigma_p(B_2)$ and $\pi_A(B_1 + B_2) = \pi_A(B_1) + \pi_A(B_2)$. Join is bilinear: $(B_1 + B_1') \bowtie B_2 = B_1 \bowtie B_2 + B_1' \bowtie B_2$, and the same in the second argument.

*Proof.* Each follows from the definition at a fixed tuple: $[p(t)](B_1(t) + B_2(t))$ splits into two terms; the sum over $t$ with $t[A] = u$ of a sum is the sum of two sums; and $(B_1(t[X_1]) + B_1'(t[X_1])) \cdot B_2(t[X_2])$ splits by distributivity. $\square$

**Theorem 1.** For every expression $E$, every database $D$ and every update $\Delta D$: $E(D + \Delta D) = E(D) + \text{DELTA}(E)$.

*Proof.* By induction on $E$. Write $E' = E(D + \Delta D)$, $E = E(D)$ and $\Delta E$ for DELTA$(E)$.

- *Base relation* (line L1): $R(D + \Delta D) = R(D) + \Delta R$ by the definition of the update.
- *Selection* (line L2): $\sigma_p(E_1') = \sigma_p(E_1 + \Delta E_1) = \sigma_p(E_1) + \sigma_p(\Delta E_1)$ by the induction hypothesis and Lemma 1.
- *Projection* (line L3): the same with $\pi_A$.
- *Sum* (line L4): $E_1' + E_2' = (E_1 + \Delta E_1) + (E_2 + \Delta E_2) = (E_1 + E_2) + (\Delta E_1 + \Delta E_2)$.
- *Join* (lines L5 and L6): by the induction hypothesis and bilinearity,
$$E_1' \bowtie E_2' = (E_1 + \Delta E_1) \bowtie (E_2 + \Delta E_2) = E_1 \bowtie E_2 + \Delta E_1 \bowtie E_2 + E_1 \bowtie \Delta E_2 + \Delta E_1 \bowtie \Delta E_2,$$
and the last three terms are what line L6 adds. A term whose delta factor is empty is the empty bag, so skipping it does not change the sum.

If no relation of $E$ has a nonzero change, every base case gives the empty bag, and by the same induction DELTA$(E)$ is empty; the shortcut that returns the empty bag at once is therefore correct. $\square$

**Theorem 2 (counting algorithm).** Assume that the stored counts equal $E(D)$ before a call of MAINTAIN with the update $\Delta D$. After the call, the counts equal $E(D + \Delta D)$, the stored database is $D + \Delta D$, and the reported inserted and deleted tuples are exactly the tuples whose count changed from at most 0 to positive, and from positive to at most 0. In particular, if $D$ and $D + \Delta D$ are ordinary bags (for example sets, under set semantics with valid inserts and deletes), the counts stay at least 0, and the set view $\{t : \text{count}(t) > 0\}$ equals the set of tuples of $E(D + \Delta D)$.

*Proof.* Line L7 computes $\Delta E = \text{DELTA}(E)$ on the old database. Lines L8 to L11 add $\Delta E(t)$ to the count of each tuple $t$ in the support of $\Delta E$, and the count of every other tuple does not change, which is right because $\Delta E(t) = 0$ for it. So the new counts are $E(D) + \Delta E = E(D + \Delta D)$ by Theorem 1. Line L11 removes a tuple whose count is 0, which does not change the function. Line L10 compares the old and new count of exactly the tuples whose count changes, so the reports are exact. Line L12 stores $D + \Delta D$, so the assumption holds for the next call.

If every relation of $D + \Delta D$ is an ordinary bag, then $E(D + \Delta D)$ is an ordinary bag, because the operators map ordinary bags to ordinary bags (selection and projection keep signs; a product of nonnegative numbers is nonnegative). So every count is at least 0, and the positive counts are the tuples of the result. The count of a tuple is then its number of derivations: under set semantics for the base relations, it is the number of ways to produce the tuple from base tuples, which is why the deletion of one derivation does not remove a tuple that has another. $\blacksquare$
