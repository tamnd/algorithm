---
title: GLR accepts exactly the words of the grammar and returns a parse tree
proves: [correctness]
status: full
---

**Notation.** $G = (V, \Sigma, P, S)$ is any context-free grammar, augmented with a new start symbol $S'$ and the production $S' \to S$, and $w = a_1 \cdots a_n$. For $0 \le i \le j \le n$, write $w_{i,j} = a_{i+1} \cdots a_j$. Items, CLOSURE, GOTO, the states $Q$ and $q_0$ are as on the page. For a string $\gamma = X_1 \cdots X_k$, $\delta(q, \gamma) = \mathrm{GOTO}(\cdots \mathrm{GOTO}(q, X_1) \cdots, X_k)$ when every step is defined, and $\delta(q, \varepsilon) = q$. A node $v$ of the GSS has a state $\mathrm{state}(v)$ and a level $\mathrm{level}(v)$. A path of $m$ edges from $u$ is a sequence $u = y_0, y_1, \ldots, y_m$ with an edge $y_{r-1} \to y_r$ for each $r$; nodes may repeat.

## Facts about the LR(0) automaton

**Fact 1 (dot positions).** CLOSURE adds only items with the dot at the start. So every item with the dot after the start in $\mathrm{GOTO}(q, X)$ has the form $A \to \beta X \bullet \gamma$, with $A \to \beta \bullet X \gamma \in q$. Such an item exists, since GOTO is defined only for a nonempty kernel. Hence every state $s = \mathrm{GOTO}(q, X)$ determines $X$, its **accessing symbol** $X(s)$, and $q_0$, which has no item with the dot after the start, is never a value of GOTO.

**Fact 2 (items move back to the start).** If $A \to \beta_1 \bullet \beta_2 \in \delta(t, \gamma)$ and $|\gamma| = |\beta_1|$, then $\gamma = \beta_1$ and $A \to \bullet \beta_1 \beta_2 \in t$. In particular, if $A \to \alpha \bullet \in \delta(t, \gamma)$ and $|\gamma| = |\alpha|$, then $\gamma = \alpha$ and $A \to \bullet \alpha \in t$.

*Proof.* By induction on $d = |\beta_1|$. For $d = 0$, $\gamma = \varepsilon$ and $\delta(t, \gamma) = t$. For $d > 0$, write $\gamma = \gamma' X$. The item has the dot after the start and is in $\mathrm{GOTO}(\delta(t, \gamma'), X)$, so by Fact 1, $\beta_1 = \beta_1' X$ and $A \to \beta_1' \bullet X \beta_2 \in \delta(t, \gamma')$, with $|\gamma'| = |\beta_1'|$. By induction, $\gamma' = \beta_1'$ and $A \to \bullet \beta_1' X \beta_2 \in t$. So $\gamma = \beta_1$. $\square$

**Fact 3 (valid items are present).** If $S' \Rightarrow^*_{rm} \delta A z \Rightarrow_{rm} \delta \beta_1 \beta_2 z$ is a rightmost derivation, then $\delta(q_0, \delta \beta_1)$ is defined and contains $A \to \beta_1 \bullet \beta_2$.

*Proof.* By the definition of GOTO, if $B \to \eta_1 \bullet X \eta_2 \in q$, then $\mathrm{GOTO}(q, X)$ is defined and contains $B \to \eta_1 X \bullet \eta_2$. Applying this $|\beta_1|$ times, it suffices to show $A \to \bullet \beta_1 \beta_2 \in \delta(q_0, \delta)$. We use induction on the length of the derivation $S' \Rightarrow^*_{rm} \delta A z$. If it has zero steps, then $A = S'$, $\delta = \varepsilon$, and $S' \to \bullet S \in q_0$. Otherwise, consider the step that introduced this occurrence of $A$: $S' \Rightarrow^*_{rm} \delta' B z' \Rightarrow_{rm} \delta' \eta_1 A \eta_2 z' \Rightarrow^*_{rm} \delta A z$. In a rightmost derivation, no symbol to the left of a nonterminal that is not yet rewritten is ever rewritten, so the steps after the introduction rewrite only $\eta_2$, and $\delta = \delta' \eta_1$. The derivation of $\delta' B z'$ is shorter, so by induction $B \to \bullet \eta_1 A \eta_2 \in \delta(q_0, \delta')$. Moving the dot over $\eta_1$ gives $B \to \eta_1 \bullet A \eta_2 \in \delta(q_0, \delta)$, and the closure then contains $A \to \bullet \beta_1 \beta_2$. $\square$

## Soundness

**Lemma 1.** For every edge $v \to x$ with $v = (s, j)$ and $x = (t, i)$: $i \le j$, $s = \mathrm{GOTO}(t, X(s))$, and the tree on the edge is a parse tree of $X(s)$ with yield $w_{i,j}$ (for a terminal, the leaf itself).

*Proof.* By induction on the order in which edges are made. A shift edge (line L12) goes from $(s, j + 1)$ to $u \in U_j$, with $s = \mathrm{GOTO}(\mathrm{state}(u), a_{j+1})$. By Fact 1, $X(s) = a_{j+1}$, and its leaf has yield $w_{j,j+1}$.

A reduction edge (line L10) comes from an entry $(u, A \to \alpha, e)$ with $u \in U_j$ and $A \to \alpha \bullet \in \mathrm{state}(u)$, and from a path $u = y_0, \ldots, y_m = x$ with $m = |\alpha|$, all of whose edges were made earlier. By induction, $\mathrm{state}(y_{r-1}) = \mathrm{GOTO}(\mathrm{state}(y_r), X_r)$ with $X_r = X(\mathrm{state}(y_{r-1}))$, and $\mathrm{level}(y_r) \le \mathrm{level}(y_{r-1})$. So $\mathrm{state}(u) = \delta(\mathrm{state}(x), \gamma)$ with $\gamma = X_m \cdots X_1$, and by Fact 2, $\gamma = \alpha$ and $A \to \bullet \alpha \in \mathrm{state}(x)$. Hence $s = \mathrm{GOTO}(\mathrm{state}(x), A)$ is defined, and $X(s) = A$ by Fact 1. The levels give $i = \mathrm{level}(x) \le \mathrm{level}(u) = j$. The trees on the edges $y_{m-1} \to y_m, \ldots, y_0 \to y_1$ are parse trees of $X_m, \ldots, X_1$ with yields $w_{\mathrm{level}(y_m), \mathrm{level}(y_{m-1})}, \ldots, w_{\mathrm{level}(y_1), \mathrm{level}(y_0)}$, which concatenate to $w_{i,j}$. With these children, bottom first, in the order of $\alpha$, the new tree is a parse tree of $A$ with yield $w_{i,j}$. $\square$

**Corollary.** If line L13 returns true, then the edge from $(\mathrm{GOTO}(q_0, S), n)$ to the root carries a parse tree of $X(\mathrm{GOTO}(q_0, S)) = S$ with yield $w_{0,n} = w$, so $S \Rightarrow^* w$.

## Termination

Each level has at most $|Q|$ nodes, and the levels are $0, \ldots, n$, so there are finitely many nodes and edges. In phase $j$, line L4 queues finitely many entries, line L8 queues entries only when it makes a node, and line L9 only when it makes an edge. So finitely many entries are queued. For each entry, line L7 enumerates finitely many paths, since they have $|\alpha|$ edges and each node has finitely many out-edges; the set of paths is fixed when the entry is removed. So every phase ends.

## Completeness

Edges are made only in two places. Line L10 in phase $j$ makes edges whose source is at level $j$; line L12 in phase $j$ makes edges whose source is at level $j + 1$. A path from a node of level $j$ never goes up a level (Lemma 1), so it uses only edges with a source at level at most $j$. Hence after the loop of lines L5 to L10 in phase $j$ ends, no edge on a path from a node of level $j$ is ever made again, and $U_j$ never changes again.

**Lemma 2 (saturation).** When the loop of lines L5 to L10 of phase $j$ ends, the following holds. For every $u \in U_j$, every $A \to \alpha \in R(\mathrm{state}(u))$, and every path $P$ of $m = |\alpha|$ edges from $u$ to a node $x$, the node $v = (\mathrm{GOTO}(\mathrm{state}(x), A), j)$ exists and has the edge $v \to x$.

*Proof.* It suffices to show that some entry $(u, A \to \alpha, e)$ is removed at line L6 after all edges of $P$ exist, with $e$ none or an edge of $P$. Then line L7 enumerates $P$, and lines L8 and L10 make $v$ and the edge if they are missing. (GOTO is defined here by the proof of Lemma 1, which shows $A \to \bullet \alpha \in \mathrm{state}(x)$.) The phase ends only when the queue is empty, so every queued entry is removed.

If $m = 0$, then $P$ has no edges and $x = u$. The node $u$ is in $U_j$ either at the start of the phase, and then line L4 queues $(u, A \to \alpha, \text{none})$, or it is made by line L8, which queues the same entry. Now let $m \ge 1$, and let $f$ be the edge of $P$ that was made last.

*Case (a): $f$ existed before the loop of phase $j$ began.* Then all edges of $P$ existed, so did their sources, and $u \in U_j$ at line L4, which queued $(u, A \to \alpha, \text{none})$.

*Case (b): $f$ was made in the loop, at line L10, in the same step in which line L8 made its source $v'$.* Let $f_r$ be the first occurrence of $f$ in $P$. If $r > 1$, the edge $f_{r-1}$ ends at $v'$ and is different from $f$, because $f$ ends at a node that existed before $v'$, while $f_{r-1}$ ends at $v'$. So $f_{r-1}$ was made before $f$, but after $v'$ was made, and nothing is made between line L8 and line L10 of one step. This is impossible, so $r = 1$ and $u = v'$. When line L8 made $u$, it queued $(u, A \to \alpha, \text{none})$, which is removed after this step, when all edges of $P$ exist.

*Case (c): $f$ was made in the loop, at line L10, from a source $v'$ that already existed.* Then the edge was new, and line L9 of the same step queued $(u', r, f)$ for every $u' \in U_j$ and every $r \in R(\mathrm{state}(u'))$ with a nonempty right side. The node $u$ was in $U_j$ at that time: it is $v'$ if $f$ is the first edge of $P$, and otherwise it is the source of the first edge of $P$, which was made before $f$. Since $m \ge 1$, the entry $(u, A \to \alpha, f)$ was queued, and it is removed after $f$ is made, when all edges of $P$ exist. The path $P$ uses $f$. $\square$

**Lemma 3 (the stacks of a rightmost derivation).** Let $S = \varphi_0 \Rightarrow_{rm} \varphi_1 \Rightarrow_{rm} \cdots \Rightarrow_{rm} \varphi_t = w$, with $t \ge 1$, where step $k$ rewrites $\varphi_k = \delta_k A_k z_k$ ($z_k \in \Sigma^*$) by $A_k \to \alpha_k$. Consider the sequence of configurations $(\gamma, i)$ of a shift-reduce parser that starts at $(\varepsilon, 0)$ and, for $k = t - 1$ down to $0$, shifts input symbols until $(\gamma, i) = (\delta_k \alpha_k, n - |z_k|)$, then reduces to $(\delta_k A_k, n - |z_k|)$. Then this sequence is well defined, ends at $(S, n)$, and $\gamma\, a_{i+1} \cdots a_n$ is a right sentential form for each configuration. Also, $\delta(q_0, \gamma)$ is defined for every $\gamma$ in it.

*Proof.* We show by downward induction on $k$ that before the shifts for step $k$, the configuration $(\gamma, i)$ has $\gamma a_{i+1} \cdots a_n = \varphi_{k+1}$ and $\gamma$ a prefix of $\delta_k \alpha_k$. Then shifting brings the stack to $\delta_k \alpha_k$, since $\varphi_{k+1} = \delta_k \alpha_k z_k$, and the reduction gives $\delta_k A_k$ with $\delta_k A_k z_k = \varphi_k$. For $k = t - 1$, the configuration is $(\varepsilon, 0)$ and $\varphi_t = w$. For the step from $k$ to $k - 1$: $\varphi_k = \delta_{k-1} \alpha_{k-1} z_{k-1}$, and $A_k$ is the rightmost nonterminal of $\varphi_k$. Since $z_{k-1}$ has no nonterminal, $A_k$ lies in $\delta_{k-1} \alpha_{k-1}$, so $\delta_k A_k$ is a prefix of $\delta_{k-1} \alpha_{k-1}$. At the end, $\varphi_0 = S$ gives $\delta_0 = \varepsilon$, $A_0 = S$, $z_0 = \varepsilon$, and the configuration $(S, n)$.

Each stack $\gamma$ of the sequence is $S$ or a prefix of some $\delta_k \alpha_k$. The derivation $S' \Rightarrow_{rm} S \Rightarrow^*_{rm} \delta_k A_k z_k \Rightarrow_{rm} \delta_k \alpha_k z_k$ and Fact 3 show that $\delta(q_0, \delta_k \alpha_k)$ is defined, so it is defined on all prefixes. Also $\mathrm{GOTO}(q_0, S)$ is defined, since $S' \to \bullet S \in q_0$. $\square$

For a configuration $(X_1 \cdots X_k, i)$ of this sequence, let $l_r$ be the input position of the configuration just after $X_r$ was pushed, so $l_1 \le \cdots \le l_k \le i$, and let $l_0 = 0$. We say the configuration is **in the GSS** if, for $v_r = (\delta(q_0, X_1 \cdots X_r), l_r)$, the nodes $v_0, \ldots, v_k$ and the edges $v_r \to v_{r-1}$ exist for $1 \le r \le k$, where $v_0$ is the root.

**Lemma 4.** Every configuration $(\gamma, i)$ of the sequence of Lemma 3 is in the GSS, with all its nodes and edges made by the end of the loop of lines L5 to L10 of phase $i$.

*Proof.* By induction along the sequence. The first configuration $(\varepsilon, 0)$ is the root, made at line L2. Note that every node of $\gamma$ at level $i$ and every edge with a source at level $i$ is made in phase $i - 1$ at line L12 or in phase $i$ at line L10, so it already exists at the end of that loop if it exists at all.

*Shift* from $(\gamma, i)$ to $(\gamma a_{i+1}, i + 1)$. By induction, the top node $u = (\delta(q_0, \gamma), i)$ is in $U_i$ when line L11 of phase $i$ runs. The state $s = \mathrm{GOTO}(\mathrm{state}(u), a_{i+1}) = \delta(q_0, \gamma a_{i+1})$ is defined by Lemma 3, so line L12 makes the node $(s, i + 1)$ and the edge to $u$. This happens before phase $i + 1$ starts.

*Reduction* from $(\delta \alpha, i)$ to $(\delta A, i)$ by $A \to \alpha$, with $m = |\alpha|$. By induction, the path $v_0, \ldots, v_{|\delta| + m}$ exists at the end of the loop of phase $i$, and its top node $u$ has level $i$. The last $m$ edges of it form a path of $m$ edges from $u$ to $x = v_{|\delta|} = (\delta(q_0, \delta), l_{|\delta|})$. The item $A \to \alpha \bullet$ is valid for $\delta \alpha$ (Lemma 3 with Fact 3), so it is in $\mathrm{state}(u) = \delta(q_0, \delta \alpha)$, and $A \to \alpha \in R(\mathrm{state}(u))$. By Lemma 2, the node $(\mathrm{GOTO}(\mathrm{state}(x), A), i) = (\delta(q_0, \delta A), i)$ exists, with an edge to $x$. The symbol $A$ was pushed at position $i$, so this is the node $v_{|\delta| + 1}$ of the new configuration, and the nodes below it are unchanged. $\square$

**Theorem.** GLR terminates, returns true if and only if $S \Rightarrow^* w$, and when it returns true, the tree it returns is a parse tree of $w$ from $S$.

*Proof.* Termination is shown above. If GLR returns true, then $S \Rightarrow^* w$ and the tree is a parse tree, by the Corollary of Lemma 1. Conversely, if $S \Rightarrow^* w$, then since $w$ has no nonterminal, there is a rightmost derivation with $t \ge 1$ steps. By Lemma 3 its last configuration is $(S, n)$, and by Lemma 4 the node $(\delta(q_0, S), n) = (\mathrm{GOTO}(q_0, S), n)$ exists with an edge to the root. Line L13 runs after phase $n$, so it finds them and returns true. $\blacksquare$
