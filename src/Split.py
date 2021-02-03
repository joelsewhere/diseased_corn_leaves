import os
import shutil
import numpy as np

class Split:
    
    def __init__(self, class_path_0, class_path_1):
        self.folders = ['train', 'test', 'val']
        self.classes = ['class_0', 'class_1']
        self.paths = {}
        self.paths['class_0'] = class_path_0
        self.paths['class_1'] = class_path_1
        self.paths['splits'] = self.create_split_paths()
        self.make_folders(self.paths['splits'])
        

    def create_split_paths(self):
        paths = {}
        for folder in self.folders:
            paths[folder] = {}
            for class_ in self.classes:
                paths[folder][class_] = os.path.join(folder,class_)
        return paths
    
    def reset(self):
        for split in self.paths['splits']:
            for class_ in self.paths['splits'][split]:
                directory = os.path.join(split, class_)
                files = os.listdir(directory)
                files = [os.path.join(directory, file) for file in files]
                if class_ == 'class_0':
                    self.move_files(files, self.paths['class_0'])
                else:
                    self.move_files(files, self.paths['class_1'])
        
        
    
    def move_files(self, files, destination_folder):
        for file in files:
            file_name = os.path.split(file)[-1]
            destination_path = os.path.join(destination_folder, file_name)
            shutil.move(file, destination_path)
        
    def make_folders(self, dictionary, parent=''):
        for path in dictionary:
            full_path = os.path.join(parent, path)
            if not os.path.isdir(full_path):
                os.mkdir(full_path)
            if type(dictionary[path]) == dict:
                self.make_folders(dictionary[path], parent=full_path)
        

    def train_test_split(self, split = .10, val = .05):
        files_0 = os.listdir(self.paths['class_0'])
        files_1 = os.listdir(self.paths['class_1'])
        files_0 = [os.path.join(self.paths['class_0'], file) for file in files_0]
        files_1 = [os.path.join(self.paths['class_1'], file) for file in files_1]
            
        training_size_0 = int((1-split)*len(files_0))
        training_size_1 = int((1-split)*len(files_1))
        
        training_0 = np.random.choice(files_0, size=training_size_0, replace=False)
        training_1 = np.random.choice(files_1, size=training_size_1, replace=False)
        testing_0 = [file for file in files_0 if file not in training_0]
        testing_1 = [file for file in files_1 if file not in training_1]
        val_0 = np.random.choice(training_0, replace=False, size = int(val*len(training_0)))
        val_1 = np.random.choice(training_1, replace=False, size = int(val*len(training_1)))
        training_0 = [file for file in training_0 if file not in val_0]
        training_1 = [file for file in training_1 if file not in val_1]
        
        self.move_files(training_0, self.paths['splits']['train']['class_0'])
        self.move_files(training_1, self.paths['splits']['train']['class_1'])
        self.move_files(testing_0, self.paths['splits']['test']['class_0'])
        self.move_files(testing_1, self.paths['splits']['test']['class_1'])
        self.move_files(val_0, self.paths['splits']['val']['class_0'])
        self.move_files(val_1, self.paths['splits']['val']['class_1'])                                                                                        