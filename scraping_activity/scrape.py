import requests
from bs4 import BeautifulSoup
import random
import re
import time
import csv
from collections import defaultdict

def scrape_article(url):
    max_retries = 3
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    delay = int(retry_after)
                else:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                
                print(f"Attempt {attempt + 1} failed with 429. Retrying after {delay} seconds...")
                time.sleep(delay)
            elif attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(base_delay * (2 ** attempt) + random.uniform(0, 1))
            else:
                print(f"Maximum retries exceeded. Error: {e}")
                return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the title
    title = soup.find('h1', class_='post-single__title')
    title_text = title.get_text(strip=True) if title else 'No title found'
    
    # Find the article body
    body = soup.find('div', class_='post-single__body')
    body_text = body.get_text(strip=True) if body else ''
    
    # Check for keywords
    has_marcos = 'Marcos' in title_text
    has_sara = 'Sara' in title_text
    
    # Extract publication year
    pub_time = soup.find('time', class_='entry-date published post__timeago')
    pub_year = pub_time['datetime'][:4] if pub_time and pub_time.has_attr('datetime') else 'Unknown'
    
    return {
        'url': url,
        'title': title_text,
        'body': body_text,
        'has_marcos': has_marcos,
        'has_sara': has_sara,
        'pub_year': pub_year
    }

# List of URLs
urls = [
    'https://www.rappler.com/philippines/marcos-updates-list-priority-measures-ledac-divorce-sogie-bills-excluded-june-2024/',
    'https://www.rappler.com/philippines/mindanao/sara-duterte-downplays-opposition-role-thinks-still-friends-with-marcos/',
    'https://www.rappler.com/voices/opinion-genuine-ilokano-reflections-marcos-loyalism/',
    'https://www.rappler.com/newsbreak/iq/stories-tracking-marcos-disinformation-propaganda-machinery/',
    'https://www.rappler.com/newsbreak/iq/stories-tracking-marcos-disinformation-propaganda-machinery/',
    'https://www.rappler.com/philippines/marcos-approves-gradual-return-old-school-calendar-may-2024/',
    'https://www.rappler.com/philippines/bongbong-marcos-evades-millions-dollars-contempt-judgment-united-states/',
    'https://www.rappler.com/philippines/marcos-reaction-sara-duterte-resignation-cabinet-impact-uniteam-june-2024/',
    'https://www.rappler.com/newsbreak/iq/breakdown-billions-recovered-marcos-ill-gotten-wealth-by-pcgg-more-to-get/',
    'https://www.rappler.com/philippines/bongbong-marcos-cambridge-analytica-rebrand-family-image/',
    'https://www.rappler.com/voices/thought-leaders/opinion-sheila-coronel-on-fathers-daughters-marcos-family-and-mine/',
    'https://www.rappler.com/philippines/malacanang-flags-deepfake-audio-marcos-ordering-military-attack-april-2024/',
    'https://www.rappler.com/voices/thought-leaders/opinion-leila-de-lima-hope-ferdinand-marcos-jr-presidency-end-suppression-dissent/',
    'https://www.rappler.com/philippines/marcos-jr-asserts-charter-change-limited-economic-reforms-nothing-more/',
    'https://www.rappler.com/philippines/marcos-open-economic-charter-change-january-2024/',
    'https://www.rappler.com/philippines/elections/ferdinand-bongbong-marcos-jr-never-saw-gold-told-court-source-wealth/',
    'https://www.rappler.com/philippines/elections/ferdinand-bongbong-marcos-jr-wins-president-philippines-may-2022/',
    'https://www.rappler.com/philippines/marcos-rejects-proposal-use-water-cannon-against-china-west-sea/',
    'https://www.rappler.com/newsbreak/inside-track/how-rift-between-liza-marcos-sara-duterte-began-rodrigo-bangag-comment-bongbong/',
    'https://www.rappler.com/philippines/marcos-grants-amnesty-rebel-groups-cpp-milf-mnlf/',
    'https://www.rappler.com/newsbreak/iq/everything-to-know-news-context-sara-duterte-resignation-marcos-jr-cabinet/',
    'https://www.rappler.com/philippines/marcos-duterte-approval-ratings-drop-double-digits-pulse-asia-september-2023/',
    'https://www.rappler.com/newsbreak/in-depth/marcos-jr-platitudes-media-relationship-first-year/',
    'https://www.rappler.com/philippines/sara-duterte-response-liza-araneta-marcos-tirades-april-2024/',
    'https://www.rappler.com/newsbreak/iq/timeline-sara-duterte-marcos-jr-cabinet-resignation/',
    'https://www.rappler.com/philippines/marcos-laments-poor-showing-asia-university-rankings-2024/',
    'https://www.rappler.com/newsbreak/in-depth/ferdinand-marcos-jr-plays-catch-up-fight-west-philippine-sea-after-duterte-administration/',
    'https://www.rappler.com/philippines/ukraine-zelenskyy-meets-marcos-jr-manila-june-2024/',
    'https://www.rappler.com/newsbreak/in-depth/158400-politics-coco-levy-marcos-noynoy-aquino/',
    'https://www.rappler.com/voices/imho/124682-marcos-economy-golden-age-philippines/',
    'https://www.rappler.com/philippines/marcos-signs-ecosystem-natural-capital-accounting-system-law-may-2024/',
    'https://www.rappler.com/newsbreak/in-depth/liza-araneta-marcos-first-lady-philippines/',
    'https://www.rappler.com/philippines/sara-duterte-appeal-marcos-jr-reconsider-resumption-peace-talks-communist-rebels/',
    'https://www.rappler.com/newsbreak/inside-track/ferdinand-marcos-jr-warns-against-overreactions-west-philippine-sea/',
    'https://www.rappler.com/philippines/elections/records-bongbong-marcos-1997-tax-conviction-hounds-presidential-campaign-2022-polls/',
    'https://www.rappler.com/philippines/marcos-tells-chinese-general-south-china-sea-peace-world-issue/',
    'https://www.rappler.com/newsbreak/inside-track/have-marcos-jr-cabinet-memorized-bagong-pilipinas-hymn-pledge/',
    'https://www.rappler.com/philippines/elections/marcos-jr-massive-overseas-filipinos-backing-2022/',
    'https://www.rappler.com/philippines/marcos-death-filipino-serviceman-foreign-attack-triggers-mutual-defense-treaty-united-states/',
    'https://www.rappler.com/philippines/video-marcos-jr-independence-day-ceremony-2024/',
    'https://www.rappler.com/philippines/marcos-says-government-eyes-shift-old-academic-calendar-2025/',
    'https://www.rappler.com/philippines/marcos-administration-proposal-confidential-intelligence-funds-op-ovp-deped-2024/',
    'https://www.rappler.com/newsbreak/iq/143592-ferdinand-marcos-world-war-ii-medals-explained/',
    'https://www.rappler.com/philippines/marcos-government-return-icc-under-study/',
    'https://www.rappler.com/business/marcos-jeepney-consolidation-deadline-april-30-2024-final/',
    'https://www.rappler.com/philippines/marcos-jr-jeepney-modernization-implemented-different-way/',
    'https://www.rappler.com/philippines/marcos-jr-lifts-price-ceiling-rice/',
    'https://www.rappler.com/philippines/video-goodbye-uniteam-sara-duterte-resigns-marcos-cabinet/',
    'https://www.rappler.com/philippines/elections/ferdinand-marcos-jr-benefited-facebook-disinformation-study/',
    'https://www.rappler.com/voices/imho/opinion-why-does-bongbong-marcos-get-so-much-support/',
    'https://www.rappler.com/philippines/marcos-signs-new-philippine-passport-act-allowing-online-applications/',
    'https://www.rappler.com/business/marcos-jr-faces-bitter-economics-sugar-imports-philippines/',
    'https://www.rappler.com/philippines/marcos-designates-carlito-galvez-jr-peace-summit-ukraine-june-2024/',
    'https://www.rappler.com/philippines/us-state-department-statement-openness-marcos-icc/',
    'https://www.rappler.com/philippines/elections/rappler-to-marcos-camp-stop-harassing-journalists/',
    'https://www.rappler.com/business/marcos-jr-government-cuts-tariffs-imported-rice-june-2024/',
    'https://www.rappler.com/newsbreak/podcasts-videos/marcos-duterte-show-walang-forever-in-politics/',
    'https://www.rappler.com/philippines/broadcaster-percy-lapid-killed-in-las-pinas-2nd-under-marcos/',
    'https://www.rappler.com/philippines/84959-bongbong-marcos-statement-oxford-wharton/',
    'https://www.rappler.com/philippines/experts-comment-ferdinand-bongbong-marcos-jr-view-west-philippine-sea/',
    'https://www.rappler.com/philippines/remulla-order-nbi-probe-marcos-jr-deepfake-audio-ordering-military-attack/',
    'https://www.rappler.com/newsbreak/iq/84936-highlights-bongbong-marcos-legislator/',
    'https://www.rappler.com/philippines/marcos-partido-federal-pilipinas-lakas-cmd-forge-alliance-2025-midterms/',
    'https://rappler.com/philippines/marcos-signs-salt-industry-development-law-march-2024/',
    'https://www.rappler.com/philippines/marcos-jr-response-arelma-ill-gotten-wealth-case-april-2024/',
    'https://www.rappler.com/newsbreak/investigative/245540-networked-propaganda-false-narratives-from-the-marcos-arsenal/',
    'https://www.rappler.com/newsbreak/iq/146867-look-back-philippine-constabulary-marcos/'
    'https://www.rappler.com/philippines/marcos-reappoints-eduardo-manalo-special-envoy-overseas-filipinos-concerns/',
    'https://www.rappler.com/philippines/marcos-orders-overhaul-redundant-government-performance-management-incentives-systems/',
    'https://www.rappler.com/philippines/elections/ferdinand-bongbong-marcos-jr-will-set-aside-hague-ruling-united-states-treaty-dealing-china/',
    'https://www.rappler.com/philippines/juan-ponce-enrile-political-survivor-marcos-jr-presidency/',
    'https://www.rappler.com/philippines/marcos-says-manila-not-rejected-beijing-proposals-south-china-sea-conflict-march-2024/',
    'https://www.rappler.com/philippines/marcos-orders-review-workers-minimum-wage-labor-day-may-2024/',
    'https://www.rappler.com/philippines/investment-deals-marcos-jr-germany-visit-march-2024/',
    'https://www.rappler.com/philippines/marcos-vows-countermeasures-against-china-attacks-march-28-2024/',
    'https://www.rappler.com/newsbreak/in-depth/240949-status-updates-rulings-court-cases-vs-marcos-family/',
    'https://www.rappler.com/philippines/103772-bongbong-marcos-regime-no-apologies/',
    'https://www.rappler.com/philippines/menardo-guevarra-marcos-jr-solicitor-general/',
    'https://www.rappler.com/philippines/marcos-statement-ayungin-incident-china-not-armed-attack-west-sea-june-2024/',
    'https://www.rappler.com/philippines/diokno-says-marcos-jr-agrees-reduce-military-pension/',
    'https://www.rappler.com/philippines/marcos-jr-says-government-not-allow-rodrigo-duterte-arrest-international-criminal-court/',
    'https://www.rappler.com/philippines/mindanao/sara-duterte-says-father-brothers-run-senate-seats-2025-elections/',
    'https://www.rappler.com/philippines/sara-duterte-response-continued-china-bullying-no-comment-april-8-2024/',
    'https://www.rappler.com/voices/newsletters/investigates-china-west-philippine-sea-de-lima-free-sara-duterte-quit-deped-secretary/',
    'https://www.rappler.com/newsbreak/in-depth/sara-duterte-brings-red-tagging-deped/',
    'https://www.rappler.com/philippines/document-sara-duterte-letter-requesting-confidential-funds-2022/',
    'https://www.rappler.com/newsbreak/inside-track/negros-occidental-governor-sees-sara-duterte-backed-challenger-2025-elections/'
    'https://www.rappler.com/philippines/reactions-sector-leaders-politicians-provinces-sara-duterte-resignation-deped/',
    'https://www.rappler.com/voices/thought-leaders/the-slingshot-red-zipper-mouth-of-sara-duterte/',
    'https://www.rappler.com/philippines/marcos-defends-sara-duterte-silence-china-aggression-sea-dispute/',
    'https://www.rappler.com/philippines/sara-duterte-draws-flak-statement-confidential-fund-critics-enemies-peace-october-2023/',
    'https://www.rappler.com/philippines/experts-petition-supreme-court-order-sara-duterte-return-confidential-funds/',
    'https://www.rappler.com/philippines/sara-duterte-resignation-filipinos-online-wish-list-next-deped-secretary/',
    'https://www.rappler.com/philippines/sara-duterte-viral-video-angry-teacher-she-just-human-no-penalties/',
    'https://www.rappler.com/philippines/mindanao/davao-confidential-funds-spending-soared-under-sara-duterte/',
    'https://www.rappler.com/philippines/sara-duterte-urged-fix-teaching-quality-chair-teacher-education-council/',
    'https://www.rappler.com/philippines/sara-duterte-statement-government-cooperation-icc-probe-drug-war/',
    'https://www.rappler.com/newsbreak/in-depth/sara-duterte-resorts-personal-attacks-critics-confidential-funds-budget/',
    'https://www.rappler.com/newsbreak/in-depth/how-sara-duterte-led-department-education/',
    'https://www.rappler.com/philippines/sara-duterte-ntf-elcac-co-vice-chairperson/',
    'https://www.rappler.com/philippines/marcos-says-no-rift-vice-president-sara-after-rodrigo-duterte-tirades/',
    'https://www.rappler.com/newsbreak/in-depth/sara-duterte-gives-up-bid-confidential-funds-2024-budget-political-strategy/',
    'https://www.rappler.com/philippines/results-pulse-asia-2028-presidential-vice-presidential-survey-march-2024/',
    'https://www.rappler.com/philippines/gloria-macapagal-arroyo-sara-duterte-history/',
    'https://www.rappler.com/philippines/sara-duterte-satisfaction-rating-drops-octa-research-survey-october-2023/',
    'https://www.rappler.com/newsbreak/in-depth/new-opposition-leader-why-not-sara-duterte/',
    'https://www.rappler.com/philippines/vp-sara-duterte-resignation-letter-department-education-secretary-ntf-elcac-vice-chairperson/',
    'https://www.rappler.com/philippines/sara-duterte-says-marcos-still-trusts-her/',
    'https://www.rappler.com/newsbreak/investigative/227422-pcij-report-rodrigo-sara-paolo-duterte-big-spikes-wealth-cash-public-office/',
    'https://www.rappler.com/newsbreak/in-depth/marcos-duterte-clans-clash-should-sara-resign-from-cabinet/',
    'https://www.rappler.com/voices/thought-leaders/opinion-sara-duterte-will-she-do-like-binay-or-robredo/',
    'https://www.rappler.com/newsbreak/in-depth/sara-duterte-gives-up-bid-confidential-funds-2024-budget-political-strategy/',
    'https://www.rappler.com/philippines/house-leaders-back-martin-romualdez-decry-bickering-rift-with-sara-duterte/',
    'https://www.rappler.com/philippines/sara-duterte-to-run-next-election/',
    'https://www.rappler.com/voices/thought-leaders/opinion-does-sara-duterte-have-game-plan-elections/',
    'https://www.rappler.com/newsbreak/inside-track/muted-support-sara-duterte-attends-rally-calling-bongbong-marcos-resignation/',
    'https://www.rappler.com/philippines/marcos-approves-vice-president-sara-duterte-key-programs-department-education-matatag-agenda-april-2024/',
    'https://www.rappler.com/philippines/elections/bongbong-marcos-sara-duterte-tandem-official-pfp-lakas/',
    'https://www.rappler.com/philippines/sara-duterte-resigns-lakas-cmd-may-19-2023/',
    'https://www.rappler.com/philippines/sara-duterte-resigns-lakas-cmd-may-19-2023/',
    'https://www.rappler.com/philippines/marcos-downplays-sara-duterte-impeachment-rumors-november-2023/',
    'https://www.rappler.com/philippines/sara-duterte-report-k12-important-lessons-missing/',
    'https://www.rappler.com/philippines/sara-duterte-promises-more-benefits-teachers-january-2024/',
    'https://www.rappler.com/philippines/elections/sara-dutete-joins-lakas-cmd-party-november-2021/',
    'https://www.rappler.com/philippines/groups-reactions-sara-duterte-proposal-mandatory-military-service-filipino-youth/',
    'https://www.rappler.com/philippines/sara-duterte-not-cooperate-icc-investigation-drug-war-human-rights/',
    'https://www.rappler.com/philippines/top-approved-most-trusted-government-officials-pulse-asia-survey-march-2023/',
    'https://www.rappler.com/newsbreak/inside-track/estelito-mendoza-sara-duterte-lawyer-confidential-funds-case-supreme-court/',
    'https://www.rappler.com/philippines/ex-quiboloy-follower-duterte-sara-left-kojc-glory-mountain-with-guns/',
    'https://www.rappler.com/philippines/mindanao/duterte-rodrigo-baste-paolo-snub-marcos-public-events-davao-city-february-2024/'
    'https://www.rappler.com/philippines/elections/profile-rodrigo-daughter-sara-duterte/',
    'https://www.rappler.com/philippines/visayas/iloilo-bacolod-mayors-trenas-benitez-take-sides-back-first-lady-liza-marcos-amid-rift-sara-duterte/',
    'https://www.rappler.com/philippines/sara-duterte-promises-more-benefits-teachers-january-2024/',
    'https://www.rappler.com/philippines/elections/sara-duterte-endorses-senate-slate-friends-2022/',
    'https://www.rappler.com/newsbreak/inside-track/martin-romualdez-sara-duterte-public-display-friendship-after-rift-july-2023/',
    'https://www.rappler.com/philippines/sara-duterte-response-vice-presidential-bid-speaker-romualdez-no-part/',
    'https://www.rappler.com/philippines/marcos-downplays-sara-duterte-liza-rift-shrugs-off-calls-fire-her-deped-april-2024/',
    'https://www.rappler.com/philippines/visayas/bacolod-teachers-hail-sara-duterte-resignation-seek-raise-reforms/',
    'https://www.rappler.com/newsbreak/inside-track/sara-duterte-dodges-issue-bags-guns-apollo-quiboloy/',
    'https://www.rappler.com/philippines/246150-sara-duterte-slams-use-manila-song-sea-games-opening-ceremonies-2019/',
    'https://www.rappler.com/newsbreak/explainers/dangers-justifying-vice-president-sara-duterte-2022-confidential-funds/',
    'https://www.rappler.com/sports/ncaa/john-amores-gushes-over-letter-from-sara-duterte/',
    'https://www.rappler.com/newsbreak/inside-track/sara-duterte-gloria-arroyo-courtesy-call-eduardo-manalo/',
    'https://www.rappler.com/philippines/sara-duterte-asks-marcos-jr-congress-give-billions-fix-education-problems/',
    'https://www.rappler.com/philippines/mindanao/red-tagged-by-sara-duterte-davao-teacher-story-experience/',
    'https://www.rappler.com/newsbreak/in-depth/sara-duterte-to-fix-education-if-given-billions-is-this-enough/',
    'https://www.rappler.com/voices/thought-leaders/slingshot-sara-duterte-millions-confidential-funds-ovp-discombobulates/',
    'https://www.rappler.com/newsbreak/fact-check/sara-duterte-still-vice-president-deped-secretary/',
    'https://www.rappler.com/voices/thought-leaders/vantage-point-sara-duterte-2028-elections/',
    'https://www.rappler.com/philippines/elections/gibo-teodoro-offers-sara-duterte-running-mate/',
    'https://www.rappler.com/philippines/coa-flags-sara-duterte-ovp-over-immediate-creation-satellite-offices/',
    'https://www.rappler.com/philippines/sara-duterte-info-officer-admits-presence-beach-party-later-raided-for-drugs/',
    'https://www.rappler.com/newsbreak/in-depth/how-sara-duterte-led-department-education/',
    'https://www.rappler.com/philippines/elections/marcos-jr-says-sara-duterte-education-secretary/',
    'https://www.rappler.com/voices/thought-leaders/pastilan-inday-sara-duterte-top-secret-curriculum-confidential-intelligence-funds/',
    'https://www.rappler.com/philippines/office-vice-president-drops-request-confidential-funds-2024-budget/',
    'https://www.rappler.com/philippines/elections/sara-duterte-running-for-vice-president-2022/',
    'https://www.rappler.com/philippines/elections/225065-sara-duterte-calls-otso-diretso-bets-liars/',
    'https://www.rappler.com/philippines/elections/duterte-says-sara-vice-president-run-decision-marcos-camp/',
    'https://www.rappler.com/philippines/video-interview-who-opposition-is-after-sara-duterte-resignation-marcos-jr-cabinet-june-2024/',
    'https://www.rappler.com/philippines/elections/willie-revillame-one-cebu-sara-duterte-endorsement/',
    'https://www.rappler.com/philippines/elections/duterte-tells-sara-pick-bong-go-as-vp-or-support-tandem/'
]

# Counters for articles containing the keywords
count_marcos_only = 0
count_sara_only = 0
count_both = 0

# Dictionary to store counts per year
keyword_counts_per_year = defaultdict(lambda: {'marcos': 0, 'sara': 0, 'both': 0})

# List to store article data
articles_data = []

# Scrape each URL
for url in urls:
    article_data = scrape_article(url)
    
    if article_data:
        has_marcos = article_data['has_marcos']
        has_sara = article_data['has_sara']
        pub_year = article_data['pub_year']
        
        if has_marcos and has_sara:
            count_both += 1
            keyword_counts_per_year[pub_year]['both'] += 1
        elif has_marcos:
            count_marcos_only += 1
            keyword_counts_per_year[pub_year]['marcos'] += 1
        elif has_sara:
            count_sara_only += 1
            keyword_counts_per_year[pub_year]['sara'] += 1
        
        articles_data.append(article_data)

# Print the results
print(f"Articles with Marcos only: {count_marcos_only}")
print(f"Articles with Sara only: {count_sara_only}")
print(f"Articles with both Marcos and Sara: {count_both}")

# Print keyword counts per year
print("\nKeyword counts per year:")
for year, counts in keyword_counts_per_year.items():
    print(f"{year}: Marcos: {counts['marcos']}, Sara: {counts['sara']}, Both: {counts['both']}")

# Write the data to a CSV file
csv_file = 'articles.csv'
csv_columns = ['url', 'title', 'body', 'has_marcos', 'has_sara', 'pub_year']

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in articles_data:
            writer.writerow(data)
except IOError:
    print("I/O error")
