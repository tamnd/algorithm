---
title: Predictive recursive descent stops and parses exactly the strings of an LL(1) grammar
proves: [correctness, termination]
status: full
---

We use the pseudocode PARSE and PROC of the page and the notation of the [context-free grammar](/context-free-grammar/) page. The grammar is $G = (V, \Sigma, P, S)$, the input is $w = a_1 \cdots a_n$ and $a_{n+1} = \$$. We assume:

1. **LL(1).** Two different productions of one nonterminal have disjoint PREDICT sets, where $\text{PREDICT}(A \to \alpha) = \text{FIRST}(\alpha)$, together with $\text{FOLLOW}(A)$ when $\alpha \Rightarrow^* \varepsilon$.
2. **No left recursion.** There is no $A \in V$ with $A \Rightarrow^+ A\beta$.

A call PROC(A) *starts* at the value $p$ of pos when it is made and *returns at* $q$ if pos is $q$ when it returns. It *reads* $a_p \cdots a_{q-1}$.

## Soundness

**Lemma 1.** If a call PROC(A) starts at $p$ and returns at $q$, the tree it returns is a parse tree with root $A$ whose leaves, from left to right, are $a_p \cdots a_{q-1}$.

*Proof.* By induction on the order in which calls return. Line L5 fixes a production $A \to X_1 \cdots X_k$. The loop of lines L7 to L11 handles $X_1, \ldots, X_k$ in order, and pos never decreases. Let $p = p_0 \le p_1 \le \cdots \le p_k = q$ be the values of pos after each symbol. If $X_i$ is a terminal, line L9 checked $a_{p_{i-1}} = X_i$ and line L10 set $p_i = p_{i-1} + 1$, so the child is the leaf $a_{p_{i-1}}$. If $X_i$ is a nonterminal, the call PROC($X_i$) started at $p_{i-1}$ and returned at $p_i$ before the call of $A$ returned, so by induction its tree has root $X_i$ and leaves $a_{p_{i-1}} \cdots a_{p_i - 1}$. The node $A$ with these children uses the production $A \to X_1 \cdots X_k$, and its leaves are the concatenation $a_p \cdots a_{q-1}$. $\square$

**Corollary.** If PARSE returns a tree, it is a parse tree of $w$ with root $S$: the call PROC(S) starts at 1, and line L3 checked that it returned at $n + 1$. So PARSE never accepts a string outside $L(G)$.

## Completeness

**Lemma 2.** Let $T$ be a parse tree of $w$ with root $S$. Let $v$ be a node of $T$ with label $A$ and production $A \to \alpha$, whose leaves are $a_p \cdots a_{q-1}$ (empty if $q = p$). Then $a_p \in \text{PREDICT}(A \to \alpha)$.

*Proof.* If $q > p$, then $\alpha \Rightarrow^* a_p \cdots a_{q-1}$, so $a_p \in \text{FIRST}(\alpha)$. If $q = p$, then $\alpha \Rightarrow^* \varepsilon$. Cutting $T$ at $v$ shows $S \Rightarrow^* a_1 \cdots a_{p-1}\, A\, \delta$ where $\delta$ is the sequence of labels of the nodes to the right of the path from the root to $v$, and $\delta \Rightarrow^* a_p \cdots a_n$. Hence $S\$ \Rightarrow^* a_1 \cdots a_{p-1}\, A\, a_p \cdots a_n \$$, and the symbol after $A$ is $a_p$ (it is $\$$ when $p = n + 1$). So $a_p \in \text{FOLLOW}(A)$, and in both cases $a_p \in \text{PREDICT}(A \to \alpha)$. $\square$

**Lemma 3.** In the setting of Lemma 2, a call PROC(A) that starts at $p$ returns at $q$ and returns the subtree of $T$ at $v$.

*Proof.* By induction on the height of $v$. By Lemma 2 the token $a_p$ is in $\text{PREDICT}(A \to \alpha)$, and by the LL(1) condition it is in no other PREDICT set of $A$, so line L5 chooses $A \to \alpha$, with $\alpha = X_1 \cdots X_k$. Let $p = p_0 \le \cdots \le p_k = q$ be the boundaries of the children of $v$ in $T$. Suppose pos is $p_{i-1}$ when the loop reaches $X_i$. If $X_i$ is a terminal, the child of $v$ is the leaf $a_{p_{i-1}} = X_i$, so line L9 does not fail and line L10 moves pos to $p_i$. If $X_i$ is a nonterminal, its child is a lower node of $T$, so by induction PROC($X_i$) returns at $p_i$ with that child. After the loop pos is $q$, and line L12 returns the node $A$ with the children of $v$. $\square$

**Corollary.** If $w \in L(G)$ with parse tree $T$, then PROC(S) starts at 1 and returns at $n + 1$ with $T$ (Lemma 3 at the root), line L3 passes, and PARSE returns $T$. Since this holds for every parse tree $T$ of $w$ and PARSE is deterministic, $w$ has only one parse tree: an LL(1) grammar is unambiguous.

## Termination

Draw an edge $A \to B$ when $G$ has a production $A \to \beta B \gamma$ with $B \in V$ and $\beta \Rightarrow^* \varepsilon$.

**Lemma 4.** Without left recursion, the edge graph has no cycle.

*Proof.* An edge $A \to B$ from $A \to \beta B \gamma$ gives $A \Rightarrow \beta B \gamma \Rightarrow^* B\gamma$. Following the edges of a cycle $A \to \cdots \to A$ composes these derivations into $A \Rightarrow^+ A\delta$ for some $\delta$, which is left recursion. $\square$

**Lemma 5.** At any moment, the active calls (made and not yet returned) that start at the same position $p$ are at most $|V|$.

*Proof.* The active calls form a chain $C_1, C_2, \ldots, C_d$, each made by the previous one at line L11, and their start positions are nondecreasing. Let $C_j$ be PROC(A) and $C_{j+1}$ be PROC(B), both starting at $p$. Then $C_j$ chose $A \to X_1 \cdots X_k$ and made $C_{j+1}$ for $X_i = B$, after handling $X_1, \ldots, X_{i-1}$ without moving pos. None of these is a terminal, since a matched terminal moves pos. Each is a nonterminal whose call returned at the position where it started, so by Lemma 1 it derives $\varepsilon$. So $A \to B$ is an edge. The calls that start at $p$ are consecutive in the chain, so their nonterminals follow a path of edges, which by Lemma 4 has no repeated vertex. So there are at most $|V|$ of them. $\square$

**Theorem.** PARSE stops on every input, and the call stack never holds more than $(n + 1)|V|$ calls.

*Proof.* Start positions lie in $1, \ldots, n + 1$, so by Lemma 5 the chain of active calls has length at most $(n + 1)|V|$. The calls of a run form a tree, the call tree, in which each call has at most $r$ children, where $r$ is the length of the longest right side, and each path from the root is a chain of active calls at some moment, of length at most $(n + 1)|V|$. A tree with bounded branching and bounded depth is finite, and each call does finitely many steps besides its calls. So the run is finite, and it ends by returning a tree or reporting an error. $\square$

## Conclusion

By the termination theorem PARSE always stops. By the corollary of Lemma 3 it returns the parse tree of every $w \in L(G)$. By the corollary of Lemma 1 it never returns a tree for $w \notin L(G)$, so on such input it stops with an error, at line L3, L5 or L9.
