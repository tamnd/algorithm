---
title: Residual BP stops only at an approximate BP fixed point, and stops on trees
proves: [correctness]
status: full
---

We use the model, the update $F_{i \to j}$ and the pseudocode of the page. Write $D$ for the set of directed edges. For each $e \in D$, $F_e(m)$ depends only on the messages $m_{k \to i}$ with $e = i \to j$ and $k \in N(i) \setminus j$; call these the *inputs* of $e$.

**Lemma 1 (dependence).** The message $m_{i \to j}$ is an input of the edge $e'$ exactly when $e' = j \to k$ with $k \ne i$.

*Proof.* By definition, $m_{a \to b}$ is an input of $b \to c$ for every $c \in N(b) \setminus a$, and of no other edge. Put $a = i$, $b = j$. $\square$

**Lemma 2 (invariant).** Each time line L3 is reached, for every $e \in D$, $c_e = F_e(m)$ and $r_e = \| c_e - m_e \|$, and $Q$ holds exactly one current (not stale) entry for $e$, with key $r_e$.

*Proof.* After line L2 this holds by construction. Assume it holds when line L3 is reached, and the loop body runs with the edge $i \to j$ taken at line L4. If line L5 stops, there is nothing to show. Otherwise line L6 sets $m_{i \to j} = c_{i \to j}$ and $r_{i \to j} = 0$, and pushes a new current entry for $i \to j$. The edge $i \to j$ is not its own input (its inputs end at $i$, and it ends at $j$), so $F_{i \to j}(m)$ is unchanged and equals $c_{i \to j} = m_{i \to j}$; so $r_{i \to j} = 0$ is correct. By Lemma 1, the only other edges whose candidates can change are $j \to k$ with $k \ne i$, and line L7 recomputes their candidates and residuals from the new $m$ and pushes new current entries. For every other edge, neither $m_e$ nor any input of $e$ changed, so $c_e$ and $r_e$ are still correct. Each push increases the version of its edge, so the earlier entry of that edge becomes stale. $\square$

**Theorem 1 (what the stop means).** If the algorithm stops at line L5, every residual is at most $\varepsilon$: $\max_{e \in D} \| F_e(m) - m_e \| \le \varepsilon$. With $\varepsilon = 0$, the messages are a fixed point of loopy BP, and the beliefs are those of that fixed point.

*Proof.* Line L4 skips stale entries, so it returns the current entry of largest key. By Lemma 2 the current entries hold exactly the residuals of all edges, so the key $r$ is the largest residual, and $r \le \varepsilon$ at line L5. By Lemma 2 again, $r_e = \| F_e(m) - m_e \|$. If $\varepsilon = 0$, then $F_e(m) = m_e$ for every $e$, which is the fixed point equation of loopy BP. $\square$

**Theorem 2 (trees).** If $G$ is a tree, $\varepsilon = 0$ and $U = \infty$, the algorithm stops after a finite number of updates, and the beliefs are the exact marginals.

*Proof.* Define the height of a directed edge $i \to j$ as $h(i \to j) = 1 + \max\{h(k \to i) : k \in N(i) \setminus j\}$, with the maximum of the empty set equal to 0. This is finite on a tree, because following the inputs moves away from $j$ along a path that cannot return.

We show by induction on $h$ that each edge of height $h$ is updated only a finite number of times. An edge of height 1 has no inputs, so its candidate never changes; after its first update its residual is 0 for ever (by Lemma 2), and it is never updated again, because an update needs a residual above $\varepsilon = 0$. Let $e$ have height $h > 1$. Its inputs have smaller height, so by induction they change only a finite number of times, say $N$ times in total. Between two changes of the inputs, the candidate $c_e$ is fixed; an update of $e$ sets $m_e = c_e$ and $r_e = 0$, and $r_e$ stays 0 until an input changes. So $e$ is updated at most once between two input changes, and at most $N + 1$ times in all.

So the total number of updates is finite. Every loop iteration either does an update, stops, or removes a stale entry, and the number of entries ever pushed is at most $|D|$ plus $|D|$ per update, which is finite. So the loop ends. If it ends because $Q$ is empty, this cannot happen while current entries exist, and there is always one current entry per edge (Lemma 2); so it ends at line L5. By Theorem 1 the messages are a fixed point of loopy BP. On a tree the fixed point is unique and its beliefs are the exact marginals (proved on the loopy belief propagation page). $\blacksquare$

**Remark.** On a graph with cycles, the loop may not end, and the bound $U$ ends it. Then the output is "not converged", and Theorem 1 does not apply. Theorem 2 needs exact equality of the candidate and the message after an update, which holds in floating point too, because line L6 copies the candidate.
