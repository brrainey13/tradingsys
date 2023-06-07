class PositionDeterminer:
    def determine(self, data):
        raise NotImplementedError
        
        
class DiffPositionDeterminer(PositionDeterminer):
    def determine(self, data):
        return data['Signal'].diff()

    
class ThresholdPositionDeterminer(PositionDeterminer):
    def __init__(self, threshold):
        self.threshold = threshold

    def determine(self, data):
        return (data['Signal'] > self.threshold).astype(int).diff()
