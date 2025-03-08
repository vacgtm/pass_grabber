class Builder:
    def __init__(self):
        self.edgePath = "../modules/get_edge.py"
        self.chromePath = "../modules/get_chrome.py"
        self.buildPath = "successful_build/client.py"

    

    
    def read_ec(self):
        edgeData = open(self.edgePath, 'r')
        chromeData = open(self.chromePath, 'r')
        self.build(edgeData.read(), chromeData.read())
    
    
    def build(self, edgeData, chromeData):
        with open(self.buildPath, 'w') as e:
            e.write(edgeData + "\n\n" + chromeData)


#a = Builder()
#a.read_ec()