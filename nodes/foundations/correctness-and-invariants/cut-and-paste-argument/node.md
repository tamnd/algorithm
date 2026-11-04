---
tag: MW4W1A
kind: technique
slug: cut-and-paste-argument
name: Cut-and-paste argument
aliases:
- Cut and paste
area: foundations/correctness-and-invariants
level: intro
summary: Transforms an optimal solution by cutting and reassembling parts to show a structural property.
prereqs: [proof-by-contradiction]
see_also: [optimal-substructure, exchange-argument, greedy-algorithm, activity-selection, single-source-shortest-paths, matrix-chain-multiplication, principle-of-optimality]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 3 (dynamic programming) and Chapter 4 (greedy algorithms)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Sections 14.3 and 15.1, and the introduction of Chapter 22
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Section 4.1 (interval scheduling; the book proves it by greedy stays ahead, a different method) and Section 4.2 (exchange argument)
---

A cut-and-paste argument proves that an optimal solution is built from optimal solutions of smaller subproblems. You assume that one part of an optimal solution is not optimal for its own subproblem. You cut that part out and paste a better one in its place. The new solution is better than the optimal one, which is a contradiction. It is the usual proof of [optimal substructure](/optimal-substructure/), the property that dynamic programming needs, and it is one half of the proof of a [greedy algorithm](/greedy-algorithm/).

## In plain words

Think of a trip from a city to another city by the shortest road. Pick two towns on the road. The part of the trip between these two towns must be a shortest road between them. If it were not, you could take a shorter road between the two towns and keep the rest of the trip. The whole trip would be shorter. But the trip was the shortest one. So the part is also the shortest.

This is the whole argument. You assume a part is not best. You swap in a better part. You check that the new whole is still a valid solution. You see that the whole became better, and this cannot be. The check that the new whole is valid is the step where the argument can go wrong.

## When it applies

Look for these signals.

- The task is to find a solution of least or greatest cost.
- A solution splits into a choice and one or more smaller solutions of the same kind of problem.
- The cost of a solution is built from the costs of its parts in an increasing way. The usual case is a sum.
- A part of one solution can be replaced by another part for the same subproblem, and the new whole is still a solution.

The last signal is the one that fails in practice. It fails when the parts share a resource or must not touch each other. The pitfalls below show an example.

## The template

Let $I$ be an instance, $\mathcal{F}(I)$ the set of feasible solutions and $c$ the cost to minimize. For a maximization problem, reverse the inequalities.

1. **Decomposition.** Name the choice. Write each feasible $X$ as $X = \mathrm{combine}(\mathrm{choice}, X_1, \ldots, X_k)$. Each $X_j$ is a feasible solution of a subinstance $I_j$. Give the cost: $c(X) = g(\mathrm{choice}) + \sum_j c(X_j)$, or another combination that is strictly increasing in each $c(X_j)$.
2. **Claim.** If $X$ is optimal for $I$, then each $X_j$ is optimal for $I_j$.
3. **Assume the opposite.** For some $j$ there is a feasible $Y_j$ for $I_j$ with $c(Y_j) < c(X_j)$.
4. **Paste.** Let $X'$ be $X$ with $X_j$ replaced by $Y_j$.
5. **Feasible.** Show that $X' \in \mathcal{F}(I)$. This is a separate step, with its own argument.
6. **Better.** Show that $c(X') < c(X)$. For a sum, $c(X') = c(X) - c(X_j) + c(Y_j) < c(X)$.
7. **Conclude.** Steps 5 and 6 contradict the optimality of $X$. So each $X_j$ is optimal.

The holes are the decomposition, the subinstances, the cost formula and the proof of step 5. A recurrence that comes from the claim must also list every choice. The claim says what an optimal solution looks like. The list of choices says that the recurrence does not miss one.

## Classic examples

### Shortest paths

Let $G = (V, E)$ be a directed graph with edge weights $w : E \to \mathbb{R}$. A walk is a sequence of vertices $v_0, v_1, \ldots, v_k$ with $(v_{i-1}, v_i) \in E$ for each $i$. Vertices may repeat. Its weight $w(p)$ is the sum of the edge weights. Call a walk from $u$ to $v$ shortest when no walk from $u$ to $v$ has a smaller weight.

**Claim.** Let $p = (v_0, \ldots, v_k)$ be a shortest walk from $v_0$ to $v_k$. For $0 \le i \le j \le k$, the subwalk $p_{ij} = (v_i, \ldots, v_j)$ is a shortest walk from $v_i$ to $v_j$.

**Proof.** Split $p$ into three parts: $p_{0i}$ from $v_0$ to $v_i$, then $p_{ij}$, then $p_{jk}$ from $v_j$ to $v_k$. Then $w(p) = w(p_{0i}) + w(p_{ij}) + w(p_{jk})$. Suppose a walk $q$ from $v_i$ to $v_j$ has $w(q) < w(p_{ij})$. Let $p'$ be $p_{0i}$, then $q$, then $p_{jk}$. It is a walk from $v_0$ to $v_k$: $p_{0i}$ ends at $v_i$ where $q$ starts, and $q$ ends at $v_j$ where $p_{jk}$ starts. Walks may repeat vertices, so no other condition is needed. This is the feasibility step. Its weight is $w(p') = w(p) - w(p_{ij}) + w(q) < w(p)$. This contradicts that $p$ is shortest. So no such $q$ exists. ∎

The claim gives the recurrence of [shortest-path](/single-source-shortest-paths/) algorithms. Let $\delta(s, v)$ be the weight of a shortest walk from $s$ to $v$. Assume that no cycle of negative weight can be reached from $s$.

A shortest walk to every reachable vertex then exists. Deleting a cycle from a walk leaves a walk with the same ends, and its weight does not increase, because the cycle has weight at least 0. So every walk from $s$ to $v$ is at least as heavy as some simple path from $s$ to $v$. There are finitely many simple paths, so one of them has the least weight, and it is a shortest walk.

Let $v \ne s$ be reachable, let $p$ be a shortest walk to $v$ and let $(u, v)$ be its last edge. The prefix of $p$ up to $u$ is a shortest walk to $u$ by the claim, so $\delta(s, v) = \delta(s, u) + w(u, v)$ for this $u$. For every edge $(u', v)$ with $u'$ reachable, appending the edge to a shortest walk to $u'$ gives a walk to $v$, so $\delta(s, v) \le \delta(s, u') + w(u', v)$. Hence

$$ \delta(s, v) = \min_{(u, v) \in E} \bigl( \delta(s, u) + w(u, v) \bigr), $$

where the minimum is over the edges whose tail $u$ is reachable from $s$. If a cycle of negative weight can be reached, going around it again and again gives walks of weight below every bound, no shortest walk exists, and the formula has no meaning (see Exercise 6).

### Activity selection

The input is a set $S$ of activities. Activity $a$ has a start $s(a)$ and a finish $f(a)$ with $s(a) < f(a)$, and it uses the half-open interval $[s(a), f(a))$. Two activities are compatible when their intervals are disjoint. The goal is a compatible subset of $S$ with the most elements. Let $a_1 \in S$ have the least finish time, and let $S' = \{ a \in S : s(a) \ge f(a_1) \}$. Activities are distinct items, even when two have the same times, and two such items are not compatible.

**Lemma 1 (a greedy choice is safe).** Some maximum compatible subset of $S$ contains $a_1$.

**Proof.** Let $A$ be a maximum compatible subset of $S$. It is not empty, because $S$ is not empty and a set of one activity is compatible, since it has no pair to check. Let $b$ be the activity of $A$ with the least finish time. If $b = a_1$, we are done. Otherwise let $A' = (A \setminus \{b\}) \cup \{a_1\}$. We cut $b$ and paste $a_1$. Take $a \in A \setminus \{b\}$. It is compatible with $b$, so $f(a) \le s(b)$ or $f(b) \le s(a)$. The first case gives $f(a) \le s(b) < f(b)$, which contradicts the choice of $b$ as the least finish. So $f(b) \le s(a)$. Because $f(a_1) \le f(b)$, we get $f(a_1) \le s(a)$, and $a$ is compatible with $a_1$. The rest of $A'$ is compatible, since it is a part of $A$. So $A'$ is compatible. Also $a_1 \notin A \setminus \{b\}$, since $a = a_1$ would give $f(a_1) \le s(a_1)$, which is false; so $|A'| = |A|$. It is maximum and contains $a_1$. ∎

**Lemma 2 (optimal substructure).** If $A$ is a maximum compatible subset of $S$ and $a_1 \in A$, then $A \setminus \{a_1\}$ is a maximum compatible subset of $S'$.

**Proof.** First, $A \setminus \{a_1\} \subseteq S'$. Take $a \in A \setminus \{a_1\}$. It is compatible with $a_1$, so $f(a) \le s(a_1)$ or $f(a_1) \le s(a)$. The first case gives $f(a) \le s(a_1) < f(a_1)$, which contradicts that $a_1$ has the least finish time in $S$. So $s(a) \ge f(a_1)$ and $a \in S'$. The set $A \setminus \{a_1\}$ is compatible, as a part of $A$. Now suppose it is not maximum for $S'$. Then there is a compatible $B \subseteq S'$ with $|B| > |A| - 1$. We cut $A \setminus \{a_1\}$ and paste $B$. Each $b \in B$ has $s(b) \ge f(a_1)$, so $b$ is compatible with $a_1$. So $B \cup \{a_1\}$ is compatible (feasibility). Also $a_1 \notin S'$ because $s(a_1) < f(a_1)$, so $a_1 \notin B$ and $|B \cup \{a_1\}| = |B| + 1 > |A|$. This contradicts that $A$ is maximum in $S$. ∎

Lemmas 1 and 2 together give $\mathrm{opt}(S) = 1 + \mathrm{opt}(S')$, where $\mathrm{opt}$ is the maximum size. By Lemma 1, a maximum set $A$ containing $a_1$ exists, and by Lemma 2 its size is $1 + \mathrm{opt}(S')$. Any compatible subset of $S'$ together with $a_1$ is compatible in $S$, so $\mathrm{opt}(S) \ge 1 + \mathrm{opt}(S')$. The greedy algorithm takes $a_1$ and repeats on $S'$. By induction on $|S|$, it returns a compatible subset of $S$ of size $\mathrm{opt}(S)$. Base case: if $S = \emptyset$, the algorithm returns $\emptyset$ and $\mathrm{opt}(\emptyset) = 0$. Otherwise $S$ is not empty, so $a_1$ exists. The induction hypothesis applies to $S'$, which has fewer elements than $S$ because $a_1 \notin S'$: the output for $S'$ is a compatible subset of $S'$ of size $\mathrm{opt}(S')$. Every activity of $S'$ starts at or after $f(a_1)$, so $a_1$ is compatible with all of them. The output for $S$ is therefore a compatible subset of $S$ of size $1 + \mathrm{opt}(S') = \mathrm{opt}(S)$.

For the 11 activities $(1,4)$, $(3,5)$, $(0,6)$, $(5,7)$, $(3,9)$, $(5,9)$, $(6,10)$, $(8,11)$, $(8,12)$, $(2,14)$, $(12,16)$, written as (start, finish), the least finish is $a_1 = (1,4)$. The set $S'$ has the 6 activities that start at 4 or later: $(5,7)$, $(5,9)$, $(6,10)$, $(8,11)$, $(8,12)$, $(12,16)$. Its maximum size is 3, and the maximum for $S$ is 4, as the lemmas say. The greedy choice gives $(1,4)$, $(5,7)$, $(8,11)$, $(12,16)$.

The following program tests $\mathrm{opt}(S) = 1 + \mathrm{opt}(S')$ against brute force on random instances.

```python
import itertools, random

def compatible(c):
    c = sorted(c, key=lambda a: a[1])
    return all(c[i][1] <= c[i + 1][0] for i in range(len(c) - 1))

def best_size(acts):
    for k in range(len(acts), -1, -1):
        if any(compatible(c) for c in itertools.combinations(acts, k)):
            return k

random.seed(1)
for _ in range(300):
    acts = []
    for k in range(random.randint(1, 8)):
        s = random.randint(0, 10)
        acts.append((s, s + random.randint(1, 5), k))   # k is the index, so equal times stay distinct
    a1 = min(acts, key=lambda a: a[1])
    rest = [a for a in acts if a[0] >= a1[1]]
    assert best_size(acts) == 1 + best_size(rest)
print("ok")
```

### Other uses

- In [matrix-chain multiplication](/matrix-chain-multiplication/), the two sub-products of an optimal parenthesization are optimal for their ranges, because the cost of the whole is the sum of the two costs plus a term that depends only on the split.
- In [longest common subsequence](/longest-common-subsequence/), a prefix pair of an optimal common subsequence is an optimal common subsequence of the two prefixes, because a longer one for the prefixes could be pasted in place of the part.
- In an [optimal binary search tree](/optimal-binary-search-tree/), each subtree of an optimal tree is optimal for its range of keys, because the cost of the whole is the cost of the subtrees plus the sum of the probabilities in the range (Exercise 4).
- See also the [principle of optimality](/principle-of-optimality/).

## Variations

- **Exchange argument.** The paste step swaps one element of a solution for another, as in Lemma 1. The page on the [exchange argument](/exchange-argument/) treats this form for greedy algorithms. Lemma 2 pastes a whole sub-solution. A proof of a greedy algorithm needs both lemmas.
- **Existence form.** If the combination of costs is only non-decreasing, the paste gives $c(X') \le c(X)$ and no contradiction. The conclusion then becomes: some optimal solution has optimal parts. This is enough for a recurrence that takes the minimum over choices.
- **Several parts.** When a solution has $k$ parts, the argument replaces one part and keeps the others. The parts must be independent: replacing one must not change what is feasible for the others.

## Pitfalls

- **The paste may be infeasible.** Take the longest simple path problem. Let the graph be the square with vertices $q, r, t, s$ and the undirected unit-weight edges $qr$, $rt$, $ts$, $sq$. The longest simple path from $q$ to $t$ has 2 edges, and $q, r, t$ is one such path. Its subpath from $q$ to $r$ has 1 edge. But the longest simple path from $q$ to $r$ is $q, s, t, r$, with 3 edges. Pasting it into $q, r, t$ gives $q, s, t, r, t$, which repeats $t$ and is not a simple path. The paste fails at the feasibility step. Longest simple path has no optimal substructure of this kind. For shortest paths, the same paste is a walk, and walks are allowed.
- **A non-strict combination proves less.** Let the cost of a path be its largest edge weight, to be minimized. Take edges $s \to a$ with weight 3, $s \to b$ with 2, $b \to a$ with 2 and $a \to t$ with 9. The paths $s, a, t$ and $s, b, a, t$ both have cost 9, so both are optimal. The subpath $s, a$ of the first has cost 3, but the best path from $s$ to $a$ has cost 2. So not every optimal solution has optimal parts. The existence form holds: the optimal path $s, b, a, t$ has optimal parts.
- **Optimal substructure is not a full algorithm.** The claim does not say which choice to make. A recurrence must take the best over all choices. A greedy algorithm needs, in addition, a proof that one choice is safe.
- **Wrong greedy choice.** With the earliest start instead of the earliest finish, Lemma 1 fails. For $(0,10)$, $(1,2)$, $(3,4)$, the earliest start gives $(0,10)$ and a set of size 1, but the maximum is 2.
- **Subproblems that are not independent.** If the parts compete for a resource, replacing one part can break another. The template then needs a state that records the resource.

## Exercises

1. Prove by cut and paste that, in an optimal parenthesization of $A_i A_{i+1} \cdots A_j$ that splits at $k$, the parenthesizations of $A_i \cdots A_k$ and $A_{k+1} \cdots A_j$ are optimal. Use that the cost of the whole is the cost of the left part, plus the cost of the right part, plus a term that depends only on $i$, $k$ and $j$.
2. Let $D$ be a set of coin values and let a solution for the amount $n$ be a multiset of coins from $D$ with the sum $n$. Prove that if $M$ is a minimum-size solution for $n$ and $d \in M$, then $M$ minus one copy of $d$ is a minimum-size solution for $n - d$. State which part is the paste and why it is feasible.
3. Add a weight $v(a) > 0$ to each activity and ask for a compatible set of the largest total weight. Show that the earliest-finish choice is not safe: find three activities, or fewer, where the greedy choice gives a worse total. Then prove with cut and paste that if $a$ is the activity of an optimal set with the latest finish, then the rest of the set is a maximum-weight compatible subset of $\{x \in S : f(x) \le s(a)\}$.
   <details><summary>Hint</summary>Try $(0,2)$ with weight 1 and $(1,10)$ with weight 100. The best total is 100, and the earliest-finish choice reaches 1.</details>
4. In a binary search tree with keys $k_1 < \cdots < k_m$ and search probabilities $p_1, \ldots, p_m$, the cost is $\sum_i p_i (d_i + 1)$, where $d_i$ is the depth of $k_i$, with the root at depth 0. Prove that each subtree of an optimal tree is optimal for its range of keys. Write the cost of the whole in terms of the cost of the subtree and the depth of its root.
5. Take the bottleneck example of the pitfalls. Prove that for the problem of the path with the least largest edge weight, some optimal path has optimal prefixes. State exactly where the proof of the strict form fails.
6. Let a cycle of negative weight be reachable from $s$, and let it lie on a walk from $s$ to $v$. Show that no shortest walk from $s$ to $v$ exists. Explain why the claim on shortest walks then says nothing, and why the formula for $\delta(s, v)$ has no meaning.
   <details><summary>Hint</summary>Going once more around the cycle lowers the weight of every walk that contains it.</details>
7. Take the square graph of the pitfalls. Write a short program that lists all simple paths and checks, for every longest simple path and every pair of its vertices, whether the subpath is longest. Report the first failure.

## References
