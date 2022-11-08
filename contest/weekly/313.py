'''
weekly contest 313

1. 求两个数字的公因子数目
(1) gcd(x, y) -> gcd(y, x % y) -> 其中 x > y
(2) 枚举最大公因子的因子, 计算数量
2. 模拟
3. 位元算
(1) lowbit: 求最低位的1及后面的0, x -= x & -x == x & x - 1
(2) 根据题目要求首先得到 cnt2: 数字2中1的个数, 为了让 x xor num1最小, 需要从高位把1抵消掉
    if cnt2 < cnt1:
        则从nums1的高位抵消, 低位的1需要减去 nums1 - lowbit(nums1) = nums1 & nums1 - 1;
    else:
        需要将nums1的低位0 -> 1, 由于减去lowbit是 nums &= num - 1;
        低位0变为1变为 nums |= nums + 1

4. 动态规划
(1) 首先根据数据范围猜测大概为 n^2 的时间复杂度
(2) 由于对于字符串 s 的进行删除操作后 -> 更小的 s 的操作
(3) 递推公式为: f[i] = f[i + j] + 1 if s[i: i + j] == s[i + j: i + 2 * j]
    如何快速判断 s[i: i + j] == s[i + j: i + 2 * j]
(4) lcp[i][j]: 为字符串s从i下标开始 与 从j开始两个字串相等字符串长度
    lcp[i][j] = lcp[i + 1][j + 1] + 1    if s[i] == s[j]
              = 0                        else s[i] != s[j]
(5) 递推公式变为
    f[i] = f[i + j] + 1 if lcp[i][j] >= j
         = 1            else
标签:
    1. 求公约数, 辗转相除法
    2. 模拟
    3. 位元算lowbit
    4. 动态规划, 快速判断两个子字符串是否相等
'''

# 1979. 找出数组的最大公约数
# https://leetcode.cn/problems/find-greatest-common-divisor-of-array/

from math import gcd
from typing import List


class find_gcd:
    def findGcd(self, nums: List[int]) -> int:
        def gcd(x: int, y: int) -> int:
            if y == 0:
                return x
            return gcd(y, x % y)

        mx = max(nums)
        mn = min(nums)
        return (mx, mn)


# 2427. 公因子的数目
# https://leetcode.cn/problems/number-of-common-factors/


class CommonFactorsSolution:
    def commonFactors(self, a: int, b: int) -> int:
        g = gcd(a, b)

        ans, i = 0, 1
        while i * i <= g:
            if g % i == 0:
                ans += 1
                # 因为因子有两个，所以此时需要在加上一个
                if i * i < g:
                    ans += 1

            i += 1

        return ans


# 2428. 沙漏的最大总和
# https://leetcode.cn/problems/maximum-sum-of-an-hourglass/


class MaxSumSolution:
    def maxSum(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            grid[i] = [0] + grid[i]

        for i in range(m):
            for j in range(1, n + 1):
                grid[i][j] = grid[i][j - 1] + grid[i][j]

        ans = 0
        for i in range(m - 2):
            for j in range(3, n + 1):
                tmp = 0
                tmp += grid[i][j] - grid[i][j - 3]
                tmp += grid[i + 1][j - 1] - grid[i + 1][j - 2]
                tmp += grid[i + 2][j] - grid[i + 2][j - 3]
                ans = max(tmp, ans)

        return ans


# 2429. 最小 XOR
# https://leetcode.cn/problems/minimize-xor/


class MinimizeXorSolution:
    def minimizeXor(self, nums1: int, nums2: int):
        # 得到nums2中二进制1的个数
        cnt2 = nums2.bit_count()
        # 得到nums1中二进制的总长度
        # len1 = nums1.bit_length()
        cnt1 = nums1.bit_count()
        # # 如果此时nums2中1的个数溢出
        # if cnt2 >= len1:
        #     return 2 ** cnt2 - 1

        # 如果此时nums2中1的个数 < nums1中1的个数
        while cnt2 < cnt1:
            nums1 &= nums1 - 1
            cnt2 += 1

        # nums1中1的个数 < 如果num2中1的个数 <= nums1的二进制长度
        while cnt1 < cnt2:
            nums1 |= nums1 + 1
            cnt1 += 1
        return nums1


# 2430. 对字母串可执行的最大删除数
# https://leetcode.cn/problems/maximum-deletions-on-a-string/


'''
1.  首先根据数据范围猜测大概为 n^2 的时间复杂度
2.  由于对于字符串 s 的进行删除操作后 -> 更小的 s 的操作
3.  递推公式为: f[i] = f[i + j] + 1 if s[i: i + j] == s[i + j: i + 2 * j]
    如何快速判断 s[i: i + j] == s[i + j: i + 2 * j]
4.  lcp[i][j]: 为字符串s从i下标开始 与 从j开始两个字串相等字符串长度
    lcp[i][j] = lcp[i + 1][j + 1] + 1    if s[i] == s[j]
              = 0                        else s[i] != s[j]
5.  递推公式变为
    f[i] = f[i + j] + 1 if lcp[i][j] >= j
         = 1            else
'''


class DeleteStringSolution:
    def deleteString(self, s: str) -> int:
        # 首先先计算 lcp
        n = len(s)
        lcp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            # 此时 i < j lcp[i][j] = lcp[i + 1][j + 1] + 1
            for j in range(n - 1, i, -1):
                if s[i] == s[j]:
                    lcp[i][j] = lcp[i + 1][j + 1] + 1

        # 之后计算f[i] = f[i + j] + 1
        # 默认初始化的值为 1
        f = [1] * n
        for i in range(n - 1, -1, -1):
            # i + 2 * j <= n
            for j in range(1, (n - i) // 2 + 1):
                if lcp[i][j] >= j:
                    f[i] = max(f[i + j] + 1, f[i])
        return f[0]
