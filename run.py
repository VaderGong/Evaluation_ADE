import argparse
from Visualizer.dependenceVisualizer import DependenceVisualizer

#run some tools
if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="run some tools")
    argparser.add_argument('-v', '--visualize', type=str, help='visualize dependence,input your path\\to\\file', default=None)
    
    if argparser.parse_args().visualize is not None:
        files = argparser.parse_args().visualize
        DependenceVisualizer(files)