---
title: Each operation of the clause database keeps the array parseable, the watch lists exact and the waste count right, and garbage collection relocates the live clauses without change
proves: [correctness]
status: full
---

We use the operations of the page. The array $A$ holds records. A record at index $r$ is a header $A[r] = k$ (the size, $k \ge 2$), $A[r+1]$ (the flags) and $A[r+2]$ (the LBD), followed by the literals $A[r+3], \ldots, A[r+2+k]$. A record is *live* when its deleted flag is clear. For a literal $\ell$, $W[\ell]$ is its watch list. We prove that the following invariant holds after every operation.

**Invariant.**

- (A) The records tile $A$: starting at index 0 and stepping from $r$ to $r + 3 + A[r]$ visits exactly the record indices and ends at $|A|$.
- (W) For each literal $\ell$, the live entries of $W[\ell]$ are distinct, and they are exactly the live records whose literal at position 0 or 1 is $\ell$. Every entry of $W[\ell]$ is a record index.
- (V) The counter `wasted` is the sum of $3 + k$ over the deleted records.

All three hold for the empty database.

**Lemma 1 (add).** ADD keeps the invariant, and the new record holds the clause with the given flags and LBD.

*Proof.* Line L1 takes $r = |A|$, which is where the walk of (A) ends, and line L2 appends a record there, so (A) holds with one more record. The new record is live. Line L3 appends $r$ to the lists of its literals at positions 0 and 1. These are different literals, because the clause has distinct variables, so $r$ appears once in each list and in no other list, and (W) holds. No record is deleted, so (V) holds. $\square$

**Lemma 2 (delete).** DELETE keeps the invariant and changes no live record.

*Proof.* Line L5 sets the flag of a live record $r$. The array keeps its length and headers, so (A) holds. The record $r$ is no longer live, and (W) speaks only of live entries and live records, so removing $r$ from both sides keeps it. Line L6 adds $3 + k$ for the newly deleted record, so (V) holds. $\square$

**Lemma 3 (swap watch).** SWAP-WATCH$(r, i, k)$ with $i \in \{0, 1\}$ and $2 \le k < A[r]$ keeps the invariant, and the record holds the same set of literals.

*Proof.* Line L7 swaps two literals inside record $r$, so (A), (V) and the set of literals hold. Let $u$ be the old literal at position $i$ and $v$ the old literal at position $k$. The literals at positions 0 and 1 of $r$ change from $u$ and $w$ to $v$ and $w$, where $w$ is the literal at the other watched position, and $w \ne u$ and $w \ne v$ because the variables are distinct. By (W) before the step, $r$ is in $W[u]$ once and not in $W[v]$. Line L8 removes it from $W[u]$ and appends it to $W[v]$. So afterwards $r$ is once in $W[v]$ and $W[w]$ and in no other list, which is (W) for the record $r$. Other records do not change. $\square$

**Lemma 4 (garbage collection).** COLLECT keeps the invariant with `wasted` $= 0$, it returns a map $M$ that is defined exactly on the live records, and for each live record $r$, the record at $M(r)$ in the new array equals the record at $r$ in the old one. The new array has length $|A| - $ `wasted`.

*Proof.* By (A), the loop of lines L10 and L11 visits each record once, in order. It copies each live record whole and sets $M(r)$ to the index where the copy starts, so the copies tile the new array $A'$ and (A) holds for $A'$, with every record live. Each copy is equal to the original, header and literals. The length of $A'$ is the sum of $3 + k$ over the live records, which is $|A|$ minus the sum over the deleted records, which is `wasted` by (V). Line L12 keeps the entries of $W[\ell]$ that are in the domain of $M$, which are the live entries, and maps them by $M$. Since $M$ is one to one, the entries stay distinct, and since the copies have the same literals at positions 0 and 1, (W) holds for $A'$. Line L13 sets `wasted` to 0, which is (V) for an array with no deleted record. $\blacksquare$

**Theorem.** After any sequence of operations, the live records, read through the maps returned by the collections, are the clauses that were added and not deleted, with the same literal sets, flags and LBD values as the last calls set them, and the watched literals of each such clause are the two literals at its positions 0 and 1.

*Proof.* By induction on the number of operations, using Lemmas 1 to 4. ADD creates the record, DELETE removes it from the live set, SWAP-WATCH and SET-LBD change it only as stated, and COLLECT moves it unchanged to the index given by $M$. Reading operations change nothing. $\blacksquare$

## Cost

ADD writes $3 + k$ ints and two list entries. DELETE writes one flag. SWAP-WATCH does one swap and one removal from a list of length $w$, so $O(w)$; a propagation loop that walks the list avoids this by rewriting the list in place as it goes. COLLECT reads the array once and each watch list once, so it costs $O(|A| + \sum_\ell |W[\ell]|)$. Each record in $A$ has exactly two watch entries, live or not, and at least 5 ints, so $\sum_\ell |W[\ell]| \le 2|A|/5$ and the cost is $O(|A|)$. If the solver collects only when `wasted` is at least half of $|A|$, the array is at most twice the space of the live clauses, and the cost $O(|A|) = O(\text{wasted})$ of a collection is at most a constant times the number of ints freed by the deletions since the previous collection. $\blacksquare$
