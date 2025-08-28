import re

BAD_WORDS = {
    "hate": "Please keep the conversation respectful. I can still help with book ideas.",
    "idiot": "Let's stay polite—happy to suggest books if you share your interests.",
    "stupid": "Let's keep things positive—I'm here to help with book suggestions.",
    "damn": "Let's keep the conversation clean. I can help with book ideas.",
    "hell": "Let's keep the conversation clean. I can help with book ideas.",
    "shit": "Please avoid profanity. I'm happy to help with book recommendations.",
    "fuck": "Please avoid profanity. I'm happy to help with book recommendations.",
    "sex": "Let's keep the conversation appropriate. I can recommend books on many topics.",
    "porn": "Sorry, I can't assist with that topic.",
    "nude": "Sorry, I can't assist with that topic.",
    "kill": "Let's keep things safe and positive. I can recommend books if you share your interests.",
    "racist": "Discriminatory language is not allowed. I can help with book ideas.",
    "sexist": "Discriminatory language is not allowed. I can help with book ideas.",
    "homophobic": "Discriminatory language is not allowed. I can help with book ideas.",
    "nazi": "Discriminatory language is not allowed. I can help with book ideas.",
}


# Check if the user is rude, inappropriate, or uses banned language
def is_clean(text: str) -> tuple[bool, str|None]:
    lowered = text.lower()

    for word, msg in BAD_WORDS.items():
        if re.search(rf"\b{re.escape(word)}\b", lowered) or word in lowered:
            return False, msg
        
    return True, None
