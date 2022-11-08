'''
# 补充完整
1. 根节点为 1, 1, n,      左节点定义: left_node =  2 * root_idx
                        右节点定义: right_node = 2 * root_idx + 1
2. 根节点为 0, 0, n-1    左节点定义: left_node = 2 * root_idx + 1;
                        右节点定义: right_node = 2 * root_idx + 2
'''

# 线段树标准模板

from typing import List


class LineTree:
    # 线段树数组大小为 4 * n
    def __init__(self, n: int, nums: List[int]):
        self.sum = [0] * 4 * n
        self.build(1, 1, n, nums)

    # 建造线段树(求区间和)
    def build(self, o: int, left: int, right: int, nums: List[int]):
        if left == right:
            # 可以进行diy操作, 例如保存区间最大值和最小值
            self.tree[o] += nums[left]
            return

        mid = (left + right) // 2
        self.build(2 * o, left, mid, nums)
        self.build(2 * o + 1, mid + 1, right, nums)

        # 此时也可以更改
        self.tree[o] = self.tree[2 * o] + self.tree[2 * o + 1]

    # def add(self, o: int, left: int, right: int, idx: int, val: int):
    #     if left == right:
    #         # 此处可以进行diy操作
    #         sum[o] += val
    #         return
    #     # 确定中点
    #     mid = (left + right) // 2
    #     # 如果当前更新节点 <= 中间节点，在左侧，否则在右侧
    #     if idx <= mid:
    #         self.add(2 * o, left, right, idx, val)
    #     else:
    #         self.add(2 * o + 1, left, right, idx, val)

    #     # 从下到上变化
    #     self.sum[o] = self.sum[2 * o] + self.sum[2 * o + 1]

    def query(self, o: int, left: int, right: int, ql: int, qr: int):
        # 要查询的数据 如果包含了当前区间, 则返回整个 sum[o]
        if ql <= left and right <= qr:
            return self.sum[o]

        # 计算得到中点
        mid = (left + right) // 2

        ans = 0
        # 如果包含了左侧区间，递归
        if ql <= mid:
            ans += self.query(2 * o, left, mid, ql, qr)
        # 如果包含了右侧区间，递归
        if qr > mid:
            ans += self.query(2 * o + 1, mid + 1, right, ql, qr)

        return ans

    # def update(self, o: int, left: int, right: int, idx: int, val: int):
    #     if left == right:
    #         self.sum[o] = val
    #         return
    #     mid = (left + right) // 2
    #     if left <= mid:
    #         self.update(2 * o, left, mid, idx, val)
    #     else:
    #         self.update(2 * o + 1, mid + 1, right, idx, val)
    #     # 最后自下而上更新
    #     self.sum[o] = self.sum[2 * o] + self.sum[2 * o + 1]
