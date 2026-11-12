---
title: The LRU cache serves get and put as the LRU rule says
proves: [correctness]
status: full
---

We use the pseudocode of the page. The abstract state is a list $A$ of the stored pairs from the most to the least recently used, with distinct keys and $|A| \le c$. The abstract operations change $A$ as follows.

- get(key) with key in $A$: move its pair to the front of $A$ and return its value. With key not in $A$: return absent, and $A$ is unchanged.
- put(key, v) with key in $A$: replace its value by $v$ and move the pair to the front. With key not in $A$: if $|A| = c$, remove the last pair of $A$; then put (key, v) at the front.

**Invariant (I).** (a) Starting at $S$ and following next pointers, we visit the nodes $x_1, \ldots, x_m$ and return to $S$, and for each node $x$ of the circle, $x.next.prev = x$ and $x.prev.next = x$. (b) The keys of $x_1, \ldots, x_m$ are distinct, $M$ holds exactly these keys, and $M[x_i.key] = x_i$. (c) The pairs $(x_1.key, x_1.value), \ldots, (x_m.key, x_m.value)$ are the list $A$, in order. Since $|A| \le c$, also $m \le c$.

**Two lemmas on the list.** Let (a) hold with the circle $S, x_1, \ldots, x_m, S$.

1. UNLINK($x_i$) gives a circle $S, x_1, \ldots, x_{i-1}, x_{i+1}, \ldots, x_m, S$ that satisfies (a). It writes $x_{i-1}.next = x_{i+1}$ and $x_{i+1}.prev = x_{i-1}$ (with $x_0 = x_{m+1} = S$), which links the two neighbors to each other; no other pointer of a node in the new circle changes.
2. PUSH-FRONT($x$) for a node $x$ that is not in the circle gives the circle $S, x, x_1, \ldots, x_m, S$ that satisfies (a). It sets $x.prev = S$, $x.next = x_1$ (or $S$ if $m = 0$), $x_1.prev = x$ and $S.next = x$.

Both use only a constant number of pointer writes, and the sentinel makes $x_{i-1}$, $x_{i+1}$ and $x_1$ always defined, so there is no special case.

**Initialization.** The empty cache has $S.next = S.prev = S$ and an empty $M$, and $A$ is empty. (I) holds with $m = 0$.

**get.** Assume (I). By (b), line L1 finds the node of key if and only if key is in $A$. If not, line L2 returns absent and nothing changes, as the abstract get says. If yes, $x = x_i$. By lemma 1 and then lemma 2, lines L3 and L4 give the circle $S, x_i, x_1, \ldots, x_{i-1}, x_{i+1}, \ldots, x_m, S$, which is $A$ with the pair of key moved to the front. $M$ does not change and still maps each key to its node. Line L5 returns the value. (I) holds.

**put of a stored key.** Lines L6 to L9 find $x_i$, set its value to $v$, and move it to the front by the two lemmas. This is the abstract put for a stored key. No node is added, so $m$ does not change. (I) holds.

**put of a new key.** Key is not in $M$, so by (b) it is not in $A$.

- If $m = c$, line L11 takes $y = S.prev = x_m$, the last node, whose pair is the last pair of $A$. Line L12 removes it from the circle (lemma 1), and line L13 deletes its key from $M$. Now (a) and (b) hold for $x_1, \ldots, x_{m-1}$, and the list is $A$ without its last pair.
- If $m < c$, nothing is removed.

Lines L14 to L16 make a node for (key, v), put it at the front (lemma 2), and add key to $M$. Key was not stored, so the keys stay distinct, and (b) holds. The list is the abstract result of put. The size is at most $c$, because a node was removed when $m = c$. (I) holds.

**delete.** It removes the node of key from the circle by lemma 1 and the key from $M$. (I) holds with $A$ less that pair.

By induction over the operations, (I) holds after each one, and each return value is the one of the abstract type. So the structure serves each sequence of operations exactly as the LRU rule. $\square$

**Cost.** Each operation does at most one lookup, one deletion and one insertion in $M$, and at most two UNLINK and one PUSH-FRONT, each with a constant number of pointer writes. With a hash table of $O(1)$ expected cost per operation, each operation takes $O(1)$ expected time. The space is one node and one map entry for each stored key, plus the sentinel, so $\Theta(c)$ when the cache is full.
