import re
import oracledb

def get_connection():
    connection = oracledb.connect(
        user = "PRODN",
        password = "Prodn0123#",
        dsn = "localhost:1521/FREEPDB1"
    )
    return connection

def fetch_rules(field_code :str):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT RULE_TYPE, RULE_VALUE, ERROR_MESSAGE
        FROM VALIDATION_RULES
        WHERE FIELD_CODE = :fc"""
    
    cursor.execute(query, fc = field_code)
    rules = cursor.fetchall()
    cursor.close()
    conn.close()
    return rules

def validate_field(field_code :str, value : str):
    rules = fetch_rules(field_code)
    errors = []

    for rule_type, rule_value, error_message in rules:
        if rule_type == 'LENGTH':
            if (len(value) != int(rule_value)):
                errors.append(error_message)
            elif rule_type == 'REGEX':
                if not re.match(rule_value, value):
                    errors.append(error_message)
            elif rule_type == 'RANGE':
                min_val, max_val = map(int, rule_value.split(','))
                if not (min_val <= int(value) <= max_val):
                    errors.append(error_message)
    return errors or ["VALID"]

if __name__ == "__main__":
    print(validate_field("PAN", "ABCDE1234F"))   # VALID
    print(validate_field("PAN", "12345"))        # Invalid PAN format
    print(validate_field("ACCNUM", "123456"))    # Account number must be 12 digits