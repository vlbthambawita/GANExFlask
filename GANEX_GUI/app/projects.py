import os
import json

class Project(object):

    def __init__(self, projectName, projectPath):

        self.name = projectName
        self.path = projectPath
        self.full_path = os.path.join(self.path, self.name)
        self.dict = {}
        self.json_file = os.path.join(self.full_path, self.name + ".json") # project json file

        # init folder and project json
        os.makedirs(self.full_path, exist_ok= True)

        if os.path.isfile(self.json_file):

            with open(self.json_file) as f:
                self.dict = json.load(f)
                f.close()

        else:

            with open(self.json_file, "w+") as f:
                json.dump(self.dict, f) 
                f.close()



    