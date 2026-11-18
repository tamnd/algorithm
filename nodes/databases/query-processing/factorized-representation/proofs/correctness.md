---
title: FROMJOIN builds a representation of the join result, each tuple is listed once, and the number of singletons is the sum of the path projections
proves: [correctness, termination, size]
status: full
---

We use the line numbers of the pseudocode. $Q$ is the natural join of the relations $R_1, \dots, R_m$ of $D$, each with at least one attribute, and $T$ is an f-tree whose node set is the set of attributes of $Q$. The relations are read as sets and hold no nulls. For a node $A$, $\mathit{anc}(A)$ is the set of proper ancestors of $A$, $\mathit{path}(A) = \mathit{anc}(A) \cup \{A\}$, and $T_A$ is the subtree rooted at $A$, with attribute set $\mathit{at}(T_A)$. For a list $F$ of subtrees, $\mathit{at}(F)$ is the union of their attribute sets. A tuple is a map from a set of attributes to values, and $t|_S$ is its restriction to $S$.

**Semantics.** A singleton $\langle A{:}a \rangle$ stands for the relation with the one tuple $\{A \mapsto a\}$. A pair $(a, P)$ in a union for $A$ stands for $\langle A{:}a \rangle \times [\![P]\!]$, a union stands for the union of its pairs, and a product $(U_1, \dots, U_k)$ stands for $[\![U_1]\!] \times \dots \times [\![U_k]\!]$. The empty product $()$ stands for $\{()\}$, the relation with the one tuple on no attributes. A union with no pairs stands for $\emptyset$.

**The target sets.** Let $F$ be the list of children of a node $B$, or the list of roots, and let $C = \mathit{path}(B)$, or $C = \emptyset$ for the roots. For a tuple $t$ on $C$, let

$$J(F, t) = \{\, u \text{ on } \mathit{at}(F) : (t \cup u)|_{R} \in R \text{ for every relation } R \text{ with } R \cap \mathit{at}(F) \ne \emptyset \,\}.$$

For one subtree $T_A$ with $\mathit{anc}(A) = C$, define $J(T_A, t)$ in the same way.

**Lemma 1 (splitting).** Let $F = (T_{A_1}, \dots, T_{A_k})$ and let $T$ satisfy the path condition. Every relation $R$ that meets $\mathit{at}(F)$ meets exactly one $\mathit{at}(T_{A_i})$, and $R \subseteq C \cup \mathit{at}(T_{A_i})$. Hence $J(F, t) = J(T_{A_1}, t) \times \dots \times J(T_{A_k}, t)$.

*Proof.* The attributes of $R$ lie on one root-to-leaf path $\pi$. A path that meets $\mathit{at}(T_{A_i})$ passes through $A_i$, and it then contains no node of $T_{A_j}$ for $j \ne i$, since the subtrees are disjoint and the nodes of $\pi$ are pairwise comparable. The nodes of $\pi$ above $A_i$ are in $\mathit{anc}(A_i) = C$. So the conditions on $u$ split into one set of conditions for each $u|_{\mathit{at}(T_{A_i})}$, and the set of solutions is the product. $\square$

**Lemma 2 (one subtree).** For a node $A$ and a tuple $t$ on $\mathit{anc}(A)$, let $V$ be the set of line L7. Then

$$J(T_A, t) = \bigcup_{a \in V} \langle A{:}a \rangle \times J(\mathit{kids}(A), t \cup \{A \mapsto a\}).$$

*Proof.* Let $u$ be in $J(T_A, t)$ with $u(A) = a$, and let $R$ contain $A$. Then $(t \cup u)|_R \in R$, and this tuple of $R$ agrees with $t$ on the attributes of $R$ above $A$ and has the value $a$ at $A$. So $a \in V$. The relations that meet $\mathit{at}(\mathit{kids}(A))$ also meet $\mathit{at}(T_A)$, so the rest of $u$ is in $J(\mathit{kids}(A), t \cup \{A \mapsto a\})$.

Conversely, let $a \in V$ and $w \in J(\mathit{kids}(A), t \cup \{A \mapsto a\})$, and put $u = \{A \mapsto a\} \cup w$. Let $R$ meet $\mathit{at}(T_A)$. If $R$ meets $\mathit{at}(\mathit{kids}(A))$, then $(t \cup u)|_R \in R$ by the choice of $w$. Otherwise $R$ contains $A$ and, by the path condition, all its other attributes are in $\mathit{anc}(A)$. Then $(t \cup u)|_R$ is the tuple that agrees with $t$ above $A$ and has $a$ at $A$, which is in $R$ because $a \in V$. $\square$

**Theorem 1 (correctness).** Let $T$ be valid for $Q$. For each call, PRODUCT$(F, t)$ returns $\emptyset$ if $J(F, t) = \emptyset$, and otherwise a product $E$ with $[\![E]\!] = J(F, t)$. UNION$(A, t)$ returns a union $U$ with $[\![U]\!] = J(T_A, t)$, whose pairs have distinct values in increasing order, and none of whose pairs has an empty product. FROMJOIN returns a representation $E$ with $[\![E]\!] = Q(D)$.

*Proof.* By induction on the height of the subtrees. If $F$ is empty, then $J(F, t) = \{()\}$ and PRODUCT returns $()$ at line L6. Otherwise lines L3 to L5 call UNION on each root $A_i$ of $F$, and by the induction hypothesis $[\![U_{A_i}]\!] = J(T_{A_i}, t)$. If one of them is empty, then $J(F, t)$ is empty by Lemma 1, and line L5 returns $\emptyset$. Otherwise line L6 returns the product, which stands for $J(F, t)$ by Lemma 1.

UNION$(A, t)$ takes the values of $V$ in increasing order (lines L7 and L8), and for each $a$ it calls PRODUCT on the children (line L9). By the induction hypothesis that call returns $\emptyset$ exactly when $J(\mathit{kids}(A), t \cup \{A \mapsto a\}) = \emptyset$, and line L10 keeps the pair only otherwise. By Lemma 2 the union of the kept pairs stands for $J(T_A, t)$.

At line L2, $F$ is the list of roots and $t$ is empty. Every attribute of $Q$ is in $T$ and every relation has an attribute, so every relation meets $\mathit{at}(F)$, and $J(F, ()) = Q(D)$. If it is empty, line L2 returns one empty union per root, which stands for $\emptyset$. Line L1 rejects an f-tree that is not valid. $\blacksquare$

**Termination.** Each call of PRODUCT or UNION goes one level down in $T$, and each union iterates over a finite set $V$, which is a subset of a finite index set. So the recursion is finite.

**Theorem 2 (enumeration and counting).** In the output, distinct paths of pairs give distinct tuples. So the enumeration lists each tuple of $Q(D)$ once, and COUNT, which adds over unions and multiplies over products, returns $|Q(D)|$.

*Proof.* The pairs of one union have distinct values of one attribute, so they stand for disjoint sets. The factors of a product are on disjoint attribute sets, so a tuple of the product determines its part in each factor. By induction, each tuple of $[\![E]\!]$ comes from exactly one choice of a pair in each union that the enumeration visits, and the size of a union is the sum of the sizes of its pairs while the size of a product is the product of the sizes of its factors. $\square$

**Theorem 3 (size).** For each attribute $A$, the number of singletons $\langle A{:}\cdot \rangle$ in the output $E$ is $|\pi_{\mathit{path}(A)} Q(D)|$. So the size of $E$ is $\sum_A |\pi_{\mathit{path}(A)} Q(D)|$.

*Proof.* An occurrence of $\langle A{:}a \rangle$ in $E$ is reached from the top by choosing one pair in each union on the way, so it determines a tuple $s$ on $\mathit{path}(A)$, with $s(A) = a$. Two occurrences of $A$ give two different tuples $s$, because the unions above them have distinct values. By Theorem 1 no union in $E$ is empty, so every occurrence lies in a nonempty product on every level, and it extends to a tuple of $[\![E]\!] = Q(D)$ that agrees with $s$. So $s \in \pi_{\mathit{path}(A)} Q(D)$. Conversely, each tuple of $Q(D)$ is reached through one occurrence of $A$, the one for its values on $\mathit{path}(A)$. This is a bijection. $\square$

This is Corollary 7.6 of Olteanu and Závodný (2015). For the bound on the page: $\pi_{\mathit{path}(A)} Q(D)$ is contained in the join of the projections $\pi_{R \cap \mathit{path}(A)} R$ over the relations that meet $\mathit{path}(A)$. By the AGM bound, the join has at most $|D|^{\rho^*}$ tuples, where $\rho^*$ is the fractional edge cover number of the query restricted to $\mathit{path}(A)$. Taking the largest exponent over the nodes gives $|E| \le |T| \cdot |D|^{s(T)}$.

**FACTORIZE.** For one relation $R$, FACTORIZE groups the rows by the value of the root and recurses on each group, and over a forest it builds each tree on the same rows. By induction, $[\![\mathrm{FACTORIZE}(T, R)]\!]$ contains $R$, because each row of $R$ is in its group at every level. If $R$ has some representation over $T$, then on each forest $R$ is the product of its projections on the trees, and on each tree it is the union over the root values of the groups, so by induction the construction stands for $R$ itself. By Theorem 2, the construction then has exactly $|R|$ tuples. So FACTORIZE raises an error exactly when $R$ has no representation over $T$, and the argument of Theorem 3 gives its size $\sum_A |\pi_{\mathit{path}(A)} R|$.
