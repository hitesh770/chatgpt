from pydantic import BaseModel, Field
from typing import Optional


class SenderInfo(BaseModel):
    first_name: str = 'Hitesh'
    company_name: str = 'Huss Law - Jeremy Huss'
    product_or_service_offer: str = 'Criminal Attorney'
    core_value_of_offer: str
    preferred_call_to_action: str = 'Direct reply to the email hitesh770@gmail.com'
    additional_sender_information: str
    website: str = 'https://jeremyhuss.com/'
    city: str = 'Arizona'


class RecipientInfo(BaseModel):
    company_name: str = 'Rosenberg Law Firm -- Jonathan Rosenberg'
    first_name: Optional[str] = 'Rajat'
    website: str = "https://rosenbergpllc.com/"
    


class EmailResponse(BaseModel):
    subject: str = Field(description="Subject for the email.")
    body: str = Field(description="Body for the email.")
