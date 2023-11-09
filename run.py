import argparse
from inheritanceVisualizer.inheritanceVisualizer import visualize_inheritance
if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="run some tools")
    argparser.add_argument('-v', '--visualize', type=str, help='visualize inheritance,input your path\\to\\file', default=None)
    
    if argparser.parse_args().visualize is not None:
        files = argparser.parse_args().visualize
        visualize_inheritance(files)