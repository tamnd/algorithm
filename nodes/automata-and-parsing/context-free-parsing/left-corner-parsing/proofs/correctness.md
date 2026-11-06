---
title: The left-corner chart recognizer accepts exactly the words of the grammar
proves: [correctness]
status: full
---

**Notation.** $G = (V, \Sigma, P, S)$ is any context-free grammar and $w = a_1 \cdots a_n$. For $0 \le i \le k \le n$, $w_{i,k} = a_{i+1} \cdots a_k$. $L(C)$ is the set of $B \in V$ such that $B = C$ or there are productions $C \to B_1 \gamma_1, B_1 \to B_2 \gamma_2, \ldots, B_{m-1} \to B \gamma_m$ in $P$, $m \ge 1$, with $B_m = B$. Note that if $B \in L(C)$ and $B \to D \gamma \in P$ with $D \in V$, then $D \in L(C)$. A pair $(C, i)$ is a **goal** once START$(C, i)$ has been called. "Add" puts an item in a set only if it is not there.

**Lemma 1 (soundness).** Every item $[C, i, B \to \alpha \bullet \beta] \in E[k]$ satisfies: $(C, i)$ is a goal, $i \le k$, $B \in L(C)$, $\alpha \Rightarrow^* w_{i,k}$, and $\alpha \ne \varepsilon$ unless $\beta = \varepsilon$. Every $(C, i, k) \in \mathrm{DONE}$ satisfies: $(C, i)$ is a goal and $C \Rightarrow^* w_{i,k}$.

*Proof.* By induction on the order of the additions. Line L14 adds $[C, k, D \to a_{k+1} \bullet \gamma]$ to $E[k + 1]$ with $D \in L(C)$, and $a_{k+1} \Rightarrow^* w_{k,k+1}$. Line L15 adds $[C, k, D \to \bullet]$ with $D \in L(C)$ and $\beta = \varepsilon$. Line L6 adds $(C, i, k)$ for a complete item $[C, i, C \to \alpha \bullet]$, and then $C \Rightarrow \alpha \Rightarrow^* w_{i,k}$. It also moves an item $[C', i', D \to \gamma \bullet C \delta] \in E[i]$ that waits on $(C, i)$ to $E[k]$; by induction $\gamma \Rightarrow^* w_{i',i}$, so $\gamma C \Rightarrow^* w_{i',k}$. Line L7 adds $[C, i, D \to B \bullet \gamma]$ for a complete item $[C, i, B \to \alpha \bullet] \in E[k]$, with $D \in L(C)$; by induction $B \Rightarrow \alpha \Rightarrow^* w_{i,k}$. Line L11 is the same as the move of line L6, for an entry $(Y, k, k') \in \mathrm{DONE}$, with $Y \Rightarrow^* w_{k,k'}$ by induction. Line L12 extends $\alpha$ by $a_{k+1}$. In each case the new item keeps its goal, which is a goal by induction, and has a nonempty $\alpha$ unless it comes from line L15. $\square$

**Lemma 2 (processing order).** Every entry $(Y, i, k')$ of DONE is added while $E[k']$ is processed. When line L11 runs for an item of $E[k]$, every entry $(Y, k, k')$ in DONE has $k' = k$. Every item ever added to $E[k]$ is processed by the loop of line L4 for this $k$.

*Proof.* Line L6 adds $(C, i, k)$ while it processes a complete item of $E[k]$. So when $E[k]$ is processed, the entries of DONE have ends at most $k$, and an entry $(Y, k, k')$ has $k' \ge k$ by Lemma 1, so $k' = k$. Hence items are added to $E[k]$ only by START$(\cdot, k)$ (line L15), by START$(\cdot, k - 1)$ (line L14), by lines L6, L7 and L11 while $E[k]$ is processed, or by line L12 while $E[k - 1]$ is processed. START$(Y, k)$ is called at line L2 with $k = 0$ before the loop, or at line L9 while $E[k]$ is processed. So no item is added to $E[k]$ after its loop ends, and the loop visits every item in the order of insertion, including the items added during the loop. $\square$

**Lemma 3 (closure).** When the loop of line L3 ends, the chart is closed under the rules of lines L6, L7, L9 to L12, L14 and L15: for every item, the items and goals that the line for it would add are present, and for every goal $(C, i)$, the items of START$(C, i)$ are present.

*Proof.* Every item is processed (Lemma 2), and START runs for every goal. Processing an item adds what lines L7, L9, L10, L11 and L12 require for it. For a complete item $[C, i, B \to \alpha \bullet] \in E[k]$, the first such item for the key $(C, i, B, k)$ is processed fully, and the effects of lines L6 and L7 depend only on this key, so they hold for the other items with the same key. It remains to show the rule of line L6 for an item $J$ that waits on $(C, i)$ and an entry $(C, i, k) \in \mathrm{DONE}$: the moved item must be in $E[k]$. If $J$ was recorded as waiting (line L10) before $(C, i, k)$ was added, then line L6 moved it when it added the entry. Otherwise the entry was in DONE when line L11 processed $J$, and line L11 moved it. $\square$

**Lemma 4 (completeness).** Let $(C, i)$ be a goal, and suppose $C \Rightarrow^* w_{i,k}$. Then $(C, i, k) \in \mathrm{DONE}$ when the loop ends.

*Proof.* By induction on the height of a parse tree $T$ of $C$ with yield $w_{i,k}$. Let $C = B_0, B_1, \ldots, B_m$ be the nodes on the left edge of $T$: $B_{r+1}$ is the first child of $B_r$, and $B_m$ is the last internal node on this edge. Each $B_r$ is in $L(C)$, since each production $B_r \to B_{r+1} \cdots$ starts with $B_{r+1}$. Let $B_r \to X_{r,1} \cdots X_{r,q_r}$ be the production at $B_r$, where $X_{r,1} = B_{r+1}$ for $r < m$, and let $i = l_{r,0} \le l_{r,1} \le \cdots \le l_{r,q_r}$ be the boundaries of the yields of its children. All nodes on the left edge start at $i$, and $B_r$ ends at $l_{r, q_r}$.

We show by downward induction on $r$, from $r = m$ to $r = 0$, that the complete item $[C, i, B_r \to X_{r,1} \cdots X_{r,q_r} \bullet]$ is in $E[l_{r,q_r}]$.

*The first item at $B_r$.* If $r = m$ and $q_m = 0$, START$(C, i)$ adds $[C, i, B_m \to \bullet]$ to $E[i]$ (line L15). If $r = m$ and $q_m > 0$, then $X_{m,1}$ is a terminal, equal to $a_{i+1}$, so $i < n$ and START$(C, i)$ adds $[C, i, B_m \to a_{i+1} \bullet X_{m,2} \cdots]$ to $E[i + 1]$ (line L14). If $r < m$, the complete item for $B_{r+1}$ is in $E[l_{r,1}]$ by the inner induction, and line L7 adds $[C, i, B_r \to B_{r+1} \bullet X_{r,2} \cdots]$ to $E[l_{r,1}]$, because $B_r \in L(C)$ (Lemma 3).

*The other children.* Suppose $[C, i, B_r \to X_{r,1} \cdots X_{r,t-1} \bullet X_{r,t} \cdots] \in E[l_{r,t-1}]$ for some $2 \le t \le q_r$. If $X_{r,t}$ is a terminal, it is $a_{l_{r,t-1}+1}$, and line L12 moves the dot into $E[l_{r,t}]$. If $X_{r,t} = Y$ is a nonterminal, then by Lemma 3 the pair $(Y, l_{r,t-1})$ is a goal (line L9) and the item waits on it (line L10). The subtree of $Y$ is a proper subtree of $T$, of smaller height, with yield $w_{l_{r,t-1}, l_{r,t}}$, so by the outer induction $(Y, l_{r,t-1}, l_{r,t}) \in \mathrm{DONE}$. By Lemma 3 (the rule of line L6), the item with the dot after $Y$ is in $E[l_{r,t}]$. After $t = q_r$, the complete item for $B_r$ is in $E[l_{r,q_r}]$.

For $r = 0$, the complete item $[C, i, C \to \cdots \bullet] \in E[k]$ has $B = C$, and the rule of line L6 puts $(C, i, k)$ in DONE. $\square$

**Termination.** There are at most $|V| (n + 1)$ goals, and for each set $E[k]$ at most $|V| (k + 1)$ goals times $|G|$ dotted productions, so finitely many items. Each item is processed once, and each step of the processing does a finite amount of work, so the loop ends.

**Theorem.** LEFT-CORNER$(G, w)$ terminates and returns true if and only if $S \Rightarrow^* w$.

*Proof.* Termination is shown above. Line L2 makes $(S, 0)$ a goal. If line L13 returns true, then $(S, 0, n) \in \mathrm{DONE}$ and $S \Rightarrow^* w_{0,n} = w$ by Lemma 1. If $S \Rightarrow^* w$, then $(S, 0, n) \in \mathrm{DONE}$ by Lemma 4, and line L13 returns true. $\blacksquare$
