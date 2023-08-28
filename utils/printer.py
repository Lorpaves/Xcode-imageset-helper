from termcolor import cprint


def __parse_args(*args: object) -> str:
    """Parses the given arguments into a single string.
    
    Args:
        *args: Variable number of arguments to be parsed.
    
    Returns:
        str: A string containing all the parsed arguments joined by a space.
    """
    
    return ' '.join(str(s) for s in args)

def print_green(*args: object):
    """Prints the given arguments in green color on a cyan background.
    
    Args:
        *args: Variable length arguments to be printed.
    
    Example:
        >>> print_green('Hello', 'World')
        Hello World
    """
    print_green = lambda x: cprint(__parse_args(*args), 'green', 'on_black', attrs=['bold'])
    print_green(args)

def print_cyan(*args: object):
    """Prints the given arguments in cyan color on a black background.
    
    Args:
        *args: Variable length arguments to be printed.
    
    Example:
        >>> print_cyan('Hello', 'World')
        Hello World
    """
    print_cyan = lambda x: cprint(__parse_args(*args), 'cyan', 'on_black', attrs=['bold'])
    print_cyan(args)

def print_white(*args: object):
    """Prints the given arguments in white color on a black background.
    
    Args:
        *args: Variable length arguments to be printed.
    
    Example:
        print_white('Hello', 'World')
    """
    print_white = lambda x: cprint(__parse_args(*args), 'white', 'on_black')
    print_white(args)