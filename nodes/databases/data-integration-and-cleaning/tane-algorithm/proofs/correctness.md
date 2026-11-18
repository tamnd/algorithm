---
title: TANE outputs each minimal functional dependency exactly once
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page for exact dependencies ($\varepsilon = 0$, key pruning on). The relation $r$ has $n$ tuples over the attribute set $R$. All dependencies are non-trivial, so in $Y \to A$ we have $A \notin Y$. $Y \to A$ is *minimal* if it holds and $Z \to A$ fails for each proper subset $Z \subsetneq Y$. A set is *processed* if it is in some level $L_\ell$ when line L5 runs, and *kept* if it is still in $L_\ell$ after line L6. We write $D(X)$ for the set that the algorithm stores as $C^+(X)$, and $C^+(X)$ for the set of the definition:

$$C^+(X) = \{ A \in R : X \setminus \{A, B\} \to B \text{ fails for every } B \in X \}.$$

We use two facts about dependencies. (Augmentation) If $Z \to B$ holds and $Z \subseteq Z'$, then $Z' \to B$ holds. (Transitivity) If $Z \to B$ holds for each $B \in W$ and $W \to A$ holds, then $Z \to A$ holds.

**Lemma 1 (the test of line L10).** For attribute sets $Z$ and an attribute $A$, $Z \to A$ holds if and only if $e(Z) = e(Z \cup \{A\})$, where $e(X) = \|\hat\pi_X\| - |\hat\pi_X|$.

*Proof.* A class of size 1 adds $1 - 1 = 0$ to $\sum_c (|c| - 1)$, so $e(X) = n - |\pi_X|$, where $\pi_X$ is the full partition of the tuples by their values on $X$. Each class of $\pi_{Z \cup \{A\}}$ lies inside one class of $\pi_Z$, so $|\pi_{Z \cup \{A\}}| \ge |\pi_Z|$, with equality if and only if the two partitions are equal. They are equal if and only if two tuples that agree on $Z$ always agree on $A$, which is $Z \to A$. $\square$

The stripped product of line L19 returns $\hat\pi_{Y \cup Z}$ from $\hat\pi_Y$ and $\hat\pi_Z$: two tuples are in one class of $\pi_{Y \cup Z}$ if and only if they share a class of $\pi_Y$ and a class of $\pi_Z$, and classes of size 1 can be dropped from either input because a tuple alone in its class is alone in the product too. So every $e$ value of the run is the right one.

**Lemma 2 (antimonotone).** If $X \subseteq X'$, then $C^+(X') \subseteq C^+(X)$.

*Proof.* Let $A \in C^+(X')$ and $B \in X$. Then $X \setminus \{A, B\} \subseteq X' \setminus \{A, B\}$. If $X \setminus \{A, B\} \to B$ held, augmentation would give $X' \setminus \{A, B\} \to B$ with $B \in X'$, which is false. $\square$

**Lemma 3 (generation).** Every subset of a processed set is processed. A set $X \neq \emptyset$ is processed if every set $X \setminus \{B\}$ with $B \in X$ is processed and kept.

*Proof.* Line L19 adds $X$ only when every $X \setminus \{A\}$ is kept, and level 1 holds all singletons, whose only proper subset $\emptyset$ is in $L_0$. Induction on the size gives the first part. For the second part, let $|X| = \ell + 1 \ge 2$ and let $Y$ and $Z$ be $X$ without its largest and without its second largest attribute. $Y$ and $Z$ are kept sets of level $\ell$ with the same first $\ell - 1$ attributes, so line L18 meets the pair, and line L19 adds $X$. For $|X| = 1$, line L2 puts $X$ in $L_1$. $\square$

**Lemma 4 (the stored sets are exact).** For every processed set $X$, after line L12 has handled $X$, $D(X) = C^+(X)$.

*Proof.* By induction on $|X|$. For $X = \emptyset$, $D(\emptyset) = R = C^+(\emptyset)$, because the condition is empty. Let $|X| \ge 1$. By Lemma 3 every $X \setminus \{B\}$ is processed, so by induction line L8 sets $D(X) = I$ with $I = \bigcap_{B \in X} C^+(X \setminus \{B\})$. By Lemma 2, $C^+(X) \subseteq I$. We show that lines L9 to L12 remove exactly the elements of $I \setminus C^+(X)$.

*Elements $A \in X$.* Here $A \in C^+(X)$ means: $X \setminus \{A, B\} \to B$ fails for every $B \in X \setminus \{A\}$, and $X \setminus \{A\} \to A$ fails. The term $B = A$ of $I$ is $C^+(X \setminus \{A\})$, and $A \in C^+(X \setminus \{A\})$ says exactly that $X \setminus \{A, B\} \to B$ fails for every $B \in X \setminus \{A\}$. So for $A \in X \cap I$, $A \in C^+(X)$ if and only if $X \setminus \{A\} \to A$ fails. Line L9 visits every $A \in X \cap I$ (line L12 removes only $A$ itself and attributes outside $X$, so no other element of $X$ leaves the loop), line L10 tests $X \setminus \{A\} \to A$ by Lemma 1, and line L12 removes $A$ when it holds.

*Elements $A \notin X$.* Here $X \setminus \{A, B\} = X \setminus \{B\}$, so $A \in C^+(X)$ if and only if $X$ has no attribute $C$ with $X \setminus \{C\} \to C$; call such an $X$ *irredundant*. This condition does not depend on $A$. If $X$ is irredundant, line L12 must remove nothing outside $X$, and indeed it removes $R \setminus X$ only after line L10 finds some $C \in X$ with $X \setminus \{C\} \to C$. If $X$ is not irredundant, every $A \notin X$ must go. There are two cases. (a) Some $X \setminus \{B\}$ with $B \in X$ is not irredundant. Then $A \notin C^+(X \setminus \{B\})$ for each $A \notin X$, because $A \notin X \setminus \{B\}$; so $A \notin I$ already. (b) Every $X \setminus \{B\}$ is irredundant, and some $C \in X$ has $X \setminus \{C\} \to C$. We show $C \in I$; then line L10 tests $C$, finds the dependency, and line L12 removes $R \setminus X$. The term $B = C$: $C \notin X \setminus \{C\}$, so $C \in C^+(X \setminus \{C\})$ because $X \setminus \{C\}$ is irredundant. A term $B \neq C$: let $W = X \setminus \{B\}$, which holds $C$ and is irredundant. For $B' \in W$, the set $W \setminus \{C, B'\}$ is a subset of $W \setminus \{B'\}$, and $W \setminus \{B'\} \to B'$ fails, so by augmentation $W \setminus \{C, B'\} \to B'$ fails too. Hence $C \in C^+(W)$. $\square$

**Lemma 5.** Let $Y \to A$ be minimal and $X = Y \cup \{A\}$. Then $A \in C^+(Z)$ for every proper subset $Z \subsetneq X$, and $A \in C^+(Y \setminus \{B\} \cup \{A\})$ for every $B \in Y$.

*Proof.* First, $Y$ is irredundant: if $Y \setminus \{C\} \to C$ for some $C \in Y$, then $Y \setminus \{C\}$ determines every attribute of $Y$, and transitivity gives $Y \setminus \{C\} \to A$, against minimality. So $A \in C^+(Y)$, as in the second case of Lemma 4. Next let $B \in Y$ and $W = Y \setminus \{B\} \cup \{A\}$. For $C = A$: $W \setminus \{A\} = Y \setminus \{B\}$, and $Y \setminus \{B\} \to A$ fails by minimality. For $C \in Y \setminus \{B\}$: $W \setminus \{A, C\} = Y \setminus \{B, C\}$, and if it determined $C$, augmentation would give $Y \setminus \{C\} \to C$, against irredundance. So $A \in C^+(W)$. The sets $Y$ and $W$ are exactly the sets $X \setminus \{B'\}$ for $B' \in X$, so by Lemma 2 every proper subset of $X$ has $A$ in its $C^+$. $\square$

**Soundness.** Each output is a minimal dependency.

*Line L11.* It outputs $X \setminus \{A\} \to A$ after line L10 has shown that it holds. Before line L12, $A \in I \subseteq C^+(X \setminus \{B\})$ for each $B \in X \setminus \{A\}$. The set $Z = X \setminus \{B\}$ holds $A$ and is processed, and by Lemma 4 $A \in C^+(Z)$ means in particular that $Z \setminus \{A\} \to A$ fails. So $X \setminus \{A, B\} \to A$ fails for every $B$. A proper subset of $X \setminus \{A\}$ lies inside some $X \setminus \{A, B\}$, so by augmentation it does not determine $A$. The dependency is minimal.

*Line L16.* $X$ is a superkey, so $X \to A$ holds. For each $B \in X$, let $Y_B = X \setminus \{B\} \cup \{A\}$. If $Y_B$ was processed, the test reads $A \in D(Y_B) = C^+(Y_B)$ by Lemma 4, and the condition for the attribute $A$ itself says that $Y_B \setminus \{A\} = X \setminus \{B\}$ does not determine $A$. If $Y_B$ was not processed, the code tests directly that $X \setminus \{B\} \to A$ fails. Either way no $X \setminus \{B\}$ determines $A$, and by augmentation no proper subset of $X$ does. The dependency is minimal.

**Completeness.** Let $Y \to A$ be minimal and $X = Y \cup \{A\}$. By Lemma 5 and Lemma 4, every processed proper subset of $X$ has a non-empty stored set, so line L14 deletes none of them.

*Case 1: no proper subset of $X$ is a superkey.* Then line L17 deletes none of them either, and Lemma 3 by induction on the size shows that every proper subset of $X$ is processed and kept, and that $X$ is processed. At line L8, $A \in I$ by Lemma 5, and $A \in X$, so line L9 visits $A$; line L10 finds that $Y \to A$ holds, and line L11 outputs it.

*Case 2: some proper subset $Z \subsetneq X$ is a superkey.* If $A \notin Z$, then $Z \subseteq Y$ and $Z \to A$, so $Z = Y$ by minimality. If $A \in Z$, then $Z \setminus \{A\} \subseteq Y$, and $Y$ determines every attribute of $Z$ (those of $Y$ trivially, and $A$ by assumption), so $Y$ is a superkey by transitivity. Either way $Y$ is a superkey. No proper subset $W$ of $Y$ is a superkey, because $W \to A$ would contradict minimality. So, as in Case 1, every proper subset of $Y$ is processed and kept and $Y$ is processed. $D(Y) = C^+(Y)$ holds $A$ by Lemma 5, so line L14 keeps $Y$, and line L15 finds that $Y$ is a superkey. At line L16, $A \in D(Y) \setminus Y$. For each $B \in Y$, if $Y_B$ was processed, then $A \in C^+(Y_B)$ by Lemma 5; if not, the direct test succeeds because $Y \setminus \{B\} \to A$ fails. So line L16 outputs $Y \to A$.

**No dependency is output twice.** Line L11 outputs $Y \to A$ only while it processes $Y \cup \{A\}$, and line L16 only while it processes $Y$, and each set is processed at most once, in the level of its size. If line L16 outputs $Y \to A$, then line L17 deletes $Y$, so by Lemma 3 the set $Y \cup \{A\}$ is never processed, and line L11 never outputs $Y \to A$.

**Termination.** Level $\ell$ holds only sets of size $\ell$, and line L7 moves to the next size. A level of size $|R| + 1$ is empty, so the loop of line L4 runs at most $|R| + 1$ times, and each pass handles finitely many sets. $\blacksquare$

**The approximate version.** With $\varepsilon > 0$, line L10 tests $e(X \setminus \{A\} \to A) \le \varepsilon$, line L12 removes $R \setminus X$ only when the dependency holds exactly, and key pruning is off. This proof does not cover that version. Lemma 4 uses augmentation and transitivity of exact dependencies, and approximate dependencies are not transitive.
