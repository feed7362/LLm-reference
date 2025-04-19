import json
import re

from utils.logger import CustomLogger
logger = CustomLogger(__name__)

def sanitize_arguments(args: dict) -> dict:
    """Sanitize function arguments by cleaning regex escape sequences."""
    if 0 in args:
        args[0] = re.sub(r'\\([a-zA-Z]+)', r'\1', args[0])
    return args

def call_function(name: str, args: dict) -> str:
    """Call specific functions based on the provided function name."""
    logger.debug("Calling function: %s with args: %s", name, args)
    sanitized_args = sanitize_arguments(args)
    match name:
        case "CalculatorRequest":
            from agency.calculator import calculator, CalculatorRequest
            validated_request = CalculatorRequest(**sanitized_args)
            logger.debug("Validated request: %s", validated_request)
            return calculator(validated_request)
        case "DateTimeRequest":
            from agency.time_managment import datetime_now, DateTimeRequest
            validated_request = DateTimeRequest(**sanitized_args)
            logger.debug("Validated request: %s", validated_request)
            return datetime_now(validated_request)
        case "CodeExecutionRequest":
            from agency.code_execution import execute_code, CodeExecutionRequest
            validated_request = CodeExecutionRequest(**sanitized_args)
            logger.debug("Validated request: %s", validated_request)
            return execute_code(validated_request)
    logger.error("Unknown function name: %s", name)
    raise ValueError(f"Unknown function name: {name}")

def extract_function_outputs(response: dict) -> list[dict]:
    """Extract outputs from function tool calls in the response."""
    function_outputs = []
    for choice in response.get("choices", []):
        message = choice.get("message", {})
        tool_calls = message.get("tool_calls", [])
        for tool_call in tool_calls:
            if tool_call.get("type") != "function":
                continue
            func_name = tool_call["function"]["name"].rstrip(":")
            try:
                arguments = json.loads(tool_call["function"]["arguments"])
            except json.JSONDecodeError as json_error:
                logger.error("Failed to decode arguments for function %s: %s", func_name, json_error)
                continue
            result = call_function(func_name, arguments)
            function_outputs.append({
                "type": "function_call_output",
                "call_id": tool_call.get("id"),
                "output": str(result)
            })
    return function_outputs
