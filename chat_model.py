from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the custom Hugging Face LLM model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

template = """
oisfjopsjg
 
{history}
Human: {human_input}
Insider:"""

prompt = 'when FC Barcelona got founded?' ##PromptTemplate(input_variables=["history", "human_input"], template=template)
input = tokenizer(prompt, return_tensors="pt")

output = model.generate(**input, 
                        max_length=100,
                        pad_token_id=tokenizer.eos_token_id, 
                        num_return_sequences=1,
                        do_sample=True, 
                        top_k=50,
                        top_p=0.95
                        )
response = tokenizer.decode(output[0], skip_special_tokens=True)

print(response)