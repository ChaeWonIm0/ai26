import torch
import requests
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, render_template, request, Blueprint, url_for, g
from pybo.forms import DiaryForm
from pybo.models import Diary
from werkzeug.utils import redirect
from pybo import db
import time
import nltk
# 저장하면 주석처리
# nltk.download('punkt')

tokenizer2 = AutoTokenizer.from_pretrained("fabiochiu/t5-base-tag-generation")
model2 = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-base-tag-generation")
from werkzeug.exceptions import BadRequestKeyError

# Load the model
tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction", max_length = 1024)

grammar = Blueprint('grammar' ,__name__, url_prefix='/grammar')

def correct_grammar(sentence):
    inputs = tokenizer.encode(sentence, max_length= 1024, truncation=False, return_tensors="pt") # sentence라는 input이 들어오면 토크나이징 후 inputs에 바인딩
    outputs = model.generate(inputs, max_length= 1024) # 디코딩
    corrected_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_sentence

def generate_tags(sentence):
    inputs = tokenizer2(sentence, max_length=512, return_tensors="pt")
    output = model2.generate(**inputs, num_beams=2, do_sample=True, min_length=10, max_length=32)
    decoded_output = tokenizer2.batch_decode(output, skip_special_tokens=True)[0]
    tags = list(set(decoded_output.strip().split(", ")))
    return tags

def split_sentence(input):
    inputs = input.split('.')
    linputs = len(inputs)
    x = 0
    split_input = []
    while x < (linputs//4):
      if len(inputs) > 4:
        S_sentence=' '.join(inputs[0:4])
        del inputs[0:4]
        split_input.append(S_sentence)
      else:
         S_sentence=' '.join(inputs[0:-1])
         split_input.append(S_sentence)
      x = x+1
    return split_input

def call_models(list):
  correct_sentence = []
  for i in list:
    C_sentence = correct_grammar(i)
    correct_sentence= "".join(C_sentence)
  return correct_sentence

# Define the function to handle the form submission
@grammar.route('/correct_grammar', methods=['POST', 'GET'])
def correct_grammar_api():
    # 단락별로 저장
    # 태그 없고, 실행시간만 계산한 코드
    # if 'review' in request.form:
    #     sentence = request.form['sentence']
    #     corrected_sentence = correct_grammar(sentence)
    #     start_time = time.time()  # 시작 시간 저장
    #     form = DiaryForm()
    #     diary = Diary(subject=form.subject.data, content=corrected_sentence,
    #                   create_date=datetime.now(), user=g.user, tags='')
    #     db.session.add(diary)
    #     db.session.commit()
    #     end_time = time.time() # 종료 시간 저장
    #     execution_time = end_time - start_time # 실행시간 계산
    #     return render_template('diary/diary_form.html', execution_time = execution_time) # tags 지움, 실행시간 추가

    # 태그 있고, 시간 표시 + form_detail에 시간은 저장하지 않는 코드
    if 'review' in request.form:
        start_time = time.time() # correction_grammar 시작시간 저장
        sentence = request.form['sentence']
        # 문장 분리를 위해 추가함
        sentence2 = split_sentence(sentence)
        corrected_sentence = call_models(sentence2)

        # corrected_sentence = correct_grammar(sentence) # 문장 분리하기 전 코드
        end_time = time.time() # correction_grammar 종료 시간 저장
        execution_time = end_time - start_time # correction_grammar 실행시간 계산

        start_time2 = time.time() # generate_tags 시작시간 저장
        tags = generate_tags(sentence)
        tags = tags[:3]
        new_tags = ",".join(tags)
        end_time2 = time.time()  # generate_tags 종료시간 저장
        execution_time2 = end_time2 - start_time2 # generate_tags 실행시간 계산

        start_time3 = time.time() # db.session 시작시간 저장
        form = DiaryForm()
        # corrected_sentence = corrected_sentence1 + corrected_sentence2
        diary = Diary(subject=form.subject.data, content=str(corrected_sentence),
                      create_date=datetime.now(), user=g.user, tags=new_tags)
        db.session.add(diary)
        db.session.commit()
        end_time3 = time.time() # db.session 종료시간 저장
        execution_time3 = end_time3 - start_time3 # 데이터베이스 저장시간 계산

        return render_template('diary/diary_form.html', execution_time = execution_time, execution_time2 = execution_time2,
                               execution_time3 = execution_time3, sentence=sentence, corrected_sentence=str(corrected_sentence), tags=new_tags)
    # elif 'save' in request.form:
    #     form = DiaryForm()
    #     sentence = request.form.get('sentence')
    #     tags = generate_tags(sentence)
    #     tags = tags[:3]
    #     new_tags = ",".join(tags)
    #     diary = Diary(subject=form.subject.data, content=form.content.data,
    #                         create_date=datetime.now(), user=g.user, tags = '')
    #     # , tags = delete_enter
    #     db.session.add(diary)
    #     db.session.commit()
    #     return redirect(url_for('diary._list'))
# def sentence_compare():
#     input = request.form['sentence'].lower()
#     before = input.split('.')
#     output = correct_grammar(sentence)



# 배진혁 파일 시작
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pybo.models import Sentence


engine = create_engine('sqlite:///sentences.db', echo=True)

# def correct_grammar(sentence):
#     inputs = tokenizer.encode(sentence, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=1024, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=3, num_beams=5, early_stopping=True)
#     corrected_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return corrected_sentence

Session = sessionmaker(bind=engine)

@grammar.route('/test')
def test():
    return render_template('diary/test.html')
#
# @grammar.route('/correction_grammar', methods=['POST'])
# def correct_grammar_api2():
#     # 단어별로 저장한 버전
#     start_time = time.time()  # grammar correction 시작 시간 저장
#     sentence = request.form['sentence'] # 사용자 입력값을 받아서
#     corrected_sentence = correct_grammar(sentence) # model serving 함수에 인자로 넣음
#     words = corrected_sentence.split()
#     # 리스트의 길이가 150 이하일 경우 빈 문자열을 삽입하여 총 150개의 요소를 갖도록 만듦
#     words += [''] * (150 - len(words))
#     # Sentence 클래스 객체 생성
#     sentence_obj = Sentence()
#     # Sentence 객체의 속성에 값을 할당하는 반복문
#     for i in range(150):
#         setattr(sentence_obj, f"sentence{i + 1}", words[i])
#     end_time = time.time()  # 종료시간 저장
#     execution_time = end_time - start_time  # 실행시간 계산
#
#     start_time2 = time.time()  # grammar correction 시작 시간 저장
#     # 세션에 추가
#     db.session.add(sentence_obj)
#     # commit 하면 db에 저장
#     db.session.commit()
#     end_time2 = time.time() # 종료시간 저장
#     execution_time2 = end_time2 - start_time2 # 실행시간 계산
#
#     return render_template('diary/test.html', sentence=sentence, corrected_sentence=corrected_sentence
#                            , execution_time = execution_time, execution_time2 = execution_time2) # 실행시간 추가

    # 문장별로 저장한 버전
    # start_time = time.time()  # DB 저장 시작 시간 저장
    # sentence = request.form['sentence']  # 사용자 입력값을 받아서
    # line = sentence.split('.')
    # line_obj = Sentence()
    # corrected_line = []
    # for i in line:
    #     corrected_line = correct_grammar(i)  # 첫번째 문장부터 correction에 넣음
    #     return corrected_line
    # # 리스트의 길이가 150 이하일 경우 빈 문자열을 삽입하여 총 150개의 요소를 갖도록 만듦
    # corrected_line += [''] * (150 - len(corrected_line))
    # for i in range(150):
    #     setattr(line_obj, f'sentence{i+1}', corrected_line[i])
    # end_time = time.time()  # 실행 종료시간 저장
    # execution_time = end_time - start_time  # grammar correction 실행시간 계산
    #
    # # 세션에 추가
    # start_time2 = time.time()  # DB 저장 시작 시간 저장
    # db.session.add(line_obj)
    # # commit 하면 db에 저장
    # db.session.commit()
    # end_time2 = time.time()  # DB 저장 종료시간 저장
    # execution_time2 = end_time2 - start_time2  # DB 저장시간 계산
    #
    # return render_template('diary/test.html', sentence=sentence, corrected_sentence = corrected_line, execution_time=execution_time,
    #                        execution_time2=execution_time2)  # 실행시간 추가