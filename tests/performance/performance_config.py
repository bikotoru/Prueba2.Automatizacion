PERFORMANCE_THRESHOLDS = {
    "login": {
        "p50": 500,
        "p95": 1500,
        "p99": 3000,
        "max_response_time": 5000,
        "min_success_rate": 95.0
    },
    "session": {
        "p50": 200,
        "p95": 500,
        "p99": 1000,
        "max_response_time": 2000,
        "min_success_rate": 99.0
    },
    "general": {
        "max_error_rate": 5.0,
        "min_throughput": 100,
        "max_cpu_usage": 80,
        "max_memory_usage": 75
    }
}

LOAD_TEST_SCENARIOS = {
    "smoke": {
        "users": 5,
        "spawn_rate": 1,
        "duration": "30s",
        "description": "Prueba básica de funcionalidad"
    },
    "load": {
        "users": 50,
        "spawn_rate": 5,
        "duration": "5m",
        "description": "Prueba de carga normal esperada"
    },
    "stress": {
        "users": 100,
        "spawn_rate": 10,
        "duration": "10m",
        "description": "Prueba de estrés del sistema"
    },
    "spike": {
        "users": 200,
        "spawn_rate": 50,
        "duration": "2m",
        "description": "Prueba de picos de tráfico"
    }
}

MONITORED_METRICS = [
    "response_time_percentiles",
    "requests_per_second",
    "error_rate",
    "concurrent_users",
    "cpu_usage",
    "memory_usage",
    "database_connections",
    "cache_hit_rate"
]