---
title: Incremental relabelling of a JTMS gives the well-founded labelling
proves: [correctness]
status: full
---

A network $N$ is a finite set of justifications $(x, I, O)$, read as the rules $x \leftarrow I, \mathit{not}\ O$ of a ground normal logic program. A *partial labelling* is a pair $(T, F)$ of disjoint sets of nodes, the IN nodes and the OUT nodes; the other nodes are undecided. We order pairs by $(T, F) \le (T', F')$ when $T \subseteq T'$ and $F \subseteq F'$.

## Definitions and known facts

- $T_N(T, F)$ is the set of nodes with a justification whose in-list is inside $T$ and whose out-list is inside $F$.
- A set $U$ is *unfounded* with respect to $(T, F)$ when each justification $(x, I, O)$ with $x \in U$ has an in-node in $F \cup U$ or an out-node in $T$. A union of unfounded sets is unfounded, so there is a *greatest unfounded set* $U_N(T, F)$.
- $W_N(T, F) = (T_N(T, F), U_N(T, F))$. Both parts grow when $(T, F)$ grows, so $W_N$ is monotone, and the *well-founded model* is its least fixed point (Van Gelder, Ross and Schlipf 1991; see [well-founded semantics](/well-founded-semantics/)). We write it $(T^*, F^*)$ for the network after the change.

**Lemma 1 (supported nodes).** For a partial labelling $(T, F)$, let $\mathrm{Pos}$ be the least set of nodes such that $y \in \mathrm{Pos}$ whenever $y$ has a justification with no in-node in $F$, every in-node in $\mathrm{Pos}$, and no out-node in $T$. Then $U_N(T, F)$ is the complement of $\mathrm{Pos}$.

*Proof.* A node $y \notin \mathrm{Pos}$ fails the rule for each of its justifications, so each has an in-node in $F$, an in-node outside $\mathrm{Pos}$, or an out-node in $T$. So the complement of $\mathrm{Pos}$ is unfounded. Conversely, let $U$ be unfounded and build $\mathrm{Pos}$ in stages. A node enters $\mathrm{Pos}$ by a justification whose in-nodes are in $\mathrm{Pos}$ already, hence not in $U$ by induction, and not in $F$, and whose out-nodes are not in $T$. This justification breaks the unfounded condition, so the node is not in $U$. $\square$

**Lemma 2 (splitting).** Let $D$ be a set of nodes such that every justification of a node of $D$ mentions only nodes of $D$, and let $N_D$ be the justifications of the nodes of $D$. Then the well-founded model of $N$, restricted to $D$, is the well-founded model of $N_D$.

*Proof.* For $x \in D$, membership of $x$ in $T_N(T, F)$ depends only on $T \cap D$ and $F \cap D$. A set $U \subseteq D$ is unfounded for $N$ exactly when it is unfounded for $N_D$, and $U_N(T, F) \cap D$ is unfounded, since the justifications of its nodes mention only nodes of $D$. So $W_N(T, F)$ restricted to $D$ is $W_{N_D}$ of the restriction, and by induction the iterates of $W_N$ and $W_{N_D}$ from $(\emptyset, \emptyset)$ agree on $D$. This is the [splitting set theorem](/splitting-set-theorem/) for the well-founded semantics. $\square$

## The procedure

We use RELABEL$(x)$ of the page, called after a justification of $x$ was added or removed, when the labels were the well-founded model of the network before the change. Line L1 computes the set $S$ of nodes that depend on $x$. Let $D$ be the set of the other nodes.

**Lemma 3.** No justification of a node of $D$ mentions a node of $S$, and the justifications of the nodes of $D$ did not change. So after line L2, every node of $D$ carries its label in $(T^*, F^*)$, with UNDEC for undecided.

*Proof.* If a justification of $d$ mentions $s \in S$, then $d$ depends on $s$ and line L1 puts $d$ in $S$. The changed justification belongs to $x \in S$. By Lemma 2, applied before and after the change, the labels of $D$ are the well-founded labels of $N_D$, which is the same network before and after. $\square$

**Lemma 4 (soundness).** At every moment, the IN nodes are in $T^*$ and the OUT nodes are in $F^*$.

*Proof.* By Lemma 3 this holds after line L2, and the labels of $D$ never change afterwards. We show that each new label keeps it.

Line L5 labels $y$ IN by a justification whose in-nodes are IN, so in $T^*$, and whose out-nodes are OUT, so in $F^*$. Then $y \in T_N(T^*, F^*) = T^*$.

Line L7 labels OUT the set $U$ of unlabeled nodes of $S$ that are not in $P$. Take $y \in U$ and a justification $(y, I, O)$. Since $y$ is not OUT and $y \notin P$, this justification breaks the rule of line L6: either an out-node is IN, or an in-node $b$ is not IN, not UNDEC and not in $P$. In the second case $b$ is OUT, or $b$ is unlabeled, and then $b \in S$ (all nodes of $D$ are labelled) and $b \in U$. So $U$ is unfounded with respect to the current labels, and since unfoundedness is kept when the labels grow, $U$ is unfounded with respect to $(T^*, F^*)$. So $U \subseteq U_N(T^*, F^*) = F^*$. $\square$

**Lemma 5 (termination).** Each round of lines L3 to L8, except the last, labels a node at line L7. Each pass of line L4 labels a node or ends the inner loop. Labels in $S$ only change from none to a label. So the procedure stops.

## Theorem

When RELABEL$(x)$ stops, IN, OUT and UNDEC are exactly the true, false and undefined nodes of the well-founded model of the new network.

*Proof.* Let $(T', F')$ be the final IN and OUT sets. By Lemma 4, $(T', F') \le (T^*, F^*)$. We show that $(T', F')$ is a fixed point of $W_N$. Since $(T^*, F^*)$ is the least fixed point, then $(T^*, F^*) \le (T', F')$, and the two are equal.

*$T_N(T', F') = T'$.* On $D$ this holds by Lemma 3 and Lemma 2, because $(T^*, F^*)$ is a fixed point and the labels on $D$ agree with it. A node of $S$ labelled IN got its label by a justification that was valid at that time, and labels never change once set, so the justification is still valid. A node of $S$ labelled UNDEC was unlabeled in the last pass of line L4, so it has no valid justification. A node $y$ of $S$ labelled OUT is in $F^*$; if a justification of $y$ were valid in $(T', F') \le (T^*, F^*)$, it would be valid in $(T^*, F^*)$ and put $y$ in $T^*$, which is disjoint from $F^*$.

*$U_N(T', F') = F'$.* On $D$ this holds as before. Each node of $S$ labelled OUT at line L7 belongs to a set that was unfounded for the labels of that time, and so for $(T', F')$; so $F' \subseteq U_N(T', F')$. For the other direction we use Lemma 1. In the last round, line L7 labelled nothing, so every node of $S$ that ends UNDEC is in the set $P$ of that round, and the IN labels did not change after it. The nodes of $T'$, the UNDEC nodes of $D$ and the nodes of $P$ are all in $\mathrm{Pos}(T', F')$: the nodes of $D$ because $\mathrm{Pos}$ on $D$ is the complement of $F^* \cap D$ by Lemma 2; an IN node of $S$ by induction on the order of labelling, through the justification that made it IN; a node of $P$ by induction on the stages of $P$, through the justification that put it in $P$, whose in-nodes are IN, UNDEC or in $P$, so not OUT, and whose out-nodes are not IN. So $U_N(T', F')$, the complement of $\mathrm{Pos}$, holds only OUT nodes. $\blacksquare$

## Corollaries

- If the network has no cycle through an out-list (it is *stratified*), its well-founded model is two-valued, so no node ends UNDEC, and the labelling is the unique stable model.
- If the final labelling has no UNDEC node, the network has exactly one stable model, and it is the set of IN nodes. This is the general fact that a two-valued well-founded model is the unique stable model.
- The labels do not depend on the order of the changes, only on the final network, because each call ends at the well-founded model.
