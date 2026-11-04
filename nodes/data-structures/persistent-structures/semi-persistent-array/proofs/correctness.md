---
title: The semi-persistent array gives each valid version its contents
proves: [correctness]
status: full
---

**Setting.** A *state* is a shared array $A$ of $n$ slots together with version records. The abstract model gives each version $v$ ever made a fixed sequence $\text{cont}(v)$ of $n$ values: the first version has the initial contents, and the version returned by SET$(v, i, x)$ has $\text{cont}(v)$ with slot $i$ set to $x$. The state is *good* if there are versions $v_0, \ldots, v_k$ such that:

- (I1) $v_k$ has kind arr, and each $v_j$ with $j < k$ has kind $\text{diff}(i_j, x_j, v_{j+1})$;
- (I2) $A = \text{cont}(v_k)$, and for $j < k$, $\text{cont}(v_j)$ equals $\text{cont}(v_{j+1})$ with slot $i_j$ set to $x_j$;
- (I3) every other version made so far has kind dead.

The valid versions are $v_0, \ldots, v_k$.

**Lemma 1 (get).** In a good state, GET$(v_j, i)$ returns slot $i$ of $\text{cont}(v_j)$, and changes nothing.

*Proof.* GET visits $v_j, v_{j+1}, \ldots$ in order. Let $l \ge j$ be the first index with $l < k$ and $i_l = i$, if there is one. For $j \le p < l$, (I2) gives slot $i$ of $\text{cont}(v_p)$ equal to slot $i$ of $\text{cont}(v_{p+1})$, since $i_p \ne i$. So slot $i$ of $\text{cont}(v_j)$ equals slot $i$ of $\text{cont}(v_l)$, which is $x_l$ by (I2), and that is what line L4 returns. If there is no such $l$, the same argument up to $v_k$ gives slot $i$ of $\text{cont}(v_k) = A[i]$, which line L6 returns. GET writes nothing. $\square$

**Lemma 2 (reroot).** In a good state, REROOT$(v_j)$ leaves a good state with valid versions $v_0, \ldots, v_j$.

*Proof.* Line L12 collects $t_p = v_{j + p}$ for $p = 0, \ldots, m$ with $m = k - j$, by (I1). We claim that after line L13 has processed $t_{m-1}, \ldots, t_l$, the array is $\text{cont}(v_{j + l})$. Before the loop it is $\text{cont}(v_k)$ by (I2). The step for $t_{l}$ sets $A[i_{j+l}] \gets x_{j+l}$, which turns $\text{cont}(v_{j+l+1})$ into $\text{cont}(v_{j+l})$ by (I2). After the loop, $A = \text{cont}(v_j)$. Line L14 marks $v_{j+1}, \ldots, v_k$ dead, and line L15 makes $v_j$ of kind arr. Now (I1) holds for $v_0, \ldots, v_j$ (the diffs of $v_0, \ldots, v_{j-1}$ are untouched), (I2) holds because $A = \text{cont}(v_j)$ and the earlier diffs are unchanged, and (I3) holds because the versions removed from the path are dead. $\square$

**Lemma 3 (set).** In a good state, SET$(v_j, i, x)$ returns a new version $w$ with $\text{cont}(w)$ equal to $\text{cont}(v_j)$ with slot $i$ set to $x$, and leaves a good state with valid versions $v_0, \ldots, v_j, w$.

*Proof.* By Lemma 2, after line L7 the state is good with $v_j$ newest and $A = \text{cont}(v_j)$. Line L8 makes $w$ of kind arr. Line L9 sets $v_j$ to $\text{diff}(i, A[i], w)$, with $A[i]$ read before the write, and line L10 sets $A[i] \gets x$. Now $A = \text{cont}(w)$, and $\text{cont}(v_j)$ equals $\text{cont}(w)$ with slot $i$ set to the old $A[i]$, which is (I2) for the pair $v_j, w$. (I1) and (I3) are clear. $\square$

**Theorem.** After any sequence of operations, the state is good; each GET or TO-LIST on a valid version returns its contents in the model; each operation on a version that is not valid is rejected; and the contents of a valid version never change.

*Proof.* The first version alone is a good state with $k = 0$. By Lemmas 1 to 3 every operation keeps the state good and returns the right answer. TO-LIST copies $A = \text{cont}(v_k)$ and applies the diffs from $v_{k-1}$ back to $v_j$, which yields $\text{cont}(v_j)$ by the argument of Lemma 2 applied to a copy. A version that is not valid has kind dead by (I3), and lines L1 and L11 reject it. Finally, $\text{cont}$ of a version is fixed by the model, and the good state represents it exactly for each valid version, so a valid version is never seen to change. $\blacksquare$
