---
title: ATMS label propagation gives sound, consistent, minimal and complete labels
proves: [correctness]
status: full
---

Let $A$ be the set of assumptions and $J$ the set of justifications $x \leftarrow a_1, \ldots, a_k$, Horn clauses over nodes, where the node $\bot$ stands for a contradiction. For an environment $E \subseteq A$, let $\mathrm{Cl}(E)$ be the set of nodes that follow from $E$ and $J$ by [forward chaining](/forward-chaining/); an assumption $a$ is in $\mathrm{Cl}(E)$ when $a \in E$. $E$ is *inconsistent* when $\bot \in \mathrm{Cl}(E)$. Since $\mathrm{Cl}$ is monotone, every superset of an inconsistent environment is inconsistent. A label $L(x)$ is

- *sound* when $x \in \mathrm{Cl}(E)$ for each $E \in L(x)$;
- *consistent* when each $E \in L(x)$ is consistent;
- *minimal* when no element of $L(x)$ is a proper subset of another;
- *complete* when each consistent $E$ with $x \in \mathrm{Cl}(E)$ has a subset in $L(x)$.

The four properties fix the label: it is the set of minimal consistent environments that derive $x$. The goal is that, when the queue is empty, every label has the four properties and the nogood list is the set of minimal inconsistent environments.

We use the procedures of the page. Adding the assumption $a$ queues $(a, \{\{a\}\})$; adding a justification $j$ queues its consequent with COMBINE$(j)$ over the full labels. Line L8 queues a consequent with the products that use the new environments $N$ of one antecedent.

## Lemma 1 (soundness and consistency of the nogoods)

Every nogood is inconsistent, and every environment in a label derives its node.

*Proof.* By induction on the steps. An environment enters a queue as $\{a\}$ for an assumption $a$, or as a union $e_1 \cup \cdots \cup e_k$ of label environments of the antecedents of a justification $x \leftarrow a_1, \ldots, a_k$. In the first case $a \in \mathrm{Cl}(\{a\})$. In the second case $a_i \in \mathrm{Cl}(e_i) \subseteq \mathrm{Cl}(e_1 \cup \cdots \cup e_k)$ for all $i$ by the induction hypothesis and monotonicity, so $x$ is in the closure of the union. An environment that line L5 turns into a nogood derives $\bot$ in the same way. Lines L6 and L13 only remove environments or add queued ones. $\square$

## Lemma 2 (consistency and minimality)

At every moment, each label is minimal and contains no superset of a nogood, and the nogood list holds no two environments one of which contains the other.

*Proof.* Line L2 drops the queued environments that contain a nogood, and line L13 removes from every label the environments that contain a new nogood. Line L3 keeps only the minimal new environments that no old one is a subset of, and line L6 removes the old ones that a new one is a subset of. Line L12 adds a nogood only when no old nogood is a subset of it (the procedure checks this first) and removes the old ones that contain it. $\square$

So, by Lemma 1, a nogood is inconsistent, and with Lemma 2, an environment in a label contains no nogood. After Lemma 4 below, this means it is consistent.

## Lemma 3 (quiescence)

When the queue is empty, for every justification $x \leftarrow a_1, \ldots, a_k$ and every choice of $e_i \in L(a_i)$, the union $u = e_1 \cup \cdots \cup e_k$ contains a nogood, or $x \ne \bot$ and $u$ has a subset in $L(x)$. For $k = 0$ this says that $\emptyset$ is in $L(x)$, or is a nogood. Also, for each assumption $a$, the set $\{a\}$ contains a nogood or has a subset in $L(a)$.

*Proof.* An environment that has once been in a label and is in it now has been in it all the time in between, since removed environments contain a nogood (line L13) or a smaller label environment (line L6), and line L3 never adds an environment with a subset in the label. Fix the choice $e_1, \ldots, e_k$ and let $e_i$ be the one that entered its label last; if $k = 0$, or no $e_i$ was added after the justification, take the moment when the justification was added. At that moment line L8 (or the queueing at JUSTIFY) put on the queue a set of environments that contains $u$ or a subset $u'$ of it, since COMBINE keeps the minimal unions of all products that use $e_i$ at its position and the current labels at the others, which already hold the other $e_l$. When this item is popped, $u'$ is either dropped at line L2, because it contains a nogood, or dropped at line L3, because it has a subset in $L(x)$, or added to $L(x)$, or turned into a nogood when $x = \bot$. In each case, from then on $u'$ contains a nogood or has a subset in $L(x)$, because nogoods are only replaced by subsets and label environments only by subsets or by removal through a nogood that they contain. Since $u' \subseteq u$, the same holds for $u$. The argument for $\{a\}$ is the same, with the item queued when $a$ became an assumption. $\square$

## Lemma 4 (completeness)

When the queue is empty, for every environment $E$ and every node $x \in \mathrm{Cl}(E)$, either $E$ contains a nogood, or $x \ne \bot$ and $E$ has a subset in $L(x)$.

*Proof.* By induction on the step at which forward chaining from $E$ derives $x$. If $x$ is an assumption in $E$, Lemma 3 for $\{a\}$ gives the claim. Otherwise $x$ is derived by a justification $x \leftarrow a_1, \ldots, a_k$ with each $a_i \in \mathrm{Cl}(E)$ derived earlier. By the induction hypothesis, $E$ contains a nogood, and we are done, or each $a_i$ has some $e_i \in L(a_i)$ with $e_i \subseteq E$. Then $u = e_1 \cup \cdots \cup e_k \subseteq E$, and Lemma 3 gives a nogood inside $u$, or a subset of $u$ in $L(x)$, both inside $E$. $\square$

## Theorem

When the queue is empty, every label $L(x)$ is sound, consistent, minimal and complete, and the nogoods are exactly the minimal inconsistent environments.

*Proof.* Soundness is Lemma 1 and minimality is Lemma 2. A consistent $E$ contains no nogood, since nogoods are inconsistent (Lemma 1); so by Lemma 4 every consistent $E$ with $x \in \mathrm{Cl}(E)$ has a subset in $L(x)$, which is completeness. An inconsistent $E$ has $\bot \in \mathrm{Cl}(E)$, so by Lemma 4 it contains a nogood. So a label environment, which contains no nogood (Lemma 2), is consistent. Finally, every inconsistent environment contains a nogood, every nogood is inconsistent, and no nogood contains another; so a nogood has no inconsistent proper subset, and every minimal inconsistent environment, which contains a nogood, equals it. $\blacksquare$

## Labels can be exponential

Take $2n$ assumptions $A_1, B_1, \ldots, A_n, B_n$ and the justifications $x_i \leftarrow A_i$, $x_i \leftarrow B_i$ for each $i$, and $g \leftarrow x_1, \ldots, x_n$. Then $L(x_i) = \{\{A_i\}, \{B_i\}\}$, and an environment derives $g$ exactly when it holds $A_i$ or $B_i$ for every $i$. There are no nogoods, so the minimal such environments are the $2^n$ sets that pick one of $A_i, B_i$ for each $i$, and none of them contains another. So $|L(g)| = 2^n$ for an input of size $O(n)$, and any procedure that writes the labels needs exponential time on this family.
