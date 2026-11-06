---
title: Memoized derivatives of a cyclic grammar graph denote the Brzozowski derivatives, so the recognizer accepts exactly L(G), and every call stops
proves: [correctness, termination]
status: full
---

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. The line numbers are those of RECOGNIZE, $D_c$ and NULLABLE on the page. For a language $L$ and a token $c$, the Brzozowski derivative is $\partial_c L = \{ v : c v \in L \}$, and $\partial_{c w} L = \partial_w \partial_c L$.

## The meaning of a graph

A node is $\emptyset$, $\varepsilon$, a token $a$, a union $x \cup y$ or a concatenation $x \circ y$, where $x$ and $y$ are nodes; the graph may have cycles. The language $[x]$ of every node is defined by the least sets that satisfy

$$[\emptyset] = \emptyset, \quad [\varepsilon] = \{\varepsilon\}, \quad [a] = \{a\}, \quad [x \cup y] = [x] \cup [y], \quad [x \circ y] = [x]\,[y].$$

Equivalently, $s \in [x]$ when there is a finite *membership proof*: a tree whose root is the claim $s \in [x]$, where a claim about $x \cup y$ has one child, $s \in [x]$ or $s \in [y]$, a claim about $x \circ y$ has two children $s_1 \in [x]$ and $s_2 \in [y]$ with $s = s_1 s_2$, and the leaves are $\varepsilon \in [\varepsilon]$ and $a \in [a]$. The *size* of a claim is the number of nodes of its smallest proof.

**Lemma 0 (the grammar graph).** For the graph built from $G$, with one union node per nonterminal (a chain of unions over its productions, ended by $\emptyset$) and one right-nested chain of concatenations per production, $[\mathrm{top}_A] = L(A)$ for every nonterminal $A$.

*Proof.* A membership proof for $s \in [\mathrm{top}_A]$ picks one production of $A$ in the union chain and splits $s$ along its right side, and each piece is again a membership proof for a symbol. Contracting the chains turns it into a parse tree of $s$ with root $A$, and expanding a parse tree gives a membership proof. $\square$

## Lemma 1: compaction

COMPACT$(x)$ (line L3) returns a node with the same language as $x$, and if $s \in [x]$ has size $m$, then $s \in [\mathrm{COMPACT}(x)]$ has size at most $m$.

*Proof.* One step replaces $\emptyset \cup y$ or $y \cup \emptyset$ by $y$, $\varepsilon \circ y$ by $y$, and returns $\emptyset$ for $\emptyset \circ y$ or $y \circ \emptyset$. Each is an identity of languages, and in the first two cases a proof for $x$ is a proof for $y$ with one or two extra nodes on top, so sizes do not grow. If the steps come back to a node already seen, the nodes $x_0, \ldots, x_r = x_0$ on the loop satisfy $[x_t] = [x_{t+1}]$ through equations with no other contribution, so a membership proof for any of them would contain a proof for the next one, then the next, without end; there is none, all of them denote $\emptyset$, and returning $\emptyset$ is correct. $\square$

## Lemma 2: nullability

After NULLABLE$(x)$ returns, every node reachable from $x$ is decided, and a node is marked nullable exactly when $\varepsilon \in [\,\cdot\,]$.

*Proof.* We have $\varepsilon \in [x \cup y]$ iff $\varepsilon \in [x]$ or $\varepsilon \in [y]$, and $\varepsilon \in [x \circ y]$ iff both, since $\varepsilon = s_1 s_2$ forces $s_1 = s_2 = \varepsilon$; tokens and $\emptyset$ never contain $\varepsilon$. So the nullable nodes are the least solution of these Boolean equations. Assume, by induction over the calls, that the nodes decided before the call are decided correctly. Line L11 collects the undecided nodes reachable from $x$; all their children are collected or decided. For each collected node, the counter holds the number of collected children that must still be marked: 0 when the node is $\varepsilon$ or a union with a child already known nullable, 1 for another union, and the number of undecided children for a concatenation whose children are not known to be non-nullable. Line L12 marks the nodes whose counter is 0 and propagates: a newly marked node decrements the counters of its users, and a counter reaching 0 marks its node. All counters are computed before any node is marked, so each child is counted once.

Soundness: by induction on the order of marking, every marked node has $\varepsilon$ in its language, since its counter reached 0 only after the required children were marked or known. Completeness: if $\varepsilon \in [x]$ for a collected node, induction on the size of the claim $\varepsilon \in [x]$ shows that the children used by its smallest proof are marked or were known nullable before the call, so the counter of $x$ reaches 0. Line L13 then sets the rest to non-nullable, which is correct. Each collected node and each edge is handled $O(1)$ times. $\square$

## Lemma 3: one derivative

Let $D_c$ be called on a root during one token step. When it returns, every node $u$ returned by a call $D_c(y)$ (line L4, L5, L6 or L10), in this step or an earlier step with the same token, satisfies $[u] = \partial_c [y]$.

*Proof.* The nodes created in this step are the memo nodes $u_x$, one for each compacted union or concatenation node $x$ reached in this step (plus the inner concatenation node of line L9). Write $d(y)$ for the value returned by $D_c(y)$: $\emptyset$ for $\emptyset$ and $\varepsilon$, $\varepsilon$ or $\emptyset$ for a token, and otherwise the memo node of $\mathrm{COMPACT}(y)$. When the stack is empty, every memo node has its children (lines L7 to L9):

- $u_x = d(x_1) \cup d(x_2)$ for $x = x_1 \cup x_2$;
- $u_x = d(x_1) \circ x_2$ for $x = x_1 \circ x_2$ with $x_1$ not nullable;
- $u_x = (d(x_1) \circ x_2) \cup d(x_2)$ for $x = x_1 \circ x_2$ with $x_1$ nullable.

The nodes $x$, $x_1$, $x_2$ are old: they were reachable from the root, and every node reachable from the root had its children before the step began, so NULLABLE$(x_1)$ is decided on a complete graph and is correct by Lemma 2. Memo nodes from earlier steps with the same token are correct by induction on the steps.

$\subseteq$: the family $X_x = \partial_c [x]$ satisfies the equations of the memo nodes, because $\partial_c (A \cup B) = \partial_c A \cup \partial_c B$, $\partial_c (A B) = (\partial_c A) B$ when $\varepsilon \notin A$, $\partial_c (A B) = (\partial_c A) B \cup \partial_c B$ when $\varepsilon \in A$, $\partial_c \{\varepsilon\} = \partial_c \emptyset = \emptyset$, and $\partial_c \{a\}$ is $\{\varepsilon\}$ for $a = c$ and $\emptyset$ otherwise; and $[\mathrm{COMPACT}(y)] = [y]$ by Lemma 1. The languages of the memo nodes are the least solution, so $[u_x] \subseteq \partial_c [x]$.

$\supseteq$: we show that $c v \in [y]$ implies $v \in [d(y)]$, by induction on the size of the claim $c v \in [y]$. By Lemma 1 we may replace $y$ by $x = \mathrm{COMPACT}(y)$ without increasing the size. If $x$ is a token, then $x = c$, $v = \varepsilon$ and $d(x) = \varepsilon$. If $x = x_1 \cup x_2$, then $c v \in [x_i]$ with a smaller claim, so $v \in [d(x_i)] \subseteq [u_x]$. If $x = x_1 \circ x_2$, then $c v = s_1 s_2$ with $s_1 \in [x_1]$ and $s_2 \in [x_2]$. If $s_1 = c v_1$, then $v_1 \in [d(x_1)]$ by induction, so $v = v_1 s_2 \in [d(x_1) \circ x_2] \subseteq [u_x]$. If $s_1 = \varepsilon$, then $x_1$ is nullable, $u_x$ has the branch $d(x_2)$, and $c v = s_2 \in [x_2]$ with a smaller claim, so $v \in [d(x_2)] \subseteq [u_x]$. $\square$

## Theorem

RECOGNIZE stops on every input and returns true exactly when $w \in L(G)$.

*Proof.* By Lemma 0 the initial node denotes $L(G)$. By Lemma 3 and induction on $i$, after $i$ iterations of line L1 the current node denotes $\partial_{a_1 \cdots a_i} L(G)$. So the final node denotes $\partial_w L(G) = \{ v : w v \in L(G) \}$, which contains $\varepsilon$ exactly when $w \in L(G)$, and line L2 returns this by Lemma 2.

Termination: COMPACT stops because it never visits a node twice. One call of $D_c$ on a root pushes one stack entry per new memo key; the keys are pairs (old node, $c$), and there are finitely many old nodes, so the loop stops. NULLABLE handles each collected node and edge a constant number of times. $\square$

## Remarks

**The running time.** Adams, Hollenbeck and Might name every node created during parsing by the node it was derived from and the tokens it was derived by, and show that the names have the form $N u$ or $N u \bullet v$ with $N$ a node of the initial grammar and $u$, $uv$ substrings of the input. There are $O(|G| n^3)$ such names, so $O(|G| n^3)$ nodes are created; each creation costs $O(1)$ apart from nullability, which is linear in the number of nodes in total by the counter method of Lemma 2. They note that the count holds with compaction too, since compaction only removes nodes.

**Why memoization matters.** Without the memo table, the rule for $x_1 \circ x_2$ with nullable $x_1$ uses $x_2$ twice, once inside $d(x_1) \circ x_2$ and once as $d(x_2)$, and repeated derivatives copy the copies; even an acyclic grammar can then make the graph grow exponentially, and a cyclic one makes the computation loop. The memo table both shares the copies and, because it stores $u_x$ before its children are computed, closes the cycles.
