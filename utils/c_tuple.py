from typing import Tuple, SupportsIndex

class c_tuple(Tuple):

    def __mul__(self, __value: SupportsIndex) -> tuple:
        """Multiply each value in the object by the given value.
        
        Args:
            __value (SupportsIndex): The value to multiply each element in the object by.
        
        Returns:
            tuple: A tuple containing the multiplied values.
        
        Example:
            obj = MyClass()
            result = obj.__mul__(2)
            # result is a tuple containing the values in obj multiplied by 2
        """
        
        return tuple(value * __value for value in self)
        
    