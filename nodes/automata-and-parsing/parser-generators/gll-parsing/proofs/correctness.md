---
title: Correctness of the GLL recognizer
proves: [correctness]
status: full
---

**Setting.** $G = (V, \Sigma, P, S)$ is any context-free grammar and $w = a_1 \cdots a_n$ the input; $w[j:i] = a_{j+1} \cdots a_i$ for $j \le i$. A GSS node other than the root $u_0$ is a pair $v = (B \to \gamma X \cdot \delta, k)$ with $X \in V$; we say that $v$ *calls* $X$ at $k$. The root calls $S$ at 0. A *configuration* $(A \to \alpha \cdot \beta, u, i)$ is *visited* if it is a descriptor taken from $R$ at line L2, or is obtained from a visited configuration by one match of line L3. Every descriptor added to $U$ is also put in $R$, and the loop runs until $R$ is empty, so every descriptor in $U$ is eventually taken, and every visited configuration is followed by lines L3 to L5 from it.

## Soundness

**Invariants.** At every moment of the run:

- (I1) If $(A \to \alpha \cdot \beta, u, i)$ is visited or in $U$, then $u$ calls $A$ at some $j$ and $\alpha \Rightarrow^* w[j:i]$.
- (I2) If the edge $v \to u$ exists with $v = (B \to \gamma X \cdot \delta, k)$, then the configuration $(B \to \gamma \cdot X \delta, u, k)$ has been visited.
- (I3) If $(v, i) \in P$ and $v$ calls $X$ at $k$, then $X \Rightarrow^* w[k:i]$; if $i$ was recorded at line L10, then $S \Rightarrow^* w[0:i]$.

*Proof.* All three hold at the start, when everything is empty. We check every step that adds to one of the sets.

- Line L1 adds $(S \to \cdot \gamma, u_0, 0)$: $u_0$ calls $S$ at 0 and $\varepsilon \Rightarrow^* w[0:0]$.
- Line L3 turns a visited $(A \to \alpha \cdot a \beta, u, i)$ with $a_{i+1} = a$ into $(A \to \alpha a \cdot \beta, u, i + 1)$; by I1, $\alpha a \Rightarrow^* w[j:i]\, a_{i+1} = w[j:i+1]$.
- Line L4 processes a visited $(A \to \alpha \cdot B \beta, u, i)$, with $u$ calling $A$ at $j$ and $\alpha \Rightarrow^* w[j:i]$. CREATE makes $v = (A \to \alpha B \cdot \beta, i)$, which calls $B$ at $i$. A new edge $v \to u$ satisfies I2 because the configuration just processed is the one I2 asks for. A replay at line L8 adds $(A \to \alpha B \cdot \beta, u, k)$ for $(v, k) \in P$; by I3, $B \Rightarrow^* w[i:k]$, so $\alpha B \Rightarrow^* w[j:k]$, and $u$ calls $A$ at $j$, which is I1. The descriptors $(B \to \cdot \gamma, v, i)$ satisfy I1 since $v$ calls $B$ at $i$.
- Line L5 processes a visited $(A \to \alpha \cdot, u, i)$, so $A \to \alpha$ is a production and, with $u$ calling $A$ at $j$, $A \Rightarrow \alpha \Rightarrow^* w[j:i]$. If $u = u_0$, then $A = S$ and $j = 0$, and line L10 records $i$ correctly. Otherwise line L11 may add $(u, i)$ to $P$, which satisfies I3. For each edge $u \to v'$, with $u = (B \to \gamma A \cdot \delta, j)$, invariant I2 says $(B \to \gamma \cdot A \delta, v', j)$ was visited, so by I1 $v'$ calls $B$ at some $j'$ with $\gamma \Rightarrow^* w[j':j]$. The added descriptor $(B \to \gamma A \cdot \delta, v', i)$ then has $\gamma A \Rightarrow^* w[j':i]$, which is I1.

No other step changes $U$, the edges or $P$. $\square$

In particular, if line L10 records $n$ then $S \Rightarrow^* w$, so every accepted input is in $L(G)$, and every span reported from $P$ is derived.

## Termination

A slot is a production and a dot position, so there are $s \le |G|$ of them. GSS nodes are pairs of a slot and a position in $0, \dots, n$, so there are at most $s (n + 1) + 1$ of them with the root, and descriptors are triples of a slot, a node and a position, so $U$ is finite. Line L12 puts each descriptor into $R$ at most once, so the main loop takes at most $|U|$ descriptors. Processing one is finite: line L3 advances the dot at most $|G|$ times, line L4 loops over the finitely many productions of $B$, and the loops of lines L8 and L11 run over the finite sets $P$ and the edges of one node. So the run terminates on every grammar and input, including grammars with cycles $A \Rightarrow^+ A$.

## Completeness

For a derivation tree, its *size* is the number of its internal nodes (nodes labelled by nonterminals). For a sequence $\eta = X_1 \cdots X_m$ and a derivation $\eta \Rightarrow^* w[k:i]$, its size is the sum of the sizes of the trees of $X_1, \dots, X_m$, where a terminal has a tree of size 0.

**Lemma A.** Let $(C \to \alpha \cdot X \beta, v, i)$ be visited, and let $X \Rightarrow^* w[i:j]$ by a tree of size $t$ ($t = 0$ when $X$ is a terminal). Then $(C \to \alpha X \cdot \beta, v, j)$ is visited.

**Lemma B.** Let $(C \to \cdot \eta, v, k)$ be visited, and let $\eta \Rightarrow^* w[k:i]$ with size $t$. Then $(C \to \eta \cdot, v, i)$ is visited.

*Proof of both, by strong induction on $t$.* We prove Lemma A for size $t$ assuming Lemma B for sizes less than $t$, and Lemma B for size $t$ assuming Lemma A for sizes at most $t$.

*Lemma A, $X$ a terminal.* Then $t = 0$, $j = i + 1$ and $a_{i+1} = X$, so line L3 matches and $(C \to \alpha X \cdot \beta, v, i + 1)$ is visited by definition.

*Lemma A, $X$ a nonterminal.* The root of the tree uses a production $X \to \eta$ and $\eta \Rightarrow^* w[i:j]$ with size $t - 1$. Processing the visited configuration reaches line L4, which makes the node $x = (C \to \alpha X \cdot \beta, i)$, ensures the edge $x \to v$, and adds $(X \to \cdot \eta, x, i)$ unless it is already in $U$; either way it is in $U$, hence taken from $R$ and visited. By Lemma B for size $t - 1$, $(X \to \eta \cdot, x, j)$ is visited, and processing it calls POP$(x, j)$ at line L5. Since $x \ne u_0$, after that call $(x, j) \in P$. Now compare the moments $T_e$, when the edge $x \to v$ was added, and $T_p$, when $(x, j)$ was added to $P$; they are different steps. If $T_e < T_p$, then at $T_p$ line L11 runs over the edges of $x$, which include $x \to v$, and adds $(C \to \alpha X \cdot \beta, v, j)$. If $T_p < T_e$, then at $T_e$ line L8 runs over the entries of $P$ for $x$, which include $(x, j)$, and adds the same descriptor. In both cases it is in $U$, hence visited.

*Lemma B.* Write $\eta = X_1 \cdots X_m$ and split $w[k:i]$ as $w[k_0:k_1] \cdots w[k_{m-1}:k_m]$ with $k_0 = k$, $k_m = i$, and $X_r \Rightarrow^* w[k_{r-1}:k_r]$ by a tree of size $t_r \le t$. If $m = 0$ the claim is the hypothesis. Otherwise apply Lemma A $m$ times: from the visited $(C \to X_1 \cdots X_{r-1} \cdot X_r \cdots X_m, v, k_{r-1})$ it gives the visited $(C \to X_1 \cdots X_r \cdot X_{r+1} \cdots X_m, v, k_r)$, and after $m$ steps $(C \to \eta \cdot, v, i)$. $\square$

**Theorem.** The recognizer accepts $w$ if and only if $S \Rightarrow^* w$. Moreover, for every GSS node $v$ that calls $X$ at $k$ and every $j$ with $X \Rightarrow^* w[k:j]$, the pair $(v, j)$ is in $P$.

*Proof.* If the input is accepted, line L10 recorded $n$, and by invariant I3 $S \Rightarrow^* w$. Conversely, let $S \Rightarrow \eta \Rightarrow^* w$. Line L1 adds $(S \to \cdot \eta, u_0, 0)$, which is then visited, and Lemma B gives that $(S \to \eta \cdot, u_0, n)$ is visited; processing it calls POP$(u_0, n)$ at line L5, so line L10 records $n$ and line L6 accepts. For the second claim, the node $v = (C \to \alpha X \cdot \beta, k)$ was created at line L4 while processing a visited $(C \to \alpha \cdot X \beta, u, k)$, and the argument in the proof of Lemma A, with $x = v$, shows that $(v, j) \in P$ for every derivation $X \Rightarrow^* w[k:j]$. $\square$

**Remark on the order.** The proofs never use the order in which descriptors are taken from $R$. Read the steps as rules: line L4 turns a configuration into a node, an edge and call descriptors; line L5 turns a configuration and an edge, or a configuration at the root, into a descriptor or a recorded end; and so on. Every member of the final sets was produced by a rule from members present earlier, and the final sets are closed under every rule, because each rule fires when the last of its premises appears (this is what lines L8 and L11 ensure for the pair of an edge and an entry of $P$). So the final sets are the least sets closed under the rules, whatever the order. ∎
