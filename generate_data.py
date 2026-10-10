import csv
import random

random.seed(42)

age_groups = ['18–24', '25–34', '35–44', 'Under 18', '45–54', '55 or above']
age_weights = [0.45, 0.35, 0.12, 0.04, 0.03, 0.01]

genders = ['Male', 'Female', 'Prefer not to say']
gender_weights = [0.55, 0.42, 0.03]

difficulties = ['Never', 'Occasionally', 'Sometimes', 'Often', 'Always']
diff_weights = [0.08, 0.22, 0.35, 0.25, 0.10]

challenges_pool = [
    'Choosing colors that go well together',
    'Matching different clothing items to create an outfit',
    'Finding a style that suits my preferences',
    'Choosing clothes for different occasions',
    'Finding clothes that fit well',
    'Finding clothes within my budget',
    'Deciding which clothes to buy',
    'Regretting a clothing purchase'
]

decide_pool = [
    'My own judgment',
    'Advice from family or friends',
    'Social media or fashion creators',
    'Online articles or videos',
    'Advice from shop staff or stylists',
    'Fashion or shopping apps',
    'I usually choose whatever is convenient'
]

regret_pool = [
    'Never',
    'Once',
    'Two or three times',
    'Four or more times',
    "I don't remember",
    "I haven't purchased clothes in the past three months"
]
regret_weights = [0.18, 0.28, 0.34, 0.12, 0.05, 0.03]

useful_pool = ['Not at all useful', 'Slightly useful', 'Moderately useful', 'Very useful', 'Extremely useful', 'Not sure']
useful_weights = [0.04, 0.10, 0.24, 0.38, 0.20, 0.04]

features_pool = [
    'Suggestions for clothing colors',
    'Help matching clothes to create outfits',
    'Outfit recommendations for different occasions',
    'Suggestions based on my personal preferences',
    'Suggestions based on an optional photo',
    'Help choosing clothes within a budget',
    'Suggestions for combining clothes I already own',
    'Recommendations for clothes available to purchase'
]

concerns_pool = [
    'Privacy when sharing photos or personal information',
    'Recommendations might not suit me',
    'Recommendations might be inaccurate',
    'The service might cost too much',
    'It might be difficult to use',
    'It might offer limited clothing choices',
    'I prefer to choose clothes myself',
    'I have no concerns'
]

try_free_pool = ['Definitely would try it', 'Probably would try it', 'Not sure', 'Probably would not try it', 'Definitely would not try it']
try_free_weights = [0.42, 0.36, 0.12, 0.07, 0.03]

frequency_pool = ['Daily or almost daily', 'Several times a week', 'About once a week', 'A few times a month', 'Less than once a month', 'Never', 'Not sure']
frequency_weights = [0.15, 0.32, 0.25, 0.18, 0.05, 0.02, 0.03]

open_feedback_samples = [
    'Instant color matching based on skin tone and contrast palette.',
    'I need outfit combinations from clothes I already have in my closet.',
    'Quick morning styling suggestions so I do not waste time before work.',
    'Budget-friendly fashion advice that links directly to affordable stores.',
    'Accurate body type sizing recommendations to prevent clothes returns.',
    'Formal and semi-formal wear suggestions for office meetings and presentations.',
    'Casual weekend looks with sneakers and denim.',
    'Seasonal color palette analysis with warm vs cool undertone detection.',
    'Simple UI without too many ads or long questionnaires.',
    'Virtual try-on preview or side-by-side color comparisons.',
    'Weather-appropriate dressing suggestions combined with occasion type.',
    'Minimalist wardrobe / capsule wardrobe planning for men.',
    'Clear fit advice for athletic and slim builds.',
    'Privacy first - do not store my face/body photos on external cloud servers.'
]

headers = [
    'Timestamp',
    'What is your age group?',
    'How do you describe your gender?',
    'How often do you find it difficult to decide what clothes to wear?',
    'Which clothing-related challenges, if any, have you experienced?',
    'How do you usually decide what clothes to wear?',
    'In the past three months, how often have you regretted buying clothes because of their color, fit, style, or difficulty matching them with other items?',
    'How useful would it be to have a fashion recommendation app that provides real-time suggestions based on the types of clothes that suit your body type, skin tone, and personal style?',
    'Which features, if any, would be useful to you?',
    'What concerns, if any, would you have about using a service like this?',
    'If a service like this became available, how likely would you be to try it for free?',
    'If the service met your needs, how often do you think you would use it?',
    'What, if anything, would make a clothing recommendation service genuinely useful to you?'
]

rows = []
for i in range(1, 131):
    day = random.randint(1, 10)
    hour = random.randint(8, 22)
    minute = random.randint(10, 59)
    second = random.randint(10, 59)
    ts = f'2026-10-{day:02d} {hour:02d}:{minute:02d}:{second:02d}'
    
    age = random.choices(age_groups, weights=age_weights)[0]
    gender = random.choices(genders, weights=gender_weights)[0]
    diff = random.choices(difficulties, weights=diff_weights)[0]
    
    # challenges (choose 1-4)
    k_ch = random.randint(1, 4)
    ch = '; '.join(random.sample(challenges_pool, k_ch))
    
    # decide methods (choose 1-3)
    k_dec = random.randint(1, 3)
    dec = '; '.join(random.sample(decide_pool, k_dec))
    
    regret = random.choices(regret_pool, weights=regret_weights)[0]
    useful = random.choices(useful_pool, weights=useful_weights)[0]
    
    # features (choose 1-4)
    k_feat = random.randint(1, 4)
    feat = '; '.join(random.sample(features_pool, k_feat))
    
    # concerns (choose 1-3)
    k_con = random.randint(1, 3)
    con = '; '.join(random.sample(concerns_pool, k_con))
    
    try_free = random.choices(try_free_pool, weights=try_free_weights)[0]
    freq = random.choices(frequency_pool, weights=frequency_weights)[0]
    feedback = random.choice(open_feedback_samples) if random.random() < 0.65 else ''
    
    rows.append([ts, age, gender, diff, ch, dec, regret, useful, feat, con, try_free, freq, feedback])

out_path = r'c:\Users\ROHIT SAGAR PATRA\OneDrive\Documents\dashboard for survey\survey_responses.csv'
with open(out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f'Successfully generated {out_path} with {len(rows)} responses.')
