# mecab_dictionary

IPA辞書をベースとして、そこに[IPA NEologd](https://github.com/neologd/mecab-ipadic-neologd)の単語を混ぜ込み、さらにユーザー定義も入れた MeCab 辞書の作り方

## 特徴

- IPA辞書が基本となっているため、ちゃんと形態素になっている気がするっぽい
- 形態素がどの辞書から引いてきたのか分かるようになっているので安心
- IPA NEologd をアップデートすることも可能

## 前提

- MeCab がインストールされている
- `mecab-dict-index` のパスが分かっている
    - Ubuntu と MacOS 用に `/usr/lib/mecab/mecab-dict-index` と `/usr/local/Cellar/mecab/0.996/libexec/mecab/mecab-dict-index` を設定済
- wget, tar, bzip2, xz, sed, nkf がインストールされている

## 制限事項

- 面倒くさいので、ローカルで作った辞書しか動作確認してない
    - `mecab-config --dicdir` で得られるMeCab辞書ディレクトリにインストールしてちゃんと動くかは検証してない
- 作られた辞書の文字コードは UTF-8 です

## 辞書の作り方

- https://taku910.github.io/mecab/dic.html に倣い、 `userdic.csv` に追加したい形態素を記入する
    - 左文脈ID, 右文脈ID, コストは空でOK
    - 品詞の分類等は頑張って入力する
    - 発音の後に、新しいエントリとして `user` を追加すること
- `make_dictionary.sh` を叩くと `mecab_ipadic` ディレクトリが出来る

## アップデートの仕方

- ユーザー定義だけ追加・削除・変更する場合
    - `userdic.csv` を追加・削除・変更
    - `make_dictionary.sh` を叩くだけ
- IPA NEologd をアップデートする場合
    - ユーザー定義の追加・削除・変更と同時にしても良い
    - `make_dictionary.sh update` とする

## 使い方

- `mecab_ipadic` を MeCab の辞書のパスに指定する
- エントリの10番目に引いてきた辞書の名前が出る
    - 未知語(UNK)の場合にはそもそもエントリが7個しかないので注意

```
> echo "太郎と丸太郎とキンタロー。が共にアズガルドに向かう" | mecab -d mecab_ipadic
太郎	名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー,ipadic
と	助詞,並立助詞,*,*,*,*,と,ト,ト,ipadic
丸太郎	名詞,固有名詞,人名,名,*,*,丸太郎,マルタロウ,マルタロー,user
と	助詞,並立助詞,*,*,*,*,と,ト,ト,ipadic
キンタロー。	名詞,固有名詞,一般,*,*,*,キンタロー。,キンタロー,キンタロー,ipadic-neologd
が	助詞,格助詞,一般,*,*,*,が,ガ,ガ,ipadic
共に	副詞,一般,*,*,*,*,共に,トモニ,トモニ,ipadic
アズガルド	名詞,一般,*,*,*,*,*
に	助詞,格助詞,一般,*,*,*,に,ニ,ニ,ipadic
向かう	動詞,自立,*,*,五段・ワ行促音便,基本形,向かう,ムカウ,ムカウ,ipadic
EOS
```
