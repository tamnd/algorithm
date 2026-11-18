---
title: The maps of the viewlet transform stay equal to their definitions after every update
proves: [correctness, termination, space.extra]
status: full
---

We use the line numbers of the pseudocode on the page. The query has atoms $R_1, \ldots, R_k$ with distinct relation names (no self-join), variable sets $V_1, \ldots, V_k$, value variables $\mathit{VALS}$ and group variables $F$. A database gives each relation a function from tuples to integers, the weights, with finitely many nonzero values; negative weights are allowed. For a set $X$ of atoms, $\mathrm{Vars}(X) = \bigcup_{i \in X} V_i$. An *assignment* to a set of variables $W$ is a function from $W$ to values, and $R_i(x)$ means the weight of the tuple $x|_{V_i}$ in $R_i$.

**Definitions.** For each set $S$ of atoms let $\mathrm{rem} = \{1, \ldots, k\} \setminus S$ and

$$K_S = \mathrm{Vars}(\mathrm{rem}) \cap (\mathrm{Vars}(S) \cup F), \qquad Z_S = \mathrm{Vars}(\mathrm{rem}) \setminus K_S,$$

$$M_S(y) = \sum_{z} \; \prod_{i \in \mathrm{rem}} R_i(y \cup z) \prod_{v \in \mathit{VALS} \cap Z_S} z_v,$$

where $y$ is an assignment to $K_S$ and the sum is over the assignments $z$ to $Z_S$. The sum is finite: a term is nonzero only if each $(y \cup z)|_{V_i}$ has nonzero weight, and $Z_S \subseteq \mathrm{Vars}(\mathrm{rem})$. For $S$ the set of all atoms, $K_S = Z_S = \emptyset$, the product is empty, and $M_S() = 1$. For $S = \emptyset$, $K_\emptyset = \mathrm{Vars}(\text{all}) \cap F = F$, so $M_\emptyset(f)$ times $\prod_{v \in \mathit{VALS} \cap F} f_v$ is the query $Q[f]$, which is what line L8 returns. The stored map holds the nonzero values of $M_S$.

**Lemma 1 (keys).** For $j \notin S$ and $S' = S \cup \{j\}$: (a) $K_{S'} \subseteq K_S \cup V_j$; (b) $K_S \setminus V_j \subseteq K_{S'}$; (c) $Z_S \setminus V_j = Z_{S'}$.

*Proof.* Let $\mathrm{rem}' = \mathrm{rem} \setminus \{j\}$, so $\mathrm{Vars}(\mathrm{rem}') \subseteq \mathrm{Vars}(\mathrm{rem})$ and $\mathrm{Vars}(\mathrm{rem}) \setminus V_j \subseteq \mathrm{Vars}(\mathrm{rem}')$. (a) A variable of $K_{S'}$ is in $\mathrm{Vars}(\mathrm{rem}')$ and in $\mathrm{Vars}(S) \cup F \cup V_j$; if it is not in $V_j$ it is in $\mathrm{Vars}(\mathrm{rem}) \cap (\mathrm{Vars}(S) \cup F) = K_S$. (b) A variable of $K_S$ not in $V_j$ is in $\mathrm{Vars}(\mathrm{rem}) \setminus V_j \subseteq \mathrm{Vars}(\mathrm{rem}')$ and in $\mathrm{Vars}(S) \cup F \subseteq \mathrm{Vars}(S') \cup F$. (c) A variable $u$ of $Z_S \setminus V_j$ is in $\mathrm{Vars}(\mathrm{rem}')$ and not in $\mathrm{Vars}(S) \cup F$ and not in $V_j$, so not in $\mathrm{Vars}(S') \cup F$: $u \in Z_{S'}$. Conversely, $u \in Z_{S'}$ is in $\mathrm{Vars}(\mathrm{rem}) $ and not in $\mathrm{Vars}(S) \cup F \cup V_j$, so $u \in Z_S \setminus V_j$. $\square$

**Lemma 2 (delta of one map).** Let the update add $w$ to the weight of tuple $t$ in $R_j$, and let $\tau$ be the assignment of $t$ to $V_j$. For $j \notin S$, the change of $M_S$ is

$$\Delta M_S(y) = \begin{cases} w \cdot \prod_{v \in \mathit{VALS} \cap Z_S \cap V_j} \tau_v \cdot M_{S'}\big((y \cup \tau)|_{K_{S'}}\big) & \text{if } y \text{ agrees with } \tau \text{ on } K_S \cap V_j, \\ 0 & \text{otherwise,} \end{cases}$$

with $M_{S'}$ read before or after the update, which are equal. For $j \in S$, $M_S$ does not change.

*Proof.* If $j \in S$, $R_j$ does not occur in the definition of $M_S$. Let $j \notin S$. Because no other atom uses the name $R_j$, the product in the definition is linear in $R_j$: replacing $R_j$ by $R_j + w[\cdot = t]$ adds the terms

$$w \sum_{z} [\,(y \cup z)|_{V_j} = \tau\,] \prod_{i \in \mathrm{rem}'} R_i(y \cup z) \prod_{v \in \mathit{VALS} \cap Z_S} z_v.$$

The bracket is zero unless $y$ agrees with $\tau$ on $K_S \cap V_j$ and $z$ agrees with $\tau$ on $Z_S \cap V_j$. Then $z$ is $\tau$ on $Z_S \cap V_j$ and a free assignment $z'$ on $Z_S \setminus V_j = Z_{S'}$ (Lemma 1c). The value factors split into the fixed part $\prod_{v \in \mathit{VALS} \cap Z_S \cap V_j} \tau_v$ and $\prod_{v \in \mathit{VALS} \cap Z_{S'}} z'_v$. The assignment $y \cup \tau$ covers $K_S \cup V_j \supseteq K_{S'}$ (Lemma 1a), and each $R_i$ with $i \in \mathrm{rem}'$ reads only variables of $\mathrm{Vars}(\mathrm{rem}') = K_{S'} \cup Z_{S'}$. So the sum over $z'$ is $M_{S'}((y \cup \tau)|_{K_{S'}})$ by definition. $M_{S'}$ does not change, because $j \in S'$. $\square$

**Lemma 3 (the loop of lines L4 to L6 adds exactly $\Delta M_S$).** For $j \notin S$, lines L4 to L6 add $\Delta M_S(y)$ to entry $y$ for every $y$ with $\Delta M_S(y) \neq 0$, and nothing else.

*Proof.* Line L4 visits each nonzero entry $y'$ of $M_{S'}$ that agrees with $\tau$ on $K_{S'} \cap V_j$, and line L5 sets $y = (y' \cup \tau)|_{K_S}$, which is well defined because $y'$ and $\tau$ agree where both are defined. The map $y' \mapsto y$ is a bijection between these entries and the $y$ that agree with $\tau$ on $K_S \cap V_j$ and have $M_{S'}((y \cup \tau)|_{K_{S'}}) \neq 0$: its inverse is $y \mapsto (y \cup \tau)|_{K_{S'}}$, because $K_{S'} \subseteq K_S \cup V_j$ (Lemma 1a) and $K_S \setminus V_j \subseteq K_{S'}$ (Lemma 1b), so $y'$ determines $y$ and $y$ determines $y'$. Line L6 adds $w$ times the value factor times $M_{S'}(y')$, which is $\Delta M_S(y)$ by Lemma 2. Every $y$ with $\Delta M_S(y) \neq 0$ has such a $y'$. $\square$

**Theorem 1 (correctness).** After every sequence of updates, each stored map $M_S$ holds exactly the nonzero values of its definition, and line L8 returns $Q$ over the current relations.

*Proof.* By induction on the number of updates. At the start every relation is empty, so every $M_S$ with $S$ not the set of all atoms is $0$ (each term has a factor $R_i = 0$ with $i \in \mathrm{rem} \neq \emptyset$), and line L1 creates empty maps and $M_{\text{all}}() = 1$. For an update, line L2 changes only the maps with $j \notin S$. Each such map reads only $M_{S'}$ with $j \in S'$, which line L2 does not change, so the order of the loop does not matter, and by Lemma 3 each $M_S$ gets exactly its change. Line L7 removes entries that become 0, so the stored entries are the nonzero values. The statement about line L8 is the case $S = \emptyset$. $\blacksquare$

The proof never uses that weights are positive. So the maps are exact for any sequence of signed updates, in any order: the final maps depend only on the final weights.

**Termination.** Line L2 visits $2^k$ maps, and line L4 visits the finitely many entries of one map.

**Space.** The stored maps hold $\sum_S |M_S|$ nonzero entries. Each $M_S$ has at most one entry for each assignment to $K_S$ that extends tuples of the relations in $\mathrm{rem}$, so with $m$ the largest number of entries in a map, the space is $O(2^k m)$. The work of one update is the number of entries visited at line L4, at most $2^k m$; with a hash index on the variables $K_{S'} \cap V_j$ of each map, only the matching entries are visited. $\square$
