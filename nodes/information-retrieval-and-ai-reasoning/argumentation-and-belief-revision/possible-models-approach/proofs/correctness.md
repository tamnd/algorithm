---
title: The method returns, for each model of K, the models of p with an inclusion-minimal change set
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is a number $n \ge 0$ of atoms, the set $K$ of the models of the belief base and the set $P$ of the models of the new formula $p$. A world is a vector in $\{0,1\}^n$, and we identify it with the set of its true atoms, so that $w \oplus v$ is the set $\mathrm{Diff}(w, v)$ of the atoms on which $w$ and $v$ differ. For a world $w$, let

$$D_w = \{w \oplus v : v \in P\}$$

be the change sets that lead from $w$ into $P$, and let $\mathrm{Min}(w) = \{v \in P : \text{no } y \in D_w \text{ has } y \subsetneq w \oplus v\}$. The possible models approach is

$$K \diamond P = \bigcup_{w \in K} \mathrm{Min}(w)$$

(Winslett 1988, Section 3, with the protected formulas left out).

**Lemma 1 (a model of p).** If $w \in P$, then $\mathrm{Min}(w) = \{w\}$.

*Proof.* $w \oplus w = \emptyset$ is in $D_w$, and $\emptyset \subsetneq y$ for every nonempty $y$. So every $v \in P$ with $v \ne w$ has $\emptyset \subsetneq w \oplus v$ in $D_w$ and is not in $\mathrm{Min}(w)$. The set $\emptyset$ has no proper subset, so $w \in \mathrm{Min}(w)$. $\square$

**Lemma 2 (the upward closure).** Fix $w \notin P$. After line L5, $C[x]$ is true exactly when $x \in D_w$. After the round $i$ of lines L6 and L7, for $i = 0, \ldots, n-1$,

> **(I)** $C[x]$ is true exactly when some $y \in D_w$ has $y \subseteq x$ and $y$ agrees with $x$ on the atoms $i+1, \ldots, n-1$.

*Proof.* Before round 0 the claim holds with "agrees on all atoms" in place of (I), since $C[x]$ is true exactly for $x \in D_w$. Suppose it holds after round $i - 1$, that is, $C[x]$ is true exactly when some $y \in D_w$ has $y \subseteq x$ and $y$ agrees with $x$ on the atoms $i, \ldots, n-1$. In round $i$, line L7 changes only the entries $C[x]$ with atom $i$ in $x$, and it reads $C[x \oplus 2^i]$, where $x \oplus 2^i$ does not contain atom $i$, so that entry is not changed in this round and the order of the updates does not matter. If atom $i$ is not in $x$, then any $y \subseteq x$ misses atom $i$ too and so agrees with $x$ on atom $i$, and the old value is already right. If atom $i$ is in $x$, the sets $y \subseteq x$ that agree with $x$ on the atoms $i + 1, \ldots, n-1$ are the ones that contain atom $i$, which the old $C[x]$ covers, and the ones that miss it, which the old $C[x \oplus 2^i]$ covers. So the new value $C[x] \vee C[x \oplus 2^i]$ is right. $\square$

After the last round, (I) with $i = n - 1$ says: $C[x]$ is true exactly when some $y \in D_w$ has $y \subseteq x$.

**Lemma 3 (the test).** Fix $w \notin P$ and $v \in P$, and let $x = w \oplus v$. After the loop of lines L6 and L7, some $y \in D_w$ has $y \subsetneq x$ if and only if $C[x \oplus 2^i]$ is true for some atom $i$ in $x$.

*Proof.* If $y \in D_w$ and $y \subsetneq x$, take an atom $i$ in $x$ but not in $y$. Then $y \subseteq x \oplus 2^i$, so $C[x \oplus 2^i]$ is true by Lemma 2. Conversely, if $C[x \oplus 2^i]$ is true for an atom $i$ in $x$, Lemma 2 gives $y \in D_w$ with $y \subseteq x \oplus 2^i \subsetneq x$. $\square$

**Theorem.** PMA$(K, P, n)$ stops and returns $K \diamond P$.

*Proof.* Every loop runs over a finite set, so the method stops. We show that for each $w \in K$ the worlds that lines L3 to L10 add to $R$ are exactly $\mathrm{Min}(w)$. If $w \in P$, lines L3 and L4 add $w$ alone, which is $\mathrm{Min}(w)$ by Lemma 1. If $w \notin P$, line L9 adds $v \in P$ exactly when no $C[x \oplus 2^i]$ with $i$ in $x$ is true, which by Lemma 3 means that no change set in $D_w$ is a proper subset of $w \oplus v$, that is $v \in \mathrm{Min}(w)$. The array $C$ is set up again for each $w$, so one model does not change the work for the next. $R$ starts empty at line L1 and only grows, so line L11 returns the union of the sets $\mathrm{Min}(w)$ for $w \in K$. $\square$

**The empty cases.** If $K$ is empty, the loop of line L2 does not run and the result is empty: an inconsistent base stays inconsistent. If $P$ is empty, no $w$ is in $P$, no entry of $C$ is set, and line L8 has nothing to run over, so the result is empty.

**Cost.** For one $w \notin P$, line L5 takes $O(2^n)$ time to clear and fill $C$, lines L6 and L7 take $O(n \cdot 2^n)$, and lines L8 to L10 take $O(n \cdot |P|) \subseteq O(n \cdot 2^n)$. For $w \in P$ the work is $O(1)$ with $P$ stored as a bit array. With $k = |K|$, the time is $O(k \cdot n \cdot 2^n)$ on the [word RAM](/word-ram/), and the extra space is the $2^n$ bits of $C$ and of $R$.
