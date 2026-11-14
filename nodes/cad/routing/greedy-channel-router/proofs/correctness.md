---
title: The greedy channel router of this page returns a legal routing of every channel, with at most as many extension columns as tracks
proves: [correctness, connectivity, termination, bound on extension columns, density bound]
status: full
---

Call the state at a column the list of tracks in order from the top, with the net that each track holds, or none. A track is *live* for net $x$ when it holds $x$. The router builds wires of three kinds in column $c$: the branches of the pins (line L3), the jogs between tracks of one net (lines L4 and L5), and the trunks, where a trunk of $x$ on track $t$ runs from the column where $x$ took $t$ to the column where $t$ was freed. Rows of tracks are fixed only at line L8, which removes empty tracks and keeps the order, so it changes no relation between wires.

**Lemma 1 (layer H).** No point of layer H holds two nets.

*Proof.* A track holds at most one net at a time. A net $x$ takes a track $t$ in column $c$ only when $t$ is empty: in line L3 the pin goes to a track that is empty or already holds $x$, and in line L5 the target must be empty. Line L5 also rejects every track freed in column $c$, and line L3 of column $c$ runs before any track is freed in column $c$. So if $t$ was freed in column $c'$, the old trunk ends at $c'$ and the new one starts at some $c \ge c' + 1$. The two trunks on $t$ do not share a column. $\square$

**Lemma 2 (layer V).** No point of layer V holds two nets.

*Proof.* In column $c$, line L3 makes at most two branches: the top pin $a$ from row 0 to its track $i$, and the bottom pin $b$ from its track $j$ to the bottom row. If $a \ne b$ and $i$ is not above $j$, line L3 gives one of the pins a new track at the edge of its own side, so afterwards $i$ is above $j$ and the two branches are disjoint. Every jog of lines L4 and L5 is added only when the rows it spans are free in column $c$ of every other net, and the jogs added so far in column $c$ are counted as used. So each new vertical wire avoids all earlier ones of other nets. $\square$

**Lemma 3 (components).** After each column, every connected part of the wire built so far for a net $x$ contains a live track of $x$.

*Proof.* By induction over the steps. A pin of $x$ that enters on a live track of $x$ joins that part. A pin that enters on an empty track makes a new part, and the track becomes live. A jog joins two parts, and both keep their live tracks. Line L4 frees tracks only inside a joined set, and it keeps one track of each set, so each part keeps a live track. Line L5 adds a jog from the only track $p$ of $x$ to an empty track, makes that track live and then frees $p$, so the part keeps a live track. Line L6 frees the only track of $x$, and then $x$ has no part left to keep. $\square$

**Theorem 1 (legal routing).** When the router stops, every net is connected and holds all its pins, and no point of a layer holds two nets.

*Proof.* Lemmas 1 and 2 give the second claim. Each pin is joined by its branch to a track of its net in its column. A net that holds no track has been freed by line L6, which needs one live track and no pin to the right. At that moment, by Lemma 3, every part of its wire holds that one track, so the wire is connected, and it holds all pins, since all of them are at or left of the current column. The loop of line L2 stops only when no track holds a net, so every net that has a pin is freed by then. $\square$

**Theorem 2 (completion).** The router stops after at most $T_n$ extension columns, where $T_n$ is the number of tracks that hold a net after column $n$. So $E \le T$.

*Proof.* In an extension column there are no pins. Suppose some track holds a net after the column before. If no net is on two or more tracks, every net holds one track and has no pin to the right, and line L6 frees them all, so the loop stops. Otherwise let $x$ be split. In line L4 no vertical wire exists yet in this column, so the first jog in the order is accepted, and the set it joins keeps one track and frees at least one. No step of an extension column takes an empty track except line L5, which frees the old track of the net in the same step. So the number of tracks that hold a net falls by at least 1 in each extension column, and after at most $T_n$ such columns it is 0. $\square$

**Theorem 3 (density bound).** The router uses at least $d$ tracks.

*Proof.* By Theorem 1 the result is a legal routing in the reserved two-layer model, within the columns of the channel and the extension columns. The density bound of the page on channel density holds for every such routing, so it has at least $d$ tracks. $\square$

**Theorem 4 (running time).** With a table of the next pin of each net and an array of the rows of column $c$ used on layer V, each column takes $O(T^2)$ time, and the router takes $O((n + E) T^2)$ time.

*Proof.* Line L3 scans the tracks from each edge once, in $O(T)$. Line L4 has fewer than $T$ jog candidates, and each is checked and marked in $O(T)$. Line L5 scans at most $T$ rows for each of at most $T$ nets, and the clearness of a growing range is checked one row at a time. Line L6 looks at each track once. Line L3 adds at most two tracks per column, so $T \le d + 2n$ stays finite. $\square$

**Tests.** No exhaustive optimum is used here, because the model with jogs in any column has too many routings to search. The tests run a geometric checker on every result, check that it rejects routings with a branch removed or with a wire given to another net, check that the number of tracks is at least $d$, and check the channels of the page.
