---
title: FILL adds exactly the sound edges, so READ decides membership and returns a parse tree
proves: [correctness]
status: full
---

**Statement.** Let $G$ be any context-free grammar and $w = a_1 \cdots a_n$. Call an edge $(i, j, A \to \alpha \cdot \beta)$ *sound* if

(P) $S \Rightarrow^* w[0:i] \, A \, \delta$ for some $\delta \in (V \cup \Sigma)^*$, and (D) $\alpha \Rightarrow^* w[i:j]$.

When FILL stops, the chart contains exactly the sound edges. Consequently READ finds a complete edge $(0, n, S \to \gamma \cdot)$ if and only if $w \in L(G)$, and in that case following the backpointers terminates and yields a parse tree of $w$. FILL itself stops, because there are at most $|G| (n + 1)^2$ edges and each is pushed on the agenda once.

*Proof.*

**Step 1 (only sound edges).** By induction on the order in which edges are added. L5 adds $(0, 0, S \to \cdot \gamma)$: (P) holds with $\delta = \varepsilon$ and (D) is $\varepsilon \Rightarrow^* \varepsilon$. Prediction at L7, from a sound $(i, j, A \to \alpha \cdot B \beta')$, adds $(j, j, B \to \cdot \gamma)$: from $S \Rightarrow^* w[0:i] A \delta \Rightarrow w[0:i] \alpha B \beta' \delta \Rightarrow^* w[0:j] B \beta' \delta$ we get (P), and (D) is trivial. The scan at L9 appends $a_{j+1}$ to $\alpha$, so (D) holds for $w[i:j+1]$, and (P) is unchanged. The fundamental rule at L8 or L10 combines $(i, j, A \to \alpha \cdot B \beta')$ with $(j, k, B \to \gamma \cdot)$, both sound: $\alpha B \Rightarrow^* w[i:j] \gamma \Rightarrow^* w[i:j] w[j:k] = w[i:k]$, and (P) is that of the active edge.

**Step 2 (the fundamental rule fires).** Suppose the edges $e' = (i, k, A \to \alpha' \cdot B \beta)$ and $f = (k, j, B \to \gamma \cdot)$ are both added. Each is pushed on the agenda once and popped later. If $f$ was added before $e'$ is popped, L8 finds $f$ in COMPLETE$(k, B)$ when $e'$ is popped. Otherwise $e'$ was popped, hence added and put into WAITING$(k, B)$ at L3, before $f$ was added, and L10 finds $e'$ when $f$ is popped. Either way $(i, j, A \to \alpha' B \cdot \beta)$ is added.

**Step 3 (all sound edges).** Let $e = (i, j, A \to \alpha \cdot \beta)$ be sound. Take a tree for the derivation in (P), with root $S$ and frontier $w[0:i] A \delta$, and at its leaf $A$ attach a node $x$ with the children $\alpha \beta$, where the children in $\alpha$ get the subtrees of a derivation $\alpha \Rightarrow^* w[i:j]$ and the children in $\beta$ stay leaves. Call the result $T$. In $T$, every leaf to the left of the last child of $\alpha$ is a terminal or $\varepsilon$.

Walk $T$ depth first, from left to right, and record an *event* $(y, 0)$ when the walk enters an inner node $y$ and an event $(y, d)$ when it has finished the $d$-th child of $y$. Stop at the event $(x, |\alpha|)$. For each recorded event $(y, d)$, all leaves to the left of $y$ and all leaves below the first $d$ children of $y$ are terminals or $\varepsilon$: they lie to the left of the end of $\alpha$ in $T$. So with $s$ the number of terminals to the left of $y$ and $t$ the number up to the end of the $d$-th child, the event names the edge $E(y, d) = (s, t, C \to \mu \cdot \nu)$, where $C \to \mu \nu$ is the production of $y$ and $|\mu| = d$. The last event names $E(x, |\alpha|) = e$. We show by induction along the walk that each named edge is added.

- $(y, 0)$ for the root: $y$ is $S$, $s = 0$, and L5 adds $(0, 0, S \to \cdot \gamma)$.
- $(y, 0)$ for a node $y$ that is the $(d + 1)$-th child of its parent $z$: the event $(z, d)$ came before, so $E(z, d)$, whose dot is before the label of $y$, is added, and when it is popped, prediction at L7 adds $E(y, 0)$.
- $(y, d)$ with $d \ge 1$ and a terminal $d$-th child: the event $(y, d - 1)$ came before; when its edge is popped, the next input token is that terminal, and the scan at L9 adds $E(y, d)$.
- $(y, d)$ with $d \ge 1$ and a nonterminal $d$-th child $u$: this child lies to the left of the end of $\alpha$, so it is an inner node, with a production $B \to \gamma$; the events $(y, d - 1)$ and $(u, |\gamma|)$ came before, so their edges $(s, k, \ldots \cdot B \ldots)$ and $(k, t, B \to \gamma \cdot)$ are added, and by Step 2 the fundamental rule adds $E(y, d)$.

So $e$ is added. Together with Step 1, the chart holds exactly the sound edges.

**Step 4 (READ).** A complete edge $(0, n, S \to \gamma \cdot)$ is sound iff $\gamma \Rightarrow^* w$ for a production $S \to \gamma$, that is, iff $w \in L(G)$; (P) holds trivially. By Steps 1 and 3, READ finds such an edge iff $w \in L(G)$. Every backpointer of an edge $e$ names edges that were already in the chart when $e$ was added, so the relation "is named by a backpointer of" is contained in the order of insertion and has no cycle; following backpointers from any edge reaches only finitely many edges and stops. For an edge built by L8, L9 or L10, the backpointer is the shorter edge for $A \to \alpha' \cdot X \beta$ and the child, a token or a complete edge for $X$; for an edge built by L5 or L7, it is empty. Unfolding the chain of an edge $(i, j, A \to \gamma \cdot)$ therefore lists children $X_1, \ldots, X_m$ with $\gamma = X_1 \cdots X_m$ and consecutive spans from $i$ to $j$, each a token equal to its terminal or a complete edge for its nonterminal. By induction on the insertion order, the tree built from $(i, j, A \to \gamma \cdot)$ is a parse tree with root $A$ and yield $w[i:j]$, so the tree read from $(0, n, S \to \gamma \cdot)$ is a parse tree of $w$. $\blacksquare$
