---
title: ID3 stops, splits on an attribute of largest gain at each node, and fits consistent data exactly
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. A sample $S$ is a finite list of examples $(x, y)$, where $x$ assigns a value to each attribute of a finite set $\mathcal{A}$, and $y$ is a label. For $A \subseteq \mathcal{A}$, call $S$ *consistent on $A$* if any two examples of $S$ that agree on every attribute of $A$ have the same label. Each attribute $a$ has a finite domain $V_a$ that contains every value of $a$ in $S$.

**Claim 1 (termination and depth).** ID3$(S, A, c)$ stops for every input, and the tree it returns has depth at most $|A|$. On each root-to-leaf path, each attribute is tested at most once.

*Proof.* By induction on $|A|$. If $|A| = 0$, one of lines L1, L2 or L4 returns a leaf, of depth 0. If $|A| \ge 1$ and no leaf is returned by L1 or L2, line L5 picks $a^* \in A$, and line L8 makes one recursive call for each of the finitely many values of $a^*$, each with the attribute set $A \setminus \{a^*\}$ of size $|A| - 1$. By the induction hypothesis each call stops and returns a tree of depth at most $|A| - 1$ that tests only attributes of $A \setminus \{a^*\}$, each at most once on a path. The new node adds one level and tests $a^*$, which no child tests. So the result has depth at most $|A|$, and each path tests $a^*$ once and the others at most once. $\square$

**Claim 2 (greedy choice).** At each internal node $u$, the attribute tested at $u$ has the largest information gain, among the attributes not tested above $u$, on the examples of $S$ that reach $u$.

*Proof.* By induction on the depth of $u$, the call that creates $u$ receives exactly the examples of $S$ whose values agree with the tests on the path to $u$ (line L8 passes $\{(x, y) \in S : x_{a^*} = v\}$ to the child for value $v$), and the attributes not tested on that path (line L8 removes $a^*$). Line L5 chooses the attribute of largest gain on that sample among those attributes. $\square$

**Claim 3 (exact fit).** If $S$ is consistent on $A$, then the tree $T$ = ID3$(S, A, c)$ classifies every example of $S$ correctly: for each $(x, y) \in S$, following the branches of $x$ from the root of $T$ reaches a leaf labeled $y$.

*Proof.* By induction on $|A|$, for all $S$ and $c$.

- If $S$ is empty, there is nothing to show.
- If all labels of $S$ equal $c'$, line L2 returns a leaf labeled $c'$, which is correct for each example.
- Otherwise $S$ holds two examples with different labels. If $A = \emptyset$, any two examples agree on all attributes of $A$, so consistency on $\emptyset$ forces all labels to be equal, which is not the case. So $A \ne \emptyset$ and line L4 does not return. Line L5 picks $a^*$ and line L8 builds, for each value $v$, the tree $T_v$ = ID3$(S_v, A \setminus \{a^*\}, m)$ with $S_v = \{(x, y) \in S : x_{a^*} = v\}$.
- Take $(x, y) \in S$ and let $v = x_{a^*}$. Then $(x, y) \in S_v$. Two examples of $S_v$ that agree on $A \setminus \{a^*\}$ also agree on $a^*$ (both have value $v$), so they agree on $A$, and by the consistency of $S$ on $A$ they have the same label. So $S_v$ is consistent on $A \setminus \{a^*\}$, and by the induction hypothesis $T_v$ classifies $(x, y)$ correctly. At the root of $T$, the example follows the branch $v$ into $T_v$, so $T$ classifies it correctly. $\square$

With $A = \mathcal{A}$, Claim 3 says: if no two training examples have the same attribute values and different labels, the ID3 tree has zero training error.

**Claim 4 (windowing stops).** If $S$ is consistent on $\mathcal{A}$ and each round adds at least one misclassified example to the window, the windowing loop stops after at most $n$ rounds with a tree that classifies all of $S$ correctly.

*Proof.* The window $W$ is a subset of $S$, so it is consistent on $\mathcal{A}$, and by Claim 3 the tree of a round classifies every example of $W$ correctly. So each misclassified example lies outside $W$, and a round that does not stop adds at least one new example to $W$. $|W|$ grows by at least 1 in each such round and is at most $n$, so there are at most $n$ rounds. The loop stops only when no example outside $W$ is misclassified, and the examples of $W$ are correct by Claim 3. $\blacksquare$
