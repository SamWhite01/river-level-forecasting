"""

"""
from sklearn.model_selection import train_test_split
class Model:
    """ 
    """
    def __init__(self, x_raw, y_raw, data_processor) -> None:
        """
        """
        x_processed = data_processor.clean(x_raw)
        y_processed = data_processor.clean(y_raw)
        self.x_train, self, self.x_test, self.y_train, self.y_test = train_test_split(x_processed, y_processed, test_size = 0.2, random_state = 0)

        self.model
    

    def train():
        """
        """
        

    def run_inference(x_in):
        """
        """
        pass