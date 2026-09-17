import re


def clean_phone_number(phone_number): 
    """Clean and normalize phone number format"""
    # Remove all non-digit characters
    cleaned = re.sub(r'\D', '', str(phone_number))
    
    # Handle international format (+234) -> local format (0)
    if cleaned.startswith('234'): 
        cleaned = '0' + cleaned[3:]
    elif cleaned.startswith('+234'): 
        cleaned = '0' + cleaned[4:]
    
    return cleaned

def validate_nigerian_number(cleaned_number): 
    """Validate if the number is a proper Nigerian mobile number"""
    if len(cleaned_number) != 11: 
        return False, "Number must be 11 digits"
    
    if not cleaned_number.startswith('0'): 
        return False, "Number must start with 0"
    
    if not cleaned_number.isdigit(): 
        return False, "Number must contain only digits"
    
    return True, "Valid"

def get_network_prefixes(): 
    """Get all network prefixes organized by provider"""
    return {
        'MTN': {
            'prefixes': ['0803', '0806', '0703', '0706', '0813', '0816', '0810', '0814', 
                        '0903', '0906', '0913', '0916', '07025', '07026', '0704'], 
            'color': '#ffcd00', 
            'description': 'Largest network in Nigeria'
        }, 
        'Glo': {
            'prefixes': ['0805', '0807', '0705', '0815', '0811', '0905', '0915'], 
            'color': '#228b22', 
            'description': 'Affordable data provider'
        }, 
        'Airtel': {
            'prefixes': ['0802', '0808', '0708', '0701', '0812', '0902', '0901', 
                         '0904', '0907', '0912'], 
            'color': '#e91e63', 
            'description': 'Quality network provider'
        }, 
        '9mobile': {
            'prefixes': ['0809', '0818', '0817', '0909', '0908'], 
            'color': '#0066cc', 
            'description': 'Former Etisalat network'
        }, 
        'Ntel': {
            'prefixes': ['0804'], 
            'color': '#9c27b0', 
            'description': '4G LTE provider'
        }, 
        'Smile': {
            'prefixes': ['0702'], 
            'color': '#ff9800', 
            'description': '4G broadband services'
        }
    }

def detect_nigerian_network(phone_number): 
    """
    Detects the network provider of a Nigerian telephone number.
    
    Args: 
        phone_number (str): The phone number to check
        
    Returns: 
        str: The network provider name or descriptive message
    """
    # Clean the phone number
    cleaned_number = clean_phone_number(phone_number)
    
    # Validate the number
    is_valid, message = validate_nigerian_number(cleaned_number)
    if not is_valid: 
        return f"Invalid Nigerian number format: {message}"
    
    # Extract the prefix (check 5-digit prefixes first, then 4-digit)
    networks = get_network_prefixes()
    
    # Try 5-digit prefixes first (like 07025, 07026)
    five_digit_prefix = cleaned_number[:5]
    for network, info in networks.items(): 
        if five_digit_prefix in info['prefixes']: 
            return network
    
    # Try 4-digit prefixes
    four_digit_prefix = cleaned_number[:4]
    for network, info in networks.items(): 
        if four_digit_prefix in info['prefixes']: 
            return network
    
    return "Unknown network"
