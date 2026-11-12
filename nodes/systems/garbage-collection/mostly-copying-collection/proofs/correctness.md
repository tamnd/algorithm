---
title: Mostly-copying collection keeps the reachable graph and moves no pinned object
proves: [correctness]
status: full
---

**Setting.** The heap is a set of pages, each with a space number or free. Before COLLECT, every object lies on a page with $space = current$. Each object has a precise layout: a known set of pointer fields, each null or the address of an object. The roots are a list of words. A root word is a *real root* if it is the address of an object; other words are noise, and the collector cannot tell the two apart. An object is *reachable* if a path of pointer fields leads to it from a real root. Let $Q$ be the final scan queue, $\Pi$ the set of pages promoted at line L4, and $K$ the set of objects on the pages of $\Pi$ at the start.

**Claim.** After COLLECT:

1. no object of $K$ has moved, and no root word has changed;
2. the retained objects are exactly $K$ and the copies made by line L10;
3. there is a map $\phi$ from the objects reachable from $K$ (by pointer fields, at the start) to retained objects, with $\phi(x) = x$ for $x \in K$ and $\phi(x)$ the copy of $x$ otherwise, such that every pointer field of $\phi(x)$ that held $y$ in $x$ now holds $\phi(y)$, and the data fields of $\phi(x)$ equal those of $x$;
4. every reachable object $x$ is in the domain of $\phi$, and $\phi(x) = x$ if a real root points to $x$.

**Proof.**

*Part 1.* Line L4 changes the space number of a page and nothing else; objects on it keep their addresses. Line L7 frees only pages whose space is not $next$, and the pages of $\Pi$ have space $next$. The collector reads the root words and never writes them.

*Part 2.* Pages get space $next$ only at line L4 (the pages of $\Pi$) or at line L10 (fresh pages that receive copies). Line L7 frees all other pages, so the retained objects are those on these two kinds of pages: the objects of $K$, and the copies.

*Invariant (Q).* Every object in $Q$ is in $K$ or is a copy, and every copy is in $Q$. Line L4 appends exactly the objects of promoted pages, and line L10 appends each copy when it is made.

*COPY returns $\phi$.* Define $\phi(x)$ for an object $x$ of the current space as $x$ if $x \in K$, and as the forwarding address of $x$ otherwise. We show that COPY$(x)$ returns $\phi(x)$ and that, after the call, $\phi(x)$ is defined. If $x$ is on a page with space $next$, then $x$ is in $K$ (copies are never passed to COPY as old objects, since each field is replaced at most once, see below), so line L8 returns $x = \phi(x)$. Otherwise $x$ is an object of the current space not in $K$. If it has a forwarding address, line L9 returns it. If not, line L10 makes exactly one copy, installs the address, and returns it. So each object of the current space outside $K$ is copied at most once, and the copy is unique.

*Each field is processed once.* An object enters $Q$ once: pages are promoted once (line L3 checks that the space is $current$, and line L4 changes it), and each copy is appended once. The loop of lines L5 and L6 visits each object of $Q$ once and replaces each of its pointer fields once. Before the replacement the field of a copy holds the same value as the field of its original, which is an object of the current space or null; the field of an object of $K$ holds an object of the current space or null. So COPY is always called with null or an object of the start heap, as used above.

*Part 3.* Let $x$ be reachable from $K$. By induction on the length of a shortest path from $K$, $\phi(x)$ is in $Q$: objects of $K$ are in $Q$ by line L4, and if $x \in Q$ (as $\phi$ of some object) has a pointer field to $y$, then processing that field calls COPY$(y)$, which defines $\phi(y)$ and puts it in $Q$ if it is a new copy. Since each object of $Q$ has all its pointer fields replaced by $\phi$ of their old values, and line L10 copies the data fields unchanged, the field condition holds for $\phi(x)$.

*Part 4.* Let $x$ be reachable, by a path $r, x_1, \ldots, x_m = x$ from a real root $r$. The word $r$ is the address of $x_1$, so it points into the page of $x_1$, which has space $current$ before any promotion. So line L3 promotes that page (or it was promoted by an earlier root word), and $x_1 \in K$, with $\phi(x_1) = x_1$. Then $x$ is reachable from $K$, so it is in the domain of $\phi$ by part 3. $\blacksquare$

**Consequence.** The program sees the same graph: a real root still holds the address of its object, which has not moved, and following pointer fields from it leads to the images under $\phi$ of the objects it led to before, with the same data. Noise words in the roots can only add pages to $\Pi$, and so retain more objects; they never cause an object to be lost or a word to change.
