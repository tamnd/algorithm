---
title: Capability lists keep attenuation, and revocation removes exactly the derived copies
proves: [correctness, invariant, termination]
status: full
---

A state is a finite set $C$ of capability records. Each record $c$ has a holder $h(c)$, a slot $\sigma(c)$, an object $\mathrm{obj}(c)$, a set of rights $\mathrm{rights}(c) \subseteq R$, a parent $p(c) \in C \cup \{\bot\}$, and a set of children $\mathrm{ch}(c)$. The c-list of $s$ maps each slot $i$ to the record $c$ with $h(c) = s$ and $\sigma(c) = i$, if there is one. Each record also has a number $\mathrm{id}(c)$, given in the order of creation.

Invariant (C):

- (C1) The map from records to pairs $(h(c), \sigma(c))$ is one to one, and the c-lists hold exactly these pairs.
- (C2) For each $c$ with $p(c) \ne \bot$: $p(c) \in C$, $\mathrm{obj}(c) = \mathrm{obj}(p(c))$, $\mathrm{rights}(c) \subseteq \mathrm{rights}(p(c))$, and $\mathrm{id}(p(c)) < \mathrm{id}(c)$.
- (C3) For each $c$: $\mathrm{ch}(c) = \{d \in C : p(d) = c\}$.

The matrix that the state stands for is $M(C)[s, o] = \bigcup \{\mathrm{rights}(c) : c \in C, h(c) = s, \mathrm{obj}(c) = o\}$.

**Lemma 1 (the parent links form a forest).** Under (C2), following parent links from any record ends at a root, a record with $p = \bot$, after finitely many steps.

*Proof.* Each step strictly decreases the id, by (C2), and ids are natural numbers. Each parent is in $C$ by (C2), so the walk stays in $C$ until it reaches a record with no parent. $\square$

Write $\mathrm{root}(c)$ for this root, and $D(c)$ for the set of descendants of $c$ together with $c$: the records whose walk passes through $c$.

**Lemma 2 (CREATE and DELEGATE keep (C)).** Each of them adds one record and changes nothing else except one children set.

*Proof.* Line L2 stores a record with $p = \bot$ in a new slot of $s$. The slot counter of $s$ only grows, so the pair $(s, \sigma)$ is new and (C1) holds; (C2) and (C3) say nothing new about a root. Line L9 is reached only after line L6 found a record $c$ in slot $i$ of $s$ and line L8 checked $T \subseteq \mathrm{rights}(c)$. It stores a record $d$ with $\mathrm{obj}(d) = \mathrm{obj}(c)$, $\mathrm{rights}(d) = T$, $p(d) = c$, a new slot of $t$ and a new id larger than every stored id, and adds $d$ to $\mathrm{ch}(c)$. So (C1) holds as before, (C2) holds for $d$, and (C3) holds for $c$ and for $d$, which has no children yet. If line L6 or L8 returns none, nothing changes. $\square$

**Lemma 3 (REVOKE removes exactly $D(c)$).** Let slot $i$ of $s$ hold $c$. Then REVOKE$(s, i)$ removes exactly the records of $D(c)$, clears their slots, keeps (C), and returns $|D(c)|$.

*Proof.* Line L11 removes $c$ from $\mathrm{ch}(p(c))$ if $c$ has a parent, and starts the stack with $c$. Each round of lines L13 and L14 pops a record, pushes its children and clears its slot. By (C3) the children pushed are exactly the records whose parent is the popped one. So every record pushed is in $D(c)$, and by induction on the length of the walk from a record of $D(c)$ up to $c$, every record of $D(c)$ is pushed. A record has one parent, so it is in one children set and is pushed at most once; by Lemma 1 there are no cycles, so the loop of line L12 ends after $|D(c)|$ rounds, and the count is $|D(c)|$.

After the loop, the records left are $C \setminus D(c)$. (C1) holds because the slots of the removed records were cleared and no other slot changed. For (C2), take a record $d$ that is left with $p(d) \ne \bot$. If $p(d) \in D(c)$, then $d \in D(c)$ by the definition of $D$, which is not the case; so $p(d)$ is left, and the other conditions of (C2) did not change. For (C3), the only children set that held a removed record and belongs to a record that is left is $\mathrm{ch}(p(c))$, and line L11 removed $c$ from it. If slot $i$ of $s$ is empty, line L10 returns 0 and nothing changes. $\square$

**Theorem 1 (attenuation, and no forgery).** In every state reached from the empty state, every record $c$ has $\mathrm{obj}(c) = \mathrm{obj}(\mathrm{root}(c))$ and $\mathrm{rights}(c) \subseteq \mathrm{rights}(\mathrm{root}(c))$, and the root was made by a call of CREATE. So $r \in M(C)[s, o]$ only if a call CREATE$(s', o, T)$ with $r \in T$ was made, and a chain of DELEGATE calls led from it to a record held by $s$.

*Proof.* The empty state holds (C). By Lemmas 2 and 3 every reachable state holds (C); CHECK changes nothing. Apply (C2) along the walk of Lemma 1: the object stays the same at each step and the set of rights can only grow toward the root, and $\subseteq$ is transitive. A root is made only by line L2, and each other record only by line L9, which is a DELEGATE call from the holder of its parent. $\square$

**Theorem 2 (CHECK).** CHECK$(s, i, o, r)$ returns true exactly when slot $i$ of $s$ holds a record $c$ with $\mathrm{obj}(c) = o$ and $r \in \mathrm{rights}(c)$.

*Proof.* Line L3 returns false for an empty slot. Otherwise, by (C1), slot $i$ names one record, and lines L4 and L5 return the stated test on it. $\square$

**Theorem 3 (the oracle of the tests).** Keep every record ever made, with a flag for each record on which REVOKE was called. Call a record live when neither it nor any ancestor has the flag. Then the stored set $C$ is exactly the set of live records.

*Proof.* By induction on the operations. CREATE and DELEGATE add a record with no flag whose parent, if any, is stored and so live by the hypothesis; both sides gain the same record. REVOKE on the record $c$ sets the flag of $c$, which makes exactly $D(c)$ not live, among the records that were live: a live record loses its status only if $c$ is on its walk to the root. By Lemma 3, REVOKE removes exactly $D(c)$. A REVOKE on an empty slot changes neither side, because an empty slot names no live record. $\square$

**Termination and cost.** CREATE, CHECK and DELEGATE run no loop; each does a constant number of table operations and, in line L8, one subset test, which is one word operation when the rights fit in a word. REVOKE runs $|D(c)|$ rounds by Lemma 3, each with a constant number of table operations plus the pushes of the children, and each record is pushed once, so the total is $O(|D(c)|)$. $\blacksquare$
