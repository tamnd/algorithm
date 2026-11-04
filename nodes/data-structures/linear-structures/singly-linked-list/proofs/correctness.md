---
title: The operations of a singly linked list keep its invariant and are correct
proves: [correctness]
status: full
---

We write $\sigma(L) = \langle x_1.key, \dots, x_n.key \rangle$ for the sequence that the list represents when the invariant (I) holds with the nodes $x_1, \dots, x_n$.

> **(I)** There are $n = L.n$ distinct nodes $x_1, \dots, x_n$ with $L.head = x_1$, $x_i.next = x_{i+1}$ for $1 \le i < n$ and $x_n.next = \text{NIL}$. If $n \ge 1$ then $L.tail = x_n$. If $n = 0$ then $L.head = L.tail = \text{NIL}$.

A new node is distinct from each node of the list, because lines L1, L6 and A1 make it fresh. Each operation below starts in a state where (I) holds.

**The empty list.** A list with $L.head = L.tail = \text{NIL}$ and $L.n = 0$ meets (I) with no nodes, and $\sigma(L) = \langle \rangle$.

**Lemma 1 (PUSH-FRONT).** After PUSH-FRONT$(L, k)$, (I) holds and $\sigma(L) = \langle k \rangle \cdot \sigma_0$, where $\sigma_0$ is the sequence before the call.

*Proof.* Let $x_0$ be the new node, with key $k$. Line L2 sets $x_0.next = x_1$ if $n \ge 1$, and NIL if $n = 0$. Line L3 sets $L.head = x_0$. No other link changes, so the chain is $x_0, x_1, \dots, x_n$, of $n + 1$ distinct nodes, ending in NIL. If $n \ge 1$, then $L.tail = x_n$ was not NIL, line L4 does nothing, and the tail is still the last node. If $n = 0$, then $L.tail = \text{NIL}$ and line L4 sets it to $x_0$, the only node. Line L5 makes the count $n + 1$. $\square$

**Lemma 2 (PUSH-BACK).** After PUSH-BACK$(L, k)$, (I) holds and $\sigma(L) = \sigma_0 \cdot \langle k \rangle$.

*Proof.* Let $x_{n+1}$ be the new node; line L6 gives it key $k$ and next NIL. If $n = 0$, line L7 sets $L.head = x_{n+1}$, so the chain is the single node. If $n \ge 1$, then $L.tail = x_n$ by (I), and line L8 sets $x_n.next = x_{n+1}$, which extends the chain $x_1, \dots, x_n$ by one node. In both cases line L9 makes the new node the tail and line L10 the count $n + 1$. $\square$

**Lemma 3 (POP-FRONT).** If $n \ge 1$, then POP-FRONT$(L)$ returns $x_1.key$, and afterwards (I) holds and $\sigma(L) = \langle x_2.key, \dots, x_n.key \rangle$.

*Proof.* Line L11 sets $x = x_1$ and line L12 sets $L.head = x_1.next$, which is $x_2$ if $n \ge 2$ and NIL if $n = 1$. No other link changes, so the chain from the head is $x_2, \dots, x_n$. If $n \ge 2$ the head is not NIL, line L13 does nothing, and $L.tail = x_n$ is still the last node. If $n = 1$ the head is NIL, and line L13 sets the tail to NIL. Line L14 makes the count $n - 1$, and line L15 returns $x_1.key$. $\square$

**Lemma 4 (SEARCH).** SEARCH$(L, k)$ returns the node $x_i$ with the least $i$ such that $x_i.key = k$, or NIL if there is none.

*Proof.* We use this invariant of the loop of line S2: $x = x_j$ for some $j$ with $1 \le j \le n + 1$, where $x_{n+1}$ means NIL, and no node $x_t$ with $t < j$ has key $k$. Line S1 sets $x = x_1$ (or NIL, which is $x_1$ when $n = 0$), with no earlier node, so the invariant holds. If the loop body runs, then $x = x_j \ne \text{NIL}$ and $x_j.key \ne k$, and line S3 moves to $x_{j+1}$, so the invariant holds for $j + 1$. The index $j$ grows by exactly 1 in each pass and cannot pass $n + 1$, because at $x_{n+1} = \text{NIL}$ the test fails. So the loop stops after at most $n$ passes. When it stops, either $x = \text{NIL}$, and by the invariant no node has key $k$, or $x = x_j$ with $x_j.key = k$ and no earlier match. Line S4 returns $x$. $\square$

**Lemma 5 (INSERT-AFTER).** If $y = x_i$ is a node of $L$, then after INSERT-AFTER$(L, y, k)$, (I) holds and $\sigma(L) = \langle x_1.key, \dots, x_i.key, k, x_{i+1}.key, \dots, x_n.key \rangle$.

*Proof.* Let $z$ be the new node with key $k$. Line A2 sets $z.next = x_i.next$, which is $x_{i+1}$, or NIL if $i = n$. Line A3 sets $x_i.next = z$. No other link changes, so the chain is $x_1, \dots, x_i, z, x_{i+1}, \dots, x_n$, of $n + 1$ distinct nodes, ending in NIL. If $i = n$, then $L.tail = x_n = y$ and line A4 makes $z$, the new last node, the tail. If $i < n$, the tail $x_n$ is still the last node and line A4 does nothing. Line A5 makes the count $n + 1$. $\square$

**Lemma 6 (DELETE).** DELETE$(L, k)$ returns false and changes nothing if no node has key $k$. Otherwise, let $x_i$ be the first node with key $k$; it returns true, and afterwards (I) holds and $\sigma(L)$ is $\sigma_0$ with its $i$-th item removed.

*Proof.* The loop of lines D2 and D3 is the loop of SEARCH, with one more variable. It keeps the invariant of Lemma 4 and also: $prev = x_{j-1}$ if $j \ge 2$, and $prev = \text{NIL}$ if $j = 1$. Line D1 makes this true for $j = 1$, and line D3 sets $prev$ to the old $x = x_j$ when $x$ moves to $x_{j+1}$. By Lemma 4, the loop stops at the first node with key $k$, or at NIL.

If it stops at NIL, line D4 returns false, and no field was written.

Else $x = x_i$. If $i = 1$, then $prev = \text{NIL}$, and line D5 sets $L.head = x_1.next$, the node $x_2$ or NIL. If $i \ge 2$, then $prev = x_{i-1}$, and line D5 sets $x_{i-1}.next = x_i.next$, which is $x_{i+1}$ or NIL. In both cases, the chain from the head is $x_1, \dots, x_{i-1}, x_{i+1}, \dots, x_n$, of $n - 1$ distinct nodes, and it ends in NIL. For the tail: if $i = n$, then $L.tail = x_n = x$, and line D6 sets the tail to $prev$, which is $x_{n-1}$, the new last node, or NIL when $n = 1$ and the list is now empty. If $i < n$, then $L.tail = x_n \ne x$ and is still the last node. Line D7 makes the count $n - 1$, and line D8 returns true. $\square$

**Theorem.** Starting from the empty list, after each finite sequence of the operations PUSH-FRONT, PUSH-BACK, POP-FRONT on a nonempty list, SEARCH, INSERT-AFTER on a node of the list, and DELETE, the invariant (I) holds, and the list represents the sequence that the same operations give on the abstract type, and each result is the one that the abstract type gives.

*Proof.* By induction on the number of operations. The empty list meets (I) and represents $\langle \rangle$. If (I) holds and the list represents the right sequence before an operation, then Lemmas 1 to 6 show that (I) holds after it, that the new sequence is the one the abstract operation gives, and that the result is correct. SEARCH changes no field, so it keeps (I) trivially. $\blacksquare$

**Cost.** Lines L1 to L15 and A1 to A5 have no loop, so each of PUSH-FRONT, PUSH-BACK, POP-FRONT and INSERT-AFTER takes $\Theta(1)$ time. By the proof of Lemma 4, the loop of SEARCH, and the same loop in DELETE, makes at most $n$ passes, and exactly $n$ on a miss, so each takes $\Theta(n)$ time in the worst case.
