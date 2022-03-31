import argparse
from algorithms.factory import embedding_factory

parser = argparse.ArgumentParser();
subparsers = parser.add_subparsers(dest='algorithm');
subparsers.required = True

# deep walk algo params
deepwalk_parser = subparsers.add_parser(
    'deep_walk', help='deep walk embedding algorithm');
deepwalk_parser.add_argument('-w', '--walks', default=10,
                             help='specify the number of walks (default: %(default)s)');
deepwalk_parser.add_argument('-wl', '--walk_len', default=10,
                             help='specify the walk length(default: %(default)s)');

# node2vec algo params
node2vec_parser = subparsers.add_parser(
    'node2vec', help='node2vec embedding algorithm');
node2vec_parser.add_argument('-w', '--walks', default=10,
                             help='specify the number of walks (default: %(default)s)');
node2vec_parser.add_argument('-wl', '--walk_len', default=10,
                             help='specify the walk length(default: %(default)s)');
node2vec_parser.add_argument(
    '--p', default=10, help='specify the return parameter p (default: %(default)s)');
node2vec_parser.add_argument(
    '--q', default=0, help='specify the out parameter q(default: %(default)s)');


args = parser.parse_args();

embedding_factory(args);