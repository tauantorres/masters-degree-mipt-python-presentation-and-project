import random
from typing import List, Dict, Any


class GeneratorUser:
    
    TAGS = [
        "user", 
        "admin", 
        "developer", 
        "tester",
    ]
    NAMES = [
        "Alice", 
        "Bob", 
        "Charlie", 
        "David", 
        "Eve", 
        "Frank",
        "Anne",
        "George",
        "Hannah",
        "James",
        "Claire",
        "Roger",
    ]
    EMAIL_DOMAINS = [
        "yahoo.com", 
        "gmail.com",  
        "email.com", 
        "mail.com",
    ]

    @staticmethod
    def generate_random_user(user_id: int) -> Dict[str, Any]:
        return {
            'id': user_id,
            'name': random.choice(GeneratorUser.NAMES),
            'email': f"{random.choice(GeneratorUser.NAMES).lower()}{user_id}@{random.choice(GeneratorUser.EMAIL_DOMAINS)}",
            'age': random.randint(18, 70),
            'is_active': random.choice([True, False]),
        }

class Generator:

    @staticmethod
    def generate_user(user_id: int) -> Dict[str, Any]:
        return GeneratorUser.generate_random_user(user_id=user_id)

def generate_users_batch(batch_size: int) -> List[Dict[str, Any]]:
    return [Generator.generate_user(user_id=i) for i in range(1, batch_size + 1)]
