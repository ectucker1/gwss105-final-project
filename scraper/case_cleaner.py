from dateutil.parser import parser as dateparser
from datetime import datetime
import us


state_names = [state.name for state in us.states.STATES_AND_TERRITORIES]


def clean_cases(cases):
    cleaned = [clean_case(case) for case in cases if clean_case(case) is not None]

    deduplicated = []
    for case in cleaned:
        if not any(existing['title'] == case['title'] for existing in deduplicated):
            deduplicated.append(case)

    return deduplicated


def clean_case(case):
    case = case.copy()

    parser = dateparser()

    if len(case['date']) > 0:
        if case['date'] == 'Late 2020':
            case['date'] = datetime(2020, 12, 1).isoformat()
        if case['date'] == 'Early 2017':
            case['date'] = datetime(2017, 1, 1).isoformat()
        else:
            case['date'] = parser.parse(case['date']).isoformat()

    if len(case['date']) == 0:
        return None

    case['state'] = get_state(case)
    if len(case['state']) == 0:
        return None

    return case


def get_state(case):
    downloaded_state = case['state']

    if len(downloaded_state) > 0:
        # Exact match
        if downloaded_state in state_names:
            return downloaded_state

        # Downloaded contains real - e.g. "Northern California"
        for real_state in state_names:
            if real_state in downloaded_state:
                return real_state

        # Supreme Court
        if 'U.S. Supreme' in downloaded_state:
            return 'Federal'
        if 'United States Supreme' in downloaded_state:
            return 'Federal'
        if 'Supreme Court of the United States' in downloaded_state:
            return 'Federal'

        if 'St. Louis' in downloaded_state:
            return us.states.MO.name

        if 'Equal Employment Opportunity Commission' == downloaded_state:
            return 'Federal'

        if 'District of Columbia' in downloaded_state:
            return us.states.DC.name

        if 'Orange Unified School District' in case['title']:
            return us.states.CA.name

        if 'Nabozny v. Podlesny' == case['title']:
            return us.states.WI.name

        return ''

    for real_state in state_names:
        if real_state in case['title']:
            return real_state

    for real_state in state_names:
        if real_state in case['desc']:
            return real_state

    if 'Cargian v. Breitling' == case['title']:
        return us.states.NY.name

    if 'Act' in case['title']:
        return ''

    if 'Library of Congress' in case['title']:
        return 'Federal'

    if 'Maniaci v. Kulstad' == case['title']:
        return us.states.MT.name

    if 'Advocacy' in case['title']:
        return ''

    if 'Seals v. Old Dominion Freight Lines, Inc.' == case['title']:
        return us.states.TN.name

    if 'Ramona, CA Harvey Milk Censorship' == case['title']:
        return us.states.CA.name

    if 'Outing at Hollis F. Price Middle College High School' == case['title']:
        return us.states.TN.name

    if 'Deane & Polyak v. Conaway' == case['title']:
        return us.states.MD.name

    if 'In re Rockefeller' == case['title']:
        return us.states.NY.name

    if 'Obergefell v. Hodges / Henry v. Hodges' == case['title']:
        return us.states.OH.name

    return ''
