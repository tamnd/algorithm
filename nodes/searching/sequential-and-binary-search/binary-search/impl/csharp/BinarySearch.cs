// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

namespace Algorithm;

/// <summary>Binary search in a sorted array.</summary>
public static class BinarySearch
{
    /// <summary>Returns an index i with a[i] == x, or -1 when x is not in a. The array must be sorted.</summary>
    public static int Search<T>(ReadOnlySpan<T> a, T x) where T : IComparable<T>
    {
        int lo = 0, hi = a.Length;              // @line L1
        while (lo < hi)                         // @line L2
        {
            int mid = lo + (hi - lo) / 2;       // @line L3
            int c = a[mid].CompareTo(x);
            if (c < 0)                          // @line L4
            {
                lo = mid + 1;                   // @line L5
            }
            else if (c > 0)                     // @line L6
            {
                hi = mid;                       // @line L7
            }
            else
            {
                return mid;                     // @line L8
            }
        }
        return -1;                              // @line L9
    }
}
