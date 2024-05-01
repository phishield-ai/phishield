import json

from fastapi import APIRouter, UploadFile

from phishield.apps.email.schemas.response import APIResponseAnalysis
from phishield.common.models.google import GoogleLM
from phishield.common.utils.email import EmailProcessor
from phishield.common.utils.prompt import analyse_email_prompt
from phishield.packages.fastapi.jcontent.schemas import Content
from phishield.packages.fastapi.jsend.response import JSendResponse
from phishield.packages.fastapi.jsend.schemas import response_documentation


router = APIRouter(
    prefix="/analysis",
    default_response_class=JSendResponse,
    include_in_schema=True,
)


@router.post(
    "",
    summary="Analyze",
    description="This endpoint analyzes an email and provides a phishing score.",
    response_model=Content[APIResponseAnalysis],
    responses=response_documentation(Content[APIResponseAnalysis]),
)
async def analyze_email_for_phishing(file: UploadFile):
    email = EmailProcessor(file.file.read())
    summary = await email.summary()

    lm = GoogleLM()
    prompt = analyse_email_prompt(object=json.dumps(summary.model_dump()))
    response = await lm.ask(prompt=prompt)

    return Content(content=response)
