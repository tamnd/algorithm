---
title: Dial's algorithm computes the distances
proves: [correctness, termination]
status: full
---

**Claim.** Let $G$ be a directed graph with integer weights in $\{0, \ldots, C\}$ and a source $s$. DIAL ends, and at the end $d[v] = \delta(s, v)$ for every $v$; for every $v \ne s$ with $d[v] < \infty$, $d[v] = d[\pi[v]] + w(\pi[v], v)$.

**Notation.** An *entry* is an occurrence of a vertex in a bucket; its *key* is the label the vertex got when the entry was added. Let $K$ be the multiset of keys of all entries in the buckets; $\text{left} = |K|$.

**Step 1: the window.** Invariant: every key in $K$ lies in $\{i, i + 1, \ldots, i + C\}$, and an entry with key $k$ is in bucket $B[k \bmod (C + 1)]$.

It holds after line L3, with $K = \{0\}$ and $i = 0$. Line L10 adds the key $i + w$ with $0 \le w \le C$, inside the window, to the right bucket. Lines L6 and L7 only remove entries. Line L5 raises $i$ by one only when $B[i \bmod (C + 1)]$ is empty. The $C + 1$ values $i, \ldots, i + C$ have distinct residues modulo $C + 1$, so only key $i$ maps to that bucket; its being empty means $i \notin K$, and all keys lie in $\{i + 1, \ldots, i + C\} \subseteq \{i + 1, \ldots, i + 1 + C\}$.

**Step 2: termination.** In line L5, $\text{left} > 0$, so some key $k \in \{i, \ldots, i + C\}$ exists, and $i$ stops at the latest at $k$. So line L5 ends. Each label drop in line L10 lowers $d[v]$; while $u$ is scanned, $d[u] = i$, and a vertex is scanned only when $d[u] = i$ (line L7), and $i$ never decreases, so each vertex is scanned at most once (a second scan would need the same label at a later moment, but its entry with that key was removed and labels only fall). So line L10 runs at most $m$ times, there are at most $m + 1$ entries in total, each pass of line L4 removes one, and the loop ends.

**Step 3: the same run as Dijkstra.** By Step 1, the bucket emptied in line L6 holds exactly the entries with key $i$, and all keys are at least $i$. So line L6 removes an entry of least key, as extract-min does on a binary heap holding the same entries. The key of an entry for $u$ satisfies $d[u] \le$ key, since labels only fall; line L7 skips it exactly when $d[u] < $ key $= i$, which is the stale test of lazy-deletion Dijkstra. Lines L8 to L10 relax the edges out of $u$ with $d[u] = i$. So the sequence of scanned vertices and label changes is that of Dijkstra's algorithm with a lazy-deletion priority queue, with ties among equal keys broken by the order inside a bucket.

**Step 4: correctness.** Dijkstra's algorithm with lazy deletion, with any tie-breaking, ends with $d[v] = \delta(s, v)$ and a shortest-path tree in $\pi$ when all weights are nonnegative; see the proof on [the correctness of Dijkstra's algorithm](/dijkstra-correctness/). For completeness, the core of it in this setting: when $u$ is scanned at index $i = d[u]$, suppose $\delta(s, u) < i$, and let $P$ be a shortest path to $u$. Its first vertex $y$ not yet scanned has a scanned predecessor $x$ (or is $s$), and the relaxation of $(x, y)$ when $x$ was scanned gave $d[y] \le \delta(s, x) + w(x, y) = \delta(s, y)$ by induction on scan order. So an entry with key at most $\delta(s, y) \le \delta(s, u) < i$ is in the buckets, against Step 1. Hence $d[u] = \delta(s, u)$ when scanned. Unscanned vertices at the end have no entry; a reachable vertex gets an entry when its predecessor on a shortest path is scanned, so every reachable vertex is scanned, and an unreachable vertex keeps $\infty$, since every finite label is the weight of a walk from $s$. When $d[v]$ was last set, it was $d[\pi[v]] + w(\pi[v], v)$ with $d[\pi[v]]$ already final, which gives the tree equation. $\blacksquare$
