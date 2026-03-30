import re   # Used for pattern matching (regular expressions)


# ================= PORTER STEMMER =================
class PorterStemmer:

    def __init__(self):
        
        self.vowel = re.compile(r'[aeiou]')

        
        self.double_consonant = re.compile(r'([^aeiou])\1$')

        
        self.cvc_pattern = re.compile(r'[^aeiou][aeiou][^aeiouwxy]$')


    # ---------- Measure Function ----------
    # Counts number of vowel-consonant pairs (VC)
    def measure(self, stem):
        form = re.sub(r'[^aeiou]+', 'C', stem)  
        form = re.sub(r'[aeiou]+', 'V', form)    
        return form.count('VC')                  


    # ---------- Check if vowel exists ----------
    def contains_vowel(self, stem):
        return bool(self.vowel.search(stem))


    # ---------- Stage 1a (plural removal) ----------
    def stage1a(self, word):
        if word.endswith("sses"):
            return word[:-2]      # classes → class
        elif word.endswith("ies"):
            return word[:-2]      # babies → babi
        elif word.endswith("ss"):
            return word           # no change
        elif word.endswith("s"):
            return word[:-1]      # cats → cat
        return word


    # ---------- Stage 1b (past tense / ing) ----------
    def stage1b(self, word):

        
        if word.endswith("eed"):
            stem = word[:-3]
            if self.measure(stem) > 0:
                return stem + "ee"

        
        elif word.endswith("ed"):
            stem = word[:-2]
            if self.contains_vowel(stem):
                word = stem

        
        elif word.endswith("ing"):
            stem = word[:-3]
            if self.contains_vowel(stem):
                word = stem

        # Additional rules
        if word.endswith(("at","bl","iz")):
            word += "e"   

        elif self.double_consonant.search(word) and not word.endswith(("l","s","z")):
            word = word[:-1]   # running → run

        elif self.measure(word) == 1 and self.cvc_pattern.search(word):
            word += "e"   # hop → hope

        return word


    # ---------- Stage 1c (y → i) ----------
    def stage1c(self, word):
        if word.endswith("y"):
            stem = word[:-1]
            if self.contains_vowel(stem):
                return stem + "i"   # happy → happi
        return word


    # ---------- Stage 2 (replace suffixes) ----------                educational → education
    def stage2(self, word):

        # Dictionary of suffix replacements                          
        rules = {
            "ational": "ate","tional": "tion","enci": "ence","anci": "ance",
            "izer": "ize","abli": "able","alli": "al","entli": "ent",
            "eli": "e","ousli": "ous","ization": "ize","ation": "ate",
            "ator": "ate","alism": "al","iveness": "ive","fulness": "ful",
            "ousness": "ous","aliti": "al","iviti": "ive","biliti": "ble"
        }

        for suf, rep in rules.items():
            if word.endswith(suf):
                stem = word[:-len(suf)]
                if self.measure(stem) > 0:
                    return stem + rep   # replace suffix
        return word


    # ---------- Stage 3 ----------            logical → logic useful → use
    def stage3(self, word):

        rules = {
            "icate": "ic","ative": "","alize": "al",
            "iciti": "ic","ical": "ic","ful": "","ness": ""
        }

        for suf, rep in rules.items():
            if word.endswith(suf):
                stem = word[:-len(suf)]
                if self.measure(stem) > 0:
                    return stem + rep
        return word


    # ---------- Stage 4 (remove suffix completely) ----------
    def stage4(self, word):

        suffixes = [
            "al","ance","ence","er","ic","able","ible","ant",
            "ement","ment","ent","ion","ou","ism","ate",
            "iti","ous","ive","ize"
        ]

        for suf in suffixes:
            if word.endswith(suf):
                stem = word[:-len(suf)]
                if self.measure(stem) > 1:

                    # Special condition for "ion"
                    if suf == "ion":                           #action → act (allowed)lion → not changed 
                        if stem.endswith(("s","t")):
                            return stem
                    else:
                        return stem
        return word


    # ---------- Stage 5 (final cleanup) ----------
    def stage5(self, word):

        # Remove ending 'e'             rate → rat
        if word.endswith("e"):
            stem = word[:-1]
            m = self.measure(stem)

            if m > 1 or (m == 1 and not self.cvc_pattern.search(stem)):
                word = stem

        # Remove double 'l'
        if self.measure(word) > 1 and word.endswith("ll"):        # fall → fal
            word = word[:-1]

        return word


    # ---------- MAIN STEM FUNCTION ----------
    def stem(self, word):

        word = word.lower()   # convert to lowercase

        # Pass word through all stages
        word = self.stage1a(word)
        word = self.stage1b(word)
        word = self.stage1c(word)
        word = self.stage2(word)
        word = self.stage3(word)
        word = self.stage4(word)
        word = self.stage5(word)

        return word


# ================= CREATE OBJECT =================
stemmer = PorterStemmer()


# ================= STREAMLIT FRONTEND =================
def run_streamlit():
    import streamlit as st

    st.title("🧠 Porter Stemmer NLP App")

    # User input box
    text = st.text_area("Enter a sentence:")

    # Button click
    if st.button("Stem Words"):

        tokens = text.split()   # split sentence into words

        # Apply stemming on each word
        result = [stemmer.stem(t) for t in tokens]

        # Display result
        st.subheader("Stemmed Output:")
        st.success(" ".join(result))


# ================= TERMINAL MODE =================
def run_terminal():

    text = input("Enter sentence: ")

    tokens = text.split()   # split sentence

    # Apply stemming
    result = [stemmer.stem(t) for t in tokens]

    print("Stemmed:", " ".join(result))


# ================= MAIN EXECUTION =================
if __name__ == "__main__":

    try:
        import streamlit as st   # check if running in Streamlit
        run_streamlit()          # run UI
    except:
        run_terminal()           # otherwise run terminal