from scraper.scrape import scrape_html


def get_all_cases():
    page = 1
    cases = []

    while 0 < page:
        content = scrape_html(get_case_listing_url(page))
        print(f'Downloaded ACLU Case Page {page}')

        for case_block in content.find_all('div', 'case__all__section'):
            case = parse_case_block(case_block)
            cases.append(case)

        # Advance to the next page, if it exists
        if page_exists(content, page + 1):
            page = page + 1
        else:
            page = 0

    return cases


def parse_case_block(case_block):
    title = get_text_or_empty(case_block.find('div', 'is-special-size-30')).strip()
    desc = get_text_or_empty(case_block.find('div', 'case__summary')).strip()
    status = get_text_or_empty(case_block.find('div', 'is-capitalized is-size-6 pb-sm')).replace('Status:', '').strip()
    date = get_text_or_empty(case_block.find('div', 'case__all__date')).strip()
    state = get_text_or_empty(case_block.find('div', 'case__icon-area')).strip()
    url = case_block.find('a', 'blocklink').get('href')
    return {
        'title': title,
        'desc': desc,
        'status': status,
        'date': date,
        'state': state,
        'url': url
    }


def get_text_or_empty(tag):
    if tag is None:
        return ''
    return tag.get_text()


def page_exists(content, page):
    for link in content.find_all('a', 'page-numbers'):
        if len(link.get_text()) > 0:
            if int(link.get_text()) == page:
                return True
    return False


def get_case_listing_url(page):
    return f'https://wp.api.aclu.org/court-cases/page/{page}?issue=lgbtq-rights#all_content'
