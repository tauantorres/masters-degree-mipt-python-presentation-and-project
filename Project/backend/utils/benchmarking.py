from typing import Self, Any, List, Dict


class BenchmarkResults:

    def __init__(self: Self, framework_name: str) -> None:
        self.framework_name = framework_name
        self.instantiation_times: List[float] = []
        self.serialization_times: List[float] = []
        self.deserialization_times: List[float] = []
        self.memory_usage: List[int] = []

    def add_instantiation_time(self: Self, time_elapsed: float) -> None:
        self.instantiation_times.append(time_elapsed)
        
    def add_serialization_time(self: Self, time_elapsed: float) -> None:
        self.serialization_times.append(time_elapsed)
        
    def add_deserialization_time(self: Self, time_elapsed: float) -> None:
        self.deserialization_times.append(time_elapsed)
        
    def add_memory_usage(self: Self, memory_bytes: int) -> None:
        self.memory_usage.append(memory_bytes)
    
    def get_avg_instantiation_time(self: Self) -> float:
        return sum(self.instantiation_times) / len(self.instantiation_times) if self.instantiation_times else 0.0

    def get_avg_serialization_time(self: Self) -> float:
        return sum(self.serialization_times) / len(self.serialization_times) if self.serialization_times else 0.0
        
    def get_avg_deserialization_time(self: Self) -> float:
        return sum(self.deserialization_times) / len(self.deserialization_times) if self.deserialization_times else 0.0
        
    def get_avg_memory_usage(self: Self) -> float:
        return sum(self.memory_usage) / len(self.memory_usage) if self.memory_usage else 0.0
        
    def to_dict(self: Self) -> Dict[str, Any]:
        return {
            'framework': self.framework_name,
            'avg_instantiation_time': self.get_avg_instantiation_time(),
            'avg_serialization_time': self.get_avg_serialization_time(),
            'avg_deserialization_time': self.get_avg_deserialization_time(),
            'avg_memory_usage': self.get_avg_memory_usage(),
            'total_operations': len(self.serialization_times)
        }
