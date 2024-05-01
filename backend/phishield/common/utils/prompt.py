def analyse_email_prompt(object: str) -> str:
    return f"""
        As a cybersecurity specialist, your task is to analyze the following JSON extracted from a preprocessing tool to determine if an email is indicative of a phishing attempt.
        Object:
        ```json
            {object}
        ```

        Submit your findings as JSON-formatted output with the following keys:
        - score: int (indicates phishing risk on a scale of 0 to 100)
        - suspicious_elements : str (enumeration of suspicious elements found on the site or "No suspicious elements" if not applicable)
        """
