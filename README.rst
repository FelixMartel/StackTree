ExecTree
========
It is common enough that a recursive function is used to traverse something while a k-ary tree is built and returned by this same function.

Since this tree is implicit from the execution, I feel there should be a way to obtain a basic tree that would represent the recorded history of the stack

Decoupling the function design and the data structure creation will hopefully allow the programmer to focus on the recursive logic.

In python this is achieved using a decorator ``@exectree``. Optionally, it is possible to specify which arguments to record by passing there indices to exectree.

Example
-------
A recursive function used to traverse a 2d map::

    from exectree import exectree,get_tree
    
    char_map = ("xxxxxxxx   "
                "x x    x   "
                "x xxxx xxxx"
                "x         x"
                "xxxxxxxxxxx")
    @exectree(indices=[1]) # keep the pos argument only
    def traverse(m, pos):
      if pos >= len(m) or pos < 0 or m[pos] == 'x':
        return False
      m[pos] = 'x'
      # go left
      traverse(m, pos-1)
      # go right
      traverse(m, pos+1)
      # go down
      traverse(m, pos+11)
      # go up
      traverse(m, pos-11)

    traverse(list(char_map), 12)
    # tree is the path the function took to fill the maze
    tree = get_tree()

Usage tips
----------
If a value is computed inside the function frame and needs to be present in the tree, it simply has to be returned

e.g. if the function used to return a boolean, it could now return a tuple (Boolean,Other)
