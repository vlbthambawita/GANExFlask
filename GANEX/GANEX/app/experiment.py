import os
import json


class Experiment(object):

    def __init__(self, expName, projectName, projectPath):

        self.projectName = projectName
        self.projectPath = projectPath

        self.expName = expName
        self.expPath = os.path.join(self.projectPath, self.expName)

        
        self.dict = {}
        self.json_file = os.path.join(self.expPath, self.expName + ".json") # project json file

        # init folder and project json
        os.makedirs(self.expPath, exist_ok= True)

        if os.path.isfile(self.json_file):

            with open(self.json_file) as f:
                self.dict = json.load(f)
                f.close()

        else:

            with open(self.json_file, "w+") as f:
                json.dump(self.dict, f)
                f.close()

        # add experiment path to project dictionary
        self.addExpToProjectDict()

    def addExpToProjectDict(self):
        projectJSONFile= self.projectPath + "/" + self.projectName + ".json"
        print("Project JSON path:", projectJSONFile)

        p_dict = {} 
        # read available json file
        with open(projectJSONFile) as f:
            p_dict = json.load(f)
            p_dict[self.expName] = self.expPath
            f.close()
            print("p_dict=", p_dict)

        # write data to file 
        with open(projectJSONFile, "w+") as f:
            json.dump(p_dict, f)
            f.close()

        



