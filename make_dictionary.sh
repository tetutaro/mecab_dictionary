#!/bin/bash
if [ -x /usr/lib/mecab/mecab-dict-index ]; then
    dictindex="/usr/lib/mecab/mecab-dict-index"
elif [ -x /usr/local/Cellar/mecab/0.996/libexec/mecab/mecab-dict-index ]; then
    dictindex="/usr/local/Cellar/mecab/0.996/libexec/mecab/mecab-dict-index"
else
    echo "mecab is not installed"
    exit 1
fi
update_neologd=0
if [ $# -gt 0 ]; then
    if [ "$1" = "update" ]; then
        update_neologd=1
    else
        echo "What?"
        exit 1
    fi
fi
if [ ! -d mecab_ipadic ]; then
    wget -O mecab-ipadic.tar.gz https://sourceforge.net/projects/mecab/files/mecab-ipadic/2.7.0-20070801/mecab-ipadic-2.7.0-20070801.tar.gz/download
    tar zxf mecab-ipadic.tar.gz
    rm -f mecab-ipadic.tar.gz
    mv mecab-ipadic-2.7.0-20070801 mecab_ipadic
    nkf -Ew --overwrite mecab_ipadic/*
    sed -i -e "s/$/,ipadic/g" mecab_ipadic/*.csv
    cd mecab_ipadic
    wget -O mecab-ipadic.model.bz2 "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7bnc5aFZSTE9qNnM"
    bzip2 -d mecab-ipadic.model.bz2
    nkf -Ew --overwrite mecab-ipadic.model
    sed -i -e "s/euc-jp/utf-8/" mecab-ipadic.model
    rm -f mecab-ipadic-euc.model
    cd ..
    update_neologd=1
fi
if [ $update_neologd -eq 1 ]; then
    git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
    xz -dk mecab-ipadic-neologd/seed/*.csv.xz
    sed -i -e "s/$/,ipadic-neologd/g" mecab-ipadic-neologd/seed/*.csv
    mv mecab-ipadic-neologd/seed/*.csv mecab_ipadic/.
    rm -rf mecab-ipadic-neologd
    cd mecab_ipadic
    ${dictindex} -f utf8 -t utf8
    cd ..
fi
${dictindex} -m mecab_ipadic/mecab-ipadic.model -d mecab_ipadic -u mecab_ipadic/User.csv -f utf8 -t utf8 -a userdic.csv
cd mecab_ipadic
${dictindex} -f utf8 -t utf8
