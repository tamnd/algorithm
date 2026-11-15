---
title: The signature file has no false negatives, its search returns exactly the documents that contain the query, and the false drop rate has a closed form
proves: [correctness]
status: full
---

Fix the width $F$ and the weight $m$ with $1 \le m \le F$. For a term $t$, the term signature $\tau(t)$ is a set of exactly $m$ of the places $0, \ldots, F - 1$, written as an $F$-bit word; it depends only on $t$ (and the fixed salt). For a finite set $T$ of terms, the signature is $\sigma(T) = \bigcup_{t \in T} \tau(t)$, the bitwise OR of the term signatures, with $\sigma(\emptyset) = 0$. A document $d$ has a set of terms $T_d$. For a query, a finite set $Q$ of terms, the answer is $A(Q) = (d : Q \subseteq T_d)$, in the order of insertion.

**Invariant (I).** The arrays $ids$, $sigs$ and $terms$ have the same length, and for each $i$, $sigs[i] = \sigma(terms[i])$, where $terms[i]$ is the term set of document $ids[i]$.

**Lemma 1.** The constructor makes (I) true and INSERT keeps it.

*Proof.* The empty file has three empty arrays. INSERT appends the id, the set $T$ of distinct terms, and SIGNATURE$(T)$, which ORs $\tau(t)$ over the distinct elements of $T$, so it is $\sigma(T)$. $\square$

**Lemma 2 (no false negatives).** If $Q \subseteq T_d$, then $\sigma(Q) \subseteq \sigma(T_d)$, that is, $\sigma(T_d) \mathbin{\&} \sigma(Q) = \sigma(Q)$.

*Proof.* $\sigma(Q) = \bigcup_{t \in Q} \tau(t) \subseteq \bigcup_{t \in T_d} \tau(t) = \sigma(T_d)$, since the second union runs over a superset of the terms of the first. A set of places $a$ is contained in $b$ exactly when $b \mathbin{\&} a = a$ as words. $\square$

The converse does not hold. Places of $\tau(t)$ for a term $t \notin T_d$ can all be set by other terms of $d$, and then $d$ passes the test of line L5 without containing $t$. Such a document is a *false drop*.

**Theorem 1.** If (I) holds, SEARCH$(Q)$ returns $A(Q)$, in the order of insertion.

*Proof.* Lines L1 and L2 compute $q = \sigma(Q)$. Line L4 visits the documents in the order of insertion, with $s = \sigma(T_d)$ by (I). If $Q \subseteq T_d$, then line L5 passes by Lemma 2 and line L6 passes, so $d$ is appended. If $Q \not\subseteq T_d$, then line L6 fails, whatever line L5 does, so $d$ is not appended. So the output is the sequence of the $d$ with $Q \subseteq T_d$, in the order of insertion, which is $A(Q)$. For $Q = \emptyset$, $q = 0$, every document passes both lines, and $A(\emptyset)$ is every document. $\square$

The same argument shows that CANDIDATES$(Q)$, which stops after line L5, returns $A(Q)$ followed in order by the false drops: every answer is a candidate, and a candidate is not an answer exactly when it is a false drop.

**The random model.** To count false drops, model each term signature as a uniform random $m$-subset of the $F$ places, independent for different terms. The code is built so that this model is the right one for an ideal hash: each 16-bit hash value below $65536 - (65536 \bmod F)$ gives a uniform place modulo $F$, values above it are rejected, and places already taken are skipped, so the $m$ distinct places form a uniform $m$-subset when the hash values are independent and uniform. BLAKE2b is not proved to be such a hash; the model is the usual assumption, and the tests check the rate that it predicts.

**Theorem 2 (the false drop rate).** Let $d$ have $D$ distinct terms, and let $t$ be a term not in $T_d$. In the random model, the probability that $d$ is a false drop for the query $\{t\}$ is

$$p(F, m, D) = \sum_{j=0}^{m} (-1)^j \binom{m}{j} \left( \frac{\binom{F-j}{m}}{\binom{F}{m}} \right)^{D}.$$

*Proof.* Condition on $\tau(t) = P$, a fixed set of $m$ places. The signatures of the $D$ terms of $d$ are independent of $\tau(t)$, since the terms are different. The document is a false drop when every place of $P$ is set in $\sigma(T_d)$. For $p \in P$ let $E_p$ be the event that $p$ is not set. By the [inclusion-exclusion principle](/inclusion-exclusion-principle/),

$$\Pr\Big[\bigcap_{p \in P} \overline{E_p}\Big] = \sum_{J \subseteq P} (-1)^{|J|} \Pr\Big[\bigcap_{p \in J} E_p\Big].$$

The event $\bigcap_{p \in J} E_p$ says that no term of $d$ sets a place of $J$. One uniform $m$-subset of the $F$ places avoids a fixed set of $j = |J|$ places with probability $\binom{F-j}{m} / \binom{F}{m}$, the share of the $m$-subsets of the other $F - j$ places, and the $D$ terms are independent, so the probability is that number to the power $D$. It depends on $J$ only through $j$, and $P$ has $\binom{m}{j}$ subsets of size $j$. This gives the formula, and since it does not depend on $P$, it is also the probability without the condition. $\blacksquare$

**Remark (the usual approximation).** If the places of each term were chosen with repetition, a place would stay unset with probability $(1 - 1/F)^{mD}$, and treating the $m$ places of the query as independent gives the false drop probability $(1 - (1 - 1/F)^{mD})^m \approx (1 - e^{-mD/F})^m$. For fixed $F$ and $D$ this is smallest near $m = (F / D) \ln 2$, the same analysis as for the [Bloom filter](/bloom-filter/). The exact formula of Theorem 2 is the one the code computes, with exact fractions.
