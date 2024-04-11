import re


class StaffValidation:

    @staticmethod
    def is_the_user_approved(staff):
        message = StaffValidation.is_email_and_phone_approved(staff)
        if message is None:
            message = StaffValidation.does_user_name_meet_requirements(staff.username)
            if message is None:
                message = StaffValidation.does_password_meet_requirements(staff.password)
                if message is None:
                    return None
                return message
            return message
        return message

    @staticmethod
    def is_email_and_phone_approved(staff):
        if staff is not None:
            message = StaffValidation.does_email_meet_requirements(staff.email)
            if message is None:
                message = StaffValidation.does_phone_number_meet_requirements(staff.phone_number)
                if message is None:
                    return None
                return message
            return message
        return "wfu"

    @staticmethod
    def does_user_name_meet_requirements(username):
        if username is not None:
            if username.strip():
                if 5 <= len(username) <= 30:
                    return None
                print("USERNAME USERNAME: ", username)
                return "uns"
            return "unb"
        return "une"

    @staticmethod
    def does_password_meet_requirements(password):
        if password is not None:
            if password.strip():
                if 5 <= len(password) <= 30:
                    return None
                return "uns"
            return "unb"
        return "une"

    @staticmethod
    def does_email_meet_requirements(email):
        if email is not None:
            if email.strip():
                if re.match(
                        r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
                        email):
                    return None
                return "epi"
            return "eb"
        return "ee"

    @staticmethod
    def does_phone_number_meet_requirements(phone_number):
        if phone_number is not None:
            if phone_number.strip():
                if re.match(r"^[0-9]{10}$", phone_number):
                    return None
                return "pnpi"
            return "pnb"
        return "pne"
