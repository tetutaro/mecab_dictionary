# mecab_dictionary

IPA辞書をベースとして、そこに[IPA NEologd](https://github.com/neologd/mecab-ipadic-neologd)の単語を混ぜ込み、さらにユーザー定義も入れた MeCab 辞書を作る

## 特徴

- IPA辞書が基本となっているため、ちゃんと形態素になっている気がするっぽい
- 形態素がどの辞書から引いてきたのか分かるようになっているので安心
- IPA NEologd をアップデートすることも可能

## 前提

- MeCab がインストールされている
- wget, tar, bzip2, xz, sed, nkf がインストールされている

## 制限事項

- Mac と Ubuntu 系のディストリビューションでは動くと思います
- 面倒くさいので、ローカルで作った辞書しか動作確認してない
    - `mecab-config --dicdir` で得られるMeCab辞書ディレクトリにインストールしてちゃんと動くかは検証してない
- 作られる辞書の文字コードは UTF-8 です

## 辞書の作り方

- https://taku910.github.io/mecab/dic.html に倣い、 `userdic.csv` に追加したい形態素を記入する
    - 左文脈ID, 右文脈ID, コストは空でOK
    - 品詞の分類等は頑張って入力する
    - 発音の後に、新しいエントリとして `user` を追加すること
- `make_dictionary.sh` を叩くと `mecab_ipadic` ディレクトリが出来る

### ！！！注意！！！

サンプルとして `userdic.csv` には「丸太郎」という単語が設定してあるので、このまま作ると「丸太郎」という単語が登録された辞書になってしまいます。削除してから `make_dictionary.sh` を叩いてください。

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

## Python から MeCab を使うサンプル

[tokenize.py](tokenize.py) にサンプル実装があります。ご参考までに。

### 必要なパッケージ

- mecab-python3
- neologdn

### 使い方

コマンドで使う場合と同じです。

```
> echo "丸太郎は吾輩は猫であるをホゲランドで読んだ" | ./tokenize.py
XXXX-XX-XX XX:XX:XX,XXX: INFO: loading local dictionary: mecab_ipadic
丸太郎(丸太郎)[マルタロウ] (0:3) 名詞,固有名詞,人名 user
は(は)[ハ] (3:4) 助詞,係助詞,* ipadic
吾輩は猫である(吾輩は猫である)[ワガハイハネコデアル] (4:11) 名詞,固有名詞,一般 ipadic-neologd
を(を)[ヲ] (11:12) 助詞,格助詞,一般 ipadic
ホゲランド(UNK)[UNK] (12:17) 名詞,一般,*
で(で)[デ] (17:18) 助詞,格助詞,一般 ipadic
読ん(読む)[ヨン] (18:20) 動詞,自立,* ipadic
だ(だ)[ダ] (20:21) 助動詞,*,* ipadic
```

辞書のパスや名前を `-d` オプションに指定することで、他のディレクトリにある辞書や、インストール済みの IPA 辞書・JUMAN 辞書・IPA NEologd 辞書を使うことも出来るようにしてあります。
（もちろんこれらの辞書がインストール済みであることが必要）

IPA 辞書の場合

```
> echo "丸太郎は吾輩は猫であるをホゲランドで読んだ" | ./tokenize.py -d ipa
XXXX-XX-XX XX:XX:XX,XXX: INFO: loading installed dictionary: ipa
丸(丸)[マル] (0:1) 名詞,固有名詞,人名
太郎(太郎)[タロウ] (1:3) 名詞,固有名詞,人名
は(は)[ハ] (3:4) 助詞,係助詞,*
吾輩(吾輩)[ワガハイ] (4:6) 名詞,代名詞,一般
は(は)[ハ] (6:7) 助詞,係助詞,*
猫(猫)[ネコ] (7:8) 名詞,一般,*
で(だ)[デ] (8:9) 助動詞,*,*
ある(ある)[アル] (9:11) 助動詞,*,*
を(を)[ヲ] (11:12) 助詞,格助詞,一般
ホゲランド(UNK)[UNK] (12:17) 名詞,一般,*
で(で)[デ] (17:18) 助詞,格助詞,一般
読ん(読む)[ヨン] (18:20) 動詞,自立,*
だ(だ)[ダ] (20:21) 助動詞,*,*
```

JUMAN 辞書の場合

```
> echo "丸太郎は吾輩は猫であるをホゲランドで読んだ" | ./tokenize.py -d juman
XXXX-XX-XX XX:XX:XX,XXX: INFO: loading installed dictionary: juman
丸(丸)[まる] (0:1) 名詞,普通名詞,*
太郎(太郎)[たろう] (1:3) 名詞,人名,*
は(は)[は] (3:4) 助詞,副助詞,*
吾輩(吾輩)[わがはい] (4:6) 名詞,普通名詞,*
は(は)[は] (6:7) 助詞,副助詞,*
猫(猫)[ねこ] (7:8) 名詞,普通名詞,*
である(だ)[である] (8:11) 判定詞,*,判定詞
を(を)[を] (11:12) 助詞,格助詞,*
ホゲランド(UNK)[UNK] (12:17) 名詞,普通名詞,*
で(で)[で] (17:18) 助詞,格助詞,*
読んだ(読む)[よんだ] (18:21) 動詞,*,子音動詞マ行
```

IPA NEologd 辞書の場合

```
> echo "丸太郎は吾輩は猫であるをホゲランドで読んだ" | ./tokenize.py -d neologd
XXXX-XX-XX XX:XX:XX,XXX: INFO: loading installed dictionary: neologd
丸(丸)[マル] (0:1) 名詞,固有名詞,人名
太郎(太郎)[タロウ] (1:3) 名詞,固有名詞,人名
は(は)[ハ] (3:4) 助詞,係助詞,*
吾輩は猫である(吾輩は猫である)[ワガハイハネコデアル] (4:11) 名詞,固有名詞,一般
を(を)[ヲ] (11:12) 助詞,格助詞,一般
ホゲランド(UNK)[UNK] (12:17) 名詞,一般,*
で(で)[デ] (17:18) 助詞,格助詞,一般
読ん(読む)[ヨン] (18:20) 動詞,自立,*
だ(だ)[ダ] (20:21) 助動詞,*,*
```
