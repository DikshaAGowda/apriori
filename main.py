from collections import defaultdict
from itertools import chain, combinations

class Apriori:

    def __init__(self, filename, support_value, confidence_value):
        self.filepath = filename+".csv"
        self.min_support = support_value/100
        self.min_confidence = confidence_value/100
        self.item_support_values = []
        self.association_rules = []
        self.freq_set = None
    
    def get_itemsets(self,data_iterator):
        "getting 1-itemsets from list of transactions"
        transactionList = list()
        itemSet = set()
        for record in data_iterator:
            transaction = frozenset(record)
            transactionList.append(transaction)
            for item in transaction:
                itemSet.add(frozenset([item]))
        return itemSet, transactionList
    
    def data_generator(self, fname):
        "opening data file as a generator"
        with open(fname, "r", encoding='cp1252') as file_iter:
            for line in file_iter: 
                line = line.strip().rstrip(",")
                record = frozenset(line.split(","))
                yield record
    
    def get_items_min_support(self, item_set, transactions, min_support):
        "Eliminating items that do not have support greater than the minimum support threshold"
        s = set()
        local_set = defaultdict(int)

        for item in item_set:
            for t in transactions:
                if item.issubset(t):
                    self.freq_set[item] += 1
                    local_set[item] += 1
                    
        for item, count in local_set.items():
            support = float(count) / len(transactions)

            if support >= self.min_support:
                s.add(item)
                
        return s
    
    def joinSet(self, item_set, length):
        """Generate n-itemsets where n>=2"""
        s = set()
        for i in item_set:
            for j in item_set:
                if i!=j and len(i.union(j)) == length:
                    s.add(i.union(j))
        return s
#         return set([i.union(j) for i in item_set for j in item_set if len(i.union(j)) == length])
    
    def subsets(self,arr):
        """ Generate all possible non empty subsets of arr"""
        return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

    def get_item_support(self, item,transactions):
        "Generate the support value of item"
        return float(self.freq_set[item])/len(transactions)
    
    
    
    
    def start_computation(self):
        "MAIN FUNCTIONALITY OF THE APRIORI ALGORITHM"
        datagen = self.data_generator(self.filepath)
        
        item_set, transactions = self.get_itemsets(datagen)
        
        self.freq_set = defaultdict(int)
        large_set = dict()        
        
        
        min_support_set = self.get_items_min_support(item_set, transactions, self.min_support)
        self.maxK = len(min_support_set)-1
        temp_set = min_support_set
        
        k=1
        while temp_set != set([]):
            large_set[k] = temp_set
            temp_set = self.joinSet(temp_set, k+1)
            cur_set = self.get_items_min_support(temp_set, transactions, self.min_support)
            temp_set = cur_set
            k = k + 1
        
        #Computting support for all entries of itemset
        for key,values in large_set.items():
            self.item_support_values.extend([(tuple(entry),self.get_item_support(entry, transactions)) for entry in values])
        
        #Computing Association rules
        for key, value in list(large_set.items())[1:]:
            for item in value:
                local_subsets = map(frozenset, [x for x in self.subsets(item)])
                for element in local_subsets:
                    remain = item.difference(element)
                    if len(remain) > 0:
                        confidence = self.get_item_support(item, transactions) / self.get_item_support(element, transactions)
                        if confidence >= self.min_confidence:
                            self.association_rules.append(((tuple(element), tuple(remain)), confidence))
        
    def print_support_values(self):
        for val, sup in sorted(self.item_support_values, key = lambda x : x[1]):
            print(", ".join(val)+ " ====> " + str(sup))
        
        
        
    def print_rules(self):
        for rule in sorted(self.association_rules, key = lambda x: x[1], reverse=True):
            s1 = ", ".join(rule[0][0])
            s2 = ", ".join(rule[0][1])
            print(s1 + "   =========>   "+ s2 +  " | " + " with confidence: " + "%.3f"%(rule[1]))
    


if __name__=="__main__":
    d = {1:"amazon", 2:"bestbuy", 3:"grocery", 4:"kmart", 5:"nike", 6:"create your own file"}
    print("Please consult following guide")
    for k,v in d.items():
        print(str(k)+ "   "+ v)

    print("\n")

    file_number = str(input("Enter File Number:")).strip()

    if file_number == 6:
        file_name = str(input("Enter File Name:")).strip()


    file_name = d[int(file_number)]
    minimumSupportValue = int(input("Enter Support Threshold").strip())
    minimumConfidenceValue = int(input("Enter Confidence Threshold").strip())


    ap = Apriori(file_name, minimumSupportValue, minimumConfidenceValue)
    ap.start_computation()

    print("\n\n")
    print("PRINTING ASSOCIATION RULES\n\n")
    ap.print_rules()
    print("\n\n")
    print("PRINTING SUPPORT VALUES\n\n")
    ap.print_support_values()

