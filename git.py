"""
Access .git stuff
"""
import os


def get_current_branch(git_root:str)->str:
    try:
        with open(os.path.join(git_root, '.git', 'HEAD'), 'r') as f:
            return f.read().split()[1]
    except IOError as e:
        return None

def get_current_tag(git_root:str, branch:str)->str:
    try:
        with open(os.path.join(git_root, branch), 'r')  as f:
            return f.read()
    except IOError as e:
        return None




