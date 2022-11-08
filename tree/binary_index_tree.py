from bisect import bisect_left, bisect_right
from typing import List
'''
<href>https://oi-wiki.org/ds/fenwick/</href>

1. 本质上使用大节点来代表一系列的小节点; 所以在计算前缀和时
(1) 查询操作: 通过查询 大节点 + 小节点 快速得出 -> 如何确定 大节点 管理的 小节点
(2) 更新操作: 更新 小节点 -> 跳到上一层较大节点更新 -> 更上一层大节点

2. 实现代码
(1) 大节点 i 管理的数据范围: [i - lowbit + 1, i] -> [i & (i - 1) + 1, i]
(2) 重要的位运算lowbit -> 快速计算得到数字 x 的 最低位的 1及其之后所有0组成的数组
    如果想要快速计算除了 lowbit 剩下的 x: x - lowbit  -> x & (x - 1)
    def lowbit(x: int) -> int:
        # 假设 x 为 1100; 将 x 取反为 0011, 再加1的到 0100; -> x & (~x + 1) = 100;
        # 根据补码可知, ~x + 1 = -x
        # x & (x - 1) = 1100 & 1011 = 1000 = x - lowbit

        lb = x & -x
        return lb
keys: 区间前缀和, 单点修改
tag: 树状数组
'''


'''
# 模板
from typing import List


class BIT:
    def __init__(self, n: int):
        self.tree = [0] * n

    # 更新操作，从小到大进行操作
    def add(self, i: int, val: int):
        while i < len(self.tree):
            self.tree[i] += val
            i += self.lowbit(i)
            # 或者是直接加入lowbit
            # i += i & -i

    # 查询操作，从小到达操作
    def query(self, i: int) -> int:
        ans = 0
        while i > 0:
            ans += self.tree[i]
            i -= self.lowbit(i)
            # 快速减去lowbit
            # i &= (i - 1)

        return ans

    # 求解lowbit
    def lowbit(self, i: int) -> int:
        return i & -i
'''

# 406 根据身高重建队列
# <href>https://leetcode.cn/problems/queue-reconstruction-by-height/</href>
'''
题目要求: 按照身高大小和人数进行排序
1.  首先我们将数组在 第一维进行排序; 按照从小到大排列
2.  之后将第二位降序排列
    理由对于 people[i][0]相同的数字(假设有K个)我们从右向左排序, 这么右边的数字不会被左边数字影响
    所以只需要快速得到连续K个位置就好了. 我们使用1来表示已经被占有的位置, 使用0表示没有被占有的位置
    为了快速得到 数组连续K个位置, 建议使用 二分+树状数组 的方式
3.  如何快速得到K的位置, 我们将使用过的位置记为1, 未使用的位置记为0.
4.  由于高度相同的位置, 前面人数 > 1, 则我们优先将其排列后, 其位置不会变
    维护一个区间内, 可以使用位置数量(随 位置变化 是一个单调递增的数组)
    使用树状数组维护当前位置已经使用的个数, 然后通过二分法快速查询某一个位置可用数量.
'''


class BIT:
    def __init__(self, n: int):
        self.tree = [0] * n

    def add(self, i: int, v: int):
        while i < len(self.tree):
            self.tree[i] += v
            i += i & -i

    def query(self, i: int) -> int:
        ans = 0
        # 注意此时避免为 0
        while i > 0:
            ans += self.tree[i]
            i &= i - 1
        return ans


class RebuildQueue:
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        # 第一维升序，第二维降序
        people.sort(key=lambda x: (x[0], -x[1]))

        # 为了优化运算，此时数组长度要声明为 n，第一个元素从1开始
        n = len(people) + 1
        bit = BIT(n)
        ans = [[0, 0] for _ in range(n - 1)]
        for p in people:
            left, right = 1, n
            k = p[1]
            # bit.query(mid)代表mid位置及之前已经使用个数，总长度为 mid
            # mid - bit.query(mid): 剩下可用的位置 > k，right = mid
            while left < right:
                mid = (left + right) // 2
                if mid - bit.query(mid) >= k + 1:
                    right = mid
                else:
                    left = mid + 1
            ans[right - 1] = p
            # 更新right及之前的已使用的个数，每个区间 加 1
            bit.add(right, 1)

        return ans


# 题目描述 剑指 Offer 51. 数组中的逆序对
# https://leetcode.cn/problems/shu-zu-zhong-de-ni-xu-dui-lcof/

'''
1.  题目中要求得到逆序对个数。假设当前数字为 num, 我们想要计算, 在num之后的数字的个数
2.  我们需要计算之后的个数, 首先采用倒序遍历, 将 num 之后的数字加入
3.  由于加入过程中 num可能存在比较大的情况, 我们采用相对位置(离散化的方式加入)
4.  此时采用倒序遍历到数字num, 其离散化下标为 idx + 1
    我们需要查询数字之后的所有数字的个数(已经插入的数字 = 倒序遍历已经加入到树状数字的数字)
    所以只需要直接查询 query(idx), 并将 idx + 1插入
ps. 离散化解释: 将 nums 数组进行排序, 然后将其下标作为数字记录

'''


class CountPairs:

    def reversePairs(self, nums: List[int]) -> int:
        n = len(nums)
        bit = BIT(n + 1)

        # 进行离散化处理
        tmp = sorted(nums)
        ans = 0
        for i in range(n - 1, -1, -1):
            idx = bisect_left(tmp, nums[i])
            ans += bit.query(idx)
            bit.add(idx + 1, 1)
        return ans


# 307. 区域和检索 - 数组可修改
# https: // leetcode.cn/problems/range-sum-query-mutable/

class NumArray:

    def __init__(self, nums: List[int]):
        # 要记录原数组, 为了更新时使用
        self.nums = nums
        self.bit = BIT(len(nums) + 1)
        for i, v in enumerate(nums):
            self.bit.add(i + 1, v)

    def update(self, index: int, val: int) -> None:
        # 更新操作
        ori_val = self.nums[index]
        self.bit.add(index + 1, val - ori_val)
        self.nums[index] = val

    def sumRange(self, left: int, right: int) -> int:
        return self.bit.query(right + 1) - self.bit.query(left)


# 2426.满足不等式的数目
# https://leetcode.cn/problems/number-of-pairs-satisfying-inequality/

'''
0 <= i < j <= n - 1 && nums[i] <= nums[j] + diff  -> 逆序对个数
nums[i] <= nums[j] + diff -> 对于当前遍历的 num <= num + diff
            所以需要查询右边界 得到 idx, 此时不需要 - 1
            在当前位置加入 x, 需要得到 查询 等于x的位置,进行 + 1操作
'''


class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], diff: int):
        nums = [x - y for x, y in zip(nums1, nums2)]
        tmp = sorted(nums)

        ans = 0
        t = BIT(len(nums) + 1)
        '''
        下面代码为 >= 的写法, 由于是前缀和, 我们一般采用 <= 的写法
        for i in range(n - 1, -1, -1):
            left = bisect_left(tmp, nums[i] - diff)
            ans += bit.query(n) - bit.query(left)
            idx = bisect_left(tmp, nums[i])
            bit.add(idx + 1, 1)
        '''
        for x in nums:
            idx = bisect_right(tmp, x + diff)
            ans += t.query(idx)
            insert_idx = bisect_left(tmp, x)
            t.add(insert_idx + 1, 1)
        return ans
