import json
from transformers import pipeline

file_path = 'dataset_spain_all_page.json'

with open(file_path, 'r') as json_file:
    data_list = json.load(json_file)

# create context from title and summary
spanish_data = [data['title'] + "\n" + data["content"] for data in data_list]

i=0
while i < len(spanish_data):
  spanish_data[i] = spanish_data[i][0:2000]
  i+=1


# print(len(spanish_data))


# SpanishClubsQA3 = pipeline('text2text-generation',
#                            model='voidful/bart-eqg-question-generator')

# For each wiki page generate a question
# spanish_qa = {'context': spanish_data,
#               'question': [],
#               'answer': [],
#               }

# spanish_qa['question'] = [SpanishClubsQA3(wiki) for wiki in spanish_data]

# from transformers import T5Tokenizer, T5ForConditionalGeneration

# model = 'google/flan-t5-base'
# tokenizer = T5Tokenizer.from_pretrained(model)
# model = T5ForConditionalGeneration.from_pretrained(model)


# tokens = tokenizer.tokenize(spanish_data[0][0:1000])
# print(f'number of tokens: {len(tokens)}')

# inputs = tokenizer('Generate a question: ' + spanish_data[0][0:1000], return_tensors='pt').input_ids
# outputs = model.generate(inputs)

# inputs_answer = tokenizer(f'Write a full formal answer for this question {tokenizer.decode(outputs[0])}: ', return_tensors='pt').input_ids
# outputs_answer = model.generate(inputs_answer)


# print(spanish_data[0])
# print('---------------------------------')
# print(tokenizer.decode(outputs[0]))
# print('---------------------------------')
# print(tokenizer.decode(outputs_answer[0]))


from transformers import pipeline

SpanishClubsQA = pipeline('text2text-generation',
                          model='voidful/context-only-question-generator')

SpanishClubsQA(spanish_data[0][0:1000])