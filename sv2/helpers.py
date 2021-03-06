import inspect


def not_private(func):
    if inspect.isfunction(func):
        if func.__name__[0] != "_":
            return True

    return False


def is_public_class(obj):
    if inspect.isclass(obj):
        if obj.__name__[0].isupper():
            return True

    return False


def get_public_members(class_obj):
    return [m[0] for m in inspect.getmembers(class_obj, not_private)]


def get_public_class(module):
    return [m[0] for m in inspect.getmembers(module, is_public_class)]


def get_checkers_to_run(class_obj, opts):
    m_l = get_public_members(class_obj)
    if opts["exclude_list"]:
        for i in opts["exclude_list"]:
            m_l.remove(i)
    elif opts["select_list"]:
        m_l = opts["select_list"]
    return m_l


def run_checkers(class_instance, opts):
    c = class_instance
    for m in get_checkers_to_run(type(c), opts):
        getattr(c, m)()
