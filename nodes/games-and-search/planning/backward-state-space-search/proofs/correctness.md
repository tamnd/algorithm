---
title: Backward state-space search is sound and complete, and breadth-first order gives a plan with the fewest actions
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode BACKWARD-SEARCH of the page, for a ground STRIPS task $(F, A, I, G)$ with $n = |F|$, $m = |A|$ and $\mathit{add}(a) \cap \mathit{del}(a) = \emptyset$ for every action. Write $s[a] = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$, $\mathit{regress}(g, a) = (g \setminus \mathit{add}(a)) \cup \mathit{pre}(a)$, and say that $a$ is relevant for $g$ when $\mathit{add}(a) \cap g \ne \emptyset$ and $\mathit{del}(a) \cap g = \emptyset$. For a sequence $\pi$ of actions and a state $s$, write $s[\pi]$ for the final state when $\pi$ is applicable from $s$.

**Lemma 1 (exactness of regression).** Let $\mathit{del}(a) \cap g = \emptyset$. For every state $s$, $\mathit{regress}(g, a) \subseteq s$ if and only if $\mathit{pre}(a) \subseteq s$ and $g \subseteq s[a]$.

*Proof.* Suppose $\mathit{regress}(g, a) \subseteq s$. Then $\mathit{pre}(a) \subseteq s$. A fact $f \in g \cap \mathit{add}(a)$ is in $s[a]$. A fact $f \in g \setminus \mathit{add}(a)$ is in $s$, and not in $\mathit{del}(a)$ because $\mathit{del}(a) \cap g = \emptyset$, so it is in $s \setminus \mathit{del}(a) \subseteq s[a]$. Conversely, suppose $\mathit{pre}(a) \subseteq s$ and $g \subseteq s[a]$. A fact $f \in g \setminus \mathit{add}(a)$ is in $s[a] = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$ and not in $\mathit{add}(a)$, so it is in $s$. With $\mathit{pre}(a) \subseteq s$ this gives $\mathit{regress}(g, a) \subseteq s$. $\square$

**Invariant (P).** At the start of each pass of the loop at line L3, for each key $h$ of `parent`, the sequence $\pi_h$ = PLAN(parent, $h$) has this property: for every state $s$ with $h \subseteq s$, $\pi_h$ is applicable from $s$ and $G \subseteq s[\pi_h]$. Every subgoal in $Q$ is a key.

*Proof.* Before the loop the only key is $G$, and $\pi_G$ is empty, so the property holds. A pass adds a key $h$ only at line L10, with $\mathit{parent}[h] = (g, a)$, where $g$ is a key, $a$ is relevant for $g$ (line L7), and $h = \mathit{regress}(g, a)$ (line L8). PLAN puts $a$ first and then the actions of $\pi_g$, so $\pi_h$ is $a$ followed by $\pi_g$. Let $h \subseteq s$. By Lemma 1, $a$ is applicable in $s$ and $g \subseteq s[a]$. By the property for $g$, $\pi_g$ is applicable from $s[a]$ and ends in a state that contains $G$. Line L9 sets `parent` only for a new key, so the sequences of the old keys do not change. Line L11 puts in $Q$ only the key just added. $\square$

**Theorem 1 (soundness).** If BACKWARD-SEARCH returns a sequence, it is a plan.

*Proof.* It returns at line L5 only for a key $g$ with $g \subseteq I$. By (P) with $s = I$, PLAN(parent, $g$) is applicable from $I$ and ends in a state that contains $G$. $\square$

**Theorem 2 (termination).** The loop makes at most $2^n$ passes.

*Proof.* The keys are distinct subsets of $F$, so there are at most $2^n$. A subgoal enters $Q$ only when it becomes a key (lines L9 to L11), and each pass removes one from $Q$. $\square$

Let the *regression graph* be the directed graph whose nodes are the subsets of $F$, with an edge from $g$ to $\mathit{regress}(g, a)$ for each action $a$ relevant for $g$. BACKWARD-SEARCH is breadth-first search in this graph from $G$, with the targets $T = \{h : h \subseteq I\}$ tested at removal.

**Lemma 2 (paths and plans).** (a) If the regression graph has a path of $k$ edges from $G$ to a node of $T$, then a plan with $k$ actions exists. (b) If a plan with $k$ actions exists, the regression graph has a path of at most $k$ edges from $G$ to a node of $T$.

*Proof.* (a) Let the path be $G = h_0, h_1, \ldots, h_k$ with $h_k \subseteq I$, where the edge from $h_{j-1}$ to $h_j$ uses the action $b_j$. We show by induction on $k - j$ that the sequence $b_j, b_{j-1}, \ldots, b_1$ is applicable from every state $s \supseteq h_j$ and ends in a state that contains $G$. For $j = 0$ the sequence is empty and $s \supseteq G$. For $j \ge 1$, $h_j = \mathit{regress}(h_{j-1}, b_j)$ and $b_j$ deletes no fact of $h_{j-1}$, so by Lemma 1, $b_j$ applies in $s$ and $s[b_j] \supseteq h_{j-1}$, and the claim for $j - 1$ finishes the step. With $j = k$ and $s = I$ we get a plan of $k$ actions.

(b) Let $a_1, \ldots, a_k$ be a plan, with states $s_0 = I$ and $s_i = s_{i-1}[a_i]$, so $G \subseteq s_k$. We define subgoals $c_k, c_{k-1}, \ldots, c_0$ with $c_i \subseteq s_i$, each reached from $G$ by a path of at most $k - i$ edges. Let $c_k = G$. For $i$ from $k$ down to 1: if $\mathit{add}(a_i) \cap c_i = \emptyset$, let $c_{i-1} = c_i$. A fact of $c_i$ is then in $s_i$ but not in $\mathit{add}(a_i)$, so it is in $s_{i-1}$; thus $c_{i-1} \subseteq s_{i-1}$, with the same path. Otherwise $\mathit{add}(a_i) \cap c_i \ne \emptyset$. Since $\mathit{add}(a_i) \cap \mathit{del}(a_i) = \emptyset$, no fact of $\mathit{del}(a_i)$ is in $s_i$, so $\mathit{del}(a_i) \cap c_i = \emptyset$, and $a_i$ is relevant for $c_i$. Let $c_{i-1} = \mathit{regress}(c_i, a_i)$, one more edge. By Lemma 1, applied to $s_{i-1}$, where $a_i$ applies and $s_{i-1}[a_i] = s_i \supseteq c_i$, we have $c_{i-1} \subseteq s_{i-1}$. At the end $c_0 \subseteq s_0 = I$, so $c_0 \in T$, and its path has at most $k$ edges. $\square$

**Theorem 3 (completeness).** If a plan exists, BACKWARD-SEARCH returns a plan. If it returns failure, no plan exists.

*Proof.* By Theorem 2 it returns a plan or failure, so the two claims are the same. Suppose it returns failure at line L12. Then every key was removed and expanded, and none is in $T$. Every node $h$ reachable from $G$ in the regression graph is a key: along a path $G = h_0, \ldots, h_j = h$, $h_0$ is a key, and if $h_{i-1}$ is a key it was expanded, its edge to $h_i$ passed line L7, and $h_i$ was a key already or became one at line L10. So no node of $T$ is reachable from $G$, and by Lemma 2 (b) no plan exists. $\square$

**Theorem 4 (fewest actions).** With the FIFO queue, a returned plan has exactly $k^*$ actions, where $k^*$ is the least number of actions of a plan.

*Proof.* Let $D(h)$ be the number of edges of a shortest path from $G$ to $h$ in the regression graph, and $\ell(h)$ the length of PLAN(parent, $h$) for a key $h$, which is the number of edges of the path in `parent` from $G$ to $h$, so $\ell(h) \ge D(h)$. The search is breadth-first search with duplicate detection on a finite graph, with the target test at removal, and the three steps of the proof of Theorem 4 on the page [forward state-space search](/forward-state-space-search/) use nothing else; we repeat them for this graph. (1) The values $\ell$ in $Q$, from the front to the back, are nondecreasing and span at most 1, because the new keys go to the back with $\ell(g) + 1$, where $g$ was removed from the front; so the removed values never decrease and grow by at most 1 from one pass to the next, and every key of value $d$ enters $Q$ before the first key of value $d$ leaves it. (2) By induction on $d$: when the first key of value $d$ is removed, every $h$ with $D(h) \le d$ is a key with $\ell(h) = D(h)$. For $d = 0$ this is $G$. For the step, a node $h$ with $D(h) = d + 1$ has a predecessor $w$ on a shortest path with $D(w) = d$; $w$ is a key of value $d$ by the hypothesis, it is removed and expanded before the first key of value $d + 1$ leaves $Q$, and its expansion makes $h$ a key of value at most $d + 1$, so $\ell(h) = D(h)$. (3) Let $D^* = \min \{ D(h) : h \in T \}$ and let $h^* \in T$ have $D(h^*) = D^*$. If the search stopped at a target $g$ with $\ell(g) > D^*$, then a key of value $D^*$ was removed before $g$, so by (2) $h^*$ was a key of value $D^*$, and by (1) it was removed before $g$ and stopped the search at line L5. This is a contradiction, so the plan has $\ell(g) = D^*$ actions. By Lemma 2 (a) a plan with $D^*$ actions exists, so $k^* \le D^*$, and by Lemma 2 (b) $D^* \le k^*$. $\square$

**Theorem 5 (cost).** Let $u$ be the number of keys at the end. BACKWARD-SEARCH takes $O(u m n)$ time and $O(u n)$ space, and $u \le 2^n$.

*Proof.* There are at most $u$ passes. In a pass, line L5, each relevance test of line L7 and each regression of line L8 cost $O(n)$, and the lookup of line L9 costs $O(n)$ to hash the subgoal plus expected $O(1)$ with a hash table. So a pass costs $O(m n)$. PLAN costs $O(n)$ per action of the plan, and the plan has at most $u$ actions. The table and the queue hold at most $u$ subgoals of $O(n)$ bits. $\square$
