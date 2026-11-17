---
title: MINIMIZE returns an equivalent conjunctive query with the fewest atoms
proves: [correctness, termination]
status: full
---

We use set semantics and the pseudocode of the page. $Q$ has the head $\bar x$ and the body $B$, a list of $k$ atoms. For a sublist $S$ of $B$, $Q_S$ is the query with the head $\bar x$ and the body $S$. A homomorphism from $P$ to $P'$ maps the variables of $P$ to the terms of $P'$, is the identity on constants, sends the head of $P$ to the head of $P'$, and sends each atom of $P$ to an atom of $P'$. We use the [Chandra-Merlin theorem](/chandra-merlin-theorem/): $P' \subseteq P$ if and only if there is a homomorphism from $P$ to $P'$. Homomorphisms compose, and a composition of homomorphisms is a homomorphism.

**Termination.** Line L2 runs $k$ times. HOM is a depth-first search of depth at most $n$, with at most $|P'|$ choices at each level, so it stops.

**Lemma 1 (HOM is correct).** HOM$(P, P')$ succeeds if and only if there is a homomorphism from $P$ to $P'$, and then it returns one.

*Proof.* Line L6 fixes the image of the head variables, as each homomorphism must, and fails if one variable must go to two different terms or a constant of the head of $P$ is not equal to the term at that place in the head of $P'$. By induction on $i$, SEARCH$(i, h)$ succeeds if and only if $h$ extends to a map that sends $\alpha_i, \ldots, \alpha_n$ to atoms of $P'$ and agrees with $h$: line L8 tries every atom $\beta$ that $\alpha_i$ can go to, and line L9 keeps exactly the extensions that send $\alpha_i$ to $\beta$. For $i = n + 1$ there is nothing left, and line L7 returns $h$. $\square$

**Lemma 2 (each step keeps equivalence and safety).** At each point, $Q_S \equiv Q$, and each head variable occurs in $S$.

*Proof.* At the start $S = B$. Suppose it holds for $S$, and line L4 sets $S \leftarrow S - \{\alpha\}$ after line L3 found a homomorphism $h$ from $Q_S$ to $Q_{S - \{\alpha\}}$. The identity is a homomorphism from $Q_{S - \{\alpha\}}$ to $Q_S$, since each atom of $S - \{\alpha\}$ is in $S$ and the heads are equal. So $Q_S \subseteq Q_{S - \{\alpha\}}$, and $h$ gives $Q_{S - \{\alpha\}} \subseteq Q_S$. For safety, let $x$ be a head variable. It occurs in some atom $\gamma \in S$, and $h(x) = x$ because $h$ sends the head to the head. So $x$ occurs in $h(\gamma)$, an atom of $S - \{\alpha\}$. $\square$

**Lemma 3 (one pass is enough).** Let $S$ be the final body. For no atom $\alpha \in S$ is there a homomorphism from $Q_S$ to $Q_{S - \{\alpha\}}$.

*Proof.* Each atom of $S$ was tried at line L3 and kept. Let $S_\alpha$ be the body at the time of that test, so $S \subseteq S_\alpha$ (as lists, with $S$ obtained from $S_\alpha$ by deletions) and $\alpha \in S$. Suppose $g$ is a homomorphism from $Q_S$ to $Q_{S - \{\alpha\}}$. By Lemma 2, $Q_S \equiv Q_{S_\alpha}$, so $Q_S \subseteq Q_{S_\alpha}$ and there is a homomorphism $f$ from $Q_{S_\alpha}$ to $Q_S$. Then $g \circ f$ is a homomorphism from $Q_{S_\alpha}$ to $Q_{S - \{\alpha\}}$. Each atom of $S - \{\alpha\}$ is an atom of $S_\alpha - \{\alpha\}$, so $g \circ f$ is also a homomorphism from $Q_{S_\alpha}$ to $Q_{S_\alpha - \{\alpha\}}$. By Lemma 1, the test at line L3 then succeeds for $\alpha$, and $\alpha$ is not kept, a contradiction. $\square$

**Lemma 4 (no deletable atom means fewest atoms).** Let $P$ be a conjunctive query with body $S$ such that for no $\alpha \in S$ there is a homomorphism from $P$ to $P_{S - \{\alpha\}}$. Then every conjunctive query $P' \equiv P$ has at least $|S|$ atoms.

*Proof.* Let $P' \equiv P$ have the body $S'$. By the Chandra-Merlin theorem there are homomorphisms $f$ from $P$ to $P'$ and $g$ from $P'$ to $P$. The map $e = g \circ f$ is a homomorphism from $P$ to $P$. Each atom of $S$ goes under $f$ to an atom of $S'$, and then under $g$ to one atom of $S$, so the set $e(S)$ of image atoms has at most $|S'|$ distinct atoms. If $|S'| < |S|$, some atom $\alpha$ of $S$ is not in $e(S)$, and $e$ is a homomorphism from $P$ to $P_{S - \{\alpha\}}$. This is not possible, so $|S'| \ge |S|$. If $S$ has two equal atoms, the identity sends $P$ to $P$ with one copy deleted, so the hypothesis already excludes equal atoms, and $|S|$ counts distinct atoms. $\square$

**Theorem.** MINIMIZE$(Q)$ returns a conjunctive query $Q_S \equiv Q$, whose body is a sublist of the body of $Q$ and whose head variables occur in the body, such that no conjunctive query equivalent to $Q$ has fewer atoms.

*Proof.* By Lemma 2, $Q_S \equiv Q$ and $Q_S$ is safe. By Lemma 3, $Q_S$ meets the hypothesis of Lemma 4. Each query equivalent to $Q$ is equivalent to $Q_S$, so by Lemma 4 it has at least $|S|$ atoms. $\blacksquare$

**Uniqueness up to renaming.** Let $Q_S$ and $Q_T$ be two results, for example from two orders of the body. Both are minimum, so $|S| = |T|$. Take homomorphisms $f$ from $Q_S$ to $Q_T$ and $g$ from $Q_T$ to $Q_S$. The map $g \circ f$ sends $Q_S$ to itself, and by the proof of Lemma 4 its image has all $|S|$ atoms, so it is a permutation of the atoms of $S$. Some power $e^r$ of $e = g \circ f$, with $r \ge 1$, fixes each atom of $S$. Each variable of $S$ is at some place of some atom, and $e^r$ fixes that atom, so $e^r$ fixes the variable too. So $e^r$ is the identity, and $f$ is injective on the variables of $S$. The image $f(S)$ is a set of atoms of $T$, and it has $|S| = |T|$ atoms because $e$ is a bijection on the atoms of $S$, so $f(S) = T$, and $f$ maps the variables of $S$ onto the variables of $T$. So $f$ is a bijection between the variables that maps the body of $Q_S$ onto the body of $Q_T$ and fixes the head and the constants. The two results differ only in the names of the existential variables. $\square$
