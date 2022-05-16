#!/usr/bin/env python3

import logging
import sys
from argparse import ArgumentParser
from libbgg.apiv2 import BGG


def get_args():
    p = ArgumentParser(
        description="A tool to get thumbnail links for games so they can be "
        "included in the aid"
    )
    p.add_argument('-D', '--debug', action='store_true', default=False,
        help='Add debug output [default: %(default)s]')
    p.add_argument('search', nargs='+', help='The game to search for')

    args = p.parse_args()

    args.search = ' '.join(args.search)

    return args


def setup_logging(args):
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        format=(
            '%(asctime)s - %(levelname)s - '
            '%(filename)s:%(lineno)d %(funcName)s - %(message)s'
        ),
        level=level,
    )


def do_search(args):
    bgg = BGG()

    res = bgg.search(args.search)

    tot = int(res['items']['total'])
    ids = []
    if tot > 1:
        ids = [o['id'] for o in res['items']['item']]
    elif tot == 1:
        ids = [res['items']['item']['id']]

    res = bgg.boardgame(ids, stats=False)

    #import json
    #print(json.dumps(res, indent=4))

    res = res['items']['item']
    if not isinstance(res, (list, tuple)):
        res = [res]

    for item in res:
        name = ''
        if isinstance(item['name'], list):
            name = item['name'][0]['value']
        else:
            name = item['name']['value']
        print(f'{name}: {item["thumbnail"]["TEXT"]}')



def main():
    args = get_args()
    setup_logging(args)

    do_search(args)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
