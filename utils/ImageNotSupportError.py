class ImageNotSupportError(Exception):
    def __init__(self, message: str, *args: str) -> None:
        """Initializes a new instance of the class.
        
        Args:
            message (str): The message to be stored.
            *args (str): Additional arguments to be passed to the parent class.
        
        Returns:
            None
        """
        
        self.messages = message
        super().__init__(*args)
             