---
title: The HiCuts lookup returns the first matching rule, and the build ends
proves: [correctness]
status: full
---

We use the notation of the page. The rules $R_1, \ldots, R_n$ are boxes in the header space, in priority order. For a box $S$ and a list $L$ of rule indices in increasing order, let $G(S, L)$ be the list that the build keeps for $S$: go through $L$ in order, skip each rule that does not meet $S$, and also skip rule $i$ if an earlier kept rule contains $R_i \cap S$. Line numbers refer to HICUTS-LOOKUP on the page. Each node $v$ is reached through a *slot*: the root through the whole space, and a child through piece $k$ of the cut of its parent. We call the box of that piece the slot box of the visit.

## Lemma 1: a direct description of $G$

**Claim.** Rule $i$ of $L$ is in $G(S, L)$ if and only if $R_i$ meets $S$ and no earlier rule of $L$ contains $R_i \cap S$.

*Proof.* "If" is clear: no earlier rule of $L$ contains $R_i \cap S$, so no earlier kept rule does. For "only if", suppose $R_i$ meets $S$ and some earlier rule $j$ of $L$ contains $R_i \cap S$; take the first such $j$. If $j$ is kept, rule $i$ is skipped. If $j$ is not kept, then $R_j$ meets $S$ (it contains the nonempty set $R_i \cap S$), so by induction on the position in $L$ some earlier rule $j'$ of $L$ contains $R_j \cap S \supseteq R_i \cap S$. That contradicts the choice of $j$. $\square$

The early exit of the build, when a kept rule covers all of $S$, only skips rules that Lemma 1 skips too, because such a rule contains $R_i \cap S$ for every later $i$.

## Lemma 2: children can start from the list of the parent

**Claim.** If $S' \subseteq S$, then $G(S', G(S, \mathit{all})) = G(S', \mathit{all})$, where $\mathit{all} = 1, \ldots, n$.

*Proof.* Let $i \in G(S', \mathit{all})$. Then $R_i$ meets $S'$, so it meets $S$, and no earlier rule contains $R_i \cap S'$. Since $R_i \cap S \supseteq R_i \cap S'$, no earlier rule contains $R_i \cap S$ either, so $i \in G(S, \mathit{all})$ by Lemma 1. A sublist has fewer earlier rules, so $i \in G(S', G(S, \mathit{all}))$.

Let $i \in G(S', G(S, \mathit{all}))$ and suppose that an earlier rule of $\mathit{all}$ contains $R_i \cap S'$. Take the first such rule $j$. $R_j$ meets $S'$ and so meets $S$. If $j \notin G(S, \mathit{all})$, Lemma 1 gives an earlier $j'$ with $R_{j'} \supseteq R_j \cap S \supseteq R_i \cap S'$, against the choice of $j$. So $j \in G(S, \mathit{all})$, it comes before $i$, and it contains $R_i \cap S'$. By Lemma 1 for the list $G(S, \mathit{all})$, $i$ is not kept, which is a contradiction. $\square$

## Lemma 3: the kept list answers every packet of the box

**Claim.** Let $x$ be a packet in a box $S$. If some rule matches $x$, the first rule of $G(S, \mathit{all})$ that matches $x$ is the first rule of $R_1, \ldots, R_n$ that matches $x$. If no rule matches $x$, no rule of $G(S, \mathit{all})$ does.

*Proof.* The second part holds because $G(S, \mathit{all})$ is a sublist. For the first part, let $i$ be the first rule that matches $x$. $R_i$ meets $S$ at $x$. An earlier rule that contains $R_i \cap S$ would contain $x$ and match it, which is impossible, so $i \in G(S, \mathit{all})$ by Lemma 1. Every rule of the list before $i$ is an earlier rule, so it does not match $x$. $\square$

## The tree invariant

**Invariant (T).** For each visit of a node $v$ through a slot box $S$: if $v$ is a leaf, its list is $G(S, \mathit{all})$; if $v$ is internal, its box is $S$, its cut is along a dimension $j$ in which $S$ has a side of $2^a$ values with $a \ge 1$, the number of pieces $np$ is a power of two with $2 \le np \le 2^a$, and child $k$ is visited through the piece $k$ of side $2^a / np$.

The build keeps (T). The root gets $G(\text{space}, \mathit{all})$. An internal node with box $S$ and list $G(S, \mathit{all})$ gives piece $k$ the list $G(S_k, G(S, \mathit{all}))$, which is $G(S_k, \mathit{all})$ by Lemma 2. The cut only uses a side with more than one value, starts with $np = 2$ and doubles $np$ only while $2 np$ is at most the side, so $np$ divides the side, which by induction is a power of two. A shared leaf is reused only for a later piece whose list is equal to its own, which is the list (T) asks for.

## The lookup is correct

**Claim.** If (T) holds, HICUTS-LOOKUP$(x)$ returns the first rule that matches $x$, or "no match".

*Proof.* We show that each node is visited through a slot box that contains $x$. This holds at the root. At an internal node with box $S$, cut along $j$, side $[b, b + 2^a - 1]$ and $np$ pieces, piece $k$ is $[b + k s, b + (k+1) s - 1]$ with $s = 2^a / np$, so $x_j$ is in piece $\lfloor (x_j - b)/s \rfloor = \lfloor (x_j - b) \cdot np / 2^a \rfloor$, which is line L4. The other sides of the piece are those of $S$. So the child is visited through a slot box that contains $x$. The walk ends at a leaf, because by (T) each step at least halves one side of the box, which can happen at most $\sum_j W_j$ times. At the leaf, lines L6 to L8 return the first rule of $G(S, \mathit{all})$ that matches $x$, or "no match", and by Lemma 3 this is the right answer. $\square$

## The build ends, and the cost

Every child box is a proper part of its parent box, with one side divided by $np \ge 2$, and a box with all sides equal to 1 has no useful cut, so the depth of the tree is at most $\sum_j W_j$ and the build ends. The build may stop at a leaf with more than $\mathit{binth}$ rules when no cut is useful; correctness does not depend on the leaf size.

A lookup visits at most $\mathrm{depth} + 1$ nodes and tests at most the number of rules in its leaf, each test in $O(d)$ time. With the usual stop rule, a leaf has at most $\mathit{binth}$ rules, so a lookup costs $O(\mathrm{depth} + d \cdot \mathit{binth})$. The rule $\mathit{sm}(C) \le \mathit{spfac} \cdot |R(v)|$ bounds the growth at each node, but only level by level. A node with $m$ rules has children whose rule counts sum to at most $\mathit{spfac} \cdot m$ (or $2m$ for a cut into 2 pieces, which is always allowed), so the rules stored at depth $k$ number at most $c^k n$ with $c = \max(2, \mathit{spfac})$. For a tree of depth $D$ this gives $O(c^D n)$ stored rules, a bound that is exponential in the depth.
