# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'


class UnionFind(object):
    def __init__(self, groups):
        self.groups = groups # groups of points
        self.items = [] # all the elements
        for group in groups:
            self.items += list(group)
        self.items = set(self.items)
        self.parent = {} # parent node
        for item in self.items:
            self.parent[item] = item
        self.create_tree()

    def findroot(self, r):
        """
        find the root node
        """
        if r == self.parent[r]:
            return r
        else:
            # path compression
            self.parent[r] = self.findroot(self.parent[r])
            return self.parent[r]

    def union(self, p, q):
        """
        combine p and q
        """
        p_root = self.findroot(p)
        q_root = self.findroot(q)

        if p_root == q_root:
            return

        # point the parent node to another point
        self.parent[p_root] = q_root
        return

    def create_tree(self):
        """
        create a tree according to the groups
        """
        for group in self.groups:
            if len(group) < 2:
                continue
            for i in range(len(group) - 1):
                if self.findroot(group[i]) != self.findroot(group[i + 1]):
                    self.union(group[i], group[i + 1])

    def is_connected(self, p, q):
        """
        judge if p and q is connected
        """
        if p not in self.items or q not in self.items:
            return False
        return self.findroot(p) == self.findroot(q)

    def add_groups(self, groups):
        """
        add extra groups
        """
        self.groups = self.groups + groups
        for group in groups:
            for item in group:
                if item in self.items:
                    continue
                self.items = list(self.items)
                self.items.append(item)
                self.parent[item] = item
        self.items = set(self.items)
        self.create_tree()

    def print_trees(self):
        """
        print the structure of the tree
        """
        rs = {}
        for item in self.items:
            root = self.findroot(item)
            rs.setdefault(root, [])
            rs[root].append(item)
        for key in rs:
            print (rs[key])
            print ('*************************')

    def get_items(self):
        """
        Get all the elements
        """
        return self.items


if __name__ == '__main__':
    # test
    groups = [((1,1), (1,2)), ((3,4), (3,3)), ((1,1), (0,1))]
    u = UnionFind(groups)
    u.print_trees()
    u.add_groups([((3,4), (3,5))])
    print ('after adding')
    u.print_trees()
    print (u.is_connected((1,1), (3,4)))
    print(u.is_connected((1, 2), (0, 1)))
