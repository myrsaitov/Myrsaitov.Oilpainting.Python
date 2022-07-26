import inspect


# Определяет имя процедуры, которая была вызвана
def retrieve_name(self, var):
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    name_list = [var_name for var_name, var_val in callers_local_vars if var_val is var]
    return name_list[0] if name_list else None
