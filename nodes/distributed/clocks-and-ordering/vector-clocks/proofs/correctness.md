---
title: Vector clocks count the causal past and characterize happened-before
proves: [correctness]
status: full
---

We use the model of the page: $n$ processes $p_1, \ldots, p_n$ and asynchronous message passing, with channels that need not be FIFO. Each event is one call of TICK, SEND or RECEIVE, and $V(e)$ is the vector that this call returns. We write $P_k$ for the set of events of $p_k$, and $\to$ for [happened-before](/happened-before/). The causal past of $e$ is $\downarrow e = \{g : g \to e\} \cup \{e\}$.

**Lemma 1 (no cycles).** If $g \to e$, then $g$ comes before $e$ in the run.

*Proof.* A chain for $g \to e$ has steps of two kinds: an earlier event to a later event of the same process, and a send to its receive. A receive comes after its send in the run. So each step goes forward in the run, and so does the chain. $\square$

**Lemma 2 (prefixes).** For each event $e$ and each $k$, the set $\downarrow e \cap P_k$ is a prefix of the sequence of events of $p_k$. If $e \in P_i$, then $\downarrow e \cap P_i$ is the prefix that ends at $e$.

*Proof.* Let $g \in \downarrow e \cap P_k$ and let $g'$ come before $g$ on $p_k$. Then $g' \to g$, and $g = e$ or $g \to e$, so $g' \to e$ by transitivity and $g' \in \downarrow e$. This shows the prefix property. If $e \in P_i$, each event of $p_i$ up to $e$ is in $\downarrow e$ by the same step. An event $g$ of $p_i$ after $e$ satisfies $e \to g$, so $g \to e$ would give $e \to e$ by transitivity, which Lemma 1 rules out. So the prefix ends at $e$. $\square$

**Lemma 3 (the count).** For each event $e$ and each $k$, $V(e)[k] = |\downarrow e \cap P_k|$.

*Proof.* By induction on the position of $e$ in the run. Let $e \in P_i$. Let $r$ be the event just before $e$ on $p_i$, if it exists, and let $s$ be the send of the message, if $e$ is a receive. Any chain that ends at $e$ has a last step from $r$ or an earlier event of $p_i$, or from $s$. So $\downarrow e = \{e\} \cup \downarrow r \cup \downarrow s$, where a missing event gives the empty set. Both $r$ and $s$ come before $e$, so the induction hypothesis holds for them.

Before the call for $e$, $V_i$ equals $V(r)$, or the zero vector of line L1 if $r$ does not exist. If $e$ is a receive, the message carries $V(s)$, because line L4 attaches the value that TICK returns. Lines L5 and L6 set $V_i[k] = \max(V(r)[k], V(s)[k])$. By Lemma 2, $\downarrow r \cap P_k$ and $\downarrow s \cap P_k$ are two prefixes of one sequence. The union of two prefixes is the longer one, so its size is the maximum of the two sizes. By the induction hypothesis this is $V_i[k]$ after line L6. For a local event or a send, there is no $s$ and the same holds with $V(r)$ alone.

The event $e$ is not in $\downarrow r \cup \downarrow s$, by Lemma 1. So $|\downarrow e \cap P_k|$ is the value above for $k \ne i$, and that value plus 1 for $k = i$. Line L2 adds exactly 1 to entry $i$ and changes no other entry, so $V(e)$ is as claimed. $\square$

**Theorem (characterization).** For all events $e \ne f$ with $e \in P_i$:

$$e \to f \iff V(e) < V(f) \iff V(e)[i] \le V(f)[i],$$

where $V < W$ means $V[k] \le W[k]$ for all $k$ and $V \ne W$. Also $e \parallel f$ if and only if neither $V(e) \le V(f)$ nor $V(f) \le V(e)$.

*Proof.* Assume $e \to f$. For each $g \in \downarrow e$, $g = e$ or $g \to e$, so $g \to f$ by transitivity. So $\downarrow e \subseteq \downarrow f$, and Lemma 3 gives $V(e) \le V(f)$. Let $f \in P_j$. Then $f \in \downarrow f$, and $f \notin \downarrow e$ because $f \to e$ and $e \to f$ would give $e \to e$. So $V(e)[j] < V(f)[j]$ and $V(e) < V(f)$.

The step from $V(e) < V(f)$ to $V(e)[i] \le V(f)[i]$ is direct.

Assume $V(e)[i] \le V(f)[i]$. By Lemma 2, $\downarrow e \cap P_i$ is the prefix of $p_i$ that ends at $e$, and $\downarrow f \cap P_i$ is a prefix of $p_i$. By Lemma 3 the second prefix is at least as long as the first, so it contains $e$. So $e \in \downarrow f$, and $e \ne f$ gives $e \to f$.

For the last claim, first $V(e) \ne V(f)$. If $V(e) = V(f)$, then $V(e)[i] \le V(f)[i]$, so $e \to f$ by the chain of equivalences, and then $V(e) < V(f)$, which excludes equality. So $V(e) \le V(f)$ is the same as $V(e) < V(f)$, and $V(f) \le V(e)$ is the same as $V(f) < V(e)$. By the first part, applied in both directions, neither holds if and only if neither $e \to f$ nor $f \to e$, which is $e \parallel f$. $\blacksquare$
