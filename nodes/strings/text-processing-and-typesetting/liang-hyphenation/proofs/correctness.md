---
title: The trie walk gives the largest digit of every matching pattern
proves: [correctness, termination]
status: full
---

**Claim.** Let $P$ be a finite set of patterns, each given as a nonempty string of letters $q = q_0 \cdots q_{k-1}$ (the mark "." counts as a letter) and a list of values $d_q[0], \ldots, d_q[k]$ in $\{0, \ldots, 9\}$, one per gap. If two entries have the same letters, merge them into one whose values are the maxima, gap by gap. Let $u = u_0 \cdots u_{N-1}$ be the word with "." at both ends, and for a gap $g$ of $u$ ($0 \le g \le N$, gap $g$ is just before $u_g$) let

$$V(g) = \max\left(\{0\} \cup \{\, d_q[g - i] : q \in P,\ u_i \cdots u_{i+k-1} = q,\ i \le g \le i + k \,\}\right).$$

Then lines L1 to L9 stop and leave $v[g] = V(g)$ for every gap $g$. Line L10 then returns exactly the positions $k$ of the word with $1 \le k < n$, $V(k + 1)$ odd, $k \ge \lambda$ and $n - k \ge \rho$, where $n = N - 2$ is the length of the word, $\lambda$ is lefthyphenmin and $\rho$ is righthyphenmin.

**Setup.** The trie has one node for each prefix of the letters of a pattern, the root for the empty prefix. The child of the node for $x$ on the letter $c$ is the node for $xc$, if $xc$ is a prefix of some pattern. The node for $q$ holds the values $d_q$ exactly when $q$ is the letters of a pattern. Merging duplicates in `add` gives the maxima of the claim, so each node holds at most one list.

**Lemma (one start).** For a fixed start $i$, the inner loop of lines L5 to L9 visits, in order of length, exactly the patterns $q \in P$ with $u_i \cdots u_{i+|q|-1} = q$, and for each it raises $v[i + t]$ to at least $d_q[t]$ for $t = 0, \ldots, |q|$.

*Proof.* We show by induction on $j \ge i$ that, if the loop reaches the step $j$, then before line L6 the variable `node` is the node for $u_i \cdots u_{j-1}$. For $j = i$, line L4 sets it to the root, the node for the empty string. At step $j$, line L6 moves to the child on $u_j$. If this child does not exist, no pattern has $u_i \cdots u_j$ as a prefix, so no pattern that starts at $i$ is longer than $j - i$, and line L7 stops the loop without missing any. Otherwise the new node is the node for $u_i \cdots u_j$, which proves the step. At the node for $u_i \cdots u_j$, line L8 finds values exactly when $u_i \cdots u_j$ is a pattern $q$, and then line L9 applies $v[i + t] \leftarrow \max(v[i + t], d_q[t])$ for $t = 0, \ldots, |q|$. The loop also stops when $j$ passes the end of $u$, and no pattern that starts at $i$ can be longer than $N - i$. $\square$

**Proof of the claim.** The array starts at 0 (line L2). Every update of line L9 is a maximum with the value of a pattern that occurs in $u$ and covers the gap $i + t$ with $d_q[t]$, so at all times $v[g] \le V(g)$. Conversely, take an occurrence of $q$ at $i$ and a gap $g$ with $i \le g \le i + |q|$. The outer loop (line L3) runs every start $i$ from 0 to $N - 1$, and by the lemma the walk from $i$ visits $q$ and raises $v[g]$ to at least $d_q[g - i]$. Values only grow. So at the end $v[g] \ge V(g)$, and hence $v[g] = V(g)$.

The code returns $v[1], \ldots, v[n + 1]$, so its entry $k$ is $V(k + 1)$, the gap of $u$ just before $u_{k+1}$, which is the gap of the word just before its letter $k$. Line L10 keeps the gaps $k$ inside the word ($1 \le k < n$) whose value is odd and that leave at least $\lambda$ letters before and $\rho$ letters after. This is the rule of the claim.

**Termination.** The outer loop runs $N$ times and the inner loop at most $N - i$ times for the start $i$, so there are at most $N(N+1)/2$ trie steps, and line L9 runs at most $|q| + 1$ times per visited pattern. $\blacksquare$

**Note on the exceptions.** When the word is in the exception list, `hyphen_positions` returns the listed positions and does not use the patterns. This matches the rule of TeX that the \hyphenation list overrides the patterns, and it needs no proof beyond the code.
