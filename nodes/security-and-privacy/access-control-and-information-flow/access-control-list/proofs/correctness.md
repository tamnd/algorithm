---
title: The access control lists store exactly the access matrix
proves: [correctness, invariant, termination]
status: full
---

Write $\mathit{acl}$ for the state: a map from each object $o$ to a finite list $\mathit{acl}[o]$ of entries $(s, T)$ with $s$ a subject and $T \subseteq R$. Objects with no list have an empty list. Invariant (A) says: (A1) no two entries of one list have the same subject, and (A2) no entry has $T = \emptyset$.

**Abstraction.** For a state that holds (A1), define the matrix $M(\mathit{acl})$ by $M(\mathit{acl})[s, o] = T$ if $(s, T)$ is an entry of $\mathit{acl}[o]$, and $M(\mathit{acl})[s, o] = \emptyset$ if no entry of $\mathit{acl}[o]$ has subject $s$. By (A1) there is at most one such entry, so $M(\mathit{acl})$ is a function.

**Lemma 1 (lists and matrices are in bijection).** Let $\mathcal{L}$ be the set of states that hold (A), and $\mathcal{M}$ the set of matrices $S \times O \to 2^R$. Then $M : \mathcal{L} \to \mathcal{M}$ is a bijection, up to the order of the entries of each list. Its inverse maps a matrix $A$ to the state whose list for $o$ holds the pairs $(s, A[s, o])$ with $A[s, o] \ne \emptyset$.

*Proof.* Call the second map $L$. For a matrix $A$, the list $L(A)[o]$ has one entry for each subject $s$ with a nonempty cell, so it holds (A1) and (A2), and $M(L(A))[s, o] = A[s, o]$ for nonempty cells by definition and $\emptyset$ for the others, because those subjects have no entry. So $M(L(A)) = A$. For a state $\mathit{acl}$ that holds (A), each entry $(s, T)$ of $\mathit{acl}[o]$ has $T \ne \emptyset$ by (A2), so it is the cell $M(\mathit{acl})[s, o]$ and it appears in $L(M(\mathit{acl}))[o]$. Conversely each entry of $L(M(\mathit{acl}))[o]$ comes from a nonempty cell, which comes from an entry of $\mathit{acl}[o]$. So the two lists hold the same entries, and by (A1) each entry once. $\square$

Lemma 1 is the reason for (A2): without it, a list could hold $(s, \emptyset)$ and the state with this entry and the state without it would give the same matrix.

**Lemma 2 (CHECK).** If $\mathit{acl}$ holds (A1), CHECK$(\mathit{acl}, s, o, r)$ returns true exactly when $r \in M(\mathit{acl})[s, o]$.

*Proof.* The loop of lines L1 and L2 visits the entries of $\mathit{acl}[o]$ in order. If some entry has subject $s$, it is the only one by (A1), so line L2 returns $r \in T$ for $T = M(\mathit{acl})[s, o]$. If none has subject $s$, the loop ends and line L3 returns false, and $M(\mathit{acl})[s, o] = \emptyset$ does not contain $r$. $\square$

**Lemma 3 (GRANT).** If $\mathit{acl}$ holds (A), then after GRANT$(\mathit{acl}, s, o, r)$ the state holds (A), and its matrix is $M(\mathit{acl})$ with $r$ added to cell $[s, o]$ and no other cell changed.

*Proof.* If $\mathit{acl}[o]$ has an entry $(s, T)$, line L5 replaces it with $(s, T \cup \{r\})$ and returns. The list keeps the same subjects, so (A1) holds, and $T \cup \{r\}$ is not empty, so (A2) holds. Only cell $[s, o]$ changes, from $T$ to $T \cup \{r\}$. If there is no such entry, the loop ends without a return and line L6 appends $(s, \{r\})$. No other entry of the list has subject $s$, so (A1) holds, and $\{r\} \ne \emptyset$, so (A2) holds. Cell $[s, o]$ changes from $\emptyset$ to $\{r\} = \emptyset \cup \{r\}$. In both cases the lists of other objects are not touched. $\square$

**Lemma 4 (REVOKE).** If $\mathit{acl}$ holds (A), then after REVOKE$(\mathit{acl}, s, o, r)$ the state holds (A), and its matrix is $M(\mathit{acl})$ with $r$ removed from cell $[s, o]$ and no other cell changed.

*Proof.* If $\mathit{acl}[o]$ has an entry $(s, T)$, line L9 replaces $T$ with $T' = T \setminus \{r\}$. If $T' = \emptyset$, line L10 removes the entry, and the cell becomes $\emptyset = T'$; otherwise the entry $(s, T')$ stays, with $T' \ne \emptyset$. Removing an entry or changing its set does not add a subject, so (A1) holds, and in both cases no empty set is stored, so (A2) holds. If there is no entry for $s$, the loop of lines L7 and L8 ends with no change, and the cell was $\emptyset = \emptyset \setminus \{r\}$. $\square$

**Lemma 5 (REVOKE-SUBJECT).** If $\mathit{acl}$ holds (A), then after REVOKE-SUBJECT$(\mathit{acl}, s)$ the state holds (A), and its matrix is $M(\mathit{acl})$ with every cell of row $s$ set to $\emptyset$ and every other cell unchanged.

*Proof.* The loop of lines L12 and L13 visits each object $o$ once. By (A1) the list $\mathit{acl}[o]$ has at most one entry for $s$, and line L13 removes it, which sets cell $[s, o]$ to $\emptyset$. Entries of other subjects are not changed. Removing entries keeps (A1) and (A2). $\square$

**Lemma 6 (objects).** CREATE-OBJECT$(o)$ adds an empty list, which holds (A) and gives the column of $o$ all empty. DELETE-OBJECT$(o)$ removes the list of $o$, so the column of $o$ becomes all empty in $M$, and the other lists are not changed.

*Proof.* Immediate from the definitions of the two operations and of $M$. $\square$

**Theorem.** Start from the empty state, which holds (A) and has the all-empty matrix. After any finite sequence of operations, the state holds (A), its matrix $M(\mathit{acl})$ is the matrix that the same sequence of abstract operations gives, and each CHECK in the sequence returns the abstract answer $r \in A[s, o]$.

*Proof.* By induction on the length of the sequence, with Lemmas 3 to 6 for the step of each changing operation and Lemma 2 for each CHECK, which changes nothing. $\square$

**Termination and cost.** Each loop of lines L1, L4 and L7 visits each entry of one list at most once and returns at the first match, so it runs at most $|\mathit{acl}[o]| \le s$ rounds by (A1). The loop of line L12 visits each object once, and line L13 scans one list, so REVOKE-SUBJECT does $O(o + n)$ steps in total, where $n = \sum_o |\mathit{acl}[o]|$ is, by Lemma 1, the number of nonempty cells. $\blacksquare$
