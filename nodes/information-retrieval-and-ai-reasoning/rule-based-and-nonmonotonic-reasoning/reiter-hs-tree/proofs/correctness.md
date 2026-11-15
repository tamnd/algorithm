---
title: The pruned HS-DAG returns exactly the minimal hitting sets
proves: [correctness]
status: full
---

Let $F$ be a finite collection of finite sets. A set $X$ *hits* $F$ if $X \cap S \neq \emptyset$ for every $S \in F$, and a hitting set is *minimal* if no proper subset of it hits $F$. In a diagnosis problem, $F$ is the collection of conflict sets and the minimal hitting sets are the minimal diagnoses (Reiter 1987, Theorem 4.4). This file proves that the HS-DAG of Greiner, Smith and Wilkerson (1989), in the form of lines L1 to L23 on the main page, returns every minimal hitting set and nothing else.

## Hypotheses on the label oracle

The algorithm asks a function $\mathrm{next}(h)$ for a label. We assume three things.

1. If $h$ hits $F$, then $\mathrm{next}(h)$ returns nothing.
2. If $h$ does not hit $F$, then $\mathrm{next}(h)$ returns a set $L$ with $L \cap h = \emptyset$ and $S \subseteq L$ for some $S \in F$.
3. Every label is a subset of one finite set $U$.

Let $\mathcal{L}$ be the family of the sets that contain some member of $F$. Every label that the oracle returns is in $\mathcal{L}$.

**Fact 0.** A set $X$ hits every member of $\mathcal{L}$ if and only if $X$ hits $F$.

*Proof.* $F \subseteq \mathcal{L}$. Conversely, if $X$ hits $F$ and $S \subseteq L$ with $S \in F$, then $X \cap L \supseteq X \cap S \neq \emptyset$. $\square$

An explicit collection with the rule "the first member of $F$ that is disjoint from $h$" satisfies the hypotheses, with $U = \bigcup F$. So does the diagnosis oracle that returns a conflict among the components outside $h$, with $U$ the set of components.

## The structure that the algorithm keeps

A node is identified by its set $H$, so two paths with the same edge labels end at the same node. A node with $|H| = j$ is at *level* $j$. The algorithm processes the levels in increasing order (lines L3 to L20). While it processes level $j$, it creates only nodes of level $j + 1$ (line L17). Each node has a status: not yet processed, *labeled*, *checked* or *closed*. A node gets a status at most once (line L5).

We claim that the following invariants hold before and after each step.

- **(I1)** Every label of a node, and every set in the list $\mathit{labels}$, is in $\mathcal{L}$.
- **(I2)** If a node $n$ has the label $L$, then $L \cap H(n) = \emptyset$, and for each $\sigma \in L$ the node $H(n) \cup \{\sigma\}$ exists and an edge marked $\sigma$ goes from $n$ to it.
- **(I3)** Every node that exists can be reached from the root.

*Proof.* At the start there is only the root, with no label. A label comes either from the list (line L7) or from the oracle (line L9). In both cases it is in $\mathcal{L}$ and is disjoint from $H(n)$: the list is searched for a disjoint set, and the oracle returns a disjoint set by hypothesis 2. Lines L14 to L19 then create the edges and the children, so (I1) and (I2) hold for $n$. The new children are reached through $n$, so (I3) holds.

The pruning step (lines L22 and L23) takes a new label $\Sigma$ and a node $n'$ with a label $S'$ such that $\Sigma \subsetneq S'$. It gives $n'$ the label $\Sigma$ and removes the edges for $\alpha \in S' \setminus \Sigma$. Then $\Sigma \in \mathcal{L}$, and $\Sigma \cap H(n') \subseteq S' \cap H(n') = \emptyset$. The edges for the elements of $\Sigma$ were there before, because $\Sigma \subseteq S'$, and they are kept. So (I1) and (I2) hold for $n'$. Next, the step deletes every node that the root no longer reaches. This gives (I3). It does not break (I2) for a node $p$ that stays: $p$ is reachable, so each child of $p$ is reachable through $p$ and stays. The list $\mathit{labels}$ only loses sets and gains $\Sigma$, so (I1) holds. $\square$

**Lemma 1 (every node is processed).** When the algorithm stops, every node that exists has a status.

*Proof.* A node of level $j + 1$ is created while level $j$ is processed, and it is put on the list of level $j + 1$ (line L18). That list is processed in the next round. A node on it is skipped only if it does not exist at that moment, or if it already has a status. A node that is created again after a deletion is put on the list again, and the creation happens during the round of level $j$, before the round of level $j + 1$. So a node that exists at the end was on the list of its level when that round ran, it existed at that moment, and it got a status. $\square$

**Lemma 2 (checked nodes are hitting sets).** If a node $n$ is checked, then $H(n)$ hits $F$.

*Proof.* A node is checked only when the oracle returns nothing (line L10). By hypothesis 2, the oracle returns a set whenever $h$ does not hit $F$. $\square$

## Completeness

**Lemma 3.** When the algorithm stops, every minimal hitting set $M$ of $F$ is $H(n)$ for some checked node $n$ that exists.

*Proof.* We walk down from the root along nodes $n_0, n_1, \ldots$ that exist at the end and have $H(n_i) \subseteq M$. The root exists and $H(n_0) = \emptyset \subseteq M$. Take the current node $n_i$. By Lemma 1 it has a status.

- If $n_i$ is checked, then $H(n_i)$ hits $F$ by Lemma 2, and $H(n_i) \subseteq M$. Since $M$ is minimal, $H(n_i) = M$, and we are done.
- If $n_i$ is closed, then at line L6 some checked node $m$ had $H(m) \subsetneq H(n_i) \subseteq M$. By Lemma 2, $H(m)$ hits $F$. This contradicts the minimality of $M$. So this case cannot happen.
- If $n_i$ has a label $L$, then $L \in \mathcal{L}$ by (I1), so $M \cap L \neq \emptyset$ by Fact 0. Take $\sigma \in M \cap L$. By (I2), $\sigma \notin H(n_i)$, and the node $n_{i+1} = H(n_i) \cup \{\sigma\}$ exists. Also $H(n_{i+1}) \subseteq M$.

Each step makes $H$ larger by one element, and $H$ stays inside $M$, which is finite. So the walk ends after at most $|M|$ steps, and it can only end at a checked node with $H = M$. $\square$

## Soundness

**Lemma 4.** When the algorithm stops, $H(n)$ is a minimal hitting set for every checked node $n$ that exists.

*Proof.* By Lemma 2, $H(n)$ hits $F$. Suppose that it is not minimal. Then it contains a minimal hitting set $M \subsetneq H(n)$. By Lemma 3, there is a checked node $m$ with $H(m) = M$ that exists at the end. Its level $|M|$ is smaller than the level $|H(n)|$ of $n$.

Nodes of level $|M|$ are created only in the round of level $|M| - 1$, and that round ends before the round of level $|H(n)|$ starts. So the node $m$ that exists at the end was created before $n$ was processed, and it was never deleted after that. It was processed, and became checked, in the round of level $|M|$, which also ended before $n$ was processed. So when $n$ was processed, $m$ existed, $m$ was checked, and $H(m) \subsetneq H(n)$. The test at line L6 then closes $n$, and $n$ is not checked. This is a contradiction. $\square$

## Termination

By hypothesis 3, each $H(n)$ is a subset of the finite set $U$, because its elements come from labels. So there are at most $|U| + 1$ levels and at most $2^{|U|}$ nodes at any time. Each round processes a finite list. A node can be deleted and created again only within the round before its level, so each list is finite. The algorithm stops.

## Theorem

Under hypotheses 1 to 3, the HS-DAG with the pruning step returns the set of all minimal hitting sets of $F$, each once.

*Proof.* Lemma 3 and Lemma 4 show that the returned sets $\{H(n) : n \text{ checked}\}$ are exactly the minimal hitting sets. Each set appears once, because a node is identified by its set $H$. $\blacksquare$

## Remarks

**Pruning is not needed for correctness.** The proof does not use the pruning step except to check that it keeps (I1) to (I3). The step makes the DAG smaller when the oracle returns labels that are not minimal. Without it, the algorithm is the basic HS-DAG, and the theorem holds for it too. That is the case that Reiter stated without a proof, and that Greiner, Smith and Wilkerson proved as their Lemma 4.2.

**Where Reiter's pruned tree breaks the invariants.** Reiter's tree has no merging of equal nodes. Its rule 3(ii) closes a node when an earlier node has the same set $H$. Its rule 3(iii) removes edges but keeps the old label. Each rule breaks one step of the proof.

- With $F = \{\{a,b\}, \{b,c\}, \{a,c\}, \{b,d\}, \{b\}\}$, the node for the path $b, a$ is closed because the node for $a, b$ exists. Later the label $\{b\}$ prunes the $a$ edge of the root, and the node for $a, b$ goes with it. The walk of Lemma 3 for $M = \{a, b\}$ then ends at a node that is closed for no valid reason, and $\{a, b\}$ is lost.
- With $F = \{\{a,b\}, \{a\}, \{b\}\}$, the root keeps the label $\{a,b\}$. The label $\{b\}$ removes its $a$ edge, and later the label $\{a\}$ removes its $b$ edge. The root then has no edges, but its label still claims $\{a, b\}$. So (I2) fails, and the walk of Lemma 3 cannot leave the root. The tree returns no hitting set, but $\{a, b\}$ is one.

In the HS-DAG the first case cannot happen, because the two paths end at one node, which stays while any of its parents stays. The second case cannot happen, because the root takes the label $\{b\}$ and the later label $\{a\}$ is not a proper subset of it.
