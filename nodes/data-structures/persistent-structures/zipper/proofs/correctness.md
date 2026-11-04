---
title: Zipper moves keep the represented tree, and replace changes only the focus
proves: [correctness]
status: full
---

**Setting.** Trees are nil or nodes $(l, x, r)$. A path is nil or $c :: p$, where $c$ is a crumb $(\text{left}, x, s)$ or $(\text{right}, x, s)$. Define
$$\text{plug}(t, \text{nil}) = t, \quad \text{plug}(t, (\text{left}, x, s) :: p) = \text{plug}((t, x, s), p), \quad \text{plug}(t, (\text{right}, x, s) :: p) = \text{plug}((s, x, t), p).$$
A position in a tree $T$ is a sequence of directions from the root. Define the position of a path by $\text{pos}(\text{nil}) = \langle\rangle$ and $\text{pos}(c :: p) = \text{pos}(p) \cdot \langle d \rangle$, where $d$ is the direction of $c$. The zipper $(t, p)$ *represents* the tree $\text{plug}(t, p)$ with the position $\text{pos}(p)$.

**Lemma 1.** For every path $p$ and trees $t, t'$, the tree $\text{plug}(t', p)$ equals $\text{plug}(t, p)$ with the subtree at $\text{pos}(p)$ replaced by $t'$, and the subtree of $\text{plug}(t, p)$ at $\text{pos}(p)$ is $t$.

*Proof.* By induction on the length of $p$. For $p = \text{nil}$ the position is the root, and both claims are clear. For $p = (\text{left}, x, s) :: p'$, the tree $\text{plug}(t, p)$ is $\text{plug}((t, x, s), p')$. By induction its subtree at $\text{pos}(p')$ is $(t, x, s)$, so its subtree at $\text{pos}(p') \cdot \langle \text{left} \rangle = \text{pos}(p)$ is $t$. Also by induction, $\text{plug}((t', x, s), p')$ is $\text{plug}((t, x, s), p')$ with the subtree at $\text{pos}(p')$ replaced by $(t', x, s)$, which is the same as replacing only the left child of that subtree, at $\text{pos}(p)$, by $t'$. The right case is symmetric. $\square$

**Lemma 2 (moves).** If $(t, p)$ represents $(T, \pi)$, then LEFT, RIGHT and UP, when they succeed, return zippers that represent $T$ with the position $\pi \cdot \langle\text{left}\rangle$, $\pi \cdot \langle\text{right}\rangle$ and $\pi$ without its last direction.

*Proof.* LEFT applies to $t = (l, x, r)$ (lines L2 and L3) and returns $(l, (\text{left}, x, r) :: p)$ (line L4). By definition $\text{plug}(l, (\text{left}, x, r) :: p) = \text{plug}((l, x, r), p) = T$, and the position is $\text{pos}(p) \cdot \langle\text{left}\rangle$. RIGHT is the same with $(\text{right}, x, l)$ and $\text{plug}(r, (\text{right}, x, l) :: p) = \text{plug}((l, x, r), p)$ (lines L5 and L6). UP applies to $p = (d, x, s) :: p'$ (lines L7 and L8). If $d = \text{left}$ it returns $((t, x, s), p')$ (line L9), and $\text{plug}((t, x, s), p') = \text{plug}(t, p) = T$; if $d = \text{right}$ it returns $((s, x, t), p')$ (line L10), and the same holds. The position is $\text{pos}(p')$, which is $\pi$ without its last direction. $\square$

**Lemma 3 (replace and top).** If $(t, p)$ represents $(T, \pi)$, then REPLACE$((t, p), t')$ represents $T$ with the subtree at $\pi$ replaced by $t'$, at the same position. TOP returns a zipper with an empty path whose focus is $T$.

*Proof.* Line L11 returns $(t', p)$, and Lemma 1 gives the first claim. TOP applies UP while the path is not nil (line L12). Each UP shortens the path by one and keeps the tree by Lemma 2, so the loop ends after $|p|$ steps with $(t'', \text{nil})$, and $t'' = \text{plug}(t'', \text{nil}) = T$. $\square$

**Theorem.** Every sequence of operations from `from_tree(T_0)` gives zippers whose represented trees and positions are those of the abstract type, `to_tree` returns the represented tree, and no operation changes what an existing zipper represents.

*Proof.* `from_tree(T_0)` returns $(T_0, \text{nil})$, which represents $T_0$ at the root. By Lemmas 2 and 3 each operation maps a zipper for $(T, \pi)$ to a zipper for the correct result, so by induction on the number of operations every zipper is correct, and `to_tree` returns the focus of TOP, which is the represented tree. No line writes to an existing node, crumb or path; each builds new cells that point to old ones. The meaning $\text{plug}(t, p)$ of a zipper depends only on the cells reachable from it, which never change, so every earlier zipper keeps its meaning. $\blacksquare$
