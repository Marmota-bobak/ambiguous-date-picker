'''
20190616 JiaYi Zhang
CYK algorithm with intersted non-terminal

Read input from stdin, parse input text with given grammar
return ranges of interested non-terminals
'''

from collections import defaultdict
from math import log,exp
grammarFiles = ['grammar.cfg','lexicon.cfg']
interestedNonterminalFile = 'target_tag.tag'


class Node:
    '''
    lchild and rchild should be a 3-tuple, representing an index in parse chart.
    '''
    def __init__(self, tag, lchild, rchild, prob):
        self.tag = tag
        self.lchild = lchild
        self.rchild = rchild
        self.prob = prob
    
    def __str__(self):
        return "{}|{},{}|{}".format(self.tag,self.lchild,self.rchild,self.prob)
    
    def __repr__(self):
        return "{}-{}".format(self.tag, self.prob)

def debug(dp,span):
    for i in range(span):
        for j in range(span-i):
            print(dp[i][j],end='')
        print()

def PCYK(binary, unary, ipt):
    span = len(ipt)
    dp = [[[] for j in range(span - i)] for i in range(span)]#lambda:defaultdict(lambda:defaultdict(lambda:[]))
    #prob = [[[] for j in range(span - i)] for i in range(span)]

    for i in range(span):
        if ipt[i] in unary:
            ks = list(unary[ipt[i]].keys())
            for k in ks:
                dp[0][i].append(Node(k,None,None,unary[ipt[i]][k]))
            #dp[0][i]+=list(unary[ipt[i]].keys())
            #for k in dp[0][i]:
            #    prob[0][i].append(unary[ipt[i]][k])
    

    for l in range(1,span):
        for s in range(span-l):
            for p in range(0,l):
                lk = dp[p][s]
                rk = dp[l-p-1][p+s+1]
                for i in lk:
                    lk_tag = i.tag
                    for j in rk:
                        rk_tag = j.tag
                        if lk_tag in binary and rk_tag in binary[lk_tag]:
                            key_list = list(binary[lk_tag][rk_tag].keys())
                            for k in range(len(key_list)):
                                if not key_list[k] in dp[l][s]:
                                    prob_l = dp[p][s][k].prob
                                    prob_r = dp[l-p-1][p+s+1][k].prob
                                    dp[l][s].append(Node(key_list[k],(p,s,k),(l-p-1,p+s+1,k),prob_l+prob_r))
                                    #prob[l][s].append(binary[i][j][k])
    
    return dp


def readRawGrammar(files):
    binary = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0.0)))
    unary = defaultdict(lambda:defaultdict(lambda:0.0))

    symbol = defaultdict(lambda: False)

    tot = defaultdict(lambda:0.0)
    # Begin reading
    for fn in files:
        with open(fn) as f:
            for l in f:
                parts = l.split()
                lhs = parts[0]
                proba = float(parts[-1])
                argLength = len(parts)
                if argLength == 5: # Binary
                    binary[parts[2]][parts[3]][lhs] += proba
                    symbol[parts[3]] = True
                    symbol[parts[2]] = True
                elif argLength == 4: # Unary
                    #print(parts[2])
                    unary[parts[2]][lhs] += proba
                    symbol[parts[2]] = True
                tot[lhs] += proba
                symbol[lhs] = True
    # End reading
    # Begin normalizing
    for i in binary:
        for j in binary[i]:
            for k in binary[i][j]:
                binary[i][j][k] = log(binary[i][j][k]) - log(tot[k])
    for i in unary:
        for j in unary[i]:
            unary[i][j] = log(unary[i][j]) - log(tot[j])
    # End normalizing
    return binary,unary,symbol,tot


def readInterest(filename):
    with open(filename) as f:
        c = f.read()
    l = c.split()
    return l

def bt(pt,pos,indent):
    if pos is None:
        return
    print(" "*indent,end='')
    print(pt[pos[0]][pos[1]][pos[2]].tag,pos[1])
    bt(pt,pt[pos[0]][pos[1]][pos[2]].lchild,indent+1)
    bt(pt,pt[pos[0]][pos[1]][pos[2]].rchild,indent+1)

def backTrace(pt,i,j,k):
    curPt = pt[i][j][k]
    print(curPt.tag,exp(curPt.prob))
    #print(curPt)
    bt(pt,curPt.lchild,1)
    bt(pt,curPt.rchild,1)
    print("#"*10)

def findInterestParse(parse_tree, interest):
    span = len(parse_tree)
    for i in range(span):
        for j in range(span-i):
            for t in interest:
                for n in range(len(parse_tree[i][j])):
                    if t == parse_tree[i][j][n].tag:
                        backTrace(parse_tree,i,j,n)


def main():
    TEST_SENTENCE = "she eats a fish with a fork"
    binary,unary,symbol,tot = readRawGrammar(grammarFiles)
    parse_tree = PCYK(binary,unary, TEST_SENTENCE.split())
    debug(parse_tree,7)
    il = readInterest(interestedNonterminalFile)
    print(il)
    findInterestParse(parse_tree,il)



main()
