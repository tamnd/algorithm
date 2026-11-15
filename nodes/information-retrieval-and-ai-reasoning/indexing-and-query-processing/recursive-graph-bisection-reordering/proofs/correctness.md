---
title: Recursive graph bisection ends and returns a permutation of the documents
proves: [correctness]
status: full
---

Let $D$ be a list of $n$ distinct documents, each a set of terms, and let the parameters be an iteration limit $I \ge 0$, a leaf size $L \ge 1$ and a depth limit. The claim is that $\text{BP}(D)$ ends and returns a list that holds each document of $D$ exactly once. The claim says nothing about the cost of the order. The method is a heuristic, and the last paragraph explains why no step of it gives a bound on the cost.

1. **One iteration keeps $A$ and $B$ a balanced split of $D$.** Line L2 sets $A$ to the first $\lceil |D|/2 \rceil$ documents of $D$ and $B$ to the rest, so $A$ and $B$ are disjoint and their union is $D$. Lines L4 to L6 only read $A$ and $B$. Line L7 reorders each list, which changes neither its set nor its size. Line L10 exchanges $A[i]$ and $B[i]$ for $i < k$, with $k \le \min(|A|, |B|)$. Each such step moves one document from $A$ to $B$ and one from $B$ to $A$. So after line L10, $A$ and $B$ are again disjoint, their union is still $D$, and $|A| = \lceil |D|/2 \rceil$ and $|B| = \lfloor |D|/2 \rfloor$ as before. By induction on the number of iterations, this holds when the loop of line L3 ends.

2. **The loop of line L3 ends.** It runs at most $I$ times. Each run of lines L4 to L10 does a finite amount of work: one pass over the terms of each document, two sorts and at most $\min(|A|, |B|)$ exchanges. Line L9 may stop it sooner.

3. **The recursion ends.** If line L1 does not return, then $|D| > L \ge 1$, so $|D| \ge 2$. Then $1 \le \lfloor |D|/2 \rfloor \le \lceil |D|/2 \rceil < |D|$, and by step 1 both calls of line L11 get a list strictly shorter than $D$. The length cannot drop below 0, so every chain of calls ends at line L1.

4. **The output is a permutation of $D$.** By strong induction on $|D|$. If line L1 returns, the output is $D$ itself. Otherwise, by step 3 and the hypothesis, $\text{BP}(A)$ is a permutation of $A$ and $\text{BP}(B)$ is a permutation of $B$. Line L11 returns their concatenation. By step 1, $A$ and $B$ are disjoint with union $D$, so each document of $D$ occurs in exactly one of the two parts, exactly once. $\blacksquare$

**What the gains mean.** For a term $t$ with $a_t$ documents in $A$ and $b_t$ in $B$, the estimate $c(a_t, b_t) = a_t \lg(|A|/(a_t+1)) + b_t \lg(|B|/(b_t+1))$ is the bit cost of the gaps of $t$ if its documents were spread evenly in each half. Line L5 computes, for $v$ in $A$, the drop in $\sum_t c(a_t, b_t)$ if $v$ alone moved to $B$, and line L6 does the same for $v$ in $B$. These are exact for one move against the current degrees. Line L10 then makes $k$ exchanges at once, and each exchange changes the degrees that the other gains assumed. So the total change of the estimate is not the sum of the gains, and the estimate can go up in an iteration. If all $k$ pairs are exchanged and $k = |A| = |B|$, the two halves simply trade places, which leaves the split the same. Also, the estimate is not the true log-gap cost of the final order, which depends on the order inside each half and on the levels below. For these reasons the method has no approximation guarantee. The tests measure its effect: it lowers the cost on collections with planted topics, and it raises the cost on the toy collection and on some random inputs.
