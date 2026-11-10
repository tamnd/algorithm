---
title: Gather, scatter and permute compute their definitions in one PRAM step
proves: [correctness]
status: full
---

**Statement.** Let $A[0 \ldots n-1]$ be an array, $I[0 \ldots n-1]$ an array of indices, and $C[0 \ldots m-1]$ an output array, with $0 \le I[i] < m$ (for a gather, $0 \le I[i] < |A|$). Run GATHER and SCATTER as one synchronous PRAM step, in which every processor does its reads before any processor writes.

1. GATHER returns $B$ with $B[i] = A[I[i]]$ for every $i$. It needs concurrent reads only when $I$ has repeated entries.
2. If the entries of $I$ are distinct, SCATTER returns $C'$ with $C'[I[i]] = A[i]$ for every $i$ and $C'[j] = C[j]$ for every $j$ that is not in $I$. This result is the same as that of the serial loop over $i$ in any order, the step is exclusive read and exclusive write, and every CRCW rule gives the same result.
3. If $P$ is a permutation of $0, \ldots, n-1$, then $D = \mathrm{PERMUTE}(A, P)$ is a rearrangement of $A$ with $D[P[i]] = A[i]$, and GATHER$(D, P) = A$. The inverse permutation $Q$, with $Q[P[i]] = i$, is SCATTER$(0 \ldots n-1, P)$, and $D = $ GATHER$(A, Q)$.
4. With repeated indices, the priority rule gives the same result as the serial loop for $i = n-1$ down to $0$. The combining rule with an operator $\otimes$ that is associative and commutative gives $C'[j] = C[j] \otimes \bigotimes_{i : I[i] = j} A[i]$, the same as the serial loop in any order.
5. Each of the operations takes $O(1)$ time with $n$ processors, so $\Theta(n)$ work.

## 1. Gather

Processor $i$ reads $I[i]$, then $A[I[i]]$, and writes $B[i]$. The cells $B[i]$ are distinct for distinct $i$, so the writes never conflict, and $B[i] = A[I[i]]$. The reads of $I$ are exclusive. The reads of $A$ are exclusive if and only if the values $I[i]$ are distinct; otherwise two processors read one cell in the same step, which a CREW PRAM allows and an EREW PRAM does not.

## 2. Scatter with distinct indices

Processor $i$ reads $A[i]$ and $I[i]$, which are cells that no other processor reads, and writes cell $I[i]$ of the output. Because the values $I[i]$ are distinct, each output cell has at most one writer, so the step is exclusive write, and no rule for concurrent writes is ever applied. That is why all rules give the same result. After the step, $C'[I[i]] = A[i]$, since processor $i$ is the only writer of that cell, and every other cell keeps its old value, since nobody writes it.

For the serial loop, the iteration for $i$ writes only cell $I[i]$ and reads only $A[i]$ and $I[i]$, which no iteration writes. So the iterations do not interact, and each order of them leaves the same final array, the one above.

## 3. Permute and its inverse

If $P$ is a permutation, its entries are distinct, so part 2 applies with $m = n$: $D[P[i]] = A[i]$ for every $i$. Since $P$ is onto, every cell of $D$ is written, so $D$ holds each item of $A$ exactly once. Then GATHER$(D, P)$ has entry $i$ equal to $D[P[i]] = A[i]$ by part 1. Scattering the values $0, \ldots, n-1$ by $P$ gives $Q$ with $Q[P[i]] = i$, which is the inverse of $P$. Finally, GATHER$(A, Q)$ has entry $P[i]$ equal to $A[Q[P[i]]] = A[i] = D[P[i]]$, and as $i$ runs over $0, \ldots, n-1$ so does $P[i]$, so GATHER$(A, Q) = D$.

## 4. Repeated indices

For a cell $j$, let $W_j = \{ i : I[i] = j \}$ be its writers. Cells with $W_j$ empty keep their value under every rule, and in the serial loops.

- **Priority.** The rule stores $A[\min W_j]$. In the serial loop that runs $i$ from $n-1$ down to $0$, the last write to cell $j$ is by the smallest $i$ in $W_j$, so the loop also leaves $A[\min W_j]$.
- **Combining.** The rule stores $C[j] \otimes \bigotimes_{i \in W_j} A[i]$. Because $\otimes$ is associative and commutative, this value does not depend on the order or the grouping of the operands. The serial loop that does $C[I[i]] \gets C[I[i]] \otimes A[i]$ applies $\otimes$ to $C[j]$ and to each $A[i]$ with $i \in W_j$ once, in some order, so it gives the same value.
- **Common and arbitrary.** The common rule requires all $A[i]$ with $i \in W_j$ to be equal, and then stores that value. The arbitrary rule stores $A[i]$ for some $i \in W_j$, so a correct program must work for every choice.

## 5. Cost

Each processor does a constant number of reads, one operation and one write, so each operation is one PRAM step of $O(1)$ time with $n$ processors, and the work is $n \cdot O(1) = \Theta(n)$. Every item must be read or written once, so the work is also $\Omega(n)$. $\blacksquare$
