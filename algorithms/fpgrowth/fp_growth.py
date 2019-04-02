import itertools

# data example
data_set = [['bread', 'milk', 'vegetable', 'fruit', 'eggs'],
               ['noodle', 'beef', 'pork', 'water', 'socks', 'gloves', 'shoes', 'rice'],
               ['socks', 'gloves'],
               ['bread', 'milk', 'shoes', 'socks', 'eggs'],
               ['socks', 'shoes', 'sweater', 'cap', 'milk', 'vegetable', 'gloves'],
               ['eggs', 'bread', 'milk', 'fish', 'crab', 'shrimp', 'rice']]

# the structure of FP Node
class FPNode:
    def __init__(self, id, count, parent):
        self.id = id
        self.count = count
        self.parent = parent
        self.nextSameItem = None
        self.children = []


# the structure of FP Tree
class FPTree:

    def __init__(self, data_set, minsup, root_id, root_frequency):
        self.root, self.head_table, self.item_frequency = self.construct(data_set, minsup, root_id, root_frequency)


    # the tree has just a single path
    def has_single_path(self, node):
        num_children = len(node.children)
        if num_children > 1:
            return False
        if num_children == 0:
            return True
        return True and self.has_single_path(node.children[0])


    # Procedure FP-growth
    def mine_patterns(self, minsup):
        if self.has_single_path(self.root):
            return self.generate_patterns()
        else:
            return self.recursively_generate_patterns(self.conditional_mining(minsup))


    def generate_patterns(self):
        patterns = {}

        if self.item_frequency is None:
            if self.root.id is not None:
                pattern_tuple = tuple([self.root.id])
                patterns[pattern_tuple] = self.root.count
            return patterns

        items = self.item_frequency.keys()

        # if this is a conditional tree
        if self.root.id is None:
            pattern_tuple = []
        else:
            pattern_tuple = [self.root.id]
            patterns[tuple(pattern_tuple)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + pattern_tuple))
                patterns[pattern] = min([self.item_frequency[x] for x in subset])

        return patterns


    def recursively_generate_patterns(self, patterns):
        pattern_tuple = self.root.id

        if pattern_tuple is not None:
            # We are in a conditional tree.
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [pattern_tuple]))] = patterns[key]

            return new_patterns

        return patterns



    # Deduce the ordered frequent items.
    # For items with the same frequency, the order is given by the alphabetical order reversely.
    def preprocess(self, data_set, minsup):
        # Scan the data, and filter out items that are not frequent, also remove the duplicates.
        item_frequency = {}
        for i in range(len(data_set)):
            # remove duplicates
            data_set[i] = list(set(data_set[i]))
            for id in data_set[i]:
                item_frequency[id] = item_frequency.get(id, 0) + 1

        # filter the dictionary
        item_frequency = {k: v for k, v in item_frequency.items() if v >= minsup}

        if (len(item_frequency) == 0):
            return None, None

        # Scan the data again, filter and sort the items
        new_data_set = []
        for id_list in data_set:
            temp = []
            for id in id_list:
                if id in item_frequency.keys():
                    temp.append(id)
            temp.sort(key=lambda x: (-item_frequency[x], x))
            new_data_set.append(temp)

        return item_frequency, new_data_set


    # Construct the FP-tree from the above data
    def construct(self, data_set, minsup, root_id, root_frequency):
        item_frequency, new_data_set = self.preprocess(data_set, minsup)
        root = FPNode(root_id, root_frequency, None)
        if item_frequency is None or new_data_set is None:
            return root, None, None
        frequent_items = list(item_frequency.keys())
        frequent_items.sort(key=lambda x: (-item_frequency[x], x))
        head_table = {k: None for k in frequent_items}
        for id_list in new_data_set:
            temp = root
            for id in id_list:
                exists = False
                # if id is existed in temp.children, then let the count of this node plus 1
                for node in temp.children:
                    if node.id == id:
                        node.count += 1
                        exists = True
                        temp = node
                        break
                # else if id is not existed in temp.children, then create a new node
                if exists == False:
                    node = FPNode(id, 1, temp)
                    temp.children.append(node)
                    temp = node

                listnode = head_table[id]
                if listnode is None:
                    head_table[id] = temp
                else:
                    exists = False
                    while listnode.nextSameItem is not None:
                        if listnode is temp:
                            exists = True
                            break
                        listnode = listnode.nextSameItem
                    if exists == False:
                        if not listnode is temp:
                            listnode.nextSameItem = temp

        return root, head_table, item_frequency


    # From the FP-tree above, construct the FP-conditional tree for each item (or itemset).
    def conditional_mining(self, minsup):
        # Traverse items in head_node_link, then find the conditional prefix path, construct the FPtree, and recursively.
        if (len(self.head_table) == 0):
            return

        patterns = {}

        frequent_items = list(self.item_frequency.keys())
        frequent_items.sort(key=lambda x: (-self.item_frequency[x], x), reverse=True)

        for item in frequent_items:
            # construct FP-conditional tree for item
            path_list = self.get_conditional_data(item)

            subtree = FPTree(path_list, minsup, item, self.item_frequency[item])
            subtree_patterns = subtree.mine_patterns(minsup)

            # Insert subtree patterns into main patterns dictionary.
            for p in subtree_patterns.keys():
                if p in patterns:
                    patterns[p] += subtree_patterns[p]
                else:
                    patterns[p] = subtree_patterns[p]

        return patterns

    def get_conditional_data(self, item):
        path_list = []
        node = self.head_table[item]
        while node is not None:
            path = self.get_path(node)
            for i in range(node.count):
                path_list.append(path)
            node = node.nextSameItem

        return path_list

    def get_path(self, node):
        path = []
        temp = node.parent
        # while temp != root
        while temp is not None and temp.id is not None:
            path.append(temp.id)
            temp = temp.parent
        path.reverse()
        return path



def get_patterns(data_set, minsup):

    tree = FPTree(data_set, minsup, None, 0)
    return tree.mine_patterns(minsup)



if __name__=='__main__':
    patterns = get_patterns(data_set, 3)
    print('Threshold is 3.\n')
    for key, value in patterns.items():
        print(key, ':', value)