import random
from typing import List, Dict, Any


class GeneratorAddress:

    STREETS = [
        "Main St", 
        "High St", 
        "Broadway", 
        "Elm St", 
        "Maple Ave",
        "Main Avenue",
        "Oak Street",
        "Pine Lane",
        "Longwood Drive",
    ]
    CITIES = [
        "London", 
        "Porto Alegre", 
        "Moscow", 
        "Bologna", 
        "Buenos Aires", 
        "Rio de Janeiro",
        "New York",
        "São Paulo",
        "Tokyo",
        "Berlin",
        "Rome",
        "Madrid",
        "Paris",
        "Barcelona",
        "Lisbon",
        "Vienna",
        "Prague",
        "Budapest",
        "Warsaw",
        "Dublin",
    ]

    @staticmethod
    def generate_random_address() -> Dict[str, Any]:
        return {
            'street': random.choice(GeneratorAddress.STREETS),
            'city': random.choice(GeneratorAddress.CITIES),
            'postal_code': f"{random.randint(10000, 99999)}"
        }

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
    def generate_random_user(user_id: int, add_addres: bool = False) -> Dict[str, Any]:
        
        user_base_data = {
            'id': user_id,
            'name': random.choice(GeneratorUser.NAMES),
            'email': f"{random.choice(GeneratorUser.NAMES).lower()}{user_id}@{random.choice(GeneratorUser.EMAIL_DOMAINS)}",
            'age': random.randint(18, 70),
            'is_active': random.choice([True, False]),
        }

        if add_addres:
            user_base_data.update({
                'address': GeneratorAddress.generate_random_address(),
                'tags': random.sample(GeneratorUser.TAGS, k=random.randint(1, len(GeneratorUser.TAGS))),
            })

        return user_base_data

class Generator:

    @staticmethod
    def generate_user(user_id: int, add_address: bool = False) -> Dict[str, Any]:
        return GeneratorUser.generate_random_user(user_id=user_id, add_addres=add_address)


def generate_users_batch(batch_size: int, add_address: bool = False) -> List[Dict[str, Any]]:
    return [Generator.generate_user(user_id=i, add_address=add_address) for i in range(1, batch_size + 1)]

