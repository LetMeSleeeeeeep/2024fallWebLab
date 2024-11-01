"""
这是 SkipList 的使用方法
使用 SkipList(rList) 初始化一个跳表，其中rList为一个list，其中的元素是该跳表的元素
跳表间允许使用 & | ~ 运算符运算
& 取交，| 取并，~ 取补
其中 ~ 运算依赖当前跳表类维护的静态变量 elements，该变量在每次建立跳表时会被更新
因此，请确保在完成**所有**倒排索引跳表的建立后再使用非运算
"""

import random

class _Node:
    def __init__(self, val = 0):
        self.val = val
        self.right = None
        self.down = None
        self.up = None

"""请确保在完成所有倒排索引跳表的建立后再使用非运算"""
class SkipList:
    elements = set()
    def __init__(self, rList: list):
        rList.sort()
        self.maxLevel = 8
        self.cnt = len(rList)
        head = [_Node(-1) for i in range(8)]
        tail = [_Node(0x7fffffff) for i in range(8)]
        for i in range(1, 8):
            head[i].right = tail[i]
            head[i].down = head[i - 1]
            head[i - 1].up = head[i]
            tail[i].down = tail[i - 1]
            tail[i - 1].up = tail[i]
        
        head[0].right = tail[0]

        for i in range(self.cnt-1, -1, -1):
            SkipList.elements.add(rList[i])
            new_node = _Node(rList[i])
            new_node.right = head[0].right
            head[0].right = new_node
            j = 1
            while j < 8 and random.randint(0, 1): 
                new_node = _Node(rList[i])
                new_node.down = head[j-1]
                head[j-1].up = new_node
                new_node.right = head[j].right
                head[j].right = new_node

        self.head_list = head

    
    def __and__(self, other):
        if not isinstance(other, SkipList):
            raise TypeError("unsupported operand type(s) for &: 'SkipList' and '{}'".format(type(other).__name__))
        rList = []
        p = self.head_list[0].right
        q = other.head_list[0].right
        while p.val != 0x7fffffff and q.val != 0x7fffffff:

            if p.val == q.val:
                while p.down != None:
                    p = p.down
                while q.down != None:
                    q = q.down    
                rList.append(p.val)
                p = p.right
                q = q.right
                continue

            if p.val > q.val:
                swap = p; p = q; q = swap

            while p.up != None:
                p = p.up
            while p.down != None and p.right.val > q.val:
                p = p.down
            p = p.right

        return SkipList(rList)
    
    def __or__(self, other):
        if not isinstance(other, SkipList):
            raise TypeError("unsupported operand type(s) for |: 'SkipList' and '{}'".format(type(other).__name__))
        rList = []
        p = self.head_list[0].right
        q = other.head_list[0].right
        while p.val != 0x7fffffff and q.val != 0x7fffffff:
            if p.val == q.val:
                rList.append(p.val)
                p = p.right
                q = q.right
            elif p.val < q.val:
                rList.append(p.val)
                p = p.right
            else:
                rList.append(q.val)
                q = q.right
        while p.val != 0x7fffffff:
            rList.append(p.val)
            p = p.right
        while q.val != 0x7fffffff:
            rList.append(q.val)
            q = q.right
        return SkipList(rList)
    
    def __invert__(self):
        elements_list = list(SkipList.elements)
        elements_list.sort()
        rList = []
        p = self.head_list[0].right
        i = 0
        while p.val != 0x7fffffff:
            if p.val == elements_list[i]:
                p = p.right
                i += 1
            else:
                rList.append(elements_list[i])
                i += 1
        return SkipList(rList)
    
    def __str__(self):
        rList = []
        p = self.head_list[0].right
        while p.val != 0x7fffffff:
            rList.append(p.val)
            p = p.right
        return str(rList)
    
if __name__ == "__main__":
    rList = [2, 3, 4, 6, 8, 9, 10]
    sList = SkipList(rList)
    rList = [1, 3, 4, 5, 6, 7, 8]
    tList = SkipList(rList)
    uList = ~sList
    print(uList)