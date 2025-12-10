import re


PROC_REGEX_PATT=r'(\d{16})|(\d{4}\.\d{4}/\d{7}-\d{1})|(\d{4}.*\d{4}.*\d{4}.*\d{1})'


class ProcNumExtractor:

    def __init__(self)->None:

        self.proc_regex_patt = re.compile(PROC_REGEX_PATT)

    def extract_proc_num(self, proc_str: str) -> str | None:

        match = self.proc_regex_patt.search(proc_str)
        if match:
            # Return the first non-None matched group
            for group in match.groups():
                if group is not None:
                    return group
        return None
    
    def clean_match(self, match: str) -> str | None:
        
        digits = re.sub(r'[^\d]', '', match)
        if digits:
            return digits
        else:
            return None
        
    def extract_and_clean(self, proc_str: str) -> int | None:

        match = self.extract_proc_num(proc_str)
        if match:
            return int(self.clean_match(match))
        return None
    
    def __call__(self, proc_str: str) -> int | None:
        
        return self.extract_and_clean(proc_str)