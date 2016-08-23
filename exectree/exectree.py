from functools import wraps
from copy import deepcopy

# On every entry to the function the tree grows downward.
# At any time there exist a pointer to a current tree node.
# When a node is first created it becomes the current node.
# Once a function returns the current node changes.
# The next current node is the parent of the current current node.
# If the current node has no parent, the tree is complete

tree = None
_done = False

class ExecTree:
    def __init__(self,parent=None,args=None,kwargs=None,ret=None):
        if args is None:
            self.args = []
        else:
            self.args = args
        if kwargs is None:
            self.kwargs = {}
        else:
            self.kwargs = kwargs
        self.ret = ret
        self.childs = []
        self.parent = parent

# TODO add options to specify which kwargs
# are to be recorded
def exectree(indices=None):
    global tree
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            init()
            push()
            ret = func(*args, **kwargs)
            args = list(args)
            select_args(args, indices)
            tree.args = deepcopy(args)
            tree.kwargs = deepcopy(kwargs)
            tree.ret = deepcopy(ret)
            pop()
            return ret
        return wrapper
    return dec

def push():
    global tree
    frame = ExecTree(parent=tree)
    if tree is None:
        tree = frame
    else:
        tree.childs.append(frame)
    tree = frame

def pop():
    global tree,_done
    if tree.parent is not None:
        tree = tree.parent
    else:
        _done = True

def init():
    global tree,_done
    if _done:
        tree = None

def select_args(args,indices):
    if indices is not None:
        to_remove = set(range(len(args))) - set(indices)
        for idx in to_remove:
            del args[idx]

def get_tree():
    global tree
    return tree
