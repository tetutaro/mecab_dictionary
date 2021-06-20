#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations
import sys
import os
import subprocess
import argparse
from logging import Logger, getLogger, Formatter, StreamHandler, INFO
from neologdn import normalize as neonorm
from MeCab import Tagger


class Morpheme(object):
    def __init__(
        self: Morpheme,
        dictionary: str,
        node: str,
        pos: int,
        logger: Logger
    ) -> None:
        logger.debug(node)
        self.start_pos = pos
        self.surface, features_str = node.split('\t', 1)
        self.length = len(self.surface)
        self.end_pos = self.start_pos + self.length
        features = features_str.split(',')
        self.speech = features[0]
        self.subspeech1 = features[1]
        self.subspeech2 = features[2]
        if dictionary == 'juman':
            self.origin = features[4]
            self.yomi = features[5]
            if (self.origin == '*') and (self.yomi == '*'):
                self.origin = 'UNK'
                self.yomi = 'UNK'
        else:
            if len(features) < 8:
                self.origin = 'UNK'
                self.yomi = 'UNK'
            else:
                self.origin = features[6]
                self.yomi = features[7]
        if len(features) == 10:
            self.dictionary = features[9]
        else:
            self.dictionary = ''
        return

    def __len__(self: Morpheme) -> int:
        return self.length

    def __str__(self: Morpheme) -> str:
        return '%s(%s)[%s] (%d:%d) %s,%s,%s %s' % (
            self.surface, self.origin, self.yomi,
            self.start_pos, self.end_pos,
            self.speech, self.subspeech1, self.subspeech2,
            self.dictionary
        )


class SeqMorpheme(object):
    def __init__(
        self: SeqMorpheme,
        dictionary: str,
        sentence: str,
        logger: Logger
    ) -> None:
        self.dictionary = dictionary
        self.sentence = sentence
        self.length = len(sentence)
        self.morphemes = list()
        self.logger = logger
        return

    def parse(self: SeqMorpheme, tagger: Tagger) -> None:
        pos = 0
        for node in tagger.parse(self.sentence).splitlines():
            node = node.strip()
            if node == 'EOS':
                break
            morpheme = Morpheme(
                dictionary=self.dictionary,
                node=node, pos=pos, logger=self.logger
            )
            self.morphemes.append(morpheme)
            pos += len(morpheme)
        self.logger.debug(
            f'len(setence)={self.length}, sum(len(morpheme))={pos}'
        )
        assert self.length == pos
        return

    def __len__(self: SeqMorpheme) -> int:
        return self.length

    def __str__(self: SeqMorpheme) -> str:
        buf = list()
        for m in self.morphemes:
            buf.append(str(m))
        return '\n'.join(buf)


class Tokenizer(object):
    INSTALLED_DICTIONARIES = ['ipa', 'juman', 'neologd']

    def __init__(
        self: Tokenizer,
        dictionary: str,
        logger: Logger
    ) -> None:
        self.dictionary = dictionary
        self.logger = logger
        self._load_mecab()
        self.seq_morpheme = None
        return

    def _load_mecab(self: Tokenizer) -> None:
        if os.path.isdir(self.dictionary):
            # load local dictionary
            self.logger.info(f'loading local dictionary: {self.dictionary}')
            self.tagger = Tagger(f'-d {self.dictionary}')
            return
        elif self.dictionary not in self.INSTALLED_DICTIONARIES:
            raise ValueError(f'dictionary not found: {self.dictionary}')
        # load installed dictionary
        mecab_config_path = None
        # retrive the directory of dictionary
        mecab_config_cands = [
            '/usr/bin/mecab-config', '/usr/local/bin/mecab-config'
        ]
        for c in mecab_config_cands:
            if os.path.exists(c):
                mecab_config_path = c
                break
        if mecab_config_path is None:
            raise SystemError(
                'mecab-config not found. check mecab is really installed'
            )
        dic_dir = subprocess.run(
            [mecab_config_path, '--dicdir'],
            check=True, stdout=subprocess.PIPE, text=True
        ).stdout.rstrip()
        # retrive the dictonary
        dic_path = None
        if self.dictionary == 'ipa':
            dic_cands = ['ipadic-utf8', 'ipadic']
        elif self.dictionary == 'juman':
            dic_cands = ['juman-utf8', 'jumandic']
        else:  # self.dictionary == 'neologd'
            dic_cands = ['mecab-ipadic-neologd']
        for c in dic_cands:
            tmpdir = os.path.join(dic_dir, c)
            if os.path.isdir(tmpdir):
                dic_path = tmpdir
                break
        if dic_path is None:
            raise SystemError(
                f'installed dictionary not found: {self.dictionary}'
            )
        # create tagger
        self.logger.info(f'loading installed dictionary: {self.dictionary}')
        self.tagger = Tagger(f'-d{dic_path}')
        return

    def tokenize(self: Tokenizer, sentence: str) -> None:
        self.seq_morpheme = SeqMorpheme(
            dictionary=self.dictionary,
            sentence=sentence,
            logger=self.logger
        )
        self.seq_morpheme.parse(tagger=self.tagger)
        return

    def printout(self: Tokenizer) -> None:
        assert self.seq_morpheme is not None
        print(self.seq_morpheme)
        return


def main() -> None:
    # setup logger
    logger = getLogger(__file__)
    logger.setLevel(INFO)
    formatter = Formatter('%(asctime)s: %(levelname)s: %(message)s')
    handler = StreamHandler(stream=sys.stdout)
    handler.setLevel(INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # get arguments
    parser = argparse.ArgumentParser(
        description='tokenize sentence into morphemes using MeCab'
    )
    parser.add_argument(
        '-d', '--dictionary', type=str, default='mecab_ipadic',
        help='path of MeCab dictonary or [ipa|jumap|neologd]'
    )
    args = parser.parse_args()
    # create Tokenizer
    tokenizer = Tokenizer(**vars(args), logger=logger)
    # read sentence from stdin
    sentence = neonorm(sys.stdin.read().strip())
    # run Tokenizer
    tokenizer.tokenize(sentence)
    # print tokens
    tokenizer.printout()
    return


if __name__ == '__main__':
    main()
