import logging
import asyncio
from copy import deepcopy
from typing import List, Dict, Any, Callable
from fastapi import Query, APIRouter, HTTPException

from models.dataclass_model import instantiate_dataclass, encode_dataclass, decode_dataclass, measure_dataclass_size
from models.pydantic_model import instantiate_pydantic, encode_pydantic, decode_pydantic, measure_pydantic_size
from models.msgspec_model import instantiate_msgspec, encode_msgspec, decode_msgspec, measure_msgspec_size
from utils.data_generator import generate_users_batch
from utils.benchmarking import BenchmarkResults


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/benchmark",
    tags=["Benchmarks"],
)


async def benchmark(
        data: List[dict],
        results: BenchmarkResults,
        function_encode: Callable,
        function_decode: Callable,
        function_instantiate: Callable,
        function_measure_size: Callable,
) -> None:
    
    import time
    # Instantiate
    start_time = time.perf_counter()
    instances = [function_instantiate(user_data) for user_data in data]
    instantiation_time = time.perf_counter() - start_time
    results.add_instantiation_time(instantiation_time)

    # Serialize
    start_time = time.perf_counter()
    serialized = [function_encode(instance) for instance in instances]
    serialization_time = time.perf_counter() - start_time
    results.add_serialization_time(serialization_time)

    # Deserialize
    start_time = time.perf_counter()
    _ = [function_decode(item) for item in serialized]
    deserialization_time = time.perf_counter() - start_time
    results.add_deserialization_time(deserialization_time)

    # Measure size
    total_size = sum(function_measure_size(instance) for instance in instances)
    results.add_memory_usage(total_size)

@router.post(path="/run", response_model=Dict[str, Any])
async def run_banchmark(
    batch_size: int = Query(default=1_000, ge=1, le=100_000, description="Number of objects to benchmark"),
    iterations: int = Query(default=10, ge=1, le=20, description="Number of iterations for averaging")
) -> Dict[str, Any]:

    try:
        # 1. Generate base data:
        raw_data = generate_users_batch(batch_size=batch_size)

        # 2. Initialize results storage:
        results = {
            'dataclass': BenchmarkResults('dataclass'),
            'pydantic': BenchmarkResults('pydantic'),
            'msgspec': BenchmarkResults('msgspec'),
        }

        # 3. Run benchmarks for each iteration:
        for iteration in range(iterations):
            logger.info(f"Starting iteration {iteration + 1}/{iterations}")

            # Create fresh copies of data for each framework to avoid cross-contamination
            dataclass_data = deepcopy(raw_data)
            pydantic_data = deepcopy(raw_data)
            msgspec_data = deepcopy(raw_data)

            # Benchmarking
            await benchmark(
                data=dataclass_data,
                results=results['dataclass'],
                function_encode=encode_dataclass,
                function_decode=decode_dataclass,
                function_instantiate=instantiate_dataclass,
                function_measure_size=measure_dataclass_size
            )

            await benchmark(
                data=pydantic_data,
                results=results['pydantic'],
                function_encode=encode_pydantic,
                function_decode=decode_pydantic,
                function_instantiate=instantiate_pydantic,
                function_measure_size=measure_pydantic_size
            )

            await benchmark(
                data=msgspec_data,
                results=results['msgspec'],
                function_encode=encode_msgspec,
                function_decode=decode_msgspec,
                function_instantiate=instantiate_msgspec,
                function_measure_size=measure_msgspec_size
            )

        # 4. Compile final results:
        benchmark_response = {
            'parameters': {
                'batch_size': batch_size,
                'iterations': iterations,
            },
            'results': {
                framework: results[framework].to_dict()
                for framework, result in results.items()
            },
            'summary': {
                'fastest_instantiation': min(results.items(), key=lambda item: item[1].get_avg_instantiation_time())[0],
                'fastest_serialization': min(results.items(), key=lambda item: item[1].get_avg_serialization_time())[0],
                'fastest_deserialization': min(results.items(), key=lambda item: item[1].get_avg_deserialization_time())[0],
                'lowest_memory_usage': min(results.items(), key=lambda item: item[1].get_avg_memory_usage())[0],
            }
        }

        return benchmark_response

    except Exception as e:
        logger.error(f"Benchmarking failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Benchmarking process failed: {str(e)}",
        )

@router.post(path="/run-parallel", response_model=Dict[str, Any])
async def run_banchmark(
    batch_size: int = Query(default=1_000, ge=1, le=100_000, description="Number of objects to benchmark"),
    iterations: int = Query(default=10, ge=1, le=20, description="Number of iterations for averaging")
) -> Dict[str, Any]:

    try:
        # 1. Generate base data:
        raw_data = generate_users_batch(batch_size=batch_size)

        # 2. Initialize results storage:
        results = {
            'dataclass': BenchmarkResults('dataclass'),
            'pydantic': BenchmarkResults('pydantic'),
            'msgspec': BenchmarkResults('msgspec'),
        }

        # 3. Run benchmarks for each iteration:
        for iteration in range(iterations):
            logger.info(f"Starting iteration {iteration + 1}/{iterations}")

            # Create fresh copies of data for each framework to avoid cross-contamination
            dataclass_data = deepcopy(raw_data)
            pydantic_data = deepcopy(raw_data)
            msgspec_data = deepcopy(raw_data)

            # Benchmarking
            await asyncio.gather(
                benchmark(
                    data=dataclass_data,
                    results=results['dataclass'],
                    function_encode=encode_dataclass,
                    function_decode=decode_dataclass,
                    function_instantiate=instantiate_dataclass,
                    function_measure_size=measure_dataclass_size,
                ),
                benchmark(
                    data=pydantic_data,
                    results=results['pydantic'],
                    function_encode=encode_pydantic,
                    function_decode=decode_pydantic,
                    function_instantiate=instantiate_pydantic,
                    function_measure_size=measure_pydantic_size,
                ),
                benchmark(
                    data=msgspec_data,
                    results=results['msgspec'],
                    function_encode=encode_msgspec,
                    function_decode=decode_msgspec,
                    function_instantiate=instantiate_msgspec,
                    function_measure_size=measure_msgspec_size,
                ),
            )

            logger.info(f"Completed iteration {iteration + 1}/{iterations}")

        # 4. Compile final results:
        benchmark_response = {
            'parameters': {
                'batch_size': batch_size,
                'iterations': iterations,
            },
            'results': {
                framework: results[framework].to_dict()
                for framework, result in results.items()
            },
            'summary': {
                'fastest_instantiation': min(results.items(), key=lambda item: item[1].get_avg_instantiation_time())[0],
                'fastest_serialization': min(results.items(), key=lambda item: item[1].get_avg_serialization_time())[0],
                'fastest_deserialization': min(results.items(), key=lambda item: item[1].get_avg_deserialization_time())[0],
                'lowest_memory_usage': min(results.items(), key=lambda item: item[1].get_avg_memory_usage())[0],
            }
        }

        return benchmark_response

    except Exception as e:
        logger.error(f"Benchmarking failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Benchmarking process failed: {str(e)}",
        )
 
@router.get(path="/quick", response_model=Dict[str, Any])
async def run_quick_benchmark() -> Dict[str, Any]:
    return await run_banchmark(batch_size=100, iterations=5)

@router.get(path="/frameworks", response_model=List[Dict[str, Any]])
async def get_available_frameworks() -> List[Dict[str, Any]]:
    return [
        {
            "name": "dataclass",
            "description": "Python standard library dataclasses",
            "version": "3.7+",
            "features": ["Type hints", "Automatic methods", "Immutability option"]
        },
        {
            "name": "pydantic",
            "description": "Data validation using Python type annotations",
            "version": "2.x",
            "features": ["Validation", "JSON Schema", "FastAPI integration"]
        },
        {
            "name": "msgspec",
            "description": "Fast serialization and validation library",
            "version": "0.18+",
            "features": ["High performance", "Multiple formats", "Schema validation"]
        },
        {
            "name": "dict",
            "description": "Native Python dictionaries (baseline)",
            "version": "All",
            "features": ["No dependencies", "Universal compatibility", "Baseline performance"]
        }
    ]
