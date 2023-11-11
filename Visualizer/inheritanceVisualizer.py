import networkx as nx
import matplotlib.pyplot as plt
import os  
import fnmatch  
  
def visualize_inheritance(path):
    files=find_all_python_files(path)
    
    # 创建一个空的有向图
    G = nx.DiGraph()

    # 遍历每个文件
    for file in files:
        # 读取文件内容
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 提取类名和父类名
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
                            G.add_edge(parent_class, class_name)
                else:
                    # 处理没有继承的情况
                    idx=line.index(':')
                    class_name=line[6:idx]
                    class_name=class_name.replace(' ','')
                    G.add_node(class_name)
    # 绘制图形
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', arrows=True)

    # 显示图形
    plt.show()

  
def find_all_python_files(directory):  
    
    python_files = []  
  
    for root, dirs, files in os.walk(directory):  
        for file in fnmatch.filter(files, "*.py"):  
            python_files.append(os.path.join(root, file))  
    return python_files  
if __name__ == '__main__':
    path="C:\\Users\\LENOVO\\Desktop\\Lib\\Evaluation_ADE\\inheritanceVisualizer"

    # 调用函数进行可视化
    visualize_inheritance(path)