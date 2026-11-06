---
title: Earley's algorithm computes exactly the valid items
proves: [correctness]
status: full
---

We use the pseudocode of the page and its notation. The grammar is $G = (V, \Sigma, P, S)$ with no restriction on its productions, and the input is $w = a_1 \cdots a_n$. For $0 \le i \le j \le n$ write $w_{i,j} = a_{i+1} \cdots a_j$, so $w_{i,i} = \varepsilon$.

**Valid items.** An item $[A \to \alpha \bullet \beta, i]$ is *valid at $j$* when

- (V1) $\alpha \Rightarrow^* w_{i,j}$, and
- (V2) $S \Rightarrow^* a_1 \cdots a_i\, A\, \gamma$ for some $\gamma \in (V \cup \Sigma)^*$.

We show that the final sets satisfy $E[j] = \{\text{items valid at } j\}$ for every $j$. Then line L13 is correct: some $[S \to \alpha \bullet, 0] \in E[n]$ if and only if some $S \to \alpha$ has $\alpha \Rightarrow^* w$ (condition V2 holds with zero steps and $\gamma = \varepsilon$), that is, if and only if $S \Rightarrow^* w$.

**Lemma 0 (line L1).** The least fixed point of "$A$ is nullable if some $A \to X_1 \cdots X_k$ has all $X_i$ nullable" is $\{A : A \Rightarrow^* \varepsilon\}$.

*Proof.* Each symbol added has a derivation of $\varepsilon$, by induction on the order of addition: if every $X_i$ derives $\varepsilon$, so does $A \Rightarrow X_1 \cdots X_k$. Conversely, if $A \Rightarrow^m \varepsilon$, the first step uses some $A \to X_1 \cdots X_k$, every $X_i$ is a nonterminal, and by the splitting lemma each $X_i \Rightarrow^{m_i} \varepsilon$ with $m_i < m$. By induction on $m$ every $X_i$ is in the fixed point, and then so is $A$. $\square$

**Lemma 1 (soundness).** Every item that the algorithm inserts into $E[j]$ is valid at $j$.

*Proof.* By induction on the order of insertion; each line uses only items inserted before.

- Line L3 inserts $[S \to \bullet \alpha, 0]$ into $E[0]$: (V1) is $\varepsilon \Rightarrow^* \varepsilon$, and (V2) holds with zero steps.
- Line L9, from $[A \to \alpha \bullet X \beta', i] \in E[j]$, inserts $[X \to \bullet \eta, j]$. (V1) is trivial. For (V2), $S \Rightarrow^* a_1 \cdots a_i A \gamma \Rightarrow a_1 \cdots a_i\, \alpha X \beta' \gamma \Rightarrow^* a_1 \cdots a_j\, X \beta' \gamma$, using $\alpha \Rightarrow^* w_{i,j}$.
- Line L10 inserts $[A \to \alpha X \bullet \beta', i]$ with $X$ nullable. (V1) holds because $\alpha X \Rightarrow^* w_{i,j}\, \varepsilon$ by Lemma 0, and (V2) is the same as for the source item.
- Line L12 inserts $[A \to \alpha a_{j+1} \bullet \beta', i]$ into $E[j+1]$: $\alpha a_{j+1} \Rightarrow^* w_{i,j}\, a_{j+1} = w_{i,j+1}$, and (V2) is unchanged.
- Line L7 uses $[A \to \eta \bullet, i] \in E[j]$ and $[B \to \gamma \bullet A \delta, k] \in E[i]$, and inserts $[B \to \gamma A \bullet \delta, k]$ into $E[j]$. By (V1) of the two items, $\gamma A \Rightarrow^* w_{k,i}\, A \Rightarrow w_{k,i}\, \eta \Rightarrow^* w_{k,i}\, w_{i,j} = w_{k,j}$. (V2) is that of the second item. $\square$

**The deduction rules.** Let $C$ be the least set of pairs (item, position) that contains $([S \to \bullet \alpha, 0], 0)$ for each $S \to \alpha$ and is closed under:

- *predict:* from $([A \to \alpha \bullet X \beta, i], j)$ with $X \in V$, derive $([X \to \bullet \eta, j], j)$ for each $X \to \eta$;
- *scan:* from $([A \to \alpha \bullet a_{j+1} \beta, i], j)$ with $j < n$, derive $([A \to \alpha a_{j+1} \bullet \beta, i], j + 1)$;
- *complete:* from $([A \to \eta \bullet, i], j)$ and $([B \to \gamma \bullet A \delta, k], i)$, derive $([B \to \gamma A \bullet \delta, k], j)$.

**Lemma 2.** Every item valid at $j$ is in $C$ at $j$.

*Proof.* Let $I = [A \to \alpha \bullet \beta, i]$ be valid at $j$, with a derivation $S \Rightarrow^{m} a_1 \cdots a_i A \gamma$ for (V2) and $\alpha \Rightarrow^{s} w_{i,j}$ for (V1). Call $(m + 1 + s,\ s,\ |\alpha|)$ the *measure* of this pair of witnesses. We prove $I \in C$ by induction on the measure, ordered lexicographically.

*Case $\alpha = \varepsilon$.* Then $i = j$. If $m = 0$, then $A = S$, $i = 0$ and $I$ is an initial item of $C$. If $m \ge 1$, look at the partial derivation tree of $S \Rightarrow^m a_1 \cdots a_i A \gamma$: its frontier is $a_1 \cdots a_i A \gamma$, the leaf $A$ is not the root, and it has a parent $B$ expanded by some $B \to \mu A \nu$. All leaves left of $A$ are terminals, so the subtree of $B$ covers $a_{k+1} \cdots a_i\, A$ followed by the frontier of $\nu$, for some $k \le i$, and $\mu \Rightarrow^{s'} w_{k,i}$, where $s'$ is the number of expanded nodes below the children of $B$ in $\mu$. Removing every node below $B$ gives a partial tree with frontier $a_1 \cdots a_k B \gamma'$ and $m'$ expanded nodes, where $m' + 1 + s' \le m$, because $B$ and the nodes below $\mu$ were removed. So the item $I' = [B \to \mu \bullet A \nu, k]$ is valid at $i$ with measure $(m' + 1 + s', s', |\mu|)$, whose first component is at most $m < m + 1$. By induction $I' \in C$ at $i$, and *predict* gives $I \in C$ at $i = j$.

*Case $\alpha = \alpha' a$ with $a \in \Sigma$.* Then $j \ge 1$, $a = a_j$, and $\alpha' \Rightarrow^{s} w_{i,j-1}$ by the splitting lemma, with the same $s$. The item $[A \to \alpha' \bullet a_j \beta, i]$ is valid at $j - 1$ with measure $(m + 1 + s, s, |\alpha| - 1)$, which is smaller. By induction it is in $C$, and *scan* gives $I$.

*Case $\alpha = \alpha' X$ with $X \in V$.* By the splitting lemma, $\alpha' \Rightarrow^{s'} w_{i,k}$ and $X \Rightarrow^{s_X} w_{k,j}$ for some $k$ with $s' + s_X = s$ and $s_X \ge 1$, since $X$ is not a terminal. Let the first step of the derivation of $X$ be $X \to \eta$, so $\eta \Rightarrow^{s_X - 1} w_{k,j}$.

- The item $I_1 = [A \to \alpha' \bullet X \beta, i]$ is valid at $k$ with measure $(m + 1 + s', s', |\alpha| - 1)$. Its first component is smaller than $m + 1 + s$ because $s_X \ge 1$.
- The item $I_2 = [X \to \eta \bullet, k]$ is valid at $j$: (V1) holds by $\eta \Rightarrow^{s_X - 1} w_{k,j}$, and (V2) by $S \Rightarrow^m a_1 \cdots a_i A \gamma \Rightarrow a_1 \cdots a_i\, \alpha' X \beta \gamma \Rightarrow^{s'} a_1 \cdots a_k X \beta \gamma$, of $m + 1 + s'$ steps. Its measure is $(m + 1 + s' + 1 + s_X - 1,\ s_X - 1,\ |\eta|) = (m + 1 + s,\ s_X - 1,\ |\eta|)$: the first component is equal, and the second is $s_X - 1 < s$.

By induction $I_1 \in C$ at $k$ and $I_2 \in C$ at $j$, and *complete* gives $I$. $\square$

With Lemma 1 applied to the rules (each rule is one of the cases of Lemma 1, where *complete* is the case of line L7 for any $i \le j$), every member of $C$ is valid. So $C$ is exactly the set of valid items.

**Lemma 3.** When the loop of line L4 ends, the sets $E[0], \ldots, E[n]$ are closed under the three rules and contain the initial items.

*Proof.* Line L3 inserts the initial items. During iteration $j$ of line L4, items are added only to $E[j]$ (lines L7, L9, L10) and to $E[j + 1]$ (line L12). So $E[j]$ does not change after iteration $j$, and every item of $E[j]$ is visited by the loop of line L5, which runs until no unvisited item is left.

- *Predict.* When $[A \to \alpha \bullet X \beta, i] \in E[j]$ is visited, either $X$ is predicted now or was predicted before in $E[j]$; in both cases line L9 has inserted $[X \to \bullet \eta, j]$ for every $X \to \eta$.
- *Scan.* When $[A \to \alpha \bullet a_{j+1} \beta, i] \in E[j]$ is visited, line L12 inserts the scanned item into $E[j + 1]$.
- *Complete,* with $[A \to \eta \bullet, i] \in E[j]$ and $[B \to \gamma \bullet A \delta, k] \in E[i]$. If $i < j$: when the first item of $E[j]$ of the form $[A \to \eta' \bullet, i]$ was visited, line L7 read all items of $E[i]$ that wait for $A$, and $E[i]$ was already final, so $[B \to \gamma A \bullet \delta, k]$ was inserted. Skipping the later items with the same pair $(A, i)$ loses nothing, because line L7 inserts the same items for each of them. If $i = j$: the item $[A \to \eta \bullet, j]$ is valid by Lemma 1, so $\eta \Rightarrow^* w_{j,j} = \varepsilon$ and $A$ is nullable by Lemma 0. The item $[B \to \gamma \bullet A \delta, k] \in E[j]$ is visited at some point, and then line L10 inserts $[B \to \gamma A \bullet \delta, k]$. $\square$

**Theorem.** For every $j$, $E[j]$ is the set of items valid at $j$, and EARLEY returns true if and only if $w \in L(G)$.

*Proof.* Lemma 3 says the sets contain the initial items and are closed under the rules, so they contain the least such set $C$, which by Lemma 2 contains all valid items. Lemma 1 says every inserted item is valid. So $E[j]$ is exactly the set of valid items at $j$, and the remark after the definition of validity gives the answer of line L13. $\square$

**The parse tree.** Every item with the dot after position 0 records the reason for its first insertion: the item it came from, plus a scanned terminal, a completed item, or a nullable nonterminal. These reasons point to items inserted strictly earlier, so following them from $[S \to \alpha \bullet, 0] \in E[n]$ ends. Walking from a completed item $[A \to X_1 \cdots X_k \bullet, i] \in E[j]$ back to its dot-zero item gives, in reverse order, one record for each $X_t$: the terminal $a_p$ for a scan from $E[p-1]$ to $E[p]$, a completed item $[X_t \to \eta \bullet, p] \in E[q]$ for a completion, or a nullable $X_t$ with an empty span. The spans of the records are consecutive and cover $w_{i,j}$, by the positions in the pointers. Each completed child is again a valid completed item, and for a nullable child the fixed tree built in the order of Lemma 0 derives $\varepsilon$ with finitely many nodes. So the result is a finite tree whose root is $A$, whose internal nodes are productions, and whose leaves spell $w_{i,j}$. For the root item this is a parse tree of $w$. $\blacksquare$
