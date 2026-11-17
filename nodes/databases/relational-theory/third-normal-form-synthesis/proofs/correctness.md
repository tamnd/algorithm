---
title: 3NF synthesis gives a lossless, dependency-preserving 3NF decomposition
proves: [correctness]
status: full
---

Let $G$ be the minimal cover from line L1. So $G^+ = F^+$, each FD of $G$ has the form $X \to A$ with $A \notin X$, no FD of $G$ is implied by the others, and no left-side attribute is extraneous: for $X \to A$ in $G$ and $B \in X$, $A \notin (X - B)^+$. All closures below are under $G$, which gives the same closures as $F$.

For a schema $R \subseteq U$, the FDs that *hold in* $R$ are the FDs $Y \to B$ of $F^+$ with $Y \cup \{B\} \subseteq R$. A set $Y \subseteq R$ is a superkey of $R$ if $R \subseteq Y^+$.

**Lemma 1.** For each left side $X$ of $G$, $X$ is a key of $R_X$.

*Proof.* Each attribute of $R_X$ is in $X$ or is an $A$ with $X \to A$ in $G$, so $R_X \subseteq X^+$, and $X$ is a superkey of $R_X$. Suppose a proper subset $X' \subset X$ is a superkey of $R_X$. Some FD $X \to A$ is in $G$, and $A \in R_X \subseteq X'^+$. Take $B \in X - X'$. Then $X' \subseteq X - B$, so $A \in X'^+ \subseteq (X - B)^+$, and $B$ is extraneous in $X \to A$. This contradicts minimality. $\square$

**Lemma 2.** Each $R_X$ is in 3NF.

*Proof.* Let $Y \to B$ hold in $R_X$, with $B \notin Y$ and $Y$ not a superkey of $R_X$. We show that $B$ is prime in $R_X$.

If $B \in X$, then $B$ is in the key $X$ of $R_X$ (Lemma 1), so it is prime.

If $B \notin X$, then $X \to B$ is in $G$. Let $G' = G - \{X \to B\}$. Since $Y$ is not a superkey of $R_X$ and $X$ is, $X \not\subseteq Y^+$. Compute $Y^+$ under $G$ by firing FDs. The FD $X \to B$ can fire only when $X$ is inside the current set, which is inside $Y^+$, so it never fires. So the closure of $Y$ under $G'$ is the same set, and $B \in Y^+_{G'}$.

Each attribute of $Y$ is in $X$, or is an $A \ne B$ with $X \to A$ in $G$, and that FD is in $G'$. So $Y \subseteq X^+_{G'}$, and then $B \in Y^+_{G'} \subseteq X^+_{G'}$. So $G'$ implies $X \to B$, and $X \to B$ is redundant in $G$. This contradicts minimality. So the case $B \notin X$ cannot occur. $\square$

**Lemma 3.** A key $K$ of $U$ is in 3NF as a schema, and in fact no nontrivial FD holds in it.

*Proof.* Let $Y \to B$ hold in $K$ with $B \notin Y$. Then $Y \subseteq K - B$, so $B \in Y^+ \subseteq (K - B)^+$, and $K \subseteq (K - B)^+$. Then $(K - B)^+ = U$, and $K$ is not minimal, a contradiction. $\square$

**Lemma 4 (line L7).** Removing a schema $S$ that is a subset of a kept schema $T$ keeps the three properties.

*Proof.* The other schemas do not change, so each stays in 3NF. Each FD inside $S$ is inside $T$, so preservation still holds. For losslessness, the proof of Lemma 6 below uses only that, for each FD $X \to A$ of $G$, some schema of the final list holds $X \cup \{A\}$, and that some schema holds a key. Both stay true when $S \subseteq T$ is replaced by $T$. $\square$

Lemmas 2, 3 and 4 show that each schema of the output is in 3NF.

**Lemma 5 (dependency preservation).** Each FD $X \to A$ of $G$ has $X \cup \{A\} \subseteq R_X$, and $R_X$ or a schema that contains it is in the output. So the FDs that hold in the output schemas include $G$, and they imply $G^+ = F^+$. $\square$

**The chase.** Let the output be $R_1, \ldots, R_s$. Build a tableau with one row $i$ per schema. Row $i$ has the distinguished symbol $a_A$ in each column $A \in R_i$, and a new symbol $b_{i,A}$ in each other column. A *chase step* with an FD $X \to A$ of $G$ takes two rows that have equal symbols in all columns of $X$ and different symbols in column $A$, and replaces one of the two symbols by the other everywhere in the tableau, preferring a distinguished symbol.

**Lemma 6 (soundness of the chase).** If some sequence of chase steps produces a row of only distinguished symbols, then the decomposition is lossless.

*Proof.* Let $r$ satisfy $F$, so it satisfies $G$. Always $r \subseteq \pi_{R_1}(r) \bowtie \cdots \bowtie \pi_{R_s}(r)$, because each $t \in r$ agrees with its own projections. For the other inclusion, let $t$ be in the join. Then for each $i$ there is $t_i \in r$ with $t_i[R_i] = t[R_i]$. Define a map $h$ on symbols: $h(a_A) = t(A)$ and $h(b_{i,A}) = t_i(A)$. Then $h$ maps row $i$ to the tuple $t_i \in r$.

We claim that after each chase step, $h$ still maps each row to a tuple of $r$, and $h(a_A) = t(A)$ still holds. A step uses $X \to A$ and two rows $u, v$ with equal symbols on $X$. Then $h(u)$ and $h(v)$ are tuples of $r$ that agree on $X$, so they agree on $A$, since $r$ satisfies $X \to A$. So the two symbols in column $A$ have the same image under $h$, and replacing one by the other changes no image. The map $h$ is the same function on the remaining symbols, so the claim holds.

At the end, a row of distinguished symbols is mapped by $h$ to $(t(A))_{A \in U} = t$, and this tuple is in $r$. So the join equals $r$. $\square$

**Lemma 7 (losslessness).** The output decomposition is lossless.

*Proof.* After lines L5 and L6, some schema $R_0$ of the output holds a key $K$ of $U$: either line L5 found a schema $T$ with $T^+ = U$, which holds a key, or line L6 added one. By Lemma 4, after line L7 a schema that contains it is still in the output; call its row $\rho$. Row $\rho$ is distinguished on $K$.

Run the closure of $K$ under $G$ and list the FDs in the order they add new attributes: $X_1 \to A_1, \ldots, X_p \to A_p$, with $X_j \subseteq K \cup \{A_1, \ldots, A_{j-1}\}$ and $K \cup \{A_1, \ldots, A_p\} = K^+ = U$. We show by induction on $j$ that the chase can make $\rho$ distinguished on $K \cup \{A_1, \ldots, A_j\}$.

For $j = 0$ this holds. For the step to $j$, let $\sigma$ be the row of a schema that holds $X_j \cup \{A_j\}$; it exists by Lemma 5. Row $\sigma$ is distinguished on $X_j \cup \{A_j\}$ from the start, and chase steps never replace a distinguished symbol by another symbol. By induction, $\rho$ is distinguished on $X_j$. So $\rho$ and $\sigma$ agree on $X_j$. If $\rho$ is not yet distinguished in column $A_j$, a chase step with $X_j \to A_j$ replaces its symbol there by $a_{A_j}$.

After step $p$, $\rho$ is distinguished on $U$. By Lemma 6, the decomposition is lossless. $\square$

**Theorem.** 3NF-SYNTHESIS returns schemas $R_1, \ldots, R_s$ whose union is $U$, each in 3NF, with a lossless join, that preserve $F$.

*Proof.* The union is $U$: a key schema or a schema with $T^+ = U$ is in the list, and each attribute outside it is the right side of an FD of $G$ (it is in $U = K^+$ and not in $K$), so it is in some $R_X$. Lines L5 to L7 only add the key and remove subsets of other schemas, so the union does not change. The three properties are Lemmas 2 to 5 and 7. $\square$
