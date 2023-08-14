from typing_extensions import Annotated
from fastapi import APIRouter, Request
from app.schemas import EmailResponse, SenderInfo, RecipientInfo
from app.config import Config
import requests
from bs4 import BeautifulSoup
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import ast


config = Config()
router = APIRouter()


@router.post('/emailresponse', tags=['email'], status_code=200, response_model=EmailResponse)
async def get_email_response(request: Request, sender_info: SenderInfo, receipient_info: RecipientInfo):
    response = requests.get(url=sender_info.website)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        llm = ChatOpenAI(temperature=0, model=config.model,
                         openai_api_key=config.open_api_token)
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
        docs = text_splitter.create_documents([soup.get_text()])

        product_or_service_offer = sender_info.product_or_service_offer
        core_value_of_offer = sender_info.core_value_of_offer
        preferred_call_to_action = sender_info.preferred_call_to_action
        additional_sender_information = sender_info.additional_sender_information
        first_name = sender_info.first_name
        company_name = sender_info.company_name
        city = sender_info.city
        website = sender_info.website
        first_name_recipient = receipient_info.first_name
        company_name_recipient = receipient_info.company_name

        subject_schema = ResponseSchema(
            name='subject', description='subject of email')
        body_schema = ResponseSchema(
            name='body', description='body of the email')

        # response formatting
        response_schemas = [subject_schema,
                            body_schema]
        output_parser = StructuredOutputParser.from_response_schemas(
            response_schemas=response_schemas)
        format_instructions = output_parser.get_format_instructions()

        # MAP prompt creation
        map_prompt = """
        I want you to act as a business-to-business cold sales email writer. I will provide you descriptions about the {product_or_service_offer}, about the target audience of specific business decision makers, and the sender's contact information for the signature line and {preferred_call_to_action}. The fields available to merge in are {first_name}, {company_name}, and {city}. Explain how the product or service can solve the {first_name_recipient} problems or help them achieve their goals. Be specific and provide examples or case studies to back up your claims. Use a clear, concise subject line. Personalize your email and use a casual and folksy friendly tone. Clearly state the value you can provide. Keep it short and to the point. At the end of your email, make it clear what you want the {first_name_recipient} to do next. This could be a phone call, a link to a calendar appointment, or visiting the {website}.:
        "{text}"
        SUMMARY:

        {format_instructions}
        """

        # setting prompt template
        map_prompt_template = PromptTemplate(
            template=map_prompt,
            input_variables=["text", "product_or_service_offer", "preferred_call_to_action",
                             "first_name", "company_name", "city", "first_name_recipient", "website"],
            partial_variables={"format_instructions": format_instructions})

        summary_chain = load_summarize_chain(
            llm=llm,
            chain_type='map_reduce',
            map_prompt=map_prompt_template,
            combine_prompt=map_prompt_template,
            verbose=False
        )
        output = summary_chain.run(input_documents=docs, product_or_service_offer=product_or_service_offer, preferred_call_to_action=preferred_call_to_action,
                                   first_name=first_name, company_name=company_name, city=city, first_name_recipient=first_name_recipient, website=website)

    return output_parser.parse(output)
