import streamlit as st
import spacy
import base64
from pathlib import Path
from spacy import displacy
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


nlp = spacy.load('en_core_web_sm')


def want_sentence():
    sentence = st.text_input(label="문장을 입력하세요: ", key='user_sentence')
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


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


def svg_view(sentence):
    doc = nlp(sentence)
    svg = displacy.render(doc, style='dep', jupyter=False)
    filename = 'output.svg'
    output_path = Path(filename)

    output_path.open('w', encoding='utf-8').write(svg)
    f = open("output.svg", "r")
    lines = f.readlines()
    line_string = ''.join(lines)

    render_svg(line_string)


def dep_mean_view():
    dep_mean = {"nsubj":"문장의 주어를 나타내는 명사와 절의 동작주, 행위자 간의 관계(명사 주어)",
                "obj":"목적어 관계", "dobj":"직접 목적어 관계", "iobj":"간접 목적어 관계", "csubj" : "주어 역할을 하는 절의 관계",
                "ccomp":"동사나 형용사의 ccomp는 종속절의 core argument, 동사나 형용사의 목적어 역할을 함",
                "xcomp":"동사나 형용사의 xcomp는 주어 없는 보어절 or 서술어, 이차 술어",
                "obl":"부사처럼 행동하는 명사에 사용, 여격", "Vocative":"담화의 참여자를 가리킴",
                "expl":"술어가 술어의 역할을 하지 않을 때 명사와의 관계",
                "dislocated":"문장의 주요 문법적인 관계를 수행하지 않는 선행사나 후행사와 명사와의 관계",
                "advcl":"다른 술어나 동사를 수식하는 절(조건절, 시간절 같은 부사절을 수식)",
                "advmod":"수식어구나 서술어를 수식하는 부사", "discourse":"감탄사, 담화의 요소",
                "aux":"시제, 동사형 같은 요소 관계","cop":"서술격 조사 관계",
                "mark":"절의 시작을 가리키는 관계", "nmod":"명사가 다른 명사를수식", "nmod:poss":"소유격 관계",
                "appos":"동격 관계", "nummod":"명사의 수식어가 숫자인 경우", "acl":"형용사절이 술어를 수식",
                "amod":"형용사 수식어", "det":"관사 관계", "clf":"명사를 세는 단위 관계",
                "case":"전치사, 후치사, 격 같은 단어 수식", "conj":"접속 관계", "cc":"접속사와 접속어의 관계",
                "fixed":"숙어 관계", "flat":"이름 날짜간의 동격 관계", "compound":"복합어","list":"나열",
                "orphan":"지배소가 생략된 경우","goeswith":"편집이 잘못되어 떨어진 단어들",
                "reparandum":"발화에서 말을 더듬은 경우", "punck":"문장 부호 관계", "root":"루트 관계",
                "dep":"알수 없는 관계", "neg":"부정 단어", "pcommp":"전치사의 보어가 절이거나 전치사구(또는 간혹 부사구)",
                "pobj":"전치사 또는 'here'와 'there' 부사 뒤에 오는 명사구의 헤드", 
                "preconj":"'either', 'both', 'neither' 등 접속어를 묶을 때 그 앞에 나타나는 단어",
                "predet":"명사구 한정사의 앞에서 그 의미를 수식", 
                "pref":"접두사","prep":"동사, 형용사, 명사 또는 심지어 다른 전치사의 의미를 수식"}
    
    sorted_dict = sorted(dep_mean.items())

    for i in range(len(sorted_dict)):
        cols2 = st.columns(2)
        cols2[0].write(sorted_dict[i][0])
        cols2[1].write(sorted_dict[i][1])


def pos_mean_view():
    pos_dic = {"CC": "접속사", "CD": "숫자", "DT": "한정사", "EX": "존재의 there", "FW": "외래어", "IN": "전치사",
               "JJ": "형용사", "JJR": "비교급 형용사", "JJS": "최상급 형용사", "LS": "괄호", "MD": "조동사",
               "NN": "단수 명사", "NNS": "복수 명사", "NNP": "단수 고유명사", "NNPS": "복수 고유명사", "PDT": "전치 한정사",
               "POS": "후치 한정사", "PRP": "인칭 대명사", "PRP$": "소유 대명사", "RB": "형용사", "RBR": "비교급 형용사", "RBS": "최상급 형용사",
               "RP": "불변화사", "TO": "to전치사", "UH": "감탄사", "VB": "동사 원형", "VBD": "동사 과거형", "VBG": "현재분사 ",
               "VBN": "과거 분사", "VBP": "단수 동사", "VBZ": "3인칭 동사", "WDT": "Wh-한정사", "WP": "Wh-대명사", "WP$": "소유격",
               "WRB": "Wh-부사"}
    pos_dic_list = list(pos_dic.items())
    for i in range(len(pos_dic_list)):
        cols3 = st.columns(2)
        cols3[0].write(pos_dic_list[i][0])
        cols3[1].write(pos_dic_list[i][1])

def main():
    # 제목
    st.markdown("<h1 style='text-align: center; color: black;'>문장 구조 분석하기\n\n</h1>", unsafe_allow_html=True)
    sentence = want_sentence()
    if st.button("Click"):

        st.write(sentence)
        pos_list(sentence)
        svg_view(sentence)
    option = st.selectbox('뜻 보기',
                          (' ', '단어 관계 뜻 보기', 'POS 뜻 보기'))
    if option == '단어 관계 뜻 보기':
        dep_mean_view()
    elif option == 'POS 뜻 보기':
        pos_mean_view()

main()
