---
title: The Boehm-Demers-Weiser collector frees no reachable object, and blacklisted blocks are not reused
proves: [correctness]
status: full
---

**Setting.** The heap is an array of blocks. A block is free, or it holds $c = \lfloor B / s \rfloor$ object slots of size $s$ and one kind, normal or atomic, each with an allocated bit and a mark bit. Let $A$ be the set of allocated slots. A word $w$ *hits* a slot $o \in A$ if $w$ is an address of a word of $o$ and, when interior pointers are off, $w$ is the first word of $o$. The free lists are $F[s, k]$. The program holds a set of root words. A root word or a word of a normal object is a *real pointer* if the program will use it to reach an object; we assume, as the collector must, that every real pointer hits the object it refers to, and that atomic objects hold no real pointers. An object is *reachable* if a path of real pointers leads to it from a root.

**Invariant (F).** Every slot on a free list is in a block in use, with the size and kind of that list, and is not in $A$. No slot is on two free lists, or twice on one.

**Claim.** Assume (F) and that no mark bit is set before COLLECT. Then:

1. after COLLECT, $A$ is exactly the set $M$ of slots marked by lines L5 and L6, and $M$ is the least set of allocated slots that contains every slot hit by a root word and every slot hit by a word of a normal slot in $M$;
2. every reachable object is in $M$, and COLLECT changes no word of any object;
3. the blacklist after COLLECT is exactly the set of free blocks that some word tested at line L9 points into;
4. (F) holds after COLLECT, after REFILL and after ALLOCATE, and ALLOCATE returns a slot that was not in $A$;
5. REFILL makes a blacklisted block live only if every free block is blacklisted.

**Proof.**

*Part 1.* MARK-IF-POINTER$(w)$ marks and pushes the slot that $w$ hits, if $w$ hits one and it is not yet marked (line L10). Each slot is pushed at most once, because it is marked when it is pushed and never unmarked during marking. So the loop at line L6 ends, and pops each marked slot once. Every marked slot was hit by a root word (line L5) or by a word of a normal marked slot (line L6), so $M$ is contained in the least set described. Conversely, every root word is tested, and every word of every normal slot in $M$ is tested when the slot is popped, so every slot hit by such a word is marked: $M$ is closed, and so it contains the least set. Line L8 clears the allocated bit of exactly the unmarked slots of blocks in use, and frees blocks with no marked slot, which hold no slot of $M$. So $A = M$ after the sweep.

*Part 2.* Let $x$ be reachable by a path $r = x_0, x_1, \ldots, x_m = x$, where $r$ is a root word that is a real pointer to $x_1$, and for $i \geq 1$, $x_i$ holds a real pointer to $x_{i+1}$. A slot that holds a real pointer is normal, by the assumption. By the assumption, $r$ hits $x_1$, so $x_1 \in M$ by part 1. If $x_i \in M$, then $x_i$ is normal and holds a word that hits $x_{i+1}$, so $x_{i+1} \in M$. By induction, $x \in M$, and by part 1 it stays allocated. COLLECT writes only mark bits, allocated bits, block headers, the free lists and the blacklist; it never writes a word of an object.

*Part 3.* Line L4 empties newBlacklist. Line L11 adds block $b$ exactly when the tested word is a heap address in block $b$ and $b$ is free; a word into a free block cannot hit a slot, so line L10 does not take it first. No block becomes free or live during marking, so the test is the same at every call. Line L7 copies newBlacklist to the blacklist (the model with blacklisting off sets it to $\emptyset$).

*Part 4.* After COLLECT, line L8 rebuilds every free list from scratch: each slot put on $F[s, k]$ is an unmarked slot of a block in use with size $s$ and kind $k$, its allocated bit is cleared, and each slot is visited once. Blocks freed at line L8 contribute no slot. So (F) holds. REFILL takes a free block, which has no slot on any list; it gives the block size $s$ and kind $k$, with all allocated bits clear, and puts each of its $c$ slots once on $F[s, k]$, so (F) still holds. If REFILL calls COLLECT first, (F) holds after it, and REFILL may return at once if the sweep refilled $F[s, k]$. ALLOCATE pops a slot $o$ from $F[s, k]$; by (F), $o \notin A$. It sets the allocated bit of $o$ and removes it from the list, so (F) holds, since $o$ was on no other list. Clearing the words of $o$ changes no allocated object.

*Part 5.* REFILL first picks among the free blocks that are not on the blacklist. Only if there is none, after a collection that rebuilds the blacklist, does it take any free block, and then every free block is blacklisted. $\blacksquare$

**Consequence.** Parts 2 and 4 together say that a reachable object is never freed and never handed out again, and that its words change only when the program writes them: the collector is safe. Part 1 says what it keeps: the closure of the pointer-looking words, which may be more than the reachable objects. Parts 3 and 5 give the purpose of blacklisting: if a word $w$ points into a free block $b$ at a collection, then no object is placed in $b$ before the next collection unless memory is exhausted, so $w$ cannot falsely retain an object allocated in that interval. A false reference that survives to the next collection blacklists $b$ again, as long as $b$ is still free.
