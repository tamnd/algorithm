---
title: DRed returns the least model of the updated stored facts
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $P$ is a Datalog program without negation. For a set $S$ of stored (EDB) facts, $P(S)$ is the least model of $P$ on $S$: the least set that contains $S$ and is closed under the rules. A *rule instance* is a rule with a map from its variables to constants. It is *true* in a set $I$ when all its body facts are in $I$. The input satisfies $M = P(E)$, and IDB predicates do not occur in $E$, $E^-$ or $E^+$.

After line L1, $E^+ \cap E = \emptyset$, $E^- \subseteq E$ and $E^- \cap E^+ = \emptyset$, and the new stored set is $E' = (E \setminus E^-) \cup E^+$, the same set as before line L1. Let $M' = P(E')$. Write $M$ for the old model throughout, $D$ for the set after the loop of line L3, $M_6 = M \setminus D$ for the set after line L6, $R$ for the set of line L7, and $M_f$ for the returned model.

**Claim.** Both loops stop, and $M_f = M'$.

**Termination.** In the loop of line L3, each $\Delta$ after the first is disjoint from the $D$ of the round before, and $D \subseteq M$, since $E^- \subseteq E \subseteq M$ and each head of line L4 is the head of an instance true in $M$, and $M$ is closed under the rules. So $D$ grows while $\Delta \ne \emptyset$ and is bounded by the finite set $M$. In the loop of line L9, each new $\Delta$ is disjoint from the $M$ before it. Lemma 2 below shows that $M$ stays inside the finite set $M'$, so this loop stops too.

**Lemma 1 (closure of $D$).** If a rule instance is true in $M$ and has a body fact in $D$, its head is in $D$.

*Proof.* The body fact entered $D$ as part of some $\Delta$, at line L2 or line L5. In the next round, line L4 reads that $\Delta$ and finds the instance, since it is true in $M$. Its head is in $N$, so it is in $D$ after line L5 of that round, whether or not it was there before. The loop runs this next round, because it stops only when $\Delta$ is empty. $\square$

**Lemma 2 (soundness).** $M_6 \subseteq M'$, $R \subseteq M'$, and every set $M$ of lines L8 to L11 is a subset of $M'$.

*Proof.* Give each fact of $M$ its *height*: 0 for a stored fact, and otherwise 1 plus the least possible largest height of the body facts of an instance with that head that is true in $M$. Each fact of $M = P(E)$ has a finite height. Let $f \in M \setminus D$, and use induction on its height. If $f$ is stored, $f \in E$ and $f \notin E^-$, since $E^- \subseteq D$; so $f \in E'$. Otherwise take an instance with head $f$ that is true in $M$ and whose body facts have smaller height. If one of them were in $D$, Lemma 1 would put $f$ in $D$. So none of them is, and by induction all of them are in $M'$. $M'$ is closed under the rules, so $f \in M'$. So $M_6 \subseteq M'$.

Each fact of $R$ is the head of an instance that is true in $M_6 \subseteq M'$, so it is in $M'$. $E^+ \subseteq E' \subseteq M'$. So after line L8, $M \subseteq M'$. Each round of the loop of line L9 adds heads of instances that are true in the current $M \subseteq M'$, so $M$ stays a subset of $M'$. $\square$

**Lemma 3 (closure).** $M_f$ contains $E'$ and is closed under the rules.

*Proof.* $E \setminus E^- \subseteq M_6$, because $D$ holds no stored fact other than those of $E^-$: the heads of line L4 are IDB facts. And $E^+$ is added at line L8. So $E' \subseteq M_f$.

Take an instance that is true in $M_f$, with head $h$. Let $\Delta_0 = R \cup E^+$ be the set of line L8 and $\Delta_1, \Delta_2, \ldots$ the sets of line L11, the last of which is empty. Then $M_f = M_6 \cup \Delta_0 \cup \Delta_1 \cup \cdots$.

Case 1: all body facts are in $M_6$. Then they are in $M$, and the instance is true in $M$, so $h \in M$ because $M$ is closed. If $h \notin D$, then $h \in M_6 \subseteq M_f$. If $h \in D$, then the instance is true in $M_6$, which is the set that line L7 reads, and $h$ is an IDB fact of $D$; so $h \in R \subseteq M_f$.

Case 2: some body fact is in $\Delta_t$, and let $t$ be the largest such index. All body facts are in $M_6 \cup \Delta_0 \cup \cdots \cup \Delta_t$, which is the set $M$ at the start of the round of line L9 that reads $\Delta_t$. That round runs, because $\Delta_t \ne \emptyset$. Line L10 finds the instance, so $h \in N$, and after line L11 $h$ is in $M$. So $h \in M_f$. $\square$

**Proof of the claim.** Termination was shown above. By Lemma 3, $M_f$ contains $E'$ and is closed under the rules, so it contains the least such set, $M' \subseteq M_f$. By Lemma 2, $M_f \subseteq M'$. So $M_f = M'$, and line L12 also returns $E'$, as line L6 computes it. $\blacksquare$
