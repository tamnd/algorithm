---
title: The symmetry index of the tablebase is well defined, and a probe returns the exact value and distance to mate
proves: [correctness, complexity]
status: full
---

We use the operations TB-INDEX, TB-BUILD and TB-PROBE of the page, on the toy king and rook against king on a 4 by 4 board. Let $G$ be the group of the 8 maps of the square board onto itself: the 4 rotations and the 4 reflections. A map $g \in G$ acts on a position $p = (k, r, k', s)$, with the white king $k$, the rook $r$, the black king $k'$ and the side to move $s$, by $g p = (g k, g r, g k', s)$.

**Lemma 1 (the rules are symmetric).** For every $g \in G$, $p$ is legal exactly when $g p$ is legal, $q$ is a move of $p$ exactly when $g q$ is a move of $g p$, and $p$ is a mate exactly when $g p$ is a mate.

*Proof.* Each $g$ is a bijection of the squares that keeps the distance $\max(|\Delta r|, |\Delta c|)$ between squares, so it keeps king steps and adjacency. It maps each row or column onto a row or column and keeps the order of the squares on it, up to reversal, so it keeps the squares a rook reaches and the first piece on each ray. Legality, the moves, check and mate are defined only from these. $\square$

**Lemma 2 (values are symmetric).** For every $g \in G$, $p$ and $g p$ have the same value and the same distance to mate.

*Proof.* By Lemma 1, $g$ maps the sets $W_n$ and $L_n$ of the page on [retrograde analysis](/retrograde-analysis/) onto themselves, by induction on $n$: $L_0$ is the set of mates, and the conditions for $W_n$ and $L_n$ are about the moves, which $g$ keeps. $\square$

**Lemma 3 (the index).** Let $\text{canon}(p)$ be the image $g p$ that is least in the order that compares first the pair of kings and then the rook. Then $\text{canon}(h p) = \text{canon}(p)$ for every $h \in G$, and TB-INDEX gives two positions the same index exactly when one is the image of the other under some $g \in G$.

*Proof.* The images of $h p$ are $\{g h p : g \in G\} = \{g p : g \in G\}$, because $G$ is a group, so the least one is the same. The index of line L2 is $(c \cdot 16 + r_0) \cdot 2 + s$, where $c$ numbers the class of the canonical pair of kings and $r_0$ is the canonical rook. This is a one-to-one map from the canonical positions to numbers, because the pair $(c, r_0, s)$ determines the canonical position: the canonical pair of kings is the least of its class, so $c$ determines it. So equal indexes mean equal canonical forms, that is, positions in one orbit. $\square$

**Theorem 4 (build and probe).** TB-PROBE$(p)$ returns the value of $p$ for the side to move and its distance to mate, for every legal $p$.

*Proof.* TB-BUILD runs the layered retrograde analysis on the canonical positions. The children of a class are the classes of the children of its representative, and the predecessors of a class are the classes of the predecessors of all positions in its orbit; by Lemma 1 this is the set of classes with a move into the class. By Lemma 2, all positions of a class have one value, so a class is won when some child class is lost, and lost when it has moves and every child class is won. The counter of a class counts its distinct child classes, so it reaches 0 exactly when every child class is won. The proof of correctness of retrograde analysis then holds word for word on the classes, and gives each class the least $n$ with its positions in $W_n$ or $L_n$. Line L4 stores the code of the value and the distance at the index of the class. The code of the page is one to one, since it keeps the distance and the value in separate parts of the byte. By Lemma 3, TB-PROBE reads the entry of the class of $p$ and decodes it. $\square$

The tests compare every probe with a forward computation of $W_n$ and $L_n$ on all 3,496 positions with no use of symmetry, for the toy and for the variant in which the white king may not move, which has draws by endless play. They also check that the 8 images of each position get the same index and the same entry.

**Counting the king placements.** A class of $G$ has at most 8 elements. The tests count the classes of the legal pairs of kings, distinct and not adjacent: 21 on the 4 by 4 board, and 462 on the 8 by 8 board. With pawns, only the left-right mirror keeps the rules, and the counts are 78 and 1,806.

**Cost.** TB-INDEX tries the 8 maps, so it takes $O(1)$ time, as does TB-PROBE. The table has $21 \cdot 16 \cdot 2 = 672$ bytes, against $16^3 \cdot 2 = 8{,}192$ for the plain index $(k, r, k', s)$; 443 entries are used, one per class. The other entries are never written: the rook would stand on a king, the position is illegal, or a symmetry keeps the pair of kings and maps the rook to a smaller square, so the rook square is not canonical. TB-BUILD takes $O(v + e)$ steps for $v$ classes and $e$ moves between classes, each with $O(1)$ work for the maps, as in retrograde analysis. $\blacksquare$
