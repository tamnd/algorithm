---
title: An MV-Register returns the maximal writes of its causal history and is a CRDT
proves: [correctness, invariant, termination]
status: full
---

**Setting.** There are $n$ replicas with ids $1, \ldots, n$. Replica $i$ runs the main block with state $S_i$. In one step a replica runs WRITE (lines L3 to L6), sends a copy of its state, or runs MERGE (line L7) on a copy that some replica sent earlier. Copies may be lost, merged more than once and merged in any order.

**Histories.** The causal history $C_i$ is a set of write events. A write $w$ at $i$ sets $C_i \leftarrow C_i \cup \{w\}$, and we define its history $h(w)$ as the new $C_i$. A MERGE at $i$ of a copy sent when the sender had history $H$ sets $C_i \leftarrow C_i \cup H$. Write $w \preceq w'$ when $w \in h(w')$. For a write $w$ let $x(w)$ be its value, $r(w)$ its replica, and $\#_j(w) = |\{u \in h(w) : r(u) = j\}|$. For a set $D$ of writes let $\max D$ be the set of $w \in D$ such that no $u \in D$ with $u \ne w$ has $w \preceq u$.

**Claim 1 (histories are down-closed and per-replica prefixes).** At every time, (a) if $w \in C_i$ then $h(w) \subseteq C_i$; (b) the writes of replica $j$ in $C_i$ are the first $k$ writes of $j$ for some $k$; (c) $\preceq$ is a partial order.

*Proof.* (a) By induction: a write adds $w$ with $h(w) = C_i \cup \{w\}$, and a merge adds a history that is down-closed by the hypothesis for the sender. (b) The writes of $i$ are made at $i$ in order and each is added to $C_i$ when it is made; any history merged into $C_i$ holds only writes of $i$ made earlier. For $j \ne i$, a merged history holds a prefix of $j$'s writes by the hypothesis, and the union of two prefixes is a prefix. (c) Reflexive since $w \in h(w)$. Transitive by (a). Antisymmetric because $u \in h(w)$ with $u \ne w$ means $u$ was made before $w$. $\square$

**Claim 2 (vectors encode the order).** Let $V(w)$ be the vector stored with $w$ on line L6. If the state invariant of Claim 3 holds when $w$ is made, then $V(w)[j] = \#_j(w)$ for every $j$, and for any two writes $V(w) \le V(w')$ exactly when $w \preceq w'$.

*Proof.* At the time of the write, by Claim 3, $S_i$ holds the maximal writes of $C_i$ with their vectors. Every write in $C_i$ is below a maximal one, so by the hypothesis on the vectors of earlier writes and Claim 1(b), the largest $j$ entry among them is the number of $j$-writes in $C_i$. Line L4 computes these numbers and line L5 counts $w$ itself, so $V(w)[j] = \#_j(w)$. For the order: if $w \preceq w'$ then $h(w) \subseteq h(w')$ by Claim 1(a), so $V(w) \le V(w')$. Conversely, let $w$ be the $k$-th write of $j$, so $V(w)[j] = k$. If $V(w) \le V(w')$, then $h(w')$ holds at least $k$ writes of $j$, which by Claim 1(b) are the first $k$, so $w \in h(w')$. $\square$

**Claim 3 (main invariant).** At every time, $S_i = \{(x(w), V(w)) : w \in \max C_i\}$, and every copy in transit satisfies the same with its history.

*Proof.* By induction on the steps, using Claim 2 for the writes made so far. At the start both sides are empty. A copy is a state and history of its sender at one time. WRITE: the new write $w$ has $h(w) = C_i \cup \{w\}$, so every write of $C_i$ is below it and $\max(C_i \cup \{w\}) = \{w\}$, which is what line L6 stores. MERGE of a copy with history $H$: by the hypothesis $S_i \cup T$ holds the pairs of $\max C_i \cup \max H$. A write $w$ is in $\max(C_i \cup H)$ exactly when it is in $\max C_i \cup \max H$ and no write of that set strictly follows it, since every write of $C_i \cup H$ is below some write of $\max C_i \cup \max H$. By Claim 2 "strictly follows" is "has a strictly larger vector", which lines L8 and L9 test. Two different writes have different vectors by Claim 2, so pairs do not collide. $\square$

**Theorem 1 (safety).** READ at $i$ returns $\{x(w) : w \in \max C_i\}$.

*Proof.* Line L2 and Claim 3. $\square$

**Theorem 2 (semilattice).** Map a state $S$ to $D(S) = \{u : u \preceq w \text{ for some } (x(w), V(w)) \in S\}$, a finite down-closed set of writes. By Claim 3, $D(S_i) = C_i$, and $S = \{(x(w), V(w)) : w \in \max D(S)\}$, so the map is one to one on reachable states. Order states by $S \le T$ when $D(S) \subseteq D(T)$; by Claim 2 this is the test "every vector of $S$ is below some vector of $T$". Finite down-closed sets under inclusion form a join-semilattice with join $\cup$, so states do too, with join $S \sqcup T$ given by the maximal writes of $D(S) \cup D(T)$. MERGE computes this join, by the argument of Claim 3, and WRITE is inflationary, since $D$ gains $w$.

*Proof.* A union of down-closed sets is down-closed, contains both, and is contained in every set that contains both, so it is the least upper bound. The rest is stated above. $\square$

**Theorem 3 (convergence).** If writes stop and every replica sends its state to every other replica infinitely often over fair-lossy channels, then there is a time after which all replicas hold the same state, and READ returns the values of the maximal writes of the whole run.

*Proof.* After the last write, each replica in the end merges a copy from every other replica sent after the last write, and then its history contains theirs. After finitely many merges every history is the set of all writes, and Claim 3 fixes the state. $\square$

**Size bound.** The writes of one replica are totally ordered by Claim 1, so $\max C_i$ has at most one write per replica and $|S_i| \le n$.

**Termination.** Each loop runs over a finite set of at most $2n$ pairs. $\blacksquare$
