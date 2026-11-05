---
title: The direct-address table and its sparse version implement a dictionary
proves: [correctness]
status: full
---

**Theorem 1 (plain table).** Start from the table with $A[k] = \text{NIL}$ for all $0 \le k < u$ and $n = 0$, and apply any sequence of DA-SEARCH, DA-INSERT and DA-DELETE with keys in $\{0, \ldots, u - 1\}$ and values other than NIL. After each operation the invariant holds:

- **(D1)** $D = \{(k, A[k]) : A[k] \ne \text{NIL}\}$ is the map that the same sequence gives on an abstract dictionary;
- **(D2)** $n = |\{k : A[k] \ne \text{NIL}\}|$.

Each search returns the value of its key in that map, or NIL.

*Proof.* At the start every slot is NIL, $D$ is the empty map and $n = 0$, so (D1) and (D2) hold. Assume they hold before an operation on key $k$, and let $D$ be the map at that time.

*Search.* Line L1 returns $A[k]$. If $k$ is a key of $D$, then $A[k] = D(k)$ by (D1). If not, then no pair of $D$ has key $k$, so $A[k] = \text{NIL}$ by (D1). No field changes.

*Insert.* Only slot $k$ and $n$ change. Line L3 sets $A[k] = v \ne \text{NIL}$, so the new set of pairs is $D$ with the pair of $k$ removed and $(k, v)$ added, which is the dictionary insert. If $A[k]$ was NIL, the number of slots that are not NIL grows by one, and line L2 adds one to $n$. If $A[k]$ was not NIL, that number does not change, and line L2 does not change $n$. So (D2) holds.

*Delete.* Only slot $k$ and $n$ change. Line L5 sets $A[k] = \text{NIL}$, so the new set of pairs is $D$ without the pair of $k$, if there was one, which is the dictionary delete. Line L4 lowers $n$ by one exactly when the slot was not NIL before, which is exactly when the number of slots that are not NIL drops by one. So (D2) holds.

By induction on the number of operations, the claim holds after each one. $\blacksquare$

**Theorem 2 (sparse version).** Let the arrays $\mathit{val}$, $\mathit{idx}$ and $\mathit{key}$ have arbitrary contents at creation, and let $t = 0$. Apply any sequence of SP-SEARCH, SP-INSERT and SP-DELETE with keys in $\{0, \ldots, u - 1\}$. Let $S$ be the set of keys of the abstract dictionary after the same sequence, with values $D(k)$. After each operation:

- **(S1)** $\mathit{key}[0], \ldots, \mathit{key}[t - 1]$ are distinct, and $\{\mathit{key}[0], \ldots, \mathit{key}[t - 1]\} = S$;
- **(S2)** $\mathit{idx}[\mathit{key}[i]] = i$ for each $0 \le i < t$;
- **(S3)** $\mathit{val}[k] = D(k)$ for each $k \in S$.

Moreover, under (S1) and (S2), VALID$(k)$ is true if and only if $k \in S$, whatever the contents of the slots that were never written. So each search returns $D(k)$ or NIL.

*Proof.* First the claim on VALID. Assume (S1) and (S2). If $k \in S$, then by (S1) $k = \mathit{key}[i]$ for some $i < t$, and by (S2) $\mathit{idx}[k] = i$. So line L6 reads $i$ and line L7 finds $0 \le i < t$ and $\mathit{key}[i] = k$, and returns true. Conversely, if line L7 returns true, then $i = \mathit{idx}[k]$ satisfies $0 \le i < t$ and $\mathit{key}[i] = k$, so $k \in S$ by (S1). This argument uses only the slots $\mathit{key}[0 \ldots t-1]$, which (S1) describes, and not the content of $\mathit{idx}[k]$ beyond the value read, so garbage cannot make VALID true for a key outside $S$.

At creation $t = 0$ and $S = \emptyset$, so (S1) to (S3) hold, the last two vacuously. Assume they hold before an operation on key $k$.

*Search.* By the claim, line L8 returns $\mathit{val}[k] = D(k)$ by (S3) when $k \in S$, and NIL otherwise. No field changes.

*Insert, $k \in S$.* VALID is true, so line L10 is skipped, and line L11 sets $\mathit{val}[k] = v$. The set $S$ does not change and the new value of $k$ is $v$, so (S1) to (S3) hold.

*Insert, $k \notin S$.* Line L10 writes $\mathit{key}[t] = k$ and $\mathit{idx}[k] = t$, then raises $t$ by one. Since $k \notin S$, the keys $\mathit{key}[0 \ldots t]$ are distinct and form $S \cup \{k\}$, which is (S1). For $i < t$ the old relation $\mathit{idx}[\mathit{key}[i]] = i$ still holds, since the only slot of $\mathit{idx}$ that changed is $\mathit{idx}[k]$, and $k$ differs from each $\mathit{key}[i]$ with $i < t$. Together with $\mathit{idx}[k] = t$ this gives (S2). Line L11 sets $\mathit{val}[k] = v$, and the other values are unchanged, so (S3) holds. The stack never overflows: by (S1), $t = |S| \le u$.

*Delete, $k \notin S$.* VALID is false and nothing changes, which is the dictionary delete of an absent key.

*Delete, $k \in S$.* Let $i = \mathit{idx}[k]$, so $\mathit{key}[i] = k$ by (S2), and let $j = \mathit{key}[t - 1]$. Line L14 sets $\mathit{key}[i] = j$ and $\mathit{idx}[j] = i$ and lowers $t$ by one. If $i = t - 1$, then $j = k$, and the effect is to drop the last stack entry, which is $k$. If $i < t - 1$, the entry $k$ at position $i$ is replaced by the last entry $j$, and the last position leaves the used part. In both cases $\mathit{key}[0 \ldots t-2]$ holds the old keys without $k$, each once, which is (S1) for $S \setminus \{k\}$. For (S2), every key other than $j$ keeps its position and its slot of $\mathit{idx}$, and $j$, if it is still stored, is now at position $i$ with $\mathit{idx}[j] = i$. The values of the other keys are unchanged, so (S3) holds.

By induction on the number of operations, (S1) to (S3) hold after each one, and with the claim on VALID each operation answers as the dictionary does. $\blacksquare$
