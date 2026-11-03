// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

using Algorithm;
using Xunit;

public class BinarySearchTests
{
    [Theory]
    [InlineData(23, 5)]
    [InlineData(2, 0)]
    [InlineData(91, 9)]
    [InlineData(30, -1)]
    [InlineData(1, -1)]
    [InlineData(100, -1)]
    public void Examples(long x, int want)
    {
        long[] a = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91];
        Assert.Equal(want, BinarySearch.Search<long>(a, x));
    }

    [Fact]
    public void Edges()
    {
        Assert.Equal(-1, BinarySearch.Search<long>(Array.Empty<long>(), 1));
        Assert.Equal(0, BinarySearch.Search<long>(new long[] { 7 }, 7));
        Assert.Equal(1, BinarySearch.Search<string>(new[] { "ant", "bee", "cat" }, "bee"));
    }

    [Fact]
    public void RandomAgainstLinearScan()
    {
        var rng = new Random(2150);
        for (int t = 0; t < 2000; t++)
        {
            var a = new long[rng.Next(31)];
            for (int i = 0; i < a.Length; i++) a[i] = rng.Next(41) - 20;
            Array.Sort(a);
            long x = rng.Next(51) - 25;
            int got = BinarySearch.Search<long>(a, x);
            if (Array.IndexOf(a, x) >= 0) Assert.Equal(x, a[got]);
            else Assert.Equal(-1, got);
        }
    }
}
