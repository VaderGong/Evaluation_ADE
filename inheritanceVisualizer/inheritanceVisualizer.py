import networkx as nx
import matplotlib.pyplot as plt

def visualize_inheritance(files):
    # 创建一个空的有向图
    G = nx.DiGraph()

    # 遍历每个文件
    for file in files:
        # 读取文件内容
        with open(file, 'r') as f:
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

# 指定要分析的文件列表
files = ['Visualizer/test_class1.py', 'Visualizer/test_class2.py']

# 调用函数进行可视化
visualize_inheritance(files)