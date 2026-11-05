---
title: Aho-Corasick outputs each occurrence of each pattern exactly once
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and patterns $P_0, \ldots, P_{k-1}$, AHO-CORASICK stops and outputs each pair $(s, j)$ with $0 \le s \le n - |P_j|$ and $T[s \ldots s + |P_j| - 1] = P_j$ exactly once, and outputs no other pair.

**Setup.** Let $N$ be the set of all prefixes of the patterns, including the empty string. After lines L1 to L3, the trie has one node for each string of $N$, $\mathrm{str}(\mathrm{root})$ is the empty string, $\mathrm{goto}(v, a)$ is defined exactly when $\mathrm{str}(v)a \in N$, and $\mathrm{out}[v]$ is the list of the indices $j$ with $P_j = \mathrm{str}(v)$, each index once. We call $v$ a *pattern node* when $\mathrm{out}[v] \ne \emptyset$. The set $N$ is closed under prefixes: if $ya \in N$, then $y \in N$. We write $|v|$ for the depth $|\mathrm{str}(v)|$. For two suffixes of one string, the shorter is a suffix of the longer.

**Lemma 1 (failure links).** For each node $u \ne \mathrm{root}$, $\mathrm{fail}[u]$ is the node of the longest proper suffix of $\mathrm{str}(u)$ that lies in $N$. Moreover, the nodes whose strings are proper suffixes of $\mathrm{str}(u)$ are exactly $\mathrm{fail}[u], \mathrm{fail}^2[u], \ldots$, ending at the root, in decreasing order of depth.

*Proof.* By induction on $|u|$. The breadth-first order of lines L4 to L13 dequeues all nodes of depth $d$ before any node of depth $d + 1$, and the link of a node $u$ of depth $d + 1 \ge 2$ is set when its parent, of depth $d$, is dequeued. So when $\mathrm{fail}[u]$ is set, the links of all nodes of depth at most $d$ are already set.

*Depth 1.* The only proper suffix of a one-character string is the empty string, and line L4 sets $\mathrm{fail}[u] = \mathrm{root}$. The chain is the root alone.

*Depth $d + 1 \ge 2$.* Let $u = \mathrm{goto}(v, a)$, so $\mathrm{str}(u) = \mathrm{str}(v)a$ and $|v| = d \ge 1$. A nonempty proper suffix of $\mathrm{str}(v)a$ has the form $ya$, where $y$ is a proper suffix of $\mathrm{str}(v)$. If $ya \in N$, then $y \in N$. So the nonempty candidates are the strings $ya$ with $y$ a proper suffix of $\mathrm{str}(v)$ in $N$ and $\mathrm{goto}(y, a)$ defined. By the induction hypothesis for $v$, these strings $y$ are the chain $\mathrm{fail}[v], \mathrm{fail}^2[v], \ldots, \mathrm{root}$, in decreasing order of length. Lines L9 to L11 walk this chain from the start and stop at the first node $f$ with $\mathrm{goto}(f, a)$ defined, or at the root. If $\mathrm{goto}(f, a)$ is defined, it is the longest candidate; it is not $u$ itself, because $|f| < |v|$. If not, then $f$ is the root and no candidate exists, and the longest proper suffix in $N$ is the empty string. Line L12 sets $\mathrm{fail}[u]$ to the right node in both cases.

For the chain, let $x$ be a proper suffix of $\mathrm{str}(u)$ in $N$, and let $w = \mathrm{fail}[u]$. By the first part, $|x| \le |w|$. If $|x| = |w|$, then $x = \mathrm{str}(w)$. If $|x| < |w|$, then $x$ is a proper suffix of $\mathrm{str}(w)$, and $|w| \le d < d + 1$, so by the induction hypothesis $x$ is on the chain of $w$. Conversely, each node of the chain spells a proper suffix of $\mathrm{str}(u)$, by transitivity of the suffix relation. Each link strictly lowers the depth, so the chain is in decreasing order of depth and ends at the root. $\square$

**Lemma 2 (dictionary links).** For each node $v$, $\mathrm{dict}[v]$ is the pattern node of the longest proper suffix of $\mathrm{str}(v)$ that is a pattern, or nil if no proper suffix is a pattern. Hence the sequence $\mathrm{dict}[v], \mathrm{dict}^2[v], \ldots$ (up to nil) lists all pattern nodes whose strings are proper suffixes of $\mathrm{str}(v)$, in decreasing order of depth, each once.

*Proof.* For the root, $\mathrm{dict}$ is nil, and the empty string has no proper suffix. For $v \ne \mathrm{root}$, line L7 runs when $v$ is dequeued. Then $\mathrm{fail}[v]$ has smaller depth, so it is the root or a node dequeued before $v$, and its $\mathrm{dict}$ value is final. By Lemma 1, the proper suffixes of $\mathrm{str}(v)$ in $N$ are $\mathrm{str}(\mathrm{fail}[v])$ and the proper suffixes of $\mathrm{str}(\mathrm{fail}[v])$ in $N$. Each pattern is in $N$. So the longest proper suffix of $\mathrm{str}(v)$ that is a pattern is $\mathrm{str}(\mathrm{fail}[v])$ if $\mathrm{fail}[v]$ is a pattern node, and else the longest proper suffix of $\mathrm{str}(\mathrm{fail}[v])$ that is a pattern, which is $\mathrm{dict}[\mathrm{fail}[v]]$ by induction on depth. This is line L7. The second statement follows by applying the first one to $\mathrm{dict}[v]$, then to $\mathrm{dict}^2[v]$, and so on; the depth strictly falls, so the sequence ends. $\square$

**Lemma 3 (REPORT).** REPORT$(v, e)$ outputs the pair $(e - |P_j|, j)$ for each $j$ such that $P_j$ is a suffix of $\mathrm{str}(v)$, each pair once, and nothing else.

*Proof.* The patterns that are suffixes of $\mathrm{str}(v)$ are $\mathrm{str}(v)$ itself, if $v$ is a pattern node, and the patterns among its proper suffixes. Line L19 starts the walk at $v$ in the first case and at $\mathrm{dict}[v]$ in the second. If $v$ is a pattern node, $\mathrm{dict}[v]$ lists exactly the remaining ones (Lemma 2). So the loop of lines L20 to L22 visits each pattern node whose string is a suffix of $\mathrm{str}(v)$ exactly once, and line L21 outputs each index stored at it. Each index $j$ is stored at exactly one node, the node of $P_j$. $\square$

**Lemma 4 (search invariant).** For $0 \le e \le n$, let $\lambda_e$ be the longest suffix of $T[0 \ldots e-1]$ that lies in $N$. When REPORT$(v, e)$ is called, $\mathrm{str}(v) = \lambda_e$.

*Proof.* By induction on $e$. For $e = 0$, the text read is empty, $\lambda_0$ is the empty string, and line L14 calls REPORT with the root.

Assume the claim for $e = i$, with $v$ the node of $\lambda_i$, and let $c = T[i]$. A nonempty suffix of $T[0 \ldots i]$ in $N$ has the form $yc$ with $y$ a suffix of $T[0 \ldots i-1]$ and $y \in N$ (prefix closure). Then $|y| \le |\lambda_i|$, so $y$ is a suffix of $\lambda_i$: it is $\lambda_i$ or a proper suffix of it in $N$, that is, $v$ or a node of the failure chain of $v$ (Lemma 1). Line L16 walks $v, \mathrm{fail}[v], \ldots$ in decreasing order of depth, and stops at the first node with a child along $c$, or at the root. If that node has the child, the child spells the longest suffix of $T[0 \ldots i]$ in $N$, and line L17 moves there. If not, the walk stopped at the root and no candidate $y$ exists, so $\lambda_{i+1}$ is empty and line L17 sets $v$ to the root. Line L18 then calls REPORT with the node of $\lambda_{i+1}$. $\square$

**Termination.** The loop of lines L10 and L11 and the loop of line L16 each lower the depth of a node by at least 1 at each pass, and depths are non-negative integers, so they stop. The loop of line L20 lowers the depth at each pass by Lemma 2. The other loops run over finite sets. So the algorithm stops.

**Theorem.** The claim holds.

*Proof.* Each call REPORT$(v, e)$ outputs pairs $(e - |P_j|, j)$ with $P_j$ a suffix of $\mathrm{str}(v) = \lambda_e$ (Lemmas 3 and 4), and $\lambda_e$ is a suffix of $T[0 \ldots e-1]$. So $P_j = T[e - |P_j| \ldots e - 1]$, and each output pair is an occurrence.

Conversely, let $(s, j)$ be an occurrence and $e = s + |P_j|$, so $0 \le e \le n$. Then $P_j$ is a suffix of $T[0 \ldots e-1]$, and $P_j \in N$. By the definition of $\lambda_e$, $|P_j| \le |\lambda_e|$, so $P_j$ is a suffix of $\lambda_e$. The search calls REPORT exactly once with the end position $e$, at line L14 if $e = 0$ and at line L18 with $i = e - 1$ otherwise, and by Lemma 3 this call outputs $(s, j)$ exactly once. Other calls have another end position, so they do not output $(s, j)$. $\blacksquare$
