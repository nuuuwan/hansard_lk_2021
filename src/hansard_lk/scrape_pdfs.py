import os

from bs4 import BeautifulSoup
from utils import timex, www

from hansard_lk._utils import log

URL = 'https://www.parliament.lk/business-of-parliament/hansards'


def parse_date(s):
    s = s.replace('Hansard of ', '')
    return timex.parse_time(s, '%B %d, %Y')


def get_pdf_info_list():
    html = www.read(URL)
    soup = BeautifulSoup(html, 'html.parser')

    pdf_info_list = []
    for a_pdf in soup.find_all('a', class_='link7'):
        ut = parse_date(a_pdf.text)
        date_id = timex.get_date_id(ut)
        url_pdf = a_pdf.get('href')
        pdf_info_list.append(
            dict(
                ut=ut,
                date_id=date_id,
                url_pdf=url_pdf,
            )
        )
    n_pdf_info_list = len(pdf_info_list)
    log.info(f'Scraped {n_pdf_info_list} PDFs.')
    return pdf_info_list


def download_pdfs():
    pdf_info_list = get_pdf_info_list()
    for pdf_info in pdf_info_list:
        date_id = pdf_info['date_id']
        url_pdf = pdf_info['url_pdf']
        pdf_file_only = f'hansard_lk.{date_id}.pdf'
        pdf_file = os.path.join('/tmp', pdf_file_only)
        url_remote_pdf = os.path.join(
            'https://github.com',
            'nuuuwan/hansard_lk/blob/data',
            pdf_file_only,
        )
        if www.exists(url_remote_pdf):
            log.warn(f'{url_remote_pdf} already exists')
        else:
            www.download_binary(url_pdf, pdf_file)
            log.info(f'Downloaded {url_pdf} to {pdf_file}')


if __name__ == '__main__':
    download_pdfs()
