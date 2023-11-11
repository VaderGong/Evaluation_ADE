import networkx as nx
import matplotlib.pyplot as plt
import os
import fnmatch
import re  

  

def remove_special_chars(input_str):  
    """
    remove all non-alphanumeric characters except underscores
    """
    return re.sub(r'[^a-zA-Z0-9_]', ' ', input_str)
    
class DependenceVisualizer:
    """
    This class is used to visualize the dependence of a python project.
    """
    def __init__(self,path):
        """
        path: the path of the project
        files: all python files in the project
        G: the graph of the dependence
        classNames: all class names in the project
        functionNames: all function names in the project
        """
        self.path=path
        self.files=self.find_all_python_files(path)
        self.G = nx.DiGraph()
        self.classNames=self.findAllClassNames()
        self.functionNames=[]
        self.findAllClassFunctionNames()
        self.AddClassDependency()
        
    def find_all_python_files(self,directory):
        """
        find all python files in the project
        directory: the path of the project
        """  
        python_files = []  
        for root, dirs, files in os.walk(directory):  
            for file in fnmatch.filter(files, "*.py"):  
                python_files.append(os.path.join(root, file))  
        return python_files
    def findAllClassNames(self):
        """
        find all class names in the project
        return: all class names in the project
        """
        classNames=[]
        for file in self.files:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                if line.startswith('class ') and line.endswith(':\n'):
                    parts = line.split()
                    class_name = parts[1]
                    if '(' in line:
                        # 处理继承的情况
                        idx = line.index('(')
                        class_name=line[6:idx]
                        class_name=class_name.replace(' ','')
                        parent_classes = line[idx + 1:-1].rstrip('):\n').split(',')
                        for parent_class in parent_classes:
                            parent_class=parent_class.replace(' ','')
                            if parent_class!='object' and parent_class!='':   
                                classNames.append(class_name)
                                self.G.add_edge(parent_class, class_name)
                    else:
                        # 处理没有继承的情况
                        idx=line.index(':')
                        class_name=line[6:idx]
                        class_name=class_name.replace(' ','')
                        classNames.append(class_name)
                        self.G.add_node(class_name)
        return classNames  
    def extractClassName(self,line:str):
        """
        extract class names from a line
        line: a line of code
        return: class names in the line
        """
        names=remove_special_chars(line).split()
        classNameList=[]
        for name in names:
            if name in self.classNames:
                classNameList.append(name)
        return classNameList
    def AddClassDependency(self):
        """
        add class dependency to the graph
        """
        isClassBegin=False
        classname=''
        dependentClassNames=[]
        for file in self.files:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                if isClassBegin:
                    if not line.startswith(' ') and not line.startswith('\n'):
                        dependentClassNames=list(set(dependentClassNames))
                        if classname in dependentClassNames:
                            dependentClassNames.remove(classname)
                        for name in dependentClassNames:
                            self.G.add_edge(name, classname)
                        isClassBegin=False
                        classname=''
                        dependentClassNames=[]
                    else:
                        classNames=self.extractClassName(line)
                        for name in classNames:
                            dependentClassNames.append(name)
                if isClassBegin==False and line.startswith('class ') and line.endswith(':\n'):
                    isClassBegin=True
                    classname=remove_special_chars(line).split()[1]
                
    def findAllClassFunctionNames(self):
        """
        find all function names in the project and add function dependency to the graph
        """
        functionNames=[]
        isClassBegin=False
        classname=''
        for file in self.files:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                
                if isClassBegin:
                    if not line.startswith(' ') and not line.startswith('\n'):
                        
                        functionNames=list(set(functionNames))
                        if '__init__' in functionNames:
                            functionNames.remove('__init__')
                        self.functionNames.extend(functionNames)
                        for name in functionNames:
                            self.G.add_edge(classname, name)
                        isClassBegin=False
                        functionNames=[]
                        classname=''
                    if line.strip().startswith('def '):
                        line=remove_special_chars(line)
                        parts = line.split()
                        function_name = parts[1]
                        functionNames.append(function_name)
                if isClassBegin==False and line.startswith('class ') and line.endswith(':\n'):
                        isClassBegin=True
                        classname=remove_special_chars(line).split()[1]
        return functionNames
    def extractFunctionNames(self,line:str):
        """
        extract function names from a line
        line: a line of code
        return: function names in the line
        """
        names=remove_special_chars(line).split()
        functionNames=[]
        for name in names:
            if name in self.functionNames:
                functionNames.append(name)
        return functionNames
    def AddFunctionDependence(self):
        """
        add function dependency to the graph
        """
        isFunctionBegin=False
        functionName=''
        for file in self.files:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if isFunctionBegin:
                        if not line.startswith(' ') and not line.startswith('\n'):
                            isFunctionBegin=False
                            functionName=''
                        else:
                            functionNames=self.extractFunctionNames(line)
                            for name in functionNames:
                                self.G.add_edge(name, functionName)
                    if isFunctionBegin==False and line.strip().startswith('def '):
                        isFunctionBegin=True
                        functionName=remove_special_chars(line).split()[1]
                        if functionName=='__init__':
                            isFunctionBegin=False
                            functionName=''
    
    def drawGraph(self):
        """
        visualize the dependence of the project
        """
        nx.spring_layout(self.G)
        for className in self.classNames:
            self.G.nodes[className]['color'] = 'red'
        # 绘制图形
        nx.draw(self.G, with_labels=True,  edge_color='gray', arrows=True)
        # 显示图形
        plt.show()
if __name__ == '__main__':
    path="C:\\Users\\LENOVO\\Desktop\\Lib\\Evaluation_ADE\\EvaluationADE"
    # 调用函数进行可视化
    visualizer=DependenceVisualizer(path)
    visualizer.drawGraph()