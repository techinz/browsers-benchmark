def find_new_child_processes(before: list, after: list):
    """
    Find new child processes that were not present in the before list

    :param before: List of processes before the operation
    :param after: List of processes after the operation
    """

    return [p for p in after if p.pid not in [b.pid for b in before]]
