
def is_valid_format_badge(badge_id):
    # Badge format validation
    if not badge_id or len(badge_id) != 3:
        return False
    return badge_id[0].upper() == 'B' and badge_id[1:].isdigit()


def is_valid_description(desc):
    # Check minimum length and remove spaces
    if not desc:
        return False
    return len(desc.strip()) >= 5

class AccessAttempt:
    #A class-based container for security logs.
    def __init__(self, badge_id, area_requested, access_result):
        self.badge_id = badge_id
        self.area = area_requested
        self.result = access_result
        # Cleaned version of the area name.
        self.formatted_area = area_requested.strip().capitalize()

    def __repr__(self):
        return f"(AccessAttempt {self.badge_id} -> {self.formatted_area})" 