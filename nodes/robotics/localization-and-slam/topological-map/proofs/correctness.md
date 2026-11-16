---
title: The topological map keeps its invariant, ROUTE finds a shortest route, and LOCALIZE returns exactly the consistent places
proves: [correctness]
status: full
---

**Setting.** A map has the places $0, \dots, V - 1$, the signatures $\mathrm{sig}[v]$ and the dictionaries $\mathrm{out}[v]$. For a place $v$ and an action $a$, write $\mathrm{step}(v, a) = w$ if $\mathrm{out}[v][a] = (w, \ell)$, and $\mathrm{step}(v, a) = \bot$ if $a$ is not a key of $\mathrm{out}[v]$. The invariant (T) is: (1) each pair $(v, a)$ has at most one entry; (2) every edge added by ADD-EDGE has its two entries; (3) every length is $\ge 0$.

For the data $\sigma_0$ and $(a_1, \sigma_1), \dots, (a_k, \sigma_k)$, a place $w$ is *consistent* if there are places $v_0, v_1, \dots, v_k = w$ with $\mathrm{sig}[v_0] = \sigma_0$ and, for $i = 1, \dots, k$, $v_i = \mathrm{step}(v_{i-1}, a_i) \ne \bot$ and $\mathrm{sig}[v_i] = \sigma_i$.

**Assumptions.** Dictionary operations behave as maps from keys to values. Lengths are compared and added exactly.

**Claim.**

1. ADD-PLACE and ADD-EDGE keep (T), or ADD-EDGE raises an error and leaves the map unchanged.
2. ROUTE$(s, t)$ returns the length of a shortest directed path from $s$ to $t$ in the graph with an arc $u \to w$ of length $\ell$ for each entry $\mathrm{out}[u][a] = (w, \ell)$, together with a path of that length and its actions, or none if there is no path.
3. LOCALIZE returns exactly the set of consistent places.

*Proof.*

*Claim 1.* ADD-PLACE appends a place with an empty dictionary, which adds no entry, so (T) still holds. ADD-EDGE first checks that both places exist and that $\ell \ge 0$, else it raises an error before any change. Line L2 raises an error if $a$ is already a key of $\mathrm{out}[u]$, or $b$ of $\mathrm{out}[v]$, or if $u = v$ and $a = b$, in which case the two writes of line L3 would give one key two meanings. Otherwise $a$ is new at $u$ and $b$ is new at $v$, and they are different keys if $u = v$, so line L3 adds two new entries and changes none. Part 1 holds because each new key was absent, part 2 because both entries are written, and part 3 because $\ell \ge 0$.

*Claim 2.* The arcs of the graph are the entries of the dictionaries, and by (T) all lengths are $\ge 0$. Lines L4 to L8 are Dijkstra's algorithm with a binary heap and lazy deletion: an entry $(\delta, u)$ with $\delta > d[u]$ is out of date and skipped. For nonnegative lengths, Dijkstra's algorithm pops each place $u$ with $\delta = d[u]$ equal to its shortest distance from $s$, and $\mathrm{prev}$ then holds a shortest path tree of the places reached; the proof is on the page of [Dijkstra's algorithm](/dijkstra/). Stopping when $t$ is popped does not change $d[t]$, which is final at that moment. If $t$ is never reached, no path exists, because every place reachable from $s$ is eventually pushed. Line L9 follows $\mathrm{prev}$ from $t$; each $\mathrm{prev}[w] = (u, a)$ was set together with $d[w] = d[u] + \ell$ for $\mathrm{out}[u][a] = (w, \ell)$, so the actions replay the path and its lengths add up to $d[t]$. The chain ends at $s$. Say that a place is settled when it is popped with $\delta = d[u]$. Line L8 sets $\mathrm{prev}[w] = (u, a)$ only while $u$ is being settled, and $w$ is settled later, after its last such update, so along the chain the settle times strictly decrease. (The place $t$ is settled when the loop stops.) Hence the chain has no cycle. It can only end at a place without $\mathrm{prev}$, and $s$ is the only such place that was reached: $d[s] = 0$ and lengths are $\ge 0$, so line L8 never sets $\mathrm{prev}[s]$, while every other place that was reached got its $d$ from line L8.

*Claim 3.* Let $C_i$ be the set after $i$ passes of line L12, and let $K_i$ be the set of places consistent with the first $i$ steps of the data. We show $C_i = K_i$ by induction on $i$.

For $i = 0$, line L10 gives $C_0 = \{v : \mathrm{sig}[v] = \sigma_0\}$, which is $K_0$ by the definition with $k = 0$.

Assume $C_{i-1} = K_{i-1}$. If $w \in K_i$, there is a chain $v_0, \dots, v_i = w$ as in the definition. Its first $i - 1$ steps show $v_{i-1} \in K_{i-1} = C_{i-1}$, and $w = \mathrm{step}(v_{i-1}, a_i)$ with $\mathrm{sig}[w] = \sigma_i$, so line L12 puts $w$ into $C_i$. Conversely, if $w \in C_i$, line L12 found some $v \in C_{i-1} = K_{i-1}$ with $\mathrm{step}(v, a_i) = w$ and $\mathrm{sig}[w] = \sigma_i$. The chain for $v$ extended by $w$ shows $w \in K_i$. So $C_i = K_i$, and LOCALIZE returns $C_k = K_k$.

By part 1 of (T), $\mathrm{step}(v, a_i)$ has at most one value, so each place of $C_{i-1}$ gives at most one place of $C_i$ and $|C_i| \le |C_{i-1}|$. $\blacksquare$

**Remark.** If the robot senses and acts without error, its true place is consistent by the definition, so it is in the set that LOCALIZE returns.
