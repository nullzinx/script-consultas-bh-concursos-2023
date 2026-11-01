import argparse
import re
from io import BytesIO
import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader


BASE_URL = "https://www.cmbh.mg.gov.br/transparencia/concursos/2023/resultados"


def building_args():
    parser = argparse.ArgumentParser(description="BH concursos scrapper")
    parser.add_argument("-q","--query",type=str,required=True)
    return parser.parse_args()


def extract_candidate(text: str, query: str):
    query = query.lower().strip()
    text = text.lower()

    pattern = rf"""
        (?P<inscricao>\d+)
        \s+
        (?P<nome>{re.escape(query)})
        \s+
        (?P<prova_objetiva>\d+)
        \s+
        (?P<prova_discursiva>[\d,]+)
        (?P<nascimento>\d{{2}}/\d{{2}}/\d{{4}})
        \s+
        (?P<situacao>aprovado|reprovado)
        \s*
        (?P<cota>negro)?
        \s*
        (?P<classificacao>\d+º)
        (?P<nota_final>[\d,]+)
    """

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.VERBOSE
    )

    if not match:
        return None

    return match.groupdict()


def scraping(query: str):
    response = httpx.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    concurso_pdf = soup.find(
        "a",
        string="Resultado final - todos os cargos (Lista geral)"
    )

    if not concurso_pdf:
        return {
            "found": False,
            "error": "PDF não encontrado na página"
        }

    pdf_url = concurso_pdf.get("href")

    pdf_response = httpx.get(pdf_url)
    pdf_response.raise_for_status()

    pdf = BytesIO(pdf_response.content)
    reader = PdfReader(pdf)

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text:
            continue

        if query.lower() not in text.lower():
            continue

        candidate = extract_candidate(
            text,
            query
        )

        if candidate:
            candidate["page"] = page_number

            return {
                "found": True,
                "candidate": candidate
            }

    return {
        "found": False
    }


if __name__ == "__main__":
    args = building_args()
    result = scraping(args.query)
    print(result)
