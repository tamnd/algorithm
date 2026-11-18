---
title: Lookup in a packed trie is correct when the letter is stored and bases are distinct
proves: [correctness, termination]
status: full
---

**Claim.** Let $D$ be a finite map from nonempty strings over an alphabet $\Sigma$ to values, with codes $\mathrm{code}(c) \in \{1, \ldots, \sigma\}$ that are distinct for distinct letters. Build the packed trie with lines L9 to L20. Then the build stops, and afterwards, for every string $x$, `get(x)` (lines L1 to L8) returns $D(x)$ if $x$ is a key and the default otherwise. Also `prefix_values(text, i)` yields exactly the pairs $(j, D(\mathrm{text}[i:j]))$ for the keys that are prefixes of $\mathrm{text}[i:]$, in increasing order of $j$.

**Setup.** Let $T$ be the trie of the keys: a node for each prefix of a key, the root for the empty string. A family is a node of $T$ with at least one child, and its transitions are the edges to its children. The build gives each family $\phi$ a base $\beta(\phi)$, and puts its transition on the letter $c$ in the slot $\beta(\phi) + \mathrm{code}(c)$, with $\mathrm{char} = c$, $\mathrm{out}$ the value of the child if the child is a key, and $\mathrm{link}$ the base of the child if the child is a family.

**Invariant of the build.** After each family is placed (lines L16 to L20):

- (I1) the bases of the placed families are distinct;
- (I2) every slot holds the transition of at most one placed family, and a slot with $\mathrm{char} \ne$ None holds exactly one;
- (I3) the slot $\beta(\phi) + \mathrm{code}(c)$ of a placed family $\phi$ holds $\mathrm{char} = c$, the correct $\mathrm{out}$, and, once the child is placed, the correct $\mathrm{link}$.

*Initialization.* Before the first family nothing is placed and all slots are free.

*Maintenance.* Lines L9 to L13 return the least $b$ with $b$ not in the set of taken bases and with every slot $b + \mathrm{code}(c)$, for the letters $c$ of the new family, free. Such a $b$ exists: any $b$ larger than every taken base and the current table length qualifies, so the search stops. Line L16 adds $b$ to the taken bases, which keeps (I1). The slots that lines L17 and L18 fill were free, and distinct letters have distinct codes, so (I2) is kept. Line L18 writes the letter and the output of each transition. The child families are queued (line L19) and placed later; when a child is placed, line L20 writes its base into the parent slot, which nothing else writes. So (I3) holds.

*Termination of the build.* The queue holds each family once (each node is queued only by its parent), there are finitely many, and each first-fit search stops.

**Lemma (one step).** Let $\phi$ be a family and $c$ a letter. Then `_slot`$(\beta(\phi), c)$ returns the slot of the transition of $\phi$ on $c$ if $\phi$ has a child on $c$, and None otherwise.

*Proof.* If $\phi$ has a child on $c$, its slot $s = \beta(\phi) + \mathrm{code}(c)$ holds $\mathrm{char} = c$ by (I3), so lines L1 and L2 return $s$. Assume now that $\phi$ has no child on $c$ but line L2 finds $\mathrm{char}[s] = c$. By (I2) the slot holds the transition of some placed family $\psi$ on some letter $c'$, with $\mathrm{char}[s] = c'$ by (I3). So $c' = c$ and $\beta(\psi) + \mathrm{code}(c) = s = \beta(\phi) + \mathrm{code}(c)$, which gives $\beta(\psi) = \beta(\phi)$. By (I1), $\psi = \phi$, so $\phi$ has a child on $c$, a contradiction. Hence line L3 returns None. (If the letter is not in the alphabet, or the base is None because the current node has no children, the code returns None at once, which is also correct.) $\square$

**Proof of the claim.** For `get`, show by induction on $t$ that after $t$ letters of $x$ the loop of line L4 is still running exactly when $x_0 \cdots x_{t-1}$ is a node of $T$, and then $s$ is the slot of the edge into that node and `base` is its base if the node is a family, or None. For $t = 0$, `base` is the base of the root. In the step, by the lemma, line L5 finds the slot of the edge on $x_t$ exactly when the node for $x_0 \cdots x_t$ exists; otherwise line L6 returns the default, which is right because no key has this prefix. Line L7 reads the base of the child from (I3). After the last letter, $x$ is a node of $T$, and $\mathrm{out}[s]$ is its value if it is a key and None otherwise, by (I3). Values are never None, so line L8 returns $D(x)$ or the default exactly as claimed. `prefix_values` runs the same walk from position $i$ and reports $\mathrm{out}$ at each step where it is not None, so it yields the keys that are prefixes of $\mathrm{text}[i:]$, shortest first, and stops when the walk leaves $T$.

**Termination of a lookup.** Each step reads one letter, so `get(x)` takes at most $|x|$ steps and each step reads $O(1)$ slots. $\blacksquare$

**Why both checks are needed.** Without the stored letter, a slot of another family could be read as a transition. Without distinct bases, two families with the same base and disjoint letters could both be placed, and a lookup from one would accept the letters of the other: the stored letter matches, but it is not the letter of the right family. The proof uses (I1) at exactly this point.
