from loger import write_logs



def decore_bd_function(func):
    def wrapper(*args):
        try:
            info = func(*args)
            return info
        except Exception as e:
            print(e)
            # write_logs(f"\nError: {e} \nfunc name: {func.__name__} \nargs: {args}", folder="error_logs") 
    return wrapper