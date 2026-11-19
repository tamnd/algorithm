---
title: The incremental algorithm returns a distinguishing description exactly when the preferred attributes allow one, and the minimal description problem is NP-hard
proves: [correctness]
status: full
---

Fix a referent $r$, a finite set $C_0$ of distractors and a non-empty list $P = (A_1, \ldots, A_p)$ of attributes. For an attribute $A$ that $r$ has, write $V_A$ for the value of $A$ on $r$, and let $\mathrm{out}(A) = \{x \in C_0 : x \text{ has a value for } A \text{ and it is not } V_A\}$; for an attribute that $r$ does not have, $\mathrm{out}(A) = \{\}$. A set $L$ of pairs $\langle A, V_A \rangle$ *distinguishes* $r$ when $\bigcup_{\langle A, V \rangle \in L} \mathrm{out}(A) = C_0$. Line L4 computes $R = \mathrm{out}(A) \cap C$ for the current $C$.

**Lemma 1 (invariant).** At the start of each round of line L2, and at line L8, $C = C_0 \setminus \bigcup_{\langle A, V \rangle \in L} \mathrm{out}(A)$, and every pair in $L$ is true of $r$.

*Proof.* Before the first round $L = \{\}$ and $C = C_0$. A round with attribute $A$ either changes nothing (when $R = \{\}$), or adds $\langle A, V_A \rangle$ to $L$ and removes $R = \mathrm{out}(A) \cap C$ from $C$. In the second case the new $C$ is $C \setminus \mathrm{out}(A)$, which is the old right side minus $\mathrm{out}(A)$. The value added is $V_A$, the value of $r$. $\square$

**Theorem 1 (soundness).** If the algorithm returns a list $L$, then $L$ distinguishes $r$, every pair of $L$ is true of $r$, and the attribute pairs of $L$ other than the type pair added at line L9 each rule out a distractor that no earlier pair ruled out.

*Proof.* Line L10 runs only when $C = \{\}$, so by Lemma 1 the pairs of $L$ rule out all of $C_0$. Adding the type pair at line L9 keeps this true, and the type pair is true of $r$. A pair is added at line L6 only when $R \ne \{\}$, and by Lemma 1 the elements of $R$ were not ruled out by earlier pairs. $\square$

**Theorem 2 (completeness for $P$).** The algorithm returns failure if and only if the full set $\{\langle A, V_A \rangle : A \in P, A \text{ is an attribute of } r\}$ does not distinguish $r$.

*Proof.* Suppose some $x \in C_0$ is in no $\mathrm{out}(A)$ for $A \in P$. Then by Lemma 1, $x \in C$ at every test of line L8, so line L10 never runs and line L11 returns failure. Conversely, suppose every $x \in C_0$ is in $\mathrm{out}(A)$ for some $A \in P$, and suppose the algorithm reaches the round of the last attribute $A_p$ without returning. Take any $x \in C_0$ and the first $A_k$ with $x \in \mathrm{out}(A_k)$. In round $k$, either $x$ was already removed, or $x \in R$, so $R \ne \{\}$ and line L7 removes $x$. Elements never come back into $C$. So after round $p$, line L8 finds $C = \{\}$ and line L10 returns $L$. $\square$

**Theorem 3 (cost).** The algorithm runs in $O(p \cdot |C_0|)$ time with hash table lookups for the attribute values, and uses $O(p + |C_0|)$ extra space.

*Proof.* There are at most $p$ rounds. In a round, line L4 checks each element of $C$ once, and line L7 removes the elements of $R$ in $O(|C|)$ time. Every other line takes $O(1)$ time, and line L9 checks $L$, of size at most $p$, once. $\square$

**Theorem 4 (no constant factor).** For every $k \ge 2$ there is an input where the minimal distinguishing description has 1 attribute pair and the algorithm returns $k$ attribute pairs.

*Proof.* Let $r$ have attributes $A_1, \ldots, A_k$, all with value 1, and no type. Let $C_0 = \{x_1, \ldots, x_{k-1}, y\}$. The distractor $x_i$ has value 0 for $A_i$ and for $A_k$, and value 1 for the other attributes; $y$ has value 0 for $A_k$ and value 1 for the other attributes. Then $\mathrm{out}(A_i) = \{x_i\}$ for $i < k$ and $\mathrm{out}(A_k) = C_0$. With $P = (A_1, \ldots, A_k)$, round $i < k$ finds $x_i \in C$, adds $\langle A_i, 1 \rangle$ and removes $x_i$. The distractor $y$ stays in $C$ until round $k$, which adds $\langle A_k, 1 \rangle$. So the result has $k$ pairs, while the single pair $\langle A_k, 1 \rangle$ rules out all of $C_0$. $\square$

**Theorem 5 (the minimal description problem is NP-complete).** The problem "given $r$, $C_0$, a set of attributes and an integer $s$, is there a distinguishing description with at most $s$ pairs?" is NP-complete.

*Proof.* It is in NP: a description of at most $s$ pairs is checked with Lemma 1 in polynomial time. For hardness, reduce from set cover, which Karp (1972) showed NP-complete: a universe $U = \{1, \ldots, m\}$, sets $S_1, \ldots, S_k \subseteq U$ and an integer $s$; is there a cover by at most $s$ sets? Build a referent $r$ with attributes $A_1, \ldots, A_k$, all with value 1, and one distractor $x_u$ for each $u \in U$, where $x_u$ has value 0 for $A_j$ if $u \in S_j$ and value 1 otherwise. Then $\mathrm{out}(A_j) = \{x_u : u \in S_j\}$. A set $J$ of indices covers $U$ exactly when $\{\langle A_j, 1 \rangle : j \in J\}$ rules out every $x_u$. So a cover of size at most $s$ exists if and only if a distinguishing description of size at most $s$ exists. The construction takes $O(mk)$ time. $\square$

Conversely, the minimal description problem is a set cover instance with universe $C_0$ and sets $\mathrm{out}(A)$, so the greedy set cover algorithm (Johnson 1974) finds a description at most $H(|C_0|)$ times the minimal size, where $H$ is the harmonic number. Dale and Reiter (1995, Section 2.2) state this correspondence; Theorem 5 is the formal reduction in the direction that gives hardness. $\blacksquare$
