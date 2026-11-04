---
title: Coalesced hashing keeps its chains and implements insert and search
proves: [correctness, termination]
status: full
---

A slot $i$ is **occupied** when $\mathit{key}[i] \ne$ EMPTY. Write $i \to j$ when $\mathit{next}[i] = j$. The invariant is:

- **(C1)** for each occupied slot $s$ with key $k$, the slot $h(k)$ is occupied, and $s$ is reached from $h(k)$ by a path $h(k) = s_0 \to s_1 \to \cdots \to s_t = s$ with $t \ge 0$;
- **(C2)** if $i \to j$, then $i$ and $j$ are occupied; each slot has at most one incoming link; and there is no cycle $i_0 \to i_1 \to \cdots \to i_0$;
- **(C3)** no key is in two slots;
- **(C4)** each slot $i$ with $r \le i \le m - 1$ is occupied, and $0 \le r \le m$.

**Lemma (walks end).** Under (C2), the walk $i, \mathit{next}[i], \mathit{next}[\mathit{next}[i]], \ldots$ from an occupied slot reaches a slot with $\mathit{next} = $ NIL after at most $n - 1$ steps, and it visits no slot twice.

*Proof.* Each slot of the walk is occupied by (C2). If the walk visited a slot twice, the part between the two visits would be a cycle, which (C2) forbids. So it visits distinct occupied slots, at most $n$ of them, and it can only stop at a NIL link. $\square$

**Theorem.** Start from the table with all slots EMPTY, all links NIL and $r = m$, and apply any sequence of COALESCED-INSERT and COALESCED-SEARCH. Each call terminates. After each call (C1) to (C4) hold, and the set of stored pairs is the map that the same sequence gives on an abstract dictionary, except that an insert of a new key into a full table reports an error and changes nothing. Each search returns the value of its key, or NIL if the key is absent.

*Proof.* At the start no slot is occupied and $r = m$, so the invariant holds. Assume it before a call on key $k$, and let $i_0 = h(k)$.

**Search.** If slot $i_0$ is EMPTY, then by (C1) no stored key has home $i_0$, so $k$ is absent and line L12 is right. Otherwise lines L13 to L15 walk from $i_0$, and by the lemma the walk ends after at most $n$ slots. If $k$ is stored, then by (C1) its slot is on the path from $i_0$, and since each slot has at most one outgoing link this path is a prefix of the walk, so line L14 finds it; by (C3) the value is the value of $k$. If the walk ends without $k$, then $k$ is absent and line L16 is right. Search changes nothing.

**Insert, home slot free.** If slot $i_0$ is EMPTY, line L2 stores $(k, v)$ there with a NIL link. By (C1) no stored key had home $i_0$, so in particular $k$ was absent and (C3) holds. (C1) holds for $k$ with $t = 0$, and for the other keys their paths did not change. The new slot has no links, so (C2) holds. (C4) holds: a slot was filled and $r$ did not change.

**Insert, home slot occupied.** Lines L3 to L6 walk from $i_0$; the walk ends by the lemma. As in the search, if $k$ is stored, line L4 finds it and only its value changes, so the invariant holds. Otherwise $k$ is absent, and the walk stops at the last slot $i$ of the walk, with $\mathit{next}[i] = $ NIL.

Line L7 lowers $r$ by at least 1 and stops at the first EMPTY slot below the old $r$, or at $r < 0$. The slots it passes over are occupied, so (C4) holds for the new $r$ as long as $r \ge 0$. If $r < 0$, every slot is occupied by (C4) and the passes of line L7, so the table is full, $k$ is absent, and line L8 reports it. (The program then sets $r = 0$, which keeps (C4).)

Else slot $r$ is EMPTY. By (C2) it has no incoming link (only occupied slots have links, and links point to occupied slots) and its own link is NIL. Line L9 sets $i \to r$, and line L10 stores $(k, v)$ in slot $r$ with a NIL link. Then:

- (C1) holds for $k$, by the path from $i_0$ to $i$ followed by $i \to r$. It holds for each other key, because no old link changed except $\mathit{next}[i]$, which was NIL and so was the end of each path through $i$.
- (C2) holds. Both ends of the new link are occupied. Slot $r$ had no incoming link, so it now has one. No cycle appears: a cycle through the new link would need a path from $r$ back to $i$, but $\mathit{next}[r] = $ NIL.
- (C3) holds since $k$ was absent.
- (C4) holds since slot $r$ is now occupied.

The stored map gains exactly $(k, v)$.

**Termination.** Each walk ends by the lemma. The loop of line L7 lowers $r$ by 1 at each pass and stops at $r < 0$ at the latest, so it ends after at most $m + 1$ passes.

By induction on the number of calls, the theorem holds. $\blacksquare$
