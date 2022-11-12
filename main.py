import streamlit as st
import nltk
import spacy
from PIL import Image
nltk.draw.download('tree')
nlp = spacy.load('en_core_web_sm')


def want_sentence():
    sentence = st.text_input("문장을 입력하세요: ")
    return sentence


def pos_list(sentence):
    # 단어에 pos달기
    s_pos_tags = [(word, word.tag_) for word in nlp(sentence)]

    # 포스 태그 한국어로 변환하기
    k_dic_tag = {"CC": "접속사", "CD": "숫자", "DT": "한정사", "EX": "존재의 there", "FW": "외래어", "IN": "전치사",
                 "JJ": "형용사", "JJR": "비교급 형용사", "JJS": "최상급 형용사", "LS": "괄호", "MD": "조동사",
                 "NN": "단수 명사", "NNS": "복수 명사", "NNP": "단수 고유명사", "NNPS": "복수 고유명사", "PDT": "전치 한정사",
                 "POS": "후치 한정사", "PRP": "인칭 대명사", "PRP$": "소유 대명사", "RB": "형용사", "RBR": "비교급 형용사", "RBS": "최상급 형용사",
                 "RP": "불변화사", "TO": "to전치사", "UH": "감탄사", "VB": "동사 원형", "VBD": "동사 과거형", "VBG": "현재분사 ",
                 "VBN": "과거 분사", "VBP": "단수 동사", "VBZ": "3인칭 동사", "WDT": "Wh-한정사", "WP": "Wh-대명사", "WP$": "소유격",
                 "WRB": "Wh-부사"}

    k_pos_tags = []

    # 튜플 리스트로 바꾸기
    for i in range(0, len(s_pos_tags)):
        a_list = list(s_pos_tags[i])
        k_pos_tags.append(a_list)

    i = 0
    for w, t in s_pos_tags:
        if t in k_dic_tag:
            k_t = k_dic_tag.get(t)
            k_pos_tags[i][1] = k_t
        i += 1
    # 리스트 튜플로 변환
    sen_lst = []
    for i in range(len(k_pos_tags)):
        a_tuple = tuple(k_pos_tags[i])
        sen_lst.append(a_tuple)

    for i in range(len(sen_lst)):
        cols = st.columns(2)
        cols[0].write(sen_lst[i][0])
        cols[1].write(sen_lst[i][1])


def convert_to_png(ps_file):
    img = Image.open(ps_file)
    # basewidth = 500
    # wpercent = (basewidth / float(img.size[0]))
    # hsize = int((float(img.size[1]) * float(wpercent)))
    # img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save("img.png", quality=100, subsampling=0)


def image_view(sentence):
    # 문장을 단어 단위로 토큰화
    words = nltk.tokenize.word_tokenize(sentence)

    # 단어에 포스 태그 달기
    pos_tags = nltk.pos_tag(words)

    # grammar = r"""
    #         S : {<명사구> <동사구>}
    #         명사구: {<DT|JJ|NN.*>+}    #To extract Noun Phrases
    #         전치사: {<IN>}               #To extract Prepositions
    #         동사: {<V.*>}              #To extract Verbs
    #         전치사 구: {<IN><NP>}        #To extract Prepositional Phrases
    #         동사구:  {<VB.*><NP|PP|CLAUSE>+$}     #To extract Verb Phrases
    #         CLAUSE: {<NP><VP>}
    #     """
    grammar = r"""
                S : {<NP> <VP>}
                NP: {<DT|JJ|NN.*>+}    #To extract Noun Phrases
                P: {<IN>}               #To extract Prepositions
                V: {<V.*>}              #To extract Verbs
                PP: {<IN><NP>}        #To extract Prepositional Phrases
                VP:  {<VB.*><NP|PP|CLAUSE>+$}     #To extract Verb Phrases
                CLAUSE: {<NP><VP>}
            """
    t = list(map(lambda sent: nltk.Tree(sent[1], children=[sent[0]]), pos_tags))

    NPChunker = nltk.RegexpParser(grammar)

    result = NPChunker.parse(t)

    nltk.draw.tree.TreeView(result)._cframe.print_to_file('output.ps')

    convert_to_png('output.ps')
    img = Image.open('img.png')
    st.image('img.png')


def main():
    # 제목
    st.markdown("<h1 style='text-align: center; color: black;'>문장 구조 분석하기\n\n</h1>", unsafe_allow_html=True)
    sentence = want_sentence()
    if st.button("Click"):
        st.write(sentence)
        pos_list(sentence)
        image_view(sentence)


main()
