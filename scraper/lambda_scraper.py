from scraper.scrape import scrape_html


def get_all_cases():
    cases = []

    content = scrape_html('https://lambdalegal.org/judicial-archive/')
    print(f'Downloaded Lambda Legal Case List')

    for case_block in content.find_all('a', 'articles-grid__posts-list-item'):
        case = parse_case_block(case_block)
        cases.append(case)

    return cases


def parse_case_block(case_block):
    title = get_text_or_empty(case_block.find('h3', 'll__copy--large articles-grid__posts-item-title')).strip()
    desc = get_text_or_empty(case_block.find('p', 'll__copy')).strip()
    status = get_text_or_empty(case_block.find('div', 'judicial-archive__case-status')).replace('Case', '').strip()
    state = get_text_or_empty(case_block.find('span', 'll__copy-bold').parent).replace('Court:', '').strip()
    url = case_block.get('href')
    date = scrape_case_date(url)
    return {
        'title': title,
        'desc': desc,
        'status': status,
        'date': date,
        'state': state,
        'url': url
    }


def scrape_case_date(url):
    content = scrape_html(url)
    print(f'Downloaded Lambda Legal Case Page {url}')

    date = get_date_from_history(content)
    if date is not None:
        return date

    date = get_date_from_docs(content, 'sectcomplaint-docs')
    if date is not None:
        return date

    date = get_date_from_docs(content, 'sectdeclaration-docs')
    if date is not None:
        return date

    date = get_date_from_docs(content, 'sectpreliminary-injunction-docs')
    if date is not None:
        return date

    date = get_date_from_docs(content, 'sectmemoranda-docs')
    if date is not None:
        return date

    date = get_date_from_docs(content, 'sectother-docs')
    if date is not None:
        return date


def get_date_from_history(page):
    history_section = page.find('div', id='secthistory')
    if history_section is None:
        return None
    return get_text_or_empty(history_section.find('strong')).replace(':', '').strip()


def get_date_from_docs(page, sect_id):
    docs_section = page.find(id=sect_id)
    if docs_section is None:
        return None
    doc_link = docs_section.find('a')
    if doc_link is None:
        return None
    return get_text_or_empty(doc_link).split('(')[1].replace(')', '').strip()


def get_text_or_empty(tag):
    if tag is None:
        return ''
    return tag.get_text()
