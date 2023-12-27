#!/usr/bin/env python3

import logging
import os
import string
import sys
from argparse import ArgumentParser
from textwrap import dedent


YAML_TPL = dedent('''
    name: "{name}"
    description: "{description}"
    text_type: {text_type}
    credits: "{credits}"
    enabled: false
    version: 1.0
    bgg_id: {bgg_id}
    yt_videos:
    expansions:
    sections:
      - name: Setup
        text: |
''').strip()


def get_args():
    p = ArgumentParser(
        description="Create a new playaid structure with stubs")
    p.add_argument('-i', '--create-img-dir', default=False, action='store_true',
        help='Also create an image dir (img) [default: %(default)s]')
    p.add_argument('-c', '--credits', default='Your Name',
        help='The credits, typically your name [default: %(default)s]')
    p.add_argument('-t', '--text-type', choices=('html', 'markdown'),
        default='markdown', help='The type of markup to use '
        '[default: %(default)s]')
    p.add_argument('-d', '--description', default='Add a description!',
        help='A short description for the module [default: %(default)s]')
    p.add_argument('-D', '--debug', action='store_true', default=False,
        help='Add debug output [default: %(default)s]')
    p.add_argument('name', nargs='+',
        help='The name of the player aid.  This should be written in proper '
        'title format in terms of case and spacing')

    args = p.parse_args()

    args.name = ' '.join(args.name)

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


def norm_name(name):
    """
    This will essentially boil this down to a directory name and return that
    """
    ret = ''
    ok_chars = string.ascii_letters + string.digits
    for let in name:
        if let in string.whitespace:
            ret += '_'  # whitespace is replaced with an underscore
        elif let in ok_chars:
            ret += let
        # And ignore everything else

    ret = ret.lower()

    logging.debug(f'Normalized "{name}" to "{ret}"')

    return ret


def select_item(bgg_res):
    """
    Given a list of results, let the user select the correct item
    """
    num_res = len(bgg_res)
    selected = None
    tpl = '{}: {} ({})'

    while not selected:
        for i, item in enumerate(bgg_res):
            name = ''
            if isinstance(item['name'], list):
                name = item['name'][0]['value']
            else:
                name = item['name']['value']

            print(tpl.format(i + 1, name, item['id']))

        selected = input('Select the correct game: ')
        try:
            selected = int(selected)
        except Exception:
            print(f'Invalid selection ({selected}), select a valid number\n')
            selected = None
            continue

        if selected < 1 or selected > num_res:
            print(f'Invalid selection ({selected}), select a valid number\n')
            selected = None
            continue

        # We have a valid selection, return the ID
        return int(bgg_res[selected - 1]['id'])


def get_bgg_id(args):
    # Try to import the bgg library, if that fails, return None
    try:
        from libbgg.apiv2 import BGG
    except Exception:
        return None

    bgg = BGG()

    res = bgg.search(args.name)

    tot = int(res['items']['total'])

    res = res['items']['item']
    if tot == 1:
        # If we only have 1 result, just return it
        return int(res['id'])

    return select_item(res)


def create_new(args):
    fdir = os.path.dirname(__file__)
    dir_name = norm_name(args.name)
    bgg_id = get_bgg_id(args) or 'supply BGG ID number here (required)'
    base_dir = os.path.join(fdir, dir_name)
    en_dir = os.path.join(base_dir, 'en')

    if os.path.isdir(base_dir):
        # Don't overwrite things if they already exist
        raise RuntimeError(f'Directory, {base_dir}, already exists!')

    logging.debug(f'Creating path: {en_dir}')
    os.makedirs(en_dir, 0o0755)

    if args.create_img_dir:
        logging.debug(f'Creating img dir')
        os.mkdir(os.path.join(base_dir, 'img'), 0o0755)

    with open(os.path.join(en_dir, 'playeraid.yaml'), 'w') as fh:
        logging.debug(f'Writing yaml file in {en_dir}')
        fh.write(YAML_TPL.format(
            name=args.name,
            description=args.description,
            text_type=args.text_type,
            bgg_id=bgg_id,
            credits=args.credits,
        ))


def main():
    args = get_args()
    setup_logging(args)

    try:
        create_new(args)
    except Exception as e:
        logging.error(f'Error creating files/dirs for {args.name}: {e}')
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
