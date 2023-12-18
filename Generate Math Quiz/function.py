from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

config = {'max_new_tokens': 256, 'temperature': 0.1}

# Create function for app
def GetLLMResponse(selected_topic_level, 
                    selected_topic,
                    num_quizzes):

    # Calling llama model
    llm = CTransformers(model="D:\Code Workspace\DL Model\llama-2-7b-chat.ggmlv3.q8_0.bin",
                        model_type = 'llama',
                        config = config)

    # llm = CTransformers(model='TheBloke/Llama-2-7B-Chat-GGML',
    #                     model_file = 'llama-2-7b-chat.ggmlv3.q8_0.bin',
    #                     model_type = 'llama',
    #                     config = config)
    
    ## Create LLM Chaining
    questions_template = "Generate a {selected_topic_level} math quiz on the topic of {selected_topic}. Include {num_quizzes} questions without providing answers."
    questions_prompt = PromptTemplate(input_variables=["selected_topic_level", "selected_topic", "num_quizzes"],
                                      template=questions_template)
    questions_chain = LLMChain(llm= llm,
                               prompt = questions_prompt,
                               output_key = "questions")


    answer_template = "From this Question:\n {questions}\n\n gave me answer to each one of them"
    answer_prompt = PromptTemplate(input_variables = ["questions"],
                                   template = answer_template)
    answer_chain = LLMChain(llm = llm,
                            prompt = answer_prompt,
                            output_key = "answer")
    
    ## Create Sequential Chaining
    seq_chain = SequentialChain(chains = [questions_chain, answer_chain],
                                input_variables = ['selected_topic_level', 'selected_topic', 'num_quizzes'],
                                output_variables = ['questions', 'answer'])
    
    response = seq_chain({'selected_topic_level': selected_topic_level, 
                            'selected_topic': selected_topic, 
                            'num_quizzes' : num_quizzes})
    
    ## Generate the response from the llama 2 model
    print(response)
    return response