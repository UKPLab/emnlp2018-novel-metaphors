#!/usr/bin/env python
import argparse
import csv
import logging
import os
import re
import zipfile
from urllib2 import urlopen

from collections import defaultdict


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def download_vuamc(download_path):
    """Downloads the VUAMC from the University of Oxford Text Archive."""
    # create path if it not exists
    try:
        os.makedirs(download_path)
    except OSError:
        pass

    logger.info('Downloading VUAMC...')
    with open(os.path.join(download_path, '2541.zip'), 'w') as f:
        f.write(urlopen(vuamc_src).read())

    logger.info('Extracting VUAMC...')
    with zipfile.ZipFile(os.path.join(download_path, '2541.zip'), 'r') as zip_f:
        zip_f.extractall(os.path.join(download_path, 'vuamc_extracted'))
    return os.path.join(download_path, 'vuamc_extracted', '2541', 'VUAMC.xml')


def augment_vuamc(vuamc_path, annotations_path, output_path, add_default=False):
    """Augments the VUAMC XML file with novelty annotations."""

    logger.info('Reading novelty scores...')
    scores = defaultdict(list)
    with open(annotations_path, 'r') as anno_f:
        reader = csv.reader(anno_f)
        next(reader)  # skip first line which only includes headers
        for line in reader:
            scores['.'.join(line[:3])].append(line[3])

    logger.info('Reading VUAMC...')
    with open(vuamc_path, 'r') as vuamc_f:
        corpus_lines = vuamc_f.readlines()

    logger.info('Augmenting VUAMC with novelty scores...')
    with open(output_path, 'w') as vuamc_novelty_f:
        text_count = -1
        sentence_count = -1
        token_count = -1
        line_count = 0

        for cl in corpus_lines:

            if re.match(r'\s*(<w|<c type)', cl):  # new token
                token_count += 1

            if re.match(r'\s*<s n', cl):  # new sentence
                sentence_count += 1
                token_count = -1  # reset token count

            if re.match(r'\s*<text x', cl):  # new text
                text_count += 1
                sentence_count = -1  # reset sentence count

            # exception handling for metaphor 96.48.9
            # word before (like) is split in two parts but should be handled as one
            if re.search(r'<w lemma="like" type="PRP">lik<seg function="mFlag" type="lex"/>e </w>', cl):
                token_count -= 1

            # exception handling for metaphor with id 69.88.33
            # one token in sentence was missing in annotation file
            if text_count == 69 and sentence_count == 88 and token_count == 32:
                token_count += 1

            # exception handling for metaphor 67.5.11
            # proper name before consists of seven words but was counted as one
            if re.search(r'<w lemma="protect" type="VVG">Protecting </w><w', cl):
                token_count += 7

            if re.match(r".*<seg function=", cl) is not None:
                score = scores['.'.join(str(i) for i in [text_count, sentence_count, token_count])]
                if add_default and not score:
                    score = [-1]
                if score:
                    if not ('<w' in cl):
                        cl = re.sub(r'">', '" score="' + str(score[0]) + '">', cl)
                    # special case that <w> appears before <seg>
                    else:
                        cl = re.sub(r'(^.*?<seg[^<>]+)(">)', r'\g<1>' + '" score="' + str(score[0]) + '\g<2>', cl)

                # handle second metaphor in same line if existing
                if re.search(r'<seg.*<seg', cl) is not None:
                    token_count += 1
                    score = scores['.'.join(str(i) for i in [text_count, sentence_count, token_count])]
                    if add_default and not score:  # insert score of second metaphor
                        score = [-1]
                    if score:  # insert score of second metaphor
                        cl = re.sub(r'(^.*<seg.*<seg.*)(">)', r'\g<1>" score="' + str(score[0]) + '\g<2>', cl)

                # handle more than one metaphor in one lemma
                # exceptions for cases where annotation file and XML file differentiate
                if re.search(r".*<seg function=", corpus_lines[line_count + 1]) and not re.search(r"pixieish", cl) and not re.search(r'<w lemma="protect" type="VVG">Protecting </w><w', cl):
                    token_count += 1

            vuamc_novelty_f.writelines(cl)
            line_count += 1


if __name__ == "__main__":
    # default paths
    annotations_path = 'vuamc_novelty.csv'
    output_path = 'VUAMC_with_novelty_scores.xml'

    # parsing arguments
    parser = argparse.ArgumentParser(description='Augments the VU Amsterdam Metaphor Corpus with novelty annotations.')
    parser.add_argument('-d', '--download', dest='download', action='store_true', default=False,
                        help='Download the VUAMC to a temp directory. Use this if you do not have the VUAMC stored.')
    parser.add_argument('-a', '--add_default', dest='add_default', action='store_true', default=False,
                        help='Add a default value of -1 to metaphors without annotation (i.e., non-content tokens).')
    parser.add_argument('-o', '--output', dest='output_path', default='',
                        help='Output path for the augmented VUAMC XML file (default: {}).'.format(output_path))
    parser.add_argument('-p', '--path', dest='vuamc_path', default='',
                        help='Path to the XML file version of the VUAMC. If not available, use option -d instead.')
    args = parser.parse_args()

    # running augmentation
    if args.download:
        vuamc_path = download_vuamc('tmp')
    elif os.path.exists(args.vuamc_path):
        vuamc_path = args.vuamc_path
    else:
        parser.print_help()
        exit('\nEither specify an existing path (using -p) or select the download option (-d).')
    if args.output_path != '':
        output_path = args.output_path
    augment_vuamc(vuamc_path, annotations_path, output_path, args.add_default)

    logger.info('Finished augmenting VUAMC. Output file written to %s', output_path)
