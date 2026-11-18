# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-matching-segmentation/. The authors are listed in prov/ZZTPQ8.jsonl.

"""Maximum matching word segmentation with a trie.

forward_max_match is the algorithm of the page: from left to right, take the
longest dictionary word that starts at the current position, or one character
when no word starts there. backward_max_match does the same from right to
left, and bidirectional_max_match picks one of the two results by a fixed rule.
unigram_segment is the dynamic program over positions that the page compares
with the greedy method. Indices are 0-based and s[i:j] is the span (i, j).
"""

from typing import Dict, Iterable, List, Mapping, Optional, Tuple

from nlslog import NEG_INF, VITERBI, safe_log

END = ""  # key of the end-of-word mark in a trie node; no edge has an empty label


def build_trie(words: Iterable[str]) -> Dict[str, dict]:
    """Return a trie of the nonempty words, as nested dicts keyed by character.

    A node that ends a word has the key END. Cost: O(L) time and space for
    words of total length L.
    """
    root: Dict[str, dict] = {}
    for w in words:
        if not w:
            raise ValueError("the dictionary holds the empty word")
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node[END] = {}
    return root


def longest_match_end(s: str, i: int, trie: Mapping[str, dict]) -> int:
    """Return the largest j > i with s[i:j] in the dictionary, or i + 1 if there is none.

    Precondition: 0 <= i < len(s). Cost: O(min(len(s) - i, m)) steps for
    dictionary words of length at most m.
    """
    n = len(s)
    v, j, k = trie, i + 1, i  # @line L3
    while k < n and s[k] in v:  # @line L4
        v, k = v[s[k]], k + 1  # @line L5
        if END in v:  # @line L6
            j = k
    return j


def forward_max_match(s: str, trie: Mapping[str, dict]) -> List[str]:
    """Segment s by forward maximum matching.

    Each word is the longest dictionary word that starts where the previous
    word ends. Where no dictionary word starts, the word is one character.
    Cost: O(n m) time for len(s) = n and dictionary words of length at most m.
    """
    i, out = 0, []  # @line L1
    n = len(s)
    while i < n:  # @line L2
        j = longest_match_end(s, i, trie)
        out.append(s[i:j])  # @line L7
        i = j  # @line L8
    return out  # @line L9


def backward_max_match(s: str, words: Iterable[str]) -> List[str]:
    """Segment s by backward maximum matching, from the right end to the left.

    It is forward matching on the reversed string with the reversed words.
    Cost: O(n m) time after an O(L) trie build.
    """
    rtrie = build_trie(w[::-1] for w in words)
    return [w[::-1] for w in reversed(forward_max_match(s[::-1], rtrie))]


def _bidirectional_key(seg: List[str], known: set) -> Tuple[int, int, int]:
    unknown = sum(1 for w in seg if w not in known)
    single = sum(1 for w in seg if len(w) == 1)
    return (len(seg), unknown, single)


def bidirectional_max_match(s: str, words: Iterable[str]) -> List[str]:
    """Run both directions and keep one result.

    The rule: fewer words, then fewer characters left outside the dictionary,
    then fewer one-character words, and the backward result on a full tie.
    This rule is a heuristic, not an optimum of any model.
    """
    words = list(words)
    known = set(words)
    fw = forward_max_match(s, build_trie(words))
    bw = backward_max_match(s, words)
    if _bidirectional_key(fw, known) < _bidirectional_key(bw, known):
        return fw
    return bw


def unigram_segment(s: str, prob: Mapping[str, float]) -> Optional[Tuple[List[str], float]]:
    """Return a most probable segmentation of s under a unigram model, and its log probability.

    Every word must be a key of prob with a positive value. The score of a
    segmentation is the sum of the log probabilities of its words. This is a
    Viterbi recursion over the positions 0 to n: best[j] is the best score of
    a segmentation of s[0:j]. Ties go to the smallest last start i. Return
    None if s has no segmentation into dictionary words. Cost: O(n m) trie
    steps and O(n) space for the table and the back pointers.
    """
    n = len(s)
    trie = build_trie(prob)
    best = [NEG_INF] * (n + 1)
    best[0] = VITERBI.one
    back = [-1] * (n + 1)
    for i in range(n):
        if best[i] == NEG_INF:
            continue
        v, k = trie, i
        while k < n and s[k] in v:
            v, k = v[s[k]], k + 1
            if END in v:
                cand = VITERBI.times(best[i], safe_log(prob[s[i:k]]))
                if cand > best[k]:
                    best[k], back[k] = cand, i
    if best[n] == NEG_INF and n > 0:
        return None
    out: List[str] = []
    j = n
    while j > 0:
        out.append(s[back[j] : j])
        j = back[j]
    out.reverse()
    return out, best[n]
