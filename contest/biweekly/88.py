'''
biweekly contest 88

1. 暴力法 -> 对于数据范围较小的，可以考虑使用暴力法解决
(1) Counter(): 方法返回一个频率的map, popitem(): 随机剔除一个元素
(2) 如果想要实现o(n)的频率,考虑使用两个map, count: 记录key出现频率.
freq: 记录value出现频率, 以及最大频率max_freq.

2. 最长序列不会下降. 使用last记录上次遍历的位置

3. 集合异或
(1) 两个集合每个元素与另一个集合xor, 结果再次xor
(2) A:[a, b, c], B:[d,e]
-> a^d, a^e, b^d, b^e, c^d, c^e
-> (a^d)^(a^e)^(b^d)^(b^e)^(c^d)^(c^e)
(3) 从上述结果可知 A中元素出现次数为B中元素个数,如果B中个数为偶数,则A中元素全部消除
同理, B中元素也是如此
(4) reduce聚合处理, 第一个参数为方法名称或者是操作符, 第二个参数为集合

4. nums1[i] - nums2[i] <= nums1[j] - nums2[j] + diff -> A[i] <= B[j] + diff
(1) 求类似于逆序对的形式， 采用归并排序的求解方式
(2) 树状数组 


标签:
    暴力法, 根据数据范围而定;
    不断递增的遍历, 使用last变量维护. for与while的区别;
    异或的特征, 相同数据结果为0.
    类逆序对 -> 归并排序的方式; 树状数组;

'''

# 6212. 删除字符使频率相同
# https://leetcode.cn/problems/remove-letter-to-equalize-frequency/
from ast import List
from functools import reduce
from operator import xor
from typing import Counter


def equeal_frequency(self, word: str) -> bool:
    # 1. leetocde前面的题目，首先要看数据范围
    # 2. 本次数据范围为100之内，考虑使用暴力法解决

    # 方法一: 不使用python的api

    # 统计字频数组
    # def cntFreq(word: str) -> List[int]:
    #     ans = [0] * 26
    #     n = len(word)
    #     for _, v in enumerate(n):
    #         idx = ord(v) - ord('a')
    #         ans[idx] += 1

    #     return ans

    # word_len = len(word)
    # for i in range(word_len):
    #     s = word[:i] + word[i + 1:]
    #     cnt = cntFreq(s)
    #     c = 0
    #     # 寻找第一个非零频率
    #     for i in cnt:
    #         if i != 0:
    #             c = i
    #             break

    #     # 如果全部等于则返回True
    #     sign = True
    #     for v in cnt:
    #         if v != 0 and v != c:
    #             sign = False
    #             break
    #     if sign: return True

    # return False

    # 方法二: 使用api
    n = len(word)
    for i in range(n):
        # 返回一个map
        cnts = Counter(word[:i] + word[i + 1:])
        # 随机删除一个键值对
        pivot = cnts.popitem()
        # 如果全部相等
        if all(c == pivot for c in cnts.values()):
            return True

    return False


# 1224. 最大相等频率
# 上述题目的衍生题目，使用o(n)解决
def max_equal_freq(self, nums: List[int]) -> bool:

    return 0


# 6197.最长上传前缀
# https://leetcode.cn/problems/longest-uploaded-prefix/

class LUPrefix:
    # 最长上传前缀不会变小，使用变量记录当前最新的传输位置

    def __init__(self, n: int):
        # 存储所有上传的id
        self.s = set()
        # 记录当前的空位
        self.last = 1

    def upload(self, video: int) -> None:
        self.s.add(video)

    def longest(self) -> int:
        # 如果当前位置已经上传，向后移动
        # 此时使用while,理由是如果不存在则此循环结束；使用while意味着遍历所有的数据
        while self.last in self.s:
            self.last += 1
        # 最大的传输位置 = 当前需要传输位置 - 1
        return self.last - 1


# 2425. 所有数对的异或和
# https://leetcode.cn/problems/bitwise-xor-of-all-pairings/

def xor_all_nums(self, nums1: List[int], nums2: List[int]) -> int:
    ans = 0
    n1 = len(nums1)
    n2 = len(nums2)
    # 将所有的元素与ans进行异或操作
    # reduce会对所有元素进行累计操作 -> 第一个参数可以是方法，也可以是操作符，第二个为集合
    if n1 % 2:
        ans ^= reduce(xor, nums2)
    if n2 % 2:
        ans ^= reduce(xor, nums1)
    return ans


# 2426.满足不等式的数目
# https://leetcode.cn/problems/number-of-pairs-satisfying-inequality/
# 0 <= i < j <= n - 1 && nums1[i] - nums2[i] <= nums1[j] - nums2[j] + diff
# 0 <= i < j <= n - 1 && nums[i] <= nums[j] + diff  -> 逆序对个数


def numberOfPairs(self, nums1: List[int], nums2: List[int], diff: int) -> int:
    def countPairs(arr: List[int]) -> int:
        if len(arr) == 1:
            return 0
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        ans = countPairs(left) + countPairs(right)

        cur = i = j = 0
        left_len, right_len = len(left), len(right)
        for x in right:
            while i < left_len and left[i] <= x + diff:
                i += 1
            ans += i
        while True:
            if i == left_len:
                arr[cur:] = right[j:]
                break
            if j == right_len:
                arr[cur:] = left[i:]
                break
            if arr[i] <= arr[j]:
                arr[cur] = arr[i]
                cur += 1
                i += 1
            else:
                arr[cur] = arr[j]
                cur += 1
                j += 1
        return ans

    nums = [x - y for x, y in zip(nums1, nums2)]
    return countPairs(nums)


# 剑指 Offer 51. 数组中的逆序对
# https://leetcode.cn/problems/shu-zu-zhong-de-ni-xu-dui-lcof/
# nums[i] >= nums[j] && 0 <= i < j <= n
# 采用分治的思想


def reversePairs(arr: List[int]) -> int:
    def merge_sort(nums: List[int]) -> int:
        if len(nums) == 1:
            return 0

        mid = len(nums) // 2
        # [i:j]是一个左闭右开区间，
        left = nums[:mid]
        right = nums[mid:]

        # ans = 左边逆序对个数 + 右边逆序对个数
        ans = merge_sort(left) + merge_sort(right)

        # 通过双指针的方法求 交叉的逆序对个数
        i, left_len = 0, len(left)
        j, right_len = 0, len(right)

        # 排序的下标变量
        cur = 0

        while i < left_len and j < right_len:
            if left[i] <= right[j]:
                nums[cur] = left[i]
                i += 1
                cur += 1
            else:
                nums[cur] = right[j]
                # 左侧数字 > 右侧数字 -> 从当前数字到最后全部计算进去
                ans += left_len - i
                j += 1
                cur += 1

        # 此时不需要计算逆序对个数
        while i < left_len:
            nums[cur] = left[i]
            i += 1
            cur += 1
        while j < right_len:
            nums[cur] = right[j]
            j += 1
            cur += 1
        return ans
    return merge_sort(arr)
